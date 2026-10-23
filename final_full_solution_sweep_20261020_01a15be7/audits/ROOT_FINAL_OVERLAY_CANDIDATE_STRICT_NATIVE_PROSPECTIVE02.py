from pathlib import Path
import json,gzip,lzma,hashlib,datetime,base64,os
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';D=A/'root_final_actual_join_overlay01';Q=A/'root_final_actual_inventory_and_numeric43_01';J=A/'final_reconciliation_join_preparation01';W=A/'final_reconciliation_new_independent_adversary01'
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':H(b)}
def load(p,h):
 b=p.read_bytes();assert H(b)==h
 n={'__file__':str(p),'__name__':'_root_final_overlay_'+p.stem};exec(compile(b,str(p),'exec',optimize=0),n);return n
def obj(p):
 b=Path(p['path']).read_bytes();assert len(b)==p['bytes']and H(b)==p['sha256']
 return json.loads(gzip.decompress(b)if p['path'].endswith('.gz')else lzma.decompress(b)if p['path'].endswith('.xz')else b)
jn=load(J/'join_readonly.py','612b8e085f388e133e94a4c87cc3514e69d0f2931cec5999809f80d7ffaf0b1d')
jn['verify_closed']('620f22164fe099650f31196258b55ab21fc52b8da0c6a8c0912c875fe2816417');prior=jn['frozen_prior_nodes']();baseline=jn['baseline']()
collectionp=Q/'ROOT_COMPLETE_ACTUAL_FINAL_COLLECTION.json.gz';collection=obj(pin(collectionp))
assert collection['kind']=='ROOT_ACTUAL_FINAL_NATIVE_COLLECTION_COMPLETE_NOT_COVERAGE_ADOPTION'and collection['actual_service_effects']==0
ledger=collection['final_ledger'];inventory=collection['final_inventory']
strict=load(W/'independent_checks.py','63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a')
sheet=obj(ledger['snapshot']);details=strict['strict_sheet'](sheet);assert len(sheet['values'])==287
roles=ledger['original_transports'];assert set(roles)=={'metadata_before','values','formulas','metadata_after'}
raws={k:strict['raw_cli'](obj(p),k,details)for k,p in roles.items()}
assert strict['typed'](raws['metadata_before'],raws['metadata_after'])and strict['typed'](raws['metadata_before'],sheet['metadata'])
assert strict['typed'](raws['values'],sheet['value_raw'])and strict['typed'](raws['formulas'],sheet['formula_raw'])
last=None;inodes=set()
for role in ['metadata_before','values','formulas','metadata_after']:
 p=roles[role];v=obj(p);start=datetime.datetime.fromisoformat(v['before']);end=datetime.datetime.fromisoformat(v['after'])
 assert start.tzinfo is not None and start.utcoffset()==datetime.timedelta(0)and end.utcoffset()==datetime.timedelta(0)and start<=end and(last is None or last<=start)
 last=end;st=Path(p['path']).lstat();inodes.add((st.st_dev,st.st_ino))
assert len(inodes)==4 and last<=datetime.datetime.fromisoformat(ledger['observed_at'])<=datetime.datetime.now(datetime.timezone.utc)
ih=load(W/'strict_inventory_native_ingress.py','f68e9b43367bc35302ccf8d1f069890fa3195bdbfa1ec49279b7fb0a14497aba')
nodes={};chron=[];last=None;lastnum=0;lastcreated=None
for index,p in enumerate(inventory['pages']):
 values,start,end=ih['native'](obj(p),ih['ASC']+str(index+1));assert last is None or last<=start;last=end
 assert type(values)is list and len(values)<=100 and(bool(values)if index<len(inventory['pages'])-1 else values==[])
 if index<len(inventory['pages'])-2:assert len(values)==100
 for v in values:
  n=ih['node'](v);created=ih['utc'](v['created_at']);assert n not in nodes and n>lastnum and(lastcreated is None or lastcreated<=created)
  nodes[n]=v;lastnum=n;lastcreated=created
 chron.append({'page':index+1,'nodes':len(values),'before':start.isoformat(),'after':end.isoformat(),'input':p})
newest,start,end=ih['native'](obj(inventory['newest']),ih['NEW']);assert len(newest)==1 and start>=last
highest=ih['node'](newest[0]);assert highest==max(nodes)and highest>=1446 and jn['identity'](newest[0])==jn['identity'](nodes[highest])
assert end<=ih['utc'](inventory['observed_at'])<=datetime.datetime.now(datetime.timezone.utc)
deltas=[];administrative_changes=[]
for n in range(9,highest+1):
 if n not in nodes:deltas.append({'pr':n,'kind':'numeric_gap'})
 elif n not in prior:deltas.append({'pr':n,'kind':'new_PR','identity':jn['identity'](nodes[n])})
 else:
  old=jn['identity'](prior[n]);new=jn['identity'](nodes[n])
  if any(old[k]!=new[k]for k in ['head','title','body_sha256']):deltas.append({'pr':n,'kind':'changed_claim','previous':old,'current':new})
  if any(old[k]!=new[k]for k in ['state','draft','merge_commit']):administrative_changes.append({'pr':n,'previous':{k:old[k]for k in ['state','draft','merge_commit']},'current':{k:new[k]for k in ['state','draft','merge_commit']},'reopened_claim_requires_closure_policy_recheck':new['state']=='OPEN'and old['state']!='OPEN'})
