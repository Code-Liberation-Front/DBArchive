FROM python:3.11.2-alpine

LABEL AUTHOR=Clemson_University

# Adding Labels to identify repository for github
LABEL org.opencontainers.image.source=https://github.com/Code-Liberation-Front/DBArchive
LABEL org.opencontainers.image.description="DBArchive Container"

COPY /requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
RUN apk update
RUN apk upgrade

WORKDIR /app
COPY . .

#Path to database
ENV DBPath="DBPATH"
#Interval between backup
ENV Interval="INTERVAL"

#Run the main program
CMD [ "python3", "-u", "snapshot.py" ]

