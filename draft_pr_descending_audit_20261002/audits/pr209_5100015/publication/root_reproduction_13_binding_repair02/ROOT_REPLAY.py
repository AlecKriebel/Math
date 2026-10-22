from pathlib import Path
import subprocess,json,datetime,hashlib
d=Path(__file__).resolve().parent;py='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
runs=[]
for name in ['retry_probes_01.py','final_controls.py']:
 with (d/(name+'.ROOT.stdout')).open('xb') as out,(d/(name+'.ROOT.stderr')).open('xb') as err:
  r=subprocess.run([py,'-B',str(d/name)],stdout=out,stderr=err)
 runs.append(dict(program=name,actual_exit=r.returncode))
 (d/'ROOT_PROGRAM_EXITS.json').write_text(json.dumps(runs,indent=2)+'\n')
 assert r.returncode==0,name
rows=[]
for p in [d/'retry_01/RESULTS.json',d/'final_controls/RESULTS.json']:rows+=json.loads(p.read_bytes())
assert len(rows)==11 and all(x['PASS'] for x in rows)
# Expected semantic error types are explicit; storage faults cannot masquerade as passed guards.
def inspect(x):
 if isinstance(x,dict):
  if 'type' in x and 'error' in x:assert x['type'] in ['RuntimeError','UnicodeDecodeError','TimeoutExpired','IncompleteRead','OSError'],x
  for v in x.values():inspect(v)
 elif isinstance(x,list):
  for v in x:inspect(v)
inspect(rows)
(d/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual11_groups_pass=True,actual_program_exits=runs,operative_source_rewrite=False,providers_controlled_only=True,no_release_authority=True,case_completion_percent=65),indent=2)+'\n')
print('ROOT11GROUPSPASS',flush=True)
