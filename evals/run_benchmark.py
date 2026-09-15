#!/usr/bin/env python3
"""Prepare and summarize the frozen Xiaoyibao A/B/C/D benchmark.

This runner does not call a language model. It validates a user-supplied,
frozen dataset, creates deterministic blind copies, prepares score templates,
and summarizes completed reviews.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import statistics
from pathlib import Path


VARIANTS = ("A", "B", "C", "D")
METRICS = (
    "naturalness",
    "human_voice",
    "ai_pattern",
    "medical_accuracy",
    "fear_control",
    "hope_control",
    "meaning_preservation",
    "information_density",
    "authorial_authenticity",
)
WEIGHTS = {
    "naturalness": 0.20,
    "human_voice": 0.20,
    "ai_pattern": 0.10,
    "medical_accuracy": 0.20,
    "fear_control": 0.10,
    "hope_control": 0.05,
    "meaning_preservation": 0.10,
    "information_density": 0.05,
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def validate_manifest(manifest_path: Path, require_frozen: bool = True):
    manifest = load_json(manifest_path)
    expected = manifest.get("expected_count")
    items = manifest.get("items")
    if expected != 20:
        raise ValueError("expected_count must be 20 for the v0.3 baseline")
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if len(items) != expected:
        raise ValueError(f"manifest has {len(items)} items; expected {expected}")
    if require_frozen and manifest.get("frozen") is not True:
        raise ValueError("dataset is not frozen")

    ids = [item.get("id") for item in items]
    if any(not value for value in ids):
        raise ValueError("every item needs a non-empty id")
    if len(set(ids)) != len(ids):
        raise ValueError("item ids must be unique")

    base = manifest_path.parent
    missing = []
    for item in items:
        item_dir = base / item["id"]
        required = ("A", "B", "C", "D") if item.get("has_human_edit") else ("A", "B", "C")
        for variant in required:
            path = item_dir / f"{variant}.txt"
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                missing.append(str(path))
    if missing:
        raise ValueError("missing required text files:\n" + "\n".join(missing))
    return manifest


def prepare(manifest_path: Path, result_dir: Path, seed: int) -> None:
    manifest = validate_manifest(manifest_path)
    rng = random.Random(seed)
    mapping = {
        "dataset_version": manifest["dataset_version"],
        "seed": seed,
        "items": {},
    }

    for item in manifest["items"]:
        item_id = item["id"]
        source_dir = manifest_path.parent / item_id
        available = list(VARIANTS if item.get("has_human_edit") else VARIANTS[:3])
        rng.shuffle(available)
        blind_map = {}
        blind_dir = result_dir / "raw" / item_id
        blind_dir.mkdir(parents=True, exist_ok=True)
        for index, variant in enumerate(available, start=1):
            label = f"Version {index}"
            blind_map[label] = variant
            shutil.copyfile(source_dir / f"{variant}.txt", blind_dir / f"{label}.txt")

        mapping["items"][item_id] = blind_map
        score_template = {
            "id": item_id,
            "reviewers": [
                {
                    "reviewer_id": "",
                    "versions": {
                        label: {metric: None for metric in METRICS}
                        for label in blind_map
                    },
                    "needs_expert_review": False,
                    "notes": "",
                }
            ],
        }
        write_json(result_dir / "scores" / f"{item_id}.json", score_template)

    write_json(result_dir / "blind-map.json", mapping)


def score_gate(scores: dict) -> str:
    if scores["medical_accuracy"] < 4:
        return "FAIL_MEDICAL_ACCURACY"
    if scores["meaning_preservation"] < 4:
        return "FAIL_MEANING_PRESERVATION"
    if scores["fear_control"] <= 2:
        return "FAIL_FEAR_CONTROL"
    return "PASS"


def summarize(result_dir: Path) -> None:
    mapping = load_json(result_dir / "blind-map.json")
    by_variant = {variant: [] for variant in VARIANTS}
    failures = []

    for item_id, blind_map in mapping["items"].items():
        score_file = result_dir / "scores" / f"{item_id}.json"
        data = load_json(score_file)
        reviewers = data.get("reviewers", [])
        for label, variant in blind_map.items():
            completed = []
            for reviewer in reviewers:
                values = reviewer.get("versions", {}).get(label, {})
                if all(isinstance(values.get(metric), (int, float)) for metric in METRICS):
                    completed.append(values)
            if not completed:
                continue
            average = {
                metric: statistics.fmean(row[metric] for row in completed)
                for metric in METRICS
            }
            weighted = sum(average[metric] * weight for metric, weight in WEIGHTS.items())
            gate = score_gate(average)
            by_variant[variant].append(
                {
                    "id": item_id,
                    "weighted_score": round(weighted, 3),
                    "gate": gate,
                    "scores": {key: round(value, 3) for key, value in average.items()},
                }
            )
            if gate != "PASS":
                failures.append({"id": item_id, "variant": variant, "gate": gate})

    summary = {
        "dataset_version": mapping["dataset_version"],
        "variants": {},
        "failures": failures,
    }
    for variant, rows in by_variant.items():
        summary["variants"][variant] = {
            "completed_items": len(rows),
            "mean_weighted_score": (
                round(statistics.fmean(row["weighted_score"] for row in rows), 3)
                if rows
                else None
            ),
            "items": rows,
        }
    write_json(result_dir / "summaries" / "summary.json", summary)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("manifest", type=Path)
    validate.add_argument("--allow-unfrozen", action="store_true")

    prep = sub.add_parser("prepare")
    prep.add_argument("manifest", type=Path)
    prep.add_argument("result_dir", type=Path)
    prep.add_argument("--seed", type=int, default=20260902)

    report = sub.add_parser("summarize")
    report.add_argument("result_dir", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "validate":
        validate_manifest(args.manifest, require_frozen=not args.allow_unfrozen)
        print("manifest valid")
    elif args.command == "prepare":
        prepare(args.manifest, args.result_dir, args.seed)
        print("blind benchmark prepared")
    elif args.command == "summarize":
        summarize(args.result_dir)
        print("summary written")


if __name__ == "__main__":
    main()
