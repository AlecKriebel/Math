#!/usr/bin/env python3
"""Pinned PR946 operation core. No action runs merely by importing this file.

The invoking interpreter, standard library, git/gh/gws executables and externally
supplied inventory/freeze pins are trust roots. File authentication and copied
code execution are provenance checks, not an operating-system sandbox.
"""
import sys
if not (sys.flags.isolated or getattr(sys.flags, 'safe_path', False)):
    raise RuntimeError('Invoke with Python -I or -P before importing any nonbuiltin module')
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
from datetime import datetime, timezone
import zipfile

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P / 'audits/pr946_6000001'
D = A / 'preprint'
HEAD = '7d3adb0e500b0414a49a449e7981d34ade329427'
KEY = '6000001'
PR = 946
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
STATE = 'unsolved_math_prioritization/state.json'
HISTORY = 'unsolved_math_prioritization/history.jsonl'
CATALOG = 'unsolved_math_prioritization/catalog.json'
RELATED = 'unsolved_math_prioritization/review_v2/related_target_groups.json'
PREFIX = 'unsolved_math_prioritization/attempts/' + KEY + '/'
SID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
HELPERS = ['accept_pr946.py', 'merge_pr946.py', 'run_pr946_zenodo.py',
           'append_pr946_tracker.py', 'update_pr946_publication_ledger.py',
           'finalize_pr946_and_gate_next.py']
KIT = 'zenodo_deposit_tool/zenodo.py'
STATEMENT = '04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd'
REVIEW = 'f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb'
DISPOSITION = 'PREPARE_FULLY_CREDITED_GLOBAL_HESSIAN_CONSTRUCTION_NOTE'
MAX_FILE = 128 * 1024 * 1024


def need(ok, label):
    if not ok:
        raise RuntimeError('PR946 guard: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe(name):
    return (type(name) is str and bool(name) and '\\' not in name and '\0' not in name
            and not PurePosixPath(name).is_absolute()
            and PurePosixPath(name).as_posix() == name
            and all(x not in ('', '.', '..') for x in name.split('/')))


def strict_json(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            need(k not in result, 'duplicate JSON key')
            result[k] = v
        return result
    def bad(value):
        raise RuntimeError('Nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def fingerprint(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}


def validate_pin(pin):
    need(type(pin) is dict and set(pin) == {'bytes', 'sha256'}
         and type(pin['bytes']) is int and 0 <= pin['bytes'] <= MAX_FILE
         and type(pin['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}', pin['sha256']) is not None,
         'fingerprint schema/cap')


def read_regular(path, cap=MAX_FILE, pin=None):
    """Anchor every repository ancestor; reject FIFO/symlink before reading."""
    path = Path(path)
    try:
        name = path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise RuntimeError('File outside trusted repository root') from error
    need(safe(name), 'unsafe repository file name')
    if pin is not None:
        validate_pin(pin)
        cap = pin['bytes']
    need(type(cap) is int and 0 <= cap <= MAX_FILE, 'read cap')
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(ROOT, flags | os.O_DIRECTORY)
    try:
        parts = name.split('/')
        for part in parts[:-1]:
            next_fd = os.open(part, flags | os.O_DIRECTORY, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        file_fd = os.open(parts[-1], flags, dir_fd=fd)
        try:
            info = os.fstat(file_fd)
            need(stat.S_ISREG(info.st_mode) and info.st_size <= cap,
                 'nonregular or oversized file: ' + name)
            if pin is not None:
                need(info.st_size == pin['bytes'], 'file size changed: ' + name)
            chunks = []
            total = 0
            while total <= cap:
                block = os.read(file_fd, min(1024 * 1024, cap + 1 - total))
                if not block:
                    break
                chunks.append(block)
                total += len(block)
            raw = b''.join(chunks)
            need(len(raw) <= cap, 'file grew beyond cap: ' + name)
            if pin is not None:
                need(fingerprint(raw) == pin, 'file fingerprint changed: ' + name)
            return raw
        finally:
            os.close(file_fd)
    finally:
        os.close(fd)


def load(path):
    return strict_json(read_regular(path, 8 * 1024 * 1024))


def save(path, value, exclusive=False):
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW
    flags |= os.O_EXCL if exclusive else os.O_TRUNC
    name = Path(path).relative_to(ROOT).as_posix()
    need(safe(name), 'unsafe receipt path')
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK
    directory_fd = os.open(ROOT, directory_flags)
    try:
        parts = name.split('/')
        for part in parts[:-1]:
            next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        fd = os.open(parts[-1], flags | os.O_NONBLOCK, 0o600, dir_fd=directory_fd)
        with os.fdopen(fd, 'wb') as stream:
            need(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'nonregular receipt output')
            stream.write(raw)
    finally:
        os.close(directory_fd)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def utc(value):
    need(type(value) is str, 'timestamp type')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    need(result.tzinfo is not None and result.utcoffset().total_seconds() == 0,
         'timestamp must be explicit UTC')
    return result


def exact(a, b):
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)


def run(args, raw=False, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=not raw, **kwargs).stdout


def blob(ref, path):
    return run(['git', 'show', ref + ':' + path], raw=True)


def remote_main():
    ref = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
    need(re.fullmatch('[0-9a-f]{40}', ref) is not None, 'remote main hash')
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', ref])
    return ref


def queue_parts(raw, key=KEY):
    lines = raw.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if ('| ' + key + ' /').encode() in line]
    need(len(matches) == 1, 'exactly one selected queue row')
    index = matches[0]
    row = lines[index]
    return b''.join(lines[:index] + lines[index + 1:]), row, index, lines


def claimed_row(raw):
    _, row, _, _ = queue_parts(raw)
    cells = row.decode().split('|')
    need(len(cells) >= 13 and cells[8].strip() == 'claimed_solved'
         and cells[9].strip() == '4/5', 'exact claimed_solved declared4/5 gate')
    return row


def validate_inventory(mapping):
    need(type(mapping) is dict and mapping.get('schema') == 'pr946-operations-v1'
         and type(mapping.get('pr')) is int and mapping['pr'] == PR
         and mapping.get('problem_id') == KEY
         and mapping.get('original_pr_head') == HEAD, 'inventory target/schema')
    records = mapping.get('files')
    expected = {P.relative_to(ROOT).as_posix() + '/' + name for name in HELPERS} | {KIT}
    need(type(records) is dict and set(records) == expected, 'entire seven-file operations inventory required')
    for name, pin in records.items():
        need(safe(name), 'inventory path')
        validate_pin(pin)
        need(0 < pin['bytes'] <= 4 * 1024 * 1024, 'operational dependency size cap')
    return records


def capture_inventory(external_pin):
    need(type(external_pin) is str and re.fullmatch('[0-9a-f]{64}', external_pin) is not None,
         'external operations-inventory pin required')
    raw = read_regular(A / 'OPERATIONS_INVENTORY.json', 1024 * 1024)
    need(sha(raw) == external_pin, 'externally pinned operations inventory changed')
    mapping = strict_json(raw)
    records = validate_inventory(mapping)
    captured = {name: read_regular(ROOT / name, pin=pin) for name, pin in records.items()}
    return {'inventory_sha256': external_pin, 'inventory': mapping, 'captured': captured}


def freeze_check(raw, external_pin, context, base=D, historical=False):
    need(sha(raw) == external_pin, 'external freeze pin changed')
    freeze = strict_json(raw)
    need(type(freeze.get('pr')) is int and freeze['pr'] == PR
         and freeze.get('problem_id') == KEY and freeze.get('original_pr_head') == HEAD,
         'freeze target')
    need(type(freeze.get('revision_candidate')) is int and freeze['revision_candidate'] >= 1
         and freeze.get('replay_normalization_ignored') == [], 'candidate revision and no implicit replay normalization')
    inv_pin = freeze.get('operations_inventory_sha256')
    if historical:
        old_raw = read_regular(base / 'OPERATIONS_INVENTORY.json', 1024 * 1024)
        need(sha(old_raw) == inv_pin, 'historical inventory pin')
        records = validate_inventory(strict_json(old_raw))
        for name, pin in records.items():
            read_regular(base / 'operations' / name, pin=pin)
    else:
        need(inv_pin == context['inventory_sha256'], 'freeze/inventory mismatch')
        records = context['inventory']['files']
    helper_pins = {name: records[P.relative_to(ROOT).as_posix() + '/' + name] for name in HELPERS}
    need(exact(freeze.get('future_helpers'), helper_pins), 'frozen entire helper inventory mismatch')
    files = freeze.get('files')
    need(type(files) is dict and bool(files) and 'FREEZE.json' not in files,
         'freeze closed file map')
    mandatory = {'research_note.pdf', 'research_note.tex', 'global_hessian_verification.zip',
                 'zenodo-deposit.json', 'package/verify_package.py', 'BUILD_RECEIPT.json',
                 *['PACKAGE_REPLAY_' + name + '.json' for name in ['normal', 'O', 'OO', 'env2']]}
    need(mandatory <= set(files), 'required frozen paper/archive/replay artifacts')
    for name, pin in files.items():
        need(safe(name), 'frozen relative path')
        read_regular(base / name, pin=pin)
    evidence = freeze.get('evidence_files')
    required = {str((A / name).relative_to(ROOT)) for name in
                ['ORIGINAL_SNAPSHOT.json', 'TARGET_IDENTITY_PREFLIGHT.json', 'PRIORITY_DISPOSITION.json']}
    need(type(evidence) is dict and required <= set(evidence), 'frozen external evidence inventory')
    for name, pin in evidence.items():
        need(safe(name), 'evidence relative path')
        # Root evidence is historical and immutable across manuscript revisions.
        read_regular(ROOT / name, pin=pin)
    return freeze


def disposition_check():
    decision = load(A / 'PRIORITY_DISPOSITION.json')
    need(decision.get('disposition') == DISPOSITION and decision.get('pr') == PR
         and str(decision.get('problem_id')) == KEY
         and decision.get('original_head') == HEAD
         and decision.get('original_status') == 'claimed_solved'
         and decision.get('original_declared_turns') == '4/5'
         and decision.get('original_native_turn_events_authenticated') is False
         and decision.get('audit_proof_search_turns_added') == 0,
         'bounded-priority disposition or honest native accounting changed')
    return decision


def source_gate(parent):
    source = load(A / 'TARGET_IDENTITY_PREFLIGHT.json')
    need(source.get('id') == KEY and source.get('review_hash') == REVIEW
         and source.get('statement_hash') == STATEMENT, 'frozen source preflight changed')
    catalog = strict_json(blob(parent, CATALOG))
    targets = [r for r in catalog if str(r.get('id')) == KEY]
    need(len(targets) == 1, 'current selected source missing/ambiguous')
    target = targets[0]
    need(target.get('present') is True and target.get('holds') == []
         and target.get('statement_hash') == STATEMENT
         and target.get('review_hash') == REVIEW, 'current source identity/readiness holds')
    groups = strict_json(blob(parent, RELATED)).get('groups')
    need(type(groups) is list, 'related-membership schema')
    membership = {str(i): g for i, g in enumerate(groups) if KEY in [str(x) for x in g.get('ids', [])]}
    need(exact(membership, source.get('related_target_groups')), 'selected related-target membership changed')
    return {'utc': utc_now(), 'remote_main': parent, 'present': True, 'holds': [],
            'statement_hash': STATEMENT, 'review_hash': REVIEW,
            'related_target_membership': membership}


def original_check(ref=HEAD):
    snapshot = load(A / 'ORIGINAL_SNAPSHOT.json')
    need(snapshot.get('head') == HEAD and type(snapshot.get('files')) is dict
         and len(snapshot['files']) == 33, 'immutable33 original inventory')
    expected = {}
    for name, pin in snapshot['files'].items():
        need(safe(name) and name.startswith(PREFIX), 'original scope')
        actual = blob(ref, name)
        disk = read_regular(A / 'original' / name)
        need(sha(actual) == pin and disk == actual, 'original actual Git/disk bytes changed')
        entry = run(['git', 'ls-tree', ref, '--', name]).strip().split(None, 3)
        git_blob = hashlib.sha1(b'blob ' + str(len(actual)).encode() + b'\0' + actual).hexdigest()
        need(len(entry) == 4 and entry[:3] == ['100644', 'blob', git_blob], 'original actual Git blob/mode')
        need(stat.S_IMODE((A / 'original' / name).lstat().st_mode) == 0o644,
             'original disk mode changed')
        expected[name] = {'bytes': len(actual), 'sha256': pin, 'git_blob': git_blob,
                          'git_mode': '100644', 'disk_mode': '0644'}
    return snapshot, expected


def archive_check(freeze, expected, base=D):
    raw = read_regular(base / 'global_hessian_verification.zip',
                       pin=freeze['files']['global_hessian_verification.zip'])
    layout = freeze.get('archive_layout')
    need(type(layout) is dict and set(layout) == {'manifest', 'package_manifest', 'original_prefix', 'pdf', 'verifier'},
         'explicit archive layout')
    need(all(type(v) is str and safe(v.rstrip('/')) for v in layout.values())
         and layout['original_prefix'].endswith('/'), 'safe archive layout')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)), 'duplicate archive members')
        inventory_raw = archive.read(layout['manifest'])
        need(sha(inventory_raw) == freeze['archive_manifest_sha256'], 'outer archive manifest pin')
        inventory = strict_json(inventory_raw)
        records = inventory.get('files')
        need(type(records) is dict and set(names) == set(records) | {layout['manifest']},
             'closed outer archive inventory')
        for info in archive.infolist():
            need(safe(info.filename) and stat.S_ISREG(info.external_attr >> 16)
                 and info.file_size <= MAX_FILE, 'nonregular/unsafe/oversized archive member')
            if info.filename in records:
                validate_pin(records[info.filename])
                need(fingerprint(archive.read(info)) == records[info.filename], 'archive payload pin')
        need(sha(archive.read(layout['package_manifest'])) == freeze['package_manifest_sha256'],
             'inner package manifest pin')
        for name, pin in expected.items():
            member = layout['original_prefix'] + name[len(PREFIX):]
            info = archive.getinfo(member)
            need((info.external_attr >> 16) == (stat.S_IFREG | 0o644)
                 and fingerprint(archive.read(member)) == {'bytes': pin['bytes'], 'sha256': pin['sha256']},
                 'original archive bytes/modes')
        need(archive.read(layout['pdf']) == read_regular(base / 'research_note.pdf'),
             'separate and archived paper differ')
    built = load(base / 'BUILD_RECEIPT.json')
    need(type(built.get('payload_files')) is int and built['payload_files'] == len(records)
         and type(built.get('zip_members')) is int and built['zip_members'] == len(names),
         'build inventory counts')
    return built


