"""One-time, reviewable correction of acceptance prose displaced into Chat.

Uses actual header names. Default creates evidence and a candidate only; --apply
requires the exact archived preimage. No state/history, research or network writes.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
QUEUE = REPO / 'unsolved_math_prioritization/QUEUE.md'
IDS = ('10000062', '2800102', '10400115', '30003713', '7000019',
       '30004186', '30003955', '10000043')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    lines = data.decode().splitlines(keepends=True)
    headers = [x for x in lines if x.startswith('| Rank | ID / code |')]
    assert len(headers) == 1, 'Ambiguous queue header'
    names = [x.strip() for x in headers[0].strip().strip('|').split('|')]
    assert len(names) == len(set(names)) == 12
    assert set(('ID / code', 'Chat', 'Findings', 'Status', 'Turns', 'DOI')) <= set(names)
    rows = {}
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = line.rstrip('\n').split('|')
        if len(cells) != len(names) + 2:
            continue
        identity = cells[1 + names.index('ID / code')].strip().split('/')[0].strip()
        if identity.isdecimal():
            assert identity not in rows, 'Duplicate numeric queue row'
            rows[identity] = (index, cells)
    return lines, names, rows


def candidate(before):
    lines, names, rows = parse(before)
    chat = 1 + names.index('Chat')
    findings = 1 + names.index('Findings')
    changes = []
    for identity in IDS:
        index, cells = rows[identity]
        assert cells[chat].strip() and not cells[findings].strip(), 'Unexpected selected-row preimage'
        assert not cells[chat].strip().startswith(('https://', 'http://')), 'A chat link must not be moved'
        revised = cells.copy()
        revised[findings] = cells[chat]
        revised[chat] = cells[findings]
        assert all(cells[i] == revised[i] for i in range(len(cells)) if i not in (chat, findings))
        lines[index] = '|'.join(revised) + ('\n' if lines[index].endswith('\n') else '')
        changes.append({'id': identity, 'old_chat_exact_cell': cells[chat],
                        'old_findings_exact_cell': cells[findings],
                        'new_chat_exact_cell': revised[chat],
                        'new_findings_exact_cell': revised[findings]})
    after = ''.join(lines).encode()
    old_lines, _, _ = parse(before)
    selected = {rows[i][0] for i in IDS}
    assert all(a == b for i, (a, b) in enumerate(zip(old_lines, lines)) if i not in selected)
    assert len(old_lines) == len(lines)
    new_lines, new_names, new_rows = parse(after)
    assert names == new_names and rows.keys() == new_rows.keys()
    assert all(not new_rows[i][1][chat].strip() and new_rows[i][1][findings] == rows[i][1][chat] for i in IDS)
    return after, changes, names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO, text=True).strip() == 'main'
    assert not (REPO / '.git/MERGE_HEAD').exists()
    if args.apply:
        before = (HERE / 'QUEUE_BEFORE.md').read_bytes()
        assert QUEUE.read_bytes() == before, 'Live queue changed; re-audit instead of overwriting'
        after, changes, names = candidate(before)
        assert after == (HERE / 'QUEUE_CANDIDATE.md').read_bytes()
        receipt = json.loads((HERE / 'ROOT_CORRECTION_PLAN.json').read_text())
        assert receipt['before_sha256'] == sha(before) and receipt['candidate_sha256'] == sha(after)
        # Final exact-preimage check directly before the authorized single-file write.
        assert QUEUE.read_bytes() == before
        QUEUE.write_bytes(after)
        assert QUEUE.read_bytes() == after
        receipt.update(status='APPLIED', applied_utc=datetime.now(timezone.utc).isoformat())
        (HERE / 'ROOT_CORRECTION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    else:
        before = QUEUE.read_bytes()
        after, changes, names = candidate(before)
        for name, data in [('QUEUE_BEFORE.md', before), ('QUEUE_CANDIDATE.md', after)]:
            path = HERE / name
            assert not path.exists() or path.read_bytes() == data, 'Do not replace archived evidence'
            path.write_bytes(data)
        receipt = {'status': 'CANDIDATE_ONLY', 'utc': datetime.now(timezone.utc).isoformat(),
                   'main_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
                   'before_sha256': sha(before), 'candidate_sha256': sha(after),
                   'header_names': names, 'changes': changes,
                   'scope': 'Move exact eight acceptance summaries from Chat to Findings; all other cells/lines unchanged. Historical acceptance evidence remains immutable and requires additive qualification.',
                   'research_state_history_scientific_package_changes': False, 'new_proof_turns': 0}
        (HERE / 'ROOT_CORRECTION_PLAN.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'rows': len(changes),
                      'before_sha256': sha(before), 'after_sha256': sha(after)}))


if __name__ == '__main__':
    main()
