#!/usr/bin/env python3
"""Fail-closed portable integrity/replay check; anchor the ZIP hash separately."""
import hashlib
import json
import pathlib
import subprocess
import sys
sys.dont_write_bytecode = True

EXPECTED = {'APPROACHES.md','IDENTITY.json','PROOF.md','README.md','SOURCES.json',
            'code/checks.py','results/checks.json','verify.py'}

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def unique_object(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key: '+key)
        out[key] = value
    return out

def read_json(file):
    return json.loads(file.read_text(encoding='utf-8'), object_pairs_hook=unique_object)

def verify(root):
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries), 'symlink forbidden')
    files = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    require(files == EXPECTED | {'MANIFEST.json'}, 'unexpected or missing file')
    manifest = read_json(root/'MANIFEST.json')
    require(set(manifest) == {'schema_version','files'}, 'unexpected manifest schema')
    require(manifest['schema_version'] == 1, 'unsupported manifest version')
    require(isinstance(manifest['files'], dict) and set(manifest['files']) == EXPECTED,
            'manifest file set mismatch')
    for name, meta in manifest['files'].items():
        require(isinstance(meta,dict) and set(meta) == {'sha256','bytes'}, 'unexpected entry schema')
        b = (root/name).read_bytes()
        require(type(meta['bytes']) is int and len(b) == meta['bytes'], 'size mismatch: '+name)
        require(hashlib.sha256(b).hexdigest() == meta['sha256'], 'digest mismatch: '+name)
    identity = read_json(root/'IDENTITY.json')
    require(identity['id'] == 6200014 and identity['problem_number'] == 'AMR-061-0014',
            'problem identity mismatch')
    require(identity['scope']['no_induced_square'] is True and identity['scope']['flag'] is True,
            'essential hypotheses absent')
    require(identity['scope']['PL_assumed_separately'] is False, 'unapproved PL strengthening')
    outputs = []
    for optimization in ([], ['-O']):
        p = subprocess.run([sys.executable,*optimization,'-B',str(root/'code/checks.py')],
                           cwd=root,check=False,capture_output=True,text=True)
        require(p.returncode == 0, 'control subprocess failed: '+p.stderr)
        outputs.append(json.loads(p.stdout, object_pairs_hook=unique_object))
    expected = read_json(root/'results/checks.json')
    require(outputs[0] == outputs[1] == expected, 'control output mismatch')
    require(expected['all_controls_pass'] is True, 'controls did not pass')
    return {'integrity_pass':True,'normal_and_optimized_replay_pass':True,
            'verified_manifest_files':len(EXPECTED),'cycle_cases':len(expected['cycle_cases']),
            'dimension_arithmetic_cases':len(expected['dimension_arithmetic_cases']),
            'topological_theorems_formally_verified':False}

if __name__ == '__main__':
    try:
        require(len(sys.argv)==1,'verify.py takes no arguments')
        print(json.dumps(verify(pathlib.Path(__file__).resolve().parent),sort_keys=True,indent=2))
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