def validate_review_sequence(specs):
    need(type(specs) is list and len(specs) >= 2, 'at least two sequential NEW full reviews required')
    for index, spec in enumerate(specs, 1):
        need(type(spec) is str and re.fullmatch(f'{index:02d}:[0-9a-f]{{64}}', spec) is not None,
             'canonical consecutive complete externally pinned review sequence')


def review_check(specs, freeze, freeze_pin, context, expected):
    validate_review_sequence(specs)
    results = []
    prior_ids = set()
    last_end = None
    reviewer_ids = set()
    for spec in specs:
        number, pin = spec.split(':')
        folder = A / 'reviews' / ('full_package_' + number)
        raw = read_regular(folder / 'MANIFEST.json', 1024 * 1024)
        need(sha(raw) == pin, 'external review seal changed')
        mapping = strict_json(raw)
        records = mapping.get('files')
        mandatory = {'RESULT.json', 'FULL_AUDIT.md', 'RESEARCH_LOG.md',
                     'AUTHENTICATION_START.json', 'AUTHENTICATION_END.json', 'COLD_REPLAY.json'}
        allowed = mapping.get('explicit_public_allowlist')
        need(type(records) is dict and mandatory <= set(records)
             and type(allowed) is list and len(allowed) == len(set(allowed))
             and set(allowed) == set(records) and 'MANIFEST.json' not in records,
             'complete explicit review inventory')
        captured = {}
        for name, record in records.items():
            need(safe(name), 'review relative path')
            captured[name] = read_regular(folder / name, pin=record)
        for name in mandatory:
            need(bool(captured[name].decode().strip()), 'empty mandatory review evidence')
            if name.endswith('.json'):
                need(type(strict_json(captured[name])) is dict and bool(strict_json(captured[name])),
                     'empty mandatory review JSON object')
            else:
                need(any(c.isalpha() for c in captured[name].decode()), 'audit/log has no text')
        result = strict_json(captured['RESULT.json'])
        need(type(result.get('pr')) is int and result['pr'] == PR
             and result.get('problem_id') == KEY and result.get('original_pr_head') == HEAD
             and result.get('clean_context') is True and result.get('full_reproducer_completed') is True,
             'NEW full review target/context/reproduction')
        reviewer = result.get('reviewer_agent_id')
        need(type(reviewer) is str and reviewer and reviewer not in reviewer_ids,
             'each NEW full review must identify a distinct reviewer')
        reviewer_ids.add(reviewer)
        start, end = utc(result['started_utc']), utc(result['completed_utc'])
        need(start < end and (last_end is None or last_end < start), 'nonsequential review chronology')
        last_end = end
        pins = result['candidate_pins']
        review_base = D
        review_freeze = freeze
        if pins['freeze'] != freeze_pin:
            revision = result['candidate_revision']
            need(type(revision) is int and revision >= 1, 'prior candidate revision')
            review_base = D / 'reviewed_candidates' / ('candidate' + str(revision).zfill(2))
            review_freeze = freeze_check(read_regular(review_base / 'FREEZE.json'), pins['freeze'],
                                         context, review_base, historical=True)
        need(pins['manifest'] == review_freeze['package_manifest_sha256']
             and pins['pdf'] == review_freeze['files']['research_note.pdf']['sha256']
             and exact(result['inspected_helper_hashes'], review_freeze['future_helpers']),
             'review candidate and inspected helper pins')
        built = archive_check(review_freeze, expected, review_base)
        times = []
        for name in ['AUTHENTICATION_START.json', 'AUTHENTICATION_END.json']:
            auth = strict_json(captured[name])
            need(auth.get('status') == 'PASS' and auth.get('original_pr_head') == HEAD
                 and auth.get('freeze_sha256') == pins['freeze']
                 and auth.get('package_manifest_sha256') == pins['manifest']
                 and exact(auth.get('future_helpers'), review_freeze['future_helpers'])
                 and exact(auth.get('candidate_files'), review_freeze['files'])
                 and type(auth.get('payloads')) is int and auth['payloads'] == built['payload_files']
                 and type(auth.get('archive_members')) is int and auth['archive_members'] == built['zip_members'],
                 'review authentication identity/inventory')
            originals = auth.get('originals')
            need(type(originals) is dict and set(originals) == set(expected), 'incomplete original authentication')
            for path, want in expected.items():
                item = originals[path]
                need(type(item) is dict and all(type(item.get(k)) is type(v) and item.get(k) == v for k, v in want.items())
                     and item.get('archive_mode') == '100644' and item.get('disk_and_archive_match') is True,
                     'original actual Git/disk/archive authentication')
            times.append(utc(auth['utc']))
        need(start <= times[0] <= times[1] <= end, 'authentication outside review interval')
        cold = strict_json(captured['COLD_REPLAY.json'])
        need(cold.get('status') == 'PASS' and cold.get('cold_extraction') is True
             and cold.get('typed_float_policy_verified') is True
             and cold.get('historical_strict_failure_preserved') is True
             and cold.get('package_manifest_sha256') == pins['manifest']
             and cold.get('externally_pinned_verifier_sha256') == review_freeze['files'][review_freeze['archive_layout']['verifier']]['sha256']
             and exact(cold.get('normalized_fields_ignored', []), review_freeze.get('replay_normalization_ignored', []))
             and times[0] <= utc(cold['utc']) <= times[1], 'cold replay pins/typed comparison/history/chronology')
        modes = cold.get('modes')
        need(type(modes) is list and len(modes) == 4, 'four actual outer replay modes')
        for row, label, optimization in zip(modes, ['normal', 'O', 'OO', 'env2'], [0, 1, 2, 2]):
            need(row.get('mode') == label and type(row.get('observed_outer_optimization')) is int
                 and row['observed_outer_optimization'] == optimization
                 and type(row.get('returncode')) is int and row['returncode'] == 0, 'actual outer optimization evidence')
            replay = row.get('receipt')
            saved = load(review_base / ('PACKAGE_REPLAY_' + label + '.json'))
            need(exact(replay, saved) and replay.get('status') == 'PASS'
                 and type(replay.get('pr')) is int and replay['pr'] == PR
                 and replay.get('problem_id') == KEY and replay.get('package_manifest_sha256') == pins['manifest']
                 and type(replay.get('original_files_unchanged')) is int and replay['original_files_unchanged'] == 33
                 and type(replay.get('worker_optimization')) is int and replay['worker_optimization'] == 0,
                 'canonical cold replay mathematical receipts')
        required, optional = result.get('required_issues'), result.get('optional_issues')
        need(type(required) is list and type(optional) is list, 'required/optional findings lists')
        issues = required + optional
        need(all(type(x) is dict and type(x.get('id')) is str and x['id'] for x in issues), 'finding IDs')
        results.append({'round': int(number), 'manifest_sha256': pin, 'completed_utc': result['completed_utc'],
                        'required_repairs': required, 'optional_improvements': optional,
                        'public_files_authenticated': len(records)})
        if spec != specs[-1]:
            prior_ids.update(x['id'] for x in issues)
    need(result['candidate_pins']['freeze'] == freeze_pin and result.get('clean_for_preprint') is True
         and result['required_issues'] == [] and result['optional_issues'] == []
         and result.get('mathematical_remaining_gap_for_stated_theorem', 'MISSING') is None,
         'latest complete review must clear exact current package with no findings')
    need(type(result.get('strongest_verified_theorem')) is str
         and bool(result['strongest_verified_theorem'].strip()), 'exact accepted theorem must be nonempty prose')
    resolutions = result.get('prior_issue_resolution', {})
    need(all(type(resolutions.get(i)) is dict and resolutions[i].get('verified') is True for i in prior_ids),
         'every prior required and optional issue needs verified resolution')
    return results, result


