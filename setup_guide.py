#!/usr/bin/env python3
"""
Open WebUI 完整设置引导程序
"""
import os
import sys
import time
import webbrowser
import subprocess
from urllib.parse import urlparse

def print_header():
    """打印欢迎头部"""
    print("=" * 60)
    print("🚀 Open WebUI 设置引导程序")
    print("   让我们一步步配置你的AI聊天界面")
    print("=" * 60)
    print()

def check_container_status():
    """检查容器状态"""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=open-webui'], 
                              capture_output=True, text=True)
        if 'open-webui' in result.stdout:
            return True, "运行中"
        else:
            # 检查是否存在但已停止
            result = subprocess.run(['docker', 'ps', '-a', '--filter', 'name=open-webui'], 
                                  capture_output=True, text=True)
            if 'open-webui' in result.stdout:
                return False, "已停止"
            else:
                return False, "未创建"
    except:
        return False, "Docker不可用"

def wait_for_service(url, max_attempts=30):
    """等待服务启动"""
    print(f"⏳ 等待服务启动... (最多等待{max_attempts}秒)")
    
    for i in range(max_attempts):
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=2)
            return True
        except:
            print(f"   尝试 {i+1}/{max_attempts}...", end='\r')
            time.sleep(1)
    
    return False

def setup_api_keys():
    """设置API密钥引导"""
    print("🔑 API密钥配置")
    print("-" * 30)
    
    current_openrouter = os.environ.get('OPENROUTER_API_KEY', '')
    current_openai = os.environ.get('OPENAI_API_KEY', '')
    
    print(f"当前OpenRouter密钥: {'✅ 已设置' if current_openrouter else '❌ 未设置'}")
    print(f"当前OpenAI密钥: {'✅ 已设置' if current_openai else '❌ 未设置'}")
    print()
    
    if not current_openrouter and not current_openai:
        print("⚠️  建议设置至少一个API密钥以使用AI功能")
        print()
        print("选项1: OpenRouter (推荐)")
        print("  - 支持多种模型 (GPT-4, Claude, Mistral等)")
        print("  - 统一API接口")
        print("  - 获取密钥: https://openrouter.ai/keys")
        print()
        print("选项2: OpenAI")
        print("  - 官方GPT模型")
        print("  - 获取密钥: https://platform.openai.com/api-keys")
        print()
        
        choice = input("是否现在设置API密钥? (y/N): ").lower().strip()
        if choice == 'y':
            setup_keys_interactive()
    
    return True

def setup_keys_interactive():
    """交互式设置密钥"""
    print("\n📝 交互式密钥设置")
    print("-" * 20)
    
    # OpenRouter密钥
    openrouter_key = input("请输入OpenRouter API密钥 (回车跳过): ").strip()
    if openrouter_key:
        os.environ['OPENROUTER_API_KEY'] = openrouter_key
        print("✅ OpenRouter密钥已设置")
    
    # OpenAI密钥
    openai_key = input("请输入OpenAI API密钥 (回车跳过): ").strip()
    if openai_key:
        os.environ['OPENAI_API_KEY'] = openai_key
        print("✅ OpenAI密钥已设置")
    
    if openrouter_key or openai_key:
        print("\n🔄 需要重启容器以应用新的API密钥")
        restart = input("是否现在重启? (Y/n): ").lower().strip()
        if restart != 'n':
            restart_container_with_keys(openrouter_key, openai_key)

def restart_container_with_keys(openrouter_key="", openai_key=""):
    """使用新密钥重启容器"""
    print("\n🔄 重启容器...")
    
    try:
        # 停止并删除旧容器
        subprocess.run(['docker', 'stop', 'open-webui'], capture_output=True)
        subprocess.run(['docker', 'rm', 'open-webui'], capture_output=True)
        
        # 构建新的Docker命令
        docker_cmd = [
            'docker', 'run', '-d',
            '--name', 'open-webui',
            '-p', '3001:8080',
            '--restart', 'unless-stopped',
            '-v', 'open-webui:/app/backend/data'
        ]
        
        # 添加环境变量
        if openrouter_key:
            docker_cmd.extend(['-e', f'OPENROUTER_API_KEY={openrouter_key}'])
        if openai_key:
            docker_cmd.extend(['-e', f'OPENAI_API_KEY={openai_key}'])
        
        docker_cmd.append('ghcr.io/open-webui/open-webui:main')
        
        # 启动新容器
        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 容器重启成功!")
            return True
        else:
            print(f"❌ 重启失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 重启过程出错: {e}")
        return False

