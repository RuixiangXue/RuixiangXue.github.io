from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "jobs" / "pipeline.json"


def load_pipeline() -> dict[str, Any]:
    return json.loads(PIPELINE.read_text(encoding="utf-8"))


def save_pipeline(data: dict[str, Any]) -> None:
    PIPELINE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    chars = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        elif chars and chars[-1] != "-":
            chars.append("-")
    return "".join(chars).strip("-") or "job"


def list_jobs() -> None:
    jobs = load_pipeline().get("jobs", [])
    for index, job in enumerate(jobs, start=1):
        print(
            f"{index}. [{job.get('status', '')}] {job.get('company', '')} - {job.get('role', '')} "
            f"| next: {job.get('next_action', '')} ({job.get('next_action_date', '')})"
        )


def add_job(args: argparse.Namespace) -> None:
    data = load_pipeline()
    slug = slugify(f"{args.company}-{args.role}")
    target_file = args.target or "targets/default.json"
    resume_file = args.resume or f"assets/cv/resume-{slug}.html"
    jd_file = f"jobs/jd/{slug}.md"
    notes_file = f"jobs/notes/{slug}.md"
    job = {
        "company": args.company,
        "role": args.role,
        "source": args.source,
        "location": args.location,
        "status": args.status,
        "priority": args.priority,
        "deadline": args.deadline,
        "jd_file": jd_file,
        "target_file": target_file,
        "resume_file": resume_file,
        "contacts": [],
        "next_action": args.next_action,
        "next_action_date": args.next_action_date,
        "notes": args.notes,
    }
    data.setdefault("jobs", []).append(job)
    save_pipeline(data)
    jd_path = ROOT / jd_file
    notes_path = ROOT / notes_file
    jd_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    if not jd_path.exists():
        jd_path.write_text(f"# {args.company} - {args.role}\n\nPaste JD here.\n", encoding="utf-8")
    if not notes_path.exists():
        notes_path.write_text(f"# {args.company} - {args.role} Notes\n\n- Status: {args.status}\n", encoding="utf-8")
    print(f"added: {args.company} - {args.role}")


def update_status(args: argparse.Namespace) -> None:
    data = load_pipeline()
    for job in data.get("jobs", []):
        if slugify(f"{job.get('company', '')}-{job.get('role', '')}") == args.slug:
            job["status"] = args.status
            if args.next_action:
                job["next_action"] = args.next_action
            if args.next_action_date:
                job["next_action_date"] = args.next_action_date
            save_pipeline(data)
            print(f"updated: {args.slug} -> {args.status}")
            return
    raise SystemExit(f"job not found: {args.slug}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage the local job-search pipeline.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list")

    add = sub.add_parser("add")
    add.add_argument("--company", required=True)
    add.add_argument("--role", required=True)
    add.add_argument("--source", default="")
    add.add_argument("--location", default="")
    add.add_argument("--status", default="to_apply")
    add.add_argument("--priority", default="medium")
    add.add_argument("--deadline", default="")
    add.add_argument("--target", default="")
    add.add_argument("--resume", default="")
    add.add_argument("--next-action", default="Tailor resume and prepare application")
    add.add_argument("--next-action-date", default="")
    add.add_argument("--notes", default="")

    status = sub.add_parser("status")
    status.add_argument("slug")
    status.add_argument("status")
    status.add_argument("--next-action", default="")
    status.add_argument("--next-action-date", default="")

    args = parser.parse_args()
    if args.command == "list":
        list_jobs()
    elif args.command == "add":
        add_job(args)
    elif args.command == "status":
        update_status(args)


if __name__ == "__main__":
    main()
