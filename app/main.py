import json
import time
from typing import Dict, Any

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.openrouter_demo import ask_model
from app.model_config import (
    ModelConfigOut,
    SessionLocal,
    get_active_config_row,
    init_tables,
    router as model_config_router,
)

app = FastAPI(title="AI模型管理系统")

AVAILABLE_MODELS = [
    {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI"},
    {"id": "openai/gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
    {"id": "anthropic/claude-3-haiku", "name": "Claude 3 Haiku", "provider": "Anthropic"},
    {"id": "anthropic/claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
    {"id": "mistralai/mistral-7b-instruct", "name": "Mistral 7B", "provider": "Mistral"},
    {"id": "google/gemini-pro", "name": "Gemini Pro", "provider": "Google"},
]

DEFAULT_ACTIVE_CONFIG: Dict[str, Any] = {
    "id": None,
    "version": 0,
    "model": "openai/gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "",
    "is_active": False,
    "created_at": None,
    "last_updated": None,
}


@app.on_event("startup")
def on_startup():
    init_tables()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"INFO: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Time: {process_time:.4f}s"
    )
    return response


@app.get("/", response_class=HTMLResponse)
async def index():
    """首页 - AI管理中心"""
    with open("/Volumes/Additional/Metaweb/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.post("/evaluate")
def evaluate(input_text: str = Body(..., embed=True)):
    feedback = ask_model(f"请帮我评价这段学习回答: {input_text}")
    return {"feedback": feedback}


@app.post("/chat")
def chat(
    message: str = Body(..., embed=True),
    model: str = Body(None),
    temperature: float = Body(None),
    max_tokens: int = Body(None),
    system_prompt: str = Body(None)
):
    """AI对话接口，支持自定义参数"""
    try:
        # 如果没有指定参数，使用当前活跃配置
        if not all([model, temperature is not None, max_tokens, system_prompt is not None]):
            active_config = serialize_active_config()
            model = model or active_config.get("model", "openai/gpt-4o-mini")
            temperature = temperature if temperature is not None else active_config.get("temperature", 0.7)
            max_tokens = max_tokens or active_config.get("max_tokens", 1000)
            system_prompt = system_prompt if system_prompt is not None else active_config.get("system_prompt", "")
        
        # 构建完整的提示词
        if system_prompt:
            full_message = f"System: {system_prompt}\n\nUser: {message}"
        else:
            full_message = message
            
        response = ask_model(
            full_message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "response": response,
            "config_used": {
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "system_prompt": system_prompt
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def serialize_active_config() -> Dict[str, Any]:
    with SessionLocal() as db:
        row = get_active_config_row(db)

    if not row:
        return dict(DEFAULT_ACTIVE_CONFIG)

    out = ModelConfigOut.from_orm_row(row)
    data = out.model_dump() if hasattr(out, "model_dump") else out.dict()
    data["last_updated"] = (
        out.created_at.isoformat() if out.created_at else None
    )
    return data


@app.get("/admin/model-config", response_class=HTMLResponse)
async def model_config_page():
    """AI模型配置管理页面"""
    with open("/Volumes/Additional/Metaweb/app/model_config_page.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/test", response_class=HTMLResponse)
async def test_page():
    """测试页面"""
    with open("/Volumes/Additional/Metaweb/app/test_page.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/setup", response_class=HTMLResponse)
async def setup_guide():
    """Open WebUI 设置引导页面"""
    with open("/Volumes/Additional/Metaweb/onboarding.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/admin", response_class=HTMLResponse)
async def admin_interface():
    models_json = json.dumps(AVAILABLE_MODELS, ensure_ascii=False)
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI模型管理</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 16px rgba(15,23,42,0.08); }}
            h1 {{ color: #1f2937; text-align: center; margin-bottom: 32px; }}
            h3 {{ margin-bottom: 12px; color: #111827; }}
            .section {{ margin-bottom: 32px; }}
            .token {{ display: flex; flex-direction: column; gap: 8px; }}
            .token input {{ padding: 10px 14px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; }}
            .token small {{ color: #6b7280; }}
            .current-config, .history {{ background: #f9fafb; padding: 18px; border-radius: 10px; border: 1px solid #e5e7eb; }}
            .form-group {{ margin-bottom: 20px; }}
            label {{ display: block; margin-bottom: 6px; font-weight: 500; color: #374151; }}
            input, select, textarea {{ width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; }}
            textarea {{ height: 120px; resize: vertical; }}
            button {{ background: #2563eb; color: white; padding: 11px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 15px; transition: background 0.15s ease; }}
            button:hover {{ background: #1d4ed8; }}
            button[disabled] {{ background: #9ca3af; cursor: not-allowed; }}
            .status {{ margin-top: 16px; padding: 12px; border-radius: 8px; font-size: 14px; display: none; }}
            .status.success {{ display: block; background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}
            .status.error {{ display: block; background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }}
            .status.info {{ display: block; background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }}
            .config-item {{ margin-bottom: 8px; }}
            .config-label {{ font-weight: 600; color: #374151; display: inline-block; width: 96px; }}
            .config-value {{ color: #4b5563; }}
            .muted {{ color: #9ca3af; }}
            .history-item {{ display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-radius: 10px; border: 1px solid #e5e7eb; margin-bottom: 12px; background: white; }}
            .history-item.active {{ border-color: #2563eb; box-shadow: 0 0 0 2px rgba(37,99,235,0.15); }}
            .history-title {{ font-weight: 600; color: #1f2937; margin-bottom: 4px; }}
            .history-meta {{ font-size: 13px; color: #6b7280; margin-bottom: 6px; }}
            .history-detail {{ font-size: 13px; color: #4b5563; }}
            .history-actions {{ display: flex; gap: 8px; align-items: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI模型管理系统</h1>

            <section class="section token">
                <h3>管理员口令</h3>
                <input type="password" id="adminToken" placeholder="请输入 x-admin-token" autocomplete="off" />
                <small>保存、发布等操作会在请求头中附带 x-admin-token。</small>
            </section>

            <section class="section current-config">
                <h3>当前生效配置</h3>
                <div id="currentConfig" class="muted">加载中...</div>
            </section>

            <section class="section">
                <h3>新建配置版本</h3>
                <form id="configForm">
                    <div class="form-group">
                        <label for="model">选择AI模型</label>
                        <select id="model" name="model"></select>
                    </div>

                    <div class="form-group">
                        <label for="temperature">创造性 (Temperature): <span id="tempValue">0.7</span></label>
                        <input type="range" id="temperature" name="temperature" min="0" max="1" step="0.05" value="0.7">
                    </div>

                    <div class="form-group">
                        <label for="max_tokens">最大回复长度</label>
                        <input type="number" id="max_tokens" name="max_tokens" min="100" max="32768" value="1000">
                    </div>

                    <div class="form-group">
                        <label for="system_prompt">系统提示词 (可选)</label>
                        <textarea id="system_prompt" name="system_prompt" placeholder="例如: 你是一个专业的编程助手..."></textarea>
                    </div>

                    <button type="submit">💾 保存新版本</button>
                </form>
            </section>

            <section class="section history">
                <h3>历史版本</h3>
                <div id="historyList" class="muted">加载中...</div>
            </section>

            <div id="status" class="status"></div>
        </div>

        <script>
            const AVAILABLE_MODELS = {models_json};
            let adminToken = '';

            const statusBox = document.getElementById('status');
            const currentConfigEl = document.getElementById('currentConfig');
            const historyList = document.getElementById('historyList');
            const temperatureInput = document.getElementById('temperature');
            const tempValue = document.getElementById('tempValue');

            function setStatus(type, message) {{
                statusBox.textContent = message;
                statusBox.className = 'status ' + type;
            }}

            function clearStatus() {{
                statusBox.textContent = '';
                statusBox.className = 'status';
            }}

            function renderCurrentConfig(config) {{
                if (!config) {{
                    currentConfigEl.innerHTML = '<p class="muted">当前没有生效配置，系统会使用默认参数。</p>';
                    return;
                }}

                const lastUpdated = config.last_updated ? new Date(config.last_updated).toLocaleString('zh-CN') : '未知';
                currentConfigEl.innerHTML = [
                    '<div class="config-item"><span class="config-label">模型:</span><span class="config-value">' + config.model + '</span></div>',
                    '<div class="config-item"><span class="config-label">温度:</span><span class="config-value">' + config.temperature + '</span></div>',
                    '<div class="config-item"><span class="config-label">最大长度:</span><span class="config-value">' + config.max_tokens + '</span></div>',
                    '<div class="config-item"><span class="config-label">系统提示:</span><span class="config-value">' + (config.system_prompt || '无') + '</span></div>',
                    '<div class="config-item"><span class="config-label">最后更新:</span><span class="config-value">' + lastUpdated + '</span></div>'
                ].join('');
            }}

            async function loadActiveConfig() {{
                try {{
                    const response = await fetch('/config/active');
                    if (!response.ok) throw new Error('获取当前配置失败');
                    const config = await response.json();
                    renderCurrentConfig(config);
                }} catch (error) {{
                    console.error('加载当前配置失败:', error);
                    setStatus('error', error.message);
                }}
            }}

            async function loadHistory() {{
                try {{
                    const response = await fetch('/config/history?limit=20');
                    if (!response.ok) throw new Error('获取历史版本失败');
                    const items = await response.json();
                    if (!items.length) {{
                        historyList.innerHTML = '<p class="muted">暂无历史版本，可先创建配置。</p>';
                        return;
                    }}

                    historyList.innerHTML = items.map((item) => {{
                        const createdAt = item.created_at ? new Date(item.created_at).toLocaleString('zh-CN') : '未知';
                        return [
                            '<div class="history-item ' + (item.is_active ? 'active' : '') + '">',
                                '<div>',
                                    '<div class="history-title">版本 V' + item.version + '</div>',
                                    '<div class="history-meta">创建时间: ' + createdAt + '</div>',
                                    '<div class="history-detail">模型: ' + item.model + '</div>',
                                    '<div class="history-detail">温度: ' + item.temperature + ' | 最大长度: ' + item.max_tokens + '</div>',
                                '</div>',
                                '<div class="history-actions">',
                                    '<button data-action="publish" data-id="' + item.id + '" ' + (item.is_active ? 'disabled' : '') + '>' + (item.is_active ? '当前生效' : '发布') + '</button>',
                                '</div>',
                            '</div>'
                        ].join('');
                    }}).join('');
                }} catch (error) {{
                    console.error('加载历史失败:', error);
                    historyList.innerHTML = '<p class="muted">无法获取历史记录。</p>';
                    setStatus('error', error.message);
                }}
            }}

            async function createConfig(payload) {{
                if (!adminToken) {{
                    throw new Error('请先输入管理员口令');
                }}
                const response = await fetch('/config', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'x-admin-token': adminToken,
                    }},
                    body: JSON.stringify(payload),
                }});
                if (!response.ok) {{
                    const errorText = await response.text();
                    throw new Error(errorText || '创建配置失败');
                }}
                return response.json();
            }}

            document.getElementById('adminToken').addEventListener('input', (event) => {{
                adminToken = event.target.value.trim();
            }});

            temperatureInput.addEventListener('input', () => {{
                tempValue.textContent = temperatureInput.value;
            }});

            document.getElementById('configForm').addEventListener('submit', async (event) => {{
                event.preventDefault();
                clearStatus();

                const payload = {{
                    model: document.getElementById('model').value,
                    temperature: parseFloat(temperatureInput.value),
                    max_tokens: parseInt(document.getElementById('max_tokens').value, 10),
                    system_prompt: document.getElementById('system_prompt').value.trim(),
                }};

                try {{
                    const created = await createConfig(payload);
                    setStatus('success', '新配置已保存: 版本 V' + created.version + ' (ID: ' + created.id + ')，请在历史列表中发布。');
                    document.getElementById('configForm').reset();
                    temperatureInput.value = '0.7';
                    tempValue.textContent = '0.7';
                    await loadHistory();
                }} catch (error) {{
                    setStatus('error', error.message);
                }}
            }});

            historyList.addEventListener('click', async (event) => {{
                const button = event.target.closest('button[data-action="publish"]');
                if (!button) {{
                    return;
                }}
                if (!adminToken) {{
                    setStatus('error', '请先输入管理员口令');
                    return;
                }}

                const configId = button.dataset.id;
                const previousText = button.textContent;
                button.disabled = true;
                button.textContent = '发布中...';

                try {{
                    const response = await fetch('/config/' + configId + '/publish', {{
                        method: 'POST',
                        headers: {{ 'x-admin-token': adminToken }},
                    }});
                    if (!response.ok) {{
                        const errorText = await response.text();
                        throw new Error(errorText || '发布失败');
                    }}
                    setStatus('success', '配置发布成功');
                    await loadActiveConfig();
                    await loadHistory();
                }} catch (error) {{
                    setStatus('error', error.message);
                }} finally {{
                    button.disabled = false;
                    button.textContent = previousText;
                }}
            }});

            function init() {{
                const modelSelect = document.getElementById('model');
                modelSelect.innerHTML = AVAILABLE_MODELS.map((item) => (
                    '<option value="' + item.id + '">' + item.name + ' (' + item.provider + ')</option>'
                )).join('');
                modelSelect.value = 'openai/gpt-4o-mini';
                tempValue.textContent = temperatureInput.value;
                loadActiveConfig();
                loadHistory();
            }}

            init();
        </script>
    </body>
    </html>
    """


@app.get("/api/config")
async def get_config():
    return serialize_active_config()


@app.put("/api/config")
async def update_config():
    raise HTTPException(
        status_code=405,
        detail="该接口已废弃，请改用 /config 系列接口。",
    )


@app.get("/api/models")
async def get_available_models():
    return AVAILABLE_MODELS


app.include_router(model_config_router)
