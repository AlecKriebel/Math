import json,hashlib,datetime,collections
from pathlib import Path
ROOT=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170');O=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/root_reproduction/whole04_20261016');P=ROOT/'NEWpreprint_v1_0';Q=ROOT/'repairs/portability01'
def load(p):return json.loads(p.read_text())
def need(c,s):
 if not c:raise RuntimeError(s)
def match(p,r):
 return p.is_file() and p.stat().st_size==r.get('bytes',r.get('size')) and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
def save(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
frozen=load(Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/reviews/package_04/FROZEN_INPUTS.json'))['files'];index=collections.defaultdict(list)
for r in frozen:
 need(match(ROOT/r['path'],r),'Review baseline changed '+r['path']);index[(r['bytes'],r['sha256'])].append(r['path'])
def locate(r,preferred=None):
 if preferred is not None and match(preferred,r):return str(preferred.relative_to(ROOT)) if preferred.is_relative_to(ROOT) else str(preferred)
 key=(r.get('bytes',r.get('size')),r['sha256']);need(bool(index[key]),'No retained exact bytes '+str(r));return index[key][0]
# Derive each original stage from its own immutable source array.
sets=[('terminal_immediate_inputs','finalization/terminal_admin_20261015/BASELINE_INPUT_PINS.json','records'),('preparation_204','NEWpreprint_v1_0/FROZEN_INPUTS.json','records'),('preparation_92','NEWpreprint_v1_0/INPUT_OUTPUT_PINS.json','records'),('repair_492_before','repairs/package01/BASELINE_INPUT_PINS.json','records'),('repair_34_outputs','repairs/package01/OUTPUT_PINS.json','records'),('repair_270_current','repairs/package01/CURRENT_OUTPUT_PINS.json','records'),('repair_480_unchanged','repairs/package01/PROTECTED_UNCHANGED.json','unchanged_records'),('whole01_25_outputs','reviews/package_01/OUTPUT_PINS.json','files'),('whole02_25_outputs','reviews/package_02/OUTPUT_PINS.json','files'),('whole02_569_inputs','reviews/package_02/INPUT_PINS.json','files')]
hist=load(Q/'HISTORICAL_STAGE_RESOLUTION.json')['records'];base=load(ROOT/'finalization/terminal_admin_20261015/HISTORICAL_STAGE_RESOLUTION.json')['records'];old=load(ROOT/'repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json');rows=[];cursor=0
for stage,src,key in sets:
 a=load(ROOT/src)[key];actual=[r for r in hist if r['stage']==stage]
 need(len(a)==len(actual),'history stage size')
 for r,h in zip(a,actual):
  need((r['path'],r['bytes'],r['sha256'])==(h['captured_path'],h['bytes'],h['sha256']),'source history mismatch')
  b=base[cursor];need(all(h[k]==b[k] for k in ['stage','captured_path','bytes','sha256']),'original history order')
  rows.append({'stage':stage,'source_manifest':src,'source_row_index':cursor,'captured_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'fresh_resolution':locate(r,ROOT/h['portability_resolution_path'])});cursor+=1
need(cursor==2788 and len(base)==2788,'2788 count')
# Added terminal stages derive from real arrays, not a reported status.
for name in ['OUTPUT_PINS.json','CURRENT_AUDIT_PINS.json','CURRENT_CANDIDATE_PINS.json','PROTECTED_UNCHANGED.json']:
 a=load(ROOT/'finalization/terminal_admin_20261015'/name)['records'];actual=[r for r in hist[2788:] if r['stage']==name]
 need(len(a)==len(actual),'additional stage size')
 for r,h in zip(a,actual):
  need((r['path'],r['bytes'],r['sha256'])==(h['captured_path'],h['bytes'],h['sha256']),'additional source mismatch')
  rows.append({'stage':name,'captured_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'fresh_resolution':locate(r,ROOT/h['portability_resolution_path'])})
need(len(rows)==len(hist)==4346,'4346 count')
need(len(old['additional_terminal_rows'])==1558,'1558 count')
order_mismatches=[{'index':i,'before':{k:a[k] for k in ['stage','captured_path','bytes','sha256']},'after':{k:b[k] for k in ['stage','captured_path','bytes','sha256']}} for i,(a,b) in enumerate(zip(old['records']+old['additional_terminal_rows'],hist)) if any(a[k]!=b[k] for k in ['stage','captured_path','bytes','sha256'])]
need(all(r['index']>=2788 for r in order_mismatches),'original2788 order differs')
save('HISTORICAL_ORDER_COUNTEREXAMPLE.json',{'declared_additional1558_values_and_order_preserved':True,'actual_additional_global_order_preserved':not order_mismatches,'mismatched_positions':len(order_mismatches),'before_source':'repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json/additional_terminal_rows','after_source':'repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json/records[2788:]','first_differences':order_mismatches[:6],'note':'Per-stage value/order preservation is checked separately against the actual terminal source arrays; this comparison addresses the unqualified global order-preservation field.'})
# Every newer pin source row is looked up independently and all bytes freshly hashed.
later=load(Q/'PRIOR_LATEST_INPUT_OUTPUT_PIN_RESOLUTION.json')['records'];laterout=[]
for r in later:
 a=load(ROOT/r['source_manifest']);key=next(k for k in ['records','rows','files'] if k in a);b=a[key][r['row_index']]
 need((b['path'],b.get('bytes',b.get('size')),b['sha256'])==(r['captured_path'],r['bytes'],r['sha256']),'later pin source mismatch')
 preferred=Path(r['resolved_path']);preferred=preferred if preferred.is_absolute() else ROOT/preferred
 laterout.append({**r,'fresh_resolution':locate(r,preferred)})
need(len(laterout)==3158,'3158 later refs')
copyrows=load(P/'INPUT_COPY_MAP.json')['copies'];before=load(Q/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies'];need(len(copyrows)==140 and len(before)==128 and copyrows[:128]==before,'copy prefix/order')
copies=[]
for r in copyrows:
 s=ROOT/r.get('source_snapshot',r['original_path']);d=P/r['package_copy'];need(match(s,r) and match(d,r) and s.read_bytes()==d.read_bytes(),'source-copy exact equality')
 copies.append({**r,'actual_source':str(s.relative_to(ROOT)),'source_and_copy_rehashed':True})
om=[]
for name in ['WHOLE01_COPY_EXCLUSIONS.json','WHOLE02_COPY_EXCLUSIONS.json','CASE_ALIAS_COPY_EXCLUSIONS.json','PORTABILITY_COPY_EXCLUSIONS.json']:
 for r in load(P/name)['records']:
  preferred=(ROOT.parents[1] if r.get('base')=='program_root' else ROOT)/r['path']
  om.append({'ledger':name,**r,'fresh_resolution':locate(r,preferred)})
need(len(om)==72,'72 individually omitted')
# Bounded change audit independently resolves every baseline and every authorized before.
entry=load(Q/'BASELINE_INPUT_PINS.json')['rows'];before=load(Q/'BEFORE_PINS.json')['rows'];bymap={r['original_path']:r for r in before};unch=[];changes=[]
for r in entry:
 if r['path'] in bymap:
  b=bymap[r['path']];need(match(ROOT/b['before_snapshot'],r),'before snapshot bytes');changes.append(r['path'])
 else:need(match(ROOT/r['path'],r),'protected baseline bytes');unch.append(r['path'])
need(len(entry)==763 and len(changes)==9 and len(unch)==754,'bounded change counts')
# Independently authenticate original nine via retained actual-object receipts; NO new Git call.
git=load(ROOT/'reviews/package_03/ACTUAL_GIT_NINE.json');submitted=load(ROOT/'SUBMITTED_PINS.json')['files'];need(len(git['rows'])==len(submitted)==9,'nine original rows')
for a,b in zip(git['rows'],submitted):
 need(a['repository_path']==b['repository_path'] and a['snapshot_path']==b['snapshot_path'] and a['sha256']==b['sha256'] and a['bytes']==b['bytes'] and a['returncode']==0 and a['same_bytes'] is True and match(ROOT/b['snapshot_path'],b),'retained Git-nine custody')
# All frozen original file identities, history statuses and seals remain unmodified.
ag=load(P/'FROZEN_INPUTS.json')['workspace_AGENTS'];need(match(Path(ag['path']),ag),'AGENTS pin')
save('CUSTODY_RECHECK.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','frozen_regular_inputs':len(frozen),'candidate_regular_files':sum(1 for p in P.rglob('*') if p.is_file()),'source_copy_pairs':copies,'original128_copy_prefix_exact':True,'historical_rows':rows,'later_pin_rows':laterout,'individual_omissions':om,'bounded_repair':{'baseline':len(entry),'authorized_changed':changes,'protected_unchanged':len(unch)},'original_nine':{'retained_actual_Git_receipt_reauthenticated':True,'fresh_Git_called':False,'head':git['head']},'workspace_AGENTS_rehashed':True})
print(json.dumps({'status':'PASS','frozen':len(frozen),'copies':len(copies),'history':len(rows),'later':len(laterout),'omissions':len(om),'baseline':len(entry),'changes':len(changes),'protected':len(unch)}))
