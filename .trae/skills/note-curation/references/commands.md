# Note Curation Commands

## 常用配套命令

### 抓取链接内容

```bash
python scripts/harness.py fetch-link-content --from-md content/AI/开发与Agent/AI-Coding-与-Agent.md
```

### 公共知识库 lint

```bash
python scripts/harness.py wiki-lint --content-dir content --strict
```

### Unity 专题索引重建

```bash
python scripts/harness.py build-topic-index
```

### 外链体检

```bash
python scripts/harness.py audit-links --root content
```

### 应用外链修复计划

```bash
python scripts/harness.py apply-link-plan --plan scripts/link_fix_plan_20260525_round4.json
```
