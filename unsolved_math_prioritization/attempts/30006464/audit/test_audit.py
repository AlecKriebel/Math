#!/usr/bin/env python3
"""Independent replay and actual mutation rejection, with isolated interpreters."""
import hashlib
import difflib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
AUTHOR_MANIFEST_SHA = '8c9aa06e0920943b23c258c8b426408f8d18435f0dec32d454f5f47473650184'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def invoke(directory, name='verify_audit.py', optimized=False):
    # -I removes the input directory and PYTHONPATH from import lookup; -B forbids writes.
    return subprocess.run([sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(directory/name)],
                          cwd=directory, env=ENV, text=True, capture_output=True)

def seal(directory):
    manifest = json.loads((directory/'MANIFEST.json').read_text())
    for name in manifest:
        path = directory/name
        if path.is_file() and not path.is_symlink():
            raw = path.read_bytes()
            manifest[name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    (directory/'MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')

def change_json(directory, name, key, value):
    path = directory/name
    content = json.loads(path.read_text())
    content[key] = value
    path.write_text(json.dumps(content, indent=2, sort_keys=True)+'\n')

def main():
    pin = json.loads((ROOT/'SOURCE_PIN.json').read_text())
    require(set(pin) == {'verify_audit.py', 'test_audit.py', 'verify_inputs.py'}, 'preexecution source inventory')
    for name, digest in pin.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, 'preexecution audit source pin')
    require(hashlib.sha256((ROOT/'AUTHOR/MANIFEST.json').read_bytes()).hexdigest() == AUTHOR_MANIFEST_SHA,
            'preexecution author manifest pin')
    normal = invoke(ROOT)
    optimized = invoke(ROOT, optimized=True)
    require(normal.returncode == optimized.returncode == 0 and normal.stdout == optimized.stdout,
            'audit normal/optimized mismatch: '+normal.stderr+optimized.stderr)
    # The audit verifier checks all author bytes before these subprocesses are allowed.
    author_normal = invoke(ROOT/'AUTHOR', 'verify.py')
    author_optimized = invoke(ROOT/'AUTHOR', 'verify.py', True)
    require(author_normal.returncode == author_optimized.returncode == 0
            and author_normal.stdout == author_optimized.stdout, 'author isolated replay mismatch')
    author_suite = invoke(ROOT/'AUTHOR', 'test_packet.py')
    require(author_suite.returncode == 0, 'author advertised suite failed')
    mutations = []
    with tempfile.TemporaryDirectory(prefix='independent short cusp audit ') as name:
        base = pathlib.Path(name)
        corrected = base/'actual corrected author copy'
        shutil.copytree(ROOT/'AUTHOR', corrected)
        correction = json.loads((ROOT/'CORRECTION.json').read_text())
        original = (corrected/'PROOFS.md').read_text()
        require(hashlib.sha256(original.encode()).hexdigest() == correction['original_proof_sha256'], 'correction preimage')
        changed = original
        for replacement in correction['replacements']:
            require(changed.count(replacement['before']) == 1, 'unique correction target')
            changed = changed.replace(replacement['before'], replacement['after'])
        require(hashlib.sha256(changed.encode()).hexdigest() == correction['corrected_proof_sha256']
                and len(changed.encode()) == correction['corrected_proof_bytes'], 'correction postimage')
        actual_patch = ''.join(difflib.unified_diff(original.splitlines(keepends=True),changed.splitlines(keepends=True),
                                                 fromfile='a/PROOFS.md',tofile='b/PROOFS.md'))
        require(actual_patch == (ROOT/'GRAM_ZERO_DIMENSION.patch').read_text(), 'actual unified correction patch')
        (corrected/'PROOFS.md').write_text(changed)
        seal(corrected)
        corrected_normal = invoke(corrected, 'verify.py')
        corrected_optimized = invoke(corrected, 'verify.py', True)
        require(corrected_normal.returncode == corrected_optimized.returncode == 0
                and corrected_normal.stdout == corrected_optimized.stdout == author_normal.stdout,
                'actual corrected author normal/optimized replay')
        corrected_suite = invoke(corrected, 'test_packet.py')
        require(corrected_suite.returncode == 0, 'actual corrected author mutation/relocation suite')
        relocated = base/'fresh relocated packet with spaces'
        shutil.copytree(ROOT, relocated)
        for opt in [False, True]:
            replay = invoke(relocated, optimized=opt)
            require(replay.returncode == 0 and replay.stdout == normal.stdout, 'audit relocation mismatch')
        def trial(label, mutate, reseal=False, expected=''):
            directory = base/label
            shutil.copytree(ROOT, directory)
            mutate(directory)
            if reseal:
                seal(directory)
            for opt in [False, True]:
                replay = invoke(directory, optimized=opt)
                require(replay.returncode != 0, 'accepted mutation: '+label)
                if expected:
                    require(expected in replay.stderr, 'unexpected rejection reason: '+label+': '+replay.stderr)
            mutations.append(label)
        trial('changed-audit-prose', lambda d:(d/'AUDIT.md').write_text('altered'), expected='manifest bytes')
        trial('missing-author-proof', lambda d:(d/'AUTHOR/PROOFS.md').unlink(), expected='inventory')
        trial('extra-pdf', lambda d:(d/'source.pdf').write_bytes(b'%PDF-1.0'), expected='inventory')
        trial('extra-source-extract', lambda d:(d/'extract.txt').write_text('not an allowed member'), expected='inventory')
        trial('extra-dataset', lambda d:(d/'dataset.json').write_text('[]'), expected='inventory')
        trial('extra-hidden-file', lambda d:(d/'.extra').write_text('x'), expected='inventory')
        trial('extra-cache-directory', lambda d:(d/'__pycache__').mkdir(), expected='inventory')
        trial('extra-nested-directory', lambda d:(d/'AUTHOR/extra').mkdir(), expected='inventory')
        trial('extra-legacy-bytecode', lambda d:(d/'hashlib.pyc').write_bytes(b'untrusted bytes never executed'), expected='inventory')
        trial('extra-import-shadow', lambda d:(d/'json.py').write_text('raise RuntimeError("UNTRUSTED_IMPORT_EXECUTED")\n'), expected='inventory')
        def symlink_file(d):
            (d/'AUTHOR/PROOFS.md').unlink()
            (d/'AUTHOR/PROOFS.md').symlink_to(ROOT/'AUTHOR/PROOFS.md')
        trial('symlink-author-proof', symlink_file, expected='nonregular')
        trial('symlink-directory', lambda d:(d/'linked').symlink_to(ROOT/'AUTHOR', target_is_directory=True), expected='nonregular')
        trial('unpinned-audit-source', lambda d:(d/'verify_inputs.py').write_text((d/'verify_inputs.py').read_text()+'\n# change\n'), True, 'audit source pin')
        trial('false-resolution', lambda d:change_json(d,'AUDIT_RESULTS.json','full_resolution',True), True, 'resolution scope')
        trial('wrong-status', lambda d:change_json(d,'AUDIT_RESULTS.json','original_status','solved'), True, 'resolution scope')
        trial('six-approach-overclaim', lambda d:change_json(d,'AUDIT_RESULTS.json','approaches_used',6), True, 'resolution scope')
        trial('zero-space-clarification-removed', lambda d:change_json(d,'AUDIT_RESULTS.json','zero_dimensional_convention_required',False), True, 'verdict scope')
        trial('unsafe-inventory-claim', lambda d:change_json(d,'AUDIT_RESULTS.json','safe_inventory_only',False), True, 'safety scope')
        trial('source-document-inclusion', lambda d:change_json(d,'SOURCE_CHECKS.json','source_files_included',True), True, 'source inclusion scope')
        def wrong_source(d):
            path=d/'SOURCE_CHECKS.json'; content=json.loads(path.read_text())
            content['pinned_pdfs'][0]['sha256']='0'*64
            path.write_text(json.dumps(content))
        trial('wrong-pdf-digest',wrong_source,True,'source metadata identity')
        def resealed_author_proof(d):
            (d/'AUTHOR/PROOFS.md').write_text('altered proof')
            seal(d/'AUTHOR')
        trial('resealed-author-proof',resealed_author_proof,True,'immutable author manifest anchor')
        def resealed_author_source(d):
            p=d/'AUTHOR/verify.py'; p.write_text(p.read_text()+'\n# source edit\n')
            pin=json.loads((d/'AUTHOR/SOURCE_PIN.json').read_text())
            pin['verify.py']=hashlib.sha256(p.read_bytes()).hexdigest()
            (d/'AUTHOR/SOURCE_PIN.json').write_text(json.dumps(pin))
            seal(d/'AUTHOR')
        trial('resealed-author-source-and-pin',resealed_author_source,True,'immutable author manifest anchor')
        trial('extra-audit-source-pin',lambda d:change_json(d,'SOURCE_PIN.json','extra.py','0'*64),True,'source pin inventory')
        trial('missing-input-verifier',lambda d:(d/'verify_inputs.py').unlink(),expected='inventory')
        trial('correction-freeze-alteration',lambda d:change_json(d,'CORRECTION.json','original_freeze_unchanged',False),True,'operative correction scope')
        trial('resealed-correction-patch',lambda d:(d/'GRAM_ZERO_DIMENSION.patch').write_text('altered patch'),True,'operative patch digest')
    output={'status':'pass','normal_optimized_relocation_agree':True,
            'isolated_interpreter':True,'audit_mutation_cases_rejected':len(mutations),
            'audit_mutation_executions':2*len(mutations),'audit_mutations':mutations,
            'independent_baseline':json.loads(normal.stdout),
            'operative_correction':{'applied_to_copy':True,'original_freeze_unchanged':True,
                                    'corrected_proof_sha256':correction['corrected_proof_sha256'],
                                    'normal_optimized_agree':True,
                                    'corrected_author_suite':json.loads(corrected_suite.stdout)},
            'author_baseline':json.loads(author_normal.stdout),
            'author_suite':json.loads(author_suite.stdout)}
    print(json.dumps(output,sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('FAIL: '+str(exc))
