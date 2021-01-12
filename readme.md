Web Gateway for the HASTE Cloud


[![Build Status](https://travis-ci.org/HASTE-project/haste-gateway.svg?branch=master)](https://travis-ci.org/HASTE-project/haste-gateway)

One configures the authentication like so:
0. Think up some credentials.
0. Edit auth.py and run (don't check in!)
0. This will print (a) the auth header the client needs to send (b) the hash of the auth header you need to run this app.

This allows the convenience of open-sourcing the web application, securely, whilst being configured with your choice of credentials. 

Run it with like this:
```
python3 -m haste.cloud_gateway hashfromstepsabove
```


Listens on http://0.0.0.0:80 by default.

Try to GET http://0.0.0.0:8080/ to test the auth.


Build + Push docker image:
```
docker build --no-cache=true -t "benblamey/haste-gateway:latest" .
docker push benblamey/haste-gateway:latest
```


Run image:

```
-p hostPort:containerPort

docker build --no-cache=true -t "benblamey/haste-gateway:latest" .
docker push benblamey/haste-gateway:latest

sudo docker ps
sudo docker stop haste_gateway
sudo docker rm haste_gateway

sudo docker run -d --name haste_gateway -p 80:8080/tcp --restart unless-stopped benblamey/haste-gateway:latest
sudo docker ps
sudo docker logs haste_gateway
```


