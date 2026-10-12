"""Read-only GitHub source authentication; all writes restricted to this packet."""
import base64,datetime,hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
head="98cc2821e9376507caf2d2c57414f7c7e7719c1b";base="c6975ca76f9f667f1250ba403d0e6da2aafe14d0"
repo="repos/AlecKriebel/Math";prefix="unsolved_math_prioritization/attempts/2715/"
streams=[]
def dump(n,obj): (root/n).write_text(json.dumps(obj,sort_keys=True,indent=2)+"\n")
def call(label,argv):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.Popen(argv,cwd="/Users/alec/Documents/Math",stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,"GIT_OPTIONAL_LOCKS":"0"})
 out,err=p.communicate()
 rec={"label":label,"argv":argv,"actual_pid":p.pid,"start_utc":start,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":p.returncode,
 "stdout_bytes":len(out),"stdout_sha256":hashlib.sha256(out).hexdigest(),"stdout_base64":base64.b64encode(out).decode(),
 "stderr_bytes":len(err),"stderr_sha256":hashlib.sha256(err).hexdigest(),"stderr_base64":base64.b64encode(err).decode()}
 streams.append(rec);dump("RETRIEVAL_FULL_COMMAND_STREAMS.json",streams)
 if p.returncode:raise RuntimeError(label+" failed; full streams preserved")
 return out
def api(label,path,*opts):return json.loads(call(label,["gh","api",path,*opts]))
pr=api("PR_start",repo+"/pulls/62")
assert pr["head"]["sha"]==head and pr["base"]["sha"]==base and pr["state"]=="open" and pr["draft"] is True
dump("PR_METADATA.json",pr)
files=api("diff_files",repo+"/pulls/62/files?per_page=100");dump("CHANGED_FILES.json",files)
science=[x for x in files if x["filename"].startswith(prefix)]
assert len(files)==18 and len(science)==17
assert {x["filename"] for x in files if not x["filename"].startswith(prefix)}=={"unsolved_math_prioritization/QUEUE.md"}
commit=api("head_commit",repo+"/git/commits/"+head)
tree=commit["tree"]["sha"];modes={}
for part in ["unsolved_math_prioritization","attempts","2715"]:
 obj=api("tree_parent_"+part,repo+"/git/trees/"+tree)
 entry=next(x for x in obj["tree"] if x["path"]==part and x["type"]=="tree");tree=entry["sha"]
def subtree(sha,relative=""):
 obj=api("scientific_tree_"+(relative or "root"),repo+"/git/trees/"+sha)
 for e in obj["tree"]:
  p=relative+e["path"]
  if e["type"]=="tree":subtree(e["sha"],p+"/")
  else:modes[p]=e
subtree(tree)
assert set(modes)=={x["filename"][len(prefix):] for x in science}
original=root/"original";original.mkdir(exist_ok=False)
auth=[]
for x in science:
 rel=x["filename"][len(prefix):];entry=modes[rel]
 assert x["sha"]==entry["sha"] and entry["mode"]=="100644" and entry["type"]=="blob"
 obj=api("blob_"+rel,repo+"/git/blobs/"+entry["sha"])
 assert obj["encoding"]=="base64";raw=base64.b64decode(obj["content"])
 assert obj["size"]==len(raw) and obj["sha"]==entry["sha"]
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==entry["sha"]
 p=original/rel;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("xb") as f:f.write(raw)
 os.chmod(p,0o444)
 auth.append({"repository_path":x["filename"],"path":str(p),"relative_path":rel,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"git_blob_sha1":entry["sha"],"git_mode":entry["mode"],"full_mode_07777":"0444","nlink":1})
queue=next(x for x in files if x["filename"]=="unsolved_math_prioritization/QUEUE.md")
q=api("QUEUE_blob",repo+"/git/blobs/"+queue["sha"]);qb=base64.b64decode(q["content"]);assert hashlib.sha1(b"blob "+str(len(qb)).encode()+b"\0"+qb).hexdigest()==queue["sha"]
dump("PR_QUEUE_SELECTED.json",{"body_bytes":len(qb),"body_sha256":hashlib.sha256(qb).hexdigest(),"git_blob_sha1":queue["sha"],"selected":[{"line":i,"text":v} for i,v in enumerate(qb.decode().split("\n"),1) if "2715 / KP-1.56" in v],"whole_body_not_copied":True})
compare=api("base_head_compare",repo+"/compare/"+base+"..."+head)
dump("COMPARE_AUTHENTICATION.json",{k:compare.get(k) for k in ["status","ahead_by","behind_by","total_commits"]}|{"base_commit":compare["base_commit"]["sha"],"merge_base_commit":compare["merge_base_commit"]["sha"],"commits":[x["sha"] for x in compare["commits"]]})
assert compare["base_commit"]["sha"]==base and compare["merge_base_commit"]["sha"]==base
end=api("PR_end",repo+"/pulls/62");assert end["head"]["sha"]==head and end["base"]["sha"]==base
dump("ORIGINAL_AUTHENTICATION.json",{"schema":"pr62-original-github-authentication/v1","actual_operator_pid":os.getpid(),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":head,"base":base,"problem_id":2715,"scientific_files":auth,"science_count":17,"diff_count":18,"whole_scientific_tree_authenticated":True,"native_Git_PR_remote_mutation":False,"ROOT_custody_or_scientific_approval":False})
print(json.dumps({"status":"PASS_ORIGINAL_17_BLOBS_AND_SCOPED_TREE","head":head,"original17":17,"diff18":18,"commands":len(streams),"operator_pid":os.getpid()},sort_keys=True))
