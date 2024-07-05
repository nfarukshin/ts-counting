# ts-counting
Scripts for parsing data from tournament site of mind games movement (rating.chgk.info)

## How to use ts-counting

Используется для копирования результатов команд, которые дисциплинарная группа рекомендует удалить с турнирного сайта. Также в консоль выводится сообщение, которое нужно добавить в комментарий к турниру.

1. После -i указываем id турнира
2. Далее указываем либо id команды, данные которой удаляются, с помощью -t; либо id площадки, команды которой удаляются, с помощью -v
3. В конце указываем ссылку на решение на сайте МАИИ с помощью -a

Пример кода:
python ts_counting.py -i 10595 -t 77032 -a https://www.maii.li/docs/2024-07-04-reshenie-dg-18/
или
ts_counting.py -i 9171 -v 3568 -a https://www.maii.li/docs/2024-07-04-reshenie-dg-18/