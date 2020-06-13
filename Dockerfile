FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /VIFA 
WORKDIR /VIFA 
COPY requirements.txt /VIFA/
RUN pip install -r requirements.txt
COPY . /VIFA/
