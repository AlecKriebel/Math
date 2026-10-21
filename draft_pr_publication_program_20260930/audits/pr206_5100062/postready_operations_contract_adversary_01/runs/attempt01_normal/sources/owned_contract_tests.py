#!/usr/bin/env python3
"""Independent owned synthetic operational contract falsification.

All fixtures are invented under this audit directory. Actual records are never
read, executed, copied into fixtures, or treated as synthetic authority. All
service and child-process effects are prohibited by an audit hook and mocks.
"""
import ast
import contextlib
import copy
import datetime
import hashlib
import io
import json
import os
import pathlib
import re
import stat
import sys
import tempfile
import types

OWN = pathlib.Path(__file__).resolve().parent
BASE = OWN.parent
MODE = sys.argv[1] if len(sys.argv) == 2 else "invalid"
TESTS = []
CHECKS = 0

def check(ok, message):
    global CHECKS
    CHECKS += 1
    if type(ok) is not bool or not ok:
        raise RuntimeError("AUDIT CHECK: " + message)

def pin(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def enc(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()

def read_source(rel):
    p = BASE / rel
    data = p.read_bytes()
    check(pin(data) == FINAL_PINS[rel], "final source bytes " + rel)
    return data

def no_effects(event, args):
    if event.startswith("socket.") or event in ("subprocess.Popen", "os.system", "os.posix_spawn", "os.fork", "pty.spawn", "urllib.Request"):
        raise RuntimeError("AUDIT PROHIBITED EFFECT: " + event)
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        flags = args[2] if len(args) > 2 else 0
        if type(flags) is int and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            p = pathlib.Path(os.fsdecode(args[0])).resolve()
            if not p.is_relative_to(OWN):
                raise RuntimeError("AUDIT WRITE OUTSIDE OWNED FIXTURE")
    if event in ("os.chmod", "os.mkdir", "os.rmdir", "os.remove", "os.rename", "os.link", "os.symlink"):
        for value in args[:2] if event in ("os.rename", "os.link") else args[:1]:
            if isinstance(value, (str, bytes, os.PathLike)):
                p = pathlib.Path(os.fsdecode(value)).resolve()
                if not p.is_relative_to(OWN):
                    raise RuntimeError("AUDIT MUTATION OUTSIDE OWNED FIXTURE")
    if event == "import":
        name = args[0]
        if isinstance(name, str) and name.split(".")[0] in ("requests", "httpx", "gws", "zenodo", "backend", "adapter", "cache", "github"):
            raise RuntimeError("AUDIT PROHIBITED SERVICE MODULE IMPORT: " + name)

FINAL = json.loads((OWN / "FINAL_SOURCE_PINS.json").read_bytes())
FINAL_PINS = FINAL["sources"]
sys.addaudithook(no_effects)
SYN = types.ModuleType("independent_synthetic_model")
exec(compile((OWN / "synthetic_model.py").read_bytes(), str(OWN / "synthetic_model.py"), "exec"), SYN.__dict__)

@contextlib.contextmanager
def fixture(name):
    p = pathlib.Path(tempfile.mkdtemp(prefix="SYNTHETIC_" + name + "_", dir=OWN / "fixtures"))
    (p / "SYNTHETIC_ONLY.txt").write_text("EXPLICIT SYNTHETIC OFFLINE FIXTURE. NO ACTUAL AUTHORITY. NO SERVICE ACTION.\n")
    yield p

def put(path, raw, mode=0o444):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        if path.is_file() and not path.is_symlink():
            path.chmod(0o600)
        path.unlink()
    path.write_bytes(raw)
    path.chmod(mode)
    return pin(raw)

def put_json(path, value):
    return put(path, enc(value))

def test(name, fn):
    before = CHECKS
    fn()
    TESTS.append({"name": name, "checks": CHECKS - before, "passed": True})

def refusal(fn, fragment=None):
    try:
        fn()
    except (RuntimeError, ValueError, KeyError, TypeError, FileNotFoundError, SystemExit, OSError) as error:
        if fragment is not None:
            check(fragment in str(error), "expected refusal reason " + repr(fragment) + " got " + repr(str(error)))
        check(True, "deliberate refusal")
        return type(error).__name__, str(error)
    raise RuntimeError("AUDIT CHECK: expected refusal did not occur")

def module_from_source(name, rel):
    raw = read_source(rel)
    m = types.ModuleType(name)
    m.__file__ = str(BASE / rel)
    m.__package__ = ""
    exec(compile(raw, m.__file__, "exec"), m.__dict__)
    return m

class SyntheticAuthority:
    def __init__(self, base):
        self.base = base
        self.package = base / "SYNTHETIC_PACKAGE_17"
        self.metadata = {"title": "EXPLICIT SYNTHETIC OFFLINE note", "description": "Synthetic contract: Ferudun DOI 10.5281/zenodo.23096994 credited.", "creators": [{"name": "Kriebel, Alec", "orcid": "0009-0001-9320-500X"}]}
        self.uploads = {"SYNTHETIC_NOTE.pdf": b"SYNTHETIC PDF\n", "SYNTHETIC_NOTE.tex": b"SYNTHETIC TEX\n", "SYNTHETIC_ORIGINAL_ARCHIVE.zip": b"SYNTHETIC IMMUTABLE ORIGINAL ARCHIVE\n"}
        for name, raw in self.uploads.items(): put(self.package / name, raw)
        put_json(self.package / "zenodo-deposit.json", {"metadata": self.metadata, "files": [{"path": n} for n in sorted(self.uploads)]})
        put_json(self.package / "PACKAGE_SEAL.json", {"EXPLICIT_SYNTHETIC_ONLY": True})
        for i in range(12): put(self.package / ("SYNTHETIC_SUPPORT_%02d.txt" % i), ("synthetic packet %d\n" % i).encode())
        self.safe = {p.name: pin(p.read_bytes()) for p in self.package.iterdir()}
        check(len(self.safe) == 17, "synthetic scientific packet exact17")
        self.other = {}
        self.preparation = {}
        for role in ("mathematics", "priority", "portable", "package", "visual"):
            rel = "SYNTHETIC_PREPARATION/" + role + ".json"
            v = put_json(base / rel, {"EXPLICIT_SYNTHETIC_ONLY": True, "role": role})
            self.other[rel] = v
            self.preparation[role] = {"path": rel, **v}
        c.PRIORITY_PIN = put(base / "ROOT_PRIORITY_EDITORIAL_GATE_01.json", b"EXPLICIT SYNTHETIC PRIORITY FACT\n")
        c.CUSTODY_PIN = put(base / "ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json", b"EXPLICIT SYNTHETIC CUSTODY FACT\n")
        self.other.update({"ROOT_PRIORITY_EDITORIAL_GATE_01.json": c.PRIORITY_PIN, "ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json": c.CUSTODY_PIN})
        self.historical = "publication_operations_preparation_01/ops_common206.py"
        self.other[self.historical] = put(base / self.historical, b"EXPLICIT SYNTHETIC FROZEN ORIGINAL07; NEVER EXECUTE\n")
        self.events = []
        for index in (1, 2):
            rel = "SYNTHETIC_REVIEW_%d" % index
            rp = put(base / rel / "REPORT.txt", ("EXPLICIT SYNTHETIC REPORT %d\n" % index).encode())
            e = {"review_number": index, "directory": rel, "report_file": "REPORT.txt", "safe_files": {"REPORT.txt": rp}, "report_pin": rp, "reviewed_package": self.package.name, "reviewed_package_seal": self.safe["PACKAGE_SEAL.json"], "verdict": "CLEANPASS", "whole_package_scope": True, "open_findings": 0}
            name = "SYNTHETIC_REVIEW_ACCEPTANCE_%d.json" % index
            ap = put_json(base / name, {"PR": 206, "original_head": SYN.HEAD, "review_accepted": True, "NEW_whole_package_reviews_completed": index, "review_cycle_repairs_required_now": False, "review_event": copy.deepcopy(e)})
            self.events.append({**e, "Root_acceptance_file": name, "Root_acceptance_pin": ap})
        self.gate = {"PR": 206, "problem_id": 5100062, "original_head": SYN.HEAD, "package": self.package.name, "package_seal": self.safe["PACKAGE_SEAL.json"], "package_safe_files": self.safe, "metadata_file": "zenodo-deposit.json", "metadata": self.metadata, "intended_upload_files": {n: self.safe[n] for n in self.uploads}, "other_safe_files": self.other, "preparation_receipts": self.preparation, "whole_package_review_events": self.events}
        self.gate.update({k: True for k in ("publication_ready_gate_accepted", "whole_package_review_loop_complete", "mathematical_clearance", "source_contract_clearance", "bounded_priority_audit_complete", "current_portable_verifier_accepted", "qualified_attributed_note_editorially_cleared")})
        self.gp = base / "ROOT_PUBLICATION_GATE_01.json"
        gatepin = put_json(self.gp, self.gate)
        inputs = {"ROOT_PUBLICATION_GATE_01.json": self.gp}
        inputs.update({self.package.name + "/" + n: self.package / n for n in self.safe})
        inputs.update({n: base / n for n in self.other})
        for e in self.events:
            inputs[e["directory"] + "/REPORT.txt"] = base / e["directory"] / "REPORT.txt"
            inputs[e["Root_acceptance_file"]] = base / e["Root_acceptance_file"]
        self.selected = SYN.selected_map({SYN.PREFIX + n: SYN.identity(p.read_bytes()) for n, p in inputs.items()})
        self.checkpoint = base / "SYNTHETIC_OFFLINE_READY"
        self.mp = self.checkpoint / "ACCEPTANCE_CURRENT_SELECTED_MAP.json"
        self.mapping = {"selected_files": self.selected, "selected_map_sha256": SYN.map_digest(self.selected), "foreign_QUEUE_reconciliation_after_checkpoint": {}}
        self.map_pin = put_json(self.mp, self.mapping)
        self.ac = SYN.acceptance(self.selected, gatepin, self.package.name, self.gate["package_seal"], self.map_pin)
        self.ap = self.checkpoint / "ACCEPTANCE.json"
        self.r = SYN.pointer(put_json(self.ap, self.ac))
        self.rp = base / "ROOT_ACTUAL_READY_CHECKPOINT.json"
        rpin = put_json(self.rp, self.r)
        self.vp = base / "ROOT_ACTUAL_READY_VERIFICATION_01.json"
        self.v = SYN.proof(self.selected, gatepin, rpin, self.r["acceptance_pin"], self.map_pin)
        vpin = put_json(self.vp, self.v)
        self.sources = {}
        for name in c.CODES:
            rel = c.OWN + "/" + name
            self.sources[rel] = put(base / rel, read_source(rel))
        for rel in (DISPATCHER_REL, CAPTURE_REL): put(base / rel, read_source(rel))
        self.adoption = {"schema": "pr206-root-publication-operations-adoption-v1", "evidence_scope": "ACTUAL_ROOT_RECEIPT", "PR": 206, "original_head": SYN.HEAD, "accepted_preparation_only": True, "sources": self.sources, "dispatcher_pin": FINAL_PINS[DISPATCHER_REL], "capture_manager_pin": FINAL_PINS[CAPTURE_REL], "approved_publication_gate_pin": gatepin, "approved_actual_ready_pointer_pin": rpin, "approved_actual_ready_verification_pin": vpin}
        self.adp = base / "ROOT_PUBLICATION_OPERATIONS_ADOPTION_01.json"
        self.addp = base / "ROOT_PUBLICATION_OPERATIONS_CONTRACT_ADDENDUM_01.json"
        self.reapprove()
    def reapprove(self, update_addendum=True):
        if update_addendum:
            self.addendum = {"schema": "pr206-root-postready-operations-contract-addendum-v1", "evidence_scope": "ACTUAL_ROOT_RECEIPT", "PR": 206, "accepted": True, "original_head": SYN.HEAD, "publication_gate_pin": self.adoption["approved_publication_gate_pin"], "actual_ready_pointer_pin": self.adoption["approved_actual_ready_pointer_pin"], "actual_ready_verification_pin": self.adoption["approved_actual_ready_verification_pin"], "source_family": c.OWN, "sources": copy.deepcopy(self.sources), "dispatcher_pin": self.adoption["dispatcher_pin"]}
            self.addendum.update({k: True for k in ("scientific_package_metadata_uploads_unchanged", "prior_native_selected_original07_files_preserved", "operations_sources_approved_after_original_ready_checkpoint", "not_a_new_scientific_or_priority_clearance", "no_advance_or_completion_granted")})
            self.addendum["executed_current_sources_claimed_present_in_original_ready_map"] = False
            self.adoption["approved_operations_contract_addendum_pin"] = put_json(self.addp, self.addendum)
        self.adoption_pin = put_json(self.adp, self.adoption)
        c.configure_authority(self.adp.name, self.adoption_pin)
    def approve_proof(self):
        self.adoption["approved_actual_ready_verification_pin"] = put_json(self.vp, self.v)
        self.reapprove()
    def context(self): return c.load_context(self.base)


def reference_module():
    rel = "publication_lifecycle_preparation_02/support206.py"
    raw = (BASE / rel).read_bytes()
    check(pin(raw) == {"bytes": 77413, "sha256": "b1de89de16876c02d8d18d76ef85eff2b3cb4654f699871c90df302d59302367"}, "immutable producer/consumer reference source pin")
    tree = ast.parse(raw)
    funcs = {"need", "rel", "bytepin", "enc", "digest", "check_acceptance", "operations", "tracker_row"}
    consts = {"RECEIPT_ALIASES", "BASE_COUNTS", "PHASES", "HEAD", "Q", "CLAIM", "CREDIT", "EFFORT", "MAX_BYTES", "MAX_SELECTED"}
    nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in funcs) or (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id in consts for x in n.targets))]
    m = types.ModuleType("independent_lifecycle_AST_only")
    m.__dict__.update({"json": json, "hashlib": hashlib, "re": re, "datetime": datetime})
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), str(BASE / rel) + "::AST_ONLY", "exec"), m.__dict__)
    return m


