#!/usr/bin/env python3
"""Prove the concrete normal-merge repair map without creating Git objects."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess

HEAD = '26df33899c95d860403ab311c568e0328bc87eeb'
MAIN = '8e04757bff6e5c6c25d2dbf23ce10f736da8c5c8'
BASE = 'ceada39994b1cd2c4935709143b53e2f7a581a45'
PREFIX = 'problems/30005116_induced_four_cycle_profile/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
GATE_SHA = '2b613efcc4d41616277c7fd259d1357dbcc69e0aeb4d330efb9618167442a2de'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--own', required=True)
    p.add_argument('--git', required=True)
    p.add_argument('--gate-code', required=True)
    p.add_argument('--historical-proposal-only', action='store_true')
    a = p.parse_args()
    own = pathlib.Path(a.own)
    private = own / 'private' / 'refresh_assessment'
    public = own / 'public'
    private.mkdir(parents=True, exist_ok=True)
    public.mkdir(parents=True, exist_ok=True)
    gate_path = pathlib.Path(a.gate_code)
    assert hashlib.sha256(gate_path.read_bytes()).hexdigest() == GATE_SHA
    spec = importlib.util.spec_from_file_location('immutable_gate', gate_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    records = []
    def run(label, argv):
        r = subprocess.run(argv, cwd=a.git, capture_output=True)
        (private / (label + '.stdout')).write_bytes(r.stdout)
        (private / (label + '.stderr')).write_bytes(r.stderr)
        records.append({'label': label, 'exit': r.returncode,
                        'stdout_sha256': hashlib.sha256(r.stdout).hexdigest(), 'stdout_bytes': len(r.stdout),
                        'stderr_sha256': hashlib.sha256(r.stderr).hexdigest(), 'stderr_bytes': len(r.stderr)})
        assert r.returncode == 0 and not r.stderr, label
        return r.stdout
    def git(label, *argv):
        return run(label, ['git', *argv])
    def tree(commit, label):
        out = {}
        for item in git(label, 'ls-tree', '-r', '-z', commit).split(b'\0'):
            if not item:
                continue
            meta, path = item.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            assert kind == 'blob'
            out[path.decode()] = (mode, oid)
        return out
    refs = json.loads(run('main_ref', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main']))
    branch = json.loads(run('head_ref', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/math/30005116-induced-four-cycle-wip']))
    assert refs['object']['sha'] == MAIN
    if not a.historical_proposal_only:
        assert branch['object']['sha'] == HEAD
    main_tree = tree(MAIN, 'main_tree')
    head_tree = tree(HEAD, 'head_tree')
    expected = dict(main_tree)
    target = {p for p in head_tree if p.startswith(PREFIX)}
    assert len(target) == 45 and not any(p.startswith(PREFIX) for p in main_tree)
    scope = target | {QUEUE}
    for name in scope:
        expected[name] = head_tree[name]
    assert {p for p in set(main_tree) | set(expected) if main_tree.get(p) != expected.get(p)} == scope
    before = git('main_queue', 'show', MAIN + ':' + QUEUE)
    parent_queue = git('base_queue', 'show', BASE + ':' + QUEUE)
    after = git('head_queue', 'show', HEAD + ':' + QUEUE)
    assert before == parent_queue
    lines = before.splitlines(keepends=True)
    assert [i for i, line in enumerate(lines) if b'| 30005116 / OWR-10252930-028 |' in line] == [410]
    cells = lines[410].split(b'|')
    assert cells[1].strip() == b'400' and cells[8] == b' queued ' and cells[9] == b' 0/5 '
    cells[8] = b' unsolved '
    cells[9] = b' 5/5 '
    lines[410] = b'|'.join(cells)
    assert b''.join(lines) == after
    merge_base = git('merge_base', 'merge-base', MAIN, HEAD).decode().strip()
    assert merge_base == BASE
    text = git('readonly_merge_tree', 'merge-tree', BASE, MAIN, HEAD).decode()
    assert '<<<<<<<' not in text and 'CONFLICT' not in text
    metadata = re.findall(r'^  (?:result|our|their)\s+([0-9]{6}) ([0-9a-f]{40}) (.+)$', text, re.M)
    assert {path for _, _, path in metadata} == scope
    results = {path: (mode, oid) for mode, oid, path in re.findall(r'^  result\s+([0-9]{6}) ([0-9a-f]{40}) (.+)$', text, re.M)}
    incoming = {path: (mode, oid) for mode, oid, path in re.findall(r'^  their\s+([0-9]{6}) ([0-9a-f]{40}) (.+)$', text, re.M)}
    for path in scope - set(results):
        assert path not in main_tree and path in incoming
        results[path] = incoming[path]
    assert set(results) == scope and all(results[path] == expected[path] for path in scope)
    output = {'status': 'PASS_HISTORICAL_PROPOSED_MAP' if a.historical_proposal_only else 'PASS_PROPOSED_NORMAL_MERGE_MAP', 'reviewed_head': HEAD,
              'actual_main': MAIN, 'merge_base': BASE,
              'observed_live_head': branch['object']['sha'],
              'historical_proposal_only': a.historical_proposal_only,
              'expected_normal_merge_parents': [HEAD, MAIN],
              'expected_tree': module.canonical_tree_sha(expected),
              'expected_scope_against_main': 46, 'unchanged_target_files': 45,
              'queue_only_pipe_cells': [8, 9], 'queue_line': 411, 'queue_rank': 400,
              'every_other_main_path_preserved': True, 'git_mutations': 0, 'service_writes': 0,
              'supported_operation': 'normal update-branch with expected_head_sha=' + HEAD,
              'official_docs': 'https://docs.github.com/en/rest/pulls/pulls#update-a-pull-request-branch',
              'future_commit_not_yet_certified': True}
    receipt = {'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'result': output, 'command_records': records,
               'immutable_gate_sha256': GATE_SHA, 'volatile_receipt_fields': ['observed_utc']}
    (public / 'refresh_assessment_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(output, sort_keys=True))

if __name__ == '__main__':
    main()
