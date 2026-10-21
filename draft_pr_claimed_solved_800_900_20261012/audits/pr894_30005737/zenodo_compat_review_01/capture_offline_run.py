#!/usr/bin/env python3
"""Preserve actual subprocess metadata and both streams before interpreting tests."""
import datetime,hashlib,json,subprocess,sys,time
from pathlib import Path
out=Path(__file__).resolve().parent
label=sys.argv[1]
flags=sys.argv[2:]
argv=[sys.executable,"-B",*flags,str(out/"adversarial_probes.py"),"--result",str(out/("RESULTS_"+label+".json"))]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
tick=time.monotonic()
p=subprocess.Popen(argv,cwd=out.parents[3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
receipt={"argv":argv,"pid":p.pid,"started_utc":started,"cwd":str(out.parents[3]),"python_version":sys.version,"status":"RUNNING","probe_sha256":hashlib.sha256((out/"adversarial_probes.py").read_bytes()).hexdigest()}
place=out/("PROCESS_"+label+".json")
place.write_text(json.dumps(receipt,indent=2)+"\n")
stdout,stderr=p.communicate()
(out/("PROCESS_"+label+".stdout")).write_bytes(stdout)
(out/("PROCESS_"+label+".stderr")).write_bytes(stderr)
receipt.update(status="COMPLETED",returncode=p.returncode,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,stdout={"path":"PROCESS_"+label+".stdout","bytes":len(stdout),"sha256":hashlib.sha256(stdout).hexdigest()},stderr={"path":"PROCESS_"+label+".stderr","bytes":len(stderr),"sha256":hashlib.sha256(stderr).hexdigest()})
place.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
print(stdout.decode())
print(stderr.decode()[-2500:])
raise SystemExit(p.returncode)
