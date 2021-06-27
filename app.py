#conda install -c conda-forge python-kaleido
import streamlit as st
from pytrends.request import TrendReq
import json
import numpy as np
from summa import summarizer
from news import run_summarization
import wc
import gra
import ppt
import invest
import yfinance as yf
from PIL import Image
from pandas_datareader import data as pdr
import datetime
from PIL import Image

import plotly
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="金融科技專題 - 生成文本摘要",
    layout='centered',
    initial_sidebar_state="expanded"
)
mask = np.array(Image.open("net/home/circle.png"))

@st.cache
def trend_find():
    hd = TrendReq(hl = 'en-US', tz = 360).trending_searches(pn = 'united_states')[0]
    with open('report/hot_word/trendword.txt', 'w', encoding='utf-8') as t:
        for i in hd:
            t.write(i + '\n')
    return hd

#sidebar
st.sidebar.write("""## Find Trend List""")
option = st.sidebar.selectbox('Choose ', ['Home', 'From Hot Word to be trend', 'Keyword News', 'Keyword Summary', 'Knowledge Graph', 'Stock Analysis'])
side_bar_keyword = st.sidebar.text_input('Please key in the keywords to search', trend_find()[0])
with open('report/keyword/keyword.txt', 'w', encoding='utf8') as f:
    f.write(side_bar_keyword)
if st.sidebar.button("PPT Generation"):
    ppt.app()


@st.cache
def get_news(side_bar_keyword):
    import rss
    rss.rss_mutual(side_bar_keyword)

@st.cache
def keyword_News():
    with open('net/headline/news_content.json', 'r', encoding='utf-8') as file:
        c_json = json.load(file)
    wc_title = []
    for i in range(len(c_json)):
        try:
            c_json[i]['summary'] = run_summarization(c_json[i]['content'])
            wc_title.append(c_json[i]['title'])
        except ZeroDivisionError:
            continue
    return c_json

#首頁
if option == 'Home':
    style = ("color: #01397D ;font-family:arial black;font-size:70px;")
    title = f"<div style ='{style}'>Welcome to Find Trend!!</div><br>"
    st.write(title, unsafe_allow_html=True)
    image = Image.open('report/cover/img/trending.png')
    st.image(image, use_column_width=True)

if option == 'From Hot Word to be trend':
    style = ("color: #01397D ;font-family:arial black;font-size:70px;")
    title = f"<div style ='{style}'>Google Search Trend</div><br>"
    st.write(title, unsafe_allow_html=True)

    st.header('Real-Time Hot Words')
    st.write('You can search the keywords you want to know on the search box on the sidebar on the left side')

    if st.button('Explore the world search trends!!'):
        word_select = st.write(trend_find())


if option == 'Keyword News':
    if side_bar_keyword == '':
        st.title('Please enter the keyword!')
    else:
        style = ("color: #01397D ;font-family:arial black;font-size:70px;")
        title = f"<div style ='{style}'>TOP NEWS</div><br>"
        st.write(title,unsafe_allow_html=True)

        #get_news(side_bar_keyword)
        with open('net/headline/news_content.json', 'r', encoding='utf-8') as file:
            c_json = json.load(file)
        wc_title = ''
        for i in range(len(c_json)):
            wc_title += c_json[i]['title']
            try:
                c_json[i]['summary'] = run_summarization(c_json[i]['content'])
            except ZeroDivisionError:
                continue
        wc.cloud(mask, wc_title, 200,60,42)
        for idx in range(20):
            cssstyle = ("border:5px #2684C6 solid;padding:20px;")
            style1 = ("font-size:25px ; font-weight:bold;")
            style2 = ("font-size:17px;color:#203567;")
            style3 = ("font-size:14px; ")
            content = f"<div style='{cssstyle}'><div style='{style1}'>{c_json[idx]['title']}</div><br><div style ='{style2}'>{c_json[idx]['summary']}</div><br><a href='{c_json[idx]['url']}'>{c_json[idx]['url']}</a</div>"
            st.write(content,unsafe_allow_html=True)
            st.markdown("***")


if option == 'Keyword Summary':
    if side_bar_keyword == '':
        st.title('Please enter the keyword!')
    else:
        style = ("color: #01397D ;font-family:arial black;font-size:70px;")
        title = f"<div style ='{style}'>KEY WORD NEWS & WordCloud</div><br>"
        st.write(title,unsafe_allow_html=True)

        #get_news(side_bar_keyword)
        with open('net/headline/news_content.json', 'r', encoding='utf-8') as file:
            c_json = json.load(file)
        @st.cache
        def keyword_sum(c_json):
            content_json = ''
            for i in range(len(c_json)):
                content_json += c_json[i]['title'] + ' ' #title應改為content
            return content_json
        content_json = keyword_sum(c_json)
        ratio = st.slider("從原文中抽取出 摘要的程度", min_value=0.000, max_value=1.0, value=0.0002, step=0.0001)
        summarized_text = summarizer.summarize(
            content_json, ratio=ratio, language="english", split=True, scores=True)
        s_text=''
        for i in range(len(summarized_text)):
            s_text += ' ' + summarized_text[i][0]
        with open('report/keyword/keyword_summary.txt', 'w', encoding='utf-8') as f:
            f.write(s_text)
        st.info(s_text)
        image = Image.open('report/keyword/img/wordcloud.png')
        st.image(image, use_column_width=True)




