from app.services.reader_service import read_repository_files

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    if chunk_size<=0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap<0 or overlap>=chunk_size:
        raise ValueError("overlap must be positive value and less than chunk_size")

    chunks = []
    start = 0

    while start<len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start+= chunk_size-overlap

    return chunks

def chunk_repository(repository_path: str) -> list[dict]:
    documents = read_repository_files(repository_path)
    all_chunks = []

    for document in documents:
        chunks = chunk_text(document["content"])

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "file_path": document["file_path"],
                "chunk_index": index,
                "content": chunk
            })

    return all_chunks