"""Portable explicit-exception controls. Run in ordinary or optimized Python."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def clean(x):
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k not in ['UTC','elapsed_seconds','optimization']}
    if isinstance(x,list):return [clean(v) for v in x]
    return x
def main():
    p=argparse.ArgumentParser();p.add_argument('--full-physical',action='store_true');p.add_argument('--guard-false',action='store_true');args=p.parse_args()
    require(not args.guard_false,'DELIBERATE FALSE CONDITION')
    m=json.loads((HERE.parent/'MANIFEST.json').read_text())
    for rel,pn in m['files'].items():
        f=HERE.parent/rel
        require(not f.is_symlink() and pin(f.read_bytes())==pn,'Manifest mismatch: '+rel)
    jobs=[
      ('source_area_checks.py','source_normal.txt','text'),
      ('exact_geometry_controls.py','geometry_exact.json','json'),
      ('exact_independent_controls.py','axis_exact.json','json'),
      ('extended_exact_controls.py','general_axis.json','json'),
      ('exact_classical_controls.py','classical_exact.json','json')]
    if args.full_physical:jobs.append(('physical_phase_checks.py','physical_fresh.json','json'))
    completed=[]
    for script,expected,kind in jobs:
        cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(HERE/script)]
        r=subprocess.run(cmd,capture_output=True,text=True)
        require(r.returncode==0,script+': '+r.stderr)
        want=(HERE/'expected'/expected).read_text()
        actual,expect=(clean(json.loads(r.stdout)),clean(json.loads(want))) if kind=='json' else (r.stdout,want)
        require(actual==expect,'Retained expected result differs: '+script)
        completed.append(script)
    print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'explicit_exceptions':True,'all_manifest_entries_verified':len(m['files']),'completed':completed,'scope':'Finite exact and noninterval numerical controls; written proof establishes all N.'},indent=2))
if __name__=='__main__':main()