def producer_and_context():
    with fixture("producer") as root:
        f = SyntheticAuthority(root)
        check(set(f.ac["facts"]) == {"DOI", "NEW_whole_package_reviews_completed", "Root_publication_gate_pin", "actual_factual_accepted", "actual_merge_accepted", "actual_original_PR_merged", "actual_publication_verified", "actual_tracker_row_verified", "advance_to_next_PR_authorized_now", "bounded_priority_audit_complete", "case_percent", "completed", "fully_completed_count", "goal_complete", "historical_firstness_independence_established", "last_completed_PR", "mathematical_clearance", "next_numeric_intake_cursor", "package", "package_seal", "priority_clearance", "priority_clearance_scope", "priority_novelty_clearance", "publication_ready", "published_count", "qualified_attributed_note_editorially_cleared", "record_id", "source_contract_clearance", "tracker_range", "whole_package_review_loop_complete"}, "synthetic nested facts exact emitted key shape")
        check(not any(k in f.ac for k in ("QUEUE_native_original_PR_unchanged", "bounded_priority_audit_complete", "qualified_attributed_note_editorially_cleared")), "synthetic receipt does not smuggle nonexistent aliases")
        lifecycle.check_acceptance("ready", f.ac, f.mapping, {"expected_main": SYN.PARENT, "commit": SYN.CHECKPOINT}, f.selected, f.ac["facts"], [SYN.PARENT])
        ctx = f.context()
        check(set(c.context_pin(ctx)) == {"gate_pin", "ready_pointer_pin", "ready_acceptance_pin", "checkpoint_commit", "package_seal", "package", "manifest_pin"}, "exact context7")
        check(c.context_pin(ctx)["ready_acceptance_pin"] == pin(f.ap.read_bytes()), "strict producer shape passes new consumer with proof")
        original = (root / f.historical).read_bytes()
        check(len(f.selected) == 4788 and f.v["ready_candidate_changed_path_count"] == 377, "owned model matches declared external actual snapshot counts")
        check(not any(SYN.PREFIX + c.OWN + "/" + n in f.selected for n in c.CODES), "current sources not falsely present in original ready map")
        f.reapprove()
        f.context()
        check((root / f.historical).read_bytes() == original, "postready approval preserves frozen original operator bytes")
        put(root / f.historical, original + b"CHANGED")
        refusal(f.context, "Supporting input changed")


