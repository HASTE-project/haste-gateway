FROM python:3.7.2

# Set the working directory to /app
WORKDIR /app

COPY haste /app/haste
COPY setup.py /app/setup.py

RUN pip3 install /app/

EXPOSE 8080

CMD ["python","-u","-m","haste.cloud_gateway","160e21820b69e63de71ed5cade2cff742a6a6442c00f5744c5110afe"]