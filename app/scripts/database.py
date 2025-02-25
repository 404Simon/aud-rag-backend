import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from psycopg2.extensions import connection, cursor


def setup_database() -> tuple[connection, cursor]:
    conn = psycopg2.connect(
        "dbname=chatbot_db user=chatbot_user password=chatbot_password host=localhost"
    )
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    register_vector(conn)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS slide_chunks (
            id SERIAL PRIMARY KEY,
            content TEXT,
            embedding VECTOR(512),
            page_number INTEGER,
            pdf_filename TEXT
        )
    """
    )
    conn.commit()
    return conn, cur


def store_chunks_and_embeddings(
    conn: connection,
    cur: cursor,
    chunks: list[tuple[str, int]],
    embeddings: np.ndarray,
    pdf_filename: str,
) -> None:
    for (chunk, page_num), embedding in zip(chunks, embeddings):
        cur.execute(
            "INSERT INTO slide_chunks (content, embedding, page_number, pdf_filename) VALUES (%s, %s, %s, %s)",
            (chunk, embedding.tolist(), page_num, pdf_filename),
        )
        print(f"Stored chunk from page {page_num} in {pdf_filename}")
    conn.commit()
