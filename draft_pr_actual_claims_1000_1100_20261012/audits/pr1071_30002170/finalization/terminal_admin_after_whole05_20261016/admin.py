"""Bounded administrative reconciliation after root-adopted whole05; no math review."""
import collections, difflib, hashlib, json, os, shutil, stat, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent; A=D.parents[1]; P=A/'NEWpreprint_v1_0'
ZIP='PR1071_preprint_v1_0_support.zip'
CHANGES=['README.md','SUPPLEMENT.md','scripts/verify_package.py','INPUT_COPY_MAP.json','PACKAGE_MANIFEST.json','UPLOAD_BINDINGS.json',ZIP,ZIP+'.sha256']
SELECT=['REPORT.md','INDEPENDENT_DERIVATION.md','VERDICT.json','SOURCE_READ_LEDGER.json','INPUT_FREEZE.json','OUTPUT_PINS.json','SEAL.json','CUSTODY_FULL_REPLAY.json','NEW_MATH_CONTROLS.json','FULL_JSON_RUNTIME_COMPARISON.json','INTERFACE_CONTROLS.json','COMMAND_SUMMARY.json','FAILED_UNRECORDED_ATTEMPTS.md','VISUAL_REVIEW.json']
ROOTS=['ROOT_WHOLE_PACKAGE_REVIEW_05.json','ROOT_HISTORY_ORDER_REPAIR_REVIEW_01.json']
def now():return datetime.now(timezone.utc).isoformat()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,n):
 s=p.lstat();need(stat.S_ISREG(s.st_mode),'Not regular '+str(p));h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':str(n),'bytes':s.st_size,'sha256':h.hexdigest(),'mode':stat.S_IMODE(s.st_mode),'nlink':s.st_nlink}
def basic(p,n):return {k:v for k,v in pin(p,n).items() if k in ['path','bytes','sha256']}
def walk(root,exclude=None):
 files=[];links=[]
 for current,dirs,names in os.walk(root,followlinks=False):
  cur=Path(current)
  dirs[:]=sorted(x for x in dirs if cur/x!=exclude)
  for name in list(dirs):
   q=cur/name
   if q.is_symlink():links.append({'path':str(q.relative_to(root)),'kind':'symlink','target':os.readlink(q)});dirs.remove(name)
  for name in sorted(names):
   q=cur/name
   if q.is_symlink():links.append({'path':str(q.relative_to(root)),'kind':'symlink','target':os.readlink(q)})
   elif q.is_file():files.append(pin(q,q.relative_to(root)))
 return sorted(files,key=lambda r:r['path']),sorted(links,key=lambda r:r['path'])
def log(t,pct):
 with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — '+str(pct)+'% of bounded terminal administration: '+t+'\n')
def freeze():
 need(not (D/'BASELINE_INPUT_PINS.json').exists(),'Already frozen')
 files,links=walk(A,D);write(D/'BASELINE_INPUT_PINS.json',{'utc':now(),'scope':'Every preexisting regular audit file, no traversal through symlink parents; this new effort excluded. Symlink fixtures have separate target-only identities.','records':files});write(D/'PREEXISTING_SYMLINK_FIXTURES.json',{'utc':now(),'records':links})
 (D/'.gitignore').write_text('/before/NEWpreprint_v1_0/'+ZIP+'\n/before/NEWpreprint_v1_0/'+ZIP+'.sha256\n/private/\n/__pycache__/\n')
 before=[]
 for n in CHANGES:
  src=P/n;dst=D/'before/NEWpreprint_v1_0'/n;dst.parent.mkdir(parents=True,exist_ok=True)
  with src.open('rb') as s,dst.open('xb') as t:shutil.copyfileobj(s,t);t.flush();os.fsync(t.fileno())
  need(src.read_bytes()==dst.read_bytes(),'Before unequal '+n)
  r=pin(src,src.relative_to(A));before.append({**r,'original_path':r['path'],'before_snapshot':str(dst.relative_to(A))})
 for parent in {(D/'before/NEWpreprint_v1_0'),D}:
  fd=os.open(parent,os.O_RDONLY);os.fsync(fd);os.close(fd)
 need(before[-2]['bytes']==1961321 and before[-2]['sha256']=='66ad5ff8ef7e4adb3d9870866c1c3f2b5dc3717a245a5a241a7cd1da7c6a3515','Original archive identity')
 write(D/'BEFORE_PINS.json',{'utc':now(),'records':before,'old_archive_and_sidecar_durable_individually_ignored_before_any_archive_mutation':True})
 log('Whole05 report, derivation, source scopes, failed-attempt ledger and root adoption read. All preexisting regular files frozen without following symlink parents. Eight existing interfaces durably copied, including exact old archive/sidecar with individual ignore entries. No candidate mutation yet.',20)
 print(json.dumps({'regular_inputs':len(files),'fixture_links':len(links),'before':len(before)}))
