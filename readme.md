Web Gateway for the HASTE Cloud

Run it with username and password like this:
```
python3 -m haste.cloud_gateway hastecloud letmein
```

Listens on http://0.0.0.0:80 by default.


Build + Push docker image:
```
```


Run image:
-p hostPort:containerPort
```
docker build --no-cache=true -t "benblamey/haste-gateway:latest" .
docker push benblamey/haste-gateway:latest

sudo docker ps
sudo docker stop haste_gateway
sudo docker rm haste_gateway


sudo docker run -d --name haste_gateway -p 80:8080/tcp --restart unless-stopped benblamey/haste-gateway:latest
sudo docker ps
sudo docker logs haste_gateway

```


