from pathlib import Path
import json, hashlib, datetime, sys
R=Path(__file__).resolve().parent
A=R.parent.parent
F=R/"INPUT_FREEZE.json"
EXPECT="6df0f15c46c4bbaa128446c0af7e1639be1cc416ce997c9a46d7849e28859448"
def physical(p):
    q=Path(p.anchor)
    for component in p.parts[1:]:
        if component not in {x.name for x in q.iterdir()}: return False
        q=q/component
    return True
f=json.loads(F.read_text()); errors=[]; bindings=[]
if hashlib.sha256(F.read_bytes()).hexdigest()!=EXPECT: errors.append("freeze hash mismatch")
for group in ("files","external_readonly_inputs"):
    for e in f[group]:
        p=Path(e["path"]); p=p if p.is_absolute() else A/p
        try:
            b=p.read_bytes(); exact=physical(p); h=hashlib.sha256(b).hexdigest()
            ok=exact and len(b)==e["bytes"] and h==e["sha256"]
            bindings.append({"group":group,"path":e["path"],"bytes":len(b),"sha256":h,"exact_physical_case":exact,"ok":ok})
            if not ok: errors.append(e["path"])
        except Exception as exc: errors.append({"path":e["path"],"error":str(exc)})
result={"schema":"math-pr1274-review-input-authentication-v1","at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"input_freeze_sha256":EXPECT,"files_checked":len(f["files"]),"external_inputs_checked":len(f["external_readonly_inputs"]),"all_ok":not errors,"errors":errors,"bindings":bindings}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="bindings"}))
sys.exit(bool(errors))
