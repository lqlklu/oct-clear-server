#!/bin/sh
docker run -it --rm \
	-p 8000:8000 \
	-u $(id -u):$(id -g) \
	-v "$(pwd)/db.sqlite3":/app/db.sqlite3 \
	-v "$(pwd)/result/":/app/result/ \
	-v "$(pwd)/upload/":/app/upload/ \
	-v "$(pwd)/generator_g/":/app/generator_g/ \
	oct-denoise-server