def pr_view():
    return strict_json(run(['gh', 'pr', 'view', str(PR), '--repo', 'AlecKriebel/Math', '--json',
                            'number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,url,mergeCommit,mergedAt']))


def main_destination(pr, merged=False):
    need(type(pr.get('number')) is int and pr['number'] == PR
         and pr.get('baseRefName') == 'main' and pr.get('headRefOid') == HEAD,
         'live actual PR/head/main destination')
    if merged:
        need(pr.get('state') == 'MERGED' and type(pr.get('mergeCommit')) is dict
             and re.fullmatch('[0-9a-f]{40}', pr['mergeCommit'].get('oid', '')) is not None,
             'confirmed actual merged destination')
    else:
        need(pr.get('state') == 'OPEN', 'PR must still be open')


def premerge_gate(freeze, require_draft=False):
    pr = pr_view()
    main_destination(pr)
    if require_draft:
        need(pr.get('isDraft') is True, 'acceptance requires still-draft PR')
    need(type(pr.get('body')) is str and sha(pr['body'].encode()) == freeze['pr_description_sha256'],
         'reviewed live PR description changed')
    parent = remote_main()
    source = source_gate(parent)
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', HEAD])
    snapshot, originals = original_check()
    claimed_row(blob(HEAD, QUEUE))
    base = run(['git', 'merge-base', HEAD, parent]).strip()
    need(queue_parts(blob(base, QUEUE))[0] == queue_parts(blob(HEAD, QUEUE))[0],
         'original PR changes another queue row')
    changed = run(['gh', 'api', f'repos/AlecKriebel/Math/pulls/{PR}/files', '--paginate', '--jq', '.[].filename']).splitlines()
    need(set(changed) <= set(snapshot['files']) | {QUEUE}, 'live PR changes unrelated paths')
    return pr, parent, source, originals


def accepted_package(context):
    accepted = load(A / 'ACCEPTANCE.json')
    need(accepted.get('accepted') is True and accepted.get('pr') == PR
         and accepted.get('problem_id') == KEY and accepted.get('original_pr_head') == HEAD
         and accepted.get('operations_inventory_sha256') == context['inventory_sha256']
         and len(accepted.get('full_package_reviews', [])) >= 2
         and accepted.get('all_prior_required_and_optional_findings_resolved') is True
         and accepted.get('proof_gap', 'MISSING') is None, 'exact complete package acceptance')
    freeze = freeze_check(read_regular(D / 'FREEZE.json'), accepted['freeze_sha256'], context)
    need(exact(accepted['files'], freeze['files']) and exact(accepted['future_helpers'], freeze['future_helpers']),
         'accepted file/helper inventory')
    disposition_check()
    return accepted, freeze


def merged_gate(accepted, freeze):
    saved = load(A / 'PR_MERGE_RECEIPT.json')
    main_destination(saved, merged=True)
    live = pr_view()
    main_destination(live, merged=True)
    need(live['mergeCommit'] == saved['mergeCommit'], 'fresh merged commit differs')
    commit = live['mergeCommit']['oid']
    parent = remote_main()
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', commit])
    run(['git', 'merge-base', '--is-ancestor', commit, parent])
    source = source_gate(parent)
    original_check(commit)
    parents = run(['git', 'show', '-s', '--format=%P', commit]).split()
    need(len(parents) == 2 and parents[1] == HEAD, 'ordinary exact-head two-parent merge')
    need(queue_parts(blob(parents[0], QUEUE))[0] == queue_parts(blob(commit, QUEUE))[0],
         'merge changed another queue row')
    claimed_row(blob(commit, QUEUE))
    return {'utc': utc_now(), 'baseRefName': 'main', 'actual_PR_readback': live,
            'merge_commit': commit, 'observed_remote_main': parent,
            'merge_commit_is_ancestor_of_observed_main': True, 'source_gate': source}


