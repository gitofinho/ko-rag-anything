"""
Tests for raganything.korean_utils.

These tests are stdlib + pytest only. They are written to pass on a clean
environment WITHOUT kiwipiepy installed (the optional morphological analyzer),
exercising the pure-Python fallback paths, while still being correct when
kiwipiepy happens to be present.
"""

import unicodedata

import pytest

from raganything.korean_utils import (
    KIWIPIEPY_AVAILABLE,
    KoreanTokenizer,
    count_korean_tokens,
    korean_morphs,
    korean_sentence_split,
    normalize_korean,
)


# ── normalize_korean ─────────────────────────────────────────────
class TestNormalizeKorean:
    def test_empty_and_none(self):
        assert normalize_korean("") == ""
        assert normalize_korean(None) == ""  # type: ignore[arg-type]

    def test_nfc_composition(self):
        # Decomposed (NFD) Hangul -> composed (NFC) single syllables.
        decomposed = unicodedata.normalize("NFD", "한국어")
        assert decomposed != "한국어"  # sanity: input really is decomposed
        result = normalize_korean(decomposed)
        assert result == "한국어"
        assert unicodedata.is_normalized("NFC", result)

    def test_collapse_whitespace(self):
        assert normalize_korean("안녕   하세요") == "안녕 하세요"
        assert normalize_korean("a\t\tb") == "a b"

    def test_strip_zero_width(self):
        assert normalize_korean("한​국") == "한국"
        assert normalize_korean("﻿안녕") == "안녕"

    def test_punctuation_normalization(self):
        assert normalize_korean("정말？") == "정말?"
        assert normalize_korean("좋아！") == "좋아!"
        assert normalize_korean("“인용”") == '"인용"'

    def test_collapse_blank_lines(self):
        assert normalize_korean("a\n\n\n\nb") == "a\n\nb"

    def test_idempotent(self):
        samples = [
            "안녕하세요！  반갑습니다。",
            unicodedata.normalize("NFD", "한국어 처리"),
            "Mixed 텍스트   with\t\tspaces\n\n\n\nend",
            "“따옴표”와 ‘작은따옴표’",
        ]
        for s in samples:
            once = normalize_korean(s)
            twice = normalize_korean(once)
            assert once == twice, f"not idempotent for: {s!r}"


# ── korean_sentence_split ────────────────────────────────────────
class TestSentenceSplit:
    def test_empty(self):
        assert korean_sentence_split("") == []

    def test_basic_korean_paragraph(self):
        text = "오늘은 날씨가 좋다. 산책을 가야겠어요. 정말 그럴까?"
        sentences = korean_sentence_split(text)
        assert sentences == [
            "오늘은 날씨가 좋다.",
            "산책을 가야겠어요.",
            "정말 그럴까?",
        ]

    def test_does_not_split_decimal(self):
        text = "원주율은 약 3.14 입니다. 외워두세요."
        sentences = korean_sentence_split(text)
        assert sentences == ["원주율은 약 3.14 입니다.", "외워두세요."]
        # The decimal must stay intact inside one sentence.
        assert any("3.14" in s for s in sentences)

    def test_ellipsis_not_split(self):
        text = "글쎄요... 잘 모르겠네요."
        sentences = korean_sentence_split(text)
        assert sentences == ["글쎄요... 잘 모르겠네요."]

    def test_abbreviation_not_split(self):
        text = "Dr. Kim은 훌륭하다. 모두가 존경한다."
        sentences = korean_sentence_split(text)
        assert sentences == ["Dr. Kim은 훌륭하다.", "모두가 존경한다."]

    def test_mixed_terminals(self):
        text = "정말 좋아! 그렇지 않아? 맞아요。"
        sentences = korean_sentence_split(text)
        assert len(sentences) == 3

    def test_no_terminal_punctuation(self):
        text = "마침표가 없는 문장"
        assert korean_sentence_split(text) == ["마침표가 없는 문장"]

    def test_endings_da_yo_kka_ham(self):
        text = "공부한다. 갈게요. 먹을까? 완료함."
        sentences = korean_sentence_split(text)
        assert sentences == ["공부한다.", "갈게요.", "먹을까?", "완료함."]