def proof_chain_tests():
    with fixture("proof_chain") as root:
        f = SyntheticAuthority(root)
        f.context()
        original = f.vp.read_bytes()
        approved = copy.deepcopy(f.adoption)
        for field, value in [("ready_candidate_changed_path_count", 1), ("checkpoint_commit", "a" * 40), ("actual_ready_pointer_pin", SYN.pin(b"CROSS POINTER")), ("accepted", False)]:
            changed = copy.deepcopy(f.v); changed[field] = value
            put_json(f.vp, changed)
            refusal(f.context, "Pinned JSON bytes changed before parsing")
            check(f.adoption == approved and f.adoption_pin == pin(f.adp.read_bytes()), "unapproved mutation preserves external adoption")
            put(f.vp, original)
        put_json(f.vp, {"schema": "REPLACEMENT", "accepted": True, "self_rehashed": SYN.pin(original)})
        refusal(f.context, "Pinned JSON bytes changed before parsing")
        put(f.vp, original)
        for key in ("approved_actual_ready_verification_pin", "approved_operations_contract_addendum_pin"):
            saved = f.adoption.pop(key); f.reapprove(update_addendum=False)
            refusal(f.context, "pin absent")
            f.adoption[key] = saved; f.reapprove(update_addendum=False)
        f.v["actual_ready_pointer_pin"] = SYN.pin(b"OTHER SYNTHETIC POINTER")
        f.approve_proof()
        refusal(f.context, "cross-binding differs")
    for field, value in [("all_three_actual_steps_and_six_alias_cleanups_verified", 1), ("original_native_custody_retained", False), ("actual_main_observed", "a" * 40), ("actual_selected_map_sha256", "0" * 64), ("actual_publication", True)]:
        with fixture("reapproved_proof") as root:
            f = SyntheticAuthority(root); f.v[field] = value; f.approve_proof()
            refusal(f.context)
    with fixture("postimage_composite") as root:
        f = SyntheticAuthority(root)
        f.v["all_five_local_readonly_native_postimages"][-1] = copy.deepcopy(f.v["all_five_local_readonly_native_postimages"][0])
        f.approve_proof(); refusal(f.context, "Malformed/duplicate/nonreadonly")
    with fixture("identity_type") as root:
        f = SyntheticAuthority(root)
        f.v["all_five_local_readonly_native_postimages"][0]["identity"] = {**f.v["all_five_local_readonly_native_postimages"][0]["identity"], "bytes": True}
        f.approve_proof(); refusal(f.context, "Malformed native postimage identity")
    with fixture("nested_scope") as root:
        f = SyntheticAuthority(root); ac = copy.deepcopy(f.ac); ac["facts"]["priority_clearance_scope"] = "SYNTHETIC_NOVELTY"
        refusal(lambda: c.ready_facts(ac, f.gate), "qualified-priority scope")
        ac = copy.deepcopy(f.ac); ac["bounded_priority_audit_complete"] = True; ac["facts"]["bounded_priority_audit_complete"] = False
        refusal(lambda: c.ready_facts(ac, f.gate), "facts not accepted")
    with fixture("generic_count_limitation") as root:
        f = SyntheticAuthority(root); f.v["ready_candidate_changed_path_count"] = 1; f.approve_proof(); f.context()
        check(True, "DOCUMENTED LIMIT: new external Root authority may approve a different positive changed count; actual Root proof remains exact377")


