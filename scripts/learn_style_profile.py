#!/usr/bin/env python3
"""Build a local, opt-in figure-style profile from explicit user feedback.

This performs preference aggregation, not model-weight training. It never reads
raw manuscript/image contents and writes only the style attributes supplied in
feedback records.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ALLOWED_ATTRIBUTES = {
    "palette", "font_family", "font_size", "line_width", "marker_size",
    "layout", "legend_position", "panel_spacing", "background",
    "axis_style", "annotation_style", "export_preference",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"Line {line_no} must contain a JSON object")
            records.append(item)
    return records


def normalize_rating(value: Any) -> int:
    if value in (1, "accept", "accepted", "like"):
        return 1
    if value in (-1, "reject", "rejected", "dislike"):
        return -1
    if value in (0, "neutral"):
        return 0
    raise ValueError("rating must be accept/reject/neutral or 1/-1/0")


def build_profile(records: list[dict[str, Any]], min_support: int = 2) -> dict[str, Any]:
    """Choose most consistently accepted attribute values per figure type."""
    counts: dict[str, dict[str, dict[str, list[int]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    )
    valid_records = 0
    for idx, record in enumerate(records, 1):
        figure_type = record.get("figure_type")
        attrs = record.get("attributes")
        if not isinstance(figure_type, str) or not figure_type.strip():
            raise ValueError(f"Record {idx}: figure_type must be a non-empty string")
        if not isinstance(attrs, dict):
            raise ValueError(f"Record {idx}: attributes must be an object")
        rating = normalize_rating(record.get("rating"))
        for key, value in attrs.items():
            if key not in ALLOWED_ATTRIBUTES:
                continue
            if value is None or isinstance(value, (dict, list)):
                continue
            bucket = counts[figure_type][key][str(value)]
            bucket[0] += 1
            if rating > 0:
                bucket[1] += 1
            elif rating < 0:
                bucket[2] += 1
        valid_records += 1

    preferences: dict[str, Any] = {}
    evidence: dict[str, Any] = {}
    for figure_type, attrs in counts.items():
        preferences[figure_type] = {}
        evidence[figure_type] = {}
        for key, values in attrs.items():
            ranked = []
            for value, (total, accepted, rejected) in values.items():
                support = accepted + rejected
                score = accepted - rejected
                ranked.append((score, support, accepted, value, total, rejected))
            ranked.sort(key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)
            if not ranked:
                continue
            score, support, accepted, value, total, rejected = ranked[0]
            if support >= min_support and score > 0:
                preferences[figure_type][key] = value
            evidence[figure_type][key] = {
                "candidate_counts": {
                    v: {"observations": n, "accepted": a, "rejected": r}
                    for v, (n, a, r) in values.items()
                },
                "selected": value if support >= min_support and score > 0 else None,
                "support": support,
            }

    return {
        "schema_version": 1,
        "profile_kind": "local_figure_style_preferences",
        "training_method": "explicit_feedback_aggregation_not_model_training",
        "records_processed": valid_records,
        "min_support": min_support,
        "preferences_by_figure_type": preferences,
        "evidence": evidence,
        "privacy": {
            "contains_raw_manuscript_or_image_data": False,
            "source": "user-provided explicit feedback records",
            "storage": "local file chosen by the user",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feedback", type=Path, help="JSONL feedback file")
    parser.add_argument("--output", type=Path, default=Path("style_profile.json"))
    parser.add_argument("--min-support", type=int, default=2,
                        help="minimum non-neutral feedback count before applying a preference (default: 2)")
    args = parser.parse_args()
    if args.min_support < 1:
        parser.error("--min-support must be at least 1")
    records = load_jsonl(args.feedback)
    profile = build_profile(records, args.min_support)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Processed {profile['records_processed']} feedback records; wrote {args.output}")


if __name__ == "__main__":
    main()
