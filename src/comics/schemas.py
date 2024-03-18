from pydantic import BaseModel


class RatingRead(BaseModel):
    id: int
    comic_id: int
    user_id: int
    value: int

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    id: int
    comic_id: int
    user_id: int
    value: int