#!/usr/bin/env python3
"""Execute actual argv and preserve binary output plus process receipt."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def meta(path):
    content = path.read_bytes()
    return {"path":str(path),"bytes":len(content),"sha256":hashlib.sha256(content).hexdigest(),
            "lines":content.count(b"\n")}


def run(name, argv, cwd=None):
    destination = ROOT / "actual_runs" / name
    destination.mkdir(parents=True,exist_ok=False)
    started = utc()
    working = str(cwd or ROOT)
    with (destination/"stdout.bin").open("wb") as stdout, (destination/"stderr.bin").open("wb") as stderr:
        process = subprocess.Popen(argv,cwd=working,stdout=stdout,stderr=stderr)
        receipt = {"name":name,"argv":argv,"cwd":working,"pid":process.pid,
                   "started_utc":started,"recorder_pid":__import__("os").getpid()}
        (destination/"started.json").write_text(json.dumps(receipt,indent=2)+"\n")
        code = process.wait()
    receipt.update({"completed_utc":utc(),"exit_code":code,
                    "stdout":meta(destination/"stdout.bin"),"stderr":meta(destination/"stderr.bin")})
    (destination/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,sort_keys=True))
    return receipt


if __name__ == "__main__":
    run(sys.argv[1],sys.argv[2:])
