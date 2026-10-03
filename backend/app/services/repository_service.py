import uuid
import shutil
import os
from git import Repo
from git.exc import GitCommandError
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.repository import Repository

BASE_REPOSITORY_DIR = "data"

class RepositoryCloneError(Exception):
    pass

def clone_repository(url: str, destination: str, branch: str):
    try:
        Repo.clone_from(url,destination, branch=branch)

        return {
            "status": "success",
            "path": destination
        }
    
        
    except GitCommandError as error:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        raise RepositoryCloneError(str(error))

def create_repository(url: str, branch: str, db: Session):
    repository_id = str(uuid.uuid4())
    destination = os.path.join(BASE_REPOSITORY_DIR,repository_id)

    clone_result = clone_repository(url,destination,branch)

    repository = Repository(
        id=repository_id,
        url=url,
        branch=branch,
        status=clone_result["status"],
        path=clone_result["path"]
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository

TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".go", ".rs", ".c", ".cpp", ".h",
    ".html", ".css", ".json", ".md", ".yaml", ".yml",
    ".toml", ".txt", ".sh", ".sql",
}

IGNORED_DIRECTORIES = {
    ".git", "node_modules", "vendor", "dist", "build",
    ".venv", "venv", "__pycache__",
}