FROM python:3.11
LABEL author="Ivan Goncharov" email="ivan.stereotekk@gmail.com"
RUN mkdir myapp
COPY ./requirements.txt /myapp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir  -r /myapp/requirements.txt
COPY . /myapp
WORKDIR /myapp
EXPOSE 80
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]