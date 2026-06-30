import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from src.core.config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)





def upload_image(image: UploadFile):
    result = cloudinary.uploader.upload(
        image.file,
        folder="mango_products"
    )

    return {
        "secure_url": result["secure_url"],
        "public_id": result["public_id"]
    }