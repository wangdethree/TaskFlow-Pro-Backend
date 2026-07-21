from fastapi import APIRouter, Depends

from app.core.dependencies import get_app_info


router = APIRouter()


@router.get("/dependency")
async def test_dependency(
    data: dict = Depends(get_app_info)
):
    return data