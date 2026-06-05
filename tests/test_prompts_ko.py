"""Tests for the Korean (한국어) prompt templates.

These tests intentionally import only :mod:`raganything.prompts_ko` and
:mod:`raganything.prompts_zh`, so they do not require lightrag or mineru to be
installed.
"""

from __future__ import annotations

import string

from raganything.prompts_ko import PROMPTS_KO
from raganything.prompts_zh import PROMPTS_ZH

# Hangul syllables block (U+AC00–U+D7A3)
_HANGUL_START = 0xAC00
_HANGUL_END = 0xD7A3


def _format_fields(template: str) -> set[str]:
    """Return the set of named format-field names in a template string."""
    fields: set[str] = set()
    for _, field_name, _, _ in string.Formatter().parse(template):
        if field_name:
            fields.add(field_name)
    return fields


def _contains_hangul(value: str) -> bool:
    return any(_HANGUL_START <= ord(ch) <= _HANGUL_END for ch in value)


def test_values_non_empty_and_match_chinese_type() -> None:
    for key, value in PROMPTS_KO.items():
        zh_value = PROMPTS_ZH[key]
        assert type(value) is type(zh_value), (
            f"type mismatch for {key}: {type(value).__name__} != {type(zh_value).__name__}"
        )
        if isinstance(value, str):
            assert value.strip(), f"empty string value for {key}"


def test_key_parity_with_chinese() -> None:
    assert set(PROMPTS_KO) == set(PROMPTS_ZH)


def test_placeholder_parity_with_chinese() -> None:
    for key, value in PROMPTS_KO.items():
        zh_value = PROMPTS_ZH[key]
        if not isinstance(value, str) or not isinstance(zh_value, str):
            continue
        assert _format_fields(value) == _format_fields(zh_value), (
            f"format-field mismatch for {key}"
        )


def test_every_value_contains_hangul() -> None:
    for key, value in PROMPTS_KO.items():
        if not isinstance(value, str):
            continue
        assert _contains_hangul(value), f"no Hangul found in {key}"
