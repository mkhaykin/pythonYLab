from uuid import UUID

from fastapi import Depends, HTTPException

from app.src import schemas
from app.src.repos import SubMenuRepository

from .base import BaseService


class SubMenusService(BaseService):
    def __init__(self, repo: SubMenuRepository = Depends()):
        self.repo = repo

    async def get_all(self, menu_id: UUID) -> list[schemas.GetSubMenu]:
        return await self.repo.get_by_ids(menu_id)

    async def get(self, menu_id: UUID, submenu_id: UUID) -> schemas.GetSubMenu | None:
        result = await self.repo.get_by_ids(menu_id, submenu_id)
        if len(result) == 0:
            raise HTTPException(404, 'submenu not found')
        return result[0]    # TODO check if more one

    async def create(self, menu_id: UUID, submenu: schemas.CreateSubMenuIn) -> schemas.CreateSubMenuOut:
        result = await self.repo.create_submenu(menu_id, submenu)
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, submenu: schemas.UpdateSubMenuIn) -> schemas.UpdateSubMenuIn:
        return await self.repo.update_submenu(menu_id, submenu_id, submenu)

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        return await self.repo.delete_submenu(menu_id, submenu_id)
