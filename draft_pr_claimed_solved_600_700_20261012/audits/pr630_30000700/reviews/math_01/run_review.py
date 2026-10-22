#!/usr/bin/env python3
"""Bind immutable inputs and replay mathematical controls without mutating them."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
REPO = Path('/Users/alec/Documents/Math')
PYTHON = '/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python'
HEAD = '810cd5c148bbae7c7c5a47423c375ada98e903b6'


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def main():
    scope_path = AUDIT/'SCOPE_AND_SNAPSHOT.json'
    scope_data = scope_path.read_bytes()
    scope = json.loads(scope_data)
    require(scope['original_head'] == HEAD, 'wrong pinned head')
    bindings = []
    for name, expected in scope['original_blobs'].items():
        path = AUDIT/'native'/name
        require(path.is_file() and not path.is_symlink(), 'native file or symlink: '+name)
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(len(data) == expected['size'] and digest(data) == expected['sha256']
                and blob == expected['git_blob'], 'scope digest: '+name)
        original = subprocess.run(['git','cat-file','blob',HEAD+':'+name],cwd=REPO,
                                  check=True,capture_output=True).stdout
        require(original == data, 'commit bytes differ: '+name)
        bindings.append({'path':name,'bytes':len(data),'sha256':digest(data),
                         'git_blob':blob,'pinned_commit_bytes_identical':True})
    require(len(bindings) == 28, 'expected 28 original files')
    write('INPUT_BINDINGS.json',{'schema':'pr630-math-input-bindings-v1',
        'captured_utc':datetime.now(timezone.utc).isoformat(),'pinned_head':HEAD,
        'scope_snapshot_sha256':digest(scope_data),'native_root':str(AUDIT/'native'),
        'original_file_count':len(bindings),'all_files_verified':True,'files':bindings,
        'python_path_invoked_without_resolving_symlink':PYTHON,
        'independent_derivation_sha256':digest((HERE/'INDEPENDENT_DERIVATION.md').read_bytes()),
        'own_control_script_sha256':digest((HERE/'exact_controls.py').read_bytes()),
        'review_runner_sha256':digest(Path(__file__).read_bytes())})

    (HERE/'tmp').mkdir(exist_ok=True)
    (HERE/'results').mkdir(exist_ok=True)
    native = AUDIT/'native/unsolved_math_prioritization/attempts/30000700'
    env = dict(os.environ, TMPDIR=str(HERE/'tmp'), PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    jobs = [
        ('author_manifest',[],native/'safe/verify_manifest.py',[],True),
        ('audit_manifest',[],native/'audit/verify_audit.py',['--author-packet',str(native/'author-packet.zip')],True),
        ('author_controls',[],native/'safe/verify.py',[],True),
        ('old_independent_controls',[],native/'audit/independent_verify.py',[],True),
        ('release_controls',[],native/'verify_release.py',[],True),
        ('release_optimized_rejection',['-O'],native/'verify_release.py',[],False),
        ('own_controls',[],HERE/'exact_controls.py',[],True),
        ('own_controls_optimized',['-O'],HERE/'exact_controls.py',[],True),
    ]
    for optimize in [False,True]:
        for fault in ['polynomial_factorial','lambda_relation']:
            jobs.append(('own_fault_'+fault+('_optimized' if optimize else ''),
                         ['-O'] if optimize else [],HERE/'exact_controls.py',
                         ['--inject-fault',fault],False))

    def run(job):
        name,flags,script,args,success = job
        command = [PYTHON,*flags,'-B',str(script),*args]
        result = subprocess.run(command,cwd=HERE,env=env,capture_output=True,text=True,timeout=300)
        (HERE/'results'/f'{name}.stdout').write_text(result.stdout)
        (HERE/'results'/f'{name}.stderr').write_text(result.stderr)
        require((result.returncode == 0) == success, f'{name}: unexpected exit {result.returncode}: {result.stderr[-1000:]}')
        return {'name':name,'command':command,'expected_success':success,
                'exit_code':result.returncode,'status':'PASS',
                'stdout_sha256':digest(result.stdout.encode()),
                'stderr_sha256':digest(result.stderr.encode())}

    # Independent executions run concurrently; no writes to native inputs.
    with ThreadPoolExecutor(max_workers=4) as pool:
        outcomes = list(pool.map(run,jobs))
    results = {row['name']:row for row in outcomes}
    require(results['own_controls']['stdout_sha256'] == results['own_controls_optimized']['stdout_sha256'],
            'optimized independent controls differ')
    require((HERE/'results/author_controls.stdout').read_bytes() == (native/'safe/CONTROL_RESULTS.json').read_bytes(),
            'saved author controls differ')
    require((HERE/'results/old_independent_controls.stdout').read_bytes() == (native/'audit/INDEPENDENT_CONTROLS.json').read_bytes(),
            'saved audit controls differ')

    # The original stand-alone scripts use Python asserts. Demonstrate why
    # the guarded release entry point is required for an optimized interpreter.
    original_script = (native/'safe/verify.py').read_text()
    changed = original_script.replace('basic=[Q(0),Q(0),Q(1,2)]','basic=[Q(0),Q(0),Q(1,3)]')
    require(changed != original_script, 'mutation did not apply')
    mutated = HERE/'tmp/author_wrong_quadratic.py'
    mutated.write_text(changed)
    normal = subprocess.run([PYTHON,'-B',str(mutated)],cwd=HERE,env=env,capture_output=True,text=True)
    optimized = subprocess.run([PYTHON,'-O','-B',str(mutated)],cwd=HERE,env=env,capture_output=True,text=True)
    require(normal.returncode != 0, 'mutated author script normal false pass')
    require(optimized.returncode == 0, 'expected assert removal behavior changed')
    (HERE/'results/author_mutation_normal.stderr').write_text(normal.stderr)
    (HERE/'results/author_mutation_optimized.stdout').write_text(optimized.stdout)
    write('TEST_RESULTS.json',{'status':'PASS','completed_utc':datetime.now(timezone.utc).isoformat(),
        'original_inputs_verified':28,'execution_count':len(outcomes),'executions':outcomes,
        'own_normal_optimized_byte_identical':True,'saved_author_controls_byte_identical':True,
        'saved_audit_controls_byte_identical':True,
        'assert_semantics_mutation':{'normal_rejected':True,'optimized_standalone_false_pass_demonstrated':True,
            'release_entry_point_rejects_optimized_python':True,
            'classification':'usage limitation already guarded by frozen release verifier; no mathematical defect'},
        'source_and_priority_checks':'outside this mathematical audit family'})


if __name__ == '__main__':
    main()
