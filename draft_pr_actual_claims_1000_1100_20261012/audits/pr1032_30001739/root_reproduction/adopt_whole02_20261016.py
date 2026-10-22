"""ROOT adoption of the final independent whole02; no candidate modifications."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import stat
import subprocess

A = Path(__file__).resolve().parent.parent
V = A / 'reviews/package_02'
P = A / 'preprint_v1_1'
O = A / 'root_reproduction/whole02_20261016/final_attempt02'


def need(value, message):
    if not value:
        raise RuntimeError(message)


def read(path):
    return json.loads(path.read_text())


def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def save(path, value):
    need(not path.exists(), 'Preserve existing ROOT receipt: ' + str(path))
    path.write_text(json.dumps(value, indent=2) + '\n')


def check(root, rows, physical=False):
    for row in rows:
        path = root / row['path']
        # INPUT_FREEZE used stat(): one historical scratch symlink pins its
        # resolved regular target. Do not invent an unfrozen link-self pin.
        info = path.stat() if physical else path.lstat()
        need(stat.S_ISREG(info.st_mode), 'Not a regular pinned input: ' + str(path))
        need(ident(path) == {'bytes': row.get('bytes', row.get('size')),
                             'sha256': row['sha256']}, 'Content drift: ' + str(path))
        if 'nlink' in row:
            need(info.st_nlink == row['nlink'], 'Link-count drift: ' + str(path))
        if physical:
            need(info.st_ino == row['inode'] and info.st_dev == row['device'],
                 'Physical input identity changed: ' + str(path))
    return len(rows)


def main():
    O.mkdir()
    need(ident(V / 'OUTPUT_INVENTORY.json')['sha256'] ==
         '672cc1ea6ed2da2d5d516ad1b638cc698e31825cc625991482a63c14de0fc1be', 'Inventory seal')
    need(ident(V / 'OUTPUT_SEAL.json')['sha256'] ==
         'ca9764375e4d227ffb77a63dd0e9f13c876a869d858df7d91bd031f445595fdc', 'Final review seal')
    inventory = read(V / 'OUTPUT_INVENTORY.json')
    need(not inventory['nonregular'], 'Unexpected nonregular review evidence')
    outputs = check(V, inventory['files'])
    inputs = check(A, read(V / 'INPUT_FREEZE.json')['files'], physical=True)
    originals = check(A, read(A / 'preparation/unknown_priority_20261016/ORIGINAL_INPUT_PINS.json')['files'])
    preparation = check(P, read(P / 'PREPARATION_SEAL.json')['files'])
    sources = read(V / 'SOURCE_INSPECTION.json')['sources']
    for row in sources:
        need(ident(Path(row['path'])) == {key: row[key] for key in ('bytes', 'sha256')},
             'Source pin changed: ' + row['id'])
    verdict = read(V / 'VERDICT.json')
    need(verdict['complete_whole_review'] and not verdict['repair_only'] and
         verdict['review_ordinal_TOTAL'] == 2 and not verdict['actionable_findings'] and
         verdict['counts'] == dict.fromkeys(('P0', 'P1', 'P2', 'P3'), 0), 'Whole-review gate')
    runs = read(V / 'COMMAND_RUNS.json')
    need(runs['executions'] == 153 and runs['unexpected'] == runs['incomplete'] == 0,
         'Actual command outcomes')
    for row in runs['runs']:
        need(row['outcome'] == 'completed' and row['expectation_met'] and
             row['returncode'] == row['expected_exit'], 'Unconfirmed reviewer command')
        for stream in ('stdout', 'stderr'):
            need(ident(V / 'commands' / (row['name'] + '.' + stream)) ==
                 {'bytes': row[stream + '_bytes'], 'sha256': row[stream + '_sha256']},
                 'Raw command stream drift')
    script = V / 'independent_combinatorics.py'
    script_pin = ident(script)

    def execute(pair):
        tag, flags = pair
        argv = ['/opt/homebrew/bin/python3.14', '-I', '-B', *flags, str(script)]
        result = subprocess.run(argv, cwd=O, capture_output=True, timeout=120)
        (O / (tag + '.stdout')).write_bytes(result.stdout)
        (O / (tag + '.stderr')).write_bytes(result.stderr)
        row = {'argv': argv, 'cwd': str(O), 'exit': result.returncode,
               'stdout': ident(O / (tag + '.stdout')), 'stderr': ident(O / (tag + '.stderr'))}
        save(O / (tag + '.json'), row)
        return row, result.stdout

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(execute, [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]))
    need(ident(script) == script_pin, 'Final independent script changed')
    expected = {'bytes': 91591, 'sha256': '48ea9da2d1af85bf9622086ef4abd17d57109a35ef01ae72fe3d724c9e6c0d96'}
    need(all(row['exit'] == 0 and row['stdout'] == expected for row, data in results) and
         len({data for row, data in results}) == 1, 'Final complete independent JSON differs')
    facts = json.loads(results[0][1])
    need(facts['discrete_set_endpoint_precedence_cases'] == 441 and
         len(facts['edge_deletion_controls']) == 5 and
         facts['positive_negative_small_graph_cases'] == 1260, 'Boundary controls absent')
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    adoption = {
        'utc': utc, 'status': 'ROOT_ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE',
        'whole_reviews_completed': 2, 'minimum_whole_reviews_TOTAL': 2,
        'actionable_P0_P1_P2_P3': verdict['counts'], 'all_three_previous_P3_resolved': True,
        'input_rows_rehashed_with_physical_identity': inputs, 'original_rows_rehashed': originals,
        'input_pin_semantics': '1017 direct regular paths plus one old package_01 scratch symlink whose INPUT_FREEZE row follows its regular target using stat/read_bytes. No initial link-self identity was supplied by that freeze; no such initial identity is claimed here.',
        'preparation_rows_rehashed': preparation, 'final_review_output_rows_rehashed': outputs,
        'source_interface_identity_rows_rehashed': len(sources),
        'actual_reviewer_commands': {'success': runs['zero_exit'], 'expected_refusal': runs['intentional_nonzero'],
                                     'unexpected': 0, 'incomplete': 0},
        'all153_command_stream_pairs_rehashed': True,
        'ROOT_read_scope': 'Complete final REPORT and independent derivation; full independent/code/package harness/runner, including later set-based and edge-deletion additions; source ledger, verdict and integrity. Current manuscript fully reread. Primary-interface scope remains as explicitly documented, not full-source theorem reproof.',
        'ROOT_fresh_commands': [row for row, data in results], 'independent_final_script': script_pin,
        'initial_ROOT_replay': 'root_reproduction/whole02_20261016/INDEPENDENT_REPLAY.json',
        'initial_replay_scope': 'Earlier 90463-byte checker before final set/edge additions; preserved, not misreported as final. New final three-mode replay above binds sealed91591-byte output.',
        'ROOT_helper_failure': 'First adapter required lstat regularity for every frozen input and stopped at the one intentional old scratch symlink before new commands/adoption. Failure receipt preserved in whole02_20261016/final; adapter now matches the actual stat-based freeze. No candidate failure.',
        'visual_scope': 'Reviewer actually viewed all9current pages and independently compiled/rendered matching9rasters. ROOT previously viewed changed current pages1,8 and other7pixels match earlier actually viewed v1.0 pages; no new ROOT compilation/render claimed.',
        'publication_ready': True, 'published': False, 'Luo_Zha_overlap': 'UNKNOWN',
        'unknown_source_nonblocking_direct_user_authorization': True, 'novelty_certified': False,
        'review_inventory': ident(V / 'OUTPUT_INVENTORY.json'), 'review_seal': ident(V / 'OUTPUT_SEAL.json'),
        'review_report': ident(V / 'REPORT.md'), 'paper': ident(P / 'paper.pdf'),
        'support_archive': ident(P / 'pr1032_supportkit_v1.1.zip'),
    }
    target = A / 'ROOT_WHOLE_PACKAGE_REVIEW_02_20261016.json'
    save(target, adoption)
    seal = {key: adoption[key] for key in ('utc', 'publication_ready', 'published', 'whole_reviews_completed',
                                         'Luo_Zha_overlap', 'paper', 'support_archive')}
    seal.update(status='CURRENT_ROOT_FINAL_READY_PRIORITY_OVERLAP_UNKNOWN_USER_ACCEPTED',
                issues_resolved=True, actionable_issues=0, all_actionable_findings_resolved=True,
                minimum_whole_reviews=2, root_adoption=ident(target),
                audited_head='810d52306312623ecfe01ecbc5f5f0dd360972c3',
                historical_scope='All previous preparation/priority/review states preserved as dated history; no canonical candidate rewritten.')
    save(A / 'CURRENT_FINAL_SEAL_20261016.json', seal)
    print(json.dumps({'status': adoption['status'], 'inputs': inputs, 'outputs': outputs,
                      'root_fresh_commands': 3, 'publication_ready': True, 'whole_reviews': 2}))


if __name__ == '__main__':
    main()
