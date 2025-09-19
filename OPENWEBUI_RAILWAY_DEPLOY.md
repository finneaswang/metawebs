# 🚀 Open WebUI Railway 部署指南

## 方法一：一键自动部署（推荐）

运行自动部署脚本：

```bash
python3 deploy_openwebui_railway.py
```

脚本会自动：
- 安装Railway CLI
- 创建Open WebUI项目文件
- 部署到Railway
- 配置环境变量

## 方法二：手动部署

### 步骤1：创建新的Railway项目

1. 访问 [Railway](https://railway.app/new)
2. 选择 "Deploy from GitHub repo"
3. 连接到Open WebUI官方仓库：
   ```
   https://github.com/open-webui/open-webui
   ```

### 步骤2：配置环境变量

在Railway项目设置中添加以下环境变量：

```bash
OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=你的OpenRouter密钥
WEBUI_SECRET_KEY=openwebui-railway-secret-2024
WEBUI_AUTH=False
PORT=8080
```

### 步骤3：等待部署完成

Railway会自动：
- 构建Docker镜像
- 部署服务
- 分配域名

### 步骤4：访问Open WebUI

部署完成后，通过Railway提供的域名访问。

## 方法三：Fork仓库部署

### 步骤1：Fork Open WebUI仓库

1. 访问 https://github.com/open-webui/open-webui
2. 点击右上角 "Fork" 按钮
3. Fork到你的GitHub账号

### 步骤2：添加Railway配置文件

在你的Fork中添加 `railway.json`：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### 步骤3：在Railway中部署

1. 在Railway中创建新项目
2. 连接到你的Fork仓库
3. 设置环境变量（同方法二）
4. 部署

## 🔧 故障排除

### 如果部署失败：

1. **检查环境变量**：确保所有必需的环境变量都已设置
2. **检查日志**：在Railway控制台查看构建和运行日志
3. **端口配置**：确保PORT环境变量设置为8080
4. **内存限制**：Open WebUI可能需要较多内存，考虑升级Railway计划

### 常见问题：

**Q: 部署后无法访问？**
A: 检查Railway域名设置，确保服务正在运行

**Q: API调用失败？**
A: 验证OpenRouter API密钥是否正确设置

**Q: 界面显示异常？**
A: 清除浏览器缓存，或尝试无痕模式

## 🎯 推荐配置

```bash
# 生产环境推荐设置
WEBUI_AUTH=True                    # 启用认证
WEBUI_SECRET_KEY=你的随机密钥      # 强密钥
OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=你的密钥
DEFAULT_MODELS=openai/gpt-4o-mini,openai/gpt-4o
WEBUI_NAME="我的AI助手"
```

## 📞 获取帮助

如果遇到问题：
1. 查看Railway项目日志
2. 检查Open WebUI GitHub Issues
3. 确认OpenRouter API配额
