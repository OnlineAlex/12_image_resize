# Изменение размера изображения

Скрипт сохраняет копию вашего изображения с заданым размером.

**Возможности:**
* подогнать по ширине
* подогнать по высоте
* задать ширину и высоту
* измерить масштаб
* сохранить в указанную папку
* сохранить рядом с оригиналом

### Пример

```bash
> python image_resize.py tevin-trinh.jpg --scale 0.7 --output_path A:\devman
Размер успешно изменен
A:\myproject\tevin-trinh.jpg
```
# Требования
Совестимые OC:
* Linux,
* Windows
* MacOS

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5 выше

И  пакетов из requirements.txt
```bash
pip install -r requirements.txt # или командой pip3
```

Поддерживаемые форматы изображений: `.jpg, .png`
# Как работать
> Запуск для всех ОС одинаковый
Стандатной командой `python` (на некоторых компьютерах `python3`).
```bash
$ python image_resize.py [-h] [--widht WIDHT] [--height HEIGHT] [--scale SCALE]
                       [--output_path OUTPUT_PATH]
                       img_path

positional arguments:
  img_path                   Адрес изображения

optional arguments:
  -h, --help                 show this help message and exit
  --widht WIDHT              Ширина изображения в px >0
  --height HEIGHT            Высота изображения в px >0
  --scale SCALE              Пропорция изменения размера >0
  --output_path OUTPUT_PATH  Адрес измененного изображения

```

Если `--output_path` не задан, изображение сохранится рядом с измененным именем
 ```bash
> python image_resize.py A:\myproject\tevin-trinh.jpg --height 1000
Размер успешно изменен
A:\myproject\tevin-trinh__1509x1000.jpg
```
Помните, рекомендуется использовать [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) для лучшего управления пакетами.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
