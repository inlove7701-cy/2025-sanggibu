import streamlit as st
import google.generativeai as genai
import importlib.metadata # 버전 확인용

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 생기부 메이트",
    page_icon="📝",
    layout="centered"
)

# --- 2. [디자인] 숲속 테마 CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
    .stTextArea textarea { border-radius: 12px; border: 1px solid rgba(85, 124, 100, 0.2); background-color: #FAFCFA; }
    h1 { font-weight: 700; letter-spacing: -1px; color: #2F4F3A; } 
    .subtitle { font-size: 16px; color: #666; margin-top: -15px; margin-bottom: 30px; }
    
    .stButton button { 
        background-color: #557C64 !important; color: white !important;
        border-radius: 10px; font-weight: bold; border: none; 
        transition: all 0.2s ease; padding: 0.8rem 1rem; font-size: 16px !important; width: 100%; 
    }
    .stButton button:hover { background-color: #3E5F4A !important; transform: scale(1.01); }
    
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div { background-color: #E0E0E0 !important; border-radius: 10px; height: 6px !important; }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div { background-color: #D4AC0D !important; height: 6px !important; }
    div[data-testid="stSlider"] div[role="slider"] { background-color: transparent !important; box-shadow: none !important; border: none !important; height: 24px; width: 24px; }
    div[data-testid="stSlider"] div[role="slider"]::after {
        content: "★"; font-size: 32px; color: #D4AC0D !important; position: absolute; top: -18px; left: -5px; text-shadow: 0px 1px 2px rgba(0,0,0,0.2);
    }
    div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p { color: #557C64 !important; }

    div[data-testid="stRadio"] { background-color: transparent; }
    div[data-testid="stRadio"] > div[role="radiogroup"] { display: flex; justify-content: space-between; width: 100%; gap: 10px; }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        flex-grow: 1; background-color: #FFFFFF; border: 1px solid #E0E5E2; border-radius: 8px; padding: 12px; justify-content: center;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover { border-color: #557C64; background-color: #F7F9F8; }
    
    .guide-box { background-color: #F7F9F8; padding: 20px; border-radius: 12px; border: 1px solid #E0E5E2; margin-bottom: 25px; font-size: 14px; color: #444; line-height: 1.6; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
    .guide-title { font-weight: bold; margin-bottom: 8px; display: block; font-size: 15px; color: #557C64;}
    .count-box { background-color: #E3EBE6; color: #2F4F3A; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 14px; margin-bottom: 10px; text-align: right; border: 1px solid #C4D7CD; }
    .analysis-box { background-color: #FCFDFD; border-left: 4px solid #557C64; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #333; }
    .footer { margin-top: 50px; text-align: center; font-size: 14px; color: #888; border-top: 1px solid #eee; padding-top: 20px; }
    .card-title { font-size: 15px; font-weight: 700; color: #557C64; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API 키 설정 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    api_key = None

# --- [디버깅용] 버전 확인 ---
try:
    lib_version = importlib.metadata.version("google-generativeai")
except:
    lib_version = "알 수 없음"

# --- 4. 헤더 영역 ---
st.title("📝 2025 1학년부 행발 메이트")
st.markdown("<p class='subtitle'>Gift for 2025 1st Grade Teachers</p>", unsafe_allow_html=True)
st.divider()

# 사이드바에 버전 정보 표시 (문제 해결용)
with st.sidebar:
    st.caption(f"🔧 System Info: google-generativeai v{lib_version}")
    if lib_version < "0.8.3":
        st.error("⚠️ 라이브러리 버전이 낮습니다! requirements.txt를 업데이트하고 Reboot 하세요.")

if not api_key:
    with st.expander("🔐 관리자 설정 (API Key 입력)"):
        api_key = st.text_input("Google API Key", type="password")

# 작성 팁
st.markdown("""
<div class="guide-box">
    <span class="guide-title">💡 풍성한 생기부를 위한 작성 팁 (3-Point)</span>
    좋은 평가를 위해 아래 3가지 요소가 포함되도록 에피소드를 적어주세요.<br>
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

# --- 6. 3단계 작성 옵션 ---
st.markdown("### 2. 작성 옵션 설정")

with st.container(border=True):
    st.markdown('<p class="card-title">① 작성 모드 선택</p>', unsafe_allow_html=True)
    mode = st.radio(
        "모드", ["✨ 풍성하게 (내용 보강)", "🛡️ 엄격하게 (팩트 중심)"],
        horizontal=True, label_visibility="collapsed"
    )

with st.container(border=True):
    st.markdown('<p class="card-title">② 희망 분량 (공백 포함)</p>', unsafe_allow_html=True)
    target_length = st.slider("글자 수", 300, 1000, 500, 50, label_visibility="collapsed")

with st.container(border=True):
    st.markdown('<p class="card-title">③ 강조할 핵심 키워드 (다중 선택)</p>', unsafe_allow_html=True)
    filter_options = ["👑 AI 자동 판단", "📘 학업 역량", "🤝 공동체 역량", "🚀 진로 역량", "🌱 발전 가능성", "🎨 창의적 문제해결력", "😊 인성/나눔/배려", "⏰ 성실성/규칙준수"]
    try:
        selected_tags = st.pills("키워드 버튼", options=filter_options, selection_mode="multi", label_visibility="collapsed")
    except:
        selected_tags = st.multiselect("키워드 선택", filter_options, label_visibility="collapsed")

# [고급 설정] 모델 선택 (간소화됨)
st.markdown("")
with st.expander("⚙️ AI 모델 직접 선택하기 (고급 설정)"):
    manual_model = st.selectbox(
        "사용할 모델을 선택하세요",
        ["⚡ gemini-1.5-flash (기본값)", "🤖 gemini-1.5-pro (고성능)"],
        index=0
    )

# --- 7. 실행 및 결과 영역 ---
st.markdown("")
if st.button("✨ 생기부 문구 생성하기", use_container_width=True):
    if not api_key:
        st.error("⚠️ API Key가 설정되지 않았습니다.")
    elif not student_input:
        st.warning("⚠️ 학생 관찰 내용을 입력해주세요!")
    else:
        # 분량 계산
        min_len = int(target_length * 0.9)
        max_len = int(target_length * 1.1)
        
        with st.spinner(f'AI가 {min_len}~{max_len}자 분량으로 작성 중입니다...'):
            try:
                genai.configure(api_key=api_key)

                # --- [수정] 구버전 fallback 제거, 신버전 강제 ---
                if "pro" in manual_model:
                    target_model = "gemini-1.5-pro"
                else:
                    target_model = "gemini-1.5-flash" # 무조건 1.5 flash 사용

                # 모드별 설정
                if "엄격하게" in mode:
                    temp = 0.2
                    prompt_instruction = f"""
                    # ★★★ 엄격 작성 원칙 ★★★
                    1. **분량 준수**: 공백 포함 **{min_len}자 이상 {max_len}자 이하**로 작성.
                    2. **내용 부족 시**: 없는 사실 지어내지 말고, 교사의 교육적 평가로 보완.
                    3. **절대 날조 금지**: 입력 안 된 에피소드 금지.
                    """
                else:
                    temp = 0.75
                    prompt_instruction = f"""
                    # ★★★ 풍성 작성 원칙 ★★★
                    1. **분량 준수**: 공백 포함 **{min_len}자 이상 {max_len}자 이하**로 작성.
                    2. **내용 보강**: 문맥에 맞는 수식어와 의미 부여로 풍성하게.
                    3. 문장을 매끄럽게 연결.
                    """

                generation_config = genai.types.GenerationConfig(temperature=temp)
                model = genai.GenerativeModel(target_model, generation_config=generation_config)

                # 키워드 처리
                if not selected_tags:
                    tags_str = "별도 지정 없음. [인성/소통] -> [학업/태도] -> [진로/관심] -> [발전가능성] 순서 준수."
                else:
                    tags_str = f"핵심 키워드: {', '.join(selected_tags)}"

                system_prompt = f"""
                당신은 입학사정관 관점의 고등학교 교사입니다.
                입력 정보: {student_input}
                작성 지침: [{tags_str}]
                
                다음 두 파트로 나누어 출력 (구분선: "---SPLIT---")

                [Part 1] 영역별 분석 (개조식)
                - [인성 / 학업 / 진로 / 공동체] 요약
                
                ---SPLIT---

                [Part 2] 행동특성 및 종합의견 (서술형 종합본)
                - 문체: ~함, ~임
                - 구조: 사례 -> 행동 -> 성장/평가
                
                {prompt_instruction}
                """

                response = model.generate_content(system_prompt)
                full_text = response.text
                
                if "---SPLIT---" in full_text:
                    parts = full_text.split("---SPLIT---")
                    analysis_text = parts[0].strip()
                    final_text = parts[1].strip()
                else:
                    analysis_text = "영역별 분석 생성 실패"
                    final_text = full_text

                char_count = len(final_text)
                char_count_no_space = len(final_text.replace(" ", "").replace("\n", ""))
                
                byte_count = 0
                for char in final_text:
                    if ord(char) > 127: byte_count += 3
                    else: byte_count += 1
                
                st.success("작성 완료!")
                
                with st.expander("🔍 영역별 분석 내용 확인하기 (클릭)", expanded=True):
                    st.markdown(analysis_text)
                
                st.markdown("---")
                st.markdown("### 📋 최종 제출용 종합본")

                st.markdown(f"""
                <div class="count-box">
                    목표: {target_length}자 내외 | <b>실제: {char_count}자</b> (공백제외 {char_count_no_space}자)<br>
                    💾 <b>예상 바이트: {byte_count} Bytes</b> (NEIS 기준)
                </div>
                """, unsafe_allow_html=True)
                
                st.caption(f"※ {mode.split()[1]} 모드 | 사용 모델: {target_model}")
                st.text_area("결과 (복사해서 나이스에 붙여넣으세요)", value=final_text, height=350)

            except Exception as e:
                # 429: 사용량 초과 / 404: 모델 없음 (라이브러리 버전 문제)
                if "429" in str(e):
                    st.error("🚨 오늘 사용 가능한 무료 AI 횟수를 모두 쓰셨습니다!")
                elif "404" in str(e):
                    st.error("🚨 서버의 라이브러리 버전이 낮아서 '1.5-flash' 모델을 못 찾고 있습니다.")
                    st.warning("👉 GitHub에서 'requirements.txt' 파일을 열고 내용을 확인해주세요.")
                    st.code("streamlit\ngoogle-generativeai>=0.8.3")
                    st.info("수정 후 [Reboot App]을 하시면 해결됩니다.")
                else:
                    st.error(f"오류가 발생했습니다: {e}")

# --- 8. 푸터 ---
st.markdown("""
<div class="footer">
    © 2025 <b>[선생님 이름]</b>. All rights reserved.<br>
    문의: <a href="mailto:teacher@school.kr" style="color: #888; text-decoration: none;">teacher@school.kr</a>
</div>
""", unsafe_allow_html=True)




