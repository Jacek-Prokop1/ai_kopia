import numpy as np
from models import KnowledgeItem
from services.ai_service import get_embedding
from services.similarity import cosine_similarity

def load_relevant_infos(question_text, lang="pl", max_results=20):
    question_embedding = get_embedding(question_text)
    infos = KnowledgeItem.query.filter_by(lang=lang).all()

    scored_infos = []
    for info in infos:
        if info.embedding:
            vec = np.array(info.embedding, dtype=float)
            score = cosine_similarity(question_embedding, vec)
            scored_infos.append((score, info))

    scored_infos.sort(key=lambda x: x[0], reverse=True)
    relevant_parts = []
    for score, info in scored_infos[:max_results]:
        block = [
            f"Tytuł: {info.title}",
            f"Kategoria: {info.category}",
            f"Źródło: {info.source_type}",
            f"Treść: {info.content}"
        ]
        if info.tags:
            block.append(f"Tagi: {info.tags}")
        relevant_parts.append("\n".join(block))

    return "\n\n---\n\n".join(relevant_parts) if relevant_parts else ""
