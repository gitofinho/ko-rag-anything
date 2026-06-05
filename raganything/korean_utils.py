"""
Korean text-processing utilities for ko-rag-anything
한국어 텍스트 처리 유틸리티

This module bundles self-contained helpers that improve the *Korean* quality of
RAG preprocessing: Unicode normalization, sentence splitting, fair token
counting, lightweight morpheme extraction, and a LightRAG-compatible tokenizer
that sizes chunks by Korean units rather than raw bytes or BPE pieces.

이 모듈은 한국어 RAG 전처리 품질을 높이기 위한 독립형 헬퍼 모음입니다.
유니코드 정규화, 문장 분리, 공정한 토큰 카운팅, 경량 형태소 추출, 그리고
LightRAG와 호환되는 한국어 토크나이저를 제공합니다.

Design goals
------------
* **Pure-Python, stdlib only.** Importing this module never requires a third
  party package. It works on a clean Python 3.10+ install.
* **Optional morphological analysis.** If the excellent ``kiwipiepy`` Korean
  morphological analyzer is installed, the morph-aware code paths use it for
  higher fidelity. Otherwise every function gracefully degrades to a
  regex/heuristic fallback and *never raises* because of the missing dependency.

Optional install (선택 설치)::

    pip install kiwipiepy

Whether kiwipiepy was importable is exposed as the module-level boolean
``KIWIPIEPY_AVAILABLE`` so callers can branch on it.
"""

from __future__ import annotations

import re
import unicodedata
from typing import List

__all__ = [
    "KIWIPIEPY_AVAILABLE",
    "normalize_korean",
    "korean_sentence_split",
    "count_korean_tokens",
    "korean_morphs",
    "KoreanTokenizer",
]


# ── Optional dependency detection ────────────────────────────────
# We probe for kiwipiepy at import time only to set the public flag. The actual
# analyzer object is created lazily (and cached) so that import stays cheap and
# side-effect free.
try:  # pragma: no cover - depends on environment
    import kiwipiepy as _kiwipiepy  # noqa: F401

    KIWIPIEPY_AVAILABLE = True
except Exception:  # ImportError, or any failure constructing the package
    KIWIPIEPY_AVAILABLE = False


# Cached Kiwi() instance. ``None`` means "not built yet"; ``False`` means
# "tried and failed, don't try again".
_KIWI_INSTANCE = None


def _get_kiwi():
    """Return a shared ``Kiwi`` instance, or ``None`` if unavailable.

    Building a ``Kiwi`` analyzer is comparatively expensive, so we construct it
    once and reuse it. Any failure (package missing, model load error) is
    swallowed and cached as ``None`` so callers transparently fall back.
    """
    global _KIWI_INSTANCE
    if _KIWI_INSTANCE is not None:
        return _KIWI_INSTANCE or None
    if not KIWIPIEPY_AVAILABLE:
        _KIWI_INSTANCE = False
        return None
    try:  # pragma: no cover - exercised only when kiwipiepy is installed
        from kiwipiepy import Kiwi

        _KIWI_INSTANCE = Kiwi()
    except Exception:
        _KIWI_INSTANCE = False
        return None
    return _KIWI_INSTANCE


# ── Character ranges & lookup tables ─────────────────────────────
# Precomposed Hangul syllables (가-힣), conjoining jamo, and compatibility jamo.
_HANGUL_PATTERN = re.compile(
    r"[가-힣ᄀ-ᇿ㄰-㆏ꥠ-꥿ힰ-퟿]"
)
# A run of Hangul characters = one "Korean word/eojeol" unit for the heuristic.
_HANGUL_RUN = re.compile(
    r"[가-힣ᄀ-ᇿ㄰-㆏ꥠ-꥿ힰ-퟿]+"
)
# Non-Korean, non-space "word" tokens (latin words, numbers, CJK, symbols).
_NON_KOREAN_TOKEN = re.compile(r"[^\s가-힣ᄀ-ᇿ㄰-㆏ꥠ-꥿ힰ-퟿]+")

# Zero-width / invisible characters to strip during normalization.
_ZERO_WIDTH = re.compile(
    "[​‌‍⁠﻿᠎­]"
)

# Full-width / variant punctuation → standard ASCII (or canonical) form.
# Korean documents frequently mix CJK full-width punctuation with ASCII; we
# canonicalize the noisy variants while keeping the sentence-final "。" since it
# is a legitimate terminal mark handled by the splitter.
_PUNCT_MAP = {
    "！": "!",
    "？": "?",
    "，": ",",
    "．": ".",
    "：": ":",
    "；": ";",
    "（": "(",
    "）": ")",
    "［": "[",
    "］": "]",
    "｛": "{",
    "｝": "}",
    "「": '"',
    "」": '"',
    "『": '"',
    "』": '"',
    "〝": '"',
    "〞": '"',
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "％": "%",
    "～": "~",
    "－": "-",
    "—": "-",
    "–": "-",
    "‥": "…",  # two-dot leader → standard ellipsis
    "・": "·",
}
_PUNCT_TABLE = {ord(k): v for k, v in _PUNCT_MAP.items()}

