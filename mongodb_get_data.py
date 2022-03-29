from pymongo import MongoClient
from pprint import pprint
from spiders.habr import HabrSpider

client = MongoClient('localhost', 27017)
database = client["habr"]
collection = database.habr

author = HabrSpider.authors_for_parse[0]
follow_type = HabrSpider.follow_lists[1]

print()
print(f"выборка из базы данных пользователей {follow_type} для автора {author}:")

users_filter = {
    'author': author,
    'follow_type': follow_type
}

search_result = collection.find(filter=users_filter)
pprint(list(search_result))
