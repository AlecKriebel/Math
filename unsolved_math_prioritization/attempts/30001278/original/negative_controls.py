#!/usr/bin/env python3
"""Bounded fail-closed packet checks, using only authored dummy mutations."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from hashlib import sha256
import json
import shutil
import tempfile
import importlib.util
_spec = importlib.util.spec_from_file_location("ramification_verify", Path(__file__).resolve().parent / "verify.py")
verify = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify)


def run():
    root = Path(__file__).resolve().parent
    verify.verify_integrity(root)
    digest = sha256((root / 'MANIFEST.json').read_bytes()).hexdigest()
    passed = []
    def trial(name, mutate, anchored=False):
        with tempfile.TemporaryDirectory(prefix='ramification-negative-') as temp:
            dest = Path(temp) / 'packet'
            shutil.copytree(root, dest)
            mutate(dest)
            try:
                verify.verify_integrity(dest, digest if anchored else None)
            except (RuntimeError, ValueError, TypeError, KeyError, OSError):
                passed.append(name)
            else:
                raise RuntimeError('Mutation was accepted: ' + name)
    def edit_manifest(dest, change):
        file = dest / 'MANIFEST.json'
        data = json.loads(file.read_text())
        change(data)
        file.write_text(json.dumps(data, indent=2) + '\n')
    trial('changed_authored_bytes', lambda d: (d/'README.md').write_text('mutated\n'))
    trial('same_size_changed_bytes', lambda d: (d/'README.md').write_bytes(b'!' + (d/'README.md').read_bytes()[1:]))
    trial('missing_authored_file', lambda d: (d/'NORMALIZATIONS.md').unlink())
    trial('unlisted_pdf', lambda d: (d/'source.pdf').write_bytes(b'%PDF-dummy-boundary-fixture'))
    trial('unlisted_source_extract', lambda d: (d/'source.txt').write_text('authored dummy fixture'))
    trial('unlisted_nested_manifest', lambda d: ((d/'nested').mkdir(), (d/'nested/MANIFEST.json').write_text('{}')))
    trial('file_symlink', lambda d: ((d/'README.md').unlink(), (d/'README.md').symlink_to(d/'SOURCE_MAP.md')))
    trial('duplicate_file_entry', lambda d: edit_manifest(d, lambda x: x['files'].append(x['files'][0])))
    trial('duplicate_json_key', lambda d: (d/'MANIFEST.json').write_text((d/'MANIFEST.json').read_text().replace('{', '{"schema":"duplicate",', 1)))
    trial('absolute_manifest_path', lambda d: edit_manifest(d, lambda x: x['files'][0].update(path='/tmp/not-a-packet-file')))
    trial('traversal_manifest_path', lambda d: edit_manifest(d, lambda x: x['files'][0].update(path='../README.md')))
    trial('boolean_byte_count', lambda d: edit_manifest(d, lambda x: x['files'][0].update(bytes=True)))
    trial('wrong_byte_count', lambda d: edit_manifest(d, lambda x: x['files'][0].update(bytes=x['files'][0]['bytes']+1)))
    trial('malformed_fingerprint', lambda d: edit_manifest(d, lambda x: x['files'][0].update(sha256='A'*64)))
    trial('wrong_problem_binding', lambda d: edit_manifest(d, lambda x: x.update(problem_id=1)))
    trial('solved_disposition', lambda d: edit_manifest(d, lambda x: x.update(disposition='solved')))
    def coordinated_change(dest):
        file = dest/'README.md'; file.write_text(file.read_text()+'\nChanged by a dummy fixture.\n')
        b=file.read_bytes()
        def change(x):
            for entry in x['files']:
                if entry['path']=='README.md': entry.update(bytes=len(b),sha256=sha256(b).hexdigest())
        edit_manifest(dest, change)
    trial('coordinated_rehash_against_external_anchor', coordinated_change, anchored=True)
    return {'result':'PASS_BOUNDED_NEGATIVE_CONTROLS', 'count':len(passed), 'rejected':passed,
            'scope':'Packet inventory, hash, schema and external-anchor checks; not a mathematical proof or malicious-code sandbox.'}


if __name__ == '__main__':
    result = run()
    expected_path = Path(__file__).resolve().parent/'NEGATIVE_RESULTS.json'
    expected = verify.strict_json(expected_path)
    verify.require(result == expected, 'retained negative results differ')
    print(json.dumps(result, indent=2, sort_keys=True))
