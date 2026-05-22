#!/bin/bash

rm -rf tempdir
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

cat > tempdir/Dockerfile << 'DOCKERFILE'
FROM python:3.9
ENV PIP_PROGRESS_BAR=off
RUN pip install --progress-bar off flask
COPY ./static /home/myapp/static/
COPY ./templates /home/myapp/templates/
COPY sample_app.py /home/myapp/
WORKDIR /home/myapp
EXPOSE 9999
CMD ["python", "sample_app.py"]
DOCKERFILE

cd tempdir
docker build -t sampleapp .
docker rm -f samplerunning 2>/dev/null
docker run -d -p 9999:9999 --name samplerunning sampleapp
docker ps -a
