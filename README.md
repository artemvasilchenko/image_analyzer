Image analyzer
======
Сервис производит анализ изображения - считает количество пискелей черного и 
белого цвета, а так же производит подсчет пикселей по HEX-коду.
Загрузка изображения и HEX-кода искомого цвета производится на HTML-странице,
после анализа сервис возвращает результат на HTML-страницу.
Поддерживаемые форматы изображений - jpg, jpeg, gif, bmp, png.

##### Содержание 
[1. Сборка и запуск проекта c помощью docker](#docker)  
[2. Сборка и запуск вручную](#hand_build)  
[3. Загрузка изображения и ввод HEX-кода искомого цвета](#upload_image)  
[4. Запуск тестов](#testing)  
[5. Просмотр JSON-логов запросов и ответов сервиса](#upload_image)  

<a name="docker"><h3>1. Сборка и запуск проекта c помощью docker.</h3></a> 

Перед сборкой и запуском необходимо установить [docker](https://docs.docker.com/engine/install/ "docker").

#### 1.1. Клонирование репозитория.
Переход в домашнюю директорию
```bash
cd ~
```
Установка `git`
```bash
sudo apt install git
```
Клонирование репозитория
```bash
git clone https://github.com/artemvasilchenko/image_analyzer.git
```

Все дальнейшие команды необходимо запускать из директории проекта
```bash
cd ~/image_analyzer
```

<a name="docker_build"><h4>1.2. Сборка проекта</h4></a> 
```bash
sudo docker build -t app .
```

после сборки проекта можно перейти к [тестированию](#testing)

#### 1.3. Запуск приложения.

```bash
sudo docker run -d --rm --name app -p 8000:8000 -v ${PWD}:/usr/src/app app
```
После запуска приложения можно перейти к [загрузке изображения и вводу HEX-кода](#upload_image) 
просмотру [JSON-логов запросов и ответов сервиса](#upload_image)  

#### 1.4. После окончания работы с сервисом необходимо остановить приложение.

```bash
sudo docker stop app
```

<a name="hand_build"><h3>2. Сборка и запуск вручную</h3></a> 

#### 2.1. Клонирование репозитория.
Переход в домашнюю директорию
```bash
cd ~
```
Установка `git`
```bash
sudo apt install git
```
Клонирование репозитория
```bash
git clone https://github.com/artemvasilchenko/image_analyzer.git
```

Все дальнейшие команды необходимо запускать из директории проекта
```bash
cd ~/image_analyzer
```

<a name="requirements"><h4>2.2. Установка зависимостей.</h4></a> 

Для работы приложения требуется установить [python 3.9](https://www.python.org/downloads/release/python-390/)

Установка [pip](https://pypi.org/project/pip/)
```bash
pip install pip
```

Установка [pipenv](https://pipenv.pypa.io/en/latest/)
```bash
pip install pipenv
```

Все зависимости указаны в `Pipfile` и `Pipfile.lock` в корне проекта.  
Установка python-зависимостей проекта - `django`, `gunicorn`, `json-log-formatter`, `pillow`
```bash
pipenv install
```

Активировать виртуальное окружение
```bash
pipenv shell
```
После установки зависимостей можно перейти [тестированию](#hand_testing)

#### 2.3. Запуск приложения.

```bash
gunicorn -b 0.0.0.0:8000 image_analyzer.wsgi:application
```
После запуска приложения можно перейти к [загрузке изображения и вводу HEX-кода](#upload_image) 
просмотру [JSON-логов запросов и ответов сервиса](#upload_image)  

#### 2.4. После окончания работы с сервисом необходимо остановить приложение нажатием клавиш `Ctrl` + `c`. 

<a name="upload_image"><h3>3. Загрузка изображения и ввод HEX-кода искомого цвета.</h3></a>

#### 3.1. Запустить сервис с помощью [docker](#docker) или [вручную](#hand_build).

#### 3.2. Запустить браузер и перейти по адресу [0.0.0.0:8000](http://0.0.0.0:8000) или [localhost:8000](http://localhost:8000) 

#### 3.3. На загрузившейся HTML-странице в форме выбрать изображение и ввести HEX-код.

HEX-код можно вводить в следующих форматах: `#FFF`, `#FFFFFF`, `#ffffff`, `#fff`.
При отсутствии HEX-кода - поиск по нему осуществляется и в результате анализа
будут результаты только по количеству черных и белых пикселей.

#### 3.4. После анализа результаты отобразятся на HTML-странице.

<a name="testing"><h3>4. Запуск тестов.</h3></a>
<a name="docker_testing"><h4>4.1. Запуск тестов в новом docker-контейнере.</h4></a>
Может выполняться после [сборки проекта](#docker_build)
```bash
cd ~/image_analyzer
```

```bash
sudo docker run --rm --name test_app app python manage.py test
```

<a name="hand_testing"><h4>4.2. Запуск тестов вручную.</h4></a>
Может выполняться после [установки зависимостей](#requirements)
```bash
cd ~/image_analyzer
```

```bash
python manage.py test
```

<a name="logging"><h3>5. Просмотр JSON-логов запросов и ответов сервиса</h3></a>

```bash
cd ~/image_analyzer
```
```bash
cat app.log
```