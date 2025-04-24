# app.py
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Streamlit secrets から取得
openai_api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=openai_api_key,
)

def get_system_prompt(expert: str) -> str:
    return {
        "歴史家": "あなたは優秀な歴史家です。以下の質問に歴史的背景や具体例を交えて答えてください。",
        "心理カウンセラー": "あなたは共感力に優れた心理カウンセラーです。感情に寄り添う優しい口調で回答してください。",
        "プログラマー": "あなたはプロのソフトウェアエンジニアです。正確な技術的情報を交えて回答してください。",
    }.get(expert, "あなたは親切なアシスタントです。")

def generate_response(question: str, expert: str) -> str:
    msgs = [
        SystemMessage(content=get_system_prompt(expert)),
        HumanMessage(content=question),
    ]
    return chat(msgs).content

st.set_page_config(page_title="LLM専門家アプリ", layout="centered")
st.title("🎓 LLMに専門家として回答してもらおう")

expert_type = st.radio("専門家の種類を選んでください：", ["歴史家", "心理カウンセラー", "プログラマー"])
user_input = st.text_area("質問を入力してください")

if st.button("実行"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("LLMが考え中..."):
            st.success("✅ 回答が届きました！")
            st.write(generate_response(user_input, expert_type))
