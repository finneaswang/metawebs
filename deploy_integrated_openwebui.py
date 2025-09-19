#!/usr/bin/env python3
"""
部署集成的Open WebUI到Railway
"""
import os
import subprocess
import sys
import json
import shutil
from pathlib import Path

def run_command(cmd, check=True, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check, cwd=cwd)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_railway_cli():
    """检查Railway CLI是否安装"""
    stdout, stderr, code = run_command("railway --version", check=False)
    if code != 0:
        print("🔧 Railway CLI未安装，正在安装...")
        if sys.platform == "darwin":  # macOS
            run_command("brew install railway")
        else:  # Linux/WSL
            run_command("curl -fsSL https://railway.app/install.sh | sh")
        print("✅ Railway CLI安装完成")
    else:
        print("✅ Railway CLI已就绪")

def prepare_openwebui_for_railway():
    """为Railway准备Open WebUI"""
    print("📦 准备Open WebUI文件...")
    
    project_root = Path(__file__).parent
    openwebui_path = project_root / "openwebui"
    
    if not openwebui_path.exists():
        print("❌ 找不到openwebui文件夹")
        return False
    
    # 创建Railway特定的环境文件
    env_content = """# Railway Environment Variables
OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
WEBUI_SECRET_KEY=openwebui-railway-secret-2024
WEBUI_AUTH=False
WEBUI_NAME=Railway Open WebUI
PORT=8080
HOST=0.0.0.0
ENABLE_SIGNUP=True
ENABLE_LOGIN_FORM=True
WORKERS=1
TIMEOUT=120
LOG_LEVEL=INFO
"""
    
    with open(openwebui_path / ".env", "w") as f:
        f.write(env_content)
    
    # 创建Railway配置文件
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "DOCKERFILE",
            "dockerfilePath": "Dockerfile"
        },
        "deploy": {
            "healthcheckPath": "/health",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE"
        }
    }
    
    with open(openwebui_path / "railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ Railway配置文件已创建")
    return True

def create_railway_project(openrouter_key):
    """创建Railway项目并部署"""
    print("🚀 创建Railway项目...")
    
    project_root = Path(__file__).parent
    openwebui_path = project_root / "openwebui"
    
    # 切换到openwebui目录
    os.chdir(openwebui_path)
    
    # 初始化git（如果还没有）
    if not (openwebui_path / ".git").exists():
        print("📝 初始化Git仓库...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial Open WebUI for Railway"')
    
    # 登录Railway
    print("🔑 登录Railway...")
    run_command("railway login")
    
    # 创建新项目
    print("📦 创建Railway项目...")
    run_command("railway init")
    
    # 设置环境变量
    print("⚙️ 设置环境变量...")
    env_vars = {
        "OPENAI_API_BASE_URL": "https://openrouter.ai/api/v1",
        "OPENAI_API_KEY": openrouter_key,
        "WEBUI_SECRET_KEY": "openwebui-railway-secret-2024",
        "WEBUI_AUTH": "False",
        "WEBUI_NAME": "Railway Open WebUI",
        "PORT": "8080",
        "HOST": "0.0.0.0",
        "ENABLE_SIGNUP": "True",
        "ENABLE_LOGIN_FORM": "True",
        "WORKERS": "1",
        "TIMEOUT": "120",
        "LOG_LEVEL": "INFO"
    }
    
    for key, value in env_vars.items():
        run_command(f'railway variables set {key}="{value}"')
        print(f"  ✅ {key}")
    
    # 部署
    print("🚀 开始部署...")
    stdout, stderr, code = run_command("railway up")
    
    if code == 0:
        print("🎉 部署成功！")
        
        # 获取域名
        stdout, stderr, code = run_command("railway domain", check=False)
        if code == 0 and stdout:
            print(f"🌐 访问地址: https://{stdout}")
            return f"https://{stdout}"
        else:
            print("📝 请在Railway控制台查看你的域名")
            return "https://railway.app/dashboard"
    else:
        print(f"❌ 部署失败: {stderr}")
        return None

def main():
    """主函数"""
    print("🚀 集成Open WebUI Railway部署工具")
    print("=" * 50)
    
    # 获取OpenRouter API密钥
    openrouter_key = input("请输入你的OpenRouter API密钥: ").strip()
    if not openrouter_key:
        print("❌ 需要OpenRouter API密钥才能继续")
        sys.exit(1)
    
    try:
        # 检查Railway CLI
        check_railway_cli()
        
        # 准备Open WebUI
        if not prepare_openwebui_for_railway():
            print("❌ 准备Open WebUI失败")
            sys.exit(1)
        
        # 创建并部署Railway项目
        url = create_railway_project(openrouter_key)
        
        if url:
            print(f"\n🎉 Open WebUI已成功部署到Railway！")
            print(f"🔗 访问地址: {url}")
            print("📱 你也可以在Railway控制台管理项目: https://railway.app/dashboard")
        else:
            print("\n❌ 部署失败，请检查错误信息")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ 部署已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
