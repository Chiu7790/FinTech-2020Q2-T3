import matplotlib.pyplot as plt
from summa import summarizer
import streamlit as st
from streamlit_quill import st_quill
import os
import json
import pandas as pd
import jsonpath
import base64

from io import BytesIO

# 這邊的news_content.json放入新用好的data名稱（關聯詞跟關鍵字的新聞data)
data = pd.read_json('net/headline/news_content.json')
b = str()
for x in range(len(data)):
  a = str(data.iloc[x]['articles']['content'])
  b += a
file = open('txtfile/test.txt', 'wt', encoding="utf-8")
file.write(b)
file.close()

def sumy_summarizer(docx):
  parser = PlaintextParser.from_string(docx,Tokenizer("english"))
  lex_summarizer = LexRankSummarizer()
  summary = lex_summarizer(parser.document,3)
  summary_list = [str(sentence) for sentence in summary]
  result = ' '.join(summary_list)
  return result

st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    st.title("關聯詞自動摘要")

    articles=''
    with open('txtfile/test.txt', mode='r',encoding="utf-8") as fp:
        articles = fp.read()

    input_sent = st.text_area("原文", articles, height=400)
    ratio = st.slider("從原文中抽取出 摘要的程度", min_value=0.000, max_value=1.0, value=0.002, step=0.001)
    summarized_text = summarizer.summarize(
        input_sent, ratio=ratio, language="english", split=True, scores=True
    )

    s_text=''
    for i in range(len(summarized_text)):
        s_text += ' ' + summarized_text[i][0]
    file = 'output.txt'
    with open('output/'+file, 'w', encoding='utf-8') as f:
        f.write(s_text)
    b64 = base64.b64encode(s_text.encode()).decode()
    new_filename = "output.txt"
    st.markdown("#### Download File ###")
    markdown_style = ("font-size: 450% ; baskground-color:red;")
    href = f'<a href="data:file/txt;base64,{b64}" download=new_filename>Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)
    st.info(s_text)

if __name__ == '__main__':
    main()

