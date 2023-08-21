FROM python:3.11.

WORKDIR /home/app/
COPY . /home/app/
RUN pip install -r ./requirements.txt

CMD [ "python3", "app.py"]

