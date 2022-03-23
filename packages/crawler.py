from bs4 import BeautifulSoup
from .datetime_manager import get_timestamp
import requests
import unicodedata


def get_soup(url):
    html_doc = requests.get(url)
    return BeautifulSoup(html_doc.text, 'html.parser')


def get_raw_news(soup, class_name):
    if not soup.find_all(class_=f'{class_name}'):
        return False

    res = soup.find_all(class_=f'{class_name}')
    return res


def get_article(tree, category):

    content_url = tree.a['href']
    content_doc = requests.get(content_url)
    if content_doc.status_code == 404:
        return False

    content_soup = BeautifulSoup(content_doc.text, 'html.parser')

    title = content_soup.find(class_='article__title')
    title = "".join(title.stripped_strings)
    image = 'none'

    if content_soup.find(class_='article__lead_photo'):
        image = content_soup.find(class_='article__lead_photo').img['src']
    
    content = content_soup.find(class_='article__writeup')
    content = "".join(content.stripped_strings)
    author = content_soup.find(class_='article__credits-author-pub')
    author = "".join(author.stripped_strings)
    snippet = content[0:150] + '...'
    date_published = content_soup.find(class_='article__date-published')
    date_published = "".join(date_published.stripped_strings)

    article = {'title': title,
               'author': author,
               'image': image,
               'snippet': unicodedata.normalize("NFKD", snippet),
               'content': unicodedata.normalize("NFKD", content),
               'category': category,
               'date_published': get_timestamp(date_published)
               }

    return article


def get_articles(debug=False):
    url = 'https://www.philstar.com/'
    #categories = ['headlines', 'opinion', 'nation', 'world', 'business', 'sports', 'entertainment', 'lifestyle']
    categories = ['headlines']
    class_names = ['titleForFeature', 'news_title', 'carousel__item__title']
    articles = []

    for category in categories:
        uri = url + category
        soup = get_soup(uri)

        for class_name in class_names:
            trees = get_raw_news(soup, class_name)
            if not trees:
                continue

            for tree in trees:
                if debug:
                    print(tree)

                article = get_article(tree, category)
                if not article:
                    continue
                articles.append(article)

    print('Articles retrieved!')

    return articles
