import streamlit as st
import requests
import fitz  # PyMuPDF
from io import BytesIO
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="ChatPDF 챗봇", layout="centered")
st.title("📚 ChatPDF 챗봇")

# 세션 상태 초기화
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# PDF 링크 입력
pdf_url = st.text_input("PDF 파일의 URL을 입력하세요:")

# PDF 링크에서 텍스트 추출
if pdf_url:
    try:
        # PDF 파일 다운로드
        response = requests.get(pdf_url)
        if response.status_code == 200:
            # PDF 파일을 BytesIO 객체로 읽기
            pdf_file = BytesIO(response.content)
            # fitz.open()에서 BytesIO 객체를 파일처럼 처리하도록 수정
            pdf_reader = fitz.open(stream=pdf_file)  # stream 파라미터로 전달
            pdf_text = ""
            
            # 모든 페이지에서 텍스트 추출
            for page_num in range(pdf_reader.page_count):
                page = pdf_reader.load_page(page_num)
                pdf_text += page.get_text()

            # 세션 상태에 텍스트 저장
            st.session_state.pdf_text = pdf_text
            st.success("PDF 파일이 성공적으로 로드되었습니다.")

            # PDF 내용 일부 미리보기
            st.text_area("PDF 내용 미리보기", value=pdf_text[:1000], height=200)

        else:
            st.error("PDF 파일을 다운로드할 수 없습니다. URL을 확인해주세요.")
    except Exception as e:
        st.error(f"PDF 파일 다운로드 또는 처리 중 오류 발생: {str(e)}")

# 질의응답
if st.session_state.pdf_text:
    user_query = st.text_input("질문을 입력하세요:")

    if user_query:
        if "api_key" in st.session_state and st.session_state.api_key:
            try:
                client = OpenAI(api_key=st.session_state.api_key)
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{
                        "role": "system", 
                        "content": "You are a chatbot that answers questions based on the content of a provided PDF."
                    },{
                        "role": "user", 
                        "content": f"PDF 내용을 바탕으로 다음 질문에 답하세요: {user_query}"
                    }],
                    temperature=0.3,
                    max_tokens=500
                )

                answer = response.choices[0].message.content
                st.markdown(f"**🤖 답변:** {answer}")

            except Exception as e:
                st.error(f"질의응답 처리 중 오류 발생: {str(e)}")
        else:
            st.warning("API Key를 입력해주세요.")
    
    # Clear 버튼 (PDF 내용 제거)
    if st.button("🧹 Clear PDF 내용"):
        st.session_state.pdf_text = ""
        st.success("PDF 내용이 초기화되었습니다.")

else:
    st.warning("PDF URL을 입력해주세요.")

