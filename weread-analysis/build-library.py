#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sqlite3
from datetime import datetime
from html import escape
from typing import Any
from urllib.parse import quote


DB_NAME = "weread-library.db"
JSON_NAME = "all-books-details.json"
HTML_NAME = "index.html"


CATEGORY_KEYWORDS = {
    "人工智能": ["人工智能", "ai", "aigc", "大模型", "chatgpt", "deepseek", "agent", "prompt", "midjourney", "sora"],
    "编程开发": ["编程", "程序", "python", "java", "javascript", "go语言", "golang", "rust", "c++", "数据库", "架构", "开发"],
    "产品商业": ["产品", "商业", "品牌", "营销", "创业", "运营", "增长", "销售", "管理", "战略", "公司"],
    "社会人文": ["社会", "文化", "纪实", "传播", "历史", "传记", "文明", "政治", "制度"],
    "心理成长": ["认知", "心理", "成长", "情绪", "思维", "学习", "写作", "方法论", "习惯"],
    "财经投资": ["经济", "金融", "投资", "理财", "基金", "股票", "商业分析", "财务"],
    "文学小说": ["小说", "文学", "故事", "悬疑", "科幻", "推理", "武侠", "言情"],
}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的微信读书图书馆</title>
    <style>
        :root {
            --bg: #07111f;
            --bg-soft: #0d1b2f;
            --panel: rgba(12, 23, 39, 0.84);
            --panel-strong: rgba(10, 19, 32, 0.94);
            --line: rgba(161, 182, 214, 0.16);
            --text: #ecf3ff;
            --muted: #9eb0cf;
            --accent: #89b4ff;
            --accent-strong: #5c8fff;
            --warm: #f4c978;
            --green: #68d7af;
            --red: #ff8b8b;
            --shadow: 0 28px 80px rgba(0, 0, 0, 0.35);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 16px;
            --radius-sm: 12px;
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at top left, rgba(92, 143, 255, 0.22), transparent 30%),
                radial-gradient(circle at top right, rgba(244, 201, 120, 0.12), transparent 26%),
                linear-gradient(180deg, #091321 0%, #06101c 55%, #050b13 100%);
            min-height: 100vh;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: 0.06;
            background-image:
                linear-gradient(rgba(255, 255, 255, 0.9) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.9) 1px, transparent 1px);
            background-size: 22px 22px;
            mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.7), transparent);
        }

        a {
            color: inherit;
        }

        .page {
            width: min(1440px, calc(100vw - 40px));
            margin: 22px auto 64px;
        }

        .shell {
            backdrop-filter: blur(18px);
            background: linear-gradient(180deg, rgba(8, 16, 29, 0.88), rgba(5, 12, 21, 0.92));
            border: 1px solid var(--line);
            border-radius: 32px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .hero {
            position: relative;
            padding: 42px 42px 34px;
            border-bottom: 1px solid var(--line);
            background:
                linear-gradient(130deg, rgba(137, 180, 255, 0.12), rgba(137, 180, 255, 0.02) 34%, rgba(244, 201, 120, 0.1)),
                linear-gradient(180deg, rgba(255, 255, 255, 0.03), transparent 58%);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.3fr) minmax(340px, 0.9fr);
            gap: 28px;
            align-items: stretch;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.09);
            color: var(--warm);
            font-size: 13px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero h1 {
            margin: 18px 0 12px;
            font-family: Georgia, "Times New Roman", "Songti SC", serif;
            font-size: clamp(38px, 5vw, 68px);
            line-height: 0.98;
            letter-spacing: -0.04em;
            max-width: 10ch;
        }

        .hero p {
            margin: 0;
            max-width: 760px;
            color: var(--muted);
            font-size: 16px;
            line-height: 1.8;
        }

        .hero-meta {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 26px;
        }

        .sync-console {
            margin-top: 24px;
            padding: 18px 18px 16px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            display: grid;
            gap: 12px;
            max-width: 760px;
        }

        .sync-console-top {
            display: flex;
            justify-content: space-between;
            gap: 14px;
            align-items: center;
            flex-wrap: wrap;
        }

        .sync-console-title {
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .sync-console-desc {
            margin: 4px 0 0;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.7;
        }

        .sync-actions {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .sync-button {
            border: 0;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(92, 143, 255, 0.96), rgba(71, 109, 255, 0.98));
            color: #fff;
            padding: 12px 16px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 14px 26px rgba(92, 143, 255, 0.24);
        }

        .sync-button:disabled {
            cursor: not-allowed;
            opacity: 0.55;
            box-shadow: none;
        }

        .sync-button-ghost {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text);
            box-shadow: none;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sync-button-ghost:hover:not(:disabled) {
            background: rgba(255, 255, 255, 0.12);
        }

        .sync-apikey {
            display: grid;
            gap: 10px;
            padding: 14px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .sync-apikey-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }

        .sync-apikey-status {
            font-size: 12px;
            color: var(--muted);
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .sync-apikey-status.is-on {
            color: var(--green);
            border-color: rgba(104, 215, 175, 0.35);
            background: rgba(104, 215, 175, 0.1);
        }

        .sync-apikey-row {
            display: grid;
            grid-template-columns: 1fr auto auto;
            gap: 8px;
            align-items: center;
        }

        .sync-apikey-row input {
            padding: 12px 14px;
        }

        .sync-apikey-feedback {
            font-size: 12px;
            color: var(--muted);
            min-height: 16px;
        }

        .sync-apikey-feedback.is-error {
            color: var(--red);
        }

        .sync-apikey-feedback.is-success {
            color: var(--green);
        }

        .sync-summary {
            padding: 14px;
            border-radius: 14px;
            background: rgba(137, 180, 255, 0.08);
            border: 1px solid rgba(137, 180, 255, 0.18);
            display: grid;
            gap: 10px;
        }

        .sync-summary-head {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 12px;
            font-size: 14px;
        }

        .sync-summary-head span {
            color: var(--muted);
            font-size: 12px;
        }

        .sync-summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 8px;
        }

        .sync-summary-grid > div {
            padding: 10px 12px;
            border-radius: 10px;
            background: rgba(5, 12, 21, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .sync-summary-grid strong {
            display: block;
            font-size: 18px;
            letter-spacing: -0.02em;
        }

        .sync-summary-grid span {
            color: var(--muted);
            font-size: 11px;
        }

        .sync-summary-extra {
            font-size: 12px;
            color: var(--muted);
            line-height: 1.7;
        }

        .sync-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 10px 12px;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: var(--muted);
            font-size: 12px;
        }

        .sync-status-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }

        .sync-status-card {
            padding: 12px 12px 11px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .sync-status-card strong {
            display: block;
            font-size: 12px;
            color: var(--muted);
            margin-bottom: 6px;
        }

        .sync-status-card span {
            display: block;
            font-size: 13px;
            line-height: 1.6;
        }

        .sync-message {
            min-height: 22px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
        }

        .sync-log {
            margin: 0;
            padding: 14px;
            border-radius: 16px;
            background: rgba(5, 10, 17, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.06);
            color: #b6c4de;
            font-family: Consolas, "SFMono-Regular", monospace;
            font-size: 12px;
            line-height: 1.65;
            white-space: pre-wrap;
            max-height: 180px;
            overflow: auto;
        }

        .meta-pill {
            padding: 11px 15px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--muted);
            font-size: 13px;
        }

        .hero-panel {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 16px;
            padding: 26px;
            border-radius: var(--radius-xl);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.03));
            border: 1px solid rgba(255, 255, 255, 0.08);
            min-height: 100%;
        }

        .hero-panel h2 {
            margin: 0;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .hero-panel p {
            margin: 6px 0 0;
            font-size: 14px;
            color: var(--muted);
            line-height: 1.75;
        }

        .hero-panel .panel-number {
            font-size: clamp(44px, 5vw, 72px);
            font-weight: 700;
            letter-spacing: -0.06em;
            color: var(--text);
        }

        .hero-panel small {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
        }

        .section {
            padding: 30px 42px 0;
        }

        .section-head {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: end;
            margin-bottom: 18px;
        }

        .section-head h2 {
            margin: 0;
            font-size: 24px;
            letter-spacing: -0.03em;
        }

        .section-head p {
            margin: 8px 0 0;
            color: var(--muted);
            line-height: 1.7;
            font-size: 14px;
        }

        .section-kicker {
            color: var(--warm);
            font-size: 12px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 14px;
        }

        .metric-card {
            padding: 18px 18px 16px;
            border-radius: var(--radius-lg);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.07);
            min-height: 132px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 13px;
        }

        .metric-value {
            margin: 14px 0 8px;
            font-size: 36px;
            font-weight: 700;
            letter-spacing: -0.05em;
        }

        .metric-note {
            color: var(--muted);
            font-size: 12px;
            line-height: 1.7;
        }

        .insights-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
            gap: 18px;
        }

        .insight-panel {
            padding: 22px;
            border-radius: var(--radius-xl);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .insight-panel h3 {
            margin: 0 0 14px;
            font-size: 18px;
        }

        .bars {
            display: grid;
            gap: 12px;
        }

        .bar-row {
            display: grid;
            gap: 8px;
        }

        .bar-meta {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
            font-size: 13px;
            color: var(--muted);
        }

        .bar {
            height: 10px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.06);
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(137, 180, 255, 0.55), rgba(92, 143, 255, 1));
        }

        .author-list {
            display: grid;
            gap: 10px;
        }

        .author-item {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
            padding: 12px 14px;
            border-radius: var(--radius-md);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .author-item strong {
            display: block;
            font-size: 14px;
        }

        .author-item span {
            color: var(--muted);
            font-size: 12px;
        }

        .shelves {
            display: grid;
            gap: 18px;
        }

        .shelf {
            padding: 24px;
            border-radius: var(--radius-xl);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.045), rgba(255, 255, 255, 0.03));
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .shelf-head {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: end;
            margin-bottom: 16px;
        }

        .shelf-head h3 {
            margin: 0;
            font-size: 19px;
        }

        .shelf-head p {
            margin: 8px 0 0;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
        }

        .shelf-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }

        .shelf-book {
            display: grid;
            grid-template-columns: 74px minmax(0, 1fr);
            gap: 12px;
            padding: 12px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
            min-height: 128px;
        }

        .shelf-book img {
            width: 74px;
            height: 106px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
            background: rgba(255, 255, 255, 0.05);
        }

        .shelf-book h4 {
            margin: 2px 0 6px;
            font-size: 14px;
            line-height: 1.45;
        }

        .shelf-book h4 a {
            text-decoration: none;
        }

        .shelf-book h4 a:hover {
            color: var(--accent);
        }

        .shelf-book p {
            margin: 0;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.65;
        }

        .shelf-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 10px;
        }

        .tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 11px;
            color: var(--muted);
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .library-browser {
            padding-bottom: 42px;
        }

        .browser-panel {
            padding: 22px;
            border-radius: var(--radius-xl);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .controls {
            display: grid;
            grid-template-columns: minmax(280px, 1.4fr) repeat(4, minmax(150px, 0.55fr));
            gap: 12px;
            align-items: center;
        }

        .control,
        .control select {
            width: 100%;
        }

        input.control,
        .control select {
            appearance: none;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(6, 14, 24, 0.74);
            color: var(--text);
            padding: 14px 16px;
            border-radius: 14px;
            font-size: 14px;
            outline: none;
        }

        input.control::placeholder {
            color: #7487aa;
        }

        .filter-pills {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 16px;
        }

        .filter-pill {
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: var(--muted);
            padding: 10px 14px;
            border-radius: 999px;
            font-size: 12px;
            cursor: pointer;
            transition: 180ms ease;
        }

        .filter-pill:hover,
        .filter-pill.is-active {
            color: var(--text);
            border-color: rgba(137, 180, 255, 0.38);
            background: rgba(92, 143, 255, 0.18);
        }

        .browser-meta {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: center;
            margin-top: 18px;
            color: var(--muted);
            font-size: 13px;
        }

        .pagination {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: center;
            margin-top: 22px;
            flex-wrap: wrap;
        }

        .pagination-info {
            color: var(--muted);
            font-size: 13px;
        }

        .pagination-controls {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }

        .page-btn {
            min-width: 40px;
            height: 40px;
            padding: 0 12px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: var(--text);
            font-size: 13px;
            cursor: pointer;
            transition: 180ms ease;
        }

        .page-btn:hover:not(:disabled),
        .page-btn.is-active {
            background: rgba(92, 143, 255, 0.18);
            border-color: rgba(137, 180, 255, 0.4);
        }

        .page-btn:disabled {
            opacity: 0.45;
            cursor: not-allowed;
        }

        .books-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin-top: 20px;
        }

        .book-card {
            position: relative;
            display: flex;
            flex-direction: column;
            min-height: 100%;
            border-radius: var(--radius-xl);
            overflow: hidden;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .book-card.is-subscription {
            background: linear-gradient(180deg, rgba(255, 214, 153, 0.08), rgba(255, 255, 255, 0.03));
            border-color: rgba(244, 201, 120, 0.2);
        }

        .book-cover {
            position: relative;
            aspect-ratio: 4 / 5;
            overflow: hidden;
            background: linear-gradient(160deg, rgba(137, 180, 255, 0.1), rgba(255, 255, 255, 0.02));
        }

        .book-cover img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .book-badges {
            position: absolute;
            top: 14px;
            left: 14px;
            right: 14px;
            display: flex;
            justify-content: space-between;
            gap: 8px;
            align-items: start;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 10px;
            border-radius: 999px;
            font-size: 11px;
            backdrop-filter: blur(12px);
            background: rgba(5, 10, 17, 0.66);
            border: 1px solid rgba(255, 255, 255, 0.09);
        }

        .badge.status-unread { color: var(--warm); }
        .badge.status-in_progress { color: var(--accent); }
        .badge.status-finished { color: var(--green); }
        .badge.status-article { color: #ffb3d0; }
        .badge.status-subscription { color: #ffd38f; }

        .book-body {
            display: flex;
            flex-direction: column;
            gap: 14px;
            padding: 16px 16px 18px;
            flex: 1;
        }

        .book-title {
            margin: 0;
            font-size: 17px;
            line-height: 1.4;
            letter-spacing: -0.03em;
        }

        .book-title a {
            text-decoration: none;
        }

        .book-title a:hover {
            color: var(--accent);
        }

        .book-author {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .book-meta {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }

        .meta-block {
            padding: 12px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .meta-block strong {
            display: block;
            font-size: 13px;
            margin-bottom: 4px;
        }

        .meta-block span {
            color: var(--muted);
            font-size: 12px;
            line-height: 1.6;
        }

        .book-description {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.8;
            min-height: 70px;
        }

        .book-footer {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
        }

        .book-category {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--muted);
        }

        .book-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            min-width: 116px;
            padding: 11px 14px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(92, 143, 255, 0.92), rgba(71, 109, 255, 0.96));
            color: white;
            text-decoration: none;
            font-size: 12px;
            font-weight: 600;
            box-shadow: 0 14px 26px rgba(92, 143, 255, 0.24);
        }

        .book-link.is-disabled {
            background: rgba(255, 255, 255, 0.06);
            color: var(--muted);
            box-shadow: none;
            cursor: default;
        }

        .subscription-note {
            padding: 10px 12px;
            border-radius: 12px;
            background: rgba(255, 214, 153, 0.08);
            border: 1px solid rgba(244, 201, 120, 0.14);
            color: #e9c98c;
            font-size: 12px;
            line-height: 1.6;
        }

        .empty-state {
            padding: 34px;
            text-align: center;
            color: var(--muted);
            border: 1px dashed rgba(255, 255, 255, 0.12);
            border-radius: var(--radius-xl);
            margin-top: 20px;
        }

        .footer {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: center;
            padding: 22px 42px 34px;
            color: var(--muted);
            font-size: 12px;
            border-top: 1px solid var(--line);
        }

        .footer strong {
            color: var(--text);
        }

        @media (max-width: 1180px) {
            .hero-grid,
            .insights-grid,
            .metrics,
            .books-grid,
            .shelf-grid,
            .controls,
            .sync-status-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .controls > :first-child {
                grid-column: 1 / -1;
            }
        }

        @media (max-width: 780px) {
            .page {
                width: min(100vw - 18px, 100%);
                margin: 10px auto 30px;
            }

            .hero,
            .section,
            .footer {
                padding-left: 18px;
                padding-right: 18px;
            }

            .hero-grid,
            .insights-grid,
            .metrics,
            .books-grid,
            .shelf-grid,
            .controls,
            .sync-status-grid {
                grid-template-columns: 1fr;
            }

            .hero h1 {
                max-width: none;
                font-size: 42px;
            }

            .browser-meta,
            .footer,
            .section-head,
            .shelf-head {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="page">
        <div class="shell">
            <section class="hero">
                <div class="hero-grid">
                    <div>
                        <span class="eyebrow">Personal WeRead Library</span>
                        <h1>我的微信读书图书馆</h1>
                        <p>把分散在微信读书里的藏书、评分、阅读状态和分类，整理成一个更像“个人书房”的离线图书馆。数据已经归档到本地 SQLite，页面可直接打开浏览，后续继续加标签、摘录或借阅清单也更方便。</p>
                        <div class="hero-meta">
                            <span class="meta-pill">最近生成：__GENERATED_AT__</span>
                            <span class="meta-pill">数据源：SQLite / JSON 双轨存档</span>
                            <span class="meta-pill">主文件：__DB_NAME__</span>
                        </div>
                        <div class="sync-console" id="syncConsole">
                            <div class="sync-console-top">
                                <div>
                                    <div class="sync-console-title">本地服务同步</div>
                                    <div class="sync-console-desc">通过本地服务触发“抓取微信读书并重建页面”。如果没配置 API Key，会自动退化成只重建本地书库。</div>
                                </div>
                                <div class="sync-actions">
                                    <span class="sync-chip" id="serviceModeChip">服务未连接</span>
                                    <button class="sync-button" id="syncButton" type="button" disabled>立即同步</button>
                                    <button class="sync-button sync-button-ghost" id="retrySyncButton" type="button" hidden>失败重试</button>
                                </div>
                            </div>
                            <div class="sync-status-grid">
                                <div class="sync-status-card">
                                    <strong>服务状态</strong>
                                    <span id="serviceStatusValue">未连接</span>
                                </div>
                                <div class="sync-status-card">
                                    <strong>同步模式</strong>
                                    <span id="syncModeValue">未知</span>
                                </div>
                                <div class="sync-status-card">
                                    <strong>最后成功</strong>
                                    <span id="lastSuccessValue">暂无</span>
                                </div>
                                <div class="sync-status-card">
                                    <strong>当前阶段</strong>
                                    <span id="currentStepValue">等待中</span>
                                </div>
                            </div>
                            <div class="sync-message" id="syncMessage">请通过本地服务打开页面后使用同步功能。</div>

                            <div class="sync-apikey" id="apiKeyPanel" hidden>
                                <div class="sync-apikey-head">
                                    <strong>WeRead API Key</strong>
                                    <span id="apiKeyStatus" class="sync-apikey-status">未配置</span>
                                </div>
                                <p class="sync-console-desc">填入后会保存到本目录的 <code>.env</code>，重启本地服务也会自动读取。</p>
                                <div class="sync-apikey-row">
                                    <input id="apiKeyInput" class="control" type="password" placeholder="粘贴你的 WEREAD_API_KEY" autocomplete="off">
                                    <button class="sync-button sync-button-ghost" id="apiKeySaveButton" type="button">保存到 .env</button>
                                    <button class="sync-button sync-button-ghost" id="apiKeyClearButton" type="button">清空</button>
                                </div>
                                <div class="sync-apikey-feedback" id="apiKeyFeedback"></div>
                            </div>

                            <div class="sync-summary" id="syncSummary" hidden>
                                <div class="sync-summary-head">
                                    <strong>上次同步摘要</strong>
                                    <span id="syncSummaryTime">--</span>
                                </div>
                                <div class="sync-summary-grid" id="syncSummaryGrid"></div>
                                <div class="sync-summary-extra" id="syncSummaryExtra"></div>
                            </div>

                            <pre class="sync-log" id="syncLog">等待服务状态...</pre>
                        </div>
                    </div>
                    <aside class="hero-panel">
                        <div>
                            <h2>图书馆总览</h2>
                            <p>这一版以“编辑式书房”做视觉方向，强调藏书规模、主题分布、精选书架和可筛选的全量浏览区，目标不是分析报告，而是长期可用的私人阅读资产库。</p>
                        </div>
                        <div class="panel-number">__TOTAL_BOOKS__</div>
                        <small>已归档书籍 / 文章共 <strong>__TOTAL_BOOKS__</strong> 条，含公众号内容、出版书、技术书和个人主题阅读集合。</small>
                    </aside>
                </div>
            </section>

            <section class="section">
                <div class="section-head">
                    <div>
                        <div class="section-kicker">Dashboard</div>
                        <h2>书房看板</h2>
                        <p>先看全局，再决定今天想读什么。这里展示你的阅读存量、活跃状态与主题构成。</p>
                    </div>
                </div>
                <div class="metrics">
                    __METRIC_CARDS__
                </div>
            </section>

            <section class="section">
                <div class="section-head">
                    <div>
                        <div class="section-kicker">Insights</div>
                        <h2>主题与作者分布</h2>
                        <p>左边看你的主题偏好，右边看藏书最多的作者，方便判断阅读重心是否过于集中。</p>
                    </div>
                </div>
                <div class="insights-grid">
                    <div class="insight-panel">
                        <h3>高频主题</h3>
                        <div class="bars">
                            __CATEGORY_BARS__
                        </div>
                    </div>
                    <div class="insight-panel">
                        <h3>收藏最多的作者</h3>
                        <div class="author-list">
                            __AUTHOR_LIST__
                        </div>
                    </div>
                </div>
            </section>

            <section class="section">
                <div class="section-head">
                    <div>
                        <div class="section-kicker">Curated Shelves</div>
                        <h2>精选书架</h2>
                        <p>不只是把书铺开，而是按“新入库 / 高分未读 / 正在翻阅”做成三组可直接开读的书架。</p>
                    </div>
                </div>
                <div class="shelves">
                    __FEATURED_SHELVES__
                </div>
            </section>

            <section class="section library-browser" id="library-browser">
                <div class="section-head">
                    <div>
                        <div class="section-kicker">Browse</div>
                        <h2>全部藏书</h2>
                        <p>支持按书名、作者、状态、分类、年份和排序方式筛选。页面离线可用，数据来自 SQLite 查询结果。</p>
                    </div>
                </div>
                <div class="browser-panel">
                    <div class="controls">
                        <input id="searchInput" class="control" type="search" placeholder="搜索书名、作者、出版社或简介关键词">
                        <select id="statusFilter" class="control">
                            <option value="all">全部状态</option>
                            <option value="unread">未开始</option>
                            <option value="in_progress">读过一些</option>
                            <option value="finished">已读完</option>
                            <option value="article">公众号订阅</option>
                        </select>
                        <select id="categoryFilter" class="control">
                            <option value="all">全部分类</option>
                        </select>
                        <select id="yearFilter" class="control">
                            <option value="all">全部年份</option>
                        </select>
                        <select id="sortFilter" class="control">
                            <option value="smart">智能排序</option>
                            <option value="recent">最近出版</option>
                            <option value="rating">评分优先</option>
                            <option value="title">书名字母</option>
                        </select>
                    </div>
                    <div class="filter-pills" id="quickFilters">
                        <button class="filter-pill is-active" type="button" data-mode="all">全部藏书</button>
                        <button class="filter-pill" type="button" data-mode="high_rating">高分精选</button>
                        <button class="filter-pill" type="button" data-mode="unread_gems">高分未读</button>
                        <button class="filter-pill" type="button" data-mode="recent">近三年出版</button>
                        <button class="filter-pill" type="button" data-mode="articles">公众号订阅</button>
                    </div>
                    <div class="browser-meta">
                        <div id="resultSummary">正在载入藏书...</div>
                        <div>本地服务模式下可直接点击“立即同步”；纯静态打开时仍需手动重建。</div>
                    </div>
                    <div class="books-grid" id="booksGrid"></div>
                    <div class="empty-state" id="emptyState" hidden>没有找到匹配的书。试试放宽关键词，或切换快速筛选。</div>
                    <div class="pagination" id="pagination" hidden>
                        <div class="pagination-info" id="paginationInfo">第 1 页</div>
                        <div class="pagination-controls" id="paginationControls"></div>
                    </div>
                </div>
            </section>

            <footer class="footer">
                <div>由 <strong>build-library.py</strong> 从 SQLite 数据库生成。数据库文件：<strong>__DB_NAME__</strong></div>
                <div>总计 __TOTAL_BOOKS__ 条记录，最后构建于 __GENERATED_AT__</div>
            </footer>
        </div>
    </div>

    <script id="libraryData" type="application/json">__BOOKS_JSON__</script>
    <script id="categoryOptionsData" type="application/json">__CATEGORY_OPTIONS__</script>
    <script id="yearOptionsData" type="application/json">__YEAR_OPTIONS__</script>
    <script>
        const LIBRARY_BOOKS = JSON.parse(document.getElementById('libraryData').textContent);
        const CATEGORY_OPTIONS = JSON.parse(document.getElementById('categoryOptionsData').textContent);
        const YEAR_OPTIONS = JSON.parse(document.getElementById('yearOptionsData').textContent);

        const statusFilter = document.getElementById('statusFilter');
        const categoryFilter = document.getElementById('categoryFilter');
        const yearFilter = document.getElementById('yearFilter');
        const sortFilter = document.getElementById('sortFilter');
        const searchInput = document.getElementById('searchInput');
        const booksGrid = document.getElementById('booksGrid');
        const resultSummary = document.getElementById('resultSummary');
        const emptyState = document.getElementById('emptyState');
        const quickFilters = Array.from(document.querySelectorAll('.filter-pill'));
        const pagination = document.getElementById('pagination');
        const paginationInfo = document.getElementById('paginationInfo');
        const paginationControls = document.getElementById('paginationControls');
        const syncButton = document.getElementById('syncButton');
        const serviceModeChip = document.getElementById('serviceModeChip');
        const serviceStatusValue = document.getElementById('serviceStatusValue');
        const syncModeValue = document.getElementById('syncModeValue');
        const lastSuccessValue = document.getElementById('lastSuccessValue');
        const currentStepValue = document.getElementById('currentStepValue');
        const syncMessage = document.getElementById('syncMessage');
        const syncLog = document.getElementById('syncLog');
        const retrySyncButton = document.getElementById('retrySyncButton');
        const apiKeyPanel = document.getElementById('apiKeyPanel');
        const apiKeyStatus = document.getElementById('apiKeyStatus');
        const apiKeyInput = document.getElementById('apiKeyInput');
        const apiKeySaveButton = document.getElementById('apiKeySaveButton');
        const apiKeyClearButton = document.getElementById('apiKeyClearButton');
        const apiKeyFeedback = document.getElementById('apiKeyFeedback');
        const syncSummary = document.getElementById('syncSummary');
        const syncSummaryTime = document.getElementById('syncSummaryTime');
        const syncSummaryGrid = document.getElementById('syncSummaryGrid');
        const syncSummaryExtra = document.getElementById('syncSummaryExtra');

        let quickMode = 'all';
        let currentPage = 1;
        const pageSize = 24;
        let syncPollingTimer = null;
        let lastKnownSuccessAt = '';
        let lastSyncFailed = false;

        function truncate(text, limit) {
            const value = String(text || '').trim();
            if (!value) return '暂无简介';
            return value.length > limit ? value.slice(0, limit) + '…' : value;
        }

        function escapeHtml(value) {
            return String(value || '')
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        function populateOptions(select, values) {
            values.forEach((value) => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                select.appendChild(option);
            });
        }

        function isLocalServiceMode() {
            return window.location.protocol === 'http:' || window.location.protocol === 'https:';
        }

        function setSyncUiDisconnected(message) {
            serviceModeChip.textContent = '服务未连接';
            serviceStatusValue.textContent = '未连接';
            syncModeValue.textContent = '不可用';
            lastSuccessValue.textContent = '暂无';
            currentStepValue.textContent = '等待中';
            syncMessage.textContent = message;
            syncLog.textContent = '请运行 python .\\\\local-service.py 后，通过 http://127.0.0.1:8765 打开页面。';
            syncButton.disabled = true;
            retrySyncButton.hidden = true;
            apiKeyPanel.hidden = true;
            syncSummary.hidden = true;
        }

        function formatNumber(value) {
            const num = Number(value || 0);
            return Number.isFinite(num) ? num.toLocaleString('zh-CN') : '0';
        }

        function renderApiKey(status) {
            apiKeyPanel.hidden = false;
            const configured = Boolean(status.apiKeyConfigured);
            apiKeyStatus.textContent = configured ? '已配置 ' + (status.apiKeyMasked || '') : '未配置';
            apiKeyStatus.classList.toggle('is-on', configured);
            apiKeyClearButton.disabled = !configured;
        }

        function renderSummary(summary) {
            if (!summary) {
                syncSummary.hidden = true;
                syncSummaryGrid.innerHTML = '';
                syncSummaryExtra.innerHTML = '';
                return;
            }
            syncSummary.hidden = false;
            syncSummaryTime.textContent = summary.generatedAt ? '生成于 ' + summary.generatedAt : '';
            const cells = [
                ['总书目', formatNumber(summary.totalBooks)],
                ['未读', formatNumber(summary.unread)],
                ['在读', formatNumber(summary.inProgress)],
                ['已读完', formatNumber(summary.finished)],
                ['公众号订阅', formatNumber(summary.articles)],
                ['有评分书目', formatNumber(summary.ratedBooks)],
                ['高分书目', formatNumber(summary.highRating)],
                ['近三个月入库', formatNumber(summary.recentBooks)],
            ];
            syncSummaryGrid.innerHTML = cells
                .map(([label, value]) => '<div class="sync-summary-cell"><span>' + escapeHtml(label) + '</span><strong>' + escapeHtml(value) + '</strong></div>')
                .join('');

            const extras = [];
            if (Array.isArray(summary.topCategories) && summary.topCategories.length) {
                const items = summary.topCategories
                    .slice(0, 5)
                    .map((entry) => escapeHtml(entry.name || '未分类') + ' · ' + formatNumber(entry.count))
                    .join('，');
                extras.push('<div><strong>热门分类：</strong>' + items + '</div>');
            }
            if (Array.isArray(summary.topAuthors) && summary.topAuthors.length) {
                const items = summary.topAuthors
                    .slice(0, 5)
                    .map((entry) => escapeHtml(entry.name || '未知作者') + ' · ' + formatNumber(entry.count))
                    .join('，');
                extras.push('<div><strong>高产作者：</strong>' + items + '</div>');
            }
            syncSummaryExtra.innerHTML = extras.join('');
        }

        function renderSyncStatus(status) {
            const connected = Boolean(status && status.serviceAvailable);
            if (!connected) {
                setSyncUiDisconnected('当前页面没有连接到本地服务，无法直接同步微信读书数据。');
                return;
            }

            const inProgress = Boolean(status.inProgress);
            const modeLabel = status.remoteSyncEnabled ? '抓微信读书 + 重建' : '仅重建本地书库';
            serviceModeChip.textContent = inProgress ? '同步进行中' : '服务已连接';
            serviceStatusValue.textContent = inProgress ? '同步进行中' : '在线';
            syncModeValue.textContent = modeLabel;
            lastSuccessValue.textContent = status.lastSuccessAt || '暂无';
            currentStepValue.textContent = status.currentStep || '等待中';
            syncMessage.textContent = status.message || (inProgress ? '正在同步，请稍候...' : '服务已连接，可以直接同步。');
            syncLog.textContent = (status.logs && status.logs.length ? status.logs.join('\\n') : '暂无日志');
            syncButton.disabled = inProgress;

            renderApiKey(status);
            renderSummary(status.lastSummary);

            lastSyncFailed = Boolean(status.lastError);
            retrySyncButton.hidden = !(lastSyncFailed && !inProgress);
            retrySyncButton.disabled = inProgress;
            if (lastSyncFailed && !inProgress) {
                syncMessage.textContent = '上次同步失败：' + (status.lastError || '未知错误') + '，可点击“失败重试”再次尝试。';
            }

            lastKnownSuccessAt = status.lastSuccessAt || lastKnownSuccessAt;
        }

        async function fetchSyncStatus() {
            if (!isLocalServiceMode()) {
                setSyncUiDisconnected('当前是文件直开模式。要使用“立即同步”，请先启动本地服务。');
                return null;
            }

            try {
                const response = await fetch('/api/status', { cache: 'no-store' });
                if (!response.ok) {
                    throw new Error('status request failed');
                }
                const status = await response.json();
                renderSyncStatus(status);

                if (status.inProgress) {
                    startSyncPolling();
                } else {
                    stopSyncPolling();
                    if (status.lastSuccessAt && lastKnownSuccessAt && status.lastSuccessAt !== lastKnownSuccessAt) {
                        syncMessage.textContent = '同步已完成，页面即将自动刷新以载入最新数据。';
                        window.setTimeout(() => window.location.reload(), 900);
                    }
                    lastKnownSuccessAt = status.lastSuccessAt || lastKnownSuccessAt;
                }

                return status;
            } catch (error) {
                stopSyncPolling();
                setSyncUiDisconnected('本地服务暂时不可达，请确认 local-service.py 正在运行。');
                return null;
            }
        }

        function startSyncPolling() {
            if (syncPollingTimer) return;
            syncPollingTimer = window.setInterval(fetchSyncStatus, 2000);
        }

        function stopSyncPolling() {
            if (!syncPollingTimer) return;
            window.clearInterval(syncPollingTimer);
            syncPollingTimer = null;
        }

        async function triggerSync() {
            if (syncButton.disabled) return;
            syncButton.disabled = true;
            syncMessage.textContent = '已发送同步请求，正在启动后台任务...';

            try {
                const response = await fetch('/api/sync', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ source: 'ui' }),
                });
                const result = await response.json();
                if (!response.ok || !result.ok) {
                    throw new Error(result.error || 'sync failed');
                }
                syncMessage.textContent = result.message || '同步任务已开始。';
                startSyncPolling();
                fetchSyncStatus();
            } catch (error) {
                syncButton.disabled = false;
                syncMessage.textContent = '同步启动失败：' + (error && error.message ? error.message : '未知错误');
            }
        }

        function setApiKeyFeedback(text, kind) {
            apiKeyFeedback.textContent = text || '';
            apiKeyFeedback.classList.remove('is-error', 'is-success');
            if (kind === 'error') {
                apiKeyFeedback.classList.add('is-error');
            } else if (kind === 'ok') {
                apiKeyFeedback.classList.add('is-success');
            }
        }

        async function postApiKey(value) {
            const response = await fetch('/api/api-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ apiKey: value }),
            });
            const result = await response.json();
            if (!response.ok || !result.ok) {
                throw new Error(result.error || 'api key request failed');
            }
            return result;
        }

        async function saveApiKey() {
            const value = (apiKeyInput.value || '').trim();
            if (!value) {
                setApiKeyFeedback('请先粘贴 API Key 后再保存。', 'error');
                return;
            }
            apiKeySaveButton.disabled = true;
            setApiKeyFeedback('正在保存到 .env ...', 'info');
            try {
                await postApiKey(value);
                apiKeyInput.value = '';
                setApiKeyFeedback('已保存到 .env，下次启动本地服务也会自动读取。', 'ok');
                fetchSyncStatus();
            } catch (error) {
                setApiKeyFeedback('保存失败：' + (error && error.message ? error.message : '未知错误'), 'error');
            } finally {
                apiKeySaveButton.disabled = false;
            }
        }

        async function clearApiKey() {
            apiKeyClearButton.disabled = true;
            setApiKeyFeedback('正在清空 .env 中的 API Key ...', 'info');
            try {
                await postApiKey('');
                apiKeyInput.value = '';
                setApiKeyFeedback('已清空 API Key，再次同步会退化成仅重建本地书库。', 'ok');
                fetchSyncStatus();
            } catch (error) {
                setApiKeyFeedback('清空失败：' + (error && error.message ? error.message : '未知错误'), 'error');
            } finally {
                apiKeyClearButton.disabled = false;
            }
        }

        function matchesQuickMode(book) {
            switch (quickMode) {
                case 'high_rating':
                    return book.rating >= 80 && book.ratingCount >= 20;
                case 'unread_gems':
                    return book.status === 'unread' && book.rating >= 75 && book.ratingCount >= 10;
                case 'recent':
                    return book.publishYear >= 2023;
                case 'articles':
                    return book.sourceType === 'article';
                default:
                    return true;
            }
        }

        function getFilteredBooks() {
            const keyword = searchInput.value.trim().toLowerCase();
            const status = statusFilter.value;
            const category = categoryFilter.value;
            const year = yearFilter.value;
            const sortBy = sortFilter.value;

            let books = LIBRARY_BOOKS.filter((book) => {
                if (!matchesQuickMode(book)) return false;
                if (status === 'article' && book.sourceType !== 'article') return false;
                if (status !== 'all' && status !== 'article' && book.status !== status) return false;
                if (category !== 'all' && book.category !== category) return false;
                if (year !== 'all' && String(book.publishYear) !== year) return false;

                if (!keyword) return true;

                const haystack = [
                    book.title,
                    book.author,
                    book.publisher,
                    book.category,
                    book.intro,
                ]
                    .filter(Boolean)
                    .join(' ')
                    .toLowerCase();

                return haystack.includes(keyword);
            });

            books.sort((a, b) => {
                if (sortBy === 'recent') {
                    return (b.publishYear || 0) - (a.publishYear || 0) || b.sortScore - a.sortScore;
                }
                if (sortBy === 'rating') {
                    return (b.rating || 0) - (a.rating || 0) || (b.ratingCount || 0) - (a.ratingCount || 0);
                }
                if (sortBy === 'title') {
                    return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hans-CN');
                }
                return (b.sortScore || 0) - (a.sortScore || 0);
            });

            return books;
        }

        function renderPagination(totalItems) {
            const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));

            if (totalItems === 0 || totalPages === 1) {
                pagination.hidden = true;
                paginationControls.innerHTML = '';
                return;
            }

            pagination.hidden = false;
            paginationInfo.textContent = `第 ${currentPage} / ${totalPages} 页，每页 ${pageSize} 本`;

            const pages = [];
            const start = Math.max(1, currentPage - 2);
            const end = Math.min(totalPages, currentPage + 2);
            for (let page = start; page <= end; page += 1) {
                pages.push(page);
            }

            const buttons = [];
            buttons.push(`<button class="page-btn" type="button" data-page="${currentPage - 1}" ${currentPage === 1 ? 'disabled' : ''}>上一页</button>`);

            if (start > 1) {
                buttons.push('<button class="page-btn" type="button" data-page="1">1</button>');
                if (start > 2) {
                    buttons.push('<button class="page-btn" type="button" disabled>…</button>');
                }
            }

            pages.forEach((page) => {
                buttons.push(`<button class="page-btn ${page === currentPage ? 'is-active' : ''}" type="button" data-page="${page}">${page}</button>`);
            });

            if (end < totalPages) {
                if (end < totalPages - 1) {
                    buttons.push('<button class="page-btn" type="button" disabled>…</button>');
                }
                buttons.push(`<button class="page-btn" type="button" data-page="${totalPages}">${totalPages}</button>`);
            }

            buttons.push(`<button class="page-btn" type="button" data-page="${currentPage + 1}" ${currentPage === totalPages ? 'disabled' : ''}>下一页</button>`);

            paginationControls.innerHTML = buttons.join('');
            paginationControls.querySelectorAll('[data-page]').forEach((button) => {
                button.addEventListener('click', () => {
                    const page = Number(button.dataset.page);
                    if (!page || page === currentPage || page < 1 || page > totalPages) {
                        return;
                    }
                    currentPage = page;
                    applyFilters(false);
                    const browserTop = document.getElementById('library-browser').offsetTop - 24;
                    window.scrollTo({ top: browserTop, behavior: 'smooth' });
                });
            });
        }

        function renderBooks(books) {
            const totalItems = books.length;
            const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));
            if (currentPage > totalPages) {
                currentPage = totalPages;
            }
            const startIndex = (currentPage - 1) * pageSize;
            const pageBooks = books.slice(startIndex, startIndex + pageSize);

            resultSummary.textContent = `当前显示第 ${currentPage} 页 ${pageBooks.length} 本，共 ${totalItems} / ${LIBRARY_BOOKS.length} 条记录`;

            if (!totalItems) {
                booksGrid.innerHTML = '';
                emptyState.hidden = false;
                pagination.hidden = true;
                return;
            }

            emptyState.hidden = true;
            renderPagination(totalItems);

            booksGrid.innerHTML = pageBooks.map((book) => {
                const statusLabelMap = {
                    unread: '未开始',
                    in_progress: '读过一些',
                    finished: '已读完',
                };
                const statusLabel = statusLabelMap[book.status] || '未开始';
                const rightBadge = book.sourceType === 'article' ? '<span class="badge status-subscription">公众号订阅</span>' : `<span class="badge">评分 ${book.rating || '暂无'}</span>`;
                const description = truncate(book.intro, 92);
                const yearText = book.publishYear ? `${book.publishYear} 年` : '年份未知';
                const ratingText = book.rating ? `${book.rating} 分` : '暂无评分';
                const countText = book.ratingCount ? `${book.ratingCount} 条点评` : '评价较少';
                const cardClass = book.sourceType === 'article' ? 'book-card is-subscription' : 'book-card';
                const titleHtml = book.isExternalLink
                    ? `<a href="${escapeHtml(book.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(book.title)}</a>`
                    : `<span>${escapeHtml(book.title)}</span>`;
                const footerAction = book.isExternalLink
                    ? `<a class="book-link" href="${escapeHtml(book.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(book.actionLabel || '前往微信读书')}</a>`
                    : `<span class="book-link is-disabled">${escapeHtml(book.actionLabel || '公众号订阅')}</span>`;
                const extraNote = book.sourceType === 'article'
                    ? '<div class="subscription-note">这是微信读书中的公众号订阅条目，不是可直达的单本图书；当前仅作为订阅记录展示。</div>'
                    : '';

                return `
                    <article class="${cardClass}">
                        <div class="book-cover">
                            <img src="${escapeHtml(book.cover)}" alt="${escapeHtml(book.title)}">
                            <div class="book-badges">
                                <span class="badge status-${escapeHtml(book.status)}">${escapeHtml(statusLabel)}</span>
                                ${rightBadge}
                            </div>
                        </div>
                        <div class="book-body">
                            <div>
                                <h3 class="book-title">${titleHtml}</h3>
                                <div class="book-author">${escapeHtml(book.author || '未知作者')}</div>
                            </div>
                            <div class="book-meta">
                                <div class="meta-block">
                                    <strong>${escapeHtml(ratingText)}</strong>
                                    <span>${escapeHtml(countText)}</span>
                                </div>
                                <div class="meta-block">
                                    <strong>${escapeHtml(yearText)}</strong>
                                    <span>${escapeHtml(book.publisher || '未记录出版社')}</span>
                                </div>
                            </div>
                            <div class="book-description">${escapeHtml(description)}</div>
                            ${extraNote}
                            <div class="book-footer">
                                <div class="book-category">${escapeHtml(book.sourceType === 'article' ? '公众号订阅' : book.category)}</div>
                                ${footerAction}
                            </div>
                        </div>
                    </article>
                `;
            }).join('');
        }

        function applyFilters(resetPage = true) {
            if (resetPage) {
                currentPage = 1;
            }
            renderBooks(getFilteredBooks());
        }

        populateOptions(categoryFilter, CATEGORY_OPTIONS);
        populateOptions(yearFilter, YEAR_OPTIONS);

        [searchInput, statusFilter, categoryFilter, yearFilter, sortFilter].forEach((element) => {
            element.addEventListener('input', applyFilters);
            element.addEventListener('change', applyFilters);
        });

        quickFilters.forEach((button) => {
            button.addEventListener('click', () => {
                quickMode = button.dataset.mode;
                quickFilters.forEach((item) => item.classList.toggle('is-active', item === button));
                applyFilters(true);
            });
        });

        syncButton.addEventListener('click', triggerSync);
        retrySyncButton.addEventListener('click', triggerSync);
        apiKeySaveButton.addEventListener('click', saveApiKey);
        apiKeyClearButton.addEventListener('click', clearApiKey);
        apiKeyInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                saveApiKey();
            }
        });

        applyFilters(true);
        fetchSyncStatus();
    </script>
