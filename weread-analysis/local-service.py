#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import webbrowser
from collections import deque
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ROOT_JSON = BASE_DIR / "all-books-details.json"
OUTPUT_JSON = OUTPUT_DIR / "all-books-details.json"
HTML_PATH = BASE_DIR / "index.html"
BUILD_SCRIPT = BASE_DIR / "build-library.py"
ANALYZE_SCRIPT = BASE_DIR / "analyze-shelf.py"
ENV_FILE = BASE_DIR / ".env"
SUMMARY_FILE = BASE_DIR / "last-sync-summary.json"
API_KEY_NAME = "WEREAD_API_KEY"


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_env_file() -> dict:
    """读取 .env 为 dict；不存在或解析失败则返回空。"""
    if not ENV_FILE.exists():
        return {}
    data: dict = {}
    try:
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                data[key] = value
    except Exception:
        return {}
    return data


def save_env_value(key: str, value: str) -> None:
    """以幂等方式把单个键写回 .env。"""
    existing = load_env_file()
    existing[key] = value
    lines = [f'{k}="{v}"' for k, v in existing.items()]
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_env_value(key: str) -> None:
    existing = load_env_file()
    if key in existing:
        existing.pop(key)
        if existing:
            ENV_FILE.write_text(
                "\n".join(f'{k}="{v}"' for k, v in existing.items()) + "\n",
                encoding="utf-8",
            )
        else:
            try:
                ENV_FILE.unlink()
            except FileNotFoundError:
                pass


def load_last_summary() -> dict:
    if not SUMMARY_FILE.exists():
        return {}
    try:
        return json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


