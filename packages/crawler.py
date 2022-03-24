from bs4 import BeautifulSoup
from .datetime_manager import get_timestamp
import requests
import unicodedata

class_names = ['titleForFeature', 'news_title', 'carousel__item__title']
article_class_names = {'title': 'article__title',
                       'author': 'article__credits-author-pub',
                       'date_published': 'article__date-published',
                       'content': 'article__writeup'
                       }
categories = ['headlines', 'opinion', 'nation', 'world', 'business', 'sports', 'entertainment', 'lifestyle']
url = 'https://www.philstar.com/'


def get_soup(url):
    html_doc = requests.get(url)
    return BeautifulSoup(html_doc.text, 'html.parser')


def get_article(tree, category):
    content_url = tree.a['href']
    content_doc = requests.get(content_url)
    if content_doc.status_code == 404:
        return False

    content_soup = BeautifulSoup(content_doc.text, 'html.parser')
    raw = content_soup.find_all(class_=article_class_names.values())
    article = {k: clean_text("".join(raw[i].stripped_strings)) for i, k in enumerate(article_class_names)}
    image = 'none'

    if content_soup.find(class_='article__lead_photo'):
        image = content_soup.find(class_='article__lead_photo').img['src']

    article.update({'image': image,
                    'date_published': get_timestamp(article['date_published']),
                    'category': category})

    return article


def get_articles(debug=False):
    articles = []
    for category in categories:
        soup = get_soup(url + category)
        trees = soup.find_all(class_=class_names)

        if debug:
            print(f'========={category.upper()}============')

        for tree in trees:
            article = get_article(tree, category)

            if debug:
                print(f'{article}\n')

            if not article:
                continue

            articles.append(article)

    return articles


def fetch_article(category, debug=False):
    articles = []
    uri = url + category
    soup = get_soup(uri)
    trees = soup.find_all(class_=class_names)

    if debug:
        print(f'========={category.upper()}============')

    for tree in trees:
        article = get_article(tree, category)

        if debug:
            print(f'{article}\n')

        if not article:
            continue

        articles.append(article)

    return articles


def clean_text(text):
    return unicodedata.normalize('NFKD', text)


def test():
    articles = []
    for category in categories:
        soup = get_soup(url + category)
        trees = soup.find_all(class_=class_names)

        for tree in trees:
            article = get_article(tree, category)

            if not article:
                continue
            articles.append(article)

    return articles


