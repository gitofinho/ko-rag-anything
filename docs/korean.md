# 한국어 RAG 가이드 (Korean RAG Guide)

이 문서는 **ko-rag-anything**(HKUDS/RAG-Anything의 한국어 특화 포크)을 한국어 문서에 맞게 설정하고 운영하는 방법을 설명한다. 영어 기준 사용법은 [README.md](../README.md)를, 빠른 예제는 [`examples/korean_example.py`](../examples/korean_example.py)와 한국어 README([README_ko.md](../README_ko.md))를 함께 참고하라.

---

## 1. 개요 — 왜 한국어 전용 설정이 필요한가

RAG-Anything은 LightRAG 위에 멀티모달 처리(이미지·표·수식)를 얹은 프레임워크다. 핵심 파이프라인(파싱 → 콘텐츠 분석 → 지식 그래프 → 검색)은 언어에 독립적이지만, 한국어 문서를 다룰 때는 다음 네 지점에서 품질 차이가 크게 벌어진다.

- **토크나이징(tokenization)** — LightRAG 기본 토크나이저는 `tiktoken`(OpenAI BPE) 기반이라 한국어를 음절·바이트 단위로 잘게 쪼갠다. 한국어 텍스트는 영어보다 토큰 수가 부풀려져 청크 경계가 어색해지고, `max_token_size` 대비 실제로 담기는 의미 단위가 줄어든다. 형태소·문장 인식을 반영한 토크나이저를 쓰면 청크 크기를 한국어 기준으로 잡을 수 있다.
- **OCR** — 스캔 PDF·이미지 문서는 OCR 언어 설정이 결과를 좌우한다. MinerU에 `lang="korean"`을 넘기면 한글 인식 정확도가 올라간다.
- **임베딩(embeddings)** — 검색 품질은 임베딩 모델이 한국어를 얼마나 잘 표현하는지에 거의 전적으로 달려 있다. 영어 위주 임베딩은 한국어 의미 유사도를 제대로 잡지 못한다.
- **프롬프트(prompts)** — 엔티티 추출·이미지 캡션·답변 생성 프롬프트가 영어면 LLM이 영어로 답하거나 한국어 고유표현(존댓말, 합성어, 조사)을 놓치기 쉽다. 한국어 프롬프트로 전환하면 출력 일관성이 좋아진다.

아래 절에서 각 지점을 순서대로 다룬다.

---

## 2. 설치

기본 설치는 영어판과 동일하다.

```bash
# 기본 설치
pip install raganything

# 형식 확장(이미지/텍스트 등)이 필요하면
pip install 'raganything[all]'
```

소스에서 설치할 경우:

```bash
git clone https://github.com/HKUDS/RAG-Anything.git
cd RAG-Anything
uv sync
```

### 한국어 추가 의존성(선택)

```bash
# 형태소 분석기 (선택 — 미설치 시 순수 파이썬 폴백 사용)
pip install kiwipiepy

# 한국어 임베딩 모델을 로컬에서 돌릴 경우
pip install sentence-transformers
```

- `kiwipiepy`는 **선택 사항**이다. 설치되어 있으면 `raganything.korean_utils`의 형태소 기반 기능이 활성화되고, 없으면 정규식 기반 순수 파이썬 폴백으로 동작한다(정확도는 낮지만 추가 설치 없이 작동).
- 한국어 임베딩 모델(아래 7절 참고)을 OpenAI 같은 외부 API 대신 로컬에서 실행하려면 `sentence-transformers`(또는 모델이 요구하는 런타임)가 필요하다.

> Office 문서(.doc/.docx/.ppt/.pptx/.xls/.xlsx) 처리는 영어판과 동일하게 LibreOffice 설치가 필요하다. 자세한 내용은 [README.md](../README.md)의 Configuration 절을 참고하라.

---

## 3. 한국어 프롬프트 전환

프롬프트 언어는 `raganything.prompt_manager`로 **프로세스 전역(process-global)** 스위치를 통해 바꾼다. 한 번 전환하면 같은 프로세스 안의 모든 RAGAnything/모달 프로세서가 그 언어 프롬프트를 사용한다.

