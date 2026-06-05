"""
HWP / HWPX → Markdown converter (lightweight fallback path)
한글(HWP/HWPX) → 마크다운 변환기 (경량 폴백 경로)

This module provides a *self-contained, low-dependency* path for turning Korean
Hangul word-processor documents into Markdown so they can flow through the rest
of the RAG pipeline. It deliberately favors portability over perfect fidelity:

* ``.hwpx`` (OWPML) is a zip of XML and is parsed with **the standard library
  only** (:mod:`zipfile` + :mod:`xml.etree.ElementTree`). No lxml, no external
  tools — it works on a clean Python 3.10+ install.
* ``.hwp`` (the older HWP v5 OLE/CFBF binary) is *not* something the stdlib can
  decode on its own. We lazily invoke the optional ``pyhwp`` package (which
  ships the ``hwp5`` Python package plus the ``hwp5html`` / ``hwp5txt`` CLIs).
  When ``pyhwp`` is absent we raise a clear, actionable error instead of failing
  obscurely.

이 모듈은 한글 문서를 마크다운으로 바꾸는 *경량* 경로입니다. 이식성을 우선해
``.hwpx``는 표준 라이브러리만으로 파싱하고, ``.hwp``(구형 OLE 바이너리)는 선택
의존성 ``pyhwp``를 지연 호출합니다. ``pyhwp``가 없으면 설치 안내가 포함된 명확한
오류를 발생시킵니다.

High-fidelity conversion (고품질 변환) — using LibreOffice to render HWP → PDF and
then MinerU for layout-aware extraction — is intentionally **out of scope** here
and is handled by a separate, heavier path. This module is the lightweight
fallback that runs anywhere.

Optional install (선택 설치)::

    pip install pyhwp

Whether the ``hwp5`` package (pyhwp) is importable is exposed as the module-level
boolean :data:`PYHWP_AVAILABLE` so callers can branch on it.
"""

from __future__ import annotations

import logging
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Union

__all__ = [
    "HWP_EXTENSIONS",
    "PYHWP_AVAILABLE",
    "HwpConversionError",
    "detect_hwp_format",
    "is_hwp_file",
    "convert_hwp_to_markdown",
    "convert_hwp_to_text",
]

logger = logging.getLogger(__name__)

#: File extensions handled by this module.
HWP_EXTENSIONS: tuple = (".hwp", ".hwpx")

# OLE / CFBF (Compound File Binary Format) magic — the signature of HWP v5
# binary documents (and other Microsoft compound files).
_OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
# ZIP local-file-header magic ("PK\x03\x04") — HWPX is a zip container.
_ZIP_MAGIC = b"PK\x03\x04"
# The mimetype recorded by an OWPML (.hwpx) package.
_HWPX_MIMETYPE = "application/hwp+zip"
# OWPML paragraph namespace (informational; we strip namespaces generically).
OWPML_PARAGRAPH_NS = "http://www.hancom.co.kr/hwpml/2011/paragraph"


# ── Optional dependency detection ────────────────────────────────
# Probe for the ``hwp5`` package (shipped by pyhwp) at import time only to set
# the public flag. We never construct anything here, so import stays cheap and
# side-effect free; the real backend is invoked lazily in the .hwp path.
try:  # pragma: no cover - depends on environment
    import hwp5 as _hwp5  # noqa: F401

    PYHWP_AVAILABLE = True
except Exception:  # ImportError, or any failure importing the package
    PYHWP_AVAILABLE = False


class HwpConversionError(Exception):
    """Raised when an HWP/HWPX document cannot be converted to Markdown.

    The message is intended to be actionable — for example, when the optional
    ``pyhwp`` backend is required but not installed it tells the user exactly
    how to install it (``pip install pyhwp``).
    """


