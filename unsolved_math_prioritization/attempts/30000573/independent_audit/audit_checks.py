#!/usr/bin/env python3
"""Independent integrity/replay/adversarial checks; not a mathematical proof checker.

The externally anchored author ZIP is required; no private source files are used.
This script never modifies it. Temporary mutations are removed on exit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ZIP_SHA = '5c52306f764afdbda9c2520fa54a02c068cbbe8c61ef6899a11116eac0d57000'
MANIFEST_SHA = '36bedb158def6832a026b31ad1d249aad1745710eef914ba1cf7f5e91a6a68e6'
MEMBERS = {'APPROACHES.json', 'AUTHOR_VALIDATION.json', 'MANIFEST.json',
           'PROOFS.md', 'PUBLIC_METADATA.json', 'RESULT.md', 'RESULTS.json',
           'SOURCES.json', 'exact_controls.py', 'verify_release.py'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate_source(path):
    data = path.read_bytes()
    require(len(data) == 19303, 'author ZIP byte count')
    require(sha(data) == ZIP_SHA, 'author ZIP external anchor')
    with zipfile.ZipFile(path) as z:
        require(len(z.infolist()) == 10, 'ZIP member count')
        require(set(z.namelist()) == {'release/' + s for s in MEMBERS}, 'ZIP member names')
        files = {s: z.read('release/' + s) for s in MEMBERS}
    require(sha(files['MANIFEST.json']) == MANIFEST_SHA, 'manifest external anchor')
    manifest = json.loads(files['MANIFEST.json'])
    require(set(manifest['files']) == MEMBERS - {'MANIFEST.json'}, 'manifest membership')
    for name, entry in manifest['files'].items():
        require(entry == {'bytes': len(files[name]), 'sha256': sha(files[name])},
                'independent byte/hash check: ' + name)
    return files


def invoke(root, anchor, optimize):
    command = [sys.executable] + (['-O'] if optimize else [])
    command += ['-B', str(root/'verify_release.py'), '--manifest-sha256', anchor]
    return subprocess.run(command, cwd=root.parent, capture_output=True,
                          text=True, timeout=120)


def reanchor(root):
    p = root/'MANIFEST.json'
    manifest = json.loads(p.read_text())
    for name in manifest['files']:
        data = (root/name).read_bytes()
        manifest['files'][name] = {'bytes': len(data), 'sha256': sha(data)}
    p.write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    return sha(p.read_bytes())


def replace_exact(path, old, new):
    text = path.read_text()
    require(text.count(old) == 1, 'mutation target not unique: '+old)
    path.write_text(text.replace(old, new))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author-zip', required=True, type=Path)
    args = parser.parse_args()
    files = validate_source(args.author_zip)
    result = {'problem_id': 30000573, 'source_zip_sha256': ZIP_SHA,
              'source_manifest_sha256': MANIFEST_SHA,
              'independent_member_hash_checks': 9,
              'author_primary_cases_per_replay': 13722,
              'baseline': [], 'negative_controls': [], 'scope_diagnostics': []}
    mutations = [
        'same_size_proof', 'missing_file', 'extra_file', 'extra_directory',
        'proof_symlink', 'manifest_symlink', 'verifier_symlink', 'controls_symlink',
        'manifest_whitespace', 'result_count', 'code_bytes', 'wrong_anchor',
        'invalid_anchor', 'root_symlink', 'stability_buffer', 'triangular_sign',
        'left_eigenfunctional_sign', 'omit_final_boundary',
    ]
    semantic = {'stability_buffer', 'triangular_sign', 'left_eigenfunctional_sign',
                'omit_final_boundary'}
    with tempfile.TemporaryDirectory(prefix='chaos independent audit ') as tmp:
        base = Path(tmp)
        source = base/'original'
        source.mkdir()
        for name, data in files.items():
            (source/name).write_bytes(data)
        for location in ['original', 'relocated nested directory/release with spaces']:
            root = base/location
            if root != source:
                shutil.copytree(source, root)
            for optimize in [False, True]:
                process = invoke(root, MANIFEST_SHA, optimize)
                require(process.returncode == 0, 'baseline: '+process.stderr)
                got = json.loads(process.stdout)
                require(got['primary_control_cases'] == 13722, 'baseline case count')
                require(got['manifest_sha256'] == MANIFEST_SHA, 'baseline manifest')
                require(got['status'] == 'PASS_INTEGRITY_AND_REPLAY', 'baseline status')
                result['baseline'].append({'location': 'original' if root == source else 'relocated',
                                           'mode': 'optimized' if optimize else 'normal',
                                           'status': 'PASS'})
        for optimize in [False, True]:
            for index, mutation in enumerate(mutations):
                root = base/('mutant_'+str(int(optimize))+'_'+str(index))
                shutil.copytree(source, root)
                anchor = MANIFEST_SHA
                if mutation == 'same_size_proof':
                    p = root/'PROOFS.md'; data = p.read_bytes(); p.write_bytes(b'!'+data[1:])
                elif mutation == 'missing_file':
                    (root/'SOURCES.json').unlink()
                elif mutation == 'extra_file':
                    (root/'unexpected.txt').write_text('unexpected')
                elif mutation == 'extra_directory':
                    (root/'unexpected').mkdir()
                elif mutation.endswith('_symlink') and mutation != 'root_symlink':
                    name = {'proof_symlink':'PROOFS.md', 'manifest_symlink':'MANIFEST.json',
                            'verifier_symlink':'verify_release.py', 'controls_symlink':'exact_controls.py'}[mutation]
                    p = root/name; p.unlink(); p.symlink_to(source/name)
                elif mutation == 'manifest_whitespace':
                    p = root/'MANIFEST.json'; p.write_bytes(p.read_bytes()+b' ')
                elif mutation == 'result_count':
                    replace_exact(root/'RESULTS.json', '13722', '13723')
                elif mutation == 'code_bytes':
                    p = root/'exact_controls.py'; p.write_bytes(p.read_bytes()+b'\n')
                elif mutation == 'wrong_anchor':
                    anchor = '0'*64
                elif mutation == 'invalid_anchor':
                    anchor = 'G'*64
                elif mutation == 'root_symlink':
                    link = base/('linked_root_'+str(int(optimize))); link.symlink_to(root)
                    root = link
                elif mutation == 'stability_buffer':
                    replace_exact(root/'exact_controls.py', '(k+2*m+1)*2**(r+n)', '(k+2*m)*2**(r+n)')
                elif mutation == 'triangular_sign':
                    replace_exact(root/'exact_controls.py', 'ring.sub(lam[n], lam[t])', 'ring.add(lam[n], lam[t])')
                elif mutation == 'left_eigenfunctional_sign':
                    replace_exact(root/'exact_controls.py',
                                  'left = ring.add(left, ring.scale(c[j-1], weights[j]))',
                                  'left = ring.sub(left, ring.scale(c[j-1], weights[j]))')
                elif mutation == 'omit_final_boundary':
                    replace_exact(root/'exact_controls.py', 'range(length + (1 if boundary else 0))', 'range(length)')
                if mutation in semantic:
                    anchor = reanchor(root)
                process = invoke(root, anchor, optimize)
                require(process.returncode != 0, 'mutation was accepted: '+mutation)
                require('REJECT:' in process.stderr, 'unexpected rejection mechanism: '+mutation)
                result['negative_controls'].append({'name': mutation,
                    'mode':'optimized' if optimize else 'normal', 'status':'REJECTED',
                    'manifest_rebound':mutation in semantic})
            # A changed proof with an intentionally replaced trust anchor is expected
            # to pass replay: arithmetic diagnostics do not analyze proof prose.
            root = base/('scope_diagnostic_'+str(int(optimize)))
            shutil.copytree(source, root)
            replace_exact(root/'PROOFS.md', 'every x∈X', 'some x∈X')
            process = invoke(root, reanchor(root), optimize)
            require(process.returncode == 0, 'rebound prose diagnostic')
            result['scope_diagnostics'].append({'name':'rebound_prose_is_not_proof_checked',
                'mode':'optimized' if optimize else 'normal', 'status':'ACCEPTED_AS_EXPECTED'})
    result['negative_control_count'] = len(result['negative_controls'])
    result['status'] = 'PASS_INDEPENDENT_INTEGRITY_REPLAY_AND_MUTATIONS'
    result['scope'] = 'Finite diagnostics and integrity only. The mathematical audit is separate.'
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