class SyncManager:
    def __init__(self, api_key: str | None):
        self.api_key = (api_key or "").strip()
        self.lock = threading.Lock()
        self.in_progress = False
        self.current_step = "等待中"
        self.message = "服务已启动，等待同步。"
        self.last_started_at = ""
        self.last_finished_at = ""
        self.last_success_at = ""
        self.last_error = ""
        self.logs = deque(maxlen=120)

    @property
    def remote_sync_enabled(self) -> bool:
        return bool(self.api_key)

    def append_log(self, line: str) -> None:
        text = line.rstrip()
        if text:
            self.logs.append(f"[{now_text()}] {text}")

    def status(self) -> dict:
        with self.lock:
            return {
                "serviceAvailable": True,
                "inProgress": self.in_progress,
                "remoteSyncEnabled": self.remote_sync_enabled,
                "apiKeyConfigured": self.remote_sync_enabled,
                "apiKeyMasked": self._mask_api_key(),
                "currentStep": self.current_step,
                "message": self.message,
                "lastStartedAt": self.last_started_at,
                "lastFinishedAt": self.last_finished_at,
                "lastSuccessAt": self.last_success_at,
                "lastError": self.last_error,
                "lastSummary": load_last_summary(),
                "logs": list(self.logs)[-24:],
            }

    def _mask_api_key(self) -> str:
        if not self.api_key:
            return ""
        if len(self.api_key) <= 8:
            return "*" * len(self.api_key)
        return f"{self.api_key[:4]}{'*' * (len(self.api_key) - 8)}{self.api_key[-4:]}"

    def update_api_key(self, new_key: str) -> str:
        new_key = (new_key or "").strip()
        with self.lock:
            self.api_key = new_key
        if new_key:
            save_env_value(API_KEY_NAME, new_key)
        else:
            remove_env_value(API_KEY_NAME)
        self.append_log("已更新 API Key" if new_key else "已清空 API Key")
        return self._mask_api_key()

    def trigger(self) -> tuple[bool, str]:
        with self.lock:
            if self.in_progress:
                return False, "同步任务已在执行中"
            self.in_progress = True
            self.current_step = "准备开始"
            self.message = "同步任务已启动"
            self.last_started_at = now_text()
            self.last_error = ""
            self.append_log("收到新的同步请求")

        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        return True, "同步任务已启动"

    def _run_command(self, command: list[str]) -> None:
        self.append_log("$ " + " ".join(command))
        process = subprocess.Popen(
            command,
            cwd=str(BASE_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert process.stdout is not None
        for line in process.stdout:
            self.append_log(line)
        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(f"命令执行失败，退出码 {return_code}: {' '.join(command)}")

    def _run(self) -> None:
        try:
            if self.remote_sync_enabled:
                with self.lock:
                    self.current_step = "抓取微信读书"
                    self.message = "正在从微信读书拉取最新书架..."
                self._run_command(
                    [
                        sys.executable,
                        str(ANALYZE_SCRIPT),
                        "--api-key",
                        self.api_key,
                    ]
                )
                if not OUTPUT_JSON.exists():
                    raise FileNotFoundError(f"未找到采集结果: {OUTPUT_JSON}")
                shutil.copy2(OUTPUT_JSON, ROOT_JSON)
                self.append_log(f"已复制最新书籍详情到 {ROOT_JSON.name}")
            else:
                with self.lock:
                    self.current_step = "仅重建本地页面"
                    self.message = "未配置 WEREAD_API_KEY，跳过远端抓取，仅重建本地图书馆。"
                self.append_log("未配置 WEREAD_API_KEY，跳过远端抓取")

            with self.lock:
                self.current_step = "重建图书馆"
                self.message = "正在重建 SQLite 和前端页面..."
            self._run_command([sys.executable, str(BUILD_SCRIPT)])

            with self.lock:
                self.current_step = "完成"
                self.message = "同步完成，页面可刷新查看最新结果。"
                self.last_success_at = now_text()
        except Exception as exc:
            with self.lock:
                self.current_step = "失败"
                self.last_error = str(exc)
                self.message = f"同步失败：{exc}"
            self.append_log(f"ERROR: {exc}")
        finally:
            with self.lock:
                self.in_progress = False
                self.last_finished_at = now_text()


class LibraryRequestHandler(SimpleHTTPRequestHandler):
    sync_manager: SyncManager | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:
        if self.sync_manager:
            self.sync_manager.append_log("HTTP " + format % args)

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            assert self.sync_manager is not None
            self._send_json(self.sync_manager.status())
            return

        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        assert self.sync_manager is not None

        if parsed.path == "/api/sync":
            started, message = self.sync_manager.trigger()
            status_code = HTTPStatus.ACCEPTED if started else HTTPStatus.CONFLICT
            self._send_json(
                {
                    "ok": started,
                    "message": message,
                    "remoteSyncEnabled": self.sync_manager.remote_sync_enabled,
                },
                status=status_code,
            )
            return

        if parsed.path == "/api/api-key":
            payload = self._read_json_body()
            new_key = str(payload.get("apiKey", "")).strip()
            try:
                masked = self.sync_manager.update_api_key(new_key)
            except Exception as exc:
                self._send_json(
                    {"ok": False, "error": f"保存失败：{exc}"},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
                return
            self._send_json(
                {
                    "ok": True,
                    "apiKeyConfigured": bool(new_key),
                    "apiKeyMasked": masked,
                    "message": "API Key 已保存到 .env" if new_key else "API Key 已清空",
                }
            )
            return

        self._send_json({"ok": False, "error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="微信读书图书馆本地服务")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址，默认 127.0.0.1")
    parser.add_argument("--port", default=8765, type=int, help="监听端口，默认 8765")
    parser.add_argument("--api-key", help="微信读书 API Key；也可通过 WEREAD_API_KEY 环境变量提供")
    parser.add_argument("--no-browser", action="store_true", help="启动后不自动打开浏览器")
    return parser.parse_args()


def ensure_index_exists(sync_manager: SyncManager) -> None:
    if HTML_PATH.exists():
        return
    sync_manager.append_log("index.html 不存在，先执行一次本地重建")
    sync_manager._run_command([sys.executable, str(BUILD_SCRIPT)])


def main() -> None:
    args = parse_args()
    env_data = load_env_file()
    api_key = (
        args.api_key
        or os.environ.get(API_KEY_NAME, "")
        or env_data.get(API_KEY_NAME, "")
    )
    sync_manager = SyncManager(api_key)
    ensure_index_exists(sync_manager)

    LibraryRequestHandler.sync_manager = sync_manager
    server = ThreadingHTTPServer((args.host, args.port), LibraryRequestHandler)

    url = f"http://{args.host}:{args.port}/"
    print(f"🚀 本地服务已启动: {url}")
    if sync_manager.remote_sync_enabled:
        print("🔄 已启用远端同步：点击页面中的“立即同步”会抓微信读书并重建页面")
    else:
        print("ℹ️ 未配置 WEREAD_API_KEY：点击“立即同步”将只重建本地图书馆")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
