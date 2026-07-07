# Link Audit Commands

## 体检

```bash
python scripts/harness.py audit-links --root content
```

```bash
python scripts/harness.py audit-links --root content/private
```

## 应用计划

```bash
python scripts/harness.py apply-link-plan --plan scripts/link_fix_plan_20260525_round4.json
```

## 直接调用底层脚本

```bash
python scripts/audit_external_links.py --root content --workers 8 --timeout 10
```

```bash
python scripts/apply_link_fixes.py --plan scripts/link_fix_plan_20260525_round4.json
```

## 建议搭配

- 先 `audit-links`
- 再写 `link_fix_plan_*.json`
- 再 `apply-link-plan`
- 最后再次 `audit-links`
