#!/usr/bin/env python3
"""Read-only frozen-source replay, hash verification, and authored-control runner."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'source_snapshot/unsolved_math_prioritization/attempts/30000999'
DIAG = OWN / 'diagnostics'


def hashes(data):
    blob = b'blob '+str(len(data)).encode()+b'\0'+data
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob_sha':hashlib.sha1(blob).hexdigest()}


def frozen_inventory():
    return {str(p.relative_to(SOURCE)):hashes(p.read_bytes()) for p in sorted(SOURCE.rglob('*')) if p.is_file()}


def execute(label, script, optimized=False, extra=(), expected=None, expected_failure=False):
    argv = [sys.executable,'-B']+(['-O'] if optimized else [])+[str(script)]+list(extra)
    proc = subprocess.run(argv,cwd=OWN,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
    stdout_name = label+'.stdout.json' if not expected_failure else label+'.stdout.txt'
    (DIAG/stdout_name).write_bytes(proc.stdout)
    stderr_name = label+'.stderr.txt'
    (DIAG/stderr_name).write_bytes(proc.stderr)
    result = {'label':label,'optimized':optimized,'exit_code':proc.returncode,
              'stdout':stdout_name,'stderr':stderr_name,
              'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest()}
    if expected_failure:
        result['expected_failure_observed'] = proc.returncode != 0 and b'InvalidClaim:' in proc.stderr
        if not result['expected_failure_observed']:
            raise RuntimeError('falsification run did not reject: '+label)
        return result
    if proc.returncode != 0:
        raise RuntimeError('checker failed: '+label)
    value = json.loads(proc.stdout)
    result['status'] = value.get('status')
    if expected:
        expected_bytes = expected.read_bytes()
        result['expected_frozen_file'] = str(expected.relative_to(SOURCE))
        result['expected_json_equal'] = value == json.loads(expected_bytes)
        result['expected_bytes_equal'] = proc.stdout == expected_bytes
        if not result['expected_json_equal']:
            raise RuntimeError('checker expected output differs: '+label)
    return result


def main():
    DIAG.mkdir(exist_ok=True)
    before = frozen_inventory()
    (DIAG/'source_inventory_before.json').write_text(json.dumps(before,indent=2,sort_keys=True)+'\n')
    manifest_results = []
    manifests = [SOURCE/'PUBLICATION_MANIFEST.json', SOURCE/'release/FROZEN_AUTHOR_MANIFEST.json',
                 SOURCE/'independent_audit/AUDIT_MANIFEST.json']
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text())
        for relative,expected in manifest['files'].items():
            target = manifest_path.parent/relative
            actual = hashes(target.read_bytes())
            fields = [key for key in ('bytes','sha256','git_blob_sha') if key in expected]
            matches = {key:actual[key] == expected[key] for key in fields}
            manifest_results.append({'manifest':str(manifest_path.relative_to(SOURCE)),
                                     'target':str(target.relative_to(SOURCE)),'matches':matches})
            if not all(matches.values()):
                raise RuntimeError('manifest mismatch: '+str(target))
        if 'author_manifest_sha256' in manifest:
            target = SOURCE/'release/FROZEN_AUTHOR_MANIFEST.json'
            actual = hashes(target.read_bytes())['sha256']
            ok = actual == manifest['author_manifest_sha256']
            manifest_results.append({'manifest':str(manifest_path.relative_to(SOURCE)),
                                     'reference':'author_manifest_sha256','matches':{'sha256':ok}})
            if not ok:
                raise RuntimeError('author manifest reference mismatch')
    (DIAG/'manifest_verification.json').write_text(json.dumps(manifest_results,indent=2,sort_keys=True)+'\n')
    runs=[]
    for tag,relative,expected in [
        ('original_author','release/check_exact.py','release/exact_results.json'),
        ('original_historical_audit','independent_audit/independent_exact.py','independent_audit/independent_exact_results.json')]:
        for optimized in (False,True):
            label=tag+('_optimized' if optimized else '_normal')
            runs.append(execute(label,SOURCE/relative,optimized,expected=SOURCE/expected))
    for optimized in (False,True):
        label='authored_wick'+('_optimized' if optimized else '_normal')
        runs.append(execute(label,OWN/'wick_controls.py',optimized))
    controls = ['hermitian_projection','equator_dimension','radial_beta_parameter',
                'ambient_gradient_energy','ratio_exponent','gamma_shift','reversed_flow',
                'circle_decay','dimension_one']
    for control in controls:
        for optimized in (False,True):
            label='reject_'+control+('_optimized' if optimized else '_normal')
            runs.append(execute(label,OWN/'wick_controls.py',optimized,
                                extra=('--false-alternative',control),expected_failure=True))
    before_normal = (DIAG/'authored_wick_normal.stdout.json').read_bytes()
    before_optimized = (DIAG/'authored_wick_optimized.stdout.json').read_bytes()
    if before_normal != before_optimized:
        raise RuntimeError('authored checker changes under optimization')
    after = frozen_inventory()
    (DIAG/'source_inventory_after.json').write_text(json.dumps(after,indent=2,sort_keys=True)+'\n')
    if before != after:
        raise RuntimeError('frozen source changed')
    summary={'status':'PASS','frozen_source_files':len(before),'frozen_source_unchanged':before==after,
             'manifest_reference_records':len(manifest_results),'all_manifest_references_valid':True,
             'normal_and_optimized_authored_outputs_identical':True,'runs':runs,
             'limitations':['Original check counts are finite evidence only.',
                            'Successful replay is not a proof or an endorsement of historical verdicts.',
                            'No numerical optimal transport calculation is used.']}
    (DIAG/'reproduction_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps({key:value for key,value in summary.items() if key!='runs'},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
