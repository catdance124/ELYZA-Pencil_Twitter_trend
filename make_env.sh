#!/bin/sh

touch .env
echo "UID=$(id -u $USER)" > .env
echo "GID=$(id -g $USER)" >> .env
echo "UNAME=$USER" >> .env

echo "TWITTER_CONSUMER_KEY" >> .env
echo "TWITTER_CONSUMER_SECRET" >> .env
echo "TWITTER_CLIENT_ID" >> .env
echo "TWITTER_CLIENT_SECRET" >> .env
echo "TWITTER_ACCESS_TOKEN" >> .env
echo "TWITTER_ACCESS_SECRET" >> .env
echo "TWITTER_ACCESS_TOKEN_PKCE" >> .env