"""MIT licensed. Own source-preparation freeze only, never ROOT custody/acceptance."""
import datetime, hashlib, json, os, pathlib, stat, sys
R=pathlib.Path(__file__).resolve().parent
if not __debug__ or sys.flags.optimize!=0:raise RuntimeError('use -E -B, no -O')
assert not (R/'SOURCE.json').exists() and not (R/'READY.md').exists()
admin=json.loads((R/'ADMIN_VERIFICATION.json').read_bytes())
assert admin['status']=='PASS_AUTHENTICATED_ORIGINAL_AND_ACTUAL_CONTROL_EVIDENCE'
assert (R/'PRESEAL_FAILURE_HISTORY.json').exists()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name in ['ROOT_verify_original.py','ROOT_close_original.py','ROOT_readback_original.py']:
    compile((R/name).read_bytes(),str(R/name),'exec')
assert 'if not __debug__' in (R/'ROOT_verify_original.py').read_text()
with (R/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'- {now} — Intake95% before final own readback: administrative child31078/controller31077 passed at19:53:10UTC. Initial captures retained; guarded564/20223 child28583/28586 passed with exact bytes. Preseal ENOSPC inspection/optional-edit failures were inspected and saved in PRESEAL_FAILURE_HISTORY.json; no partial SOURCE/READY existed then. Writes resumed; current ROOT helper guard syntax-read only. Preparing exact self-excluded index with all07777 files0444/dirs0755. Separate final own reader and future ROOT custody/decision remain distinct. No discovery/audit increment; unsolved1/5.\n')
ready='''# PR62 original SOURCE handoff conditions

2715/KP1.56: **unsolved1/5**, original substantive attempts1, new0/audit0/novelty0, no paper/DOI. Literal endpoint-isotopy question and both remarks were read in the pinned private K3 text LF2867-2893. Original17 bodies remain unchanged. Current precision is mandatory in SOURCE_PRECISION_QUALIFICATION.md: endpoint isotopy is the target, not product isotopy of a particular annulus; Boninger's page range is81-95. Original dated triage/bibliography are archived verbatim.

Head98cc2821e9376507caf2d2c57414f7c7e7719c1b; base/common merge-basec6975ca76f9f667f1250ba403d0e6da2aafe14d0. Complete GitHub scientific tree/17blob bodies and18diff paths were authenticated with full actual command streams. Raw prior ABSENT/selectednull differs from SQL TEXT `{}` through its measured missing-report default; the unsolved1/5 historical ledger is not reset. No native/Git/ref/index/PR/remote mutation.

Original564 and historical20223 finite diagnostics reproduced exact archived bytes. First successful captures have unmeasured historical optimization/debug state. Separate later exact-body guarded replays use-E-B/no-O, with actual separate same-flags optimize0/debugtrue probes; full sources, streams, PIDs and UTC are retained. These are finite algebra/logical checks, not knot Floer computations or universal geometric proof. Known imported rigidity cases are credited; the arbitrary-successor endpoint-isotopy gap remains.

Primary reading is bounded exactly by PRIMARY_READING_RECEIPT.json; inaccessible Boninger publisher-PDF and Agol DOI attempts are preserved as access limitations. No underlying imported-theorem/TQFT reconstruction, exhaustive priority, figure reading or full-publication comparison is certified. Private corpus/cache references stay external and are not part of fixed SOURCE custody. No third-party full papers or images are redistributed.

SOURCE.json is self-excluded and binds complete bytes, SHA256, full07777 modes and exact regular-file/directory topology. Only a successful separate own final reader confirms the finished freeze; its genuine capture lies outside this fixed packet within A62. Preseal ENOSPC events are recorded, including the observed unchanged helper and absent SOURCE/READY at that checkpoint. No historical seal was rewritten.

ROOT_verify_original.py, ROOT_close_original.py and ROOT_readback_original.py are unexecuted and unimported by the preparer; source/syntax was read only. Invoke under separate ROOT-owned captures with-E-B/no-O. The closer enforces an outside-packet receipt within A62. Their future use establishes custody only, and remains pending here. No ROOT scientific adjudication, native acceptance, merge, publication or DOI is inferred or created.
'''
with (R/'READY.md').open('x') as f:f.write(ready)
for p in R.rglob('*'):
    assert not p.is_symlink(),str(p)
    if p.is_file():assert p.stat().st_nlink==1;os.chmod(p,0o444)
    elif p.is_dir():os.chmod(p,0o755)
    else:raise AssertionError('special object '+str(p))
os.chmod(R,0o755)
files=[];directories=[{'path':'.','full_mode_07777':'0755'}]
for p in sorted(R.rglob('*')):
    rel=p.relative_to(R).as_posix()
    if p.is_file():
        b=p.read_bytes();s=p.stat()
        assert stat.S_IMODE(s.st_mode)==0o444 and s.st_nlink==1
        files.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode_07777':'0444','nlink':1})
    else:
        assert stat.S_IMODE(p.stat().st_mode)==0o755
        directories.append({'path':rel,'full_mode_07777':'0755'})
source={'schema':'pr62-original-self-excluded-fixed-source/v1','self_indexed':False,
    'prepared_by':'/root/analytic_convex_audit','prepared_utc':now,'preparer_actual_pid':os.getpid(),
    'packet':str(R),'problem_id':2715,'problem_number':'KP-1.56',
    'head':'98cc2821e9376507caf2d2c57414f7c7e7719c1b','base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0',
    'original_science_count':17,'diff_count':18,'status':'unsolved','original_attempts':1,'budget':5,
    'new_attempts':0,'audit_increment':0,'novelty_credit':0,'paper':False,
    'ROOT_custody':False,'ROOT_scientific_approval':False,'ROOT_helpers_executed':False,
    'external_inputs':'Dated in-place references only, outside fixed packet custody; no primary cache needed for byte/mode ROOT verification.',
    'prepared_file_count':len(files),'prepared_bytes':sum(e['bytes'] for e in files),
    'files':files,'directories':directories}
body=(json.dumps(source,sort_keys=True,indent=2)+'\n').encode()
with (R/'SOURCE.json').open('xb') as f:f.write(body)
os.chmod(R/'SOURCE.json',0o444)
assert set(e['path'] for e in files)|{'SOURCE.json'}=={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}
print(json.dumps({'status':'OWN_PREPARED_SOURCE_FREEZE_ONLY','pid':os.getpid(),
    'SOURCE_sha256':hashlib.sha256(body).hexdigest(),'SOURCE_bytes':len(body),
    'prepared_files':len(files),'total_files_with_self':len(files)+1,
    'directories':len(directories),'prepared_bytes':source['prepared_bytes'],
    'ROOT_helpers_executed':False,'ROOT_custody':False,'scientific_approval':False},sort_keys=True))
