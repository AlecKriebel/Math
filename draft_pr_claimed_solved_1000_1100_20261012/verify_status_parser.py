"""Reproduce the independent gate checks and the reported parser regression."""
import datetime
import hashlib
import json
from pathlib import Path

from intake import queue_rows

HERE = Path(__file__).resolve().parent

def main():
    inv = json.loads((HERE / 'inventory.json').read_text())
    content = (HERE / 'queue_remote_main.md').read_bytes()
    assert hashlib.sha256(content).hexdigest() == inv['queue_sha256']
    rows = queue_rows(content.decode())
    assert [p['number'] for p in inv['prs']] == list(range(1000, 1101))
    checks = []
    for pr in inv['prs']:
        actual = rows[pr['problem_id']]['status']
        assert rows[pr['problem_id']]['canonical_width']
        assert actual == pr['queue_status'] == 'queued'
        assert pr['state'] == 'OPEN' and pr['isDraft']
        assert pr['disposition'] == 'skip_status'
        checks.append({'pr': pr['number'], 'problem_id': pr['problem_id'], 'status': actual})
    edge = json.loads((HERE / 'reviews/status_gate_01/parser_edge_case.json').read_text())
    try:
        queue_rows(edge['row'])
    except ValueError:
        spoof_rejected = True
    else:
        raise AssertionError('Malformed unescaped-pipe row must fail closed')
    second = json.loads((HERE / 'reviews/status_gate_01/parser_second_edge_case.json').read_text())
    try:
        queue_rows(second['synthetic_row'])
    except ValueError:
        second_spoof_rejected = True
    else:
        raise AssertionError('Shifted prefix columns must fail closed')
    # Correctly escaped pipes stay inside a Problem cell and cannot supply Status.
    escaped = r'| 1 | 123 / TEST | Text \| claimed_solved \| 0/5 | 0.1 | 5.5 | 3 | unknown | queued | 0/5 | | | |'
    assert queue_rows(escaped)['123']['status'] == 'queued'
    # An ordinary eligible row continues to be recognized.
    ordinary = '| 1 | 123 / TEST | Text | 0.1 | 5.5 | 3 | unknown | claimed_solved | 1/5 | | | |'
    assert queue_rows(ordinary)['123']['status'] == 'claimed_solved'
    # Even a fully valid-looking duplicate prefix cannot enter the gate: target
    # rows must have exactly the header's width. Wider rows require clarification.
    duplicate_schema = '| 1 | 123 / TEST | Text | 0.1 | 5.5 | 3 | unknown | claimed_solved | 1/5 | | 0.1 | 5.5 | 3 | unknown | queued | 0/5 | | | |'
    assert not queue_rows(duplicate_schema)['123']['canonical_width']
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'all_101_dispositions_reproduced': True, 'spoof_rejected': spoof_rejected,
               'second_spoof_rejected': second_spoof_rejected,
               'duplicate_schema_refused_by_width_gate': True,
               'escaped_title_status_preserved': True, 'ordinary_claimed_solved_recognized': True,
               'reviewed_pr_mathematics': False, 'checks': checks}
    (HERE / 'status_parser_verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'checks'}, indent=2))

if __name__ == '__main__':
    main()
