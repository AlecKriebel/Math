#!/usr/bin/env python3
"""Independent complete-artifact and operational preflight; writes only own cache."""
import ast
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
PUB = AUDIT / 'publication'
CACHE = HERE / '.cache'
EXTRACTED = CACHE / 'archive/zero_filling_verification'
PROFILE = '(version 1) (allow default) (deny network*)'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(args, cwd=None, env=None):
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    return {'args': [str(x) for x in args], 'exit': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in sorted(root.rglob('*')) if p.is_file()}


def clone_tree(destination):
    """Reconstruct precisely the producer's explicit inputs, never copy caches."""
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for source in PUB.iterdir():
        if source.is_file():
            target = destination / 'publication' / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
    # Every archive member maps back to an explicit input of this producer.
    for source in EXTRACTED.rglob('*'):
        if not source.is_file():
            continue
        rel = source.relative_to(EXTRACTED)
        if rel.parts[0] in ('original', 'reviews', 'root_reproduction') or len(rel.parts) == 1:
            target = destination / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())


def reseal_outer(root):
    path = root / 'MANIFEST.json'
    manifest = json.loads(path.read_text())
    manifest['files'] = {p.relative_to(root).as_posix():
                         {'bytes': len(p.read_bytes()), 'sha256': sha(p.read_bytes())}
                         for p in root.rglob('*') if p.is_file() and p != path}
    path.write_text(json.dumps(manifest, indent=2)+'\n')


def altered_copy(label, mutate, expected):
    target = CACHE / 'tamper' / label
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(EXTRACTED, target)
    mutate(target)
    result = run(['/usr/bin/sandbox-exec', '-p', PROFILE,
                  sys.executable, '-B', str(target/'run_all.py')])
    if result['exit'] == 0 or expected not in result['stderr']:
        raise AssertionError((label, expected, result))
    return {'label': label, 'expected_diagnostic': expected,
            'exit': result['exit'], 'stderr': result['stderr']}


