from pathlib import Path
import datetime,json,sys
from capture_v2 import capture,sha,dump
P=Path(__file__).resolve().parent.parent;N=P/"private_notes";F=P/"publicfiles"
r=capture("zenodo_local_check",[sys.executable,"-E","-B","/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py","check",str(P/"zenodo-deposit.json")],Path("/Users/alec/Documents/Math"),[P/"zenodo-deposit.json",F/"SHA256SUMS.txt"])
checks=json.loads((N/"processes/zenodo_local_check/stdout.bin").read_text())
if len(checks["files"])!=7:raise RuntimeError("deposit file count")
for e in checks["files"]:
 if sha(F/e["name"])!=e["sha256"]:raise RuntimeError("deposit hash")
inputs=json.loads((N/"INPUTS.json").read_text())
for e in inputs["files"]:
 p=P.parent/e["file"]
 if sha(p)!=e["sha256"] or p.stat().st_size!=e["bytes"]:raise RuntimeError("protected V1/round1/input changed")
report=P.parent/"whole_qualified_package_round1_20261005/REPORT.md"
closed=P.parent/"whole_qualified_package_round1_20261005/CLOSED_MANIFEST.json"
if sha(report)!="be4f8abab1cda0ea36fd60b0174bb409570942fe62ee780e9624f8187ac139e2":raise RuntimeError("round1 report hash")
if sha(closed)!="30b71243599df77235d73d7c8b118c342f31bb94654ee6648f1e8bf39e98a4c0":raise RuntimeError("round1 closed hash")
v1=P.parent/"qualified_publication_package_v1"
d=json.loads((v1/"PREPARATION_MANIFEST.json").read_text())
for e in d["files"]:
 if sha(v1/e["file"])!=e["sha256"]:raise RuntimeError("frozen V1 body changed")
for name in ["pr95_note.tex","pr95_note.pdf"]:
 if sha(F/name)!=sha(v1/"publicfiles"/name):raise RuntimeError("manuscript/PDF change")
if sha(P/"zenodo-deposit.json")!=sha(v1/"zenodo-deposit.json"):raise RuntimeError("metadata change")
dump(N/"PRESERVATION_CHECK.json",{"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"V1_manifest_entries":len(d["files"]),"all_V1_unchanged":True,"all_read_inputs_unchanged":True,"round1_report_sha256":sha(report),"round1_closed_manifest_sha256":sha(closed),"manuscript_pdf_deposit_metadata_identical":True,"metadata_version":"1.0"})
print(json.dumps({"zenodo_local_exit":r["exit_code"],"frozen_V1_entries_unchanged":len(d["files"]),"current_metadata_unchanged":True}))