# ── Format detection ─────────────────────────────────────────────
def detect_hwp_format(file_path: Union[str, Path]) -> str:
    """Detect whether ``file_path`` is an HWP v5 binary or an HWPX package.

    Returns ``"hwp"`` for the OLE/CFBF binary (magic bytes
    ``D0 CF 11 E0 A1 B1 1A E1``) or ``"hwpx"`` for the OWPML zip (a PK zip whose
    ``mimetype`` entry is ``application/hwp+zip``, or that contains
    ``Contents/section0.xml``).

    Raises:
        ValueError: if the file is neither an HWP nor an HWPX document.
    """
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File does not exist: {path}")

    with open(path, "rb") as fh:
        header = fh.read(8)

    if header == _OLE_MAGIC:
        return "hwp"

    if header[:4] == _ZIP_MAGIC:
        # Confirm it is specifically an OWPML/HWPX package rather than some
        # other zip (docx, jar, plain .zip, ...).
        try:
            with zipfile.ZipFile(path) as zf:
                names = set(zf.namelist())
                if "mimetype" in names:
                    try:
                        mimetype = zf.read("mimetype").decode("ascii", "ignore").strip()
                    except Exception:
                        mimetype = ""
                    if mimetype == _HWPX_MIMETYPE:
                        return "hwpx"
                # Some packages omit/garble the mimetype entry; fall back to the
                # presence of the canonical body section.
                if any(
                    n == "Contents/section0.xml" or n.endswith("/section0.xml")
                    for n in names
                ):
                    return "hwpx"
        except zipfile.BadZipFile:
            pass

    raise ValueError(
        f"Not an HWP/HWPX document (unrecognized signature): {path.name}"
    )


def is_hwp_file(file_path: Union[str, Path]) -> bool:
    """Return ``True`` if ``file_path`` looks like an HWP/HWPX document.

    The check is permissive: a recognized extension is enough, and otherwise we
    fall back to content sniffing via :func:`detect_hwp_format`. Any error during
    sniffing (missing file, unreadable, unknown signature) yields ``False``
    rather than raising.
    """
    path = Path(file_path)
    if path.suffix.lower() in HWP_EXTENSIONS:
        return True
    try:
        detect_hwp_format(path)
        return True
    except Exception:
        return False


# ── HWPX (OWPML) parsing — stdlib only ───────────────────────────
def _local_name(tag: str) -> str:
    """Strip an XML namespace from a tag/attribute name.

    ElementTree expands namespaced tags to ``{uri}local``; OWPML also uses a
    handful of prefixes. We match on the bare local name so the parser stays
    robust to namespace-URI drift across HWPX versions.
    """
    if not tag:
        return ""
    # ElementTree form: "{namespace}local"
    if "}" in tag:
        tag = tag.rsplit("}", 1)[1]
    # Prefixed form (rare after ET expansion): "hp:local"
    if ":" in tag:
        tag = tag.rsplit(":", 1)[1]
    return tag


def _iter_section_names(zf: zipfile.ZipFile) -> List[str]:
    """Return the body section XML entries in reading order.

    OWPML stores the document body as ``Contents/section0.xml``,
    ``Contents/section1.xml`` … We sort numerically so section 10 follows
    section 9 rather than section 1.
    """
    sections = [
        n
        for n in zf.namelist()
        if "section" in n.lower()
        and n.lower().endswith(".xml")
        and "/section" in ("/" + n).lower()
    ]

    def _key(name: str) -> tuple:
        stem = Path(name).stem  # e.g. "section3"
        digits = "".join(ch for ch in stem if ch.isdigit())
        return (int(digits) if digits else 0, name)

    return sorted(sections, key=_key)


def _collect_text(node: ET.Element, parts: List[str]) -> None:
    """Recursively gather text from ``node`` without descending into tables.

    A paragraph may *contain* a nested table; that table's cell text is rendered
    separately as a markdown table, so we must not also fold it into the
    paragraph's own text (which would duplicate the content). We therefore skip
    any subtree rooted at a ``<hp:tbl>``.
    """
    for child in node:
        name = _local_name(child.tag)
        if name == "tbl":
            continue  # rendered separately as a markdown table
        if name == "t":
            if child.text:
                parts.append(child.text)
            for inner in child:
                if inner.tail:
                    parts.append(inner.tail)
        elif name in ("lineBreak", "linebreak"):
            parts.append("\n")
        else:
            _collect_text(child, parts)


def _paragraph_text(para: ET.Element) -> str:
    """Collect the visible text of a single OWPML paragraph element.

    Text lives in ``<hp:t>`` runs; line breaks are represented by ``<hp:lineBreak>``
    (and the legacy ``<hp:lineseg>`` boundaries). We concatenate the run text in
    document order so reading order is preserved. Nested tables are skipped here
    because they are emitted separately as markdown tables.
    """
    parts: List[str] = []
    # Include text directly on the paragraph element, then walk its children.
    if para.text:
        parts.append(para.text)
    _collect_text(para, parts)
    return "".join(parts).strip()


