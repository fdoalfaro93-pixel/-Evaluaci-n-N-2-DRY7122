#!/bin/bash

rm -rf tempdir
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python:3.9" >> tempdir/Dockerfile
echo "RUN pip install --no-input --no-cache-dir flask" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 9999" >> tempdir/Dockerfile
echo "CMD python /home/myapp/sample_app.py" >> tempdir/Dockerfile

cd tempdir
docker build --security-opt seccomp=unconfined -t sampleapp .
docker rm -f samplerunning 2>/dev/null
docker run -t -d -p 9999:9999 --name samplerunning sampleapp
docker ps -a
