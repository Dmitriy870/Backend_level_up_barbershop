import base64

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.redis_dec import cache_red, invalidate_cache
from app.models.specialist import Specialist

from ..exceptions import SpecialistHTTPException
from .shema import CreateSpecialist, SpecialistRespon, UpdateSpecialist


@invalidate_cache
async def create_specialist(
    session: AsyncSession,
    specialist_data: CreateSpecialist,
) -> SpecialistRespon:
    specialist = Specialist(
        last_name=specialist_data.last_name,
        first_name=specialist_data.first_name,
        avatar=specialist_data.avatar,
    )

    session.add(specialist)
    await session.commit()
    await session.refresh(specialist)

    specialist_resp = SpecialistRespon(
        id=specialist.id,
        last_name=specialist_data.last_name,
        first_name=specialist_data.first_name,
        avatar_base64=base64.b64encode(specialist.avatar).decode("utf-8"),
    )

    return specialist_resp


@cache_red(SpecialistRespon)
async def get_specialist(
    session: AsyncSession,
    specialist_id: int,
) -> SpecialistRespon:
    specialist = await session.get(Specialist, specialist_id)
    if not specialist:
        raise SpecialistHTTPException.specialist_not_found

    if specialist.avatar is None:
        raise SpecialistHTTPException.avatar_not_found

    specialist_resp = SpecialistRespon(
        id=specialist.id,
        last_name=specialist.last_name,
        first_name=specialist.first_name,
        avatar_base64=base64.b64encode(specialist.avatar).decode("utf-8"),
    )

    return specialist_resp


@cache_red(SpecialistRespon)
async def get_all_specialists(
    session: AsyncSession,
) -> list[SpecialistRespon]:
    result = await session.execute(select(Specialist))
    specialists = result.scalars().all()

    return [
        SpecialistRespon(
            id=s.id,
            last_name=s.last_name,
            first_name=s.first_name,
            avatar_base64=(
                base64.b64encode(s.avatar).decode("utf-8") if s.avatar else None
            ),
        )
        for s in specialists
    ]


@invalidate_cache
async def update_specialist(
    session: AsyncSession,
    specialist_id: int,
    update_data: UpdateSpecialist,
):
    specialist = await session.get(Specialist, specialist_id)

    if not specialist:
        raise SpecialistHTTPException.specialist_not_found

    if specialist.avatar is None:
        raise SpecialistHTTPException.avatar_not_found

    specialist.last_name = update_data.last_name
    specialist.first_name = update_data.first_name
    specialist.avatar = update_data.avatar

    session.add(specialist)
    await session.commit()
    await session.refresh(specialist)

    specialist_resp = SpecialistRespon(
        id=specialist.id,
        last_name=specialist.last_name,
        first_name=specialist.first_name,
        avatar_base64=base64.b64encode(specialist.avatar).decode("utf-8"),
    )
    return specialist_resp


@invalidate_cache
async def delete_specialist(session: AsyncSession, specialist_id: int):
    specialist = await session.get(Specialist, specialist_id)

    if not specialist:
        raise SpecialistHTTPException.specialist_not_found

    await session.delete(specialist)
    await session.commit()
