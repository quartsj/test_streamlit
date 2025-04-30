import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="GPT-4.1 Mini 질문 응답기", layout="centered")
st.title("GPT-4.1 Mini 질문 응답기")

api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

model = st.selectbox(
    "사용할 모델을 선택하세요:",
    options=["gpt-3.5-turbo", "gpt-4.1-mini"],
    index=1
)

temperature = st.slider("창의성(temperature) 설정:", 0.0, 1.0, 0.7, step=0.1)

question = st.text_area("질문을 입력하세요:", height=150)

if st.button("질문하기"):
    if not api_key:
        st.error("OpenAI API Key를 입력해주세요.")
    elif not question.strip():
        st.error("질문을 입력해주세요.")
    else:
        try:
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

            answer = response.choices[0].message.content
            st.success("GPT의 답변:")
            st.write(answer)

        except Exception as e:
           st.error(f"오류 발생: {str(e).encode('utf-8', errors='ignore').decode('utf-8')}")
