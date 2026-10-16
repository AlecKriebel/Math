#!/usr/bin/env python3
"""Bounded administrative reconciliation; never accesses a service or Git index."""
from pathlib import Path
import datetime, difflib, hashlib, io, json, shutil, sys, zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PACKAGE=AUDIT/'preprint_v1_0'
STAGE='READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032'
CHANGED={'README.md','verify_package.py','COPY_MAP.json','SAFE_INPUT_PINS.json','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','support.zip','publication/DEPOSIT_BINDING.json'}

def require(c,m):
 if not c: raise ValueError(m)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def rec(p,root):
 data=p.read_bytes(); return {'path':p.relative_to(root).as_posix(),'bytes':len(data),'sha256':sha(data)}
def write(p,d): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,indent=2)+'\n')
def load(p): return json.loads(p.read_text())
def match(p,r): return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256']
def pkgfiles(): return sorted(p for p in PACKAGE.rglob('*') if p.is_file() and not {'tmp','__pycache__'}.intersection(p.relative_to(PACKAGE).parts))
def baseline_files():
 known=set()
 # Retain the preceding complete review's full non-disposable input boundary,
 # including any primary-body/tree identities; hash these without copying.
 for r in load(AUDIT/'reviews/package_03/INPUT_CUSTODY.json')['files']:
  p=AUDIT/r['path']; require(match(p,r),'whole03 frozen input changed before terminal freeze '+r['path'])
  known.add(p)
 for p in sorted(known):yield p
 for p in sorted(AUDIT.rglob('*')):
  if not p.is_file() or p.is_symlink() or p.is_relative_to(HERE) or p in known: continue
  parts=p.relative_to(AUDIT).parts
  if set(parts).intersection({'tmp','private','.venv','__pycache__','render','renders','extracted','raw','snapshots.git'}): continue
  if p.suffix in {'.png','.pyc'}: continue
  yield p

def freeze():
 require(not (HERE/'INPUT_PINS.json').exists(),'baseline already exists')
 write(HERE/'INPUT_PINS.json',{'utc':utc(),'scope':'Immediate non-disposable own audit files before terminal administrative edits; hash-only. Excludes this new finalization, private/raw/extracted/render/tmp/runtime caches and generated source PNGs. No bodies copied.','records':[rec(p,AUDIT) for p in baseline_files()]})
 before=[]
 for name in sorted(CHANGED):
  p=PACKAGE/name; dest=HERE/'before/preprint_v1_0'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
  before.append(dict(rec(p,AUDIT),preserved_path=dest.relative_to(HERE).as_posix()))
 write(HERE/'BEFORE_PINS.json',{'scope':'Exact immediate before bytes only for the nine permitted changed files.','entries':before})
 (HERE/'.gitignore').write_text('tmp/\n__pycache__/\n*.pyc\n')
 (HERE/'RESEARCH_LOG.md').write_text('# Terminal administrative reconciliation for PR1064\n\n'+utc()+' — 10%: full whole03 report/verdict and ROOT adoption read; immediate own inputs frozen before changes. No mathematical or bibliographic edit authorized.\n')
 print(json.dumps({'frozen_inputs':len(load(HERE/'INPUT_PINS.json')['records']),'exact_before_files':len(before)}))

def selected_sources():
 selections=[]
 # Each sealed record receives its own explicit included/omitted decision.
 for folder,omit in [('reviews/package_03', {'.gitignore':'Runtime ignore configuration; not scholarly evidence.', 'EXECUTIONS.jsonl':'Raw process output is redundant with authored terminal reproduction/guard receipts; retained locally.', 'EXECUTIONS_ATTEMPT01.jsonl':'Raw failed-harness process capture retained locally; the authored report and reproduction receipts disclose this incident.'}), ('repairs/package02', {})]:
  records=load(AUDIT/folder/'OUTPUT_PINS.json')['entries']
  records=records+[rec(AUDIT/folder/'OUTPUT_PINS.json',AUDIT/folder)]
  if folder=='reviews/package_03': records.append(rec(AUDIT/folder/'SEAL.json',AUDIT/folder))
  for r in records:
   path=folder+'/'+r['path']; reason=omit.get(r['path'])
   if r['path'].startswith('before/'):
    reason='Exact historical saved-before local stage file, including duplicate old archive; retained locally and resolved by hashes rather than duplicated in delivery.'
   elif folder=='repairs/package02' and r['path']=='EXECUTIONS.jsonl':
    reason='Raw process capture retained locally; authored guard, reproduction, and checker receipts are included.'
   selections.append({'source_path':path,'bytes':r['bytes'],'sha256':r['sha256'],'included':reason is None,'reason':reason or 'Authored exact historical analysis, code, locators, stage pins or terminal receipts; no primary source body.'})
 for name in ['ROOT_WHOLE_PACKAGE_REVIEW_03.json','ROOT_REPAIR_REVIEW_02.json']:
  selections.append(dict(source_path=name,**{k:v for k,v in rec(AUDIT/name,AUDIT).items() if k!='path'},included=True,reason='ROOT adoption of the exact dated complete review or bounded repair; preserved verbatim.'))
 return selections

