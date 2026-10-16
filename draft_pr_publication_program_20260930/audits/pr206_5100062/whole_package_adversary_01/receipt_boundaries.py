"""Actual CLI receipt failures; only fresh audit-owned fixtures."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parent / "publication_package_v1/verification/portable_exact_verifier.py"
PY = "/opt/homebrew/opt/python@3.14/bin/python3.14"


def main():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != "dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85":
        raise RuntimeError("source changed")
    out = OWN / "receipt_boundaries"
    out.mkdir(exist_ok=False)
    target = out / "sentinel.txt"
    target.write_text("unchanged audit sentinel\n")
    link = out / "temporary_fixture_link"
    link.symlink_to(target)
    directory = out / "existing_directory"
    directory.mkdir()
    attempts = []
    try:
        for opt in (False, True):
            for name, path, fault in [
                ("symlink",link,None), ("directory",directory,None),
                ("missing_parent",out / "missing_parent/receipt.json",None),
                ("fault_no_receipt",out / ("fault"+str(opt)+".json"),"wrong-area")]:
                argv = [PY,"-E","-S","-B","-P"]+(["-O"] if opt else [])+[str(SOURCE),"--receipt",str(path)]+(["--fault",fault] if fault else [])
                p = subprocess.run(argv,cwd=OWN,capture_output=True,text=True,timeout=60)
                item = {"name":name,"utc":datetime.now(timezone.utc).isoformat(),"argv":argv,"exit":p.returncode,"stdout":p.stdout,"stderr":p.stderr,"source_sha256":digest}
                attempts.append(item)
                if p.returncode != 1 or p.stderr or json.loads(p.stdout)["status"] != "FAIL":
                    raise RuntimeError("receipt failure did not reject cleanly")
                if target.read_text() != "unchanged audit sentinel\n":
                    raise RuntimeError("symlink target changed")
                if name == "fault_no_receipt" and path.exists():
                    raise RuntimeError("failure wrote receipt")
    finally:
        link.unlink(missing_ok=True)
        (out / "raw_attempts.json").write_text(json.dumps(attempts,indent=2)+"\n")
    print(json.dumps({"status":"PASS","attempts":len(attempts),"temporary_symlink_removed":True,"source_sha256":digest}))


if __name__ == "__main__":
    main()