existingp=R/'EXISTING_PUBLICATION_REMAINING34_RECONCILIATION.json';pubp=R/'PR1131_PUBLICATION_VERIFICATION.json';ex=json.loads(existingp.read_bytes());pub=json.loads(pubp.read_bytes())
assert ex['complete']is True and ex['new_publications']==0 and ex['new_rows']==34 and ex['after_rows']==286
assert pub['complete']is True and pub['pr']==1131 and pub['ledger_row']==287
def predicates(v):
 out=[{'pointer':'/complete','equals':True}]
 for k,value in v.get('required_native_checks',{}).items():
  assert value is True,'Material native completion condition unresolved '+k
  out.append({'pointer':'/required_native_checks/'+k.replace('~','~0').replace('/','~1'),'equals':True})
 assert len(out)>1
 return out
rows=ex['exact_rows'];assert len(rows)==34
frozen=baseline['pending_family_obligations'];by_family={v['family_pr']:v for v in rows}
assert len(by_family)==34 and set(by_family)=={v['family_pr']for v in frozen}
assert {v['ledger_row']for v in rows}==set(range(253,287))
original_inputs=json.loads(lzma.decompress((J/'private/LOCAL_ORIGINAL_INPUTS.json.xz').read_bytes()))
old_sheet=obj(next(p for p in original_inputs['external_pins']if p['path'].endswith('/AFTER_COMPLETE_SHEET.json')))
assert strict['typed'](sheet['values'][:252],old_sheet['values'])and strict['typed'](sheet['formulas'][:252],old_sheet['formulas'])
for index,f in enumerate(frozen,253):
 v=by_family[f['family_pr']];literal=f['literal_four_cells'];lr=v['ledger_row']
 assert lr==index and type(lr)is int
 assert v['literal_four_cells_sha256']==f['literal_four_cells_sha256']==H(C(literal))
 assert v['associated_prs']==f['associated_prs']and v['cells']==literal
 assert strict['typed'](sheet['values'][lr-1][:4],literal)and strict['typed'](sheet['formulas'][lr-1][:4],literal)
 assert sum(strict['typed'](row[:4],literal)for row in sheet['values'])==1
 if f['selected_C_DOI']:assert jn['one_doi'](sheet['values'],f['selected_C_DOI'])==lr
assert type(pub['record'])is int and pub['record']>0 and jn['norm'](pub['doi'])=='10.5281/zenodo.'+str(pub['record'])
assert jn['one_doi'](sheet['values'],pub['doi'])==287
assert type(pub['ledger_new_four_literal_cells'])is list and len(pub['ledger_new_four_literal_cells'])==4
assert strict['typed'](sheet['values'][286][:4],pub['ledger_new_four_literal_cells'])and strict['typed'](sheet['formulas'][286][:4],pub['ledger_new_four_literal_cells'])
live_pub=jn['identity'](nodes[1131])
assert live_pub['state']=='MERGED'and live_pub['head']==pub['integrated_head']=='9601e1e768c94522bc8ad105db4dfae4770bad75'
assert live_pub['merge_commit']==pub['merge_commit']=='67915a3df87d3bdd19be74ac04b1a39fd0ce89f3'
payload={'final_ledger':ledger,'completion_outcomes':[{'kind':'remaining34_actual_recorded','receipt':pin(existingp),'required_native_checks':predicates(ex)+[{'pointer':'/new_publications','equals':0},{'pointer':'/after_rows','equals':286}],'rows':[{'family_pr':v['family_pr'],'ledger_row':v['ledger_row'],'literal_four_cells_sha256':v['literal_four_cells_sha256']}for v in rows]},{'kind':'PR1131_actual_published_recorded','receipt':pin(pubp),'required_native_checks':predicates(pub)+[{'pointer':'/pr','equals':1131},{'pointer':'/ledger_row','equals':287}]}],'final_inventory':inventory,'claim_reconciliations':[],'numeric_gap_reconciliations':[]}
assert not D.exists();D.mkdir(mode=0o700)
def save(name,v):
 b=(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
 assert sum(x.lstat().st_blocks*512 for x in[D,*D.rglob('*')])+len(b)<16*1024**2 and os.statvfs(D).f_bavail*os.statvfs(D).f_frsize-len(b)>=125829120
 p=D/name
 with p.open('xb')as f:os.fchmod(f.fileno(),0o600);f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
candidate={'kind':'ROOT_FINAL_OVERLAY_INPUT_CANDIDATE_NOT_YET_ADOPTED','at':now(),'payload':payload,'full_native_collection':pin(collectionp),'strict_full_numeric43_details':details,'original_numeric_physical_captures':4,'numeric_original_request_and_chronology_checks_passed':True,'inventory_full_native_chronology':chron,'highest':highest,'numeric_slots':highest-8,'material_claim_changes_or_gaps':deltas,'administrative_state_draft_merge_changes':administrative_changes,'all34_frozen_literal_identities_and_unique_rows_checked':True,'all252_typed_prefix_values_and_formulas_exact':True,'PR1131_literal_DOI_record_unique287_and_native_merge_head_bound':True,'all_native_receipts_reviewed':False,'final_reconciliation_complete':False}
cp=save('ROOT_OVERLAY_INPUT_CANDIDATE.json',candidate)
print(json.dumps({'candidate':cp,'highest':highest,'numeric_slots':highest-8,'full_sheet_rows':len(sheet['values']),'deltas':deltas,'administrative_changes':administrative_changes,'no_final_adoption':True}))
