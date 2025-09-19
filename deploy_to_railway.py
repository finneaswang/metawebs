#!/usr/bin/env python3
"""
一键部署到Railway的脚本
"""
import os
import sys
import subprocess
import json

def check_git():
    """检查Git是否已初始化"""
    return os.path.exists('.git')

def check_railway_cli():
    """检查Railway CLI是否已安装"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_railway_cli():
    """安装Railway CLI"""
    print("📦 安装Railway CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ Railway CLI安装失败")
        print("请手动安装: npm install -g @railway/cli")
        return False
    except FileNotFoundError:
        print("❌ 需要先安装Node.js和npm")
        print("请访问: https://nodejs.org")
        return False

def init_git():
    """初始化Git仓库"""
    print("📁 初始化Git仓库...")
    try:
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit for Railway deployment'], check=True)
        print("✅ Git仓库初始化成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git初始化失败: {e}")
        return False

def railway_login():
    """Railway登录"""
    print("🔐 Railway登录...")
    try:
        subprocess.run(['railway', 'login'], check=True)
        print("✅ Railway登录成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ Railway登录失败")
        return False

def railway_init():
    """初始化Railway项目"""
    print("🚄 初始化Railway项目...")
    try:
        subprocess.run(['railway', 'init'], check=True)
        print("✅ Railway项目初始化成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ Railway项目初始化失败")
        return False

def set_environment_variables():
    """设置环境变量"""
    print("🔧 设置环境变量...")
    
    # 获取用户输入
    openrouter_key = input("请输入OpenRouter API密钥 (回车跳过): ").strip()
    admin_token = input("请输入管理员密码 (回车使用默认: admin123): ").strip() or "admin123"
    
    env_vars = [
        ('ADMIN_TOKEN', admin_token),
        ('DATABASE_URL', 'sqlite:///./metaweb.db')
    ]
    
    if openrouter_key:
        env_vars.append(('OPENROUTER_API_KEY', openrouter_key))
    
    try:
        for key, value in env_vars:
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
            print(f"✅ 设置环境变量: {key}")
        return True
    except subprocess.CalledProcessError:
        print("❌ 环境变量设置失败")
        return False

def deploy():
    """部署到Railway"""
    print("🚀 部署到Railway...")
    try:
        result = subprocess.run(['railway', 'up'], capture_output=True, text=True, check=True)
        print("✅ 部署成功!")
        
        # 获取部署URL
        try:
            url_result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
            if url_result.returncode == 0 and url_result.stdout.strip():
                print(f"🌐 应用URL: {url_result.stdout.strip()}")
            else:
                print("📋 部署完成，请在Railway控制台查看应用URL")
        except:
            print("📋 部署完成，请在Railway控制台查看应用URL")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失败: {e}")
        print("请检查Railway控制台的错误日志")
        return False

def main():
    print("🚄 Railway 一键部署脚本")
    print("=" * 40)
    
    # 检查当前目录
    if not os.path.exists('requirements.txt'):
        print("❌ 请在Metaweb项目根目录运行此脚本")
        return
    
    # 1. 检查并安装Railway CLI
    if not check_railway_cli():
        print("⚠️  Railway CLI未安装")
        if input("是否现在安装? (y/N): ").lower() == 'y':
            if not install_railway_cli():
                return
        else:
            print("❌ 需要Railway CLI才能继续")
            return
    else:
        print("✅ Railway CLI已安装")
    
    # 2. 初始化Git（如果需要）
    if not check_git():
        if not init_git():
            return
    else:
        print("✅ Git仓库已存在")
    
    # 3. Railway登录
    print("\n📋 接下来需要登录Railway...")
    input("按回车键继续...")
    if not railway_login():
        return
    
    # 4. 初始化Railway项目
    if not railway_init():
        return
    
    # 5. 设置环境变量
    if not set_environment_variables():
        return
    
    # 6. 部署
    if not deploy():
        return
    
    print("\n" + "=" * 40)
    print("🎉 部署完成!")
    print("📋 接下来你可以:")
    print("  • 访问Railway控制台查看应用状态")
    print("  • 在环境变量中添加更多API密钥")
    print("  • 设置自定义域名")
    print("  • 查看应用日志")
    print("=" * 40)

if __name__ == "__main__":
    main()
