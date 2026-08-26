
from datetime import datetime, timezone, date
from types import new_class
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import TransactionCreate, TransactionResponse, TransactionSummaryResponse
import models
from database import get_db


router = APIRouter(tags=["transactions"])

# TODO: Maybe add a limit to transactions.
@router.get("",response_model=list[TransactionResponse])
async def get_transactions(profile_id: int, db:Annotated[AsyncSession, Depends(get_db)]):
    today = datetime.now(ZoneInfo("Asia/Karachi")).date()
    month_start = today.replace(day=1)

    result = await db.execute(
        select(models.Transaction)
        .where(
            models.Transaction.profile_id == profile_id,
            models.Transaction.transaction_date >= month_start,
            models.Transaction.transaction_date <= today
        )
        .options(
            selectinload(models.Transaction.category),
            selectinload(models.Transaction.tags)
        )
        .order_by(
                models.Transaction.transaction_date.desc(),
                models.Transaction.created_at.desc()
        )
        )
    
    transactions = result.scalars().all()

    return transactions

@router.post("",response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    profile_id:int,
    transaction: TransactionCreate,
    db:Annotated[AsyncSession, Depends(get_db)]
    ):
    #We get category_id that we have to validate that it belongs to this user
    #We get tag_ids list that we have to validate that all tag belonds to this user
    # Then we insert the transaction
    
    # 1. Check weather this category_id exists and belong to the user
    category = await db.get(models.Category, transaction.category_id)
    if category is None or category.profile_id != profile_id or category.type != transaction.transaction_type:
        print([category.profile_id, category.type] if category else "Category doesnt exist" )
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Category for this profile")
    
    tags = []

    if transaction.tag_ids:
        # 2. Check all tags belong to this user
        tags =  (
                await (db.scalars(
                                select(models.Tag)
                                .where(
                                    models.Tag.id.in_(transaction.tag_ids),
                                    models.Tag.profile_id == profile_id,
                                    models.Tag.type == transaction.transaction_type
                                )
                                ))
                ).all()

        
        valid_tag_ids = {tag.id for tag in tags}

        if valid_tag_ids != set(transaction.tag_ids):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Invalid tag_ids for this profile")
        
    # Insert transaction without tags into Transaction

    new_transaction = models.Transaction(
        profile_id=profile_id,
        category_id = transaction.category_id,
        amount= transaction.amount,
        transaction_date= transaction.transaction_date,
        transaction_type = transaction.transaction_type,
        notes = transaction.notes,
        tags = tags,
        description=transaction.description
    )

    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction, attribute_names=["tags", "category"])
    return new_transaction
    

@router.get("/summary", response_model=TransactionSummaryResponse)
async def get_summary(profile_id : int, db: Annotated[AsyncSession, Depends(get_db)]):

    today = datetime.now(ZoneInfo("Asia/Karachi")).date()
    month_start = today.replace(day=1)

    row = (await db.execute(
        select(
            func.coalesce(
                func.sum(models.Transaction.amount)
                    .filter(models.Transaction.transaction_type == "income"), 0
            ).label("income"),
            func.coalesce(
                func.sum(models.Transaction.amount)
                    .filter(models.Transaction.transaction_type == "expense"), 0
            ).label("expense"),
        ).where(
            models.Transaction.profile_id == profile_id,
            models.Transaction.transaction_date >= month_start,
            models.Transaction.transaction_date <= today,
        )
    )).one()

    return {
        "income": row.income,
        "expense": row.expense,
        "balance": row.income - row.expense
    }



