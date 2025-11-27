import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="2025 생기부 메이트", page_icon="📝", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; font-family: 'Helvetica', sans-serif; }
    .stTextArea textarea { background-color: #F7F9FB; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 16px; line-height: 1.6; }
    h1 { font-weight: 700; color: #333333; letter-spacing: -1px; }
    .subtitle { font-size: 16px; color: #888888; margin-top: -15px; margin-bottom: 30px; }
    .stButton button { background-color: #2E86C1; color: white; border-radius: 8px; font-weight: bold; border: none; }
    .stButton button:hover { background-color: #1B4F72; }
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
                - 분량: 500자~700자
                - 미사여구보다 구체적 사실(Fact) 위주로 작성할 것.
                """
                
                response = model.generate_content(system_prompt)
                
                st.success("작성 완료!")
                st.caption(f"※ 사용된 AI 모델: {target_model}") # 어떤 모델이 쓰였는지 보여줌
                st.text_area("결과 (복사해서 사용하세요)", value=response.text, height=300)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
                st.info("여전히 오류가 난다면, GitHub의 requirements.txt 파일 내용을 확인해주세요.")
                
# --- 1. 페이지 설정 (Notion 스타일) ---
st.set_page_config(
    page_title="2025 생기부 메이트",
    page_icon="📝",
    layout="centered"
)

# CSS 스타일
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; font-family: 'Helvetica', sans-serif; }
    .stTextArea textarea { background-color: #F7F9FB; border: 1px solid #E0E0E0; border-radius: 8px; font-size: 16px; line-height: 1.6; }
    h1 { font-weight: 700; color: #333333; letter-spacing: -1px; }
    .subtitle { font-size: 16px; color: #888888; margin-top: -15px; margin-bottom: 30px; }
    .stButton button { background-color: #2E86C1; color: white; border-radius: 8px; font-weight: bold; border: none; }
    .stButton button:hover { background-color: #1B4F72; }
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
# pills가 없으면 multiselect로 대체됨 (버전 호환성)
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
                # --- 여기가 중요합니다! (들여쓰기 주의) ---
                genai.configure(api_key=api_key)
                
                # 모델 이름을 1.5-pro로 설정 (가장 안전하고 성능 좋음)
                model = genai.GenerativeModel('gemini-1.5-pro')

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
                - 분량: 500자~700자
                - 미사여구보다 구체적 사실(Fact) 위주로 작성할 것.
                """
                
                response = model.generate_content(system_prompt)
                
                st.success("작성 완료!")
                st.text_area("결과 (복사해서 사용하세요)", value=response.text, height=300)

            except Exception as e:
                # --- 여기가 except 블록입니다 (오류 잡는 곳) ---
                st.error(f"오류가 발생했습니다: {e}")
                st.markdown("---")
                st.info("💡 팁: '404' 오류가 뜨면 models/gemini-1.5-pro 대신 models/gemini-pro 로 코드를 바꿔보세요.")


