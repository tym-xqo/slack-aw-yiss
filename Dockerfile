FROM python:3-alpine
MAINTAINER tym@adops.com

RUN mkdir /awyiss
WORKDIR /awyiss

COPY awyiss.py /awyiss/awyiss.py
RUN chmod +x /awyiss/awyiss.py
COPY requirements.txt /awyiss/

RUN pip3 install -r requirements.txt

EXPOSE 5757

CMD ["gunicorn", "-b", "0.0.0.0:5757", "awyiss:app", "--log-file=-"]
