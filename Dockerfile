FROM python:3.12.3-alpine

LABEL AUTHOR=Clemson_University

# Adding Labels to identify repository for github
LABEL org.opencontainers.image.source=https://github.com/Code-Liberation-Front/DBArchive
LABEL org.opencontainers.image.description="DBArchive Container"

COPY /requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
RUN apk update
RUN apk upgrade --available && sync
RUN apk add --no-cache postgresql16-client

WORKDIR /app
COPY . .

#Run the main program
CMD [ "python3", "-u", "backup.py" ]

