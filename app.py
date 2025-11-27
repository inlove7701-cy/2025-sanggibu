import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="2025 생기부 메이트", page_icon="📝", layout="centered")

st.markdown("""
    <style>
    /* 1. 폰트 설정 (깔끔한 고딕체) */
    html, body, [class*="css"] {
        font-family: 'Pretendard', 'Apple SD Gothic Neo', 'Helvetica', sans-serif;
    }
    
    /* 2. 입력창 디자인 (테마에 따라 배경색 자동 변경되도록 투명도 활용) */
    .stTextArea textarea {
        border-radius: 10px;        /* 둥근 모서리 */
        border: 1px solid rgba(128, 128, 128, 0.2); /* 은은한 테두리 */
    }

    /* 3. 헤더 및 소제목 스타일 */
    h1 {
        font-weight: 700;
        letter-spacing: -1px;
    }
    .subtitle {
        font-size: 16px;
        color: gray; /* 회색은 다크/라이트 모드 모두 잘 보임 */
        margin-top: -15px;
        margin-bottom: 30px;
        font-weight: 400;
    }

    /* 4. 버튼 스타일 (Streamlit 기본 색상 활용하여 가독성 확보) */
    .stButton button {
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.2s ease;
    }
    /* 버튼에 마우스 올렸을 때 살짝 커지는 효과 */
    .stButton button:hover {
        transform: scale(1.02);
    }
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

# --- 4. 입력 영역 ---
st.markdown("### 1. 학생 관찰 내용")
student_input = st.text_area(
    "학생의 에피소드, 특징, 성격 등을 자유롭게 적어주세요.",
    height=250,
    placeholder="예시: 수학 성적은 낮지만 질문이 많음. 체육대회 때 반티 문제 해결함."
)

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
                target_model = "gemini-pro" # 기본값 (최후의 수단)
                
                try:
                    # 내 키로 쓸 수 있는 모델 리스트를 다 가져옴
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    
                    # 우선순위: 1.5 Pro -> 1.5 Flash -> 1.0 Pro
                    if any('gemini-1.5-pro' in m for m in available_models):
                        # 리스트에서 정확한 이름(models/gemini-1.5-pro-001 등)을 찾아서 씀
                        target_model = [m for m in available_models if 'gemini-1.5-pro' in m][0]
                    elif any('gemini-1.5-flash' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-1.5-flash' in m][0]
                    elif any('gemini-pro' in m for m in available_models):
                        target_model = [m for m in available_models if 'gemini-pro' in m][0]
                        
                except Exception as e:
                    # 리스트 조회 실패 시 그냥 기본값 사용
                    pass
                
                # 자동으로 찾은 모델 이름으로 설정
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
                - 분량: 400자~600자
                - 미사여구보다 구체적 사실(Fact) 위주로 작성할 것.
          # 작성 원칙 (매우 중요)
                1. **No Hallucination (날조 금지)**: 사용자가 입력한 내용에 없는 사실을 절대 지어내지 마십시오. 만약 입력된 정보가 부족하면 문장을 화려하게 꾸미기보다 있는 사실을 담백하게 서술하십시오.
                2. **3-Point Rule (3요소 포함)**: 입력된 텍스트에서 **최소 3가지만큼의 구체적인 에피소드나 키워드**를 찾아내어 문단에 포함시키십시오. (만약 입력 정보가 3가지 미만이라면 있는 것만 활용하십시오.)
                3. **Structure (구성)**: [구체적 사례] → [학생의 행동/태도] → [성장/잠재력 평가]의 흐름을 유지하십시오.
                
                위 원칙을 지켜 500자~700자 분량의 '행동특성 및 종합의견'을 작성하세요.
                """
                
                response = model.generate_content(system_prompt)
                
                st.success("작성 완료!")
                st.caption(f"※ 사용된 AI 모델: {target_model}") # 어떤 모델이 쓰였는지 보여줌
                st.text_area("결과 (복사해서 사용하세요)", value=response.text, height=300)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
                st.info("여전히 오류가 난다면, GitHub의 requirements.txt 파일 내용을 확인해주세요.")



