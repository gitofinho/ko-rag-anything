<div align="center">

<div style="margin: 20px 0;">
  <img src="./assets/logo.png" width="120" height="120" alt="RAG-Anything Logo" style="border-radius: 20px; box-shadow: 0 8px 32px rgba(0, 217, 255, 0.3);">
</div>

# 🚀 RAG-Anything: 올인원 RAG 프레임워크

<a href="https://trendshift.io/repositories/14959" target="_blank"><img src="https://trendshift.io/api/badge/repositories/14959" alt="HKUDS%2FRAG-Anything | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=24&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=600&lines=Welcome+to+RAG-Anything;Next-Gen+Multimodal+RAG+System;Powered+by+Advanced+AI+Technology" alt="Typing Animation" />
</div>

<div align="center">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 25px; text-align: center;">
    <p>
      <a href='https://github.com/HKUDS/RAG-Anything'><img src='https://img.shields.io/badge/🔥Project-Page-00d9ff?style=for-the-badge&logo=github&logoColor=white&labelColor=1a1a2e'></a>
      <a href='https://arxiv.org/abs/2510.12323'><img src='https://img.shields.io/badge/📄arXiv-2510.12323-ff6b6b?style=for-the-badge&logo=arxiv&logoColor=white&labelColor=1a1a2e'></a>
      <a href='https://github.com/HKUDS/LightRAG'><img src='https://img.shields.io/badge/⚡Based%20on-LightRAG-4ecdc4?style=for-the-badge&logo=lightning&logoColor=white&labelColor=1a1a2e'></a>
    </p>
    <p>
      <a href="https://github.com/HKUDS/RAG-Anything/stargazers"><img src='https://img.shields.io/github/stars/HKUDS/RAG-Anything?color=00d9ff&style=for-the-badge&logo=star&logoColor=white&labelColor=1a1a2e' /></a>
      <img src="https://img.shields.io/badge/🐍Python-3.10-4ecdc4?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e">
      <a href="https://pypi.org/project/raganything/"><img src="https://img.shields.io/pypi/v/raganything.svg?style=for-the-badge&logo=pypi&logoColor=white&labelColor=1a1a2e&color=ff6b6b"></a>
      <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/⚡uv-Ready-ff6b6b?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e"></a>
    </p>
    <p>
      <a href="https://discord.gg/yF2MmDJyGJ"><img src="https://img.shields.io/badge/💬Discord-Community-7289da?style=for-the-badge&logo=discord&logoColor=white&labelColor=1a1a2e"></a>
      <a href="https://github.com/HKUDS/RAG-Anything/issues/7"><img src="https://img.shields.io/badge/💬WeChat-Group-07c160?style=for-the-badge&logo=wechat&logoColor=white&labelColor=1a1a2e"></a>
    </p>
    <p>
      <a href="README_zh.md"><img src="https://img.shields.io/badge/🇨🇳中文版-1a1a2e?style=for-the-badge"></a>
      <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸English-1a1a2e?style=for-the-badge"></a>
      <a href="README_ko.md"><img src="https://img.shields.io/badge/🇰🇷한국어-1a1a2e?style=for-the-badge"></a>
    </p>
    <p>
      <a href="https://pepy.tech/projects/raganything"><img src="https://static.pepy.tech/personalized-badge/raganything?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads"></a>
    </p>
  </div>
</div>

</div>

<div align="center">
  <div style="width: 100%; height: 2px; margin: 20px 0; background: linear-gradient(90deg, transparent, #00d9ff, transparent);"></div>
</div>

<div align="center">
  <a href="#-빠른-시작" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/Quick%20Start-Get%20Started%20Now-00d9ff?style=for-the-badge&logo=rocket&logoColor=white&labelColor=1a1a2e">
  </a>
</div>

---

<div align="center">
  <table>
    <tr>
      <td style="vertical-align: middle;">
        <img src="./assets/LiteWrite.png"
             width="56"
             height="56"
             alt="LiteWrite"
             style="border-radius: 12px;" />
      </td>
      <td style="vertical-align: middle; padding-left: 12px;">
        <a href="https://litewrite.ai">
          <img src="https://img.shields.io/badge/🚀%20LiteWrite-AI%20Native%20LaTeX%20Editor-ff6b6b?style=for-the-badge&logoColor=white&labelColor=1a1a2e">
        </a>
      </td>
    </tr>
  </table>
</div>

---

## 🇰🇷 ko-rag-anything 소개

