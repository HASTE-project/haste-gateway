[![Build Status](https://travis-ci.org/HASTE-project/haste-gateway.svg?branch=master)](https://travis-ci.org/HASTE-project/haste-gateway)

REST Gateway for the HASTE Cloud. Part of the *HASTE Toolkit*.

See:
```
"Rapid development of cloud-native intelligent data pipelines for scientific data streams using the HASTE Toolkit"
https://www.biorxiv.org/content/10.1101/2020.09.13.274779v1
```


# Authentication

One configures the authentication like so:

0. Think up some credentials.
0. Edit `auth.py` and run (don't check in!)
0. This will print (a) the auth header the client needs to send (b) the hash of the auth header you need to run this app.

This allows the convenience of open-sourcing the web application, securely, whilst being configured with your choice of credentials. 

Run it with like this:
```
python3 -m haste.cloud_gateway hashfromstepsabove
```

# Deployment

The simplest thing to do is to simply run the image using Docker. 

0. Install Docker.
0. Generate a new credential hash based on the instructions above (this can be done on a different machine).
0. Pull the Docker image: 
```
docker pull benblamey/haste-gateway:latest`
```
0. Run the image as a daemon, mapping the port to 8080 (on the container) to port 80. Specify the credential hash you generated earlier.  
```
sudo docker run -d --name haste_gateway -p 80:8080/tcp --restart unless-stopped benblamey/haste-gateway:latest python -u -m haste.cloud_gateway a50e4d16b2fdf18619d696931e24dfd4c1572337b5c4c1cd4fb968cc
```
0. Try to GET http://0.0.0.0:80/ to test the auth. You should see "Hello!"

0. To stop the container:
```
sudo docker stop haste_gateway
sudo docker rm haste_gateway
```
