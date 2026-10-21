#!/usr/bin/env python3
"""Pinned closed packet checker; imports no candidate or peer code."""
import argparse,hashlib,json,os,stat,sys,subprocess
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
ROOT_SOURCE_SHA="92c0b6666f23bcab7624a7801d79247d8dc9a3d01333da8a300d2328da75db70"
HEAD="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
STATEMENT="628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6"
REVIEW="cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f"
def require(b,s):
    if not b:raise ValueError(s)
def digest(b):return hashlib.sha256(b).hexdigest()
def nofollow(p,isdir=False):
    p=Path(os.path.abspath(p))
    for a in reversed([p,*p.parents]):
        st=a.lstat();require(not stat.S_ISLNK(st.st_mode),"symlink")
    st=p.lstat()
    if isdir:require(stat.S_ISDIR(st.st_mode),"not directory")
    else:require(stat.S_ISREG(st.st_mode) and st.st_nlink==1,"not single-link regular file")
    return p
def safe(s):
    require(isinstance(s,str) and s and "\\" not in s,"invalid relative path")
    p=PurePosixPath(s);require(not p.is_absolute() and all(x not in ("",".","..") for x in p.parts) and str(p)==s,"unsafe relative path")
    return s
def load(b):
    def obj(pairs):
        d={}
        for k,v in pairs:
            require(k not in d,"duplicate JSON key");d[k]=v
        return d
    return json.loads(b,object_pairs_hook=obj,parse_constant=lambda s:(_ for _ in ()).throw(ValueError("nonfinite JSON")))
def read(p):return nofollow(p).read_bytes()
def inventory(root):
    result=set()
    def walk(d):
        for p in sorted(d.iterdir()):
            if p==root/"scratch":
                nofollow(p,True);continue
            st=p.lstat()
            if stat.S_ISDIR(st.st_mode):
                nofollow(p,True);require(any(p.iterdir()),"empty unexpected directory");walk(p)
            else:
                nofollow(p);result.add(p.relative_to(root).as_posix())
    walk(root);return result
def verify(args):
    nofollow(Path(__file__))
    root=nofollow(args.packet_root,True)
    require(digest(read(root/"verify_packet.py"))==args.expected_checker_sha256,"checker external pin")
    mb=read(root/"MANIFEST.json");require(digest(mb)==args.expected_manifest_sha256,"manifest external pin")
    mf=load(mb);require(set(mf)=={"format","files"} and mf["format"]=="pr789-source-geometry-v1","manifest format")
    expected={"MANIFEST.json"}
    for item in mf["files"]:
        require(set(item)=={"path","bytes","sha256"},"manifest row")
        rel=safe(item["path"]);require(rel not in expected,"duplicate file row");expected.add(rel)
        b=read(root/rel);require(len(b)==item["bytes"] and digest(b)==item["sha256"],"packet digest")
    require(inventory(root)==expected,"closed authored inventory")
    first=load(read(root/"INITIAL_POSITION_SHA256.json"))
    require(first["candidate_exposure"] is False and digest(read(root/"INITIAL_POSITION.md"))==first["sha256"],"independent first freeze")
    require(load(read(root/"VERDICT.json"))["result"]=="PASS","verdict")
    ib=load(read(root/"INPUT_BINDINGS.json"));require(ib["head"]==HEAD and ib["original_files"]==58,"target identity")
    checked_inputs=0
    if args.input_root:
        ir=nofollow(args.input_root,True);seen=set()
        for item in ib["records"]:
            rel=safe(item["path"]);require(rel not in seen,"duplicate input row");seen.add(rel)
            b=read(ir/rel);require(len(b)==item["bytes"] and digest(b)==item["sha256"],"input binding")
            if "git_blob" in item:require(hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==item["git_blob"],"Git blob")
            checked_inputs+=1
        identitybytes=read(ir/"ROOT_SOURCE_IDENTITY.json")
        require(digest(identitybytes)==ROOT_SOURCE_SHA,"externally supplied source identity")
        identity=load(identitybytes);require(identity["reviewed_head"]==HEAD,"original head")
        rec=load(read(ir/"SELECTED_PUBLIC_RECORD.json"))
        require(str(rec["problem"]["id"])=="30001478" and rec["prior_research"]=={},"selected problem")
        require(digest(rec["problem"]["statement"].encode())==STATEMENT,"statement")
        require(digest(json.dumps([rec["problem"],rec["prior_research"]],sort_keys=True).encode())==REVIEW,"review pair")
        gate=load(read(ir/"ELIGIBILITY_GATE.json"))
        require(gate["queue_status"]=="claimed_solved" and gate["pr_metadata"]["headRefOid"]==HEAD and gate["original_explicit_budget"]=="1/5","claimed-only eligibility")
        original=ir/"original/unsolved_math_prioritization/attempts/30001478"
        actual=set(); actual_dirs=set()
        for p in original.rglob("*"):
            if stat.S_ISDIR(p.lstat().st_mode):
                nofollow(p,True);actual_dirs.add(p.relative_to(ir).as_posix())
            else:
                nofollow(p);actual.add(p.relative_to(ir).as_posix())
        wanted={r["path"] for r in ib["records"] if r["path"].startswith("original/")}
        require(actual==wanted and len(actual)==58,"closed original source")
        wanted_dirs=set()
        for rel in wanted:
            for parent in PurePosixPath(rel).parents:
                ps=str(parent)
                if ps.startswith("original/unsolved_math_prioritization/attempts/30001478/"):wanted_dirs.add(ps)
        require(actual_dirs==wanted_dirs,"closed original directories")
        cert=load(read(original/"author/certificate.json"))
        # Compare against independent hard-coded official tensor without importing it.
        expected_tensor=load(read(root/"RELATION_TENSOR.json"))
        require([r["terms"] for r in cert["relations"]]==expected_tensor,"candidate source tensor")
    primary=0
    if args.source_root:
        sr=nofollow(args.source_root,True)
        for item in load(read(root/"PRIMARY_BINDINGS.json"))["records"]:
            b=read(sr/safe(item["path"]));require(len(b)==item["bytes"] and digest(b)==item["sha256"],"primary body binding");primary+=1
    replay=False
    if args.replay:
        cmd=[sys.executable,"-I","-B"]
        if sys.flags.optimize:cmd.append("-O")
        cp=subprocess.run(cmd+[str(root/"CHECKS.py")],check=True,capture_output=True,text=True,timeout=90)
        require(load(cp.stdout)==load(read(root/"CHECK_RESULTS.json")),"independent exact replay");replay=True
    return {"result":"PASS","authored_files":len(expected),"bound_inputs_checked":checked_inputs,"primary_files_checked":primary,
       "diagnostics_replayed":replay,"original_head":HEAD,"scope":"Authenticates this closed authored packet; optional exact originals and primary bytes. Does not execute candidate audit gates or certify priority."}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet-root",required=True);ap.add_argument("--expected-manifest-sha256",required=True);ap.add_argument("--expected-checker-sha256",required=True)
    ap.add_argument("--input-root");ap.add_argument("--source-root");ap.add_argument("--replay",action="store_true");args=ap.parse_args()
    try:out=verify(args)
    except Exception as e:
        print(json.dumps({"result":"FAIL","error":type(e).__name__+": "+str(e)}));return 1
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