def accept(args, context):
    need(not (A / 'ACCEPTANCE.json').exists(), 'existing acceptance: inspect rather than overwrite')
    need(type(args.freeze) is str and re.fullmatch('[0-9a-f]{64}', args.freeze) is not None,
         'external freeze pin required')
    freeze = freeze_check(read_regular(D / 'FREEZE.json'), args.freeze, context)
    disposition_check()
    pr, parent, source, originals = premerge_gate(freeze, require_draft=True)
    archive_check(freeze, originals)
    reviews, latest = review_check(args.review, freeze, args.freeze, context, originals)
    # Review-chain authentication must not substitute for a fresh final gate.
    pr, parent, source, _ = premerge_gate(freeze, require_draft=True)
    value = {'utc': utc_now(), 'accepted': True, 'pr': PR, 'problem_id': KEY,
             'original_pr_head': HEAD, 'live_gate_status': 'claimed_solved',
             'original_declared_turns': '4/5', 'native_turns_used_to_record': 4,
             'author_native_history_authenticated': False, 'original_total_attempt_count_known': False,
             'proof_search_turns_added_by_audit': 0,
             'turn_count_status': 'original_PR_declared_four_native_event_history_unavailable',
             'operations_inventory_sha256': context['inventory_sha256'],
             'freeze_sha256': args.freeze, 'files': freeze['files'], 'future_helpers': freeze['future_helpers'],
             'package_manifest_sha256': freeze['package_manifest_sha256'],
             'exact_claim': latest['strongest_verified_theorem'], 'proof_gap': None,
             'priority': 'Bounded primary audit; fully credited construction; firstness/novelty/current openness unestablished',
             'full_package_reviews': reviews, 'all_prior_required_and_optional_findings_resolved': True,
             'AI_assisted': True, 'unrefereed': True, 'independent_human_peer_review': False,
             'formal_machine_proof_certification': False, 'merge_and_publication_authorized_by_user': True}
    save(A / 'FINAL_ACCEPTANCE_GATE.json', {'utc': utc_now(), 'pr': {k: v for k, v in pr.items() if k != 'body'},
                                           'remote_main': parent, 'source_gate': source,
                                           'actual33_Git_disk_archive_preserved': True,
                                           'original_declared_turns': '4/5', 'native_events_authenticated': False})
    save(A / 'ACCEPTANCE.json', value, exclusive=True)
    print(json.dumps({'accepted': True, 'freeze_sha256': args.freeze, 'reviews': len(reviews), 'original_files': 33}))


def merge(args, context):
    accepted, freeze = accepted_package(context)
    pr = pr_view()
    if pr.get('state') != 'MERGED':
        need(not (A / 'PR_MERGE_INTENT.json').exists(), 'prior merge intent: read back uncertain outcome before any retry')
        pr, parent, source, _ = premerge_gate(freeze)
        save(A / 'PR_MERGE_INTENT.json', {'utc': utc_now(), 'expected_head': HEAD,
             'accepted_freeze_sha256': accepted['freeze_sha256'], 'pre_action': pr,
             'remote_main': parent, 'source_gate': source, 'blind_retry_permitted': False}, exclusive=True)
        if pr['isDraft']:
            ready = subprocess.run(['gh', 'pr', 'ready', str(PR), '--repo', 'AlecKriebel/Math'],
                                   cwd=ROOT, capture_output=True, text=True)
            save(A / 'PR_READY_ACTION.json', {'utc': utc_now(), 'returncode': ready.returncode,
                 'stdout': ready.stdout, 'stderr': ready.stderr})
            need(ready.returncode == 0, 'ready action uncertain/failed: inspect saved action')
        # Refresh all target and destination gates after the ready mutation.
        premerge_gate(freeze)
        result = subprocess.run(['gh', 'pr', 'merge', str(PR), '--repo', 'AlecKriebel/Math',
                                 '--merge', '--match-head-commit', HEAD], cwd=ROOT,
                                capture_output=True, text=True)
        save(A / 'PR_MERGE_ACTION.json', {'utc': utc_now(), 'returncode': result.returncode,
             'stdout': result.stdout, 'stderr': result.stderr})
        pr = pr_view()
        save(A / 'PR_MERGE_ACTION_READBACK.json', pr)
        main_destination(pr, merged=True)
    else:
        main_destination(pr, merged=True)
    save(A / 'PR_MERGE_RECEIPT.json', pr)
    destination = merged_gate(accepted, freeze)
    save(A / 'MERGED_PACKET_INTEGRITY.json', {**destination, 'all33_original_files_byte_identical': True,
         'all_other_queue_bytes_preserved': True, 'original_declared_turns': '4/5',
         'shared_checkout_index_head_untouched': True})
    print(json.dumps({'state': 'MERGED', 'merge_commit': pr['mergeCommit']['oid'], 'original_files': 33}))


def descriptor_check(freeze):
    descriptor = load(D / 'zenodo-deposit.json')
    need(set(descriptor) == {'metadata', 'files'} and type(descriptor['metadata']) is dict,
         'exact kit descriptor schema')
    files = descriptor['files']
    need(type(files) is list and len(files) == 2
         and {x.get('path') for x in files} == {'research_note.pdf', 'global_hessian_verification.zip'},
         'only accepted PDF and verification archive may upload')
    expected = []
    for item in files:
        need(type(item) is dict and set(item) == {'path', 'name'} and safe(item['path'])
             and type(item['name']) is str and safe(item['name']) and '/' not in item['name'], 'kit file entry')
        pin = freeze['files'][item['path']]
        read_regular(D / item['path'], pin=pin)
        expected.append({'name': item['name'], 'size': pin['bytes'], 'sha256': pin['sha256']})
    need(len({x['name'] for x in expected}) == 2, 'distinct upload names')
    metadata = descriptor['metadata']
    need(metadata.get('upload_type') == 'publication' and metadata.get('publication_type') == 'preprint'
         and metadata.get('creators') == [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                                           'orcid': '0009-0001-9320-500X'}],
         'author/preprint metadata')
    return descriptor, expected


def runtime_upload_copy(freeze):
    """Stable private manifest path keeps kit stage/publish state linked."""
    runtime = A / 'operations_runtime'
    runtime.mkdir(mode=0o700, exist_ok=True)
    need(runtime.is_dir() and not runtime.is_symlink()
         and stat.S_IMODE(runtime.stat().st_mode) == 0o700, 'private runtime directory')
    for name in ['zenodo-deposit.json', 'research_note.pdf', 'global_hessian_verification.zip']:
        pin = freeze['files'][name]
        raw = read_regular(D / name, pin=pin)
        target = runtime / name
        try:
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
        except FileExistsError:
            read_regular(target, pin=pin)
        else:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
            read_regular(target, pin=pin)
    return runtime / 'zenodo-deposit.json'


def zenodo(args, context):
    accepted, freeze = accepted_package(context)
    destination = merged_gate(accepted, freeze)
    descriptor, expected = descriptor_check(freeze)
    action = args.action
    intent_path = D / ('ZENODO_' + action.upper() + '_INTENT.json')
    if action in ('stage', 'publish'):
        need(not intent_path.exists(), 'prior Zenodo action intent: inspect/reconcile, never blindly repeat')
    command = [action]
    ident = None
    if action == 'publish':
        stage = load(D / 'ZENODO_STAGE.json')
        ident = stage.get('id')
        need(type(ident) is int and ident > 0 and stage.get('state') == 'ready_to_publish'
             and exact(stage.get('files'), expected), 'exact staged record/files required')
        command += ['--confirm-id', str(ident)]
    if action == 'inspect':
        command += ['--check-doi']
    runtime = runtime_upload_copy(freeze)
    # argparse accepts positional manifest before optional action flags.
    kit_args = [action, str(runtime)] + command[1:]
    intent = {'utc': utc_now(), 'action': action, 'pr': PR, 'original_pr_head': HEAD,
              'accepted_freeze_sha256': accepted['freeze_sha256'],
              'operations_inventory_sha256': context['inventory_sha256'],
              'descriptor_sha256': freeze['files']['zenodo-deposit.json']['sha256'],
              'repository_kit_sha256': context['inventory']['files'][KIT]['sha256'],
              'runtime_manifest': str(runtime.relative_to(ROOT)),
              'merged_commit': destination['merge_commit'], 'merged_base': 'main',
              'destination_readback': destination, 'blind_retry_permitted': False}
    save(intent_path, intent, exclusive=action in ('stage', 'publish'))
    source = context['captured'][KIT]
    bootstrap = ('import sys; p=sys.argv[1]; sys.argv=sys.argv[1:]; '
                 'g={"__name__":"__main__","__file__":p,"__package__":None}; '
                 'exec(compile(sys.stdin.buffer.read(),p,"exec",dont_inherit=True,optimize=0),g)')
    result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', bootstrap,
                             str(ROOT / KIT), *kit_args], cwd=ROOT, input=source, capture_output=True)
    if result.returncode != 0:
        save(D / ('ZENODO_' + action.upper() + '_FAILURE.json'),
             {**intent, 'returncode': result.returncode, 'stdout': result.stdout.decode(errors='replace'),
              'stderr': result.stderr.decode(errors='replace'), 'instruction': 'Inspect saved exact-ID state; no write retry.'})
        raise RuntimeError('Zenodo action unconfirmed: inspect recorded failure without repeating write')
    receipt = strict_json(result.stdout)
    need(receipt.get('environment') == 'production' and receipt.get('title') == descriptor['metadata']['title']
         and exact(receipt.get('files'), expected), 'kit verified exact metadata title/environment/files')
    if action in ('publish', 'inspect') and receipt.get('state') == 'published':
        record_id = receipt.get('id')
        need(type(record_id) is int and record_id > 0
             and receipt.get('doi') == f'10.5281/zenodo.{record_id}'
             and receipt.get('record_url') == f'https://zenodo.org/records/{record_id}', 'published exact DOI/record ID')
    if action == 'publish':
        need(receipt.get('state') == 'published' and receipt.get('id') == ident,
             'publication must confirm exact staged ID')
    if action == 'stage':
        need(receipt.get('state') == 'ready_to_publish' and type(receipt.get('id')) is int
             and receipt['id'] > 0, 'staged exact ID absent')
    save(D / ('ZENODO_' + action.upper() + '.json'), receipt)
    print(json.dumps({'action': action, 'id': receipt.get('id'), 'state': receipt.get('state'), 'doi': receipt.get('doi')}))


