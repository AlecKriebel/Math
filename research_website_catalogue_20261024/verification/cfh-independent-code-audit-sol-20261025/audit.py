"""Independent read-only audit of one sealed CFH proposal.

Executes only the inspected new source-view helper, never renderer/checker,
builders or finalizers. Changed reads are virtual; no sealed fixture changes.
Writes only this worker's namespace. No network, subprocess or Git calls.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from copy import deepcopy
from unittest.mock import patch
import ast
import difflib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STAGE = ROOT / "verification/local-cubic-fps-hessian-stage-sol-20261025"
IDS = ["23204952", "22983138", "23409904"]
NATIVE_READ = Path.read_bytes
READS = {}


def blob(path, purpose):
    path = Path(path)
    data = NATIVE_READ(path)
    item = READS.setdefault(str(path), {"bytes": len(data), "sha256": sha256(data).hexdigest(), "purposes": []})
    if purpose not in item["purposes"]:
        item["purposes"].append(purpose)
    return data


def obj(path, purpose):
    return json.loads(blob(path, purpose))


def snapshot():
    paths = set(p for p in STAGE.rglob("*") if p.is_file())
    for rid in IDS:
        paper = ROOT / "papers" / rid
        paths.update(p for p in (paper / "sources").rglob("*") if p.is_file())
        paths.update([paper / "publication.json", paper / "promotion.json"])
        for name in [f"root-clearance-{rid}-20261025.json", f"root-editorial-{rid}-20261025.json"]:
            paths.add(ROOT / "verification" / name)
        gate = obj(paper / "promotion.json", "whole original promotion object and review/custody paths")
        paths.add(ROOT / gate["root_custody_receipt"])
        paths.add(paper / "reviews/editorial/SEAL.json")
        editorial = obj(paper / "reviews/editorial/SEAL.json", "whole original editorial seal and owned bindings")
        paths.update(paper / relative for relative in editorial["owned_output_bindings"])
        paths.update(ROOT / relative for relative in editorial.get("common_owned_editorial_code_bindings", {}))
        for review in gate["reviews"].values():
            paths.update([paper / review["report"], paper / review["verdict_file"]])
    paths.update(ROOT / p for p in ["scripts/render_page.py", "verification/final-content-check.py", "scripts/bosonic_source.py", "scripts/published_assets.py", "scripts/dipole_source.py"])
    return {str(path): {"bytes": len(data), "sha256": sha256(data).hexdigest()}
            for path in sorted(paths) for data in [blob(path, "preservation byte binding only unless another purpose is listed")]}


def write(name, value):
    path = HERE / name
    if path.exists():
        raise RuntimeError("Refusing evidence overwrite: " + name)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    before = snapshot()
    seal = blob(STAGE / "stage-readiness-manifest.json", "authenticate actual readiness manifest")
    assert sha256(seal).hexdigest() == "bfebb68338fb0bace50ad3e6e99cd7bc0fb97dab49747334f201603c31ffb2bf"
    manifest = json.loads(seal)
    manifest_shape = {key: {"type": type(value).__name__, "length": len(value) if hasattr(value, "__len__") else None} for key,value in manifest.items()}
    code_paths = ["cfh_source.py", "render_page.proposed.py", "final-content-check.proposed.py",
                  "render_page.stage.py", "final-content-check.stage.py", "proposed-shared-renderer.diff",
                  "proposed-shared-checker.diff", "renderer-staging-overrides.diff", "checker-staging-overrides.diff"]
    for name in code_paths:
        data = blob(STAGE / name, "complete actual changed-code or diff read")
        if name.endswith(".py"):
            ast.parse(data)
    blob(ROOT / "scripts/bosonic_source.py", "complete contained_file/digest dependency inspected before helper execution")
    blob(ROOT / "scripts/published_assets.py", "complete independent asset resolver inspected for downstream containment")
    comparisons = {}
    for label, old_rel, proposed, diff_name, a, b in [
        ("renderer", "scripts/render_page.py", "render_page.proposed.py", "proposed-shared-renderer.diff", "a/scripts/render_page.py", "b/scripts/render_page.py"),
        ("checker", "verification/final-content-check.py", "final-content-check.proposed.py", "proposed-shared-checker.diff", "a/verification/final-content-check.py", "b/verification/final-content-check.py"),
    ]:
        original = blob(ROOT / old_rel, "actual current implementation for direct diff")
        frozen_original = blob(STAGE / "inputs" / Path(old_rel).name, "frozen baseline bytes")
        assert original == frozen_original
        changed = blob(STAGE / proposed, "actual proposed full code")
        direct = "".join(difflib.unified_diff(original.decode().splitlines(keepends=True), changed.decode().splitlines(keepends=True), fromfile=a,tofile=b))
        assert direct == blob(STAGE / diff_name, "validate reported diff against actual code").decode()
        comparisons[label] = {"actual_current_equals_frozen_input": True, "actual_diff_equals_reported_diff": True,
                              "original_sha256": sha256(original).hexdigest(), "proposed_sha256": sha256(changed).hexdigest()}
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("cfh_independent_inspected_helper", STAGE / "cfh_source.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    configs = {}; gates = {}; original_summary = {}
    for rid in IDS:
        paper = ROOT / "papers" / rid
        config = configs[rid] = obj(paper / "publication.json", "whole exact publication object")
        gate = gates[rid] = obj(paper / "promotion.json", "whole exact promotion object")
        receipt = obj(paper / "sources/receipt.json", "whole exact original receipt")
        science = obj(ROOT / gate["root_clearance_file"], "whole separate root scientific authority")
        editorial = obj(ROOT / "verification" / f"root-editorial-{rid}-20261025.json", "whole separate root editorial authority")
        meta = obj(paper / config["source_binding"]["metadata_path"], "whole exact actual metadata")
        raw_record = obj(paper / config["source_binding"]["record_path"], "whole actual record object")
        if rid == "23204952":
            raw_api = obj(paper / "sources/record/api.raw.json", "whole actual cubic raw API")
        else:
            raw_api = raw_record
        assert receipt == gate["source_receipt_record"]
        assert receipt["files"] == gate["source_files"] == config["source_binding"]["files"]
        assert science == gate["root_clearance_record"]
        for role, review in gate["reviews"].items():
            full = obj(paper / review["verdict_file"], "whole original custom verdict, no status projection")
            assert full == review["verdict"]
            assert science["reviews"][role] == review["root_authority_entry"]
        assert gate["rendered_copy_verified"] is gate["live_verified"] is gate["browser_verified"] is False
        assert gate["native_sheet_aa_url"] is gate["follow_up"] is config["follow_up"] is science["follow_up"] is None
        original_summary[rid] = {"receipt_entries": len(receipt["files"]), "actual_api_files": len(raw_api["files"]),
             "receipt_fields_per_entry": [sorted(item) for item in receipt["files"]],
             "whole_verdicts_equal": True, "separate_root_authority_equal": True,
             "publication_gates_remain_false": True, "alias_exists": (paper / "sources/record.json").exists(),
             "original_abstract_sha256": sha256(config["source_binding"]["abstract_tex"].encode()).hexdigest()}
    controls = []

    def exercise(label, rid, target=None, transform=None, missing=False, symlink=False, alias=False, config_change=None):
        config, gate = deepcopy(configs[rid]), deepcopy(gates[rid])
        config_before, gate_before = deepcopy(config), deepcopy(gate)
        if config_change:
            config_change(config)
        target = Path(target) if target else None
        native_symlink, native_exists = Path.is_symlink, Path.exists
        def changed_read(path):
            data = blob(path, "new helper authentication read under bounded virtual control")
            if target is not None and path == target:
                if missing:
                    raise FileNotFoundError("Virtual missing read: " + str(path))
                if transform:
                    return transform(data)
            return data
        def changed_symlink(path):
            return True if symlink and path == target else native_symlink(path)
        def changed_exists(path):
            return True if alias and path == target else native_exists(path)
        error = None
        result = None
        try:
            with patch.object(Path, "read_bytes", changed_read), patch.object(Path, "is_symlink", changed_symlink), patch.object(Path, "exists", changed_exists):
                result = helper.cfh_source_view(ROOT / "papers" / rid, config, gate)
        except Exception as exc:
            error = type(exc).__name__ + ": " + str(exc)
        negative = bool(target or config_change)
        assert (error is not None) == negative, (label, error)
        if not negative:
            raw, selected, asset_root = result
            assert raw == gates[rid]["source_receipt_record"]
            assert len(selected["files"]) == {"23204952":2,"22983138":3,"23409904":2}[rid]
            old_raw = deepcopy(raw)
            selected["files"][0]["audit_mutation_sentinel"] = True
            assert raw == old_raw
            assert config == config_before and gate == gate_before
        controls.append({"label":label, "record_id":rid, "negative":negative, "rejected":error is not None,
                         "exception":error, "expected_outcome_pass":True})

    for rid in IDS:
        exercise("exact original positive and independent ephemeral copy", rid)
    def mutate_json(fn):
        def transform(data):
            value=json.loads(data);fn(value);return json.dumps(value).encode()
        return transform
    p = lambda rid, rel: ROOT / "papers" / rid / rel
    exercise("missing metadata read", "22983138", p("22983138","sources/metadata.normalized.json"), missing=True)
    exercise("truncated raw record", "23409904", p("23409904","sources/zenodo-record.raw.json"), transform=lambda b:b[:80])
    exercise("wrong title in cubic actual metadata", "23204952", p("23204952","sources/record.json"), transform=mutate_json(lambda j:j["metadata"].update(title="Wrong title")))
    exercise("missing published abstract field", "22983138", p("22983138","publication.json"), transform=mutate_json(lambda j:j.pop("abstract")))
    exercise("cubic invented transport status", "23204952", p("23204952","sources/receipt.json"), transform=mutate_json(lambda j:j["files"][0].update(status=200)))
    exercise("FPS deleted genuine third checksum receipt", "22983138", p("22983138","sources/receipt.json"), transform=mutate_json(lambda j:j["files"].pop(0)))
    exercise("Hessian promoted endpoint into fake asset", "23409904", p("23409904","sources/receipt.json"), transform=mutate_json(lambda j:j["files"][2].update(actual_file_object={"key":"versions.raw.json"})))
    exercise("truncated complete original custom verdict", "23204952", p("23204952",gates["23204952"]["reviews"]["scope"]["verdict_file"]), transform=lambda b:b[:80])
    exercise("missing root authority read", "23409904", ROOT / gates["23409904"]["root_clearance_file"], missing=True)
    exercise("wrong root editorial authority", "22983138", ROOT / "verification/root-editorial-22983138-20261025.json", transform=mutate_json(lambda j:j.update(status="PASS")))
    exercise("truncated abstract source", "23409904", p("23409904",configs["23409904"]["source_binding"]["source_tex_path"]), transform=lambda b:b[:80])
    exercise("truncated original PDF", "23204952", p("23204952","sources/paper.pdf"), transform=lambda b:b[:80])
    exercise("truncated 170-byte checksum", "22983138", p("22983138","sources/SHA256SUMS"), transform=lambda b:b[:80])
    exercise("invented FPS record alias", "22983138", p("22983138","sources/record.json"), alias=True)
    exercise("source PDF symlink", "23204952", p("23204952","sources/paper.pdf"), symlink=True)
    exercise("metadata path escape in passed binding", "22983138", config_change=lambda j:j["source_binding"].update(metadata_path="../publication.json"))
    exercise("truncated passed abstract", "22983138", config_change=lambda j:j.update(abstract=j["abstract"][:40]))
    exercise("missing passed abstract", "23409904", config_change=lambda j:j.pop("abstract"))
    after = snapshot()
    assert before == after
    write("PRESERVATION_BINDINGS.json", {"utc":datetime.now(timezone.utc).isoformat(),"status":"ALL_BOUND_BYTES_UNCHANGED","count":len(before),"before":before,"after_identical":True})
    write("READ_LEDGER.json", {"utc":datetime.now(timezone.utc).isoformat(),"reads":READS})
    write("CODE_AUTHORITY_CONTROLS.json", {"utc":datetime.now(timezone.utc).isoformat(),"manifest_shape":manifest_shape,"direct_code_comparisons":comparisons,"original_object_summary":original_summary,"controls":controls,"all_expected_outcomes_pass":True,"whole_old_checker_repeated":False,"builders_or_finalizers_executed":False})
    print(json.dumps({"preserved_bindings":len(before),"controls":len(controls),"all_expected_outcomes_pass":True,"manifest_shape":manifest_shape},indent=2))
