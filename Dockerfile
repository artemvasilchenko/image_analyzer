FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY='some_secret_key'

WORKDIR /usr/src/app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . .


EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "image_analyzer.wsgi:application", "--reload"]