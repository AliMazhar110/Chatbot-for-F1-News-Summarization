import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Formula+1&'
       'from=2010-10-25&'
       'sortBy=date&'
       'apiKey=033281b480d844d4a83cef16377f9565')

response = requests.get(url)

print (response.json)