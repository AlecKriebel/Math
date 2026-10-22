from pathlib import Path,PurePosixPath
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys,urllib.parse,urllib.request
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr788_30001522/tmp";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,head_oid
from remote_scoped_commit import tree_oid,oid
head=head_oid();remote=Remote(head);prefix=T.relative_to(R).as_posix();root=remote.entry(prefix);assert root["type"]=="tree"
r=subprocess.run(["gh","api","repos/AlecKriebel/Math/git/trees/"+root["sha"]+"?recursive=1"],capture_output=True,text=True)
assert r.returncode==0,r.stderr
data=json.loads(r.stdout);assert not data.get("truncated")
entries={x["path"]:{k:x[k]for k in["mode","type","sha"]}for x in data["tree"]};assert len(entries)==len(data["tree"])
trees={"":root["sha"]};trees.update({n:r["sha"]for n,r in entries.items()if r["type"]=="tree"})
for parent,pin in trees.items():
 children={PurePosixPath(n).name:r for n,r in entries.items()if PurePosixPath(n).parent.as_posix()==(parent or".")}
 assert tree_oid(children)==pin,(parent,"Merkle identity")
files={n:r for n,r in entries.items()if r["type"]=="blob"}
assert all(r["mode"]=="100644"for r in files.values())
def get(item):
 name,row=item;parts=PurePosixPath(name).parts
 assert not name.startswith("/")and all(x not in["","..","."]for x in parts)
 url="https://raw.githubusercontent.com/AlecKriebel/Math/"+head+"/"+urllib.parse.quote(prefix+"/"+name,safe="/")
 with urllib.request.urlopen(url,timeout=60)as response:raw=response.read()
 assert oid("blob",raw)==row["sha"],name
 path=T/name
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():assert path.is_file()and not path.is_symlink()and path.read_bytes()==raw,("local conflict",name)
 else:path.write_bytes(raw)
 return {"path":name,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"git_blob":row["sha"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:rows=list(pool.map(get,sorted(files.items())))
recovery=T/"session-recovery";recovery.mkdir(exist_ok=True)
for name in ["STATE.json","RESEARCH_LOG.md","RESULTS.md","checkpoint_receipts.jsonl","audits/pr788_30001522/RESEARCH_LOG.md"]:
 raw=remote.read(D.name+"/"+name)
 dest=recovery/("program-"+name.replace("/","__"));dest.write_text(raw)
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","remote_main":head,"remote_T_tree":root["sha"],"restored_files":rows,"restored_count":len(rows),"location_device_now":T.stat().st_dev,"location_now_regular_APFS_not_old_RAM":True,"free_bytes":os.statvfs(T).f_bavail*os.statvfs(T).f_frsize,"unfinished_whole_round01":"Old child handle absent; no terminal sealed report in authoritative Git tree. Not counted as completed. Must restart new reviewer.","private_state_recovered_or_published":False}
(recovery/"RECOVERY_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","head":head,"restored_files":len(rows),"restored_bytes":sum(x["bytes"]for x in rows),"source_manifest_sha256":hashlib.sha256((T/"preprint/source/MANIFEST.json").read_bytes()).hexdigest(),"disk_free":receipt["free_bytes"]}))
