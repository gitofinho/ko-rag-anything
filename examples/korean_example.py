#!/usr/bin/env python
"""한국어 문서 처리용 RAGAnything 엔드투엔드 예제.

이 스크립트는 `raganything_example.py`의 구조를 그대로 따르되, 한국어 문서에
맞게 다음을 보여 준다.

1. `set_prompt_language("ko")` 로 멀티모달/질의 프롬프트를 한국어로 전환
2. MinerU 파서에 한국어 OCR 설정(`lang="korean"`)을 전달
3. 한국어에 강한 임베딩 모델(`BAAI/bge-m3`, 대안: `nlpai-lab/KURE-v1`) 배선
4. `normalize_korean` 으로 입력 텍스트를 정규화하고, 가능하면
   `KoreanTokenizer` 를 토크나이저로 주입
5. 한국어 샘플 질의로 텍스트/멀티모달 질의 시연

무거운 의존성(lightrag, mineru, raganything 본체)은 `main()`/함수 내부에서
임포트하므로, 해당 패키지가 설치돼 있지 않아도 `python3 -m py_compile` 과
`--help` 는 동작한다.
"""

import os
import argparse
import asyncio
import logging
import logging.config
from functools import partial
from pathlib import Path

# 프로젝트 루트를 파이썬 경로에 추가
import sys

sys.path.append(str(Path(__file__).parent.parent))


def _load_dotenv():
    """`.env` 파일을 로드한다(설치돼 있을 때만)."""
    try:
        from dotenv import load_dotenv

        load_dotenv(dotenv_path=".env", override=False)
    except ImportError:
        # python-dotenv 가 없어도 환경변수만으로 동작하도록 무시한다.
        pass


def configure_logging():
    """애플리케이션 로깅 설정"""
    # 로그 디렉터리 경로를 환경변수에서 읽거나 현재 디렉터리 사용
    log_dir = os.getenv("LOG_DIR", os.getcwd())
    log_file_path = os.path.abspath(os.path.join(log_dir, "korean_example.log"))

    print(f"\nRAGAnything 한국어 예제 로그 파일: {log_file_path}\n")
    os.makedirs(os.path.dirname(log_file_path) or ".", exist_ok=True)

    # 로그 파일 최대 크기/백업 개수를 환경변수에서 읽음
    log_max_bytes = int(os.getenv("LOG_MAX_BYTES", 10485760))  # 기본 10MB
    log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5))  # 기본 5개

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(levelname)s: %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "file": {
                    "formatter": "detailed",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "maxBytes": log_max_bytes,
                    "backupCount": log_backup_count,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "lightrag": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )

    # lightrag 로거 레벨을 INFO 로 설정(설치돼 있을 때만)
    try:
        from lightrag.utils import logger, set_verbose_debug

        logger.setLevel(logging.INFO)
        # 필요하면 상세 디버그 활성화
        set_verbose_debug(os.getenv("VERBOSE", "false").lower() == "true")
    except ImportError:
        pass


