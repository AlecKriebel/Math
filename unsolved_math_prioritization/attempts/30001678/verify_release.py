#!/usr/bin/env python3
"""Portable frozen-byte and model replay; not a formal mathematical proof checker."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

PINS = {
    'author_packet/MANIFEST.json': 'a387cbefe3b91492f1948ff6cb20b912b0ebe21a924a19a9b371ca0e428f31d5',
    'independent_audit/MANIFEST.json': '47675e4982186f9ea376d4b5b35e10c0b5088beb3f9a445aa05a6efe04f0efc3',
}
AUTHOR_NAMES = set('APPROACH_LOG.md MANIFEST.json PROOF.md README.md SOURCE_STATUS.md example_results.json source_verification.json verify_examples.py verify_packet.py'.split())
AUDIT_NAMES = set('AUDIT.md BINDINGS.json INDEPENDENT_CONTROLS.py MANIFEST.json NEGATIVE_CONTROLS.md RESULTS.json SOURCE_CHECKS.json'.split())
TOP_NAMES = set('README.md RELEASE_STATUS.json FROZEN_BINDINGS.json verify_release.py REPLAY_RESULTS.json RELEASE_MANIFEST.json'.split())
EXPECTED = TOP_NAMES | {'author_packet/'+s for s in AUTHOR_NAMES} | {'independent_audit/'+s for s in AUDIT_NAMES}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def record_check(root, name, rec):
    require(set(rec) == {'bytes','sha256'}, 'record schema: '+name)
    b = (root/name).read_bytes()
    require(len(b) == rec['bytes'] and sha(b) == rec['sha256'], 'byte mismatch: '+name)

def verify(root, replay=True):
    found = set()
    dirs = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink')
        name = p.relative_to(root).as_posix()
        if p.is_file():
            found.add(name)
        else:
            require(p.is_dir(), 'special node')
            dirs.add(name)
    require(found == EXPECTED, 'exact release file boundary')
    require(dirs == {'author_packet','independent_audit'}, 'exact directory boundary')
    m = json.loads((root/'RELEASE_MANIFEST.json').read_bytes())
    require(set(m) == {'schema','problem_id','files'}, 'release manifest schema')
    require(m['schema'] == 1 and m['problem_id'] == '30001678', 'release identity')
    require(set(m['files']) == EXPECTED-{'RELEASE_MANIFEST.json'}, 'release inventory')
    for name,rec in m['files'].items():
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'unsafe path')
        record_check(root, name, rec)
    for name,h in PINS.items():
        require(sha((root/name).read_bytes()) == h, 'external manifest pin: '+name)
    author = json.loads((root/'author_packet/MANIFEST.json').read_bytes())
    audit = json.loads((root/'independent_audit/MANIFEST.json').read_bytes())
    bindings = json.loads((root/'independent_audit/BINDINGS.json').read_bytes())
    require(author['problem_id'] == '30001678' and author['status'] == 'unresolved_scoped_partials', 'author identity')
    require(set(author['files']) == AUTHOR_NAMES-{'MANIFEST.json'}, 'author inventory')
    require(set(audit['files']) == AUDIT_NAMES-{'MANIFEST.json'}, 'audit inventory')
    require(set(bindings['frozen_files']) == AUTHOR_NAMES, 'binding inventory')
    require(audit['research_disposition'] == 'unsolved' and audit['approaches_completed'] == 5, 'audit status')
    for name,rec in author['files'].items(): record_check(root/'author_packet', name, rec)
    for name,rec in audit['files'].items(): record_check(root/'independent_audit', name, rec)
    for name,rec in bindings['frozen_files'].items(): record_check(root/'author_packet', name, rec)
    status = json.loads((root/'RELEASE_STATUS.json').read_bytes())
    require(status['problem_id'] == '30001678' and status['queue_status'] == 'unsolved' and status['turns'] == '5/5', 'release disposition')
    require(status['controlling_cantor_extraction_clarification_adopted'] is True, 'clarification not adopted')
    result = {'result':'PASS_RELEASE_INTEGRITY_AND_REPLAY', 'release_files':len(EXPECTED),
              'author_files':9, 'audit_files':7,
              'qualification':'Integrity and finite/model replay only; no formal proof, source-resolution, novelty, or global-openness certificate.'}
    if replay:
        modes = {}
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            prefix = [sys.executable,'-B']+flags
            example = subprocess.run(prefix+[str(root/'author_packet/verify_examples.py')], capture_output=True, check=True)
            require(not example.stderr and example.stdout == (root/'author_packet/example_results.json').read_bytes(), 'example replay')
            independent = subprocess.run(prefix+[str(root/'independent_audit/INDEPENDENT_CONTROLS.py'),'--release',str(root/'author_packet')], capture_output=True, check=True)
            require(not independent.stderr and independent.stdout == (root/'independent_audit/RESULTS.json').read_bytes(), 'audit replay')
            a = json.loads(independent.stdout)
            direct_author = subprocess.run(prefix+[str(root/'author_packet/verify_packet.py'),'--self-test'], capture_output=True, check=True)
            require(not direct_author.stderr and json.loads(direct_author.stdout) == a['author_checker_replay'], 'direct author verifier replay')
            require(a['independent_models']['total_model_assertions'] == 2932, 'model count')
            require(a['author_checker_replay']['exact_example_assertions'] == 47729, 'author count')
            require(len(a['independent_mutations_rejected']) == 11 and len(a['author_checker_replay']['rejected_mutations']) == 7, 'corruption counts')
            modes[mode] = {'author_assertions':47729, 'independent_model_assertions':2932,
                           'author_mutations_rejected':7, 'independent_mutations_rejected':11,
                           'exact_stdout_matches_frozen_results':True}
        result['modes'] = modes
    return result

def corruptions(root):
    cases = ['changed_author','changed_audit','changed_guide','missing','extra_hidden','nested_empty',
             'symlink','unlisted_pdf','manifest_traversal','manifest_omission',
             'coordinated_author_and_manifests','coordinated_audit_and_manifests','wrong_status']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='perfect-product-release-mutation-') as tmp:
            p = Path(tmp)/'packet'; shutil.copytree(root,p)
            if case.startswith('changed_'):
                file = {'changed_author':'author_packet/PROOF.md','changed_audit':'independent_audit/AUDIT.md','changed_guide':'README.md'}[case]
                b = bytearray((p/file).read_bytes()); b[0] ^= 1; (p/file).write_bytes(b)
            elif case == 'missing': (p/'README.md').unlink()
            elif case == 'extra_hidden': (p/'.extra').write_text('control')
            elif case == 'nested_empty': (p/'independent_audit/extra').mkdir()
            elif case == 'symlink': (p/'README.md').unlink(); (p/'README.md').symlink_to('author_packet/README.md')
            elif case == 'unlisted_pdf': (p/'source.pdf').write_bytes(b'%PDF synthetic corruption control')
            elif case in ('manifest_traversal','manifest_omission'):
                m = json.loads((p/'RELEASE_MANIFEST.json').read_bytes()); rec = m['files'].pop('README.md')
                if case == 'manifest_traversal': m['files']['../README.md'] = rec
                (p/'RELEASE_MANIFEST.json').write_text(json.dumps(m))
            else:
                m = json.loads((p/'RELEASE_MANIFEST.json').read_bytes())
                if case == 'wrong_status':
                    path = 'RELEASE_STATUS.json'; s = json.loads((p/path).read_bytes()); s['queue_status']='claimed_solved'
                    (p/path).write_text(json.dumps(s)); b=(p/path).read_bytes(); m['files'][path]={'bytes':len(b),'sha256':sha(b)}
                else:
                    folder = 'author_packet' if 'author' in case else 'independent_audit'
                    name = 'PROOF.md' if 'author' in case else 'AUDIT.md'
                    (p/folder/name).write_bytes((p/folder/name).read_bytes()+b'\nchanged\n')
                    inner = json.loads((p/folder/'MANIFEST.json').read_bytes()); b=(p/folder/name).read_bytes()
                    inner['files'][name]={'bytes':len(b),'sha256':sha(b)}
                    (p/folder/'MANIFEST.json').write_text(json.dumps(inner))
                    for path in (folder+'/'+name,folder+'/MANIFEST.json'):
                        b=(p/path).read_bytes(); m['files'][path]={'bytes':len(b),'sha256':sha(b)}
                (p/'RELEASE_MANIFEST.json').write_text(json.dumps(m))
            try: verify(p,replay=False)
            except (ValueError,KeyError,OSError): pass
            else: raise RuntimeError('accepted actual corruption: '+case)
    return cases

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    result = verify(root)
    if '--self-test' in sys.argv:
        result['release_mutations_rejected'] = corruptions(root)
    print(json.dumps(result,indent=2,sort_keys=True))
