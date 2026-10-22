#!/usr/bin/env python3
"""Bounded PR1064 terminal reconciliation; local files only, no Git/services."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PACKAGE=AUDIT/'preprint_v1_0'
STATUS='TERMINAL_STATUS_20261016.json'
STAGE='TERMINAL_ADMIN_COMPLETE_PENDING_ROOT_EXTERNAL_FINAL_INTEGRITY'
MUTABLE={'README.md','verify_package.py','COPY_MAP.json','SAFE_INPUT_PINS.json','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','support.zip','publication/DEPOSIT_BINDING.json'}

def need(c,m):
 if not c:raise RuntimeError(m)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def rec(p,root):
 b=p.read_bytes();return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':sha(b)}
def match(p,r):
 return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256']
def pkgfiles():return sorted(p for p in PACKAGE.rglob('*') if p.is_file() and not p.is_relative_to(PACKAGE/'tmp'))

def selected_sources():
 # The output seal's entire bounded list receives an explicit selection decision.
 selected={'FULLREPORT.md','VERDICT.json','INDEPENDENT_DERIVATION.md','DERIVATION_FREEZE.json','SOURCE_LEDGER.json','independent_rigorous_controls.py','INDEPENDENT_NORMAL.json','INDEPENDENT_OPTIMIZED.json','INDEPENDENT_FAULT_RECEIPTS.json','HISTORICAL_CUSTODY_RECHECK.json'}
 R=AUDIT/'reviews/package_04'
 records=load(R/'OUTPUT_PINS.json')['entries']+[rec(R/'OUTPUT_PINS.json',R),rec(R/'SEAL.json',R)]
 decisions=[]
 for r in records:
  source='reviews/package_04/'+r['path'];included=r['path'] in selected
  decisions.append(dict(source_path=source,package_path='support/history/'+source,bytes=r['bytes'],sha256=r['sha256'],included=included,reason=('Exact authored report, verdict, frozen derivation, metadata/locator analysis, rigorous finite control or explicitly qualified historical recheck; dated whole04 scope only.' if included else 'Retained locally under whole04 output seal. Custody/input/raw execution/derivative/archive/PDF receipts, stage-specific harnesses and seals are unnecessary duplicate delivery evidence; no source body or raw tree is added.')))
 source='ROOT_WHOLE_PACKAGE_REVIEW_04.json';r=rec(AUDIT/source,AUDIT)
 decisions.append(dict(source_path=source,package_path='support/history/'+source,bytes=r['bytes'],sha256=r['sha256'],included=True,reason='Exact ROOT adoption of complete whole04; terminal administration and NEW external final integrity remain required.'))
 return decisions

def prepare():
 need(not (PACKAGE/STATUS).exists(),'dated status already exists')
 baseline=load(HERE/'INPUT_PINS.json')['records']
 for r in baseline:need(match(AUDIT/r['path'],r),'pre-edit input changed '+r['path'])
 root=load(AUDIT/'ROOT_WHOLE_PACKAGE_REVIEW_04.json')
 need(root['whole_reviews_completed']==4 and root['minimum_whole_reviews']==2 and root['actionable_P0_P1_P2_P3']==0,'ROOT complete whole04 adoption missing')
 need(root['terminal_administration_and_NEW_external_final_integrity_required'] is True,'ROOT final-integrity gate missing')
 verdict=load(AUDIT/'reviews/package_04/VERDICT.json')
 need(verdict['verdict']=='ZERO_ACTIONABLE_FINDINGS' and verdict['this_complete_whole_review_ordinal']==4,'latest complete review invalid')
 decisions=selected_sources();copies=load(PACKAGE/'COPY_MAP.json')['copies'];need(len(copies)==165,'expected exact prior165 copies')
 oldcopies=list(copies)
 for r in decisions:
  src=AUDIT/r['source_path'];need(match(src,r),'selected source changed '+r['source_path'])
  if not r['included']:continue
  dest=PACKAGE/r['package_path'];need(not dest.exists(),'copy collision '+r['package_path']);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
  copies.append({k:r[k] for k in ['source_path','package_path','bytes','sha256']})
 need(copies[:165]==oldcopies,'copy prefix changed')
 ledger={'scope':'Every24 whole04 sealed outputs plus its OUTPUT_PINS/SEAL and ROOT adoption individually selected or omitted. Only11 exact authored files are added; all165 prior copy rows retain their order and full values. All earlier selection ledgers preserve their original boundaries. Historical programs and records retain dated stage scopes; no all-historical-pointer authenticity or omitted-program replay claim.','records':decisions,'local_only_exclusions':['All complete input freezes, source bodies and renders, original source/runtime/cache trees, raw execution output, old ZIP/before snapshots and terminal scratch stay local.','New finalization/terminal_admin_20261016 code, custody, diffs, receipts, report and seals remain local; ROOT external final integrity is a separate required act.']}
 write(PACKAGE/'TERMINAL_SELECTION_LEDGER_20261016.json',ledger)
 obj=load(PACKAGE/'COPY_MAP.json');obj['copies']=copies;write(PACKAGE/'COPY_MAP.json',obj)
 obj=load(PACKAGE/'SAFE_INPUT_PINS.json');obj['records']=copies;write(PACKAGE/'SAFE_INPUT_PINS.json',obj)
 status={'schema_version':1,'stage':STAGE,'snapshot_date':'2026-10-16','pr':1064,'problem_id':30001073,'evidence_paths_relative_to':'preprint_v1_0 support-kit root','whole_package_reviews_completed':4,'whole_package_reviews_required':2,'latest_complete_review':'support/history/reviews/package_04/VERDICT.json','root_complete_review_adoption':'support/history/ROOT_WHOLE_PACKAGE_REVIEW_04.json','actionable_P0_P1_P2_P3':0,'latest_complete_review_root_adopted':True,'new_complete_whole_review_currently_required':False,'root_terminal_administration_adoption_required':True,'root_external_final_integrity_required':True,'ready_for_submission':False,'publication_ready':False,'published':False,'issues_updated':False,'issues_resolved':False,'ascending_publication_hold_after_pr':1032,'novelty':'UNKNOWN','historical_priority':'UNKNOWN','individual_unsupported_historical_reference_occurrences':5,'universal_historical_pointer_authentication_claim':False,'scope':'Administrative reconciliation of the ROOT-adopted fourth complete whole-package review. Previous statuses/seals remain immutable dated history. No additional complete whole review is currently required; a new actionable finding requires bounded repair and a NEW complete whole05. ROOT must independently read/reproduce/adopt this terminal administration and create NEW external final integrity before any readiness promotion. No service, publication, issue disposition or outreach occurred.'}
 write(PACKAGE/STATUS,status);write(AUDIT/STATUS,status)
 (PACKAGE/'TERMINAL_ACCEPTANCE_20261016.md').write_text('''# Terminal status, 16 October 2026

Four complete whole-package reviews have finished, with a minimum of two required. Latest whole04 is ZERO actionable P0–P3 and ROOT has adopted it. `TERMINAL_STATUS_20261016.json` is the current workflow snapshot. No further complete whole review is currently required. This bounded administrative reconciliation is not a fifth whole review or a new mathematical result. ROOT must read and independently reproduce/adopt the terminal records and create NEW external final integrity. Readiness is not yet promoted: ready_for_submission, publication_ready, published, issues_updated and issues_resolved are false; the ascending service hold remains after PR1032.

All old statuses, reports, FINAL_SEAL/FINAL_INTEGRITY records and stage output pins retain their exact bytes and dated meanings. The former case-alias repair snapshot required whole04 at its date; that review and ROOT adoption have now occurred. This dated record supersedes that workflow requirement without rewriting it. An actionable new finding would require bounded repair and NEW complete whole05.

The paper, proof, canonical PDF, bibliographic metadata, native uploader manifest and path-guard implementations are unchanged. Full whole04 records the actual compilation and views of all five pages. This administrative step performs no compilation or rerender. Its actual standard-library replays, semantic mutations, guard controls and full-JSON comparisons are recorded separately in the local finalization folder. Finite diagnostics do not replace the analytic proof.

The selection ledger adds only eleven exact authored whole04/ROOT records and preserves every prior copy row and history boundary. Historical pointer qualifications persist: two copies of package02 CHANGE_INVENTORY.added_package_files[0] name an unsupported 29,119-byte SHA256 3cceebbd4a4db6264b13adc04460809fc90d4f72918c10f29829e5817f5f5743 artifact. The actual immutable CURRENT_OUTPUT_PINS_WHOLE03.json has the same byte count and SHA256 7a4378d695e7206eb5681a8d3fcecf171ffdc2e025ba2d9cfd081aa9d91cadbb and is validly bound by later seals. Three deliberately invalid old binding fixtures are the other unsupported occurrences. No old pointer is rewritten, no missing bytes are manufactured, and no claim that all historical rows resolve is made. The exact whole04 historical recheck carries all five occurrences and their locators.

Historical novelty and priority remain UNKNOWN. The result remains a credited corollary, extensively AI-assisted, unrefereed and without external human peer review or formal proof-assistant certification. No upload, DOI, release, PR/issue/tracker action, publication or external communication occurred. Only the human user may communicate externally.
''')
 p=PACKAGE/'README.md';text=p.read_text();start=text.index('The current `REPAIR_STATUS_CASE_ALIAS01.json`');end=text.index('\n\nRun the following',start)
 text=text[:start]+'''The current dated `TERMINAL_STATUS_20261016.json` records four completed complete whole-package reviews, with a minimum of two required. Latest whole04 is ZERO actionable P0–P3 and ROOT-adopted. No further complete whole review is currently required. ROOT terminal-administration adoption and NEW external final integrity remain required; ready_for_submission, publication_ready, published, issues_updated and issues_resolved are false, and the ascending service hold remains after PR1032. `TERMINAL_ACCEPTANCE_20261016.md` records these gates. Every older status, including the case-alias repair's then-pending whole04 gate and the earlier terminal status, remains verbatim dated history. A new actionable finding requires bounded repair and NEW complete whole05. These workflow gates are not premises of the proof.'''+text[end:]
 text=text.replace('`TERMINAL_OUTPUT_PINS.json` seals this terminal stage separately.','`TERMINAL_OUTPUT_PINS.json` seals the dated 14 October terminal stage. `TERMINAL_OUTPUT_PINS_20261016.json` separately seals this administrative package stage, while ROOT external final integrity remains required.')
 text+='''
`TERMINAL_SELECTION_LEDGER_20261016.json` individually selects or omits the whole04 sealed outputs and ROOT adoption. Only eleven exact authored records are added; all prior history/copy boundaries persist. Whole04 retains five explicitly unsupported historical pointer occurrences: two stale package02 CHANGE_INVENTORY rows naming the absent 29,119-byte SHA256 3cceebbd4a4db6264b13adc04460809fc90d4f72918c10f29829e5817f5f5743 artifact, and three intentionally invalid old binding fixtures. The actual immutable CURRENT_OUTPUT_PINS_WHOLE03.json is 29,119 bytes with SHA256 7a4378d695e7206eb5681a8d3fcecf171ffdc2e025ba2d9cfd081aa9d91cadbb and later valid seals bind those bytes. The copied exact whole04 HISTORICAL_CUSTODY_RECHECK lists each occurrence. No all-historical-pointer resolution or original-stage replay is claimed.
''';p.write_text(text)
 p=PACKAGE/'verify_package.py';text=p.read_text();needle=" require(load('support/CHECKS.json')['pass'] is True,'authored diagnostic record not passed')"
 need(text.count(needle)==1,'verifier insertion location changed')
 guard=""" # Earlier status checks above preserve their dated historical states.
 dated=load('TERMINAL_STATUS_20261016.json')
 require(dated['stage']=='TERMINAL_ADMIN_COMPLETE_PENDING_ROOT_EXTERNAL_FINAL_INTEGRITY' and dated['snapshot_date']=='2026-10-16','dated terminal stage altered')
 require(dated['whole_package_reviews_completed']==4 and dated['whole_package_reviews_required']==2,'dated terminal complete-review count altered')
 require(dated['latest_complete_review']=='support/history/reviews/package_04/VERDICT.json' and dated['root_complete_review_adoption']=='support/history/ROOT_WHOLE_PACKAGE_REVIEW_04.json','dated terminal review pointers altered')
 require(dated['actionable_P0_P1_P2_P3']==0 and dated['latest_complete_review_root_adopted'] is True and dated['new_complete_whole_review_currently_required'] is False,'dated terminal whole-review adoption altered')
 require(dated['root_terminal_administration_adoption_required'] is True and dated['root_external_final_integrity_required'] is True,'dated terminal ROOT integrity gate altered')
 require(all(dated[k] is False for k in ['ready_for_submission','publication_ready','published','issues_updated','issues_resolved']),'dated terminal readiness/publication gate altered')
 require(dated['ascending_publication_hold_after_pr']==1032 and dated['novelty']=='UNKNOWN' and dated['historical_priority']=='UNKNOWN','dated terminal hold or novelty boundary altered')
 require(dated['individual_unsupported_historical_reference_occurrences']==5 and dated['universal_historical_pointer_authentication_claim'] is False,'dated historical qualification altered')
 latest_review=load(dated['latest_complete_review'])
 require(latest_review['verdict']=='ZERO_ACTIONABLE_FINDINGS' and latest_review['this_complete_whole_review_ordinal']==4 and latest_review['minimum_whole_reviews']==2 and all(latest_review['severity_counts'][s]==0 for s in ['P0','P1','P2','P3']),'dated latest complete-review verdict altered')
 latest_adoption=load(dated['root_complete_review_adoption'])
 require(latest_adoption['status']=='ADOPT_COMPLETE_WHOLE04_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN' and latest_adoption['whole_reviews_completed']==4 and latest_adoption['minimum_whole_reviews']==2 and latest_adoption['actionable_P0_P1_P2_P3']==0,'dated ROOT whole04 adoption altered')
 require(latest_adoption['terminal_administration_and_NEW_external_final_integrity_required'] is True and latest_adoption['publication_ready'] is False and latest_adoption['published'] is False and latest_adoption['services_held_after_pr']==1032,'dated ROOT whole04 terminal gate altered')