def pinned_buffer_and_addendum():
    class OneBuffer:
        def __init__(self, raw): self.raw = raw; self.calls = 0
        def read_bytes(self): self.calls += 1; return self.raw if self.calls == 1 else b"DIFFERENT"
    x = OneBuffer(enc({"synthetic": True})); check(c.read_pinned(x, pin(x.raw)) == {"synthetic": True} and x.calls == 1, "one authenticated buffer parsed exactly once")
    real_loads = c.json.loads; parses = []
    def watched(*a, **k): parses.append(True); return real_loads(*a, **k)
    c.json.loads = watched
    try: refusal(lambda: c.read_pinned(OneBuffer(b"{not-json"), pin(b"DIFFERENT")), "before parsing")
    finally: c.json.loads = real_loads
    check(not parses, "pin mismatch precedes JSON interpretation")
    for field, value in [("dispatcher_pin", SYN.pin(b"OTHER DISPATCHER")), ("actual_ready_verification_pin", SYN.pin(b"OTHER PROOF")), ("source_family", "publication_operations_preparation_01"), ("scientific_package_metadata_uploads_unchanged", 1), ("executed_current_sources_claimed_present_in_original_ready_map", True), ("no_advance_or_completion_granted", False)]:
        with fixture("addendum") as root:
            f = SyntheticAuthority(root); f.addendum[field] = value
            f.adoption["approved_operations_contract_addendum_pin"] = put_json(f.addp, f.addendum); f.reapprove(update_addendum=False)
            refusal(f.context)
    for value in (1, "True", [], None): refusal(lambda value=value: c.require(value, "must be bool"), "actual bool")

