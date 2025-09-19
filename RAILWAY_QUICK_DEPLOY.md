# 🚄 Railway 快速部署指南

## 🚀 部署步骤

### 1. 连接到Railway
1. 访问 [railway.app](https://railway.app)
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"

### 2. 选择仓库
- 如果还没有GitHub仓库，先创建一个
- 推送这个项目到GitHub
- 在Railway中选择你的仓库

### 3. 配置环境变量
在Railway项目设置中添加以下环境变量：

```
OPENROUTER_API_KEY=your_openrouter_key_here
ADMIN_TOKEN=admin123
DATABASE_URL=sqlite:///./metaweb.db
```

### 4. 自动部署
Railway会自动检测到配置文件并开始部署。

## 📁 重要文件说明

- **`railway.json`** - Railway配置文件
- **`Procfile`** - 启动命令
- **`requirements.txt`** - Python依赖
- **`start_server.py`** - 启动脚本（已适配Railway）

## 🔄 更新部署

每次你想更新应用时，只需：

```bash
git add .
git commit -m "Update: 描述你的更改"
git push origin main
```

Railway会自动重新部署！

## 🌐 访问应用

部署成功后，Railway会提供一个URL，类似：
`https://metaweb-production-xxxx.up.railway.app`

### 主要页面
- **首页**: `/`
- **AI配置管理**: `/admin/model-config`
- **设置向导**: `/setup`
- **API文档**: `/docs`

## 🔧 Railway特性

✅ **自动HTTPS** - 免费SSL证书  
✅ **全球CDN** - 快速访问  
✅ **自动扩容** - 根据流量调整  
✅ **零配置部署** - 检测框架自动配置  
✅ **持续部署** - Git推送自动更新  
✅ **环境变量管理** - 安全的配置管理  
✅ **日志监控** - 实时查看应用日志  

## 💰 费用

- **Hobby Plan**: $5/月，包含充足的资源
- **免费试用**: 新用户有免费额度
- **按使用量计费**: 只为实际使用的资源付费

## 🛠️ 故障排除

### 部署失败
1. 检查Railway部署日志
2. 确保requirements.txt包含所有依赖
3. 检查环境变量是否正确设置

### 应用无法访问
1. 确认部署状态为"Active"
2. 检查应用日志中的错误
3. 验证环境变量配置

### API错误
1. 检查OPENROUTER_API_KEY是否正确
2. 确认API密钥有足够余额
3. 查看应用日志中的详细错误

## 📊 监控

Railway提供：
- **实时日志** - 查看应用输出
- **资源使用** - CPU、内存、网络监控
- **部署历史** - 查看所有部署记录
- **健康检查** - 自动检测应用状态

## 🔒 安全建议

1. **更改默认密码**
   ```
   ADMIN_TOKEN=your_secure_password
   ```

2. **使用强API密钥**
   - 定期轮换API密钥
   - 不要在代码中硬编码

3. **监控使用量**
   - 定期检查API使用量
   - 设置使用量警报
