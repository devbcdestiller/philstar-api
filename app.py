from flask import Flask, jsonify
from packages.models import News, NewsSchema
from packages.db import db
from packages import crawler
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'news.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

categories = ['headlines', 'opinion', 'nation', 'world', 'business', 'sports', 'entertainment', 'lifestyle']


def update_db():
    db_seed()


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
    articles = crawler.get_articles()

    for article in articles:
        a = News(title=article['title'],
                 author=article['author'],
                 image=article['image'],
                 snippet=article['snippet'],
                 content=article['content'],
                 category=article['category']
                 )

        db.session.add(a)

    db.session.commit()
    print('database seeded!')


@app.route('/category/<string:input_category>', methods=['GET'])
def category(input_category: str):
    if input_category not in categories:
        return jsonify(message="Request must either in the list of categories: ['headlines', 'opinion', 'nation', "
                               "'world', 'business', 'sports', 'entertainment', 'lifestyle']"), 406

    articles_list = News.query.filter_by(category=input_category)
    result = articles_schema.dump(articles_list)

    return jsonify(result)


article_schema = NewsSchema()
articles_schema = NewsSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
