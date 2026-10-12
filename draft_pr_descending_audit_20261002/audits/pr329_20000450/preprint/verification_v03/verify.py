#!/usr/bin/env python3
"""Read-only public integrity, scientific replay and negative controls."""
import sys
if sys.flags.optimize:
    raise SystemExit('Verification refuses Python optimization (-O/-OO).')
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,re,stat,subprocess
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
def require(ok,label):
    if not ok:raise ValueError(label)
parser=argparse.ArgumentParser()
parser.add_argument('--suite',choices=['all','arithmetic'],default='all')
parser.add_argument('--python',default=sys.executable)
args=parser.parse_args()
manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
records=manifest['files']
def inventory():
    files={};dirs={}
    for p in sorted(ROOT.rglob('*')):
        require(not p.is_symlink(),'Symlink: '+str(p))
        rel=str(p.relative_to(ROOT))
        if p.is_file():
            b=p.read_bytes();files[rel]=dict(bytes=len(b),sha256=sha(b),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
        elif p.is_dir():dirs[rel]=f'{stat.S_IMODE(p.stat().st_mode):04o}'
    return files,dirs
before,dirs=inventory()
require(set(before)==set(records)|{'MANIFEST.json'},'Complete file inventory mismatch')
require({k:v for k,v in before.items() if k!='MANIFEST.json'}==records,'File body/mode mismatch')
require(dirs==manifest['directory_modes'],'Directory mode/inventory mismatch')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
env.pop('PYTHONOPTIMIZE',None)
results=[]
def run(name,extra=(),expected_exit=0,expected_name=None):
    argv=[args.python,'-B',str(ROOT/'programs'/(name+'.py')),*extra]
    started=utc();r=subprocess.run(argv,cwd=ROOT,capture_output=True,env=env,timeout=180)
    ended=utc();require(r.returncode==expected_exit,f'{name}: exit{r.returncode}; '+r.stderr.decode(errors='replace'))
    require(r.stderr==b'',name+': unexpected stderr')
    target=expected_name or name
    if name.startswith('geometry'):
        lines=[]
        for line in r.stdout.decode().splitlines():
            if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',line):continue
            line=re.sub(r' native_utc \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00$','',line)
            lines.append(line)
        value=('\n'.join(lines)+'\n').encode()
        require(value==(ROOT/'expected'/(target+'.txt')).read_bytes(),name+': complete mathematical text mismatch')
    else:
        value=json.loads(r.stdout)
        if name=='division_chord':require('interpreter' in value,'Missing interpreter provenance');del value['interpreter']
        require(value==json.loads((ROOT/'expected'/(target+'.json')).read_bytes()),name+': complete mathematical JSON mismatch')
    results.append(dict(program=name,argv=argv,start_utc=started,end_utc=ended,actual_exit=r.returncode,
        stdout_bytes=len(r.stdout),stdout_sha256=sha(r.stdout),stderr_bytes=len(r.stderr),
        complete_mathematical_output_equal=True,mutant=extra[1] if extra else None))
if args.suite=='all':
    ver=subprocess.run([args.python,'-B','-c','import sys,sympy; print(sys.version.split()[0]); print(sympy.__version__)'],capture_output=True,env=env,cwd=ROOT)
    require(ver.returncode==0 and ver.stderr==b'','Dependency probe failed')
    require(ver.stdout.decode().splitlines()[-1]=='1.14.0','Require SymPy1.14.0')
    for name in ['geometry_source','geometry_quotient','geometry','geometry_primitivity','division_chord','division_model','division_finite','division_quintic','candidate']:
        run(name)
run('priority')
run('arithmetic')
for mutant in ['drop_twist','wrong_radical','wrong_cyclotomic','wrong_norm_degree']:
    run('arithmetic',('--mutant',mutant),1,'mutant_'+mutant)
require(inventory()==(before,dirs),'Replay changed an owned file or mode')
print(json.dumps(dict(status='PASS',suite=args.suite,payload_files=len(records),
    positive_programs=11 if args.suite=='all' else 2,negative_mutants=4,all_bodies_modes_inventory_unchanged=True,
    manifest_sha256=before['MANIFEST.json']['sha256'],results=results,
    scope='Exact identities and falsification controls supplement the proof and credited modular input; no sampling proof of all-fiber or priority claims.'),indent=2))
