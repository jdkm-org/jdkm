FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
COPY docker-run-tpl.sh /docker-run-tpl.sh
WORKDIR /
RUN apt update && apt upgrade -y && apt install nginx cron git -y && \
    sed -i '51 a autoindex on;' /etc/nginx/sites-available/default && \
    rm -rf /var/www/html/* && git clone https://github.com/jdkm-org/index.git /var/www/html && \
    chown -R www-data:www-data /var/www/html/ && chmod +x /docker-run-tpl.sh && \
    echo '*/5 * * * * www-data rm -rf /var/www/html/* && rm -rf /var/www/html/.g* && git clone https://github.com/jdkm-org/index.git /var/www/html' >> /etc/crontab
CMD ["bash","/docker-run-tpl.sh"]