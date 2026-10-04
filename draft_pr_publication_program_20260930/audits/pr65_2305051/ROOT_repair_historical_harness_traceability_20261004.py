"""Append exact historical harness evidence; keep reviewed mathematics unchanged."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, zipfile
if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no -O')
A=Path(__file__).resolve().parent;K=A/'publication_package_v1';F=A/'ROOT_round1_harness_traceability_repair_20261004'
F.mkdir(exist_ok=False)
shutil.copytree(K,F/'before')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
math_before={n:sha(K/n) for n in ['note.tex','note.pdf','verification/author/CANDIDATE.md','verification/author/verify_recursion.py','verification/legacy_independent/independent_checks.py','verification/analytic/diagnostics.py','verification/factorization/exact_factorization_controls.py','run_verification.py','execution/EXECUTIONS.json','zenodo-deposit.json']}
old=A/'reviewable_note_v1/run_verification.py';body=old.read_bytes();receipt=json.loads((K/'execution/EXECUTIONS.json').read_bytes())
if hashlib.sha256(body).hexdigest()!=receipt['harness_sha256']:
    raise RuntimeError('Historical harness source does not match archived receipt')
target=K/'execution/historical_run_verification.py'
with target.open('xb') as f:f.write(body)
provenance=json.loads((K/'PROVENANCE.json').read_bytes())
provenance['copied_files'].append({'package_path':'execution/historical_run_verification.py','source_path_relative_to_audit':'reviewable_note_v1/run_verification.py','sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'copy_status':'unchanged byte-for-byte; historical operator for archived execution receipt, not current entry point'})
provenance['historical_execution_harness']={'package_path':'execution/historical_run_verification.py','archived_receipt':'execution/EXECUTIONS.json','matching_sha256':receipt['harness_sha256'],'current_entry_point':'run_verification.py','current_runner_changes':'Reject optimized interpreters; launch unchanged checkers with -E -B. Archived source-package executions remain genuine historical evidence.'}
(K/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
with (K/'README.md').open('a') as f:
    f.write('\n## Historical runner custody\n\n')
    f.write('`execution/historical_run_verification.py` is the exact source operator whose SHA-256 appears in the archived `execution/EXECUTIONS.json`. It is retained as historical evidence and is not the current entry point. The current `run_verification.py` adds rejection of optimized interpreters and launches the unchanged finite checkers with `-E -B`. Thus the archived receipts are not represented as executions of the modified current runner. The provenance record pins both this historical copy and the unchanged diagnostic sources. Run the current root-level entry point in a disposable copy; do not run the historical source in place.\n')
rows=[]
def execute(label,argv,cwd):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
    (F/(label+'.stdout.bin')).write_bytes(out);(F/(label+'.stderr.bin')).write_bytes(err)
    rows.append({'label':label,'argv':argv,'cwd':str(cwd),'started_utc':start,'actual_child_pid':p.pid,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    (F/'EXECUTIONS.json').write_text(json.dumps(rows,indent=2)+'\n')
    if p.returncode:raise RuntimeError('Command failed: '+label)
execute('create_manifest',[sys.executable,'-E','-B',str(K/'manifest.py'),'--create'],K)
execute('verify_manifest',[sys.executable,'-E','-B',str(K/'manifest.py'),'--verify'],K)
archive=K/'blaschke-bloch-verification-v1.zip'
if archive.read_bytes()!=(F/'before/blaschke-bloch-verification-v1.zip').read_bytes():raise RuntimeError('Old archive drift')
archive.unlink()
members=sorted(p for p in K.rglob('*') if p.is_file() and p.name!='note.pdf')
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in members:
        info=zipfile.ZipInfo(str(p.relative_to(K)),(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None or z.namelist()!=[str(p.relative_to(K)) for p in members]:raise RuntimeError('Archive inventory failure')
    for p in members:
        if z.read(str(p.relative_to(K)))!=p.read_bytes():raise RuntimeError('Archive byte failure')
    copy=F/'disposable_replay';z.extractall(copy)
execute('verify_archive',[sys.executable,'-E','-B',str(copy/'manifest.py'),'--verify'],copy)
execute('replay_current_runner',[sys.executable,'-E','-B',str(copy/'run_verification.py')],copy)
if {n:sha(K/n) for n in math_before}!=math_before:raise RuntimeError('Mathematical/source/metadata/receipt drift')
pins=[{'path':str(p.relative_to(K)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(K.rglob('*')) if p.is_file()]
result={'status':'HISTORICAL_HARNESS_TRACEABILITY_REPAIR_PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_writer_pid':os.getpid(),'mathematics_PDF_metadata_frozen_sources_and_historical_receipts_unchanged':True,'historical_harness_sha256':receipt['harness_sha256'],'archive_member_count':len(members),'package_files':pins,'priority_clearance':False,'publication_authorized':False,'PR65_publication_or_merge':False,'scope':'Supporting-evidence traceability repair; no new proof or substantive proof-search turn.'}
(F/'REPAIR_READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='package_files'},indent=2))
