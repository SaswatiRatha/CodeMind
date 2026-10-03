from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.repository import Repository
from app.models.schemas import RepositoryRequest, RepositoryResponse
from app.services.repository_service import create_repository, RepositoryCloneError
from app.dependencies import get_app_name

router = APIRouter(prefix="/repositories", tags=["Repositories"])

@router.get("/", response_model=list[RepositoryResponse])
def list_repositories(db: Session = Depends(get_db)):
    return db.query(Repository).all()

@router.get("/{repository_id}", response_model=RepositoryResponse)
def get_repository(repository_id: str, db: Session = Depends(get_db)):
    repository = db.query(Repository).filter(Repository.id == repository_id).first()

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )
    return repository

@router.post("/", response_model=RepositoryResponse, status_code=201)
def create_repository_endpoint(repository: RepositoryRequest, db: Session = Depends(get_db)):
    try:
        return create_repository(
            str(repository.url),
            repository.branch,
            db
        )
    except RepositoryCloneError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
