"""Prepare the fixed index of an already completed round-2 review.
No replay, scientific review, closure-helper execution or release activity.
Only new bookkeeping files are made read-only; existing artifacts are preserved.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, stat

BASE=Path(__file__).resolve().parent
PACKAGE=BASE.parent/'publication_package_v1'
NEW=['INDEX_NOTE.md','PACKAGING_LOG.md','ROOT_close_round2.py','ROOT_readback_round2.py','prepare_index.py']

def utc(): return datetime.now(timezone.utc).isoformat()
def pin(q):
    s=q.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1: raise ValueError('Regular single-link evidence required')
    body=q.read_bytes()
    return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o'),
            'type':'regular_file','nlink':s.st_nlink}
def save(name,body):
    with (BASE/name).open('x') as out: out.write(body)
def jsonbody(obj): return json.dumps(obj,indent=2,sort_keys=True)+'\n'

def main():
    for name in ['SOURCE.json','READY.json','INDEX_NOTE.md','PACKAGING_LOG.md']:
        if (BASE/name).exists() or (BASE/name).is_symlink(): raise ValueError('Refuse existing new index output: '+name)
    started=utc()
    existing={str(q.relative_to(BASE)):pin(q) for q in BASE.rglob('*') if q.is_file() and str(q.relative_to(BASE)) not in NEW}
    if len(existing)!=58: raise ValueError('Delivered existing review topology must remain 58 files')
    save('PACKAGING_LOG.md',f'# Evidence packaging checkpoints\n\n- {started}: Began indexing the previously completed round-2 review. Delivered REPORT/VERDICT and all previous artifacts are preserved in body and full modes; no new scientific review or credit. Evidence-bookkeeping completion estimate: 20%.\n')
    note='''# Fixed round-2 evidence index

This packet indexes the already delivered independent review, not a new review.
The exact REPORT.md and VERDICT.json remain operative and unchanged. Packaging
adds zero scientific attempt or independent-review credit and claims no ROOT
approval, native acceptance, publication, DOI or external communication.

SOURCE.json is a read-only exact file/topology/full-07777-mode/body index.
READY.json pins that index. Existing evidence keeps its delivered 0644 modes
and both existing subdirectories retain 0755; their bodies and complete modes
are pinned, not silently changed. Only the new bookkeeping files are 0444.

All 58 prior meaningful review files are included: initial independent argument,
delivered report/verdict/log, artifact pins, complete prelaunch/capture records
and full successful/expected-failure streams, fresh independent operator control,
archive/source/metadata checks, original review operators, the diagnostic archive
extraction and its locally rebuilt ZIP, and six retained PDF previews. The
isolated extraction and rebuilt ZIP are diagnostic support, not new publication
files. The six previews are tied to the exact actual final six-page PDF capture.

The original four publication bodies and complete modes are independently pinned
in place; nothing from the publication package is copied or changed here. The
previous verification captures remain the actual executions already documented.
Index checking never replays the checker, archive builder, rendering or review.

ROOT_close_round2.py and ROOT_readback_round2.py are newly saved, syntax-parsed,
unexecuted ROOT-only helpers. ROOT must personally read the complete delivered
report/verdict and this SOURCE before explicitly running the closure helper.
The separate reader imports no closure-helper code. Their future records are
siblings outside the exact fixed packet and refuse overwrite. They verify
evidence, not publication authorization. Historical handoff absences do not
override later actual execution or ROOT records.
'''
    save('INDEX_NOTE.md',note)
    for name in ['ROOT_close_round2.py','ROOT_readback_round2.py','prepare_index.py']:
        ast.parse((BASE/name).read_text(),filename=name)
    relationships=[]
    for label in ['checker_normal','checker_O','checker_ENV','archive_build','archive_overwrite_refusal']:
        relationships.append({'capture':label+'.CAPTURE.json','prelaunch':label+'.PRELAUNCH.json',
                              'stdout':label+'.stdout.bin','stderr':label+'.stderr.bin'})
    relationships.extend([{'capture':'OPERATOR_CAPTURE.json','prelaunch':'OPERATOR_PRELAUNCH.json',
                           'stdout':'operator.stdout.bin','stderr':'operator.stderr.bin'},
                          {'capture':'PDF_RENDER_CAPTURE.json','prelaunch':'PDF_RENDER_PRELAUNCH.json',
                           'stdout':'pdf_render.stdout.bin','stderr':'pdf_render.stderr.bin'}])
    for row in relationships:
        cap=json.loads((BASE/row['capture']).read_text());pre=json.loads((BASE/row['prelaunch']).read_text())
        if cap.get('actual_execution') is not True or any(cap[k]!=v for k,v in pre.items()): raise ValueError('Actual/prelaunch binding')
        for channel in ['stdout','stderr']:
            seen=pin(BASE/row[channel])
            if any(seen[k]!=cap[channel][k] for k in ['bytes','sha256']): raise ValueError('Complete actual stream binding')
        if datetime.fromisoformat(cap['end_utc'])<datetime.fromisoformat(cap['start_utc']): raise ValueError('UTC chronology')
    pdf=json.loads((BASE/'PDF_RENDER_CAPTURE.json').read_text())
    if set(pdf['pages'])!={f'page-{i}.png' for i in range(1,7)}: raise ValueError('Exactly six preview pages')
    for name,expected in pdf['pages'].items():
        actual=pin(BASE/'pdf_review'/name)
        if any(actual[k]!=expected[k] for k in ['bytes','sha256']): raise ValueError('Preview render binding')
    oldpins=json.loads((BASE/'ARTIFACT_PINS.json').read_text())['artifacts'];publication=[]
    for name,expected in oldpins.items():
        q=PACKAGE/name;seen=pin(q)
        if any(seen[k]!=expected[k] for k in ['bytes','sha256']): raise ValueError('Original publication pin changed')
        publication.append({'path':str(q),'pin':seen})
    if pdf['input_pdf']!=oldpins['integer_endpoint_discontinuity.pdf']: raise ValueError('Preview source PDF')
    if (BASE/'checker_normal.stdout.bin').read_bytes()!=(BASE/'isolated_archive/expected_results.json').read_bytes(): raise ValueError('Finite diagnostic output')
    if (BASE/'isolated_archive/integer-endpoint-discontinuity-verification-v1.zip').read_bytes()!=(PACKAGE/'integer-endpoint-discontinuity-verification-v1.zip').read_bytes(): raise ValueError('Diagnostic rebuilt archive')
    for name,expected in existing.items():
        if pin(BASE/name)!=expected: raise ValueError('Prior artifact changed during indexing: '+name)
    finished=utc()
    with (BASE/'PACKAGING_LOG.md').open('a') as out:
        out.write(f'- {finished}: Checked all 58 prior file bodies/types/links/full modes, all seven actual capture/prelaunch/full-stream relationships, original four publication pins, six retained preview pins and diagnostic archive/result equality. New helpers syntax-parsed only and not run. Evidence-bookkeeping completion estimate: 100%; new scientific credit: zero.\n')
    for name in NEW: os.chmod(BASE/name,0o444)
    files={};dirs={'.':{'type':'directory','full_mode_07777':format(stat.S_IMODE(BASE.lstat().st_mode),'04o')}}
    for q in sorted(BASE.rglob('*')):
        rel=str(q.relative_to(BASE));s=q.lstat()
        if stat.S_ISREG(s.st_mode): files[rel]=pin(q)
        elif stat.S_ISDIR(s.st_mode):dirs[rel]={'type':'directory','full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o')}
        else: raise ValueError('Unsupported owned topology: '+rel)
    source={'schema':'pr57-round2-fixed-source-evidence-index/v1','prepared_at_utc':finished,'actual_preparer_pid':os.getpid(),
            'files':files,'directories':dirs,'index_excluded_files':['SOURCE.json','READY.json'],
            'final_exact_regular_file_domain':sorted(set(files)|{'SOURCE.json','READY.json'}),
            'publication_artifacts':publication,'capture_relationships':relationships,
            'delivered_report_verdict_preserved':True,'prior_file_count':len(existing),
            'diagnostic_extraction_and_rebuilt_archive_are_not_new_publication':True,
            'retained_PDF_preview_count':6,'all_preexisting_body_and_modes_preserved':True,
            'new_scientific_review_credit_from_packaging':0,'ROOT_approval_claimed':False,
            'root_helpers_saved_unexecuted':True,'helpers_syntax_parse_only':True,
            'expected_future_root_records':[str(BASE.parent/'ROOT_PREPRINT_ROUND2_ADJUDICATION_20261003.json'),
                                            str(BASE.parent/'ROOT_PREPRINT_ROUND2_READBACK_20261003.json')]}
    save('SOURCE.json',jsonbody(source));os.chmod(BASE/'SOURCE.json',0o444)
    ready={'schema':'pr57-round2-fixed-evidence-ready/v1','status':'READY_FOR_ROOT_PERSONAL_READ_AND_EXACT_EVIDENCE_CLOSURE',
           'source':pin(BASE/'SOURCE.json'),'delivered_report':files['REPORT.md'],'delivered_verdict':files['VERDICT.json'],
           'owned_regular_file_count':len(files)+2,'directory_count':len(dirs),
           'prepared_at_utc':finished,'evidence_bookkeeping_completion_percent':100,
           'scientific_review_already_completed':True,'new_scientific_review_credit_from_packaging':0,
           'ROOT_approval_claimed':False,'root_helpers_executed':False,'native_acceptance_or_publication_claimed':False}
    save('READY.json',jsonbody(ready));os.chmod(BASE/'READY.json',0o444)
    for name,expected in existing.items():
        if pin(BASE/name)!=expected: raise ValueError('Prior artifact changed at freeze: '+name)
    print(jsonbody({'status':ready['status'],'actual_preparer_pid':os.getpid(),'SOURCE':pin(BASE/'SOURCE.json'),
                    'READY':pin(BASE/'READY.json'),'REPORT':files['REPORT.md'],'VERDICT':files['VERDICT.json'],
                    'owned_regular_file_count':len(files)+2,'directory_count':len(dirs),
                    'root_helpers_executed':False,'new_scientific_review_credit':0}))

if __name__=='__main__':main()
