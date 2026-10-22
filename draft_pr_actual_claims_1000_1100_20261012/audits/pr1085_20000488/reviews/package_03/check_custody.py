from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent;A=R.parent.parent;K=A/'preprint_v1_0';F=A/'repairs/case_alias01';P=A.parent.parent;REPO=P.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(b,msg):
 if not b:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def expected(r):return {'bytes':r.get('bytes',r.get('size')),'sha256':r['sha256']}
def dump(n,o):(R/n).write_text(json.dumps(o,indent=2)+'\n')
freeze=load(R/'INPUT_FREEZE.json')['files'];current={str(p.relative_to(A)):ident(p) for p in A.rglob('*') if p.is_file() and not p.is_symlink() and R not in p.parents}
need(all(current[r['path']]==expected(r) for r in freeze),'frozen input changed')
# Full per-source partitions and byte pairs; copied historical paths resolve explicitly to saved before snapshots.
copies=[];partitions=[]
for cmap,pins,excl in [('COPY_MAP.json','PREPARATION_INPUT_PINS.json','EXCLUSIONS.json'),('TERMINAL_COPY_MAP.json','TERMINAL_INPUT_PINS.json','TERMINAL_EXCLUSIONS.json')]:
 f=load(K/pins)['files'];fm={r['path']:r for r in f};c=load(K/cmap)['files'];e=load(K/excl)['files'];cs=[r['source_relative_audit'] for r in c];es=[r['path'] for r in e]
 need(len(fm)==len(f) and len(set(cs))==len(cs) and len(set(es))==len(es) and set(cs).isdisjoint(es) and set(cs+es)==set(fm),'partition '+cmap)
 for r in c:
  s=A/r.get('source_snapshot_relative_audit',r['source_relative_audit']);d=K/r['copy'];need(ident(s)==ident(d)==expected(r)==expected(fm[r['source_relative_audit']]) and s.read_bytes()==d.read_bytes(),'copy '+r['copy']);copies.append({'map':cmap,'source':str(s.relative_to(A)),'copy':r['copy'],**ident(d),'exact_byte_pair':True})
 for r in e:need(expected(r)==expected(fm[r['path']]) and bool(r['reason']),'exclusion '+r['path'])
 partitions.append({'map':cmap,'frozen':len(f),'copies':len(c),'individual_exclusions':len(e)})
for r in load(K/'CASE_ALIAS_REPAIR_COPY_MAP.json')['files']:
 s=P/r['source_relative_program'];d=K/r['copy'];need(ident(s)==ident(d)==expected(r) and s.read_bytes()==d.read_bytes(),'case pair');copies.append({'map':'CASE_ALIAS_REPAIR_COPY_MAP.json','source':r['source_relative_program'],'copy':r['copy'],**ident(d),'exact_byte_pair':True})
need(len(copies)==124,'124 copies')
# Independently resolve exact historical hashes. No old executable is run and no dated pin is changed.
index={}
for rel,i in current.items():index.setdefault((i['bytes'],i['sha256']),[]).append(rel)
def digest_rows(o,p=''):
 if isinstance(o,dict):
  if isinstance(o.get('sha256'),str) and type(o.get('bytes',o.get('size'))) is int:yield p,o
  for k,v in o.items():yield from digest_rows(v,p+'/'+str(k))
 elif isinstance(o,list):
  for k,v in enumerate(o):yield from digest_rows(v,p+'/'+str(k))
baseline=load(F/'BASELINE_INPUT_PINS.json')['files'];allowed=set(load(F/'AUTHORIZED_EXISTING_CHANGES.json')['files']);resolved=[];stages=[]
for row in baseline:
 rel=row['path'];loc=F/'before'/rel if rel in allowed else A/rel;need(ident(loc)==expected(row),'repair baseline explicit before conservation')
 if 'PINS' in Path(rel).name or Path(rel).name in ['MANIFEST.json','SUPPORT_MANIFEST.json']:
  n=0
  for pointer,r in digest_rows(load(loc)):
   matches=index.get((r.get('bytes',r.get('size')),r['sha256']),[]);need(bool(matches),'unresolved exact historical '+rel+pointer)
   hint=r.get('snapshot_path',r.get('path',r.get('file',pointer.split('/')[-1])))
   candidates=[A/hint,loc.parent/hint,loc.parent/'frozen'/hint];chosen=next((str(q.relative_to(A)) for q in candidates if q.is_relative_to(A) and str(q.relative_to(A)) in matches),matches[0])
   need(current[chosen]==expected(r),'rehash historical')
   resolved.append({'stage':rel,'pointer':pointer,'old_locator':hint,'exact_extant_artifact':chosen,**expected(r)});n+=1
  stages.append({'stage':rel,'stage_read_from':str(loc.relative_to(A)),'rows':n,'stage_identity':ident(loc)})
 resolved.append({'stage':'repair baseline','pointer':'/'+rel,'old_locator':rel,'exact_extant_artifact':str(loc.relative_to(A)),**expected(row)})
