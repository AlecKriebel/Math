#!/usr/bin/env python3
"""Isolated full replay and adversarial release-contract checks.

Writes copies/source-free outputs only below this review's ignored .cache.
Never alters the original snapshot. Run from any directory.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parents[1] / 'original/unsolved_math_prioritization/attempts/30004404'
CACHE = HERE / '.cache/reproduction'
CACHE.mkdir(parents=True,exist_ok=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): {'bytes':len(p.read_bytes()),'sha256':digest(p.read_bytes())}
            for p in sorted(root.rglob('*')) if p.is_file()}


before = inventory(ORIGINAL)
assert len(before) == 22
snapshot=json.loads((HERE.parents[1]/'ORIGINAL_SNAPSHOT.json').read_text())
prefix='unsolved_math_prioritization/attempts/30004404/'
expected_inventory={entry['path'].removeprefix(prefix):{'bytes':entry['size'],'sha256':entry['sha256']}
                    for entry in snapshot['files']}
assert before == expected_inventory
assert snapshot['head'] == 'e4b27ac757babc1aea75149ea986ed2beea438f9'
copy = CACHE / 'release'
if copy.exists():
    shutil.rmtree(copy)
shutil.copytree(ORIGINAL,copy)
assert inventory(copy) == before
runs = []


def run(script, args=(), expected=None, name=None):
    start = datetime.now(timezone.utc).isoformat()
    tick=time.monotonic()
    result = subprocess.run([sys.executable,str(copy/script),*args],cwd=copy,capture_output=True)
    label=name or Path(script).stem
    (CACHE/(label+'.stdout')).write_bytes(result.stdout)
    (CACHE/(label+'.stderr')).write_bytes(result.stderr)
    assert result.returncode == 0, (label,result.stderr.decode())
    assert result.stderr == b''
    parsed=json.loads(result.stdout)
    receipt={'label':label,'script':script,'args':list(args),'started_utc':start,
             'duration_seconds':round(time.monotonic()-tick,4),'exit_code':result.returncode,
             'stdout_bytes':len(result.stdout),'stdout_sha256':digest(result.stdout),'stderr_bytes':0,
             'full_json':parsed}
    if expected:
        expected_bytes=(copy/expected).read_bytes()
        assert result.stdout == expected_bytes
        assert parsed == json.loads(expected_bytes)
        receipt.update(expected=expected,byte_exact=True,full_json_equal=True)
    runs.append(receipt)
    return parsed


run('package/controls/check.py',expected='package/controls/expected.json',name='author')
run('audit-independent/independent_checks.py',expected='audit-independent/independent_results.json',name='old_independent')
release = run('verify_release.py',['--self-test'],name='release_self_test')
assert release['release_files_verified'] == 21
assert release['mutants_rejected'] == ['changed_proof','changed_audit','missing_expected_output','unexpected_file']

# Test the stronger safety claim separately from honest-manifest integrity.
# In each mutant all frozen child payloads and child manifests remain untouched.
mutant_results=[]
for mode in ('added_manifested_pdf','added_manifested_corpus_text','unsafe_parent_path','symlink_payload'):
    target=CACHE/mode
    if target.exists():shutil.rmtree(target)
    shutil.copytree(copy,target)
    manifest_path=target/'RELEASE_MANIFEST.json'
    manifest=json.loads(manifest_path.read_text())
    if mode in ('added_manifested_pdf','added_manifested_corpus_text'):
        # Synthetic harmless payloads; source PDFs themselves stay in private cache.
        name='source.pdf' if mode.endswith('pdf') else 'imported_corpus.txt'
        data=b'%PDF-1.7\nsynthetic excluded-payload control\n' if name.endswith('.pdf') else b'synthetic imported corpus control\n'
        (target/name).write_bytes(data)
        manifest['files'].append({'path':name,'bytes':len(data),'sha256':digest(data)})
    elif mode == 'unsafe_parent_path':
        manifest['files'].append({'path':'../outside.txt','bytes':0,'sha256':digest(b'')})
    else:
        (target/'alias').symlink_to('PUBLICATION_STATUS.md')
        data=(target/'PUBLICATION_STATUS.md').read_bytes()
        manifest['files'].append({'path':'alias','bytes':len(data),'sha256':digest(data)})
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    result=subprocess.run([sys.executable,str(target/'verify_release.py')],cwd=target,capture_output=True)
    entry={'mode':mode,'exit_code':result.returncode,'accepted':result.returncode==0,
           'stdout_sha256':digest(result.stdout),'stderr_sha256':digest(result.stderr)}
    if result.returncode==0:entry['full_json']=json.loads(result.stdout)
    else:entry['last_error']=result.stderr.decode().strip().splitlines()[-1]
    mutant_results.append(entry)
assert [x['accepted'] for x in mutant_results] == [True,True,False,False]
after=inventory(ORIGINAL)
assert after==before
report={'result':'PASS_FOR_FROZEN_REPLAY_WITH_RELEASE_CONTRACT_FINDING',
        'snapshot_head':snapshot['head'],'all_22_match_snapshot_inventory':True,
        'python_version':sys.version,'isolated_copy_identical_before_runs':True,
        'original_inventory':before,'original_file_count':len(before),'original_unchanged_after_runs':True,
        'runs':runs,'fresh_release_contract_controls':mutant_results,
        'finding':'Outer manifest extension with a prohibited source-like payload is accepted and source_files_included remains false; exact frozen inventory itself is clean.'}
print(json.dumps(report,indent=2,sort_keys=True))
