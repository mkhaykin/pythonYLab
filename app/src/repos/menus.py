from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.crud import MenusCRUD

from .base import BaseRepository


class MenuRepository(BaseRepository):
    _crud: MenusCRUD
    _name: str = 'menu'

    def __init__(
            self,
            crud: MenusCRUD = Depends(),
    ):
        super().__init__(crud)

    async def get_by_ids(
            self,
            menu_id: UUID | None = None
    ) -> list[schemas.GetMenu]:
        items = await self._crud.get_by_ids(menu_id)
        result = [schemas.GetMenu(**item) for item in items]
        return result

    async def get_orm_all(self):
        return await self._crud.get_orm_all()

    async def create_menu(
            self,
            obj: schemas.CreateMenuIn,
            obj_id: UUID | None = None
    ) -> schemas.CreateMenuOut:
        return schemas.CreateMenuOut(**await self._create(**obj.model_dump(), id=obj_id))

    async def update_menu(
            self,
            menu_id: UUID,
            menu: schemas.UpdateMenuIn
    ) -> schemas.UpdateMenuOut:
        return schemas.UpdateMenuOut(**await self._update(menu_id, **menu.model_dump()))

    async def delete_menu(
            self,
            menu_id: UUID
    ) -> None:
        await self._delete(menu_id)
        return
