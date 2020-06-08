FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN pip install gunicorn 

COPY . /app

EXPOSE 8050

CMD ["gunicorn", "-b", ":8050", "app:app"]  