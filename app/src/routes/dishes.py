import http
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.src import schemas
from app.src.services import DishesService

router = APIRouter()

DISH_PRICE_ENCODER = {float: lambda x: f'{round(float(x), 2):.2f}'}


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes
@router.get(path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
            summary='Get all dishes from a submenu',
            status_code=http.HTTPStatus.OK)
async def get_dishes(menu_id: UUID, submenu_id: UUID, service: DishesService = Depends()):
    # check menu | submenu | dish
    # TODO check submenu? 2 jsonable_encoder (((
    res = jsonable_encoder(await service.get_by_submenu(menu_id, submenu_id))
    return jsonable_encoder(res, custom_encoder=DISH_PRICE_ENCODER)


# GET /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.get(path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            summary='Get the dish by and id',
            status_code=http.HTTPStatus.OK
            )
async def get_dish(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, service: DishesService = Depends()
):
    res = jsonable_encoder(await service.get(menu_id, submenu_id, dish_id))
    return jsonable_encoder(res,
                            custom_encoder=DISH_PRICE_ENCODER)


# POST /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes
@router.post(path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
             summary='Create the dish',
             status_code=http.HTTPStatus.CREATED)
async def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish: schemas.CreateDish,
        service: DishesService = Depends(),
):
    return jsonable_encoder(await service.create(menu_id, submenu_id, dish),
                            custom_encoder=DISH_PRICE_ENCODER)


# PATCH /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Update the dish',
    status_code=http.HTTPStatus.OK,
)
async def patch_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish: schemas.UpdateDish,
        service: DishesService = Depends(),
):
    return jsonable_encoder(await service.update(menu_id, submenu_id, dish_id, dish),
                            custom_encoder=DISH_PRICE_ENCODER)


# DELETE /app/v1/menus/{{api_test_menu_id}}/submenus/{{api_test_submenu_id}}/dishes/{{api_test_dish_id}}
@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
               summary='Delete the dish',
               status_code=http.HTTPStatus.OK,
               )
async def delete_dish(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, service: DishesService = Depends(),
):
    return await service.delete(menu_id, submenu_id, dish_id)
