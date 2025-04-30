import streamlit as st
import openai

st.set_page_config(page_title="GPT-4.1 Mini 질문 응답기", layout="centered")
st.title(" GPT-4.1 Mini 질문 응답기")

api_key = st.text_input(" OpenAI API Key를 입력하세요:", type="password")

question = st.text_input(" 질문을 입력하세요:")

if st.button("질문하기"):
    if not api_key:
        st.error(" OpenAI API Key를 입력해주세요.")
    elif not question:
        st.error(" 질문을 입력해주세요.")
    else:
        try:
            openai.api_key = api_key

                response = openai.ChatCompletion.create(
                    model="gpt-4.1-mini",  
                    messages=[
                        {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500,
                )

                answer = response['choices'][0]['message']['content']
                st.success(" GPT의 답변:")
                st.write(answer)

        except Exception as e:
            st.error(f" 오류 발생: {e}")
