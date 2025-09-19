#!/usr/bin/env python3
"""Railway one-click deployment helper for Open WebUI."""

from __future__ import annotations

import json
import secrets
import shutil
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence

ROOT_DIR = Path(__file__).resolve().parent
OPENWEBUI_DIR = ROOT_DIR / "openwebui"
RAILWAY_CONFIG_PATH = OPENWEBUI_DIR / "railway.json"
DEFAULT_SERVICE_NAME = "openwebui"
DEFAULT_ENVIRONMENT = "production"


class CommandError(RuntimeError):
    """Raised when a shell command fails."""


def print_header() -> None:
    banner = textwrap.dedent(
        """
        🚄  Open WebUI Railway 部署向导
        ---------------------------------
        该脚本将自动：
          • 检查并安装 Railway CLI
          • 帮你登录并创建/关联项目
          • 设置 Open Router 所需环境变量
          • 使用 openwebui/Dockerfile 触发部署
        """
    ).strip()
    print(banner)
    print()


def run_command(
    cmd: Sequence[str],
    *,
    cwd: Optional[Path] = None,
    check: bool = True,
    silent: bool = False,
) -> subprocess.CompletedProcess:
    display = " ".join(cmd)
    prefix = f"[{cwd}] " if cwd else ""
    print(f"→ {prefix}{display}")
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise CommandError(f"命令不存在: {cmd[0]}") from exc

    if result.stdout and not silent:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print(result.stderr.strip())

    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "未知错误"
        raise CommandError(f"执行失败: {display}\n{message}")

    return result


def ensure_cli_available() -> None:
    if shutil.which("railway"):
        version = run_command(["railway", "--version"], silent=True, check=False)
        if version.stdout:
            print(f"✅ Railway CLI 已就绪: {version.stdout.strip()}")
        else:
            print("✅ Railway CLI 已安装")
        return

    print("🔧 Railway CLI 未安装，尝试自动安装...")
    install_commands = []
    if shutil.which("npm"):
        install_commands.append(["npm", "install", "-g", "@railway/cli"])
    if sys.platform == "darwin" and shutil.which("brew"):
        install_commands.append(["brew", "install", "railway"])
    install_commands.append(["bash", "-lc", "curl -fsSL https://railway.app/install.sh | sh"])

    for command in install_commands:
        try:
            run_command(command, check=True)
        except CommandError as err:
            print(f"⚠️ 尝试安装失败: {err}")
            continue
        if shutil.which("railway"):
            version = run_command(["railway", "--version"], silent=True, check=False)
            if version.stdout:
                print(f"✅ Railway CLI 已安装: {version.stdout.strip()}")
            else:
                print("✅ Railway CLI 安装成功")
            return

    raise CommandError(
        "无法自动安装 Railway CLI，请手动安装后重新运行脚本\n"
        "https://docs.railway.app/cli/installation"
    )


def ensure_logged_in() -> None:
    if _is_logged_in():
        return

    print("🔐 正在打开 Railway 登录流程...")
    run_command(["railway", "login"], check=True)
    if not _is_logged_in():
        raise CommandError("Railway 登录未完成，请重试")
    print("✅ Railway 登录成功")


def _is_logged_in() -> bool:
    result = run_command(["railway", "whoami"], check=False, silent=True)
    if result.returncode == 0 and result.stdout.strip():
        print(f"✅ 已登录账户: {result.stdout.strip()}")
        return True
    return False


