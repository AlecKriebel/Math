#!/usr/bin/env python3
"""Replay frozen finite diagnostics in disposable copies; never overwrite evidence."""
import argparse,fnmatch,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'diagonal_permuton_1778_20261014'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--list',action='store_true')
p.add_argument('--all',action='store_true')
p.add_argument('--match',action='append',default=[],help='Glob of data-root-relative script path; repeatable')
p.add_argument('--modes',default='0',help='Comma-separated Python optimization modes, e.g. 0,1,2')
p.add_argument('--output',help='New directory outside the frozen package')
a=p.parse_args()
scripts=sorted(str(f.relative_to(DATA)) for f in DATA.rglob('*.py'))
selected=[s for s in scripts if a.all or any(fnmatch.fnmatch(s,g) for g in a.match)]
if a.list or not (a.all or a.match):
 print('\n'.join(scripts));sys.exit(0)
modes=[int(x) for x in a.modes.split(',')]
if not modes or any(m not in (0,1,2) for m in modes):p.error('Modes must be 0, 1 or 2.')
if not selected:p.error('No script matches.')
if not a.output:p.error('--output is required for a replay.')
out=Path(a.output).resolve()
if out==ROOT or ROOT in out.parents:p.error('Use an output directory outside the frozen package.')
if out.exists():p.error('The output directory must be new.')
out.mkdir(parents=True)
summary={'scope':'Finite diagnostic replay only, not an asymptotic proof or a new mathematical investigation.','python':sys.version,'runs':[]}
for script in selected:
 for mode in modes:
  key=script.replace('/','__').removesuffix('.py')+'__opt'+str(mode)
  dest=out/key;dest.mkdir()
  with tempfile.TemporaryDirectory(prefix='permuton-replay-') as td:
   copy=Path(td)/DATA.name;shutil.copytree(DATA,copy)
   command=[sys.executable]+(['-'+('O'*mode)] if mode else [])+[str(copy/script)]
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
   started=time.monotonic()
   with (dest/'stdout.txt').open('wb') as stdout,(dest/'stderr.txt').open('wb') as stderr:
    run=subprocess.run(command,cwd=copy,env=env,stdout=stdout,stderr=stderr)
   changed=[]
   for generated in copy.rglob('*.json'):
    rel=generated.relative_to(copy);original=DATA/rel
    if not original.exists() or generated.read_bytes()!=original.read_bytes():
     target=dest/'generated'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(generated,target)
     changed.append(str(rel))
   record={'script':script,'optimization':mode,'exit_code':run.returncode,'seconds':round(time.monotonic()-started,3),'changed_json_reports':changed}
   summary['runs'].append(record)
   print(json.dumps(record),flush=True)
   (out/'REPLAY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
summary['all_processes_succeeded']=all(r['exit_code']==0 for r in summary['runs'])
summary['caution']='Successful exit is a diagnostic replay outcome. Consult stdout, generated reports, and original check scope. No finite output establishes an all-size theorem.'
(out/'REPLAY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
sys.exit(0 if summary['all_processes_succeeded'] else 1)
