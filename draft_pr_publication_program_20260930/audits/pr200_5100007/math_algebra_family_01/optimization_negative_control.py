"""False first submitted check: normal must reject, -O falsely passes."""
from pathlib import Path
import sys,subprocess,json
root=Path(__file__).resolve().parent
source=(root.parent/"original_submitted_head"/"verify.py").read_text()
old="ck('universal_U_plus_V',sy.expand(U+V-2*q*(1-z*t))==0)"
new="ck('universal_U_plus_V',False)  # DELIBERATE NEGATIVE CONTROL"
if source.count(old)!=1:raise RuntimeError("unique mutation target not found")
source=source.replace(old,new)
results={"mutation":{"old":old,"new":new},"purpose":"Show -O printed PASS/counts do not establish checks", "runs":{}}
for mode,options in [("normal",[]),("optimized",["-O"])]:
    replay=root/("false_check_"+mode);replay.mkdir(exist_ok=True)
    (replay/"verify.py").write_text(source)
    (replay/"PROOF.md").write_bytes((root.parent/"original_submitted_head"/"PROOF.md").read_bytes())
    launcher="import sys,runpy;sys.path.insert(0,"+repr(str(root/"runtime_packages"))+");runpy.run_path("+repr(str(replay/"verify.py"))+",run_name='__main__')"
    run=subprocess.run([sys.executable,"-E","-B","-P"]+options+["-c",launcher],text=True,capture_output=True)
    (replay/"stdout.txt").write_text(run.stdout);(replay/"stderr.txt").write_text(run.stderr)
    results["runs"][mode]={"returncode":run.returncode,"printed_PASS":'"status": "PASS"' in run.stdout}
if results["runs"]["normal"]["returncode"]==0:raise RuntimeError("normal failed to reject deliberate false check")
if results["runs"]["optimized"]!={"returncode":0,"printed_PASS":True}:raise RuntimeError("unexpected optimized control behavior")
(root/"optimization_negative_control.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
