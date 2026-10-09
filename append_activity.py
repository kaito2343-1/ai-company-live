#!/usr/bin/env python3
"""Append trusted-owner GitHub issue *declarations* to the public dashboard feed.
This does not verify claims, publish posts or read ChatGPT Work execution logs.
"""
import datetime
import json
import os
import pathlib
import re
import sys
from urllib.parse import urlparse

FIELD_NAMES = {
    "事業": "business", "担当役員": "role", "作業状況": "status",
    "作業内容": "summary", "成果物URL（任意）": "evidence",
}
ROLE_SET = {"CEO", "COO", "CMO", "CPO", "CIO", "CGO", "法務", "品質", "調査"}
STATUS_SET = {"企画中", "制作中", "確認待ち", "完成（未公開）", "公開（本人申告）", "確認済み（本人申告）"}


def parse_sections(body):
    fields = {}
    current = None
    for line in body.splitlines():
        if line.startswith("### "):
            key = line[4:].strip()
            current = FIELD_NAMES.get(key)
            if current:
                fields[current] = []
        elif current:
            fields[current].append(line)
    return {key: "\n".join(value).strip() for key, value in fields.items()}


def https_url(value):
    if not value or value == "_No response_":
        return ""
    url = urlparse(value)
    if url.scheme != "https" or not url.netloc or re.search(r"\s", value):
        raise ValueError("成果物URLはhttps://で始まるURLか空欄にしてください")
    return value[:700]


def make_record(event):
    issue = event["issue"]
    fields = parse_sections(issue.get("body") or "")
    business = fields.get("business", "").split("｜")[0].strip()
    role = fields.get("role", "").split("｜")[0].strip()
    status = fields.get("status", "").strip()
    summary = fields.get("summary", "").strip()
    if business not in {"bunko", "kakemaru"}:
        raise ValueError("事業が不正です。フォームから登録してください")
    if role not in ROLE_SET or status not in STATUS_SET:
        raise ValueError("担当または状況が不正です。フォームから登録してください")
    if not 2 <= len(summary) <= 500:
        raise ValueError("作業内容は2～500文字で入力してください")
    url = issue.get("html_url", "")
    if not (url.startswith("https://github.com/") and "/issues/" in url):
        raise ValueError("Issue URLが不正です")
    return {
        "id": f"github-issue-{issue['number']}",
        "business": business,
        "role": role,
        "summary": summary,
        "status": status,
        "at": issue["created_at"],
        "source": "github_issue",
        "verification": "本人申告・未検証",
        "issueUrl": url,
        "evidence": https_url(fields.get("evidence", "")),
    }


def main():
    event_path = pathlib.Path(os.environ["GITHUB_EVENT_PATH"])
    event = json.loads(event_path.read_text(encoding="utf-8"))
    issue = event["issue"]
    repository_owner = event["repository"]["owner"]["login"]
    if issue["user"]["login"] != repository_owner:
        raise ValueError("リポジトリ所有者以外のIssueは拒否しました")
    if not issue.get("title", "").startswith("[実績]"):
        raise ValueError("実績ログではないIssueです")
    record = make_record(event)
    path = pathlib.Path(os.environ.get("ACTIVITY_FILE", "activity.json"))
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "schemaVersion": 1, "records": [], "metrics": {
            "bunko": {"posts": None, "articles": None, "sales": None, "revenue": None, "updatedAt": "未取得"},
            "kakemaru": {"posts": None, "articles": None, "sales": None, "revenue": None, "updatedAt": "未取得"},
        }}
    records = data.get("records", [])
    records = [r for r in records if r.get("id") != record["id"]]
    records.insert(0, record)
    data["records"] = sorted(records, key=lambda r: r.get("at", ""), reverse=True)[:500]
    data["schemaVersion"] = 1
    data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    data["notes"] = "GitHub Issue上の所有者の自己申告。作業実施や公開をAPIで検証したものではありません。数値KPIは別途確認が必要。"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"記録更新: {record['id']} / {record['business']} / {record['role']} / {record['status']}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"記録できませんでした: {e}", file=sys.stderr)
        sys.exit(1)
