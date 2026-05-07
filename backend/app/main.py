from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="产品评价分析系统", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API路由
@app.get("/")
async def root():
    return {"message": "产品评价分析系统 API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 导入API路由
from app.api import scrape, analyze, report

app.include_router(scrape.router, prefix="/api/v1/scrape", tags=["数据采集"])
app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["数据分析"])
app.include_router(report.router, prefix="/api/v1/report", tags=["报告生成"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
