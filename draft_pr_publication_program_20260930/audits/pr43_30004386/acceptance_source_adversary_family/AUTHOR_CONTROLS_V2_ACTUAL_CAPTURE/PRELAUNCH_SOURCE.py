"""Correct own AST export inspection for tuple-unpacked production constants."""
from pathlib import Path
import hashlib,json,os,datetime
H=Path(__file__).resolve().parent;p=H/'independent_controls.py';raw=p.read_bytes();text=raw.decode()
old="exported=set(guard)|{n.id for z in trees['pr43_guards.py'].body if isinstance(z,ast.Assign)for n in z.targets if isinstance(n,ast.Name)}"
new="exported=set(guard)|{n.id for z in trees['pr43_guards.py'].body if isinstance(z,ast.Assign)for target in z.targets for n in ast.walk(target) if isinstance(n,ast.Name)}"
assert text.count(old)==1 and not(H/'PRIVATE').exists();text=text.replace(old,new)
with(H/'independent_controls_v2.py').open('x')as f:f.write(text)
record={'schema':'PR43_SOURCE_ADVERSARY_OWN_CONTROL_REPAIR_v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'old_source_sha256':hashlib.sha256(raw).hexdigest(),'new_source_sha256':hashlib.sha256(text.encode()).hexdigest(),'reason':'Own inspection listed only direct assignment targets and missed actual tuple-unpacked ID,CODE,PR. The production definitions exist. V1 failed before private fixtures. Both actual prelaunch/failure and original source are retained.','old_source_preserved':p.read_bytes()==raw,'proposed_code_executed':False}
(H/'OWN_CONTROL_REPAIR.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