# Collapse any run of horizontal whitespace (tabs, full-width spaces, etc.)
_HSPACE = re.compile(r"[ \t 　\f\v]+")
# Collapse 3+ newlines down to a paragraph break (max two newlines).
_MULTI_NEWLINE = re.compile(r"\n{3,}")
# Trailing spaces before a newline.
_TRAILING_SPACE = re.compile(r"[ \t]+\n")


def normalize_korean(text: str) -> str:
    """Normalize Korean (and mixed) text for stable downstream processing.

    The transformation is **idempotent** — ``normalize_korean(normalize_korean(x))
    == normalize_korean(x)`` — and performs:

    1. Unicode **NFC** normalization (composes decomposed Hangul jamo into
       precomposed syllables so ``len`` and equality behave intuitively).
    2. Stripping of zero-width and other invisible formatting characters.
    3. Mapping full-width / variant punctuation to standard forms
       (e.g. ``！？，`` → ``!?,``, smart quotes → straight quotes).
    4. Collapsing redundant horizontal whitespace to single spaces, trimming
       trailing spaces on each line, and collapsing 3+ blank lines to one
       paragraph break.

    Empty or non-string input yields an empty string.
    """
    if not text:
        return ""
    # NFC first so that any decomposed jamo become single codepoints before we
    # touch punctuation/whitespace.
    text = unicodedata.normalize("NFC", text)
    text = _ZERO_WIDTH.sub("", text)
    text = text.translate(_PUNCT_TABLE)
    # Normalize line endings, then whitespace runs.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _HSPACE.sub(" ", text)
    text = _TRAILING_SPACE.sub("\n", text)
    text = _MULTI_NEWLINE.sub("\n\n", text)
    return text.strip()


# ── Sentence splitting ───────────────────────────────────────────
# Abbreviations / patterns where a period must NOT end a sentence.
_ABBREVIATIONS = (
    "Mr.",
    "Mrs.",
    "Ms.",
    "Dr.",
    "Prof.",
    "Sr.",
    "Jr.",
    "St.",
    "vs.",
    "etc.",
    "e.g.",
    "i.e.",
    "No.",
    "Fig.",
    "Vol.",
    "approx.",
)
# Placeholder used to hide protected periods during splitting, then restored.
_DOT_PLACEHOLDER = "DOT"

# Terminal punctuation that ends a sentence. We treat one or more terminal marks
# (possibly followed by a closing quote/bracket) as the boundary.
_SENTENCE_BOUNDARY = re.compile(
    r"""
    (?<=[\.!\?…。])      # a terminal mark just before the split point
    [\)\]\}"'”’」』]?      # optional trailing closer
    \s+                   # whitespace separating the sentences
    """,
    re.VERBOSE,
)

# Protect decimals like 3.14 (digit . digit) — turn the dot into a placeholder.
_DECIMAL = re.compile(r"(?<=\d)\.(?=\d)")
# Protect runs of dots used as ellipsis written with periods ("...").
_DOTS_ELLIPSIS = re.compile(r"\.{2,}")


def korean_sentence_split(text: str) -> List[str]:
    """Split Korean (and mixed) text into sentences.

    Pure-Python / regex based — no external dependencies. It splits on Korean
    and Latin terminal punctuation (``. ! ? … 。``) and the closing quotes that
    may follow them, while protecting:

    * **decimals** such as ``3.14`` (never split mid-number),
    * **ellipses** written as ``...`` or ``…`` (kept attached to the sentence),
    * common **abbreviations** (``e.g.``, ``Dr.``, ``etc.`` …).

    Korean sentence-ending forms such as ``~다.``, ``~요.``, ``~까?``, ``~함.``
    are handled naturally because the trailing terminal mark drives the split.
    The input is normalized first, so callers need not pre-clean whitespace.

    Returns a list of trimmed, non-empty sentences. A string with no terminal
    punctuation comes back as a single-element list.
    """
    if not text:
        return []
    text = normalize_korean(text)
    if not text:
        return []

    # 1) Protect decimals: 3.14 -> 3<DOT>14
    protected = _DECIMAL.sub(_DOT_PLACEHOLDER, text)

    # 2) Protect multi-dot ellipsis ("..." / "....") so it isn't a boundary on
    #    the first dot; collapse to a single sentinel that is NOT a terminal.
    protected = _DOTS_ELLIPSIS.sub(
        lambda m: _DOT_PLACEHOLDER * len(m.group(0)), protected
    )

    # 3) Protect abbreviations by hiding their internal/trailing dots.
    for abbr in _ABBREVIATIONS:
        protected = protected.replace(
            abbr, abbr.replace(".", _DOT_PLACEHOLDER)
        )

    # 4) Split on the remaining genuine sentence boundaries.
    raw_parts = _SENTENCE_BOUNDARY.split(protected)

    # 5) Restore protected dots and clean up.
    sentences = []
    for part in raw_parts:
        restored = part.replace(_DOT_PLACEHOLDER, ".").strip()
        if restored:
            sentences.append(restored)
    return sentences


