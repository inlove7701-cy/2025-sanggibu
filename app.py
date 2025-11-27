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
    .stTextArea textarea { border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.2); }
    h1 { font-weight: 700; letter-spacing: -1px; }
    .subtitle { font-size: 16px; color: gray; margin-top: -15px; margin-bottom: 30px; }
    .stButton button { border-radius: 8px; font-weight: bold; border: none; transition: all 0.2s ease; }
    .stButton button:hover { transform: scale(1.02); }
    /* 경고 문구 스타일 */
    .warning-text { color: #e67e22; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API 키 설정 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    api_key = None

# --- 3. 헤더 영역 ---
st.title("📝 2025 생기부 메이트")
st.markdown("<p class='subtitle'>Gift for 2025 1st Grade Teachers</p>", unsafe_allow_html=True)
st.divider()

if not api_key:
    with st.expander("🔐 관리자 설정 (API Key 입력)"):
        api_key = st.text_input("Google API Key", type="password")

# --- 4. 입력 영역 (안내 강화) ---
st.markdown("### 1. 학생 관찰 내용 (3가지 이상)")
st.caption("AI가 없는 말을 지어내지 않도록, 구체적인 사례 3가지를 꼭 포함해서 적어주세요.")

student_input = st.text_area(
    "입력창",
    height=250,
    placeholder="""[작성 팁: 아래와 같이 3가지 에피소드를 넣어주세요]
1. (학업) 수학 점수는 낮으나 오답노트를 꼼꼼히 작성함
2. (인성) 체육대회 때 뒷정리를 도맡아 함
3. (진로) 동아리에서 코딩 멘토링 활동을 함
""",
    label_visibility="collapsed"
)

# 입력 글자수 체크 및 가이드
if student_input and len(student_input) < 50:
    st.markdown("<p class='warning-text'>⚠️ 내용이 조금 짧습니다. 더 풍성한 생기부를 위해 에피소드를 추가해 보세요.</p>", unsafe_allow_html=True)


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
        with st.spinner('AI 입학사정관이 사실에 기반하여 분석 중입니다...'):
            try: 
                genai.configure(api_key=api_key)
                
                # 모델 자동 선택 로직
                target_model = "gemini-pro"
                try:
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    if any('gemini-1.5-pro' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-pro' in m][0]
                    elif any('gemini-1.5-flash' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-flash' in m][0]
                except:
                    pass
                model = genai.GenerativeModel(target_model)

                if not selected_tags:
                    tags_str = "전체적인 맥락에서 가장 우수한 역량 자동 추출"
                else:
                    tags_str = ", ".join(selected_tags)

                # --- [핵심] 팩트 체크 및 3요소 강제 프롬프트 ---
                system_prompt = f"""
                당신은 생활기록부 작성의 원칙을 철저히 준수하는 고등학교 교사입니다.
                
                [입력 정보]: {student_input}
                [강조 영역]: {tags_str}
                
                # 작성 원칙 (매우 중요)
                1. **No Hallucination (날조 금지)**: 사용자가 입력한 내용에 없는 사실을 절대 지어내지 마십시오. 만약 입력된 정보가 부족하면 문장을 화려하게 꾸미기보다 있는 사실을 담백하게 서술하십시오.
                2. **3-Point Rule (3요소 포함)**: 입력된 텍스트에서 **최소 3가지만큼의 구체적인 에피소드나 키워드**를 찾아내어 문단에 포함시키십시오. (만약 입력 정보가 3가지 미만이라면 있는 것만 활용하십시오.)
                3. **Structure (구성)**: [구체적 사례] → [학생의 행동/태도] → [성장/잠재력 평가]의 흐름을 유지하십시오.
                
                위 원칙을 지켜 500자~700자 분량의 '행동특성 및 종합의견'을 작성하세요.
                """
                
                response = model.generate_content(system_prompt)
                
                st.success("작성 완료!")
                st.caption(f"※ 팩트 기반 작성 모드 동작 중 ({target_model})")
                st.text_area("결과 (복사해서 사용하세요)", value=response.text, height=300)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

