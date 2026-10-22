"""Exact PR1391 integration; no local Git/index/ref writes or force updates."""
from pathlib import Path
import base64,datetime,gzip,hashlib,json,os,subprocess,sys
D=Path(__file__).resolve().parent
P=json.loads((D/"INTEGRATION_PLAN.json").read_text())
def need(ok,message):
    if not ok: raise RuntimeError(message)
def durable(name,value):
    path=D/name
    data=json.dumps(value,ensure_ascii=False,indent=2).encode()+b"\n"
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"wb") as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    directory=os.open(D,os.O_RDONLY)
    try:os.fsync(directory)
    finally:os.close(directory)
def api(endpoint,method="GET",body=None,label=None):
    if method!="GET":
        need(label is not None,"Write must have unique durable intent")
        durable(label+"_INTENT.json",{"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"method":method,"endpoint":endpoint,"body_sha256":hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()})
    command=["gh","api","--hostname","github.com","repos/AlecKriebel/Math/"+endpoint,"--method",method]
    data=None
    if body is not None:
        command+=["--input","-"];data=json.dumps(body,ensure_ascii=False).encode()
    result=subprocess.run(command,input=data,capture_output=True)
    need(result.returncode==0,"API failed; preserve intent and reconcile before another write: "+endpoint+" "+result.stderr.decode()[:300])
    value=json.loads(result.stdout)
    if method!="GET":durable(label+"_RESPONSE.json",value)
    return value
def tree(sha,recursive=False):
    value=api("git/trees/"+sha+("?recursive=1" if recursive else ""))
    need(not value.get("truncated"),"Incomplete tree")
    return {x["path"]:x for x in value["tree"]}
def same_except(a,b,allowed,label):
    need(set(a)-allowed==set(b)-allowed,label+" membership")
    for key in set(a)-allowed:need(a[key]==b[key],label+" changed "+key)
def state_gate():
    pr=api("pulls/1391")
    need(pr["state"]=="open" and not pr["merged"],"PR changed state")
    need(pr["head"]["sha"]==P["expected_old_head"] and pr["head"]["ref"]==P["head_ref"],"PR head changed")
    need(api("git/ref/heads/main")["object"]["sha"]==P["main_parent"],"Main advanced; rebuild on latest")
    return pr
def verify_tree(new):
    old=tree(P["base_tree"]);fresh=tree(new);project=P["project_root"]
    need(project not in old,"Existing main project would be overwritten")
    same_except(old,fresh,{"unsolved_math_prioritization",project},"repository")
    a=tree(old["unsolved_math_prioritization"]["sha"]);b=tree(fresh["unsolved_math_prioritization"]["sha"])
    same_except(a,b,{"QUEUE.md"},"all other unsolved program content")
    wanted={x["path"][len(project)+1:]:x["git_blob"] for x in P["selected"] if x["path"].startswith(project+"/")}
    actual={p:e["sha"] for p,e in tree(fresh[project]["sha"],True).items() if e["type"]=="blob"}
    need(actual==wanted,"Complete new project exact leaves differ")
    queue=next(x for x in P["selected"] if x["path"]=="unsolved_math_prioritization/QUEUE.md")
    need(b["QUEUE.md"]["sha"]==queue["git_blob"],"Exact one-row QUEUE differs")
def construct():
    state_gate();entries=[]
    original=tree(P["old_root_unsolved_tree"])["QUEUE.md"]["sha"]
    rawblob=api("git/blobs/"+original)
    oldqueue=base64.b64decode(rawblob["content"])
    oldline=P["target_queue_old_line"].encode()
    newline=P["target_queue_new_line"].encode()
    need(oldqueue.count(oldline)==1,"Queue source row not unique")
    exactqueue=oldqueue.replace(oldline,newline,1)
    planned=next(x for x in P["selected"] if x["path"]=="unsolved_math_prioritization/QUEUE.md")
    need(exactqueue==gzip.decompress((D/"private"/planned["private_payload"]).read_bytes()),"Unrelated queue bytes would change")
    for index,item in enumerate(P["selected"]):
        raw=gzip.decompress((D/"private"/item["private_payload"]).read_bytes())
        need(len(raw)==item["bytes"] and hashlib.sha256(raw).hexdigest()==item["sha256"],"Frozen selected bytes changed")
        entry={"path":item["path"],"mode":"100644","type":"blob"}
        try:entry["content"]=raw.decode("utf-8")
        except UnicodeDecodeError:
            value=api("git/blobs","POST",{"encoding":"base64","content":base64.b64encode(raw).decode()},"BLOB_"+str(index))
            need(value["sha"]==item["git_blob"],"Binary blob mismatch")
            entry["sha"]=value["sha"]
        entries.append(entry)
    state_gate()
    created=api("git/trees","POST",{"base_tree":P["base_tree"],"tree":entries},"TREE")
    verify_tree(created["sha"])
    commit=api("git/commits","POST",{"message":"Integrate reviewed full Hochschild BV classification for PR1391","tree":created["sha"],"parents":P["new_commit_parents"]},"COMMIT")
    check=api("git/commits/"+commit["sha"])
    need(check["tree"]["sha"]==created["sha"] and [x["sha"] for x in check["parents"]]==P["new_commit_parents"],"Commit identity")
    durable("CONSTRUCTED.json",{"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"commit":commit["sha"],"tree":created["sha"],"verified_unselected_preservation":True,"selected_paths":len(P["selected"]),"parents":P["new_commit_parents"],"branch_changed":False,"publication_pending":True})
    print(json.dumps({"status":"constructed_verified_unpushed","commit":commit["sha"],"selected_paths":len(P["selected"])}))
def push():
    # Root separately supplies a just-completed live dedup readback receipt.
    gate=json.loads((D/"ROOT_FRESH_DEDUP_FOR_PUSH.json").read_text())
    need(gate["accepted"] is True and gate["no_new_duplicate"] is True,"Fresh dedup adoption missing")
    when=datetime.datetime.fromisoformat(gate["completed_at"])
    need(0<=(datetime.datetime.now(datetime.timezone.utc)-when).total_seconds()<180,"Stale fresh dedup")
    built=json.loads((D/"CONSTRUCTED.json").read_text());state_gate();verify_tree(built["tree"]);state_gate()
    need((datetime.datetime.now(datetime.timezone.utc)-when).total_seconds()<180,"Dedup aged during final checks")
    endpoint="git/refs/heads/"+P["head_ref"]
    result=api(endpoint,"PATCH",{"sha":built["commit"],"force":False},"BRANCH_FF")
    need(result["object"]["sha"]==built["commit"],"Ambiguous branch update; GET only")
    current=api("pulls/1391");need(current["head"]["sha"]==built["commit"],"Branch result not reflected in PR; GET only")
    durable("PUSH_VERIFIED.json",{"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":built["commit"],"force":False,"local_git_writes":False,"publication_pending":True})
    print(json.dumps({"status":"pushed_verified","head":built["commit"]}))
if __name__=="__main__":
    need(sys.argv[1:] in [["construct"],["push"]],"Exact phase required")
    globals()[sys.argv[1]]()
