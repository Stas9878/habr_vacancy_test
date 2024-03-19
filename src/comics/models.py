from sqlalchemy import (ForeignKey, Column, 
                        Integer, String, Float, orm)

from database import Base
from auth.models import User

class Comics(Base):
    __tablename__ = 'comics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    count_of_ratings = Column(Integer, default=0)
    total = Column(Integer, default=0)
    rating = Column(Float, default=0)
    

class Rating(Base):
    __tablename__ = 'rating'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    comics_id = Column(Integer, ForeignKey(Comics.id))
    user_id = Column(Integer, ForeignKey(User.id))
    value = Column(Integer, nullable=False)

    @orm.validates('value')
    def validate_value(cls, value):
        if not 0 < value < 6:
            raise ValueError(f'Invalid rating value: {value}\nRating must be from 1 to 5 ')
        return value