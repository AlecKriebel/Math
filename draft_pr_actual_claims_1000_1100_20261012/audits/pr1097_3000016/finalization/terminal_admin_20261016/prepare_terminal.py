#!/usr/bin/env python3
"""Administrative reconciliation only; no compilation, service, or Git operations."""
import sys
sys.dont_write_bytecode = True
import datetime, difflib, hashlib, io, json, os, zipfile
from pathlib import Path
F = Path(__file__).resolve().parent
A = F.parent.parent
P = A / 'preprint_v1_0'
K = P / 'kit'
T = K / 'provenance/terminal_admin_20261016'
def need(q,m):
    if not q: raise ValueError(m)
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p): return json.loads(p.read_text())
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.terminal-tmp')
    with tmp.open('xb') as s:s.write(b)
    os.replace(tmp,p)
def write(p,v):put(p,(json.dumps(v,indent=2)+'\n').encode())
def main():
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    freeze=load(F/'INPUT_FREEZE.json')['entries']
    before={r['path']:r for r in load(F/'BEFORE_BYTES.json')['entries']}
    for r in freeze:need(pin(A/r['path'])=={k:r[k] for k in ['bytes','sha256']},'pre-mutation freeze '+r['path'])
    terminal={
      'recorded_at_utc':utc,'record_type':'DATED_TERMINAL_ADMINISTRATIVE_RECONCILIATION_ONLY',
      'pr':1097,'head':'ad7b0eeef847da65afe1b691705cfa6e832e8201',
      'complete_whole_package_reviews_completed':2,'minimum_complete_whole_package_reviews_required':2,
      'latest_complete_whole_review':'NEW_COMPLETE_WHOLE_PACKAGE_02',
      'latest_whole_review_finding_counts':{'P0':0,'P1':0,'P2':0,'P3':0},
      'latest_whole_review_root_adopted':True,'repair01_root_adopted':True,
      'further_complete_whole_review_currently_required':False,
      'external_ROOT_final_integrity_required':True,'external_ROOT_final_integrity_adopted':False,
      'publication_ready':False,'issues_resolved':False,'published':False,'ordered_service_hold_pr':1032,
      'mathematics_paper_checker_path_guards_native_metadata':'UNCHANGED',
      'priority_independent_discovery_worldwide_openness':'UNKNOWN',
      'historical_omitted_program_replayed':False,'external_actions_performed':False,
      'optimized_history':'Initial empty INDEPENDENT_OPTIMIZED.json is an uncompleted historical attempt. Completed INDEPENDENT_OPTIMIZED_RERUN.json is the actual completed result; both prior identities remain unchanged.',
      'supersession_scope':'Preparation STATUS and CURRENT_REPAIR are exact dated past checkpoints. This separate record reconciles later review count and ROOT adoption only; it is not a readiness seal.',
      'substantive_new_defect_policy':'Hold, repair, then a new complete whole03 before any readiness promotion.'}
    write(P/'TERMINAL_ADMIN.json',terminal);write(K/'TERMINAL_ADMIN.json',terminal)
    paragraph='''\n## Terminal administrative checkpoint, 16 October 2026\n\n`TERMINAL_ADMIN.json` records two completed new full whole-package reviews,\nmeeting the minimum of two. The latest whole02 found zero actionable P0–P3\nfindings and ROOT independently adopted it; ROOT also adopted repair01. No\nfurther whole review is currently required. External ROOT final integrity of\nthis reconciled package is still required and has not been adopted. Publication\nreadiness, issues-resolved and published remain false; the service hold after\nPR #1032 remains in force. A substantive new defect requires a hold, repair\nand a new complete whole03. This administrative checkpoint grants no publication\nauthority and performs no external action.\n\nThe preparation zero-review statements and repair one-review/pending statements\nabove, in STATUS and in CURRENT_REPAIR describe their exact past checkpoints.\nThey remain unchanged history, rather than the current review count. The native\nmetadata's notes already describe past preparation and every native field and\n`zenodo-deposit.json` remain byte-identical. The mathematical proof, PDF/TeX,\nchecker, source credits, citation and all path guards remain byte-identical.\nThe initially empty optimized independent output remains an uncompleted attempt;\n`INDEPENDENT_OPTIMIZED_RERUN.json` is the actual completed result.\n\n`provenance/terminal_admin_20261016/` in the kit adds individually located safe\nauthored whole02/ROOT records and exact old interfaces, with separate omission\nreasons and pin resolutions. Historical code copies are evidence, not supported\nportable commands or claims of omitted-program replay. No old/current ZIP,\nthird-party body/text/pixels, runtime or raw command/compiler/Git stream is newly\nredistributed as provenance. The delivery ZIP contains the current kit only.\n'''
    for n in ['README.md','kit/README.md']:
        text=(F/'before'/n).read_text()
        if n=='README.md':
            text=text.replace('Third-party source bodies and historical code are not distributed.','Third-party source bodies and omitted original checker programs are not distributed. Historical reviewer code copies are provenance only.')
            text=text.replace('`kit/CURRENT_REPAIR.json` is the current repair-stage accounting:', '`kit/CURRENT_REPAIR.json` retains the dated repair-stage accounting:')
        put(P/n,(text+paragraph).encode())
    text=(F/'before/kit/provenance/README.md').read_text()+paragraph
    put(K/'provenance/README.md',text.encode())
    # Only the verifier gains administrative semantics. Shared common/path guards stay exact.
    text=(F/'before/kit/scripts/verify.py').read_text()
    text=text.replace('from common import inventory, binding_check','from common import KIT, inventory, binding_check, read_json, record, require')
    helper='''
def terminal_semantics():
    value = read_json(KIT / "TERMINAL_ADMIN.json")
    expected = {
        "record_type": "DATED_TERMINAL_ADMINISTRATIVE_RECONCILIATION_ONLY",
        "pr": 1097, "head": "ad7b0eeef847da65afe1b691705cfa6e832e8201",
        "complete_whole_package_reviews_completed": 2,
        "minimum_complete_whole_package_reviews_required": 2,
        "latest_complete_whole_review": "NEW_COMPLETE_WHOLE_PACKAGE_02",
        "latest_whole_review_finding_counts": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
        "latest_whole_review_root_adopted": True, "repair01_root_adopted": True,
        "further_complete_whole_review_currently_required": False,
        "external_ROOT_final_integrity_required": True,
        "external_ROOT_final_integrity_adopted": False,
        "publication_ready": False, "issues_resolved": False, "published": False,
        "ordered_service_hold_pr": 1032,
        "mathematics_paper_checker_path_guards_native_metadata": "UNCHANGED",
        "priority_independent_discovery_worldwide_openness": "UNKNOWN",
        "historical_omitted_program_replayed": False, "external_actions_performed": False,
    }
    for key, want in expected.items():
        require(type(value.get(key)) is type(want) and value[key] == want,
                "terminal semantic mismatch: " + key)
    layer = KIT / "provenance" / "terminal_admin_20261016"
    copies = read_json(layer / "COPIES.json")["entries"]
    for row in copies:
        require(record(KIT / row["copy_path"]) ==
                {"bytes": row["bytes"], "sha256": row["sha256"]},
                "terminal exact copy mismatch")
    root = read_json(layer / "selected" / "ROOT_WHOLE_PACKAGE_REVIEW_02.json")
    require(root["status"] == "ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN"
            and root["whole_reviews_completed"] == 2 and root["minimum_whole_reviews"] == 2
            and root["actionable_P0_P1_P2_P3"] == 0
            and root["terminal_administrative_reconciliation_and_root_final_integrity_required"] is True
            and root["publication_ready"] is False and root["published"] is False
            and root["services_held_after_pr"] == 1032, "terminal ROOT adoption mismatch")
    verdict = read_json(layer / "selected" / "reviews" / "package_02" / "VERDICT.json")
    require(verdict["review"] == value["latest_complete_whole_review"]
            and verdict["findings"] == []
            and verdict["finding_counts"] == value["latest_whole_review_finding_counts"],
            "terminal whole02 verdict mismatch")
    original = read_json(KIT / "provenance" / "CUSTODY.json")["entries"]
    repair = read_json(KIT / "provenance" / "repair01" / "CUSTODY.json")["entries"]
    require(len(original) == 165 and sum(r["decision"] == "EXACT_AUTHORED_COPY" for r in original) == 83
            and sum(r["decision"] == "EXCLUDED" for r in original) == 82,
            "terminal original custody counts")
    require(len(repair) == 332 and sum(r["decision"] == "EXACT_DISTRIBUTED_BYTES" for r in repair) == 233
            and sum(r["decision"] == "EXCLUDED" for r in repair) == 99,
            "terminal repair custody counts")
    # These fields intentionally remain earlier dated history.
    old = read_json(KIT / "CURRENT_REPAIR.json")
    require(old["complete_whole_package_reviews_completed"] == 1
            and old["repair_root_adoption"] == "PENDING" and old["new_complete_whole02"] == "REQUIRED",
            "terminal dated repair history changed")
    history = read_json(KIT / "provenance" / "repair01" / "STAGE_RESOLUTION.json")["entries"]
    require(len(history) == 1127 and sum(r["original_audit_resolution"]["state"] == "INDIVIDUAL_OMISSION"
            for r in history) == 18, "terminal historical omissions changed")
    return {"whole_reviews_completed": 2, "minimum_whole_reviews": 2,
            "latest_zero_actionable_root_adopted": True,
            "external_ROOT_final_integrity": "REQUIRED_NOT_ADOPTED",
            "publication_ready": False, "issues_resolved": False, "published": False,
            "ordered_service_hold_pr": 1032}

'''
    text=text.replace('def main():',helper+'def main():')
    text=text.replace('    result.pop("metadata")','    result.pop("metadata")\n    result["terminal"] = terminal_semantics()')
    put(K/'scripts/verify.py',text.encode())
    source_copies=[]
    def copy(src,dst,locator):
        need(not dst.exists(),'new copy exists '+str(dst));put(dst,src.read_bytes())
        source_copies.append({'source_locator':locator,'source_path':src.relative_to(A).as_posix(),
                             'copy_path':dst.relative_to(K).as_posix(),**pin(src)})
    selected=['ROOT_REPAIR_REVIEW_01.json','ROOT_WHOLE_PACKAGE_REVIEW_02.json']
    selected+=['reviews/package_02/'+n for n in ['REPORT.md','VERDICT.json','FINAL_SEAL.json','INPUT_FREEZE.json','INPUT_PRESERVATION.json','OUTPUT_PINS.json','SOURCE_READ_LEDGER.json','INDEPENDENT_DERIVATION.md','INDEPENDENT_NORMAL.json','INDEPENDENT_OPTIMIZED_RERUN.json','INDEPENDENT_REPRODUCTION.json','MATH_HARNESS_CORRECTION.json','MATH_OPTIMIZED_PROCESS.json','REVIEW_HARNESS_EVENTS.json','RESEARCH_LOG.md','CUSTODY_REPRODUCTION.json','ZIP_CLOSED.json','PDF_RENDER_RECEIPT.json','PDF_VISUAL_REVIEW.json','WRITER_GUARDS.json','SCRATCH_CLEANUP.json','EXTRA_SCRATCH_CLEANUP.json','SCRATCH_PINS.json','EXTRA_SCRATCH_PINS.json','ADDITIONAL_INPUT_PINS.json','PACKAGE_REPRODUCTION.json','independent_math.py','independent_math_initial.py']]
    for n in selected:copy(A/n,T/'selected'/n,n)
    for n in ['INPUT_FREEZE.json','BEFORE_BYTES.json']:copy(F/n,T/n,'finalization/terminal_admin_20261016/'+n)
    for r in before.values():
        if not r['path'].endswith('.zip'):
            n=r['path'].removeprefix('preprint_v1_0/')
            copy(A/r['before_path'],T/'before'/n,r['path'])
    write(T/'COPIES.json',{'utc':utc,'historical_code_scope':'Historical authored code copies only; not supported commands or omitted-program replay.','entries':source_copies})
    distributed={}
    for p in sorted(K.rglob('*')):
        if p.is_file() and p!=K/'MANIFEST.json':
            r=pin(p);distributed.setdefault((r['bytes'],r['sha256']),[]).append(p.relative_to(K).as_posix())
    def omit_reason(n):
        if n.endswith('.zip'):return 'Old/current ZIP identity retained locally only; no ZIP redistributed as provenance.'
        if '/sources/' in n or n.endswith(('.pdf','.png','.txt')):return 'Third-party body/text/pixels or local derivative omitted; retain individual prior identity and omission, no restored-byte claim.'
        if n.endswith(('.stdout','.stderr')) or '/tmp/' in n or 'COMMAND_RECEIPTS' in n or 'HARNESS_FAILURE' in n:return 'Raw command/compiler/Git stream or local harness artifact omitted; exact captured hash only.'
        return 'Unselected local historical artifact/program/configuration omitted; exact source locator/hash only, no replay or distributed-byte claim.'
    custody=[]
    actual={}
    for r in freeze:
        n=r['path'];key=(r['bytes'],r['sha256']);src=A/(before[n]['before_path'] if n in before else n)
        need(pin(src)=={k:r[k] for k in ['bytes','sha256']},'before identity '+n)
        actual.setdefault(key,[]).append(src.relative_to(A).as_posix())
        row={'captured_path':n,'bytes':r['bytes'],'sha256':r['sha256']}
        if key in distributed:row.update(decision='EXACT_DISTRIBUTED_BYTES',copy_path=distributed[key][0])
        else:row.update(decision='EXCLUDED',reason=omit_reason(n))
        custody.append(row)
    write(T/'CUSTODY.json',{'utc':utc,'scope':'One terminal-capture decision per preexisting regular audit file. Original165 and repair332 decisions are unchanged.','entries':custody})
    # External instruction/tool pins remain metadata-only in the portable kit.
    external={}
    for r in load(A/'reviews/package_02/ADDITIONAL_INPUT_PINS.json')['files']:
        p=Path(r['path']);need(pin(p)=={k:r[k] for k in ['bytes','sha256']},'external pin changed')
        external[(r['bytes'],r['sha256'])]=str(p)
    oldrows=load(K/'provenance/repair01/STAGE_RESOLUTION.json')['entries']
    old_omissions={(r['bytes'],r['sha256']):r for r in oldrows if r['original_audit_resolution']['state']=='INDIVIDUAL_OMISSION'}
    rows=[];missing=[]
    for f in freeze:
        n=f['path']
        if not n.endswith('.json') or not any(s in Path(n).name for s in ['PINS','FREEZE','BEFORE_BYTES']):continue
        value=load(A/(before[n]['before_path'] if n in before else n))
        for field in ['entries','files','records','renders']:
            source=value.get(field)
            if not isinstance(source,list):continue
            for index,r in enumerate(source):
                size=r.get('bytes',r.get('size'));digest=r.get('sha256')
                need(isinstance(size,int) and isinstance(digest,str),'unsupported row '+n)
                key=(size,digest);locator=r.get('snapshot_path',r.get('path',r.get('file',r.get('repository_path'))))
                row={'inventory':n,'array':field,'row_zero_based':index,'captured_locator':locator,'bytes':size,'sha256':digest}
                if key in actual:row['original_audit_resolution']={'state':'EXACT_CURRENT_OR_CAPTURED_BEFORE_BYTES','path':actual[key][0]}
                elif key in external:row['original_audit_resolution']={'state':'EXACT_EXTERNAL_READ_ONLY_INPUT','path':external[key]}
                else:
                    if key in old_omissions:reason='Retained preexisting individual omission of third-party page-image identity; never restored or fabricated.'
                    elif '/package_02/SCRATCH_PINS.json' in n or '/package_02/EXTRA_SCRATCH_PINS.json' in n:reason='Retained individually pinned removed reviewer scratch identity; cleanup recorded by whole02 SCRATCH_CLEANUP/EXTRA_SCRATCH_CLEANUP. Not available current bytes.'
                    else:missing.append({'inventory':n,'row':index,'locator':locator,'bytes':size,'sha256':digest});reason='REQUIRES_INVESTIGATION'
                    row['original_audit_resolution']={'state':'INDIVIDUAL_OMISSION','reason':reason}
                if key in distributed:row['portable_resolution']={'state':'EXACT_DISTRIBUTED_BYTES','path':distributed[key][0]}
                else:row['portable_resolution']={'state':'INDIVIDUAL_OMISSION','reason':omit_reason(str(locator))}
                rows.append(row)
    write(F/'UNRESOLVED_PRIOR_PINS.json',{'entries':missing})
    need(not missing,'unresolved prior pin identities; administrative hold')
    write(T/'STAGE_RESOLUTION.json',{'utc':utc,'scope':'Every row of all preexisting *PINS*, *FREEZE* and BEFORE_BYTES inventories, with individual original/current-before and portable resolution. The prior1127 rows are unchanged historical records.','entries':rows})
    put(T/'README.md',('''# Terminal administrative custody — 16 October 2026

INPUT_FREEZE captures all 683 preexisting regular audit files. CUSTODY has one
individual decision for each. COPIES gives each exact safe authored whole02/ROOT
and old-interface source locator, copy locator, byte count and hash. BEFORE_BYTES
records the seven minimal old active interfaces; old ZIP bytes stay local only.
STAGE_RESOLUTION resolves every prior inventory row independently, retaining
prior omissions (including the 18 already-absent third-party page-image rows)
and removed reviewer scratch identities individually. No bytes are fabricated.

Original 165/83-copy/82-exclusion decisions, repair 332/233-exact/99-exclusion
decisions, all 1127 old stage rows, statuses, reports, pins, counters and seals
remain byte-exact dated history. Current TERMINAL_ADMIN records two completed
new full reviews, minimum two, latest whole02 zero actionable and ROOT-adopted.
No further whole review is currently required. External ROOT final integrity
is still required, not adopted. Publication-ready, issues-resolved and published
remain false and ordered services are held after PR #1032.

The old initially empty optimized output is an uncompleted attempt. The exact
completed INDEPENDENT_OPTIMIZED_RERUN.json is included as completed evidence.
Historical authored code copies are evidence only, not supported portable
commands or omitted-program replay claims. Source bodies/text/pixels, runtimes,
raw command/compiler/Git streams and old/current ZIPs are not newly distributed
as provenance. The current delivery ZIP packages the kit and is external to its
own content inventory. The external binding remains outside the kit and ZIP.
These inventories are hashes, not signatures or publication authority.
''').encode())
    files=sorted(p for p in K.rglob('*') if p.is_file() and p!=K/'MANIFEST.json')
    manifest=load(F/'before/kit/MANIFEST.json');manifest['entries']=[{'path':p.relative_to(K).as_posix(),**pin(p)} for p in files]
    write(K/'MANIFEST.json',manifest)
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_STORED) as z:
        for p in sorted(p for p in K.rglob('*') if p.is_file()):
            info=zipfile.ZipInfo(p.relative_to(K).as_posix(),(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes())
    put(P/'pr1097_support_v1_0.zip',stream.getvalue())
    binding=load(F/'before/DEPOSIT_BINDING.json');binding['kit_manifest_sha256']=pin(K/'MANIFEST.json')['sha256'];binding['files']=[{'name':n,**pin(P/n)} for n in ['paper.pdf','pr1097_support_v1_0.zip']]
    write(P/'DEPOSIT_BINDING.json',binding)
    changes=[];diff=[]
    for r in freeze:
        n=r['path'];now=pin(A/n)
        if now!={k:r[k] for k in ['bytes','sha256']}:
            need(n in before,'unpermitted mutation '+n)
            old=A/before[n]['before_path'];changes.append({'path':n,'before_path':old.relative_to(A).as_posix(),'before':pin(old),'current':now})
            if not n.endswith('.zip'):diff.extend(difflib.unified_diff(old.read_text().splitlines(True),(A/n).read_text().splitlines(True),fromfile='before/'+n,tofile='current/'+n))
            else:diff.append('\nBINARY ARCHIVE CHANGE\n'+json.dumps(changes[-1],indent=2)+'\n')
    diff.extend(difflib.unified_diff([], (K/'TERMINAL_ADMIN.json').read_text().splitlines(True),fromfile='/dev/null',tofile='new/preprint_v1_0/kit/TERMINAL_ADMIN.json'))
    diff.append('\nIdentical new external TERMINAL_ADMIN.json: preprint_v1_0/TERMINAL_ADMIN.json\n')
    for n in ['README.md']:
        diff.extend(difflib.unified_diff([], (T/n).read_text().splitlines(True),fromfile='/dev/null',tofile='new/'+(T/n).relative_to(A).as_posix()))
    put(F/'COMPLETE_OPERATIVE_CODE_PROSE_DIFF.patch',''.join(diff).encode())
    write(F/'CURRENT_CHANGES.json',{'utc':utc,'changes':changes,'unchanged_preexisting_files':len(freeze)-len(changes),'all_replacements_atomic':True})
    write(F/'CONSTRUCTION.json',{'utc':utc,'preexisting_files':len(freeze),'minimal_existing_changes':len(changes),'new_source_copies':len(source_copies),'prior_pin_rows':len(rows),'archive':pin(P/'pr1097_support_v1_0.zip'),'members':len(files)+1,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032})
    print(json.dumps(load(F/'CONSTRUCTION.json'),indent=2))
if __name__=='__main__':main()