# ── Token counting ───────────────────────────────────────────────
def count_korean_tokens(text: str, *, use_morphs: bool = False) -> int:
    """Approximate the token count of Korean (and mixed) text.

    Two modes:

    * ``use_morphs=True`` **and** kiwipiepy installed → counts morphemes
      (the most faithful unit for Korean), via :func:`korean_morphs`.
    * Otherwise → a **heuristic**: count each maximal run of Hangul characters
      (≈ one eojeol / spacing-word) as one token, plus each whitespace-delimited
      non-Korean token (Latin words, numbers, punctuation clusters, CJK). This
      avoids the pathological over-counting of byte/BPE tokenizers on Hangul
      (where a single syllable can cost 2-3 BPE tokens) while staying stable and
      dependency-free.

    The count is always ``>= 0`` and is monotonic with respect to appending
    text: adding non-empty content never decreases the count.
    """
    if not text or not text.strip():
        return 0

    if use_morphs and KIWIPIEPY_AVAILABLE:
        morphs = korean_morphs(text)
        # korean_morphs falls back to word splitting if kiwi fails to load; in
        # that case len(morphs) is still a sane, monotonic count.
        return len(morphs)

    normalized = normalize_korean(text)
    if not normalized:
        return 0
    hangul_units = len(_HANGUL_RUN.findall(normalized))
    non_korean_units = len(_NON_KOREAN_TOKEN.findall(normalized))
    return hangul_units + non_korean_units


def korean_morphs(text: str) -> List[str]:
    """Return a list of morphemes for ``text``.

    If kiwipiepy is installed and loads successfully, real morphological
    analysis is used (each surface morpheme form is returned in order). If it is
    not available — or fails to initialize — this falls back to a pure-Python
    split on whitespace and word/punctuation boundaries. **It never raises** due
    to a missing optional dependency.
    """
    if not text or not text.strip():
        return []

    kiwi = _get_kiwi()
    if kiwi is not None:
        try:  # pragma: no cover - only when kiwipiepy is installed
            result = []
            for token in kiwi.tokenize(text):
                # kiwipiepy Token exposes ``.form`` for the surface morpheme.
                form = getattr(token, "form", None)
                result.append(form if form is not None else str(token))
            return result
        except Exception:
            # Fall through to the heuristic on any analyzer error.
            pass

    # Pure-Python fallback: separate Hangul runs and non-space tokens. We split
    # on whitespace first, then further break each chunk into Hangul runs and
    # non-Korean runs so "안녕hello" -> ["안녕", "hello"].
    morphs: List[str] = []
    token_pattern = re.compile(
        r"[가-힣ᄀ-ᇿ㄰-㆏ꥠ-꥿ힰ-퟿]+"
        r"|[^\s가-힣ᄀ-ᇿ㄰-㆏ꥠ-꥿ힰ-퟿]+"
    )
    for piece in token_pattern.findall(text):
        piece = piece.strip()
        if piece:
            morphs.append(piece)
    return morphs


# ── LightRAG-compatible tokenizer ────────────────────────────────
class KoreanTokenizer:
    """A deterministic, lossless tokenizer that counts Korean units fairly.

    LightRAG sizes chunks by ``len(tokenizer.encode(text))`` and reconstructs
    text with ``tokenizer.decode(tokens)``. Byte-level or BPE tokenizers tend to
    inflate Korean: a single Hangul syllable can cost several tokens, so a
    "1200-token" chunk holds far less Korean prose than English. This tokenizer
    maps text to **Unicode codepoints**, so one Hangul syllable = exactly one
    token. That makes chunk-size limits count Korean characters fairly and
    consistently, regardless of UTF-8 byte width.

    The mapping is a plain ``ord``/``chr`` round-trip, so it is fully reversible
    for *any* input — Korean, Latin, mixed, emoji, control characters — and
    requires no vocabulary file or external model.

    Usage with LightRAG::

        from raganything.korean_utils import KoreanTokenizer
        from lightrag import LightRAG

        rag = LightRAG(
            working_dir="./rag_storage",
            tokenizer=KoreanTokenizer(),
            chunk_token_size=1200,   # now ≈ 1200 Korean characters
            # ... other LightRAG args ...
        )

    Because each token is one codepoint, ``chunk_token_size`` becomes an
    intuitive "characters per chunk" budget for Hangul-heavy corpora.
    """

    def encode(self, text: str) -> List[int]:
        """Encode ``text`` to a list of integer tokens (Unicode codepoints).

        One token per codepoint. Returns an empty list for empty input.
        """
        if not text:
            return []
        return [ord(ch) for ch in text]

    def decode(self, tokens: List[int]) -> str:
        """Decode a list of integer tokens back to the original string.

        Inverse of :meth:`encode`: ``decode(encode(s)) == s`` for any string
        ``s``. Non-iterable or empty input yields an empty string.
        """
        if not tokens:
            return ""
        return "".join(chr(int(t)) for t in tokens)
