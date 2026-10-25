#!/usr/bin/env python3
"""Refresh tracker/data/processing-times.json from IRCC's published processing-time data.

Runs weekly in GitHub Actions (see .github/workflows/update-processing-times.yml).
Standard library only. Usage:
    python3 scripts/update_ircc_times.py                 # fetch live from canada.ca
    python3 scripts/update_ircc_times.py --from-dir DIR  # use saved IRCC JSON files (testing)
"""
import argparse
import datetime as dt
import json
import pathlib
import sys
import urllib.request

BASE = "https://www.canada.ca/content/dam/ircc/documents/json/"
FILES = {
    "country": "data-ptime-en.json",
    "non_country": "data-ptime-non-country-en.json",
    "pr": "flpt-en.json",
}
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tracker" / "data" / "processing-times.json"
NAMES = ROOT / "tracker" / "data" / "country-names.json"

# IRCC key -> app visa id (applications made from outside Canada, by country)
COUNTRY_PROGRAMS = {
    "visitor-outside-canada": "trv",
    "supervisa": "super",
    "study": "study",
    "work": "work",
}

# Times that do not vary by country: (visa id, label, source file, section, key)
PROGRAMS = [
    ("trv", "Visitor visa, applying from inside Canada", "non_country", "visitor_inside_canada", "visitor_inside_canada"),
    ("trv", "Extending a visit (visitor record)", "non_country", "visitor_extension", "visitor_extension"),
    ("trv", "Electronic travel authorization (eTA)", "non_country", "eta", "eta"),
    ("study", "Extending a study permit from inside Canada", "non_country", "study_extension", "study_extension"),
    ("work", "Extending a work permit from inside Canada", "non_country", "work_extension", "work_extension"),
    ("work", "International Experience Canada (working holiday)", "non_country", "iec", "iec"),
    ("ee", "Canadian Experience Class", "pr", "current-flpt", "cec"),
    ("ee", "Federal Skilled Worker", "pr", "current-flpt", "fsw"),
    ("ee", "Federal Skilled Trades", "non_country", "fed_skilled_trades", "skilled_trades_ee"),
    ("pnp", "Provincial nominee, through Express Entry", "pr", "current-flpt", "pnp-ee"),
    ("pnp", "Provincial nominee, paper (base) stream", "pr", "current-flpt", "pnp-base"),
    ("family", "Spouse or partner living outside Canada (outside Quebec)", "pr", "current-flpt", "spousal-abroad-roc"),
    ("family", "Spouse or partner living in Canada (outside Quebec)", "pr", "current-flpt", "spousal-canada-roc"),
    ("family", "Spouse or partner living outside Canada (Quebec)", "pr", "current-flpt", "spousal-abroad-quebec"),
    ("family", "Spouse or partner living in Canada (Quebec)", "pr", "current-flpt", "spousal-canada-quebec"),
    ("family", "Parents and grandparents (outside Quebec)", "pr", "current-flpt", "pgp-roc"),
    ("family", "Parents and grandparents (Quebec)", "pr", "current-flpt", "pgp-quebec"),
    ("family", "Dependent children living outside Canada (outside Quebec)", "pr", "current-flpt", "dependants-abroad-roc"),
    ("pr", "PR card for a new permanent resident", "non_country", "pr_card", "new_pr"),
    ("pr", "Renewing a PR card", "non_country", "pr_card", "existing_pr"),
]


def fetch(name):
    req = urllib.request.Request(
        BASE + name,
        headers={"User-Agent": "Mozilla/5.0 (compatible; KTIS-tracker/1.0; +https://kevinthibbles.com)",
                 "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8-sig"))


def load(from_dir):
    raw = {}
    for k, name in FILES.items():
        raw[k] = json.loads((pathlib.Path(from_dir) / name).read_text("utf-8-sig")) if from_dir else fetch(name)
    return raw


def build(raw, names):
    country = raw["country"]
    by_country, updated_temp = {}, None
    for ircc_key, visa in COUNTRY_PROGRAMS.items():
        block = country.get(ircc_key)
        if not isinstance(block, dict):
            raise SystemExit(f"IRCC data is missing '{ircc_key}'; the format may have changed.")
        updated_temp = updated_temp or block.get("lastupdated")
        by_country[visa] = {c: v for c, v in block.items() if len(c) == 2 and isinstance(v, str)}
        for c in by_country[visa]:
            names.setdefault(c, c)

    programs = []
    for visa, label, src, section, key in PROGRAMS:
        val = (raw[src].get(section) or {}).get(key)
        if isinstance(val, str) and val.strip():
            programs.append({"visa": visa, "application": label, "time": val.strip()})

    nc_update = (raw["non_country"].get("default-update") or {}).get("lastupdated")
    pr_update = (raw["pr"].get("default-update") or {}).get("flpt_lastupdated")
    total = sum(len(v) for v in by_country.values())
    if total < 400 or len(programs) < 10:
        raise SystemExit(f"Refusing to write: only {total} country values and {len(programs)} programs found.")
    return {
        "source": "Immigration, Refugees and Citizenship Canada (IRCC), canada.ca processing-times data",
        "updated_temporary": updated_temp or nc_update,
        "updated_pr": pr_update,
        "fetched_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "by_country": by_country,
        "programs": programs,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-dir", help="read IRCC JSON files from this folder instead of canada.ca")
    args = ap.parse_args()
    names = json.loads(NAMES.read_text("utf-8")) if NAMES.exists() else {}
    data = build(load(args.from_dir), names)
    old = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    same = {k: v for k, v in old.items() if k != "fetched_at"} == {k: v for k, v in data.items() if k != "fetched_at"}
    if same:
        print("No change in IRCC processing times.")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", "utf-8")
    NAMES.write_text(json.dumps(dict(sorted(names.items())), ensure_ascii=False, indent=1) + "\n", "utf-8")
    print(f"Updated: temporary {data['updated_temporary']}, PR {data['updated_pr']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
