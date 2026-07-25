import select
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from auth.deps import get_current_user
from schemas import TagCreate, TagResponse
import models
from database import get_db


router = APIRouter(tags=["tags"])

@router.get("", response_model=list[TagResponse])
async def get_tags(
    profile_id:int,
    db: Annotated[AsyncSession, Depends(get_db)]
    ):
    tags = await db.scalars(select(models.Tag).where(models.Tag.profile_id == profile_id))
    return tags 

@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    profile_id: int, 
    tag: TagCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]):
    new_tag = models.Tag(name= tag.name,profile_id= profile_id, type = tag.type)

    try:
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, f"You already have tag with this name for {tag.type}")

    return new_tag