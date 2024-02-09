import logging
import redis
import sys

from typing import List
from mongoengine import *
from redis_lru import RedisLRU


class Author(Document):
    fullname = StringField(max_length=200, required=True, unique=True)
    born_date = DateTimeField(required=True)
    born_location = StringField(max_length=300, required=True)
    description = StringField(max_length=10000, required=True)

    meta = {"db_alias": "some_db"}


class Tag(EmbeddedDocument):
    name = StringField(max_length=100, required=True)
    meta = {"db_alias": "some_db"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(max_length=500, required=True)
    tags = ListField(EmbeddedDocumentField(Tag))
    meta = {"db_alias": "some_db"}


class QueryData:
    client = redis.StrictRedis(host="localhost", port=6379, password=None)
    cache = RedisLRU(client)

    @staticmethod
    def transform_query_data(quotes: List[Quote]) -> List[dict]:
        return [
            {
                "author": quote.author.fullname,
                "quote": quote.quote,
                "tags": [tag.name for tag in quote.tags],
            }
            for quote in quotes
        ]

    @staticmethod
    @cache
    def get_quotes_by_name(author_name: str):
        author = Author.objects(fullname=author_name).first()
        quotes = Quote.objects(author=author)
        return QueryData.transform_query_data(quotes=quotes)

    @staticmethod
    @cache
    def get_quotes_by_tags(*args):
        quotes = Quote.objects(tags__name__in=args)
        return QueryData.transform_query_data(quotes=quotes)
