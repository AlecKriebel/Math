#!/usr/bin/env python3
"""Externally authenticate this bootstrap before use. It authenticates payload before execution."""
from pathlib import Path
import hashlib,json,math,re,stat,subprocess,sys
MANIFEST_SHA256="9ddef9ad585717ca652952fddceef1d3cf0f753f2e23c59a5cdc581ff92e5850"
class Rejected(Exception):pass
def require(ok,msg):
    if not ok:raise Rejected(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,"duplicate JSON key");d[k]=v
    return d
def bad_constant(x):raise Rejected("nonfinite JSON constant")
def finite_float(s):
    x=float(s);require(math.isfinite(x),"nonfinite JSON number");return x
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=bad_constant,parse_float=finite_float)
def regular(p):
    s=p.lstat();require(stat.S_ISREG(s.st_mode),"symlink or nonregular file")
    require(stat.S_IMODE(s.st_mode) in (0o444,0o644),"unexpected payload mode")
    return s
def main():
    require(len(sys.argv)==2,"usage: bootstrap.py /path/to/author")
    base=Path(__file__).resolve().parent;mp=base/"AUTHOR_MANIFEST.json";regular(mp)
    raw=mp.read_bytes();require(len(raw)<1000000 and sha(raw)==MANIFEST_SHA256,"manifest trust-anchor mismatch")
    m=parse(raw);require(type(m) is dict and set(m)=={"schema","problem_id","status","approaches_used","files"},"manifest schema")
    require(m["schema"]=="critical-value-collisions-manifest-v1","manifest version")
    require(type(m["problem_id"]) is int and m["problem_id"]==10800003,"target")
    require(type(m["approaches_used"]) is int and m["approaches_used"]==5 and m["status"]=="unsolved","disposition")
    p=Path(sys.argv[1]);require(not p.is_symlink() and p.is_dir(),"payload root")
    root=p.resolve();require(stat.S_IMODE(root.stat().st_mode) in (0o555,0o755),"payload root mode")
    es=m["files"];require(type(es) is list and len(es)==10,"manifest inventory count")
    names=[]
    for e in es:
        require(type(e) is dict and set(e)=={"path","bytes","sha256"},"entry schema")
        n=e["path"];require(type(n) is str and re.fullmatch(r"[A-Za-z0-9_.-]+",n) is not None and n not in (".",".."),"unsafe filename")
        require(n not in names,"duplicate entry");names.append(n)
        require(type(e["bytes"]) is int and 0<=e["bytes"]<=10000000,"entry size")
        require(type(e["sha256"]) is str and re.fullmatch(r"[a-f0-9]{64}",e["sha256"]) is not None,"entry hash")
        fp=root/n;ss=regular(fp);require(ss.st_size==e["bytes"],"payload size mismatch")
        b=fp.read_bytes();require(len(b)==e["bytes"] and sha(b)==e["sha256"],"payload hash mismatch: "+n)
        if n.endswith(".json"):parse(b)
    require(set(x.name for x in root.iterdir())==set(names),"extra/missing payload inventory")
    flags=[] if sys.flags.optimize==0 else (["-O"] if sys.flags.optimize==1 else ["-OO"])
    r=subprocess.run([sys.executable,"-I","-S","-B",*flags,str(root/"verify.py")],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    require(r.returncode==0,"pinned verifier failed: "+r.stderr.decode("utf-8","replace"))
    require(r.stdout==(root/"DIAGNOSTICS.json").read_bytes(),"diagnostic output mismatch")
    return {"schema":"critical-value-collisions-bootstrap-v1","status":"PASS","files":len(names),"manifest_sha256":MANIFEST_SHA256,"diagnostic_sha256":sha(r.stdout)}
if __name__=="__main__":
    try:print(json.dumps(main(),sort_keys=True,separators=(",",":")))
    except (Rejected,OSError,ValueError,TypeError,KeyError,IndexError,subprocess.SubprocessError) as e:
        print("REJECT: "+str(e),file=sys.stderr);sys.exit(1)
