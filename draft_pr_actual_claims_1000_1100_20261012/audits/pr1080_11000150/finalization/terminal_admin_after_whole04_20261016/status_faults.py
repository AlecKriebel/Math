#!/usr/bin/env python3
"""Coherently rehashed and closed-repacked current status/evidence faults."""
from pathlib import Path
import copy,datetime,hashlib,io,json,subprocess,sys,zipfile
W=Path(__file__).resolve().parent;K=W/'scratch/clean_check/verification_kit';rows=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise RuntimeError(s)
def js(v):return (json.dumps(v,indent=2)+'\n').encode()
initial={p.relative_to(K).as_posix():p.read_bytes() for p in K.rglob('*') if p.is_file()};names=sorted(initial)
status_name='CURRENT_TERMINAL_AFTER_WHOLE04.json';s=json.loads(initial[status_name]);cases=[]
for field,value,needle in [('whole_reviews_completed',3,'complete review count'),('minimum_whole_reviews',1,'complete review count'),('latest_complete_review','whole03','latest findings'),('latest_review_actionable_counts',{'P0':0,'P1':0,'P2':0,'P3':1},'latest findings'),('root_whole04_adopted',False,'adopted complete review boundary'),('root_archive_wording_repair01_adopted',False,'adopted complete review boundary'),('new_complete_review_required',True,'adopted complete review boundary'),('root_integrity_adoption_required',False,'publication/service boundary'),('root_integrity_adopted',True,'publication/service boundary'),('publication_ready',True,'publication/service boundary'),('issues_resolved',True,'publication/service boundary'),('published',True,'publication/service boundary'),('services_held_at',1080,'publication/service boundary'),('full_original_maximum_classification_bundle','RESOLVED','scope boundary'),('exact_application_priority','CONFIRMED','scope boundary')]:
 v=copy.deepcopy(s);v[field]=value;cases.append(('status-'+field,status_name,v,needle))
vname=s['whole04_verdict'];v=json.loads(initial[vname]);v['findings']=[{'priority':'P3','description':'Injected semantic evidence fault'}];cases.append(('verdict-nonzero-findings',vname,v,'captured whole04 evidence differs'))
aname=s['root_whole04_adoption'];v=json.loads(initial[aname]);v['finding_counts']['P3']=1;cases.append(('ROOT-adoption-nonzero-findings',aname,v,'captured root whole04 adoption differs'))
try:
 for opt in [False,True]:
  prefix=[sys.executable,'-I','-B']+(['-O'] if opt else [])
  for label,name,value,needle in cases:
   altered=dict(initial);altered[name]=js(value)
   # Coherent fault evidence: update every stage/history content pin naming this changed delivered member.
   for ledger,key in [('REPAIR01_STAGE_COPIES.json','files'),('REPAIR01_HISTORY_RESOLUTION.json','references')]:
    v=json.loads(initial[ledger]);changed=False
    for r in v[key]:
     if r.get('destination')==name:r['bytes']=len(altered[name]);r['sha256']=sha(altered[name]);changed=True
    if changed:altered[ledger]=js(v)
   manifest=json.loads(initial['MANIFEST.json'])
   for r in manifest['files']:r['bytes']=len(altered[r['path']]);r['sha256']=sha(altered[r['path']])
   altered['MANIFEST.json']=js(manifest)
   buffer=io.BytesIO()
   with zipfile.ZipFile(buffer,'w',compression=0) as z:
    for n in names:
     i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;z.writestr(i,altered[n])
   packed=buffer.getvalue()
   with zipfile.ZipFile(io.BytesIO(packed)) as z:
    need(z.testzip() is None and all(z.read('verification_kit/'+n)==altered[n] for n in names),'Closed coherent fault ZIP')
    need(z.namelist()==['verification_kit/'+n for n in names] and not z.comment and all(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==0 and not i.extra and not i.comment and i.flag_bits==0 for i in z.infolist()),'Closed fault ZIP complete headers')
   changed=[n for n in names if altered[n]!=initial[n]]
   for n in changed:(K/n).write_bytes(altered[n])
   result=subprocess.run(prefix+[str(K/'verify.py')],capture_output=True,text=True,timeout=120)
   r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'optimized':opt,'argv':prefix+[str(K/'verify.py')],'returncode':result.returncode,'expected_success':False,'stdout':result.stdout,'stderr':result.stderr,'coherent_manifest':True,'all_member_payloads_verified_against_closed_fault_ZIP':True,'fault_archive':{'bytes':len(packed),'sha256':sha(packed)},'changed_members':changed}
   rows.append(r)
   with (W/'STATUS_SEMANTIC_RECEIPTS.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
   for n in changed:(K/n).write_bytes(initial[n])
   need(result.returncode!=0 and needle in result.stderr,'Wrong status semantic rejection '+label)
finally:
 for n,b in initial.items():
  if (K/n).read_bytes()!=b:(K/n).write_bytes(b)
need({p.relative_to(K).as_posix():sha(p.read_bytes()) for p in K.rglob('*') if p.is_file()}=={n:sha(b) for n,b in initial.items()},'Extracted fixture restoration')
(W/'STATUS_SEMANTIC_RESULTS.json').write_text(json.dumps({'status':'PASS','actual_commands':len(rows),'independent_faults':len(cases),'both_modes':True,'all_faults_coherently_rehashed_and_closed_repacked':True,'all_inputs_restored':len(initial)},indent=2)+'\n');print((W/'STATUS_SEMANTIC_RESULTS.json').read_text())
