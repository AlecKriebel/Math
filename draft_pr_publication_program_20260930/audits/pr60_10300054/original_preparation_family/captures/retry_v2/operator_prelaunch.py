"""Owned PR60 read-only GitHub intake. No Git, PR, queue, or remote mutations."""
import base64,datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
HEAD="1e762651b698c1fb519901bd924c5bd3717cc5ef"
REPO="AlecKriebel/Math"
PREFIX="unsolved_math_prioritization/attempts/10300054/"
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("xb") as f: f.write(b)
def run(name,args):
 cap=ROOT/"captures"/"retry_v2"/name; cap.mkdir(parents=True,exist_ok=False)
 argv=["/opt/homebrew/bin/gh"]+args
 start=utc()
 child=subprocess.Popen(argv,cwd="/Users/alec/Documents/Math",stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=child.communicate(); end=utc()
 write(cap/"stdout.bin",out); write(cap/"stderr.bin",err)
 rec={"actual_execution":True,"controller_pid":os.getpid(),"pid":child.pid,"argv":argv,"cwd":"/Users/alec/Documents/Math","started_utc":start,"finished_utc":end,"exit_code":child.returncode,"stdin_supplied":False,"stdout":{"bytes":len(out),"sha256":sha(out)},"stderr":{"bytes":len(err),"sha256":sha(err)},"operator_sha256":sha(pathlib.Path(__file__).read_bytes()),"read_only_service_access":True,"ROOT_helper":False}
 write(cap/"CAPTURE.json",(json.dumps(rec,indent=2,sort_keys=True)+"\n").encode())
 if child.returncode: raise RuntimeError("read failed: "+name)
 return out
def api(name,path,jq=None):
 args=["api",path]
 if jq is not None: args+=["--jq",jq]
 return run(name,args)
started=utc()
controller=pathlib.Path(__file__).read_bytes()
write(ROOT/"captures"/"retry_v2"/"operator_prelaunch.py",controller)
meta=json.loads(api("pr_metadata_start","repos/"+REPO+"/pulls/60","{number,title,state,html_url,body,head:{sha:.head.sha,ref:.head.ref},base:{sha:.base.sha,ref:.base.ref},changed_files,additions,deletions}"))
assert meta["head"]["sha"]==HEAD
files=json.loads(api("pr_changed_files","repos/"+REPO+"/pulls/60/files?per_page=100","[.[]|{filename,status,sha,additions,deletions,changes}]"))
assert len(files)==18
gitcommit=json.loads(api("git_commit","repos/"+REPO+"/git/commits/"+HEAD))
assert gitcommit["sha"]==HEAD
entries=[]
for name,rel in [("contents_attempt",""),("contents_review","independent_review/"),("contents_author_replay","independent_review/author_replay/")]:
 rows=json.loads(api(name,"repos/"+REPO+"/contents/"+(PREFIX+rel).rstrip("/")+"?ref="+HEAD))
 entries.extend(x for x in rows if x["type"]=="file")
assert len(entries)==17 and len({x["path"] for x in entries})==17
changed={x["filename"] for x in files}
assert {x["path"] for x in entries}==changed-{"unsolved_math_prioritization/QUEUE.md"}
decoded={}
pins=[]
for row in sorted(entries,key=lambda x:x["path"]):
 blobsha=row["sha"]
 if blobsha not in decoded:
  blob=json.loads(api("blob_"+blobsha,"repos/"+REPO+"/git/blobs/"+blobsha))
  assert blob["sha"]==blobsha and blob["encoding"]=="base64"
  b=base64.b64decode(blob["content"])
  assert len(b)==blob["size"]
  assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==blobsha
  decoded[blobsha]=b
 b=decoded[blobsha]
 rel=row["path"][len(PREFIX):]
 write(ROOT/"original"/rel,b)
 pins.append({"repository_path":row["path"],"local_path":"original/"+rel,"git_blob_sha1":blobsha,"sha256":sha(b),"bytes":len(b),"github_size":row["size"],"git_mode":"not separately authenticated; immutable blob body authenticated","local_mode_at_write":oct((ROOT/"original"/rel).stat().st_mode&0o7777)})
queuefile=next(x for x in files if x["filename"]=="unsolved_math_prioritization/QUEUE.md")
qb=json.loads(api("blob_queue_"+queuefile["sha"],"repos/"+REPO+"/git/blobs/"+queuefile["sha"]))
qbody=base64.b64decode(qb["content"])
assert hashlib.sha1(b"blob "+str(len(qbody)).encode()+b"\0"+qbody).hexdigest()==queuefile["sha"]
selected=[{"line":i+1,"text":line} for i,line in enumerate(qbody.decode().splitlines()) if "10300054" in line]
assert len(selected)==1
write(ROOT/"PR_QUEUE_SELECTED.json",(json.dumps({"head":HEAD,"full_blob_git_sha1":queuefile["sha"],"full_blob_bytes":len(qbody),"full_blob_sha256":sha(qbody),"selected_lines":selected,"full_queue_not_redistributed":True},indent=2,sort_keys=True)+"\n").encode())
patch=run("full_pr_diff",["pr","diff","60","--repo",REPO])
write(ROOT/"FULL_PR_DIFF.patch",patch)
endmeta=json.loads(api("pr_metadata_end","repos/"+REPO+"/pulls/60","{number,head:{sha:.head.sha,ref:.head.ref},base:{sha:.base.sha,ref:.base.ref},state}"))
assert endmeta["head"]["sha"]==HEAD
write(ROOT/"PR_METADATA.json",(json.dumps(meta,sort_keys=True,indent=2)+"\n").encode())
write(ROOT/"CHANGED_FILES.json",(json.dumps(files,sort_keys=True,indent=2)+"\n").encode())
result={"schema":"pr60-original-github-intake/v1","started_utc":started,"finished_utc":utc(),"operator_pid":os.getpid(),"operator_prelaunch_sha256":sha(controller),"head":HEAD,"reported_github_base":meta["base"]["sha"],"local_git_head_object_absent_at_initial_read":True,"local_merge_base":"not available without fetching; no fetch performed","scientific_files":pins,"scientific_file_count":17,"changed_file_count":18,"unique_scientific_blobs":len(decoded),"head_confirmed_after_retrieval":True,"original_body_preserved":True,"author_code_replayed_by_this_preparer":False,"mathematical_acceptance_or_ROOT_approval":False,"queue_native_or_remote_mutation":False}
write(ROOT/"ORIGINAL_AUTHENTICATION.json",(json.dumps(result,indent=2,sort_keys=True)+"\n").encode())
print(json.dumps({"head":HEAD,"scientific_files":len(pins),"original":str(ROOT/"original"),"operator_pid":os.getpid(),"intake_only":True},sort_keys=True))