**ko-rag-anything**는 [HKUDS/RAG-Anything](https://github.com/HKUDS/RAG-Anything)을 기반으로 한국어 RAG 환경에 맞춰 강화한 포크입니다. 상위 프로젝트의 모든 멀티모달 기능을 그대로 유지하면서, 한국어 문서 처리·검색 품질을 끌어올리기 위한 다음 기능들을 추가로 제공합니다.

- **한국어 프롬프트 템플릿** — `raganything.prompt_manager`의 `set_prompt_language("ko")`를 호출하면 이미지 분석, 표 해석, 엔티티 추출 등 파이프라인 전반의 프롬프트를 한국어로 전환합니다. (사용 가능한 언어가 없을 경우 `register_prompt_language()`로 직접 등록할 수 있습니다.)
- **한국어 텍스트 유틸리티** — `raganything.korean_utils`는 정규화(normalization), 문장 분리, 한국어 인식 토크나이저를 제공하며, 선택적으로 `kiwipiepy` 기반 형태소 분석을 활용할 수 있습니다.
- **한국어 임베딩·OCR 가이드** — `BAAI/bge-m3`, `nlpai-lab/KURE-v1`처럼 한국어를 잘 지원하는 임베딩 모델과, `lang="korean"` 옵션을 적용한 MinerU OCR 사용을 권장합니다.

자세한 사용 방법은 [`docs/korean.md`](docs/korean.md) 가이드와 [`examples/korean_example.py`](examples/korean_example.py) 예제를 참고하세요.

---

## 🎉 소식
- [X] [2025.10]🎯📢 🚀 [RAG-Anything](http://arxiv.org/abs/2510.12323)의 기술 보고서를 공개했습니다. 지금 확인하고 최신 연구 성과를 살펴보세요.
- [X] [2025.08]🎯📢 🔍 RAG-Anything이 **VLM 강화 질의(VLM-Enhanced Query)** 모드를 지원합니다! 문서에 이미지가 포함되어 있으면 시스템이 이를 VLM에 매끄럽게 통합하여 시각적·텍스트적 문맥을 결합한 고급 멀티모달 분석으로 더 깊은 인사이트를 제공합니다.
- [X] [2025.07]🎯📢 RAG-Anything에 [컨텍스트 구성 모듈](docs/context_aware_processing.md)이 추가되어, 관련 문맥 정보를 지능적으로 통합해 멀티모달 콘텐츠 처리를 향상시킵니다.
- [X] [2025.07]🎯📢 🚀 RAG-Anything이 멀티모달 질의 기능을 지원하여, 텍스트·이미지·표·수식을 매끄럽게 처리하는 강화된 RAG를 구현했습니다.
- [X] [2025.07]🎯📢 🎉 RAG-Anything이 GitHub에서 1k🌟 스타를 달성했습니다! 변함없는 성원과 소중한 기여에 감사드립니다.

---

## 🌟 시스템 개요

*차세대 멀티모달 인텔리전스*

<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border-radius: 15px; padding: 25px; margin: 20px 0; border: 2px solid #00d9ff; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);">

현대의 문서는 텍스트, 이미지, 표, 수식, 차트, 멀티미디어 등 점점 더 다양한 멀티모달 콘텐츠를 담고 있으며, 텍스트 중심의 전통적인 RAG 시스템으로는 이를 효과적으로 처리하기 어렵습니다. **RAG-Anything**은 [LightRAG](https://github.com/HKUDS/LightRAG) 위에 구축된 종합 **올인원 멀티모달 문서 처리 RAG 시스템**으로서 이 과제를 해결합니다.

통합 솔루션인 RAG-Anything은 **여러 전문 도구를 따로 사용할 필요를 없애 줍니다**. 하나의 통합된 프레임워크 안에서 **모든 콘텐츠 모달리티에 걸친 매끄러운 처리와 질의**를 제공합니다. 비텍스트 요소를 다루는 데 어려움을 겪는 기존 RAG 방식과 달리, 본 올인원 시스템은 **종합적인 멀티모달 검색 기능**을 제공합니다.

사용자는 **텍스트가 뒤섞인 콘텐츠**, **시각적 다이어그램**, **구조화된 표**, **수학적 표현**이 포함된 문서를 **하나의 일관된 인터페이스**로 질의할 수 있습니다. 이러한 통합 접근 방식 덕분에 RAG-Anything은 풍부한 혼합 콘텐츠 문서가 **통합 처리 프레임워크**를 요구하는 학술 연구, 기술 문서, 재무 보고서, 기업 지식 관리 분야에서 특히 유용합니다.

<img src="assets/rag_anything_framework.png" alt="RAG-Anything" />

</div>

### 🎯 핵심 기능

<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; padding: 25px; margin: 20px 0;">

- **🔄 엔드투엔드 멀티모달 파이프라인** - 문서 수집과 파싱부터 지능적인 멀티모달 질의 응답까지 이어지는 완전한 워크플로
- **📄 범용 문서 지원** - PDF, Office 문서, 이미지 등 다양한 파일 형식의 매끄러운 처리
- **🧠 특화된 콘텐츠 분석** - 이미지, 표, 수학 수식, 이질적인 콘텐츠 유형을 위한 전용 프로세서
- **🔗 멀티모달 지식 그래프** - 자동 엔티티 추출과 모달 간 관계 발견으로 이해도 향상
- **⚡ 적응형 처리 모드** - 유연한 MinerU 기반 파싱 또는 직접 멀티모달 콘텐츠 주입 워크플로
- **📋 콘텐츠 리스트 직접 삽입** - 외부 소스에서 미리 파싱한 콘텐츠 리스트를 직접 삽입하여 문서 파싱 단계를 생략
- **🎯 하이브리드 지능형 검색** - 문맥 이해를 바탕으로 텍스트와 멀티모달 콘텐츠를 아우르는 고급 검색 기능
- **🇰🇷 한국어 강화** - 한국어 프롬프트 템플릿(`set_prompt_language("ko")`), 한국어 텍스트 유틸리티(`raganything.korean_utils`), 한국어 임베딩·OCR 가이드 제공

</div>

---

## 🏗️ 알고리즘 및 아키텍처

<div style="background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%); border-radius: 15px; padding: 25px; margin: 20px 0; border-left: 5px solid #00d9ff;">

### 핵심 알고리즘

**RAG-Anything**은 전통적인 RAG 아키텍처를 근본적으로 확장하는 효과적인 **다단계 멀티모달 파이프라인**을 구현하여, 지능적인 오케스트레이션과 모달 간 이해를 통해 다양한 콘텐츠 모달리티를 매끄럽게 처리합니다.

</div>

<div align="center">
  <div style="width: 100%; max-width: 600px; margin: 20px auto; padding: 20px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2);">
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">📄</div>
        <div style="font-size: 14px; color: #00d9ff;">Document Parsing</div>
      </div>
      <div style="font-size: 20px; color: #00d9ff;">→</div>
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🧠</div>
        <div style="font-size: 14px; color: #00d9ff;">Content Analysis</div>
      </div>
      <div style="font-size: 20px; color: #00d9ff;">→</div>
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🔍</div>
        <div style="font-size: 14px; color: #00d9ff;">Knowledge Graph</div>
      </div>
      <div style="font-size: 20px; color: #00d9ff;">→</div>
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🎯</div>
        <div style="font-size: 14px; color: #00d9ff;">Intelligent Retrieval</div>
      </div>
    </div>
  </div>
</div>

### 1. 문서 파싱 단계

<div style="background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #4ecdc4;">

시스템은 적응형 콘텐츠 분해를 통해 고충실도의 문서 추출을 제공합니다. 문맥적 관계를 보존하면서 이질적인 요소를 지능적으로 분할합니다. 전문화되고 최적화된 파서를 통해 범용 형식 호환성을 달성합니다.

**핵심 구성 요소:**

- **⚙️ MinerU 통합**: [MinerU](https://github.com/opendatalab/MinerU)를 활용하여 복잡한 레이아웃에서도 고충실도의 문서 구조 추출과 의미 보존을 수행합니다.

- **🧩 적응형 콘텐츠 분해**: 문맥적 관계를 보존하면서 문서를 일관된 텍스트 블록, 시각적 요소, 구조화된 표, 수학 수식, 특수 콘텐츠 유형으로 자동 분할합니다.

- **📁 범용 형식 지원**: 형식별 최적화를 갖춘 전문 파서를 통해 PDF, Office 문서(DOC/DOCX/PPT/PPTX/XLS/XLSX), 이미지 및 신규 형식을 폭넓게 처리합니다.

</div>

### 2. 멀티모달 콘텐츠 이해 및 처리

<div style="background: linear-gradient(90deg, #16213e 0%, #0f3460 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #ff6b6b;">

시스템은 콘텐츠를 자동으로 분류하고 최적화된 채널로 라우팅합니다. 텍스트와 멀티모달 처리를 병렬화하기 위해 동시 파이프라인을 사용합니다. 변환 과정에서 문서 계층 구조와 관계가 보존됩니다.

**핵심 구성 요소:**

- **🎯 자율적 콘텐츠 분류 및 라우팅**: 서로 다른 콘텐츠 유형을 자동으로 식별·분류하고 최적화된 실행 채널로 라우팅합니다.

- **⚡ 동시 다중 파이프라인 아키텍처**: 전용 처리 파이프라인을 통해 텍스트 콘텐츠와 멀티모달 콘텐츠를 동시에 실행합니다. 이 방식은 콘텐츠 무결성을 유지하면서 처리량 효율을 극대화합니다.

- **🏗️ 문서 계층 구조 추출**: 콘텐츠 변환 과정에서 원본 문서의 계층 구조와 요소 간 관계를 추출·보존합니다.

</div>

### 3. 멀티모달 분석 엔진

<div style="background: linear-gradient(90deg, #0f3460 0%, #1a1a2e 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #00d9ff;">

시스템은 이질적인 데이터 모달리티를 위해 모달리티 인식 처리 유닛을 배치합니다:

**전문 분석기:**

- **🔍 시각 콘텐츠 분석기(Visual Content Analyzer)**:
  - 이미지 분석을 위해 비전 모델을 통합합니다.
  - 시각적 의미를 기반으로 문맥 인식 설명 캡션을 생성합니다.
  - 시각적 요소 간의 공간적 관계와 계층 구조를 추출합니다.

- **📊 구조화 데이터 해석기(Structured Data Interpreter)**:
  - 표 및 구조화된 데이터 형식을 체계적으로 해석합니다.
  - 데이터 추세 분석을 위한 통계적 패턴 인식 알고리즘을 구현합니다.
  - 여러 표 데이터셋 전반에 걸친 의미적 관계와 의존성을 식별합니다.

- **📐 수학 표현 파서(Mathematical Expression Parser)**:
  - 복잡한 수학 표현과 공식을 높은 정확도로 파싱합니다.
  - 학술 워크플로와의 매끄러운 통합을 위해 네이티브 LaTeX 형식을 지원합니다.
  - 수학 수식과 도메인별 지식 베이스 간의 개념적 매핑을 구축합니다.

- **🔧 확장형 모달리티 핸들러(Extensible Modality Handler)**:
  - 사용자 정의 및 신규 콘텐츠 유형을 위한 구성 가능한 처리 프레임워크를 제공합니다.
  - 플러그인 아키텍처를 통해 새로운 모달리티 프로세서를 동적으로 통합할 수 있습니다.
  - 특수 사용 사례를 위한 처리 파이프라인의 런타임 구성을 지원합니다.

</div>

### 4. 멀티모달 지식 그래프 인덱스

<div style="background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #4ecdc4;">

멀티모달 지식 그래프 구축 모듈은 문서 콘텐츠를 구조화된 의미 표현으로 변환합니다. 멀티모달 엔티티를 추출하고, 모달 간 관계를 설정하며, 계층적 구조를 보존합니다. 시스템은 최적화된 지식 검색을 위해 가중 관련도 점수화를 적용합니다.

**핵심 기능:**

- **🔍 멀티모달 엔티티 추출**: 중요한 멀티모달 요소를 구조화된 지식 그래프 엔티티로 변환합니다. 이 과정에는 의미 주석과 메타데이터 보존이 포함됩니다.

- **🔗 모달 간 관계 매핑**: 텍스트 엔티티와 멀티모달 구성 요소 사이에 의미적 연결과 의존성을 설정합니다. 이는 자동화된 관계 추론 알고리즘을 통해 이루어집니다.

- **🏗️ 계층 구조 보존**: "belongs_to" 관계 체인을 통해 원본 문서 구성을 유지합니다. 이 체인은 논리적 콘텐츠 계층과 섹션 간 의존성을 보존합니다.

- **⚖️ 가중 관계 점수화**: 관계 유형에 정량적 관련도 점수를 부여합니다. 점수는 문서 구조 내의 의미적 근접성과 문맥적 중요도를 기반으로 산정됩니다.

</div>

### 5. 모달리티 인식 검색

<div style="background: linear-gradient(90deg, #16213e 0%, #0f3460 100%); border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #ff6b6b;">

하이브리드 검색 시스템은 종합적인 콘텐츠 검색을 위해 벡터 유사도 검색과 그래프 순회 알고리즘을 결합합니다. 모달리티 인식 랭킹 메커니즘을 구현하고 검색된 요소 간의 관계적 일관성을 유지하여, 문맥적으로 통합된 정보 전달을 보장합니다.

**검색 메커니즘:**

- **🔀 벡터-그래프 융합**: 벡터 유사도 검색과 그래프 순회 알고리즘을 통합합니다. 이 방식은 의미 임베딩과 구조적 관계를 모두 활용하여 종합적인 콘텐츠 검색을 수행합니다.

- **📊 모달리티 인식 랭킹**: 콘텐츠 유형의 관련성에 따라 검색 결과에 가중치를 부여하는 적응형 점수화 메커니즘을 구현합니다. 시스템은 질의별 모달리티 선호도에 맞춰 랭킹을 조정합니다.

- **🔗 관계적 일관성 유지**: 검색된 요소 간의 의미적·구조적 관계를 유지합니다. 이를 통해 일관된 정보 전달과 문맥 무결성을 보장합니다.

</div>

---

## 🚀 빠른 시작

*AI 여정을 시작하세요*

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">
</div>

### 설치

#### 옵션 1: PyPI에서 설치 (권장)

```bash
# 기본 설치
pip install raganything

# 확장 형식 지원을 위한 선택적 의존성과 함께 설치:
pip install 'raganything[all]'              # 모든 선택적 기능
pip install 'raganything[image]'            # 이미지 형식 변환 (BMP, TIFF, GIF, WebP)
pip install 'raganything[text]'             # 텍스트 파일 처리 (TXT, MD)
pip install 'raganything[image,text]'       # 여러 기능 동시 선택
```

#### 옵션 2: 소스에서 설치
```bash
# uv 설치 (아직 설치하지 않은 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh

# uv로 프로젝트 클론 및 설정
git clone https://github.com/HKUDS/RAG-Anything.git
cd RAG-Anything

# 가상 환경에 패키지와 의존성 설치
uv sync

# 네트워크 타임아웃이 발생하는 경우 (특히 opencv 패키지):
# UV_HTTP_TIMEOUT=120 uv sync

# uv로 직접 명령 실행 (권장 방식)
uv run python examples/raganything_example.py --help

# 선택적 의존성과 함께 설치
uv sync --extra image --extra text  # 특정 extras
uv sync --all-extras                 # 모든 선택적 기능
```

#### 선택적 의존성

- **`[image]`** - BMP, TIFF, GIF, WebP 이미지 형식 처리 지원 (Pillow 필요)
- **`[text]`** - TXT 및 MD 파일 처리 지원 (ReportLab 필요)
- **`[all]`** - 모든 Python 선택적 의존성 포함

> **⚠️ Office 문서 처리 요구 사항:**
> - Office 문서(.doc, .docx, .ppt, .pptx, .xls, .xlsx)는 **LibreOffice** 설치가 필요합니다
> - [LibreOffice 공식 웹사이트](https://www.libreoffice.org/download/download/)에서 다운로드하세요
> - **Windows**: 공식 웹사이트에서 설치 프로그램 다운로드
> - **macOS**: `brew install --cask libreoffice`
> - **Ubuntu/Debian**: `sudo apt-get install libreoffice`
> - **CentOS/RHEL**: `sudo yum install libreoffice`

**MinerU 설치 확인:**

```bash
# 설치 확인
mineru --version

# 올바르게 구성되었는지 확인
python -c "from raganything import RAGAnything; rag = RAGAnything(); print('✅ MinerU installed properly' if rag.check_parser_installation() else '❌ MinerU installation issue')"
```

모델은 최초 사용 시 자동으로 다운로드됩니다. 수동 다운로드는 [MinerU Model Source Configuration](https://github.com/opendatalab/MinerU/blob/master/README.md#22-model-source-configuration)을 참고하세요.

> **🇰🇷 한국어 문서 팁:** 한국어 문서를 OCR 처리할 때는 MinerU에 `lang="korean"` 옵션을 전달하면 인식 정확도가 향상됩니다. 또한 한국어를 잘 지원하는 임베딩 모델(예: `BAAI/bge-m3`, `nlpai-lab/KURE-v1`)을 사용하는 것을 권장합니다. 자세한 내용은 [`docs/korean.md`](docs/korean.md)를 참고하세요.

### 사용 예제

#### 1. 엔드투엔드 문서 처리

```python
import asyncio
from functools import partial
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc

async def main():
    # API 구성 설정
    api_key = "your-api-key"
    base_url = "your-base-url"  # 선택 사항

    # RAGAnything 구성 생성
    config = RAGAnythingConfig(
        working_dir="./rag_storage",
        parser="mineru",  # 파서 선택: mineru, docling, 또는 paddleocr
        parse_method="auto",  # 파싱 방법: auto, ocr, 또는 txt
        enable_image_processing=True,
        enable_table_processing=True,
        enable_equation_processing=True,
    )

    # LLM 모델 함수 정의
    def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
        return openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )

    # 이미지 처리를 위한 비전 모델 함수 정의
    def vision_model_func(
        prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs
    ):
        # messages 형식이 제공되면 (멀티모달 VLM 강화 질의용) 그대로 사용
        if messages:
            return openai_complete_if_cache(
                "gpt-4o",
                "",
                system_prompt=None,
                history_messages=[],
                messages=messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs,
            )
        # 전통적인 단일 이미지 형식
        elif image_data:
            return openai_complete_if_cache(
                "gpt-4o",
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
        # 순수 텍스트 형식
        else:
            return llm_model_func(prompt, system_prompt, history_messages, **kwargs)

    # 임베딩 함수 정의
    embedding_func = EmbeddingFunc(
        embedding_dim=3072,
        max_token_size=8192,
        func=partial(
            openai_embed.func,
            model="text-embedding-3-large",
            api_key=api_key,
            base_url=base_url,
        ),
    )

    # RAGAnything 초기화
    rag = RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        vision_model_func=vision_model_func,
        embedding_func=embedding_func,
    )

    # 문서 처리
    await rag.process_document_complete(
        file_path="path/to/your/document.pdf",
        output_dir="./output",
        parse_method="auto"
    )

    # 처리된 콘텐츠 질의
    # 순수 텍스트 질의 - 기본 지식 베이스 검색용
    text_result = await rag.aquery(
        "What are the main findings shown in the figures and tables?",
        mode="hybrid"
    )
    print("Text query result:", text_result)

    # 특정 멀티모달 콘텐츠를 포함한 멀티모달 질의
    multimodal_result = await rag.aquery_with_multimodal(
    "Explain this formula and its relevance to the document content",
    multimodal_content=[{
        "type": "equation",
        "latex": "P(d|q) = \\frac{P(q|d) \\cdot P(d)}{P(q)}",
        "equation_caption": "Document relevance probability"
    }],
    mode="hybrid"
)
    print("Multimodal query result:", multimodal_result)

if __name__ == "__main__":
    asyncio.run(main())
```

> **🇰🇷 한국어 프롬프트 사용:** 파이프라인 전반의 프롬프트를 한국어로 전환하려면 RAGAnything 초기화 전에 한 번 호출하세요.
>
> ```python
> from raganything.prompt_manager import set_prompt_language
>
> set_prompt_language("ko")  # 프로세스 전역으로 한국어 프롬프트 적용
> ```
>
> 자세한 내용은 [`docs/korean.md`](docs/korean.md)와 [`examples/korean_example.py`](examples/korean_example.py)를 참고하세요.

#### 2. 멀티모달 콘텐츠 직접 처리

```python
import asyncio
from functools import partial
from lightrag import LightRAG
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
from raganything.modalprocessors import ImageModalProcessor, TableModalProcessor

async def process_multimodal_content():
    # API 구성 설정
    api_key = "your-api-key"
    base_url = "your-base-url"  # 선택 사항

    # LightRAG 초기화
    rag = LightRAG(
        working_dir="./rag_storage",
        llm_model_func=lambda prompt, system_prompt=None, history_messages=[], **kwargs: openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        ),
        embedding_func=EmbeddingFunc(
            embedding_dim=3072,
            max_token_size=8192,
            func=partial(
                openai_embed.func,
                model="text-embedding-3-large",
                api_key=api_key,
                base_url=base_url,
            ),
        )
    )
    await rag.initialize_storages()

    # 이미지 처리
    image_processor = ImageModalProcessor(
        lightrag=rag,
        modal_caption_func=lambda prompt, system_prompt=None, history_messages=[], image_data=None, **kwargs: openai_complete_if_cache(
            "gpt-4o",
            "",
            system_prompt=None,
            history_messages=[],
            messages=[
                {"role": "system", "content": system_prompt} if system_prompt else None,
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]} if image_data else {"role": "user", "content": prompt}
            ],
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        ) if image_data else openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )
    )

    image_content = {
        "img_path": "path/to/image.jpg",
        "image_caption": ["Figure 1: Experimental results"],
        "image_footnote": ["Data collected in 2024"]
    }

    description, entity_info = await image_processor.process_multimodal_content(
        modal_content=image_content,
        content_type="image",
        file_path="research_paper.pdf",
        entity_name="Experimental Results Figure"
    )

    # 표 처리
    table_processor = TableModalProcessor(
        lightrag=rag,
        modal_caption_func=lambda prompt, system_prompt=None, history_messages=[], **kwargs: openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )
    )

    table_content = {
        "table_body": """
        | Method | Accuracy | F1-Score |
        |--------|----------|----------|
        | RAGAnything | 95.2% | 0.94 |
        | Baseline | 87.3% | 0.85 |
        """,
        "table_caption": ["Performance Comparison"],
        "table_footnote": ["Results on test dataset"]
    }

    description, entity_info = await table_processor.process_multimodal_content(
        modal_content=table_content,
        content_type="table",
        file_path="research_paper.pdf",
        entity_name="Performance Results Table"
    )

if __name__ == "__main__":
    asyncio.run(process_multimodal_content())
```

#### 3. 배치 처리

```python
# 여러 문서 처리
await rag.process_folder_complete(
    folder_path="./documents",
    output_dir="./output",
    file_extensions=[".pdf", ".docx", ".pptx"],
    recursive=True,
    max_workers=4
)
```

#### 4. 사용자 정의 모달 프로세서

```python
from raganything.modalprocessors import GenericModalProcessor

class CustomModalProcessor(GenericModalProcessor):
    async def process_multimodal_content(self, modal_content, content_type, file_path, entity_name):
        # 사용자 정의 처리 로직
        enhanced_description = await self.analyze_custom_content(modal_content)
        entity_info = self.create_custom_entity(enhanced_description, entity_name)
        return await self._create_entity_and_chunk(enhanced_description, entity_info, file_path)
```

#### 5. 질의 옵션

RAG-Anything은 세 가지 유형의 질의 방법을 제공합니다:

**순수 텍스트 질의** - LightRAG를 사용한 직접 지식 베이스 검색:
```python
# 텍스트 질의를 위한 다양한 질의 모드
text_result_hybrid = await rag.aquery("Your question", mode="hybrid")
text_result_local = await rag.aquery("Your question", mode="local")
text_result_global = await rag.aquery("Your question", mode="global")
text_result_naive = await rag.aquery("Your question", mode="naive")

# 동기 버전
sync_text_result = rag.query("Your question", mode="hybrid")
```

**VLM 강화 질의** - VLM을 사용하여 검색된 문맥의 이미지를 자동 분석:
```python
# VLM 강화 질의 (vision_model_func가 제공되면 자동 활성화)
vlm_result = await rag.aquery(
    "Analyze the charts and figures in the document",
    mode="hybrid"
    # vision_model_func가 사용 가능할 때 vlm_enhanced=True가 자동으로 설정됨
)

# VLM 강화를 수동으로 제어
vlm_enabled = await rag.aquery(
    "What do the images show in this document?",
    mode="hybrid",
    vlm_enhanced=True  # VLM 강화 강제 활성화
)

vlm_disabled = await rag.aquery(
    "What do the images show in this document?",
    mode="hybrid",
    vlm_enhanced=False  # VLM 강화 강제 비활성화
)

# 문서에 이미지가 포함되어 있으면 VLM이 직접 보고 분석할 수 있습니다
# 시스템은 자동으로 다음을 수행합니다:
# 1. 이미지 경로를 포함한 관련 문맥 검색
# 2. 이미지를 base64로 로드 및 인코딩
# 3. 텍스트 문맥과 이미지를 모두 VLM에 전달하여 종합 분석
```

**멀티모달 질의** - 특정 멀티모달 콘텐츠 분석을 포함한 강화 질의:
```python
# 표 데이터를 포함한 질의
table_result = await rag.aquery_with_multimodal(
    "Compare these performance metrics with the document content",
    multimodal_content=[{
        "type": "table",
        "table_data": """Method,Accuracy,Speed
                        RAGAnything,95.2%,120ms
                        Traditional,87.3%,180ms""",
        "table_caption": "Performance comparison"
    }],
    mode="hybrid"
)

# 수식 콘텐츠를 포함한 질의
equation_result = await rag.aquery_with_multimodal(
    "Explain this formula and its relevance to the document content",
    multimodal_content=[{
        "type": "equation",
        "latex": "P(d|q) = \\frac{P(q|d) \\cdot P(d)}{P(q)}",
        "equation_caption": "Document relevance probability"
    }],
    mode="hybrid"
)
```

#### 6. 기존 LightRAG 인스턴스 불러오기

```python
import asyncio
from functools import partial
from raganything import RAGAnything, RAGAnythingConfig
from lightrag import LightRAG
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import EmbeddingFunc
import os

async def load_existing_lightrag():
    # API 구성 설정
    api_key = "your-api-key"
    base_url = "your-base-url"  # 선택 사항

    # 먼저, 기존 LightRAG 인스턴스를 생성하거나 불러옵니다
    lightrag_working_dir = "./existing_lightrag_storage"

    # 이전 LightRAG 인스턴스가 존재하는지 확인
    if os.path.exists(lightrag_working_dir) and os.listdir(lightrag_working_dir):
        print("✅ Found existing LightRAG instance, loading...")
    else:
        print("❌ No existing LightRAG instance found, will create new one")

    # 구성에 맞춰 LightRAG 인스턴스 생성/불러오기
    lightrag_instance = LightRAG(
        working_dir=lightrag_working_dir,
        llm_model_func=lambda prompt, system_prompt=None, history_messages=[], **kwargs: openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        ),
        embedding_func=EmbeddingFunc(
            embedding_dim=3072,
            max_token_size=8192,
            func=partial(
                openai_embed.func,
                model="text-embedding-3-large",
                api_key=api_key,
                base_url=base_url,
            ),
        )
    )

    # 스토리지 초기화 (가능한 경우 기존 데이터를 불러옵니다)
    await lightrag_instance.initialize_storages()
    await initialize_pipeline_status()

    # 이미지 처리를 위한 비전 모델 함수 정의
    def vision_model_func(
        prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs
    ):
        # messages 형식이 제공되면 (멀티모달 VLM 강화 질의용) 그대로 사용
        if messages:
            return openai_complete_if_cache(
                "gpt-4o",
                "",
                system_prompt=None,
                history_messages=[],
                messages=messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs,
            )
        # 전통적인 단일 이미지 형식
        elif image_data:
            return openai_complete_if_cache(
                "gpt-4o",
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
        # 순수 텍스트 형식
        else:
            return lightrag_instance.llm_model_func(prompt, system_prompt, history_messages, **kwargs)

    # 이제 기존 LightRAG 인스턴스를 사용하여 RAGAnything 초기화
    rag = RAGAnything(
        lightrag=lightrag_instance,  # 기존 LightRAG 인스턴스 전달
        vision_model_func=vision_model_func,
        # 참고: working_dir, llm_model_func, embedding_func 등은 lightrag_instance에서 상속됩니다
    )

    # 기존 지식 베이스 질의
    result = await rag.aquery(
        "What data has been processed in this LightRAG instance?",
        mode="hybrid"
    )
    print("Query result:", result)

    # 기존 LightRAG 인스턴스에 새로운 멀티모달 문서 추가
    await rag.process_document_complete(
        file_path="path/to/new/multimodal_document.pdf",
        output_dir="./output"
    )

if __name__ == "__main__":
    asyncio.run(load_existing_lightrag())
```

#### 7. 콘텐츠 리스트 직접 삽입

이미 사전 파싱된 콘텐츠 리스트가 있는 경우(예: 외부 파서 또는 이전 처리 결과), 문서 파싱 없이 RAGAnything에 직접 삽입할 수 있습니다:

```python
import asyncio
from functools import partial
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc

async def insert_content_list_example():
    # API 구성 설정
    api_key = "your-api-key"
    base_url = "your-base-url"  # 선택 사항

    # RAGAnything 구성 생성
    config = RAGAnythingConfig(
        working_dir="./rag_storage",
        enable_image_processing=True,
        enable_table_processing=True,
        enable_equation_processing=True,
    )

    # 모델 함수 정의
    def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
        return openai_complete_if_cache(
            "gpt-4o-mini",
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )

    def vision_model_func(prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs):
        # messages 형식이 제공되면 (멀티모달 VLM 강화 질의용) 그대로 사용
        if messages:
            return openai_complete_if_cache(
                "gpt-4o",
                "",
                system_prompt=None,
                history_messages=[],
                messages=messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs,
            )
        # 전통적인 단일 이미지 형식
        elif image_data:
            return openai_complete_if_cache(
                "gpt-4o",
                "",
                system_prompt=None,
                history_messages=[],
                messages=[
                    {"role": "system", "content": system_prompt} if system_prompt else None,
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                        ],
                    } if image_data else {"role": "user", "content": prompt},
                ],
                api_key=api_key,
                base_url=base_url,
                **kwargs,
            )
        # 순수 텍스트 형식
        else:
            return llm_model_func(prompt, system_prompt, history_messages, **kwargs)

    embedding_func = EmbeddingFunc(
        embedding_dim=3072,
        max_token_size=8192,
        func=partial(
            openai_embed.func,
            model="text-embedding-3-large",
            api_key=api_key,
            base_url=base_url,
        ),
    )

    # RAGAnything 초기화
    rag = RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        vision_model_func=vision_model_func,
        embedding_func=embedding_func,
    )

    # 예시: 외부 소스에서 사전 파싱된 콘텐츠 리스트
    content_list = [
        {
            "type": "text",
            "text": "This is the introduction section of our research paper.",
            "page_idx": 0  # 이 콘텐츠가 나타나는 페이지 번호
        },
        {
            "type": "image",
            "img_path": "/absolute/path/to/figure1.jpg",  # 중요: 절대 경로 사용
            "image_caption": ["Figure 1: System Architecture"],
            "image_footnote": ["Source: Authors' original design"],
            "page_idx": 1  # 이 이미지가 나타나는 페이지 번호
        },
        {
            "type": "table",
            "table_body": "| Method | Accuracy | F1-Score |\n|--------|----------|----------|\n| Ours | 95.2% | 0.94 |\n| Baseline | 87.3% | 0.85 |",
            "table_caption": ["Table 1: Performance Comparison"],
            "table_footnote": ["Results on test dataset"],
            "page_idx": 2  # 이 표가 나타나는 페이지 번호
        },
        {
            "type": "equation",
            "latex": "P(d|q) = \\frac{P(q|d) \\cdot P(d)}{P(q)}",
            "text": "Document relevance probability formula",
            "page_idx": 3  # 이 수식이 나타나는 페이지 번호
        },
        {
            "type": "text",
            "text": "In conclusion, our method demonstrates superior performance across all metrics.",
            "page_idx": 4  # 이 콘텐츠가 나타나는 페이지 번호
        }
    ]

    # 콘텐츠 리스트 직접 삽입
    await rag.insert_content_list(
        content_list=content_list,
        file_path="research_paper.pdf",  # 인용용 참조 파일 이름
        split_by_character=None,         # 선택적 텍스트 분할
        split_by_character_only=False,   # 선택적 텍스트 분할 모드
        doc_id=None,                     # 선택적 사용자 정의 문서 ID (제공하지 않으면 자동 생성됨)
        display_stats=True               # 콘텐츠 통계 표시
    )

    # 삽입된 콘텐츠 질의
    result = await rag.aquery(
        "What are the key findings and performance metrics mentioned in the research?",
        mode="hybrid"
    )
    print("Query result:", result)

    # 서로 다른 문서 ID로 여러 콘텐츠 리스트를 삽입할 수도 있습니다
    another_content_list = [
        {
            "type": "text",
            "text": "This is content from another document.",
            "page_idx": 0  # 이 콘텐츠가 나타나는 페이지 번호
        },
        {
            "type": "table",
            "table_body": "| Feature | Value |\n|---------|-------|\n| Speed | Fast |\n| Accuracy | High |",
            "table_caption": ["Feature Comparison"],
            "page_idx": 1  # 이 표가 나타나는 페이지 번호
        }
    ]

    await rag.insert_content_list(
        content_list=another_content_list,
        file_path="another_document.pdf",
        doc_id="custom-doc-id-123"  # 사용자 정의 문서 ID
    )

if __name__ == "__main__":
    asyncio.run(insert_content_list_example())
```

**콘텐츠 리스트 형식:**

`content_list`는 표준 형식을 따라야 하며, 각 항목은 다음을 포함하는 딕셔너리입니다:

- **텍스트 콘텐츠**: `{"type": "text", "text": "content text", "page_idx": 0}`
- **이미지 콘텐츠**: `{"type": "image", "img_path": "/absolute/path/to/image.jpg", "image_caption": ["caption"], "image_footnote": ["note"], "page_idx": 1}`
- **표 콘텐츠**: `{"type": "table", "table_body": "markdown table", "table_caption": ["caption"], "table_footnote": ["note"], "page_idx": 2}`
- **수식 콘텐츠**: `{"type": "equation", "latex": "LaTeX formula", "text": "description", "page_idx": 3}`
- **일반 콘텐츠**: `{"type": "custom_type", "content": "any content", "page_idx": 4}`

**중요 참고 사항:**
- **`img_path`**: 이미지 파일의 절대 경로여야 합니다(예: `/home/user/images/chart.jpg` 또는 `C:\Users\user\images\chart.jpg`)
- **`page_idx`**: 원본 문서에서 콘텐츠가 나타나는 페이지 번호를 나타냅니다(0부터 시작하는 인덱싱)
- **콘텐츠 순서**: 항목은 리스트에 나타나는 순서대로 처리됩니다

이 방법은 다음과 같은 경우에 특히 유용합니다:
- 외부 파서(MinerU/Docling 이외)에서 가져온 콘텐츠가 있는 경우
- 프로그래밍 방식으로 생성된 콘텐츠를 처리하려는 경우
- 여러 소스의 콘텐츠를 단일 지식 베이스에 삽입해야 하는 경우
- 재사용하려는 캐시된 파싱 결과가 있는 경우

---

## 🛠️ 예제

*실용적인 구현 데모*

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212257455-13e3e01e-d6a6-45dc-bb92-3ab87b12dfc1.gif" width="300">
</div>

`examples/` 디렉터리에는 포괄적인 사용 예제가 포함되어 있습니다:

- **`raganything_example.py`**: MinerU를 사용한 엔드투엔드 문서 처리
- **`modalprocessors_example.py`**: 멀티모달 콘텐츠 직접 처리
- **`office_document_test.py`**: MinerU를 사용한 Office 문서 파싱 테스트 (API 키 불필요)
- **`image_format_test.py`**: MinerU를 사용한 이미지 형식 파싱 테스트 (API 키 불필요)
- **`text_format_test.py`**: MinerU를 사용한 텍스트 형식 파싱 테스트 (API 키 불필요)
- **`korean_example.py`**: 한국어 프롬프트·임베딩·OCR 설정을 적용한 한국어 처리 예제

**예제 실행:**

```bash
# 파서 선택을 포함한 엔드투엔드 처리
python examples/raganything_example.py path/to/document.pdf --api-key YOUR_API_KEY --parser mineru

# 직접 모달 처리
python examples/modalprocessors_example.py --api-key YOUR_API_KEY

# Office 문서 파싱 테스트 (MinerU 전용)
python examples/office_document_test.py --file path/to/document.docx

# 이미지 형식 파싱 테스트 (MinerU 전용)
python examples/image_format_test.py --file path/to/image.bmp

# 텍스트 형식 파싱 테스트 (MinerU 전용)
python examples/text_format_test.py --file path/to/document.md

# LibreOffice 설치 확인
python examples/office_document_test.py --check-libreoffice --file dummy

# PIL/Pillow 설치 확인
python examples/image_format_test.py --check-pillow --file dummy

# ReportLab 설치 확인
python examples/text_format_test.py --check-reportlab --file dummy
```

---

## 🔧 구성

*시스템 최적화 매개변수*

### 환경 변수

`.env` 파일을 생성하세요(`.env.example` 참고):

```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_base_url  # 선택 사항
OUTPUT_DIR=./output             # 파싱된 문서의 기본 출력 디렉터리
PARSER=mineru                   # 파서 선택: mineru, docling, 또는 paddleocr
PARSE_METHOD=auto              # 파싱 방법: auto, ocr, 또는 txt
```

**참고:** 하위 호환성을 위해 레거시 환경 변수 이름도 여전히 지원됩니다:
- `MINERU_PARSE_METHOD`는 더 이상 사용되지 않으므로 `PARSE_METHOD`를 사용하세요

> **참고**: API 키는 LLM 통합을 포함한 전체 RAG 처리에만 필요합니다. 파싱 테스트 파일(`office_document_test.py` 및 `image_format_test.py`)은 파서 기능만 테스트하며 API 키가 필요하지 않습니다.

### 문제 해결 및 멀티모달 체크리스트

- 일반적인 파이프라인 이슈(OCR, 표, 검색 편향, 디버깅 팁)에 대한 짧은 체크리스트는 **[docs/multimodal_rag_failure_modes.md](docs/multimodal_rag_failure_modes.md)**를 참고하세요. 관련 이슈: [#207](https://github.com/HKUDS/RAG-Anything/issues/207), [#213](https://github.com/HKUDS/RAG-Anything/issues/213).

### 공개 미디어 URL (CDN / 오브젝트 스토리지)

수집(ingestion)이 서버에서 실행되지만 UI나 다른 서비스에서 그림에 대한 **HTTPS**(또는 S3 스타일) 링크가 필요한 경우 다음을 설정하세요:

```bash
# 에셋의 기본 URL (끝에 슬래시 불필요)
RAGANYTHING_PUBLIC_ASSET_BASE_URL=https://my-bucket.s3.us-east-1.amazonaws.com/prefix
# 해당 트리 아래의 절대 경로에서 제거할 파일 시스템 루트
RAGANYTHING_PUBLIC_ASSET_STRIP_PREFIX=/var/rag/output
```

파싱 후, 비어 있지 않은 각 `img_path`, `table_img_path`, `equation_img_path`에 형제 필드 `*_public_url`이 추가될 수 있으며, 원본 경로는 로컬 처리를 위해 디스크에 그대로 유지됩니다. [#272](https://github.com/HKUDS/RAG-Anything/issues/272)를 참고하세요.

> **현재 적용 범위**: 이 매핑은 MinerU 파서 경로에서만 실행됩니다. 다른 파서(예: Docling)는 계속 작동하지만, 해당 헬퍼가 content_list 후처리에 연결되기 전까지는 `*_public_url` 필드를 생성하지 않습니다. 두 환경 변수 중 하나만 설정된 경우 RAG-Anything은 경고를 기록하고 URL 첨부를 건너뜁니다.

### 파서 구성

RAGAnything은 이제 각각 고유한 장점을 가진 여러 파서를 지원합니다:

#### MinerU 파서
- PDF, 이미지, Office 문서 등 다양한 형식 지원
- 강력한 OCR 및 표 추출 기능
- GPU 가속 지원

#### Docling 파서
- Office 문서 및 HTML 파일에 최적화
- 더 나은 문서 구조 보존
- 여러 Office 형식에 대한 네이티브 지원

#### PaddleOCR 파서
- 이미지 및 PDF를 위한 OCR 중심 파서
- 기존 `content_list` 처리와 호환되는 텍스트 블록 생성
- 먼저 PDF로 변환하여 Office/TXT/MD 파싱을 선택적으로 지원

PaddleOCR 파서 extras 설치:

```bash
pip install -e ".[paddleocr]"
# 또는
uv sync --extra paddleocr
```

> **참고**: PaddleOCR은 `paddlepaddle`도 필요합니다(CPU/GPU 패키지는 플랫폼에 따라 다름). 공식 가이드에 따라 설치하세요: https://www.paddlepaddle.org.cn/install/quick

### MinerU 구성

```bash
# MinerU 2.0은 설정 파일 대신 명령줄 매개변수를 사용합니다
# 사용 가능한 옵션 확인:
mineru --help

# 일반적인 구성:
mineru -p input.pdf -o output_dir -m auto    # 자동 파싱 모드
mineru -p input.pdf -o output_dir -m ocr     # OCR 중심 파싱
mineru -p input.pdf -o output_dir -b pipeline --device cuda  # GPU 가속
```

RAGAnything 매개변수를 통해서도 파싱을 구성할 수 있습니다:

```python
# 파서 선택을 포함한 기본 파싱 구성
await rag.process_document_complete(
    file_path="document.pdf",
    output_dir="./output/",
    parse_method="auto",          # 또는 "ocr", "txt"
    parser="mineru"               # 선택 사항: "mineru", "docling", 또는 "paddleocr"
)

# 특수 매개변수를 포함한 고급 파싱 구성
await rag.process_document_complete(
    file_path="document.pdf",
    output_dir="./output/",
    parse_method="auto",          # 파싱 방법: "auto", "ocr", "txt"
    parser="mineru",              # 파서 선택: "mineru", "docling", 또는 "paddleocr"

    # MinerU 특수 매개변수 - 지원되는 모든 kwargs:
    lang="ch",                   # OCR 최적화를 위한 문서 언어 (예: "ch", "en", "ja", "korean")
    device="cuda:0",             # 추론 장치: "cpu", "cuda", "cuda:0", "npu", "mps"
    start_page=0,                # 시작 페이지 번호 (0부터 시작, PDF용)
    end_page=10,                 # 끝 페이지 번호 (0부터 시작, PDF용)
    formula=True,                # 수식 파싱 활성화
    table=True,                  # 표 파싱 활성화
    backend="pipeline",          # 파싱 백엔드: pipeline|hybrid-auto-engine|hybrid-http-client|vlm-auto-engine|vlm-http-client.
    source="huggingface",        # 모델 소스: "huggingface", "modelscope", "local"
    # vlm_url="http://127.0.0.1:3000" # backend=vlm-http-client 사용 시 서비스 주소

    # 표준 RAGAnything 매개변수
    display_stats=True,          # 콘텐츠 통계 표시
    split_by_character=None,     # 텍스트를 분할할 선택적 문자
    doc_id=None                  # 선택적 문서 ID
)
```

> **참고**: MinerU 2.0은 더 이상 `magic-pdf.json` 설정 파일을 사용하지 않습니다. 모든 설정은 이제 명령줄 매개변수 또는 함수 인자로 전달됩니다. RAG-Anything은 MinerU, Docling, PaddleOCR을 포함한 여러 문서 파서를 지원합니다.

> **🇰🇷 한국어 OCR 팁**: 한국어 문서를 처리할 때는 `lang="korean"`을 전달하여 OCR 정확도를 높이세요. 한국어 임베딩 모델(예: `BAAI/bge-m3`, `nlpai-lab/KURE-v1`)과 함께 사용하면 한국어 검색 품질이 향상됩니다. 자세한 내용은 [`docs/korean.md`](docs/korean.md)를 참고하세요.

### 처리 요구 사항

서로 다른 콘텐츠 유형은 특정 선택적 의존성을 필요로 합니다:

- **Office 문서** (.doc, .docx, .ppt, .pptx, .xls, .xlsx): [LibreOffice](https://www.libreoffice.org/download/download/) 설치
- **확장 이미지 형식** (.bmp, .tiff, .gif, .webp): `pip install raganything[image]`로 설치
- **텍스트 파일** (.txt, .md): `pip install raganything[text]`로 설치
- **PaddleOCR 파서** (`parser="paddleocr"`): `pip install raganything[paddleocr]`로 설치한 뒤, 플랫폼에 맞는 `paddlepaddle` 설치

> **📋 빠른 설치**: 모든 형식 지원을 활성화하려면 `pip install raganything[all]`을 사용하세요(Python 의존성만 해당 — LibreOffice는 여전히 별도 설치 필요)

---

## 🧪 지원 콘텐츠 유형

### 문서 형식

- **PDF** - 연구 논문, 보고서, 프레젠테이션
- **Office 문서** - DOC, DOCX, PPT, PPTX, XLS, XLSX
- **이미지** - JPG, PNG, BMP, TIFF, GIF, WebP
- **텍스트 파일** - TXT, MD

### 멀티모달 요소

- **이미지** - 사진, 다이어그램, 차트, 스크린샷
- **표** - 데이터 표, 비교 차트, 통계 요약
- **수식** - LaTeX 형식의 수학 공식
- **일반 콘텐츠** - 확장형 프로세서를 통한 사용자 정의 콘텐츠 유형

*형식별 의존성 설치는 [구성](#-구성) 섹션을 참고하세요.*

---

## 📖 인용

*학술 참조*

<div align="center">
  <div style="width: 60px; height: 60px; margin: 20px auto; position: relative;">
    <div style="width: 100%; height: 100%; border: 2px solid #00d9ff; border-radius: 50%; position: relative;">
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; color: #00d9ff;">📖</div>
    </div>
    <div style="position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%); width: 20px; height: 20px; background: white; border-right: 2px solid #00d9ff; border-bottom: 2px solid #00d9ff; transform: rotate(45deg);"></div>
  </div>
</div>

연구에 RAG-Anything이 유용하다고 판단되면, 다음 논문을 인용해 주세요:

```bibtex
@misc{guo2025raganythingallinoneragframework,
      title={RAG-Anything: All-in-One RAG Framework},
      author={Zirui Guo and Xubin Ren and Lingrui Xu and Jiahao Zhang and Chao Huang},
      year={2025},
      eprint={2510.12323},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2510.12323},
}
```

---

## 🔗 관련 프로젝트

*생태계 및 확장*

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/HKUDS/LightRAG">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 32px;">⚡</span>
          </div>
          <b>LightRAG</b><br>
          <sub>Simple and Fast RAG</sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/HKUDS/VideoRAG">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 32px;">🎥</span>
          </div>
          <b>VideoRAG</b><br>
          <sub>Extreme Long-Context Video RAG</sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/HKUDS/MiniRAG">
          <div style="width: 100px; height: 100px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 32px;">✨</span>
          </div>
          <b>MiniRAG</b><br>
          <sub>Extremely Simple RAG</sub>
        </a>
      </td>
    </tr>
  </table>
</div>

---

## ⭐ Star History

*커뮤니티 성장 추이*

<div align="center">
  <a href="https://star-history.com/#HKUDS/RAG-Anything&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/RAG-Anything&type=Date" style="border-radius: 15px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);" />
    </picture>
  </a>
</div>

---

## 🤝 기여

*혁신에 함께하세요*

<div align="center">
  소중한 기여를 해주신 모든 기여자분께 감사드립니다.
</div>

<div align="center">
  <a href="https://github.com/HKUDS/RAG-Anything/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=HKUDS/RAG-Anything" style="border-radius: 15px; box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);" />
  </a>
</div>

---

<div align="center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 30px; margin: 30px 0;">
  <div>
    <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="500">
  </div>
  <div style="margin-top: 20px;">
    <a href="https://github.com/HKUDS/RAG-Anything" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/⭐%20Star%20us%20on%20GitHub-1a1a2e?style=for-the-badge&logo=github&logoColor=white">
    </a>
    <a href="https://github.com/HKUDS/RAG-Anything/issues" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/🐛%20Report%20Issues-ff6b6b?style=for-the-badge&logo=github&logoColor=white">
    </a>
    <a href="https://github.com/HKUDS/RAG-Anything/discussions" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/💬%20Discussions-4ecdc4?style=for-the-badge&logo=github&logoColor=white">
    </a>
  </div>
</div>

<div align="center">
  <div style="width: 100%; max-width: 600px; margin: 20px auto; padding: 20px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); border-radius: 15px; border: 1px solid rgba(0, 217, 255, 0.2);">
    <div style="display: flex; justify-content: center; align-items: center; gap: 15px;">
      <span style="font-size: 24px;">⭐</span>
      <span style="color: #00d9ff; font-size: 18px;">Thank you for visiting RAG-Anything!</span>
      <span style="font-size: 24px;">⭐</span>
    </div>
    <div style="margin-top: 10px; color: #00d9ff; font-size: 16px;">Building the Future of Multimodal AI</div>
  </div>
</div>
</content>
</invoke>
