from fastapi import APIRouter, Request, Depends, Query
from pydantic import BaseModel, EmailStr

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import create_response
from app.core.db import get_db

from app.services.user import UserAuthService

router = APIRouter(prefix="/user/auth", tags=["user auth"])


class VcodeLogin(BaseModel):
    target: EmailStr
    vcode: str

class VcodeRegister(BaseModel):
    nickname: str
    password: str
    avatar_path: str = None
    target: EmailStr
    vcode: str

class PswLogin(BaseModel):
    target: EmailStr
    password: str

class RefreshToken(BaseModel):
    refresh_token: str


@router.post("/login/vcode", summary="邮箱验证码登录")
async def user_vcode_login(request: Request, data: VcodeLogin, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = UserAuthService(db)
        result = await auth_service.login_with_email_vcode(data.target, data.vcode, {
            "ipv4": request.client.host,
            "ipv6": request.client.host,
            "device_info": request.headers.get("User-Agent"),
        })
        return create_response(data=result)
    except ValueError as e:
        return create_response(code=400, message=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return create_response(code=500, message="登录失败，请稍后重试")


@router.post("/login/psw", summary="邮箱密码登录")
async def user_psw_login(request: Request, data: PswLogin, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = UserAuthService(db)
        result = await auth_service.login_with_email_password(data.target, data.password, {
            "ipv4": request.client.host,
            "ipv6": request.client.host,
            "device_info": request.headers.get("User-Agent"),
        })
        return create_response(data=result)
    except ValueError as e:
        return create_response(code=400, message=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return create_response(code=500, message="登录失败，请稍后重试")


@router.post("/register/vcode", summary="邮箱验证码注册账号")
async def create_user(request: Request, data: VcodeRegister, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = UserAuthService(db)
        result = await auth_service.register_with_email_vcode(
            nickname=data.nickname,
            password=data.password,
            avatar_path=data.avatar_path,
            target=data.target,
            vcode=data.vcode,
            client_info={
                "ipv4": request.client.host,
                "ipv6": request.client.host,
                "device_info": request.headers.get("User-Agent"),
            }
        )
        return create_response(data=result)
    except ValueError as e:
        return create_response(code=400, message=str(e))
    except Exception as e:
        return create_response(code=500, message="注册失败，请稍后重试")


@router.post("/refresh", summary="刷新访问令牌")
async def refresh_access_token(data: RefreshToken, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = UserAuthService(db)
        result = await auth_service.refresh_token(data.refresh_token)
        return create_response(data=result)
    except ValueError as e:
        return create_response(code=400, message=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return create_response(code=500, message="刷新令牌失败，请重新登录")


@router.post("/logout", summary="退出登录")
async def user_logout(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        # 从Authorization请求头中获取访问令牌
        access_token = request.headers.get("Authorization")
        auth_service = UserAuthService(db)
        await auth_service.logout(access_token)
        return create_response(message="退出登录成功")
    except ValueError as e:
        return create_response(code=400, message=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return create_response(code=500, message="退出登录失败，请稍后重试")