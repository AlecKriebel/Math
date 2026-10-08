#!/usr/bin/env python3
"""Replay pinned author inputs on disposable read-only copies, as UID 1000."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

AUTHOR_MANIFEST_SHA256="b744942d6086721c08ab2508a87b71e6c0d553486964b898e6cb9e1a81d10662"
AUTHOR_ARCHIVE_SHA256="beabecc7f40e4a064740fc457c5a2f1c735695c63a255021d8f35decae74d342"


def need(x,message):
    if not x:
        raise ValueError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix():{"bytes":p.stat().st_size,"sha256":digest(p.read_bytes())}
            for p in root.rglob("*") if p.is_file()}


def seal(root):
    for p in root.rglob("*"):
        if p.is_symlink():
            continue
        p.chmod(0o555 if p.is_dir() else 0o444)
    root.chmod(0o555)


def unseal(root):
    root.chmod(0o755)
    for p in root.rglob("*"):
        if p.is_dir() and not p.is_symlink():
            p.chmod(0o755)


def run(script,opt,cwd,args=()):
    cmd=[sys.executable,"-B"]+([opt] if opt else [])+[str(script)]+list(args)
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=120)
    return {"mode":opt or "normal","exit_code":r.returncode,
            "stdout_sha256":digest(r.stdout.encode()),"stderr":r.stderr.strip()},r.stdout


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--author-root",type=Path,required=True)
    args=p.parse_args()
    root=args.author_root.resolve(); packet=root/"packet"
    manifest=root/"FREEZE_MANIFEST.json"; archive=root/"source_free_packet.tar.gz"
    need(os.getuid()==1000 and os.geteuid()==1000,"Must actually run as UID and EUID 1000")
    need(digest(manifest.read_bytes())==AUTHOR_MANIFEST_SHA256,"Author manifest pin mismatch")
    need(archive.stat().st_size==16496 and digest(archive.read_bytes())==AUTHOR_ARCHIVE_SHA256,
         "Author archive pin mismatch")
    expected=json.loads(manifest.read_text())["packet_files"]
    before=snapshot(packet)
    need(before==expected,"Author directory differs from pinned manifest")
    author_code=(packet/"verify.py").read_text()
    need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(author_code))),
         "Optimization-sensitive assert found")
    evidence={"schema":"lefschetz-2974-independent-replay-v1","uid":os.getuid(),"euid":os.geteuid(),
              "author_manifest_sha256":AUTHOR_MANIFEST_SHA256,"author_archive_sha256":AUTHOR_ARCHIVE_SHA256,
              "author_archive_bytes":16496,"author_assert_nodes":0,
              "positive":[],"integrity_mutations":[],"arithmetic_mutations":[],"cli_controls":[]}
    with tempfile.TemporaryDirectory(prefix="lefschetz2974-independent-") as td:
        td=Path(td); cwd=td/"readonly-cwd"; cwd.mkdir(); cwd.chmod(0o555)
        q=td/"archive-replay"; q.mkdir()
        with tarfile.open(archive,"r:gz") as tar:
            members=tar.getmembers()
            need(len(members)==len(expected),"Archive member count differs")
            need({m.name for m in members}=={"packet/"+name for name in expected},"Archive inventory differs")
            for member in members:
                need(member.isfile() and not member.issym() and not member.islnk(),"Nonregular archive member")
                data=tar.extractfile(member).read()
                item=expected[member.name.removeprefix("packet/")]
                need(len(data)==item["bytes"] and digest(data)==item["sha256"],"Archive bytes differ")
                path=q/member.name.removeprefix("packet/"); path.write_bytes(data)
        seal(q)
        probes=[]
        for target,mode in ((cwd/"forbidden-new-file","xb"),(q/"forbidden-new-file","xb"),(q/"REPORT.md","ab")):
            try:
                with target.open(mode):
                    pass
            except PermissionError:
                probes.append(True)
            else:
                probes.append(False)
        need(all(probes),"Read-only permission probe unexpectedly allowed a write")
        evidence["readonly_write_probes_denied"]=len(probes)
        pins=["--manifest",str(manifest),"--manifest-sha256",AUTHOR_MANIFEST_SHA256]
        initial=snapshot(q)
        for opt in ("","-O","-OO"):
            row,out=run(q/"verify.py",opt,cwd,pins)
            need(row["exit_code"]==0,"Author read-only replay failed: "+row["stderr"])
            result=json.loads(out)
            need(result.pop("integrity")["verified"],"Integrity verification missing")
            need(result==json.loads((q/"CHECK_RESULTS.json").read_text()),"Recorded author results differ from replay")
            evidence["positive"].append(row)
        need(snapshot(q)==initial,"Author replay wrote into sealed packet")
        evidence["archive_replay_exact_inventory"]=True
        evidence["recorded_author_results_match_replay"]=True
        cases=("same_length_report","missing_file","extra_file","symlink","fifo","directory_instead_of_file",
               "bad_pin","changed_manifest","invalid_json_pinned","wrong_schema_pinned","wrong_byte_count_pinned")
        for name in cases:
            c=td/name; shutil.copytree(packet,c)
            mp=manifest; pin=AUTHOR_MANIFEST_SHA256
            if name=="same_length_report":
                f=c/"REPORT.md"; data=f.read_bytes(); f.write_bytes(data.replace(b"universal",b"univErsal",1))
            elif name=="missing_file":
                (c/"STATUS.json").unlink()
            elif name=="extra_file":
                (c/"unlisted.txt").write_text("extra")
            elif name=="symlink":
                (c/"unlisted-link").symlink_to(c/"REPORT.md")
            elif name=="fifo":
                os.mkfifo(c/"unlisted-fifo")
            elif name=="directory_instead_of_file":
                (c/"STATUS.json").unlink(); (c/"STATUS.json").mkdir()
            elif name=="bad_pin":
                pin="0"*64
            else:
                mp=td/(name+".json")
                if name=="changed_manifest":
                    mp.write_bytes(manifest.read_bytes()+b"\n")
                elif name=="invalid_json_pinned":
                    mp.write_text("{"); pin=digest(mp.read_bytes())
                else:
                    data=json.loads(manifest.read_text())
                    if name=="wrong_schema_pinned":
                        data["schema"]="invalid"
                    else:
                        data["packet_files"]["REPORT.md"]["bytes"]+=1
                    mp.write_text(json.dumps(data)); pin=digest(mp.read_bytes())
            seal(c)
            for opt in ("","-O","-OO"):
                row,_=run(c/"verify.py",opt,cwd,["--manifest",str(mp),"--manifest-sha256",pin])
                need(row["exit_code"]!=0,"Integrity mutation accepted: "+name)
                row["mutation"]=name; evidence["integrity_mutations"].append(row)
            unseal(c)
        mutations=[
            ("wrong_genus","a*b+1, 2*a*b, 6*a*b","a*b+2, 2*a*b, 6*a*b",False),
            ("wrong_polarization","((0,4,0,0),(-4,0,0,0)","((0,5,0,0),(-5,0,0,0)",False),
            ("omit_n_dependence","((2*n*a)%p,b,0)","((0*n*a)%p,b,0)",False),
            ("omit_initial_lattice","((2*n*a)%p,b,0)","((2*n*a)%p,0,0)",False),
            ("wrong_content","(0,6*n)","(0,7*n)",False),
            ("wrong_blowup_signature","e+b,sigma-b","e+b,sigma+b",False),
            ("wrong_base_change_coefficient","d*ey+4*(d-1)*(h-1)","d*ey+3*(d-1)*(h-1)",False),
            ("odd_prime_factor_two_blind_spot","((2*n*a)%p,b,0)","((n*a)%p,b,0)",True),
        ]
        for name,old,new,accept in mutations:
            need(old in author_code,"Mutation target missing: "+name)
            c=td/(name+".py"); c.write_text(author_code.replace(old,new,1)); c.chmod(0o444)
            for opt in ("","-O","-OO"):
                row,_=run(c,opt,cwd)
                need((row["exit_code"]==0)==accept,"Arithmetic mutation outcome differs: "+name)
                row["mutation"]=name; row["expected_acceptance"]=accept
                evidence["arithmetic_mutations"].append(row)
        for flags in (["--manifest",str(manifest)],["--manifest-sha256",AUTHOR_MANIFEST_SHA256]):
            for opt in ("","-O","-OO"):
                row,_=run(q/"verify.py",opt,cwd,flags)
                need(row["exit_code"]!=0,"One-sided manifest flags accepted")
                row["flag"]=flags[0]; evidence["cli_controls"].append(row)
        # Test the independent checker from a separately sealed directory.
        iq=td/"independent"; iq.mkdir()
        shutil.copy2(Path(__file__).with_name("independent_checks.py"),iq/"independent_checks.py")
        seal(iq); evidence["independent_positive"]=[]
        for opt in ("","-O","-OO"):
            row,out=run(iq/"independent_checks.py",opt,cwd)
            need(row["exit_code"]==0,"Independent read-only check failed")
            need(json.loads(out)["deliberate_factor_two_error_rejected"],"Missing even-modulus negative control")
            evidence["independent_positive"].append(row)
        need(snapshot(q)==initial,"Packet changed after controls")
        unseal(q); unseal(iq); cwd.chmod(0o755)
    need(snapshot(packet)==before,"Original author packet changed")
    need(digest(manifest.read_bytes())==AUTHOR_MANIFEST_SHA256 and digest(archive.read_bytes())==AUTHOR_ARCHIVE_SHA256,
         "Original author freeze changed")
    evidence["author_freeze_preserved"]=True
    evidence["scope"]="Independent read-only replay, corruption controls and arithmetic guards; no geometric certification"
    print(json.dumps(evidence,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
