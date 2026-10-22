#!/usr/bin/env python3
"""Authenticate the exact author freeze and replay finite checks in isolation."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    "archive": (14759,"0f9410f5d63e3d6985d9c34096c16a3eecf7f306e6281bcea49b3e806481c9d6"),
    "manifest": (1942,"b1e084a80ccd3f8192684c0155b3cd5176943b000dbc56e5e46d95e6a034d484"),
    "receipt": (5223,"d22e09f027f94256657575d48b52198f612e8fcb776e9f962f81c49ca527b4e7"),
}


def require(ok, text):
    if not ok:
        raise ValueError(text)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    out = {}
    for key,value in pairs:
        require(key not in out,"duplicate JSON key")
        out[key] = value
    return out


def parsed(data):
    return json.loads(data,object_pairs_hook=unique)


def pin(data, name):
    size,sha = PINS[name]
    require(len(data)==size and digest(data)==sha,"untrusted "+name)


def run(script, mode, cwd, args=()):
    result = subprocess.run([sys.executable,*mode,str(script),*args],cwd=cwd,
        capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive",type=Path,required=True)
    parser.add_argument("--manifest",type=Path,required=True)
    parser.add_argument("--receipt",type=Path,required=True)
    args=parser.parse_args()
    inputs = {}
    for name in PINS:
        p=getattr(args,name)
        require(p.is_file() and not p.is_symlink(),"input must be regular file: "+name)
        inputs[name]=p.read_bytes()
        pin(inputs[name],name)
    outer=parsed(inputs["manifest"])
    receipt=parsed(inputs["receipt"])
    require(receipt["checks"]==139 and receipt["count"]==30,"author receipt scope changed")
    require(outer["archive"]["sha256"]==PINS["archive"][1],"archive pin disagreement")
    expected=outer["files"]
    checks=[]
    bootstrap=[]
    for name,data in inputs.items():
        try:
            pin(data[:-1]+bytes([data[-1]^1]),name)
        except ValueError:
            bootstrap.append({"test":"mutated "+name,"result":"REJECTED_AS_EXPECTED"})
        else:
            raise ValueError("bootstrap accepted mutated "+name)
    with tempfile.TemporaryDirectory(prefix="minimal foliation replay ") as tmp:
        root=Path(tmp)
        package=root/"relocated author"
        package.mkdir()
        elsewhere=root/"unrelated working directory"
        elsewhere.mkdir()
        with zipfile.ZipFile(args.archive) as z:
            names=z.namelist()
            require(len(names)==len(set(names))==len(expected)==10,"ZIP member multiplicity")
            require(set(names)==set(expected),"ZIP member allowlist")
            for info in z.infolist():
                path=PurePosixPath(info.filename)
                require(len(path.parts)==1 and path.name==info.filename,"unsafe ZIP path")
                mode=info.external_attr>>16
                require(not info.is_dir() and not stat.S_ISLNK(mode),"nonregular ZIP entry")
                require(info.file_size==expected[info.filename]["bytes"],"ZIP entry size")
                data=z.read(info)
                require(digest(data)==expected[info.filename]["sha256"],"ZIP entry digest")
                (package/info.filename).write_bytes(data)
        expected_calculation=(package/"calculation_results.json").read_bytes()
        expected_integrity=b'{"files": 9, "result": "PASS_LOCAL_MANIFEST_INTEGRITY"}\n'
        def record(test,mode,r,expect_ok,expected_stdout=None,diagnostic=None):
            require((r.returncode==0)==expect_ok,"unexpected exit: "+test)
            if expected_stdout is not None:
                require(r.stdout==expected_stdout,"output differs: "+test)
            if diagnostic is not None:
                require(diagnostic.encode() in r.stderr,"wrong failure diagnostic: "+test)
            checks.append({"test":test,"mode":" ".join(mode) or "default",
                "exit_code":r.returncode,"result":"PASS" if expect_ok else "REJECTED_AS_EXPECTED",
                "stdout_sha256":digest(r.stdout),"stderr":r.stderr.decode().strip()})
        for mode in ([],["-O"],["-OO"]):
            record("author calculations",mode,run(package/"check_calculations.py",mode,elsewhere),True,expected_calculation)
            record("author integrity",mode,run(package/"verify_release.py",mode,elsewhere),True,expected_integrity)
            record("author calculation negative control",mode,run(package/"check_calculations.py",mode,elsewhere,["--negative-control"]),False,diagnostic="intentional negative control")
            mutations = ["proof-byte","missing-file","extra-file","symlink","bad-json","duplicate-key","boolean-version",
                "same-size-proof-byte","extra-directory","float-byte-count","boolean-byte-count","missing-manifest-entry",
                "extra-manifest-key","duplicate-nested-key","wrong-hash","unexpected-argument"]
            for mutation in mutations:
                d=root/("mutation "+mutation)
                shutil.copytree(package,d)
                mp=d/"MANIFEST.json"
                m=parsed(mp.read_bytes())
                extra_args=[]
                if mutation=="proof-byte": (d/"PROOF.md").write_bytes((d/"PROOF.md").read_bytes()+b" ")
                elif mutation=="same-size-proof-byte":
                    p=d/"PROOF.md"; data=p.read_bytes(); p.write_bytes(bytes([data[0]^1])+data[1:])
                elif mutation=="missing-file": (d/"PROOF.md").unlink()
                elif mutation=="extra-file": (d/"UNLISTED").write_text("unexpected")
                elif mutation=="extra-directory": (d/"UNLISTED").mkdir()
                elif mutation=="symlink":
                    (d/"PROOF.md").unlink(); (d/"PROOF.md").symlink_to(package/"PROOF.md")
                elif mutation=="bad-json": mp.write_text("{")
                elif mutation=="duplicate-key": mp.write_text('{"format_version":1,"format_version":1,"files":{}}')
                elif mutation=="duplicate-nested-key":
                    t=mp.read_text(); old='"bytes": 1710'; require(old in t,"nested mutation anchor"); mp.write_text(t.replace(old,old+', "bytes": 1710',1))
                elif mutation=="boolean-version": m["format_version"]=True
                elif mutation=="float-byte-count": m["files"]["PROOF.md"]["bytes"]=float(m["files"]["PROOF.md"]["bytes"])
                elif mutation=="boolean-byte-count": m["files"]["PROOF.md"]["bytes"]=True
                elif mutation=="missing-manifest-entry": del m["files"]["PROOF.md"]
                elif mutation=="extra-manifest-key": m["unlisted"]=1
                elif mutation=="wrong-hash": m["files"]["PROOF.md"]["sha256"]="0"*64
                elif mutation=="unexpected-argument": extra_args=["unexpected"]
                if mutation in ["boolean-version","float-byte-count","boolean-byte-count","missing-manifest-entry","extra-manifest-key","wrong-hash"]:
                    mp.write_text(json.dumps(m))
                record(mutation,mode,run(d/"verify_release.py",mode,elsewhere,extra_args),False,diagnostic="FAIL:")
                shutil.rmtree(d)
            independent=Path(__file__).resolve().with_name("independent_calculations.py")
            result=run(independent,mode,elsewhere)
            expected_independent=independent.with_name("independent_calculations.json").read_bytes()
            record("independent calculations",mode,result,True,expected_independent)
            record("independent negative control",mode,run(independent,mode,elsewhere,["--negative-control"]),False,diagnostic="intentional independent negative control")
        # None of the tests may have modified a trusted input or baseline member.
        for name,data in inputs.items():
            require(getattr(args,name).read_bytes()==data,"original input changed")
        for name,item in expected.items():
            require(digest((package/name).read_bytes())==item["sha256"],"baseline altered")
    print(json.dumps({"result":"PASS_INDEPENDENT_REPLAY","author_checks_per_mode":139,
        "replay_cases":len(checks),"bootstrap_negative_controls":bootstrap,"checks":checks,
        "relocated":True,"working_directory_independent":True,"original_inputs_unchanged":True,
        "finite_computation_only":True,"mathematical_proof_certified_by_computation":False},indent=2,sort_keys=True))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: "+str(exc),file=sys.stderr)
        sys.exit(1)
