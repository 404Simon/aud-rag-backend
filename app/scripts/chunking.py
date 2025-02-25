import spacy


def chunk_pages(pages: list[tuple[int, str]]) -> list[tuple[str, int]]:
    nlp = spacy.load("de_core_news_sm")
    chunks: list[tuple[str, int]] = []
    current_chunk = ""
    chunk_start_page = 1

    for page_num, text in pages:
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 500:
                if not current_chunk:  # Start of a new chunk
                    chunk_start_page = page_num
                current_chunk += sentence + " "
            else:
                chunks.append((current_chunk.strip(), chunk_start_page))
                current_chunk = sentence + " "
                chunk_start_page = page_num

    if current_chunk:
        chunks.append((current_chunk.strip(), chunk_start_page))

    return chunks
