from pathlib import Path
import subprocess,json,shutil,tempfile,os,datetime
a=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr781_4600024")
p=a/"tmp/preprint-workspace/repair_candidate";original=a/"tmp/preprint-workspace/preprint";pin=json.loads((p/"CANDIDATE_IDENTITY.json").read_text())["source_manifest_sha256"]
(p/"tmp").mkdir(exist_ok=True);results=[]
with tempfile.TemporaryDirectory(prefix="nonregular-guard-",dir=p/"tmp") as temporary:
 work=Path(temporary)
 for opt in [False,True]:
  flags=["/opt/homebrew/bin/python3"]+(["-O"] if opt else [])+["-B"]
  for tool in ["verifier","builder"]:
   for target_name in ["MANIFEST.json","build_package.py","external.pdf"]:
    for kind in ["fifo","directory","symlink"]:
     with tempfile.TemporaryDirectory(prefix="case-",dir=work) as one:
      case=Path(one);source=case/"source";shutil.copytree(p/"source",source)
      target=case/"external.pdf" if target_name=="external.pdf" else source/target_name
      if target.exists():target.unlink()
      if kind=="fifo":os.mkfifo(target)
      elif kind=="directory":target.mkdir()
      else:
       sentinel=case/"sentinel";sentinel.write_bytes(b"owned sentinel");target.symlink_to(sentinel)
      pdf=target if target_name=="external.pdf" else original/"output/pdf/paper.pdf"
      if tool=="verifier":
       cmd=flags+[str(source/"verify_bundle.py"),"--expected-manifest-sha256",pin,"--pdf",str(pdf)]
      else:
       cmd=flags+[str(p/"source/build_package.py"),"--source",str(source),"--expected-manifest-sha256",pin,"--pdf",str(pdf),"--output-dir",str(case/"out")]
      try:r=subprocess.run(cmd,capture_output=True,text=True,timeout=3)
      except subprocess.TimeoutExpired:raise RuntimeError("nonregular input hung:"+str((tool,target_name,kind,opt)))
      if r.returncode==0:raise RuntimeError("nonregular input accepted")
      results.append({"tool":tool,"target":target_name,"kind":kind,"optimized":opt,"result":"REJECTED_WITHIN3SECONDS","returncode":r.returncode})
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_manifest_sha256":pin,"result":"PASS","cases":results,"case_count":len(results),"current_review01_package_unchanged":True,"scope":"Repair-candidate physical FIFO/directory/symlink guards; no publication or change to sealed-review inputs"}
(p/"ROOT_NONREGULAR_GUARD_REPAIR.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","physical_nonregular_cases":len(results),"source_manifest_sha256":pin}))
