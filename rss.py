import feedparser
from craw_url import catch_yahoo_finance,catch_reuters,catch_cnbc,catch_fin_post,catch_fox,catch_motley_fool
import json

#以google news爬蟲
def rss_mutual(key):
    urlList = [
        f'https://news.google.com/rss/search?q={key}%20site:finance.yahoo.com%20when:7d&hl=en-US&gl=US&ceid=US:en',
        f'https://news.google.com/rss/search?q={key}%20site:Reuters.com%20when:7d&hl=en-US&gl=US&ceid=US:en',
        f'https://news.google.com/rss/search?q={key}%20site:CNBC.com%20when:7d&hl=en-US&gl=US&ceid=US:en',
        f'https://news.google.com/rss/search?q={key}%20site:financialpost.com%20when:7d&hl=en-US&gl=US&ceid=US:en',
        f'https://news.google.com/rss/search?q={key}%20site:foxbusiness.com%20%22Tesla%22%20when:7d&hl=en-US&gl=US&ceid=US:en',
        f'https://news.google.com/rss/search?q={key}%20site:fool.com%20when:7d&hl=en-US&gl=US&ceid=US:en'
    ]
    List_wc = ""
    List_json = []
    for i in range(6):
        d = feedparser.parse(urlList[i])
        for art in d.entries:
            if i == 0:
                data = {
                    "source": art.source.title,
                    "title": art.title.replace(art.source.title, '').replace(' -',''),
                    "url": art.link,
                    "date": art.published,
                    "content": catch_yahoo_finance(art.link)
                }
            if i==1:
                data = {
                    "source": art.source.title,
                    "title": art.title.replace(art.source.title, '').replace(' -',''),
                    "url": art.link,
                    "date": art.published,
                    "content": catch_reuters(art.link)
                }
            if i==2:
                data = {
                    "source": art.source.title,
                    "title": art.title.replace(art.source.title, '').replace(' -',''),
                    "url": art.link,
                    "date": art.published,
                    "content": catch_cnbc(art.link)
                }
            if i==3:
                data = {
                    "source": art.source.title,
                    "title": art.title.replace(art.source.title, '').replace(' -',''),
                    "url": art.link,
                    "date": art.published,
                    "content": catch_fin_post(art.link)
                }
            if i==4:
                data = {
                    "source": art.source.title,
                    "title": art.title.replace(art.source.title, '').replace(' -',''),
                    "url": art.link,
                    "date": art.published,
                    "content": catch_fox(art.link)
                }
            if i == 5:
                data = {
                    "source": art.source.title,
                    "title": art.title.replace(art.source.title, '').replace(' -',''),
                    "url": art.link,
                    "date": art.published,
                    "content": catch_motley_fool(art.link)
                }
            List_json.append(data)
            List_wc = List_wc + art.title.replace(art.source.title, '').replace(' -','') + '\n'
    with open('net/headline/news_content.json', 'w', encoding='utf-8') as f:
        json.dump(List_json,f)
    #with open('net/headline/articleList.txt', 'w' ,encoding='utf-8') as t:
        #t.write(List_wc)

#x,y = rss_mutual('Tesla')

