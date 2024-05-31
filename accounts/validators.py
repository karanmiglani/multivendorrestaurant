from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #cover_image.jpg [0] = cover_image [1] = .jpg
    print(ext)
    valid_extension =['.png' , '.jpg' ,'.jpeg' ,'.PNG' , '.JPG' , '.JPEG',]
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension. Allowed extensions: ' + ', '.join(valid_extension))
