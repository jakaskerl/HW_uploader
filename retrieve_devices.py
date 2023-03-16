import pdfkit as pk
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest
import scrapy
from bs4 import BeautifulSoup
import json


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://docs.luxonis.com/projects/hardware/en/latest/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        devices = {"names": [], "urls": []}

        device_tables= soup.find_all("table", {"class": "docutils align-default"})
        # get name and link to every device in table
        for soup in device_tables:
            for th in soup.find_all("th", {"class": "head"}):
                    devices["names"].append(th.text)

            for a in soup.find_all("a", {"class": "reference internal"}):
                devices["urls"].append(self.start_urls[0] + a["href"])

        with open("devices.json", "w") as f:
            json.dump(devices, f)

# run spider
process = CrawlerProcess()
process.crawl(MySpider)
process.start()