async def process_with_rag(
    file_path: str,
    output_dir: str,
    api_key: str,
    base_url: str = None,
    working_dir: str = None,
    parser: str = None,
    lang: str = "korean",
):
    """RAGAnything 으로 한국어 문서를 처리한다.

    Args:
        file_path: 처리할 문서 경로
        output_dir: RAG 결과 출력 디렉터리
        api_key: OpenAI 호환 API 키
        base_url: 선택적 API base URL
        working_dir: RAG 저장소 작업 디렉터리
        parser: 파서 선택(mineru, docling, paddleocr)
        lang: 파서 OCR 언어 힌트(한국어 문서는 "korean")
    """
    # --- 무거운 의존성은 여기서 지연 임포트 ---
    from lightrag.llm.openai import openai_complete_if_cache, openai_embed
    from lightrag.utils import EmbeddingFunc, logger
    from raganything import RAGAnything, RAGAnythingConfig

    # 프롬프트 언어를 한국어로 전환 → 멀티모달 캡션/질의 프롬프트가 한국어로 생성됨
    from raganything.prompt_manager import set_prompt_language

    set_prompt_language("ko")

    # 한국어 텍스트 유틸리티(정규화/문장분리/토크나이저).
    # 이 모듈이 아직 없는 환경에서도 예제가 죽지 않도록 안전하게 처리한다.
    try:
        from raganything.korean_utils import (
            normalize_korean,
            korean_sentence_split,
            KoreanTokenizer,
        )

        korean_utils_available = True
    except ImportError:
        logger.warning(
            "raganything.korean_utils 를 찾을 수 없습니다. "
            "한국어 정규화/토크나이저 없이 진행합니다."
        )
        normalize_korean = None
        korean_sentence_split = None
        KoreanTokenizer = None
        korean_utils_available = False

    try:
        # RAGAnything 설정 생성
        config = RAGAnythingConfig(
            working_dir=working_dir or "./rag_storage",
            parser=parser,  # 파서 선택: mineru, docling, paddleocr
            parse_method="auto",  # 파싱 방법: auto, ocr, txt
            enable_image_processing=True,
            enable_table_processing=True,
            enable_equation_processing=True,
        )

        # LLM 모델 함수 정의
        llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        vision_model = os.getenv("VISION_MODEL", "gpt-4o")

        def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return openai_complete_if_cache(
                llm_model,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs,
            )

        # 이미지 처리용 비전 모델 함수 정의
        def vision_model_func(
            prompt,
            system_prompt=None,
            history_messages=[],
            image_data=None,
            messages=None,
            **kwargs,
        ):
            # messages 포맷이 주어지면(멀티모달 VLM 질의) 그대로 사용
            if messages:
                return openai_complete_if_cache(
                    vision_model,
                    "",
                    system_prompt=None,
                    history_messages=[],
                    messages=messages,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs,
                )
            # 단일 이미지 포맷
            elif image_data:
                return openai_complete_if_cache(
                    vision_model,
                    "",
                    system_prompt=None,
                    history_messages=[],
                    messages=[
                        {"role": "system", "content": system_prompt}
                        if system_prompt
                        else None,
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_data}"
                                    },
                                },
                            ],
                        }
                        if image_data
                        else {"role": "user", "content": prompt},
                    ],
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs,
                )
            # 순수 텍스트 포맷
            else:
                return llm_model_func(prompt, system_prompt, history_messages, **kwargs)

        # 임베딩 함수 정의 - 환경변수로 설정
        #
        # 한국어 권장 임베딩 모델:
        #   - 기본: BAAI/bge-m3 (다국어, 한국어 성능 우수, embedding_dim=1024)
        #   - 대안: nlpai-lab/KURE-v1 (한국어 특화, 강력한 한국어 검색 성능)
        #
        # OpenAI 호환 엔드포인트(예: vLLM/Ollama 의 /v1)로 bge-m3 를 서빙하면
        # 아래 openai_embed 그대로 사용 가능하다. EMBEDDING_MODEL 환경변수에
        # 한국어 모델 이름을 넣고, EMBEDDING_DIM 을 모델 차원에 맞추면 된다.
        embedding_dim = int(os.getenv("EMBEDDING_DIM", "1024"))  # bge-m3 = 1024
        embedding_model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

        embedding_func = EmbeddingFunc(
            embedding_dim=embedding_dim,
            max_token_size=8192,
            func=partial(
                openai_embed.func,
                model=embedding_model,
                api_key=api_key,
                base_url=base_url,
            ),
        )

        # 새 dataclass 구조로 RAGAnything 초기화
        rag = RAGAnything(
            config=config,
            llm_model_func=llm_model_func,
            vision_model_func=vision_model_func,
            embedding_func=embedding_func,
        )

        # 한국어 토크나이저 주입(선택):
        # LightRAG 는 인스턴스의 tokenizer 속성으로 청크 토큰 계산을 수행한다.
        # KoreanTokenizer 는 encode/decode 를 제공하는 LightRAG 호환 토크나이저로,
        # 내부 LightRAG 인스턴스 생성 후 교체할 수 있다. 예제 수준에서는 내부
        # 인스턴스가 lazy 하게 만들어지므로, 직접 주입 API 가 노출되지 않은 경우
        # 아래처럼 안전하게 시도만 한다.
        if korean_utils_available and KoreanTokenizer is not None:
            try:
                lightrag_inst = getattr(rag, "lightrag", None)
                if lightrag_inst is not None and hasattr(lightrag_inst, "tokenizer"):
                    lightrag_inst.tokenizer = KoreanTokenizer()
                    logger.info("KoreanTokenizer 를 LightRAG 토크나이저로 주입했습니다.")
                else:
                    logger.info(
                        "LightRAG 토크나이저 직접 주입 지점이 노출되지 않아 "
                        "기본 토크나이저를 사용합니다."
                    )
            except Exception as exc:  # noqa: BLE001
                logger.info(f"토크나이저 주입을 건너뜁니다: {exc}")

        # 문서 처리 - 한국어 OCR 을 위해 lang 을 파서로 전달(MinerU: -l korean)
        await rag.process_document_complete(
            file_path=file_path,
            output_dir=output_dir,
            parse_method="auto",
            lang=lang,
        )

        # 예제 질의 - 다양한 질의 방식 시연
        logger.info("\n처리된 문서에 질의합니다:")

        # 1. aquery() 를 사용한 순수 텍스트 질의(한국어)
        text_queries = [
            "이 문서의 핵심 내용은 무엇인가요?",
            "문서에서 다루는 주요 주제를 정리해 주세요.",
            "결론에서 강조하는 시사점은 무엇인가요?",
        ]

        for query in text_queries:
            # 입력 질의를 한국어 정규화(자모 결합/공백 정리 등)
            normalized_query = (
                normalize_korean(query)
                if (korean_utils_available and normalize_korean)
                else query
            )
            logger.info(f"\n[텍스트 질의]: {normalized_query}")
            result = await rag.aquery(normalized_query, mode="hybrid")
            logger.info(f"답변: {result}")

            # 답변 문장 분리 데모(유틸리티가 있을 때만)
            if korean_utils_available and korean_sentence_split and isinstance(result, str):
                sentences = korean_sentence_split(result)
                logger.info(f"(답변 문장 수: {len(sentences)})")

        # 2. aquery_with_multimodal() 로 표 데이터 멀티모달 질의(한국어)
        logger.info("\n[멀티모달 질의]: 문서 맥락에서 성능 데이터 분석")
        multimodal_result = await rag.aquery_with_multimodal(
            "이 성능 데이터를 문서에 언급된 유사한 결과와 비교해 설명해 주세요.",
            multimodal_content=[
                {
                    "type": "table",
                    "table_data": """방법,정확도,처리시간
                                RAGAnything,95.2%,120ms
                                기존_RAG,87.3%,180ms
                                베이스라인,82.1%,200ms""",
                    "table_caption": "성능 비교 결과",
                }
            ],
            mode="hybrid",
        )
        logger.info(f"답변: {multimodal_result}")

        # 3. 수식 콘텐츠 멀티모달 질의(한국어)
        logger.info("\n[멀티모달 질의]: 수식 분석")
        equation_result = await rag.aquery_with_multimodal(
            "이 수식을 설명하고 문서에 나오는 수학적 개념과 연관 지어 주세요.",
            multimodal_content=[
                {
                    "type": "equation",
                    "latex": "F1 = 2 \\cdot \\frac{precision \\cdot recall}{precision + recall}",
                    "equation_caption": "F1 점수 계산 수식",
                }
            ],
            mode="hybrid",
        )
        logger.info(f"답변: {equation_result}")

    except Exception as e:
        logger.error(f"RAG 처리 중 오류: {str(e)}")
        import traceback

        logger.error(traceback.format_exc())


