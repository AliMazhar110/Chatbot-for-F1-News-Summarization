from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from newspaper import Article
import re

root = "https://www.google.com/"

def nlp(text_data):
    no_whitespaces = ' '.join(text_data.split())
    urls = re.compile(r'https?://\S+|www\.\S+')
    no_url = urls.sub(r'', no_whitespaces)
    no_special_characters = re.sub('[^A-Za-z0-9. ]+', '', no_url)
    emojis = re.compile("["
          u"\U0001F600-\U0001F64F"  # emoticons
          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
          u"\U0001F680-\U0001F6FF"  # transport & map symbols
          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
    return emojis.sub(r'', no_special_characters)

def news(link):
    req = Request(link, headers = {'User-Agent':'Chrome/106.0.5249.119'})
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html5lib')
    # print(soup)
    for item in soup.find_all('div', attrs = {'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'}):
        raw_link = (item.find('a', href = True)['href'])
        link = (raw_link.split('/url?q=')[1]).split('&sa=U&')[0]
            
        title = (item.find('div', attrs = {'class': 'BNeawe vvjwJb AP7Wnd'}).get_text())

        title = title.replace(',', '')
        description = 'a'
        summary = 'a'
        try:
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()
            description = nlp(article.text)
            summary = nlp(article.summary)
        except:
            pass

        print(nlp(title))
        print(summary)
        print(link)
        print()

        document = open("/home/khal-drog0/Codes/Chatbot_News_Summarization/data.csv", "a")
        document.write('{}, {}, {}, {}\n'.format(title, link, summary, description))
        document.close()
      
    next = soup.find('a', attrs = {'aria-label': 'Next page'})
    next = (next['href'])
    link = root + next
    news(link)

link = "https://www.google.com/search?q=formula+1&tbs=cdr:1,cd_min:10/25/2014,cd_max:10/24/2015,sbd:1&tbm=nws&sxsrf=ALiCzsbRfc2_FgFkydvQTCVgRz5_CdWIAQ:1666706048622&source=lnt&sa=X&ved=2ahUKEwij--Pvw_v6AhWbFLcAHQB7Bf0QpwV6BAgCECE&biw=1536&bih=714&dpr=1.25"

news(link)
