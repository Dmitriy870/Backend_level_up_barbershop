from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import get_current_admin, get_current_user
from app.database import db_helper
from app.models.user import User

from . import service
from .dependencies import get_specialist_by_id
from .shema import CreateSpecialist, SpecialistRespon, UpdateSpecialist

router = APIRouter(tags=["specialist"])


@router.get("/specialists", response_model=list[SpecialistRespon])
async def get_all_specialists(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(get_current_user),
):
    return await service.get_all_specialists(session=session)


@router.get("/specialists/{specialist_id}", response_model=SpecialistRespon)
async def get_specialist(
    result=Depends(get_specialist_by_id),
    user: User = Depends(get_current_user),
):
    return result


@router.post("/add_specialist/", status_code=status.HTTP_201_CREATED)
async def add_specialist(
    last_name: str = Form(...),
    first_name: str = Form(...),
    avatar: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    admin: User = Depends(get_current_admin),
) -> SpecialistRespon:
    img_bytes = await avatar.read()  # Читаем байты изображения
    specialist_data = CreateSpecialist(
        last_name=last_name, first_name=first_name, avatar=img_bytes
    )
    return await service.create_specialist(
        session=session, specialist_data=specialist_data
    )


@router.put("/update_specialist/{id}", response_model=SpecialistRespon)
async def update_specialist(
    id: int,
    specialist_update: UpdateSpecialist,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    admin: User = Depends(get_current_admin),
):
    return await service.update_specialist(
        session=session, specialist_id=id, update_data=specialist_update
    )


@router.delete("/delete_specialist/{id}", status_code=204)
async def delete_specialist(
    id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(get_current_user),
):
    await service.delete_specialist(session=session, specialist_id=id)
