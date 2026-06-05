"""
Korean (한국어) prompt templates for multimodal content processing.

Provides Korean-language prompt templates as an alternative to the default
English templates.  Users can activate these at process level by calling
``set_prompt_language("ko")`` from :mod:`raganything.prompt_manager`.

Addresses GitHub issue #85 — prompt language support.
"""

from __future__ import annotations
from typing import Any

PROMPTS_KO: dict[str, Any] = {}

# System prompts for different analysis types
PROMPTS_KO["IMAGE_ANALYSIS_SYSTEM"] = (
    "당신은 전문 이미지 분석가입니다. 상세하고 정확한 설명을 제공하세요."
)
PROMPTS_KO["IMAGE_ANALYSIS_FALLBACK_SYSTEM"] = (
    "당신은 전문 이미지 분석가입니다. 주어진 정보를 바탕으로 상세한 분석을 제공하세요."
)
PROMPTS_KO["TABLE_ANALYSIS_SYSTEM"] = (
    "당신은 전문 데이터 분석가입니다. 구체적인 통찰을 담은 상세한 표 분석을 제공하세요."
)
PROMPTS_KO["EQUATION_ANALYSIS_SYSTEM"] = "당신은 수학 전문가입니다. 상세한 수학적 분석을 제공하세요."
PROMPTS_KO["GENERIC_ANALYSIS_SYSTEM"] = "당신은 {content_type} 콘텐츠를 전문으로 하는 전문 분석가입니다."

# Image analysis prompt template
PROMPTS_KO["vision_prompt"] = """이 이미지를 상세히 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음 지침에 따라 이미지에 대한 포괄적이고 상세한 설명:
    - 전체 구도와 배치를 설명
    - 모든 사물, 인물, 텍스트, 시각적 요소를 식별
    - 요소 간의 관계를 설명
    - 색상, 조명, 시각적 스타일에 주목
    - 표현된 모든 동작이나 활동을 설명
    - 관련된 경우 기술적 세부 사항(차트, 도표 등)을 포함
    - 대명사 대신 항상 구체적인 명칭을 사용",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "image",
        "summary": "이미지 내용과 그 중요성에 대한 간결한 요약(100단어 이내)"
    }}
}}

추가 정보:
- 섹션 경로: {section_path}
- 이미지 경로: {image_path}
- 캡션: {captions}
- 각주: {footnotes}

지식 검색에 유용하도록 정확하고 상세한 시각적 분석을 제공하는 데 집중하세요.
의미를 담은 entity_name을 생성하세요. figure_30_1과 같은 파일명이나 그림 번호는 그것이 실제 제목이 아닌 한 반환하지 마세요."""

# Image analysis prompt with context support
PROMPTS_KO[
    "vision_prompt_with_context"
] = """주변 맥락을 고려하여 이 이미지를 상세히 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음 지침에 따라 이미지에 대한 포괄적이고 상세한 설명:
    - 전체 구도와 배치를 설명
    - 모든 사물, 인물, 텍스트, 시각적 요소를 식별
    - 요소 간의 관계 및 주변 맥락과의 연관성을 설명
    - 색상, 조명, 시각적 스타일에 주목
    - 표현된 모든 동작이나 활동을 설명
    - 관련된 경우 기술적 세부 사항(차트, 도표 등)을 포함
    - 관련 있을 때 주변 콘텐츠와의 연결을 언급
    - 대명사 대신 항상 구체적인 명칭을 사용",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "image",
        "summary": "이미지 내용, 중요성 및 주변 콘텐츠와의 관계에 대한 간결한 요약(100단어 이내)"
    }}
}}

주변 콘텐츠 맥락:
{context}

문서 구조:
- 섹션 경로: {section_path}

이미지 세부 정보:
- 이미지 경로: {image_path}
- 캡션: {captions}
- 각주: {footnotes}

지식 검색에 유용하도록 맥락을 반영한 정확하고 상세한 시각적 분석을 제공하는 데 집중하세요.
의미를 담은 entity_name을 생성하세요. figure_30_1과 같은 파일명이나 그림 번호는 그것이 실제 제목이 아닌 한 반환하지 마세요."""

# Image analysis prompt with text fallback
PROMPTS_KO["text_prompt"] = """다음 이미지 정보를 바탕으로 분석을 제공하세요:

이미지 경로: {image_path}
캡션: {captions}
각주: {footnotes}

{vision_prompt}"""

