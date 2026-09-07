#!/usr/bin/env python3
"""
Northgate prototype — feedback loop (FR13, FR13a).

The trust-building mechanism, demoed as two commands:

  1. override  — the analyst reviewed a NEEDS_REVIEW row in the sheet and
     knows the right answer. Her reasoning gets captured as a new candidate
     knowledge-base entry, status=pending_review. It does NOT affect any
     live determination yet (FR12a) — this is the point being demonstrated.

  2. approve   — the hub tax manager reviews the candidate and approves it.
     Status flips to approved. Re-running determine.py after this will pick
     it up via RAG retrieval (retrieve_kb_context) for future transactions
     in that jurisdiction — this is "gets smarter over time," made concrete.

Usage:
    python3 apply_feedback.py override --invoice INV-1005 --jurisdiction FR \\
        --rule "Cross-border services from EU suppliers to Northgate's French \\
                entity: absent an explicit intra-group designation in the \\
                contract, resolve as a fully recoverable taxable third-party supply."

    python3 apply_feedback.py approve --id KB-FR-003 --reviewer "hub tax manager"

    python3 apply_feedback.py list
"""

import argparse
import json
import os
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
KB_PATH = os.path.join(DATA_DIR, "knowledge_base.json")


def load_kb():
    with open(KB_PATH) as f:
        return json.load(f)


def save_kb(doc):
    with open(KB_PATH, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")


def next_id(doc, jurisdiction):
    existing = [e["id"] for e in doc["knowledge_base_entries"] if f"-{jurisdiction}-" in e["id"]]
    n = len(existing) + 1
    return f"KB-{jurisdiction}-{n:03d}"


def cmd_override(args):
    doc = load_kb()
    entry_id = args.id or next_id(doc, args.jurisdiction)
    entry = {
        "id": entry_id,
        "status": "pending_review",
        "jurisdiction": args.jurisdiction,
        "rule": args.rule,
        "provenance": {
            "source": "Analyst override, captured directly from the review sheet",
            "added_by": "reviewing analyst",
            "date": date.today().isoformat(),
            "reviewed_by": None,
            "review_date": None,
        },
        "origin_transaction": args.invoice,
    }
    doc["knowledge_base_entries"].append(entry)
    save_kb(doc)
    print(f"Created {entry_id} — status: pending_review, origin: {args.invoice}")
    print("This entry does NOT affect any determination until it's approved (FR12a).")


def cmd_approve(args):
    doc = load_kb()
    for entry in doc["knowledge_base_entries"]:
        if entry["id"] == args.id:
            if entry["status"] == "approved":
                print(f"{args.id} is already approved.")
                return
            entry["status"] = "approved"
            entry["provenance"]["reviewed_by"] = args.reviewer
            entry["provenance"]["review_date"] = date.today().isoformat()
            save_kb(doc)
            print(f"{args.id} approved by {args.reviewer}.")
            print("Re-run determine.py — future transactions in this jurisdiction will now retrieve this entry (RAG, FR12).")
            return
    print(f"No entry found with id {args.id}")


def cmd_list(args):
    doc = load_kb()
    for e in doc["knowledge_base_entries"]:
        origin = e["origin_transaction"] or "seed (curated migration)"
        print(f"{e['id']:12} [{e['status']:14}] {e['jurisdiction']}  from: {origin}")
        print(f"             {e['rule']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_override = sub.add_parser("override", help="Capture an analyst override as a candidate KB entry")
    p_override.add_argument("--invoice", required=True, help="Origin invoice id, e.g. INV-1005")
    p_override.add_argument("--jurisdiction", required=True, help="Jurisdiction code, e.g. FR")
    p_override.add_argument("--rule", required=True, help="Plain-language rule, in her own words")
    p_override.add_argument("--id", default=None, help="Optional explicit id, otherwise auto-generated")
    p_override.set_defaults(func=cmd_override)

    p_approve = sub.add_parser("approve", help="Approve a pending_review entry (hub tax manager)")
    p_approve.add_argument("--id", required=True, help="Entry id, e.g. KB-FR-003")
    p_approve.add_argument("--reviewer", default="hub tax manager", help="Who approved it")
    p_approve.set_defaults(func=cmd_approve)

    p_list = sub.add_parser("list", help="List all knowledge-base entries")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)
