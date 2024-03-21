from pydantic import BaseModel


#RATING

#Схема для Rating.POST
class RatingCreate(BaseModel):
    comics_id: int
    user_id: int
    value: int

#Схема для ответа в Rating.POST
class ResponseCreateRating(BaseModel):
    status: str
    detail: str
    data: RatingCreate | None = None


#COMICS
    
#Схема для Comics.GET
class ComicsRead(BaseModel):
    comics_id: int
    title: str
    author: str
    rating: int

    class Config:
        from_attributes = True

#Схема для Comics.POST
class ComicsCreate(BaseModel):
    title: str
    author: str