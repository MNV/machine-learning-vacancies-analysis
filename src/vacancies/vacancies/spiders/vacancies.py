import json
import random
from json import JSONDecodeError
from typing import Any, Generator, List, Optional

from scrapy.http import TextResponse
from scrapy.spiders import Spider

from vacancies.vacancies.items import (
    Address,
    AreaType,
    Employer,
    IdName,
    KeySkill,
    Metro,
    Specialization,
    VacancyItem,
)


class VacanciesSpider(Spider):
    """
    Парсинг вакансий с api.hh.ru.
    """

    name = "vacancies"
    start_urls = ["https://api.hh.ru/areas"]

    @staticmethod
    def _load_json(response: TextResponse) -> Optional[dict]:
        """
        Обработка ответа от сервера.

        :param response: Ответ от сервера.
        :return:
        """

        try:
            result = json.loads(response.body)
        except (TypeError, JSONDecodeError):
            result = None

        return result

    def parse(self, response: TextResponse, **kwargs: Any) -> Optional[Generator]:
        """
        Парсинг данных о регионах.

        :param response: Ответ от сервера.
        :param kwargs:
        :return:
        """

        json_res = self._load_json(response)
        if not isinstance(json_res, list) or len(json_res) < 1:
            return None

        areas_ru: List = []
        area_ru_id = "113"  # Russia
        for item in json_res:
            if item["id"] == area_ru_id:
                areas_ru = item["areas"]
                break

        if not areas_ru:
            return None

        areas_to_parse = list({area["id"] for area in areas_ru})
        random.shuffle(areas_to_parse)
        self.logger.info(f"Area IDs count – {len(areas_to_parse)}.")

        # &industry=7&specialization=1
        # page = random.randint(0, 10)
        for area_id in areas_to_parse:
            next_url = f"https://api.hh.ru/vacancies?per_page=100&area={area_id}"
            yield response.follow(next_url, callback=self.parse_pages)

        return None

    def parse_pages(self, response: TextResponse, **kwargs: Any) -> Optional[Generator]:
        """
        Парсинг списка вакансий в указанном регионе с пагинацией.

        :param response: Ответ от сервера.
        :param kwargs:
        :return:
        """

        json_res = self._load_json(response)
        if not json_res:
            return None

        pages = int(json_res["pages"])
        if not isinstance(json_res, dict) or pages < 1:
            return None

        if len(json_res["items"]):
            for item in json_res["items"]:
                next_url = f"https://api.hh.ru/vacancies/{item['id']}"
                yield response.follow(next_url, callback=self.parse_detail)

        request_url = response.request.url
        if not request_url:
            return None

        for page in range(1, pages + 1):
            next_url = f"{request_url}&page={page}"
            yield response.follow(next_url, callback=self.parse_items)

        return None

    def parse_items(self, response: TextResponse, **kwargs: Any) -> Optional[Generator]:
        """
        Парсинг ссылок на вакансии с детальным описанием.

        :param response: Ответ от сервера.
        :param kwargs:
        :return:
        """

        json_res = self._load_json(response)
        if not isinstance(json_res, dict) or len(json_res["items"]) < 1:
            return None

        for item in json_res["items"]:
            next_url = f"https://api.hh.ru/vacancies/{item['id']}"
            yield response.follow(next_url, callback=self.parse_detail)

        return None

    def parse_detail(
        self, response: TextResponse, **kwargs: Any
    ) -> Optional[Generator]:
        """
        Парсинг детальной информации о конкретной вакансии.

        :param response: Ответ от сервера.
        :param kwargs:
        :return:
        """

        json_res = self._load_json(response)
        if not json_res:
            return None

        vacancy = VacancyItem()

        keys = {
            "id",
            "premium",
            "relations",
            "name",
            "insider_interview",
            "response_letter_required",
            "salary",
            "allow_messages",
            "contacts",
            "description",
            "accept_handicapped",
            "accept_kids",
            "archived",
            "response_url",
            "code",
            "hidden",
            "quick_responses_allowed",
            "driver_license_types",
            "accept_incomplete_resumes",
            "published_at",
            "created_at",
            "initial_created_at",
            "negotiations_url",
            "suitable_resumes_url",
            "apply_alternate_url",
            "has_test",
            "test",
            "alternate_url",
            "working_days",
            "working_time_intervals",
            "working_time_modes",
            "accept_temporary",
            "languages",
        }

        for key in keys:
            vacancy[key] = json_res.get(key)

        vacancy["billing_type"] = (
            IdName(
                id=json_res["billing_type"]["id"],
                name=json_res["billing_type"]["name"],
            )
            if json_res["billing_type"]
            else None
        )
        vacancy["area"] = (
            AreaType(
                id=json_res["area"]["id"],
                name=json_res["area"]["name"],
                url=json_res["area"]["url"],
            )
            if json_res["area"]
            else None
        )
        vacancy["type"] = (
            IdName(
                id=json_res["type"]["id"],
                name=json_res["type"]["name"],
            )
            if json_res["type"]
            else None
        )
        vacancy["address"] = (
            Address(
                city=json_res["address"]["city"],
                street=json_res["address"]["street"],
                building=json_res["address"]["building"],
                description=json_res["address"]["description"],
                lat=json_res["address"]["lat"],
                lng=json_res["address"]["lng"],
                raw=json_res["address"]["raw"],
                metro=Metro(
                    station_name=json_res["address"]["metro"]["station_name"],
                    line_name=json_res["address"]["metro"]["line_name"],
                    station_id=json_res["address"]["metro"]["station_id"],
                    line_id=json_res["address"]["metro"]["line_id"],
                    lat=json_res["address"]["metro"]["lat"],
                    lng=json_res["address"]["metro"]["lng"],
                )
                if json_res["address"]["metro"]
                else None,
                metro_stations=[
                    Metro(
                        station_name=metro["station_name"],
                        line_name=metro["line_name"],
                        station_id=metro["station_id"],
                        line_id=metro["line_id"],
                        lat=metro["lat"],
                        lng=metro["lng"],
                    )
                    for metro in json_res["address"]["metro_stations"]
                    if json_res["address"]["metro_stations"]
                ]
                if json_res["address"]["metro_stations"]
                else None,
            )
            if json_res["address"]
            else None
        )
        vacancy["experience"] = (
            IdName(
                id=json_res["experience"]["id"],
                name=json_res["experience"]["name"],
            )
            if json_res["experience"]
            else None
        )
        vacancy["schedule"] = (
            IdName(
                id=json_res["schedule"]["id"],
                name=json_res["schedule"]["name"],
            )
            if json_res["schedule"]
            else None
        )
        vacancy["employment"] = (
            IdName(
                id=json_res["employment"]["id"],
                name=json_res["employment"]["name"],
            )
            if json_res["employment"]
            else None
        )
        vacancy["department"] = (
            IdName(
                id=json_res["department"]["id"],
                name=json_res["department"]["name"],
            )
            if json_res["department"]
            else None
        )

        # содержит исходный код с текстом из description
        # vacancy["branded_description"] = json_res["branded_description"]

        vacancy["vacancy_constructor_template"] = json_res[
            "vacancy_constructor_template"
        ]
        vacancy["key_skills"] = (
            [KeySkill(name=skill["name"]) for skill in json_res["key_skills"]]
            if json_res["key_skills"]
            else None
        )
        vacancy["specializations"] = (
            [
                Specialization(
                    id=specialization["id"],
                    name=specialization["name"],
                    profarea_id=specialization["profarea_id"],
                    profarea_name=specialization["profarea_name"],
                )
                for specialization in json_res["specializations"]
            ]
            if json_res["specializations"]
            else None
        )
        vacancy["professional_roles"] = (
            [
                IdName(
                    id=role["id"],
                    name=role["name"],
                )
                for role in json_res["professional_roles"]
            ]
            if json_res["professional_roles"]
            else None
        )
        vacancy["employer"] = (
            Employer(
                id=json_res["employer"].get("id"),
                name=json_res["employer"].get("name"),
                url=json_res["employer"].get("url"),
                alternate_url=json_res["employer"].get("alternate_url"),
                logo_urls=json_res["employer"].get("logo_urls"),
                vacancies_url=json_res["employer"].get("vacancies_url"),
                trusted=json_res["employer"].get("trusted"),
            )
            if json_res["employer"]
            else None
        )

        yield vacancy
