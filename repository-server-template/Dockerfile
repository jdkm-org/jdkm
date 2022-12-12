FROM ubuntu:latest
RUN apt update && apt apt upgrade -y && apt install nginx cron git -y && \
    service nginx start && service cron start
RUN cd /var/www/html && git clone https://github.com/swxfll/jjvmm-repo.git



apt install nginx cron git -y