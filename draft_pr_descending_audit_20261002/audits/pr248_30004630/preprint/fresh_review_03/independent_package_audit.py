from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,zipfile

HERE=Path(__file__).resolve().parent
PRE=HERE.parent
INITIAL=PRE.parent/'initial_review_20261013'
REPO=Path('/Users/alec/Documents/Math')
HEAD='e9c5d10978764db2cf25fa7d49cf4bd14a82d604'
def digest(data): return hashlib.sha256(data).hexdigest()
def pin(path):
    data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':digest(data)}
def normalized(x): return {k:v for k,v in x.items() if k not in {'utc','python'}}
candidate=json.loads((PRE/'FROZEN_CANDIDATE.json').read_text())
verified=[]
for p in candidate['files']:
    q=pin(PRE/p['path'])
    assert q['bytes']==p['bytes'] and q['sha256']==p['sha256']
    verified.append(p)
package=HERE/'private_work'/'extracted_archive'
if package.exists(): shutil.rmtree(package)
package.mkdir(parents=True)
with zipfile.ZipFile(PRE/'output/critical_wave_verification.zip') as z:
    infos=z.infolist()
    assert all(not i.is_dir() for i in infos)
    assert len({i.filename for i in infos})==len(infos)
    for i in infos:
        target=package/i.filename
        assert target.resolve().is_relative_to(package.resolve())
    z.extractall(package)
files=sorted(p for p in package.rglob('*') if p.is_file())
assert len(files)==113
manifest=json.loads((package/'FILE_MANIFEST.json').read_text())
assert len(manifest['files'])==112
assert {p.relative_to(package).as_posix() for p in files}=={x['path'] for x in manifest['files']}|{'FILE_MANIFEST.json'}
for p in manifest['files']:
    q=pin(package/p['path'])
    assert q['bytes']==p['bytes'] and q['sha256']==p['sha256'],p
assert (package/'manuscript/critical_wave_growth.tex').read_bytes()==(PRE/'critical_wave_growth.tex').read_bytes()
meta=json.loads((PRE/'metadata.json').read_text())
assert json.loads((PRE/'deposit.json').read_text())['metadata']==meta
assert json.loads((package/'metadata.json').read_text())==meta
specs=json.loads((package/'CHECKSETS.json').read_text())
assert len(specs)==7
replays=[]
for spec in specs:
    work=HERE/'private_work'/'isolated_checkers'/spec['name']
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    script=package/spec['script']
    copied=work/script.name
    shutil.copyfile(script,copied)
    run=subprocess.run([sys.executable,str(copied)],cwd=work,capture_output=True,text=True,timeout=120)
    (work/'stdout.txt').write_text(run.stdout)
    (work/'stderr.txt').write_text(run.stderr)
    assert run.returncode==0,(spec['name'],run.stderr)
    stdout=json.loads(run.stdout)
    actual=json.loads((work/spec['emitted_receipt']).read_text()) if spec['emitted_receipt'] else stdout
    reference=json.loads((package/spec['reference']).read_text())
    assert normalized(actual)==normalized(reference),spec['name']
    if spec['emitted_receipt'] and 'sha256' in stdout:
        assert stdout['sha256']==digest((work/spec['emitted_receipt']).read_bytes())
    replays.append({'name':spec['name'],'returncode':run.returncode,'complete_receipt_match':True,'receipt':actual,'stdout':stdout,'stderr':run.stderr})
portable=HERE/'private_work'/'portable_runner'
portable.mkdir(exist_ok=True)
run=subprocess.run([sys.executable,str(package/'verify_all.py')],cwd=portable,capture_output=True,text=True,timeout=240)
assert run.returncode==0,run.stderr
portable_report=json.loads((portable/'VERIFICATION_RUN.json').read_text())
assert portable_report['status']=='PASS' and portable_report['checksets']==7
prefix='unsolved_math_prioritization/attempts/30004630/'
listing=subprocess.run(['git','ls-tree','-r','--name-only',HEAD,'--',prefix],cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines()
assert len(listing)==19
original=[]
for full in listing:
    relative=full.removeprefix(prefix)
    git_data=subprocess.run(['git','show',HEAD+':'+full],cwd=REPO,capture_output=True,check=True).stdout
    archive_data=(package/'original_submission'/relative).read_bytes()
    disk_data=(INITIAL/'submitted'/full).read_bytes()
    assert git_data==archive_data==disk_data
    oid=subprocess.run(['git','rev-parse',HEAD+':'+full],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()
    original.append({'path':relative,'git_blob_oid':oid,'bytes':len(git_data),'sha256':digest(git_data)})
def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values(): yield from walk(v)
    elif isinstance(x,list):
        for v in x: yield from walk(v)
nested=[]
for manifest_path in files:
    if manifest_path.suffix!='.json' or manifest_path.name=='FILE_MANIFEST.json': continue
    doc=json.loads(manifest_path.read_text())
    for item in walk(doc):
        name=item.get('path',item.get('relative_path',item.get('name')))
        sha=item.get('sha256')
        if not isinstance(name,str) or not isinstance(sha,str) or len(sha)!=64: continue
        choices=[manifest_path.parent/name,package/name,REPO/name,INITIAL/name]
        if manifest_path.parent.name=='historical_snapshot_01': choices.append(manifest_path.parent.parent/name)
        # Archive relocation retains originals in their corresponding audit family.
        rel=manifest_path.relative_to(package)
        if rel.parts[0]=='audits': choices.extend([INITIAL/Path(*rel.parts[1:-1])/name])
        if rel.parts[0]=='original_submission': choices.append(INITIAL/'submitted'/prefix/name)
        matches=[]
        for q in choices:
            if q.is_file() and digest(q.read_bytes())==sha and ('bytes' not in item or len(q.read_bytes())==item['bytes']): matches.append(str(q))
        if not matches:
            # Private primary paths in copied source manifests may be relative to a different
            # historical directory; locate an exact-byte original within this effort only.
            for q in INITIAL.rglob(Path(name).name):
                if q.is_file() and digest(q.read_bytes())==sha and ('bytes' not in item or len(q.read_bytes())==item['bytes']): matches.append(str(q))
        if not matches and 'bytes' in item:
            # Preserved as-read snapshots are sometimes renamed. Require exact length/hash.
            for q in INITIAL.rglob('*'):
                if q.is_file() and q.stat().st_size==item['bytes'] and digest(q.read_bytes())==sha:
                    matches.append(str(q))
        assert matches,(str(manifest_path.relative_to(package)),name,sha)
        nested.append({'manifest':str(manifest_path.relative_to(package)),'bound_path':name,'sha256':sha,'verified_against':matches[0]})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','candidate_pins':verified,'archive_files':len(files),'top_level_pins':len(manifest['files']),'metadata_equal':True,'independent_checksets':replays,'portable_result':json.loads(run.stdout) if False else {'status':portable_report['status'],'checksets':portable_report['checksets'],'exact_assertions':portable_report['exact_assertions'],'noncertified_diagnostics':portable_report['noncertified_diagnostics']},'original_git_head':HEAD,'original_files':original,'nested_pin_checks':nested,'limitations':'Finite assertions are algebra/control checks, not PDE discretization, certified PDE constants or priority proof. Private source files were checked locally and are not redistributed.'}
(HERE/'PACKAGE_REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','archive_files':len(files),'top_level_pins':len(manifest['files']),'original_git_files':len(original),'nested_pin_checks':len(nested),'seven_complete_receipts_match':True,'portable_runner':'PASS'},indent=2))
