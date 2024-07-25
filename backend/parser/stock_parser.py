import asyncio

import requests

from bs4 import BeautifulSoup

from fake_useragent import UserAgent

import re

from misc.format_data import clean_string


class StockURL:
    stockURL = "https://сушеф.рф/catalog/akcii/?back_url_admin=%2Fbitrix%2Fadmin%2Fiblock_list_admin.php%3FIBLOCK_ID%3D5%26type%3Dcontent%26lang%3Dru%26find_section_section%3D109"


class HTMLtags:
    # all stocks on page:
    stock_container_html_tag = "div"
    stock_container_html_attrs = {
        "class": "flex-grid__item product-ajax-cont"
    }
    # image link:
    stock_image_url_tag = "a"
    stock_image_url_attrs = {
        "class": "product-card-item__pic js-show-product-popup-control open-popup-link"
    }
    # stock info:
    stock_info_tag = "div"
    stock_info_attrs = {
        "class": "product-card-item__desc product-card-item__desc_excerpt"
    }
    # title:
    stock_title_tag = "div"
    stock_title_attrs = {
        "class": "product-card-item__title"
    }


class HTMLParser:
    def __init__(self, html_soup):
        # soup per stock:
        self.html_soup = html_soup
        # result data per stock:
        self.data = []

    async def image_url(self):
        stock_html = self.html_soup.find(
            HTMLtags.stock_image_url_tag,
            attrs=HTMLtags.stock_image_url_attrs
        )
        address = re.search(r'src="(.*?)"', str(stock_html)).group(1)
        url = f"https://сушеф.рф{address}"
        self.data.append(url)

    async def title(self):
        stock_html = self.html_soup.find(
            HTMLtags.stock_title_tag,
            attrs=HTMLtags.stock_title_attrs
        )
        title = stock_html.text
        self.data.append(clean_string(title))

    async def info(self):
        stock_html = self.html_soup.find(
            HTMLtags.stock_info_tag,
            attrs=HTMLtags.stock_info_attrs
        )
        info = stock_html.text
        self.data.append(clean_string(info))

    async def get_parse(self):
        await asyncio.gather(
            self.image_url(),
            self.title(),
            self.info()
        )
        return self.data


class ParseSuchefStock:
    def __init__(self):
        self.url = StockURL.stockURL
        self.user_agent = UserAgent()
        self.headers = None
        self.soup = None
        self.actual_stocks = []

    def create_headers(self):
        random_user_agent = self.user_agent.random
        headers = {
            'user-agent': random_user_agent
        }
        self.headers = headers

    def get_request(self):
        self.create_headers()
        try:
            response = requests.get(
                url=self.url,
                headers=self.headers
            )
        except requests.RequestException as _ex:
            raise _ex

        return response

    def get_html_page_source(self):
        response = self.get_request()
        if response.status_code == 200:
            html_page_source = response.content

            return html_page_source
        else:
            print(response.status_code)

            return -1

    def get_soup(self):
        html_page_source = self.get_html_page_source()
        if html_page_source != -1:
            soup = BeautifulSoup(
                html_page_source,
                "html.parser"
            )
            self.soup = soup

    def get_html_stocks(self):
        self.get_soup()
        if self.soup is not None:
            stocks = self.soup.find_all(
                HTMLtags.stock_container_html_tag,
                attrs=HTMLtags.stock_container_html_attrs
            )
            return stocks

    def parse_stock(self):
        html_stocks = self.get_html_stocks()
        for html_stock in html_stocks:
            html_parser = HTMLParser(
                html_soup=html_stock
            )
            asyncio.run(html_parser.get_parse())
            stock = html_parser.data
            self.actual_stocks.append(stock)

        return self.actual_stocks
