from pydantic import BaseModel


class ComicsRead(BaseModel):
    comics_id: int
    rating: int

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