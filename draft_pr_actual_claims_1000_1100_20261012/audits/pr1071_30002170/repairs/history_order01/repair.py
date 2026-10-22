"""Append a scoped current correction; never rewrite prior sealed records."""
import collections, difflib, hashlib, json, os, shutil, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent; A=D.parents[1]; P=A/'NEWpreprint_v1_0'
ZIP='PR1071_preprint_v1_0_support.zip'
CHANGES=['README.md','SUPPLEMENT.md','scripts/verify_package.py','INPUT_COPY_MAP.json','PACKAGE_MANIFEST.json','UPLOAD_BINDINGS.json',ZIP,ZIP+'.sha256']
def now(): return datetime.now(timezone.utc).isoformat()
def need(ok,msg):
 if not ok: raise RuntimeError(msg)
def read(p): return json.loads(p.read_text())
def pin(p,n):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return {'path':str(n),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
def write(p,o):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+'\n')
def log(text,percent):
 with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — '+str(percent)+'% of bounded WHOLE04-P3-01 repair: '+text+'\n')
def freeze():
 need(not (D/'BASELINE_INPUT_PINS.json').exists(),'Already frozen')
 baseline=[pin(f,f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and D not in f.parents]
 write(D/'BASELINE_INPUT_PINS.json',{'utc':now(),'records':baseline,'scope':'Every preexisting regular audit file; this effort excluded.'})
 rows=[]
 for name in CHANGES:
  src=P/name;dst=D/'before/NEWpreprint_v1_0'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
  r=pin(src,src.relative_to(A));need(pin(dst,'')['sha256']==r['sha256'],'Before equality')
  rows.append({'original_path':r['path'],'before_snapshot':str(dst.relative_to(A)),'bytes':r['bytes'],'sha256':r['sha256']})
 write(D/'BEFORE_PINS.json',{'utc':now(),'records':rows})
 need(rows[-2]['bytes']==1773348 and rows[-2]['sha256']=='11a16cbe77cc084cf1ac50f4396159ad7ddd3b301a888adbf5b38613d771dbeb','Original ZIP identity')
 log('Full report/root adoption/order evidence read. Exact baseline frozen; eight bounded current interfaces copied before changes, including original1773348-byte182-member ZIP. Old sealed order assertion is false only globally; mathematical/native/path/runtime assets are protected. No Git/services/outreach/subagents.',20)
 print(json.dumps({'baseline':len(baseline),'before':len(rows)}))
def mutate():
 need(not (P/'HISTORY_ORDER_REPAIR_STATUS.json').exists(),'Already applied')
 old=read(A/'repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json');late=read(A/'repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json')
 keys=['stage','captured_path','bytes','sha256']
 project=lambda r:{k:r[k] for k in keys}
 before=[project(r) for r in old['additional_terminal_rows']];after=[project(r) for r in late['records'][2788:]]
 need(len(before)==len(after)==1558,'1558 count')
 first=[project(r) for r in old['records']];need(first==[project(r) for r in late['records'][:2788]],'First2788 order')
 sig=lambda rows:hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 need(collections.Counter(map(lambda x:json.dumps(x,sort_keys=True),before))==collections.Counter(map(lambda x:json.dumps(x,sort_keys=True),after)),'multiset')
 mismatches=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b];need(len(mismatches)==939 and mismatches[0]==30,'Counterexample count')
 quant=read(A/'reviews/package_04/ORDER_QUANTIFICATION.json')
 stages=[]
 for stage in ['OUTPUT_PINS.json','CURRENT_CANDIDATE_PINS.json','CURRENT_AUDIT_PINS.json','PROTECTED_UNCHANGED.json']:
  b=[r for r in before if r['stage']==stage];a=[r for r in after if r['stage']==stage];need(b==a,'Per-stage order')
  stages.append({'stage':stage,'count':len(b),'before_and_after_projected_rows_sha256':sig(b),'internal_values_and_order_preserved':True})
 stamp=now()
 qualification={'utc':stamp,'finding':'WHOLE04-P3-01','kind':'CURRENT_SUPERSEDING_LOCAL_CUSTODY_ORDER_QUALIFICATION','historical_false_claim':{'path':'repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json','field':'additional1558_values_and_order_preserved','recorded_value':True,'truth_for_global_order':False,'also_report':'repairs/portability01/REPORT.md:122-124','preserved_as_dated_history':True},'original2788_global_values_and_order_preserved':True,'additional1558_global_order_preserved':False,'additional1558_exact_row_multiset_preserved':True,'additional1558_per_stage_values_and_order_preserved':True,'mismatched_global_additional_positions':939,'first_mismatch_additional_zero_based':30,'first_mismatch_global_zero_based':2818,'before_groups':quant['before_groups'],'after_groups':quant['after_groups'],'before_projected_rows_sha256':sig(before),'after_projected_rows_sha256':sig(after),'projection_keys':keys,'projection_digest_encoding':'UTF-8 JSON sort_keys=True,separators=(comma,colon); array order retained','per_stage':stages,'first_difference':{'before':before[30],'after':after[30]},'source_records':[pin(A/'repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json','repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json'),pin(A/'repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json','repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json')],'historical_references':4346,'historical_byte_resolution_claim':'All4346 original historical references resolve to exact retained bytes; global order correction changes no referenced bytes. Current local repair receipts independently rehash each locator.','scope':'Local custody report only. No mathematical, paper/PDF, native bibliographic metadata, path policy, historical finite checker, baseline or runtime change. The raw false historical assertion is retained and explicitly superseded here.'}
 write(P/'HISTORY_ORDER_QUALIFICATION.json',qualification)
 status={'utc':stamp,'state':'PENDING_NEW_COMPLETE_WHOLE05_AFTER_HISTORY_ORDER_QUALIFICATION','pr':1071,'head':'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','fresh_whole_package_reviews_completed':4,'minimum_fresh_reviews_required':2,'latest_complete_review_findings':{'P0':0,'P1':0,'P2':0,'P3':1},'bounded_repair_findings_fixed':['WHOLE04-P3-01'],'new_complete_whole_review_required':5,'new_complete_whole_review_completed':False,'root_repair_adoption_required':True,'root_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'qualification':'HISTORY_ORDER_QUALIFICATION.json','latest_review':'custody/reviews/package_04/VERDICT.json','root_review_adoption':'custody/ROOT_WHOLE_PACKAGE_REVIEW_04.json','meaning':'Four complete reviews finished, minimum two. Whole04 has one scoped local reporting P3; this bounded explicit qualification is pending root repair adoption, a NEW COMPLETE whole05, then root terminal adoption. All earlier statuses/counters/seals and the raw false order claim retain dated history. This repair grants no readiness.'}
 write(P/'HISTORY_ORDER_REPAIR_STATUS.json',status)
 notes=stamp+'\n\n# Historical custody order correction\n\nWHOLE04-P3-01 found the unqualified additional1558_values_and_order_preserved=true claim in repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json and its REPORT.md false for global order. Those sealed raw records remain byte-exact dated history. HISTORY_ORDER_QUALIFICATION.json explicitly supersedes that claim; it does not silently repair old evidence.\n\nThe old additional1558 sequence is OUTPUT_PINS30, CURRENT_CANDIDATE_PINS306, CURRENT_AUDIT_PINS633, PROTECTED_UNCHANGED589. The portability sequence is OUTPUT_PINS30, CURRENT_AUDIT_PINS633, CURRENT_CANDIDATE_PINS306, PROTECTED_UNCHANGED589. The two intact middle blocks were permuted;939 global positions differ, beginning at additional zero-based30/global2818. Exact row multiset and every stage\'s internal values/order are preserved. The first2788 rows retain global order. All4346 referenced bytes remain exactly resolvable. The two source-ledger pins, canonical projected-array digests, per-stage digests, group boundaries and first difference make the correction checkable.\n\nFour NEW complete whole reviews have finished (minimum two); latest whole04 has one P3. HISTORY_ORDER_REPAIR_STATUS.json now governs current workflow: bounded qualification pending root repair adoption, then a NEW COMPLETE whole05 and root terminal adoption. publication_ready=false, issues_resolved=false, published=false; services held after PR1032. All old status records are dated stages. The mathematical claim, source/PDF, native metadata, citation, finite runtime contract and UNKNOWN priority/novelty/current-open qualifications retain their exact scope. This repair is not whole05 or terminal administrative adoption. No Git, service, communication, new compile/render/PDF marker or omitted-program replay is performed.\n'
 (P/'HISTORY_ORDER_REPAIR_NOTES.md').write_text(notes)
 oldmap=read(D/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json');need(len(oldmap['copies'])==140,'140 prefix')
 copies=list(oldmap['copies']);newnames=[]
 def add(src,rel,original=None,source_snapshot=None):
  dst=P/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);r=pin(src,'')
  row={'original_path':original or str(src.relative_to(A)),'package_copy':rel,'bytes':r['bytes'],'sha256':r['sha256'],'byte_exact':True,'meaning':'Exact authored before-stage or whole04 evidence; historical claims retain dated scope and are superseded by HISTORY_ORDER_QUALIFICATION.json for global custody order.'}
  if source_snapshot:row['source_snapshot']=source_snapshot
  copies.append(row);newnames.append(rel)
 for name in CHANGES:
  if name in [ZIP,ZIP+'.sha256']:continue
  src=D/'before/NEWpreprint_v1_0'/name
  add(src,'history/pre_history_order01/'+name,'NEWpreprint_v1_0/'+name,str(src.relative_to(A)))
 for name in ['REPORT.md','VERDICT.json','OUTPUT_PINS.json','SEAL.json','ORDER_QUANTIFICATION.json','HISTORICAL_ORDER_COUNTEREXAMPLE.json']:
  add(A/'reviews/package_04'/name,'custody/reviews/package_04/'+name)
 add(A/'ROOT_WHOLE_PACKAGE_REVIEW_04.json','custody/ROOT_WHOLE_PACKAGE_REVIEW_04.json')
 need(copies[:140]==oldmap['copies'],'Prefix changed');oldmap['copies']=copies;write(P/'INPUT_COPY_MAP.json',oldmap)
 excluded=[]
 for name in [ZIP,ZIP+'.sha256']:
  src=D/'before/NEWpreprint_v1_0'/name;excluded.append({**pin(src,src.relative_to(A)),'reason':'Exact original pre-history-order archive/sidecar retained locally; excluded from redistribution to avoid recursively carrying old archives.'})
 write(P/'HISTORY_ORDER_COPY_EXCLUSIONS.json',{'utc':stamp,'records':excluded})
 readme=(P/'README.md').read_text();readme=readme.replace('and currently by PORTABILITY_REPAIR_STATUS.json for workflow accounting.','then by PORTABILITY_REPAIR_STATUS.json, and currently by HISTORY_ORDER_REPAIR_STATUS.json for workflow accounting.')
 readme=readme.replace('PORTABILITY_REPAIR_STATUS.json now governs current workflow: three complete whole reviews (minimum two), whole03 one new P3 support finding, bounded portability repair applied, root repair adoption then a NEW COMPLETE whole04 and root terminal adoption required.','PORTABILITY_REPAIR_STATUS.json preserves the dated portability stage. HISTORY_ORDER_REPAIR_STATUS.json now governs current workflow: four complete whole reviews (minimum two), whole04 one local custody reporting P3, bounded qualification applied, root repair adoption then a NEW COMPLETE whole05 and root terminal adoption required.')
 start=readme.index('## Current support hold and review accounting')
 readme=readme[:start]+'''## Current support hold and review accounting

Four NEW complete whole reviews are complete (minimum two). Latest whole04 retained the mathematics and distribution interfaces and found WHOLE04-P3-01, a local custody reporting claim: the portability ledger swapped intact633-row CURRENT_AUDIT and306-row CURRENT_CANDIDATE blocks within1558 later references. Exactly939 global positions differ; the row multiset, every stage's internal values/order, first2788 global rows and all4346 referenced byte identities are preserved. The old unqualified global-order claim is false and remains sealed dated history, explicitly superseded by HISTORY_ORDER_QUALIFICATION.json and HISTORY_ORDER_REPAIR_NOTES.md.

HISTORY_ORDER_REPAIR_STATUS.json governs the current gate: root repair adoption, then a NEW COMPLETE whole05 and root terminal adoption are required. This bounded correction is neither whole05 nor readiness authority. Readiness/issues-resolved/published remain false; services held after PR1032. All earlier statuses/counters/seals retain dated meanings. PORTABILITY_REPAIR_NOTES.md still defines the unchanged finite runtime contract.

The external native uploader input remains publication/zenodo-deposit.json in the audit tree; its unchanged metadata equals the three unchanged bibliographic objects and it selects unchanged paper.pdf and the same-named current support ZIP. Included deposit.json remains a historical metadata wrapper. Every prior140 exact copy-map row remains unchanged and ordered, including its original128-row prefix; six exact before-interface snapshots and seven safe authored whole04/root records are appended. Old archives and raw evidence remain individually pinned locally. The analytic theorem, source/PDF, citation, source-version boundaries and UNKNOWN priority/novelty/current-open qualifications are unchanged.
'''
 (P/'README.md').write_text(readme)
 sup=(P/'SUPPLEMENT.md').read_text();sup=sup.replace('The current portability gate requires root repair adoption, then a NEW COMPLETE whole04 and root terminal adoption; three complete reviews have finished, with one new P3 in whole03.','The current HISTORY_ORDER_REPAIR_STATUS.json gate requires root repair adoption, then a NEW COMPLETE whole05 and root terminal adoption; four complete reviews have finished, with one local reporting P3 in whole04.')
 sup=sup.replace('the final portability paragraph below gives the current gate.','the final history-order paragraph below gives the current gate.').replace('Current CASE-1071 support repair (','Dated CASE-1071 support repair (').replace('CASE_ALIAS_REPAIR_STATUS.json governs the current support hold:','CASE_ALIAS_REPAIR_STATUS.json governed that dated support hold:').replace('Current portability repair (','Dated portability repair (').replace('PORTABILITY_REPAIR_STATUS.json supersedes earlier workflow claims:','PORTABILITY_REPAIR_STATUS.json superseded earlier workflow claims at that dated stage:')
 sup+='\nCurrent history-order correction ('+stamp+'): four NEW complete whole reviews have completed (minimum two); whole04 found only WHOLE04-P3-01 in local custody reporting. The sealed portability statement that all1558 later rows preserve global order is false: intact633-row CURRENT_AUDIT and306-row CURRENT_CANDIDATE blocks were permuted, changing939 global positions starting at additional30/global2818. Exact row multiset and each stage\'s internal values/order are preserved, first2788 rows retain global order, and all4346 historical byte references resolve exactly. HISTORY_ORDER_QUALIFICATION.json explicitly supersedes the raw historical claim without rewriting it. HISTORY_ORDER_REPAIR_STATUS.json now governs root repair adoption, NEW COMPLETE whole05 and root terminal adoption; publication_ready/issues_resolved/published=false and services held after PR1032. Six exact before-interface copies and seven safe authored whole04/root records extend all140 prior ordered copy rows. All old sealed records and raw false claims remain dated history. No mathematical/PDF/TeX, native metadata, path policy, finite runtime contract, original checker/baseline, citation or priority qualification change is asserted.\n'
 (P/'SUPPLEMENT.md').write_text(sup)
 code=(P/'scripts/verify_package.py').read_text();marker="    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:"
 insertion=(D/'verifier_insertion.txt').read_text();need(code.count(marker)==1,'Verifier marker');code=code.replace(marker,insertion+'\n'+marker);(P/'scripts/verify_package.py').write_text(code)
 m=read(P/'PACKAGE_MANIFEST.json');names={r['path'] for r in m['members']};names.update(newnames);names.update(['HISTORY_ORDER_QUALIFICATION.json','HISTORY_ORDER_REPAIR_STATUS.json','HISTORY_ORDER_REPAIR_NOTES.md','HISTORY_ORDER_COPY_EXCLUSIONS.json'])
 m['policy']+='; explicit current whole04 global-order qualification and whole05/root hold, exact six pre-history-order interfaces, all140 prior copy rows preserved.';m['members']=[pin(P/n,n) for n in sorted(names)];write(P/'PACKAGE_MANIFEST.json',m)
 temp=P/(ZIP+'.history-order-tmp');need(not temp.exists(),'Temp exists')
 with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
  for name in sorted(names|{'PACKAGE_MANIFEST.json'}):
   i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(P/name).read_bytes())
 os.replace(temp,P/ZIP);archive=pin(P/ZIP,ZIP);(P/(ZIP+'.sha256')).write_text(archive['sha256']+'  '+ZIP+'\n')
 binding=read(P/'UPLOAD_BINDINGS.json');binding['archive']['bytes']=archive['bytes'];binding['archive']['sha256']=archive['sha256'];binding['manifest_sha256']=pin(P/'PACKAGE_MANIFEST.json','')['sha256'];write(P/'UPLOAD_BINDINGS.json',binding)
 write(D/'BUILD_SUMMARY.json',{'utc':now(),'archive':archive,'members':len(names)+1,'copy_rows':len(copies),'prior140_copy_prefix_exact':True,'new_custody_copies':newnames,'original_archive_retained':str((D/'before/NEWpreprint_v1_0'/ZIP).relative_to(A))})
 log('Explicit global-order correction/status appended, current README/SUPPLEMENT/verifier aligned with four reviews and required whole05. Six before-interface and seven authored review/root evidence copies appended, prior140 rows unchanged. Archive/bindings refreshed; no validation outcomes claimed yet.',50)
 print(json.dumps(read(D/'BUILD_SUMMARY.json'),indent=2))
if __name__=='__main__':{'freeze':freeze,'mutate':mutate}[sys.argv[1]]()
