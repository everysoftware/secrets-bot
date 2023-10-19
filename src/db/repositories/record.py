from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import User, Record, Comment


class RecordRepo(Repository[Record]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Record, session=session)

    def new(
            self,
            user: User,
            url: str,
            title: str,
            username: bytes,
            password: bytes,
            salt: bytes,
            comment: Comment,
    ) -> Record:
        new_record = Record(
            user=user,
            url=url,
            title=title,
            username=username,
            password_=password,
            salt=salt,
            comment=comment,
        )
        self.session.add(new_record)
        return new_record