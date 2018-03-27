import argparse
from PIL import Image
import os


def is_valid_path(argument_path):
    if not os.path.exists(argument_path):
        error_message = 'Путь {} не существует'.format(argument_path)
        raise argparse.ArgumentTypeError(error_message)

    return argument_path


def is_positive_int(size_str):
    size_int = int(size_str)
    if size_int < 1:
        error_message = 'Отрицательно число: {} <= 0'.format(size_str)
        raise argparse.ArgumentTypeError(error_message)

    return size_int


def is_positive_float(scale_str):
    scale_float = float(scale_str)
    if scale_float > 0:
        return scale_float

    error_message = 'Отрицательно число: {} <= 0'.format(scale_str)
    raise argparse.ArgumentTypeError(error_message)


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'img_path',
        type=is_valid_path,
        help='Адрес изображения'
    )
    parser.add_argument(
        '--widht',
        type=is_positive_int,
        default=False,
        help='Ширина изображения в px >0'
    )
    parser.add_argument(
        '--height',
        type=is_positive_int,
        default=False,
        help='Высота изображения в px >0'
    )
    parser.add_argument(
        '--scale',
        type=is_positive_float,
        default=False,
        help='Пропорция изменения размера >0'
    )
    parser.add_argument(
        '--output_path',
        type=is_valid_path,
        default=False,
        help='Адрес измененного изображения'
    )
    return parser.parse_args()


def open_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except OSError:
        return False


def get_new_size(old_size, widht, height, scale):
    old_widht, old_height = old_size

    if height and widht:
        new_widht, new_height = widht, height
    elif widht:
        new_height = widht / (old_widht / old_height)
        new_widht = widht
    elif height:
        new_widht = old_widht / old_height * height
        new_height = height
    elif scale:
        new_widht, new_height = [size * scale for size in old_size]
    else:
        return False

    return int(new_widht), int(new_height)


def has_new_ratio(old_size, new_size):
    old_widht, old_height = old_size
    new_widht, new_height = new_size
    old_ratio = old_widht / old_height
    new_ratio = new_widht / new_height
    return abs(old_ratio - new_ratio) > 0.05


def get_new_image_path(image_path, image_name):
    if image_path:
        return os.path.join(image_path, image_name)
    else:
        return os.path.join(os.getcwd(), image_name)


def resize_image(image, image_size):
    return image.resize(image_size, Image.ANTIALIAS)


def get_new_image_name(old_name, image_size):
    main_name, img_format = os.path.splitext(old_name)
    new_name = '{}__{}x{}{}'.format(
        main_name,
        image_size[0],
        image_size[1],
        img_format
    )
    return new_name


def print_result_resizing(image_path, change_ratio):
    if change_ratio:
        print('Изменены пропорции изображения')

    print('Размер успешно изменен\n{}'.format(image_path))


if __name__ == '__main__':
    arg = parsing_arguments()
    if (arg.height or arg.widht) and arg.scale:
        exit('Нельзя одновременно менять размер изображения и масштаб\n'
             'Начните с чего-то одного')
    elif not any([arg.height, arg.widht, arg.scale]):
        exit('Вы не написали по каким критериям изменять размер изображения')

    original_img = open_image(arg.img_path)
    if not original_img:
        exit('Формат изображения не поддерживается')

    user_img = {
        'image': Image.open(arg.img_path),
        'name': os.path.basename(arg.img_path),
        'size': Image.open(arg.img_path).size
    }

    new_image_size = get_new_size(
        user_img['size'],
        arg.widht,
        arg.height,
        arg.scale
    )
    is_ratio_changed = has_new_ratio(user_img['size'], new_image_size)
    resized_img = resize_image(user_img['image'], new_image_size)

    if arg.output_path:
        new_image_path = get_new_image_path(
            arg.output_path,
            user_img['name']
        )
    else:
        new_image_name = get_new_image_name(user_img['name'], new_image_size)
        new_image_path = get_new_image_path(
            os.path.dirname(arg.img_path),
            new_image_name
        )

    resized_img.save(new_image_path)
    print_result_resizing(new_image_path, is_ratio_changed)
