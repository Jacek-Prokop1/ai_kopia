def build_system_message(baza_problemow, lang="pl"):
    if baza_problemow:
        return (
            "Odpowiadaj jak ekspert techniczny:\n"
            "1. Udzielaj konkretnych i rzeczowych odpowiedzi.\n"
            "2. Używaj maksymalnie kilku zdań, unikaj lania wody.\n"
            "3. Nie powtarzaj oczywistych informacji ani fragmentów źródeł.\n"
            "4. Jeśli brakuje danych w bazie, wskaż to i podaj krótką, własną sugestię.\n"
            f"Źródła:\n{baza_problemow}"
        )
    return (
        "Nie znaleziono odpowiedzi w bazie danych. "
        "Użyj własnej wiedzy AI, ale wyraźnie zaznacz brak danych.\nŹródła:\nBRAK"
    )

def build_messages(chat_history, user_question, system_message, lang="pl"):
    lang_instruction = (
        "Odpowiadaj jak doradca techniczny. Udzielaj zwięzłych odpowiedzi: "
        "maksymalnie 5–6 zdań. Nie powtarzaj informacji. Unikaj oczywistości."
        if lang == "pl"
        else "Answer as a technical consultant. Be concise: max 5–6 sentences. "
             "Do not repeat obvious facts or restate sources unnecessarily."
    )

    messages = [{"role": "system", "content": system_message}]
    for entry in chat_history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["assistant"]})
    messages.append({"role": "user", "content": f"{user_question}\n{lang_instruction}"})
    return messages
