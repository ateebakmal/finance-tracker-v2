from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response,status
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, inspect

# From auth module import oauth
from auth.oauth import oauth
from auth.utils import create_access_token, generate_refresh_token, hash_refresh_token
from auth.deps import get_current_user

from schemas import AuthMeResponse, AuthRefreshAccessTokenResponse
from database import get_db
from config import settings
import models

import traceback
router = APIRouter()
REFRESH_COOKIE = "refresh_cookie"
# Helper functions might move into a new file
def set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        key = REFRESH_COOKIE,
        value = refresh_token,
        httponly=True,
        secure = settings.cookie_secure,
        samesite=settings.cookie_samesite,        
        max_age = settings.refresh_token_expire_days * 24 * 3600,
        path = "/api/auth"
    )

@router.get("/google/login")
async def google_login(request: Request):
    """Step 1: bounce the browser to Google. Authlib generates & stores `state`."""
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db : Annotated[AsyncSession, Depends(get_db)]):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Google authentication failed")
    
    claims = token["userinfo"]

    google_sub,email = claims["sub"], claims["email"]

    
    # TODO: Might need to move these database functions into seperate functions
    # 1. Get or create user
    result = await db.execute(select(models.User).where(models.User.google_sub == google_sub))
    user = result.scalar_one_or_none()

    # 1.1 If user doesnt exist with this sub create one
    if user is None:
        user = models.User(google_sub = google_sub, email = email)
        db.add(user)
        await db.flush()
    
    # Now either we have user that already existed or newly created user
    # return {c.key: getattr(user, c.key) for c in inspect(user).mapper.column_attrs}

    # 2. Create refresh token in the database
    refresh_token = generate_refresh_token()
    refresh_token_hash = hash_refresh_token(refresh_token)

    session = models.Session(
        user_id = user.id,
        token_hash = refresh_token_hash,
        expires_at = datetime.now(timezone.utc) + timedelta(days = settings.refresh_token_expire_days),
        device_info = request.headers.get("user-agent")
    )
    db.add(session)

    #now session and user are added into db.

    await db.commit()

    response = RedirectResponse(url= f"{settings.frontend_url}/dashboard")
    set_refresh_cookie(response, refresh_token)

    return response

@router.post("/refresh", response_model=AuthRefreshAccessTokenResponse)
async def refresh(
        request : Request,
        response : Response,
        db: Annotated[AsyncSession, Depends(get_db)]
    ):
    print(request.cookies)
    refresh_token = request.cookies.get(REFRESH_COOKIE)
    

    # If there is no refresh cookie we reject the request
    if not refresh_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"No refresh token")
    
    # If there is refresh token
    # Validate it. If it is valid create access_token and return it

    result = await db.execute(
                    select(models.Session)
                    .where(models.Session.token_hash == hash_refresh_token(refresh_token))    
                )
    
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"No Refresh Found")
    
    if session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token expired")
    
    # We now session is valid.
    # We create new refresh token

    new_refresh_token = generate_refresh_token()
    # Update refresh token since old one is used
    session.token_hash = hash_refresh_token(new_refresh_token)
    session.expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    await db.commit()
    # Set new refresh token to the cookie
    set_refresh_cookie(response, new_refresh_token)

    
    # Return new access token
    return {
        "access_token" : create_access_token(session.user_id),
        "token_type" : "bearer"
    }
    
@router.get("/me", response_model=AuthMeResponse)
async def get_me(
        current_user : Annotated[models.User, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)]
    ):
    # Get profiles for this user
    result = await db.execute(
        select(models.Profile)
        .where(models.Profile.user_id == current_user.id)
        )
    profiles = result.scalars().all()
    return {
        "id" : current_user.id,
        "email" : current_user.email,
        "setup_completed": current_user.setup_completed,
        "profiles" : profiles
    }


@router.post("/logout")
async def logout(request: Request, db:Annotated[AsyncSession, Depends(get_db)]):
    refresh_token = request.cookies.get(REFRESH_COOKIE)

    if refresh_token:
        await db.execute(
            delete(models.Session).where(models.Session.token_hash == hash_refresh_token(refresh_token))
            )
        
        await db.commit()

    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(REFRESH_COOKIE,path="/api/auth")
    return response
    