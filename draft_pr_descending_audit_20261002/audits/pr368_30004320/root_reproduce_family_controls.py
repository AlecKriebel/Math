"""Read-only original family binding validation and independent full-output control replay."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'snapshot/problems/30004320_laurent_descent';S=A/'root_family_control_streams';S.mkdir(exist_ok=True)
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(v,name):checks.append({'name':name,'pass':bool(v)});assert v,name
def get(rev,path):return subprocess.check_output(['git','show',rev+':'+path],cwd=R)
def bound(root,row):
 p=PurePosixPath(row['path']);ck(not p.is_absolute() and '..' not in p.parts and str(p)==row['path'],'safe binding '+str(root.name)+'/'+row['path'])
 f=root/p;ck(not f.is_symlink() and f.resolve().is_relative_to(root.resolve()),'owned bound file '+row['path']);b=f.read_bytes();ck(len(b)==row['bytes'] and sha(b)==row['sha256'],'complete immutable binding '+root.name+'/'+row['path']);return b
root=json.loads((A/'root_original_reproduction_receipt.json').read_bytes());ck(root['status']=='PASS' and root['check_count']==501 and all(r['pass'] for r in root['checks']),'own complete501 frozen reproduction')
configs=[('descent_cohomology_review',35,'ADVERSARIAL_CONTROLS.py','ADVERSARIAL_CONTROLS.stdout',1923,'INTEGRITY_REPLAY_RECEIPT.json',866),('residue_valuation_review',37,'residue_valuation_controls.py','RESIDUE_VALUATION_CONTROLS.json',3029,'ARTIFACT_REPRODUCTION.json',434),('clean_final_adversary',47,'adversarial_controls.py','ADVERSARIAL_CONTROLS.json',8387,'FROZEN_PROVENANCE_AND_REPLAY.json',618)]
root_streams={r['label']:(A/'root_original_streams'/(r['label']+'.stdout')).read_bytes() for r in root['replays']}
def expected_stream(label):
 if label.startswith('author_turn_'):return root_streams['author'+label.rsplit('_',1)[1]]
 if label.startswith('author_') and label[7:].isdigit():return root_streams['author'+label[7:]]
 return root_streams[{'historical_review_controls':'historical_review','historical_independent':'historical_review','prior_independent':'historical_review','author_wrapper':'packet_with_sources','packet_with_sources':'packet_with_sources','packet_without_sources':'packet_without_sources','historical_review_wrapper':'review_wrapper','review':'review_wrapper','publication_no_sources':'publication_without_sources','publication_without_sources':'publication_without_sources','publication_with_sources':'publication_with_sources'}[label]]
families=[]
for family,count,program,output,ncontrols,receipt,nchecks in configs:
 F=A/family;mf=json.loads((F/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
 for row in mf['files']:
  ck(row['path'] not in seen,'unique family path '+family+'/'+row['path']);seen.add(row['path']);bound(F,row)
 ck(len(seen)==count,'complete family count '+family)
 if family=='descent_cohomology_review':actual={p.name for p in F.iterdir() if p.is_file() and p.name!='PUBLIC_MANIFEST.json'}
 else:actual={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and not any(x=='private' or x.startswith('private_') or x in ['final_live','post_merge','provenance_appendix','__pycache__'] for x in p.relative_to(F).parts) and p.name!='PUBLIC_MANIFEST.json'}
 ck(actual==seen,'closed original family scope '+family)
 times=[]
 for name in ['SOURCE_FIRST_SEAL.json','MATHEMATICAL_SEAL.json']:
  seal=json.loads((F/name).read_bytes());times.append(datetime.datetime.fromisoformat(seal.get('sealed_utc',seal.get('sealed_at'))))
  if 'files' in seal:
   for row in seal['files']:bound(F,row)
  else:bound(F,{'path':seal['file'],'bytes':seal['bytes'],'sha256':seal['sha256']})
 ck(times[0]<times[1]<datetime.datetime.fromisoformat(root['root_math_sealed_utc']),'independent pre-root source/proof chronology '+family)
 if family=='clean_final_adversary':
  for row in json.loads((F/'FINAL_SEAL.json').read_bytes())['bindings']:bound(F,row)
 j=json.loads((F/receipt).read_bytes());records=j['checks'];ck(len(records)==j.get('check_count',j.get('checks_count'))==nchecks,'entire family receipt count '+family)
 for row in records:
  ck(isinstance(row,str) or isinstance(row,dict),'full typed receipt check '+family)
  if isinstance(row,dict) and 'pass' in row:ck(row['pass'] is True,'no failed receipt check '+family+'/'+row['check'])
 ck((j.get('status')=='PASS' if family!='clean_final_adversary' else j['verdict']=='PASS frozen packet; live acceptance pending'),'qualified frozen family outcome '+family)
 replays=j.get('replays',j.get('streams'));ck(len(replays)==10,'all10 stored complete replay pairs '+family)
 for e in replays:
  label=e['label'];parent=F if family=='descent_cohomology_review' else F/'replay_streams';out=(parent/(label+'.stdout')).read_bytes();err=(parent/(label+'.stderr')).read_bytes()
  ck(e.get('returncode',e.get('exit_code'))==0 and not err,'clean prior family replay '+family+'/'+label)
  ck(len(out)==e['stdout_bytes'] and sha(out)==e['stdout_sha256'] and len(err)==e['stderr_bytes'] and sha(err)==e['stderr_sha256'],'complete prior stream hashes '+family+'/'+label)
  ck(out==expected_stream(label),'entire root/family outputs equal '+family+'/'+label)
 rows=[]
 if family=='descent_cohomology_review':
  for e in json.loads((F/'SOURCE_ACQUISITION.json').read_bytes())['sources']:
   b=(F/'private/sources'/(e['id']+'.pdf')).read_bytes();ck(e['historical_match'] and len(b)==e['bytes']==e['actual_bytes'] and sha(b)==e['sha256']==e['actual_sha256'],'independent family original primary '+e['id']);rows.append(e)
 elif family=='residue_valuation_review':
  rows=json.loads((F/'PRIMARY_SOURCE_RECEIPT.json').read_bytes())['sources']+json.loads((F/'SUPPLEMENTARY_SOURCE_RECEIPT.json').read_bytes())['sources']
  for e in rows:
   b=(F/'private'/e['name']).read_bytes();ck(e['historical_match'] and len(b)==e['bytes'] and sha(b)==e['sha256'],'independent family primary '+e['name'])
 else:
  rows=json.loads((F/'SOURCE_DOWNLOAD_RECEIPT.json').read_bytes())
  for e in rows:
   b=(F/'private_sources'/e['name']).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'independent family primary '+e['name']);t0=datetime.datetime.fromisoformat(e['download_start_utc']);t1=datetime.datetime.fromisoformat(e['download_end_utc']);ck(t0<=t1<times[0],'actual download before baseline '+e['name'])
 ck(len(rows)==11 and {(e['url'],e['bytes'],e['sha256']) for e in rows}=={(e['url'],e['bytes'],e['sha256']) for e in root['primary_sources']},'all11 complete source identities '+family)
 r=subprocess.run([str(PY),'-B',str(F/program)],cwd=A/'tmp',env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True);(S/(family+'.stdout')).write_bytes(r.stdout);(S/(family+'.stderr')).write_bytes(r.stderr)
 ck(not r.returncode and not r.stderr,'new control clean replay '+family);ck(r.stdout==(F/output).read_bytes(),'complete new-control byte equality '+family);o=json.loads(r.stdout);ck(o['status']=='PASS' and o['exact_assertions']==ncontrols,'actual new-control count '+family)
 verifier='verify_family_manifest.py' if family=='descent_cohomology_review' else 'verify_manifest.py'
 v=subprocess.run([str(PY),'-B',str(F/verifier)],cwd=A/'tmp',capture_output=True);(S/(family+'_manifest.stdout')).write_bytes(v.stdout);(S/(family+'_manifest.stderr')).write_bytes(v.stderr);ck(not v.returncode and not v.stderr and json.loads(v.stdout)['status']=='PASS','original read-only manifest utility '+family)
 families.append({'family':family,'manifest_sha256':sha((F/'PUBLIC_MANIFEST.json').read_bytes()),'bound_files':count,'prior_receipt_sha256':sha((F/receipt).read_bytes()),'prior_check_count':nchecks,'all10_prior_full_output_pairs_equal_root':True,'fresh_primary_count':len(rows),'new_controls':ncontrols,'control_stdout_bytes':len(r.stdout),'control_stdout_sha256':sha(r.stdout),'complete_control_output':o,'manifest_verifier_output':json.loads(v.stdout)})
# Reproduce actual tamper negatives privately without touching the sealed family.
F=A/'clean_final_adversary';N=A/'tmp/root_drift02';N.mkdir(exist_ok=True);s=(F/'drift_negatives.py').read_text()
old="HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];CAND=HERE.parent/'snapshot/problems/30004320_laurent_descent';PYTHON=REPO/"
new=f"HERE=Path({str(N)!r});REPO=Path({str(R)!r});CAND=Path({str(D)!r});PYTHON=REPO/"
ck(s.count(old)==1,'exact private negative-program path adaptation');shadow=N/'drift_negatives.py';shadow.write_text(s.replace(old,new).replace("(HERE.parent/'snapshot'/Q)",f"(Path({str(A.resolve()/'snapshot')!r})/Q)"))
r=subprocess.run([str(PY),'-B',str(shadow)],cwd=N,capture_output=True);(S/'drift.stdout').write_bytes(r.stdout);(S/'drift.stderr').write_bytes(r.stderr);ck(not r.returncode and not r.stderr,'actual private drift-negatives clean replay')
x=json.loads((F/'DRIFT_NEGATIVES.json').read_bytes());y=json.loads(r.stdout);ck(x.keys()==y.keys() and x['negative_controls']==y['negative_controls']==14 and len(x['results'])==len(y['results'])==14,'all14 negative controls complete shape')
for key in x:
 if key not in ['utc','results']:ck(x[key]==y[key],'unchanged full negative metadata '+key)
for a,b in zip(x['results'],y['results']):
 ck(a.keys()==b.keys() and a['control']==b['control'] and a['rejected'] is b['rejected'] is True,'same complete negative record '+a['control'])
 for key in a:
  if key not in ['stderr_bytes','stderr_sha256']:ck(a[key]==b[key],'entire negative leaf '+a['control']+'/'+key)
 if 'exit_code' in a:
  label=a['control'];old=(F/(label+'.stderr')).read_bytes();cur=(N/(label+'.stderr')).read_bytes()
  ck(len(cur)==b['stderr_bytes'] and sha(cur)==b['stderr_sha256'] and len(old)==a['stderr_bytes'] and sha(old)==a['stderr_sha256'],'actual tamper complete stderr identities '+label)
  ck(old.replace(str(F/'private_controls').encode(),b'PRIVATE_CANDIDATE')==cur.replace(str(N/'private_controls').encode(),b'PRIVATE_CANDIDATE'),'entire tamper traceback equality after exact private root '+label)
ck(sum(f['new_controls'] for f in families)==13339,'all13339 distinct family mathematical controls')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'checks':checks,'families':families,'total_bound_family_files':119,'new_controls_total':13339,'negative_controls_replayed':14,'full_negative_output':y,'private_negative_program_sha256':sha(shadow.read_bytes()),'historical_source_reading_not_backdated':True,'novelty_current_open_human_review_certified':False,'original_problem_resolved':False,'live_acceptance_pending':True}
(A/'root_family_control_reproduction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','check_count','total_bound_family_files','new_controls_total','negative_controls_replayed']},indent=2))
