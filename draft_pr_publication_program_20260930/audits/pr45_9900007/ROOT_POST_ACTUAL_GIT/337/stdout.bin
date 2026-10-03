"""Read every original byte and receipt structurally, without executing mathematical helpers."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

A = Path(__file__).resolve().parent
S = A / 'source_snapshot'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def pairs(items):
    out = {}
    for k, v in items:
        assert k not in out, ('duplicate JSON key', k)
        out[k] = v
    return out

def parse(b):
    return json.loads(b, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def write(name, body):
    assert len(body) < 100 * 1024 * 1024
    with (A / name).open('xb') as f:
        f.write(body)
        f.flush()
        os.fsync(f.fileno())

def main():
    source = Path(__file__).read_bytes()
    write('ORIGINAL_INSPECTION_PRELAUNCH_SOURCE.py', source)
    m = parse((A / 'snapshot_manifest.json').read_bytes())
    rows = m['files']
    assert len(rows) == 18
    texts, objects, receipts = {}, {}, []
    for r in rows:
        p = S / r['relative_path']
        b = p.read_bytes()
        assert len(b) == r['bytes'] and sha(b) == r['sha256']
        assert not p.is_symlink() and stat.S_IMODE(p.stat().st_mode) == 0o444
        texts[r['relative_path']] = b.decode('utf-8')
        if p.suffix == '.json':
            objects[r['relative_path']] = parse(b)
        elif p.suffix == '.jsonl':
            objects[r['relative_path']] = [parse(line) for line in b.splitlines() if line.strip()]
        receipts.append({'relative_path': r['relative_path'], 'complete_bytes_read': len(b),
                         'sha256': sha(b), 'full_mode': stat.S_IMODE(p.stat().st_mode)})
    # Reconstruct every added file from the complete whole-repository diff.
    diff = (A / 'original_diff.patch').read_bytes()
    chunks = diff.split(b'diff --git ')[1:]
    assert len(chunks) == 19
    reconstructed = []
    for c in chunks[1:]:
        lines = c.splitlines(keepends=True)
        expected = lines[0].decode().strip().split(' b/', 1)[1]
        assert expected.startswith('unsolved_math_prioritization/attempts/9900007/')
        rel = expected.split('/9900007/', 1)[1]
        assert b'new file mode 100644\n' in lines
        hunk = next(i for i, line in enumerate(lines) if line.startswith(b'@@ '))
        assert all(line.startswith(b'+') for line in lines[hunk+1:])
        body = b''.join(line[1:] for line in lines[hunk+1:])
        assert body == (S / rel).read_bytes()
        reconstructed.append(rel)
    assert set(reconstructed) == {r['relative_path'] for r in rows}
    assert texts['PARTIAL.md'] == texts['review/PARTIAL.md']
    assert texts['verify_binary_process.py'] == texts['review/verify_binary_process.py']
    assert texts['binary_verification.json'] == texts['review/submitted_results.json']
    status = objects['status.json']
    assert status['status'] == 'unsolved' and status['full_source_solved'] is False
    assert status['new_discovery_claim'] is False and status['novelty'] == 'unestablished'
    assert status['turns_used'] == 1 and status['turn_limit'] == 5
    assert len(objects['turns.jsonl']) == 1 and objects['turns.jsonl'][0]['turn'] == 1
    assert objects['turns.jsonl'][0]['outcome'] == 'partial'
    assert sha((S / 'PARTIAL.md').read_bytes()) == status['artifact_sha256']
    assert sha((S / 'verify_binary_process.py').read_bytes()) == status['verifier_sha256']
    assert sha((S / 'review/REVIEW.md').read_bytes()) == status['review_sha256']
    author = objects['binary_verification.json']
    assert type(author['exact_assertions']) is int and author['exact_assertions'] == 885
    assert type(author['window_cases']) is int and author['window_cases'] == 42
    assert author['transition_products'] == 240 and len(author['window_receipts']) == 42
    assert [(r['n'], r['r']) for r in author['window_receipts']] == [(n, r) for n in (0, 1, 2, 5, 10, 50) for r in range(7)]
    assert all(set(r) == {'n', 'r', 'tv', 'no_flip'} and type(r['tv']) is str and type(r['no_flip']) is str for r in author['window_receipts'])
    # Complete expected label set from the inspected independent helper; these
    # are receipt-shape checks only, not re-evaluation of its mathematical predicates.
    expected = set()
    for n in range(1, 10):
        expected.update(('mass_%d' % n, 'fair_last_%d' % n))
        for mm in range(n):
            expected.add('max_finite_history_correlation_%d_%d' % (n, mm))
            expected.update('conditional_%d_%d_%d' % (n, mm, j) for j in range(2**(mm+1)))
    for n in range(4, 10):
        for mask in range(16):
            expected.update('%s_%d_%d' % (name, n, mask) for name in ('anticipative_B_fair', 'anticipative_tower', 'anticipative_mismatch'))
    for n in range(6):
        for r in range(5):
            expected.update(('window_TV_%d_%d' % (n, r), 'no_flip_window_%d_%d' % (n, r)))
    for idx in range(64):
        for b in (-1, 1):
            expected.add('metric_pointwise_%d_%d' % (idx, b))
    expected.update('offset_bound_%d_%d' % (n, s) for n in range(40) for s in range(9))
    expected.update('offset_union_sum_%d' % mm for mm in range(40))
    expected.update('double_time_gap_%d' % n for n in range(1, 80))
    independent = objects['review/independent_results.json']
    assert independent['passed'] == len(expected) == 3044 and independent['failed'] == 0
    assert set(independent['checks']) == expected and all(type(v) is str and v == 'PASS' for v in independent['checks'].values())
    assert independent['reviewed_sha256'] == status['artifact_sha256']
    assert objects['review/verdict.json']['mandatory_corrections'] == []
    assert objects['review/verdict.json']['full_characterization_resolved'] is False
    assert objects['source_record.json']['problem']['id'] == 9900007
    assert objects['source_record.json']['problem']['problem_number'] == 'AMR-098-0007'
    record = {'schema': 'pr45-original-complete-byte-and-typed-receipt-inspection/v1',
       'actual_pid': os.getpid(), 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
       'original_manifest_sha256': sha((A / 'snapshot_manifest.json').read_bytes()),
       'original_files_read_in_full': 18, 'original_bytes_read': sum(r['complete_bytes_read'] for r in receipts),
       'all_original_file_receipts': receipts, 'complete_original_JSON_and_JSONL_objects': objects,
       'full_diff_bytes_read': len(diff), 'full_diff_sha256': sha(diff),
       'all_18_added_hunks_reconstructed_and_byte_exact': True, 'whole_diff_changed_files': 19,
       'independent_receipt_all_3044_labels_and_values_inspected': True,
       'author_receipt_all_42_windows_inspected': True,
       'helper_execution_performed': False, 'mathematical_predicates_reproduced': False,
       'universal_coupling_proof_independently_certified': False, 'acceptance_verdict': None,
       'fresh_foreign_primary_content_read': False, 'foreign_body_publication': False,
       'original_substantive_turns': 1, 'new_substantive_turns': 0, 'audit_consumes_turns': 0}
    write('ORIGINAL_COMPLETE_READ_RECEIPT.json', (json.dumps(record, indent=2, sort_keys=True) + '\n').encode())
    assert Path(__file__).read_bytes() == source
    print(json.dumps({k: record[k] for k in ('original_files_read_in_full', 'original_bytes_read',
       'full_diff_bytes_read', 'all_18_added_hunks_reconstructed_and_byte_exact', 'helper_execution_performed',
       'mathematical_predicates_reproduced', 'acceptance_verdict', 'original_substantive_turns')}, sort_keys=True))

if __name__ == '__main__':
    main()
