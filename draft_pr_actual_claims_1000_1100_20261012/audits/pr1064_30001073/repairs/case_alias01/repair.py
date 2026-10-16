#!/usr/bin/env python3
"""Bounded PR1064 static output-contract repair; no mathematics or services."""
from pathlib import Path
import datetime,difflib,hashlib,json,shutil,sys,zipfile
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PACKAGE=AUDIT/'preprint_v1_0'
PROGRAM=AUDIT.parent.parent
CHANGED={'build_archive.py','verify_package.py','README.md','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','COPY_MAP.json','SAFE_INPUT_PINS.json','publication/DEPOSIT_BINDING.json','support.zip'}
def require(c,m):
 if not c:raise ValueError(m)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def rec(p,base):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
def match(p,r):return p.is_file() and not p.is_symlink() and rec(p,p.parent)['bytes']==r['bytes'] and rec(p,p.parent)['sha256']==r['sha256']
def write(p,value):
 # Atomic replacement avoids changing immutable historical hardlinks in place.
 p.parent.mkdir(parents=True,exist_ok=True)
 temp=p.with_name(p.name+'.case_alias01-writing');temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(p)
def text_replace(p,value):
 temp=p.with_name(p.name+'.case_alias01-writing');temp.write_text(value);temp.replace(p)
