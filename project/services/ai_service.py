import re
import json
from openai_client import client  

# generuje wektory
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# klasyfikacja
def safe_json_parse(result_text):
    try:
        cleaned = re.search(r"\[.*\]", result_text, re.S)
        if cleaned:
            return json.loads(cleaned.group(0))
    except Exception:
        pass
    return []

def classify_section(section, retries=2):
    """
    Klasyfikuje sekcję tekstu i generuje embedding.
    """
    prompt = (
        "Podziel poniższy tekst na kategorie: Tytuł, Typ (info/problem/solution/inne), "
        "Treść, listę tagów oraz język ('pl' lub 'en').\n"
        "Zwróć JSON w formacie:\n"
        "[{\"title\": \"...\", \"type\": \"...\", \"content\": \"...\", \"tags\": [\"...\"], \"lang\": \"pl\"}]\n\n"
        f"Tekst:\n{section}"
    )

    for _ in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=400
            )
            result_text = response.choices[0].message.content.strip()
            parsed = safe_json_parse(result_text)

            for item in parsed:
                item["embedding"] = get_embedding(item.get("content", section))

            if parsed:
                return parsed
        except Exception:
            pass
    return []
