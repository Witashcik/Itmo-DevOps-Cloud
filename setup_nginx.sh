#!/bin/bash

sudo ln -sf /root/Itmo-DevOps-Cloud/lab1/web_server/nginx.conf /etc/nginx/sites-enabled/lab1.conf

if sudo nginx -t; then
    echo "Nginx конфигурация успешна"

sudo systemctl restart nginx
    echo "Nginx перезапущен"
else
    echo "Ошибка в конфигурации Nginx"
    exit 1
fi
