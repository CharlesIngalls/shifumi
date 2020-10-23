FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /back
WORKDIR /back
ADD requirements.txt /back/
RUN pip install -r requirements.txt
ADD . /back/
EXPOSE 8000