def valid_tracker_range(value):
    if type(value) is not str:
        return False
    match = re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1", value)
    return match is not None and int(match[1]) >= 2


def publication_links(accepted, freeze, tracker=None, native=None):
    descriptor, expected = descriptor_check(freeze)
    stage = load(D / 'ZENODO_STAGE.json')
    publication = load(D / 'ZENODO_PUBLISH.json')
    inspection = load(D / 'ZENODO_INSPECT.json')
    ident = publication.get('id')
    need(type(ident) is int and ident > 0, 'published integer ID')
    doi = f'10.5281/zenodo.{ident}'
    for name, record in [('stage', stage), ('publication', publication), ('inspection', inspection)]:
        need(record.get('id') == ident and exact(record.get('files'), expected)
             and record.get('title') == descriptor['metadata']['title'] and record.get('environment') == 'production',
             'staged/published/inspected metadata and file linkage: ' + name)
    need(stage.get('state') == 'ready_to_publish', 'staged state')
    for record in [publication, inspection]:
        need(record.get('state') == 'published' and record.get('doi') == doi
             and record.get('record_url') == f'https://zenodo.org/records/{ident}', 'published/inspected DOI record')
    intent = load(D / 'ZENODO_PUBLISH_INTENT.json')
    merge = load(A / 'PR_MERGE_RECEIPT.json')
    main_destination(merge, merged=True)
    destination = intent.get('destination_readback', {})
    readback = destination.get('actual_PR_readback', {})
    main_destination(readback, merged=True)
    need(intent.get('pr') == PR and intent.get('action') == 'publish'
         and intent.get('accepted_freeze_sha256') == accepted['freeze_sha256']
         and intent.get('operations_inventory_sha256') == accepted['operations_inventory_sha256']
         and intent.get('descriptor_sha256') == freeze['files']['zenodo-deposit.json']['sha256']
         and intent.get('merged_base') == 'main' and intent.get('merged_commit') == merge['mergeCommit']['oid']
         and destination.get('baseRefName') == 'main' and destination.get('merge_commit') == merge['mergeCommit']['oid']
         and destination.get('merge_commit_is_ancestor_of_observed_main') is True
         and readback.get('mergeCommit') == merge['mergeCommit']
         and re.fullmatch('[0-9a-f]{40}', destination.get('observed_remote_main', '')) is not None,
         'publication exact freeze/main/ancestry intent')
    if tracker is not None:
        need(tracker.get('confirmed') is True and tracker.get('readback_matches') is True
             and tracker.get('pr') == PR and tracker.get('problem_id') == KEY
             and tracker.get('original_pr_head') == HEAD and tracker.get('merged_head') == HEAD
             and tracker.get('merge_commit') == merge['mergeCommit']['oid'] and tracker.get('merged_base') == 'main'
             and tracker.get('accepted_freeze_sha256') == accepted['freeze_sha256']
             and tracker.get('doi') == doi and tracker.get('zenodo_record_id') == ident
             and tracker.get('spreadsheet_id') == SID and tracker.get('gid') == 1254632077
             and tracker.get('tab_title') == 'Math Puzzles' and valid_tracker_range(tracker.get('updated_range')),
             'tracker exact target/destination/receipt linkage')
        row = tracker.get('row')
        saved = load(A / 'TRACKER_READBACK.json')
        need(type(row) is list and len(row) == 4 and row[2] == 'https://doi.org/' + doi
             and saved.get('range') == tracker['updated_range'] and saved.get('values') == [row],
             'tracker exact four-column row readback')
    if native is not None:
        need(tracker is not None and native.get('push_confirmed') is True, 'native requires confirmed tracker')
        event = native.get('published_event', {})
        need(event.get('id') == KEY and event.get('pr') == PR and event.get('doi') == doi
             and event.get('original_pr_head') == HEAD and event.get('merged_base') == 'main'
             and event.get('merged_commit') == merge['mergeCommit']['oid']
             and event.get('accepted_freeze_sha256') == accepted['freeze_sha256']
             and event.get('zenodo_record_id') == ident
             and event.get('evidence', {}).get('tracker_range') == tracker['updated_range'], 'native publication linkage')
    return publication, merge


def gws(args):
    return strict_json(run(['gws', *args]))


def publication_note(publication):
    return ('6000001 / AMR-059-0001. Global Hessian realizations of statistical manifolds. '
            'A proper global realization of any smooth positive boundaryless statistical n-manifold '
            'and its ordered torsion-free dual pair in a positive Hessian open domain of dimension '
            'binomial(2n+4,3), n>=1; a general dual pair admits such a flat torsion-free ambient '
            'realization iff both input connections are torsion-free. The domain may be nonconvex '
            'and incomplete; no globally injective dual gradient, finite probability model, or optimal '
            'dimension is claimed. Fully credited construction answering the checked historical '
            'Amari/FMU question. Bounded primary priority audits establish no full predecessor; '
            'firstness, novelty and continued openness remain uncertified. Extensive AI assistance; '
            'unrefereed, no independent human review or formal proof certification. '
            'All33 original files and original declared4/5 preserved; historical native turn events '
            'unavailable, no proof-search turn added by audit. '
            'https://github.com/AlecKriebel/Math/pull/946 DOI ' + publication['doi'])


