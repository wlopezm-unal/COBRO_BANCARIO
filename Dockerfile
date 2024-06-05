FROM python:3.12.1
COPY . /main
WORKDIR /main
RUN pip install -r requirements.tx
EXPOSE $PORT
CMD