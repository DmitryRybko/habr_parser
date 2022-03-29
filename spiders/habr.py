import scrapy
import json
from pprint import pprint
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from items import HabrparserItem


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = []
    authors_for_parse = ['grigoryvp', 'Doublesharp']
    follow_lists = ["followers", "followed"]
    for follow_item in follow_lists:
        for author in authors_for_parse:
            start_urls.append(f'https://habr.com/kek/v2/users/{author}/{follow_item}?page=1')

    def parse(self, response):

        current_url = response.url
        author_name = current_url.split("/")[6]
        follow_option = current_url.split("/")[7].split("?")[0]

        json_response = json.loads(response.text)
        pages_count = json_response["pagesCount"]
        for page in range(1, pages_count+1):
            followers_dict = json_response.get("authorRefs")
            for follower in followers_dict:
                follower_data = followers_dict.get(follower)
                item = HabrparserItem(
                    _id=follower_data.get('id'),
                    username=follower_data.get('alias'),
                    photo=follower_data.get('avatarUrl'),
                    author=author_name,
                    follow_type=follow_option
                )

                yield item

            next_page_url = current_url.split("=")[0]
            next_page = f'{next_page_url}={page}'
            yield response.follow(next_page, callback=self.parse)


