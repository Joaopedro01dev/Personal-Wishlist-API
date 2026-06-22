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

    dados = request.context.json.model_dump(exclude_none=True)
    item = WishlistItem(**dados)

    db.session.add(item)
    db.session.commit()

    response = DefaultResponse(id=item.id, msg="Item criado com sucesso.").model_dump()

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
@api.validate(json=WishlistItemUpdate, resp=Response(HTTP_200=WishlistItemResponse, HTTP_404=DefaultResponse), tags=["wishlistItem"])
def put_item(item_id):
    """
    Update an item by id
    """

    item = db.session.get(WishlistItem, item_id)

    if item is None:
        response = DefaultResponse(msg="Item nao foi encontrado")
        return response, 404
    
    dados_novos = request.context.json.model_dump(exclude_unset=True)

    for chave, valor in dados_novos.items():
        setattr(item, chave, valor)

    db.session.commit()
    response = WishlistItemResponse.model_validate(item).to_response_dict()

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

