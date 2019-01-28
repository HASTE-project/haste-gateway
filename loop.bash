#!/usr/bin/env bash

while :
do
    git pull
    python3 pip install -e .
	python3 -m haste.cloud_gateway hastecloud replacethis
	sleep 1
done

# @reboot  /home