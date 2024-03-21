from pydantic import BaseModel


#RATING

class RatingCreate(BaseModel):
    comics_id: int
    user_id: int
    value: int

class ResponseCreateRating(BaseModel):
    status: str
    detail: str
    data: RatingCreate | None = None


#COMICS

class ComicsRead(BaseModel):
    comics_id: int
    title: str
    author: str
    rating: int

    class Config:
        from_attributes = True

class ComicsCreate(BaseModel):
    title: str
    author: str