#!/usr/bin/env python3
"""
Open WebUI Deployment Script
"""
import os
import sys
import subprocess
import time

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            print(f"   {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    print("❌ Docker is not available")
    return False

def deploy_with_docker():
    """Deploy Open WebUI using Docker"""
    print("\n🐳 Deploying Open WebUI with Docker...")
    
    # Set environment variables
    env_vars = [
        f"OPENROUTER_API_KEY={os.environ.get('OPENROUTER_API_KEY', '')}",
        f"OPENAI_API_KEY={os.environ.get('OPENAI_API_KEY', '')}",
    ]
    
    # Docker command
    docker_cmd = [
        'docker', 'run', '-d',
        '--name', 'open-webui',
        '-p', '3001:8080',
        '--restart', 'unless-stopped'
    ]
    
    # Add environment variables
    for env_var in env_vars:
        if env_var.split('=')[1]:  # Only add if value is not empty
            docker_cmd.extend(['-e', env_var])
    
    # Add volume for data persistence
    docker_cmd.extend(['-v', 'open-webui:/app/backend/data'])
    
    # Add the image
    docker_cmd.append('ghcr.io/open-webui/open-webui:main')
    
    print(f"📋 Running: {' '.join(docker_cmd)}")
    
    try:
        # Remove existing container if it exists
        subprocess.run(['docker', 'rm', '-f', 'open-webui'], 
                      capture_output=True, text=True)
        
        # Run the new container
        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Open WebUI container started successfully!")
            print(f"📋 Container ID: {result.stdout.strip()}")
            print("🌐 Access URL: http://localhost:3001")
            
            # Wait a moment and check if container is running
            time.sleep(3)
            check_result = subprocess.run(['docker', 'ps', '--filter', 'name=open-webui'], 
                                        capture_output=True, text=True)
            if 'open-webui' in check_result.stdout:
                print("✅ Container is running properly")
                return True
            else:
                print("❌ Container may have stopped, checking logs...")
                logs = subprocess.run(['docker', 'logs', 'open-webui'], 
                                    capture_output=True, text=True)
                print(f"📋 Container logs:\n{logs.stdout}")
                return False
        else:
            print(f"❌ Failed to start container: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Docker deployment failed: {e}")
        return False

def deploy_local():
    """Deploy Open WebUI locally using pip"""
    print("\n🐍 Deploying Open WebUI locally with pip...")
    
    try:
        # Install open-webui
        print("📦 Installing open-webui...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'open-webui'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
        print("✅ Open WebUI installed successfully!")
        
        # Set environment variables
        os.environ['PORT'] = '3001'
        os.environ['HOST'] = '0.0.0.0'
        
        print("🚀 Starting Open WebUI server...")
        print("🌐 Access URL: http://localhost:3001")
        print("⚠️  Press Ctrl+C to stop the server")
        
        # Start the server
        subprocess.run([sys.executable, '-m', 'open_webui', 'serve', '--port', '3001'])
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Local deployment failed: {e}")
        return False

def main():
    print("🚀 Open WebUI Deployment Script")
    print("=" * 40)
    
    # Load configuration
    try:
        import openwebui_config
        print("✅ Configuration loaded")
    except ImportError:
        print("⚠️  Configuration file not found, using defaults")
    
    # Check API keys
    openrouter_key = os.environ.get('OPENROUTER_API_KEY', '')
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    
    if not openrouter_key and not openai_key:
        print("⚠️  Warning: No API keys found in environment variables")
        print("   Set OPENROUTER_API_KEY or OPENAI_API_KEY before running")
        print("   Example: export OPENROUTER_API_KEY='your_key_here'")
    
    # Try Docker first, then fall back to local
    if check_docker():
        if deploy_with_docker():
            return
        else:
            print("\n🔄 Docker deployment failed, trying local installation...")
    
    deploy_local()

if __name__ == "__main__":
    main()
