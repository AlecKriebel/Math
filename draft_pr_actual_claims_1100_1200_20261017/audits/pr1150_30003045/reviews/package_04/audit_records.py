from pathlib import Path
import json,hashlib,difflib,subprocess,os
D=Path(__file__).absolute().parent;S=D/'private/source';A=S/'draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045';real=D.parent.parent
out={}
def pin(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
family=[('target_quadric_01','RECEIPT.json',['artifacts','inputs','private_sources_and_history']),('norm_obstruction_01','RECEIPT.json',['artifacts','inputs','private_source_files']),('symbols_01','RECEIPT.json',['authored_artifacts','inputs','private_source_material']),('priority_target_01','RECEIPT.json',['artifacts','inputs','private_evidence']),('priority_mixed_01','READ_RECEIPT.json',['pins']),('priority_brauer_01','READ_RECEIPT.json',['artifacts','inputs'])]
for f,r,groups in family:
 base=A/'reviews'/f;receipt=json.loads((base/r).read_text());rows=[]
 for g in groups:
  for x in receipt[g]:
   p=(base/x['path']).resolve();available=p.is_file();okay=pin(p)=={'bytes':x['bytes'],'sha256':x['sha256']} if available else None
   if available and not okay:raise ValueError((f,x['path']))
   rows.append({'group':g,'path':x['path'],'available_in_distribution':available,'exact_pin_match':okay,'classification':'available authored/input authentication' if available else 'intentionally omitted private body/tool/history; not an operative math failure'})
 out[f]={'receipt':pin(base/r),'pins':rows,'available':sum(x['available_in_distribution'] for x in rows),'omitted':sum(not x['available_in_distribution'] for x in rows)}
prior={}
for f in ['package_01','package_02','package_03']:
 base=real/'reviews'/f;r=json.loads((base/'EXTERNAL_FINAL_RECEIPT.json').read_text());g=r.get('evidence') or r.get('artifacts') or r.get('pins');rows=[]
 if isinstance(g,dict):
  for n,w in g.items():rows.append({'path':n,'pin_match':pin(base/n)==w})
 elif isinstance(g,list):
  for w in g:rows.append({'path':w['path'],'pin_match':pin(base/w['path'])=={'bytes':w['bytes'],'sha256':w['sha256']}})
 if not all(x['pin_match'] for x in rows):raise ValueError((f,'receipt evidence mismatch'))
 prior[f]={'receipt':pin(base/'EXTERNAL_FINAL_RECEIPT.json'),'public_evidence_checked':rows,'frozen_six_record':r.get('frozen_six') if f!='package_03' else r['frozen_six_unchanged']}
checks={}
for name in ['inputs','pr_repair_candidate']:
 b=A/name;m=json.loads((b/'MANIFEST.json').read_text());entries=m.get('entries') or m.get('files')
 if isinstance(entries,list):entries={w['file']:{'bytes':w['bytes'],'sha256':w['sha256']} for w in entries}
 names=m.get('members') or list(entries)+['MANIFEST.json'];checks[name]={'members':len(names),'exact_inventory':set(names)=={p.name for p in b.iterdir()},'all_nonself_pins':all(pin(b/n)==w for n,w in entries.items())}
checks['final_equals_current']=(A/'FINAL_PROOF.md').read_bytes()==(A/'pr_repair_candidate/COUNTEREXAMPLE.md').read_bytes()
checks['symbols_current_family_equal']=(A/'pr_repair_candidate/verify_symbols.py').read_bytes()==(A/'reviews/symbols_01/verify_symbols.py').read_bytes()
x=(A/'reviews/norm_obstruction_01/diagnose_norm.py').read_text();y=(A/'pr_repair_candidate/diagnose_norm.py').read_text();(D/'NORM_COPY.diff').write_text(''.join(difflib.unified_diff(x.splitlines(True),y.splitlines(True))));checks['norm_only_docstring']=x.replace('REPORT.md','COUNTEREXAMPLE.md',1)==y
jsons=[p for p in S.rglob('*.json') if '/output/' not in str(p)];checks['source_tree_JSON_count_after_private_build']=len(jsons);checks['source_archive_JSON_count']=sum(r['name'].endswith('.json') for r in json.loads((D/'INVENTORY.json').read_text())['source']['members']);checks['source_all_JSON_parse']=all(json.loads(p.read_text()) is not None for p in jsons)
checks['workspace_vs_frozen_authored']={str(p.relative_to(A)):pin(p)==pin(real/p.relative_to(A)) for p in A.rglob('*') if p.is_file()}
for n,a,b in [('ORIGINAL_TO_INTERMEDIATE.diff','inputs/COUNTEREXAMPLE.md','REVIEWED_PROOF.md'),('INTERMEDIATE_TO_FINAL.diff','REVIEWED_PROOF.md','FINAL_PROOF.md')]:
 x=(real/a).read_text();y=(real/b).read_text();(D/n).write_text(''.join(difflib.unified_diff(x.splitlines(True),y.splitlines(True),fromfile=a,tofile=b)))
(D/'HISTORICAL_AUTHENTICATION.json').write_text(json.dumps({'families':out,'prior_packages':prior,'checks':checks},indent=2)+'\n')
print('family available',sum(x['available'] for x in out.values()),'omitted',sum(x['omitted'] for x in out.values()));print('checks', {k:v for k,v in checks.items() if k!='workspace_vs_frozen_authored'});print('workspace archived match',all(checks['workspace_vs_frozen_authored'].values()))
G=D/'private/offline_guard';G.mkdir(exist_ok=True);(G/'sitecustomize.py').write_text('import socket\ndef forbidden(*args,**kwargs):\n raise RuntimeError("NETWORK DISABLED IN PACKAGE04 OFFLINE CHECK")\nsocket.socket=forbidden\nsocket.create_connection=forbidden\nsocket.getaddrinfo=forbidden\n')
env=dict(os.environ,PYTHONPATH=str(G),PYTHONDONTWRITEBYTECODE='1');runs=[]
for flags in [[],['-O']]:
 r=subprocess.run(['python3','-B',*flags,str(S/'verification/verify_all.py')],cwd=S,env=env,capture_output=True);runs.append({'flags':flags,'exit':r.returncode,'stderr':r.stderr.decode(),'bytes':len(r.stdout),'sha256':hashlib.sha256(r.stdout).hexdigest(),'frozen_receipt_match':r.stdout==(S/'verification/REPLAY_RECEIPT.json').read_bytes()})
if not all(x['exit']==0 and x['frozen_receipt_match'] for x in runs):raise ValueError('offline replay failed')
(D/'OFFLINE_REPLAY.json').write_text(json.dumps({'guard':pin(G/'sitecustomize.py'),'scope':'socket construction,connection,address resolution disabled through inherited PYTHONPATH in outer and every child','runs':runs},indent=2)+'\n');print('offline',runs)