# Table analysis prompt template
PROMPTS_KO["table_prompt"] = """이 표 내용을 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음을 포함한 표에 대한 포괄적인 분석:
    - 표의 구조와 구성 방식
    - 열 머리글과 그 의미
    - 핵심 데이터 포인트와 패턴
    - 통계적 통찰과 추세
    - 데이터 요소 간의 관계
    - 제시된 데이터의 중요성
    포괄적인 표현 대신 항상 구체적인 명칭과 수치를 사용하세요.",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "table",
        "summary": "표의 목적과 핵심 발견에 대한 간결한 요약(100단어 이내)"
    }}
}}

표 정보:
이미지 경로: {table_img_path}
제목: {table_caption}
본문: {table_body}
각주: {table_footnote}

표 데이터에서 의미 있는 통찰과 관계를 추출하는 데 집중하세요."""

# Table analysis prompt with context support
PROMPTS_KO[
    "table_prompt_with_context"
] = """주변 맥락을 고려하여 이 표 내용을 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음을 포함한 표에 대한 포괄적인 분석:
    - 표의 구조와 구성 방식
    - 열 머리글과 그 의미
    - 핵심 데이터 포인트와 패턴
    - 통계적 통찰과 추세
    - 주변 맥락과 관련한 데이터 요소 간의 관계
    - 표가 주변 콘텐츠의 개념을 어떻게 뒷받침하거나 설명하는지
    포괄적인 표현 대신 항상 구체적인 명칭과 수치를 사용하세요.",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "table",
        "summary": "표의 목적, 핵심 발견 및 주변 콘텐츠와의 관계에 대한 간결한 요약(100단어 이내)"
    }}
}}

주변 콘텐츠 맥락:
{context}

표 정보:
이미지 경로: {table_img_path}
제목: {table_caption}
본문: {table_body}
각주: {table_footnote}

주변 콘텐츠의 맥락에서 표 데이터로부터 의미 있는 통찰과 관계를 추출하는 데 집중하세요."""

# Equation analysis prompt template
PROMPTS_KO["equation_prompt"] = """이 수학 수식을 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음을 포함한 수식에 대한 포괄적인 분석:
    - 수학적 의미와 해석
    - 변수와 그 정의
    - 사용된 수학적 연산과 함수
    - 적용 영역과 배경
    - 물리적 또는 이론적 의의
    - 다른 수학적 개념과의 관계
    - 실제 적용 사례나 활용
    항상 정확한 수학 용어를 사용하세요.",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "equation",
        "summary": "수식의 목적과 중요성에 대한 간결한 요약(100단어 이내)"
    }}
}}

수식 정보:
수식: {equation_text}
형식: {equation_format}

수학적 통찰을 제공하고 수식의 중요성을 설명하는 데 집중하세요."""

# Equation analysis prompt with context support
PROMPTS_KO[
    "equation_prompt_with_context"
] = """주변 맥락을 고려하여 이 수학 수식을 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음을 포함한 수식에 대한 포괄적인 분석:
    - 수학적 의미와 해석
    - 맥락 속에서의 변수 정의
    - 사용된 수학적 연산과 함수
    - 주변 자료에 기반한 적용 영역과 배경
    - 물리적 또는 이론적 의의
    - 맥락에서 언급된 다른 수학적 개념과의 관계
    - 실제 적용 사례나 활용
    - 수식이 더 넓은 논의나 틀과 어떻게 연관되는지
    항상 정확한 수학 용어를 사용하세요.",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "equation",
        "summary": "수식의 목적, 중요성 및 맥락에서의 역할에 대한 간결한 요약(100단어 이내)"
    }}
}}

주변 콘텐츠 맥락:
{context}

수식 정보:
수식: {equation_text}
형식: {equation_format}

더 넓은 맥락 속에서 수학적 통찰을 제공하고 수식의 중요성을 설명하는 데 집중하세요."""

# Generic content analysis prompt template
PROMPTS_KO["generic_prompt"] = """이 {content_type} 콘텐츠를 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음을 포함한 콘텐츠에 대한 포괄적인 분석:
    - 콘텐츠 구조와 구성
    - 핵심 정보와 요소
    - 구성 요소 간의 관계
    - 배경과 중요성
    - 지식 검색과 관련된 세부 사항
    항상 {content_type} 콘텐츠에 적합한 전문 용어를 사용하세요.",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "{content_type}",
        "summary": "콘텐츠의 목적과 요점에 대한 간결한 요약(100단어 이내)"
    }}
}}

콘텐츠: {content}

지식 검색에 유용한 의미 있는 정보를 추출하는 데 집중하세요."""

