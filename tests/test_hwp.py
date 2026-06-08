"""Tests for the HWP/HWPX/HWPML → Markdown converter.

These tests are stdlib-only and must pass *without* pyhwp, kordoc, or even
pytest installed. The HWPX fixture is built in-process with :mod:`zipfile`, the
HWP path is exercised only for its missing-backend error behavior (skipped if
pyhwp happens to be available), and the kordoc CLI integration is exercised with
tiny shell-script fakes pointed at by ``$KORDOC_CMD``.

The module under test is loaded standalone with :mod:`importlib` so that
importing the ``raganything`` package (which pulls in heavy, possibly-missing
dependencies) is never required just to test ``hwp.py``. The file also doubles
as a plain script: run ``python3 tests/test_hwp.py`` and every test function is
collected and executed.
"""

from __future__ import annotations

import importlib.util
import os
import stat
import tempfile
import zipfile
from pathlib import Path

# ── pytest shim ──────────────────────────────────────────────────
# Real pytest is preferred when present, but the test box has none, so fall back
# to a tiny stand-in exposing just the two helpers used here (``raises`` and
# ``skip``). Both behaviors stay identical under either runner.
try:  # pragma: no cover - depends on environment
    import pytest
except ImportError:  # pragma: no cover - exercised on the bare test box

    class _Skipped(Exception):
        """Raised by the shimmed ``pytest.skip`` to abort a test as skipped."""

    class _Raises:
        def __init__(self, expected):
            self.expected = expected

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            if exc_type is None:
                raise AssertionError(
                    f"DID NOT RAISE {getattr(self.expected, '__name__', self.expected)}"
                )
            return issubclass(exc_type, self.expected)

    class _PytestShim:
        Skipped = _Skipped

        @staticmethod
        def raises(expected):
            return _Raises(expected)

        @staticmethod
        def skip(reason=""):
            raise _Skipped(reason)

    pytest = _PytestShim()  # type: ignore[assignment]


# ── load hwp.py standalone (no raganything package import) ────────
_HWP_PATH = Path(__file__).resolve().parent.parent / "raganything" / "hwp.py"
_spec = importlib.util.spec_from_file_location("_raganything_hwp_under_test", _HWP_PATH)
assert _spec is not None and _spec.loader is not None
hwp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hwp)

HWP_EXTENSIONS = hwp.HWP_EXTENSIONS
PYHWP_AVAILABLE = hwp.PYHWP_AVAILABLE
KORDOC_AVAILABLE = hwp.KORDOC_AVAILABLE
HwpConversionError = hwp.HwpConversionError
_KordocUnavailable = hwp._KordocUnavailable
convert_hwp_to_markdown = hwp.convert_hwp_to_markdown
convert_hwp_to_text = hwp.convert_hwp_to_text
detect_hwp_format = hwp.detect_hwp_format
is_hwp_file = hwp.is_hwp_file
resolve_kordoc_command = hwp.resolve_kordoc_command
_kordoc_timeout = hwp._kordoc_timeout
_convert_with_kordoc = hwp._convert_with_kordoc
_markdown_to_text = hwp._markdown_to_text

# Magic bytes for the OLE/CFBF (HWP v5 binary) container.
_OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

# A minimal but valid OWPML section: two text runs + a 2x2 table, all under the
# HWPML 2011 paragraph namespace.
_SECTION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section"
        xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">
  <hp:p>
    <hp:run><hp:t>안녕하세요 서울연치과입니다</hp:t></hp:run>
  </hp:p>
  <hp:p>
    <hp:run><hp:t>임플란트 진료 안내</hp:t></hp:run>
  </hp:p>
  <hp:p>
    <hp:run>
      <hp:tbl>
        <hp:tr>
          <hp:tc><hp:subList><hp:p><hp:run><hp:t>항목</hp:t></hp:run></hp:p></hp:subList></hp:tc>
          <hp:tc><hp:subList><hp:p><hp:run><hp:t>비용</hp:t></hp:run></hp:p></hp:subList></hp:tc>
        </hp:tr>
        <hp:tr>
          <hp:tc><hp:subList><hp:p><hp:run><hp:t>임플란트</hp:t></hp:run></hp:p></hp:subList></hp:tc>
          <hp:tc><hp:subList><hp:p><hp:run><hp:t>문의</hp:t></hp:run></hp:p></hp:subList></hp:tc>
        </hp:tr>
      </hp:tbl>
    </hp:run>
  </hp:p>
