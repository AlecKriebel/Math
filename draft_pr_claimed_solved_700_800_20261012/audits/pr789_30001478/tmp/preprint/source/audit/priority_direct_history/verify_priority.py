#!/usr/bin/env python3
"""Closed authored-packet and optional source custody; not a priority proof."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

HEAD = 'aa44dec3baf8c1cd179cf8b55f32be95c74ee81a'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def strict(data):
    def bad(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    require(isinstance(value, str) and '\\' not in value, 'unsafe path')
    p = PurePosixPath(value)
    require(value and not p.is_absolute() and str(p) == value and
            all(x not in ('', '.', '..') for x in p.parts), 'unsafe path')
    return p


def root_path(value):
    p = Path(value).absolute()
    require(p == p.resolve(strict=True), 'root or ancestor symlink')
    require(stat.S_ISDIR(os.lstat(p).st_mode), 'root is not a directory')
    return p


def safe_read(root, name):
    rel = relative(name)
    p = root
    for part in rel.parts[:-1]:
        p = p / part
        require(stat.S_ISDIR(os.lstat(p).st_mode), 'unsafe ancestor')
    p = p / rel.name
    before = os.lstat(p)
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            'nonregular, symlink or hardlinked file')
    require(before.st_size <= 16_000_000, 'file too large')
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) |
                 getattr(os, 'O_NONBLOCK', 0))
    try:
        now = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size) ==
                (now.st_dev, now.st_ino, now.st_size), 'file changed before open')
        chunks = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                break
            chunks.append(chunk)
        data = b''.join(chunks)
        after = os.fstat(fd)
        require((now.st_dev, now.st_ino, now.st_size, now.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
                'file changed while reading')
        require(len(data) == before.st_size, 'short read')
        return data
    finally:
        os.close(fd)


def inventory(root):
    out = set()
    def visit(folder):
        for entry in os.scandir(folder):
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(any(os.scandir(entry.path)), 'empty directory')
                visit(Path(entry.path))
            else:
                require(stat.S_ISREG(mode), 'nonregular packet entry')
                out.add(Path(entry.path).relative_to(root).as_posix())
    visit(root)
    return out


def verify_rows(root, rows):
    require(isinstance(rows, list), 'bad binding rows')
    seen = set()
    data = {}
    for row in rows:
        require(set(row) == {'path', 'bytes', 'sha256'}, 'bad row shape')
        name = str(relative(row['path']))
        require(name not in seen, 'duplicate binding path')
        seen.add(name)
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'bad size')
        raw = safe_read(root, name)
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'],
                'binding mismatch: ' + name)
        data[name] = raw
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--packet-root', required=True)
    p.add_argument('--expected-manifest-sha256', required=True)
    p.add_argument('--expected-checker-sha256', required=True)
    p.add_argument('--intake-root', required=True)
    p.add_argument('--primary-root')
    a = p.parse_args()
    root = root_path(a.packet_root)
    require(Path(__file__).absolute() == root / 'verify_priority.py',
            'checker must be the pinned packet entrypoint')
    require(digest(safe_read(root, 'verify_priority.py')) ==
            a.expected_checker_sha256, 'checker pin mismatch')
    raw = safe_read(root, 'MANIFEST.json')
    require(digest(raw) == a.expected_manifest_sha256, 'manifest pin mismatch')
    mf = strict(raw)
    require(set(mf) == {'schema', 'problem', 'pr', 'files'} and
            mf['schema'] == 'priority-direct-history-v1' and
            mf['problem'] == 30001478 and mf['pr'] == 789, 'wrong manifest target')
    data = verify_rows(root, mf['files'])
    require(inventory(root) == set(data) | {'MANIFEST.json'}, 'packet not closed')
    v = strict(data['VERDICT.json'])
    require(v['problem'] == 30001478 and v['pr'] == 789 and
            v['candidate_head'] == HEAD and
            v['status'] == 'PASS_BOUNDED_PRIORITY_AUDIT' and
            v['priority_status'] == 'PRIORITY_UNRESOLVED_EXPLICIT_QUOTIENT_CANDIDATE',
            'wrong verdict scope')
    for key in ('novelty_or_firstness_claimed', 'current_open_status_certified',
                'global_absence_certified'):
        require(v[key] is False, 'unsupported certification')
    for key in ('verified_full_predecessors', 'required_mathematical_repairs',
                'blocking_priority_findings'):
        require(v[key] == [], 'verdict no longer matches sealed position')
    require(v['external_contact_count'] == 0 and v['completion_percent'] == 100,
            'wrong completion/contact scope')
    plan = strict(data['INDEPENDENT_SEARCH_PLAN.json'])
    provisional = strict(data['INDEPENDENT_PROVISIONAL_ASSESSMENT.json'])
    comparison = strict(data['ORIGINAL_AUDIT_COMPARISON.json'])
    require(plan['candidate_head'] == provisional['candidate_head'] == HEAD,
            'wrong original candidate')
    require(provisional['plan_sha256'] == digest(data['INDEPENDENT_SEARCH_PLAN.json'])
            and comparison['independent_provisional_sha256'] ==
            digest(data['INDEPENDENT_PROVISIONAL_ASSESSMENT.json']),
            'independence binding mismatch')
    times = [datetime.datetime.fromisoformat(x['timestamp_utc'])
             for x in (plan, provisional, comparison)]
    require(times[0] < times[1] < times[2], 'independence chronology mismatch')
    require(len(comparison['same_primary_source_bytes']) == 3 and
            all(x['pass'] is True for x in comparison['same_primary_source_bytes']),
            'old/fresh source comparison mismatch')
    log = strict(data['SEARCH_LOG.json'])
    require(len(log['batches']) == 13 and log['query_count'] == 52 and
            sum(len(x['queries']) for x in log['batches']) == 52,
            'search count mismatch')
    sources = strict(data['PRIMARY_SOURCES.json'])
    require(sources['valid_pdf_retrievals'] == 22 and
            sources['actual_article_or_slide_body_retrievals'] == 21,
            'source reading scope mismatch')
    names = {x['name']: x for x in sources['sources']}
    require(names['NS_accepted']['reading_scope'].startswith('TWO-PAGEFILE'),
            'mislabeled download cannot establish journal content')
    require('Kirkman' in names['Homological']['version'] and
            'Zhou' in names['Acyclic']['version'], 'bibliographic correction lost')
    inputs = strict(data['INPUT_BINDINGS.json'])
    require(len(inputs['files']) == 8, 'wrong intake binding scope')
    intake = verify_rows(root_path(a.intake_root), inputs['files'])
    selected = strict(intake['SELECTED_PUBLIC_RECORD.json'])
    require(selected['problem']['id'] == 30001478 and
            selected['prior_research'] == {}, 'wrong selected problem')
    external_count = 0
    if a.primary_root:
        ext = strict(data['EXTERNAL_BINDINGS.json'])
        require(len(ext['files']) == 62, 'wrong external binding scope')
        external = verify_rows(root_path(a.primary_root), ext['files'])
        external_count = len(external)
        loc = strict(data['PASSAGE_LOCATORS.json'])['pages']
        require(len(loc) == 14, 'wrong passage count')
        for item in loc:
            pages = external[item['source'] + '.txt'].decode().split('\f')
            require(digest(pages[item['pdf_page'] - 1].encode()) ==
                    item['extracted_page_sha256'], 'passage binding mismatch')
    print(json.dumps({'status': 'PASS', 'problem': 30001478, 'pr': 789,
                      'authored_files': len(data) + 1, 'intake_inputs': 8,
                      'external_inputs_rehashed': external_count,
                      'priority_certified': False, 'mathematical_replay': False},
                     sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({'status': 'FAIL', 'error': str(e)}, sort_keys=True))
        sys.exit(1)
