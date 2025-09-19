# Railway 简易部署指南

## 准备工作
- macOS 或 Linux（已安装 Python 3.9+）
- 可访问 [Railway](https://railway.app) 与 [OpenRouter](https://openrouter.ai) 的网络
- 一个有效的 OpenRouter API Key

> **提示**：脚本会尝试自动安装 Railway CLI。如果机器缺少 `npm` 或 `brew`，请提前手动安装 Railway CLI，或确保可以通过 `curl` 安装。

## 一键部署步骤
1. **拉取/更新代码**，确保本仓库位于 `/Volumes/Additional/Metaweb/`。
2. **执行脚本**：
   ```bash
   cd /Volumes/Additional/Metaweb
   python3 deploy_to_railway.py
   ```
3. **按照提示完成登录**：首次运行会打开 Railway CLI 登录流程。
4. **确认/命名项目**：脚本会自动创建新的 Railway 项目（可自定义名称）。
5. **输入 OpenRouter API Key**：用于下游推理请求。
6. 部署完成后，脚本会尝试为 `openwebui` 服务生成域名，并输出访问链接。

## 部署细节
- 部署使用 `openwebui/railway.json`，直接调用上游 Open WebUI Dockerfile。
- 默认环境变量：
  - `OPENAI_API_BASE_URL=https://openrouter.ai/api/v1`
  - `OPENAI_API_KEY=<运行时输入>`
  - `WEBUI_SECRET_KEY=<自动生成>`
  - `WEBUI_AUTH=False`
  - `PORT=8080`
  - `HOST=0.0.0.0`
- 健康检查路径：`/health`
- 重启策略：`ON_FAILURE`，最大重试 10 次

## 验证部署
- 访问脚本输出的 Railway 域名，或在 Railway 控制台的 **Deployments** 查看状态。
- 如需查看日志：
  ```bash
  railway logs --service openwebui
  ```

## 常见问题
| 问题 | 处理办法 |
| --- | --- |
| CLI 安装失败 | 按提示手动安装：`npm install -g @railway/cli` 或 `brew install railway` |
| 登录卡住 | 重新执行脚本；或运行 `railway login` 单独登录 |
| API Key 无效 | 确认 OpenRouter Key 可用；在 Railway 控制台更新 `OPENAI_API_KEY` |
| 域名未生成 | 运行 `railway domain --service openwebui` 或在控制台 -> Domains 手动创建 |

## 下一步
- 在 Railway 控制台绑定自定义域名
- 根据需要扩展环境变量（如 `ENABLE_SIGNUP`、`WEBUI_NAME` 等）
- 将项目导入 GitHub 并配置 Railway 自动部署