def prompt(text: str, default: Optional[str] = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or (default or "")


def prompt_yes_no(question: str, default: bool = True) -> bool:
    default_txt = "Y/n" if default else "y/N"
    while True:
        value = input(f"{question} ({default_txt}): ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("请输入 y 或 n")


def load_status() -> Optional[Dict[str, object]]:
    result = run_command(["railway", "status", "--json"], cwd=OPENWEBUI_DIR, check=False, silent=True)
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def ensure_project_link(project_name: str) -> Dict[str, object]:
    status = load_status()
    if status:
        name = status.get("name") or status.get("project") or "未知项目"
        print(f"📌 当前目录已关联项目: {name}")
        reuse = prompt_yes_no("是否复用该项目?", default=True)
        if not reuse:
            run_command(["railway", "unlink"], cwd=OPENWEBUI_DIR, check=True)
            status = None

    if not status:
        print(f"🚀 创建新的 Railway 项目: {project_name}")
        run_command(["railway", "init", "--name", project_name], cwd=OPENWEBUI_DIR, check=True)
        status = load_status()
        if not status:
            raise CommandError("未能创建或链接 Railway 项目")
    return status


def ensure_service_link(service_name: str) -> Dict[str, object]:
    status = load_status() or {}
    edges: Iterable[Dict[str, object]] = status.get("services", {}).get("edges", [])  # type: ignore[arg-type]
    services = {edge.get("node", {}).get("name") for edge in edges if isinstance(edge, dict)}

    if service_name not in services:
        print(f"➕ 创建服务: {service_name}")
        try:
            run_command(["railway", "add", "--service", service_name], cwd=OPENWEBUI_DIR, check=True)
        except CommandError as err:
            if "already exists" not in str(err).lower():
                raise
            print("ℹ️ 服务已存在，跳过创建")
        status = load_status() or status

    run_command(["railway", "service", service_name], cwd=OPENWEBUI_DIR, check=True)
    refreshed = load_status()
    if not refreshed:
        raise CommandError("无法读取服务状态")
    return refreshed


def collect_env_vars() -> Dict[str, str]:
    print()
    print("⚙️ 配置环境变量")
    api_key = ""
    while not api_key:
        api_key = input("请输入 OpenRouter API Key (OPENAI_API_KEY): ").strip()
        if not api_key:
            print("API Key 不能为空")

    secret_key = secrets.token_urlsafe(32)
    print(f"🔑 已生成 WEBUI_SECRET_KEY: {secret_key}")

    return {
        "OPENAI_API_BASE_URL": "https://openrouter.ai/api/v1",
        "OPENAI_API_KEY": api_key,
        "WEBUI_SECRET_KEY": secret_key,
        "WEBUI_AUTH": "False",
        "PORT": "8080",
        "HOST": "0.0.0.0",
    }


def set_environment_variables(service_name: str, variables: Dict[str, str]) -> None:
    for key, value in variables.items():
        run_command(
            [
                "railway",
                "variables",
                "--service",
                service_name,
                "--set",
                f"{key}={value}",
                "--skip-deploys",
            ],
            cwd=OPENWEBUI_DIR,
            check=True,
        )
        print(f"  ✅ 已设置 {key}")


def deploy_service(service_name: str) -> None:
    print("🚢 正在部署 Open WebUI...")
    run_command(
        ["railway", "up", "--service", service_name, "--detach"],
        cwd=OPENWEBUI_DIR,
        check=True,
    )
    print("✅ Railway 已开始部署 (使用 openwebui/Dockerfile)")


def fetch_domain(service_name: str) -> Optional[str]:
    result = run_command(
        ["railway", "domain", "--service", service_name, "--json"],
        cwd=OPENWEBUI_DIR,
        check=False,
        silent=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    domain = payload.get("domain") or payload.get("hostname")
    if domain:
        print(f"🌐 分配的域名: https://{domain}")
    return domain if isinstance(domain, str) else None


def guard_environment() -> None:
    if not OPENWEBUI_DIR.exists():
        raise CommandError(f"未找到 openwebui 目录: {OPENWEBUI_DIR}")
    if not RAILWAY_CONFIG_PATH.exists():
        raise CommandError("缺少 openwebui/railway.json，请先生成配置文件")


def main() -> None:
    print_header()
    guard_environment()
    ensure_cli_available()
    ensure_logged_in()

    default_project_name = f"openwebui-{int(time.time())}"
    project_name = prompt("Railway 项目名称", default=default_project_name)
    status = ensure_project_link(project_name)

    if not status:
        raise CommandError("Railway 项目状态异常")

    status = ensure_service_link(DEFAULT_SERVICE_NAME)

    env_vars = collect_env_vars()
    set_environment_variables(DEFAULT_SERVICE_NAME, env_vars)
    deploy_service(DEFAULT_SERVICE_NAME)
    fetch_domain(DEFAULT_SERVICE_NAME)

    print()
    print("🎉 全部完成！")
    print("可以通过 Railway 控制台查看部署进度和日志。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ 已取消部署")
    except CommandError as error:
        print(f"❌ {error}")
        sys.exit(1)
