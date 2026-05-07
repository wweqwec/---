from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter()

class ReportRequest(BaseModel):
    task_id: str
    format: str = "pdf"  # pdf, docx, xlsx
    title: str = "产品评价分析报告"

@router.post("/generate")
async def generate_report(request: ReportRequest):
    """生成分析报告"""
    # 这里应该调用实际的报告生成逻辑
    # 使用 PDF/Word/Excel Skills
    
    return {
        "task_id": request.task_id,
        "status": "generated",
        "format": request.format,
        "download_url": f"/api/v1/report/download/{request.task_id}"
    }

@router.get("/download/{task_id}")
async def download_report(task_id: str, format: str = "pdf"):
    """下载报告"""
    # 模拟文件路径
    file_path = f"./reports/{task_id}/report.{format}"
    
    # 实际应该检查文件是否存在
    if not os.path.exists(file_path):
        # 生成一个示例文件
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write("示例报告内容")
    
    return FileResponse(
        path=file_path,
        filename=f"产品评价分析报告.{format}",
        media_type="application/octet-stream"
    )

@router.get("/list")
async def list_reports():
    """列出所有报告"""
    reports = [
        {
            "id": "report_001",
            "title": "iPhone 15 Pro Max 评价分析",
            "created_at": "2026-04-28",
            "formats": ["pdf", "docx", "xlsx"]
        },
        {
            "id": "report_002",
            "title": "华为Mate 60 Pro 竞品对比",
            "created_at": "2026-04-27",
            "formats": ["pdf"]
        }
    ]
    
    return {"total": len(reports), "reports": reports}
