
Анализ вакансий
****************

На порталах с объявлениями о работе нередко встречаются вакансии без указания заработной платы.
Часто хочется узнать, на какую зарплату можно претендовать по описанию вакансии.
Также в описании вакансии содержатся ключевые навыки кандидата – полезно их автоматически анализировать и делать выводы.

Установка
=========

Установите требуемое ПО:

1. Docker для контейнеризации – |link_docker|

.. |link_docker| raw:: html

   <a href="https://www.docker.com" target="_blank">Docker Desktop</a>

2. Для работы с системой контроля версий – |link_git|

.. |link_git| raw:: html

   <a href="https://github.com/git-guides/install-git" target="_blank">Git</a>

3. IDE для работы с исходным кодом – |link_pycharm|

.. |link_pycharm| raw:: html

    <a href="https://www.jetbrains.com/ru-ru/pycharm/download" target="_blank">PyCharm</a>

Клонируйте репозиторий проекта в свою рабочую директорию:

    .. code-block:: console

        git clone https://github.com/mnv/machine-learning-vacancies-analysis.git

Использование
=============

Перед началом использования приложения необходимо его сконфигурировать.

.. note::

    Для конфигурации выполните команды, описанные ниже, находясь в корневой директории проекта (на уровне с директорией `src`).

1. Скопируйте файл настроек `.env.sample`, создав файл `.env`:
    .. code-block:: console

        cp .env.sample .env

    Этот файл содержит преднастроенные переменные окружения, значения которых будут общими для всего приложения.
    Файл примера (`.env.sample`) содержит набор переменных со значениями по умолчанию.
    Созданный файл `.env` можно настроить в зависимости от окружения.

    .. warning::

        Никогда не добавляйте в систему контроля версий заполненный файл `.env` для предотвращения компрометации информации о конфигурации приложения.

2. Соберите Docker-контейнер с помощью Docker Compose:
    .. code-block:: console

        docker-compose build

    Данную команду необходимо выполнять повторно в случае обновления зависимостей в файле `requirements.txt`.
