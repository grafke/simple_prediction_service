#!/usr/bin/env bash
set -e
. ./bin/docker_settings.sh

docker build -t "$prefixed_tag" .