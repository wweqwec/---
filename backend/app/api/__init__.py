from fastapi import APIRouter

router = APIRouter()

from app.api import scrape, analyze, report

router.include_router(scrape.router)
router.include_router(analyze.router)
router.include_router(report.router)
