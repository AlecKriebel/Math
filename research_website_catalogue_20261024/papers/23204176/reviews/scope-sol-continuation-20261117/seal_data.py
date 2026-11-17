"""Finite own-lane seal: bytes/modes/topology only; no scientific execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204176/reviews/scope-sol-continuation-20261117')
TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(name, data):
    path = ROOT / name
    assert not path.exists(), name
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

before = json.loads((ROOT / 'CUSTODY_BEFORE.json').read_bytes())
after = json.loads((ROOT / 'CUSTODY_AFTER.json').read_bytes())
assert after['whole_before_after_exact'] is True
assert before['entries'] == after['entries']
assert (ROOT / 'CUSTODY_AFTER.stderr.txt').read_bytes() == b''
retrieval = json.loads((ROOT / 'PINNED_RETRIEVAL_INPUT.json').read_bytes())
assert retrieval['pinned_commit'] == 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
assert len(retrieval['files']) == 74
for row in retrieval['files']:
    data = (ROOT / 'primary' / row['path']).read_bytes()
    assert len(data) == row['bytes'] and digest(data) == row['sha256'], row['path']
execution = json.loads((ROOT / 'NATIVE_EXECUTION.json').read_bytes())
assert execution['invocations'] == 1 and execution['exit_code'] == 0
for stream in ('stdout', 'stderr'):
    data = (ROOT / ('NATIVE.' + stream + '.txt')).read_bytes()
    assert len(data) == execution[stream + '_bytes']
    assert digest(data) == execution[stream + '_SHA256']

classical = []
for pdf in sorted((ROOT / 'classical').glob('*.pdf')):
    data = pdf.read_bytes()
    text_path = pdf.with_suffix('.txt')
    headers = pdf.with_suffix('.headers.txt')
    assert text_path.is_file() and headers.is_file()
    classical.append({'path': pdf.relative_to(ROOT).as_posix(), 'bytes': len(data),
                      'sha256': digest(data), 'response_headers': headers.relative_to(ROOT).as_posix(),
                      'cover_text_first_45_lines': text_path.read_text().splitlines()[:45]})
assert len(classical) == 16
write_json('CLASSICAL_INPUTS.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'actual_retrieved_editions_not_a_journal_byte_identity_claim': True, 'items': classical})
write_json('FINAL.json', {'row': 191, 'record': '23204176', 'family': 'SCOPE',
           'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'decision': 'DEFER_UNCONDITIONAL_SCIENTIFIC_CLEARANCE_EVIDENCE_LIMIT',
           'confirmed_target_counterexample_or_fatal_error': False,
           'full_pinned_main_proof_read': True,
           'native_route_count': 1, 'native_exit': 0,
           'source_whole_files': 43, 'source_whole_childdirs': 7,
           'old_INITIAL_whole_files': 30, 'old_INITIAL_whole_childdirs': 0,
           'whole_source_and_old_INITIAL_preservation_exact': True,
           'pinned_primary_files_exact': 74, 'changed_pinned_bytes': 0,
           'native_version': None, 'follow_up': None,
           'bounded_review_and_packet_completion_percent': 100,
           'best_guess_independent_full_validation_coverage_percent': 70,
           'scientific_report': 'SCIENTIFIC_REVIEW.md', 'exposure_ledger': 'EXPOSURE_LEDGER.md',
           'private_only': True, 'root_owns_final_disposition_and_publication': True})

for name in sorted(TERMINALS):
    with (ROOT / name).open('xb'):
        pass

entries = []
def visit(path):
    info = path.lstat()
    rel = path.relative_to(ROOT).as_posix()
    row = {'path': rel, 'mode_octal': oct(stat.S_IMODE(info.st_mode)),
           'hidden_component': any(part.startswith('.') and part != '.' for part in Path(rel).parts)}
    if stat.S_ISDIR(info.st_mode):
        children = sorted(path.iterdir(), key=lambda p: os.fsencode(p.name))
        row.update(kind='directory', empty=not children, mtime_ns=info.st_mtime_ns)
        entries.append(row)
        for child in children:
            visit(child)
    else:
        assert stat.S_ISREG(info.st_mode), rel
        if rel in TERMINALS:
            row.update(kind='file', terminal_control=True,
                       hash_exclusion='this exact terminal file only; recursive hash avoided')
        else:
            data = path.read_bytes()
            row.update(kind='file', bytes=len(data), sha256=digest(data), mtime_ns=info.st_mtime_ns)
        entries.append(row)
visit(ROOT)
files = sum(r['kind'] == 'file' for r in entries)
dirs = sum(r['kind'] == 'directory' for r in entries)
manifest = {'schema': 'finite-own-namespace-with-explicit-terminal-entries-v1',
            'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'root': str(ROOT),
            'entries': entries, 'files_including_terminals': files,
            'child_directories': dirs - 1, 'root_directory_included': True,
            'exact_recursive_hash_exclusions': sorted(TERMINALS),
            'no_hidden_or_empty_object_exclusions': True}
manifest_path = ROOT / 'FINAL_MANIFEST.json'
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
seal = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'root': str(ROOT), 'manifest_sha256': digest(manifest_path.read_bytes()),
        'FINAL_json_sha256': digest((ROOT / 'FINAL.json').read_bytes()),
        'scientific_report_sha256': digest((ROOT / 'SCIENTIFIC_REVIEW.md').read_bytes()),
        'source_before_after_snapshot_sha256': digest((ROOT / 'CUSTODY_AFTER.json').read_bytes()),
        'files_including_two_terminals': files, 'child_directories': dirs - 1,
        'actual_terminal_files': [{'path': n, 'kind': 'file',
                                  'mode_octal': oct(stat.S_IMODE((ROOT / n).lstat().st_mode))}
                                 for n in sorted(TERMINALS)],
        'exact_recursive_hash_exclusions': sorted(TERMINALS),
        'whole_original_source_and_INITIAL_preserved': True,
        'bounded_review_and_packet_completion_percent': 100,
        'best_guess_independent_full_validation_coverage_percent': 70,
        'follow_up': None, 'quiescent_after_this_seal': True}
seal_path = ROOT / 'FINAL_SEAL.json'
seal_path.write_text(json.dumps(seal, indent=2, sort_keys=True) + '\n')

actual_paths = {'.'} | {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')}
assert actual_paths == {row['path'] for row in entries}
for row in entries:
    path = ROOT if row['path'] == '.' else ROOT / row['path']
    info = path.lstat()
    assert oct(stat.S_IMODE(info.st_mode)) == row['mode_octal']
    if row['kind'] == 'directory':
        assert stat.S_ISDIR(info.st_mode)
        assert (not any(path.iterdir())) == row['empty']
        assert info.st_mtime_ns == row['mtime_ns']
    elif not row.get('terminal_control'):
        data = path.read_bytes()
        assert len(data) == row['bytes'] and digest(data) == row['sha256']
        assert info.st_mtime_ns == row['mtime_ns']
assert digest(manifest_path.read_bytes()) == seal['manifest_sha256']
print(json.dumps({'files': files, 'childdirs': dirs - 1,
                  'manifest_sha256': seal['manifest_sha256'],
                  'FINAL_sha256': seal['FINAL_json_sha256'],
                  'seal_sha256': digest(seal_path.read_bytes()), 'quiescent': True}))
