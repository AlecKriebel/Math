from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");I=T/"intake";M=T/"root-receipts";W=T/"root_priority_replays";W.mkdir(exist_ok=True);assert not(M/"ROOT_PRIORITY_FAMILY_REPLAYS.json").exists()
pythons=["/opt/homebrew/bin/python3","/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]
families=[
("priority_direct_history","8cbc07becc1d551a0d1abd298bf1bc7112092626a3ece8324ee58d98b86c42e7","c47727f6a498b5784e31a9a31ae24a50e3c946e5c8d0752606c34dfb3c8d643b","scratch_priority_direct_history",18),
("priority_structural","8999e2b03e1d0271bc2e4e28fa053c127588c3de31d0a91bfccf4f6a1ce88f31","78aa687589626f412a58431a2fc4aa9a5f1134d303b10a4427344835e0433ed3","scratch_priority_structural",16)]
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","families":[],"mathematical_or_priority_completeness_claim":False}
for family,mf,cp,body,count in families:
 p=T/family
 assert hashlib.sha256((p/"MANIFEST.json").read_bytes()).hexdigest()==mf
 assert hashlib.sha256((p/"verify_priority.py").read_bytes()).hexdigest()==cp
 rows=json.loads((p/"MANIFEST.json").read_text())["files"]
 assert len(rows)+1==count
 for r in rows:
  f=p/r["path"];assert f.is_file()and not f.is_symlink()
  assert len(f.read_bytes())==r["bytes"]and hashlib.sha256(f.read_bytes()).hexdigest()==r["sha256"]
 args=(["--packet-root",str(p),"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp,"--intake-root",str(I)]if family.endswith("history")else["--packet-root",str(p),"--input-root",str(I),"--manifest-sha256",mf,"--checker-sha256",cp])
 a={"family":family,"manifest_sha256":mf,"checker_sha256":cp,"authored_files_including_manifest":count,"root_modes":[]}
 for py in pythons:
  for opt in[False,True]:
   cmd=[py,"-I","-B"]+(["-O"]if opt else[])+[str(p/"verify_priority.py")]+args+["--primary-root",str(T/body)]
   r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);assert r.returncode==0,(cmd,r.stderr);receipt=json.loads(r.stdout);assert receipt.get("result",receipt.get("status"))=="PASS"
   a["root_modes"].append({"interpreter":py,"optimized":opt,"result":receipt})
 control="run_controls.py"if family.endswith("history")else"control_runner.py"
 outfile=M/("ROOT_"+family.upper()+"_CONTROLS.json")
 ca=[str(p/control)]+args+["--primary-root",str(T/body),"--scratch",str(W/(family+"_controls")),("--output"if family.endswith("history")else"--out"),str(outfile)]
 if not outfile.exists():
  r=subprocess.run([pythons[0],"-I","-B"]+ca,capture_output=True,text=True,timeout=240)
  assert r.returncode==0,(r.stdout,r.stderr)
 c=json.loads(outfile.read_text());assert c.get("result",c.get("status"))=="PASS"
 a["control_result"]=c
 a["sealed_control_receipt_byte_identical"]=outfile.read_bytes()==(p/"CONTROL_RESULTS.json").read_bytes()
 sealed=json.loads((p/"CONTROL_RESULTS.json").read_text())
 def summary(d):
  rows=d.get("results",d.get("cases",[]));return[(x.get("name",x.get("case")),x.get("pass"))for x in rows]
 assert summary(c)==summary(sealed) and all(x[1]for x in summary(c))
 a["sealed_control_outcomes_semantically_identical"]=True
 a["historical_preseal_control_receipt_difference"]=not a["sealed_control_receipt_byte_identical"]
 out["families"].append(a)
(M/"ROOT_PRIORITY_FAMILY_REPLAYS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","families":2,"root_modes":8,"controls":[{"family":a["family"],"receipt":a["control_result"].get("summary",a["control_result"].get("positive_cases"))}for a in out["families"]]}))
