#!/usr/bin/env python3
"""Bounded current administrative successor; historical records remain immutable."""
from pathlib import Path
import collections,datetime,difflib,hashlib,json,os
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit';H='terminal_after_whole04_history'
def obj(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def put(p,b):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def pin(p,root,key='path'):return {key:p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
if (W/'AUTHORING_COMPLETE.json').exists():raise RuntimeError('Already authored')
before=obj(W/'BEFORE_COPIES.json')['files'];by={r['original_path']:r for r in before}
for r in before:
 if (A/r['original_path']).read_bytes()!=(A/r['source_snapshot']).read_bytes():raise RuntimeError('Before bytes changed')
review=obj(A/'newreviews/package_04/VERDICT.json');adopt=obj(A/'ROOT_WHOLE_PACKAGE_REVIEW_04.json')
if review['findings'] or adopt['finding_counts']!={'P0':0,'P1':0,'P2':0,'P3':0}:raise RuntimeError('Wrong adopted review')
selected_whole=['REPORT.md','VERDICT.json','INDEPENDENT_DERIVATION.md','SOURCE_READ_LEDGER.json','FULL_MATHEMATICAL_OUTPUT_COMPARISON.json','FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json','REPRODUCTION_SUMMARY.json','SEMANTIC_RESULTS.json','CUSTODY_RESULTS.json','VISUAL_QA.json','INPUT_RECHECK.json','DIAGNOSTIC_EVENTS.json','CAPTURED750_CHECK_RECEIPT.json','DERIVATION_FREEZE.json','OUTPUT_PINS.json','SEAL.json']
selected=['newreviews/package_04/'+n for n in selected_whole]+['ROOT_WHOLE_PACKAGE_REVIEW_04.json','ROOT_ARCHIVE_WORDING_REPAIR_REVIEW_01.json']
newcopies=[];selectedpins=[]
for r in before:
 if r['original_path'].endswith('.zip'):continue
 dest=H+'/before/'+r['original_path'];put(K/dest,(A/r['source_snapshot']).read_bytes());newcopies.append({**r,'destination':dest,'stage':'terminal-after-whole04 exact immediately-before stage'})
for n in selected:
 dest=H+'/evidence/'+n;put(K/dest,(A/n).read_bytes());p=pin(A/n,A);selectedpins.append(p);newcopies.append({'original_path':n,'source_snapshot':n,'destination':dest,'bytes':p['bytes'],'sha256':p['sha256'],'stage':'terminal-after-whole04 selected authored evidence'})
dump(W/'SELECTED_INPUTS.json',{'scope':'18 exact authored review/source-interface summaries and ROOT adoptions; no source body, raw program, raw stream, image, runtime or archive newly selected.','files':selectedpins})
oldout=obj(A/'newreviews/package_04/OUTPUT_PINS.json')['files'];decisions=[]
for r in oldout:
 n='newreviews/package_04/'+r['path'];s=n in selected
 decisions.append({**r,'original_path':n,'disposition':'exact_captured_stage_or_canonical_copy' if s else 'omitted',**({'destination':H+'/evidence/'+n} if s else {'reason':'Not selected for the bounded public terminal package; exact original remains locally sealed. Raw programs, streams, pixels, primary-body derivatives and private/environment material are not newly distributed; authored interface summaries are selected separately.'})})
dump(K/'TERMINAL_AFTER_WHOLE04_OUTPUT_DECISIONS.json',{'scope':'Every one of the 52 whole04 sealed output rows in exact inventory order; selection does not imply replay of omitted bodies or historical workspace tails. Inventory and separate seal are additionally selected exact evidence.','source_inventory':'newreviews/package_04/OUTPUT_PINS.json','files':decisions})
dump(W/'WHOLE04_OUTPUT_DECISIONS.json',obj(K/'TERMINAL_AFTER_WHOLE04_OUTPUT_DECISIONS.json'))
status={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'TERMINAL_ADMIN_AFTER_ADOPTED_WHOLE04_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','whole_reviews_completed':4,'minimum_whole_reviews':2,'latest_complete_review':'whole04','latest_review_actionable_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'latest_complete_review_zero_findings':True,'root_whole04_adopted':True,'root_archive_wording_repair01_adopted':True,'new_complete_review_required':False,'required_next_review':None,'root_integrity_adoption_required':True,'root_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'full_original_maximum_classification_bundle':'PARTIAL','exact_application_priority':'UNKNOWN','mathematical_research_completion_best_guess_percent':60,'whole04_verdict':H+'/evidence/newreviews/package_04/VERDICT.json','root_whole04_adoption':H+'/evidence/ROOT_WHOLE_PACKAGE_REVIEW_04.json','supersedes_dated_review_accounting_only':['TERMINAL_ADMIN_STAGE.json','CURRENT_CASE_ALIAS_REPAIR01.json','CURRENT_ARCHIVE_WORDING_REPAIR01.json'],'scope':'Fixed-g essential positive factorizations of one boundary twist with repetitions and pairwise geometric intersection<=1: finite simultaneous-conjugacy classes and attained finite maximum. Separate restricted arbitrary-length clause negative; higher-genus exact maximum/classification PARTIAL; priority/novelty/worldwide openness UNKNOWN. Four complete reviews/minimum two/latest whole04 ZERO and ROOT-adopted. No further complete review currently required. Final external ROOT integrity is required and unadopted. No new compile/render/view; whole04 actually compiled and viewed all seven unchanged pages.'}
for base in [D,K]:dump(base/'CURRENT_TERMINAL_AFTER_WHOLE04.json',status)
for base in [D,K]:
 p=base/'README.md';s=p.read_text();start=s.index('Three complete whole-candidate reviews are finished;');end=s.index('Prior statuses and seals retain their exact dated meaning.',start)+len('Prior statuses and seals retain their exact dated meaning.')
 s=s[:start]+'Four complete whole-candidate reviews are finished; minimum two remains unchanged. ROOT adopted complete whole04 with zero actionable P0–P3 findings and adopted the bounded archive-wording repair. `CURRENT_TERMINAL_AFTER_WHOLE04.json` controls current accounting. No further complete whole review is currently required. Separate external final ROOT integrity adoption remains required and unadopted; publication readiness, issues-resolved and publication remain false, with services held at PR1032. Prior statuses, seals and metadata notes retain their exact dated meaning.'+s[end:]
 s=s.replace('The current archive-wording checkpoint requires NEW complete whole04;', 'At its dated pre-whole04 checkpoint, the archive-wording repair required NEW complete whole04; that review is now ROOT-adopted with zero findings;')
 s=s.replace('Those are historical checks; `CURRENT_ARCHIVE_WORDING_REPAIR01.json` supplies current three-review/one-P3 accounting and the required NEW complete whole04.', 'Those are historical checks. The verifier additionally validates `CURRENT_TERMINAL_AFTER_WHOLE04.json` for current four-review/latest-zero accounting and the unadopted final ROOT integrity requirement.')
 s=s.replace('The archive-wording checkpoint below controls current accounting: three completed reviews, latest one P3, and NEW complete whole04 required.', 'The archive-wording checkpoint below preserves its dated three-review/one-P3/required-whole04 accounting; the terminal successor records current four-review/latest-zero ROOT-adopted accounting.')
 s=s.replace('`CURRENT_ARCHIVE_WORDING_REPAIR01.json` records three completed whole reviews, minimum two, latest whole03 with one P3 wording issue addressed by this candidate pending ROOT adoption, and mandatory NEW complete whole04.', '`CURRENT_ARCHIVE_WORDING_REPAIR01.json` preserves its dated three completed reviews, minimum two, latest whole03 with one P3 and mandatory NEW complete whole04 checkpoint. ROOT subsequently adopted the wording repair and complete whole04 with zero actionable findings.')
 s=s.replace('All checkers and output guards remain byte-identical and continue validating their dated historical checkpoint.', 'At that archive-wording stage all checkers and output guards stayed byte-identical. This terminal successor adds current-status semantic and custody checks to the verifier; mathematical programs and output guards remain unchanged.')
 s+='''
## Current terminal administration after adopted whole04

`CURRENT_TERMINAL_AFTER_WHOLE04.json` is identical inside and outside the kit and explicitly bound. Four complete whole reviews are finished, minimum two, latest whole04 has zero P0–P3 findings and is ROOT-adopted. No further complete review is currently required. The separate external final ROOT integrity decision is required and unadopted. Publication_ready, issues_resolved and published remain false; services stay held at PR1032.

`terminal_after_whole04_history` contains eight exact nonarchive before snapshots and eighteen selected authored review/interface/adoption files. No raw reviewer program, source body/extract, rendered image, runtime, raw stream or new duplicate archive is selected. All 52 whole04 output rows receive individual selected/omitted decisions. The immediately previous ZIP remains an exact durable ignored local before snapshot only. The three existing historical archives listed above, all old dated records, 181 old copy rows, 4,666 history rows, and nine earlier relocations remain exact; the new relocation map preserves complete old rows that formerly named the live verifier. Before maps and structured pointer resolutions preserve original stale pins without rewriting them.

Actual canonical and clean checks, full mathematical JSON in both Python modes against adopted whole04, coherent semantic faults, complete output guards, closed deterministic ZIP rebuild and the native repository LOCAL check are recorded in `../finalization/terminal_admin_after_whole04_20261016` relative to the delivery folder. No new compilation/render/page view is claimed here; whole04 actually compiled and individually viewed all seven unchanged pages. The historical captured750 checker is stage-specific, not a future file-count API. Explicit earlier ENOSPC failures remain exact events; the older erasing-fault cause remains UNESTABLISHED and ROOT attempt02 cause remains UNCONFIRMED. The accepted theorem, credited sources, PARTIAL/UNKNOWN qualifications, AI/unrefereed/no-human-review disclosures and native metadata are unchanged.
'''
 p.write_text(s)
# Append-only stage copies/history; relocate only through a separate full-original-row map.
copies=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json');copies['files']+=newcopies;dump(K/'REPAIR01_STAGE_COPIES.json',copies);dump(W/'NEW_COPY_ROWS.json',{'files':newcopies})
history=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json');refs=history['references'];oldrel={r['reference_index']:r for name in ['TERMINAL_HISTORY_RELOCATIONS.json','CASE_ALIAS_HISTORY_RELOCATIONS.json'] for r in obj(K/name)['rows']};rel=[]
for i,r in enumerate(refs):
 if r['disposition']!='exact_captured_stage_or_canonical_copy' or i in oldrel:continue
 n='preprint_v1_0/verification_kit/'+r['destination']
 if n in by:
  b=by[n]
  if (r['bytes'],r['sha256'])!=(b['bytes'],b['sha256']):raise RuntimeError('Old history mismatched before')
  rel.append({'reference_index':i,'historical_reference':r,'current_exact_destination':H+'/before/'+n,'reason':'Separate exact-before relocation; complete old row preserved unchanged.'})
dump(K/'TERMINAL_AFTER_WHOLE04_HISTORY_RELOCATIONS.json',{'rows':rel})
added=[]
for r in before:
 b={'stage':'terminal-after-whole04-changed-before','inventory':'finalization/terminal_admin_after_whole04_20261016/BEFORE_COPIES.json','original_path':r['original_path'],'bytes':r['bytes'],'sha256':r['sha256']}
 b.update({'disposition':'omitted','reason':'Exact durable immediate old ZIP retained only at '+r['source_snapshot']+'; not newly packed.'} if r['original_path'].endswith('.zip') else {'disposition':'exact_captured_stage_or_canonical_copy','destination':H+'/before/'+r['original_path']});added.append(b)
for r in decisions:
 b={key:r[key] for key in ['original_path','bytes','sha256','disposition']};b.update({key:r[key] for key in ['reason','destination'] if key in r});b.update({'stage':'terminal-after-whole04-output52','inventory':'newreviews/package_04/OUTPUT_PINS.json'});added.append(b)
extra=[r for r in selectedpins if r['path'] not in {x['original_path'] for x in decisions}]
for r in extra:added.append({'stage':'terminal-after-whole04-extra-selected','inventory':'finalization/terminal_admin_after_whole04_20261016/SELECTED_EXTRA_INPUTS.json','original_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'disposition':'exact_captured_stage_or_canonical_copy','destination':H+'/evidence/'+r['path']})
dump(W/'SELECTED_EXTRA_INPUTS.json',{'files':extra});history['references']+=added;history['inventory_counts'].update({'terminal-after-whole04-changed-before':len(before),'terminal-after-whole04-output52':len(decisions),'terminal-after-whole04-extra-selected':len(extra)});dump(K/'REPAIR01_HISTORY_RESOLUTION.json',history);dump(W/'APPENDED_HISTORY_ROWS.json',{'references':added})
# All preexisting structured size/hash pointers to the nine changed bytes, including historical copy chains.
hashes=collections.defaultdict(list)
for r in before:hashes[(r['bytes'],r['sha256'])].append(r)
res=[]
def walk(v,pt,source):
 if isinstance(v,dict):
  for b in hashes.get((v.get('bytes'),v.get('sha256')),[]) if type(v.get('bytes')) is int and isinstance(v.get('sha256'),str) else []:
   res.append({'source_inventory':source,'source_snapshot':by[source]['source_snapshot'] if source in by else source,'json_pointer':pt,'original_pin':v,'changed_current_path':b['original_path'],'exact_local_before':b['source_snapshot'],'delivered_before':None if b['original_path'].endswith('.zip') else H+'/before/'+b['original_path'],'disposition':'old_archive_local_only_not_newly_packed' if b['original_path'].endswith('.zip') else 'exact_delivered_before_bytes'})
  for k,x in v.items():walk(x,pt+'/'+str(k).replace('~','~0').replace('/','~1'),source)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,pt+'/'+str(i),source)
for r in obj(W/'IMMEDIATE_INPUT_PINS.json')['files']:
 if r['path'].endswith('.json'):
  n=r['path'];p=A/(by[n]['source_snapshot'] if n in by else n)
  try:walk(obj(p),'',n)
  except (ValueError,UnicodeDecodeError):pass
dump(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json',{'references':res});dump(K/'TERMINAL_AFTER_WHOLE04_OLD_PIN_RESOLUTIONS.json',{'references':res})
dump(K/'TERMINAL_AFTER_WHOLE04_BEFORE_MAP.json',{'files':[{**r,'delivered_before':None if r['original_path'].endswith('.zip') else H+'/before/'+r['original_path'],'reason':'Old archive local only; other before bytes exact delivered.'} for r in before]})
sources=obj(A/'newreviews/package_04/SOURCE_READ_LEDGER.json')
dump(W/'SOURCE_LEDGER_STRUCTURE.json',{'keys':list(sources)})
# Current semantic verification, preserving earlier dated checkpoint checks.
p=K/'verify.py';s=p.read_text();anchor='    native = native_metadata()\n'
new='''    current = json.loads(regular_input(ROOT / "CURRENT_TERMINAL_AFTER_WHOLE04.json").read_text())
    require(current["status"] == "TERMINAL_ADMIN_AFTER_ADOPTED_WHOLE04_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY",
            "current terminal authority")
    require(type(current["whole_reviews_completed"]) is int and current["whole_reviews_completed"] == 4
            and type(current["minimum_whole_reviews"]) is int and current["minimum_whole_reviews"] == 2,
            "current terminal complete review count")
    require(current["latest_complete_review"] == "whole04" and current["latest_review_actionable_counts"] == {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
            and current["latest_complete_review_zero_findings"] is True, "current terminal latest findings")
    require(current["root_whole04_adopted"] is True and current["root_archive_wording_repair01_adopted"] is True
            and current["new_complete_review_required"] is False and current["required_next_review"] is None,
            "current terminal adopted complete review boundary")
    require(current["root_integrity_adoption_required"] is True and current["root_integrity_adopted"] is False
            and all(current[k] is False for k in ["publication_ready", "issues_resolved", "published"])
            and current["services_held_at"] == 1032, "current terminal publication/service boundary")
    require(current["full_original_maximum_classification_bundle"] == "PARTIAL"
            and current["exact_application_priority"] == "UNKNOWN", "current terminal scope boundary")
    latest = json.loads(regular_input(safe_path(current["whole04_verdict"])).read_text())
    require(latest["status"] == "COMPLETE_WHOLE04_ZERO_ACTIONABLE_FINDINGS" and latest["findings"] == []
            and latest["findings_by_priority"] == {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
            and latest["whole_reviews_completed"] == 4 and latest["minimum_whole_reviews"] == 2,
            "captured whole04 evidence differs")
    adoption = json.loads(regular_input(safe_path(current["root_whole04_adoption"])).read_text())
    require(adoption["status"] == "ROOT_ADOPT_COMPLETE_WHOLE04_ZERO_ACTIONABLE_PENDING_CURRENT_TERMINAL_ADMIN"
            and adoption["whole_reviews_completed"] == 4 and adoption["minimum_whole_reviews"] == 2
            and adoption["finding_counts"] == {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
            "captured root whole04 adoption differs")
'''
if s.count(anchor)!=1:raise RuntimeError('Verifier anchor')
s=s.replace(anchor,new+anchor)
anchor='    for index, r in enumerate(history["references"]):\n'
new='''    terminal_after = json.loads(regular_input(ROOT / "TERMINAL_AFTER_WHOLE04_HISTORY_RELOCATIONS.json").read_text())["rows"]
    for relocation in terminal_after:
        index = relocation["reference_index"]
        require(type(index) is int and 0 <= index < 4666 and index not in relocations
                and history["references"][index] == relocation["historical_reference"],
                "terminal after whole04 relocation changed original row")
        relocations[index] = relocation
'''
s=s.replace(anchor,new+anchor)
anchor='        # Present bindings are always strict. Explicit artifact paths work after extraction.\n'
new='''        require(regular_input(p.parent / "CURRENT_TERMINAL_AFTER_WHOLE04.json").read_bytes()
                == (ROOT / "CURRENT_TERMINAL_AFTER_WHOLE04.json").read_bytes(), "external current terminal status differs")
        record = data["current_terminal_after_whole04"]
        require(record["filename"] == "CURRENT_TERMINAL_AFTER_WHOLE04.json"
                and regular_input(p.parent / record["filename"]).stat().st_size == record["bytes"]
                and digest(p.parent / record["filename"]) == record["sha256"], "external current terminal status binding")
'''
s=s.replace(anchor,new+anchor);p.write_text(s)
dump(W/'NEW_COPY_ROWS.json',{'files':newcopies})
dump(W/'AUTHORING_COMPLETE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_evidence':len(selected),'whole04_output_rows':len(decisions),'selected_output_rows':sum(x['disposition']!='omitted' for x in decisions),'new_copies':len(newcopies),'new_history':len(added),'new_relocations':len(rel),'new_old_pointer_resolutions':len(res),'old_copy_prefix':181,'old_history_prefix':4666,'new_complete_review_currently_required':False,'publication_ready':False})
print(json.dumps(obj(W/'AUTHORING_COMPLETE.json'),indent=2))
