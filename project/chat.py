from flask import Blueprint, render_template, request, session, redirect, url_for, Response, stream_with_context
from services.chat_service import build_messages, build_system_message
from services.knowledge_service import load_relevant_infos
from services.ai_service import client
from models import db, ChatFeedback
import uuid

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["GET"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("chat.html", chat=session.get("chat_history", []))


@chat_bp.route("/stream", methods=["POST"])
def stream_chat():
    user_question = request.form.get("question", "").strip()
    lang = request.form.get("lang", "pl")

    if "chat_history" not in session:
        session["chat_history"] = []

    # Jeden rekord ChatFeedback na sesję
    if "feedback_id" not in session:
        feedback_entry = ChatFeedback(
            session_id=session["session_id"],
            user_question="",  # puste
            ai_response="",
            rating=None,
            lang=lang
        )
        db.session.add(feedback_entry)
        db.session.commit()
        session["feedback_id"] = feedback_entry.id
    else:
        feedback_entry = ChatFeedback.query.get(session["feedback_id"])

    # budowanie wiadomości dla AI
    baza_problemow = load_relevant_infos(user_question, lang=lang)
    system_message = build_system_message(baza_problemow, lang)
    messages = build_messages(session["chat_history"], user_question, system_message, lang)

    def generate():
        session["chat_history"].append({"user": user_question, "assistant": ""})
        session.modified = True
        idx = len(session["chat_history"]) - 1

        # wyślij ID feedbacku do frontendu
        yield f"data:__FEEDBACK_ID__:{feedback_entry.id}\n\n"

        full_answer = ""
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0,
                max_tokens=400,
                stream=True
            )
            for chunk in response:
                piece = getattr(chunk.choices[0].delta, "content", None)
                if piece:
                    full_answer += piece
                    session["chat_history"][idx]["assistant"] = full_answer
                    session.modified = True

                    # zapis całości historii w jednym rekordzie
                    convo_text = ""
                    for msg in session["chat_history"]:
                        convo_text += f"Ty: {msg['user']}\nAI: {msg['assistant']}\n"
                    feedback_entry.ai_response = convo_text
                    db.session.commit()

                    yield f"data:{piece}\n\n"

        except Exception as e:
            yield f"data:Błąd API: {str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@chat_bp.route("/clear")
def clear():
    session.pop("chat_history", None)
    session.pop("feedback_id", None)
    return redirect(url_for("chat.index"))
