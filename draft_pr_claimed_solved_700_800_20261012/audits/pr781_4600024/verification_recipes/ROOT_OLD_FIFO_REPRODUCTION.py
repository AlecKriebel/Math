from pathlib import Path
import subprocess,tempfile,shutil,os,json,datetime,hashlib
a=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr781_4600024");old=a/"tmp/preprint-revisions/review01_input";ram=a/"tmp/root-receipts"
pin="c893760f12971fd4a36e695996304885bb5a927d7fd8cb68cd99fea78808f66e"
if hashlib.sha256((old/"source/MANIFEST.json").read_bytes()).hexdigest()!=pin:raise RuntimeError("old input changed")
rows=[]
for opt in [False,True]:
 for target_name in ["MANIFEST.json","external.pdf"]:
  with tempfile.TemporaryDirectory(prefix="old-fifo-repro-",dir=a/"tmp") as d:
   work=Path(d);source=work/"source";shutil.copytree(old/"source",source)
   target=source/target_name if target_name=="MANIFEST.json" else work/target_name
   if target.exists():target.unlink()
   os.mkfifo(target)
   pdf=target if target_name=="external.pdf" else old/"output/pdf/paper.pdf"
   cmd=["/opt/homebrew/bin/python3"]+(["-O"] if opt else [])+["-B",str(source/"verify_bundle.py"),"--expected-manifest-sha256",pin,"--pdf",str(pdf)]
   try:
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=2)
    raise RuntimeError("Expected old FIFO hang did not reproduce:"+r.stdout+r.stderr)
   except subprocess.TimeoutExpired:
    rows.append({"target":target_name,"optimized":opt,"outcome":"TIMEOUT_AFTER2SECONDS_CHILD_KILLED_AND_REAPED","command":cmd})
rec={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"CONFIRMED_OLD_MANIFEST_AND_PDF_FIFO_HANG","source_manifest_sha256":pin,"cases":rows,"input_modified":False,"disposable_copy_only":True,"root_repair_candidate_rejections":"36normal/O nonregular cases reject promptly"}
(ram/"ROOT_OLD_FIFO_REPRODUCTION.json").write_text(json.dumps(rec,indent=2)+"\n");print(json.dumps({"result":rec["result"],"cases":len(rows)}))