def main():
    CACHE.mkdir(exist_ok=True)
    results = {}
    archive = PUB / 'verification_package.zip'
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == 104
        assert all(n.startswith('zero_filling_verification/') for n in names)
        assert all(not any(part in ('.cache','sources','scratch','qa','.secrets')
                           or '.private' in part for part in Path(n).parts) for n in names)
        assert not any(n.endswith(('.pdf','.png','.jpg','.log','.aux','.synctex.gz')) for n in names)
        z.extractall(CACHE/'archive')
    manifest = json.loads((EXTRACTED/'MANIFEST.json').read_text())
    payloads = {p.relative_to(EXTRACTED).as_posix(): p.read_bytes()
                for p in EXTRACTED.rglob('*') if p.is_file()}
    assert set(payloads) == set(manifest['files']) | {'MANIFEST.json'}
    assert len(manifest['files']) == 103
    for name, record in manifest['files'].items():
        assert len(payloads[name]) == record['bytes']
        assert sha(payloads[name]) == record['sha256']
    assert payloads['zero_filling.tex'] == (PUB/'zero_filling.tex').read_bytes()
    assert json.loads(payloads['metadata.json']) == json.loads((PUB/'zenodo-deposit.json').read_text())
    sys.path.insert(0, str(EXTRACTED))
    integrity = load('reviewed_integrity', EXTRACTED/'integrity.py')
    registry = json.loads(payloads['SEALS.json'])
    assert manifest['nested_seals'] == registry
    assert integrity.verify_nested(payloads, registry) == (90,22)
    snapshot = json.loads(payloads['ORIGINAL_SNAPSHOT.json'])
    git = []
    for item in snapshot['files']:
        p = subprocess.run(['git','show',snapshot['head']+':'+item['path']],
                           capture_output=True)
        assert p.returncode == 0
        b = payloads['original/'+item['path']]
        assert p.stdout == b
        git.append({'path':item['path'],'bytes':len(b),'sha256':sha(b),'git_blob_equal':True})
    results['artifact_inventory'] = {
        'zip_bytes':archive.stat().st_size,'zip_sha256':sha(archive.read_bytes()),
        'members':len(names),'outer_payloads':103,'nested_seals':10,'nested_entries':90,
        'all_payloads_read': [{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payloads.items())],
        'all22_original_git_blobs_exact':git,
        'metadata_matches_archive':True,'raw_pdf_ocr_cache_account_files_found':False}
    probe = run(['/usr/bin/sandbox-exec','-p',PROFILE,sys.executable,'-B','-c',
                 'import socket; s=socket.socket(); s.connect(("127.0.0.1",9))'])
    assert probe['exit'] != 0 and 'Operation not permitted' in probe['stderr']
    results['network_denial_probe'] = probe
    before = inventory(EXTRACTED)
    replay = run(['/usr/bin/sandbox-exec','-p',PROFILE,sys.executable,'-B',str(EXTRACTED/'run_all.py')])
    assert replay['exit'] == 0, replay
    lines = [json.loads(s) for s in replay['stdout'].splitlines()]
    assert len(lines) == 8 and lines[-1]['replayed_jobs'] == 7
    assert all(x.get('normalized_fields') == [] for x in lines[:-1])
    assert before == inventory(EXTRACTED)
    results['all_seven_actual_jobs_os_network_denied'] = replay
    rebuilds = []
    for external in ('ordinary','.cache','scratch'):
        root = CACHE/'relocated'/external/'audit'
        clone_tree(root)
        before_originals = inventory(root/'original')
        r = run([sys.executable,'-B',str(root/'publication/make_package.py')])
        assert r['exit'] == 0, r
        rebuilt = root/'publication/verification_package.zip'
        assert rebuilt.read_bytes() == archive.read_bytes()
        assert inventory(root/'original') == before_originals
        rebuilds.append({'external_ancestor':external,'exact_zip':True,
                         'bytes':rebuilt.stat().st_size,'sha256':sha(rebuilt.read_bytes()),'stdout':r['stdout']})
    results['relocated_producer_rebuilds'] = rebuilds
    # Execute the producer's *actual* local add function, extracted without edits.
    producer = ast.parse((PUB/'make_package.py').read_text())
    mainfn = next(n for n in producer.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    addfn = next(n for n in mainfn.body if isinstance(n,ast.FunctionDef) and n.name=='add')
    testroot = CACHE/'add_guards/audit'
    if testroot.exists():
        shutil.rmtree(testroot)
    testroot.mkdir(parents=True,exist_ok=True)
    (testroot/'allowed').mkdir(exist_ok=True)
    good = testroot/'allowed/good.md'; good.write_text('authored benign fixture\n')
    (testroot/'sources').mkdir(exist_ok=True)
    (testroot/'sources/paper.txt').write_text('synthetic source-like fixture\n')
    namespace={'safe_path':integrity.safe_path,'AUDIT':testroot,'files':{}}
    exec(compile(ast.Module(body=[addfn],type_ignores=[]),'actual_make_package_add','exec'),namespace)
    add=namespace['add']; guards=[]
    def reject(label,name,path):
        namespace['files']={}
        try:
            add(name,path)
        except (RuntimeError,ValueError) as e:
            guards.append({'label':label,'rejected':True,'diagnostic':str(e)})
        else:
            raise AssertionError(('guard accepted',label,name,str(path)))
    for component in ('.cache','sources','scratch','qa','.secrets'):
        folder=testroot/component; folder.mkdir(exist_ok=True)
        bad=folder/'bad.md'; bad.write_text('benign fixture\n')
        reject('lexical_'+component,'neutral.md',bad)
        reject('archive_'+component,component+'/bad.md',good)
        alias=testroot/('alias_'+component.replace('.',''))
        alias.symlink_to(folder,target_is_directory=True)
        reject('resolved_'+component,'neutral.md',alias/'bad.md')
    for name in ('../bad.md','/absolute.md','a/../bad.md','a//bad.md','./bad.md','a\\bad.md','a:bad.md',''):
        reject('malformed_archive_'+repr(name),name,good)
    reject('private_archive','user.private.md',good)
    private=testroot/'user.private.md'; private.write_text('benign\n')
    reject('private_source','neutral.md',private)
    outside=testroot.parent/'outside.md'; outside.write_text('benign\n')
    reject('lexical_escape','neutral.md',outside)
    aliasout=testroot/'alias_out'; aliasout.symlink_to(testroot.parent,target_is_directory=True)
    reject('resolved_escape','neutral.md',aliasout/'outside.md')
    symlink=testroot/'leaf.md';symlink.symlink_to(good)
    reject('leaf_symlink','neutral.md',symlink)
    namespace['files']={};add('good.md',good)
    try:
        add('good.md',good)
    except RuntimeError as e:
        guards.append({'label':'duplicate_archive','rejected':True,'diagnostic':str(e)})
    else:
        raise AssertionError('duplicate accepted')
    results['actual_producer_add_guards']=guards
    # Real current driver failures, with outer re-sealing to reach deeper gates.
    failures=[]
    def addextra(root): (root/'extra.md').write_text('extra\n')
    failures.append(altered_copy('outer_extra',addextra,'Outer payload inventory mismatch'))
    def change_current(root): (root/'zero_filling.tex').write_text('changed\n')
    failures.append(altered_copy('outer_changed',change_current,'Outer payload mismatch'))
    def nested(root):
        p=root/'reviews/topology01/REPORT.md';p.write_bytes(p.read_bytes()+b'\nbenign changed text\n');reseal_outer(root)
    failures.append(altered_copy('nested_resealed_outer',nested,'Nested hash mismatch'))
    def oldfile(root):
        p=root/'original/unsolved_math_prioritization/attempts/30004404/verify_release.py';p.write_bytes(p.read_bytes()+b'\n# benign mutation\n');reseal_outer(root)
    failures.append(altered_copy('original_resealed_outer',oldfile,'Original size differs'))
    def snapshot(root):
        p=root/'ORIGINAL_SNAPSHOT.json';d=json.loads(p.read_text());d['captured_at']='synthetic';p.write_text(json.dumps(d,indent=2)+'\n');reseal_outer(root)
    failures.append(altered_copy('snapshot_resealed_outer',snapshot,'Original snapshot binding differs'))
    for filename in ('source.pdf','imported_corpus.txt'):
        def manifested(root,filename=filename):
            prefix=root/'original/unsolved_math_prioritization/attempts/30004404'
            extra=prefix/filename;extra.write_text('synthetic source-like sentinel only\n')
            p=prefix/'RELEASE_MANIFEST.json';d=json.loads(p.read_text());d['files'].append({'path':filename,'bytes':extra.stat().st_size,'sha256':sha(extra.read_bytes())});p.write_text(json.dumps(d,indent=2)+'\n');reseal_outer(root)
        failures.append(altered_copy('R1_manifested_'+filename,manifested,'Original inventory differs'))
    def original_with_resealed_snapshot(root):
        p=root/'original/unsolved_math_prioritization/attempts/30004404/verify_release.py';p.write_bytes(p.read_bytes()+b'\n# benign mutation\n')
        s=root/'ORIGINAL_SNAPSHOT.json';d=json.loads(s.read_text());r=next(x for x in d['files'] if x['path'].endswith('/verify_release.py'));r['size']=p.stat().st_size;r['sha256']=sha(p.read_bytes());s.write_text(json.dumps(d,indent=2)+'\n');reseal_outer(root)
    failures.append(altered_copy('R1_changed_original_resealed_snapshot',original_with_resealed_snapshot,'Original snapshot binding differs'))
    results['real_driver_tamper_rejections']=failures
    optimized=run([sys.executable,'-O','-B',str(EXTRACTED/'run_all.py')])
    assert optimized['exit'] != 0 and 'assertions enabled' in optimized['stderr']
    results['optimization_rejected']=optimized
    assert inventory(EXTRACTED)==before
    (HERE/'CONTROLS_RESULT.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'status':'PASS','outer_payloads':103,'nested_entries':90,
                      'originals22_git_exact':True,'os_network_denied_jobs':7,
                      'relocated_exact_zip_rebuilds':len(rebuilds),
                      'actual_add_guard_rejections':len(guards),
                      'real_driver_tamper_rejections':len(failures)}))


if __name__=='__main__':
    main()
