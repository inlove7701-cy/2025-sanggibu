import streamlit as st
import google.generativeai as genai

st.title("🛠️ 모델 진단 모드")

# API 키 설정
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = st.text_input("Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    if st.button("사용 가능한 모델 리스트 확인하기"):
        try:
            st.write("내 키로 사용할 수 있는 모델 목록:")
            # 사용 가능한 모델을 서버에 물어봐서 화면에 출력합니다.
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    st.code(m.name)
        except Exception as e:
            st.error(f"에러 발생: {e}")
                