def _cell_text(cell: ET.Element) -> str:
    """Extract the text of a table cell (``<hp:tc>``), joining its paragraphs."""
    lines = []
    for para in cell.iter():
        if _local_name(para.tag) == "p":
            text = _paragraph_text(para)
            if text:
                lines.append(text)
    cell_text = " ".join(lines).strip()
    # Markdown table cells cannot contain raw pipes/newlines.
    return cell_text.replace("|", "\\|").replace("\n", " ")


def _table_to_markdown(tbl: ET.Element) -> List[str]:
    """Convert an OWPML table (``<hp:tbl>``) to GitHub-flavored markdown rows.

    Returns a list of markdown lines (header + separator + body). Falls back to
    an empty list when the table has no extractable rows.
    """
    rows: List[List[str]] = []
    for tr in tbl.iter():
        if _local_name(tr.tag) != "tr":
            continue
        cells = [
            _cell_text(tc) for tc in tr if _local_name(tc.tag) == "tc"
        ]
        if cells:
            rows.append(cells)

    if not rows:
        return []

    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]

    lines: List[str] = []
    header = rows[0]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def _section_to_markdown(root: ET.Element) -> List[str]:
    """Render a parsed OWPML section tree to markdown blocks.

    We walk the *direct* paragraph/table structure of the section in order.
    Tables are emitted as markdown tables; every other top-level paragraph
    becomes a markdown line. Reading order is preserved by iterating the tree in
    document order and skipping the paragraphs that live *inside* a table (those
    are consumed by the table renderer).
    """
    blocks: List[str] = []

    # Paragraphs that belong to a table are rendered by the table itself; track
    # them so we do not also emit them as standalone lines.
    table_paragraphs = set()
    for tbl in root.iter():
        if _local_name(tbl.tag) == "tbl":
            for p in tbl.iter():
                if _local_name(p.tag) == "p":
                    table_paragraphs.add(id(p))

    handled_tables = set()
    for node in root.iter():
        name = _local_name(node.tag)
        if name == "tbl":
            if id(node) in handled_tables:
                continue
            handled_tables.add(id(node))
            table_md = _table_to_markdown(node)
            if table_md:
                blocks.append("\n".join(table_md))
        elif name == "p":
            if id(node) in table_paragraphs:
                continue
            text = _paragraph_text(node)
            if text:
                blocks.append(text)
    return blocks


def _convert_hwpx(path: Path) -> str:
    """Convert an HWPX (OWPML) file to a markdown string using only the stdlib."""
    blocks: List[str] = []
    try:
        with zipfile.ZipFile(path) as zf:
            section_names = _iter_section_names(zf)
            if not section_names:
                raise HwpConversionError(
                    f"No body sections (Contents/section*.xml) found in {path.name}"
                )
            for name in section_names:
                try:
                    data = zf.read(name)
                    root = ET.fromstring(data)
                except (ET.ParseError, KeyError) as exc:
                    logger.warning("Skipping unparseable HWPX section %s: %s", name, exc)
                    continue
                blocks.extend(_section_to_markdown(root))
    except zipfile.BadZipFile as exc:
        raise HwpConversionError(
            f"HWPX file is not a valid zip archive: {path.name}"
        ) from exc

    return "\n\n".join(b for b in blocks if b.strip()).strip() + "\n"


