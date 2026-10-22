#!/usr/bin/env python3
"""Bounded documentation successor; no mathematical or executable payload edit."""
import datetime, hashlib, json, os
from pathlib import Path
W=Path(__file__).resolve().parent; A=W.parents[1]; D=A/'preprint_v1_0'; K=D/'verification_kit'
def obj(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True); q=p.with_name(p.name+'.archive_wording01-new'); q.write_bytes(b); os.replace(q,p)
def dump(p,d): put(p,(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def replace(s,a,b):
    if s.count(a)!=1: raise RuntimeError('Unique prose anchor missing: '+a)
    return s.replace(a,b)
if (W/'AUTHORING_COMPLETE.json').exists(): raise RuntimeError('One-shot authoring already completed')
before=obj(W/'BEFORE_COPIES.json')['files']
for r in before:
    p=A/r['original_path']; q=A/r['source_snapshot']
    if p.read_bytes()!=q.read_bytes() or sha(q)!=r['sha256']: raise RuntimeError('Before snapshot mismatch')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
status={'utc':now,'status':'BOUNDED_ARCHIVE_WORDING_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE04',
 'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_review':'whole03',
 'latest_review_actionable_counts':{'P0':0,'P1':0,'P2':0,'P3':1},'latest_complete_review_zero_findings':False,
 'root_whole03_adopted':True,'latest_P3_bounded_wording_addressed_pending_ROOT_adoption':True,
 'new_complete_review_required':True,'required_next_review':'NEW complete whole04',
 'root_repair_adoption_required':True,'root_repair_adopted':False,
 'root_integrity_adoption_required':True,'root_integrity_adopted':False,
 'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,
 'full_original_maximum_classification_bundle':'PARTIAL','exact_application_priority':'UNKNOWN',
 'mathematical_research_completion_best_guess_percent':60,
 'supersedes_current_case_alias_review_accounting':True,
 'historical_boundary':'CURRENT_CASE_ALIAS_REPAIR01.json remains exact dated two-review/pending-whole03 evidence; the unchanged verifier validates that historical checkpoint. This record controls current review accounting; it does not certify ROOT repair adoption or final readiness.',
 'scope':'Current archive-exclusion prose qualified for three already retained individually pinned historical ZIP members, including two byte-identical archives. Paper/PDF/TeX, all executable checkers/pathguards, native metadata, source credits and dated evidence unchanged. No new compile/render/view.'}
for base in [D,K]: dump(base/'CURRENT_ARCHIVE_WORDING_REPAIR01.json',status)
for base in [D,K]:
    p=base/'README.md'; s=p.read_text()
    if base==D:
        start='Two complete whole-candidate reviews are now finished.'
        end='Earlier statuses retain their exact historical meaning.'
    else:
        start='Two complete whole-candidate reviews are finished.'
        end='Earlier statuses remain exact historical records.'
    first=s.index(start); last=s.index(end,first)+len(end)
    s=s[:first]+('Three complete whole-candidate reviews are finished; minimum two remains unchanged. Whole01 had repaired bounded package issues; whole02 had zero actionable findings. ROOT adopted complete whole03 with one P3 inconsistency in archive-exclusion wording. `CURRENT_ARCHIVE_WORDING_REPAIR01.json` records this bounded wording correction pending ROOT repair adoption and a **NEW complete whole04**. Latest whole03 is not a zero-findings review. Final ROOT integrity adoption remains required; publication readiness, issues-resolved and publication remain false, with services held at PR1032. Prior statuses and seals retain their exact dated meaning.')+s[last:]
    if base==D:
        s=replace(s,'Source body/images, raw service/Git captures, environments and duplicate archives are not distributed.',
          'The currently authored payload adds no third-party source body/image, raw service/Git capture, environment/runtime material or newly selected duplicate archive. The delivered kit retains three individually pinned historical ZIP members, including two byte-identical archives, and legitimate captured earlier code as dated history; these retained historical exceptions are described below.')
        s=replace(s,'Current standard-library, archive, binding and local uploader commands were rerun for this repair; receipts are in `../repairs/package01/REPRODUCTION_RECEIPTS.jsonl`.',
          'At repair01, standard-library, archive, binding and local uploader commands were rerun; those dated receipts remain in `../repairs/package01/REPRODUCTION_RECEIPTS.jsonl`. Current archive-wording repair receipts and complete custody accounting are in `../repairs/archive_wording01`.')
        s=s.replace('## Current repair and local submission check','## Original package repair and local submission check').replace('Current repair custody and ordinary/optimized receipts are in `../repairs/package01`.','That original repair custody and its ordinary/optimized receipts remain in `../repairs/package01`.')
    else:
        s=replace(s,'No third-party full PDF, extracted body, source image, raw service/Git filename capture, environment or duplicate archive is included.',
          'The currently authored payload adds no third-party full PDF, extracted body, source image, raw service/Git filename capture, environment/runtime material or newly selected duplicate archive. The delivered kit retains three individually pinned historical ZIP members, including two byte-identical archives, and legitimate captured earlier code as dated history; these retained historical exceptions are described below.')
    s=replace(s,'The later `CURRENT_CASE_ALIAS_REPAIR01.json` requires NEW complete whole03 after the physical case-alias repair; `TERMINAL_ADMIN_STAGE.json` remains unchanged historical evidence.',
      'The later dated `CURRENT_CASE_ALIAS_REPAIR01.json` required NEW complete whole03 after the physical case-alias repair; that review is now ROOT-adopted with one P3 wording finding. The current archive-wording checkpoint requires NEW complete whole04; `TERMINAL_ADMIN_STAGE.json` and the case-alias checkpoint remain unchanged historical evidence.')
    s=s.replace('Current `verify.py` additionally checks two completed reviews, latest zero findings, the ROOT review adoption, the separate final-integrity requirement and PR1032 service hold.',
      'The unchanged `verify.py` validates the dated terminal checkpoint with two completed reviews, its then-latest zero findings, its ROOT adoption, the separate final-integrity requirement and PR1032 service hold. Those are historical checks; `CURRENT_ARCHIVE_WORDING_REPAIR01.json` supplies current three-review/one-P3 accounting and the required NEW complete whole04.')
    s=replace(s,"`CURRENT_CASE_ALIAS_REPAIR01.json` supersedes the dated terminal record's earlier no-new-review requirement. The terminal P3 case-alias finding is repaired in this candidate, pending ROOT adoption and a **NEW complete whole03**. The two prior complete reviews remain completed; minimum two remains unchanged. Readiness, issues-resolved and publication remain false; services remain held at PR1032. This bounded repair is not whole03 or final readiness clearance.",
      '`CURRENT_CASE_ALIAS_REPAIR01.json` records the dated physical case-alias repair checkpoint that superseded the terminal record’s earlier no-new-review requirement. ROOT subsequently adopted that bounded repair and complete whole03. Its exact two-review/pending-whole03 fields remain historical evidence. The archive-wording checkpoint below controls current accounting: three completed reviews, latest one P3, and NEW complete whole04 required. Readiness, issues-resolved and publication remain false; services remain held at PR1032.')
    s+='''
## Archive wording successor and retained historical exceptions

The three retained archive members are `metadata_date02_history/before/preprint_v1_0/verification_kit.zip` (2,056,267 bytes, SHA256 `9d585b3626bc349611626c5449819e4e1fd6f0f80cb06c467bae96f0532916a0`), and `metadata_date02_history/prior_repair01/before/preprint_v1_0/verification_kit.zip` plus `repair01_history/before/preprint_v1_0/verification_kit.zip` (each 607,553 bytes, SHA256 `d1c03ef097938934641907c3552f05a0687347ea7945b399fff1a365322a1a1b`). Paths here are relative to the kit. The last two are byte-identical. They remain legitimate immutable custody history, together with captured earlier code. This successor adds no newly selected duplicate ZIP; its immediate old ZIP is retained locally in the repair workspace only. Historical exclusion prose and dated records are preserved as evidence of their earlier stages.

`CURRENT_ARCHIVE_WORDING_REPAIR01.json` records three completed whole reviews, minimum two, latest whole03 with one P3 wording issue addressed by this candidate pending ROOT adoption, and mandatory NEW complete whole04. Selected exact authored whole03/source-interface evidence and ROOT adoption are under `archive_wording01_history/evidence`. The original 157 stage-copy rows and 4,641 history rows remain exact prefixes; the two terminal and seven case relocations remain unchanged. New before maps and individual old-pin resolutions preserve old pointers rather than rewriting them. All checkers and output guards remain byte-identical and continue validating their dated historical checkpoint. Current candidate custody and actual reproduction receipts are in `../repairs/archive_wording01` relative to the delivery folder. The older unexplained erasing-fault cause remains UNESTABLISHED; whole03’s explicit ENOSPC events remain separate recorded events. No new compilation, rendering or page viewing is claimed, and publication_ready/issues_resolved/published remain false with services held at PR1032.
'''
    put(p,s.encode())
selected=['ROOT_WHOLE_PACKAGE_REVIEW_03.json']+['reviews/package_03/'+n for n in [
 'FULLREPORT.md','VERDICT.json','FROZEN_INDEPENDENT_DERIVATION.md','SOURCE_READ_LEDGER.json',
 'HISTORICAL_ZIP_DISTRIBUTION_EVIDENCE.json','FULL_MATHEMATICAL_OUTPUT_COMPARISON.json',
 'FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json','ACTUAL_VERIFICATION_SUMMARY.json',
 'INDEPENDENT_CUSTODY_RESULTS.json','INDEPENDENT_SEMANTIC_RESULTS.json','MANUAL_ZIP_RECONSTRUCTION.json',
 'independent_checks03.py','fullmath_capture03.py','fullmath_capture03_O.py','semantic_checks03.py','manual_zip03.py']]
new=[]; selectedpins=[]
for r in before:
    if r['original_path'].endswith('.zip'): continue
    dest='archive_wording01_history/before/'+r['original_path'];put(K/dest,(A/r['source_snapshot']).read_bytes())
    new.append({**r,'destination':dest,'stage':'archive-wording01 exact immediately-before stage'})
for name in selected:
    p=A/name; dest='archive_wording01_history/evidence/'+name;put(K/dest,p.read_bytes())
    r={'path':name,'bytes':p.stat().st_size,'sha256':sha(p)};selectedpins.append(r)
    new.append({'original_path':name,'source_snapshot':name,'destination':dest,'bytes':r['bytes'],'sha256':r['sha256'],'stage':'archive-wording01 selected exact authored whole03/root/interface evidence'})
dump(W/'SELECTED_WHOLE03_INPUTS.json',{'scope':'Exact authored summaries, source interface ledger and programs only; no raw streams, source bodies, pixels, runtime/cache or newly selected archive.','files':selectedpins})
copies=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json');copies['files']+=new;dump(K/'REPAIR01_STAGE_COPIES.json',copies);dump(W/'NEW_COPY_ROWS.json',{'files':new})
history=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json');added=[]
for r in before:
    item={'stage':'archive-wording01-changed-before','inventory':'repairs/archive_wording01/BEFORE_COPIES.json','original_path':r['original_path'],'bytes':r['bytes'],'sha256':r['sha256']}
    item.update({'disposition':'omitted','reason':'Exact immediately-before ZIP retained only at '+r['source_snapshot']+'; deliberately not newly packed as another duplicate archive.'} if r['original_path'].endswith('.zip') else {'disposition':'exact_captured_stage_or_canonical_copy','destination':'archive_wording01_history/before/'+r['original_path']})
    added.append(item)
for r in selectedpins:
    added.append({'stage':'archive-wording01-selected-evidence','inventory':'repairs/archive_wording01/SELECTED_WHOLE03_INPUTS.json','original_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'disposition':'exact_captured_stage_or_canonical_copy','destination':'archive_wording01_history/evidence/'+r['path']})
history['references']+=added;history['inventory_counts'].update({'archive-wording01-changed-before':len(before),'archive-wording01-selected-evidence':len(selectedpins)})
dump(K/'REPAIR01_HISTORY_RESOLUTION.json',history);dump(W/'APPENDED_HISTORY_ROWS.json',{'references':added})
dump(W/'AUTHORING_COMPLETE.json',{'utc':now,'status':'BOUNDED_WORDING_AND_SEPARATE_ACCOUNTING_AUTHORED_PENDING_PACKAGING_AND_VERIFICATION','new_stage_copies':len(new),'new_history_rows':len(added),'no_executable_or_native_metadata_changes':True})
print(json.dumps({'status':'AUTHORED','copies':len(new),'references':len(added)}))
