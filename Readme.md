## Instructions:
 ```
 mv password_.py password.py     #Database credentials hardcoded in password_.py (for now, do not deploy), change name to password.py
 sudo docker-compose up
 ```
 There will be errors the fist time beacause the database must be initialised, wait till there is no more scroling in the terminal. Then open http://localhost
 
 
 To shut down, pres `ctrl-c` and wait, it sometimes takes a while.
 ___
## Debugign/Development
You can know edit the app.py file and it will reload automaticaly, so you only need to refresh the page. 
### Flask
Best way is to not use nginx/gunicorn in development beacause it interferes with the flask debuging system. So the best way is to run:
```
docker exec -it diy-satellites_flask_1 /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"
```
and then inside the new shell
```
python app.py
```
The logs will be printed in the same shell.
 
Go then to http://localhost:5000
To get to specific directorys do like this: http://localhost:5000/api/getall/
## Viewing logs
Logs are automaticaly printed in the terminal together when using docker-compose. Python app.py prints extra to the mylog.log file. This can be used to print to the file and track things for example in the api_getall() funktion there is an example of how to use it.
___
## Clean up
To delete database files and all folder/files that outside the permisions of the host user:
```
sudo bash clean_rm.sh
```
___
## Useful comands 
`docker ps -a` list all running conteiner with extra information
`docker-compose build` you have to build image manualy when `Dockerfile` is changed 
`docker-compose up -d` runs docker conteiners detacht, shut down with...
`docker-compose down` tu shutdown the conteiners opened by the docker-compose.yml and `docker-compose up -d`
___
# TODO
* Change how .csv are read so that it reads the ones from https://github.com/silviatelo/NOTOS: 
* **Fix import DateTime in Dataline.add_dataline() to actualy reading the date**
* so much more omg 
## Neat .csv **OLD**
 Date  |    Lat    |    Long   | AltGPS | Temp  | Hum  |AltBar | Pressure |  NO2  |  CO  | NH3 | PM1.0 | PM2.5 | PM10.0 |  Date  |  Time    |
:-----:|:---------:|:---------:|:------:|:-----:|:----:|:-----:|:--------:|:-----:|:----:|:---:|:-----:|:-----:|:------:|:------:|:--------:|
line1  |40.4103952 | -3.693736 |   0    | 26.58 |  32  | 618.9 |  941.09  | 34.99 | 2.97 |  0  |   0   |   0   |   2    | 7/7/19 | 17:57:50 |
line1  |40.4103952 | -3.693736 |   0    | 26.85 | 32.03| 618.7 |  941.11  | 33.23 | 3.22 |  0  |   2   |   3   |   3    | 7/7/19 | 17:57:50 |

## Raw .csv **OLD**
Lat, Long, AltGPS, Temp, Hum, AltBar, Pressure, NO2, CO, NH3, PM1.0, PM2.5, PM10.0 ,Date, Time
40.4103952,-3.693736,0,26.58,32,618.9,941.09,34.99,2.97,0,0,0,2,7/7/19,17:57:50

## PostgreSQL
point_id |          DateTime          |                    geo                     |  Latitude  | Longitude  | AltGPS |  Temp   |  Hum  |  AltBar  | Pressure |  NO2   |   CO   | NH3 | PM1_0 | PM2_5 | PM10_0 
----------+----------------------------+--------------------------------------------+------------+------------+--------+---------+-------+----------+----------+--------+--------+-----+-------+-------+--------
        1 | 2019-09-18 16:58:20.140323 | 01010000007D76C075C58C0DC0BB3775D487344440 | 40.4103952 |  -3.693736 |      0 |   26.58 |    32 |    618.9 |   941.09 |  34.99 |   2.97 |   0 |     0 |     0 |      2
        2 | 2019-09-18 16:58:20.169652 | 0101000000DDC6B0D4C48C0DC073710AE187344440 | 40.4103967 | -3.6937348 |      0 |   26.56 | 31.99 |   619.28 |   941.05 |  34.99 |   3.04 |   0 |     2 |     2 |      4

