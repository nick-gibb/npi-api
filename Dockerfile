FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN pip install gunicorn 

COPY . /app

EXPOSE 80

CMD ["gunicorn", "-b", ":80", "app:app"]  