def prepare():
 require((HERE/'INPUT_PINS.json').exists(),'freeze first')
 require(not (PACKAGE/'TERMINAL_STATUS.json').exists(),'terminal stage already exists')
 adoption=load(AUDIT/'ROOT_WHOLE_PACKAGE_REVIEW_03.json')
 require(adoption['whole_reviews_completed']==3 and adoption['actionable_P0_P1_P2_P3']==0,'ROOT whole03 authority absent')
 for r in load(HERE/'INPUT_PINS.json')['records']: require(match(AUDIT/r['path'],r),'input changed before authorized edits '+r['path'])
 selections=selected_sources(); old=load(PACKAGE/'COPY_MAP.json')['copies'];require(len(old)==122,'old122 map count changed')
 copies=list(old)
 for r in selections:
  source=AUDIT/r['source_path'];require(match(source,r),'selected source differs '+r['source_path'])
  if not r['included']:continue
  name='support/history/'+r['source_path'];dest=PACKAGE/name;require(not dest.exists(),'copy collision '+name)
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  copies.append({'source_path':r['source_path'],'package_path':name,'bytes':r['bytes'],'sha256':r['sha256']})
 write(PACKAGE/'TERMINAL_SELECTION_LEDGER.json',{'scope':'Every record in whole03 and repair02 output seals, the seals themselves and ROOT adoptions is individually accounted for. Other private source/render/scratch exclusions remain in EXCLUSION_LEDGER. Included historical programs retain original candidate/stage scope; they are not current-stage replay claims.','records':selections})
 write(PACKAGE/'COPY_MAP.json',{'scope':load(PACKAGE/'COPY_MAP.json')['scope'],'copies':copies})
 write(PACKAGE/'SAFE_INPUT_PINS.json',{'scope':'Exact authored selected source bytes; historical copies keep original meanings.','records':copies})
 terminal={'schema_version':1,'stage':STAGE,'snapshot_date':'2026-10-14','pr':1064,'problem_id':30001073,'whole_package_reviews_completed':3,'whole_package_reviews_required':2,'latest_complete_review':'support/history/reviews/package_03/VERDICT.json','root_complete_review_adoption':'support/history/ROOT_WHOLE_PACKAGE_REVIEW_03.json','actionable_P0_P1_P2_P3':0,'ready_for_submission_after_root_adoption':True,'root_terminal_adoption_required':True,'publication_ready':False,'published':False,'issues_updated':False,'ascending_publication_hold_after_pr':1032,'novelty':'UNKNOWN','historical_priority':'UNKNOWN','scope':'Terminal administrative reconciliation of ROOT-adopted complete whole03. Root terminal seal remains required; dated earlier pending statuses are immutable history. No services or disposition occurred.'}
 write(PACKAGE/'TERMINAL_STATUS.json',terminal)
 (PACKAGE/'TERMINAL_ACCEPTANCE.md').write_text('# Terminal package status\n\nThe mathematical/source/PDF/bibliographic edition has completed three new full adversarial reviews; the latest whole03 has zero actionable P0–P3 findings and has been adopted by ROOT. Its unchanged five-page paper is a credited corollary, with historical priority and novelty UNKNOWN.\n\n`TERMINAL_STATUS.json` records READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032. Terminal administrative adoption by ROOT remains required. This administrative step is not a fourth whole review or a new mathematical validation. The original `STATUS.json`, repair01 `CURRENT_STATUS.json` and repair02 `CURRENT_STATUS_WHOLE03.json` remain verbatim dated historical pending stages with counts zero, one and two. They are superseded for current workflow status, without changing their original verdicts.\n\nNo upload, DOI creation, spreadsheet operation, PR/issue action or publication occurred. The ascending service gate remains held after PR1032. Extensive AI assistance, unrefereed status, absence of external human peer review/formal certification and all source credits are unchanged.\n\nThe selection ledger individually identifies every included and omitted whole03/repair02 sealed output. Copied programs and receipts refer to their own original editions; the older `check_package.py` and local stage resolver are not advertised as working against this later edition without their original preserved-stage context. Only the four standard-library README commands and the current verifier were replayed for this administrative step. No recompilation or visual rerender was performed because the canonical paper bytes are unchanged; actual real compilation and all five page views are recorded in whole03.\n')
 verifier=PACKAGE/'verify_package.py';text=verifier.read_text();needle=" require(load('support/CHECKS.json')['pass'] is True,'authored diagnostic record not passed')"
 require(needle in text,'verifier insertion location missing')
 guard=""" terminal=load('TERMINAL_STATUS.json')
 require(terminal['stage']=='READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032' and terminal['snapshot_date']=='2026-10-14','terminal stage altered')
 require(terminal['whole_package_reviews_completed']==3 and terminal['whole_package_reviews_required']>=2,'terminal complete-review count altered')
 require(terminal['actionable_P0_P1_P2_P3']==0 and terminal['ready_for_submission_after_root_adoption'] is True,'terminal clean-review readiness altered')
 require(terminal['root_terminal_adoption_required'] is True and terminal['publication_ready'] is False and terminal['published'] is False and terminal['issues_updated'] is False,'terminal adoption/publication gate altered')
 require(terminal['ascending_publication_hold_after_pr']==1032,'terminal ascending hold altered')
 require(terminal['novelty']=='UNKNOWN' and terminal['historical_priority']=='UNKNOWN','terminal novelty boundary altered')
 review=load('support/history/reviews/package_03/VERDICT.json')
 require(review['verdict']=='ZERO_ACTIONABLE_FINDINGS' and all(review['severity_counts'][s]==0 for s in ['P0','P1','P2','P3']),'terminal complete-review verdict altered')
 adoption=load('support/history/ROOT_WHOLE_PACKAGE_REVIEW_03.json')
 require(adoption['whole_reviews_completed']==3 and adoption['minimum_whole_reviews']>=2 and adoption['actionable_P0_P1_P2_P3']==0,'terminal ROOT review adoption altered')
"""
 verifier.write_text(text.replace(needle,guard+needle))
 readme=PACKAGE/'README.md';text=readme.read_text();start=text.index('The dated preparation snapshot');end=text.index('\n\nRun the following',start)
 text=text[:start]+"The current `TERMINAL_STATUS.json` records `READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032`: three complete whole-package reviews, at least two required, latest whole03 ZERO actionable P0–P3, and ROOT adoption of that complete review. Terminal administrative adoption by ROOT remains required. No publication, service or issue action occurred; publication_ready=false and issues_updated=false remain preparation flags here. The ascending service gate is held after PR1032. `TERMINAL_ACCEPTANCE.md` describes this distinction. The unchanged dated `STATUS.json`, `CURRENT_STATUS.json` and `CURRENT_STATUS_WHOLE03.json` preserve the earlier counts zero, one and two and their pending-stage meanings. Whole01's two P3 package findings and whole02's archive-output P3 were repaired and accepted in full whole03. These workflow gates are not premises of the proof."+text[end:]
 text=text.replace('`CURRENT_OUTPUT_PINS_WHOLE03.json` seals the latest stage separately.','`CURRENT_OUTPUT_PINS_WHOLE03.json` seals the immutable repair02 stage. `TERMINAL_OUTPUT_PINS.json` seals this terminal stage separately.')
 text+='\n`TERMINAL_SELECTION_LEDGER.json` accounts for each whole03/repair02 sealed-output inclusion or omission; safe selected history is byte-exact. Historical scripts and captures retain their dated original stage scopes, and are not represented as current-edition replay. The external `publication/zenodo-deposit.json` is the repository uploader\'s native `{metadata, files}` manifest; its bibliographic object is exactly the unchanged metadata, and it selects this canonical PDF plus exact support ZIP. Its repository `check` is local only.\n'
 readme.write_text(text)
 exclusions=load(PACKAGE/'EXCLUSION_LEDGER.json');exclusions['local_package_files']+=['TERMINAL_OUTPUT_PINS.json','publication/zenodo-deposit.json']
 exclusions['source_exclusion_groups'] += [{'group':'reviews/package_03 private sources, extracted text, source/render images and raw process captures','reason':'Only exact authored analysis, locators and terminal receipts selected individually in TERMINAL_SELECTION_LEDGER; no source bodies/images or raw execution logs delivered.'},{'group':'finalization/terminal_admin_20261014 before/input/validation/process trees','reason':'Exact immediate custody and administrative receipts remain local, with separate ROOT adoption; do not create archive/seal cycles.'}]
 write(PACKAGE/'EXCLUSION_LEDGER.json',exclusions)
 oldallow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members']
 added=[r['package_path'] for r in copies[122:]]+['TERMINAL_STATUS.json','TERMINAL_ACCEPTANCE.md','TERMINAL_SELECTION_LEDGER.json']
 allow=sorted(set(oldallow+added));write(PACKAGE/'SUPPORT_ALLOWLIST.json',{'members':allow})
 manifest={'entries':[rec(PACKAGE/name,PACKAGE) for name in allow if name!='SUPPORT_MANIFEST.json']};write(PACKAGE/'SUPPORT_MANIFEST.json',manifest)
 # Independent builder; final bytes are compared only after ZipFile closes.
 with zipfile.ZipFile(PACKAGE/'support.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for name in allow:
   info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;info.internal_attr=0
   z.writestr(info,(PACKAGE/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 binding=load(PACKAGE/'publication/DEPOSIT_BINDING.json'); binding['support_archive']=rec(PACKAGE/'support.zip',PACKAGE);write(PACKAGE/'publication/DEPOSIT_BINDING.json',binding)
 write(PACKAGE/'publication/zenodo-deposit.json',{'metadata':load(PACKAGE/'metadata.json'),'files':[{'path':'../paper.pdf','name':'paper.pdf'},{'path':'../support.zip','name':'support.zip'}]})
 write(PACKAGE/'TERMINAL_OUTPUT_PINS.json',{'utc':utc(),'stage':STAGE,'root_terminal_adoption_required':True,'publication_ready':False,'issues_updated':False,'entries':[rec(p,PACKAGE) for p in pkgfiles() if p.name!='TERMINAL_OUTPUT_PINS.json']})
 print(json.dumps({'safe_new_copies':len(copies)-122,'current_copies':len(copies),'selected_records':len(selections),'omissions':sum(not r['included'] for r in selections),'archive':rec(PACKAGE/'support.zip',PACKAGE),'members':len(allow),'current_files':len(pkgfiles())},indent=2))

def resolve(r):
 relative=r['path'];candidates=[AUDIT/relative,HERE/'before'/relative]
 if relative.startswith('preprint_v1_0/'):
  name=relative[len('preprint_v1_0/'):]
  candidates += [AUDIT/'repairs/package02/before/preprint_v1_0'/name,AUDIT/'repairs/package01/before/preprint_v1_0'/name]
 for p in candidates:
  if match(p,r):return p
 raise ValueError('No exact captured-stage resolution '+relative)

def reconcile():
 frozen=load(HERE/'INPUT_PINS.json')['records'];changed=[];unchanged=[]
 for r in frozen:
  p=AUDIT/r['path']
  if match(p,r):unchanged.append(r)
  else:
   require(r['path'].startswith('preprint_v1_0/') and r['path'][len('preprint_v1_0/'):] in CHANGED,'unauthorized mutation '+r['path'])
   require(match(HERE/'before'/r['path'],r),'missing exact immediate before '+r['path'])
   changed.append({'path':r['path'],'before':r,'after':rec(p,AUDIT),'preserved_path':(HERE/'before'/r['path']).relative_to(AUDIT).as_posix()})
 require({r['path'][len('preprint_v1_0/'):] for r in changed}==CHANGED,'changed set differs')
 for r in load(HERE/'BEFORE_PINS.json')['entries']:require(match(HERE/r['preserved_path'],r),'immediate before byte mismatch')
 stages=[]
 for name,key,count in [('preprint_v1_0/OUTPUT_PINS.json','entries',103),('preprint_v1_0/CURRENT_OUTPUT_PINS.json','entries',124),('repairs/package01/FINAL_CURRENT_PINS.json','records',125),('repairs/package01/INPUT_PINS.json','records',294),('repairs/package02/INPUT_PINS.json','records',402),('repairs/package02/FINAL_CURRENT_PINS.json','records',158),('preprint_v1_0/CURRENT_OUTPUT_PINS_WHOLE03.json','entries',157)]:
  rows=load(AUDIT/name)[key];require(len(rows)==count,'historical count changed '+name); prefix='preprint_v1_0/' if '/FINAL_CURRENT_PINS.json' in name or name.startswith('preprint_v1_0/') else ''
  out=[]
  for r in rows:
   rr=dict(r,path=prefix+r['path']); p=resolve(rr);out.append(dict(rr,resolved_path=p.relative_to(AUDIT).as_posix()))
  stages.append({'stage':name,'count':count,'records':out})
 for folder,count in [('repairs/package01',37),('repairs/package02',41),('reviews/package_01',17),('reviews/package_02',28),('reviews/package_03',24)]:
  rows=load(AUDIT/folder/'OUTPUT_PINS.json')['entries'];require(len(rows)==count,'terminal historical count changed '+folder)
  for r in rows:require(match(AUDIT/folder/r['path'],r),'immutable historical output changed '+folder+'/'+r['path'])
  stages.append({'stage':folder+'/OUTPUT_PINS.json','count':count,'all_unchanged':True})
 for r in load(PACKAGE/'INPUT_PINS.json')['records']:require(match(AUDIT/r['path'],r),'original preparation input changed')
 copies=load(PACKAGE/'COPY_MAP.json')['copies'];old=load(HERE/'before/preprint_v1_0/COPY_MAP.json')['copies'];require(copies[:122]==old,'old122 map changed')
 for r in copies:require(match(AUDIT/r['source_path'],r) and match(PACKAGE/r['package_path'],r),'copy/source mismatch '+r['source_path'])
 require(load(PACKAGE/'SAFE_INPUT_PINS.json')['records']==copies,'SAFE map mismatch')
 protected_names=['paper.tex','paper.pdf','metadata.json','publication/zenodo.json','publication/release_metadata.json','ATTRIBUTION.md','LICENSE.txt','SOURCE_LEDGER.json','STATUS.json','CURRENT_STATUS.json','CURRENT_STATUS_WHOLE03.json','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json','CURRENT_OUTPUT_PINS_WHOLE03.json','PREPARATION_REPORT.md','FINAL_VERIFICATION.json','RESEARCH_LOG.md','build_pdf.py','run_checks.py','fresh_guard_checker.py']
 lookup={r['path']:r for r in frozen};protected=[lookup['preprint_v1_0/'+n] for n in protected_names]
 for r in protected:require(match(AUDIT/r['path'],r),'protected semantic byte changed '+r['path'])
 meta=load(PACKAGE/'metadata.json');require(all(load(PACKAGE/n)['metadata']==meta for n in ['publication/zenodo.json','publication/release_metadata.json','publication/zenodo-deposit.json']),'metadata objects differ')
 oldbinding=load(HERE/'before/preprint_v1_0/publication/DEPOSIT_BINDING.json');binding=load(PACKAGE/'publication/DEPOSIT_BINDING.json')
 require(binding['paper_pdf']==oldbinding['paper_pdf'] and binding['schema_version']==oldbinding['schema_version'],'PDF or schema binding changed')
 write(HERE/'PRIOR_STAGE_RECEIPTS.json',{'utc':utc(),'pass':True,'scope':'Exact captured-stage resolution only; no historical pin or verdict rebound; old local resolvers need their original stages.','stages':stages})
 write(HERE/'PROTECTED_BYTE_RECEIPT.json',{'utc':utc(),'pass':True,'immediate_inputs':len(frozen),'authorized_changes':len(changed),'unchanged_inputs':len(unchanged),'unchanged_records':unchanged,'explicit_protected':protected,'old122_maps_unchanged':True,'source_equal_current_copies':len(copies),'historical_stages_exact':True,'bibliographic_objects_byte_unchanged_and_equal':True})
 additions=[rec(p,AUDIT) for p in pkgfiles() if p.relative_to(AUDIT).as_posix() not in lookup]
 write(HERE/'CHANGE_INVENTORY.json',{'utc':utc(),'scope':'Administrative status/custody/archive/interface only; no math, PDF, metadata-object, source or checker change.','modified':changed,'added_package_files':additions,'added_copy_count':len(copies)-122,'root_terminal_adoption_required':True})
 diff=[]
 for name in ['verify_package.py','README.md']:
  diff+=list(difflib.unified_diff((HERE/'before/preprint_v1_0'/name).read_text().splitlines(True),(PACKAGE/name).read_text().splitlines(True),fromfile='before/preprint_v1_0/'+name,tofile='preprint_v1_0/'+name))
 for name in ['TERMINAL_STATUS.json','TERMINAL_ACCEPTANCE.md']:
  diff+=list(difflib.unified_diff([],(PACKAGE/name).read_text().splitlines(True),fromfile='/dev/null',tofile='preprint_v1_0/'+name))
 (HERE/'CODE_PROSE_DIFF.patch').write_text(''.join(diff))
 write(HERE/'FINAL_CURRENT_PINS.json',{'utc':utc(),'records':[rec(p,PACKAGE) for p in pkgfiles()]})
 print(json.dumps({'pass':True,'immediate_inputs':len(frozen),'changed':len(changed),'unchanged':len(unchanged),'current_files':len(pkgfiles()),'source_equal_copies':len(copies),'stages':[{k:v for k,v in s.items() if k!='records'} for s in stages]},indent=2))

if __name__=='__main__':
 {'freeze':freeze,'prepare':prepare,'reconcile':reconcile}[sys.argv[1]]()
