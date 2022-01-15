FROM python:3.8.5-alpine3.12
WORKDIR /usr/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
RUN apk add --no-cache gcc libc-dev linux-headers zlib-dev jpeg-dev libjpeg
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask","run","--host","0.0.0.0"]
