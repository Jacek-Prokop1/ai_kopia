from flask import Blueprint, render_template, request, jsonify
from models import db, ChatFeedback

admin_feedback_bp = Blueprint("admin_feedback", __name__, url_prefix="/admin/feedbacks")


@admin_feedback_bp.route("/")
def feedback_list():
    """
    Lista wszystkich feedbacków – admin widzi skrót (pierwsze pytanie, fragment odpowiedzi, data, ocena).
    """
    feedbacks = ChatFeedback.query.order_by(ChatFeedback.created_at.desc()).all()
    return render_template("feedback_list.html", feedbacks=feedbacks)


@admin_feedback_bp.route("/confirm", methods=["POST"])
def feedback_confirm():
    """
    API do potwierdzania/odrzucania feedbacku przez admina.
    """
    data = request.json
    feedback_id = data.get("feedback_id")
    confirmed = data.get("confirmed")  # True / False

    if feedback_id is None or confirmed not in [True, False]:
        return jsonify({"error": "Niepoprawne dane"}), 400

    feedback_entry = ChatFeedback.query.get(feedback_id)
    if not feedback_entry:
        return jsonify({"error": "Nie znaleziono feedbacku"}), 404

    feedback_entry.admin_confirmed = confirmed
    db.session.commit()
    return jsonify({"success": True, "admin_confirmed": feedback_entry.admin_confirmed})