# ── count_korean_tokens ──────────────────────────────────────────
class TestCountTokens:
    def test_empty(self):
        assert count_korean_tokens("") == 0
        assert count_korean_tokens("    ") == 0

    def test_positive(self):
        assert count_korean_tokens("안녕하세요") >= 1

    def test_heuristic_units(self):
        # Two Hangul runs + one number token.
        assert count_korean_tokens("안녕 하세요 123") == 3

    def test_monotonicity(self):
        base = "한국어 처리"
        longer = base + " 추가 문장입니다"
        assert count_korean_tokens(longer) >= count_korean_tokens(base)

    def test_monotonic_appending(self):
        text = ""
        prev = 0
        for token in ["오늘", "은", "좋은", "날", "입니다"]:
            text += " " + token
            current = count_korean_tokens(text)
            assert current >= prev
            prev = current

    def test_use_morphs_does_not_raise_without_kiwi(self):
        # Even requesting morph mode must work; falls back to heuristic when
        # kiwipiepy is absent.
        n = count_korean_tokens("형태소 분석 테스트", use_morphs=True)
        assert n >= 1


# ── korean_morphs ────────────────────────────────────────────────
class TestKoreanMorphs:
    def test_empty(self):
        assert korean_morphs("") == []
        assert korean_morphs("   ") == []

    def test_never_raises_returns_list(self):
        result = korean_morphs("안녕하세요 세계 hello world 123")
        assert isinstance(result, list)
        assert all(isinstance(m, str) for m in result)
        assert len(result) >= 1

    def test_fallback_separates_korean_and_latin(self):
        # Only assert the fallback behaviour when kiwipiepy is not installed,
        # since the analyzer tokenizes differently (and more finely).
        if not KIWIPIEPY_AVAILABLE:
            assert korean_morphs("안녕hello") == ["안녕", "hello"]


# ── KoreanTokenizer ──────────────────────────────────────────────
class TestKoreanTokenizer:
    def setup_method(self):
        self.tok = KoreanTokenizer()

    def test_encode_returns_ints(self):
        tokens = self.tok.encode("한국")
        assert tokens == [ord("한"), ord("국")]

    def test_empty_roundtrip(self):
        assert self.tok.encode("") == []
        assert self.tok.decode([]) == ""

    def test_one_token_per_codepoint(self):
        # Each Hangul syllable is exactly one token — the whole point.
        assert len(self.tok.encode("한국어")) == 3

    @pytest.mark.parametrize(
        "text",
        [
            "안녕하세요",
            "Hello, 세계! 반가워요.",
            "이모지 😀🎉 포함 텍스트",
            "숫자 3.14 와 기호 ~!@#$%",
            "\n탭\t줄바꿈\n섞임",
            unicodedata.normalize("NFD", "분해된한글"),
            "",
        ],
    )
    def test_lossless_roundtrip(self, text):
        assert self.tok.decode(self.tok.encode(text)) == text

    def test_roundtrip_does_not_normalize(self):
        # The tokenizer must be lossless, i.e. NOT silently normalize input.
        decomposed = unicodedata.normalize("NFD", "한")
        assert self.tok.decode(self.tok.encode(decomposed)) == decomposed


# ── Optional dependency contract ─────────────────────────────────
class TestOptionalDependency:
    def test_flag_is_bool(self):
        assert isinstance(KIWIPIEPY_AVAILABLE, bool)

    def test_all_functions_work_without_kiwi(self):
        # Regardless of kiwipiepy presence, none of these should raise.
        normalize_korean("테스트")
        korean_sentence_split("문장 하나. 문장 둘.")
        count_korean_tokens("토큰 카운트")
        count_korean_tokens("토큰", use_morphs=True)
        korean_morphs("형태소")
        KoreanTokenizer().encode("토크나이저")
