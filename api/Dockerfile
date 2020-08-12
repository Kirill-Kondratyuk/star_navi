FROM python:3.8-alpine3.10

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev
RUN mkdir logs
RUN cd logs && touch gunicorn.errors
RUN mkdir api
COPY . /api

WORKDIR /api

RUN python3.8 -m venv venv
ENV VIRTUAL_ENV ./venv
ENV PATH /venv/bin:$PATH

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "api.wsgi:application", "-w", "2", "-b", ":8000", "--reload", "--log-level", "info"]