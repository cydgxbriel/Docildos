from fastapi import APIRouter
from app.api import pedidos, receitas, estoque, agenda, stats, chat, import_api

api_router = APIRouter()

api_router.include_router(pedidos.router)
api_router.include_router(receitas.router)
api_router.include_router(estoque.router)
api_router.include_router(agenda.router)
api_router.include_router(stats.router)
api_router.include_router(chat.router)
api_router.include_router(import_api.router)

