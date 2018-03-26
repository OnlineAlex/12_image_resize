import argparse
from PIL import Image
import os


def validation_image(string):
    valid_formats = ['.png', '.jpg']

    if not os.path.exists(string):
        raise argparse.ArgumentTypeError('Изоражение не найдено')

    image_format = os.path.splitext(string)[-1]
    if image_format not in valid_formats:
        error_message = 'Формат изображения не поддерживается'
        raise argparse.ArgumentTypeError(error_message)

    return string


def validation_path(string):
    if not os.path.exists(string):
        raise argparse.ArgumentTypeError('Папку не найдено')

    return string


def validation_positive_float(string):
    number_float = float(string)
    if 0 >= number_float:
        error_message = 'Отрицательно число: {} <= 0'.format(string)
        raise argparse.ArgumentTypeError(error_message)
    return number_float


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'img_path',
        type=validation_image,
        help='Адрес изображения'
    )
    parser.add_argument(
        '--widht',
        type=validation_positive_float,
        default=False,
        help='Ширина изображения в px >0'
    )
    parser.add_argument(
        '--height',
        type=validation_positive_float,
        default=False,
        help='Высота изображения в px >0'
    )
    parser.add_argument(
        '--scale',
        type=validation_positive_float,
        default=False,
        help='Пропорция изменения размера >0'
    )
    parser.add_argument(
        '--output_path',
        type=validation_path,
        default=False,
        help='Адрес измененного изображения'
    )
    return parser.parse_args()


def get_new_size(old_size, widht, height, scale):
    old_widht = old_size[0]
    old_height = old_size[1]

    if height and widht:
        new_widht, new_height = widht, height
    elif widht:
        new_height = old_widht / old_height / widht
        new_widht = widht
    elif height:
        new_widht = old_widht / old_height * height
        new_height = height
    elif scale:
        new_widht, new_height = [size * scale for size in old_size]
    else:
        return False

    return int(new_widht), int(new_height)


def resize_image(image, new_image_size):
    return image.resize(new_image_size, Image.ANTIALIAS)


def get_new_image_name(old_name, new_image_size):
    main_name, img_format = os.path.splitext(old_name)
    new_name = '{}__{}x{}{}'.format(
        main_name,
        new_image_size[0],
        new_image_size[1],
        img_format
    )
    return new_name


def print_result_resize(image_path, change_ratio):
    if change_ratio:
        print('Изменены пропорции изображения')
    if not os.path.dirname(image_path):
        image_path = os.path.join(os.getcwd(), image_path)

    print('Размер успешлно изменен\n{}'.format(image_path))


if __name__ == '__main__':
    arg = parsing_arguments()
    if (arg.height or arg.widht) and arg.scale:
        exit('Нельзя одновременно менять размер изображения и масштаб\n'
             'Начните с чего-то одного')
    elif not any([arg.height, arg.widht, arg.scale]):
        exit('Вы не написали по каким критериям изменять размер изображения')

    user_img = {
        'image': Image.open(arg.img_path),
        'name': os.path.basename(arg.img_path),
        'size': Image.open(arg.img_path).size
    }

    new_size = get_new_size(
        user_img['size'],
        arg.widht,
        arg.height,
        arg.scale
    )
    is_change_ratio = bool(
        new_size[0] / new_size[1] != user_img['size'][0] / user_img['size'][1]
    )
    resized_img = resize_image(user_img['image'], new_size)

    if arg.output_path:
        new_image_path = os.path.join(
            arg.output_path,
            user_img['name']
        )
        resized_img.save(new_image_path)
    else:
        new_image_name = get_new_image_name(user_img['name'], new_size)
        new_image_path = os.path.join(
            os.path.dirname(arg.img_path),
            new_image_name
        )
        resized_img.save(new_image_name)

    print_result_resize(new_image_path, is_change_ratio)
