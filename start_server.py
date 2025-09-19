#!/usr/bin/env python3
"""
启动Metaweb AI模型管理服务器
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置工作目录
os.chdir(project_root)

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    # 设置默认环境变量
    if not os.environ.get("DATABASE_URL"):
        os.environ["DATABASE_URL"] = "sqlite:///./metaweb.db"
    if not os.environ.get("ADMIN_TOKEN"):
        os.environ["ADMIN_TOKEN"] = "admin123"
    
    # 获取端口，Railway会设置PORT环境变量
    port = int(os.environ.get("PORT", 8113))
    
    print("🚀 启动Metaweb AI模型管理服务器...")
    print(f"📊 管理界面: http://localhost:{port}/admin")
    print(f"🤖 模型配置: http://localhost:{port}/admin/model-config")
    print(f"📚 API文档: http://localhost:{port}/docs")
    print("🔑 默认管理员口令: admin123")
    print("-" * 50)
    
    # Railway环境下不使用reload，本地开发时使用reload
    is_railway = os.environ.get("RAILWAY_ENVIRONMENT_NAME") is not None
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=not is_railway,
        log_level="info"
    )