from app.db.models import SlideChunk
from app.scripts.embedding import generate_embedding
from sqlalchemy.orm import Session
from sqlalchemy import text


def query_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 5,
    document_title_filter_patterns: list[str] | None = None,
) -> list[tuple[int, str, int, str, float]]:
    embedding = generate_embedding(query)

    sql_query = """
        SELECT id, content, page_number, pdf_filename, embedding <-> CAST(:embedding AS vector) AS similarity_score
        FROM slide_chunks
    """

    where_clause = []
    if document_title_filter_patterns:
        for i, pattern in enumerate(document_title_filter_patterns):
            where_clause.append(f"pdf_filename LIKE :pattern_{i}")

    if where_clause:
        sql_query += " WHERE " + " OR ".join(where_clause)

    sql_query += """
        ORDER BY similarity_score
        LIMIT :top_k
    """

    params = {"embedding": embedding, "top_k": top_k}
    if document_title_filter_patterns:
        for i, pattern in enumerate(document_title_filter_patterns):
            params[f"pattern_{i}"] = pattern

    return db.query(SlideChunk).from_statement(text(sql_query)).params(**params).all()