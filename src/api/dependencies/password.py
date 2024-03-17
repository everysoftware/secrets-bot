from fastapi import Depends

from src.api.exceptions import PasswordNotFound, NotEnoughRights
from src.application.auth import get_current_user
from src.application.dependencies import get_password_service
from src.application.services import PasswordService
from src.domain.schemes import SPassword
from src.infrastructure.models import UserOrm


async def valid_password(
    item_id: int,
    user: UserOrm = Depends(get_current_user),
    service: PasswordService = Depends(get_password_service),
) -> SPassword:
    password = await service.get(item_id)

    if password is None:
        raise PasswordNotFound()

    if password.user_id != user.id and not user.is_superuser:
        raise NotEnoughRights()

    return password
