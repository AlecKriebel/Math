#!/usr/bin/env python3
"""Externally pinned custody and optional independent diagnostic replay."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,"duplicate JSON key")
        out[key]=value
    return out


def strict(data):
    def bad(value):
        raise ValueError("nonfinite JSON "+value)
    return json.loads(data,object_pairs_hook=unique,parse_constant=bad)


def ancestry(path, last_directory=True):
    for entry in [path,*path.parents]:
        mode=entry.lstat().st_mode
        if entry==path and not last_directory:
            need(stat.S_ISREG(mode) and entry.lstat().st_nlink==1,"nonregular or linked file")
        else:
            need(stat.S_ISDIR(mode),"nonregular directory ancestry")


def safe_relative(value):
    need(type(value) is str and bool(value),"empty path")
    p=PurePosixPath(value)
    need(not p.is_absolute() and not any(part in ("..",".") for part in p.parts)
         and str(p)==value and "\\" not in value,"unsafe relative path")
    return p


def inventory(root):
    ancestry(root)
    files={}
    directories=set()
    for current,ds,fs in os.walk(root,followlinks=False):
        for name in ds+fs:
            p=Path(current)/name
            relative=p.relative_to(root).as_posix()
            mode=p.lstat().st_mode
            if stat.S_ISDIR(mode): directories.add(relative)
            else:
                need(stat.S_ISREG(mode) and p.lstat().st_nlink==1,"nonregular or linked packet entry")
                files[relative]=p
    return files,directories


def check_bytes(path,entry):
    ancestry(path,last_directory=False)
    data=path.read_bytes()
    need((len(data),sha(data))==(entry["bytes"],entry["sha256"]),"content mismatch: "+str(path))
    if "git_blob" in entry:
        blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        need(blob==entry["git_blob"],"Git blob mismatch")
    return data


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--packet",required=True)
    parser.add_argument("--intake-root",required=True)
    parser.add_argument("--expected-manifest-sha256",required=True)
    parser.add_argument("--expected-checker-sha256",required=True)
    parser.add_argument("--primary-root")
    parser.add_argument("--replay",action="store_true")
    args=parser.parse_args()
    invocation=Path(__file__).absolute()
    ancestry(invocation,last_directory=False)
    root=Path(args.packet).absolute()
    need(invocation.parent==root,"checker is not in requested packet")
    files,directories=inventory(root)
    need(sha(invocation.read_bytes())==args.expected_checker_sha256,"checker pin mismatch")
    raw=files["MANIFEST.json"].read_bytes()
    need(sha(raw)==args.expected_manifest_sha256,"manifest pin mismatch")
    manifest=strict(raw)
    need(set(manifest)=={"schema","files"} and manifest["schema"]=="pr789-quotient-algebra-v1","manifest schema")
    expected={}
    for entry in manifest["files"]:
        need(set(entry)=={"path","bytes","sha256"} and type(entry["bytes"]) is int and entry["bytes"]>=0,"manifest entry")
        name=str(safe_relative(entry["path"]))
        need(name not in expected,"duplicate manifest path")
        expected[name]=entry
    need(set(files)==set(expected)|{"MANIFEST.json"},"closed packet file inventory")
    want_dirs={str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent)!="."}
    need(directories==want_dirs,"closed packet directory inventory")
    for name,entry in expected.items(): check_bytes(files[name],entry)
    intake=Path(args.intake_root).absolute()
    ancestry(intake)
    binding=strict(files["SOURCE_BINDINGS.json"].read_bytes())
    need(binding["reviewed_head"]=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","candidate identity")
    seen=set()
    for entry in binding["inputs"]:
        name=str(safe_relative(entry["path"]))
        need(name not in seen,"duplicate input binding")
        seen.add(name)
        check_bytes(intake/name,entry)
    original=intake/"original/unsolved_math_prioritization/attempts/30001478"
    original_files,_=inventory(original)
    original_names={name.removeprefix("original/unsolved_math_prioritization/attempts/30001478/")
                    for name in seen if name.startswith("original/unsolved_math_prioritization/attempts/30001478/")}
    need(len(original_names)==58 and set(original_files)==original_names,"closed original source inventory")
    selected=strict((intake/"SELECTED_PUBLIC_RECORD.json").read_bytes())
    gate=strict((intake/"ELIGIBILITY_GATE.json").read_bytes())
    catalog=strict((intake/"CATALOG_ENTRY.json").read_bytes())
    identity=strict((intake/"ROOT_SOURCE_IDENTITY.json").read_bytes())
    need(sha(selected["problem"]["statement"].encode())==catalog["statement_hash"]==identity["statement_sha256"]=="628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6","statement identity")
    need(sha(json.dumps([selected["problem"],selected["prior_research"]],sort_keys=True).encode())==catalog["review_hash"]==identity["review_hash"]=="cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f","complete review identity")
    need(gate["queue_status"]=="claimed_solved" and gate["pr_metadata"]["headRefOid"]==binding["reviewed_head"],"eligibility identity")
    primary_count=0
    if args.primary_root:
        primary=Path(args.primary_root).absolute()
        ancestry(primary)
        for entry in strict(files["PRIMARY_SOURCES.json"].read_bytes())["files"]:
            check_bytes(primary/str(safe_relative(entry["path"])),entry)
            primary_count+=1
    replayed=False
    if args.replay:
        proc=subprocess.run([sys.executable,"-I","-B"]+(["-O"] if sys.flags.optimize else [])+
            [str(files["check_algebra.py"])],cwd=root.parent,capture_output=True,text=True,timeout=120)
        need(proc.returncode==0,"independent algebra replay: "+proc.stderr)
        need(strict(proc.stdout)==strict(files["ALGEBRA_RESULTS.json"].read_bytes()),"saved independent result mismatch")
        replayed=True
    print(json.dumps({"status":"PASS","packet_files":len(files),"bound_inputs":len(seen),
        "original_files":58,"primary_files_rehashed":primary_count,"independent_algebra_replayed":replayed,
        "mathematical_verdict":"PASS_NO_REQUIRED_REPAIRS","priority":"NOT_AUDITED"},sort_keys=True,indent=2))


if __name__=="__main__":
    try: main()
    except Exception as error:
        print("REJECT: "+str(error),file=sys.stderr)
        sys.exit(1)
