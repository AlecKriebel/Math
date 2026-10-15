from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, zipfile, shutil, os, ast

HERE=Path(__file__).resolve().parent
PRE=HERE.parent
REPO=PRE.parents[3]
TEMP=HERE/'private_tmp';TEMP.mkdir(exist_ok=True)
os.environ['TMPDIR']=str(TEMP)
SHA='e9c5d10978764db2cf25fa7d49cf4bd14a82d604'
NATIVE='unsolved_math_prioritization/attempts/30004630/'
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(n,v):
    (HERE/n).write_text(json.dumps(v,indent=2)+'\n')
freeze=json.loads((PRE/'FROZEN_CANDIDATE.json').read_text())
candidate=[]
for p in freeze['files']:
    q=pin(PRE/p['path'])
    assert q['bytes']==p['bytes'] and q['sha256']==p['sha256']
    candidate.append(q)
dump('INITIAL_INPUT_PINS.json',{'utc':datetime.now(timezone.utc).isoformat(),'frozen_manifest':pin(PRE/'FROZEN_CANDIDATE.json'),'files':candidate})
ROOT=HERE/'extracted_archive'
ROOT.mkdir(exist_ok=True)
with zipfile.ZipFile(PRE/'output/critical_wave_verification.zip') as z:
    members=z.infolist()
    assert len(members)==113 and len({i.filename for i in members})==113
    assert z.testzip() is None
    for i in members:
        rel=PurePosixPath(i.filename)
        assert not rel.is_absolute() and '..' not in rel.parts and not i.is_dir()
        assert (i.external_attr>>16)&0o170000!=0o120000
    z.extractall(ROOT)
manifest=json.loads((ROOT/'FILE_MANIFEST.json').read_text())
assert len(manifest['files'])==112
assert set(p['path'] for p in manifest['files'])=={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}-{'FILE_MANIFEST.json'}
payload=[]
for p in manifest['files']:
    q=pin(ROOT/p['path'])
    assert q['bytes']==p['bytes'] and q['sha256']==p['sha256']
    payload.append({'path':p['path'],'bytes':q['bytes'],'sha256':q['sha256'],'match':True})
assert (ROOT/'manuscript/critical_wave_growth.tex').read_bytes()==(PRE/'critical_wave_growth.tex').read_bytes()
assert (ROOT/'metadata.json').read_bytes()==(PRE/'metadata.json').read_bytes()
archive_names={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
candidate_package=PRE/'verification_package'
assert archive_names=={p.relative_to(candidate_package).as_posix() for p in candidate_package.rglob('*') if p.is_file()}
for name in archive_names:assert (ROOT/name).read_bytes()==(candidate_package/name).read_bytes()
meta=json.loads((PRE/'metadata.json').read_text());dep=json.loads((PRE/'deposit.json').read_text())
assert meta==dep['metadata']
assert dep['files']==[{'path':'output/pdf/critical_wave_growth.pdf'},{'path':'output/critical_wave_verification.zip'}]
native=[]
listing=subprocess.check_output(['git','ls-tree','-r','--name-only',SHA,'--',NATIVE],cwd=REPO).decode().splitlines()
assert len(listing)==19
for name in listing:
    b=subprocess.check_output(['git','show',SHA+':'+name],cwd=REPO)
    rel=name[len(NATIVE):]
    a=(ROOT/'original_submission'/rel).read_bytes()
    assert a==b
    native.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'native_commit_match':True})
assert len(list((ROOT/'original_submission').rglob('*')))>19
dump('PACKAGE_PIN_AUDIT.json',{'utc':datetime.now(timezone.utc).isoformat(),'archive_entries':113,'payload_pins':payload,'native_head':SHA,'native_files':native,'exact_manuscript_bytes':True,'exact_metadata_bytes':True,'deposit_metadata_equal':True,'archive_equals_candidate_package':True,'zip_crc_integrity':True})

def normalize(r):
    return {k:v for k,v in r.items() if k not in ('utc','python')}