```python
from raganything.prompt_manager import (
    set_prompt_language,
    get_prompt_language,
    reset_prompts,
)

# 이 프로세스의 모든 프롬프트를 한국어로 전환
set_prompt_language("ko")

# 현재 활성 언어 확인
print(get_prompt_language())  # -> "ko"

# 다시 영어 기본값으로 복귀
reset_prompts()
print(get_prompt_language())  # -> "en"
```

`set_prompt_language("ko")`는 한국어 템플릿(`raganything.prompts_ko.PROMPTS_KO`)을 자동으로 지연 로딩(lazy-load)한다. 별도 등록 없이 `"en"`, `"zh"`, `"ko"`를 바로 쓸 수 있다.

### 동작 방식과 영어 폴백

- 전환은 전역 `PROMPTS` 딕셔너리를 통째로 교체하는 방식이며, 스레드 락으로 원자적(atomic)으로 처리된다. 따라서 동시 접근 시에도 비어 있거나 일부만 채워진 상태를 읽지 않는다.
- **영어 폴백**: 한국어 템플릿에 없는 키는 자동으로 영어 원본으로 채워진다. 즉 일부 프롬프트만 번역되어 있어도 나머지는 깨지지 않고 영어로 동작한다.
- 전역 스위치이므로, 한 프로세스에서 여러 언어를 동시에 섞어 쓰려면 프로세스를 분리하거나 요청 사이에 명시적으로 전환해야 한다.

### 새 언어/커스텀 프롬프트 등록

직접 만든 프롬프트 집합을 등록하거나 기존 한국어 프롬프트를 덮어쓰려면 `register_prompt_language`를 사용한다. 키는 `raganything.prompt.PROMPTS`와 동일하게 맞춘다.

```python
from raganything.prompt_manager import register_prompt_language, set_prompt_language

my_ko_prompts = {
    "IMAGE_ANALYSIS_SYSTEM": "당신은 한국어로 이미지를 분석하는 전문가입니다. ...",
    # 정의하지 않은 키는 영어로 폴백됨
}

register_prompt_language("ko", my_ko_prompts)
set_prompt_language("ko")
```

> 참고: `get_available_languages()`로 등록·지연 로딩 가능한 언어 목록을 확인할 수 있다.

---

## 4. 한국어 텍스트 유틸 (`raganything.korean_utils`)

`raganything.korean_utils` 모듈은 한국어 정규화·문장 분리·토큰 카운트·형태소 분석과, LightRAG에 꽂아 쓸 수 있는 토크나이저를 제공한다. `kiwipiepy`가 설치되어 있으면 형태소 기반으로, 없으면 순수 파이썬 폴백으로 동작한다.

```python
from raganything.korean_utils import (
    normalize_korean,
    korean_sentence_split,
    count_korean_tokens,
    korean_morphs,
    KoreanTokenizer,
)

# 1) 정규화: 유니코드 정규화·공백 정리 등
text = normalize_korean("한국어   문서를\t정규화합니다.")

# 2) 문장 분리: 한국어 종결부호 기준으로 문장 리스트 반환
sentences = korean_sentence_split("첫 번째 문장입니다. 두 번째 문장이에요!")
# -> ["첫 번째 문장입니다.", "두 번째 문장이에요!"]

# 3) 토큰 수 계산: 청크 크기 산정에 사용
n = count_korean_tokens("한국어 토큰 수를 셉니다.")

# 4) 형태소 분석: kiwipiepy 설치 시 형태소 단위, 미설치 시 폴백
morphs = korean_morphs("한국어 형태소를 분석합니다.")
```

### LightRAG 토크나이저로 사용하기

`KoreanTokenizer`는 `encode`/`decode` 인터페이스를 제공하여 LightRAG의 토크나이저 슬롯에 직접 꽂을 수 있다. 이렇게 하면 청크 분할이 한국어 기준 토큰 수로 계산되어, 영어 BPE로 부풀려지는 문제 없이 적절한 청크 경계를 만든다.

