FROM ubuntu:latest
RUN apt update && apt apt upgrade -y && apt install nginx -y && apt install cron -y && apt install git -y && \
    service nginx start && service cron start
RUN cd /var/www/html && git clone https://github.com/swxfll/jjvmm-repo.git
