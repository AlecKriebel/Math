#!/usr/bin/env python3
"""Isolated, credential-free controls for the exact known-draft repair recipe.

Only the recipe's fixed T constant is redirected to owned fixtures. The approved
driver is hash-checked as bytes but never imported. Its public interfaces are
stubbed. The unchanged upload tool's pure functions and exact run() body are AST
extracted, with all network/state/token interfaces replaced by in-memory fakes.
This tests administrative guards, not the truth of completed scientific reviews.
"""
from __future__ import annotations
import argparse, ast, contextlib, copy, hashlib, html, importlib.util, io, json
import re, shutil, sys, tempfile, types, urllib.request
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[2]
OWN = Path(__file__).resolve().parents[1]
ROOT = T.parents[3]
RECIPE = T / "verification_recipes/RESUME_KNOWN_DRAFT_V4_AFTER_REVIEW.py"
RECIPE_SHA = "e11b7f1426e28fbe0b3407dad777fb9ae4287213e1f5eabc96ad22f9bf36b8d2"
DRIVER_SHA = "a02c7910936f6d871fc760af4f5f41005f2ca055dc7cc99e84913a0893a47f96"
TOOL_SHA = "a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca"
MF = "b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa"
H = "aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
RID = 23423736
ZIP_ID = "00000000-0000-4000-8000-000000000001"
PDF_ID = "00000000-0000-4000-8000-000000000002"
BUCKET = "https://zenodo.org/api/files/00000000-0000-4000-8000-000000000003"

def need(v, message):
    if not v:
        raise RuntimeError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

def tool_functions(tool_bytes):
    names = {"DepositError", "read_json", "digest", "load_manifest", "server_files",
             "matching_file", "validate_record", "verify", "run"}
    source = ast.parse(tool_bytes)
    selected = [n for n in source.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                and n.name in names]
    need({n.name for n in selected} == names, "Exact tool functions missing")
    # Postponed annotations avoid evaluating the deliberately unimported client.
    future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
    program = ast.fix_missing_locations(ast.Module(body=[future] + selected, type_ignores=[]))
    ns = {"Path": Path, "json": json, "hashlib": hashlib, "html": html, "re": re,
          "argparse": argparse, "MAX_FILES": 100, "MAX_BYTES": 50 * 1024**3,
          "CHUNK": 1024 * 1024}
    exec(compile(program, "<unchanged-upload-tool-pure-functions>", "exec"), ns)
    return ns

class RedirectRoot(ast.NodeTransformer):
    def __init__(self, destination):
        self.destination, self.changed = destination, 0
    def visit_Constant(self, node):
        if node.value == str(T):
            self.changed += 1
            return ast.copy_location(ast.Constant(value=str(self.destination)), node)
        return node

