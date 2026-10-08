#!/usr/bin/env python3
"""Authenticate all packet bytes before running the finite diagnostics."""
from pathlib import Path
import hashlib,json,subprocess,sys
EXPECTED_MANIFEST = "0c1731e5864003466319176235ee3e4feb16c0d7bc29d75a0bc6e43c1f289d89"
class VerificationError(Exception): pass
def require(condition,message):
    if not condition: raise VerificationError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def run():
    require(len(sys.argv) in (1,2),"usage: bootstrap.py [packet-directory]")
    here=Path(__file__).resolve().parent
    root=Path(sys.argv[1]).resolve() if len(sys.argv)==2 else here/"packet"
    manifest=here/"AUTHOR_MANIFEST.json"
    require(not manifest.is_symlink(),"symlink manifest")
    raw=manifest.read_bytes()
    require(sha(raw)==EXPECTED_MANIFEST,"manifest trust anchor mismatch")
    data=json.loads(raw)
    require(set(data)=={"schema","problem_id","disposition","approaches","files"},"manifest keys")
    require(data["schema"]=="minimal-surfaces-author-manifest-v1","manifest schema")
    require(type(data["problem_id"]) is int and data["problem_id"]==10300008,"manifest identity")
    require(data["disposition"]=="unsolved" and type(data["approaches"]) is int and data["approaches"]==5,"disposition")
    require(type(data["files"]) is list and len(data["files"])>0,"inventory")
    names=[]
    for item in data["files"]:
        require(type(item) is dict and set(item)=={"path","bytes","sha256"},"entry schema")
        name=item["path"]
        require(type(name) is str and name not in ("",".","..") and "/" not in name and "\\" not in name,"unsafe path")
        require(name not in names,"duplicate path")
        names.append(name)
        p=root/name
        require(p.is_file() and not p.is_symlink(),"missing or symlink payload")
        b=p.read_bytes()
        require(type(item["bytes"]) is int and len(b)==item["bytes"],"size: "+name)
        require(sha(b)==item["sha256"],"digest: "+name)
    require(set(p.name for p in root.iterdir())==set(names),"extra/missing payload")
    expected=(root/"DIAGNOSTICS.json").read_bytes()
    flags=[]
    if sys.flags.optimize==1:flags=["-O"]
    elif sys.flags.optimize>=2:flags=["-OO"]
    result=subprocess.run([sys.executable,"-I","-S","-B"]+flags+[str(root/"verify.py")],cwd=root,
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    require(result.returncode==0,"diagnostics rejected: "+result.stderr.decode("utf-8","replace"))
    require(result.stdout==expected,"diagnostic output mismatch")
    return {"schema":"minimal-surfaces-bootstrap-v1","status":"pass","files":len(names),
            "manifest_sha256":EXPECTED_MANIFEST,"diagnostic_sha256":sha(expected)}
if __name__=="__main__":
    try: print(json.dumps(run(),sort_keys=True,separators=(",",":")))
    except (VerificationError,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print("REJECT: "+str(e),file=sys.stderr);sys.exit(1)
