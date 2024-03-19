from fastapi_users_db_sqlalchemy import AsyncSession
from sqlalchemy import update
from comics.models import Comics, Rating
from comics.schemas import RatingCreate


async def update_comics_rating(data: RatingCreate, session: AsyncSession, old_value: int, plus_total:bool = False):
    print(old_value, data.value, plus_total)
    query = await session.execute(
        update(Comics)
            .where(Comics.id == data.comics_id)
                .values(count_of_ratings=(Comics.count_of_ratings + 1) 
                                if plus_total 
                                else Comics.count_of_ratings,

                        total=(Comics.total + data.value) 
                                if plus_total 
                                else (Comics.total - old_value) + data.value,
                                
                        rating=(Comics.total + data.value) / (Comics.count_of_ratings + 1)
                                if plus_total
                                else ((Comics.total - old_value) + data.value) / (Comics.count_of_ratings)
 
                    )
        )   
    

def validate_value(value):
    if not (1 <= value <= 5):
        raise ValueError