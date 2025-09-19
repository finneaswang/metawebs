# 🚄 Railway 部署指南

## 快速部署到Railway

### 方法1: GitHub连接部署 (推荐)

1. **推送代码到GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/metaweb.git
   git push -u origin main
   ```

2. **在Railway上部署**
   - 访问 [railway.app](https://railway.app)
   - 点击 "Deploy from GitHub repo"
   - 选择你的Metaweb仓库
   - Railway会自动检测并部署

3. **设置环境变量**
   在Railway项目设置中添加：
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   ADMIN_TOKEN=your_admin_password
   DATABASE_URL=sqlite:///./metaweb.db
   ```

### 方法2: Railway CLI部署

1. **安装Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **登录Railway**
   ```bash
   railway login
   ```

3. **初始化项目**
   ```bash
   railway init
   ```

4. **部署**
   ```bash
   railway up
   ```

## 🔧 配置说明

### 必需的环境变量
- `OPENROUTER_API_KEY` - OpenRouter API密钥
- `ADMIN_TOKEN` - 管理员密码 (默认: admin123)

### 可选的环境变量
- `PORT` - 端口号 (Railway自动设置)
- `DATABASE_URL` - 数据库URL (默认使用SQLite)

## 🌐 访问应用

部署成功后，Railway会提供一个公网URL，格式类似：
`https://metaweb-production-xxxx.up.railway.app`

### 主要页面
- **首页**: `https://your-app.railway.app/`
- **AI聊天配置**: `https://your-app.railway.app/admin/model-config`
- **设置向导**: `https://your-app.railway.app/setup`
- **API文档**: `https://your-app.railway.app/docs`

## 🔒 安全设置

1. **更改默认管理员密码**
   在Railway环境变量中设置：
   ```
   ADMIN_TOKEN=your_secure_password_here
   ```

2. **API密钥安全**
   - 不要在代码中硬编码API密钥
   - 使用Railway的环境变量功能
   - 定期轮换API密钥

## 📊 监控和日志

- **查看日志**: Railway控制台 → 项目 → Deployments → 查看日志
- **监控状态**: Railway会自动监控应用健康状态
- **重启应用**: 在Railway控制台中可以手动重启

## 🚀 自动部署

设置后，每次推送到GitHub主分支时，Railway会自动重新部署应用。

## 💡 优化建议

1. **使用PostgreSQL**
   ```bash
   railway add postgresql
   ```
   然后更新DATABASE_URL环境变量

2. **设置自定义域名**
   在Railway项目设置中添加自定义域名

3. **启用HTTPS**
   Railway自动提供SSL证书

## 🔧 故障排除

### 部署失败
- 检查requirements.txt是否完整
- 查看部署日志中的错误信息
- 确保所有文件都已提交到Git

### 应用无法访问
- 检查PORT环境变量是否正确
- 确保应用监听0.0.0.0而不是localhost
- 查看Railway项目状态

### API错误
- 检查环境变量是否正确设置
- 确认API密钥有效且有足够余额
- 查看应用日志中的错误信息

## 📞 获取帮助

- Railway文档: https://docs.railway.app
- Railway社区: https://railway.app/discord
- 项目Issues: 在GitHub仓库中创建issue
