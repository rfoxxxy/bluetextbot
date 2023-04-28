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

mkdir -p "$(pwd)"/static

docker container rm bot_template$(test "$ENV" != production && echo "_test") > /dev/null 2>&1

# -p 3939:3939 for webhook
docker run -it \
    $(test "$DAEMON" == "true" && echo "-d") \
    --mount type=bind,source="$(pwd)"/static,target=/app/static \
    --name bot_template$(test "$ENV" != production && echo "_test") \
    bot_template$(test "$ENV" != production && echo "_test")