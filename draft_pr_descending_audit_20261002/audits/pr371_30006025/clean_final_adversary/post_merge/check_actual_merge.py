#!/usr/bin/env python3
"""Read-only independent actual merge readback; default output remains private."""
import argparse
import base64
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import traceback

ROOT = Path(__file__).resolve().parent
MERGE = "6466f4a301c94d513435401bf772c285bc7b4c42"
HEAD = "212d6c498026765966bbe01ebe3ea09a76bb215f"
BASE = "41b15a086acb109f1707320dbe5db39778cdceca"
TREE = "bd83cce0cde75f29b0cbc469e33f01e9230fd511"
PUBLISHED = "1836407486e6cea540bb9b5e33e05b9c04d83272"
FROZEN = "51fddd150e8da33f4cf17b1a642a0ffd3466bf5d"
PREFIX = "problems/30006025_geometric_chapuy/"
AUDIT = "draft_pr_descending_audit_20261002/audits/pr371_30006025/"
OWN = AUDIT + "clean_final_adversary/"
QUEUE = "unsolved_math_prioritization/QUEUE.md"


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    run = ROOT / "private" / ("run_" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    run.mkdir(parents=True)
    receipt_path = args.receipt.resolve() if args.receipt else run / "receipt.json"
    receipt = {"started_utc": now(), "actual_merge": MERGE, "reviewed_head": HEAD, "premerge_base": BASE,
               "tree": TREE, "status": "RUNNING", "raw_storage": str(run.relative_to(ROOT)), "checks": []}

    def check(condition, name, **details):
        receipt["checks"].append({"name": name, "passed": bool(condition), **details})
        if not condition:
            raise AssertionError(name)

    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args])

    def data(rev, path):
        return git("show", rev + ":" + path)

    def obj(rev, path):
        return json.loads(data(rev, path))

    def api(label, path):
        proc = subprocess.run(["gh", "api", "repos/AlecKriebel/Math/" + path], capture_output=True)
        (run / (label + ".stdout")).write_bytes(proc.stdout)
        (run / (label + ".stderr")).write_bytes(proc.stderr)
        if proc.returncode:
            raise RuntimeError(label + ": GitHub read failed, exit " + str(proc.returncode))
        return json.loads(proc.stdout)

    def tree(rev, recursive=True):
        raw = git("ls-tree", *(["-r"] if recursive else []), "-z", rev)
        entries = {}
        for row in raw.split(b"\0"):
            if row:
                fields, path = row.split(b"\t", 1)
                mode, kind, identity = fields.decode().split()
                entries[path.decode()] = {"mode": mode, "type": kind, "sha": identity}
        return entries, {"entries": len(entries), "raw_bytes": len(raw), "raw_sha256": sha(raw)}

    def observe(label):
        pr = api(label + "_pr", "pulls/371")
        current_main = api(label + "_main", "git/ref/heads/main")["object"]["sha"]
        actual = api(label + "_actual_merge", "git/commits/" + MERGE)
        compare = api(label + "_main_ancestry", "compare/" + MERGE + "..." + current_main)
        local_main = git("rev-parse", "refs/heads/main").decode().strip()
        local_ancestor = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", MERGE, local_main], capture_output=True)
        body = data(PUBLISHED, AUDIT + "accepted_pr_body.txt")
        observation = {"utc": now(), "state": pr["state"], "draft": pr["draft"], "merged": pr["merged"],
                       "merged_at": pr["merged_at"], "head": pr["head"]["sha"], "base": pr["base"]["sha"],
                       "actual_merge": pr["merge_commit_sha"], "body": pr["body"], "body_sha256": sha(pr["body"].encode()),
                       "parents": [r["sha"] for r in actual["parents"]], "tree": actual["tree"]["sha"],
                       "remote_current_main": current_main, "local_main": local_main,
                       "remote_ancestry_status": compare["status"], "remote_main_merge_base": compare["merge_base_commit"]["sha"]}
        check(pr["state"] == "closed" and pr["merged"] is True and pr["draft"] is False and pr["head"]["sha"] == HEAD and pr["base"]["sha"] == BASE and pr["merge_commit_sha"] == MERGE and pr["merged_at"] == "2026-10-03T11:33:31Z",
              label + "_raw_actual_closed_merged_exact_head_base_commit_time")
        check(pr["body"].encode() == body, label + "_actual_literal_accepted_body", body_sha256=sha(body))
        check(actual["sha"] == MERGE and observation["parents"] == [BASE, HEAD] and actual["tree"]["sha"] == TREE,
              label + "_actual_exact_parents_and_tree")
        check(compare["status"] in {"ahead", "identical"} and compare["merge_base_commit"]["sha"] == MERGE and local_ancestor.returncode == 0,
              label + "_remote_and_local_main_descend_from_actual_merge", remote_current_main=current_main, local_main=local_main)
        return observation

    try:
        receipt["first_observation"] = observe("first")
        for label, rev in [("actual_merge", MERGE), ("premerge_base", BASE), ("reviewed_head", HEAD), ("published_audit", PUBLISHED)]:
            remote = api(label + "_commit", "git/commits/" + rev)
            local_root = git("rev-parse", rev + "^{tree}").decode().strip()
            local_parents = git("show", "-s", "--format=%P", rev).decode().strip().split()
            check(remote["sha"] == rev and remote["tree"]["sha"] == local_root and [r["sha"] for r in remote["parents"]] == local_parents,
                  label + "_remote_commit_matches_local_root_and_parents", tree=local_root, parents=local_parents)
            remote_root = api(label + "_complete_root_entries", "git/trees/" + local_root)
            local, stats = tree(rev, False)
            remote_entries = {r["path"]: {k: r[k] for k in ["mode", "type", "sha"]} for r in remote_root["tree"]}
            check(not remote_root.get("truncated") and remote_entries == local,
                  label + "_complete_literal_all_root_mode_type_identity_matches", **stats,
                  scope="Complete immediate-root identities bind all child trees; exhaustive local recursive comparison follows. No truncated remote recursive result is used.")
        before, before_stats = tree(BASE)
        actual, actual_stats = tree(MERGE)
        reviewed, reviewed_stats = tree(HEAD)
        check(actual == reviewed and actual_stats == reviewed_stats, "actual_complete_recursive_tree_equals_reviewed_tree", actual=actual_stats, reviewed=reviewed_stats)
        changed = {p for p in set(before) | set(actual) if before.get(p) != actual.get(p)}
        declared = {r["path"] for r in obj(PUBLISHED, OWN + "FROZEN_FILE_INVENTORY.json")["paths"]}
        check(changed == declared and len(changed) == 47 and all(actual[p]["mode"] == "100644" and actual[p]["type"] == "blob" for p in changed),
              "actual47_literal_diff_scope_modes_types_blob_identities", base=before_stats, actual=actual_stats,
              unchanged_entries=sum(before.get(p) == actual.get(p) for p in set(before) | set(actual)),
              changed_entries=[{"path": p, "before": before.get(p), "after": actual.get(p)} for p in sorted(changed)])
        check({p for p in actual if p.startswith(PREFIX)} == changed - {QUEUE}, "actual_complete46_target_scope")

        def individual(path):
            remote = api("individual_" + path.replace("/", "__"), "contents/" + path + "?ref=" + MERGE)
            decoded = base64.b64decode(remote["content"])
            raw = data(MERGE, path)
            return {"path": path, "bytes": len(raw), "sha256": sha(raw), "git_blob": blob(raw),
                    "passed": decoded == raw and remote["size"] == len(raw) and remote["sha"] == blob(raw) == actual[path]["sha"] and raw == data(HEAD, path),
                    "frozen_target_preserved": path == QUEUE or raw == data(FROZEN, path)}
        individuals = list(concurrent.futures.ThreadPoolExecutor(8).map(individual, sorted(changed)))
        check(all(r["passed"] and r["frozen_target_preserved"] for r in individuals), "all47_individual_actual_remote_blobs_and46_frozen_targets", rows=individuals)
        raw_before, raw_actual = data(BASE, QUEUE), data(MERGE, QUEUE)
        lines = raw_before.splitlines(keepends=True)
        target_rows = [i for i, line in enumerate(lines) if b"30006025 / OWR-14298589-010" in line]
        check(target_rows == [384], "actual_queue_unique_physical385")
        cells = lines[384].split(b"|")
        check(cells[8:10] == [b" queued ", b" 0/5 "], "actual_queue_premerge_literal_cells")
        cells[8:10] = [b" unsolved ", b" 5/5 "]
        lines[384] = b"|".join(cells)
        check(b"".join(lines) == raw_actual, "actual_whole_queue_only_cells8_9", before_bytes=len(raw_before), actual_bytes=len(raw_actual),
              before_sha256=sha(raw_before), actual_sha256=sha(raw_actual), target_line=lines[384].decode(), all_other_bytes_preserved=True)

        def bind_record(directory, record):
            raw = data(MERGE, directory + record["path"])
            passed = len(raw) == record.get("bytes", record.get("size"))
            if record.get("sha256"):
                passed &= sha(raw) == record["sha256"]
            identity = record.get("git_blob_sha1", record.get("sha"))
            if identity:
                passed &= blob(raw) == identity
            return {"path": directory + record["path"], "bytes": len(raw), "sha256": sha(raw), "git_blob": blob(raw), "passed": bool(passed)}
        nested = []
        for name in ["FINAL_AUTHOR_MANIFEST.json", "PUBLICATION_MANIFEST.json", *[f"TURN_{i}_MANIFEST.json" for i in range(1, 6)]]:
            nested.extend(bind_record(PREFIX, r) for r in obj(MERGE, PREFIX + name)["files"])
        nested.extend(bind_record(PREFIX + "independent_review/", r) for r in obj(MERGE, PREFIX + "independent_review/REVIEW_MANIFEST.json")["files"])
        check(len(nested) == 113 and all(r["passed"] for r in nested), "actual_all113_nested_manifest_bindings", rows=nested)
        published_entries, published_stats = tree(PUBLISHED)
        families = []
        for family in ["clean_final_adversary", "surface_surgery_review", "combinatorial_metric_review", "hyperbolic_arithmetic_review"]:
            directory = AUDIT + family + "/"
            manifest_raw = data(PUBLISHED, directory + "PUBLIC_MANIFEST.json")
            manifest = json.loads(manifest_raw)
            bindings = [bind_record(directory, r) for r in manifest["files"]]
            literal = {directory + r["path"] for r in manifest["files"]} | {directory + "PUBLIC_MANIFEST.json"}
            good = literal == {p for p in published_entries if p.startswith(directory)}
            good &= data(MERGE, directory + "PUBLIC_MANIFEST.json") == manifest_raw
            good &= all(r["passed"] and data(MERGE, r["path"]) == data(PUBLISHED, r["path"]) for r in bindings)
            if family == "clean_final_adversary":
                good &= len(bindings) == 28 and sha(manifest_raw) == "8378341e32581f377548f5e480d285daa12b8f9637740f22517d9bf37b5c76d8"
                good &= (repo / directory / "PUBLIC_MANIFEST.json").read_bytes() == manifest_raw
                good &= all((repo / r["path"]).read_bytes() == data(MERGE, r["path"]) for r in bindings)
            families.append({"family": family, "files_including_manifest": len(literal), "bindings": bindings, "passed": bool(good)})
        check(all(r["passed"] for r in families), "actual_four_immutable_family_packets_and_own28_bound_files", rows=families)
        own_baseline = obj(MERGE, OWN + "SOURCE_FIRST_BASELINE.json")
        own_math = obj(MERGE, OWN + "MATHEMATICAL_VERDICT.json")
        check(own_baseline["baseline_sha256"] == sha(data(MERGE, OWN + "SOURCE_FIRST_BASELINE.md")) and own_math["source_baseline_sha256"] == sha(data(MERGE, OWN + "SOURCE_FIRST_BASELINE.json")) and own_math["verdict_sha256"] == sha(data(MERGE, OWN + "MATHEMATICAL_VERDICT.md")) and own_baseline["utc"] < own_math["utc"] and own_math["sealed_before_programs_checks_final_results_reviews"],
              "actual_original_source_first_and_mathematical_seals_preserved", source_first_utc=own_baseline["utc"], math_seal_utc=own_math["utc"])
        live = repo / OWN / "final_live"
        live_manifest_raw = (live / "PUBLIC_MANIFEST.json").read_bytes()
        live_manifest = json.loads(live_manifest_raw)
        live_rows = []
        for record in live_manifest["files"]:
            raw = (live / record["path"]).read_bytes()
            live_rows.append({"path": record["path"], "bytes": len(raw), "sha256": sha(raw), "passed": len(raw) == record["bytes"] and sha(raw) == record["sha256"] and blob(raw) == record["git_blob_sha1"]})
        live_seal = json.loads((live / "LIVE_GATE_SEAL.json").read_text())
        seal_pass = all(len((live / r["path"]).read_bytes()) == r["bytes"] and sha((live / r["path"]).read_bytes()) == r["sha256"] for r in live_seal["bound_files"])
        check(sha(live_manifest_raw) == "b894005f63ae187b55c58f8c6e472077550dea900fb9d76fe4df3e9f572d553c" and len(live_rows) == 10 and all(r["passed"] for r in live_rows) and seal_pass and live_seal["head"] == HEAD and live_seal["base"] == BASE and live_seal["tree"] == TREE,
              "final_live10_bound_files_manifest_and_seal_immutable", bindings=live_rows,
              publication_scope="Final-live files were checked in their working immutable packet; this does not falsely claim they were included in the earlier actual merge tree.")

        root_source = obj(MERGE, AUDIT + "root_source_provenance_recheck.json")
        root_rows = []
        for record in root_source["fresh_source_files"]:
            raw = (repo / AUDIT / record["path"]).read_bytes()
            root_rows.append({**record, "passed": len(raw) == record["bytes"] and sha(raw) == record["sha256"]})
        own_rows = []
        for record in own_baseline["sources"]:
            raw = (repo / OWN / "private/sources" / record["name"]).read_bytes()
            own_rows.append({**record, "passed": len(raw) == record["bytes"] and sha(raw) == record["sha256"]})
        own_assets = []
        for path in sorted((repo / OWN / "private/sources").iterdir()):
            if path.is_file() and path.suffix in {".pdf", ".txt", ".png"}:
                raw = path.read_bytes()
                own_assets.append({"name": path.name, "bytes": len(raw), "sha256": sha(raw)})
        own_ids = {(r["bytes"], r["sha256"]) for r in own_assets}
        root_ids = {(r["bytes"], r["sha256"]) for r in root_rows}
        own_history = obj(MERGE, OWN + "SOURCE_PROVENANCE_RECEIPT.json")
        own_matches = sum((r["expected_bytes"], r["expected_sha256"]) in own_ids for r in own_history["bindings"])
        root_matches = sum((r["historical_declaration"]["bytes"], r["historical_declaration"]["sha256"]) in root_ids for r in root_source["historical_binding_comparisons"])
        check(all(r["passed"] for r in root_rows + own_rows) and own_matches == 11 and root_matches == 10 and root_source["exact_primary_pdf_identities_matched"] == 9 and root_source["all_27_historical_bindings_recertified"] is False and root_source["all_differences_proved_footer_only"] is False,
              "actual_source_evidence_bytes_and_exact_historical_limitations", root_sources=root_rows, own_sources=own_rows,
              root_historical_instances_matched=root_matches, own_historical_instances_matched=own_matches, historical_instances=27,
              root_statement_metadata=root_source["used_primary_readings"], own_statement_metadata=obj(MERGE, OWN + "FRESH_SOURCE_READINGS.json"),
              limitation="Neither root nor this independent audit reproduces all27 historical assets. Current Cambridge mathematical statements are fresh evidence, not an assertion of historical byte identity or only-footer difference.")
        author = obj(MERGE, OWN + "AUTHOR_REPLAY_FULL_RECEIPT.json")
        historical = obj(MERGE, OWN + "MANIFEST_AND_HISTORICAL_REPLAY.json")
        check(author["all_passed"] and author["assertions"] == 15618 and historical["historical_receipt_comparison"]["old_author_full_json_equal"] and all(r["exit"] == 0 and r["stderr_bytes"] == 0 for r in historical["review_replays"]),
              "unchanged_complete_author_history_reproduction_applies_to_actual_merge", author_assertions=15618, historical_assertions=24692,
              reason="Actual46 mathematical inputs, executables and expected outputs equal frozen and reviewed bytes; no changed computation needs rerun.")
        receipt["last_observation"] = observe("last")
        stable = ["state", "draft", "merged", "merged_at", "head", "base", "actual_merge", "body", "parents", "tree"]
        check(all(receipt["first_observation"][k] == receipt["last_observation"][k] for k in stable), "late_actual_merge_state_body_parent_tree_stability", stable_fields=stable,
              ancestry_policy="Each remote/local main observation separately descends from the actual merge; legitimate later descendant checkpoints need not equal the merge SHA.")
        receipt["status"] = "PASS_ACTUAL_MERGE_SCOPED_UNSOLVED_5_OF_5"
        receipt["disposition"] = "PR371 actually merged as unsolved5/5 partials. Original Question4 remains unresolved. No historical novelty, all27 source identity, paper, release, DOI or external communication is inferred."
    except Exception:
        receipt["status"] = "FAIL"
        receipt["failure"] = traceback.format_exc()
    receipt["completed_utc"] = now()
    receipt["program_sha256"] = sha(Path(__file__).read_bytes())
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "checks": len(receipt["checks"]), "receipt": str(receipt_path), "failure": receipt.get("failure")}))
    raise SystemExit(0 if receipt["status"].startswith("PASS") else 1)


if __name__ == "__main__":
    main()
