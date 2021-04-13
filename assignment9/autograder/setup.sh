#!/usr/bin/env bash

useradd -ms /bin/bash vagrant

apt-get update

apt-get install -y python3-pip python3-dev sudo
