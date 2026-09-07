#!/usr/bin/env python3
"""
Northgate prototype — feedback loop (FR13, FR13a), v2 (CSV-backed).

Operates directly on `input/emea_vat_exceptions.csv` — her actual shadow
spreadsheet, now the real knowledge-base file, not a database abstraction.

  1. override  — the analyst reviewed a NEEDS_REVIEW row in the sheet and
     knows the right answer. Her reasoning gets appended as a new row,
     status=pending_review. It does NOT affect any live determination yet
     (FR12a) — this is the point being demonstrated.

  2. approve   — the hub tax manager reviews the candidate and approves it.
     Status flips to approved. Re-running determine.py after this will pick
     it up via RAG retrieval for future transactions in that jurisdiction —
     this is "gets smarter over time," made concrete.

Usage:
    python3 apply_feedback.py override --invoice INV-1005 --jurisdiction FR \\
        --rule "Cross-border services from EU suppliers to Northgate's French \\
                entity: absent an explicit intra-group designation in the \\
                contract, resolve as a fully recoverable taxable third-party supply."

    python3 apply_feedback.py approve --id KB-FR-003 --reviewer "hub tax manager"

    python3 apply_feedback.py list
"""

import argparse
import csv
import os
from datetime import date

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "input")
KB_PATH = os.path.join(INPUT_DIR, "emea_vat_exceptions.csv")
FIELDNAMES = ["id", "status", "jurisdiction", "rule", "added_by", "date", "reviewed_by", "review_date", "origin_transaction"]


def load_kb():
    with open(KB_PATH, newline="") as f:
        return list(csv.DictReader(f))


def save_kb(rows):
    with open(KB_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def next_id(rows, jurisdiction):
    existing = [r["id"] for r in rows if f"-{jurisdiction}-" in r["id"]]
    return f"KB-{jurisdiction}-{len(existing) + 1:03d}"


def cmd_override(args):
    rows = load_kb()
    entry_id = args.id or next_id(rows, args.jurisdiction)
    rows.append({
        "id": entry_id,
        "status": "pending_review",
        "jurisdiction": args.jurisdiction,
        "rule": args.rule,
        "added_by": "reviewing analyst",
        "date": date.today().isoformat(),
        "reviewed_by": "",
        "review_date": "",
        "origin_transaction": args.invoice,
    })
    save_kb(rows)
    print(f"Appended {entry_id} to {os.path.basename(KB_PATH)} — status: pending_review, origin: {args.invoice}")
    print("This entry does NOT affect any determination until it's approved (FR12a).")


def cmd_approve(args):
    rows = load_kb()
    for row in rows:
        if row["id"] == args.id:
            if row["status"] == "approved":
                print(f"{args.id} is already approved.")
                return
            row["status"] = "approved"
            row["reviewed_by"] = args.reviewer
            row["review_date"] = date.today().isoformat()
            save_kb(rows)
            print(f"{args.id} approved by {args.reviewer}.")
            print("Re-run determine.py — future transactions in this jurisdiction will now retrieve this entry (RAG, FR12).")
            return
    print(f"No entry found with id {args.id}")


def cmd_list(args):
    rows = load_kb()
    for r in rows:
        origin = r["origin_transaction"] or "seed (curated migration)"
        print(f"{r['id']:12} [{r['status']:14}] {r['jurisdiction']}  from: {origin}")
        print(f"             {r['rule']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_override = sub.add_parser("override", help="Capture an analyst override as a candidate KB entry")
    p_override.add_argument("--invoice", required=True)
    p_override.add_argument("--jurisdiction", required=True)
    p_override.add_argument("--rule", required=True)
    p_override.add_argument("--id", default=None)
    p_override.set_defaults(func=cmd_override)

    p_approve = sub.add_parser("approve", help="Approve a pending_review entry (hub tax manager)")
    p_approve.add_argument("--id", required=True)
    p_approve.add_argument("--reviewer", default="hub tax manager")
    p_approve.set_defaults(func=cmd_approve)

    p_list = sub.add_parser("list", help="List all knowledge-base entries")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)
