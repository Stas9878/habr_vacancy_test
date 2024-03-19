from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, insert
from fastapi_users_db_sqlalchemy import AsyncSession
from database import get_async_session
from comics.models import Rating, Comics
from comics.schemas import ComicsRead, RatingCreate, ResponseCreateRating
from comics.utils import update_comics_rating, validate_value


router = APIRouter()

@router.post('/ratings', response_model=ResponseCreateRating)
async def add_rating(new_value: RatingCreate, session: AsyncSession = Depends(get_async_session)) -> ResponseCreateRating:    
    try:
        validate_value(new_value.value)

        plus_total = False

        result = await session.execute(
            select(Rating).filter(
                Rating.user_id == new_value.user_id, 
                Rating.comics_id == new_value.comics_id
                )
            )

        rating_obj = result.one_or_none()

        old_value = rating_obj[0].value if rating_obj else 0

        if rating_obj:
            await session.execute(
                update(Rating).where(
                    Rating.comics_id == new_value.comics_id, 
                    Rating.user_id == new_value.user_id
                    ).values(new_value.model_dump())
                )
                
            detail = 'Вы изменили вашу предыдущую оценку на этот комикс.'

        else:
            await session.execute(
                insert(Rating).values(new_value.model_dump())
            )

            detail = 'Мы сохранили вашу оценку.'

            plus_total = True
        
        await update_comics_rating(data=new_value, session=session, plus_total=plus_total, old_value=old_value)

        await session.commit()

        return {
            'status': 'success',
            'detail': detail,
            'data': new_value,
            }
    
    except ValueError:
        return {
            'status': 'error',
            'detail': f'Ваша оценка ({new_value.value}) не находится в диапазоне от 1 до 5',
            'data': None
        }

@router.get('/comics/{comic_id}/rating', response_model=ComicsRead, )
async def get_rating(comic_id: int, session: AsyncSession = Depends(get_async_session)) -> ComicsRead:
    query = select(Comics).where(Comics.id == comic_id)
    
    result = await session.execute(query)

    comics = result.one_or_none()

    if comics:
        return {
            'comics_id': comics[0].id,
            'rating': comics[0].rating
        }
    
    raise HTTPException(status_code=404, detail='Комикса с таким id не существует.')