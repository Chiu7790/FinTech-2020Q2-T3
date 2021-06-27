import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup


def risk_free_rate(start_date, end_date):
    # 爬取網頁
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 整理並補齊缺漏數據
    b = ["".join(data.getText().split())
         for data in soup.find_all('td', {'class': 'text_view_data'})]
    cleaned = [b[i:i+13] for i in range(0, len(b), 13)]
    df = pd.DataFrame(cleaned, columns=[h.getText()
                                        for h in soup.find_all('th')])
    df.index = df['Date']
    df = df.drop('Date', axis=1).replace(
        'N/A', 0).drop('10/11/10').drop('04/14/17').astype(float)
    df.index = pd.to_datetime(df.index)

    for i in range(0, len(df)):
        for d in range(0, 12):
            try:
                if df.iloc[i][d] == 0 and df.iloc[i][d+1] != 0:
                    df.iloc[i][d] = df.iloc[i][d+1]
                elif df.iloc[i][d] == 0 and df.iloc[i][d+1] == 0:
                    df.iloc[i][d] = df.iloc[i][d+2]
            except:
                if df.iloc[i][d] == 0 and df.iloc[i][d-1] != 0:
                    df.iloc[i][d] = df.iloc[i][d-1]
                pass

    # 取得 1 年期公債table，並計算區間內的無風險利率平均值
    df_1yr = df[['1 yr']]
    df_time_interval = df_1yr.loc[start_date:end_date]
    treasury_mean = df_time_interval['1 yr'].mean() / 100
    return treasury_mean


def CAPM_daily(data_target, data_market,start_date, end_date, stock_market, stock_target):
    data_target.reset_index(inplace=True)
    data_market.reset_index(inplace=True)

    # Create a dataframe with the close
    data = pd.DataFrame(
        {'Invest_Close': data_target['Close'], 'Market_Close': data_market['Close']})

    # Calc the stock and market retuens by computing log(n)/log(n-1)
    data[['Invest_Ret', 'Market_Ret']] = np.log(
        data[['Invest_Close', 'Market_Close']]/data[['Invest_Close', 'Market_Close']].shift(1))
    # Drop null values
    data.dropna(inplace=True)

    # Generate covarience matrix & Calc beta from matrix
    beta_form = (data[['Invest_Ret', 'Market_Ret']].cov() /
                 data['Market_Ret'].var()).iloc[0].iloc[1]
    # Calc beta from regression
    beta_reg, alpha_reg = np.polyfit(
        x=data['Market_Ret'], y=data['Invest_Ret'], deg=1)

    # Calc expected return
    risk_free_return = risk_free_rate(start_date, end_date)
    expected_return = round(risk_free_return + beta_reg *
                            (data["Market_Ret"].mean()*365-risk_free_return), 4)

    # format return value
    beta = '{:.4f}'.format(beta_reg)
    alpha = '{:.4f}'.format(alpha_reg)
    expected_rm = '{:.2%}'.format(expected_return)

    #Plot the CAPM model
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))

    # Plot zero return axis
    plt.axvline(0, color='grey', alpha=0.5)
    plt.axhline(0, color='grey', alpha=0.5)

    # Plot scattterplot & lineplot
    sns.scatterplot(x='Market_Ret', y='Invest_Ret',
                    data=data, label='Daily Returns')
    sns.lineplot(x=data['Market_Ret'], y=alpha_reg + data['Market_Ret'] * beta_reg, label='CAPM Line', color='lightblue')

    plt.xlabel(f'Market Daily Return : {stock_market}')
    plt.ylabel(f'Investment Daily Return : {stock_target}')
    plt.legend(loc=0, frameon=True, facecolor='white')
    plt.title('Daily Return Scatter Plot with CAPM Regression',
            fontsize=16, fontweight='bold')
    plt.savefig('report/stock/img/capm.png')
    return beta, alpha, expected_rm, risk_free_return

