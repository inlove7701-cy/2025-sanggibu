import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 생기부 메이트",
    page_icon="📝",
    layout="centered"
)

# --- [디자인] 반응형 CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif; }
    
    /* 입력창 스타일 */
    .stTextArea textarea { 
        border-radius: 10px; 
        border: 1px solid rgba(128, 128, 128, 0.2); 
    }
    
    /* 제목 및 텍스트 스타일 */
    h1 { font-weight: 700; letter-spacing: -1px; }
    .subtitle { font-size: 16px; color: gray; margin-top: -15px; margin-bottom: 30px; }
    
    /* 버튼 스타일 */
    .stButton button { border-radius: 8px; font-weight: bold; border: none; transition: all 0.2s ease; }
    .stButton button:hover { transform: scale(1.02); }
    
    /* 안내 박스 스타일 */
    .guide-box {
        background-color: rgba(240, 242, 246, 0.5); /* 반투명 회색 배경 */
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        margin-bottom: 20px;
        font-size: 14px;
        color: #444;
        line-height: 1.6;
    }
    .guide-title { font-weight: bold; margin-bottom: 8px; display: block; font-size: 15px;}
    
    /* 글자 수 표시 박스 스타일 */
    .count-box {
        background-color: #E8F6F3; /* 연한 민트색 */
        color: #1D8348;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 5px;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API 키 설정 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    api_key = None

# --- 3. 헤더 영역 ---
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
    1. <b>(학업)</b> 수학 점수는 낮으나 오답노트를 꼼꼼히 작성함<br>
    2. <b>(인성)</b> 체육대회 때 뒷정리를 도맡아 함<br>
    3. <b>(진로)</b> 동아리에서 코딩 멘토링 활동을 함
</div>
""", unsafe_allow_html=True)


# --- 4. 입력 영역 ---
st.markdown("### 1. 학생 관찰 내용")
student_input = st.text_area(
    "입력창",
    height=200,
    placeholder="위의 작성 팁을 참고하여, 학생의 구체적인 행동 특성을 자유롭게 적어주세요.", 
    label_visibility="collapsed"
)

# 입력 글자수 체크
if student_input and len(student_input) < 30:
    st.markdown("<p style='color:#e67e22; font-size:14px;'>⚠️ 내용이 조금 짧습니다. 3가지 에피소드가 들어갔나요?</p>", unsafe_allow_html=True)

# --- 5. 필터 영역 ---
st.markdown("### 2. 강조할 핵심 키워드 선택")
filter_options = [
    "👑 AI 입학사정관 자동 판단", "📘 학업 역량", "🤝 공동체 역량", 
    "🚀 진로 역량", "🌱 발전 가능성", "🎨 창의적 문제해결력", 
    "😊 인성/나눔/배려", "⏰ 성실성/규칙준수"
]
try:
    selected_tags = st.pills("키워드 버튼", options=filter_options, selection_mode="multi")
except:
    selected_tags = st.multiselect("키워드 선택", filter_options)

# --- 6. 실행 및 결과 영역 ---
st.markdown("")
if st.button("✨ 생기부 문구 생성하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ API Key가 설정되지 않았습니다.")
    elif not student_input:
        st.warning("⚠️ 학생 관찰 내용을 입력해주세요!")
    else:
        with st.spinner('AI 입학사정관이 분석 중입니다...'):
            try: 
                genai.configure(api_key=api_key)
                
                # --- [핵심] 사용 가능한 모델 자동 찾기 로직 ---
                target_model = "gemini-pro" # 기본값
                
                try:
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    
                    if any('gemini-1.5-pro' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-pro' in m][0]
                    elif any('gemini-1.5-flash' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-flash' in m][0]
                    elif any('gemini-pro' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-pro' in m][0]
                except Exception as e:
                    pass
                
                model = genai.GenerativeModel(target_model)
                # ---------------------------------------------

                if not selected_tags:
                    tags_str = "전체적인 맥락에서 가장 우수한 역량 자동 추출"
                else:
                    tags_str = ", ".join(selected_tags)

                system_prompt = f"""
                당신은 입학사정관 관점을 가진 고등학교 교사입니다.
                입력 정보: {student_input}
                강조 영역: [{tags_str}]
                
                위 학생의 '행동특성 및 종합의견'을 작성하세요.
                - 문체: ~함, ~임 (개조식+서술형)
                - 구조: 사례 -> 행동 -> 성장/평가
                - 분량: 500자 내외
                
                # 작성 원칙 (매우 중요)
                1. **No Hallucination (날조 금지)**: 입력된 내용에 없는 사실을 절대 지어내지 마십시오.
                2. **3-Point Rule (3요소 포함)**: 입력된 텍스트에서 최소 3가지 이상의 에피소드를 포함하십시오.
                3. **Structure (구성)**: [구체적 사례] → [행동/태도] → [성장/평가] 흐름 유지.
                """
                
                # [수정 포인트] 들여쓰기 오류 수정됨
                response = model.generate_content(system_prompt)
