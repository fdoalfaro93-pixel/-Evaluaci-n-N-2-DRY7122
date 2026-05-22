#!/bin/bash

rm -rf tempdir
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python:3.9" > tempdir/Dockerfile
echo "ENV PIP_PROGRESS_BAR=off" >> tempdir/Dockerfile
echo "RUN pip install --progress-bar off flask" >> tempdir/Dockerfile
echo "COPY ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "WORKDIR /home/myapp" >> tempdir/Dockerfile
echo "EXPOSE 9999" >> tempdir/Dockerfile
printf 'CMD ["python", "sample_app.py"]\n' >> tempdir/Dockerfile

cd tempdir
docker rmi -f sampleapp 2>/dev/null
docker build --no-cache -t sampleapp .
docker rm -f samplerunning 2>/dev/null
docker run -d -p 9999:9999 --name samplerunning sampleapp
docker ps -a
