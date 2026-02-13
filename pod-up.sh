#!/bin/bash

# Script to bring up pods for any environment specified as arg 1
#

if [ "$#" -ne 1 ]; then
  echo "Usage: pod-up.sh <environment file>" >&2
  echo "environment variable ENV should be defined in an environment file like dev.env, test.env" >&2
  exit 1
fi

ENV_FILE=$1
if [[ -s "$ENV_FILE" ]]; then
  echo "file passed: $ENV_FILE"
  echo "environment file $ENV_FILE exists and is not empty" >&2
  source $ENV_FILE
  podman compose --env-file $ENV_FILE -f compose.yaml --in-pod ${ENV}-artha-pod -p ${ENV}-artha up --build -d
else
  echo "environment file $ENV_FILE does not exist." >&2
fi
exit 0
