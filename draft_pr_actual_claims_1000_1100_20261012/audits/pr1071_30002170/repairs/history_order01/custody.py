"""Resolve source arrays and each historical locator without rewriting history."""
import collections,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';Q=A/'repairs/portability01';C=A/'repairs/case_alias01';T=A/'finalization/terminal_admin_20261015'
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def pin(p,n):return {'path':str(n),'bytes':p.stat().st_size,'sha256':sha(p)}
def matches(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r.get('bytes',r.get('size')) and sha(p)==r['sha256']
def rel(p):return str(p.relative_to(A)) if p.is_relative_to(A) else str(p)
def write(n,o):(D/n).write_text(json.dumps(o,indent=2)+'\n')
baseline=read(D/'BASELINE_INPUT_PINS.json')['records'];before={r['original_path']:r for r in read(D/'BEFORE_PINS.json')['records']};index=collections.defaultdict(list);changes=[];protected=[]
for r in baseline:
 if r['path'] in before:
  p=A/before[r['path']]['before_snapshot'];need(matches(p,r),'Before baseline '+r['path']);changes.append({'path':r['path'],'before':r,'before_snapshot':rel(p),'after':pin(A/r['path'],r['path'])})
 else:p=A/r['path'];need(matches(p,r),'Protected baseline '+r['path']);protected.append(r)
 index[(r['bytes'],r['sha256'])].append(p)
for r in read(P/'INPUT_COPY_MAP.json')['copies']:
 p=P/r['package_copy'];need(matches(p,r),'New copy pin');index[(r['bytes'],r['sha256'])].append(p)
def resolve(r,preferred):
 p=Path(preferred);p=p if p.is_absolute() else A/p
 if matches(p,r):return rel(p)
 options=index[(r.get('bytes',r.get('size')),r['sha256'])];need(bool(options),'No retained exact bytes '+str(preferred)+' '+str(r));p=options[0];need(matches(p,r),'Resolver exact check');return rel(p)
keys=['stage','captured_path','bytes','sha256'];project=lambda r:{k:r[k] for k in keys}
old=read(C/'HISTORICAL_STAGE_RESOLUTION.json');hist=read(Q/'HISTORICAL_STAGE_RESOLUTION.json')['records'];terminal=read(T/'HISTORICAL_STAGE_RESOLUTION.json')['records'];need(len(hist)==4346 and len(terminal)==len(old['records'])==2788,'History lengths')
sets=[('terminal_immediate_inputs',T/'BASELINE_INPUT_PINS.json','records'),('preparation_204',P/'FROZEN_INPUTS.json','records'),('preparation_92',P/'INPUT_OUTPUT_PINS.json','records'),('repair_492_before',A/'repairs/package01/BASELINE_INPUT_PINS.json','records'),('repair_34_outputs',A/'repairs/package01/OUTPUT_PINS.json','records'),('repair_270_current',A/'repairs/package01/CURRENT_OUTPUT_PINS.json','records'),('repair_480_unchanged',A/'repairs/package01/PROTECTED_UNCHANGED.json','unchanged_records'),('whole01_25_outputs',A/'reviews/package_01/OUTPUT_PINS.json','files'),('whole02_25_outputs',A/'reviews/package_02/OUTPUT_PINS.json','files'),('whole02_569_inputs',A/'reviews/package_02/INPUT_PINS.json','files')]
rows=[];cursor=0
for stage,source,key in sets:
 source_rows=read(source)[key];actual=[r for r in hist[:2788] if r['stage']==stage];need(len(source_rows)==len(actual),'Stage size')
 for source_index,(s,r) in enumerate(zip(source_rows,actual)):
  need((s['path'],s['bytes'],s['sha256'])==(r['captured_path'],r['bytes'],r['sha256']),'Actual original source row')
  need(project(r)==project(terminal[cursor])==project(old['records'][cursor]),'Original2788 ordered values')
  locators=[]
  for name in ['prior_resolution_path','resolved_path','portability_resolution_path']:
   if name in r:locators.append({'field':name,'captured_locator':r[name],'current_exact_resolution':resolve(r,r[name])})
  rows.append({'global_index':cursor,'source_manifest':rel(source),'source_row_index':source_index,**project(r),'locators':locators});cursor+=1
need(cursor==2788,'Original cursor')
for name in ['OUTPUT_PINS.json','CURRENT_AUDIT_PINS.json','CURRENT_CANDIDATE_PINS.json','PROTECTED_UNCHANGED.json']:
 source=T/name;source_rows=read(source)['records'];actual=[r for r in hist[2788:] if r['stage']==name];prior=[r for r in old['additional_terminal_rows'] if r['stage']==name];need(len(source_rows)==len(actual)==len(prior),'Later stage size')
 for source_index,(s,r,b) in enumerate(zip(source_rows,actual,prior)):
  need((s['path'],s['bytes'],s['sha256'])==(r['captured_path'],r['bytes'],r['sha256']),'Later actual source row');need(project(r)==project(b),'Per-stage order')
  locators=[]
  for name2 in ['prior_resolution_path','resolved_path','portability_resolution_path']:
   if name2 in r:locators.append({'field':name2,'captured_locator':r[name2],'current_exact_resolution':resolve(r,r[name2])})
  rows.append({'global_index':cursor,'source_manifest':rel(source),'source_row_index':source_index,**project(r),'locators':locators});cursor+=1
need(cursor==4346,'All historical rows')
a=list(map(project,old['additional_terminal_rows']));b=list(map(project,hist[2788:]));canon=lambda r:json.dumps(r,sort_keys=True,separators=(',',':'))
need(collections.Counter(map(canon,a))==collections.Counter(map(canon,b)),'Exact multiset')
mismatches=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(mismatches)==939 and mismatches[0]==30,'Actual global permutation')
qual=read(P/'HISTORY_ORDER_QUALIFICATION.json');need(qual['additional1558_global_order_preserved'] is False,'Current truth')
sig=lambda x:hashlib.sha256(canon(x).encode()).hexdigest();need(qual['before_projected_rows_sha256']==sig(a) and qual['after_projected_rows_sha256']==sig(b),'Current projection digests')
for r in qual['source_records']:need(matches(A/r['path'],r),'Original source qualification pin')
write('HISTORICAL_STAGE_RESOLUTION.json',{'utc':now(),'status':'PASS','original2788_global_values_and_order_preserved':True,'additional1558_global_order_preserved':False,'additional1558_exact_row_multiset_preserved':True,'additional1558_per_stage_values_and_order_preserved':True,'mismatched_global_additional_positions':939,'first_mismatch_additional_zero_based':30,'records':rows,'historical_false_claim_retained_byte_exact':True})
later=[]
for r in read(Q/'PRIOR_LATEST_INPUT_OUTPUT_PIN_RESOLUTION.json')['records']:
 src=A/r['source_manifest'];v=read(src);key=next(k for k in ['records','rows','files'] if k in v);s=v[key][r['row_index']]
 need((s['path'],s.get('bytes',s.get('size')),s['sha256'])==(r['captured_path'],r['bytes'],r['sha256']),'Later source/index mismatch')
 later.append({**r,'current_exact_resolution':resolve(r,r['resolved_path'])})
