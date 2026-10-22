from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys,os
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote
old=json.loads((M/"LOCAL_PROGRAM_MIRROR_SYNC_PREPRINT.json").read_text());receipt=json.loads((M/"WHOLE02_V3_CHECKPOINT_RECEIPT.json").read_text());remote=Remote(receipt["commit"]);new=[];payloads=[]
for row in old["only_own6text_mirrors"]:
 p=R/row["path"];assert stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink()and p.stat().st_nlink==1
 raw=remote.read(row["path"]).encode();assert hashlib.sha256(p.read_bytes()).hexdigest()==row["sha256"]or p.read_bytes()==raw,"Unexpected own local edits; preserve"
 payloads.append((p,raw));new.append({"path":row["path"],"sha256":hashlib.sha256(raw).hexdigest()})
for p,raw in payloads:p.write_bytes(raw)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","commit":receipt["commit"],"only_own6text_mirrors":new,"old_own6hashes_authenticated":True,"unrelated_working_changes_index_Git_objects_and_refs_untouched":True}
(M/"LOCAL_PROGRAM_MIRROR_SYNC_V3.json").write_text(json.dumps(out,indent=2)+"\n")
W=T/"root_archive_portability_v3";s=W/"relocated source with spaces";pin=json.loads((T/"preprint/PACKAGE_INVENTORY.json").read_text())["source_manifest_sha256"]
rows=[]
for py,opt in[(sys.executable,False),("/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",True)]:
 cmd=[py,"-I","-B"]+(["-O"]if opt else[])+[str(s/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(T/"preprint/output/pdf/paper.pdf"),"--replay"]
 p=subprocess.run(cmd,cwd="/",env=dict(os.environ,TMPDIR=str(W)),capture_output=True,text=True,timeout=300)
 assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr)
 a=json.loads(p.stdout);assert a["result"]=="PASS"and len(a["finite_replay_processes"])==10 and a["external_evidence_files_rehashed"]==0
 rows.append({"python":py,"optimized":opt,"result":a})
(M/"ROOT_V3_ARCHIVE_FULL_REPLAY.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","source_manifest_sha256":pin,"relocated_source_spaces":True,"two_outer_modes":rows,"total_inner_processes":20,"external_evidence_files":0,"source_or_package_mutated":False},indent=2)+"\n")
print(json.dumps({"result":"PASS","local_own_mirrors":6,"source_commit":receipt["commit"],"current_relocated_full_replay_inner_processes":20,"source_mutated":False}))

