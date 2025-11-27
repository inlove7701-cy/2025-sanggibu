import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 생기부 메이트",
    page_icon="📝",
    layout="centered"
)

# --- 2. [디자인] 반응형 CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif; 
    }
    
    .stTextArea textarea { 
        border-radius: 10px; 
        border: 1px solid rgba(128, 128, 128, 0.2); 
    }
    
    h1 { font-weight: 700; letter-spacing: -1px; }
    .subtitle { font-size: 16px; color: gray; margin-top: -15px; margin-bottom: 30px; }
    
선생님, 정말 섬세하신 부분까지 신경 쓰시는군요! 하루 종일 모니터를 보셔야 하는 선생님들께는 **'눈의 피로도'**가 정말 중요하죠.

에메랄드 그린은 예쁘지만 채도가 높아서 오래 보면 눈이 시릴 수 있습니다. 대신, '세이지 그린(Sage Green)' 색상을 강력 추천합니다.

색상 특징: 쑥색이나 말린 잎사귀 색에 가깝습니다.

장점: 채도를 낮춰서 눈부심이 없고, 자연의 색이라 심리적인 안정감을 줍니다. 스타벅스나 고급 스파 브랜드에서 주로 쓰는 '힐링' 컬러입니다.

아래 코드는 **[차분한 세이지 그린]**을 적용한 최종 코드입니다.

🌿 [눈이 편안한 세이지 그린] 최종 코드 (app.py)
Python

import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 생기부 메이트",
    page_icon="📝",
    layout="centered"
)

# --- 2. [디자인] 반응형 CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif; 
    }
    
    .stTextArea textarea { 
        border-radius: 10px; 
        border: 1px solid rgba(128, 128, 128, 0.2); 
    }
    
    h1 { font-weight: 700; letter-spacing: -1px; }
    .subtitle { font-size: 16px; color: gray; margin-top: -15px; margin-bottom: 30px; }
    
    /* [색상 변경됨] 버튼 스타일: 눈이 편안한 세이지 그린 (Sage Green) */
    .stButton button { 
        background-color: #557C64 !important; /* 차분한 쑥색/세이지 그린 */
        color: white !important;
        border-radius: 8px; 
        font-weight: bold; 
        border: none; 
        transition: all 0.2s ease; 
        padding: 0.6rem 1rem; /* 버튼을 살짝 더 도톰하게 */
        font-size: 16px !important;
    }
    /* 마우스 올렸을 때: 조금 더 깊은 숲색 */
    .stButton button:hover { 
        background-color: #3E5F4A !important; 
        transform: scale(1.02); 
        color: white !important;
    }
    
    .guide-box {
        background-color: rgba(240, 242, 246, 0.5);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        margin-bottom: 20px;
        font-size: 14px;
        color: #444;
        line-height: 1.6;
    }
    .guide-title { font-weight: bold; margin-bottom: 8px; display: block; font-size: 15px;}
    
    /* 글자 수 표시 박스: 버튼 색과 어울리는 연한 톤 */
    .count-box {
        background-color: #EDF5F0; /* 아주 연한 세이지색 배경 */
        color: #2D4F3A;            /* 짙은 녹색 글씨 */
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 5px;
        text-align: right;
    }
    
    /* 분석 박스 왼쪽 선: 버튼 색과 깔맞춤 */
    .analysis-box {
        background-color: #f8f9fa;
        border-left: 4px solid #557C64; 
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        font-size: 14px;
        color: #333;
    }
    
    /* 푸터 스타일 */
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 12px;
        color: #888;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API 키 설정 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    api_key = None

# --- 4. 헤더 영역 ---
st.title("📝 2025 1학년부 행발 메이트")
st.markdown("<p class='subtitle'>Gift for 2025 1st Grade Teachers</p>", unsafe_allow_html=True)
st.divider()

if not api_key:
    with st.expander("🔐 관리자 설정 (API Key 입력)"):
        api_key = st.text_input("Google API Key", type="password")

# 작성 팁 헤더
st.markdown("""
<div class="guide-box">
    <span class="guide-title">💡 풍성한 생기부를 위한 작성 팁 (3-Point)</span>
    좋은 평가를 위해 아래 3가지 요소가 포함되도록 에피소드를 적어주세요.<br>
    [예시]<br>
    1. <b>(학업)</b> 수학 점수는 낮으나 오답노트를 꼼꼼히 작성함<br>
    2. <b>(인성)</b> 체육대회 때 뒷정리를 도맡아 함<br>
    3. <b>(진로)</b> 동아리에서 코딩 멘토링 활동을 함
</div>
""", unsafe_allow_html=True)

# --- 5. 입력 영역 ---
st.markdown("### 1. 학생 관찰 내용")
student_input = st.text_area(
    "입력창",
    height=200,
    placeholder="위의 작성 팁을 참고하여, 학생의 구체적인 행동 특성을 자유롭게 적어주세요.", 
    label_visibility="collapsed"
)

