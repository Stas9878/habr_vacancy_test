from pydantic import BaseModel


class RatingRead(BaseModel):
    id: int
    comics_id: int
    user_id: int
    value: int

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    comics_id: int
    user_id: int
    value: int

class ResponseCreateRating(BaseModel):
    status: str
    detail: str
    data: RatingCreate | None = None