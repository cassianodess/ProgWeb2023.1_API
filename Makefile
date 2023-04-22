#!/bin/bash
SHELL=/bin/bash

include .env
export

init:
	python3 -m venv venv;

run:
	source venv/bin/activate; export FLASK_APP=app; flask run --port=8080 --host=0.0.0.0

debug:
	source venv/bin/activate; export FLASK_APP=app; export FLASK_DEBUG=true; flask run --port=8080