def tracker_append(args, context):
    accepted, freeze = accepted_package(context)
    merged_gate(accepted, freeze)
    publication, merge = publication_links(accepted, freeze)
    tabs = gws(['sheets', 'spreadsheets', 'get', '--params', json.dumps({'spreadsheetId': SID, 'fields': 'sheets.properties'})])
    matches = [x['properties'] for x in tabs.get('sheets', []) if x.get('properties', {}).get('sheetId') == 1254632077]
    need(len(matches) == 1 and matches[0].get('title') == 'Math Puzzles', 'exact sheet gid/title')
    table = "'Math Puzzles'!A:D"
    existing = gws(['sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({'spreadsheetId': SID, 'range': table})])
    save(A / 'tracker_existing_rows_private.json', existing)
    values = existing.get('values')
    need(type(values) is list and values and values[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'],
         'exact tracker headers')
    row = ['https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en', '',
           'https://doi.org/' + publication['doi'], publication_note(publication)]
    hits = [(i + 1, r) for i, r in enumerate(values) if any(publication['doi'] in str(v) for v in r)]
    if hits:
        need(len(hits) == 1 and hits[0][1] == row and hits[0][0] >= 2, 'existing DOI entry needs reconciliation')
        index = hits[0][0]
        updated = f"'Math Puzzles'!A{index}:D{index}"
        response = {'recovered_existing_identical_row': True}
    else:
        need(not (A / 'TRACKER_APPEND_INTENT.json').exists(), 'prior append intent without identical row: reconcile; no retry')
        params = {'spreadsheetId': SID, 'range': table, 'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS'}
        save(A / 'TRACKER_APPEND_INTENT.json', {'utc': utc_now(), 'params': params, 'row': row,
             'accepted_freeze_sha256': accepted['freeze_sha256'], 'blind_retry_permitted': False}, exclusive=True)
        response = gws(['sheets', 'spreadsheets', 'values', 'append', '--params', json.dumps(params), '--json', json.dumps({'values': [row]})])
        save(A / 'TRACKER_APPEND_RESPONSE.json', response)
        updates = response.get('updates', {})
        need(type(updates.get('updatedRows')) is int and updates['updatedRows'] == 1
             and type(updates.get('updatedCells')) is int and updates['updatedCells'] == 4, 'exact append dimensions')
        updated = updates.get('updatedRange')
    need(valid_tracker_range(updated), 'exact quoted Math Puzzles single A:D data-row range')
    readback = gws(['sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({'spreadsheetId': SID, 'range': updated})])
    save(A / 'TRACKER_READBACK.json', readback)
    need(readback.get('range') == updated and readback.get('values') == [row], 'exact tracker row readback')
    receipt = {'utc': utc_now(), 'confirmed': True, 'readback_matches': True, 'pr': PR,
               'problem_id': KEY, 'original_pr_head': HEAD, 'merged_head': HEAD,
               'merge_commit': merge['mergeCommit']['oid'], 'merged_base': 'main',
               'accepted_freeze_sha256': accepted['freeze_sha256'], 'zenodo_record_id': publication['id'],
               'spreadsheet_id': SID, 'gid': 1254632077, 'tab_title': 'Math Puzzles',
               'updated_range': updated, 'doi': publication['doi'], 'row': row,
               'append_result': response, 'cli': 'Google Workspace CLI gws'}
    save(A / 'TRACKER_RECEIPT.json', receipt)
    publication_links(accepted, freeze, receipt)
    print(json.dumps({'confirmed': True, 'updated_range': updated, 'doi': publication['doi']}))


def raw_json_members(raw):
    text = raw.decode() if type(raw) is bytes else raw
    strict_json(text)
    decoder = json.JSONDecoder()
    pos = text.index('{') + 1
    members = {}
    while True:
        while text[pos].isspace() or text[pos] == ',':
            pos += 1
        if text[pos] == '}':
            break
        start = pos
        name, pos = decoder.raw_decode(text, pos)
        need(type(name) is str and name not in members, 'state member name')
        while text[pos].isspace():
            pos += 1
        need(text[pos] == ':', 'state member colon')
        pos += 1
        while text[pos].isspace():
            pos += 1
        value_start = pos
        _, pos = decoder.raw_decode(text, pos)
        members[name] = {'literal': text[start:pos], 'value_start': value_start, 'value_end': pos}
    return members


def replace_entry(raw, key, value):
    parsed = strict_json(raw)
    members = raw_json_members(raw)
    if key in members:
        item = members[key]
        result = raw[:item['value_start']] + json.dumps(value, indent=2, ensure_ascii=False) + raw[item['value_end']:]
    else:
        index = raw.rfind('}')
        entry = json.dumps(key) + ': ' + json.dumps(value, indent=2, ensure_ascii=False)
        result = raw[:index].rstrip() + (',\n' if parsed else '\n') + entry + '\n}' + raw[index + 1:]
    changed = strict_json(result)
    need(exact(changed[key], value), 'state target replacement')
    after = raw_json_members(result)
    need({k: v['literal'] for k, v in members.items() if k != key}
         == {k: v['literal'] for k, v in after.items() if k != key}, 'another state member literal changed')
    return result


def explicit_tree(parent, replacements):
    need(set(replacements) == {QUEUE, STATE, HISTORY}, 'only three native paths')
    updates = {}
    for path, text in replacements.items():
        oid = run(['git', 'hash-object', '-w', '--stdin'], input=text).strip()
        entry = run(['git', 'ls-tree', parent, '--', path]).split()
        need(entry[0] == '100644' and entry[1] == 'blob', 'native blob mode')
        cursor = updates
        parts = path.split('/')
        for part in parts[:-1]:
            cursor = cursor.setdefault(part.encode(), {})
        cursor[parts[-1].encode()] = (b'100644', b'blob', oid.encode())
    def rebuild(old, changes):
        entries = {}
        for row in run(['git', 'ls-tree', '-z', old], raw=True).split(b'\0'):
            if row:
                header, name = row.split(b'\t', 1)
                entries[name] = tuple(header.split(b' '))
        for name, value in changes.items():
            if type(value) is dict:
                need(name in entries and entries[name][1] == b'tree', 'native tree ancestor')
                entries[name] = (entries[name][0], b'tree', rebuild(entries[name][2].decode(), value).encode())
            else:
                entries[name] = value
        payload = b''.join(b' '.join(header) + b'\t' + name + b'\0' for name, header in entries.items())
        return run(['git', 'mktree', '-z'], raw=True, input=payload).decode().strip()
    return rebuild(parent, updates)


def native_event(prior, accepted, publication, merge, tracker, note):
    need(type(prior) is dict, 'native prior state record')
    if prior.get('doi'):
        need(prior['doi'] == publication['doi'], 'prior DOI needs reconciliation')
    if 'turns_used' in prior:
        need(type(prior['turns_used']) is int and 0 <= prior['turns_used'] <= 4,
             'newer native counter requires reconciliation')
    event = {**prior, 'at': utc_now(), 'id': KEY, 'status': 'preprint_published',
             'note': note, 'doi': publication['doi'], 'pr': PR,
             'event': 'audited_imported_candidate_publication',
             'event_id': f"pr946_zenodo{publication['id']}_v1.0",
             'statement_hash': STATEMENT, 'review_hash': REVIEW,
             'turn_count_status': 'original_PR_declared_four_native_event_history_unavailable',
             'original_total_attempt_count_known': False, 'author_native_history_authenticated': False,
             'proof_search_turns_added_by_audit': 0, 'turn_limit': 5,
             'turns_used': 4, 'candidate_turn': 4, 'original_declared_turns': '4/5',
             'original_pr_head': HEAD, 'accepted_freeze_sha256': accepted['freeze_sha256'],
             'merged_commit': merge['mergeCommit']['oid'], 'merged_base': 'main',
             'zenodo_record_id': publication['id'],
             'evidence': {'accepted_artifacts': str((A / 'ACCEPTANCE.json').relative_to(ROOT)),
                          'zenodo_record': publication['record_url'], 'tracker_range': tracker['updated_range'],
                          'priority_limit': 'Firstness, novelty and current openness not established',
                          'original_candidate_turns': 'PR-declared4/5 retained; native event history unavailable; audit adds0'}}
    if 'turns_used' in prior and prior['turns_used'] != 4:
        event['previous_state_recorded_turns_used'] = prior['turns_used']
    # Never inherit an unrelated proof-turn tag or a claim of authenticated native events.
    event.pop('verified_candidate_approaches', None)
    event.pop('new_mechanism_native_receipt_sha256', None)
    event['turns_used_interpretation'] = 'Original PR-declared4/5 imported honestly; four historical CLI calls are not authenticated or recreated. Verification/publication adds0 proof responses.'
    return event


def native_write(args, context):
    need(not (A / 'NATIVE_PUBLICATION_RECEIPT.json').exists(), 'native receipt exists: inspect/read back')
    accepted, freeze = accepted_package(context)
    merged_gate(accepted, freeze)
    tracker = load(A / 'TRACKER_RECEIPT.json')
    publication, merge = publication_links(accepted, freeze, tracker)
    note = publication_note(publication) + '; tracker ' + tracker['updated_range'] + ' read back.'
    for attempt in range(1, 7):
        # A fresh exact actual destination/source/related gate on EVERY CAS parent.
        live = pr_view()
        main_destination(live, merged=True)
        need(live['mergeCommit'] == merge['mergeCommit'], 'native retry fresh merged commit differs')
        parent = remote_main()
        run(['git', 'merge-base', '--is-ancestor', merge['mergeCommit']['oid'], parent])
        source = source_gate(parent)
        queue = blob(parent, QUEUE).decode()
        _, old_raw, index, lines_raw = queue_parts(queue.encode())
        claimed_row(queue.encode())
        lines = [x.decode() for x in lines_raw]
        old = old_raw.decode()
        cells = old.rstrip('\n').split('|')
        cells[8] = ' preprint_published '
        cells[9] = ' 4/5 '
        cells[11] = ' ' + cells[11].strip() + ' ' + note.replace('|', '/') + ' '
        cells[12] = f" [{publication['doi']}](https://doi.org/{publication['doi']}) "
        lines[index] = '|'.join(cells) + ('\n' if old.endswith('\n') else '')
        revised_queue = ''.join(lines)
        need(queue_parts(queue.encode())[0] == queue_parts(revised_queue.encode())[0], 'other queue bytes changed')
        state = blob(parent, STATE).decode()
        prior = strict_json(state).get(KEY, {})
        history = blob(parent, HISTORY).decode()
        event_id = f"pr946_zenodo{publication['id']}_v1.0"
        events = [strict_json(line) for line in history.splitlines() if line.strip()]
        need(not any(x.get('event_id') == event_id for x in events), 'publication already in native history: reconcile existing commit')
        event = native_event(prior, accepted, publication, merge, tracker, note)
        revised_state = replace_entry(state, KEY, event)
        revised_history = history + ('' if not history or history.endswith('\n') else '\n') + json.dumps(event, ensure_ascii=False) + '\n'
        replacements = {QUEUE: revised_queue, STATE: revised_state, HISTORY: revised_history}
        tree = explicit_tree(parent, replacements)
        paths = run(['git', 'diff', '--name-only', parent, tree]).splitlines()
        need(set(paths) == set(replacements), 'native commit must change exactly declared paths')
        commit = run(['git', 'commit-tree', tree, '-p', parent], input='Record verified PR946 Hessian-realization preprint and honest declared-turn import\n').strip()
        intent_name = A / f'NATIVE_PUBLICATION_CAS_{attempt:02d}_INTENT.json'
        save(intent_name, {'utc': utc_now(), 'parent': parent, 'commit': commit, 'source_gate': source,
             'accepted_freeze_sha256': accepted['freeze_sha256'], 'paths': paths}, exclusive=True)
        pushed = subprocess.run(['git', 'push', 'origin', commit + ':refs/heads/main'], cwd=ROOT, capture_output=True, text=True)
        save(A / f'NATIVE_PUBLICATION_CAS_{attempt:02d}_ACTION.json', {'utc': utc_now(), 'returncode': pushed.returncode,
             'stdout': pushed.stdout, 'stderr': pushed.stderr})
        if pushed.returncode == 0:
            observed = remote_main()
            run(['git', 'merge-base', '--is-ancestor', commit, observed])
            save(A / 'NATIVE_PUBLICATION_RECEIPT.json', {'utc': utc_now(), 'parent': parent, 'commit': commit,
                 'paths': paths, 'published_event': event, 'push_confirmed': True,
                 'observed_remote_main': observed, 'other_queue_rows_and_state_entries_preserved': True,
                 'shared_checkout_index_and_local_head_untouched': True, 'attempt': attempt}, exclusive=True)
            print(json.dumps({'commit': commit, 'doi': publication['doi'], 'declared_turns': '4/5', 'audit_turns_added': 0}))
            return
        race = re.search(r"cannot lock ref 'refs/heads/main': is at ([0-9a-f]{40}) but expected ([0-9a-f]{40})", pushed.stderr)
        rejected = ('non-fast-forward' in pushed.stderr or 'fetch first' in pushed.stderr
                    or (race is not None and race[2] == parent and race[1] != parent))
        need(rejected, 'push uncertain/non-CAS failure: inspect; do not automatically repeat')
    raise RuntimeError('Six explicit main races; publication ledger pending')


def native_verify(publication, merge, tracker, accepted, native):
    commit, parent = native['commit'], native['parent']
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', commit])
    observed = remote_main()
    run(['git', 'merge-base', '--is-ancestor', commit, observed])
    run(['git', 'merge-base', '--is-ancestor', merge['mergeCommit']['oid'], commit])
    need(run(['git', 'show', '-s', '--format=%P', commit]).strip() == parent, 'native actual single parent')
    paths = run(['git', 'diff', '--name-only', parent, commit]).splitlines()
    need(set(paths) == {QUEUE, STATE, HISTORY} and paths == native['paths'], 'native actual changed paths')
    before, _, _, _ = queue_parts(blob(parent, QUEUE))
    after, row, _, _ = queue_parts(blob(commit, QUEUE))
    cells = row.decode().split('|')
    need(before == after and cells[8].strip() == 'preprint_published' and cells[9].strip() == '4/5'
         and publication['doi'] in row.decode(), 'native other queue bytes/target row')
    old_state, new_state = blob(parent, STATE), blob(commit, STATE)
    old_members, new_members = raw_json_members(old_state), raw_json_members(new_state)
    need({k: v['literal'] for k, v in old_members.items() if k != KEY}
         == {k: v['literal'] for k, v in new_members.items() if k != KEY}, 'native other state literal bytes')
    event = strict_json(new_state)[KEY]
    need(exact(event, native['published_event']) and type(event.get('turns_used')) is int
         and event['turns_used'] == 4 and event.get('candidate_turn') == 4 and event.get('turn_limit') == 5
         and event.get('original_total_attempt_count_known') is False
         and event.get('author_native_history_authenticated') is False
         and type(event.get('proof_search_turns_added_by_audit')) is int and event['proof_search_turns_added_by_audit'] == 0
         and event.get('turn_count_status') == 'original_PR_declared_four_native_event_history_unavailable',
         'native exact honest declared-counter import')
    old_history, new_history = blob(parent, HISTORY), blob(commit, HISTORY)
    need(new_history.startswith(old_history), 'native old history prefix changed')
    appended = [strict_json(s) for s in new_history[len(old_history):].splitlines() if s.strip()]
    need(exact(appended, [event]), 'native exact one appended publication event')
    claimed_row(blob(HEAD, QUEUE))
    original_check(merge['mergeCommit']['oid'])
    return {'utc': utc_now(), 'accepted_freeze_sha256': accepted['freeze_sha256'],
            'actual33_original_Git_disk_archive_preserved': True, 'actual_tracker_exact_row_readback': True,
            'native_commit_on_current_remote_main': observed, 'native_other_queue_state_history_preserved': True,
            'original_declared_turns': '4/5', 'native_turn_events_authenticated': False,
            'proof_search_turns_added_by_audit': 0, 'workflow_completion_percent': 100}


def gate_next(inventory, state):
    skipped = []
    selected = None
    for old in sorted([r for r in inventory if PR < r['number'] <= 1000], key=lambda r: r['number']):
        number = old['number']
        pr = strict_json(run(['gh', 'pr', 'view', str(number), '--repo', 'AlecKriebel/Math', '--json',
                               'number,state,isDraft,headRefOid,headRefName,baseRefName,url']))
        if pr.get('state') != 'OPEN' or pr.get('isDraft') is not True:
            skipped.append({'pr': number, 'action': 'SKIP_NOT_OPEN_DRAFT', 'math_source_read': False})
            old.update(eligible=False, disposition='skipped_not_open_draft')
            if number in state['eligible_prs'] and number not in state['completed_prs']:
                state['eligible_prs'].remove(number)
            continue
        ids = [str(x['id']) for x in old['entries']]
        need(len(ids) == 1, 'next target needs narrow metadata reconciliation')
        key = ids[0]
        queue = run(['gh', 'api', 'repos/AlecKriebel/Math/contents/' + QUEUE + '?ref=' + pr['headRefOid'],
                     '-H', 'Accept: application/vnd.github.raw+json'], raw=True)
        _, row, _, _ = queue_parts(queue, key)
        status = row.decode().split('|')[8].strip()
        if status != 'claimed_solved':
            skipped.append({'pr': number, 'problem_id': key, 'status': status, 'action': 'SKIP_STATUS_ONLY', 'math_source_read': False})
            old.update(eligible=False, disposition='skipped_status_gate')
            if number in state['eligible_prs'] and number not in state['completed_prs']:
                state['eligible_prs'].remove(number)
            continue
        need(pr.get('baseRefName') == 'main', 'next exact claimed target base changed')
        selected = {**pr, 'problem_id': key, 'status': status, 'eligible': True,
                    'gate_utc': utc_now(), 'queue_row_sha256': sha(row.rstrip(b'\r\n')),
                    'math_source_read': False, 'snapshot_not_yet_created': True}
        old.update(eligible=True, status=status)
        if number not in state['eligible_prs']:
            state['eligible_prs'].append(number)
            state['eligible_prs'].sort()
        break
    return skipped, selected


def finalize(args, context):
    accepted, freeze = accepted_package(context)
    merged_gate(accepted, freeze)
    tracker = load(A / 'TRACKER_RECEIPT.json')
    native = load(A / 'NATIVE_PUBLICATION_RECEIPT.json')
    publication, merge = publication_links(accepted, freeze, tracker, native)
    readback = gws(['sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({'spreadsheetId': SID, 'range': tracker['updated_range']})])
    need(readback.get('range') == tracker['updated_range'] and readback.get('values') == [tracker['row']],
         'fresh actual tracker exact row')
    verification = native_verify(publication, merge, tracker, accepted, native)
    save(A / 'PUBLICATION_FINAL_VERIFICATION.json', verification)
    record = {'utc': utc_now(), 'pr': PR, 'problem_id': KEY, 'outcome': 'accepted_merged_preprint_published',
              'original_pr_head': HEAD, 'merge_commit': merge['mergeCommit']['oid'],
              'doi': publication['doi'], 'record_url': publication['record_url'],
              'tracker_range': tracker['updated_range'], 'merged_base': 'main',
              'native_ledger_commit': native['commit'], 'native_ledger_readback_confirmed': True,
              'original_turns_preserved': 'Original PR-declared4/5; native per-turn history unavailable; audit adds0',
              'priority_limit': 'Fully credited construction; firstness, novelty and current openness unestablished',
              'AI_and_peer_review': 'Extensive AI assistance; unrefereed; no independent human or formal proof certification',
              'full_package_review_count': len(accepted['full_package_reviews']),
              'clean_final_review_manifest_sha256': accepted['full_package_reviews'][-1]['manifest_sha256'],
              'paper_candidate_revision': freeze['revision_candidate'],
              'all_prior_required_and_optional_findings_resolved': True}
    save(A / 'PUBLICATION_RECORD.json', record)
    body = ('Accepted and published after independent jet, global Hessian, source/model, adversarial '
            'global and reproducibility audits, three deep priority reviews, and sequential NEW '
            'whole-package adversarial reviews with every required and optional issue addressed.\n\n'
            + accepted['exact_claim'] + '\n\n'
            + '**Global Hessian realizations of statistical manifolds**, Alec Kriebel, version1.0. '
            + f"[Preprint DOI](https://doi.org/{publication['doi']}); [Zenodo record]({publication['record_url']}). "
            + 'The PDF and source/verification archive give a self-contained global construction '
            'answering the checked historical Amari/FMU question. Prior statistical frameworks, '
            'contrast constructions, finite compact models, local Hessian extensions and global '
            'constant-curvature cases are credited. Bounded primary searches did not establish a '
            'complete earlier unrestricted finite-ambient theorem. Firstness, novelty and continued '
            'openness are not certified. Actual AJLS2017 Theorems4.10 and4.11 state finite models '
            'for compact inputs and countable models in general; the full proof and several final '
            'versions remain access gaps.\n\n'
            'The ambient domain may be nonconvex and incomplete. No injective global dual gradient, '
            'finite probability model, or optimal dimension is claimed. All33 original PR files remain '
            'unchanged. Historical strict byte replay failed across Python environments; current '
            'checks preserve that failure and use an explicit twelve-field finite floating policy '
            'with exact comparison elsewhere. Finite controls supplement the proof and provide '
            'neither a priority certificate nor an operating-system sandbox.\n\n'
            'AI tools were used extensively in research, proof development, source checking, '
            'computation, writing and adversarial verification. This is an unrefereed preprint; '
            'AI-assisted review is not independent human or journal peer review, and no such review '
            'or formal proof-assistant certification is claimed. Original PR-declared4/5 is '
            'preserved; native per-turn event history is unavailable, no historical CLI events '
            'were fabricated, and the audit added zero proof-search turns.\n\n'
            + f"Exact DOI/files and tracker {tracker['updated_range']} were read back. "
            + f'Original and merged head: `{HEAD}`. Audit/publication receipts: '
            + '`draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001/`.\n')
    path = A / 'PR_PUBLISHED_BODY.md'
    path.write_text(body)
    title = '6000001: accepted global Hessian construction and published preprint'
    current = pr_view()
    main_destination(current, merged=True)
    if current.get('body') != body or current.get('title') != title:
        need(type(current.get('body')) is str
             and sha(current['body'].encode()) == freeze['pr_description_sha256'],
             'live body changed from reviewed original: reconcile before final metadata edit')
        need(not (A / 'PR_FINAL_METADATA_INTENT.json').exists(), 'prior metadata edit intent needs readback reconciliation')
        save(A / 'PR_FINAL_METADATA_INTENT.json', {'utc': utc_now(), 'title': title, 'body_sha256': sha(body.encode()),
             'merged_commit': merge['mergeCommit']['oid'], 'blind_retry_permitted': False}, exclusive=True)
        edit = subprocess.run(['gh', 'pr', 'edit', str(PR), '--repo', 'AlecKriebel/Math', '--title', title,
                               '--body-file', str(path)], cwd=ROOT, capture_output=True, text=True)
        save(A / 'PR_FINAL_METADATA_ACTION.json', {'utc': utc_now(), 'returncode': edit.returncode,
             'stdout': edit.stdout, 'stderr': edit.stderr})
    confirmed = pr_view()
    main_destination(confirmed, merged=True)
    need(confirmed['mergeCommit'] == merge['mergeCommit'] and confirmed.get('title') == title
         and confirmed.get('body') == body, 'final PR metadata exact readback')
    save(A / 'PR_PUBLISHED_METADATA.json', confirmed)
    state = load(P / 'CURRENT_STATE.json')
    already = PR in state['completed_prs']
    need(state.get('active_pr') in (PR, None) or already, 'unexpected active research target')
    if already and state.get('active_pr') not in (PR, None):
        print(json.dumps({'already_finalized': True, 'next_pr': state.get('active_pr')}))
        return
    completed = sorted([r for r in state['completed_results'] if r['pr'] != PR] + [record], key=lambda r: r['pr'])
    state.update(utc=utc_now(), completed_results=completed, completed_prs=[r['pr'] for r in completed],
                 published_prs=[r['pr'] for r in completed if r['outcome'] == 'accepted_merged_preprint_published'],
                 closed_prs=[r['pr'] for r in completed if r['outcome'].startswith('closed_')],
                 active_pr=None, active_problem_id=None, active_pr_completion_estimate_percent=0,
                 phase='next_status_gate_after_PR946')
    inventory = load(P / 'inventory.json')
    for item in inventory:
        if item['number'] == PR:
            item.update(disposition=record['outcome'], doi=publication['doi'], tracker_range=tracker['updated_range'])
    skipped, selected = gate_next(inventory, state)
    for field in ['active_original_head', 'original_candidate_turns', 'review_families',
                  'priority_families', 'publication_disposition', 'priority_status',
                  'full_package_reviews', 'active_candidate_revision', 'active_freeze_sha256',
                  'active_package_manifest_sha256', 'new_priority_research_positive_turns',
                  'known_effort_positive_turns', 'new_mechanism_status']:
        state.pop(field, None)
    if selected is not None:
        state.update(active_pr=selected['number'], active_problem_id=selected['problem_id'],
                     next_pr=selected['number'], active_original_head=selected['headRefOid'],
                     phase=f"PR{selected['number']}_exact_claimed_solved_status_only_gate_passed")
    else:
        state['next_pr'] = None
    state['shard_completion_estimate_percent'] = 100 * len(state['completed_prs']) / len(state['eligible_prs'])
    if not already:
        with (P / 'README.md').open('a') as out:
            out.write(f"\nPR #946 accepted, merged and published: [{publication['doi']}](https://doi.org/{publication['doi']}); tracker {tracker['updated_range']}. Fully credited global Hessian construction; original declared4/5 and native-history uncertainty preserved; audit adds0.\n")
        for path in [P / 'RESEARCH_LOG.md', A / 'RESEARCH_LOG.md']:
            with path.open('a') as out:
                out.write(f"\n{utc_now()} — PR946 workflow100%; shard {state['shard_completion_estimate_percent']:.2f}%. Actual merge {merge['mergeCommit']['oid']}; DOI {publication['doi']}; tracker {tracker['updated_range']}; native {native['commit']}. Exact readbacks verified; other target bytes preserved; original declared4/5/native-history uncertainty retained, zero audit proof turns.\n")
    save(P / 'CURRENT_STATE.json', state)
    save(P / 'inventory.json', inventory)
    save(P / 'POST_PR946_STATUS_GATES.json', {'utc': utc_now(), 'skipped': skipped, 'next_eligible': selected,
                                            'math_source_read': False, 'ascending_range': [947, 1000]})
    print(json.dumps({'PR946': record, 'next_pr': state.get('active_pr'), 'status_only_skips': skipped}))


def operation(action, args, context):
    need(sys.flags.optimize == 0, 'operation worker must execute nonoptimized')
    {'accept': accept, 'merge': merge, 'zenodo': zenodo, 'tracker': tracker_append,
     'native': native_write, 'finalize': finalize}[action](args, context)


def entry(action):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operations-sha256', required=True)
    if action == 'accept':
        parser.add_argument('--freeze', required=True)
        parser.add_argument('--review', action='append', required=True)
    if action == 'zenodo':
        parser.add_argument('action', choices=['stage', 'publish', 'inspect'])
    args = parser.parse_args()
    context = capture_inventory(args.operations_sha256)
    # Every repository dependency is authenticated BEFORE a copied-byte worker
    # starts. -I -S -B gives an actual optimization0 worker even if this trusted
    # entry point was invoked with -O/-OO/PYTHONOPTIMIZE.
    bundle = {'action': action, 'args': vars(args),
              'inventory_sha256': context['inventory_sha256'], 'inventory': context['inventory'],
              'captured': {name: base64.b64encode(raw).decode('ascii') for name, raw in context['captured'].items()}}
    bootstrap = ('import argparse,base64,json,sys; '
                 'b=json.loads(sys.stdin.buffer.read()); '
                 'c={"inventory_sha256":b["inventory_sha256"],"inventory":b["inventory"],'
                 '"captured":{n:base64.b64decode(v,validate=True) for n,v in b["captured"].items()}}; '
                 'p=sys.argv[1]; n={"__name__":"_pr946_authenticated_core_","__file__":p,"__package__":None}; '
                 'exec(compile(c["captured"][sys.argv[2]],p,"exec",dont_inherit=True,optimize=0),n); '
                 'n["operation"](b["action"],argparse.Namespace(**b["args"]),c)')
    core = str((P / 'accept_pr946.py').relative_to(ROOT))
    result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', bootstrap,
                             str(P / 'accept_pr946.py'), core], cwd=ROOT,
                            input=json.dumps(bundle).encode())
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    entry('accept')
