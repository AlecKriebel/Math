#!/usr/bin/env python3
"""Offline controls, mutations limited to allocated disposable scratch copies."""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, datetime

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def reseal(packet):
    rows = [{"path":p.name,"bytes":p.stat().st_size,"sha256":sha(p)} for p in sorted(packet.iterdir()) if p.name != "MANIFEST.json"]
    (packet/"MANIFEST.json").write_text(json.dumps({"schema":"pr788-priority-question-authored-v1","files":rows},indent=2)+"\n")
    return sha(packet/"MANIFEST.json")

def run(args, optimize, packet, intake, manifest_pin, checker_pin, bodies=None):
    cmd = [sys.executable,"-B"] + (["-O"] if optimize else []) + [str(pathlib.Path(args.packet_root)/"verify_packet.py"),"--packet-root",str(packet),"--intake-root",str(intake),"--manifest-sha256",manifest_pin,"--checker-sha256",checker_pin]
    if bodies:
        cmd += ["--bodies-root",str(bodies)]
    done = subprocess.run(cmd,text=True,capture_output=True,timeout=8)
    return {"exit_code":done.returncode,"stdout":done.stdout.strip(),"stderr":done.stderr.strip()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet-root",required=True)
    ap.add_argument("--intake-root",required=True)
    ap.add_argument("--bodies-root",required=True)
    ap.add_argument("--scratch-root",required=True)
    ap.add_argument("--output",required=True)
    args = ap.parse_args()
    packet = pathlib.Path(args.packet_root)
    intake = pathlib.Path(args.intake_root)
    scratch = pathlib.Path(args.scratch_root)
    scratch.mkdir(parents=True,exist_ok=True)
    pin, cp = sha(packet/"MANIFEST.json"), sha(packet/"verify_packet.py")
    cases = [
        ("wrong_manifest_pin","manifest pin mismatch"),
        ("wrong_checker_pin","checker pin mismatch"),
        ("changed_report","payload mismatch"),
        ("unexpected_member","packet membership mismatch"),
        ("fifo_manifest","not a regular file"),
        ("fifo_helper","not a regular file"),
        ("symlink_payload",None),
        ("root_ancestor_symlink",None),
        ("input_fifo","not a regular file"),
        ("missing_original",None),
        ("external_pdf_fifo","not a regular file"),
        ("resealed_priority_inflation","scope inflation: source ledger"),
    ]
    rows = []
    for optimize in (False,True):
        before = run(args,optimize,packet,intake,pin,cp,pathlib.Path(args.bodies_root))
        if before["exit_code"] != 0:
            raise RuntimeError("positive baseline failed "+str(before))
        rows.append({"case":"positive_full_body_baseline","optimization":int(optimize),"expected_accept":True,"passed":True,"result":before})
        for name, marker in cases:
            with tempfile.TemporaryDirectory(prefix="priority-control-",dir=scratch) as folder:
                c = pathlib.Path(folder)
                p = c/"packet"
                shutil.copytree(packet,p)
                i = intake
                mp, cpin, bodies = pin, cp, None
                if name in ("input_fifo","missing_original"):
                    i = c/"intake"
                    shutil.copytree(intake,i)
                if name == "wrong_manifest_pin":
                    mp = "0"*64
                elif name == "wrong_checker_pin":
                    cpin = "0"*64
                elif name == "changed_report":
                    (p/"REPORT.md").write_bytes((p/"REPORT.md").read_bytes()+b"\nchanged\n")
                elif name == "unexpected_member":
                    (p/"UNEXPECTED.md").write_text("not reviewed\n")
                elif name in ("fifo_manifest","fifo_helper"):
                    f = p/("MANIFEST.json" if name == "fifo_manifest" else "verify_packet.py")
                    f.unlink()
                    os.mkfifo(f)
                elif name == "symlink_payload":
                    f = p/"REPORT.md"
                    f.unlink()
                    f.symlink_to(packet/"REPORT.md")
                elif name == "root_ancestor_symlink":
                    a = c/"alias"
                    a.symlink_to(c,target_is_directory=True)
                    p = a/"packet"
                elif name == "input_fifo":
                    f = i/"SELECTED_PUBLIC_RECORD.json"
                    f.unlink()
                    os.mkfifo(f)
                elif name == "missing_original":
                    original = next(r["path"] for r in json.loads((packet/"INPUT_BINDINGS.json").read_text())["files"] if r["path"].startswith("original/"))
                    (i/original).unlink()
                elif name == "external_pdf_fifo":
                    bodies = c/"bodies"
                    bodies.mkdir()
                    first = json.loads((packet/"SOURCE_LEDGER.json").read_text())["sources"][0]["pdf_file"]
                    os.mkfifo(bodies/first)
                elif name == "resealed_priority_inflation":
                    f = p/"SOURCE_LEDGER.json"
                    obj = json.loads(f.read_text())
                    obj["full_matching_prior_verified"] = True
                    f.write_text(json.dumps(obj,indent=2)+"\n")
                    mp = reseal(p)
                result = run(args,optimize,p,i,mp,cpin,bodies)
                passed = result["exit_code"] == 2 and result["stderr"].startswith("FAIL:") and (marker is None or marker in result["stderr"])
                rows.append({"case":name,"optimization":int(optimize),"expected_accept":False,"passed":passed,"result":result})
                if not passed:
                    raise RuntimeError("negative control failed "+json.dumps(rows[-1]))
        after = run(args,optimize,packet,intake,pin,cp)
        if after["exit_code"] != 0:
            raise RuntimeError("post-control baseline failed "+str(after))
        rows.append({"case":"post_control_core_baseline","optimization":int(optimize),"expected_accept":True,"passed":True,"result":after})
    result = {"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"python":sys.version,"result":"PASS","negative_cases_per_mode":len(cases),"rows":rows,"tested_manifest_sha256":pin,"tested_checker_sha256":cp,"scope":"Provisional sealed baseline plus bounded local negatives. No external API calls, no original/other worker mutations. This output is added before final reseal; final baseline receipt remains outside self-bound packet."}
    pathlib.Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"result":"PASS","negative_cases_per_mode":len(cases),"modes":2,"subprocess_rows":len(rows)}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