class OwnedKit:
    def __init__(self, f, lose=None): self.f=f; self.id=987654321001; self.published=False; self.calls=[]; self.lose=lose
    def run(self, argv, env):
        mode=argv[6]; self.calls.append(mode)
        check(argv[1:5] == ["-E", "-S", "-B", "-P"], "synthetic kit child flags")
        marker=self.f.base/"private_operations/zenodo"/(mode.upper()+"_INFLIGHT.json")
        if mode in ("stage", "publish"): check(marker.is_file(), "intent exists before fake mutation")
        if mode == "publish": self.published=True
        if self.lose == mode: raise OSError("SYNTHETIC LOST RESPONSE")
        j={"environment":"production", "id":self.id, "state":"published" if self.published else "ready_to_publish", "title":self.f.metadata["title"], "metadata_normalizations":[], "files":[{"name":n,"size":v["bytes"],"sha256":v["sha256"]} for n,v in self.f.gate["intended_upload_files"].items()]}
        if self.published: j.update({"record_url":"https://zenodo.org/records/"+str(self.id),"doi":"10.5281/zenodo."+str(self.id),"doi_url":"https://doi.org/10.5281/zenodo."+str(self.id),"doi_resolution":{"status":"resolved","http_status":200}})
        return types.SimpleNamespace(returncode=0,stdout=json.dumps(j),stderr="")
class OwnedPublic:
    def __init__(self,f,ident): self.f=f; self.id=ident; self.calls=[]
    def get(self,url,limit):
        self.calls.append(url)
        if url.startswith("https://doi.org/"): return 200,b"","https://zenodo.org/records/"+str(self.id)
        n=url.split("/files/",1)[1].split("/content",1)[0]
        return 200,self.f.uploads[n],url

def prepare_publication(f, lose=None):
    ctx=f.context(); kit=OwnedKit(f,lose); public=OwnedPublic(f,kit.id)
    pub=publisher.Publisher(f.base,f.base/"SYNTHETIC_KIT/zenodo.py",kit,public)
    pub.facts=lambda:(f.context(),f.base/"SYNTHETIC_KIT/zenodo.py")
    return pub,kit,public

def published_fixture(f):
    pub,kit,public=prepare_publication(f)
    pub.invoke("stage"); pub.invoke("publish",kit.id); pub.invoke("inspect-doi",kit.id)
    result=pub.finalize()
    check(len(public.calls)==4 and len(result["package_safe_files"])==17, "three synthetic downloads plus DOI and exact17 packet")
    return result

