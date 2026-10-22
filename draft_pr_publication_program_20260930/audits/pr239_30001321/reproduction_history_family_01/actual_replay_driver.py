from pathlib import Path
import hashlib,json,sys,datetime,os,subprocess,time
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr239_30001321")
B=A/"authenticated_sources_01/current/unsolved_math_prioritization/attempts/30001321"
O=A/"reproduction_history_family_01"
O.mkdir()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def out(name,d):
 p=O/name
 raw=(json.dumps(d,indent=2,sort_keys=True)+"\n").encode()
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 with os.fdopen(fd,"wb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return {"path":str(p),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
checks=[]
manifest_path=A/"authenticated_sources_01/SOURCE_MATERIALIZATION_MANIFEST.json"
raw=manifest_path.read_bytes()
assert len(raw)==65348 and hashlib.sha256(raw).hexdigest()=="4ddb9e5c9dc2487b9fb5fd8f993e562517b5efe2b4af2c2ae87c1a5c61feefa4"
mat=json.loads(raw)
for ent in mat["files"]:
 b=Path(ent["path"]).read_bytes()
 assert len(b)==ent["bytes"] and hashlib.sha256(b).hexdigest()==ent["sha256"]
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==ent["native_blob"]
checks.append({"scope":"complete materialization full body SHA1/SHA256/length","files":len(mat["files"])})
for name,prefix in [("TURN_1_MANIFEST.json",B),("TURN_2_MANIFEST.json",B),("FROZEN_MANIFEST.json",B),("independent_review/REVIEW_MANIFEST.json",B/"independent_review")]:
 d=json.loads((B/name).read_bytes())
 for ent in d["files"]:
  b=(prefix/ent["path"]).read_bytes()
  assert len(b)==ent["bytes"] and hashlib.sha256(b).hexdigest()==ent["sha256"]
 checks.append({"manifest":name,"bound_files":len(d["files"]),"all_pins_match":True})
reviewed=json.loads((B/"independent_review/reviewed_hashes.json").read_bytes())
assert reviewed["author_manifest_sha256"]==hashlib.sha256((B/"FROZEN_MANIFEST.json").read_bytes()).hexdigest()
assert reviewed["author_files"]==json.loads((B/"FROZEN_MANIFEST.json").read_bytes())["files"]
assert json.loads((B/"TURN_2_MANIFEST.json").read_bytes())["earlier_manifest_sha256"]==hashlib.sha256((B/"TURN_1_MANIFEST.json").read_bytes()).hexdigest()
O.joinpath("RESEARCH_LOG.md").write_text("# PR239 reproduction and review-history audit\n\n"+utc()+" — Began after complete reading of the four executable checker sources, PROOF.md, TURN_1.md, TURN_2.md, historical manifests and independent review. Completion estimate: 30%. Scope: finite exact reproduction and historical-package authentication; no novelty or asymptotic conclusion from finite checks. No source edits, network or external effects.\n")
out("AUTHENTICATION_RECEIPT.json",{"UTC":utc(),"status":"PASS","checks":checks,"historical_independence_boundary":"Exact bytes and internally recorded ordering authenticated; distinct reviewer identity, absence of prior influence, and historical PDF access are not independently established by these files."})
runs=[]
for script,receipt in [("check_turn1.py","turn1_receipt.json"),("check_turn2.py","turn2_receipt.json"),("check_turn3.py","turn3_receipt.json"),("independent_review/independent_check.py","independent_review/independent_check.json")]:
 argv=["/opt/homebrew/bin/python3.11","-E","-B"]
 if "turn1" not in script:argv+=["-S","-P"]
 argv+=[str(B/script)]
 start=time.monotonic();r=subprocess.run(argv,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=600)
 got=json.loads(r.stdout)
 assert r.returncode==0 and not r.stderr and r.stdout==(B/receipt).read_bytes()
 run={"script":script,"script_sha256":hashlib.sha256((B/script).read_bytes()).hexdigest(),"argv":argv,"exit_code":r.returncode,"stderr_bytes":len(r.stderr),"elapsed_seconds":round(time.monotonic()-start,6),"actual_stdout_bytes":len(r.stdout),"actual_stdout_sha256":hashlib.sha256(r.stdout).hexdigest(),"byte_identical_to_frozen_receipt":True,"result":got}
 out("ACTUAL_"+Path(script).stem+".json",run);runs.append(run)
out("ALL_FOUR_ACTUAL_REPLAYS.json",{"UTC":utc(),"status":"PASS","exact_assertions_by_script":[r["result"]["exact_assertions"] for r in runs],"scope":"Four actual executed finite checker outputs, each byte identical to its historical frozen receipt. No asymptotic or priority certification."})
print(json.dumps({"status":"PASS","runs":[(r["script"],r["result"]["exact_assertions"]) for r in runs],"output":str(O)}))