def packagefiles():return [p for p in sorted(PACKAGE.rglob('*')) if p.is_file() and not {'tmp','__pycache__'}.intersection(p.relative_to(PACKAGE).parts)]
def prepare():
 baseline=load(HERE/'INPUT_PINS.json')['records']
 for r in baseline:require(match(AUDIT/r['path'],r),'input changed before edits '+r['path'])
 before=load(HERE/'BEFORE_PINS.json')['entries'];require({r['path'].removeprefix('preprint_v1_0/') for r in before}==CHANGED,'bounded edit list differs')
 for r in before:require(match(HERE/r['preserved_path'],r),'before snapshot differs')
 builder=(PACKAGE/'build_archive.py').read_text()
 old="if out.is_relative_to(root):v.require(out==root/'support.zip' or out.is_relative_to(root/'tmp'),'inside package output must be support.zip or under tmp/')"
 require(builder.count(old)==1,'old lexical check differs')
 new="""def physical_relative(path,directory):
 # Resolve() can preserve a case alias. Walk past absent components until an
 # existing ancestor is physically the directory; keep its remaining suffix.
 suffix=[]
 while True:
  if path.exists() and directory.exists() and path.samefile(directory):return Path(*reversed(suffix))
  parent=path.parent
  if parent==path:return None
  suffix.append(path.name);path=parent
inside=physical_relative(out,root)
if inside is not None:
 v.require(inside==Path('support.zip') or (inside.parts and inside.parts[0]=='tmp') or physical_relative(out,root/'tmp') is not None,'inside package output must be support.zip or under tmp/')"""
 text_replace(PACKAGE/'build_archive.py',builder.replace(old,new))
 scope=PROGRAM/'reviews/case_alias_scope_20261016/REPORT.md'
 report=scope.read_text();start=report.index('### CASE-1064');end=report.index('### CASE-1071',start)
 root=PROGRAM/'ROOT_CASE_ALIAS_SCOPE_REVIEW.json';rootobj=load(root)
 finding={'utc':utc(),'scope':'PR1064-only exact excerpt of complete scope REPORT; other PR prose and reproduction records intentionally omitted. Full sources hash-pinned locally and here. This is a new finding on dated current support bytes, not a changed old zero verdict.','sources':[rec(scope,PROGRAM),rec(root,PROGRAM)],'exact_REPORT_excerpt':report[start:end],'root_selected_fields':{k:rootobj[k] for k in ['utc','status','mathematical_acceptance_unchanged','existing_input_overwrite_observed','required_repairs','published_records_not_inspected_or_changed','publication_ready_for_affected','services_held_after_pr']},'root_PR1064_actual_commands':[r for r in rootobj['root_actual_reproduction'] if r['pr']==1064]}
 write(HERE/'CASE1064_FINDING.json',finding)
 mechanism='''# PR1064 physical ancestry repair

The static filesystem contract permits support.zip and tmp/ inside the kit and ZIP files outside it. Existing direct, symlink and hardlink aliases of protected inputs remain rejected before output-directory creation or writer opening. A fresh unlisted file inside the kit must be rejected even when an existing directory is addressed through a case alias.

Path.resolve() on the observed case-insensitive filesystem preserves alias spelling. The new physical_relative walks the resolved output and every lexical parent, remembering the suffix. At each existing ancestor it tests samefile against the kit directory. If it reaches a physically identical directory it returns that suffix. This includes the existing kit ancestor above any number of absent descendants. No case folding, lowercase assumption, string-prefix containment or absent-leaf samefile assumption is used. An actually external output has no physically identical kit ancestor and stays permitted. Existing tmp ancestors are also checked by identity, preserving aliases of that intentionally mutable directory.

The existing protected-input identity loop runs first without removal or relaxation. The extension does not claim protection against hostile concurrent directory replacement. Symlink resolution retains its previous behavior. The unchanged source/PDF, all nine submitted originals, mathematical checks, source credits and bibliographic objects stay exact. The new P3 finding supersedes dated readiness, requiring ROOT repair adoption and NEW COMPLETE whole04; this focused repair validation is not whole04.
'''
 text_replace(HERE/'MECHANISM.md',mechanism)
 status={'schema_version':1,'snapshot_date':'2026-10-16','pr':1064,'problem_id':30001073,'stage':'PENDING_ROOT_CASE_ALIAS_REPAIR_ADOPTION_AND_NEW_COMPLETE_WHOLE04','whole_package_reviews_completed':3,'whole_package_reviews_required':2,'latest_prior_complete_review':'support/history/reviews/package_03/VERDICT.json','latest_prior_complete_review_actionable_P0_P1_P2_P3':0,'new_support_finding':'CASE-1064 P3: fresh physically internal output through case alias bypassed whitelist','bounded_repair_applied':True,'focused_validation_is_complete_whole_review':False,'new_complete_whole04_required':True,'root_repair_adoption_required':True,'ready_for_submission':False,'publication_ready':False,'published':False,'issues_updated':False,'ascending_publication_hold_after_pr':1032,'novelty':'UNKNOWN','historical_priority':'UNKNOWN','supersedes_current_readiness':'TERMINAL_STATUS.json is unchanged dated history; its old readiness does not certify these repaired bytes.'}
 write(PACKAGE/'REPAIR_STATUS_CASE_ALIAS01.json',status)
 acceptance='''# Current bounded repair status

REPAIR_STATUS_CASE_ALIAS01.json supersedes the current readiness interpretation of the unchanged, dated TERMINAL_STATUS.json. Three prior whole-package reviews completed; at least two are required. The latest prior whole03 was zero actionable P0–P3 on its original bytes. A subsequently confirmed CASE-1064 P3 support-location finding required this bounded repair. ROOT adoption of the repair and NEW COMPLETE whole04 are required before any new readiness decision. Focused repair checks do not constitute whole04 or change prior review verdicts.

Publication, published and issues-updated flags remain false. The ordered service gate remains held after PR1032. The exact five-page paper, mathematical proof, constants, checker programs, source credits and bibliographic objects are unchanged. It remains an explicitly credited prior corollary; novelty, historical priority and worldwide still-open status are not certified. Extensive AI assistance, unrefereed status, and absence of formal or external human peer review remain disclosed. No compiler, renderer, Git, service or outreach action occurred in this repair.
'''
 text_replace(PACKAGE/'REPAIR_ACCEPTANCE_CASE_ALIAS01.md',acceptance)
 readme=(PACKAGE/'README.md').read_text();start=readme.index('The current `TERMINAL_STATUS.json`');end=readme.index('\n\nRun the following',start)
 replacement='The current `REPAIR_STATUS_CASE_ALIAS01.json` records `PENDING_ROOT_CASE_ALIAS_REPAIR_ADOPTION_AND_NEW_COMPLETE_WHOLE04`. Three prior complete whole-package reviews finished, with at least two required; latest whole03 was ZERO actionable P0–P3 on its original bytes. A later CASE-1064 P3 support-output finding supersedes dated readiness and has received this bounded physical-ancestry repair. ROOT repair adoption and NEW COMPLETE whole04 are required. Focused repair tests are not whole04. `REPAIR_ACCEPTANCE_CASE_ALIAS01.md` records these current gates. The unchanged dated `TERMINAL_STATUS.json` and earlier status files preserve their original review counts and meanings. No publication, service or issue action occurred; publication_ready=false, published=false and issues_updated=false remain current flags, and the ascending service gate stays held after PR1032. These workflow gates are not premises of the proof.'
 readme=readme[:start]+replacement+readme[end:]
 readme=readme.replace('Ordinary independent `support.zip` regeneration and `tmp/rebuilt.zip` remain allowed.','Physical existing-ancestor identity, including above absent descendants, enforces that internal outputs are `support.zip` or under `tmp/`, even through case aliases. Ordinary independent `support.zip` regeneration, `tmp/rebuilt.zip` and external ZIP outputs remain allowed.')
 readme+='\n`CASE_ALIAS_SELECTION_LEDGER.json` identifies the two new safe authored evidence copies. The full scope finding is deliberately represented by a clearly labelled PR1064-only excerpt with full-source pins; other PR evidence, private source bodies, old archives, before snapshots and repair scratch remain outside this delivery. `CASE_ALIAS_OUTPUT_PINS.json` is a separate local repaired-stage seal. Earlier seals and historical programs retain their own exact stages and are not promised to replay against this later edition.\n'
 text_replace(PACKAGE/'README.md',readme)
 verifier=(PACKAGE/'verify_package.py').read_text();needle=" require(load('support/CHECKS.json')['pass'] is True,'authored diagnostic record not passed')"
 guard=""" repaired=load('REPAIR_STATUS_CASE_ALIAS01.json')
 require(repaired['stage']=='PENDING_ROOT_CASE_ALIAS_REPAIR_ADOPTION_AND_NEW_COMPLETE_WHOLE04' and repaired['snapshot_date']=='2026-10-16','case-alias repair stage altered')
 require(repaired['whole_package_reviews_completed']==3 and repaired['whole_package_reviews_required']>=2 and repaired['latest_prior_complete_review_actionable_P0_P1_P2_P3']==0,'prior review count or verdict altered')
 require(repaired['bounded_repair_applied'] is True and repaired['new_complete_whole04_required'] is True and repaired['root_repair_adoption_required'] is True and repaired['focused_validation_is_complete_whole_review'] is False,'required fresh review/adoption altered')
 require(all(repaired[k] is False for k in ['ready_for_submission','publication_ready','published','issues_updated']),'current repair gate altered')
 require(repaired['ascending_publication_hold_after_pr']==1032 and repaired['novelty']=='UNKNOWN' and repaired['historical_priority']=='UNKNOWN','repair hold or novelty boundary altered')
"""
 require(verifier.count(needle)==1,'verifier insertion missing');text_replace(PACKAGE/'verify_package.py',verifier.replace(needle,guard+needle))
 selections=[];copies=load(PACKAGE/'COPY_MAP.json')['copies']
 require(len(copies)==163,'old copy count differs')
 for name in ['CASE1064_FINDING.json','MECHANISM.md']:
  source=HERE/name;dest=PACKAGE/'support/history/repairs/case_alias01'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  r=rec(source,AUDIT);entry={'source_path':r['path'],'package_path':dest.relative_to(PACKAGE).as_posix(),'bytes':r['bytes'],'sha256':r['sha256']};copies.append(entry);selections.append(dict(entry,included=True,reason='New authored PR1064-only evidence or mechanism; no third-party body, unrelated PR evidence, raw repository capture or binary.'))
 write(PACKAGE/'CASE_ALIAS_SELECTION_LEDGER.json',{'scope':'All pre-existing163 exact copy records preserved. These two new selected authored records are the entire new copied payload. Full prior selection/omission ledgers remain dated history. Complete immediate custody and individual historical pin resolutions/omissions stay in the local repair folder.','records':selections,'local_only_exclusions':['repairs/case_alias01/before: exact private immediate old bytes including old ZIP; never redistributed','repairs/case_alias01/INPUT_PINS.json: hash-only ALL prior regular audit inputs, including private source/cache/old scratch','repairs/case_alias01 validation scratch, runtime outputs, complete report, process receipts, prior pin resolutions and separate seals: local-only repair evidence','Full root case-alias scope report/adoption: PR1064-only excerpt supplied with full-source hashes; other PR material excluded']})
 write(PACKAGE/'COPY_MAP.json',{'scope':load(PACKAGE/'COPY_MAP.json')['scope'],'copies':copies})
 write(PACKAGE/'SAFE_INPUT_PINS.json',{'scope':'Exact authored selected source bytes; historical copies keep original meanings.','records':copies})
 exclusion=load(PACKAGE/'EXCLUSION_LEDGER.json');exclusion['local_package_files'].append('CASE_ALIAS_OUTPUT_PINS.json');exclusion['source_exclusion_groups'].append({'group':'repairs/case_alias01 private before/hash-only custody, old ZIP, input/source caches and scratch/runtime/process/validation/report/seal trees; full multi-PR root scope material','reason':'Only two individually selected authored PR1064 evidence/mechanism records are added. Full sources remain hash-pinned, scope excerpt labelled. No source bodies, unrelated PR evidence, old binary duplication or omitted-program replay claim.'});write(PACKAGE/'EXCLUSION_LEDGER.json',exclusion)
 allow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members'];allow=sorted(allow+['REPAIR_STATUS_CASE_ALIAS01.json','REPAIR_ACCEPTANCE_CASE_ALIAS01.md','CASE_ALIAS_SELECTION_LEDGER.json']+[r['package_path'] for r in selections]);write(PACKAGE/'SUPPORT_ALLOWLIST.json',{'members':allow})
 write(PACKAGE/'SUPPORT_MANIFEST.json',{'entries':[rec(PACKAGE/n,PACKAGE) for n in allow if n!='SUPPORT_MANIFEST.json']})
 # Construct separately from the supplied builder; close before binding/hash checks.
 temp=PACKAGE/'tmp/case_alias01-build.zip';temp.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for n in allow:
   info=zipfile.ZipInfo(n,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;info.internal_attr=0
   z.writestr(info,(PACKAGE/n).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 temp.replace(PACKAGE/'support.zip')
 binding=load(PACKAGE/'publication/DEPOSIT_BINDING.json');binding['support_archive']=rec(PACKAGE/'support.zip',PACKAGE);write(PACKAGE/'publication/DEPOSIT_BINDING.json',binding)
 write(PACKAGE/'CASE_ALIAS_OUTPUT_PINS.json',{'utc':utc(),'stage':status['stage'],'root_repair_adoption_required':True,'new_complete_whole04_required':True,'publication_ready':False,'entries':[rec(p,PACKAGE) for p in packagefiles() if p.name!='CASE_ALIAS_OUTPUT_PINS.json']})
 print(json.dumps({'modified_permitted_existing':len(CHANGED),'new_exact_copies':len(selections),'archive':rec(PACKAGE/'support.zip',PACKAGE),'members':len(allow),'current_files':len(packagefiles())},indent=2))
if __name__=='__main__':prepare()