class OwnedSheet:
    def __init__(self,f,behavior=None): self.f=f; self.behavior=behavior; self.data=[list(tracker.HEADERS),["FOREIGN","","","duplicate"],["FOREIGN","","","duplicate"],[True,1,"TYPED",""]]; self.appends=0; self.reads=0
    def run(self,resources,params,body=None):
        if resources==["spreadsheets","get"]:
            j={"spreadsheetId":tracker.SID,"sheets":[{"properties":{"sheetId":tracker.GID,"title":tracker.TAB,"gridProperties":{"columnCount":4}}}]}
        elif resources[-1]=="append":
            self.appends+=1
            check(params["valueInputOption"]=="RAW" and params["insertDataOption"]=="INSERT_ROWS" and len(body["values"])==1, "one synthetic RAW INSERT_ROWS request")
            self.data.append(copy.deepcopy(body["values"][0]))
            if self.behavior=="lost_after": raise OSError("SYNTHETIC LOST APPEND RESPONSE")
            n=len(self.data); j={"spreadsheetId":tracker.SID,"updates":{"updatedRows":1,"updatedColumns":4,"updatedCells":4,"updatedRange":"'Math Puzzles'!A%d:D%d"%(n,n),"updatedData":{"values":body["values"]}}}
        elif params["range"]==tracker.FULL_RANGE:
            self.reads+=1
            if self.behavior=="second_foreign_loss" and self.reads==4: self.data.pop(1)
            j={"values":copy.deepcopy(self.data)}
        else:
            n=int(params["range"].split("!A")[1].split(":D")[0]); j={"values":[copy.deepcopy(self.data[n-1])]}
        return types.SimpleNamespace(returncode=0,stdout=json.dumps(j),stderr="")

def downstream_and_mutations():
    with fixture("downstream") as root:
        f=SyntheticAuthority(root); pub=published_fixture(f); sheet=OwnedSheet(f)
        tr=tracker.Tracker(root,sheet).run()
        check(sheet.appends==1 and sheet.reads==4 and all(tr[k] is True for k in ("two_fresh_full_prechecks","two_fresh_full_readbacks","original_preappend_baseline_retained")), "literalTrue two-readback producer facts")
        check(set(tr["publication_facts"])=={"id","doi","doi_url","record_url","metadata","package","package_safe_files","intended_upload_files","original_head","problem_id"}, "exact copied publication facts ten keys")
        lifecycle.ready_context=lambda:(f.gate,c.context_pin(f.context()))
        artifacts={"ROOT_PUBLICATION_RECEIPT.json":pub,"ROOT_TRACKER_RECEIPT.json":tr}
        lifecycle.artifact=lambda name:copy.deepcopy(artifacts[name])
        lifecycle.frozen=lambda name:(root/name).read_bytes()
        lifecycle.pin=SYN.pin
        lifecycle.operations()
        check(True,"actual extracted downstream operations accepts real helper-produced synthetic receipts")
        for field in ("two_fresh_full_readbacks","two_fresh_full_prechecks"):
            artifacts["ROOT_TRACKER_RECEIPT.json"][field]=1
            refusal(lifecycle.operations,"Actual tracker prechecks/readback")
            artifacts["ROOT_TRACKER_RECEIPT.json"][field]=True
        artifacts["ROOT_TRACKER_RECEIPT.json"]["publication_facts"]["SYNTHETIC_EXTRA"]=True
        refusal(lifecycle.operations,"copied publication facts")
        artifacts["ROOT_TRACKER_RECEIPT.json"]["publication_facts"].pop("SYNTHETIC_EXTRA")
        artifacts["ROOT_PUBLICATION_RECEIPT.json"]["context"]["SYNTHETIC_EXTRA"]=True
        refusal(lifecycle.operations,"publication context")
        refusal(lambda:tracker.Tracker(root,sheet).run(),"Final tracker receipt exists")
        check(sheet.appends==1,"accepted tracker never appends again")
    for behavior in ("duplicate_doi","second_foreign_loss","lost_after"):
        with fixture("tracker_"+behavior) as root:
            f=SyntheticAuthority(root); pub=published_fixture(f); sheet=OwnedSheet(f,behavior)
            if behavior=="duplicate_doi": sheet.data += [["FOREIGN DOI",pub["doi"],"",""],["FOREIGN DOI2","",pub["doi"],""]]
            tr=tracker.Tracker(root,sheet); refusal(tr.run)
            check(not (root/"ROOT_TRACKER_RECEIPT.json").exists(),"failed synthetic tracker produces no accepted receipt")
            if behavior=="duplicate_doi":check(sheet.appends==0,"existing duplicate DOI blocks before append")
            elif behavior=="lost_after":
                marker=(tr.directory/"APPEND_INFLIGHT.json").read_bytes(); result=tr.run(True)
                check(result["recovered_unknown_outcome"] is True and sheet.appends==1 and (tr.directory/"APPEND_INFLIGHT.json").read_bytes()==marker,"uncertain append recovers read-only with original intent")
            else:
                refusal(lambda:tr.run(True));check(sheet.appends==1,"lost foreign multiplicity never causes append retry")
    for mode in ("stage","publish"):
        with fixture("unknown_"+mode) as root:
            f=SyntheticAuthority(root); pub,kit,public=prepare_publication(f,mode)
            if mode=="publish":pub.invoke("stage")
            refusal(lambda:pub.invoke(mode,kit.id if mode=="publish" else None),"outcome unknown")
            refusal(lambda:pub.invoke(mode,kit.id if mode=="publish" else None),"already attempted")
            check(kit.calls.count(mode)==1 and not public.calls and not (root/"ROOT_PUBLICATION_RECEIPT.json").exists(),"unknown mutation no retry or fabricated publication")


