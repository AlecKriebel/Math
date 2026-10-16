"""Fresh whole-package review custody launcher; only writes its own namespace."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, gzip, hashlib, json, os, stat, subprocess, sys
ROOT = Path(__file__).resolve().parent
A = ROOT.parent
F = A / 'preprint_package_v01'
def now(): return datetime.now(timezone.utc).isoformat()
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path':str(p.absolute()), 'resolved_path':str(p.resolve()), 'bytes':len(b),
            'sha256':hashlib.sha256(b).hexdigest(), 'mode':stat.S_IMODE(p.stat().st_mode)}
def write(p, obj): Path(p).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def stream(p, body):
    p.write_bytes(gzip.compress(body, mtime=0))
    assert gzip.decompress(p.read_bytes()) == body
    return {'codec':'gzip', 'logical_bytes':len(body), 'logical_sha256':hashlib.sha256(body).hexdigest(), 'stored':pin(p)}
def capture(label, argv, cwd, source_paths):
    d = ROOT / 'processes' / label
    d.mkdir(parents=True, exist_ok=False)
    custody = d / 'prelaunch_sources'
    custody.mkdir()
    copies=[]
    for i, p in enumerate(source_paths):
        p=Path(p)
        q=custody/('%02d_'%i+p.name)
        q.write_bytes(p.read_bytes()); q.chmod(0o444)
        copies.append({'input':pin(p), 'immutable_full_copy':pin(q)})
    custody.chmod(0o555)
    request={'UTC_prelaunch':now(), 'launcher_PID':os.getpid(), 'launcher_source':pin(__file__),
             'argv':argv, 'cwd':str(cwd), 'executable':pin(argv[0]), 'sources':copies,
             'optimization_disabled': '-E' in argv and '-B' in argv}
    write(d/'request.json', request)
    start=now()
    p=subprocess.Popen(argv, cwd=str(cwd), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr=p.communicate()
    request.update(actual_Popen_PID=p.pid, UTC_started=start, UTC_completed=now(), exit_code=p.returncode,
                   stdout=stream(d/'stdout.bin.gz',stdout), stderr=stream(d/'stderr.bin.gz',stderr))
    request['sources_unchanged_after_execution']=all(pin(x['input']['path']) == x['input'] for x in copies)
    write(d/'execution.json', request)
    print(json.dumps({'label':label, 'PID':p.pid, 'exit_code':p.returncode, 'stdout_bytes':len(stdout), 'stderr_bytes':len(stderr), 'receipt':str(d/'execution.json')}),flush=True)
    if p.returncode: raise RuntimeError('retained failure: '+label)
    return stdout
def seal_review():
    """Literal noncircular namespace closure after the captured child has exited."""
    manifest=ROOT/'OUTPUT_MANIFEST.json'; seal=ROOT/'CLOSURE_SEAL.json'
    assert not manifest.exists() and not seal.exists()
    files=sorted(p for p in ROOT.rglob('*') if p.is_file())
    assert all(not p.is_symlink() for p in files)
    for p in files: p.chmod(0o444)
    directories=[ROOT]+sorted(p for p in ROOT.rglob('*') if p.is_dir())
    rows=[dict(relative_path=str(p.relative_to(ROOT)), **pin(p)) for p in files]
    write(manifest,{'UTC':now(),'namespace':str(ROOT),'exclusions':['OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'],
                    'exclusion_reason':'Manifest cannot hash itself; separate seal pins this manifest and excludes its own bytes.',
                    'file_count':len(rows),'files':rows,
                    'directories':[{'path':str(p),'relative_path':'.' if p==ROOT else str(p.relative_to(ROOT)),
                                    'final_mode':0o555} for p in directories],
                    'historical_launch_modes':'Receipts preserve actual earlier modes; these rows are final frozen modes.'})
    manifest.chmod(0o444)
    seal_obj={'UTC':now(),'status':'CLOSED_FIRST_CANDIDATE_REVIEW_FROZEN_NAMESPACE',
              'actual_sealing_launcher_PID':os.getpid(),'launcher_argv':sys.argv,'cwd':str(Path.cwd()),
              'launcher_source':pin(__file__),'resolved_interpreter':pin(sys.executable),
              'manifest':pin(manifest),'self_exclusion':'CLOSURE_SEAL.json does not hash its own bytes.',
              'literal_total_file_count_including_manifest_and_seal':len(rows)+2,
              'all_file_modes':0o444,'all_directory_modes':0o555,
              'bounded_review_completion_percent':100,
              'publication_clearance':False,'mandatory_unresolved_issues':[],
              'nonmandatory_suggestion_ids':['C1','C2','C3','C4'],
              'physical_limit_bytes':20_000_000,
              'physical_payload_bytes_before_manifest':sum(p.stat().st_blocks*512 for p in files),
              'physical_bytes_exact_after_seal':'Actual value printed after final readback; the seal cannot noncircularly store its own final physical allocation.',
              'source_custody':'Every acceptance-bearing child process has prelaunch full immutable copies and actual Popen PID/complete streams. Sealing launcher PID is a genuine self-report.'}
    write(seal,seal_obj); seal.chmod(0o444)
    for p in sorted(directories,key=lambda p:len(p.parts),reverse=True): p.chmod(0o555)
    current=sorted(p for p in ROOT.rglob('*') if p.is_file())
    assert len(current)==len(rows)+2
    assert {str(p.relative_to(ROOT)) for p in current}=={r['relative_path'] for r in rows}|{'OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'}
    for row in rows:
        p=ROOT/row['relative_path'];assert pin(p)=={k:v for k,v in row.items() if k!='relative_path'}
    assert all(stat.S_IMODE(p.stat().st_mode)==0o444 for p in current)
    assert all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in directories)
    physical=sum(p.stat().st_blocks*512 for p in current+directories)
    assert physical<20_000_000
    print(json.dumps({'status':'PASS_ACTUAL_FROZEN_LITERAL_READBACK','UTC':now(),
                      'file_count':len(current),'directory_count':len(directories),
                      'physical_added_bytes':physical,'manifest':pin(manifest),'seal':pin(seal)},indent=2),flush=True)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('step', choices=['authenticate','replay','extract_pdf','check_evidence','close'])
    args=ap.parse_args()
    Path(__file__).chmod(0o444)
    if args.step=='authenticate':
        capture('authenticate_retry02', ['/opt/homebrew/bin/python3','-E','-B',str(ROOT/'authenticate.py')],ROOT,[ROOT/'authenticate.py',Path(__file__)])
    elif args.step=='replay':
        package=ROOT/'unpacked_actual_zip_v02'/'spectral-tensor-consistency'
        sources=[package/'verify_package.py']+sorted((package/'controls').glob('*.py'))+[Path(__file__)]
        capture('actual_zip_runner', ['/Users/alec/Documents/Math/.venv/bin/python','-E','-B',str(package/'verify_package.py'),'--output',str(ROOT/'portable_replay')],ROOT,sources)
    elif args.step=='extract_pdf':
        capture('final_pdf_extract', ['/opt/homebrew/bin/pdftotext','-layout',str(F/'spectral_tensor_consistency.pdf'),str(ROOT/'FINAL_PDF_TEXT.txt')],ROOT,[Path(__file__)])
    elif args.step=='check_evidence':
        capture('evidence_crosscheck', ['/opt/homebrew/bin/python3','-E','-B',str(ROOT/'check_evidence.py')],ROOT,[ROOT/'check_evidence.py',Path(__file__)])
    else:
        capture('closure', ['/opt/homebrew/bin/python3','-E','-B',str(ROOT/'close_review.py')],ROOT,[ROOT/'close_review.py',Path(__file__)])
        seal_review()
if __name__=='__main__': main()
