from httpx import AsyncClient

from .utils import round_price


async def get_dish(
    client: AsyncClient, menu_id: str, submenu_id: str, dish_id: str
) -> dict:
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'price' in response.json()
    return response.json()


async def create_dish(
    client: AsyncClient,
    menu_id: str,
    submenu_id: str,
    title: str,
    description: str,
    price: str,
) -> str:
    response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json={'title': title, 'description': description, 'price': round_price(price)},
    )
    assert response.status_code == 201

    dishes_id = response.json()['id']
    assert response.json() == {
        'id': dishes_id,
        'submenu_id': submenu_id,
        'title': title,
        'description': description,
        'price': round_price(price),
    }
    return dishes_id


async def patch_dish(
    client: AsyncClient,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    title: str,
    description: str,
    price: str,
):
    response = await client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json={
            'title': title,
            'description': description,
            'price': price,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': dish_id,
        'submenu_id': submenu_id,
        'title': title,
        'description': description,
        'price': round_price(price)
    }


async def check_dish_eq_dish(client: AsyncClient, menu_id: str, dish: dict):
    data = await get_dish(client, menu_id, dish['submenu_id'], dish['id'])
    assert data == dish


async def check_dish_in_dishes(client: AsyncClient, menu_id: str, dish: dict):
    response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{dish['submenu_id']}/dishes")
    assert response.status_code == 200
    assert response.json() and any(
        map(
            lambda item: item == dish,
            response.json(),
        )
    )


async def check_dish_not_in_dishes(
    client: AsyncClient, menu_id: str, submenu_id: str, dish_id: str
):
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert not response.json() or not any(
        map(
            lambda item: item['id'] == dish_id,
            response.json(),
        )
    )
