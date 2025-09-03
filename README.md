# Проект: Course Project DRF
Инструкция по развертыванию Django REST Framework проекта на сервере с автоматическим деплоем через GitHub Actions.

## Предварительные требования
Ubuntu сервер (24.04 LTS или новее)

Учетная запись на GitHub

Учетная запись на Docker Hub

## Настройка сервера
1. Подключитесь к серверу

2. Обновление сервера до последней версии и установка необходимых пакетов

3. Настройка Docker по документации с оф. сайта

4. Создание структуры директорий

`mkdir -p ~/projects/course_9/course_project_drf`
`cd ~/projects/course_9/course_project_drf`
5. Получите SSH ключи и добавьте на GitHub

## Настройка GitHub репозитория

1. Добавление секретов в GitHub
В настройках репозитория (Settings → Secrets → Actions) добавьте:

SERVER_HOSTNAME - IP-адрес вашего сервера

SERVER_USERNAME - имя пользователя на сервере

SSH_PRIVATE_KEY - приватный SSH-ключ сервера

DOCKER_HUB_USERNAME - ваш логин на Docker Hub

DOCKER_HUB_ACCESS_TOKEN - токен доступа к Docker Hub

SECRET_KEY - секретный ключ вашего django приложения


## Настройка проекта на сервере

1. Клонирование репозитория

`cd ~/projects/course_9/course_project_drf`
`git clone git@github.com:AlekseiSvidetelev/course_project_drf.git .`
`git checkout feature/doker_homework`
2. Создание .env файла

`nano .env`

Заполните файл по шаблону [.env.example]()

3. Запуск проекта

`docker-compose up -d --build`

4. Проверка статуса

`docker-compose ps`

`docker-compose logs`

## GitHUB Actions

После настройки, при каждом пуше в ветке feature/doker_homework будет автоматически:

1. Проверка линтера flake8

2. Запуск тестов

3. Сборка образа на DockerHUB

4. Пуш образа в Docker Hub. Деплой на сервер с обновлением контейнеров

# Остановка
docker-compose down

# Перезапуск
docker-compose up -d --build

# Демо
Приложение развернуто по адресу: http://158.160.194.221/swagger/

