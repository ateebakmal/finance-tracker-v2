from datetime import date, datetime
from zoneinfo import ZoneInfo

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=3, max_length=15)

class ProfileCreate(Profile):
    # For creating profile we only need name, we extract user_id from token
    pass
     
class ProfileResponse(Profile):
    id:int


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email : EmailStr
    setup_completed: bool

class AuthMeResponse(UserPublic):
    """
    looks like this
    {
     id,
     email,
     setup_completed,
     profiles = []
    }"""
    model_config = ConfigDict(from_attributes=True)
    
    profiles:list[ProfileResponse]

class AuthRefreshAccessTokenResponse(BaseModel):
    access_token:str
    token_type:str


class CategoryBase(BaseModel):
    # We get profile id from url
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    category_name:str = Field(min_length=3, max_length=50)
    parent_id: int | None = Field(gt=0, default=None)
    type:Literal["income","expense"]

    @field_validator("category_name", mode="before")
    @classmethod
    def clean_name(cls, v:str)->str:
        return " ".join(v.split())

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    profile_id: int

class CategoryMini(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id:int
    category_name:str
    type:str

class TagMini(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id:int
    name:str
    type:str

class TagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=3,max_length=25)
    type:Literal["income","expense"]

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v:str)->str:
        return " ".join(v.split())

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id:int = Field(gt=0)


class TransactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    description:str | None = Field(default=None)
    amount:int = Field(gt=0)
    transaction_type:Literal["income","expense"]
    transaction_date: date
    notes:str | None = Field(max_length=500, default=None)
    source_template_id:int | None = Field(default= None)

    # We shouldnt check this here because this check is for TransactionCreate. Its not wrong if its here because no transaction greater than today will be created anyway
    @field_validator("transaction_date")
    @classmethod
    def check_not_in_future(cls, v:date)->date:
        print("We here in this check")
        if v > datetime.now(ZoneInfo("Asia/Karachi")).date():
            raise ValueError("Date cannot be greater than today's date")
        return v
    
class TransactionCreate(TransactionBase):
    category_id:int
    tag_ids:list[int] | None = Field(default=None)

class TransactionResponse(TransactionBase):
    id:int
    profile_id:int
    category:CategoryMini
    tags:list[TagMini]

class TransactionSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    income:int
    expense:int
    balance:int
