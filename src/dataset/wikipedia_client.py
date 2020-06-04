#!/usr/local/bin/python

from requests import get
from mwparserfromhell import parse
from urllib import parse as urllibparse

class WikipediaClient:
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php"
        self.search_params = {
            'action': 'query',
            'list': 'search',
            'format': 'json',
        }
        self.content_params = {
            'action': 'parse',
            'prop': 'text',
            # 'section': 2,
            'format': 'json',
        }
        self.headers = {
            'Accept': 'application/json',
        }

    def search_for_pageid(self, title):
        params = self.search_params.copy()
        params['srsearch'] = urllibparse.quote(title, safe='')

        result = get(url=self.url, params=params, headers=self.headers)
        data = result.json()
        return data['query']['search'].pop(0)['pageid']

    def retrieve_page_content(self, title):
        pageid = self.search_for_pageid(title)
        params = self.content_params.copy()
        params['pageid'] = pageid

        result = get(url=self.url, params=params, headers=self.headers)
        data = result.json()
        return data['parse']['text']['*']


if __name__ == "__main__":
    wc = WikipediaClient()

    # print(wc.retrieve_page_content('qualtrics'))
    print(wc.retrieve_page_content('coldwell banker real estate'))