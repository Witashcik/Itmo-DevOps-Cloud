
# Лаба №1 - Настройка nginx

### Для начала посмотрим, что от нас хотят

#### Необходимые поинты:

- Nginx должен работать по https c сертификатом
- Настроить принудительное перенаправление HTTP-запросов (порт 80) на HTTPS (порт 443) для обеспечения безопасного соединения.
- Использовать alias для создания псевдонимов путей к файлам или каталогам на сервере.
- Настроить виртуальные хосты для обслуживания нескольких доменных имен на одном сервере.
- Что угодно еще под требования проекта (optional)


## Подготовка окружения
У нас есть выбор: арендовать сервер либо использовать все локально. 

В нашем случае выбор пал на аренду сервера (от [тайм.веб](https://timeweb.cloud/))
![](/lab1/media/time_web.png)
После аренды сервера добавляем себе второй айпишник для того чтобы в будущем `настроить виртуальные хосты для обслуживания нескольких доменных имен на одном сервере`

![](/lab1/media/ips.png)

Далее заходим на сервер и настраиваем его (действия происходят в терминале/консоле):

Заходим на сам сервак: подключаемся по ssh `ssh root@server_ip` и вводим Root-пароль `**********` (попадаем в ~/root/)

#### Устанавливаем и обновляем необходимые пакеты 
```bash
apt update && apt install nginx 
```
#
Проверяем что все работает -

ну... оно не заработало

Все потому что он выключен либо порт нужно проверить `sudo lsof -i :80`. И видим что апаче the second мешает. Сносим его `systemctl stop apache2` после чего тестируем его на работоспособность `nginx -t` и если все гуд, то перезагружаем его и запускаемся снова `systemctl restart nginx`
![](/lab1/media/welcome.png)
omg
#
### Соединяемся к нашему репозиторию для удобства
#### Создаем ssh ключ и копируем его содержимое, после чего добавляем его к себе на гитхаб и клонируем репу
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com" #generation WOW
cat ~/.ssh/id_rsa.pub #выделяем ключ и ⌘+C
git clone git@github.com:nick/repo.git
```
В общем, все у нас в руте, а поэтому мы должны сделать оч небезопасный момент, заменить права на `root` в основном конфиге и еще прописать дополнительный `location/` (а то будет ненаход) 


![](/lab1/media/root.png)
#### add `location/` to our own `nginx.conf` 
![](/lab1/media/location.png)

## Set SSL cert
### будем использовать самоподписанный сертификат

```bash
sudo mkdir /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/nginx.key \
  -out /etc/nginx/ssl/nginx.crt
```
#
Вводим данные
```bash
Country Name (2 letter code) [AU]: RU
State or Province Name (full name) [Some-State]: Saint-Petersburg
Locality Name (eg, city) []: Saint-Petersburg
Organization Name (eg, company) [Internet Widgits Pty Ltd]: ITMO
Organizational Unit Name (eg, section) []: IT
Common Name (e.g. server FQDN or YOUR name) []: ip-address
Email Address []: some@mail.ru
```

После создания сертификата для удобства перенесли их в репу
```bash
sudo mkdir /root/repo/lab/web_server/ssl
sudo mv /etc/nginx/ssl/nginx.crt /root/repo/lab1/web_server/ssl/nginx.crt
sudo mv /etc/nginx/ssl/nginx.key /root/repo/lab1/web_server/ssl/nginx.key
```

#
С серваком разобрались. Осталось понять что мы собираемся деплоить.

Решили не заморачиватся и сделали два so ezz html

`first.html`
```html
<html>
    <head>
        <title>first page</title>
    </head>
    <body>
        <meta charset="utf-8">
        <h1>(The) First Page</h1>
       <p1>это первая страница</p1>
    </body>
</html>
```
#
`second.html`
```html
<html>
    <head>
        <title>first page</title>
    </head>
    <body>
        <meta charset="utf-8">
        <h1>(The) Second Page</h1>
       <p1>это вторая страница</p1>
    </body>
</html>
```


# Настройка конфига

#### берем [базу](https://timeweb.cloud/) для нашего конфига, и с помощью интернет ресурсов и подсказок от интеллектуального ассистента помощника олега собираем его под себя
создаем файлик в нашей репе 
```bash
nano /root/repo/lab/web_server/nginx.conf
``` 
#
`nginx.conf` 
```nginx
server {
#redirect✈️
    listen 80;
    server_name 147.45.106.50;

    return 301 https://$host$request_uri;
}

server {
#Читаем
    listen 443 ssl;
    server_name 147.45.106.50;

#указываем путь к сертификату и ключу 
    ssl_certificate /root/Itmo-DevOps-Cloud/lab1/web_server/ssl/nginx.crt;
    ssl_certificate_key /root/Itmo-DevOps-Cloud/lab1/web_server/ssl/nginx.key;

#кродемся к нашему html файлу
    location / {
        alias /root/Itmo-DevOps-Cloud/lab1/site1/;
        index first.html;
    }

#собираем логи ошибок
    error_log /root/Itmo-DevOps-Cloud/lab1/logs/site1_error.log;
}

server {  
#redirect✈️      
    listen 80;
    server_name 45.8.97.55;

    return 301 https://$host$request_uri;
}

server {
#слушаем
    listen 443 ssl;
    server_name 45.8.97.55;

#указываем путь к сертификату и ключу    
    ssl_certificate /root/Itmo-DevOps-Cloud/lab1/web_server/ssl/nginx.crt;
    ssl_certificate_key /root/Itmo-DevOps-Cloud/lab1/web_server/ssl/nginx.key;

#указываем путь к нашему html файлу
    location / {
        alias /root/Itmo-DevOps-Cloud/lab1/site2/;
        index second.html;
    }

#отчет если че то сломалось или ненаход
    error_log /root/Itmo-DevOps-Cloud/lab1/logs/site2_error.log;
}   
```
#
После создания конфига тестим его `nginx -t` на работоспособность и, если все successful, перезагружаемся `systemctl restart nginx`

В дериктории нашей лабы :
`git add .`
`git commit -m "dobavil che to"`
`git push origin main`

#### После того как все необходимое подготовили пытаемся запуститься

![](/lab1/media/first.png)
#
![](/lab1/media/second.png)

as u can see - все работает

# Итоги
При выполнении лабораторной работы было довольно много проблем, с которыми мы столкнулись. Не могли разобраться с локейшином и вообще с тем, что от нас хотят. Но в итоге посидев и разобравшись вроде как поняли что нужно сделать. 
Мы задеплоили два html на веб сервере, который обслуживает два ip (не домена, извините💸🚫) с ssl сертификатом, использует alias для создания псевдонимов путей к html's и перенаправляет 80 порт на 443.

Домен можно использовать локально, для этого нужно создать/открыть `nano etc/hosts`, написать наши ip's и приписать им имена, после чего в конфиге поменять айпишники на домены. Перейти по домену получится только локально.