def main():
    """예제 실행 메인 함수"""
    parser = argparse.ArgumentParser(description="MinerU 한국어 RAG 예제")
    parser.add_argument("file_path", help="처리할 문서 경로")
    parser.add_argument(
        "--working_dir", "-w", default="./rag_storage", help="작업 디렉터리 경로"
    )
    parser.add_argument(
        "--output", "-o", default="./output", help="출력 디렉터리 경로"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("LLM_BINDING_API_KEY"),
        help="OpenAI 호환 API 키 (기본값: LLM_BINDING_API_KEY 환경변수)",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("LLM_BINDING_HOST"),
        help="선택적 API base URL",
    )
    parser.add_argument(
        "--parser",
        default=os.getenv("PARSER", "mineru"),
        help=(
            "파서 선택. 내장: mineru, docling, paddleocr. "
            "register_parser() 로 동일 프로세스에 등록한 커스텀 파서도 "
            "라이브러리로 사용할 때 허용된다. 이 예제는 플러그인 자동 탐색을 "
            "수행하지 않는다."
        ),
    )
    parser.add_argument(
        "--lang",
        default=os.getenv("PARSE_LANG", "korean"),
        help=(
            "파서 OCR 언어 힌트. 한국어 문서는 'korean'(MinerU 는 -l korean 으로 전달). "
            "기본값: PARSE_LANG 환경변수 또는 'korean'."
        ),
    )

    args = parser.parse_args()

    # API 키 확인
    if not args.api_key:
        print("오류: OpenAI 호환 API 키가 필요합니다.")
        print("API 키 환경변수를 설정하거나 --api-key 옵션을 사용하세요.")
        return

    # 출력 디렉터리 생성
    if args.output:
        os.makedirs(args.output, exist_ok=True)

    # RAG 처리 실행
    asyncio.run(
        process_with_rag(
            args.file_path,
            args.output,
            args.api_key,
            args.base_url,
            args.working_dir,
            args.parser,
            args.lang,
        )
    )


if __name__ == "__main__":
    # .env 로드 후 로깅 설정
    _load_dotenv()
    configure_logging()

    print("RAGAnything 한국어 예제")
    print("=" * 30)
    print("멀티모달 RAG 파이프라인으로 한국어 문서 처리")
    print("=" * 30)

    main()
