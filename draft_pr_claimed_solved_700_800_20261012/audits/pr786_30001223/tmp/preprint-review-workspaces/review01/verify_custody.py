"""Explicit-exception PR786 whole-review custody; read-only standard library."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,os,re,stat,sys,zipfile
HEAD="34f21454986a28ca49f24999be3a0fd1b42755f8"
INPUT_PIN="776e821d5311caf44eeb1a2aa1ef0070ac3bc46b75c1fc027d21a69a0c40b207"
SOURCE_PIN="32d7a891fa5ad3ff49269865e122f5ed3327da4fe83b3344738d958130bcf38b"
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {"bytes":len(b),"sha256":sha(b)}
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,"Duplicate JSON key");d[k]=v
    return d
def reject(x):raise ValueError("Nonfinite JSON")
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=reject)
def pin(s):need(isinstance(s,str) and re.fullmatch("[0-9a-f]{64}",s) is not None,"Bad external pin")
def regular(p):
    fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    try:
        need(stat.S_ISREG(os.fstat(fd).st_mode),"Nonregular file:"+str(p))
        with os.fdopen(os.dup(fd),"rb") as f:return f.read()
    finally:os.close(fd)
def safe(name):
    need(isinstance(name,str) and name and "\\" not in name,"Bad relative path")
    p=PurePosixPath(name)
    need(not p.is_absolute() and str(p)==name and all(x not in ("",".","..") for x in name.split("/")),"Unsafe path")
    return p
def child(root,name):
    p=root
    for part in safe(name).parts:
        p=p/part;need(not p.is_symlink(),"Input path symlink")
    return p
def verify(root,inputs,manifest_pin,checker_pin):
    pin(manifest_pin);pin(checker_pin)
    need(root.is_dir() and not root.is_symlink(),"Bad packet root")
    need(inputs.is_dir() and not inputs.is_symlink(),"Bad input root")
    need(sha(regular(root/"verify_custody.py"))==checker_pin,"External checker pin mismatch")
    raw=regular(root/"MANIFEST.json");need(sha(raw)==manifest_pin,"External manifest mismatch")
    manifest=parse(raw)
    need(manifest["schema"]=="pr786-whole-preprint-review01/v1" and manifest["head"]==HEAD,"Wrong target")
    need(manifest["explicit_exceptions"]==["MANIFEST.json"],"Exceptions differ")
    files=manifest["files"]
    need(set(p.name for p in root.iterdir())==set(files)|{"MANIFEST.json"},"Packet flat closure differs")
    for name,row in files.items():
        need(len(safe(name).parts)==1 and name!="MANIFEST.json","Bad flat member")
        need(ident(regular(root/name))==row,"Authored file differs:"+name)
    bound=parse(regular(root/"INPUTS.json"))
    got={}
    for name,row in bound["files"].items():
        b=regular(child(inputs,name));need(ident(b)==row,"Frozen input differs:"+name);got[name]=b
    need(len(got)==9 and sha(got["REVIEW_INPUTS.json"])==INPUT_PIN,"Frozen input pin differs")
    receipt=parse(got["REVIEW_INPUTS.json"])
    need(receipt["reviewed_head"]==HEAD and receipt["source_manifest_sha256"]==SOURCE_PIN,"Input target")
    need(len(receipt["files"])==8,"Eight reviewed files required")
    for row in receipt["files"]:
        need(ident(got[row["path"]])=={k:row[k] for k in ("bytes","sha256")},"Input inventory differs")
    with zipfile.ZipFile(io.BytesIO(got["source-and-verification.zip"])) as z:
        names=z.namelist();need(len(names)==213 and len(set(names))==213,"Source ZIP closure")
        for item in z.infolist():
            safe(item.filename);need(stat.S_ISREG(item.external_attr>>16),"Nonregular source ZIP member")
        source={name:z.read(name) for name in names}
    need(sha(source["MANIFEST.json"])==SOURCE_PIN,"External source pin differs")
    sm=parse(source["MANIFEST.json"]);rows=sm["files"];expected={}
    for row in rows:
        name=row["path"];safe(name);need(name!="MANIFEST.json" and name not in expected,"Repeated source entry")
        expected[name]={k:row[k] for k in ("bytes","sha256")}
    need(set(source)==set(expected)|{"MANIFEST.json"},"Closed source differs")
    for name,row in expected.items():need(ident(source[name])==row,"Source bytes differ:"+name)
    sel=source["audit/intake/SELECTED_PUBLIC_RECORD.json"]
    need(sha(sel)==bound["selected_record_sha256"],"Selected record differs")
    selected=parse(sel)
    identity=parse(source["audit/intake/ROOT_SOURCE_IDENTITY.json"])
    need(identity["reviewed_head"]==HEAD and len(identity["original_files"])==41,"Original scope differs")
    need(sha(json.dumps([selected["problem"],selected["prior_research"]],sort_keys=True).encode())==identity["review_hash"],"Complete record differs")
    originals=set()
    for row in identity["original_files"]:
        name="audit/intake/original/"+row["path"];originals.add(name);b=source[name]
        need(ident(b)=={k:row[k] for k in ("bytes","sha256")},"Original bytes differ")
        need(hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==row["git_blob"],"Original Git identity")
    need(len(originals)==41 and {n for n in source if n.startswith("audit/intake/original/")}==originals,"Original41 closure")
    init=parse(regular(root/"INITIAL_POSITION.json"))
    need(init["inputs"]["paper.tex"]==sha(got["paper.tex"]),"Initial paper binding differs")
    v=parse(regular(root/"VERDICT.json"))
    need(v["actionable_issue_count"]==0 and v["verdict"]=="PASS_ZERO_ACTIONABLE_ISSUES","Verdict differs")
    return {"result":"PASS","artifact_files":len(files),"frozen_input_files":9,"source_files":213,
            "original_files":41,"source_manifest_sha256":SOURCE_PIN,"optimized":bool(sys.flags.optimize)}
def main():
    a=argparse.ArgumentParser();a.add_argument("--root",type=Path,default=Path(__file__).absolute().parent)
    a.add_argument("--input-root",required=True,type=Path)
    a.add_argument("--expected-manifest-sha256",required=True);a.add_argument("--expected-checker-sha256",required=True)
    x=a.parse_args()
    try:v=verify(x.root.absolute(),x.input_root.absolute(),x.expected_manifest_sha256,x.expected_checker_sha256)
    except Exception as e:print(json.dumps({"result":"FAIL","error":str(e)}));return 1
    print(json.dumps(v,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
