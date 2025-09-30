from app.core.settings import Settings
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from fastapi import UploadFile

cloudinary.config(
    cloud_name=Settings.CLOUDINARY_CLOUD_NAME,      
    api_key=Settings.CLOUDINARY_API_KEY,
    api_secret=Settings.CLOUDINARY_API_SECRET,
    secure=True
)

class FileService:
    @staticmethod
    async def upload_image(file: UploadFile, user_id:str):
        result = upload(
            file.file,
            folder=f'profile_pictures/{user_id}/',
            public_id=file.filename.split('.')[0],
            overwrite=True,
            resource_type="image"
        )
        return result['secure_url']
    