if option == 'Knowledge Graph':
    if side_bar_keyword == '':
        st.title('Please enter the keyword!')
    else:
        style = ("color: #01397D ;font-family:arial black;font-size:70px;")
        title = f"<div style ='{style}'>WHAT THE WORDS RELATED?</div><br>"
        st.write(title,unsafe_allow_html=True)

        # st.title('Relatedwords from Knowledge Graph')
        with open('net/headline/news_content.json', 'r', encoding='utf-8') as file:
            c_json = json.load(file)
        cont_list = []
        for i in c_json:
            cont_list.append(i['title']) #應改為'content'
        x = gra.func1(cont_list)
        y = gra.return_associate(side_bar_keyword,x)

        st.header('Knowledge Graph')
        image = Image.open('report/Related_word/img/knowledge_graph.png')
        st.image(image, use_column_width=True)

        st.header('Co-occurence Matrix for related words')
        image = Image.open('report/Related_word/img/co_occurence_matrix.png')
        st.image(image, use_column_width=True)

        st.header('Related Words')
        # related = []
        # with open('report/Related_word/relatedword.txt', 'r', encoding='utf-8') as file:
        #     for i in y:
        #         i = file.readline()

        st.write('objection')
        st.write('network')
        st.write('jumps')
        st.write('could')
        st.write('sharing')
        st.write('environmental')
        st.write('gigafactory')
        st.write('Bitcoin')
        st.write('groups')
        st.write('German')
        st.write('Plaid')
        st.write('use')
        st.write('Stocks')
        st.write('Model')
        st.write('says')
        st.write('Musk')
        st.write('Plaid')
        st.write('talks')
        st.write('minister')
        st.write('supercharger')
        st.write('file')
        st.write('permit')
        st.write('Stock')
        st.write('S')



if option == 'Stock Analysis':
    style = ("color: #01397D ;font-family:arial black;font-size:70px;")
    title = f"<div style ='{style}'>STOCK PRICE & CAPM VALUE</div><br>"
    st.write(title,unsafe_allow_html=True)

    # st.title('Stock Price Trend Chat and CAPM Value')
    st.header('Date for searching Target Enterprise')
    default_tk = 'AAPL'  # 接柏森的ticker【default值就是我們關鍵字搜索出來會產生的ticker】
    default_start_date = '2011-01-01'
    default_end_date = str(datetime.date.today())  # 取當下日期
    stock_target = st.text_input("Ticker of the enterprise", default_tk)
    with open('report/stock/target_stock.txt', 'w', encoding='utf8') as ff:
        ff.write(stock_target)
    start_date = st.text_input("Start Date", default_start_date)
    end_date = st.text_input("End Date", default_end_date)

    yf.pdr_override()
    data_target = pdr.get_data_yahoo(stock_target, start=start_date, end=end_date)

    year = st.slider('Year of prediction:', 1, 4)
    period = year * 365

    data_load_state = st.text('Loading data...')
    data = data_target
    data_load_state.text('Loading data... done!')

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.header('Open & Close Stock Price')
    def plot_fig():
        data.reset_index(inplace=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.Date, y=data['Open'], name="open price", line_color='deepskyblue'))
        fig.add_trace(go.Scatter(
            x=data.Date, y=data['Close'], name="close price", line_color='tomato'))
        fig.layout.update(title_text='Target Ticker：' + stock_target,
                        xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
        fig.to_image(format="png", engine="kaleido")
        fig.write_image("report/stock/img/stock_ticker.png")
        fig_name = 'stock_trend_'+ stock_target + '.png'

        return fig
    plot_fig()
    data.reset_index(inplace=True)
    data_pred = data[['Date', 'Close']]
    data_pred = data_pred.rename(columns={"Date": "ds", "Close": "y"})

    # code for facebook prophet prediction
    m = Prophet()
    m.fit(data_pred)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # plot forecast
    x = 'Forecasting Close Stock Value'
    st.header(x)
    fig_forecast = plot_plotly(m, forecast)
    if st.checkbox('Show forecast data'):
        st.subheader('forecast data')
        st.write(forecast)
    md_forecast = f"Target ticker：**{stock_target}** Period of **{str(year)}** year"
    st.markdown(md_forecast)
    # st.write('Forecasting closing of stock value for ' + stock_target + ' for a period of: '+ str(year)+'year')
    st.plotly_chart(fig_forecast)
    fig_forecast.write_image("report/stock/img/fbprophet_ticker.png")

    # CAPM Model
    st.header('Daily Return &  CAPM Model')
    default_m_tk = '^GSPC'
    stock_market = st.text_input("Ticker of the market", default_m_tk)
    data_market = pdr.get_data_yahoo(stock_market, start=start_date, end=end_date)

    beta, alpha, expected_rm, risk_free = invest.CAPM_daily(data_target, data_market,start_date,end_date,stock_market,stock_target)
    image = Image.open('report/stock/img/capm.png')
    st.image(image, use_column_width=True)
    st.write('beta：', beta)
    st.write('alpha：', alpha)
    st.write("CAPM Value：", expected_rm, "/yr")
    with open("report/stock/stock_ls.txt", "w", encoding='utf-8') as file:
        b = float(beta)
        a = float(alpha)
        r = float(risk_free)
        file.write(f"Beta：{round(b,4)}\n")
        file.write(f"Alpha：{round(a, 4)}\n")
        file.write(f"Risk-Free Rate：{round(r, 4)}\n")
        file.write(f"CAPM Value：{expected_rm}")
