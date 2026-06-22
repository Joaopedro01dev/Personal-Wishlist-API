from flask import Blueprint
from flask.globals import request
from spectree import Response
from sqlalchemy import select

from factory import db, api
from models import WishlistItem
from schemas import WishlistItemCreate, WishlistItemResponse, WishlistItemUpdate, WishlistItemList
from utils import DefaultResponse

wishlistItem_controller = Blueprint("wishlistItem_controller", __name__, url_prefix="/api/wishlist")

@wishlistItem_controller.post("/")
@api.validate(json=WishlistItemCreate, resp=Response(HTTP_201=DefaultResponse), tags=["wishlistItem"])
def post_item():
    """
    Create an wishlist item
    """

    data = request.json

    item = WishlistItem(
        name = data["name"],
        description = data["description"] if "description" in data else None,
        link = data["link"] if "link" in data else None,
        purchased = data["purchased"] if "purchased" in data else None,
        sort_order = data["sort_order"] if "sort_order" in data else None
    )

    db.session.add(item)
    db.session.commit()

    response = DefaultResponse(id=item.id, msg="Item criado com sucesso")

    return response, 201

@wishlistItem_controller.get("/")
@api.validate(resp=Response(HTTP_200=WishlistItemList),  tags=["wishlistItem"])
def get_items():
    """
    Get all items
    """

    items = db.session.scalars(select(WishlistItem)).all()
    response = WishlistItemList(items=[WishlistItemResponse.model_validate(item) for item in items]).to_response_dict()

    return response, 200

@wishlistItem_controller.get("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=WishlistItemResponse, HTTP_404=DefaultResponse), tags=["wishlistItem"])
def get_item(item_id):
    """
    Get an item by id
    """

    item = db.session.get(WishlistItem, item_id)

    if item is None:
        response = DefaultResponse(msg=f"Item com o id {item_id} nao foi encontrado")
        return response, 404
    
    response = WishlistItemResponse.model_validate(item).to_response_dict()
    return response, 200

@wishlistItem_controller.put("/<int:item_id>")
@api.validate(json=WishlistItemCreate, resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["wishlistItem"])
def put_item(item_id):
    """
    Update an item by id
    """

    item = db.session.get(WishlistItem, item_id)

    if item is None:
        response = DefaultResponse(msg=f"Item com o id {item_id} nao foi encontrado")
        return response, 404
    
    data = request.json

    item.name = data["name"]
    item.description = data["description"] if "description" in data else item.description
    item.link = data["link"] if "link" in data else item.link
    item.purchased = data["purchased"] if "purchased" in data else item.purchased
    item.sort_order = sort_order = data["sort_order"] if "sort_order" in data else item.sort_order

    db.session.commit()
    response = DefaultResponse(id=item_id, msg="Item atualizado com sucesso")

    return response, 200

@wishlistItem_controller.delete("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["wishlistItem"])
def delete_item(item_id):
    """
    Delete an item by id
    """

    item = db.session.get(WishlistItem, item_id)

    if item is None:
        response = DefaultResponse(id=item_id, msg=f"O item com id {item_id} nao foi encontrado")
        return response, 404
    
    db.session.delete(item)
    db.session.commit()

    response = DefaultResponse(id=item_id, msg=f"Item com id {item_id} foi deletado com sucesso")
    return response, 200

