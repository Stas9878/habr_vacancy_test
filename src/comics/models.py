from datetime import datetime
from sqlalchemy import (ForeignKey, Column, 
                        Integer, String, orm)

from database import Base
from auth.models import User

class Comic(Base):
    __tablename__ = 'comic'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    rating = Column(Integer, default=0)
    

class Rating(Base):
    __tablename__ = 'rating'
    
    id = Column(Integer, primary_key=True)
    comic_id = Column(Integer, ForeignKey(Comic.id))
    user_id = Column(Integer, ForeignKey(User.id))
    value = Column(Integer, nullable=False)

    @orm.validates('value')
    def validate_age(self, value):
        if not 0 < value < 6:
            raise ValueError(f'Invalid rating value: {value}\nRating must be from 1 to 5 ')
        return value