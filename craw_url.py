import urllib.request as req
import bs4

#可爬取reuters, bussiness-insider, bloomberg(有時會失效), financialpost
#希望後續增加

def catch_reuters(url):
    adj_content = ''
    request = req.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find_all("p", class_="Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x")
    if content == []:
        content = root.find_all("p", class_="Text__text___3eVx1j Text__dark-grey___AS2I_p Text__regular___Bh17t- Text__large___1i0u1F Body__base___25kqPt Body__large_body___3g04wK ArticleBody__element___3UrnEs")
    try :
        for tag in content:
            if tag.string !=None:
                if "=====" not in tag.string:
                    adj_content += tag.string+' '
    except AttributeError:
        return ' '
    return adj_content

def catch_BI(url):
    adj_content = ''
    request_BI = req.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})
    with req.urlopen(request_BI) as response:
        data_BI = response.read()
    root_BI = bs4.BeautifulSoup(data_BI, "html.parser")
    content_BI = root_BI.find("div", class_="col-xs-12 news-content no-padding")
    if content_BI == None:
        content_BI = root_BI.find("div", class_="content-lock-content")

    try:
        for tag in content_BI.find_all('p'):
            if tag.find('span'):
                continue
            if tag.get('class'):
                continue
            if tag.find('em'):
                continue
            if tag.text != None:
                adj_content += tag.text + ' '
        for tag in content_BI.find_all('li'):
            if tag.text != None:
                if "Sign up" not in tag.text:
                    if "Pros" not in tag.text:
                        if "Details" not in tag.text:
                            adj_content += tag.text + ' '
    except AttributeError:
        return ' '
    return adj_content


def catch_bloomberg(url):
    adj_content = ''
    request = req.Request(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        })
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="body-columns")

    try:
        for i in content.find_all('p'):
            if i.find('span'):
                continue
            if i.text != None:
                if "Sign up" not in i.text:
                    if "Read more" not in i.text:
                        if "*" not in i.text:
                            if "Data:" not in i.text:
                                if "LISTEN:" not in i.text:
                                    if "— With" not in i.text:
                                        adj_content += i.text + ' '
        for j in content.find_all('h2'):
            if j.text != None:
                if "SHARE THIS ARTICLE" not in j.text:
                    if "LISTEN TO" not in j.text:
                        adj_content += j.text +' '
    except AttributeError:
        return ' '
    return adj_content


def catch_fin_post(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find_all("section", class_="article-content__content-group")

    try:
        for section in content:
            for i in section.find_all('p'):
                if i.find('em'):
                    continue
                if i.text != None:
                    if "_____________________________________________________________" not in i.text:
                        adj_content += i.text + ' '
            for j in section.find_all('h2'):
                if j.text != None :
                    if 'Article content' not in j.text:
                        if 'More On This Topic' not in j.text:
                            adj_content += i.text+' '
    except AttributeError:
        return ' '
    return adj_content

def catch_yahoo_finance(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="caas-body")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_cnbc(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find_all("div", class_="group")

    try:
        for sec in content:
            for i in sec.find_all('p'):
                if i.text != None:
                    adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_motley_fool(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("span", class_="article-content")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                adj_content += i.text.replace('"',' ') + ' '
    except AttributeError:
        return ' '
    except HTTPError:
        return ' '
    return adj_content

def catch_engadget(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="article-text")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_electrek(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="post-body")

    try :
        for i in content.find_all('p'):
            if i.text != None:
                if "Subscribe to Electrek" not in i.text:
                    adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_fox(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="article-body")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                if "Check out what's clicking on FoxBusiness.com." not in i.text:
                    if "(Reporting by" not in i.text:
                        if "CLICK HERE TO READ MORE" not in i.text:
                            if "GET FOX BUSINESS" not in i.text:
                                adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_ksl(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("article", id="kslMainArticle")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                if "Copyright ©" not in i.text:
                    adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_cointelegraph(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="post-content")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def catch_forbes(url):
    adj_content = ''
    request = req.Request(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
    with req.urlopen(request) as response:
        data = response.read()
    root = bs4.BeautifulSoup(data, "html.parser")
    content = root.find("div", class_="article-body fs-article fs-premium fs-responsive-text current-article font-body color-body bg-base font-accent article-subtype__masthead")

    try:
        for i in content.find_all('p'):
            if i.text != None:
                adj_content += i.text + ' '
    except AttributeError:
        return ' '
    return adj_content

def classify(url):
    if "reuters.com" in url:
        return catch_reuters(url)
    if "businessinsider.com" in url:
        return catch_BI(url)
    if "www.bloomberg.com" in url:
        return catch_bloomberg(url)
    if "financialpost.com" in url:
        return catch_fin_post(url)
    if "engadget.com" in url:
        return catch_engadget(url)
    if "electrek.co" in url:
        return catch_electrek(url)
    if "foxbusiness.com" in url:
        return catch_fox(url)
    if "ksl.com" in url:
        return catch_ksl(url)
    if "cointelegraph.com" in url:
        return catch_cointelegraph(url)
    if "forbes.com" in url:
        return catch_forbes(url)
    if "finance.yahoo.com" in url:
        return catch_yahoo_finance(url)
    else:
        pass


#classify('https://www.forbes.com/sites/theapothecary/2021/06/09/el-salvador-enacts-bitcoin-law-ushering-in-new-era-of-global-monetary-inclusion/')
catch_fin_post("https://financialpost.com/pmn/business-pmn/german-environmental-groups-file-objection-against-tesla-gigafactory-permit")