import streamlit as st
from openai import OpenAI
from typing import Optional

# 사이트 레이아웃 설정
st.set_page_config(page_title="GPT-4.1 Mini 질문 응답기", layout="centered")
st.title("GPT-4.1 Mini 질문 응답기")

# API 키 입력 및 세션 상태에 저장
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key_input = st.text_input("OpenAI API Key를 입력하세요:", type="password", value=st.session_state.api_key)
st.session_state.api_key = api_key_input  # 업데이트 반영

# 모델 선택
model = st.selectbox(
    "사용할 모델을 선택하세요:",
    options=["gpt-3.5-turbo", "gpt-4.1-mini"],
    index=1
)

# temperature 설정
temperature = st.slider("창의성(temperature) 설정:", 0.0, 1.0, 0.7, step=0.1)

# 질문 입력
question = st.text_area("질문을 입력하세요:", height=150)

# GPT 응답을 캐시하는 함수
@st.cache_data(show_spinner="GPT 응답 생성 중...")
def get_gpt_response(api_key: str, model: str, temperature: float, question: str) -> Optional[str]:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
            {"role": "user", "content": question}
        ],
        temperature=temperature,
        max_tokens=500,
    )
    return response.choices[0].message.content

# 질문 버튼 클릭 시 처리
if st.button("질문하기"):
    if not st.session_state.api_key:
        st.error("OpenAI API Key를 입력해주세요.")
    elif not question.strip():
        st.error("질문을 입력해주세요.")
    else:
        try:
            answer = get_gpt_response(
                api_key=st.session_state.api_key,
                model=model,
                temperature=temperature,
                question=question.strip()
            )
            st.success("GPT의 답변:")
            st.write(answer)
        except Exception as e:
            st.error(f"오류 발생: {str(e).encode('utf-8', errors='ignore').decode('utf-8')}")
