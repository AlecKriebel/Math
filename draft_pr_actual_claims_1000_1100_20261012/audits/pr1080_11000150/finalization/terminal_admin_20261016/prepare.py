#!/usr/bin/env python3
"""One-shot bounded terminal administrative successor; no service or Git calls."""
import datetime, hashlib, json, shutil
from pathlib import Path

WORK = Path(__file__).resolve().parent
AUDIT = WORK.parents[1]
DELIVERY = AUDIT / 'preprint_v1_0'
KIT = DELIVERY / 'verification_kit'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p, root): return {'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)}
def dump(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
def obj(p): return json.loads(p.read_text())
def require(test, message):
    if not test: raise RuntimeError(message)

def main():
    require(not (WORK/'IMMEDIATE_INPUT_PINS.json').exists(), 'Do not restart a captured administrative stage')
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    baseline = [row(p, AUDIT) for p in sorted(AUDIT.rglob('*')) if p.is_file() and not p.is_symlink() and not p.is_relative_to(WORK)]
    dump(WORK/'IMMEDIATE_INPUT_PINS.json', {'utc':utc,'scope':'Every preexisting audit regular file, including private/source caches, hashed before any candidate mutation; no other effort touched.','files':baseline})
    edits = ['preprint_v1_0/README.md','preprint_v1_0/verification_kit/README.md','preprint_v1_0/verification_kit/verify.py','preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json','preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json','preprint_v1_0/verification_kit/ALLOWLIST.json','preprint_v1_0/verification_kit/MANIFEST.json','preprint_v1_0/verification_kit.zip','preprint_v1_0/EXTERNAL_BINDING.json']
    before = []
    for name in edits:
        p = AUDIT/name; q=WORK/'before'/name; q.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,q)
        before.append({'original_path':name,'source_snapshot':q.relative_to(AUDIT).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q)})
    dump(WORK/'BEFORE_COPIES.json', {'files':before,'scope':'Every authorized existing edit has its complete exact before bytes. The old ZIP stays outside delivery and is not newly packed.'})
    old_copies = obj(KIT/'REPAIR01_STAGE_COPIES.json'); require(len(old_copies['files'])==100,'Original stage-copy count')
    old_history = obj(KIT/'REPAIR01_HISTORY_RESOLUTION.json'); require(len(old_history['references'])==2312,'Original history count')
    whole = obj(AUDIT/'ROOT_WHOLE_PACKAGE_REVIEW_02.json')
    require(whole['whole_reviews_completed']==2 and whole['actionable_P0_P1_P2_P3']==0 and whole['status']=='ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','Root whole02 not adopted')
    stage = {'as_of_utc':utc,'stage':'terminal administrative reconciliation after two complete whole-candidate reviews',
        'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest_complete_review':'whole02','latest_review_actionable_P0_P1_P2_P3':0,
        'new_complete_review_required':False,'root_whole02_adopted':True,'root_integrity_adoption_required':True,
        'root_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,
        'current_state_authority':'A later external ROOT FINAL_INTEGRITY.json and FINAL_SEAL.json must adopt this terminal package before publication readiness can be affirmed. This delivered record describes only its dated pre-adoption checkpoint.',
        'historical_state_rule':'All earlier dated statuses, verdicts, inventories and seals remain unchanged historical stages, including CURRENT_STATUS_REPAIR01.json and METADATA_DATE02_ADMIN_STAGE.json.',
        'whole02_verdict':'terminal_admin_history/whole02/VERDICT.json','root_whole02_adoption':'terminal_admin_history/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json',
        'full_original_maximum_classification_bundle':'PARTIAL','exact_application_priority':'UNKNOWN',
        'math_research_completion_best_guess_percent':60,'administrative_subtask_completion_percent':100,
        'unchanged_paper_compile_and_page_scope':'No new compilation, render, page view or PDF marker in this administrative stage; all seven unchanged pages and actual compilation were checked by complete whole02.'}
    dump(DELIVERY/'TERMINAL_ADMIN_STAGE.json',stage); dump(KIT/'TERMINAL_ADMIN_STAGE.json',stage)
    append=[]
    def copy(source,destination,original=None):
        target=KIT/destination; require(not target.exists(),'New copy exists: '+destination)
        target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,target)
        append.append({'original_path':original or source.relative_to(AUDIT).as_posix(),'source_snapshot':source.relative_to(AUDIT).as_posix(),'destination':destination,'bytes':source.stat().st_size,'sha256':sha(source),'stage':'terminal-admin-20261016 exact captured stage'})
    for r in before:
        if not r['original_path'].endswith('.zip'):
            copy(AUDIT/r['source_snapshot'],'terminal_admin_history/before/'+r['original_path'],r['original_path'])
    # Only authored review documents, programs and structured receipts. Compiler stdout/raw web/images remain omitted.
    selection=[]
    for p in sorted((AUDIT/'reviews/package_02').iterdir()):
        if p.is_file() and p.name not in {'REPRODUCTION_RECEIPTS.jsonl'}:
            selection.append((p,'terminal_admin_history/whole02/'+p.name))
    for name in ['ROOT_WHOLE_PACKAGE_REVIEW_02.json','ROOT_REPAIR_REVIEW_01_DATE02.json']:
        selection.append((AUDIT/name,'terminal_admin_history/root/'+name))
    for name in ['REPORT.md','OUTPUT_PINS.json','TERMINAL_SEAL.json','IMMEDIATE_INPUT_PINS.json','CURRENT_INPUT_PINS.json','PROTECTED_INPUT_PINS.json']:
        selection.append((AUDIT/'repairs/package01_metadata_date02'/name,'terminal_admin_history/date02/'+name))
    selection.append((WORK/'IMMEDIATE_INPUT_PINS.json','terminal_admin_history/admin/IMMEDIATE_INPUT_PINS.json'))
    for p,d in selection: copy(p,d)
    dump(WORK/'NEW_COPY_ROWS.json',{'files':append})
    old_copies['files'].extend(append); dump(KIT/'REPAIR01_STAGE_COPIES.json',old_copies)
    # Index every exact delivered byte identity. Resolve ordered old references without altering their meaning.
    index={}
    for p in sorted(KIT.rglob('*')):
        if p.is_file(): index.setdefault((p.stat().st_size,sha(p)),p.relative_to(KIT).as_posix())
    inventories=[('terminal-admin-immediate',WORK/'IMMEDIATE_INPUT_PINS.json','files',''),
        ('whole02-input',AUDIT/'reviews/package_02/FROZEN_INPUTS.json','files',''),
        ('whole02-output',AUDIT/'reviews/package_02/OUTPUT_PINS.json','files','reviews/package_02/'),
        ('whole02-reviewed-assets',AUDIT/'reviews/package_02/VERDICT.json','reviewed_assets',''),
        ('metadata-date02-current',AUDIT/'repairs/package01_metadata_date02/CURRENT_INPUT_PINS.json','files',''),
        ('metadata-date02-protected',AUDIT/'repairs/package01_metadata_date02/PROTECTED_INPUT_PINS.json','files',''),
        ('metadata-date02-output',AUDIT/'repairs/package01_metadata_date02/OUTPUT_PINS.json','files','repairs/package01_metadata_date02/'),
        ('metadata-date02-immediate-repeat',AUDIT/'repairs/package01_metadata_date02/IMMEDIATE_INPUT_PINS.json','files','')]
    specification=[]
    for stage_name, inventory,key,prefix in inventories:
        source=obj(inventory)[key]; old_history['inventory_counts'][stage_name]=len(source)
        specification.append({'stage':stage_name,'inventory':inventory.relative_to(AUDIT).as_posix(),'key':key,'prefix':prefix,'count':len(source)})
        for r in source:
            ref={'stage':stage_name,'inventory':inventory.relative_to(AUDIT).as_posix(),'original_path':prefix+r['path'],'bytes':r['bytes'],'sha256':r['sha256']}
            dest=index.get((r['bytes'],r['sha256']))
            if dest: ref.update(disposition='exact_captured_stage_or_canonical_copy',destination=dest)
            else: ref.update(disposition='omitted',reason='This individual historical reference is not distributed as a new artifact: primary source bodies/extracts/images, raw service/compiler captures, environments, duplicate archives and unselected administrative scratch are excluded. It is not represented as replayed or as a delivered original path; its original size/hash and stage remain recorded.')
            old_history['references'].append(ref)
    dump(KIT/'REPAIR01_HISTORY_RESOLUTION.json',old_history)
    dump(WORK/'APPENDED_HISTORY_SPECIFICATION.json',{'inventories':specification,'old_reference_count':2312})
    p=KIT/'verify.py'; text=p.read_text()
    insertion='''    terminal = json.loads(regular_input(ROOT / "TERMINAL_ADMIN_STAGE.json").read_text())
    require(type(terminal["whole_reviews_completed"]) is int and terminal["whole_reviews_completed"] == 2 and type(terminal["minimum_whole_reviews"]) is int and terminal["minimum_whole_reviews"] == 2, "terminal complete review count")
    require(terminal["latest_complete_review"] == "whole02" and type(terminal["latest_review_actionable_P0_P1_P2_P3"]) is int and terminal["latest_review_actionable_P0_P1_P2_P3"] == 0, "terminal latest review findings")
    require(terminal["new_complete_review_required"] is False and terminal["root_whole02_adopted"] is True and terminal["root_integrity_adoption_required"] is True and terminal["root_integrity_adopted"] is False, "terminal root adoption boundary")
    require(terminal["publication_ready"] is False and terminal["issues_resolved"] is False and terminal["published"] is False and terminal["services_held_at"] == 1032, "terminal publication/service boundary")
    require(terminal["full_original_maximum_classification_bundle"] == "PARTIAL" and terminal["exact_application_priority"] == "UNKNOWN", "terminal scope boundary")
    latest = json.loads(regular_input(safe_path(terminal["whole02_verdict"])).read_text())
    require(latest["status"] == "COMPLETE_WHOLE02_ZERO_ACTIONABLE_FINDINGS" and latest["findings"] == [] and latest["findings_by_priority"] == {"P0": 0, "P1": 0, "P2": 0, "P3": 0} and latest["whole_reviews_completed"] == 2 and latest["minimum_whole_reviews"] == 2, "captured whole02 status/count differs")
    adoption = json.loads(regular_input(safe_path(terminal["root_whole02_adoption"])).read_text())
    require(adoption["status"] == "ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN" and adoption["whole_reviews_completed"] == 2 and adoption["minimum_whole_reviews"] == 2 and adoption["actionable_P0_P1_P2_P3"] == 0, "captured root whole02 adoption differs")
'''
    text=text.replace('    native = native_metadata()\n',insertion+'    native = native_metadata()\n')
    text=text.replace('        require(regular_input(p.parent / "CURRENT_STATUS_REPAIR01.json").read_bytes()', '        require(regular_input(p.parent / "TERMINAL_ADMIN_STAGE.json").read_bytes() == (ROOT / "TERMINAL_ADMIN_STAGE.json").read_bytes(), "external terminal status differs")\n        require(regular_input(p.parent / "CURRENT_STATUS_REPAIR01.json").read_bytes()')
    text=text.replace('["CURRENT_STATUS_REPAIR01.json", "README.md", "deposit_metadata.json", "metadata.json", "preprint.tex", "research_metadata.json"]','["CURRENT_STATUS_REPAIR01.json", "README.md", "TERMINAL_ADMIN_STAGE.json", "deposit_metadata.json", "metadata.json", "preprint.tex", "research_metadata.json"]')
    p.write_text(text)
    # Replace live summaries, retaining exact full prior prose in delivered before snapshots.
    for p in [DELIVERY/'README.md',KIT/'README.md']:
        text=p.read_text()
        if p.parent==DELIVERY:
            start=text.index('One complete whole-candidate review found two package issues;')
            end=text.index('\n\nThe note proves',start)
            text=text[:start]+'Two complete whole-candidate reviews are now finished. Whole01 found two bounded package issues, which were repaired; NEW complete whole02 found zero actionable P0–P3 issues and ROOT adopted that review. `TERMINAL_ADMIN_STAGE.json` records the current dated successor: final ROOT integrity adoption is required, readiness/issues-resolved/publication remain false, and services remain held at PR1032. Earlier statuses retain their exact historical meaning.'+text[end:]
            text=text.replace('Whole02 must perform those checks again.','Complete whole02 subsequently checked compilation and all seven pages; see its preserved report and source/interface derivation under `verification_kit/terminal_admin_history/whole02`. This administrative successor performs no new compile or page review.')
        else:
            start=text.index('One complete whole-candidate review found two package issues;')
            end=text.index('\n\nFor each fixed',start)
            text=text[:start]+'Two complete whole-candidate reviews are finished. Whole01 found two repaired package issues; NEW complete whole02 found zero actionable P0–P3 concerns and ROOT adopted it. `TERMINAL_ADMIN_STAGE.json` is the current dated successor, pending separate ROOT integrity adoption; publication readiness, issues-resolved and publication remain false, with external services held at PR1032. Earlier statuses remain exact historical records.'+text[end:]
            text=text.replace('fresh complete whole02 must check them again.','complete whole02 subsequently checked actual compilation and all seven unchanged pages. Its authored report and source/interface derivation are in `terminal_admin_history/whole02`. This terminal administrative stage makes no new compilation or page-view claim.')
        text=text.replace('The dated-metadata substage on 15 October 2026 is still pending a NEW complete whole02; current readiness/publication remain false and services remain held at PR1032.','At the dated-metadata substage on 15 October 2026 a NEW complete whole02 was still required. That review is now complete and ROOT-adopted; its historical pending state remains preserved. Current terminal state is recorded separately in `TERMINAL_ADMIN_STAGE.json`.')
        text+='\n## Terminal administrative successor\n\nThe terminal successor on 16 October 2026 preserves the complete paper, all native metadata objects, finite-checker/output-guard programs and all earlier records exactly. It adds selected authored whole02 outputs and ROOT adoption, exact before copies and individually resolved historical inventory references; no new source body, raw compiler stream, image, environment or current/old archive is newly packed. The original 100 stage-copy rows and 2,312 historical references remain exact prefixes. Current `verify.py` additionally checks two completed reviews, latest zero findings, the ROOT review adoption, the separate final-integrity requirement and PR1032 service hold. A later external ROOT integrity seal controls actual readiness. No earlier unrefereed or priority qualification changes.\n'
        p.write_text(text)
    dump(WORK/'PREPARATION_RESULT.json',{'utc':utc,'baseline':len(baseline),'allowed_existing_edits':edits,'before_copies':len(before),'old_copy_rows':100,'new_copy_rows':len(append),'old_history_rows':2312,'appended_history_rows':len(old_history['references'])-2312,'total_history_rows':len(old_history['references']),'publication_ready':False,'published':False})
    print(json.dumps(obj(WORK/'PREPARATION_RESULT.json'),indent=2))

if __name__=='__main__': main()
