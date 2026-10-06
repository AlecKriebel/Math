#!/usr/bin/env python3
"""Fully verify original PR48 bindings and reproduce literal and current inputs privately."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sqlite3
import stat
import sys
from capture import capture, ref

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent
AUDIT = FAMILY.parent
REPO = AUDIT.parents[2]
HEAD = 'e2e5c8c3e5ad218f867fa753c465bb96b3687bda'
MERGE_BASE = '60292bed09f59236aa192cb17aa138f7b4750e1a'
ORIGINAL_MF = '278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, obj):
    (FAMILY / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def strict_load(data):
    def pairs(rows):
        out = {}
        for key, value in rows:
            assert key not in out, ('duplicate key', key)
            out[key] = value
        return out
    return json.loads(data, object_pairs_hook=pairs)


def typed(value):
    if isinstance(value, dict):
        return ('dict', tuple(sorted((key, typed(val)) for key, val in value.items())))
    if isinstance(value, list):
        return ('list', tuple(typed(val) for val in value))
    return (type(value).__name__, value)


def run_git(name, args):
    cap = capture(name, ['git'] + args, REPO)
    return (FAMILY / 'captures' / name / 'stdout.bin').read_bytes(), cap


def main():
    started = datetime.now(timezone.utc).isoformat()
    mf_path = AUDIT / 'ORIGINAL_PREPARATION_MANIFEST.json'
    mf_bytes = mf_path.read_bytes()
    assert sha(mf_bytes) == ORIGINAL_MF
    mf = strict_load(mf_bytes)
    assert mf['files_count'] == 574 and mf['self_excluded'] == ['ORIGINAL_PREPARATION_MANIFEST.json']
    body_reads = []
    for row in mf['files']:
        path = AUDIT / row['path']
        assert path.is_file() and not path.is_symlink()
        body = path.read_bytes()
        mode = stat.S_IMODE(path.stat().st_mode)
        assert len(body) == row['bytes'] and sha(body) == row['sha256'] and mode == row['full_mode'] == 0o444
        body_reads.append(dict(row))
    expected_files = {row['path'] for row in mf['files']}
    expected_dirs = {row['path']: row['full_mode'] for row in mf['owned_directory_bindings']}
    discovered_files, discovered_dirs = set(), {}
    for root in mf['authorship_directory_roots']:
        directory = AUDIT / root
        assert directory.is_dir() and not directory.is_symlink()
        for path in [directory] + sorted(directory.rglob('*')):
            assert not path.is_symlink()
            relative = path.relative_to(AUDIT).as_posix()
            if path.is_dir():
                discovered_dirs[relative] = stat.S_IMODE(path.stat().st_mode)
            else:
                assert path.is_file()
                discovered_files.add(relative)
    for name in mf['authorship_root_files']:
        discovered_files.add(name)
    assert discovered_files == expected_files and discovered_dirs == expected_dirs
    assert stat.S_IMODE(mf_path.stat().st_mode) == 0o444
    captures = []
    for row in mf['complete_prior_actual_captures']:
        cp = AUDIT / row['path']
        obj = strict_load(cp.read_bytes())
        assert obj['argv'] == row['argv'] and obj['cwd'] == row['cwd']
        assert obj['exit_code'] == row['exit_code']
        a = datetime.fromisoformat(row['started_utc'])
        b = datetime.fromisoformat(row['finished_utc'])
        assert a.utcoffset().total_seconds() == 0 and b >= a
        captures.append({'path': row['path'], 'exit_code': obj['exit_code'], 'full_body_checked': True})
    assert len(captures) == 103

    snap = strict_load((AUDIT / 'snapshot_manifest.json').read_bytes())
    original_copy = FAMILY / 'original_science'
    original_copy.mkdir(exist_ok=False)
    scientific_reads = []
    git_caps = []
    for i, row in enumerate(snap['files']):
        body, cap = run_git('original_science_%02d_body' % i, ['show', HEAD + ':' + row['path']])
        tree, treecap = run_git('original_science_%02d_tree' % i, ['ls-tree', HEAD, '--', row['path']])
        literal = (AUDIT / 'source_snapshot' / row['relative_path']).read_bytes()
        assert body == literal and len(body) == row['bytes'] and sha(body) == row['sha256']
        assert tree.decode() == row['git_mode'] + ' blob ' + row['git_object'] + '\t' + row['path'] + '\n'
        target = original_copy / row['relative_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        scientific_reads.append(dict(row))
        git_caps.extend([cap, treecap])
    assert len(scientific_reads) == 17
    diff, diffcap = run_git('original_whole_diff', ['diff', '--binary', '--no-ext-diff', MERGE_BASE, HEAD, '--'])
    assert diff == (AUDIT / 'original_diff.patch').read_bytes()
    assert len(diff) == 80679 and sha(diff) == '994b4bbd4993227d1100cbd9d7493de776c6619c9daa379dca7f4ef3b3a26698'
    git_caps.append(diffcap)
    mb, mbcap = run_git('actual_merge_base', ['merge-base', 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0', HEAD])
    assert mb.decode().strip() == MERGE_BASE
    git_caps.append(mbcap)
    sections = diff.split(b'diff --git ')[1:]
    assert len(sections) == 18
    science_hunks = []
    for section in sections:
        first = section.splitlines()[0]
        path = first.split(b' b/', 1)[1].decode()
        if path.endswith('/QUEUE.md'):
            (FAMILY / 'ORIGINAL_QUEUE_DIFF.txt').write_bytes(b'diff --git ' + section)
            continue
        row = next(row for row in scientific_reads if row['path'] == path)
        added = b''.join(line[1:] + b'\n' for line in section.splitlines() if line.startswith(b'+') and not line.startswith(b'+++'))
        assert added == (original_copy / row['relative_path']).read_bytes()
        science_hunks.append(path)
    assert len(science_hunks) == 17

    notes_old = (FAMILY / 'captures/historical_partial/stdout.bin').read_bytes()
    assert sha(notes_old) == '0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2'
    notes_final = (original_copy / 'PARTIAL.md').read_bytes()
    pending = b'Separate adversarial review is pending.'
    passed = b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.'
    assert notes_old.count(pending) == 1 and notes_old.replace(pending, passed) == notes_final
    receipt_old = (original_copy / 'check_results.json').read_bytes()
    assert receipt_old == (original_copy / 'review/author_replay/check_results.json').read_bytes()
    assert (original_copy / 'check_algebra.py').read_bytes() == (original_copy / 'review/author_replay/check_algebra.py').read_bytes()
    replays = []
    for name, source, notes in [
            ('literal_author_old_input', original_copy / 'check_algebra.py', notes_old),
            ('literal_submitted_old_input', original_copy / 'review/author_replay/check_algebra.py', notes_old),
            ('final_author_current_input', original_copy / 'check_algebra.py', notes_final)]:
        private = FAMILY / 'private_replays' / name
        private.mkdir(parents=True, exist_ok=False)
        script = private / 'check_algebra.py'
        script.write_bytes(source.read_bytes())
        (private / 'PARTIAL.md').write_bytes(notes)
        cap = capture(name, ['/usr/bin/python3', '-B', str(script)], private, source=script)
        actual = (private / 'check_results.json').read_bytes()
        saved_obj, actual_obj = strict_load(receipt_old), strict_load(actual)
        assert actual_obj['assertions'] == 6570 and type(actual_obj['assertions']) is int
        assert type(actual_obj['all_passed']) is bool and actual_obj['all_passed'] is True
        if name != 'final_author_current_input':
            assert actual == receipt_old and typed(actual_obj) == typed(saved_obj)
        else:
            assert actual != receipt_old
            saved_obj['partial_sha256'] = sha(notes_final)
            assert typed(actual_obj) == typed(saved_obj)
        assert (FAMILY / 'captures' / name / 'stdout.bin').read_bytes() == actual
        replays.append({'name': name, 'capture': cap, 'result': actual_obj,
                        'exact_saved_receipt_bytes': name != 'final_author_current_input',
                        'input_note_sha256': sha(notes), 'result_ref': ref(private / 'check_results.json')})
    private = FAMILY / 'private_replays/historical_independent'
    private.mkdir(parents=True, exist_ok=False)
    script = private / 'independent_checks.py'
    script.write_bytes((original_copy / 'review/independent_checks.py').read_bytes())
    cap = capture('historical_independent', ['/usr/bin/python3', '-B', str(script)], private, source=script)
    actual = (FAMILY / 'captures/historical_independent/stdout.bin').read_bytes()
    expected = (original_copy / 'review/independent_results.json').read_bytes()
    assert actual == expected and typed(strict_load(actual)) == typed(strict_load(expected))
    assert strict_load(actual)['assertions'] == 228 and type(strict_load(actual)['assertions']) is int
    replays.append({'name': 'historical_independent', 'capture': cap, 'result': strict_load(actual),
                    'exact_saved_receipt_bytes': True, 'scope': 'Historical additional checker, distinct from author duplicate.'})
    turns = [strict_load(line) for line in (original_copy / 'turns.jsonl').read_bytes().splitlines()]
    assert len(turns) == 2 and [turn['turn'] for turn in turns] == [1, 2]
    assert all(type(turn['turn']) is int for turn in turns)
    readiness = strict_load((original_copy / 'readiness.json').read_bytes())
    assert readiness['used_substantive_attempts'] == 2 and readiness['maximum_substantive_attempts'] == 5
    write('ORIGINAL_REPRODUCTION_RESULT.json', {
        'schema': 'pr48-algebra-family-complete-original-reproduction/v1', 'status': 'PASS_EXACT_ORIGINAL_AND_QUALIFIED_FINAL_INPUT',
        'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(), 'actual_pid': os.getpid(),
        'original_manifest': ref(mf_path), 'original_complete_file_reads': body_reads,
        'original_complete_directory_checks': expected_dirs, 'all_original_103_capture_bodies_checked': captures,
        'scientific_full_reads': scientific_reads, 'full_diff': {'bytes': len(diff), 'sha256': sha(diff)},
        'all_17_added_science_hunks_byte_exact': True, 'whole_diff_paths': 18, 'actual_fixed_git_children': git_caps,
        'original_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_turns': 0, 'audit_turns': 0,
        'original_ledger_kind': 'JSONL', 'original_turns': turns, 'replays': replays,
        'author_duplicate_is_not_independent_evidence': True,
        'old_and_final_notes_differ_by_exact_review_status_sentence_only': True,
        'saved_old_receipt_is_not_final_note_hash': True, 'full_target_resolved': False,
        'mathematical_acceptance': 'PENDING_FAMILY_REVIEW', 'future_ROOT_merge_approval': False})
    print(json.dumps({'status': 'PASS', 'actual_pid': os.getpid(), 'original_owned_files': 574,
                      'original_directories': len(expected_dirs), 'original_actual_captures': len(captures),
                      'fixed_git_children': len(git_caps), 'replays': 4, 'counts': [6570, 6570, 6570, 228]}, indent=2))


if __name__ == '__main__':
    main()
