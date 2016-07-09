#!/usr/bin/env bash

zip -r backend.zip backend

scp backend.zip kelvinabrokwa@130.211.120.248:~

ssh kelvinabrokwa@130.211.120.248 'sudo rm -rf backend'

ssh kelvinabrokwa@130.211.120.248 'unzip backend.zip -d backend'
