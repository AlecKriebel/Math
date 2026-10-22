from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";W=T/"root_archive_portability_v3";W.mkdir(exist_ok=False)
r=json.loads((P/"PACKAGE_INVENTORY.json").read_text());pin=r["source_manifest_sha256"];dest=W/"relocated source with spaces";dest.mkdir()
with zipfile.ZipFile(P/"source-and-verification.zip")as z:
 names=z.namelist();assert len(names)==len(set(names))==151
 for info in z.infolist():
  name=info.filename;assert name and not name.startswith("/")and"\\"not in name and all(part not in("","..",".")for part in name.split("/"))and not info.is_dir()
  out=dest/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(info));assert out.read_bytes()==(S/name).read_bytes()
rows=[]
for py,opt in[(sys.executable,False),("/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",True)]:
 cmd=[py,"-I","-B"]+(["-O"]if opt else[])+[str(dest/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf")]
 p=subprocess.run(cmd,cwd="/",env=dict(os.environ,TMPDIR=str(W)),capture_output=True,text=True,timeout=120);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr);value=json.loads(p.stdout);assert value["result"]=="PASS"and value["source_files"]==151 and not value["finite_replay_processes"]and value["external_evidence_files_rehashed"]==0;rows.append({"interpreter":py,"optimized":opt,"result":value})
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","source_files":151,"relocated_exact_archive_bytes":True,"normal_and_optimized_interpreters":rows,"external_body_files":0,"finite_replay_in_this_relocation":False,"separate_historical_v1_full_ten_process_replay_receipt":"FIRST_PORTABLE_VERIFICATION.stdout","separate_historical_full_replay_source_manifest_sha256":"6287da0dabdad505f3d312dfeefc9e75f34caaeccb267fada3f9119502cfa6be","current_v3_optional_body_custody_receipt":"V3_OPTIONAL_BODY_CUSTODY.json","current_fresh_whole_review_full_replay_pending":True,"source_manifest_sha256":pin,"limitation":"Core source custody at a relocated path with spaces; historical v1 full processes are separately recorded with the old source pin; the V3 change is bibliography endpoint and optional harness documentation only. Current V3 body custody checks139files, and the new fresh whole reviewer is independently checking current full replay/relocation."}
(M/"ROOT_ARCHIVE_PORTABILITY_V3.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":"PASS","archive_files":151,"relocation_modes":2,"external_bodies":0}))
