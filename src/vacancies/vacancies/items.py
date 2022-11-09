from scrapy import Field, Item


class IdName(Item):
    """
    Общая модель с идентификатором и наименованием.
    """

    id = Field()
    name = Field()


class AreaType(IdName):
    """
    Информация о регионе.
    """

    url = Field()


class Metro(Item):
    """
    Информация о ближайшей станции метро.
    """

    station_name = Field()
    line_name = Field()
    station_id = Field()
    line_id = Field()
    lat = Field()
    lng = Field()


class Address(Item):
    """
    Адрес места работы.
    """

    city = Field()
    street = Field()
    building = Field()
    description = Field()
    lat = Field()
    lng = Field()
    raw = Field()
    metro = Field(serializer=Metro)
    metro_stations = Field(serializer=Metro)


class KeySkill(Item):
    """
    Ключевой навык.
    """

    name = Field()


class Specialization(IdName):
    """
    Специализация.
    """

    profarea_id = Field()
    profarea_name = Field()


class LogoUrls(Item):
    """
    Ссылка на логотип компании.
    """

    original = Field()


class Employer(IdName):
    """
    Данные о работодателе.
    """

    url = Field()
    alternate_url = Field()
    logo_urls = Field(serializer=LogoUrls)
    vacancies_url = Field()
    trusted = Field()


class VacancyItem(Item):
    """
    Данные вакансии.
    """

    id = Field()
    premium = Field()
    billing_type = Field(serializer=IdName)
    relations = Field()
    name = Field()
    insider_interview = Field()
    response_letter_required = Field()
    area = Field(serializer=AreaType)
    salary = Field()
    type = Field(serializer=IdName)
    address = Field(serializer=Address)
    allow_messages = Field()
    experience = Field(serializer=IdName)
    schedule = Field(serializer=IdName)
    employment = Field(serializer=IdName)
    department = Field(serializer=IdName)
    contacts = Field()
    description = Field()
    branded_description = Field()
    vacancy_constructor_template = Field()
    key_skills = Field()
    accept_handicapped = Field()
    accept_kids = Field()
    archived = Field()
    response_url = Field()
    specializations = Field()
    professional_roles = Field()
    code = Field()
    hidden = Field()
    quick_responses_allowed = Field()
    driver_license_types = Field()
    accept_incomplete_resumes = Field()
    employer = Field(serializer=Employer)
    published_at = Field()
    created_at = Field()
    initial_created_at = Field()
    negotiations_url = Field()
    suitable_resumes_url = Field()
    apply_alternate_url = Field()
    has_test = Field()
    test = Field()
    alternate_url = Field()
    working_days = Field()
    working_time_intervals = Field()
    working_time_modes = Field()
    accept_temporary = Field()
    languages = Field()
