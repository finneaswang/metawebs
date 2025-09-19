# 🤖 Codex提示词：Railway Open WebUI部署

## 任务描述

你是一个专业的全栈开发工程师，需要帮助用户将已下载的Open WebUI源码部署到Railway平台。用户已经有了完整的Open WebUI源码在项目的`openwebui`文件夹中，现在需要你创建一个可以直接在Railway上运行的完整解决方案。

## 项目背景

- **项目位置**: `/Volumes/Additional/Metaweb/`
- **Open WebUI源码位置**: `/Volumes/Additional/Metaweb/openwebui/` (完整的官方源码)
- **目标平台**: Railway (容器化部署平台)
- **API提供商**: OpenRouter (https://openrouter.ai/api/v1)
- **部署要求**: 一键部署，自动配置，生产就绪

## 技术栈

- **Frontend**: Svelte + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: SQLite (Railway提供持久化存储)
- **Container**: Docker (使用Open WebUI原生Dockerfile)
- **Deployment**: Railway + GitHub集成

## 需要你完成的任务

### 1. 创建Railway部署配置

创建`railway.json`文件，包含：
- Docker构建配置
- 环境变量定义
- 健康检查设置
- 重启策略

### 2. 优化Dockerfile（如果需要）

检查并优化`openwebui/Dockerfile`以适配Railway环境：
- 端口配置 (Railway使用PORT环境变量)
- 启动命令优化
- 环境变量处理
- 构建优化

### 3. 创建环境变量配置

设置Railway所需的环境变量：
```bash
OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=用户的OpenRouter密钥
WEBUI_SECRET_KEY=安全密钥
WEBUI_AUTH=False
PORT=8080
HOST=0.0.0.0
WEBUI_NAME=Railway Open WebUI
```

### 4. 创建自动部署脚本

创建`deploy_to_railway.py`脚本，功能包括：
- 检查Railway CLI
- 自动安装Railway CLI（如果需要）
- 登录Railway
- 创建新项目
- 设置环境变量
- 部署应用
- 获取访问域名

### 5. 创建用户指南

创建简洁的`RAILWAY_DEPLOY_GUIDE.md`，包含：
- 前置要求
- 一键部署步骤
- 手动部署步骤
- 故障排除
- 访问说明

### 6. 集成到现有系统

修改现有的FastAPI应用(`app/main.py`)，添加：
- 新的路由`/openwebui-deploy`
- 部署状态检查
- 部署指导页面

## 技术要求

### Railway特定配置
- 使用`PORT`环境变量（Railway动态分配）
- 配置健康检查路径`/health`
- 设置合适的构建超时
- 配置重启策略

### 安全要求
- 环境变量加密存储
- API密钥安全处理
- 生产环境优化

### 性能要求
- Docker构建优化
- 启动时间优化
- 内存使用优化

## 预期输出

### 文件结构
```
/Volumes/Additional/Metaweb/
├── openwebui/                    # 现有的Open WebUI源码
│   ├── Dockerfile               # 可能需要优化
│   ├── railway.json             # 新增：Railway配置
│   └── ...                      # 其他Open WebUI文件
├── deploy_to_railway.py         # 新增：自动部署脚本
├── RAILWAY_DEPLOY_GUIDE.md      # 新增：部署指南
└── app/main.py                  # 修改：添加新路由
```

### 部署流程
1. 用户运行：`python3 deploy_to_railway.py`
2. 脚本自动处理所有配置
3. 创建Railway项目
4. 设置环境变量
5. 部署并获取域名
6. 用户可以直接访问Open WebUI

## 示例命令

用户应该能够通过以下简单命令完成部署：

```bash
# 方法1：自动部署
python3 deploy_to_railway.py

# 方法2：手动部署
cd openwebui
railway login
railway init
railway up
```

## 成功标准

- ✅ 用户可以一键部署Open WebUI到Railway
- ✅ 部署的Open WebUI功能完整（聊天、模型切换、设置等）
- ✅ 支持OpenRouter API集成
- ✅ 数据持久化正常工作
- ✅ 域名访问正常
- ✅ 生产环境稳定运行

## 注意事项

1. **保持原有功能**: 不要破坏现有的AI管理系统
2. **Railway限制**: 注意Railway的构建时间和资源限制
3. **环境变量**: 敏感信息通过环境变量管理
4. **错误处理**: 提供清晰的错误信息和解决方案
5. **文档完整**: 确保用户能够轻松跟随指南

## 开始编码

请基于以上要求，创建完整的Railway部署解决方案。重点关注：
- 自动化程度（用户操作越少越好）
- 错误处理（提供清晰的错误信息）
- 文档质量（让非技术用户也能理解）
- 生产就绪（稳定、安全、高性能）

开始吧！🚀
