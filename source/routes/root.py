from fastapi import APIRouter

router = APIRouter(
    include_in_schema=False,
)


@router.get("/")
def root():
    return {"message": "Auth Service is running"}


@router.get("/health")
def health():
    return {"message": "Auth Service is healthy"}