def mutate():
 need(not (P/'TERMINAL_AFTER_WHOLE05_STATUS.json').exists(),'Already mutated')
 root=read(A/ROOTS[0]);need(root['status']=='ROOT_ADOPT_COMPLETE_WHOLE05_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN' and root['whole_reviews_completed']==5 and root['finding_counts']==dict.fromkeys(['P0','P1','P2','P3'],0),'Root adoption prerequisite')
 old=read(D/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json');need(len(old['copies'])==153,'153 prior copies')
 copies=list(old['copies']);new=[]
 def copy(src,rel,original=None):
  dst=P/rel;need(not dst.exists(),'Copy exists '+rel);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);r=basic(src,'')
  row={'original_path':original or str(src.relative_to(A)),'package_copy':rel,'bytes':r['bytes'],'sha256':r['sha256'],'byte_exact':True,'meaning':'Exact authored evidence or before-interface snapshot. Dated status/counter/false-order claims retain historical scope; terminal after-whole05 status governs current workflow, pending external ROOT final integrity.'}
  if original:row['source_snapshot']=str(src.relative_to(A))
  copies.append(row);new.append(rel)
 for n in CHANGES:
  if n not in [ZIP,ZIP+'.sha256']:copy(D/'before/NEWpreprint_v1_0'/n,'history/pre_terminal_after_whole05/'+n,'NEWpreprint_v1_0/'+n)
 W=A/'reviews/package_05';inventory=read(W/'OUTPUT_PINS.json');need(len(inventory['records'])==903 and len(inventory['symlink_fixtures'])==3,'Whole05 inventory counts')
 decisions=[]
 for r in inventory['records']:
  p=W/r['path'];actual=pin(p,r['path']);need(actual==r,'Whole05 exact row '+r['path'])
  selected=r['path'] in SELECT
  if selected:reason='Selected complete authored report, independent derivation, verdict, scoped source ledger, custody/replay/interface summary or failure disclosure; not an omitted raw program replay claim.'
  elif r['path'].startswith('scratch/'):reason='Owned retained review fixture/extraction/checker/compiler product; not selected for redistribution. Identity retained, no execution newly claimed from this omission.'
  elif r['path'].endswith(('.png','.pdf','.zip')):reason='Rendered pixels or duplicate/failed archive artifact retained locally; excluded from the distribution.'
  elif r['path'].endswith(('.stdout','.stderr','.jsonl','.py')):reason='Raw execution stream/command ledger or review program retained locally; selected inventories pin it without redistributing or claiming new replay.'
  else:reason='Unselected review-authored finite diagnostic, receipt, private configuration or checkpoint; individually pinned locally, selected complete report defines its scope.'
  decisions.append({'original_path':'reviews/package_05/'+r['path'],**{k:v for k,v in r.items() if k!='path'},'kind':'regular','selected':selected,'reason':reason,**({'package_copy':'custody/reviews/package_05/'+r['path']} if selected else {})})
 for r in inventory['symlink_fixtures']:
  p=W/r['path'];need(p.is_symlink() and os.readlink(p)==r['target'],'Fixture target drift')
  decisions.append({'original_path':'reviews/package_05/'+r['path'],'kind':'symlink','target':r['target'],'selected':False,'reason':'Owned symlink fixture identity is its link target, not a regular body; never followed or redistributed.'})
 for n in SELECT:
  copy(W/n,'custody/reviews/package_05/'+n)
  if n in ['OUTPUT_PINS.json','SEAL.json']:decisions.append({'original_path':'reviews/package_05/'+n,**{k:v for k,v in pin(W/n,n).items() if k!='path'},'kind':'regular','selected':True,'package_copy':'custody/reviews/package_05/'+n,'reason':'Complete inventory or separate final seal; binds retained omitted outputs without raw-program replay or redistribution claim.'})
 for n in ROOTS:copy(A/n,'custody/'+n)
 stamp=now();write(P/'WHOLE05_DISTRIBUTION_DECISIONS.json',{'utc':stamp,'scope':'Every903 regular OUTPUT_PINS inventory row and3 fixture symlinks decided individually, plus the inventory and its separate seal. Included inventories bind omitted local artifacts; they do not claim raw-program replay or redistribution. Source-read scopes are limited to the actual ledger descriptions, never whole-body truth.','source_inventory':basic(W/'OUTPUT_PINS.json','reviews/package_05/OUTPUT_PINS.json'),'inventory_regular_rows':903,'inventory_symlink_rows':3,'records':decisions})
 excluded=[{**basic(D/'before/NEWpreprint_v1_0'/n,str((D/'before/NEWpreprint_v1_0'/n).relative_to(A))),'reason':'Exact durable pre-terminal archive/sidecar retained individually ignored outside public distribution; recursive old archives are omitted.'} for n in [ZIP,ZIP+'.sha256']]
 write(P/'TERMINAL_AFTER_WHOLE05_COPY_EXCLUSIONS.json',{'utc':stamp,'records':excluded})
 status={'utc':stamp,'state':'TERMINAL_ADMIN_COMPLETE_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','pr':1071,'head':'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','fresh_whole_package_reviews_completed':5,'minimum_fresh_reviews_required':2,'latest_review':'custody/reviews/package_05/VERDICT.json','root_review_adoption':'custody/ROOT_WHOLE_PACKAGE_REVIEW_05.json','latest_complete_review_findings':dict.fromkeys(['P0','P1','P2','P3'],0),'new_complete_whole_review_currently_required':False,'terminal_administration_complete':True,'root_final_integrity_required':True,'root_final_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'current_qualification':'HISTORY_ORDER_QUALIFICATION.json','supersedes_workflow_only':['STATUS.json','CURRENT_STATUS.json','TERMINAL_STATUS.json','CASE_ALIAS_REPAIR_STATUS.json','PORTABILITY_REPAIR_STATUS.json','HISTORY_ORDER_REPAIR_STATUS.json'],'meaning':'Five complete whole reviews, minimum two; latest whole05 has zero actionable P0–P3 findings and is root-adopted. No further complete whole review is currently required. This bounded terminal administration requires a new external ROOT final integrity adoption, which is not yet adopted here. Only that later external ROOT final seal may override readiness. Every earlier seal/status/counter and raw false global-order claim remains dated history. Services stay held after PR1032.'}
 write(P/'TERMINAL_AFTER_WHOLE05_STATUS.json',status)
 notes='''# Terminal administration after root-adopted whole05

STAMP

Five NEW complete whole-package reviews have completed (minimum two). Latest whole05 has zero actionable P0, P1, P2 or P3 findings and ROOT adopted it in custody/ROOT_WHOLE_PACKAGE_REVIEW_05.json. No further complete whole review is currently required. TERMINAL_AFTER_WHOLE05_STATUS.json governs current workflow: bounded terminal administration is complete, but a NEW external ROOT final integrity adoption is REQUIRED and UNADOPTED. publication_ready=false, issues_resolved=false, published=false; services held after PR1032. A later external ROOT final seal governs any subsequent readiness; this internal status cannot confer it. Earlier FINAL seals, statuses and counters remain exact dated history.

The unchanged HISTORY_ORDER_QUALIFICATION.json governs the earlier false global-order assertion:939 positions differ because intact633-row audit and306-row candidate blocks were swapped. The exact multiset and every stage's internal order, first2788 global rows and all4346 historical byte identities remain preserved. The raw false assertion remains sealed history and is explicitly superseded, without retconning it.

The analytic manuscript/PDF, original finite checker/expected baseline, native bibliographic objects, citation, path policy and finite runtime acceptance contract are unchanged. The claim covers each fixed H in(1/4,1), all T>0, n>=1, every L2 estimator from both uniform grids, independent standard equal-H components and canonical X. Brownian optimum and smooth rate are prior. There is no endpoint, H-uniform, sharp/adaptive/nonuniform/unequal/correlated claim. Full novelty, method/theorem priority and worldwide current openness stay UNKNOWN. The source ledger records10 retained identities and7 text identities with actual semantic scopes; identity alone is not whole-body truth. Dickinson and complete Jackowski implications remain unresolved.

Whole05 recorded306 child commands:57 successes,248 intended rejections and1 unexpected custody-harness failure, corrected through a later fully recorded retry. Initial ENOSPC interface-suite child exit is UNKNOWN and not counted complete; the later recorded retry passed. Review-local quoting/schema/prefix errors were not candidate findings. Deeper disk causes remain UNKNOWN. The prior reviewer actually compiled four byte-equal PDFs and viewed all seven rendered pages; this bounded administration does not repeat compilation/rendering of unchanged paper bytes.

All prior153 copy rows retain their exact order and values, including50/83/116/128/140 prefixes. Six before-interface snapshots and16 safe complete authored review/root records are appended. Every903 whole05 regular inventory row and3 fixture symlink targets is individually selected or omitted with a reason. Raw programs/streams/source bodies/images/duplicate archives/runtime fixtures remain locally pinned; including inventories makes no new replay or redistribution claim. The old current ZIP and sidecar were durably retained and individually ignored before any mutation, outside the public distribution.

The actual native LOCAL-only uploader input remains external publication/zenodo-deposit.json with metadata/files; its metadata and two selected names remain unchanged. Included deposit.json is a historical metadata wrapper. No Git, index, branch, service operation, outreach, other-shard edit, delegated review or new mathematical review is performed by this bounded administration.
'''.replace('STAMP',stamp)
 (P/'TERMINAL_AFTER_WHOLE05_NOTES.md').write_text(notes)
 readme=(P/'README.md').read_text();readme=readme.replace('HISTORY_ORDER_REPAIR_STATUS.json now governs current workflow: four complete whole reviews (minimum two), whole04 one local custody reporting P3, bounded qualification applied, root repair adoption then a NEW COMPLETE whole05 and root terminal adoption required.','HISTORY_ORDER_REPAIR_STATUS.json preserves the dated history-order repair stage. TERMINAL_AFTER_WHOLE05_STATUS.json now governs current workflow: five complete whole reviews (minimum two), latest whole05 zero actionable findings and root-adopted, no further complete whole review currently required; terminal administration complete but NEW external ROOT final integrity REQUIRED and UNADOPTED.')
 readme=readme.replace('and currently by HISTORY_ORDER_REPAIR_STATUS.json for workflow accounting.','by HISTORY_ORDER_REPAIR_STATUS.json at that dated stage, and currently by TERMINAL_AFTER_WHOLE05_STATUS.json for workflow accounting.')
 start=readme.index('## Current support hold and review accounting')
 readme=readme[:start]+'''## Current support hold and review accounting

Five NEW complete whole reviews are complete (minimum two). Latest whole05 found zero actionable P0–P3 issues and is root-adopted. No further complete whole review is currently required. TERMINAL_AFTER_WHOLE05_STATUS.json governs current workflow: terminal administration is complete, but NEW external ROOT final integrity is REQUIRED and UNADOPTED. Readiness/issues-resolved/published remain false; services held after PR1032. Only a later external ROOT final seal can override readiness. All earlier statuses/counters/FINAL seals retain dated meanings.

HISTORY_ORDER_QUALIFICATION.json remains unchanged: the old global-order claim is false because intact633-row audit and306-row candidate blocks were swapped within1558 later references, changing939 global positions. The exact row multiset, each stage's internal order, first2788 global rows and all4346 byte identities are preserved. The raw false assertion remains sealed dated history and explicitly superseded. PORTABILITY_REPAIR_NOTES.md still defines the unchanged finite runtime contract.

The external native uploader input remains publication/zenodo-deposit.json with metadata/files in the audit tree; included deposit.json remains a historical metadata wrapper. All prior153 ordered copy rows and50/83/116/128/140 prefixes remain exact; six before-interface snapshots and16 complete safe authored whole05/root records are appended. WHOLE05_DISTRIBUTION_DECISIONS.json decides every903 regular inventory row and3 fixture link targets individually. Inventories pin omitted raw programs/streams/bodies/images/fixtures without claiming new replay or redistribution. Old ZIP/sidecar remain durably retained outside the distribution. The mathematical paper/PDF, native bibliographic objects, citation, source boundaries and UNKNOWN priority/novelty/current-open qualifications are unchanged. See TERMINAL_AFTER_WHOLE05_NOTES.md for actual historical execution/failure scopes and final adoption requirements.
'''
 (P/'README.md').write_text(readme)
 sup=(P/'SUPPLEMENT.md').read_text();sup=sup.replace('The current HISTORY_ORDER_REPAIR_STATUS.json gate requires root repair adoption, then a NEW COMPLETE whole05 and root terminal adoption; four complete reviews have finished, with one local reporting P3 in whole04.','The current TERMINAL_AFTER_WHOLE05_STATUS.json gate records five completed complete whole reviews, minimum two, latest whole05 zero actionable and root-adopted, no further complete whole review currently required; terminal administration complete but NEW external ROOT final integrity REQUIRED and UNADOPTED.')
 sup=sup.replace('the final history-order paragraph below gives the current gate.','the final after-whole05 paragraph below gives the current gate.').replace('Current history-order correction (','Dated history-order correction (').replace('HISTORY_ORDER_REPAIR_STATUS.json now governs root repair adoption, NEW COMPLETE whole05 and root terminal adoption;','HISTORY_ORDER_REPAIR_STATUS.json governed root repair adoption, NEW COMPLETE whole05 and root terminal adoption at that dated stage;')
 sup+='\nCurrent after-whole05 terminal administration ('+stamp+'): five NEW complete whole reviews completed (minimum two), latest whole05 zero actionable P0–P3 and root-adopted. No further complete whole review is currently required. TERMINAL_AFTER_WHOLE05_STATUS.json now governs workflow: terminal administration complete, NEW external ROOT final integrity REQUIRED and UNADOPTED, publication_ready/issues_resolved/published=false, services held after PR1032. Only the later external ROOT final seal may override readiness. All earlier seals/status counters and raw false order claims remain dated history. The unchanged explicit history-order qualification remains authoritative. All153 prior ordered copy rows and earlier prefixes are preserved; six exact before-interface copies and16 complete safe authored whole05/root records are added. Every903 regular whole05 inventory row and3 fixture targets is individually decided; raw bodies/programs/streams/images/fixtures stay locally pinned without new replay/redistribution claims. The native external metadata/files input, included historical wrapper distinction, mathematical/PDF/TeX, citation, source-version/UNKNOWN qualifications, checker/baseline, physical path and finite runtime policies are unchanged. Latest review actually compiled four byte-equal PDFs and viewed all seven pages; unchanged paper is not recompiled/rendered here. See TERMINAL_AFTER_WHOLE05_NOTES.md for exact failure and pending-adoption scopes.\n'
 (P/'SUPPLEMENT.md').write_text(sup)
 code=(P/'scripts/verify_package.py').read_text();marker="    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:";need(code.count(marker)==1,'Verifier anchor');insert=(D/'verifier_insertion.txt').read_text();(P/'scripts/verify_package.py').write_text(code.replace(marker,insert+'\n'+marker))
 need(copies[:153]==old['copies'] and len(copies)==175,'Prior copy prefix');write(P/'INPUT_COPY_MAP.json',{**old,'scope':old['scope']+'; terminal after-whole05 safe complete authored evidence and exact before-interface history appended after all153 unchanged ordered rows; omitted inventory rows individually decided.','copies':copies})
 m=read(D/'before/NEWpreprint_v1_0/PACKAGE_MANIFEST.json');names={r['path'] for r in m['members']}|set(new)|{'TERMINAL_AFTER_WHOLE05_STATUS.json','TERMINAL_AFTER_WHOLE05_NOTES.md','WHOLE05_DISTRIBUTION_DECISIONS.json','TERMINAL_AFTER_WHOLE05_COPY_EXCLUSIONS.json'}
 m['policy']+='; terminal after root-adopted zero-finding whole05, five/minimum2, explicit pending external ROOT final integrity,16 narrow complete authored review/root records and6 before interfaces; all153 prior ordered copies unchanged, every903 regular/3 link inventory row decided.';m['members']=[basic(P/n,n) for n in sorted(names)];write(P/'PACKAGE_MANIFEST.json',m)
 rebuild();write(D/'BUILD_SUMMARY.json',{'utc':now(),'archive':basic(P/ZIP,ZIP),'archive_members':len(names)+1,'copy_rows':len(copies),'prior153_exact_ordered_prefix':True,'new_copies':new,'selected_complete_review_and_root_records':16,'old_archive_before':str((D/'before/NEWpreprint_v1_0'/ZIP).relative_to(A))})
 log('Current workflow appended after root-adopted whole05. Earlier statuses/qualification left exact. All153 prior copy rows preserved; six before interfaces and16 complete authored records appended, every903 regular/3 symlink inventory row decided. Deterministic ZIP and external bindings rebuilt. Independent bounded controls still pending.',50)
 print(json.dumps(read(D/'BUILD_SUMMARY.json'),indent=2))
def rebuild():
 m=read(P/'PACKAGE_MANIFEST.json');names=sorted([r['path'] for r in m['members']]+['PACKAGE_MANIFEST.json']);temp=P/(ZIP+'.after-whole05-tmp');need(not temp.exists(),'Archive temp exists')
 with zipfile.ZipFile(temp,'x',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
  for n in names:
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(P/n).read_bytes())
 os.replace(temp,P/ZIP);r=basic(P/ZIP,ZIP);(P/(ZIP+'.sha256')).write_text(r['sha256']+'  '+ZIP+'\n');b=read(P/'UPLOAD_BINDINGS.json');b['archive']['bytes']=r['bytes'];b['archive']['sha256']=r['sha256'];b['manifest_sha256']=basic(P/'PACKAGE_MANIFEST.json','')['sha256'];write(P/'UPLOAD_BINDINGS.json',b)
if __name__=='__main__':{'freeze':freeze,'mutate':mutate}[sys.argv[1]]()
