from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from app.core.db import get_db
from app.core.responses import create_response

from app.services.verification import VerificationCodeService

router = APIRouter(prefix="/verification", tags=["verification"])

class EmailVerifyCode(BaseModel):
    target: EmailStr


@router.post("/email/send", summary="发送邮箱验证码")
async def send_email_verify_code(request: Request, data: EmailVerifyCode, db: AsyncSession = Depends(get_db)):
    try:
        verification_service = VerificationCodeService(db)
        verification_service.is_email(data.target)
        await verification_service.create_code(data.target, "LexTrade 注册验证码")
        return create_response(message="验证码发送成功")
    except ValueError as e:
        return create_response(code=400, message=str(e))
    except Exception as e:
        return create_response(code=500, message=str(e))