```python
from raganything.korean_utils import KoreanTokenizer

tokenizer = KoreanTokenizer()

ids = tokenizer.encode("한국어 청크 크기를 한국어 기준으로 맞춥니다.")
text = tokenizer.decode(ids)

# LightRAG 인스턴스 생성 시 tokenizer로 주입 (토크나이저 주입은 LightRAG 계층에서 이뤄진다)
from lightrag import LightRAG

rag = LightRAG(
    working_dir="./rag_storage",
    tokenizer=KoreanTokenizer(),
    # llm_model_func, embedding_func 등은 아래 절 참고
)
```

> `kiwipiepy`는 선택 의존성이다. 미설치 환경에서도 `KoreanTokenizer`와 위 함수들은 순수 파이썬 폴백으로 동작하므로 import 에러는 발생하지 않는다. 형태소 정확도가 중요한 경우에만 `pip install kiwipiepy`를 권장한다.

---

## 5. 한국어 OCR (MinerU)

스캔 PDF나 이미지 형태의 한국어 문서는 MinerU의 OCR 언어 설정이 결과 품질을 좌우한다. `process_document_complete`에 MinerU 파라미터 `lang="korean"`을 넘긴다.

```python
await rag.process_document_complete(
    file_path="한국어문서.pdf",
    output_dir="./output",
    parse_method="ocr",      # 스캔 문서는 "ocr", 텍스트 레이어가 있으면 "auto"
    parser="mineru",
    lang="korean",           # 한국어 OCR 최적화
    formula=True,            # 수식 파싱
    table=True,              # 표 파싱
)
```

한국어 문서 처리 팁:

- **텍스트 레이어 유무 판단**: 디지털 PDF(복사 가능한 텍스트)는 `parse_method="auto"`로 충분하고 빠르다. 스캔본·이미지 PDF만 `parse_method="ocr"`로 강제한다.
- **`lang` 값**: MinerU OCR 언어 코드로 한국어는 `"korean"`을 사용한다(영어 위주 문서는 `"en"`). 혼합 문서는 5절·8절의 FAQ를 참고하라.
- **이미지 단일 파일**(JPG/PNG 등)도 같은 방식으로 `lang="korean"`을 지정해 OCR 정확도를 높인다.
- **GPU 가속**: 대량 문서는 `device="cuda:0"` 등을 함께 넘기면 OCR 속도가 크게 개선된다.

> 파서·OCR 관련 일반적인 실패 모드와 디버깅 체크리스트는 [docs/multimodal_rag_failure_modes.md](multimodal_rag_failure_modes.md)에 정리되어 있다.

---

## 6. 한글(HWP/HWPX) 문서 처리

### 왜 필요한가

공공기관·관공서·학술 자료 상당수가 한글(HWP/HWPX) 형식으로 배포된다. 그런데 기본 파이프라인의 핵심 파서인 MinerU는 PDF·이미지·Office 문서를 다룰 뿐 HWP/HWPX는 직접 지원하지 않는다. 그래서 한글 문서를 그대로 넣으면 파싱 단계에서 막힌다. ko-rag-anything은 이 공백을 메우기 위한 **경량 폴백(lightweight fallback)** 변환기를 내장한다.

### 동작 방식(현재 구현 = 경량 폴백)

확장자가 `.hwp`(HWP v5 바이너리)이거나 `.hwpx`(OWPML, 개방형 XML zip)이면 자동으로 감지해 **Markdown으로 먼저 변환**한 뒤, 변환된 `.md`를 기존 마크다운 인덱싱 경로로 그대로 흘려보낸다. 즉 별도 분기를 의식할 필요 없이 `.md`/`.txt`와 동일한 일반 경로를 타게 된다.

- **`.hwpx`** — 표준 라이브러리만으로 처리된다(zip + XML 파싱). 추가 설치가 필요 없다.
- **`.hwp`** — HWP v5 바이너리를 읽기 위해 `pyhwp`가 필요하다. 선택 의존성이므로 한글 `.hwp` 문서를 처리할 때만 설치하면 된다.

```bash
# .hwp(바이너리) 변환에만 필요한 선택 의존성
pip install pyhwp
```

### 사용법

별도 설정 없이 `.hwp`/`.hwpx` 파일 경로를 그대로 `process_document_complete(...)`에 넘기면 위 라우팅이 자동으로 적용된다.

