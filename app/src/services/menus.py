from uuid import UUID

from fastapi import Depends

from app.src import schemas
from app.src.repos import MenuRepository

from .base import BaseService
from .submenus import SubMenusService


class MenusService(BaseService):
    def __init__(self, repo: MenuRepository = Depends(),
                 service_submenu: SubMenusService = Depends()):
        self.repo = repo
        self.service_submenu = service_submenu

    async def get_orm_all(self) -> list:
        return await self.repo.get_orm_all()

    async def get_all(self) -> list[schemas.GetMenu]:
        return await self.repo.get_by_ids()

    async def get_full(self) -> list[schemas.GetMenuFull]:
        result: list[schemas.GetMenuFull] = []
        menus: list[schemas.GetMenu] = await self.repo.get_by_ids()
        for menu in menus:
            result_menu: schemas.GetMenuFull
            submenus = await self.service_submenu.get_full(menu.id)
            result_menu = schemas.GetMenuFull(**menu.model_dump(), submenus=submenus)
            result.append(result_menu)
        return result

    async def get(self, menu_id: UUID) -> schemas.GetMenu | None:
        result = await self.repo.get_by_ids(menu_id)
        return self.get_one(result, 'menu not found')

    async def create(self, menu: schemas.CreateMenuIn) -> schemas.CreateMenuOut:
        return await self.repo.create_menu(menu)

    async def update(self, menu_id: UUID, menu: schemas.UpdateMenuIn) -> schemas.UpdateMenuOut:
        return await self.repo.update_menu(menu_id, menu)

    async def delete(self, menu_id: UUID) -> schemas.MessageMenuDeleted:
        await self.repo.delete_menu(menu_id)
        return schemas.MessageMenuDeleted()
