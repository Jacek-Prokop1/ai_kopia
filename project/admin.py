from flask import Blueprint, request, redirect, url_for, flash, render_template
from models import db, KnowledgeItem
from services.pdf_service import extract_pdf_sections
from services.ai_service import classify_section
from models import ChatFeedback

admin_bp = Blueprint('admin', __name__)

progress_data = {"current": 0, "total": 0}

@admin_bp.route('/save_message', methods=['POST'])
def save_message():
    global progress_data

    full_text = request.form.get('full_text', '').strip()
    msg_kind = request.form.get('msg_kind', 'message')

    if not full_text:
        flash('Pole wiadomości jest puste', 'error')
        return redirect(url_for('admin.panel'))

    try:
        if full_text.lower().endswith(".pdf"):
            print("[INFO] Rozpoczynam przetwarzanie PDF...")
            sections = extract_pdf_sections(full_text)
            print(f"[INFO] Znaleziono {len(sections)} sekcji w PDF")

            progress_data = {"current": 0, "total": len(sections)}

            for idx, section in enumerate(sections, start=1):
                print(f"[INFO] Przetwarzanie sekcji {idx}")
                progress_data["current"] = idx  

                classification = classify_section(section)

                if classification:
                    for item in classification:
                        print(f" -> Dodaję element: {item.get('title', f'Sekcja {idx}')}")
                        db.session.add(KnowledgeItem(
                            title=item.get("title", f"Sekcja {idx}"),
                            source_type="pdf",
                            category=item.get("type", "inne"),
                            content=item.get("content", section),
                            tags=item.get("tags", []),
                            lang=item.get("lang", "pl"),
                            embedding=item.get("embedding")
                        ))
                else:
                    print(f" -> Sekcja {idx} nie została sklasyfikowana, zapisuję raw content")
                    db.session.add(KnowledgeItem(
                        title=f"Sekcja {idx}",
                        source_type="pdf",
                        category="inne",
                        content=section,
                        lang="pl"
                    ))

            db.session.commit()
            print("[INFO] PDF został zapisany do bazy")
            flash("PDF podzielony i zapisany pomyślnie", "success")

            progress_data = {"current": len(sections), "total": len(sections)}

        else:
            source_type = "general" if msg_kind == "description" else "whatsapp"
            title = "Opis od admina" if msg_kind == "description" else "Wiadomość od admina"

            print(f"[INFO] Zapisuję wiadomość typu {source_type}")
            classification = classify_section(full_text)

            progress_data = {"current": 0, "total": 1}

            if classification:
                for item in classification:
                    print(f" -> Dodaję element: {item.get('title', title)}")
                    db.session.add(KnowledgeItem(
                        title=item.get("title", title),
                        source_type=source_type,
                        category=item.get("type", "inne"),
                        content=item.get("content", full_text),
                        tags=item.get("tags", []),
                        lang=item.get("lang", "pl"),
                        embedding=item.get("embedding")
                    ))
            else:
                print(" -> Brak klasyfikacji, zapisuję całość jako 'inne'")
                db.session.add(KnowledgeItem(
                    title=title,
                    source_type=source_type,
                    category="inne",
                    content=full_text,
                    lang="pl"
                ))

            db.session.commit()
            print("[INFO] Wiadomość zapisana w bazie")
            flash("Wiadomość zapisana pomyślnie", "success")

            progress_data = {"current": 1, "total": 1}

    except Exception as e:
        print(f"[ERROR] Wystąpił błąd: {e}")
        flash(f"Błąd podczas zapisywania: {e}", "error")

    return redirect(url_for('admin.panel'))


@admin_bp.route('/progress')
def progress():
    return progress_data

@admin_bp.route('/')
def panel():
    feedbacks = ChatFeedback.query.order_by(ChatFeedback.created_at.desc()).all()
    return render_template('admin.html', feedbacks=feedbacks)