</hs:sec>
"""

# Kordoc-related environment variables that the tests mutate; saved/restored
# wholesale by :func:`_clean_kordoc_env` so no test leaks state into another.
_KORDOC_ENV_VARS = (
    "KORDOC_CMD",
    "KO_RAG_DISABLE_KORDOC",
    "KO_RAG_KORDOC_AUTO_INSTALL",
    "KO_RAG_KORDOC_TIMEOUT",
)


def _make_hwpx(directory: Path) -> Path:
    """Build a minimal valid .hwpx package and return its path."""
    hwpx_path = directory / "sample.hwpx"
    with zipfile.ZipFile(hwpx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # The mimetype is conventionally stored first and uncompressed.
        zf.writestr("mimetype", "application/hwp+zip")
        zf.writestr("Contents/section0.xml", _SECTION_XML)
    return hwpx_path


def _snapshot_kordoc_env() -> dict:
    """Capture the current values of the kordoc env vars for later restore."""
    return {name: os.environ.get(name) for name in _KORDOC_ENV_VARS}


def _restore_env(snapshot: dict) -> None:
    """Restore env vars to a snapshot taken by :func:`_snapshot_kordoc_env`."""
    for name, value in snapshot.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value


def _clear_kordoc_env() -> None:
    """Remove every kordoc-related env var so a test starts from a clean slate."""
    for name in _KORDOC_ENV_VARS:
        os.environ.pop(name, None)


def _write_fake_kordoc(directory: Path, body: str) -> Path:
    """Write an executable POSIX shell-script fake kordoc and return its path.

    ``body`` is the script body (after the shebang). The caller is responsible
    for guarding on ``os.name == 'posix'`` before invoking the result.
    """
    script = directory / "fake_kordoc.sh"
    script.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    mode = script.stat().st_mode
    script.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return script


# ── existing lightweight-backend tests ───────────────────────────
def test_detect_hwpx():
    with tempfile.TemporaryDirectory() as tmp:
        hwpx = _make_hwpx(Path(tmp))
        assert detect_hwp_format(hwpx) == "hwpx"
        assert is_hwp_file(hwpx) is True


def test_hwpx_roundtrips_to_markdown():
    # Disable kordoc so this exercises the stdlib path regardless of host setup.
    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()
        os.environ["KO_RAG_DISABLE_KORDOC"] = "1"
        with tempfile.TemporaryDirectory() as tmp:
            hwpx = _make_hwpx(Path(tmp))
            out_dir = Path(tmp) / "out"
            md_path = convert_hwp_to_markdown(hwpx, output_dir=out_dir)

            assert os.path.isabs(md_path)
            assert md_path.endswith(".md")
            assert Path(md_path).is_file()

            content = Path(md_path).read_text(encoding="utf-8")
            # Expected Korean text from the runs.
            assert "안녕하세요 서울연치과입니다" in content
            assert "임플란트 진료 안내" in content
            # A markdown table row and the separator must be present.
            assert "| 항목 | 비용 |" in content
            assert "| --- | --- |" in content
            assert "| 임플란트 | 문의 |" in content
    finally:
        _restore_env(snapshot)


def test_hwp_binary_detection_and_missing_backend():
    # Disable kordoc so the missing-pyhwp error surfaces deterministically.
    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()
        os.environ["KO_RAG_DISABLE_KORDOC"] = "1"
        with tempfile.TemporaryDirectory() as tmp:
            hwp_file = Path(tmp) / "sample.hwp"
            hwp_file.write_bytes(_OLE_MAGIC + b"\x00" * 512)
            assert detect_hwp_format(hwp_file) == "hwp"
            assert is_hwp_file(hwp_file) is True

            if PYHWP_AVAILABLE:
                pytest.skip("pyhwp installed; missing-backend path not applicable")
            with pytest.raises(HwpConversionError):
                convert_hwp_to_markdown(hwp_file, output_dir=tmp)
    finally:
        _restore_env(snapshot)


def test_non_hwp_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        txt = Path(tmp) / "notes.txt"
        txt.write_text("just some plain text, not a hwp file", encoding="utf-8")

        assert is_hwp_file(txt) is False
        with pytest.raises(ValueError):
            detect_hwp_format(txt)


def test_extensions_constant():
    assert HWP_EXTENSIONS == (".hwp", ".hwpx", ".hwpml")
    # ``.hwpml`` is kordoc-only; assert it explicitly so the constant cannot
    # silently regress to the old two-element tuple.
    assert ".hwpml" in HWP_EXTENSIONS


# ── new: resolve_kordoc_command ──────────────────────────────────
def test_resolve_kordoc_command_disabled_returns_none():
    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()
        # Even with an explicit command set, the disable flag wins.
        os.environ["KORDOC_CMD"] = "/usr/local/bin/kordoc"
        os.environ["KO_RAG_DISABLE_KORDOC"] = "1"
        assert resolve_kordoc_command() is None
    finally:
        _restore_env(snapshot)


def test_resolve_kordoc_command_npx_override():
    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()
        os.environ["KORDOC_CMD"] = "npx -y kordoc"
        assert resolve_kordoc_command() == ["npx", "-y", "kordoc"]
    finally:
        _restore_env(snapshot)


def test_resolve_kordoc_command_absolute_path_override():
    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()
        abs_path = "/opt/tools/bin/kordoc"
        os.environ["KORDOC_CMD"] = abs_path
        assert resolve_kordoc_command() == [abs_path]
    finally:
        _restore_env(snapshot)


# ── new: _kordoc_timeout ─────────────────────────────────────────
def test_kordoc_timeout_parsing():
    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()

        os.environ["KO_RAG_KORDOC_TIMEOUT"] = "bad"
        assert _kordoc_timeout() == 300  # invalid → default

        os.environ["KO_RAG_KORDOC_TIMEOUT"] = "-5"
        assert _kordoc_timeout() == 300  # non-positive → default

        os.environ["KO_RAG_KORDOC_TIMEOUT"] = "42"
        assert _kordoc_timeout() == 42  # valid positive int → itself

        os.environ.pop("KO_RAG_KORDOC_TIMEOUT", None)
        assert _kordoc_timeout() == 300  # unset → default
    finally:
        _restore_env(snapshot)


# ── new: kordoc SUCCESS through the public entry points ───────────
def test_kordoc_success_markdown_and_text():
    if os.name != "posix":
        pytest.skip("shell-script fake requires a POSIX shell")

    snapshot = _snapshot_kordoc_env()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # A fake kordoc that prints a known markdown table to stdout, exit 0.
            # Mirror the table the lightweight backend would emit for the fixture
            # so the assertion is unambiguous about which backend produced it —
            # we tag the heading so only the kordoc output can satisfy it.
            fake_md = (
                "# kordoc-rendered document\n\n"
                "| 항목 | 비용 |\n"
                "| --- | --- |\n"
                "| 임플란트 | 문의 |\n"
            )
            fake = _write_fake_kordoc(
                tmp_path,
                "cat <<'KORDOC_EOF'\n" + fake_md + "KORDOC_EOF\n",
            )

            _clear_kordoc_env()
            os.environ["KORDOC_CMD"] = str(fake)

            hwpx = _make_hwpx(tmp_path)
            out_dir = tmp_path / "out"
            md_path = convert_hwp_to_markdown(hwpx, output_dir=out_dir)

            content = Path(md_path).read_text(encoding="utf-8")
            # The kordoc-specific heading proves the kordoc backend was used.
            assert "# kordoc-rendered document" in content
            assert "| 항목 | 비용 |" in content
            assert "| --- | --- |" in content
            assert "| 임플란트 | 문의 |" in content

            # convert_hwp_to_text reduces the same kordoc output to plain text,
            # dropping the "| --- |" separator row.
            text = convert_hwp_to_text(hwpx)
            assert "| 항목 | 비용 |" in text
            assert "| 임플란트 | 문의 |" in text
            assert "| --- | --- |" not in text
            assert "| --- |" not in text
    finally:
        _restore_env(snapshot)


# ── new: kordoc REAL FAILURE → lightweight fallback ──────────────
def test_kordoc_real_failure_falls_back_to_stdlib():
    # /bin/false exits 1 with empty stderr → a real failure (no missing marker),
    # so convert_hwp_to_markdown must fall back to the stdlib .hwpx path.
    if not Path("/bin/false").exists():
        pytest.skip("/bin/false not available on this host")

    snapshot = _snapshot_kordoc_env()
    try:
        _clear_kordoc_env()
        os.environ["KORDOC_CMD"] = "/bin/false"

        with tempfile.TemporaryDirectory() as tmp:
            hwpx = _make_hwpx(Path(tmp))
            out_dir = Path(tmp) / "out"
            md_path = convert_hwp_to_markdown(hwpx, output_dir=out_dir)

            content = Path(md_path).read_text(encoding="utf-8")
            # Body text only the stdlib parser would produce from the fixture.
            assert "안녕하세요 서울연치과입니다" in content
            assert "임플란트 진료 안내" in content
            assert "| 항목 | 비용 |" in content
    finally:
        _restore_env(snapshot)


# ── new: kordoc MISSING MARKER → _KordocUnavailable ──────────────
def test_kordoc_missing_marker_raises_unavailable():
    if os.name != "posix":
        pytest.skip("shell-script fake requires a POSIX shell")

    snapshot = _snapshot_kordoc_env()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake = _write_fake_kordoc(
                tmp_path,
                'echo "could not determine executable to run" 1>&2\nexit 1\n',
            )
            _clear_kordoc_env()
            os.environ["KORDOC_CMD"] = str(fake)

            hwpx = _make_hwpx(tmp_path)
            # A "missing" marker on stderr means "kordoc isn't really installed":
            # the internal helper must raise _KordocUnavailable, NOT HwpConversionError.
            with pytest.raises(_KordocUnavailable):
                _convert_with_kordoc(hwpx)
    finally:
        _restore_env(snapshot)


# ── new: kordoc EMPTY OUTPUT → HwpConversionError ────────────────
def test_kordoc_empty_output_raises_conversion_error():
    if os.name != "posix":
        pytest.skip("shell-script fake requires a POSIX shell")

    snapshot = _snapshot_kordoc_env()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Exit 0 but print nothing → kordoc "ran" but produced no document.
            fake = _write_fake_kordoc(tmp_path, "exit 0\n")
            _clear_kordoc_env()
            os.environ["KORDOC_CMD"] = str(fake)

            hwpx = _make_hwpx(tmp_path)
            with pytest.raises(HwpConversionError):
                _convert_with_kordoc(hwpx)
    finally:
        _restore_env(snapshot)


# ── standalone runner ────────────────────────────────────────────
def _run_all() -> int:
    """Discover and run every ``test_*`` function in this module as a script.

    Returns a process exit code: 0 if all tests pass or skip, 1 otherwise. Used
    when the file is executed directly (``python3 tests/test_hwp.py``) on a box
    without pytest.
    """
    skipped_exc = getattr(pytest, "Skipped", None)
    tests = sorted(
        (name, obj)
        for name, obj in globals().items()
        if name.startswith("test_") and callable(obj)
    )
    passed = failed = skipped = 0
    for name, func in tests:
        try:
            func()
        except Exception as exc:  # noqa: BLE001 - report any failure
            if skipped_exc is not None and isinstance(exc, skipped_exc):
                skipped += 1
                print(f"SKIP {name}: {exc}")
                continue
            failed += 1
            import traceback

            print(f"FAIL {name}: {exc!r}")
            traceback.print_exc()
            continue
        passed += 1
        print(f"PASS {name}")

    print(f"\n{passed} passed, {failed} failed, {skipped} skipped")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys

    sys.exit(_run_all())
