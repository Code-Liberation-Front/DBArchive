FROM python:3.11.2-alpine

LABEL AUTHOR=Clemson_Universiry

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

