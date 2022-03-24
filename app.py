from flask import Flask, jsonify
from packages.models import News, NewsSchema
from packages.db import db
from packages import crawler
import os

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'news.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# print(os.path.exists(os.path.join(basedir, 'news.db')))


def update_db():
    db_seed()


@app.cli.command('test')
def test():
    crawler.test()


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('database dropped!')


@app.cli.command('db_seed')
def db_seed():
    articles = crawler.get_articles(debug=DEBUG)

    for article in articles:
        test = News.query.filter_by(title=article['title']).first()
        if test:
            continue

        a = News(title=article['title'],
                 author=article['author'],
                 image=article['image'],
                 snippet=article['snippet'],
                 content=article['content'],
                 category=article['category'],
                 date_published=article['date_published']
                 )

        db.session.add(a)

    db.session.commit()
    print('database seeded!')


@app.route('/fetch_article/<string:input_category>', methods=['GET'])
def fetch_category(input_category: str):
    if input_category not in crawler.categories:
        return jsonify(message="Request must either in the list of categories: ['headlines', 'opinion', 'nation', "
                               "'world', 'business', 'sports', 'entertainment', 'lifestyle']"), 406

    return jsonify(crawler.fetch_article(input_category, debug=DEBUG))


@app.route('/category/<string:input_category>', methods=['GET'])
def category(input_category: str):
    if input_category not in crawler.categories:
        return jsonify(message="Request must either in the list of categories: ['headlines', 'opinion', 'nation', "
                               "'world', 'business', 'sports', 'entertainment', 'lifestyle']"), 406

    articles_list = News.query.filter_by(category=input_category)
    result = articles_schema.dump(articles_list)

    return jsonify(result)


article_schema = NewsSchema()
articles_schema = NewsSchema(many=True)


if __name__ == '__main__':
    app.run(debug=DEBUG)