def with_argv(args, fn):
    prior=sys.argv; sys.argv=list(args)
    try:return fn()
    finally:sys.argv=prior


def dispatcher_tests():
    for action in ("preflight","append","inspect"):
        with fixture("dispatch_"+action) as root:
            f=SyntheticAuthority(root); m=module_from_source("owned_dispatcher",DISPATCHER_REL)
            m.A=root; m.D=root/pathlib.Path(DISPATCHER_REL).parent; m.__file__=str(root/DISPATCHER_REL)
            loaded=[]; calls=[]
            def fake_load(name,path,raw):
                check(pin(raw)==FINAL_PINS[c.OWN+"/"+path.name],"dispatcher uses authenticated operator buffer")
                loaded.append(name)
                q=types.ModuleType(name);sys.modules[name]=q
                if path.name=="ops_common206.py":q.configure_authority=lambda *a:None;q.load_context=lambda base:f.context();q.context_pin=c.context_pin
                else:q.main=lambda:calls.append(list(sys.argv))
                return q
            m.load_module=fake_load
            aliases=("ops_common206","Root_pr206_publisher","Root_pr206_tracker");old={n:sys.modules.get(n) for n in aliases};present={n:n in sys.modules for n in aliases}
            sentinels={n:types.ModuleType("prior_"+n) for n in aliases};sys.modules.update(sentinels)
            args=[m.__file__,"--adoption",f.adp.name,"--adoption-bytes",str(f.adoption_pin["bytes"]),"--adoption-sha256",f.adoption_pin["sha256"],action]
            if action=="inspect":args += ["--confirm-id","987654321001"]
            original_args=list(sys.argv)
            try:
                with contextlib.redirect_stdout(io.StringIO()):with_argv(args,m.main)
                check(all(sys.modules.get(n) is sentinels[n] for n in aliases),"dispatcher restores prior module aliases")
                check(sys.argv==original_args,"dispatcher restores argv")
                check((not calls) if action=="preflight" else len(calls)==1,"exact synthetic route count")
                if calls:check(("tracker206.py" in calls[0][0])==(action=="append"),"correct operator routing")
                if action=="inspect":check(calls[0][-2:]==["--confirm-id","987654321001"],"explicit ID forwarded")
                bad="SYNTHETIC_SECRET_ARGUMENT"
                out=io.StringIO();err=io.StringIO()
                with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):refusal(lambda:with_argv(args+[bad],m.entry))
                check(bad not in out.getvalue()+err.getvalue(),"safe parser does not echo rejected token")
                put(f.vp,b"{MALFORMED UNAPPROVED PROOF")
                before=len(loaded);refusal(lambda:with_argv(args,m.main),"Exact input pin")
                check(len(loaded)==before,"proof mismatch stops before all source compilation")
            finally:
                for n in aliases:
                    if present[n]:sys.modules[n]=old[n]
                    else:sys.modules.pop(n,None)
    with fixture("dispatch_nonregular") as root:
        f=SyntheticAuthority(root);m=module_from_source("owned_dispatcher_nonregular",DISPATCHER_REL);m.A=root
        p=root/"SYNTHETIC_FIFO";os.mkfifo(p)
        refusal(lambda:m.checked(p,SYN.pin(b"")),"Regular readonly input before open")
        p2=root/"SYNTHETIC_LINK";p2.symlink_to(f.vp)
        refusal(lambda:m.checked(p2,pin(f.vp.read_bytes())),"Normalized path")


