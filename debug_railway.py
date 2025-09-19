#!/usr/bin/env python3
"""
Railway部署调试脚本
"""
import os
import sys

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    print("-" * 30)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查环境变量
    env_vars = [
        'PORT', 
        'RAILWAY_ENVIRONMENT_NAME',
        'DATABASE_URL',
        'ADMIN_TOKEN',
        'OPENROUTER_API_KEY'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        if var == 'OPENROUTER_API_KEY' and value != 'Not set':
            value = f"{value[:8]}..." if len(value) > 8 else value
        print(f"{var}: {value}")
    
    print()

def test_imports():
    """测试模块导入"""
    print("📦 测试模块导入...")
    print("-" * 20)
    
    modules = [
        'fastapi',
        'uvicorn', 
        'sqlalchemy',
        'pydantic',
        'requests',
        'python-dotenv'
    ]
    
    for module in modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
    
    print()

def test_app_import():
    """测试应用导入"""
    print("🚀 测试应用导入...")
    print("-" * 20)
    
    try:
        from app.main import app
        print("✅ FastAPI应用导入成功")
        return True
    except Exception as e:
        print(f"❌ FastAPI应用导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """测试数据库连接"""
    print("🗄️ 测试数据库...")
    print("-" * 15)
    
    try:
        from app.model_config import init_tables, SessionLocal
        init_tables()
        with SessionLocal() as db:
            print("✅ 数据库连接成功")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def main():
    print("🔧 Railway部署调试")
    print("=" * 40)
    
    check_environment()
    test_imports()
    
    if test_app_import():
        test_database()
        print("🎉 基本检查完成，应用应该可以启动")
    else:
        print("❌ 应用导入失败，需要修复")

if __name__ == "__main__":
    main()
