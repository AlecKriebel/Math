#!/usr/bin/env python3
"""Authenticate source-free payload before running any payload code."""
from pathlib import Path
import hashlib,json,re,stat,subprocess,sys
EXPECTED_MANIFEST="abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c"
class Reject(Exception):pass
def require(ok,msg):
    if not ok:raise Reject(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
    d={}
    for k,v in xs:
        require(k not in d,"duplicate JSON key");d[k]=v
    return d
def main():
    require(len(sys.argv) in (1,2),"usage: bootstrap.py [packet-directory]")
    here=Path(__file__).resolve().parent;p=Path(sys.argv[1]) if len(sys.argv)==2 else here/"packet"
    require(not p.is_symlink(),"symlink packet")
    root=p.resolve();require(root.is_dir(),"missing packet")
    mp=here/"AUTHOR_MANIFEST.json";require(not mp.is_symlink() and stat.S_ISREG(mp.stat().st_mode),"bad manifest file")
    raw=mp.read_bytes();require(len(raw)<=1000000 and sha(raw)==EXPECTED_MANIFEST,"manifest trust-anchor mismatch")
    m=json.loads(raw,object_pairs_hook=pairs)
    require(type(m) is dict and set(m)=={"schema","problem_id","resolution","approaches_used","files"},"manifest keys")
    require(m["schema"]=="habiro-rank-manifest-v1","schema")
    require(type(m["problem_id"]) is int and m["problem_id"]==10400145,"identity")
    require(m["resolution"]=="negative_literal_statement" and type(m["approaches_used"]) is int and m["approaches_used"]==1,"resolution")
    require(type(m["files"]) is list and len(m["files"])>0,"empty inventory")
    names=[]
    for e in m["files"]:
        require(type(e) is dict and set(e)=={"path","bytes","sha256"},"entry schema")
        n=e["path"];require(type(n) is str and re.fullmatch(r"[A-Za-z0-9_.-]+",n) is not None and n not in (".",".."),"unsafe path")
        require(n not in names,"duplicate file");names.append(n)
        require(type(e["bytes"]) is int and 0<=e["bytes"]<=10000000,"invalid size")
        require(type(e["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}",e["sha256"]) is not None,"invalid hash")
        p=root/n;require(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode),"bad payload type")
        v=p.read_bytes();require(len(v)==e["bytes"] and sha(v)==e["sha256"],"payload mismatch: "+n)
    require(set(x.name for x in root.iterdir())==set(names),"extra/missing payload")
    require("verify.py" in names and "DIAGNOSTICS.json" in names,"missing checker or receipt")
    flags=[] if sys.flags.optimize==0 else (["-O"] if sys.flags.optimize==1 else ["-OO"])
    r=subprocess.run([sys.executable,"-I","-S","-B",*flags,str(root/"verify.py")],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    require(r.returncode==0,"checker failed: "+r.stderr.decode("utf-8","replace"))
    require(r.stdout==(root/"DIAGNOSTICS.json").read_bytes(),"checker output mismatch")
    return {"schema":"habiro-rank-bootstrap-v1","status":"PASS","files":len(names),"manifest_sha256":EXPECTED_MANIFEST,"diagnostic_sha256":sha(r.stdout)}
if __name__=="__main__":
    try:print(json.dumps(main(),sort_keys=True,separators=(",",":")))
    except (Reject,OSError,ValueError,KeyError,TypeError,IndexError,subprocess.SubprocessError) as e:
        print("REJECT: "+str(e),file=sys.stderr);sys.exit(1)
