from flask import Blueprint, request, jsonify
from .db.crud import get_all_categories

api = Blueprint('api', __name__)


@api.route("/get-categories", methods=["GET"])
def get_categories():
    categories: dict = get_all_categories()  # Fetch all categories to display in the dropdown - {id: "name"}

    return jsonify({"categories": categories}), 200

    