#!/usr/bin/env python3
"""
在Railway上部署Open WebUI的自动化脚本
"""
import os
import subprocess
import sys
import json
import time

def run_command(cmd, check=True):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
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
        
        # 添加到PATH
        if "railway" not in os.environ.get("PATH", ""):
            os.environ["PATH"] += ":/home/runner/.local/bin:/usr/local/bin"
    
    print("✅ Railway CLI已准备就绪")

def create_openwebui_project():
    """创建Open WebUI项目文件"""
    
    # 创建项目目录
    project_dir = "/tmp/openwebui-railway"
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)
    
    # 创建Dockerfile
    dockerfile_content = """
FROM ghcr.io/open-webui/open-webui:main

# 设置环境变量
ENV WEBUI_SECRET_KEY=""
ENV OPENAI_API_BASE_URL=""
ENV OPENAI_API_KEY=""
ENV WEBUI_AUTH=False

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "-m", "open_webui.main"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # 创建railway.json配置
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "DOCKERFILE",
            "dockerfilePath": "Dockerfile"
        },
        "deploy": {
            "startCommand": "",
            "healthcheckPath": "/health",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    # 创建.gitignore
    gitignore_content = """
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    # 创建README
    readme_content = """# Open WebUI on Railway

这是一个部署在Railway上的Open WebUI实例。

## 环境变量

请在Railway项目中设置以下环境变量：

- `OPENAI_API_BASE_URL`: https://openrouter.ai/api/v1
- `OPENAI_API_KEY`: 你的OpenRouter API密钥
- `WEBUI_SECRET_KEY`: 随机字符串用于加密
- `WEBUI_AUTH`: False (禁用认证)

## 访问

部署完成后，通过Railway提供的域名访问Open WebUI。
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Open WebUI项目文件已创建在: {project_dir}")
    return project_dir

def deploy_to_railway(project_dir, openrouter_key):
    """部署到Railway"""
    os.chdir(project_dir)
    
    print("🚀 开始部署到Railway...")
    
    # 初始化git仓库
    run_command("git init")
    run_command("git add .")
    run_command('git commit -m "Initial Open WebUI setup"')
    
    # 登录Railway
    print("🔑 请在浏览器中完成Railway登录...")
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
        "PORT": "8080"
    }
    
    for key, value in env_vars.items():
        run_command(f'railway variables set {key}="{value}"')
        print(f"  ✅ {key}")
    
    # 部署
    print("🚀 部署中...")
    stdout, stderr, code = run_command("railway up")
    
    if code == 0:
        print("🎉 部署成功！")
        # 获取域名
        stdout, stderr, code = run_command("railway domain")
        if code == 0 and stdout:
            print(f"🌐 访问地址: https://{stdout}")
        else:
            print("📝 请在Railway控制台查看你的域名")
    else:
        print(f"❌ 部署失败: {stderr}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 Open WebUI Railway 部署工具")
    print("=" * 40)
    
    # 获取OpenRouter API密钥
    openrouter_key = input("请输入你的OpenRouter API密钥: ").strip()
    if not openrouter_key:
        print("❌ 需要OpenRouter API密钥才能继续")
        sys.exit(1)
    
    try:
        # 检查Railway CLI
        check_railway_cli()
        
        # 创建项目文件
        project_dir = create_openwebui_project()
        
        # 部署到Railway
        if deploy_to_railway(project_dir, openrouter_key):
            print("\n🎉 Open WebUI已成功部署到Railway！")
            print("📱 请在Railway控制台查看部署状态和域名")
            print("🔗 Railway控制台: https://railway.app/dashboard")
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
