"""Private visual reading inputs from the supplied PDF; no re-publication."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

base = Path(__file__).resolve().parent
cache = base / "private_inputs"
pdf = Path("/Users/alec/Downloads/Some-New-Results-on-Geometric-Transversals.pdf")
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
        full_mode_07777=format(stat.S_IMODE(p.stat().st_mode),"04o"))
source = pin(pdf)
assert source["sha256"] == "478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc"
caps = []
for page in [5,11,15,17,20,21,24,25,28]:
    prefix = cache / ("visual_page_%02d" % page)
    argv = ["/opt/homebrew/bin/pdftoppm","-f",str(page),"-l",str(page),
            "-r","120","-png","-singlefile",str(pdf),str(prefix)]
    pre = dict(controller_pid=os.getpid(), utc=datetime.now(timezone.utc).isoformat(),
        argv=argv, source_pdf=source, operator_source=pin(Path(__file__)),
        executable=pin(Path(argv[0])))
    (cache / (prefix.name+".PRELAUNCH.json")).write_text(json.dumps(pre,indent=2,sort_keys=True)+"\n")
    (cache / (prefix.name+".PRELAUNCH_SOURCE.py")).write_bytes(Path(__file__).read_bytes())
    out, err = Path(str(prefix)+".stdout.bin"), Path(str(prefix)+".stderr.bin")
    with out.open("wb") as stdout, err.open("wb") as stderr:
        child = subprocess.Popen(argv, stdout=stdout, stderr=stderr)
        code = child.wait()
    cap = dict(prelaunch=pre, child_pid=child.pid, exit_code=code,
        end_utc=datetime.now(timezone.utc).isoformat(), stdout=pin(out), stderr=pin(err),
        image=pin(Path(str(prefix)+".png")) if code==0 else None)
    (cache / (prefix.name+".CAPTURE.json")).write_text(json.dumps(cap,indent=2,sort_keys=True)+"\n")
    caps.append(cap)
    if code:
        raise SystemExit(code)
assert pin(pdf) == source
(base / "RENDER_RECEIPT.json").write_text(json.dumps(dict(schema="pr18-selected-page-render/v1",
    controller_pid=os.getpid(), source=source, captures=caps,
    rendered_pages=[5,11,15,17,20,21,24,25,28],
    rendering_is_not_personal_inspection=True, private_not_redistributed=True),
    indent=2,sort_keys=True)+"\n")
print(json.dumps(dict(controller_pid=os.getpid(), children=[c["child_pid"] for c in caps],
    all_exit0=all(c["exit_code"]==0 for c in caps),
    all_stderr0=all(c["stderr"]["bytes"]==0 for c in caps), source=source),indent=2,sort_keys=True))
