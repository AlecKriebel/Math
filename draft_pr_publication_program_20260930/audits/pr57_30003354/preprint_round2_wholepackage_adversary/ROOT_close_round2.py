"""ROOT-only evidence closure. Saved but not run by the round-2 adversary.
Reads pinned evidence; does not rerun controls, review mathematics, or publish.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, sys

BASE = Path(__file__).resolve().parent
DEST = BASE.parent / 'ROOT_PREPRINT_ROUND2_ADJUDICATION_20261003.json'
FLAG = '--root-only-after-personally-reading-report-verdict-and-source'

def utc(): return datetime.now(timezone.utc).isoformat()
def observed(path):
    s=path.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1: raise ValueError('Regular single-link file required: '+str(path))
    body=path.read_bytes()
    return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
            'full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o'),'type':'regular_file','nlink':s.st_nlink}

def verify():
    source=json.loads((BASE/'SOURCE.json').read_text())
    ready=json.loads((BASE/'READY.json').read_text())
    if observed(BASE/'SOURCE.json')!=ready['source']: raise ValueError('SOURCE binding')
    if stat.S_IMODE((BASE/'READY.json').lstat().st_mode)!=0o444: raise ValueError('READY mode')
    expected=set(source['files'])|{'SOURCE.json','READY.json'}
    actual=set()
    directories={'.'}
    for path in BASE.rglob('*'):
        name=str(path.relative_to(BASE)); mode=path.lstat().st_mode
        if stat.S_ISREG(mode): actual.add(name)
        elif stat.S_ISDIR(mode): directories.add(name)
        else: raise ValueError('Unsupported topology: '+name)
    if actual!=expected or directories!=set(source['directories']): raise ValueError('Exact owned topology')
    for name,pin in source['files'].items():
        if observed(BASE/name)!=pin: raise ValueError('Owned evidence pin: '+name)
    for name,pin in source['directories'].items():
        path=BASE if name=='.' else BASE/name
        if format(stat.S_IMODE(path.lstat().st_mode),'04o')!=pin['full_mode_07777']: raise ValueError('Directory mode: '+name)
    for row in source['publication_artifacts']:
        if observed(Path(row['path']))!=row['pin']: raise ValueError('Original publication artifact changed')
    for row in source['capture_relationships']:
        cap=json.loads((BASE/row['capture']).read_text()); pre=json.loads((BASE/row['prelaunch']).read_text())
        if not cap['actual_execution'] or any(cap[k]!=v for k,v in pre.items()): raise ValueError('Capture/prelaunch relation')
        for stream in ['stdout','stderr']:
            pin=observed(BASE/row[stream])
            if any(pin[k]!=cap[stream][k] for k in ['bytes','sha256']): raise ValueError('Full capture stream')
    pdf=json.loads((BASE/'PDF_RENDER_CAPTURE.json').read_text())
    for name,pin in pdf['pages'].items():
        q=observed(BASE/'pdf_review'/name)
        if any(q[k]!=pin[k] for k in ['bytes','sha256']): raise ValueError('Rendered page body')
    if (BASE/'checker_normal.stdout.bin').read_bytes()!=(BASE/'isolated_archive/expected_results.json').read_bytes(): raise ValueError('Recorded finite output')
    if ready['ROOT_approval_claimed'] or source['new_scientific_review_credit_from_packaging']!=0: raise ValueError('Claim scope')
    return source, ready

def main():
    if sys.argv[1:]!=[FLAG]: raise ValueError('ROOT must read the report, verdict and SOURCE before using '+FLAG)
    if DEST.exists() or DEST.is_symlink(): raise ValueError('Refusing existing ROOT closure')
    started=utc(); source,ready=verify()
    record={'schema':'pr57-root-round2-evidence-closure/v1','status':'ROOT_EXACT_ROUND2_EVIDENCE_CHECK_COMPLETE',
            'actual_executor_pid':os.getpid(),'start_utc':started,'end_utc':utc(),
            'source':observed(BASE/'SOURCE.json'),'ready':observed(BASE/'READY.json'),
            'report':observed(BASE/'REPORT.md'),'verdict':observed(BASE/'VERDICT.json'),
            'owned_regular_file_count':len(source['files'])+2,'directory_count':len(source['directories']),
            'original_publication_artifact_count':len(source['publication_artifacts']),
            'ROOT_reports_personally_read_report_verdict_source':True,
            'new_scientific_review_credit':0,'ROOT_release_approval_claimed':False,
            'native_acceptance_or_publication_claimed':False,
            'closure_scope':'Exact completed evidence and original artifact readback only; no new scientific review or release action'}
    with DEST.open('x') as out: json.dump(record,out,indent=2,sort_keys=True);out.write('\n')
    os.chmod(DEST,0o444)
    print(json.dumps(record,indent=2,sort_keys=True))

if __name__=='__main__': main()