"""
 p.write_text(text.replace(needle,guard+needle))
 exclusions=load(PACKAGE/'EXCLUSION_LEDGER.json');need(len(exclusions['local_package_files'])==12,'old local exclusion count changed')
 exclusions['local_package_files'].append('TERMINAL_OUTPUT_PINS_20261016.json')
 exclusions['source_exclusion_groups'].append({'group':'reviews/package_04 omitted outputs and finalization/terminal_admin_20261016 input/before/scratch/process/custody/report/seal files','reason':'Every whole04 output selected or omitted individually in dated selection ledger; only eleven exact authored records enter delivery. Source bodies, old archive and private before copies remain local. No historical all-pointer certificate or original-stage replay is claimed.'})
 write(PACKAGE/'EXCLUSION_LEDGER.json',exclusions)
 allow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members']
 allow+=['TERMINAL_STATUS_20261016.json','TERMINAL_ACCEPTANCE_20261016.md','TERMINAL_SELECTION_LEDGER_20261016.json']+[r['package_path'] for r in decisions if r['included']]
 need(len(allow)==len(set(allow)),'allowlist collision');allow=sorted(allow);write(PACKAGE/'SUPPORT_ALLOWLIST.json',{'members':allow})
 manifest=load(PACKAGE/'SUPPORT_MANIFEST.json');manifest['entries']=[rec(PACKAGE/name,PACKAGE) for name in allow if name!='SUPPORT_MANIFEST.json'];write(PACKAGE/'SUPPORT_MANIFEST.json',manifest)
 cmd=[sys.executable,'-I','-B',str(PACKAGE/'build_archive.py'),'--output',str(PACKAGE/'support.zip')]
 p=subprocess.run(cmd,capture_output=True,text=True);write(HERE/'BUILD_RECEIPT.json',{'utc':utc(),'argv':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});need(p.returncode==0,'build failed '+p.stderr)
 binding=load(PACKAGE/'publication/DEPOSIT_BINDING.json')
 for key,name in [('paper_pdf','paper.pdf'),('support_archive','support.zip')]:binding[key]=rec(PACKAGE/name,PACKAGE)
 write(PACKAGE/'publication/DEPOSIT_BINDING.json',binding)
 with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — 40% of bounded terminal administration: separate dated outer/kit status, exact eleven-file whole04 evidence addition, append-only copies, current semantic guards and README reconciled. Archive and binding regenerated. All former statuses/seals, paper, metadata, native manifest and path guards remain protected. Validation and ROOT external final integrity remain.\n')
 print(json.dumps({'prepared':True,'members':len(allow),'copies':len(copies),'selected_authored_files':11,'stage':STAGE}))

if __name__=='__main__':prepare()