need(len(later)==3158,'3158 later pins')
write('PRIOR_LATER_PIN_RESOLUTION.json',{'utc':now(),'status':'PASS','records':later})
newer=[]
manifest_sets=[(Q/'BASELINE_INPUT_PINS.json',A,'rows','path'),(Q/'BEFORE_PINS.json',A,'rows','before_snapshot'),(Q/'PROTECTED_UNCHANGED.json',A,'records','path'),(Q/'CURRENT_AUDIT_PINS.json',A,'records','path'),(Q/'CURRENT_CANDIDATE_PINS.json',P,'records','path'),(Q/'OUTPUT_PINS.json',Q,'records','path'),(A/'reviews/package_04/FROZEN_INPUTS.json',A,'files','path'),(A/'reviews/package_04/OUTPUT_PINS.json',A/'reviews/package_04','files','path')]
for source,base,key,pathkey in manifest_sets:
 for i,r in enumerate(read(source)[key]):newer.append({'source_manifest':rel(source),'source_row_index':i,**r,'current_exact_resolution':resolve(r,base/r[pathkey])})
write('LATEST_STAGE_PIN_RESOLUTION.json',{'utc':now(),'status':'PASS','records':newer})
copyrows=read(P/'INPUT_COPY_MAP.json')['copies'];prior=read(D/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies'];need(len(copyrows)==153 and len(prior)==140 and copyrows[:140]==prior,'140 exact copy prefix')
prefixes=[]
for src,count in [(T/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json',83),(C/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json',116),(Q/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json',128)]:
 rr=read(src)['copies'];need(len(rr)==count and copyrows[:count]==rr,'Old exact prefix '+str(count));prefixes.append({'source':rel(src),'count':count,'values_and_order_exact':True})
actualcopies=[]
for r in copyrows:
 src=A/r.get('source_snapshot',r['original_path']);dst=P/r['package_copy'];need(matches(src,r) and matches(dst,r) and src.read_bytes()==dst.read_bytes(),'Actual source/copy '+r['package_copy']);actualcopies.append({**r,'actual_source':rel(src),'actual_source_and_copy_rehashed':True})
write('COPY_EQUALITY_RECHECK.json',{'utc':now(),'status':'PASS','prior140_values_and_order_exact':True,'earlier_prefixes':prefixes,'records':actualcopies})
omissions=[]
for name in ['WHOLE01_COPY_EXCLUSIONS.json','WHOLE02_COPY_EXCLUSIONS.json','CASE_ALIAS_COPY_EXCLUSIONS.json','PORTABILITY_COPY_EXCLUSIONS.json','HISTORY_ORDER_COPY_EXCLUSIONS.json']:
 for r in read(P/name)['records']:
  preferred=(A.parents[1] if r.get('base')=='program_root' else A)/r['path'];omissions.append({'ledger':name,**r,'current_exact_resolution':resolve(r,preferred)})
need(len(omissions)==74,'74 individual omissions')
write('INDIVIDUAL_OMISSIONS_RECHECK.json',{'utc':now(),'status':'PASS','records':omissions,'omitted_program_replay_claim':False})
submitted=read(A/'SUBMITTED_PINS.json');need(len(submitted['files'])==9,'Nine submitted')
for r in submitted['files']:need(matches(A/r['snapshot_path'],r),'Original submitted bytes')
ag=read(P/'FROZEN_INPUTS.json')['workspace_AGENTS'];need(matches(Path(ag['path']),ag),'Workspace instruction identity')
native=read(A/'publication/zenodo-deposit.json');metadata=read(P/'metadata.json');need(set(native)=={'metadata','files'} and native['metadata']==metadata==read(P/'metadata_wrapped.json')['metadata']==read(P/'deposit.json')['metadata'],'Native/bare/wrapper equality')
need(native['files']==[{'path':'../NEWpreprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../NEWpreprint_v1_0/PR1071_preprint_v1_0_support.zip','name':'PR1071_preprint_v1_0_support.zip'}],'Native file selection')
oldbinding=read(D/'before/NEWpreprint_v1_0/UPLOAD_BINDINGS.json');binding=read(P/'UPLOAD_BINDINGS.json');adjusted=json.loads(json.dumps(oldbinding));adjusted['archive']['bytes']=binding['archive']['bytes'];adjusted['archive']['sha256']=binding['archive']['sha256'];adjusted['manifest_sha256']=binding['manifest_sha256'];need(adjusted==binding,'More than three binding scalars changed')
write('CHANGE_INVENTORY.json',{'utc':now(),'authorized_existing_changes':changes,'all_new_paths_outside_effort':[pin(f,f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and D not in f.parents and str(f.relative_to(A)) not in {r['path'] for r in baseline}]})
write('PROTECTED_UNCHANGED.json',{'utc':now(),'records':protected})
summary={'utc':now(),'status':'PASS','baseline':len(baseline),'authorized_existing_changes':len(changes),'protected_unchanged':len(protected),'historical_rows':len(rows),'historical_locators_individually_resolved':sum(len(r['locators']) for r in rows),'prior_later_rows':len(later),'latest_stage_rows':len(newer),'copy_pairs':len(actualcopies),'original_prefixes':[83,116,128,140],'omissions':len(omissions),'native_and_metadata_unchanged':True,'original_nine_unchanged':True,'all_old_sealed_claims_unchanged':True}
write('CUSTODY_SUMMARY.json',summary);print(json.dumps(summary))
