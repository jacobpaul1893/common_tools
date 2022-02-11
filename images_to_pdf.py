import os
from typing import Union
from pydantic import BaseModel, validator
from PIL import Image

class ArgValidator(BaseModel):
    image_list: Union[str, list[str]]
    path_to_save: str

    @validator('*', pre=True)
    def check_field_null(cls, v):
        if not v:
            raise ValueError("Field should not be empty")
        return v

    @validator("path_to_save")
    def check_pdf_extension(cls, v):
        if not v.endswith(".pdf"):
            v = f"{v}.pdf"
        return v

def convert_images_to_pdf(
    img_to_convert: Union[str, list[str]],
    path_to_save: str
) -> str:
    """
    Convert an image or a list of images to pdf.
    For list of images the order of pages in pdf file will follow list order.

    Parameters
    ----------

    img: string or list
        Provide an image or a list of images.
    path_to_save: string
        The relative or absolute path to save pdf file.

    Returns
    -------

    A string mentioning pdf saved location

    """
    params = ArgValidator(
        image_list=img_to_convert,
        path_to_save=path_to_save
    )

    imgs = params.image_list
    file_path = params.path_to_save

    path_list = file_path.split("/")
    if len(path_list) > 1:
        dir_path = "/".join(path_list[:-1])
        os.makedirs(dir_path, exist_ok=True)

    if type(imgs) == str:
        im1 = Image.open(imgs)
        im1.save(file_path, "PDF", resolution=100.0, save_all=True)
        return f"PDF file created at {file_path}"

    im1 = Image.open(imgs[0])
    rest_of_images = [Image.open(img) for img in imgs[1:]]
    im1.save(file_path, "PDF", resolution=100.0, save_all=True, append_images=rest_of_images)
    return f"PDF file created at {file_path}"
