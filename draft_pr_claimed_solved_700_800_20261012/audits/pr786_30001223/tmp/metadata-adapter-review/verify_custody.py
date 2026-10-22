"""External-pin custody of the PR786 administrative integration review."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,sys
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {"bytes":len(b),"sha256":sha(b)}
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,"Duplicate key");d[k]=v
    return d
def nonfinite(x):raise ValueError("Nonfinite JSON")
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=nonfinite)
def regular(p):
    fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    try:
        need(stat.S_ISREG(os.fstat(fd).st_mode),"Nonregular file")
        with os.fdopen(os.dup(fd),"rb") as s:return s.read()
    finally:os.close(fd)
def safe(name):
    need(isinstance(name,str) and name and "\\" not in name,"Bad path")
    p=PurePosixPath(name)
    need(not p.is_absolute() and str(p)==name and all(s not in ("",".","..") for s in name.split("/")),"Unsafe path")
    return p
def child(root,name):
    p=root
    for part in safe(name).parts:p=p/part;need(not p.is_symlink(),"Input symlink")
    return p
def verify(root,case,tool,mpin,cpin):
    for p in (mpin,cpin):need(re.fullmatch("[0-9a-f]{64}",p) is not None,"Bad pin")
    need(root.is_dir() and not root.is_symlink(),"Bad review root")
    need(case.is_dir() and not case.is_symlink(),"Bad case root")
    need(sha(regular(root/"verify_custody.py"))==cpin,"External checker pin")
    raw=regular(root/"MANIFEST.json");need(sha(raw)==mpin,"External manifest pin")
    m=parse(raw);need(m["schema"]=="pr786-production-adapter-review/v1","Wrong schema")
    need(m["explicit_exceptions"]==["MANIFEST.json"],"Exceptions differ")
    files=m["files"];need(set(p.name for p in root.iterdir())==set(files)|{"MANIFEST.json"},"Flat closure differs")
    for n,row in files.items():
        need(len(safe(n).parts)==1 and n!="MANIFEST.json","Bad flat member")
        need(ident(regular(root/n))==row,"Authored file differs:"+n)
    bindings=parse(regular(root/"INPUTS.json"))
    for n,row in bindings["case_files"].items():
        need(ident(regular(child(case,n)))==row,"Case input differs:"+n)
    need(ident(regular(tool))==bindings["repository_tool"],"Repository tool differs")
    v=parse(regular(root/"VERDICT.json"))
    need(v["actionable_issue_count"]==0 and v["whole_paper_review_round"] is False,"Verdict scope")
    replay=parse(regular(root/"OFFLINE_REPLAY.json"))
    need(len(replay["runs"])==2 and all(x["result"]["result"]=="PASS" for x in replay["runs"]),"Offline replay")
    return {"result":"PASS","artifact_files":len(files),"case_input_files":len(bindings["case_files"]),
            "repository_tool_checked":True,"whole_paper_review_round":False,"optimized":bool(sys.flags.optimize)}
def main():
    a=argparse.ArgumentParser();a.add_argument("--root",type=Path,default=Path(__file__).absolute().parent)
    a.add_argument("--case-root",required=True,type=Path);a.add_argument("--tool",required=True,type=Path)
    a.add_argument("--expected-manifest-sha256",required=True);a.add_argument("--expected-checker-sha256",required=True);x=a.parse_args()
    try:v=verify(x.root.absolute(),x.case_root.absolute(),x.tool.absolute(),x.expected_manifest_sha256,x.expected_checker_sha256)
    except Exception as e:print(json.dumps({"result":"FAIL","error":str(e)}));return 1
    print(json.dumps(v,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