stages.append({'stage':'repair baseline','rows':len(baseline)})
need(len(resolved)==4109 and len(stages)==44,'4109 rows 44 stages')
# Allowed changes all have exact BEFORE artifacts; every protected artifact remains exact.
changes=[];protected=[]
for r in baseline:
 p=A/r['path']
 if r['path'] in allowed:
  before=F/'before'/r['path'];need(ident(before)==expected(r) and ident(p)!=expected(r),'bounded changed before');changes.append({'path':r['path'],'before_custody':str(before.relative_to(A)),'before':ident(before),'current':ident(p)})
 else:need(ident(p)==expected(r),'protected '+r['path']);protected.append(r)
need(len(changes)==7 and len(protected)==456,'7/456 bounded repair')
for r in load(F/'CURRENT_CANDIDATE_PINS.json')['files']:need(ident(K/r['path'])==expected(r),'current candidate pin')
seals=[]
for rel in ['preprint_v1_0/PREPARATION_SEAL.json','reviews/ground_state_01/REVIEW_SEAL.json','reviews/hardy_absence_01/SEAL.json','reviews/priority_01/SEAL.json','reviews/package_01/FINAL_SEAL.json','reviews/package_02/SEAL.json','finalization/terminal_admin_20261016/SEAL.json','repairs/case_alias01/SEAL.json']:
 s=A/rel;obj=load(s);inv=s.parent/'OUTPUT_PINS.json';i=ident(inv);need(obj.get('output_pins_sha256',obj.get('manifest_sha256'))==i['sha256'],'seal inventory binding');seals.append({'seal':rel,'inventory':str(inv.relative_to(A)),**i,'verified':True})
# All 34 repair output rows checked relative to repair; self-exclusion avoids hash cycle.
outs=load(F/'OUTPUT_PINS.json')['files']
for r in outs:need(ident(F/r['path'])==expected(r),'repair output')
need(len(outs)==34,'34 repair outputs')
# Metadata all fields are identical across formats and the saved pre-repair binding.
meta=load(K/'.zenodo.json')
need(meta==load(K/'metadata.json')['metadata']==load(K/'zenodo-deposit.json')['metadata']==load(K/'UPLOAD_BINDINGS.json')['metadata']==load(F/'before/preprint_v1_0/UPLOAD_BINDINGS.json')['metadata'],'full native metadata')
# Original six submitted artifacts remain exactly pinned, preserving original incomplete-attribution history.
for r in load(A/'SUBMITTED_PINS.json')['files']:need(ident(A/r['snapshot_path'])==expected(r),'original submitted')
dump('CUSTODY_COPY_PAIRS.json',{'utc':now,'partitions':partitions,'exact_copies':len(copies),'pairs':copies})
dump('HISTORICAL_RESOLUTION.json',{'utc':now,'rows':resolved,'stages':stages,'historical_rows':len(resolved),'historical_stages':len(stages),'no_historical_pin_rewrite':True,'no_historical_program_replay':True})
dump('CUSTODY_VERIFICATION.json',{'utc':now,'passed':True,'preexisting_input_freeze_count':len(freeze),'all_frozen_inputs_unchanged':True,'current_candidate_files':len(load(F/'CURRENT_CANDIDATE_PINS.json')['files']),'exact_copy_pairs':len(copies),'partitions':partitions,'bounded_repair_changes':changes,'bounded_repair_protected':len(protected),'historical_rows':len(resolved),'historical_stages':len(stages),'seal_inventory_bindings':seals,'repair_outputs':len(outs),'native_metadata_all_fields_identical':True,'original_submitted_six_exact':True})
print({'passed':True,'frozen':len(freeze),'copies':len(copies),'historical_rows':len(resolved),'stages':len(stages),'seals':len(seals)})
