#!/usr/bin/env python3
"""Read-only exact-live gate. Default receipts and raw data are ignored/private.

Run with --repo PATH. --receipt PATH explicitly selects a new public receipt.
No Git index, refs, checkout, service state, or frozen audit file is modified.
"""
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
FROZEN = "51fddd150e8da33f4cf17b1a642a0ffd3466bf5d"
PUBLISHED = "1836407486e6cea540bb9b5e33e05b9c04d83272"
BASE = PUBLISHED
HEAD = "137d5e30efe05bb5f68a5b0bcc4e37480c8a9493"
TREE = "4470a8767ee00e28b34108ef240684b6a830c0e0"
AUTHOR = "308b3ee53312800cfe6a82a2cdcc9763e1f90422"
PREFIX = "problems/30006025_geometric_chapuy/"
AUDIT = "draft_pr_descending_audit_20261002/audits/pr371_30006025/"
OWN = AUDIT + "clean_final_adversary/"
QUEUE = "unsolved_math_prioritization/QUEUE.md"
CHECKPOINTS = ["6fb965118ce87d6a25afa60f92cc21c78605eb4b", "649acde2cf13c0a89ba7433b5cf4214e45cb8901", "96158499a002790d1e82a62b8d43ee47836a312b", "67c1e19c1c56f757896f509fab402441e99a58ea", AUTHOR]
ORIGINAL_BASE = "efd29c05204703acca9a0860812f54b94fae54b1"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    global HEAD, BASE, TREE
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--head", default=HEAD)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--tree", default=TREE)
    ap.add_argument("--parent-head", default=FROZEN, help="Exact previous reviewed PR head that the current-main repair descends from.")
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()
    HEAD, BASE, TREE = args.head, args.base, args.tree
    repo = args.repo.resolve()
    run = ROOT / "private" / ("run_" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    run.mkdir(parents=True)
    receipt_path = args.receipt.resolve() if args.receipt else run / "receipt.json"
    receipt = {"started_utc": now(), "head": HEAD, "base": BASE, "tree": TREE,
               "frozen_head": FROZEN, "published_audit_commit": PUBLISHED, "expected_parent_head": args.parent_head, "checks": [], "status": "RUNNING",
               "raw_storage": str(run.relative_to(ROOT)),
               "source_history_limit": "Root 10/27 and own 11/27 historical bindings reproduced; neither certifies all27. Nine stable primary PDFs match. Fresh Cambridge mathematical evidence is separately bound, not asserted byte-identical to historical copy or differing only in its footer."}

    def check(condition, name, **details):
        receipt["checks"].append({"name": name, "passed": bool(condition), **details})
        if not condition:
            raise AssertionError(name)

    def git(*argv):
        return subprocess.check_output(["git", "-C", str(repo), *argv])

    def data(rev, path):
        return git("show", rev + ":" + path)

    def obj(rev, path):
        return json.loads(data(rev, path))

    def api(label, endpoint):
        proc = subprocess.run(["gh", "api", "repos/AlecKriebel/Math/" + endpoint], capture_output=True)
        (run / (label + ".stdout")).write_bytes(proc.stdout)
        (run / (label + ".stderr")).write_bytes(proc.stderr)
        if proc.returncode:
            raise RuntimeError(label + ": GitHub read failed, exit " + str(proc.returncode))
        return json.loads(proc.stdout)

    def local_tree(rev, recursive=True):
        flags = ["-r"] if recursive else []
        raw = git("ls-tree", *flags, "-z", rev)
        entries = {}
        for row in raw.split(b"\0"):
            if not row:
                continue
            fields, path = row.split(b"\t", 1)
            mode, kind, identity = fields.decode().split()
            entries[path.decode()] = {"mode": mode, "type": kind, "sha": identity}
        return entries, {"entries": len(entries), "raw_bytes": len(raw), "raw_sha256": sha(raw)}

    def bind(directory, record):
        path = directory + record["path"]
        raw = data(HEAD, path)
        wanted_blob = record.get("git_blob_sha1", record.get("sha"))
        passed = len(raw) == record.get("bytes", record.get("size"))
        if record.get("sha256"):
            passed &= sha(raw) == record["sha256"]
        if wanted_blob:
            passed &= blob(raw) == wanted_blob
        return {"path": path, "bytes": len(raw), "sha256": sha(raw), "git_blob": blob(raw), "passed": bool(passed)}

    def observe(label):
        pr = api(label + "_pr", "pulls/371")
        mainref = api(label + "_main", "git/ref/heads/main")
        merge = api(label + "_test_merge", "git/commits/" + pr["merge_commit_sha"])
        accepted = data(PUBLISHED, AUDIT + "accepted_pr_body.txt")
        observation = {"utc": now(), "head": pr["head"]["sha"], "base": pr["base"]["sha"],
                       "current_main": mainref["object"]["sha"], "state": pr["state"], "draft": pr["draft"],
                       "merged": pr["merged"], "mergeable": pr["mergeable"], "mergeable_state": pr["mergeable_state"],
                       "title": pr["title"], "body": pr["body"], "body_sha256": sha(pr["body"].encode()),
                       "body_bytes": len(pr["body"].encode()), "test_merge": merge["sha"],
                       "test_merge_parents": [x["sha"] for x in merge["parents"]], "test_merge_tree": merge["tree"]["sha"]}
        check(pr["head"]["sha"] == HEAD and pr["base"]["sha"] == BASE and mainref["object"]["sha"] == BASE,
              label + "_exact_head_base_current_main")
        check(pr["state"] == "open" and not pr["draft"] and not pr["merged"] and pr["mergeable"] is True and pr["mergeable_state"] == "clean",
              label + "_open_ready_mergeable_clean")
        check(pr["body"].encode() == accepted, label + "_literal_accepted_body", accepted_sha256=sha(accepted))
        check(observation["test_merge_parents"] == [BASE, HEAD] and observation["test_merge_tree"] == TREE,
              label + "_test_merge_exact_parents_tree")
        return observation

    try:
        receipt["first_observation"] = observe("first")
        for label, revision in [("base", BASE), ("head", HEAD), ("frozen", FROZEN), ("published", PUBLISHED)]:
            remote = api(label + "_commit", "git/commits/" + revision)
            local_id = git("rev-parse", revision).decode().strip()
            local_root = git("rev-parse", revision + "^{tree}").decode().strip()
            local_parents = git("show", "-s", "--format=%P", revision).decode().strip().split()
            check(remote["sha"] == local_id and remote["tree"]["sha"] == local_root and [x["sha"] for x in remote["parents"]] == local_parents,
                  label + "_remote_commit_root_parents_match", commit=local_id, tree=local_root, parents=local_parents)
            root_api = api(label + "_all_root_entries", "git/trees/" + local_root)
            root_entries, root_stats = local_tree(revision, False)
            remote_entries = {x["path"]: {k: x[k] for k in ["mode", "type", "sha"]} for x in root_api["tree"]}
            check(not root_api.get("truncated") and remote_entries == root_entries,
                  label + "_complete_literal_all_root_entries_remote_match", **root_stats,
                  rationale="112 literal immediate root entries bind all child trees; avoids the recursive API's 100000-entry truncation. Full local recursive entries are compared separately.")
        check(git("rev-parse", HEAD + "^{tree}").decode().strip() == TREE, "head_tree_exact")
        check(git("show", "-s", "--format=%P", HEAD).decode().strip().split() == [args.parent_head, BASE], "queue_refresh_parents_exact")
        check(subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", BASE, HEAD], capture_output=True).returncode == 0, "current_main_is_head_ancestor")
        before, before_stats = local_tree(BASE)
        after, after_stats = local_tree(HEAD)
        changed = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
        expected_paths = {r["path"] for r in obj(PUBLISHED, OWN + "FROZEN_FILE_INVENTORY.json")["paths"]}
        check(changed == expected_paths and len(changed) == 47, "full_recursive_repository_literal_mode_type_blob_scope",
              base_tree=before_stats, head_tree=after_stats, changed_entries=[{"path": p, "before": before.get(p), "after": after.get(p)} for p in sorted(changed)],
              unchanged_entries=sum(before.get(p) == after.get(p) for p in set(before) | set(after)),
              no_glob_allowlist=True)
        targets = {p for p in after if p.startswith(PREFIX)}
        check(targets == changed - {QUEUE} and len(targets) == 46, "complete_46_target_scope")
        check(all(after[p]["mode"] == "100644" and after[p]["type"] == "blob" for p in changed), "all47_regular_blob_modes")

        def remote_file(path):
            downloaded = api("content_" + path.replace("/", "__"), "contents/" + path + "?ref=" + HEAD)
            decoded = base64.b64decode(downloaded["content"])
            local = data(HEAD, path)
            return {"path": path, "bytes": len(local), "sha256": sha(local), "git_blob": blob(local),
                    "api_bytes_equal": decoded == local, "api_blob_equal": downloaded["sha"] == after[path]["sha"] == blob(local),
                    "api_size_equal": downloaded["size"] == len(local),
                    "frozen_target_preserved": path == QUEUE or data(FROZEN, path) == local}
        remote_files = list(concurrent.futures.ThreadPoolExecutor(8).map(remote_file, sorted(changed)))
        receipt["remote_files"] = remote_files
        check(all(r["api_bytes_equal"] and r["api_blob_equal"] and r["api_size_equal"] and r["frozen_target_preserved"] for r in remote_files), "all47_live_remote_bytes_and46_frozen_targets")

        base_queue, head_queue = data(BASE, QUEUE), data(HEAD, QUEUE)
        lines = base_queue.splitlines(keepends=True)
        target_rows = [i for i, line in enumerate(lines) if b"30006025 / OWR-14298589-010" in line]
        check(target_rows == [384], "queue_target_unique_physical385")
        cells = lines[384].split(b"|")
        check(cells[8] == b" queued " and cells[9] == b" 0/5 ", "queue_before_literal_cells8_9")
        cells[8], cells[9] = b" unsolved ", b" 5/5 "
        expected_line = b"|".join(cells)
        lines[384] = expected_line
        check(b"".join(lines) == head_queue, "full_queue_bytes_only_two_literal_cells", base_bytes=len(base_queue), head_bytes=len(head_queue),
              base_sha256=sha(base_queue), head_sha256=sha(head_queue), expected_target_line=expected_line.decode(), target_line=385,
              all_other_lines_cells_and_final_newline_preserved=True)

        bindings = []
        for name in ["FINAL_AUTHOR_MANIFEST.json", "PUBLICATION_MANIFEST.json", *[f"TURN_{i}_MANIFEST.json" for i in range(1, 6)]]:
            manifest = obj(HEAD, PREFIX + name)
            bindings.extend(bind(PREFIX, r) for r in manifest["files"])
            if "previous_manifest_sha256" in manifest:
                turn = int(name.split("_")[1])
                check(manifest["previous_manifest_sha256"] == sha(data(HEAD, PREFIX + f"TURN_{turn-1}_MANIFEST.json")), name + "_previous_manifest_hash")
        review_manifest = obj(HEAD, PREFIX + "independent_review/REVIEW_MANIFEST.json")
        bindings.extend(bind(PREFIX + "independent_review/", r) for r in review_manifest["files"])
        check(len(bindings) == 113 and all(x["passed"] for x in bindings), "all113_nested_manifest_bindings", bindings=bindings)
        historical = obj(HEAD, PREFIX + "independent_review/REMOTE_BINDING.json")
        wip_rows = [{"path": r["path"], "preserved": data(AUTHOR, PREFIX + r["path"]) == data(HEAD, PREFIX + r["path"]),
                     "passed": bind(PREFIX, r)["passed"]} for r in historical["files"]]
        check(len(wip_rows) == 37 and all(x["preserved"] and x["passed"] for x in wip_rows), "actual37_author_wip_target_binding", rows=wip_rows,
              scope="Actual author target in historical WIP commit, not whole WIP repository certification")
        checkpoint_rows = []
        for i, commit in enumerate(CHECKPOINTS, 1):
            metadata = api(f"checkpoint_{i}", "git/commits/" + commit)
            parent = ORIGINAL_BASE if i == 1 else CHECKPOINTS[i-2]
            state = obj(commit, PREFIX + f"TURN_{i}_STATE.json")
            good = [x["sha"] for x in metadata["parents"]] == [parent]
            good &= metadata["tree"]["sha"] == git("rev-parse", commit + "^{tree}").decode().strip()
            good &= state["author_turns_completed"] == i and state["budget"] == 5
            good &= data(commit, PREFIX + f"TURN_{i}.md") == data(HEAD, PREFIX + f"TURN_{i}.md")
            good &= data(commit, PREFIX + f"TURN_{i}_MANIFEST.json") == data(HEAD, PREFIX + f"TURN_{i}_MANIFEST.json")
            checkpoint_rows.append({"turn": i, "commit": commit, "parent": parent, "state": state, "passed": bool(good)})
        check(all(x["passed"] for x in checkpoint_rows), "five_actual_checkpoint_objects_state_and_preserved_proof_chain", rows=checkpoint_rows)

        allowlist = obj(PUBLISHED, "draft_pr_descending_audit_20261002/checkpoint_371_math_public_allowlist.json")["explicit_owned_paths"]
        publication_paths = git("diff-tree", "--no-commit-id", "--name-only", "-r", PUBLISHED).decode().splitlines()
        check(len(allowlist) == len(set(allowlist)) == 200 and set(publication_paths) == set(allowlist), "root200_publication_exact_literal_owned_path_scope")
        publication_rows = []
        for path in sorted(allowlist):
            raw = data(PUBLISHED, path)
            publication_rows.append({"path": path, **before[path], "bytes": len(raw), "sha256": sha(raw),
                                     "head_preserved": data(HEAD, path) == raw and data(BASE, path) == raw and before[path] == after[path]})
        check(all(x["head_preserved"] and x["mode"] == "100644" and x["type"] == "blob" for x in publication_rows), "all200_published_owned_files_preserved", rows=publication_rows)
        published_entries, published_stats = local_tree(PUBLISHED)
        family_rows = []
        for family in ["clean_final_adversary", "surface_surgery_review", "combinatorial_metric_review", "hyperbolic_arithmetic_review"]:
            directory = AUDIT + family + "/"
            manifest = obj(PUBLISHED, directory + "PUBLIC_MANIFEST.json")
            records = [bind(directory, r) for r in manifest["files"]]
            listed = {directory + r["path"] for r in manifest["files"]} | {directory + "PUBLIC_MANIFEST.json"}
            actual_scope = {p for p in published_entries if p.startswith(directory)}
            good = listed == actual_scope and all(r["passed"] for r in records)
            if family == "clean_final_adversary":
                good &= len(records) == 28 and sha(data(PUBLISHED, directory + "PUBLIC_MANIFEST.json")) == "8378341e32581f377548f5e480d285daa12b8f9637740f22517d9bf37b5c76d8"
                good &= all((repo / r["path"]).read_bytes() == data(PUBLISHED, r["path"]) for r in records)
                good &= (repo / directory / "PUBLIC_MANIFEST.json").read_bytes() == data(PUBLISHED, directory + "PUBLIC_MANIFEST.json")
            family_rows.append({"family": family, "literal_scope_count_including_manifest": len(listed), "passed": bool(good), "bindings": records})
        check(all(x["passed"] for x in family_rows), "all_four_immutable_family_packets_and_own28_plus_manifest_unchanged", rows=family_rows)

        own_sources = obj(PUBLISHED, OWN + "SOURCE_FIRST_BASELINE.json")["sources"]
        own_rows = []
        for record in own_sources:
            raw = (repo / OWN / "private/sources" / record["name"]).read_bytes()
            own_rows.append({**record, "present_bytes": len(raw), "present_sha256": sha(raw), "passed": len(raw) == record["bytes"] and sha(raw) == record["sha256"]})
        check(all(r["passed"] for r in own_rows), "own_fresh_sealed_source_bytes_preserved", sources=own_rows)
        root_sources = obj(PUBLISHED, AUDIT + "root_source_provenance_recheck.json")
        root_rows = []
        for record in root_sources["fresh_source_files"]:
            raw = (repo / AUDIT / record["path"]).read_bytes()
            root_rows.append({**record, "passed": len(raw) == record["bytes"] and sha(raw) == record["sha256"]})
        check(all(r["passed"] for r in root_rows), "root_fresh_stored_source_bytes_preserved", sources=root_rows, mathematical_statement_metadata=root_sources["used_primary_readings"])
        own_history = obj(PUBLISHED, OWN + "SOURCE_PROVENANCE_RECEIPT.json")
        own_matching = sum(x.get("fresh_byte_hash_equal", False) for x in own_history["bindings"])
        own_asset_rows = []
        for asset in sorted((repo / OWN / "private/sources").iterdir()):
            if asset.is_file() and asset.suffix in {".pdf", ".txt", ".png"}:
                raw = asset.read_bytes()
                own_asset_rows.append({"name": asset.name, "bytes": len(raw), "sha256": sha(raw)})
        own_asset_identities = {(r["bytes"], r["sha256"]) for r in own_asset_rows}
        root_asset_identities = {(r["bytes"], r["sha256"]) for r in root_rows}
        own_fresh_matching = sum((r["expected_bytes"], r["expected_sha256"]) in own_asset_identities for r in own_history["bindings"])
        root_fresh_matching = sum((r["historical_declaration"]["bytes"], r["historical_declaration"]["sha256"]) in root_asset_identities for r in root_sources["historical_binding_comparisons"])
        check(own_fresh_matching == own_matching == 11 and root_fresh_matching == root_sources["exact_matched_instances"] == 10,
              "historical_27_counts_recomputed_from_current_stored_asset_bytes", own_fresh_match_instances=own_fresh_matching,
              root_fresh_match_instances=root_fresh_matching, own_current_asset_metadata=own_asset_rows,
              no_historical_all27_match_inferred=True)
        check(root_sources["exact_matched_instances"] == 10 and own_matching == 11 and root_sources["exact_primary_pdf_identities_matched"] == 9 and root_sources["all_27_historical_bindings_recertified"] is False and root_sources["all_differences_proved_footer_only"] is False,
              "source_history_exact_qualified_counts", root_matches=10, own_matches=11, stable_primary_pdfs=9, historical_instances=27,
              own_statement_metadata=obj(PUBLISHED, OWN + "FRESH_SOURCE_READINGS.json"))
        author_replay = obj(PUBLISHED, OWN + "AUTHOR_REPLAY_FULL_RECEIPT.json")
        prior_replay = obj(PUBLISHED, OWN + "MANIFEST_AND_HISTORICAL_REPLAY.json")
        check(author_replay["all_passed"] and author_replay["assertions"] == 15618 and prior_replay["all_record_bindings_pass"] and prior_replay["historical_receipt_comparison"]["old_author_full_json_equal"] and all(r["exit"] == 0 and not r["stderr_bytes"] for r in prior_replay["review_replays"]),
              "prior_complete_replay_remains_applicable_to_identical46_bytes", author_assertions=15618, historical_assertions=24692,
              rationale="All46 target bytes including every executable and expected receipt were freshly proven equal to the frozen replay inputs. No changed mathematical executable/input warrants repeat computation.")
        receipt["last_observation"] = observe("last")
        stable_fields = ["head", "base", "current_main", "state", "draft", "merged", "mergeable", "mergeable_state", "title", "body", "test_merge", "test_merge_parents", "test_merge_tree"]
        check(all(receipt["first_observation"][k] == receipt["last_observation"][k] for k in stable_fields), "late_exact_state_body_testmerge_stability", stable_fields=stable_fields)
        receipt["status"] = "PASS_EXACT_LIVE_SCOPED_UNSOLVED_PACKET"
        receipt["merge_scope"] = "This read-only gate approves only the observed HEAD/BASE/body/test-merge tree. Root must perform its own gate and actual merge readback. Any head/main/body/tree movement invalidates this gate. Original mathematical question remains unsolved5/5; no release or other publication is authorized here."
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
