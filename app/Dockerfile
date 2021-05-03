FROM python:3.6-alpine AS BASE
RUN adduser -D favorites_browser
WORKDIR /home/favorites_browser
COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev g++ py3-gunicorn python3-dev postgresql-dev
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

FROM python:3.6-alpine
RUN adduser -D favorites_browser
WORKDIR /home/favorites_browser
ENV PYTHONPATH=/home/favorites_browser
COPY --from=BASE /home/favorites_browser/venv ./venv
RUN apk add --no-cache postgresql-dev
ADD *.py app/
RUN chown -R favorites_browser:favorites_browser ./
USER favorites_browser
EXPOSE 5000
CMD . venv/bin/activate && exec gunicorn -b :5000 app.main:app
