"""Fresh INERT boundary and time controls; no actual final evidence or authority."""
from pathlib import Path
import json,hashlib,base64,copy
W=Path(__file__).resolve().parent
def load(name,h):
 p=W/name;b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h
 n={'__file__':str(p),'__name__':'_inert_'+name};exec(compile(b,str(p),'exec',optimize=0),n);return n
I=load('independent_checks.py','63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a')
T=load('actual_final_timestamp_checks.py','4e6fae5a1c4bfacb69a65b347ad1ad2f5c063d7b2848d6a0c1f8f05fd607d003')
n=I['frozen_join']();v=n['baseline']();full=n['frozen_prior_nodes']();C=I['C'];H=I['H'];need=I['need'];results=[]
registry={};counter=[0];oldpin=n['objpin']
def mp(obj):
 counter[0]+=1;key='INERT_BOUNDARY_MODEL:'+str(counter[0]);registry[key]=copy.deepcopy(obj);return {'path':key,'bytes':len(C(obj)),'sha256':H(C(obj))}
def op(pin):
 if pin['path'].startswith('INERT_BOUNDARY_MODEL:'):
  o=registry[pin['path']];need(len(C(o))==pin['bytes']and H(C(o))==pin['sha256'],'Inert model pin');return copy.deepcopy(o)
 return oldpin(pin)
n['objpin']=op
def envelope(obj,url):return {'method':'GET','url':url,'status':200,'raw_body_base64':base64.b64encode(C(obj)).decode(),'raw_sha256':H(C(obj))}
def model(highest):
 registry.clear();counter[0]=0
 d={k:{a:q.get(a)for a in ['number','title','body','head','state','draft','merged_at','merge_commit_sha']}for k,q in full.items()if k<=highest}
 if highest>1446:
  d[highest]={'number':highest,'title':'INERT NEW FULL CLAIM','body':'INERT boundary claim only.','head':{'sha':'0'*40},'state':'open','draft':True,'merged_at':None,'merge_commit_sha':None}
 a=[d[k]for k in sorted(d)];pages=[]
 for start in range(0,len(a),100):pages.append(mp(envelope(a[start:start+100],'https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=asc&per_page=100&page='+str(len(pages)+1))))
 pages.append(mp(envelope([],'https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=asc&per_page=100&page='+str(len(pages)+1))))
 newest=mp(envelope([d[max(d)]],'https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=desc&per_page=1'))
 p={'final_inventory':{'pages':pages,'newest':newest,'observed_at':'INERT_MODEL_ONLY'}}
 root=mp({'kind':'ROOT_ADOPTED_FINAL_JOIN_OVERLAY','all_native_receipts_reviewed':True,'payload_sha256':H(C(p))})
 return n['apply_overlay'](v,mp({'schema':'root-adopted-final-join-overlay-v1','payload':p,'root_adoption':root}))
for highest in [1447,1701]:
 r=model(highest);prs={x['pr']for x in r['unresolved_new_changed_or_gap_claims']}
 need(r['highest_inventory_observed_dated']==highest and highest in prs and 1447 in prs and r['final_observations_current']is False,'New/highest claims must not be skipped or truncated')
 results.append({'inert_case':'new_higher_'+str(highest),'highest_retained':highest,'unresolved_count':len(prs),'final_current':False})
try:model(1445)
except RuntimeError as e:results.append({'inert_case':'highest_regression','rejected':True,'error':str(e)})
else:raise RuntimeError('Highest regression accepted')
# Timestamp-only seam, independent of native data validation already tested in50 controls.
roles=['metadata_before','values','formulas','metadata_after'];names=['START.json','NATIVE_JOIN_ORIGINAL_TRANSPORT.json','NATIVE_INDEPENDENT_FOUNDATION_ORIGINAL_TRANSPORT.json','HISTORICAL_DEDUPLICATION_AND_FAMILY_COUNTS.json']
def clock_model(mut=None):
 e={role:{'before':'2026-10-22T00:00:0'+str(i*2+1)+'+00:00','after':'2026-10-22T00:00:0'+str(i*2+2)+'+00:00'}for i,role in enumerate(roles)}
 pins={role:{'path':str(W/name),'bytes':1,'sha256':'INERT_ONLY'}for role,name in zip(roles,names)}
 l={'original_transports':pins,'observed_at':'2026-10-22T00:00:09+00:00'}
 if mut:mut(e,pins,l)
 index={pin['path']:e[role]for role,pin in pins.items()}
 T['I']['final_ingress']=lambda p:{'status':'INERT_TIMESTAMPS_ONLY_NOT_ACTUAL_INGRESS'}
 T['I']['objpin']=lambda p:({'payload':{'final_ledger':l}}if p['path']=='INERT_CLOCK_OVERLAY'else copy.deepcopy(index[p['path']]))
 return T['check']({'path':'INERT_CLOCK_OVERLAY','bytes':1,'sha256':'INERT_ONLY'})
r=clock_model();need(r['strict_original_brackets_verified']is True,'Inert chronological positive')
results.append({'inert_case':'four_chronological_original_times','accepted':True,'actual_final_ingress':False})
attacks=[
 ('missing_before',lambda e,p,l:e['values'].pop('before')),
 ('missing_after',lambda e,p,l:e['values'].pop('after')),
 ('naive_time',lambda e,p,l:e['values'].update(before='2026-10-22T00:00:03')),
 ('non_UTC_time',lambda e,p,l:e['values'].update(before='2026-10-22T01:00:03+01:00')),
 ('negative_duration',lambda e,p,l:e['values'].update(after='2026-10-22T00:00:02+00:00')),
 ('overlapping_brackets',lambda e,p,l:e['formulas'].update(before='2026-10-22T00:00:03+00:00')),
 ('observation_before_finish',lambda e,p,l:l.update(observed_at='2026-10-22T00:00:07+00:00')),
 ('future_observation',lambda e,p,l:l.update(observed_at='2999-01-01T00:00:00+00:00')),
 ('duplicate_original_file',lambda e,p,l:p['metadata_after'].update(path=p['metadata_before']['path']))]
for name,fn in attacks:
 try:clock_model(fn)
 except Exception as e:results.append({'inert_case':name,'rejected':True,'error':repr(e)})
 else:raise RuntimeError('Clock control accepted '+name)
print(json.dumps({'status':'PASS_FRESH_HIGHER_BOUNDARY_AND_TIMESTAMP_MODELS','count':len(results),'results':results,'actual_service_effects':0,'actual_final_inputs_tested':False,'actual_receipt_or_authority_files_created':False},indent=2,sort_keys=True))
