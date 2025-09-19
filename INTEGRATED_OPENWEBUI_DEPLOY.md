# 🚀 集成Open WebUI部署指南

## 概述

Open WebUI源码已成功集成到项目中，现在可以直接部署到Railway。

## 📁 项目结构

```
/Volumes/Additional/Metaweb/
├── openwebui/                    # Open WebUI完整源码
│   ├── Dockerfile               # Docker构建文件
│   ├── backend/                 # 后端Python代码
│   ├── src/                     # 前端Svelte代码
│   └── ...                      # 其他Open WebUI文件
├── deploy_integrated_openwebui.py # 自动部署脚本
├── railway-openwebui.json       # Railway配置文件
└── ...                          # 其他项目文件
```

## 🚀 部署方法

### 方法一：自动部署（推荐）

1. **运行部署脚本**:
   ```bash
   python3 deploy_integrated_openwebui.py
   ```

2. **输入OpenRouter API密钥**:
   - 访问 [OpenRouter](https://openrouter.ai/keys) 获取API密钥
   - 在脚本提示时输入密钥

3. **等待部署完成**:
   - 脚本会自动处理所有配置
   - 创建新的Railway项目
   - 设置环境变量
   - 部署并获取域名

### 方法二：手动部署

1. **进入Open WebUI目录**:
   ```bash
   cd openwebui
   ```

2. **初始化Git仓库**:
   ```bash
   git init
   git add .
   git commit -m "Initial Open WebUI for Railway"
   ```

3. **登录Railway**:
   ```bash
   railway login
   ```

4. **创建Railway项目**:
   ```bash
   railway init
   ```

5. **设置环境变量**:
   ```bash
   railway variables set OPENAI_API_BASE_URL="https://openrouter.ai/api/v1"
   railway variables set OPENAI_API_KEY="你的密钥"
   railway variables set WEBUI_SECRET_KEY="openwebui-railway-secret-2024"
   railway variables set WEBUI_AUTH="False"
   railway variables set PORT="8080"
   railway variables set HOST="0.0.0.0"
   ```

6. **部署**:
   ```bash
   railway up
   ```

## ⚙️ 环境变量配置

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_BASE_URL` | `https://openrouter.ai/api/v1` | OpenRouter API地址 |
| `OPENAI_API_KEY` | 你的密钥 | OpenRouter API密钥 |
| `WEBUI_SECRET_KEY` | `openwebui-railway-secret-2024` | WebUI加密密钥 |
| `WEBUI_AUTH` | `False` | 禁用认证（可选） |
| `WEBUI_NAME` | `Railway Open WebUI` | WebUI名称 |
| `PORT` | `8080` | 服务端口 |
| `HOST` | `0.0.0.0` | 监听地址 |
| `ENABLE_SIGNUP` | `True` | 允许注册 |
| `WORKERS` | `1` | 工作进程数 |
| `LOG_LEVEL` | `INFO` | 日志级别 |

## 🔧 故障排除

### 部署失败

1. **检查Railway CLI**:
   ```bash
   railway --version
   ```
   如果未安装，运行：
   ```bash
   # macOS
   brew install railway
   
   # Linux/WSL
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **检查API密钥**:
   - 确保OpenRouter API密钥有效
   - 检查账户余额

3. **检查Docker构建**:
   - Open WebUI使用Docker构建
   - 构建时间可能较长（10-15分钟）

### 访问问题

1. **等待部署完成**:
   - Railway构建可能需要时间
   - 在控制台查看构建日志

2. **检查域名**:
   ```bash
   railway domain
   ```

3. **查看日志**:
   ```bash
   railway logs
   ```

## 🎯 使用建议

1. **首次使用**:
   - 访问部署的域名
   - 创建管理员账户
   - 配置模型设置

2. **模型配置**:
   - 在设置中添加OpenRouter模型
   - 测试不同模型的响应

3. **数据持久化**:
   - Railway提供持久化存储
   - 聊天记录会自动保存

## 📞 获取帮助

- **Railway控制台**: https://railway.app/dashboard
- **Open WebUI文档**: https://docs.openwebui.com
- **OpenRouter文档**: https://openrouter.ai/docs

## 🎉 完成！

部署成功后，你将拥有一个完全功能的Open WebUI实例，运行在Railway云平台上，支持多种AI模型和完整的聊天功能。
