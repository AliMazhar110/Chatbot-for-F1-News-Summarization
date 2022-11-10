import requests, json, re
from parsel import Selector

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
}

params = {
    "q": "formula 1",  # search query
    "hl": "en",              # language of the search
    "gl": "in",              # country of the search
    "num": "100",            # number of search results per page
    "tbm": "nws"             # news results
}

html = requests.get("https://www.google.com/search", headers=headers, params=params, timeout=30)
selector = Selector(text=html.text)

news_results = []

# extract thumbnails
all_script_tags = selector.css("script::text").getall()

for result, thumbnail_id in zip(selector.css(".xuvV6b"), selector.css(".FAkayc img::attr(id)")):
    thumbnails = re.findall(r"s=\'([^']+)\'\;var\s?ii\=\['{_id}'\];".format(_id=thumbnail_id.get()), str(all_script_tags))

    decoded_thumbnail = "".join([
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in thumbnails
    ])
    
    news_results.append(
        {
            "title": result.css(".MBeuO::text").get(),
            "link": result.css("a.WlydOe::attr(href)").get(),
            "source": result.css(".NUnG9d span::text").get(),
            "snippet": result.css(".GI74Re::text").get(),
            "date_published": result.css(".ZE0LJd span::text").get(),
            "thumbnail": None if decoded_thumbnail == "" else decoded_thumbnail
        }
    )

json_object = json.dumps(news_results, indent=2, ensure_ascii=False)

with open('scraped_data.json', 'w') as outfile:
    outfile.write(json_object)