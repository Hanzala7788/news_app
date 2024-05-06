import os
from flask import Flask, render_template, request
from newsapi import NewsApiClient
from flask_caching import Cache
# Init Flask app
app = Flask(__name__)
app.config.from_object('config')

# Init NewsAPI client
newsapi = NewsApiClient(api_key=app.config['NEWS_API_KEY'])

# Initialize cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def get_sources_and_domains():
    sources = []
    domains = []
    for source in newsapi.get_sources()['sources']:
        sources.append(source['id'])
        domain = source['url'].replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        domains.append(domain)
    return ', '.join(sources), ', '.join(domains)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        keyword = request.form['keyword']
        sources, domains = get_sources_and_domains()
        cached_data = cache.get(keyword)
        if cached_data:
            all_articles = cached_data
        else:
            all_articles = newsapi.get_everything(q=keyword, sources=sources, domains=domains, language='en', sort_by='relevancy')['articles']
            cache.set(keyword, all_articles, timeout=app.config['CACHE_TIMEOUT'])
        return render_template('home.html', all_articles=all_articles, keyword=keyword)
    else:
        cached_data = cache.get('top_headlines')
        if cached_data:
            all_headlines = cached_data
        else:
            all_headlines = newsapi.get_top_headlines(country=app.config['DEFAULT_COUNTRY'], language='en')['articles']
            cache.set('top_headlines', all_headlines, timeout=app.config['CACHE_TIMEOUT'])
        return render_template('home.html', all_headlines=all_headlines)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])