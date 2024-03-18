from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from fastapi_users_db_sqlalchemy import AsyncSession
from database import get_async_session
from comics.models import Rating, Comic
from comics.schemas import RatingRead, RatingCreate


router = APIRouter()

@router.post('/ratings')
async def add_rating(new_value: RatingCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(Rating).where(Rating.user_id == new_value.user_id, Rating.comic_id == new_value.comic_id)
    result = await session.execute(query)
    arr = result.mappings().all()

    if arr:
        print(arr, arr[0])
        
    return {
        'status': 'success',
        'data': result.mappings().all(),
        'details': None
    }