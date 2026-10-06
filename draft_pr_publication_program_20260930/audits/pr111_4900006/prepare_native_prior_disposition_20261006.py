"""Source-bound native correction, only after fresh disposition/actual closure."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, os, sqlite3, subprocess, sys, textwrap

A = Path(__file__).resolve().parent
C = A.parents[2]
R = Path("/Users/alec/Documents/Math")
K = "4900006"
GIT = "/opt/homebrew/Cellar/git/2.38.2/bin/git"
PY = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
D = A / "native_prior_disposition_20261006"
B = D / "private_backend"
records = []
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value, reason):
    if not value: raise RuntimeError(reason)
def load(p): return json.loads(p.read_text())
def dump(p, obj): p.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
def digest(body): return hashlib.sha256(body).hexdigest()
def sha(path): return digest(path.read_bytes())
def run(argv, cwd=C):
    start = now()
    child = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    records.append({"argv": argv, "cwd": str(cwd), "PID": child.pid, "UTC_start": start,
        "UTC_end": now(), "exit_code": child.returncode, "stdout_bytes": len(out),
        "stdout_sha256": digest(out), "stderr_bytes": len(err), "stderr_sha256": digest(err)})
    dump(D / "PROCESS_JOURNAL.json", {"actual_operator_PID": os.getpid(), "records": records})
    require(child.returncode == 0, err.decode("utf-8", "replace")[:1200])
    return out
def git(*args): return run([GIT, *args])

require(not D.exists(), "Existing native run: inspect actual state before retry")
ready = load(A / "ROOT_DISPOSITION_READY_20261006.json")
closed = load(A / "actual_closure_20261006/RECEIPT.json")
require(ready["fresh_disposition_review_PASS"] and ready["native_status_correction_supported"], "Disposition gate")
require(closed["same_head_closed_without_merge"] and closed["original_head"] == ready["original_head"], "Actual closure")
D.mkdir()
B.mkdir()
(D / ".gitignore").write_text("private_backend/\n")
require(git("branch", "--show-current").strip() == b"main", "Not main")
base = git("rev-parse", "HEAD").decode().strip()
require(base == sys.argv[1], "Main advanced; reconcile first")
require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == base, "Remote advanced")
require(not git("diff", "--cached", "--name-only"), "Index contains foreign work")
prefix = "unsolved_math_prioritization/"
N = C / prefix / "attempts" / K
require(not N.exists() and not git("ls-tree", "-r", "--name-only", base, "--", str(N.relative_to(C))), "Existing native attempt")
names = ["queue.py", "manifest.json", "policy.json", "catalog.json", "assessments.json", "state.json",
    "history.jsonl", "assessment_history.jsonl", "ranking.csv", "summary.json", "SHORTLIST.md", "QUEUE.md"]
before = {}
for name in names:
    data = git("show", base + ":" + prefix + name)
    before[name] = data
    materialized = C / prefix / name
    require(not materialized.is_symlink() and (not materialized.exists() or materialized.read_bytes() == data), "Unknown native worktree edit " + name)
    (B / name).write_bytes(data)
(B / "cache").mkdir()
cache = B / "cache/catalog.sqlite"
run(["/bin/cp", "-c", str(R / prefix / "cache/catalog.sqlite"), str(cache)])
manifest = load(B / "manifest.json")
db = sqlite3.connect("file:" + str(cache) + "?mode=ro", uri=True)
require(db.execute("SELECT revision FROM metadata").fetchone() == (manifest["revision"],), "Cache revision")
require(db.execute("SELECT count(*) FROM records").fetchone()[0] == manifest["records"], "Cache count")
raw, report = db.execute("SELECT payload,report FROM records WHERE key=?", (K,)).fetchone()
db.close()
source, prior = json.loads(raw), json.loads(report)
O = A / "original_head_authentication_20261006/original_attempt"
require(source == load(O / "source_record.json") and prior == load(O / "prior_imported_report.json"), "Complete source pair mismatch")
review_hash = digest(json.dumps([source, prior], sort_keys=True).encode())
oldrows = json.loads(before["catalog.json"])
catalog = {row["id"]: row for row in oldrows}
row = catalog[K]
require(review_hash == row["review_hash"] == "50f6cc93288c790920827f4dadde3d9f72b5e5189ba0f5f59b578f0434fe450d", "Source binding")
require(sha(O / "COUNTEREXAMPLE.md") == "a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266", "Original theorem changed")
original_auth = load(A / "original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json")
require(original_auth["original_effort"] == "2/5" and original_auth["literal_original_status"] == "claimed_solved", "Original effort provenance")
states = json.loads(before["state.json"])
require(K not in states, "Existing native state requires reconciliation")
evidence = {"review_hash": review_hash, "exact_claim": source["statement"],
    "classification_scope": "Overbroad imported manifold-inclusive target has an elementary classical negative specialization; not previously published priority for the full strengthened R5 theorem.",
    "original_head": ready["original_head"], "original_effort_imported": 2, "original_budget": "2/5",
    "effort_provenance": str((A / "original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json").relative_to(C)),
    "original_proof_sha256": sha(O / "COUNTEREXAMPLE.md"), "original_archive": str(O.relative_to(C)),
    "stronger_R5_mathematical_gate": str((A / "ROOT_MATHEMATICAL_GATE_20261006.json").relative_to(C)),
    "priority_reasoning": str((A / "ROOT_PRIORITY_DISPOSITION_20261006.md").relative_to(C)),
    "fresh_review": ready["fresh_disposition_review"], "closed_PR_comment": closed["closing_comment_url"],
    "full_stronger_theorem_exact_prior_authenticated": False, "full_stronger_theorem_novelty_established": False,
    "historical_thesis_scope_authenticated": False, "new_central_proof_search_turns": 0,
    "no_fabricated_proof_turns_or_readiness": True}
dump(B / "evidence.json", evidence)
imported = {"at": now(), "id": K, "status": "already_solved", "turns_used": 2,
    "review_hash": review_hash, "statement_hash": row["statement_hash"], "evidence": evidence,
    "note": "Imported authenticated original submitted effort2/5 from immutable QUEUE; no new proof turn or synthetic readiness/candidate ledger.",
    "original_effort_import": evidence}
states[K] = imported
dump(B / "state.json", states)
with (B / "history.jsonl").open("a") as handle:
    handle.write(json.dumps({**imported, "event": "import_authenticated_submitted_author_effort"}, ensure_ascii=False) + "\n")
oldass = json.loads(before["assessments.json"])
old = oldass[K]
note = "Literal unrestricted manifold-inclusive target already has an elementary classical torus-product obstruction. Stronger entire-R5 theorem203/50 mathematically verified; no exact earlier full theorem authenticated, stronger novelty unresolved. Historical narrower conjectures not resolved. PR111 closed without merge or solved-problem publication. Original2/5 imported; new proof turns0."
assessment = {**old, "p_solve": 0, "p_valid_open": 0, "resolution": "already_solved", "route": "proof",
    "decision": "exclude", "review_policy": "2.0-five-turn-proof", "review_type": "fresh full-source mathematical and priority disposition",
    "review_hash": review_hash, "note": note,
    "rationale": "Three independent math/source families, three independent priority families and fresh cross-family/disposition checks verify the stronger explicit construction while withholding original-open-problem publication clearance. A contracting coordinate times irrational torus rotations already defeats the broad imported assertion, including its modern manifold phase and explicit ambient-extension convention. This classification concerns that broad target only; it does not claim a duplicate published entire-R5 theorem.",
    "remaining_gap": "No mathematical gap in the verified entire-R5 example or classical literal-scope obstruction. Stronger theorem's substantive novelty, original thesis quantifiers and material historical source bodies remain unestablished; Lorenz/chaotic/generic/transitive variants are untouched.",
    "first_experiment": "Do not allocate further proof turns to this overbroad imported target. Preserve exact theorem and verification. Any independently framed research note or narrower new target needs its own scope/priority decision; no solved-problem paper or DOI follows from this disposition.",
    "sources": ["https://arxiv.org/pdf/2510.14870v2", "https://sergey-zelik.co.uk/publications/dlyap.pdf",
        "https://doi.org/10.3934/cpaa.2008.7.971", "https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf"],
    "original_budget": "2/5", "new_central_proof_search_turns": 0, "evidence": evidence}
dump(B / "assessment.json", assessment)
run([PY, "-E", "-S", "-B", "-P", str(B / "queue.py"), "assess", K, "--file", str(B / "assessment.json")], B)
run([PY, "-E", "-S", "-B", "-P", str(B / "queue.py"), "status", K, "already_solved", "--note", note, "--evidence", str(B / "evidence.json")], B)
afterass, afterstate = load(B / "assessments.json"), load(B / "state.json")
aftercatalog = {x["id"]: x for x in load(B / "catalog.json")}
require({k:v for k,v in afterass.items() if k != K} == {k:v for k,v in oldass.items() if k != K}, "Unrelated assessment changed")
require({k:v for k,v in afterstate.items() if k != K} == json.loads(before["state.json"]), "Unrelated state changed")
require(afterstate[K]["turns_used"] == 2 and afterstate[K]["status"] == "already_solved", "Status/effort")
require(aftercatalog[K]["local_status"] == "already_solved" and not aftercatalog[K]["eligible"] and aftercatalog[K]["turns_used"] == 2, "Catalog target")
require(set(catalog) == set(aftercatalog), "Catalog identities")
for name in ["history.jsonl", "assessment_history.jsonl"]:
    require((B / name).read_bytes().startswith(before[name]), "Historical prefix modified")
events = [json.loads(s) for s in (B / "history.jsonl").read_bytes()[len(before["history.jsonl"]):].decode().splitlines()]
ae = [json.loads(s) for s in (B / "assessment_history.jsonl").read_bytes()[len(before["assessment_history.jsonl"]):].decode().splitlines()]
require(len(events) == 2 and len(ae) == 1 and all(x["id"] == K for x in events + ae), "Event scope")
require(events[0]["event"] == "import_authenticated_submitted_author_effort" and all(x["turns_used"] == 2 for x in events), "Original-effort import")
drift = []
for key, oldrow in catalog.items():
    if key == K: continue
    diff = {f: {"before": oldrow.get(f), "after": aftercatalog[key].get(f)} for f in set(oldrow) | set(aftercatalog[key]) if f != "rank" and oldrow.get(f) != aftercatalog[key].get(f)}
    if diff:
        require(set(diff) <= {"local_status", "eligible", "turns_used"}, "Unexplained unrelated drift " + key)
        st = afterstate.get(key, {})
        require(aftercatalog[key]["local_status"] == st["status"] and aftercatalog[key]["turns_used"] == st.get("turns_used", 0), "Unexplained state projection")
        drift.append({"id": key, "difference": diff, "baseline_preserved": True})
dump(D / "UNRELATED_BASELINE_PROJECTION_DRIFT.json", {"base_commit": base, "differences": drift, "other_targets_not_reassessed": True})
rows = [dict(aftercatalog[K]) if x["id"] == K else dict(x) for x in oldrows]
rows.sort(key=lambda x: (not x["eligible"], -x["ev"], x["id"]))
for i, x in enumerate([x for x in rows if x["eligible"]], 1): x["rank"] = i
for x in rows:
    if not x["eligible"]: x["rank"] = None
code = (B / "queue.py").read_text()
render = textwrap.dedent(code[code.index("    write(ROOT/'catalog.json',rows)"):code.index("def seen_ids")])
spec = importlib.util.spec_from_file_location("pr111_native_queue_writer", B / "queue.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
namespace = dict(module.__dict__)
namespace.update(rows=rows, cfg=load(B / "policy.json"), reviews=afterass, state=afterstate)
exec(compile(render, str(B / "queue.py") + ":pinned-native-render", "exec"), namespace)
for x in load(B / "catalog.json"):
    if x["id"] != K:
        require({f:v for f,v in x.items() if f != "rank"} == {f:v for f,v in catalog[x["id"]].items() if f != "rank"}, "Unrelated semantic row changed")
dump(D / "SCOPED_RENDER_RECEIPT.json", {"UTC": now(), "queue_py_sha256": sha(B / "queue.py"),
    "native_render_code_sha256": digest(render.encode()), "unrelated_catalog_rows_preserved_except_rank": True,
    "baseline_drift_preserved": len(drift)})
lines = before["QUEUE.md"].decode().splitlines()
positions = [i for i,s in enumerate(lines) if "| 4900006 / AMR-048-0006 |" in s]
require(len(positions) == 1, "Unique campaign row")
i = positions[0]
cells = lines[i].split("|")
require(cells[8].strip() == "queued" and cells[9].strip() == "0/5", "Campaign baseline changed")
cells[4], cells[8], cells[9] = " 0.0000 ", " already_solved ", " 2/5 "
cells[11] = " 2026-10-06: Broad manifold-inclusive target has classical irrational-torus obstruction; stronger entire-R5 theorem203/50 verified, exact prior and substantive novelty unresolved. Narrower historical conjectures untouched. PR111 closed without merge/new paper; original2/5 imported, audit0; no DOI/tracker. "
lines[i] = "|".join(cells)
require([s for j,s in enumerate(lines) if j != i] == [s for j,s in enumerate(before["QUEUE.md"].decode().splitlines()) if j != i], "Unrelated campaign rows changed")
(B / "QUEUE.md").write_text("\n".join(lines) + "\n")
N.mkdir(parents=True)
dump(N / "assessment.json", assessment)
dump(N / "HISTORICAL_DESK_ASSESSMENT.json", old)
dump(N / "PRIORITY_EVIDENCE.json", evidence)
(N / "README.md").write_text("# 4900006: source-scope disposition\n\nStatus already_solved applies only to the overbroad imported manifold-inclusive target's elementary classical obstruction. The complete analytic entire-R5 example, strict203/50 dominance over its actual equilibrium/periodic competitors, and separately checked dimension conventions remain mathematically verified. No exact previous full theorem was authenticated; substantive novelty remains unestablished. The historical Lorenz/chaotic/generic/transitive variants are not resolved.\n\nPR111 closed without merge or solved-problem publication: " + closed["closing_comment_url"] + "\n\nImmutable original proof/effort2/5 and effective v2 diagnostics are preserved in ../../../draft_pr_publication_program_20260930/audits/pr111_4900006/. No synthetic readiness/candidate ledger, new central proof turn, paper, DOI, or tracker row. Extensive AI-assisted verification; no conventional human peer review claimed.\n")
(N / "RESEARCH_LOG.md").write_text("# Source-scope disposition log\n\n" + now() + ": Math/source100%; bounded priority audit100%, publication novelty clearance false; workflow95% pending committed/remote correction readback. Original2/5 imported, new proof turns0. Broader target classical; stronger theorem valid with novelty unresolved. Same-head PR closure verified. Program18/99=18.18%; goal active.\n")
export = ["assessments.json", "state.json", "history.jsonl", "assessment_history.jsonl", "catalog.json", "ranking.csv", "summary.json", "SHORTLIST.md", "QUEUE.md"]
for name in export:
    out = C / prefix / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes((B / name).read_bytes())
record = {"schema": "pr111-native-source-scope-correction/v1", "UTC": now(), "actual_operator_PID": os.getpid(),
    "base_commit": base, "PR":111, "status":"already_solved", "original_budget":"2/5", "new_central_proof_search_turns":0,
    "original_effort_import_not_new_proof_event":True, "scope": evidence["classification_scope"],
    "source_review_hash":review_hash, "full_source_and_prior_authenticated":True, "historical_desk_assessment_preserved":True,
    "unrelated_assessments_states_and_campaign_rows_preserved":True, "other_catalog_rows_only_rank_may_change":True,
    "baseline_projection_drift_preserved":len(drift), "native_commands":["assess","status"],
    "source_inputs":[{"path":prefix+name,"bytes":len(body),"sha256":digest(body),"Git_commit":base} for name,body in before.items()],
    "cache_snapshot_sha256":sha(cache), "cache_revision":manifest["revision"], "cache_records":manifest["records"],
    "closing_comment_url":closed["closing_comment_url"], "same_head_closed_without_merge":True,
    "publication":False, "DOI":None, "tracker":False, "main_checkpoint_pending":True, "primary_checkout_mutated":False}
dump(N / "DISPOSITION.json", record)
paths = [C / prefix / name for name in export] + [path for path in N.iterdir() if path.is_file()]
record["native_pins"] = [{"path":str(path.relative_to(C)),"bytes":path.stat().st_size,"sha256":sha(path)} for path in paths]
dump(D / "PREPARED_RECEIPT.json", record)
print(json.dumps({k:v for k,v in record.items() if k not in {"source_inputs","native_pins"}},sort_keys=True))