sentinel={'utc':'x','python':'y','sympy':'1.14.0','scientific':{'utc':'nested-scientific','python':'nested-scientific'},'count':7}
tree=ast.parse((ROOT/'verify_all.py').read_text())
func=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='normalize')
module=ast.Module(body=[func],type_ignores=[]);namespace={}
exec(compile(ast.fix_missing_locations(module),'packaged_normalize','exec'),namespace)
packaged_normalize=namespace['normalize']
assert packaged_normalize(sentinel)==normalize(sentinel)
assert packaged_normalize({**sentinel,'count':8})!=packaged_normalize(sentinel)
assert packaged_normalize({**sentinel,'sympy':'other'})!=packaged_normalize(sentinel)
assert packaged_normalize({**sentinel,'scientific':{'utc':'changed','python':'nested-scientific'}})!=packaged_normalize(sentinel)
assert normalize(sentinel)=={'sympy':'1.14.0','scientific':{'utc':'nested-scientific','python':'nested-scientific'},'count':7}
assert normalize({**sentinel,'count':8})!=normalize(sentinel)
assert normalize({**sentinel,'sympy':'other'})!=normalize(sentinel)
assert normalize({**sentinel,'scientific':{'utc':'changed','python':'nested-scientific'}})!=normalize(sentinel)
specs=json.loads((ROOT/'CHECKSETS.json').read_text())
assert len(specs)==7
receipts=[];total=0;diagnostics=0
for spec in specs:
    work=HERE/'independent_replays'/spec['name'];work.mkdir(parents=True,exist_ok=True)
    script=ROOT/spec['script'];dest=work/script.name;shutil.copyfile(script,dest)
    run=subprocess.run([sys.executable,str(dest)],cwd=work,capture_output=True,text=True,timeout=120)
    (work/'stdout.txt').write_text(run.stdout);(work/'stderr.txt').write_text(run.stderr)
    assert run.returncode==0,(spec['name'],run.stderr)
    expected=json.loads((ROOT/spec['reference']).read_text())
    actual=json.loads((work/spec['emitted_receipt']).read_text()) if spec['emitted_receipt'] else json.loads(run.stdout)
    assert normalize(actual)==normalize(expected),(spec['name'],'complete receipt changed')
    (work/'ACTUAL_RECEIPT.json').write_text(json.dumps(actual,indent=2)+'\n')
    stdout=json.loads(run.stdout)
    if spec['emitted_receipt'] and 'sha256' in stdout:
        assert stdout['sha256']==hashlib.sha256((work/spec['emitted_receipt']).read_bytes()).hexdigest()
    count=actual.get('exact_assertions',actual.get('exact_checks',actual.get('assertions')))
    diag=actual.get('categories',{}).get('threshold_high_precision_sanity',0)
    if 'categories' in actual: assert sum(actual['categories'].values())==count
    if 'families' in actual: assert sum(actual['families'].values())==count
    if diag: assert len(actual['diagnostic_samples'])==diag
    total+=count-diag;diagnostics+=diag
    receipts.append({'name':spec['name'],'complete_receipt_equal':True,'exact_assertions':count-diag,'diagnostics':diag,'actual_receipt':pin(work/'ACTUAL_RECEIPT.json'),'returncode':run.returncode,'stderr':run.stderr})
assert total==5603 and diagnostics==5
portable=HERE/'portable_runner';portable.mkdir(exist_ok=True)
run=subprocess.run([sys.executable,str(ROOT/'verify_all.py')],cwd=portable,capture_output=True,text=True,timeout=240)
(portable/'stdout.txt').write_text(run.stdout);(portable/'stderr.txt').write_text(run.stderr)
assert run.returncode==0,run.stderr
runner=json.loads((portable/'VERIFICATION_RUN.json').read_text())
assert runner['status']=='PASS' and runner['packaged_files_verified']==112 and runner['checksets']==7
assert runner['exact_assertions']==total and runner['noncertified_diagnostics']==diagnostics
for record in runner['results']:
    expected=json.loads((ROOT/next(s['reference'] for s in specs if s['name']==record['checkset'])).read_text())
    assert normalize(record['receipt'])==normalize(expected)
dump('INDEPENDENT_REPLAY_AUDIT.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','python':sys.version,'independently_derived_exact_total':total,'independently_derived_noncertified_diagnostics':diagnostics,'checksets':receipts,'portable_runner_passed':True,'normalization':'only top-level utc/python removed; dependency/scientific/nested fields retained','normalization_negative_controls':4,'limits':'Finite algebra and control receipts only; no nonlinear PDE, unknown analytic constant, or exhaustive historical priority certification.'})
for p in freeze['files']:
    q=pin(PRE/p['path']);assert q['sha256']==p['sha256'] and q['bytes']==p['bytes']
print(json.dumps({'status':'PASS','entries':113,'payload_pins':112,'native_files':19,'independent_checksets':7,'portable_runner_checksets':7,'exact_assertions':total,'diagnostics':diagnostics},indent=2))
