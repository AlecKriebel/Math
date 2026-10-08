#!/usr/bin/env python3
"""Authenticate the complete source-free payload before executing any payload code."""
from pathlib import Path
import hashlib,json,subprocess,sys,re
EXPECTED_MANIFEST = "a8e8ce66abc1366122e72cd8086b9cba999e04e05b9f8d1b7b41111d3a2fbcd6"
class VerificationError(Exception):pass
def require(ok,message):
    if not ok:raise VerificationError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,"duplicate JSON key")
        d[k]=v
    return d
def run():
    require(len(sys.argv) in (1,2),"usage: bootstrap.py [packet-directory]")
    here=Path(__file__).resolve().parent
    arg=Path(sys.argv[1]) if len(sys.argv)==2 else here/"packet"
    require(not arg.is_symlink(),"symlink packet directory")
    root=arg.resolve();require(root.is_dir(),"missing packet directory")
    manifest=here/"AUTHOR_MANIFEST.json"
    require(not manifest.is_symlink(),"symlink manifest")
    raw=manifest.read_bytes();require(sha(raw)==EXPECTED_MANIFEST,"manifest trust anchor mismatch")
    m=json.loads(raw,object_pairs_hook=pairs)
    require(type(m) is dict and set(m)=={"schema","problem_id","disposition","approaches","files"},"manifest schema keys")
    require(m["schema"]=="fixed-span-author-manifest-v1","manifest schema")
    require(type(m["problem_id"]) is int and m["problem_id"]==10400013,"manifest identity")
    require(m["disposition"]=="unsolved" and type(m["approaches"]) is int and m["approaches"]==5,"disposition")
    require(type(m["files"]) is list and len(m["files"])>0,"inventory")
    names=[]
    for e in m["files"]:
        require(type(e) is dict and set(e)=={"path","bytes","sha256"},"entry schema")
        name=e["path"]
        require(type(name) is str and bool(re.fullmatch(r"[A-Za-z0-9_.-]+",name)) and name not in (".",".."),"unsafe path")
        require(name not in names,"duplicate path")
        require(type(e["bytes"]) is int and e["bytes"]>=0,"size type")
        require(type(e["sha256"]) is str and bool(re.fullmatch(r"[0-9a-f]{64}",e["sha256"])),"hash type")
        names.append(name);p=root/name
        require(p.is_file() and not p.is_symlink(),"missing or symlink payload")
        b=p.read_bytes();require(len(b)==e["bytes"],"size: "+name);require(sha(b)==e["sha256"],"digest: "+name)
    require(set(p.name for p in root.iterdir())==set(names),"extra/missing payload")
    expected=(root/"DIAGNOSTICS.json").read_bytes()
    flags=[] if not sys.flags.optimize else (["-O"] if sys.flags.optimize==1 else ["-OO"])
    result=subprocess.run([sys.executable,"-I","-S","-B",*flags,str(root/"verify.py")],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    require(result.returncode==0,"diagnostics failed: "+result.stderr.decode("utf-8","replace"))
    require(result.stdout==expected,"diagnostics output mismatch")
    return {"schema":"fixed-span-bootstrap-v1","status":"PASS","files":len(names),"manifest_sha256":EXPECTED_MANIFEST,"diagnostic_sha256":sha(expected)}
if __name__=="__main__":
    try:print(json.dumps(run(),sort_keys=True,separators=(",",":")))
    except (VerificationError,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print("REJECT: "+str(e),file=sys.stderr);sys.exit(1)
