import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="2025 생기부 메이트", layout="centered")
st.title("🤖 2025 생기부 메이트")
st.markdown("<p style='color:#888;'>Gift for 2025 1st Grade Teachers</p>", unsafe_allow_html=True)
st.divider()

# 2. 사이드바 (API 키 및 설정)
with st.sidebar:
    st.header("설정")
    # 선생님이 직접 키를 제공하고 싶다면 이 부분을 Secrets로 처리해야 하지만, 
    # 일단은 각자 입력하는 방식으로 안전하게 갑니다.
    api_key = st.text_input("OpenAI API Key", type="password")
    st.info("학생의 특징을 대화하듯 편하게 입력해주세요.\nAI가 생기부 문구로 정리해줍니다.")
    
    options = ["자동(전체)", "학업역량", "인성/공동체", "진로적성", "발전가능성"]
    selected_mode = st.selectbox("어떤 부분을 강조할까요?", options)

# 3. 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "선생님, 안녕하세요! 2025 생기부 메이트입니다. 학생의 에피소드나 특징을 알려주시면 멋진 문장을 만들어 드릴게요."
    })

# 4. 화면 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 입력 및 처리
if prompt := st.chat_input("예: 수학 질문이 많고, 체육대회 때 응원단장을 함."):
    if not api_key:
        st.error("왼쪽 사이드바에 API Key를 먼저 입력해주세요!")
    else:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            system_role = f"당신은 고등학교 생기부 작성 전문가입니다. 사용자가 입력한 학생 정보를 바탕으로 [{selected_mode}] 위주로 구체적이고 전문적인 '행동특성 및 종합의견'을 작성해주세요."

            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True,
                )

                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"오류 발생: {e}")