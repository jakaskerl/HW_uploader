import pdfkit as pk
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest
import scrapy
from bs4 import BeautifulSoup
import json

# load config file for devices (their names and urls)
with open("devices.json") as f:
    devices = json.load(f)

urls = devices["urls"]
devices = iter(devices["names"])

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})


    def parse(self, response):
        # get html from response and convert it to pdf
        soup = BeautifulSoup(response.body)
        self.convert_to_pdf(soup, next(devices))
        

    def parse_html(self, soup):
        # replace all relative links with absolute links
        for href in soup.find_all(href=True):
            if href["href"].startswith(".."):
                href["href"] = "https://docs.luxonis.com/projects/hardware/en/latest/" + href["href"][3:]
        for src in soup.find_all(src=True):
            if src["src"].endswith("navbar.js"):
                src["src"] = ""
            if src["src"].startswith(".."):
                src["src"] = "https://docs.luxonis.com/projects/hardware/en/latest/" + src["src"][3:]

        #find and delete navbar and sidebar
        nav = soup.find("nav", {"class": "wy-nav-side"})
        nav.decompose()
        head = soup.find("div", {"aria-label": "breadcrumbs navigation"})
        head.decompose()
        #remove footer
        foot = soup.find('footer')
        foot.decompose()
        return soup

    def convert_to_pdf(self, soup, device_name):
        path_to_wkhtmltopdf = "/usr/bin/wkhtmltopdf"
        config = pk.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        soup = self.parse_html(soup)
        try: 
            pk.from_string(str(soup), f"pdfs/{device_name}.pdf", configuration=config)
        except Exception as e:
            pass #this exeption is thrown when pdfkit thinks html is empy but it is not
        return

# run spider
process = CrawlerProcess()
process.crawl(MySpider)
process.start()