def first_time_setup_guide():
    """首次使用设置指南"""
    print("🎯 首次使用指南")
    print("-" * 20)
    print("1. 创建管理员账户")
    print("   - 首次访问时会要求创建管理员账户")
    print("   - 设置用户名和密码")
    print()
    print("2. 配置模型设置")
    print("   - 点击右上角设置图标 ⚙️")
    print("   - 选择'连接'选项卡")
    print("   - 添加API密钥 (如果之前未设置)")
    print()
    print("3. 选择AI模型")
    print("   - 在聊天界面顶部选择模型")
    print("   - 推荐: GPT-4o Mini (快速且经济)")
    print()
    print("4. 调整参数")
    print("   - Temperature: 控制创造性 (0-1)")
    print("   - Max Tokens: 控制回复长度")
    print("   - System Prompt: 设置AI角色")
    print()

def open_browser_guide():
    """浏览器打开指南"""
    url = "http://localhost:3001"
    
    print("🌐 打开浏览器")
    print("-" * 15)
    print(f"访问地址: {url}")
    
    try_open = input("是否现在自动打开浏览器? (Y/n): ").lower().strip()
    if try_open != 'n':
        try:
            webbrowser.open(url)
            print("✅ 浏览器已打开")
        except:
            print("❌ 无法自动打开浏览器，请手动访问上述地址")
    
    print("\n💡 如果页面无法加载，请等待几秒钟后刷新")

def show_usage_tips():
    """显示使用技巧"""
    print("\n💡 使用技巧")
    print("-" * 15)
    print("• 💬 聊天: 直接输入消息开始对话")
    print("• ⚙️ 设置: 点击右上角齿轮图标")
    print("• 🔄 新对话: 点击'新对话'按钮")
    print("• 📁 历史: 左侧面板查看聊天历史")
    print("• 🎨 主题: 设置中可切换深色/浅色模式")
    print("• 📤 导出: 可导出聊天记录")
    print("• 🔌 插件: 支持各种扩展功能")

def show_troubleshooting():
    """显示故障排除"""
    print("\n🔧 故障排除")
    print("-" * 15)
    print("• 页面无法访问:")
    print("  - 检查容器状态: docker ps")
    print("  - 查看日志: docker logs open-webui")
    print("  - 重启容器: docker restart open-webui")
    print()
    print("• API错误:")
    print("  - 检查API密钥是否正确")
    print("  - 确认账户有足够余额")
    print("  - 在设置中重新配置密钥")
    print()
    print("• 端口冲突:")
    print("  - 停止容器: docker stop open-webui")
    print("  - 更换端口重新运行")

def main():
    """主程序"""
    print_header()
    
    # 1. 检查容器状态
    print("📋 步骤 1: 检查服务状态")
    is_running, status = check_container_status()
    print(f"   容器状态: {status}")
    
    if not is_running:
        print("❌ 服务未运行，请先运行部署脚本:")
        print("   python3 deploy_openwebui.py")
        return
    
    print("✅ 服务正在运行")
    print()
    
    # 2. 等待服务启动
    print("📋 步骤 2: 等待服务就绪")
    if wait_for_service("http://localhost:3001"):
        print("✅ 服务已就绪")
    else:
        print("⚠️  服务可能还在启动中，请稍后手动访问")
    print()
    
    # 3. API密钥设置
    print("📋 步骤 3: API密钥配置")
    setup_api_keys()
    print()
    
    # 4. 首次使用指南
    print("📋 步骤 4: 使用指南")
    first_time_setup_guide()
    
    # 5. 打开浏览器
    print("📋 步骤 5: 访问应用")
    open_browser_guide()
    
    # 6. 使用技巧
    show_usage_tips()
    
    # 7. 故障排除
    show_troubleshooting()
    
    print("\n" + "=" * 60)
    print("🎉 设置完成！享受你的AI聊天体验!")
    print("=" * 60)

if __name__ == "__main__":
    main()
