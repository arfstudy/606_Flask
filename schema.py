from typing import Optional

from pydantic import BaseModel, field_validator


class CreateAdvertisement(BaseModel):
    title: str
    description: Optional[str]
    owner: str

    @field_validator("title")
    def secure_title(cls, value):
        if len(value) > 20:
            raise ValueError("The title is too long")
        return value


class UpdateAdvertisement(BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    @field_validator("title")
    def secure_title(cls, value):
        if len(value) > 20:
            raise ValueError("The title is too long")
        return value
