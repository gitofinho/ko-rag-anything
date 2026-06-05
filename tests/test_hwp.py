"""Tests for the lightweight HWP/HWPX → Markdown converter.

These tests are stdlib-only and must pass *without* pyhwp installed. The HWPX
fixture is built in-process with :mod:`zipfile`, and the HWP path is exercised
only for its missing-backend error behavior (skipped if pyhwp happens to be
available in the environment).
"""

from __future__ import annotations

import os
import tempfile
import zipfile
from pathlib import Path

import pytest

from raganything.hwp import (
    HWP_EXTENSIONS,
    PYHWP_AVAILABLE,
    HwpConversionError,
    convert_hwp_to_markdown,
    detect_hwp_format,
    is_hwp_file,
)

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


def _make_hwpx(directory: Path) -> Path:
    """Build a minimal valid .hwpx package and return its path."""
    hwpx_path = directory / "sample.hwpx"
    with zipfile.ZipFile(hwpx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # The mimetype is conventionally stored first and uncompressed.
        zf.writestr("mimetype", "application/hwp+zip")
        zf.writestr("Contents/section0.xml", _SECTION_XML)
    return hwpx_path


def test_detect_hwpx():
    with tempfile.TemporaryDirectory() as tmp:
        hwpx = _make_hwpx(Path(tmp))
        assert detect_hwp_format(hwpx) == "hwpx"
        assert is_hwp_file(hwpx) is True


def test_hwpx_roundtrips_to_markdown():
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


def test_hwp_binary_detection_and_missing_backend():
    with tempfile.TemporaryDirectory() as tmp:
        hwp = Path(tmp) / "sample.hwp"
        hwp.write_bytes(_OLE_MAGIC + b"\x00" * 512)
        assert detect_hwp_format(hwp) == "hwp"
        assert is_hwp_file(hwp) is True

        if PYHWP_AVAILABLE:
            pytest.skip("pyhwp installed; missing-backend path not applicable")
        with pytest.raises(HwpConversionError):
            convert_hwp_to_markdown(hwp, output_dir=tmp)


def test_non_hwp_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        txt = Path(tmp) / "notes.txt"
        txt.write_text("just some plain text, not a hwp file", encoding="utf-8")

        assert is_hwp_file(txt) is False
        with pytest.raises(ValueError):
            detect_hwp_format(txt)


def test_extensions_constant():
    assert HWP_EXTENSIONS == (".hwp", ".hwpx")
