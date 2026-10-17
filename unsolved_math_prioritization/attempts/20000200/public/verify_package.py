#!/usr/bin/env python3
"""Offline integrity and exact-example replay, not a general signature solver."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ACCEPTED_REPORT = '856cf9b1560aeee8f26f1197f587e1d81838a8cb423c8c3f320be1aaa5c21ad5'
ACCEPTED_MANIFEST = '0abde8744824b2c29492f4c79ca11a8d46e736bbc13069cac40fc29583be46ec'
REQUIRED = {
    'README.md', 'CONTRACT.md', 'RESULTS_AND_SCOPE.md', 'SOURCES.md',
    'requirements.txt', 'EDITION_MAP.json', 'verify_package.py',
    'REPLAY_REPORT.json', 'TAMPER_CONTROLS.json',
    'cover/CANONICAL_COVER_THEOREM.md', 'cover/AUDIT_CHECKLIST.md',
    'differentials/EXACTNESS_AND_BASE_ODES.md', 'differentials/verify_formulas.py',
    'differentials/SYMBOLIC_CHECKS.json',
    'degeneracies/DEGENERACIES_AND_IMAGE_AUDIT.md', 'degeneracies/verify_signs.py',
    'degeneracies/SIGN_CHECKS.json', 'effectivity/EFFECTIVITY_AUDIT.md',
    'exact/EXACT_EXAMPLES_AND_CONTROLS.md', 'exact/check_examples.py',
    'exact/CHECK_RECEIPT.json', 'audit/INDEPENDENT_ACCEPTANCE_REPORT.md',
    'audit/ACCEPTANCE.json', 'audit/independent_controls.py',
    'audit/INDEPENDENT_CONTROLS.json', 'sources/CORPUS_BINDINGS.json',
    'sources/PREPARATION_SOURCE_INSPECTION.json',
    'sources/EFFECTIVITY_SOURCE_INSPECTION.json', 'sources/INDEPENDENT_SOURCE_CHECKS.json',
}
SUITES = [
    ('exact/check_examples.py', 'exact/CHECK_RECEIPT.json', 49),
    ('degeneracies/verify_signs.py', 'degeneracies/SIGN_CHECKS.json', 67),
    ('differentials/verify_formulas.py', 'differentials/SYMBOLIC_CHECKS.json', 12),
    ('audit/independent_controls.py', 'audit/INDEPENDENT_CONTROLS.json', 30),
]
CHECKER_HASHES = {
    'exact/check_examples.py':'a3fee81c0150d2f20b47ebcd01b67d058073ce5eba698904af9ea85446bfca4d',
    'degeneracies/verify_signs.py':'c62a719053d904cb93c93e9f0cc679d0719958b013d6868a131805ab3c39df49',
    'differentials/verify_formulas.py':'d89b8465635dd775ff0dc291629dc22c39c7e77771d46b2442cf2ef5af31a131',
    'audit/independent_controls.py':'ce9b9ee5cfe5ddf3fcd15a37e9158575989f2137ed922c47e3c7207912c6c773',
}
BOOTSTRAP = r'''
import json, pathlib, sys
if sys.flags.optimize != 0 or not __debug__:
    raise RuntimeError('Child interpreter assertions are disabled')
try:
    exec(compile('assert False, "assertion-probe"', '<assertion-probe>', 'exec', optimize=0), {})
except AssertionError:
    pass
else:
    raise RuntimeError('Deliberately false assertion did not fail')
p = pathlib.Path(sys.argv[1])
exec(compile(p.read_bytes(), str(p), 'exec', optimize=0),
     {'__name__':'__main__', '__file__':str(p), '__builtins__':__builtins__})
print('ASSERTION_GUARD=' + json.dumps({'optimize':sys.flags.optimize,
    'debug':__debug__, 'false_assertion_rejected':True, 'compile_optimize':0}, sort_keys=True))
'''

def digest(data): return hashlib.sha256(data).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def inventory():
    result = {}
    for path in sorted(ROOT.rglob('*')):
        name = path.relative_to(ROOT).as_posix()
        require(not path.is_symlink(), 'Symlink is not allowed: '+name)
        if path.is_file():
            result[name] = path.read_bytes()
        else:
            require(path.is_dir(), 'Nonregular package object: '+name)
    return result

def validate_receipt(script, receipt, count):
    require(receipt.get('sympy_version') == '1.14.0', 'Frozen replay requires SymPy 1.14.0')
    entries = receipt.get('checks')
    if script.startswith('differentials/'):
        require(isinstance(entries, dict) and len(entries) == count, 'Wrong symbolic check count')
        require(receipt.get('all_pass') is True, 'Symbolic receipt is not all-pass')
        require(all(isinstance(k,str) and k and v == 'PASS' for k,v in entries.items()), 'Bad symbolic verdict')
    else:
        require(isinstance(entries,list) and len(entries) == count, 'Wrong named check count')
        require(receipt.get('all_passed') is True, 'Receipt is not all-passed')
        count_key = 'checks_count' if script.startswith('exact/') else 'count'
        require(receipt.get(count_key) == count, 'Reported count differs')
        names=[]
        for entry in entries:
            require(isinstance(entry,dict), 'Check entry is not an object')
            key='check' if script.startswith('degeneracies/') else 'name'
            name=entry.get(key)
            require(isinstance(name,str) and bool(name), 'Missing check name')
            names.append(name)
            require(entry.get('result') == 'PASS' if script.startswith('exact/') else entry.get('passed') is True,
                    'Failed named check: '+name)
        require(len(set(names)) == count, 'Duplicate named check')
    if script.startswith('audit/'):
        require(receipt.get('homogeneous_slopes_checked') == 108, 'Wrong homogeneous-slope comparison count')

def integrity(expected_manifest=None):
    files = inventory()
    require('MANIFEST.json' in files, 'Missing MANIFEST.json')
    raw = files['MANIFEST.json']
    if expected_manifest is not None:
        require(digest(raw) == expected_manifest, 'Manifest digest differs from external trust anchor')
    manifest = json.loads(raw)
    require(manifest.get('schema') == 'fixed_signature_public_package_v1', 'Wrong manifest schema')
    require(manifest.get('disposition') == 'scoped_resolved1/5', 'Wrong disposition')
    require(manifest.get('queue_row') == 1793 and manifest.get('catalog_id') == 20000200, 'Wrong target identity')
    require(manifest.get('accepted_report_sha256') == ACCEPTED_REPORT, 'Wrong accepted-report binding')
    require(manifest.get('accepted_frozen_manifest_sha256') == ACCEPTED_MANIFEST, 'Wrong accepted-manifest binding')
    entries = manifest.get('files')
    require(isinstance(entries,list), 'Manifest files must be a list')
    names=[]
    for entry in entries:
        require(isinstance(entry,dict), 'Manifest file entry is not an object')
        name=entry.get('path')
        require(isinstance(name,str), 'Nonstring manifest path')
        p=PurePosixPath(name)
        require(not p.is_absolute() and p.as_posix() == name and '..' not in p.parts and '\\' not in name,
                'Unsafe or noncanonical manifest path')
        require(name != 'MANIFEST.json' and name not in names, 'Duplicate or self-referential manifest path')
        names.append(name)
        require(name in files, 'Missing file: '+name)
        require(entry.get('bytes') == len(files[name]), 'Byte count mismatch: '+name)
        require(entry.get('sha256') == digest(files[name]), 'Hash mismatch: '+name)
    require(set(names) == REQUIRED, 'Manifest does not enumerate the exact disclosed package')
    require(set(files) == REQUIRED | {'MANIFEST.json'}, 'Unexpected or missing package file')
    accepted = json.loads(files['audit/ACCEPTANCE.json'])
    require(accepted.get('accepted_report_sha256') == ACCEPTED_REPORT, 'Acceptance report anchor mismatch')
    require(accepted.get('accepted_frozen_manifest_sha256') == ACCEPTED_MANIFEST, 'Acceptance manifest anchor mismatch')
    require(accepted.get('verdict') == 'ACCEPT' and accepted.get('status') == 'scoped_resolved'
            and accepted.get('turns') == '1/5' and accepted.get('unresolved_gaps') == [], 'Acceptance disposition mismatch')
    require(accepted.get('queue_row') == 1793 and accepted.get('catalog_id') == 20000200, 'Acceptance target mismatch')
    require(accepted.get('named_exact_checks_passed') == 158
            and accepted.get('additional_homogeneous_slope_comparisons') == 108, 'Acceptance count mismatch')
    for key in ['complete_decision_software_implemented','novelty_claim','broad_AIM_resolution_claim']:
        require(accepted.get(key) is False, 'Unaccepted scope expansion: '+key)
    editions = json.loads(files['EDITION_MAP.json'])
    require(editions.get('mathematical_content_changed') is False
            and editions.get('executable_checker_bytes_changed') is False, 'Unaccepted content change')
    bindings=accepted.get('artifact_bindings')
    require(isinstance(bindings,list) and len(bindings) == 15, 'Wrong accepted artifact count')
    require(editions.get('artifact_bindings') == bindings, 'Edition map disagrees with acceptance')
    bound=[]
    for entry in bindings:
        path=entry['path']
        require(path in files and path not in bound, 'Missing or duplicate bound artifact')
        bound.append(path)
        b=files[path]
        require(entry.get('public_bytes') == len(b) and entry.get('public_sha256') == digest(b), 'Public artifact binding mismatch: '+path)
        require(entry.get('edition') in ['byte-identical','presentation-only'], 'Unknown edition kind')
        if entry['edition'] == 'byte-identical':
            require(entry.get('accepted_bytes') == len(b) and entry.get('accepted_sha256') == digest(b), 'Original byte identity mismatch: '+path)
    for script,output,count in SUITES:
        require(digest(files[script]) == CHECKER_HASHES[script], 'Accepted checker bytes changed: '+script)
        validate_receipt(script,json.loads(files[output]),count)
    return files,digest(raw)

def execute_checker(script, data, directory, timeout=600):
    target=directory/script
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    env=dict(os.environ)
    for key in ['PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME','PYTHONSTARTUP']:
        env.pop(key,None)
    proc=subprocess.run([sys.executable,'-I','-B','-c',BOOTSTRAP,str(target)],
                        cwd=directory,env=env,capture_output=True,text=True,timeout=timeout)
    require(proc.returncode == 0, 'CHECKER_FAILED '+script+'\n'+proc.stdout+proc.stderr)
    markers=[line.split('=',1)[1] for line in proc.stdout.splitlines() if line.startswith('ASSERTION_GUARD=')]
    require(len(markers) == 1, 'Missing child assertion guard: '+script)
    guard=json.loads(markers[0])
    require(guard == {'optimize':0,'debug':True,'false_assertion_rejected':True,'compile_optimize':0},
            'Child assertion guard failed: '+script)
    return guard

def replay(files):
    results=[]
    with tempfile.TemporaryDirectory(prefix='fixed-signature-replay-') as temp:
        tmp=Path(temp)
        for script,output,count in SUITES:
            guard=execute_checker(script,files[script],tmp)
            result=(tmp/output).read_bytes()
            require(result == files[output], 'Replay differs byte for byte: '+output)
            validate_receipt(script,json.loads(result),count)
            results.append({'script':script,'status':'PASS','named_checks':count,
                            'output_sha256':digest(result),'byte_identical_to_frozen_output':True,
                            'child_assertion_guard':guard})
    require(sum(row['named_checks'] for row in results) == 158, 'Wrong total named check count')
    return results

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only',action='store_true')
    parser.add_argument('--manifest-sha256',help='Externally trusted SHA-256 of MANIFEST.json')
    args=parser.parse_args()
    files,anchor=integrity(args.manifest_sha256)
    result={'status':'PASS','integrity':'PASS','package_files':len(files),
            'manifest_sha256':anchor,'caller_optimize':sys.flags.optimize,
            'accepted_report_sha256':ACCEPTED_REPORT}
    if not args.integrity_only:
        result['replay']=replay(files)
        result['named_exact_checks_passed']=158
        result['homogeneous_slope_comparisons_within_aggregate_check']=108
        require(inventory() == files, 'Package changed during replay')
        result['package_unchanged']=True
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
