from pathlib import Path
import json,hashlib,stat,os,subprocess,datetime,shutil
O=Path(__file__).resolve().parent;A=O.parents[1];P=A.parents[2];D=A/'preprint';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
f=json.loads((D/'FREEZE.json').read_bytes());results=[]
for family,item in f['family_authentication'].items():
 base=A/'reviews'/family;raw=(base/'MANIFEST.json').read_bytes();assert sha(raw)==item['manifest_sha256'];doc=json.loads(raw);entries=doc.get('files',doc.get('payloads',doc.get('public_payloads')))
 rows=entries.items() if type(entries) is dict else ((x['path'],x) for x in entries)
 checked=[]
 for n,r in rows:
  b=(base/n).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'];copy=D/'package/reviews'/family/n;assert copy.read_bytes()==b;checked.append(n)
 results.append({'family':family,'manifest_sha256':sha(raw),'actual_schema':doc['schema'],'public_files':checked,'package_copies_exact':True})
save('FIVE_FAMILY_AUTHENTICATION.json',{'utc':now(),'status':'PASS','families':results})
old=D/'reviewed_candidates/candidate01';oldfreeze=json.loads((old/'FREEZE.json').read_bytes());inventory=json.loads((old/'OPERATIONS_INVENTORY.json').read_bytes())
for n,r in oldfreeze['files'].items():b=(old/n).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for n,r in oldfreeze['evidence_files'].items():b=(old/'evidence'/n).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for n,r in inventory['files'].items():b=(old/'operations'/n).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
oldman=A/'operations_engineering_01/MANIFEST.json';assert sha(oldman.read_bytes())=='3fc478015918320f37f980632b9f6aa78a012f5444a85404ccf56ab39e346c7e';m=json.loads(oldman.read_bytes());own=0
for n,r in m['files'].items():
 p=P/n
 if not n.startswith('draft_pr_claimed_solved_900_1000_20261012/audits/pr952_10400145/operations_engineering_01/'):
  p=old/'operations'/n
 else:own+=1
 b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],str(p)
save('HISTORICAL_CANDIDATE_AUTHENTICATION.json',{'utc':now(),'status':'PASS','candidate_revision':1,'freeze_sha256':sha((old/'FREEZE.json').read_bytes()),'candidate_files':len(oldfreeze['files']),'evidence_files':len(oldfreeze['evidence_files']),'operations':len(inventory['files']),'operations01_own_payloads':own,'operations01_oldcore_authenticated_in_archive':True,'currentcore_different_intentionally':True,'full_review_credit_for_candidate01':False})
# Parse entire sealed evidence into structure inventories; don't confuse this
# with personally close-reading every primary body represented by metadata.
intake=[]
for directory in [A/'package_engineering_01',A/'operations_engineering_01',A/'operations_engineering_02',*[A/'reviews'/x['family'] for x in results]]:
 for p in sorted(directory.iterdir()):
  if not p.is_file() or p.suffix not in ('.json','.md','.py'):continue
  raw=p.read_bytes();row={'path':str(p.relative_to(P)),'bytes':len(raw),'sha256':sha(raw),'type':p.suffix}
  if p.suffix=='.json':
   data=json.loads(raw);row['json_root_type']=type(data).__name__;row['keys']=list(data) if type(data) is dict else [];row['status']=data.get('status') if type(data) is dict else None
  intake.append(row)
save('PRIOR_EVIDENCE_STRUCTURAL_INTAKE.json',{'utc':now(),'scope':'Entire current/historical sealed evidence parsed/authenticated; reports, executable guards and selected source pages separately close-read. Raw receipts are historical observations, never new passes.','files':intake})
work=O/'private_legacy';work.mkdir(exist_ok=True);packet=work/'packet';shutil.copytree(A/'original/unsolved_math_prioritization/attempts/10400145',packet)
def launch(label,cmd,cwd,env):
 start=now();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=120);(O/(label+'.stdout.json')).write_bytes(r.stdout);(O/(label+'.stderr.txt')).write_bytes(r.stderr);save(label+'.launch.json',{'started_utc':start,'completed_utc':now(),'argv':cmd,'cwd':str(cwd),'returncode':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)});return r
legacy=[]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 r=launch('LEGACY_FULL_'+label,['python3','-I','-S','-B',*flags,str(packet/'BOOTSTRAP.py'),str(packet)],work,dict(os.environ,TMPDIR=str(work)))
 assert r.returncode!=0 and b'bwrap' in r.stderr;legacy.append({'mode':label,'returncode':r.returncode,'status':'NOT_REPRODUCED','reason':'actual full launcher fails because bwrap absent'})
save('LEGACY_REPLAY_OBSERVATION.json',{'utc':now(),'status':'NOT_REPRODUCED','which_bwrap':shutil.which('bwrap'),'modes':legacy,'portable_pass_is_distinct':True})
# Fresh actual route checkers in own folder; algebra's assertions only earn
# unoptimized evidence, as the supplement already states.
checks=O/'private_route_controls';checks.mkdir(exist_ok=True)
for family,name in [('algebra_falsifier_01','independent_controls.py'),('quantum_bridge_01','INDEPENDENT_CHECKS.py')]:
 src=A/'reviews'/family/name;dest=checks/(family+'.py');dest.write_bytes(src.read_bytes());r=launch('ROUTE_'+family,['python3','-I','-S','-B',str(dest)],checks,dict(os.environ,TMPDIR=str(checks)));assert r.returncode==0,(family,r.stderr)
print(json.dumps({'status':'PASS','family_seals':5,'historical_files':len(oldfreeze['files']),'historical_evidence':len(oldfreeze['evidence_files']),'historical_operations':7,'prior_evidence_structural_files':len(intake),'legacy_actual_nonpasses':3,'route_controls':2},sort_keys=True))
