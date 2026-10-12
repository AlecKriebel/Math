#!/usr/bin/env python3
"""Close only this independently authored audit family; retain every own file."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

OWN = Path(__file__).resolve().parent
A = OWN.parent
R = A.parents[2]
TARGET = OWN / 'FIRST_PARTY_MANIFEST.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    if TARGET.exists() or TARGET.is_symlink():
        raise ValueError('Audit already closed; inspect rather than recycle')
    files, directories = [], set()
    for f in sorted(OWN.rglob('*')):
        n = f.relative_to(OWN).as_posix()
        p = PurePosixPath(n)
        if f.is_symlink() or {'.git', '__pycache__', '..'}.intersection(p.parts):
            raise ValueError('Unsafe owned member')
        if f.is_dir():
            directories.add(n)
            continue
        if not f.is_file() or not stat.S_ISREG(f.stat().st_mode):
            raise ValueError('Special owned member')
        raw = f.read_bytes()
        files.append({'path': n, 'bytes': len(raw), 'sha256': sha(raw)})
    expected_dirs = {q.as_posix() for z in files for q in PurePosixPath(z['path']).parents
                     if q.as_posix() != '.'}
    if directories != expected_dirs:
        raise ValueError('Unexpected empty owned directory')
    result = json.loads((OWN / 'RESULT.json').read_bytes())
    if result['verdict'] != 'MANDATORY_ADMINISTRATIVE_SOURCE_REPAIRS_BEFORE_EXECUTION':
        raise ValueError('Wrong source-only disposition')
    original = A / 'acceptance_preparation_family/PREPARATION_MANIFEST.json'
    if sha(original.read_bytes()) != result['reviewed_preparation_manifest_sha256']:
        raise ValueError('Original closed preparation changed')
    external_foreign = json.loads((OWN / 'FOREIGN_DEPENDENCIES.json').read_bytes())['individual_files']
    if len(external_foreign) != 46 or len({z['path'] for z in external_foreign}) != 46:
        raise ValueError('Individual foreign dependency count')
    for z in external_foreign:
        f = R / z['path']
        raw = f.read_bytes()
        if len(raw) != z['bytes'] or sha(raw) != z['sha256']:
            raise ValueError('Foreign dependency changed')
    obj = {'schema': 'pr41-independent-source-adversary-exact-first-party-closure/v1',
           'status': 'CLOSED_INDEPENDENT_ACCEPTANCE_SOURCE_ADVERSARY',
           'closed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'administrative_closure_actual_pid': os.getpid(),
           'self_excluded': ['FIRST_PARTY_MANIFEST.json'],
           'files_count': len(files), 'files': files,
           'directories_count': len(directories), 'directories': sorted(directories),
           'foreign_members_within_family': [],
           'individual_external_foreign_dependencies_excluded_from_authored_copy': external_foreign,
           'foreign_external_dependencies_count': 46, 'foreign_prefix_exclusions': [],
           'all_authored_files_mode': '0444',
           'source_pins_in': 'SOURCE_PINS_AND_READ_COVERAGE.json',
           'input_full_byte_reads_in': 'READ_LEDGER.json',
           'complete_typed_JSON_nodes_in': 'COMPLETE_TYPED_NODES.jsonl',
           'report_sha256': sha((OWN / 'REPORT.md').read_bytes()),
           'result_sha256': sha((OWN / 'RESULT.json').read_bytes()),
           'reviewed_preparation_manifest_sha256': result['reviewed_preparation_manifest_sha256'],
           'original_packet_unchanged': True,
           'verdict': result['verdict'], 'mandatory_administrative_repairs': 3,
           'candidate_helpers_imported_compiled_or_executed': False,
           'future_runtime_PASS_claimed': False,
           'scientific_reexecution_claimed': False,
           'review_completion_estimate_percent': 100,
           'actual_acceptance_execution_estimate_percent': 0,
           'unconditional_discovery_estimate_percent': 0,
           'original_substantive_attempts': 2, 'turn_limit': 5,
           'new_substantive_attempts': 0, 'audit_turns': 0,
           'external_human_contact': False, 'paper_or_new_DOI_or_tracker': False}
    for z in files:
        (OWN / z['path']).chmod(0o444)
    with TARGET.open('xb') as stream:
        stream.write((json.dumps(obj, indent=2) + '\n').encode())
        stream.flush()
        os.fsync(stream.fileno())
    TARGET.chmod(0o444)
    for z in files:
        f = OWN / z['path']
        raw = f.read_bytes()
        if len(raw) != z['bytes'] or sha(raw) != z['sha256'] or f.stat().st_mode & 0o7777 != 0o444:
            raise ValueError('Final owned member mismatch')
    print(json.dumps({'status': obj['status'], 'actual_closure_pid': os.getpid(),
                      'files_count': len(files), 'directories_count': len(directories),
                      'manifest_sha256': sha(TARGET.read_bytes()),
                      'verdict': result['verdict'], 'mandatory_administrative_repairs': 3,
                      'review_completion_estimate_percent': 100,
                      'unconditional_discovery_estimate_percent': 0}, indent=2))


if __name__ == '__main__':
    main()
