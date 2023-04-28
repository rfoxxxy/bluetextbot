#!/bin/bash

if [[ -z "${ENV}" ]]
then
    read -p 'Prod?: ' IS_PROD
    if [[ "$IS_PROD" = 'true' || "$IS_PROD" = 'y' ]]
    then
        ENV="production"
    else
        ENV="development"
    fi
fi

docker build \
    -t bot_template$(test "$ENV" != production && echo "_test") \
    --build-arg ENV="$ENV" \
    .