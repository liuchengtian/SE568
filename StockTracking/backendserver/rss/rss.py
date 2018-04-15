import feedparser

def feed(ticker: str):
    rss_url = 'http://finance.yahoo.com/rss/headline?s=' + ticker
    # get rss
    feeds = feedparser.parse(rss_url)
    rss = dict()
    # get version of rss
    # print(feeds.version)

    # get http head
    # print(feeds.headers)
    # print(feeds.headers.get('Content-Type'))

    # rss title
    rss['title'] = feeds['feed']['title']
    # rss link
    rss['link'] = feeds['feed']['link']
    # rss subtitle
    rss['sub title'] = feeds['feed']['subtitle']
    # number of articles
    n = len(feeds['entries'])
    rss['number'] = n
    rss['article'] = []

    for i in range(n):
        rss['article'][i] = dict()
        rss['article'][i]['index'] = i
        rss['article'][i]['title'] = feeds['entries'][i]['title']
        rss['article'][i]['link'] = feeds['entries'][i]['link']
        rss['article'][i]['date'] = feeds['entries'][i]['published_parsed']
        rss['article'][i]['summary'] = feeds['entries'][i]['summary']

    return rss