```python
# .hwp / .hwpx 도 PDF·이미지와 똑같이 넘기면 된다 (자동 라우팅)
await rag.process_document_complete(
    file_path="공고문.hwp",     # 또는 "보고서.hwpx"
    output_dir="./output",
)
```

배치 처리에서도 인식되도록 `RAGAnythingConfig`의 `SUPPORTED_FILE_EXTENSIONS` 기본값에 `.hwp,.hwpx`가 이미 포함되어 있다(폴더 일괄 처리 시 한글 문서가 자동으로 대상에 잡힌다).

인덱싱까지 가지 않고 **변환만** 직접 하고 싶다면 변환 함수를 호출한다. 생성된 `.md` 파일 경로를 문자열로 반환한다.

```python
from raganything.hwp import convert_hwp_to_markdown

# convert_hwp_to_markdown(file_path, output_dir=None) -> str
md_path = convert_hwp_to_markdown("문서.hwp")
print(md_path)  # -> 생성된 .md 파일 경로
```

`output_dir`을 생략하면 적당한 위치에 변환 결과를 두고 그 경로를 돌려준다. 필요한 백엔드가 설치되어 있지 않거나 변환에 실패하면 `HwpConversionError`가 발생한다.

```python
from raganything.hwp import (
    HWP_EXTENSIONS,        # {".hwp", ".hwpx"} — 라우팅에 쓰이는 확장자 집합
    HwpConversionError,
    convert_hwp_to_markdown,
)

try:
    md_path = convert_hwp_to_markdown("문서.hwp", output_dir="./output")
except HwpConversionError as e:
    print(f"변환 실패: {e}")  # 예: pyhwp 미설치, 손상된 파일 등
```

### 한계와 권장

현재 경량 경로는 **텍스트와 기본 표 위주**다. 복잡한 표·이미지·수식이 많은 문서는 충실도(fidelity)가 낮아질 수 있다. 다음 사항을 권장한다.

