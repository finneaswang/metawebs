# 🚀 Open WebUI 部署指南

## 方法1: Docker 部署 (推荐)

### 1. 确保Docker已启动
打开Docker Desktop应用

### 2. 运行以下命令
```bash
# 基础部署
docker run -d \
  --name open-webui \
  -p 3001:8080 \
  -v open-webui:/app/backend/data \
  ghcr.io/open-webui/open-webui:main

# 带API密钥的部署
docker run -d \
  --name open-webui \
  -p 3001:8080 \
  -e OPENAI_API_KEY=your_openai_key_here \
  -e OPENROUTER_API_KEY=your_openrouter_key_here \
  -v open-webui:/app/backend/data \
  ghcr.io/open-webui/open-webui:main
```

### 3. 访问应用
打开浏览器访问: http://localhost:3001

### 4. 检查状态
```bash
# 查看运行中的容器
docker ps

# 查看日志
docker logs open-webui

# 停止容器
docker stop open-webui

# 重启容器
docker start open-webui
```

## 方法2: pip 本地安装

### 1. 安装
```bash
pip install open-webui
```

### 2. 启动
```bash
open-webui serve --port 3001
```

### 3. 访问
http://localhost:3001

## 🔧 配置API密钥

### 在终端设置环境变量:
```bash
export OPENROUTER_API_KEY="your_openrouter_key_here"
export OPENAI_API_KEY="your_openai_key_here"
```

### 或在Open WebUI界面中设置:
1. 打开 http://localhost:3001
2. 点击设置 ⚙️
3. 在"连接"部分添加API密钥

## 🎯 功能特性

✅ 现代化聊天界面  
✅ 支持多种AI模型  
✅ 实时参数调整 (temperature, max_tokens等)  
✅ 聊天历史管理  
✅ 系统提示词设置  
✅ 响应流式输出  
✅ 文档上传和分析  

## 🔍 故障排除

### Docker相关问题:
- 确保Docker Desktop已启动
- 检查端口3001是否被占用: `lsof -i :3001`
- 更换端口: 将`-p 3001:8080`改为`-p 3002:8080`

### API密钥问题:
- 确保密钥格式正确
- 在Open WebUI设置中重新配置
- 检查密钥权限和余额

### 网络问题:
- 检查防火墙设置
- 尝试使用`http://127.0.0.1:3001`
- 清除浏览器缓存
