"""Explicit-exception, external-pin custody for review01; no input mutations."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,sys
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,"Duplicate JSON key");d[k]=v
    return d
def nonfinite(v):raise ValueError("Nonfinite JSON")
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=nonfinite)
def regular(p):
    # O_NONBLOCK prevents a FIFO open from becoming a denial of service.
    fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    try:
        need(stat.S_ISREG(os.fstat(fd).st_mode),"Nonregular input: "+str(p))
        with os.fdopen(os.dup(fd),"rb") as f:return f.read()
    finally:os.close(fd)
def rel(name):
    p=PurePosixPath(name)
    need(isinstance(name,str) and name and not p.is_absolute() and str(p)==name
         and all(x not in ("",".","..") for x in name.split("/")) and "\\" not in name,"Unsafe path")
    return p
def verify(root,inputs,pin):
    need(re.fullmatch("[0-9a-f]{64}",pin) is not None,"Bad external pin")
    need(not root.is_symlink() and root.is_dir(),"Bad packet root")
    need(not inputs.is_symlink() and inputs.is_dir(),"Bad input root")
    raw=regular(root/"MANIFEST.json");need(sha(raw)==pin,"External manifest mismatch")
    m=parse(raw);need(m["schema"]=="pr781-preprint-review01/v1","Bad manifest schema")
    need(m["explicit_exceptions"]==["MANIFEST.json"],"Exceptions differ")
    need(m["head"]=="4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f","Head differs")
    files=m["files"];need(set(p.name for p in root.iterdir())==set(files)|{"MANIFEST.json"},"Flat closure differs")
    for name,row in files.items():
        need(len(rel(name).parts)==1 and name!="MANIFEST.json","Bad flat name")
        b=regular(root/name);need({"bytes":len(b),"sha256":sha(b)}==row,"Artifact differs:"+name)
    bindings=parse(regular(root/"INPUTS.json"))
    for name,row in bindings["files"].items():
        path=inputs
        for part in rel(name).parts:
            path=path/part;need(not path.is_symlink(),"Input symlink")
        b=regular(path);need({"bytes":len(b),"sha256":sha(b)}==row,"Input differs:"+name)
    initial=parse(regular(root/"INITIAL_POSITION.json"))
    need(initial["inputs"]["paper.tex"]==bindings["files"]["paper.tex"]["sha256"],"Initial paper differs")
    verdict=parse(regular(root/"VERDICT.json"))
    need(verdict["actionable_issue_count"]==1 and verdict["mathematical_issues"]==[],"Verdict differs")
    return {"result":"PASS","artifact_files":len(files),"input_bindings":len(bindings["files"]),
            "manifest_sha256":pin,"optimized":bool(sys.flags.optimize)}
def main():
    a=argparse.ArgumentParser();a.add_argument("--root",type=Path,default=Path(__file__).absolute().parent)
    a.add_argument("--input-root",type=Path,required=True);a.add_argument("--expected-manifest-sha256",required=True)
    x=a.parse_args()
    try:v=verify(x.root.absolute(),x.input_root.absolute(),x.expected_manifest_sha256)
    except Exception as e:print(json.dumps({"result":"FAIL","error":str(e)}));return 1
    print(json.dumps(v,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
