#!/bin/bash
# Clean up carriage returns in input vars
clean_opco=$(echo "$opco" | tr -d '\r')

docker build \
    --build-arg opco="$clean_opco" \
    -t "172.23.12.160:8083/$clean_opco/uat/data-science-api-chatbot-ai:1.0.0.2-prod" \
    .
