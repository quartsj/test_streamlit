import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="GPT-4.1 Mini 질문 응답기", layout="centered")

# API Key 세션 저장
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
api_key_input = st.text_input("OpenAI API Key를 입력하세요:", type="password", value=st.session_state.api_key)
st.session_state.api_key = api_key_input

# 페이지 선택
page = st.sidebar.radio("페이지 선택", ["Q&A", "Chat"])

# GPT 응답 캐시 함수 (Q&A용)
@st.cache_data(show_spinner="GPT 응답 생성 중...")
def get_gpt_response(api_key, model, temperature, question):
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

# === Q&A 페이지 ===
if page == "Q&A":
    st.title("GPT-4.1 Mini 질문 응답기 - Q&A")

    model = st.selectbox("사용할 모델을 선택하세요:", ["gpt-3.5-turbo", "gpt-4.1-mini"], index=1)
    temperature = st.slider("창의성(temperature) 설정:", 0.0, 1.0, 0.7, step=0.1)
    question = st.text_area("질문을 입력하세요:", height=150)

    if st.button("질문하기"):
        if not st.session_state.api_key:
            st.error("OpenAI API Key를 입력해주세요.")
        elif not question.strip():
            st.error("질문을 입력해주세요.")
        else:
            try:
                answer = get_gpt_response(st.session_state.api_key, model, temperature, question.strip())
                st.success("GPT의 답변:")
                st.write(answer)
            except Exception as e:
                st.error(f"오류 발생: {str(e).encode('utf-8', errors='ignore').decode('utf-8')}")

# === Chat 페이지 ===
elif page == "Chat":
    st.title("GPT-4.1 Mini 챗봇")

    # 대화 상태 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "당신은 친절한 AI 챗봇입니다."}]

    # 모델 및 창의성 설정
    model = st.selectbox("사용할 모델을 선택하세요:", ["gpt-3.5-turbo", "gpt-4.1-mini"], index=1, key="chat_model")
    temperature = st.slider("창의성(temperature) 설정:", 0.0, 1.0, 0.7, step=0.1, key="chat_temp")

    # Clear 버튼: 대화 초기화
    if st.button("🧹 Clear 대화 초기화"):
        st.session_state.messages = [{"role": "system", "content": "당신은 친절한 AI 챗봇입니다."}]
        st.experimental_rerun()

    # 이전 대화 내용 표시
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(f"**🧑 사용자:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🤖 GPT:** {msg['content']}")

    # 사용자 입력
    user_input = st.text_input("메시지를 입력하세요:", key="chat_input")
    if user_input and st.session_state.api_key:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            client = OpenAI(api_key=st.session_state.api_key)
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=500,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()

        except Exception as e:
            st.error(f"오류 발생: {str(e).encode('utf-8', errors='ignore').decode('utf-8')}")
