from pathlib import Path
import sys,subprocess,json,hashlib
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp")
rows=[]
for name,pin,vpin in [("math_definition_crosscheck","310d9a87bb320f079b345f3a977612b697a6c07c02ebf51be3a0da821128fb3d","a46e0245e3611758719c17ca754bade7713bb0de72f8d0c627f8719aaabb8c97"),("math_group_crosscheck","767aaa58b6951a3a8320213127e5ec17e4b8c6033c814d58f1d4c784aeeeb529","061ba4f0d1918aeca18cd98e565581b6bd03b0e9afe3ba0c7670ffcdbf698ca7")]:
 b=T/name
 if hashlib.sha256((b/"MANIFEST.json").read_bytes()).hexdigest()!=pin or hashlib.sha256((b/"CHECK.py").read_bytes()).hexdigest()!=vpin:raise RuntimeError("Crosscheck outside pin")
 for py in [sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
  for opt in [False,True]:
   r=subprocess.run([py,"-I","-B",*(["-O"]if opt else[]),str(b/"CHECK.py"),*(["--manifest-sha256",pin]if name=="math_group_crosscheck"else[])],cwd="/",capture_output=True,text=True,timeout=120)
   if r.returncode or r.stderr:raise RuntimeError(r.stderr)
   got=json.loads(r.stdout)
   if got["status"]!="PASS":raise RuntimeError("Replay notpass")
   rows.append({"folder":name,"python":py,"optimized":opt,"status":"PASS"})
(T/"root-receipts/ROOT_MATH_CROSSCHECK_REPLAY.json").write_text(json.dumps({"status":"PASS","modes":rows,"interpretation":"Independent adversarial arguments checked in written crosschecks; byte/algebra replay is not a formal topology proof"},indent=2)+"\n")
p=T/"root-receipts/ROOT_PRIORITY_ADDITIONAL_DOWNLOADS.json";d=json.loads(p.read_text())
for r in d["sources"]:
 if r["name"]=="Hanke_Szymik2026":
  r["name"]="Hausmann2026";r["title"]="Group Actions and Chromatic Homotopy Theory";r["author"]="Markus Hausmann";r["temporary_download_label_corrected_after_primary_body_inspection"]=True
  for ext in ["html","txt"]:
   a=T/"root_priority_scratch"/("Hanke_Szymik2026."+ext);z=T/"root_priority_scratch"/("Hausmann2026."+ext)
   if a.exists()and not z.exists():a.rename(z)
p.write_text(json.dumps(d,indent=2)+"\n")
print("PASS:8 crosscheck modes; primary source author label authenticated/corrected")
