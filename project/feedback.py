from flask import Blueprint, request, jsonify
from models import db, ChatFeedback

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/rate", methods=["POST"])
def rate_chat():
    data = request.json
    feedback_id = data.get("feedback_id")
    rating = data.get("rating")  # "up" / "down"

    if not feedback_id or rating not in ["up", "down"]:
        return jsonify({"error": "Niepoprawne dane"}), 400

    feedback_entry = ChatFeedback.query.get(feedback_id)
    if not feedback_entry:
        return jsonify({"error": "Nie znaleziono wpisu"}), 404

    feedback_entry.rating = rating
    db.session.commit()

    return jsonify({"success": True})
