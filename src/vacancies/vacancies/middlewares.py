# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from typing import Generator, Iterable

from scrapy import Request, Spider, signals
from scrapy.crawler import Crawler
from scrapy.http import Response


class VacanciesSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "VacanciesSpiderMiddleware":
        # This method is used by Scrapy to create your spiders.
        spider_middleware = cls()
        crawler.signals.connect(
            spider_middleware.spider_opened, signal=signals.spider_opened
        )

        return spider_middleware

    def process_spider_input(self, response: Response, spider: Spider) -> None:
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(
        self, response: Response, result: Iterable, spider: Spider
    ) -> Generator:
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(
        self, response: Response, exception: Exception, spider: Spider
    ) -> None:
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(
        self, start_requests: Iterable, spider: Spider
    ) -> Generator:
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for request in start_requests:
            yield request

    def spider_opened(self, spider: Spider) -> None:
        spider.logger.info(f"Spider opened:{spider.name}")


class VacanciesDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "VacanciesDownloaderMiddleware":
        # This method is used by Scrapy to create your spiders.
        spider_middleware = cls()
        crawler.signals.connect(
            spider_middleware.spider_opened, signal=signals.spider_opened
        )
        return spider_middleware

    def process_request(self, request: Request, spider: Spider) -> None:
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(
        self, request: Request, response: Response, spider: Spider
    ) -> Response:
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(
        self, request: Request, exception: Exception, spider: Spider
    ) -> None:
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider: Spider) -> None:
        spider.logger.info(f"Spider opened: {spider.name}")