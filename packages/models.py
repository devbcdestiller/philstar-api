from .db import db, ma
from sqlalchemy import Column, Integer, String, Float


class News(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    author = Column(String)
    image = Column(String)
    snippet = Column(String)
    content = Column(String)
    category = Column(String)
    date_published = Column(Float)


class NewsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'image', 'snippet', 'content', 'category',
                  'date_published')
