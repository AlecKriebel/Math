#!/usr/bin/env python3
"""Read-only frozen artifact binding and private-copy replay for PR369."""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess,datetime
own=Path(__file__).resolve().parent
review=own.parent
snapshot=review/"snapshot"
prefix=Path("unsolved_math_prioritization/attempts/2302055")
frozen=snapshot/prefix
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","failures":[]}
def verify_entries(manifest, root):
    data=json.loads(manifest.read_text())
    records=[]
    for f in data["files"]:
        raw=(root/f["path"]).read_bytes()
        ok=(len(raw)==f["bytes"] and hashlib.sha256(raw).hexdigest()==f["sha256"])
        records.append({"path":f["path"],"pass":ok})
        if not ok:receipt["failures"].append({"manifest":str(manifest.relative_to(review)),"path":f["path"]})
    return {"manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest(),"entries":len(records),"all_pass":all(f["pass"] for f in records)}
receipt["snapshot"]=verify_entries(review/"snapshot_manifest.json",snapshot)
receipt["historical_manifests"]={}
for name in ["SOURCE_GATE_MANIFEST.json"]+[f"TURN_{i}_MANIFEST.json" for i in range(1,6)]+["FINAL_AUTHOR_MANIFEST.json","PUBLICATION_MANIFEST.json","review/REVIEW_MANIFEST.json"]:
    man=frozen/name
    root=man.parent if name.startswith("review/") else frozen
    receipt["historical_manifests"][name]=verify_entries(man,root)
private=own/"private"/"replay"
if private.exists():shutil.rmtree(private)
shutil.copytree(frozen,private)
receipt["replays"]=[]
targets=[(f"verify_turn{i}.py",f"TURN_{i}_CHECKS.json",[]) for i in range(1,6)]
targets += [("review/independent_check.py","review/INDEPENDENT_CHECKS.json",[]),
            ("review/replay_author.py","review/AUTHOR_REPLAY.json",[str(private)])]
for script,expected,args in targets:
    r=subprocess.run([sys.executable,str(private/script),*args],cwd=private,capture_output=True,timeout=180)
    (private/(script.replace("/","_")+".stdout")).write_bytes(r.stdout)
    (private/(script.replace("/","_")+".stderr")).write_bytes(r.stderr)
    ok=r.returncode==0 and r.stdout==(private/expected).read_bytes()
    entry={"script":script,"exit":r.returncode,"stdout_byte_equal":ok,"stdout_sha256":hashlib.sha256(r.stdout).hexdigest()}
    if r.returncode==0:entry["output"]=json.loads(r.stdout)
    if not ok:receipt["failures"].append(entry)
    receipt["replays"].append(entry)
receipt["author_assertions_total"]=sum(x["output"]["exact_assertions"] for x in receipt["replays"][:5])
receipt["prior_independent_assertions"]=receipt["replays"][5]["output"]["independent_assertions"]
receipt["status"]="PASS" if not receipt["failures"] else "FAIL"
receipt["finite_checks_not_universal_analytic_proofs"]=True
(own/"ARTIFACT_REPRODUCTION.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":receipt["status"],"frozen_files":receipt["snapshot"]["entries"],"historical_manifests":len(receipt["historical_manifests"]),"byte_equal_replays":sum(x["stdout_byte_equal"] for x in receipt["replays"]),"author_assertions":receipt["author_assertions_total"],"prior_independent_assertions":receipt["prior_independent_assertions"]},indent=2))
if receipt["failures"]:sys.exit(1)
