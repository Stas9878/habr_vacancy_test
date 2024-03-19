from fastapi import APIRouter, Depends
from sqlalchemy import select, update, insert
from fastapi_users_db_sqlalchemy import AsyncSession
from database import get_async_session
from comics.models import Rating
from comics.schemas import RatingRead, RatingCreate, ResponseCreateRating
from comics.utils import update_comics_rating


router = APIRouter()

@router.post('/ratings', response_model=ResponseCreateRating)
async def add_rating(new_value: RatingCreate, session: AsyncSession = Depends(get_async_session)) -> ResponseCreateRating:
    plus_total = False

    result = await session.execute(
        select(Rating).filter(
            Rating.user_id == new_value.user_id, 
            Rating.comics_id == new_value.comics_id
            )
        )
    
    if result.one_or_none():
        await session.execute(
            update(Rating).where(
                Rating.comics_id == new_value.comics_id, 
                Rating.user_id == new_value.user_id
                ),
            new_value.model_dump()
            )
        detail = 'Вы изменили вашу предыдущую оценку на этот комикс.'

    else:
        await session.execute(
            insert(Rating),
            new_value.model_dump()
        )
        detail = 'Мы сохранили вашу оценку.'
        plus_total = True
    
    await update_comics_rating(new_value, session, plus_total=plus_total)

    await session.commit()

    return {
        'status': 'success',
        'detail': detail,
        'data': new_value,
        }

# @router.get('/ratings')
# async def get_rating(new_value: RatingCreate, session: AsyncSession = Depends(get_async_session)):
#     query = select(Rating).where(Rating.user_id == new_value.user_id, Rating.comic_id == new_value.comic_id)
#     result = await session.execute(query)
#     arr = result.mappings().all()


#     return {
#         'status': 'success',
#         'data': result.mappings().all(),
#         'details': None
#     }