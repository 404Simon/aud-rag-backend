from database import setup_database, store_chunks_and_embeddings
from extraction import extract_text_from_pdf
from chunking import chunk_pages
from embedding import generate_embeddings
import os


def rag_pipeline(pdf_directory: str) -> None:
    conn, cur = setup_database()
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            pages = extract_text_from_pdf(pdf_path)
            chunks = chunk_pages(pages)
            embeddings = generate_embeddings(chunks)
            store_chunks_and_embeddings(conn, cur, chunks, embeddings, filename)
    cur.close()
    conn.close()


def main():
    pdf_directory: str = "data/AuD_Slides/pdfs"
    rag_pipeline(pdf_directory)


if __name__ == "__main__":
    main()
