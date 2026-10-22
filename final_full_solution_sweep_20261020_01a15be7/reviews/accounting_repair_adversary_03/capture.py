from pathlib import Path
import collections, datetime as dt, difflib, hashlib, json, os, shutil, sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE="1", GIT_OPTIONAL_LOCKS="0")
R=Path(__file__).resolve().parent
B=R.parent.parent
P=B/"reviews/accounting_repair_adversary_02"
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def put(p,d):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(d if isinstance(d,bytes) else (json.dumps(d,indent=2)+"\n").encode())
entries=[]
def capture(src,dst,data=None):
 if src.is_symlink() or not src.is_file(): raise RuntimeError("Nonregular source "+str(src))
 start=now(); b=src.read_bytes() if data is None else data
 put(dst,b)
 entries.append(dict(source=str(src),captured_path=str(dst),read_started_at=start,captured_at=now(),bytes=len(b),sha256=sha(b)))
put("RESEARCH_LOG.json",[dict(at=now(),completion_estimate_percent=5,event="Independent bounded second-repair review started; all writes restricted to this new review directory; no providers, Git mutations or external communication.")])
seals=[]
for prior in [B/"reviews/completed_publications_accounting_adversary",P]:
 manifest=json.loads((prior/"OUTPUT_MANIFEST.json").read_text());bad=[]
 for e in manifest["files"]:
  b=(prior/e["path"]).read_bytes()
  if len(b)!=e["bytes"] or sha(b)!=e["sha256"]:bad.append(e["path"])
 seals.append(dict(review=prior.name,at=now(),files=len(manifest["files"]),mismatches=bad,manifest_sha256=sha((prior/"OUTPUT_MANIFEST.json").read_bytes())))
 if bad: raise RuntimeError("Prior output seal mismatch")
put("PRIOR_SEAL_VALIDATION.json",seals)
for src in sorted((P/"inputs").rglob("*")):
 if src.is_file():capture(src,Path("inputs/prior02")/src.relative_to(P/"inputs"))
for name in ["REPORT.md","controls.py","supplementary.py","CONTROL_RESULTS.json","CONTROL_SUMMARY.json","SUPPLEMENTARY_RESULTS.json","INPUT_MANIFEST.json","OUTPUT_MANIFEST.json","INDEPENDENT_ACCOUNTING.json","SOURCE_DIFF.patch"]:
 capture(P/name,Path("inputs/prior02_review")/name)
# Capture the three changing top-level inputs as a coherent numerical-prefix baseline.
attempts=[]
for attempt in range(30):
 start=now(); a={n:(B/n).read_bytes() for n in ["STATE.json","dispositions.jsonl","rest_inventory.json"]}
 s=json.loads(a["STATE.json"]); j=[json.loads(x) for x in a["dispositions.jsonl"].splitlines() if x.strip()]
 stable=all((B/n).read_bytes()==b for n,b in a.items())
 coherent=[e["pr"] for e in j]==list(range(s["start_pr"],s["next_pr"])) and s["last_completely_processed_pr"]==s["next_pr"]-1 and s["completed_pr_count"]==len(j)
 attempts.append(dict(at=start,attempt=attempt,stable_individual_rereads=stable,coherent_prefix=coherent,next_pr=s["next_pr"],journal_count=len(j)))
 if stable and coherent:break
else:raise RuntimeError("Could not capture coherent changing inputs")
for n,b in a.items():capture(B/n,Path("inputs/current")/n,b)
for name in ["coverage_snapshot.py","ACCOUNTING_REPAIR02_ROOT_REPLAY.json","ROOT_ACCOUNTING_REVIEW02_ACCEPTANCE.json"]:capture(B/name,Path("inputs/current")/name)
for src in sorted((B/"accounting_history").rglob("*")):
 if src.is_file():capture(src,Path("inputs/current/accounting_history")/src.relative_to(B/"accounting_history"))
for e in j:capture(B/f"PR{e['pr']:04d}_DISPOSITION.json",Path("inputs/current")/f"PR{e['pr']:04d}_DISPOSITION.json")
for e in s["reopened_disposition_overrides"]:capture(B/e["replacement_disposition"],Path("inputs/current")/e["replacement_disposition"])
for e in s["completed_publications"]:
 name=e["verification"];capture(B/name,Path("inputs/current")/name)
 proof=json.loads((R/"inputs/current"/name).read_text())
 for rel in proof["evidence"].values():
  p=Path(rel)
  if not p.is_absolute() and (B/p).is_file():capture(B/p,Path("inputs/current")/p)
# Verify every saved journal entry and mutable top-level input during this capture.
saved=[json.loads((R/"inputs/current"/f"PR{e['pr']:04d}_DISPOSITION.json").read_text())==e for e in j]
if not all(saved):raise RuntimeError("Per-PR capture incoherent")
put("CAPTURE_COHERENCE.json",dict(at=now(),attempts=attempts,all_saved_dispositions_equal=all(saved),note="Individual exact byte captures; coherent captured numerical prefix. No assertion of globally atomic provider state or continued canonical-file immutability."))
put("INPUT_MANIFEST.json",dict(at=now(),files=entries,note="Each source read individually. Mutable canonical files may advance after capture. Prior02 inputs copied recursively in full before mounting current code only into separate replay fixtures."))
old=(R/"inputs/current/accounting_history/repair01_20261021T1708/coverage_snapshot.py").read_text().splitlines(True)
new=(R/"inputs/current/coverage_snapshot.py").read_text().splitlines(True)
put("SOURCE_DIFF.patch",''.join(difflib.unified_diff(old,new,fromfile="first_repair",tofile="second_repair")).encode())
replay=R/"replay"
shutil.copytree(R/"inputs/prior02",replay/"inputs")
for n in ["controls.py","supplementary.py"]:shutil.copyfile(R/"inputs/prior02_review"/n,replay/n)
shutil.copyfile(R/"inputs/current/coverage_snapshot.py",replay/"inputs/current/coverage_snapshot.py")
print(json.dumps(dict(captured_files=len(entries),next_pr=s["next_pr"],journal_count=len(j),current_source_sha256=sha((R/"inputs/current/coverage_snapshot.py").read_bytes()),prior_seals=seals),indent=2))
