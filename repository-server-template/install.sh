#!/usr/bin/env sh

# ======================================================================================================================
# Installation Guide
# 1. Run command:
# 2. Select install mode: Docker or Local
# 3. Select Web Server: Nginx or Apache Httpd
# 4. Set storage location, default to /var/www/html:
# 5. Auto start JJVMM Repository Server.
# 6. Edit /etc/crontab file:
# ======================================================================================================================

echo 'Prepare to install jjvmm repository server...'

sudo mkdir -p /usr/local/src/jdkm
sudo cd /usr/local/src/jdkm

# shellcheck disable=SC1068
temp = $(curl -fsSL https://raw.githubusercontent.com/jdkm-org/jdkm/main/repository-server-template/Dockerfile)
sudo echo $temp  &> Dockerfile

sudo docker build -f ./DockerFile -t  jdkm-repository-server-template:1.0.0 .
sudo docker run -id -p 9900:80 --name "jdkm-repository-server" jdkm-repository-server-template:1.0.0