if student_input and len(student_input) < 30:
    st.markdown("<p style='color:#e67e22; font-size:14px;'>⚠️ 내용이 조금 짧습니다. 3가지 에피소드가 들어갔나요?</p>", unsafe_allow_html=True)

# --- 6. 옵션 영역 (키워드 + 글자수) ---
col1, col2 = st.columns([1, 1]) 

st.markdown("### 2. 강조할 핵심 키워드")
filter_options = [
    "👑 AI 입학사정관 자동 판단", "📘 학업 역량", "🤝 공동체 역량", 
    "🚀 진로 역량", "🌱 발전 가능성", "🎨 창의적 문제해결력", 
    "😊 인성/나눔/배려", "⏰ 성실성/규칙준수"
]
try:
    selected_tags = st.pills("키워드 버튼", options=filter_options, selection_mode="multi")
except:
    selected_tags = st.multiselect("키워드 선택", filter_options)

st.markdown("### 3. 희망 분량 설정 (종합본 기준)")
target_length = st.slider(
    "생성할 글자 수 (공백 포함)",
    min_value=200,
    max_value=600,
    value=500,
    step=50,
    help="AI가 최종 종합본을 이 분량에 맞춰 작성합니다."
)

# --- 7. 실행 및 결과 영역 ---
st.markdown("")
if st.button("✨ 생기부 문구 생성하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ API Key가 설정되지 않았습니다.")
    elif not student_input:
        st.warning("⚠️ 학생 관찰 내용을 입력해주세요!")
    else:
        with st.spinner(f'AI가 {target_length}자 내외로 분석 중입니다...'):
            try:
                genai.configure(api_key=api_key)

                # 모델 자동 탐색 로직
                target_model = "gemini-pro"
                try:
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    if any('gemini-1.5-pro' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-pro' in m][0]
                    elif any('gemini-1.5-flash' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-flash' in m][0]
                    elif any('gemini-pro' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-pro' in m][0]
                except:
                    pass
                
                model = genai.GenerativeModel(target_model)

                if not selected_tags:
                    tags_str = "전체적인 맥락에서 가장 우수한 역량 자동 추출"
                else:
                    tags_str = ", ".join(selected_tags)
# [핵심] 분리 출력을 위한 프롬프트 변경
                system_prompt = f"""
                당신은 입학사정관 관점을 가진 고등학교 교사입니다.
                입력 정보: {student_input}
                강조 영역: [{tags_str}]
                
                다음 두 가지 파트로 나누어 출력하세요. 두 파트 사이에는 반드시 "---SPLIT---" 이라고 적어 구분해주세요.

                [Part 1] 영역별 분석 (개조식)
                - 입력된 내용을 [인성 / 학업 / 진로 / 공동체] 등으로 분류하여 핵심 키워드와 내용을 요약 정리할 것.
                
                ---SPLIT---

                [Part 2] 행동특성 및 종합의견 (서술형 종합본)
                - 실제 생기부에 입력할 완성된 줄글 형태.
                - 문체: ~함, ~임 (개조식+서술형)
                - 구조: 사례 -> 행동 -> 성장/평가
                - 목표 분량: 공백 포함 약 {target_length}자 (오차범위 ±10%)
                - 주의: 날조 금지, 3요소 포함
                """

                response = model.generate_content(system_prompt)
                full_text = response.text
                
                # [핵심] 결과 쪼개기 (분석본 vs 종합본)
                if "---SPLIT---" in full_text:
                    parts = full_text.split("---SPLIT---")
                    analysis_text = parts[0].strip()
                    final_text = parts[1].strip()
                else:
                    analysis_text = "영역별 분석을 생성하지 못했습니다."
                    final_text = full_text

                # 글자 수 계산 (종합본만 계산)
                char_count = len(final_text)
                char_count_no_space = len(final_text.replace(" ", "").replace("\n", ""))
                
                st.success("작성 완료!")
                
                # 1. 영역별 분석 보여주기 (Expander로 깔끔하게)
                with st.expander("🔍 영역별 분석 내용 확인하기 (클릭)", expanded=True):
                    st.markdown(analysis_text)
                
                st.markdown("---")
                st.markdown("### 📋 최종 제출용 종합본")

                # 2. 글자 수 표시 (종합본 기준)
                st.markdown(f"""
                <div class="count-box">
                    📊 목표: {target_length}자 | 실제: {char_count}자 (공백제외 {char_count_no_space}자)
                </div>
                """, unsafe_allow_html=True)
                
                st.caption(f"※ 팩트 기반 작성 모드 동작 중 ({target_model})")
                
                # 3. 최종 결과 텍스트 영역
                st.text_area("결과 (복사해서 나이스에 붙여넣으세요)", value=final_text, height=350)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# --- 8. [NEW] 저작권 및 이메일 표시 (푸터) ---
st.markdown("""
<div class="footer">
<br>
    © 2025 <b>Chaeyun teacher with Ai</b>. All rights reserved.<br>
    문의: <a href="mailto:teacher@school.kr" style="color: #888; text-decoration: none;">inlove11@naver.com</a>
</div>
""", unsafe_allow_html=True)



