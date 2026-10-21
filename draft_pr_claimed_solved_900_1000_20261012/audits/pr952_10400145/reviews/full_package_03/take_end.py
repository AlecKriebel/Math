"""Fresh immutable read-only end boundary; preserve every launch and failure."""
from pathlib import Path
import json,hashlib,subprocess,sys,datetime
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1];D=A/'preprint';label=sys.argv[1]
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
pins={P/'accept_pr952.py':'14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec',D/'FREEZE.json':'ab027971f0245481783e2afa106292543c41f06a93c3c83a0cf8dcea4cff9d77',A/'publication/workflow/OPERATIONS_INVENTORY.json':'9650f0baf87ac6d83a5a7eb934d212cc66ea67dea4c8758813bec47f5a24cc05'}
for path,pin in pins.items():
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise RuntimeError('external authority changed')
def launch(prefix,cmd,private=False):
 base=(R/'private' if private else R)/prefix
 if Path(str(base)+'.launch.json').exists():raise RuntimeError('never overwrite prior actual launch')
 begin=stamp();p=subprocess.run(cmd,capture_output=True,cwd=R);finish=stamp()
 Path(str(base)+'.stdout.raw').write_bytes(p.stdout);Path(str(base)+'.stderr.raw').write_bytes(p.stderr);Path(str(base)+'.launch.json').write_text(json.dumps({'start':begin,'end':finish,'argv':cmd,'returncode':p.returncode},indent=2)+'\n')
 return p
existing=R/'AUTHENTICATION_END.json'
if existing.exists():
 keep=R/'private'/('AUTHENTICATION_END_before_'+label+'.json')
 if keep.exists():raise RuntimeError('preserve actual prior END once')
 keep.write_bytes(existing.read_bytes())
p=launch(label+'_MECHANICAL',[sys.executable,'-I','-S','-B',str(R/'authenticate.py'),'END'])
if p.returncode:raise RuntimeError('mechanical END failed; raw preserved')
obs=R/('preflight_'+label.lower());obs.mkdir()
cmd=[sys.executable,'-I','-S','-B',str(P/'accept_pr952.py'),'--operations-sha256',pins[A/'publication/workflow/OPERATIONS_INVENTORY.json'],'--freeze',pins[D/'FREEZE.json'],'--preflight-only','--observation-dir',str(obs)]
p=launch('PREFLIGHT_'+label,cmd,True)
print('ACTUAL_READ_ONLY_PREFLIGHT_EXIT',p.returncode,flush=True)
if p.returncode:raise SystemExit(p.returncode)
for suffix in ['stdout.raw','stderr.raw','launch.json']:(R/'private'/('PREFLIGHT_END.'+suffix)).write_bytes((R/'private'/('PREFLIGHT_'+label+'.'+suffix)).read_bytes())
p=launch(label+'_FORMAT',[sys.executable,'-I','-S','-B',str(R/'format_authentication.py'),'END'])
if p.returncode:raise RuntimeError('END formatting failed; raw preserved')
(R/'private'/('AUTHENTICATION_'+label+'.json')).write_bytes(existing.read_bytes())
summary=json.loads((R/'ACTUAL_END_PREFLIGHT_SUMMARY.json').read_bytes());print('END_PASS',summary['utc'],summary['actual_main'])
