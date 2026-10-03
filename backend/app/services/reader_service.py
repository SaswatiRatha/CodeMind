from pathlib import Path

from app.services.file_service import discover_files

def read_repository_files(repository_path: str) -> list[dict]:
    root = Path(repository_path)
    files = discover_files(repository_path)

    documents = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8",errors="replace")

            documents.append({
                "file_path": str(file_path.relative_to(root)),
                "content": content
            })

        except OSError as error:
            print(f"Could not read {file_path}: {error}")

    return documents