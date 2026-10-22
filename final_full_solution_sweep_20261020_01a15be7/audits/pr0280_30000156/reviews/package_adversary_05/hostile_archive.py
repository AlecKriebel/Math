#!/usr/bin/env python3
from pathlib import Path
import copy,hashlib,json,os,shutil,subprocess,sys
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];W=R/'private/pr0280_package05';P=W/'extract/birational-cycle-verification';H=W/'hostile';H.mkdir(exist_ok=True)
cases=['schema_bool','schema_float','schema_string','schema_extra','bytes_bool','bytes_float','duplicate_entry','parent_path','absolute_path','backslash_path','normalized_path','extra_file','missing_file','payload_tamper','payload_symlink','manifest_symlink','directory_symlink','fifo','coherently_rehashed_false_baseline','duplicate_json_schema','duplicate_json_path']
results=[]
for mode in [[],['-O']]:
 for case in cases:
  D=H/(('O_' if mode else 'N_')+case);shutil.copytree(P,D);M=D/'MANIFEST.json';m=json.loads(M.read_text());raw=None
  if case.startswith('schema_'):
   if case=='schema_extra':m['unknown']=1
   else:m['schema']={'schema_bool':True,'schema_float':1.0,'schema_string':'1'}[case]
  if case=='bytes_bool':m['files'][0]['bytes']=True
  if case=='bytes_float':m['files'][0]['bytes']=float(m['files'][0]['bytes'])
  if case=='duplicate_entry':m['files'].append(copy.deepcopy(m['files'][0]))
  if case in ['parent_path','absolute_path','backslash_path','normalized_path']:m['files'][0]['path']={'parent_path':'../x','absolute_path':'/x','backslash_path':'paper\\main.tex','normalized_path':'paper/../CITATION.cff'}[case]
  if case=='extra_file':(D/'unexpected').write_text('x')
  if case=='missing_file':(D/'CITATION.cff').unlink()
  if case=='payload_tamper':(D/'paper/main.tex').write_text('changed')
  if case=='payload_symlink':(D/'CITATION.cff').unlink();(D/'CITATION.cff').symlink_to(P/'CITATION.cff')
  if case=='manifest_symlink':M.unlink();M.symlink_to(P/'MANIFEST.json')
  if case=='directory_symlink':shutil.rmtree(D/'paper');(D/'paper').symlink_to(P/'paper',target_is_directory=True)
  if case=='fifo':os.mkfifo(D/'fifo')
  if case=='coherently_rehashed_false_baseline':
   q=D/'expected_checks.json';v=json.loads(q.read_text());v['exact_checks']+=1;b=(json.dumps(v,indent=2)+'\n').encode();q.write_bytes(b)
   e=next(e for e in m['files'] if e['path']=='expected_checks.json');e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  if case=='duplicate_json_schema':raw=json.dumps(m).replace('"schema": 1','"schema": false, "schema": 1',1)
  if case=='duplicate_json_path':raw=json.dumps(m).replace('"path": "CITATION.cff"','"path": "../unsafe", "path": "CITATION.cff"',1)
  if case!='manifest_symlink':M.write_text(raw or json.dumps(m,indent=2))
  r=subprocess.run([sys.executable,'-B',*mode,'verify.py'],cwd=D,capture_output=True,text=True,timeout=30)
  expected_accept=case.startswith('duplicate_json_')
  if (r.returncode==0)!=expected_accept:raise RuntimeError('unexpected outcome '+case+' '+r.stderr)
  results.append({'case':case,'optimized':bool(mode),'accepted':r.returncode==0,'exit':r.returncode,'last_error':r.stderr.splitlines()[-1] if r.stderr else None,'scope':'JSON duplicate object keys use Python last-value-wins' if expected_accept else 'reject expected'})
(O/'HOSTILE_ARCHIVE.json').write_text(json.dumps({'distinct_mutations':len(cases),'rejections':sum(not r['accepted'] for r in results),'accepted_duplicate_key_observations':sum(r['accepted'] for r in results),'results':results,'interpretation':'The verifier rejects malformed schema/value/path/inventory and semantic changes under both modes. JSON object duplicate keys are not separately rejected; the decoder uses last-value-wins. This is disclosed as a parser boundary, not proof of a changed fixed release or a new mathematical failure.'},indent=2)+'\n');print(json.dumps({'rejected':sum(not r['accepted'] for r in results),'dupkey_last_wins_observations':sum(r['accepted'] for r in results)}))
