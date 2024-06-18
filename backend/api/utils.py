import base64
import os
import uuid

from django.conf import settings
from django.core.files.base import ContentFile

# from django.core.files.storage import FileSystemStorage


def get_image(data):
    if isinstance(data, str) and data.startswith('data:image'):
        # base64 encoded image - decode
        format, imgstr = data.split(';base64,')  # format ~= data:image/X,
        ext = format.split('/')[-1]  # угадать расширение файла

        id = uuid.uuid4()
        imgstr += '=' * (-len(imgstr) % 4)
        decode_data = base64.b64decode(imgstr)
        data = ContentFile(decode_data, name=id.urn[9:] + '.' + ext)
    return data


def save_file(folder: str, file, filename=None) -> str:
    """Сохраняет файл и возвращает путь с именем в uuid"""
    image_bytes = file.read()
    if not filename:
        b_64img = str(base64.b64encode(image_bytes))
        filename = '{}.{}'.format(
            str(uuid.uuid5(uuid.NAMESPACE_X500, b_64img)),
            file.name.rsplit('.')[-1]
        )
    with open(os.path.join(settings.MEDIA_ROOT, folder, filename), "wb") as _f:
            _f.write(image_bytes)
    return os.path.join(settings.MEDIA_URL, folder, filename)
    # fs = FileSystemStorage()
    # path = fs.save('{}{}/{}'.format(
    #     settings.MEDIA_URL, folder, filename), file)
    # return '{}{}'.format(settings.MEDIA_ROOT, path)


def delete_file(path: str) -> None:
    """Удалить файл из директории"""
    try:
        os.remove(path)
    except Exception as e:
        print(e)
