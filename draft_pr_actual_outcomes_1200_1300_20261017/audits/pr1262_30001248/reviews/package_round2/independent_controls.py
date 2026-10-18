#!/usr/bin/env python3
"""New exact finite checks, actual schema controls and all-field kit POST guards."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
from collections import Counter
from math import comb
import argparse,copy,datetime,hashlib,importlib.util,json,os,subprocess,sys,types
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';S=R/'_local';S.mkdir(exist_ok=True)
def need(x,m):
 if not x:raise RuntimeError(m)
def load(p):
 spec=importlib.util.spec_from_file_location('review_'+p.stem,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def reject(fn,label):
 try:fn()
 except (ValueError,RuntimeError,KeyError,FileNotFoundError):return label
 raise RuntimeError('Bad input accepted '+label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def choose(n,k):return comb(n,k) if n>=k>=0 else 0
exact=[];strata=0;count=0
for n in [3,4,5]:
 edges=list(combinations(range(n),2));N=len(edges);index={e:i for i,e in enumerate(edges)}
 masks=[sum(1<<index[e] for e in combinations(v,2)) for v in combinations(range(n),3)]
 hist=Counter();ws={m:[] for m in range(N+1)}
 for g in range(1<<N):
  count+=1;present=[e for i,e in enumerate(edges) if g>>i&1];M=len(present);T=sum((g&t)==t for t in masks)
  degrees=[sum(v in e for e in present) for v in range(n)];W=sum(choose(d,2) for d in degrees)
  Y=sum(set(e).isdisjoint(f) for e,f in combinations(present,2));need(Y==choose(M,2)-W,'ordinary2K2');hist[M,T,Y]+=1;ws[M].append(W)
 for p in [F(3,7),F(2,3)]:
  sums=[F(0) for _ in range(4)]
  for (M,T,Y),c in hist.items():
   w=c*p**M*(1-p)**(N-M)
   for i,v in enumerate((T,T*T,Y,Y*Y)):sums[i]+=w*v
  tvar=sums[1]-sums[0]**2;yvar=sums[3]-sums[2]**2
  need(sums[0]==choose(n,3)*p**3,'trianglemean')
  want=choose(n,3)*p**3*(1-p**3)+12*choose(n,4)*p**5*(1-p)
  need(tvar==want,'truevariance');need(yvar==N*choose(n-2,2)**2*p**3*(1-p)+3*choose(n,4)*p**2*(1-p)**2,'disjointvariance')
  projection=N*(n-2)**2*p**5*(1-p);remainder=3*choose(n,3)*p**4*(1-p)**2+choose(n,3)*p**3*(1-p)**3
  need(tvar==projection+remainder,'orthogonality');exact.append({'n':n,'p':str(p),'triangle_variance':str(tvar),'disjoint_variance':str(yvar)})
 if n>=4:
  AA=N*(n-2);BB=AA*(4*n-10);need(BB-4*F(AA*AA,N)==-2*AA,'cancellation')
  for m,values in ws.items():
   def falling(x,j):
    r=1
    for i in range(j):r*=x-i
    return r
   q={j:F(falling(m,j),falling(N,j)) for j in [2,3,4]};mean=F(sum(values),len(values));var=F(sum(v*v for v in values),len(values))-mean*mean
   need(var==AA*(q[2]-q[4])+BB*(q[3]-q[4])+AA*AA*(q[4]-q[2]**2),'conditionalvariance');strata+=1
v=load(P/'verification/verify.py');c=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text());registry=c['authored_freezes'];checked=v.authenticate_nested_manifests(P/'verification',registry);need(len(checked)==13,'actual13registry')
reg=next(x for x in registry if x['base']=='reviews/fourier_adversary');obj=json.loads((P/'verification'/reg['path']).read_text());need(reg['entries_key']=='entries' and reg['path_key']=='relative_path' and reg['size_key']=='bytes','Fourieractualschema')
family=S/'schema'/'reviews/fourier_adversary';family.mkdir(parents=True,exist_ok=True)
for entry in obj['entries']:
 name=entry['relative_path'];q=family/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((P/'verification'/reg['base']/name).read_bytes())
# Poison every irrelevant path field, then supply a NEW test-manifest anchor.
for entry in obj['entries']:entry['path']='/absent/POISONED/READ_MUST_NOT_HAPPEN'
mp=family/'AUTHORED_MANIFEST.json';mp.write_text(json.dumps(obj));testreg={**reg,'sha256':sha(mp)}
v.authenticate_nested_manifests(S/'schema',[testreg],require_complete=False)
bad=copy.deepcopy(obj);bad['entries'][0]['relative_path']='/outside';mp.write_text(json.dumps(bad));testreg['sha256']=sha(mp)
schema_reject=reject(lambda:v.authenticate_nested_manifests(S/'schema',[testreg],require_complete=False),'selected_absolute_relative_path_rejected')
# Independently ensure exact parsed wrappers and current prose contracts.
for name in v.STRUCTURED:
 current=json.loads((A/'current_edition'/name).read_text());need(current['schema']=='triangle-modular-threshold-current-v3','v3schema');need(current['historical_submitted_record_20261011']==json.loads((A/'submitted'/name).read_text()),'historicalwrapper');need(current==c['structured_records'][name],'contextrecord')
for name,text in c['edition_text'].items():need((A/'current_edition'/name).read_text()==text,'contextprose')
metadata=json.loads((P/'zenodo-deposit.json').read_text())['metadata'];need(metadata==c['metadata'] and len(metadata)==11,'actual11metadata')
coordinator=load(A.parents[1]/'publication_coordinators/pr1262.py');kit=coordinator.load_exact_kit();kit.STATE_DIR=S/'own-kit-state';kit.STATE_DIR.mkdir(exist_ok=True);kit.doi_status=lambda doi:{'status':'resolved','http_status':200}
manifest=P/'zenodo-deposit.json';meta,files=kit.load_manifest(manifest);statepath=kit.state_path(manifest.resolve(),'production');kit.save_state(statepath,{'manifest':str(manifest.resolve()),'environment':'production','id':345})
base={'id':345,'submitted':False,'metadata':copy.deepcopy(meta),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']} for f in files]};events=[]
class Client:
 def __init__(self,d):self.d=d
 def get(self,i):events.append('GET '+str(i));return copy.deepcopy(self.d)
 def publish(self,i):events.append('POST '+str(i));raise RuntimeError('POST must not be called for corrupted metadata')
rejections=[]
for key in meta:
 bad=copy.deepcopy(base);bad['metadata'][key]=None;events.clear()
 try:kit.run(argparse.Namespace(command='publish',manifest=manifest,sandbox=False,confirm_id=345,check_doi=False),client=Client(bad))
 except kit.DepositError:pass
 else:raise RuntimeError('all-field pre-POST guard failed '+key)
 need(events==['GET 345'],'mutation before exact verification');rejections.append(key)
# Narrow shared-kit normalization must also be blocked in the actual coordinator wrapper.
normal=copy.deepcopy(base);normal['metadata']['creators']=[{k:val for k,val in x.items() if k!='affiliation'} for x in meta['creators']]
# Actual explicit affiliation differs substantively and must reject.
try:kit.verify(normal,meta,files)
except kit.DepositError:pass
else:raise RuntimeError('creator field deletion accepted')
# Canonical same-ID validation is still needed when all supplied metadata matches.
wrong=copy.deepcopy(base);wrong['id']=346;events.clear()
try:kit.run(argparse.Namespace(command='publish',manifest=manifest,sandbox=False,confirm_id=345,check_doi=False),client=Client(wrong))
except kit.DepositError:pass
else:raise RuntimeError('wrong deposition ID accepted')
need(events==['GET 345'],'wrong ID mutation')
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','own_exhaustive_graphs':count,'exact_cases':exact,'conditional_strata':strata,'actual_registry_members':checked,'Fourier_unused_absolute_path_poison_ignored':True,'selected_path_negative_control':schema_reject,'current_v3_wrappers_exact':True,'metadata_all_eleven_equal_context':True,'each_supplied_field_rejected_before_actual_kit_POST':rejections,'same_ID_required_before_actual_kit_POST':True,'services':'Actual kit.run with mocked client only; state redirected to own scratch. No token read, service request, Git mutation or real gate.'}
(R/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','graphs':count,'conditional_strata':strata,'metadata_fields':len(rejections)}))