def case(name, recipe_bytes, driver_bytes, tool_bytes):
    scratch = OWN / "scratch/known_draft_repair"
    scratch.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix=name + "-", dir=scratch))
    p, u, m, old = (folder / "preprint", folder / "publication",
                    folder / "root-receipts", folder / "package_versions/v3_review03")
    for d in (p, u, m, old):
        d.mkdir(parents=True)
    for src, dst in ((T / "preprint", p), (T / "package_versions/v3_review03", old)):
        for rel in ("zenodo-deposit.json", "source-and-verification.zip", "output/pdf/paper.pdf"):
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src / rel, dst / rel)
    (folder / "publication_driver.py").write_bytes(driver_bytes)
    g = {"actual_whole_preprint_rounds": 4, "final_current_round_clean": True,
         "reviewed_head": H, "fixture_only": True}
    inv = {"source_manifest_sha256": MF}
    save(folder / "FINAL_READINESS.json", g)
    shutil.copyfile(folder / "FINAL_READINESS.json", u / "READINESS_AT_PUBLICATION_V4.json")
    save(m / "WHOLE04_V4_READY_CHECKPOINT_RECEIPT.json", {"fixture_only": True})
    ns = tool_functions(tool_bytes)
    real_load = ns["load_manifest"]
    metadata, newfiles = real_load(p / "zenodo-deposit.json")
    need([e["name"] for e in newfiles] == ["paper.pdf", "source-and-verification.zip"],
         "Positive and direct wrapper controls require the frozen manifest order")
    _, oldfiles = real_load(old / "zenodo-deposit.json")
    remote = {}
    for entry in oldfiles:
        remote[entry["name"]] = {"filename": entry["name"], "filesize": entry["size"],
                                  "checksum": "md5:" + entry["md5"],
                                  "id": ZIP_ID if entry["name"].endswith("zip") else PDF_ID}
    events, state_calls, get_calls, load_calls = [], 0, 0, 0
    remote_meta = copy.deepcopy(metadata)
    submitted = False
    scope = {}

    if name == "three_round_gate":
        g["actual_whole_preprint_rounds"] = 3
    elif name == "final_clean_false":
        g["final_current_round_clean"] = False
    elif name == "wrong_source_manifest":
        inv["source_manifest_sha256"] = "0" * 64
    elif name == "snapshot_drift":
        (u / "READINESS_AT_PUBLICATION_V4.json").write_text("{}")
    elif name == "missing_checkpoint":
        (m / "WHOLE04_V4_READY_CHECKPOINT_RECEIPT.json").unlink()
    elif name in {"existing_publication_intent", "existing_publish_receipt", "existing_replacement_intent"}:
        filename = {"existing_publication_intent": "PUBLICATION_INTENT.json",
                    "existing_publish_receipt": "PUBLISH_RECEIPT.json",
                    "existing_replacement_intent": "V4_ZIP_REPLACEMENT_INTENT.json"}[name]
        save(u / filename, {"fixture_only": True})
    elif name == "driver_pin_drift":
        (folder / "publication_driver.py").write_bytes(driver_bytes + b"\n")
    elif name == "already_published":
        submitted = True
    elif name == "remote_metadata_drift":
        remote_meta["title"] += " changed"
    elif name == "extra_remote_file":
        remote["extra"] = {"filename": "extra"}
    elif name == "old_zip_md5_drift":
        remote["source-and-verification.zip"]["checksum"] = "md5:" + "0" * 32
    elif name == "pdf_initial_md5_drift":
        remote["paper.pdf"]["checksum"] = "md5:" + "0" * 32
    elif name == "malformed_file_uuid":
        remote["source-and-verification.zip"]["id"] = "not-a-uuid"

    def local_state(path, environment):
        nonlocal state_calls
        state_calls += 1
        need(path == (p / "zenodo-deposit.json").resolve() and environment == "production",
             "Unexpected mock state location")
        missing = name == "missing_initial_state" or (name == "state_lost_before_stage" and state_calls == 2)
        record = 12345678 if name == "other_initial_state" or (name == "state_changed_before_stage" and state_calls == 2) else RID
        return folder / "mock-local-state.json", None if missing else {"id": record}

    def load_manifest(path):
        nonlocal load_calls
        load_calls += 1
        value = real_load(path)
        if load_calls == 3:
            if name == "stage_metadata_drift":
                value[0]["title"] += " changed"
            elif name == "zip_bytes_changed_before_upload":
                data = bytearray((p / "source-and-verification.zip").read_bytes())
                data[0] ^= 1
                (p / "source-and-verification.zip").write_bytes(data)
            elif name == "zip_hardlinked_before_upload":
                import os
                os.link(p / "source-and-verification.zip", p / "second-link")
            elif name == "zip_symlinked_before_upload":
                (p / "source-and-verification.zip").rename(p / "real.zip")
                (p / "source-and-verification.zip").symlink_to(p / "real.zip")
        return value

    class Client:
        token = "MOCK_TOKEN_NEVER_READ_FROM_ENVIRONMENT"
        def __init__(self, environment, token):
            need(environment == "production" and token == self.token, "Unexpected mock client")
        def get(self, record):
            nonlocal get_calls
            events.append({"method": "GET", "id": record})
            get_calls += 1
            need(record == RID, "A raw GET reached another record")
            if get_calls == 3 and name == "pdf_missing_before_stage":
                remote.pop("paper.pdf", None)
            if get_calls == 2 and name == "pdf_missing_after_delete":
                remote.pop("paper.pdf", None)
            bucket = BUCKET + "-changed" if get_calls == 3 and name == "bucket_changed_before_stage" else BUCKET
            response = {"id": RID, "submitted": submitted, "metadata": copy.deepcopy(remote_meta),
                        "files": copy.deepcopy(list(remote.values())),
                        "links": {"bucket": bucket, "html": "https://zenodo.org/deposit/23423736"}}
            if name == "returned_id_changed_after_delete" and get_calls == 2:
                response["id"] = 12345678
            return response
        def create(self, value):
            events.append({"method": "CREATE"})
            raise RuntimeError("Raw create must never be reached")
        def upload(self, bucket, entry):
            events.append({"method": "UPLOAD", "bucket": bucket, "name": entry["name"],
                           "sha256": entry["sha256"]})
            remote[entry["name"]] = {"filename": entry["name"], "filesize": entry["size"],
                                      "checksum": "md5:" + entry["md5"], "id": ZIP_ID}
        def update(self, record, value):
            events.append({"method": "UPDATE", "id": record, "exact_metadata": value == metadata})
            need(record == RID, "A raw update reached another record")
            remote_meta.clear()
            remote_meta.update(copy.deepcopy(value))

    ns.update(load_manifest=load_manifest, local_state=local_state, ZenodoClient=Client,
              token_for=lambda environment: Client.token,
              save_state=lambda *args: (_ for _ in ()).throw(RuntimeError("No state creation allowed")))
    z = types.SimpleNamespace(**{k: ns[k] for k in ("load_manifest", "local_state", "run",
                              "server_files", "matching_file", "validate_record", "ZenodoClient", "token_for")})
    d = types.SimpleNamespace(gate=lambda: (g, inv), save=save, load_tool=lambda: z)
    def fresh_eligibility(value):
        events.append({"method": "MOCK_FRESH_ELIGIBILITY"})
        if name == "fresh_claim_ineligible":
            raise RuntimeError("Mock claim no longer eligible")
        d.save(folder / "ignored.json", {"fixture_only": True})
    d.fresh_eligibility = fresh_eligibility
    def make_spec(module_name, path):
        need(Path(path) == folder / "publication_driver.py", "Unexpected import path")
        events.append({"method": "MOCK_DRIVER_IMPORT"})
        return types.SimpleNamespace(loader=types.SimpleNamespace(exec_module=lambda module: None))

    class Response:
        status = 200 if name == "delete_non204" else 204
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self, limit):
            need(limit == 4096, "Unexpected response read")
            return b"unexpected" if name == "delete_nonempty204" else b""
    def build_opener(handler):
        def open_request(request, timeout):
            need(request.get_method() == "DELETE" and request.full_url ==
                 "https://zenodo.org/api/deposit/depositions/23423736/files/" + ZIP_ID,
                 "DELETE scope changed")
            need((u / "V4_ZIP_REPLACEMENT_INTENT.json").exists(), "DELETE preceded durable intent")
            events.append({"method": "DELETE", "id": RID, "file_id": ZIP_ID})
            if name == "delete_redirect":
                handler().redirect_request(request, None, 302, "redirect", {}, "https://example.invalid/")
            if name == "delete_unknown_outcome":
                raise OSError("Mock timeout")
            remote.pop("source-and-verification.zip")
            return Response()
        return types.SimpleNamespace(open=open_request)

    transform = RedirectRoot(folder)
    tree = transform.visit(ast.parse(recipe_bytes))
    need(transform.changed == 1, "Recipe root rewrite is no longer exactly one literal")
    code = compile(ast.fix_missing_locations(tree), "<exact-known-draft-recipe-redirected-root>", "exec")
    error, completed = None, False
    with patch.object(importlib.util, "spec_from_file_location", make_spec), \
         patch.object(importlib.util, "module_from_spec", lambda spec: d), \
         patch.object(urllib.request, "build_opener", build_opener), \
         patch.object(urllib.request, "urlopen", side_effect=RuntimeError("Real network prohibited")), \
         contextlib.redirect_stdout(io.StringIO()):
        try:
            exec(code, scope)
            completed = True
        except (RuntimeError, KeyError, ValueError, OSError, TypeError, ns["DepositError"]) as exc:
            error = type(exc).__name__ + ": " + str(exc)
    deletes = [x for x in events if x["method"] == "DELETE"]
    uploads = [x for x in events if x["method"] == "UPLOAD"]
    updates = [x for x in events if x["method"] == "UPDATE"]
    success = name == "exact_same_draft_repair"
    control = completed == success
    expected_errors = {
        "three_round_gate": "Completed exact four-round final gate required",
        "final_clean_false": "Completed exact four-round final gate required",
        "wrong_source_manifest": "Wrong V4 source",
        "snapshot_drift": "Exact final V4 publication snapshot required",
        "missing_checkpoint": "Completed scoped prepublication checkpoint required",
        "existing_publication_intent": "Publication already attempted",
        "existing_publish_receipt": "Publication already attempted",
        "existing_replacement_intent": "Replacement was attempted",
        "driver_pin_drift": "Approved production driver pin differs before import",
        "fresh_claim_ineligible": "Mock claim no longer eligible",
        "missing_initial_state": "The sole known draft state is required",
        "other_initial_state": "The sole known draft state is required",
        "already_published": "Only unpublished23423736 may be repaired",
        "remote_metadata_drift": "Existing canonical metadata must exactly match every V4 supplied field",
        "extra_remote_file": "Exact known two-file inventory required",
        "old_zip_md5_drift": "Existing draft differs from the preserved exact V3 files",
        "pdf_initial_md5_drift": "Existing draft differs from the preserved exact V3 files",
        "malformed_file_uuid": "badly formed hexadecimal UUID string",
        "delete_non204": "Unexpected removal response",
        "delete_nonempty204": "Unexpected removal response",
        "delete_redirect": "Known-file removal outcome unconfirmed",
        "delete_unknown_outcome": "Known-file removal outcome unconfirmed",
        "pdf_missing_after_delete": "Known draft after removal differs",
        "returned_id_changed_after_delete": "Zenodo returned a different deposition ID",
        "state_lost_before_stage": "A second deposition creation is prohibited",
        "state_changed_before_stage": "Refusing a different record ID before GET or stage mutation",
        "pdf_missing_before_stage": "Refusing a different bucket, file, or PDF upload",
        "bucket_changed_before_stage": "Refusing a different bucket, file, or PDF upload",
        "zip_bytes_changed_before_upload": "Frozen approved ZIP path or bytes differ before upload",
        "zip_hardlinked_before_upload": "Frozen approved ZIP path or bytes differ before upload",
        "zip_symlinked_before_upload": "Frozen approved ZIP path or bytes differ before upload",
        "stage_metadata_drift": "Refusing different record or metadata before PUT"}
    intended_guard_hit = success or bool(error and expected_errors[name] in error)
    control = control and intended_guard_hit
    control = control and not any(x.get("id", RID) != RID or x["method"] == "CREATE" for x in events)
    control = control and len(deletes) <= 1 and len(uploads) <= 1
    control = control and all(x["name"] == "source-and-verification.zip" and x["bucket"] == BUCKET for x in uploads)
    control = control and all(x["exact_metadata"] for x in updates)
    if success:
        control = control and len(deletes) == len(uploads) == len(updates) == 1
        control = control and (u / "STAGE_RECEIPT.json").exists()
    elif name not in {"stage_metadata_drift"}:
        control = control and not uploads and not updates
    else:
        # The exact ZIP may already have uploaded when an independently changed
        # manifest metadata is refused. A PUT with changed metadata cannot occur.
        control = control and len(uploads) == 1 and not updates
    result = {"case": name, "completed": completed, "expected_completion": success,
              "control_pass": bool(control), "intended_guard_hit": intended_guard_hit,
              "error": error, "mock_events": events,
              "replacement_intent_exists": (u / "V4_ZIP_REPLACEMENT_INTENT.json").exists(),
              "stage_receipt_exists": (u / "STAGE_RECEIPT.json").exists()}
    if success:
        # Directly test bound wrappers after their authentic positive path.
        probes = [("different_get", lambda: scope["only_known_get"](12345678)),
                  ("boolean_get", lambda: scope["only_known_get"](True)),
                  ("string_get", lambda: scope["only_known_get"](str(RID))),
                  ("different_update", lambda: scope["only_known_update"](12345678, metadata)),
                  ("changed_metadata_update", lambda: scope["only_known_update"](RID, {**metadata, "title": "changed"})),
                  ("pdf_upload", lambda: scope["only_approved_ZIP_upload"](BUCKET, newfiles[0])),
                  ("second_zip_upload", lambda: scope["only_approved_ZIP_upload"](BUCKET, newfiles[1]))]
        result["wrapper_negative_controls"] = []
        for label, probe in probes:
            before = copy.deepcopy(events)
            try:
                probe()
                passed = False
            except RuntimeError:
                passed = events == before
            result["wrapper_negative_controls"].append({"case": label, "control_pass": passed})
            result["control_pass"] = result["control_pass"] and passed
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    recipe_bytes = RECIPE.read_bytes()
    driver_bytes = (T / "publication_driver.py").read_bytes()
    tool_bytes = (ROOT / "zenodo_deposit_tool/zenodo.py").read_bytes()
    need(sha(recipe_bytes) == RECIPE_SHA, "Known-draft recipe differs from externally supplied pin")
    need(sha(driver_bytes) == DRIVER_SHA, "Approved driver bytes differ")
    need(sha(tool_bytes) == TOOL_SHA, "Unchanged upload tool bytes differ")
    names = ["exact_same_draft_repair", "three_round_gate", "final_clean_false", "wrong_source_manifest",
             "snapshot_drift", "missing_checkpoint", "existing_publication_intent", "existing_publish_receipt",
             "existing_replacement_intent", "driver_pin_drift", "fresh_claim_ineligible", "missing_initial_state",
             "other_initial_state", "already_published", "remote_metadata_drift", "extra_remote_file",
             "old_zip_md5_drift", "pdf_initial_md5_drift", "malformed_file_uuid", "delete_non204",
             "delete_nonempty204", "delete_redirect", "delete_unknown_outcome", "pdf_missing_after_delete",
             "returned_id_changed_after_delete", "state_lost_before_stage", "state_changed_before_stage",
             "pdf_missing_before_stage", "bucket_changed_before_stage", "zip_bytes_changed_before_upload",
             "zip_hardlinked_before_upload", "zip_symlinked_before_upload", "stage_metadata_drift"]
    results = [case(name, recipe_bytes, driver_bytes, tool_bytes) for name in names]
    total = len(results) + sum(len(r.get("wrapper_negative_controls", [])) for r in results)
    value = {"result": "MOCKED_KNOWN_DRAFT_REPAIR_CONTROLS_PASS" if all(r["control_pass"] for r in results) else "FAIL",
             "recipe_sha256": RECIPE_SHA, "driver_sha256": DRIVER_SHA, "original_tool_sha256": TOOL_SHA,
             "source_manifest_sha256": MF, "known_record_id": RID, "controls": total,
             "credentials_read": False, "network_accessed": False, "real_mutations": False,
             "driver_imported": False, "upload_tool_imported": False,
             "unchanged_upload_tool_functions_ast_extracted": True, "cases": results}
    if args.out:
        destination = args.out.resolve()
        need(destination.is_relative_to(OWN), "Output must stay inside the owned admin_scope")
        save(destination, value)
    print(json.dumps({k: v for k, v in value.items() if k != "cases"}, indent=2))
    if value["result"] == "FAIL":
        print(json.dumps([r for r in results if not r["control_pass"]], indent=2))
        raise SystemExit(1)

if __name__ == "__main__":
    main()