</body>
</html>
"""


def normalize_text(text: Any) -> str:
    return str(text or "").strip()


def safe_json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def normalize_search_keywords(title: str) -> str:
    keywords = normalize_text(title)
    keywords = re.sub(r"[（(][^）)]*[）)]", " ", keywords)
    keywords = re.sub(r"[“”\"'‘’：:？?!！，,、/\\|]+", " ", keywords)
    keywords = re.sub(r"\s+", " ", keywords).strip()
    return keywords or normalize_text(title)


def build_public_account_url(title: str) -> str:
    return ""


def build_book_url(book_id: str, title: str) -> str:
    book_id = normalize_text(book_id)
    if book_id.startswith("MP_WXS_"):
        return build_public_account_url(title)

    if not book_id or book_id.isdigit() or book_id.startswith("YueWen_"):
        return "https://weread.qq.com/web/search/books?keyword=" + quote(normalize_search_keywords(title), safe="")

    return "https://weread.qq.com/web/bookDetail/" + quote(book_id, safe="")


def infer_category(title: str, author: str, original_category: str, book_id: str) -> str:
    category = normalize_text(original_category)
    if category and category != "未分类":
        return category

    if normalize_text(book_id).startswith("MP_WXS_"):
        return "公众号订阅"

    haystack = f"{normalize_text(title)} {normalize_text(author)}".lower()
    for category_name, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in haystack for keyword in keywords):
            return category_name
    return "未分类"


def parse_publish_year(publish_time: str) -> int:
    value = normalize_text(publish_time)
    if not value:
        return 0
    match = re.match(r"(\d{4})", value)
    return int(match.group(1)) if match else 0


def reading_status(read_update_time: int, finish_reading: int) -> str:
    if finish_reading == 1:
        return "finished"
    if int(read_update_time or 0) > 0:
        return "in_progress"
    return "unread"


def compute_sort_score(rating: int, rating_count: int, publish_year: int, status: str) -> float:
    score = float(rating or 0)
    score += min((rating_count or 0), 400) * 0.45
    if publish_year >= 2024:
        score += 65
    elif publish_year >= 2020:
        score += 28
    if status == "finished":
        score += 18
    elif status == "in_progress":
        score += 10
    return round(score, 2)


def create_database(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS books (
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            translator TEXT,
            cover TEXT,
            rating INTEGER NOT NULL DEFAULT 0,
            rating_count INTEGER NOT NULL DEFAULT 0,
            intro TEXT,
            isbn TEXT,
            category TEXT,
            publisher TEXT,
            publish_time TEXT,
            publish_year INTEGER NOT NULL DEFAULT 0,
            read_update_time INTEGER NOT NULL DEFAULT 0,
            finish_reading INTEGER NOT NULL DEFAULT 0,
            reading_status TEXT NOT NULL,
            source_type TEXT NOT NULL,
            search_url TEXT NOT NULL,
            sort_score REAL NOT NULL DEFAULT 0,
            imported_at TEXT NOT NULL,
            raw_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_books_category ON books(category);
        CREATE INDEX IF NOT EXISTS idx_books_status ON books(reading_status);
        CREATE INDEX IF NOT EXISTS idx_books_publish_year ON books(publish_year DESC);
        CREATE INDEX IF NOT EXISTS idx_books_sort_score ON books(sort_score DESC);
        """
    )