# Generic content analysis prompt with context support
PROMPTS_KO[
    "generic_prompt_with_context"
] = """주변 맥락을 고려하여 이 {content_type} 콘텐츠를 분석하고 다음 JSON 구조로 답변을 제공하세요:

{{
    "detailed_description": "다음을 포함한 콘텐츠에 대한 포괄적인 분석:
    - 콘텐츠 구조와 구성
    - 핵심 정보와 요소
    - 구성 요소 간의 관계
    - 주변 콘텐츠와 관련한 배경과 중요성
    - 이 콘텐츠가 더 넓은 논의와 어떻게 연결되거나 이를 뒷받침하는지
    - 지식 검색과 관련된 세부 사항
    항상 {content_type} 콘텐츠에 적합한 전문 용어를 사용하세요.",
    "entity_info": {{
        "entity_name": "{entity_name}",
        "entity_type": "{content_type}",
        "summary": "콘텐츠의 목적, 요점 및 주변 맥락과의 관계에 대한 간결한 요약(100단어 이내)"
    }}
}}

주변 콘텐츠 맥락:
{context}

콘텐츠: {content}

지식 검색에 유용한 의미 있는 정보를 추출하고 더 넓은 맥락에서 콘텐츠의 역할을 이해하는 데 집중하세요."""

# Modal chunk templates
PROMPTS_KO["image_chunk"] = """
이미지 콘텐츠 분석:
- 섹션 경로: {section_path}
- 인접 텍스트: {neighbor_text}
이미지 경로: {image_path}
캡션: {captions}
각주: {footnotes}

시각적 분석: {enhanced_caption}"""

PROMPTS_KO["table_chunk"] = """표 분석:
이미지 경로: {table_img_path}
제목: {table_caption}
구조: {table_body}
각주: {table_footnote}

분석: {enhanced_caption}"""

PROMPTS_KO["equation_chunk"] = """수학 수식 분석:
수식: {equation_text}
형식: {equation_format}

수학적 분석: {enhanced_caption}"""

PROMPTS_KO["generic_chunk"] = """{content_type} 콘텐츠 분석:
콘텐츠: {content}

분석: {enhanced_caption}"""

# Query-related prompts
PROMPTS_KO["QUERY_IMAGE_DESCRIPTION"] = (
    "이 이미지의 주요 내용, 핵심 요소, 중요한 정보를 간략히 설명하세요."
)

PROMPTS_KO["QUERY_IMAGE_ANALYST_SYSTEM"] = (
    "당신은 이미지 내용을 정확하게 설명할 수 있는 전문 이미지 분석가입니다."
)

PROMPTS_KO["QUERY_TABLE_ANALYSIS"] = """다음 표 데이터의 주요 내용, 구조, 핵심 정보를 분석하세요:

표 데이터:
{table_data}

표 제목: {table_caption}

표의 주요 내용, 데이터 특징, 중요한 발견을 간략히 요약하세요."""

PROMPTS_KO["QUERY_TABLE_ANALYST_SYSTEM"] = (
    "당신은 표 데이터를 정확하게 분석할 수 있는 전문 데이터 분석가입니다."
)

PROMPTS_KO["QUERY_EQUATION_ANALYSIS"] = """다음 수학 수식의 의미와 용도를 설명하세요:

LaTeX 수식: {latex}
수식 제목: {equation_caption}

이 수식의 수학적 의미, 적용 상황, 중요성을 간략히 설명하세요."""

PROMPTS_KO["QUERY_EQUATION_ANALYST_SYSTEM"] = "당신은 수학 수식을 명확하게 설명할 수 있는 수학 전문가입니다."

PROMPTS_KO[
    "QUERY_GENERIC_ANALYSIS"
] = """다음 {content_type} 유형의 콘텐츠를 분석하고 주요 정보와 핵심 특징을 추출하세요:

콘텐츠: {content_str}

이 콘텐츠의 주요 특징과 중요한 정보를 간략히 요약하세요."""

PROMPTS_KO["QUERY_GENERIC_ANALYST_SYSTEM"] = (
    "당신은 {content_type} 유형의 콘텐츠를 정확하게 분석할 수 있는 전문 콘텐츠 분석가입니다."
)

PROMPTS_KO["QUERY_ENHANCEMENT_SUFFIX"] = (
    "\n\n사용자 질의와 제공된 멀티모달 콘텐츠 정보를 바탕으로 포괄적인 답변을 제공하세요."
)
