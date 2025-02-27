from flask import Blueprint, request, jsonify
from .db.crud import get_all_categories, get_all_topics

api = Blueprint('api', __name__)


@api.route("/get-categories", methods=["GET"])
def get_categories():
    categories: list[dict] = get_all_categories()   # Fetch all categories to display in the dropdown 
                                                    # {
                                                    # "category_id": category_id, -> str: int
                                                    # "category": category        -> str: str
                                                    # }

    return jsonify({"categories": categories}), 200


@api.route("/get-topics", methods=["GET"])
def get_topics():
    topics: list[dict] = get_all_topics()   # Fetch all topics to display in the dropdown
                                            # {
                                            # "topic_id": topic_id,   -> str: int
                                            # "topic": topic, -> str: str
                                            # "category_id", category_id  -> str: int
                                            # } 

    return jsonify({"topics": topics}), 200