# ── HWP (v5 binary) parsing — optional pyhwp backend ─────────────
class _HtmlToMarkdown(HTMLParser):
    """A tiny, dependency-free HTML→Markdown converter for hwp5html output.

    It is intentionally minimal: it handles paragraphs, headings, line breaks,
    and tables (mapping ``<table>/<tr>/<td|th>`` to GitHub markdown tables),
    which covers the structures ``hwp5html`` emits for HWP body text. Anything
    else degrades to plain text.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._out: List[str] = []
        self._buf: List[str] = []
        self._in_table = False
        self._rows: List[List[str]] = []
        self._cur_row: List[str] = []
        self._cell: List[str] = []
        self._in_cell = False
        self._heading_level = 0

    # -- helpers -------------------------------------------------
    def _flush_paragraph(self) -> None:
        text = "".join(self._buf).strip()
        self._buf = []
        if not text:
            return
        if self._heading_level:
            self._out.append("#" * self._heading_level + " " + text)
        else:
            self._out.append(text)

    # -- parser callbacks ---------------------------------------
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "table":
            self._flush_paragraph()
            self._in_table = True
            self._rows = []
        elif tag == "tr" and self._in_table:
            self._cur_row = []
        elif tag in ("td", "th") and self._in_table:
            self._in_cell = True
            self._cell = []
        elif tag in ("br",):
            self._buf.append("\n")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush_paragraph()
            self._heading_level = int(tag[1])

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "table" and self._in_table:
            self._emit_table()
            self._in_table = False
        elif tag == "tr" and self._in_table:
            if self._cur_row:
                self._rows.append(self._cur_row)
            self._cur_row = []
        elif tag in ("td", "th") and self._in_table:
            cell = "".join(self._cell).strip().replace("|", "\\|").replace("\n", " ")
            self._cur_row.append(cell)
            self._in_cell = False
            self._cell = []
        elif tag in ("p", "div"):
            self._flush_paragraph()
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush_paragraph()
            self._heading_level = 0

    def handle_data(self, data):
        if self._in_cell:
            self._cell.append(data)
        else:
            self._buf.append(data)

    def _emit_table(self) -> None:
        if not self._rows:
            return
        width = max(len(r) for r in self._rows)
        rows = [r + [""] * (width - len(r)) for r in self._rows]
        lines = ["| " + " | ".join(rows[0]) + " |"]
        lines.append("| " + " | ".join(["---"] * width) + " |")
        for row in rows[1:]:
            lines.append("| " + " | ".join(row) + " |")
        self._out.append("\n".join(lines))
        self._rows = []

    def to_markdown(self) -> str:
        self._flush_paragraph()
        return "\n\n".join(b for b in self._out if b.strip()).strip() + "\n"


def _missing_pyhwp_error(file_name: str) -> HwpConversionError:
    return HwpConversionError(
        f"Converting the legacy HWP v5 binary '{file_name}' requires the optional "
        "'pyhwp' backend, which is not installed.\n"
        "Install it with:\n\n    pip install pyhwp\n\n"
        "pyhwp provides the 'hwp5' package and the 'hwp5html'/'hwp5txt' commands "
        "used to extract HWP content. (HWPX '.hwpx' files do not need pyhwp.)"
    )


def _convert_hwp_binary(path: Path) -> str:
    """Convert a legacy HWP v5 binary to markdown via the optional pyhwp backend.

    Strategy: prefer ``hwp5html`` (preserves tables) and feed its HTML through
    :class:`_HtmlToMarkdown`. If that fails, fall back to ``hwp5txt`` (plain
    text). Raises :class:`HwpConversionError` with install guidance if pyhwp is
    unavailable, or on any conversion failure.
    """
    if not PYHWP_AVAILABLE:
        raise _missing_pyhwp_error(path.name)

    # --- richer path: hwp5html → HTML → markdown ---------------
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            result = subprocess.run(
                ["hwp5html", "--output", str(tmp_dir), str(path)],
                capture_output=True,
                text=True,
                timeout=120,
                encoding="utf-8",
                errors="ignore",
            )
            if result.returncode == 0:
                html_files = list(tmp_dir.glob("*.html")) + list(
                    tmp_dir.glob("**/*.xhtml")
                )
                # hwp5html commonly writes "index.xhtml".
                html_files += list(tmp_dir.glob("**/*.html"))
                html_files = sorted(set(html_files))
                if html_files:
                    html = ""
                    for hf in html_files:
                        try:
                            html += hf.read_text(encoding="utf-8", errors="ignore")
                        except Exception:
                            continue
                    parser = _HtmlToMarkdown()
                    parser.feed(html)
                    markdown = parser.to_markdown()
                    if markdown.strip():
                        return markdown
            else:
                logger.warning(
                    "hwp5html failed for %s: %s", path.name, result.stderr.strip()
                )
    except FileNotFoundError:
        logger.debug("hwp5html CLI not found; falling back to hwp5txt")
    except subprocess.TimeoutExpired:
        logger.warning("hwp5html timed out for %s", path.name)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("hwp5html conversion error for %s: %s", path.name, exc)

    # --- fallback: hwp5txt → plain text ------------------------
    text = _hwp_binary_to_text(path)
    if text.strip():
        # Map non-empty lines to markdown paragraphs.
        lines = [ln.strip() for ln in text.splitlines()]
        blocks = [ln for ln in lines if ln]
        return "\n\n".join(blocks).strip() + "\n"

    raise HwpConversionError(
        f"Failed to extract any content from HWP binary '{path.name}' via pyhwp."
    )


def _hwp_binary_to_text(path: Path) -> str:
    """Extract plain text from an HWP v5 binary using ``hwp5txt`` (pyhwp)."""
    if not PYHWP_AVAILABLE:
        raise _missing_pyhwp_error(path.name)
    try:
        result = subprocess.run(
            ["hwp5txt", str(path)],
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8",
            errors="ignore",
        )
    except FileNotFoundError as exc:
        raise HwpConversionError(
            "The 'hwp5txt' command (from pyhwp) was not found on PATH even though "
            "the 'hwp5' package is importable. Reinstall with: pip install pyhwp"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise HwpConversionError(
            f"hwp5txt timed out while converting '{path.name}'."
        ) from exc

    if result.returncode != 0:
        raise HwpConversionError(
            f"hwp5txt failed for '{path.name}': {result.stderr.strip()}"
        )
    return result.stdout


# ── Public entry points ──────────────────────────────────────────
def convert_hwp_to_text(file_path: Union[str, Path]) -> str:
    """Convert an HWP/HWPX document to a plain-text string.

    For ``.hwpx`` this strips markdown table formatting down to readable lines;
    for ``.hwp`` it uses the ``hwp5txt`` backend. Raises
    :class:`HwpConversionError` on failure (including missing pyhwp for ``.hwp``).
    """
    path = Path(file_path).resolve()
    fmt = detect_hwp_format(path)
    if fmt == "hwpx":
        # Reuse the structured parse, then drop markdown table syntax.
        markdown = _convert_hwpx(path)
        lines = []
        for line in markdown.splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and set(stripped) <= set("| -"):
                continue  # skip table separator rows
            lines.append(line)
        return "\n".join(lines).strip() + "\n"
    return _hwp_binary_to_text(path)


def convert_hwp_to_markdown(
    file_path: Union[str, Path], output_dir: Optional[Union[str, Path]] = None
) -> str:
    """Convert an HWP/HWPX document to Markdown and write a ``<stem>.md`` file.

    Args:
        file_path: Path to the ``.hwp`` or ``.hwpx`` document.
        output_dir: Directory to write the ``.md`` file into. If ``None``, a
            sibling ``hwp_output`` directory next to the source is used (mirroring
            how :mod:`raganything.parser` derives output directories); if the
            source location is not writable, a system temp directory is used.

    Returns:
        The absolute path (as ``str``) to the written ``.md`` file.

    Raises:
        HwpConversionError: on any conversion failure, or when the optional
            ``pyhwp`` backend is required (``.hwp``) but not installed.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        raise HwpConversionError(f"Input file does not exist: {path}")

    try:
        fmt = detect_hwp_format(path)
    except ValueError as exc:
        raise HwpConversionError(str(exc)) from exc

    logger.info("Converting %s (detected format: %s) to markdown", path.name, fmt)

    if fmt == "hwpx":
        markdown = _convert_hwpx(path)
    else:  # "hwp"
        markdown = _convert_hwp_binary(path)

    # Determine and create the output directory.
    if output_dir is not None:
        base_output_dir = Path(output_dir)
    else:
        base_output_dir = path.parent / "hwp_output"

    try:
        base_output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        base_output_dir = Path(tempfile.mkdtemp(prefix="hwp_output_"))

    out_path = (base_output_dir / f"{path.stem}.md").resolve()
    try:
        out_path.write_text(markdown, encoding="utf-8")
    except OSError as exc:
        raise HwpConversionError(
            f"Failed to write markdown output to {out_path}: {exc}"
        ) from exc

    logger.info("Wrote markdown: %s (%d chars)", out_path, len(markdown))
    return str(out_path)
