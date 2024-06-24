import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from ninja import UploadedFile, File


def save_file(file_path: str, file: UploadedFile=File(...)) -> str:
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    image = Image.open(BytesIO(file.read()))
    image.save(file_path)

    return os.path.relpath(file_path, settings.MEDIA_ROOT)
