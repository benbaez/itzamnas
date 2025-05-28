#!/usr/bin/env bash

# openssl x509 -in http_ca.crt -out elastic.pem -outform PEM

openssl x509 -in /persist/es01/config/certs/http_ca.crt -out /persist/cerebro/conf/elastic.pem -outform PEM