def capture_tests():
    import subprocess as std_subprocess
    for behavior in ("completed","timeout"):
        with fixture("capture_"+behavior) as root:
            f=SyntheticAuthority(root);m=module_from_source("owned_capture",CAPTURE_REL);m.A=root;m.D=root/pathlib.Path(CAPTURE_REL).parent;m.__file__=str(root/CAPTURE_REL)
            calls=[]
            def fake_run(argv,**kwargs):
                calls.append(list(argv))
                check(kwargs["cwd"]==root and kwargs["timeout"]==600,"capture exact bounded one-child invocation")
                if behavior=="timeout":raise std_subprocess.TimeoutExpired(argv,600,output=b"SYNTHETIC PARTIAL",stderr=b"SYNTHETIC ERROR")
                return types.SimpleNamespace(stdout=b"SYNTHETIC CHILD OUTPUT\n",stderr=b"",returncode=0)
            m.subprocess=types.SimpleNamespace(run=fake_run,TimeoutExpired=std_subprocess.TimeoutExpired,PIPE=std_subprocess.PIPE)
            args=[m.__file__,"operations","publish","SYNTHETIC_TAG","--adoption-bytes",str(f.adoption_pin["bytes"]),"--adoption-sha256",f.adoption_pin["sha256"],"--confirm-id","987654321001"]
            with contextlib.redirect_stdout(io.StringIO()):
                try:with_argv(args,m.main)
                except SystemExit as e:check(e.code==(0 if behavior=="completed" else 124),"capture preserves child/timeout exit")
            check(len(calls)==1 and calls[0][1:5]==["-E","-S","-B","-P"] and calls[0][-2:]==["--confirm-id","987654321001"],"capture invokes one exact routed child")
            result=json.loads((m.D/"execution_records/operations_SYNTHETIC_TAG.RESULT.json").read_bytes())
            check(result["actual_phase_acceptance_or_publication_not_inferred_by_manager"] is True,"capture never promotes raw process result")
            if behavior=="timeout":check(result["exit_code"]==124 and "do not repeat mutation" in result["outcome"],"ambiguous timeout explicitly not success")
            refusal(lambda:with_argv(args,m.main))
            check(len(calls)==1,"same capture tag cannot retry ambiguous or completed child")


def optimized_early_refusal():
    import builtins
    for rel in (DISPATCHER_REL,CAPTURE_REL):
        raw=read_source(rel);seen=[];real=builtins.__import__
        def watched(name,*args,**kwargs):seen.append(name);return real(name,*args,**kwargs)
        scope={"__name__":"owned_optimized_refusal","__file__":str(BASE/rel),"__builtins__":dict(vars(builtins),__import__=watched)}
        refusal(lambda:exec(compile(raw,str(BASE/rel),"exec"),scope),"required")
        check(seen==["sys"],"optimized dispatcher/capture refuses before dependencies: "+rel)


def main():
    global c,publisher,tracker,lifecycle
    (OWN/"fixtures").mkdir(exist_ok=True)
    for rel in FINAL_PINS:
        raw=read_source(rel);tree=ast.parse(raw)
        check(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),"no correctness assert in final source "+rel)
    if MODE=="dispatcher_optimized":test("optimized_dispatcher_and_capture_early_refusal",optimized_early_refusal)
    elif MODE in ("normal","optimized"):
        c=module_from_source("independent_common",c_rel)
        prior=sys.modules.get("ops_common206");sys.modules["ops_common206"]=c
        try:
            publisher=module_from_source("independent_publisher",c.OWN+"/publisher206.py")
            tracker=module_from_source("independent_tracker",c.OWN+"/tracker206.py")
        finally:
            if prior is None:sys.modules.pop("ops_common206",None)
            else:sys.modules["ops_common206"]=prior
        lifecycle=reference_module()
        test("strict_emitted_producer_shape_and_context7",producer_and_context)
        test("unchanged_external_authority_and_composite_proof_chain",proof_chain_tests)
        test("authenticated_single_buffer_and_narrow_addendum",pinned_buffer_and_addendum)
        test("actual_downstream_consumer_and_synthetic_unknown_state_controls",downstream_and_mutations)
        if MODE=="normal":
            test("dispatcher_source_auth_routing_cleanup_and_paths",dispatcher_tests)
            test("capture_single_child_and_unknown_outcome",capture_tests)
    else:raise RuntimeError("invalid mode")
    print(json.dumps({"schema":"pr206-independent-owned-offline-contract-audit-v1","synthetic_only":True,"status":"PASS","mode":MODE,"optimization":sys.flags.optimize,"checks":CHECKS,"tests":TESTS,"actual_service_or_API_or_Git_calls":0,"actual_authority_records_read_or_executed":0,"source_manifest":pin((OWN/"FINAL_SOURCE_PINS.json").read_bytes()),"reference_source":{"bytes":77413,"sha256":"b1de89de16876c02d8d18d76ef85eff2b3cb4654f699871c90df302d59302367"}},sort_keys=True))

c_rel="publication_operations_preparation_02/ops_common206.py"
DISPATCHER_REL="root_publication_ops_runner_01/run_operations206_v5.py"
CAPTURE_REL="root_operations_execution_capture_02/capture206.py"
if __name__=="__main__":main()
