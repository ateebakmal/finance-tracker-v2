
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from auth.deps import get_current_user
from database import get_db
import models
from schemas import CategoryCreate, CategoryResponse

# Note that: All these routes here are prefixed with "/api/profiles/{profile_id}"
# So all routes will have access to profile_id

router = APIRouter(tags=["Categories"])

@router.get("", response_model=list[CategoryResponse])
async def get_all_categories(
    profile_id: int,
    user: Annotated[models.User, Depends(get_current_user)],
    db : Annotated[AsyncSession, Depends(get_db)]
    ):

    result = await db.execute(
        select(models.Category)
        .where(models.Category.profile_id == profile_id)
        )
    
    categories = result.scalars().all()

    return categories

# @router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    profile_id: int,
    category: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
    ):

    # Check parent category belongs to this user.
    if category.parent_id:
        existing = await db.scalar(
                        select(models.Category)
                        .where(models.Category.id == category.parent_id,models.Category.profile_id == profile_id)
                        )
        if existing is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid parent id")
            
    new_category = models.Category(
        profile_id = profile_id,
        category_name = category.category_name, 
        parent_id = category.parent_id,
        type = category.type
        )

    try:
        db.add(new_category)
        await db.commit()

        await db.refresh(new_category)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "You already have a category with this name")
    
    return new_category

