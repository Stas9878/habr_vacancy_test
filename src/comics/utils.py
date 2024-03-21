from fastapi_users_db_sqlalchemy import AsyncSession
from sqlalchemy import update
from comics.models import Comics
from comics.schemas import RatingCreate


#Функция для обновления среднего рейтинга комикса
async def update_comics_rating(data: RatingCreate, session: AsyncSession, old_value: int, plus_total:bool = False) -> None:
    '''count_of_ratings: 

        plus_total = True - прибавляем 1 к числу 
        пользователей, которые оценили этот комикс

        plus_total = False - Не меняем значение счётчика
    
    total:

        plus_total = True - К общей сумме оценок прибавляем 
        новую оценку

        plus_total = False - От общей оценки отнимаем старую оценку 
        юзера и прибавляем новую

    rating: 

        plus_total = True - К общей сумме оценок прибавляем новую
        и делим на общее кол-во оценок + 1 (потому что нужно оценка 
        новая и нужно учесть этого юзера)

        plus_total = False - От общей суммы оценок отнимаем старую  
        и прибавляем новую оценку, потом делим на общее число оценок,
        и не прибавляем 1, потому что счётчик при обновлении оценки не 
        прибавляется.'''

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
    
#Валидация оценки
def validate_value(value) -> None:
    if not (1 <= value <= 5):
        raise ValueError