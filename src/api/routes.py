from fastapi import APIRouter
from starlette.responses import JSONResponse

from models import Trinket
from src.api.utils import handle_exception
from src.config import settings
from src.services.trinket_client import TrinketClient

router = APIRouter()


@router.post("/trinkets")
async def create_trinket(data: Trinket):
    async with TrinketClient() as client:
        try:
            await client.page.wait_for_load_state("networkidle")
            await client.login(settings.LOGIN, settings.PASSWORD)
            trinket_id, code = await client.create_trinket(data.title, data.code)
            return JSONResponse(content={"id": trinket_id, "title": data.title, "code": code}, status_code=201)
        except Exception as e:
            return handle_exception(e)


@router.patch("/trinkets/{trinket_id}")
async def update_trinket(trinket_id: str, data: Trinket):
    async with TrinketClient() as client:
        try:
            await client.page.wait_for_load_state("networkidle")
            await client.login(settings.LOGIN, settings.PASSWORD)
            updated_code = await client.update_trinket(trinket_id, data.title, data.code)
            return JSONResponse(content={"id": trinket_id, "title": data.title, "code": updated_code}, status_code=200)
        except Exception as e:
            return handle_exception(e)
