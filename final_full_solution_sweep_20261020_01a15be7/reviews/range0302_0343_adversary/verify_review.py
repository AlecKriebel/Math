#!/usr/bin/env python3
"""Reconcile pinned row differences, source custody, publication manifests and saved live evidence.

No network, checkout/index writes, mutation or external-service writes. This is the
single deliberate reproduction of the initial diff-based classification.
"""
from collections import Counter
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
SWEEP = HERE.parent.parent
REPO = SWEEP.parent
RAW = HERE / "raw/private"
SCOPE = list(range(302, 344))
PUBLICATIONS = {302: (23157237, 26, "30003508"), 305: (23149775, 24, "5100034"),
                311: (23146753, 22, "30005303"), 329: (23137834, 21, "20000450")}
QUEUE = "unsolved_math_prioritization/QUEUE.md"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def read(path):
    return json.loads(path.read_text())


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def main():
    first = {record["pr"]: record for record in read(HERE / "initial_independent_classification.json")["records"]}
    inventory = {record["number"]: record for record in read(RAW / "inventory_scope.json")}
    latest = {record["pr"]: record for record in read(HERE / "live_inventory_checks.json")["records"]}
    checks = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "expected_scope": SCOPE, "scope_complete_contiguous_unique": sorted(first) == SCOPE == sorted(inventory) == sorted(latest),
              "classification_reproduction_method": "Counter difference of complete canonical table rows at merge-base and head, independently of diff hunk context",
              "prs": [], "missing_status_custody": [], "publications": []}
    for number in SCOPE:
        initial = first[number]
        eligibility = read(SWEEP / f"eligibility/pr{number:04d}.json")
        disposition = read(SWEEP / f"PR{number:04d}_DISPOSITION.json")
        head, base = initial["head_sha"], initial["merge_base"]
        head_queue, base_queue = git("show", f"{head}:{QUEUE}"), git("show", f"{base}:{QUEUE}")
        head_rows = Counter(line for line in head_queue.decode().splitlines() if line.startswith("|"))
        base_rows = Counter(line for line in base_queue.decode().splitlines() if line.startswith("|"))
        added_rows = list((head_rows - base_rows).elements())
        parsed = []
        for line in added_rows:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            parsed.append({"problem": cells[1], "status": cells[7], "turns": cells[8], "source_line": line})
        listing = git("ls-tree", "-r", head, "--", *eligibility["changed_paths"]).decode()
        tree = {line.split("\t", 1)[1]: line.split("\t", 1)[0].split()[2] for line in listing.splitlines()}
        expected_tree = {file["filename"]: file["sha"] for file in eligibility["files"] if file["status"] != "removed"}
        item = {"pr": number, "head": head, "merge_base": base,
                "reproduced_added_rows": parsed, "reproduces_initial_diff_rows": added_rows == [row["source_line"] for row in initial["queue_added_rows"]],
                "reproduces_eligibility_added_rows": added_rows == [row["source_line"] for row in eligibility["added_queue_rows"]],
                "all_changed_path_tree_blobs_match_eligibility": tree == expected_tree,
                "changed_file_count": len(tree), "queue_head_blob": blob(head_queue),
                "live_head_matches": latest[number]["head_sha"] == head,
                "live_state_matches": latest[number]["state"] == inventory[number]["state"] == disposition["pr_state"],
                "live_base_matches": latest[number]["base_sha"] == inventory[number]["baseRefOid"] == disposition["inventory_base_sha"],
                "live_body_matches_saved_disposition": sha256(read(RAW / f"pr{number:04d}_live.json")["body"].encode()) == disposition["inventory_body_sha256"],
                "disposition_head_matches": disposition["inventory_head_sha"] == head,
                "root_disposition": disposition["disposition"]}
        if parsed and all(row["status"] in {"unsolved", "already_solved"} for row in parsed):
            item["disposition_follows_explicit_own_added_rows"] = disposition["explicit_pr_queue_statuses"] == [row["status"] for row in parsed] and disposition["disposition"] == "skip_explicit_non_claimed_solved"
        elif parsed:
            item["claimed_solved_has_publication_coverage"] = number in PUBLICATIONS and all((SWEEP / f"PR{number:04d}_{suffix}.json").is_file() for suffix in ["PUBLICATION_VERIFICATION", "PAYLOAD_COVERAGE", "PUBLICATION_LEADS"])
        else:
            item["no_generic_queued_exclusion"] = number in {336, 338} and disposition["disposition"] == "skip_inferred_no_full_solution_claim"
        checks["prs"].append(item)

    for number in [336, 338]:
        initial = first[number]
        snapshot_path = next((SWEEP / "audits").glob(f"pr{number:04d}*/SOURCE_SNAPSHOT.json"))
        snapshot = read(snapshot_path)
        actual_paths = git("diff", "--no-ext-diff", "--no-renames", "--name-only", initial["merge_base"], initial["head_sha"]).decode().splitlines()
        custody = {"pr": number, "snapshot_head_matches": snapshot["head"] == initial["head_sha"],
                   "snapshot_comparison_ref_matches_inventory": snapshot["comparison_base"] == initial["base_sha"],
                   "snapshot_comparison_merge_base_matches": git("merge-base", snapshot["comparison_base"], snapshot["head"]).decode().strip() == initial["merge_base"],
                   "derived_merge_base": initial["merge_base"],
                   "snapshot_paths_complete": actual_paths == sorted(snapshot["exact_pinned_changed_paths"]) == sorted(entry["repository_path"] for entry in snapshot["files"]),
                   "no_actual_queue_change": QUEUE not in actual_paths, "files": []}
        for entry in snapshot["files"]:
            data = git("show", f"{initial['head_sha']}:{entry['repository_path']}")
            custody["files"].append({"path": entry["repository_path"], "bytes": len(data),
                                     "git_blob": blob(data), "sha256": sha256(data),
                                     "snapshot_git_blob_matches": entry["git_blob"] == blob(data),
                                     "snapshot_sha256_matches": entry["sha256"] == sha256(data),
                                     "snapshot_bytes_match": entry["bytes"] == len(data),
                                     "snapshot_local_bytes_match": (snapshot_path.parent / entry["local"]).read_bytes() == data,
                                     "independent_local_bytes_match": (RAW / f"pr{number:04d}_pinned" / entry["local"].removeprefix("original/")).read_bytes() == data})
        checks["missing_status_custody"].append(custody)

    rows = read(RAW / "ledger_formula.json")["values"]
    fetched = {record["pr"]: record for record in read(HERE / "publications_fresh.json")}
    checks["ledger"] = {"saved_file_sha256": sha256((RAW / "ledger_formula.json").read_bytes()),
                        "range": read(RAW / "ledger_formula.json")["range"], "rows": len(rows),
                        "retrieval": "gws sheets spreadsheets values get, FORMULA, full A1:AQ range; read-only"}
    for number, (record, row_number, problem_id) in PUBLICATIONS.items():
        directory = RAW / f"publication_pr{number:04d}"
        current = fetched[number]
        metadata = read(directory / "record.json")
        root = read(SWEEP / f"PR{number:04d}_PUBLICATION_VERIFICATION.json")
        lead = read(SWEEP / f"PR{number:04d}_PUBLICATION_LEADS.json")
        row = rows[row_number - 1]
        doi = f"10.5281/zenodo.{record}"
        exact_pr = re.compile(rf"https://github\.com/AlecKriebel/Math/pull/{number}(?!\d)")
        exact_id = re.compile(rf"(?<!\d){problem_id}(?!\d)")
        pr_rows = [i + 1 for i, value in enumerate(rows) if exact_pr.search(" ".join(map(str, value)))]
        id_rows = [i + 1 for i, value in enumerate(rows) if exact_id.search(" ".join(map(str, value)))]
        doi_rows = [i + 1 for i, value in enumerate(rows) if any(doi in str(cell).lower() for cell in value)]
        item = {"pr": number, "record": record, "doi": doi, "ledger_row": row_number,
                "current_doi_matches": current["doi"] == doi == metadata["doi"] == root["doi"],
                "published": metadata["submitted"] is True and metadata["state"] == "done",
                "doi_resolves_correct_record": current["doi_resolution"]["http_status"] == 200 and current["doi_resolution"]["final_url"].rstrip("/") == f"https://zenodo.org/records/{record}",
                "ledger_primary_doi_matches": len(row) > 2 and row[2] == "https://doi.org/" + doi,
                "unique_PR_row": pr_rows == [row_number], "unique_problem_row": id_rows == [row_number],
                "unique_DOI_row": doi_rows == [row_number],
                "ledger_matches_root_lead": any(match["row"] == row_number and match["values"] == row[:4] for match in lead["matches"]),
                "title_matches": current["title"] == root["title"], "files": []}
        for file in current["files"]:
            data = (directory / file["name"]).read_bytes()
            check = {"name": file["name"], "bytes": len(data), "sha256": sha256(data),
                     "record_size_matches": file["record_size_matches"], "record_checksum_matches": file["record_checksum_matches"],
                     "root_size_matches": file["root_size_matches"], "root_sha256_matches": file["root_sha256_matches"]}
            if file["name"].endswith(".zip"):
                with zipfile.ZipFile(directory / file["name"]) as archive:
                    members = archive.namelist()
                    manifests = [name for name in members if name == "MANIFEST.json" or name.endswith("/MANIFEST.json")]
                    if len(manifests) != 1:
                        raise AssertionError(f"ambiguous archive manifest PR{number}")
                    manifest_name = manifests[0]
                    manifest = json.loads(archive.read(manifest_name))
                    prefix = str(Path(manifest_name).parent)
                    prefix = "" if prefix == "." else prefix + "/"
                    payload = manifest.get("payload", manifest.get("files", manifest))
                    if isinstance(payload, list):
                        payload = {entry["path"]: entry for entry in payload}
                    declarations = {prefix + name: entry for name, entry in payload.items()}
                    files_only = [name for name in members if not name.endswith("/")]
                    check.update(zip_crc_ok=archive.testzip() is None,
                                 duplicate_members_absent=len(members) == len(set(members)),
                                 exact_declared_file_set=set(files_only) == set(declarations) | {manifest_name},
                                 declared_payloads=len(declarations), file_members=len(files_only), directory_entries=len(members) - len(files_only),
                                 root_member_set_matches=file["root_members_match"], payloads=[])
                    for name, declaration in declarations.items():
                        body = archive.read(name)
                        check["payloads"].append({"name": name, "bytes": len(body), "sha256": sha256(body),
                                                  "declared_bytes_match": len(body) == declaration["bytes"],
                                                  "declared_sha256_matches": sha256(body) == declaration["sha256"]})
            item["files"].append(check)
        checks["publications"].append(item)
    (HERE / "checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    false_values = []
    def walk(value, path=""):
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, path + "." + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path + f"[{index}]")
        elif value is False:
            false_values.append(path)
    walk(checks)
    summary = {"42_prs_verified": len(checks["prs"]), "status_counts": dict(Counter(row["status"] for item in checks["prs"] for row in item["reproduced_added_rows"])),
               "claimed_solved_PRs": sorted(PUBLICATIONS), "missing_status_files_verified": sum(len(item["files"]) for item in checks["missing_status_custody"]),
               "publication_payloads_verified": sum(file.get("declared_payloads", 0) for item in checks["publications"] for file in item["files"]),
               "false_checks": false_values}
    (HERE / "checks_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if false_values:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
