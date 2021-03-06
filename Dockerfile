FROM python:3.7-buster

WORKDIR /home

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install tf-nightly
RUN python -m nltk.downloader popular

COPY src ./src

ENTRYPOINT [ "python" ]