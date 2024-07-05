# ts-counting
Scripts for parsing data from tournament site of mind games movement (rating.chgk.info)

## How to use

1. После -i указываем id турнира
2. Далее указываем либо id команды, данные которой удаляются, с помощью -t; либо id площадки, команды которой удаляются, с помощью -v

Пример кода:
python ts_counting.py -i 10595 -t 89090
или
ts_counting.py -i 9171 -v 3568