def load_books(json_path: str) -> list[dict[str, Any]]:
    with open(json_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def import_books(conn: sqlite3.Connection, books: list[dict[str, Any]]) -> None:
    imported_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for book in books:
        book_id = normalize_text(book.get("bookId"))
        title = normalize_text(book.get("title"))
        author = normalize_text(book.get("author"))
        translator = normalize_text(book.get("translator"))
        publish_time = normalize_text(book.get("publishTime"))
        publish_year = parse_publish_year(publish_time)
        rating = int(book.get("newRating") or 0)
        rating_count = int(book.get("newRatingCount") or 0)
        finish_reading = int(book.get("finishReading") or 0)
        read_update_time = int(book.get("readUpdateTime") or 0)
        status = reading_status(read_update_time, finish_reading)
        source_type = "article" if book_id.startswith("MP_WXS_") else "book"
        category = infer_category(
            title,
            author,
            normalize_text(book.get("category")) or normalize_text(book.get("categoryName")),
            book_id,
        )
        cover = normalize_text(book.get("cover"))
        intro = normalize_text(book.get("intro"))
        isbn = normalize_text(book.get("isbn"))
        publisher = normalize_text(book.get("publisher"))
        url = build_book_url(book_id, title)
        sort_score = compute_sort_score(rating, rating_count, publish_year, status)

        rows.append(
            (
                book_id or title,
                title or "未命名书籍",
                author,
                translator,
                cover,
                rating,
                rating_count,
                intro,
                isbn,
                category,
                publisher,
                publish_time,
                publish_year,
                read_update_time,
                finish_reading,
                status,
                source_type,
                url,
                sort_score,
                imported_at,
                json.dumps(book, ensure_ascii=False),
            )
        )

    conn.executemany(
        """
        INSERT INTO books (
            book_id, title, author, translator, cover, rating, rating_count, intro, isbn,
            category, publisher, publish_time, publish_year, read_update_time, finish_reading,
            reading_status, source_type, search_url, sort_score, imported_at, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(book_id) DO UPDATE SET
            title = excluded.title,
            author = excluded.author,
            translator = excluded.translator,
            cover = excluded.cover,
            rating = excluded.rating,
            rating_count = excluded.rating_count,
            intro = excluded.intro,
            isbn = excluded.isbn,
            category = excluded.category,
            publisher = excluded.publisher,
            publish_time = excluded.publish_time,
            publish_year = excluded.publish_year,
            read_update_time = excluded.read_update_time,
            finish_reading = excluded.finish_reading,
            reading_status = excluded.reading_status,
            source_type = excluded.source_type,
            search_url = excluded.search_url,
            sort_score = excluded.sort_score,
            imported_at = excluded.imported_at,
            raw_json = excluded.raw_json
        """,
        rows,
    )
    conn.commit()


def fetch_rows(conn: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    return list(conn.execute(query, params))


def metric_card(label: str, value: Any, note: str) -> str:
    return (
        '<article class="metric-card">'
        f'<div class="metric-label">{escape(str(label))}</div>'
        f'<div class="metric-value">{escape(str(value))}</div>'
        f'<div class="metric-note">{escape(str(note))}</div>'
        "</article>"
    )


def category_bar(name: str, count: int, max_count: int) -> str:
    width = 0 if max_count == 0 else round(count / max_count * 100, 2)
    return (
        '<div class="bar-row">'
        f'<div class="bar-meta"><span>{escape(name)}</span><span>{count} 本</span></div>'
        f'<div class="bar"><div class="bar-fill" style="width:{width}%"></div></div>'
        "</div>"
    )


def author_item(name: str, count: int) -> str:
    return (
        '<div class="author-item">'
        f'<div><strong>{escape(name)}</strong><span>共收藏 {count} 本</span></div>'
        f'<div>{count}</div>'
        "</div>"
    )


def shelf_book_card(row: sqlite3.Row) -> str:
    tags = [
        row["category"],
        f"{row['publish_year']}年" if row["publish_year"] else "未知年份",
        f"{row['rating']}分" if row["rating"] else "暂无评分",
    ]
    tags_html = "".join(f'<span class="tag">{escape(tag)}</span>' for tag in tags if tag)
    title_html = (
        f'<span>{escape(row["title"])}</span>'
        if row["source_type"] == "article"
        else f'<a href="{escape(row["search_url"])}" target="_blank" rel="noopener noreferrer">{escape(row["title"])}</a>'
    )
    return (
        '<article class="shelf-book">'
        f'<img src="{escape(row["cover"] or "")}" alt="{escape(row["title"])}">'
        "<div>"
        f"<h4>{title_html}</h4>"
        f'<p>{escape(row["author"] or "未知作者")}</p>'
        f'<div class="shelf-tags">{tags_html}</div>'
        "</div>"
        "</article>"
    )


def shelf_section(title: str, description: str, rows: list[sqlite3.Row]) -> str:
    content = "".join(shelf_book_card(row) for row in rows)
    return (
        '<section class="shelf">'
        '<div class="shelf-head">'
        f'<div><h3>{escape(title)}</h3><p>{escape(description)}</p></div>'
        f'<div class="meta-pill">{len(rows)} 册</div>'
        "</div>"
        f'<div class="shelf-grid">{content}</div>'
        "</section>"
    )


def serialize_book(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["book_id"],
        "title": row["title"],
        "author": row["author"],
        "cover": row["cover"],
        "rating": row["rating"],
        "ratingCount": row["rating_count"],
        "intro": row["intro"],
        "category": row["category"],
        "publisher": row["publisher"],
        "publishTime": row["publish_time"],
        "publishYear": row["publish_year"],
        "status": row["reading_status"],
        "sourceType": row["source_type"],
        "url": row["search_url"],
        "sortScore": row["sort_score"],
        "actionLabel": "公众号订阅" if row["source_type"] == "article" else "前往微信读书",
        "sourceLabel": "公众号订阅" if row["source_type"] == "article" else "图书",
        "isExternalLink": row["source_type"] != "article",
    }


def build_html(conn: sqlite3.Connection, output_path: str, db_name: str) -> None:
    total_books = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    unread = conn.execute("SELECT COUNT(*) FROM books WHERE reading_status = 'unread'").fetchone()[0]
    in_progress = conn.execute("SELECT COUNT(*) FROM books WHERE reading_status = 'in_progress'").fetchone()[0]
    finished = conn.execute("SELECT COUNT(*) FROM books WHERE reading_status = 'finished'").fetchone()[0]
    articles = conn.execute("SELECT COUNT(*) FROM books WHERE source_type = 'article'").fetchone()[0]
    recent_books = conn.execute("SELECT COUNT(*) FROM books WHERE publish_year >= 2023").fetchone()[0]
    high_rating = conn.execute("SELECT COUNT(*) FROM books WHERE rating >= 80 AND rating_count >= 20").fetchone()[0]
    rated_books = conn.execute("SELECT COUNT(*) FROM books WHERE rating > 0").fetchone()[0]

    top_categories = fetch_rows(
        conn,
        """
        SELECT category, COUNT(*) AS count
        FROM books
        GROUP BY category
        ORDER BY count DESC, category ASC
        LIMIT 8
        """,
    )
    top_authors = fetch_rows(
        conn,
        """
        SELECT author, COUNT(*) AS count
        FROM books
        WHERE author <> ''
        GROUP BY author
        ORDER BY count DESC, author ASC
        LIMIT 8
        """,
    )

    recent_shelf = fetch_rows(
        conn,
        """
        SELECT *
        FROM books
        ORDER BY publish_year DESC, sort_score DESC
        LIMIT 4
        """,
    )
    unread_gems_shelf = fetch_rows(
        conn,
        """
        SELECT *
        FROM books
        WHERE reading_status = 'unread'
          AND rating >= 75
        ORDER BY rating DESC, rating_count DESC, publish_year DESC
        LIMIT 4
        """,
    )
    in_progress_shelf = fetch_rows(
        conn,
        """
        SELECT *
        FROM books
        WHERE reading_status = 'in_progress'
        ORDER BY sort_score DESC, publish_year DESC
        LIMIT 4
        """,
    )

    all_books = fetch_rows(
        conn,
        """
        SELECT *
        FROM books
        ORDER BY sort_score DESC, publish_year DESC, title ASC
        """
    )

    category_values = [row["category"] for row in fetch_rows(conn, "SELECT DISTINCT category FROM books ORDER BY category ASC")]
    year_values = [str(row["publish_year"]) for row in fetch_rows(conn, "SELECT DISTINCT publish_year FROM books WHERE publish_year > 0 ORDER BY publish_year DESC")]

    metrics_html = "".join(
        [
            metric_card("总藏书", total_books, "包含出版书与公众号内容"),
            metric_card("未开始", unread, "还没翻开的潜在待读清单"),
            metric_card("读过一些", in_progress, "有阅读痕迹但尚未读完"),
            metric_card("已读完", finished, "已经明确标记完成"),
            metric_card("高分精选", high_rating, "评分高且评价人数足够"),
            metric_card("近三年出版", recent_books, "新出版内容的占比观察"),
        ]
    )

    max_category_count = top_categories[0]["count"] if top_categories else 0
    category_html = "".join(category_bar(row["category"], row["count"], max_category_count) for row in top_categories)
    author_html = "".join(author_item(row["author"], row["count"]) for row in top_authors)
    shelves_html = "".join(
        [
            shelf_section("最近入库", "从出版年份和综合排序里挑出最近值得先看的新书。", recent_shelf),
            shelf_section("高分未读", "把口碑不错但还没开始的内容先推到手边。", unread_gems_shelf),
            shelf_section("正在翻阅", "适合当下继续推进的书，别让它们再次沉底。", in_progress_shelf),
        ]
    )

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    books_json = safe_json_dumps([serialize_book(row) for row in all_books])
    category_json = safe_json_dumps(category_values)
    year_json = safe_json_dumps(year_values)

    html = (
        HTML_TEMPLATE.replace("__GENERATED_AT__", escape(generated_at))
        .replace("__DB_NAME__", escape(db_name))
        .replace("__TOTAL_BOOKS__", str(total_books))
        .replace("__METRIC_CARDS__", metrics_html)
        .replace("__CATEGORY_BARS__", category_html)
        .replace("__AUTHOR_LIST__", author_html)
        .replace("__FEATURED_SHELVES__", shelves_html)
        .replace("__BOOKS_JSON__", books_json)
        .replace("__CATEGORY_OPTIONS__", category_json)
        .replace("__YEAR_OPTIONS__", year_json)
    )

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"✅ 已生成图书馆页面：{output_path}")
    print(f"🗄️ SQLite 书库：{os.path.join(os.path.dirname(output_path), db_name)}")
    print(f"📚 总条目：{total_books}，高分精选：{high_rating}，已评分：{rated_books}，公众号：{articles}")

    summary = {
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totalBooks": total_books,
        "unread": unread,
        "inProgress": in_progress,
        "finished": finished,
        "articles": articles,
        "recentBooks": recent_books,
        "highRating": high_rating,
        "ratedBooks": rated_books,
        "topCategories": [
            {"name": row["category"], "count": row["count"]}
            for row in top_categories
        ],
        "topAuthors": [
            {"name": row["author"], "count": row["count"]}
            for row in top_authors
        ],
    }
    summary_path = os.path.join(os.path.dirname(output_path), "last-sync-summary.json")
    with open(summary_path, "w", encoding="utf-8") as summary_file:
        json.dump(summary, summary_file, ensure_ascii=False, indent=2)


def main() -> None:
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, JSON_NAME)
    db_path = os.path.join(base_dir, DB_NAME)
    html_path = os.path.join(base_dir, HTML_NAME)

    print("📖 读取书籍源数据...")
    books = load_books(json_path)
    print(f"🧾 共载入 {len(books)} 条记录")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        print("🗄️ 初始化 SQLite 书库...")
        create_database(conn)
        print("📥 导入书籍到数据库...")
        import_books(conn, books)
        print("🎨 生成个人图书馆页面...")
        build_html(conn, html_path, DB_NAME)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