- **표·도표가 많은 문서**: 향후 고품질 경로(**LibreOffice + H2Orestart → PDF → MinerU**)가 권장되나, 이는 **아직 미구현인 향후 계획**이다. 현 시점에서는 경량 폴백만 제공된다.
- **다국어·한자 혼용 문서**: 검색 품질은 임베딩 모델 선택에 크게 좌우된다. 상단 [7절 한국어 임베딩 모델](#7-한국어-임베딩-모델) 및 혼합 언어 관련 팁(아래 FAQ)을 참고해 다국어 임베딩(`BAAI/bge-m3` 등)을 선택한다.

### FAQ

- **`.hwp` 변환이 안 될 때** — `pyhwp`가 설치되어 있는지 확인한다(`pip install pyhwp`). `.hwp` 바이너리 경로는 이 백엔드가 없으면 `HwpConversionError`로 실패한다.
- **`.hwpx`가 깨질 때** — 파일이 표준 OWPML(zip + XML) 형식인지 확인한다. 손상되었거나 비표준으로 저장된 `.hwpx`는 표준 라이브러리 파서가 읽지 못할 수 있다.

---

## 7. 한국어 임베딩 모델

검색 품질은 한국어를 잘 표현하는 임베딩 모델 선택에 거의 전적으로 좌우된다. 권장 모델:

- **`BAAI/bge-m3`** — 다국어(한국어 포함) 강세, 범용적으로 무난한 선택.
- **`nlpai-lab/KURE-v1`** — 한국어에 특화된 임베딩 모델.

임베딩 함수는 **LightRAG 계층의 `EmbeddingFunc`** 로 주입한다. RAGAnythingConfig에는 임베딩 관련 필드가 없으며(설정은 파서·멀티모달·컨텍스트 관련만 보유), 모델 주입은 LightRAG 쪽에서 이뤄진다. 아래는 `sentence-transformers`로 로컬 한국어 임베딩을 꽂는 예시다.

```python
from functools import partial
import numpy as np
from sentence_transformers import SentenceTransformer
from lightrag.utils import EmbeddingFunc
from raganything import RAGAnything, RAGAnythingConfig

# 한국어 임베딩 모델 로드 (예: BAAI/bge-m3 또는 nlpai-lab/KURE-v1)
_model = SentenceTransformer("BAAI/bge-m3")

def korean_embed(texts: list[str]) -> np.ndarray:
    return _model.encode(texts, normalize_embeddings=True)

embedding_func = EmbeddingFunc(
    embedding_dim=1024,        # bge-m3 차원 수 (모델에 맞게 조정)
    max_token_size=8192,
    func=korean_embed,
)

config = RAGAnythingConfig(
    working_dir="./rag_storage",
    parser="mineru",
    parse_method="auto",
)

# RAGAnything에 한국어 임베딩 함수를 전달
rag = RAGAnything(
    config=config,
    llm_model_func=llm_model_func,        # 3·5절 참고
    vision_model_func=vision_model_func,  # 이미지 처리 시
    embedding_func=embedding_func,
)
```

`embedding_dim`은 반드시 선택한 모델의 출력 차원과 일치시켜야 한다(예: `bge-m3`는 1024). 전체적으로 동작하는 구성은 [`examples/korean_example.py`](../examples/korean_example.py)를 참고하라.

> 외부 임베딩 API를 쓰는 경우(예: OpenAI `text-embedding-3-large`)에도 한국어 품질은 떨어질 수 있으므로, 한국어 문서가 주력이라면 위 한국어 특화 모델 사용을 권장한다.

---

## 8. 비용/성능 팁 & 자주 묻는 질문(FAQ)

### 청크 크기

- 영어 BPE 토크나이저는 한국어 토큰 수를 부풀린다. `KoreanTokenizer`(4절)를 LightRAG에 주입하면 청크가 한국어 기준 토큰으로 계산되어, 같은 `max_token_size`라도 더 자연스러운 의미 단위로 잘린다.
- 너무 작은 청크는 문맥을 잃고, 너무 큰 청크는 검색 정밀도와 비용을 해친다. 한국어 일반 문서는 중간 크기로 시작해 검색 품질을 보며 조정하는 것을 권장한다.

### 혼합 언어 문서

- 한·영 혼합 문서는 OCR `lang` 선택이 까다롭다. 한국어 비중이 높으면 `lang="korean"`이 보통 더 안전하다.
- 프롬프트는 전역 스위치이므로(3절), 문서 묶음 단위로 언어를 통일해 처리하거나 프로세스를 분리하는 것이 안정적이다.
- 임베딩은 다국어 모델(`BAAI/bge-m3`)이 혼합 문서에 유리하다.

### 표/수식 처리

- 표·수식은 `enable_table_processing`, `enable_equation_processing`(기본값 `True`)와 MinerU의 `table=True`, `formula=True`로 활성화한다.
- 수식은 LaTeX로 추출되며 언어 의존성이 낮다. 표는 캡션·주석이 한국어일 때 한국어 프롬프트(3절)를 켜두면 요약·엔티티 추출 품질이 좋아진다.
- 멀티모달 콘텐츠가 잘 처리되지 않을 때의 점검 항목은 [docs/multimodal_rag_failure_modes.md](multimodal_rag_failure_modes.md)를 참고하라.

### 비용 절감

- `kiwipiepy` 기반 토크나이징과 적절한 청크 크기로 불필요한 토큰 팽창을 줄이면 LLM·임베딩 호출 비용이 절감된다.
- 로컬 한국어 임베딩 모델을 쓰면 임베딩 API 비용을 0으로 만들 수 있다(대신 GPU/메모리 자원 필요).
- 오프라인·네트워크 제한 환경에서는 `tiktoken` 캐시 설정이 필요하다. [docs/offline_setup.md](offline_setup.md)를 참고하라.

---

## 9. 참고

- 한국어 README: [README_ko.md](../README_ko.md)
- 한국어 예제 스크립트: [`examples/korean_example.py`](../examples/korean_example.py)
- 영어 전체 가이드: [README.md](../README.md)
- 멀티모달 실패 모드 체크리스트: [docs/multimodal_rag_failure_modes.md](multimodal_rag_failure_modes.md)
- 오프라인 환경 설정: [docs/offline_setup.md](offline_setup.md)
