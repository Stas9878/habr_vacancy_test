from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update, insert
from fastapi_users_db_sqlalchemy import AsyncSession
from database import get_async_session
from comics.models import Rating, Comics
from comics.schemas import (ComicsRead, RatingCreate, 
                            ResponseCreateRating, ComicsCreate)
from comics.utils import update_comics_rating, validate_value
from auth.base_config import current_user
from auth.models import User


#Роутер для основного приложения
router = APIRouter(tags=['Rating and Comics'])


#Контроллер для добавления рейтинга комиксу
@router.post('/ratings', response_model=ResponseCreateRating)
async def add_rating(new_value: RatingCreate, 
                     user: User = Depends(current_user), 
                     session: AsyncSession = Depends(get_async_session)) -> ResponseCreateRating:    
    try:
        #Проверяем значение на диапазон от 1 до 5 
        validate_value(new_value.value)

        #Если юзер меняет свою оценку, то мы не меняем счётчик оценок
        plus_total = False
        
        #Пытаемся найти оценку этого пользователя на этот комикс
        result = await session.execute(
            select(Rating).filter(
                Rating.user_id == user.id, 
                Rating.comics_id == new_value.comics_id
                )
            )
        
        rating_obj = result.one_or_none()

        #Старая оценка этого пользователя
        old_value = rating_obj[0].value if rating_obj else 0

        #Если юзер уже оставлял оценку, то обновляем её
        if rating_obj:
            await session.execute(
                update(Rating).where(
                    Rating.comics_id == new_value.comics_id, 
                    Rating.user_id == user.id
                    ).values(new_value.model_dump())
                )
                
            detail = 'Вы изменили вашу предыдущую оценку на этот комикс.'

        #Если нет, то создаём объект Rating с оценкой
        else:
            await session.execute(
                insert(Rating).values(new_value.model_dump())
            )

            detail = 'Мы сохранили вашу оценку.'
            
            #Меняем флаг, чтобы увеличить счётчик, 
            # т.к этот юзер не оценивал данный комикс
            plus_total = True
        
        #Ожидаем функцию по обновлению рейтинга комикса
        await update_comics_rating(data=new_value, session=session, plus_total=plus_total, old_value=old_value)

        #Сохраняем изменения в БД
        await session.commit()

        #Возвращаем словарь, который соответствует
        #схеме ResponseCreateRating
        return {
            'status': 'success',
            'detail': detail,
            'data': new_value,
            }
    
    except ValueError:
        #Если не прошли валидацию диапазона оценки
        return {
            'status': 'error',
            'detail': f'Ваша оценка ({new_value.value}) не находится в диапазоне от 1 до 5',
            'data': None
        }


#Возвращаем средний рейтинг комикса
@router.get('/comics/{comic_id}/rating', response_model=ComicsRead)
async def get_rating(comic_id: int, session: AsyncSession = Depends(get_async_session)) -> ComicsRead:
    #Запрос который ищет нужный комикс по id
    query = select(Comics).where(Comics.id == comic_id)

    #Выполнение запроса
    result = await session.execute(query)

    #Или комикс или None
    comics = result.one_or_none()

    if comics:
        #Если комикс есть, то возвращаем его
        return {
            'comics_id': comics[0].id,
            'title': comics[0].title,
            'author': comics[0].author,
            'rating': comics[0].rating
        }

    #Если комикса нет, райзим ошибку
    raise HTTPException(status_code=404, detail='Комикса с таким id не существует.')

#Контроллер для добавления комикса
@router.post('/add_comics')
async def add_comics(comics: ComicsCreate, session: AsyncSession = Depends(get_async_session)) -> ComicsCreate:
    #Добавляем новый комикс
    new_comics = await session.execute(
        insert(Comics).values(comics.model_dump())
    )
    
    #Применяем запрос
    await session.commit()

    return comics