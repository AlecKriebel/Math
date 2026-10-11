from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys
if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no -O')
A=Path(__file__).resolve().parent;S=A/'whole_package_round1_20261004';F=A/'ROOT_round1_review_readback_20261004';F.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
m=S/'AUDIT_MANIFEST.json';manifest=json.loads(m.read_bytes())
if sha(m.read_bytes())!='b046695dd12d137b2010a6c5951bce97bc9d99cce37db48ab00e2da7d5057953':raise RuntimeError('Manifest mismatch')
if (S/'AUDIT_MANIFEST.sha256').read_text().split()[0]!=sha(m.read_bytes()):raise RuntimeError('Digest mismatch')
expected=set()
for r in manifest['files']:
    p=Path(r['path'])
    if p.is_absolute() or '..' in p.parts or str(p) in expected or (S/p).is_symlink():raise RuntimeError('Unsafe manifest')
    expected.add(str(p));b=(S/p).read_bytes()
    if len(b)!=r['bytes'] or sha(b)!=r['sha256']:raise RuntimeError('File drift: '+str(p))
actual={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}
if actual!=expected|{'AUDIT_MANIFEST.json','AUDIT_MANIFEST.sha256'}:raise RuntimeError('Inventory mismatch')
records=[]
for p in sorted((S/'execution').glob('*/record.json')):
    r=json.loads(p.read_bytes())
    if not isinstance(r['child_pid'],int) or r['child_pid']<=0:raise RuntimeError('Missing actual PID')
    for stream in ['stdout','stderr']:
        b=(p.parent/(stream+'.bin')).read_bytes()
        if len(b)!=r[stream+'_bytes'] or sha(b)!=r[stream+'_sha256']:raise RuntimeError('Stream mismatch')
    records.append({'record':str(p.relative_to(S)),'child_pid':r['child_pid'],'exit_code':r['exit_code']})
copy=F/'independent_adversary.py';shutil.copyfile(S/'independent_adversary.py',copy)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();argv=[sys.executable,'-E','-B',str(copy)]
p=subprocess.Popen(argv,cwd=F,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
(F/'stdout.bin').write_bytes(out);(F/'stderr.bin').write_bytes(err)
receipt={'argv':argv,'cwd':str(F),'started_utc':start,'actual_child_pid':p.pid,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'source_sha256':sha(copy.read_bytes()),'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)}
(F/'EXECUTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
if p.returncode or err:raise RuntimeError('Independent adversary failed')
got=json.loads(out);old=json.loads((S/'INDEPENDENT_ADVERSARY_RESULTS.json').read_bytes())
if got!=old or got['exact_checks']!=293966 or got['cycles_including_high_translates']!=10048:raise RuntimeError('Replay differs')
result={'status':'ROUND1_REPORT_EVIDENCE_AND_ADVERSARY_REPLAY_PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),'manifest_members':len(expected),'manifest_sha256':sha(m.read_bytes()),'actual_review_processes':records,'new_adversary_exact_checks':got['exact_checks'],'replay_equals_reviewer_JSON':True,'reviewer_report_sha256':sha((S/'REPORT.md').read_bytes()),'minor_traceability_issue_repaired_separately':True,'priority_clearance':False,'publication_authorized':False,'scope':'Bounded exact controls and review artifact custody only; not universal proof or priority certification.'}
(F/'READBACK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
