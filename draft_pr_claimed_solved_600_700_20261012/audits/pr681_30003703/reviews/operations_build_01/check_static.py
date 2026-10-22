#!/usr/bin/env python3
"""Static author checks only: compile/parse the two sources without executing them."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).absolute().parent
A = HERE.parents[1]
checks = []

def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})
    if not condition:
        raise ValueError(name)

sources = {name: (A / name).read_bytes() for name in ('prepare_integration.py', 'record_tracker.py')}
trees = {}
for name, raw in sources.items():
    for optimize in (0, 2):
        compile(raw, str(A / name), 'exec', optimize=optimize)
        check(name + ': in-memory compilation optimize=' + str(optimize), True)
    trees[name] = ast.parse(raw, filename=str(A / name))
    check(name + ': runtime gates do not use assert', not any(isinstance(n, ast.Assert) for n in ast.walk(trees[name])))
    check(name + ': no stale PR662 scientific identifiers', not re.search(rb'\b662\b|2306086|real_schlicht|preschwarzian|Hayman|Jenkins|Aleksandrov|AMR-022', raw))
    check(name + ': no hardcoded Zenodo record DOI', not re.search(rb'10\.5281/zenodo\.[0-9]+', raw))
    check(name + ': no publication command or skill generation', b'generate-skills' not in raw and b'zenodo-kit publish' not in raw)

s = sources['prepare_integration.py'].decode()
t = sources['record_tracker.py'].decode()
constants = {}
for item in trees['prepare_integration.py'].body:
    if isinstance(item, ast.Assign) and len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
        try:
            constants[item.targets[0].id] = ast.literal_eval(item.value)
        except (ValueError, TypeError):
            pass
check('PR681 immutable identity', constants['PR'] == 681 and constants['PROBLEM'] == '30003703'
      and constants['ORIGINAL'] == 'e92320ea5979c812089780a982fbd88136a26522'
      and constants['BRANCH'] == 'research/30003703-andreadakis-counterexamples')
check('exact accepted title', constants['TITLE'] == "Counterexamples to Satoh's SL(2) representation-filtration conjecture")
check('snapshot SHA fixed to actual captured bytes', constants['SNAPSHOT_SHA'] == hashlib.sha256((A / 'SCOPE_AND_SNAPSHOT.json').read_bytes()).hexdigest())
check('ten scientific inputs, only PDF/ZIP upload', len(constants['PUB_NAMES']) == 10 and len(set(constants['PUB_NAMES'])) == 10
      and constants['UPLOAD_NAMES'] == ('satoh_filtration_counterexamples.pdf', 'satoh_filtration_verification.zip'))
check('sibling publication and native prefixes', constants['PREFIX'] == 'unsolved_math_prioritization/attempts/30003703/'
      and constants['PUB_PREFIX'] == 'unsolved_math_prioritization/publications/30003703/')
check('exact false claim flags', set(constants['FALSE_FLAGS']) == {
    'degree5_rank3_claim', 'every_degree_failure_claim', 'SLm_m_gt2_claim', 'character_algebra_claim',
    'ordinary_IA_LCS_conjecture_claim', 'new_PI_identity_claim', 'new_general_PI_method_claim',
    'historical_firstness_claim', 'exhaustive_novelty_clearance', 'current_literature_openness_certified',
    'formal_proof_certificate', 'AI_reviews_are_human_peer_review'})
for token in ("'degree5_rank_min': 4", "'degree6_rank_min': 3", "'component_algebra': 'rational_SL2_matrix_entry_functions'",
              "'A_uses_integral_free_group_LCS': True", "'D_acts_on_whole_J_quotient': True",
              "'classical_identity_explicitly_credited': True", "'AI_tools_used_extensively': True", "'unrefereed': True"):
    check('scope token ' + token, token in s)
check('source-only dependency compile with executed SHA seed', 'exec(compile(_dependency_source' in t
      and '_dependency._CAPTURED_SOURCE_SHA256 = INTEGRATION_HELPER_SHA256' in t and 'importlib' not in t)
check('source captures reject links and mid-read mutation', "dir_fd=directory" in s and "'O_NOFOLLOW'" in s
      and 'before.st_mtime_ns, before.st_ctime_ns' in s)
check('accepted gate pins all helpers and research gates', "accepted.get('helper_sha256') == helpers" in s
      and "set(bindings) == set(GATE_NAMES)" in s)
check('reports bind exact science, helpers, gates', "report.get('publication_files') == records" in s
      and "report.get('helper_sha256') == helpers" in s and "report.get('gate_bindings') == bindings" in s)
check('two sequential distinct zero-finding review chain', 'len(rounds) >= 2' in s and 'reviewer not in reviewers' in s
      and "report['previous_report_sha256'] == previous_hash" in s and 'previous_end <= start' in s
      and "report.get('findings') == []" in s and "report.get('findings_waived') is False" in s)
check('post-accepted final publication gate required', "'pr681-publication-final-acceptance-v1'" in s
      and "final.get('accepted_input_gate_sha256') == sha(accepted_bytes)" in s)
check('receipts require actual published production identities and file hashes', "receipt.get('environment') == 'production'" in s
      and "receipt.get('state') == 'published'" in s and "receipt.get('record_url') == 'https://zenodo.org/records/'" in s
      and "resolution.get('resolved_url') == 'https://zenodo.org/records/'" in s and "== expected_files" in s)
check('timestamps remain distinct', "'publication_confirmed_utc': confirmed_utc, 'integration_prepared_utc': now" in s)
check('native replay checks exact known wrapper shape', "native_report.get('result') == 'PASS'" in s
      and "native_report.get('packet_files') == 23" in s and "native_report.get('author_negative_controls') == 5" in s
      and "native_report.get('independent_negative_controls') == 12" in s
      and "native_report.get('assertions_enabled_in_frozen_subprocesses') is True" in s)
check('supplement replay includes offline selftest', "package / 'verify_package.py', ['--replay', '--selftest']" in s)
check('archive and extracted native modes are explicit 0644', "stat.S_IMODE(entry.external_attr >> 16) == 0o644" in s
      and s.count('path.chmod(0o644)') == 3)
check('supplement selftest status, cases and both rejection modes validated', "controls.get('status') == 'PASS'" in s
      and 'type(count) is int and count >= 30' in s and "controls.get('total_rejections') == 2 * count" in s
      and "rejected['normal'] == rejected['optimized']" in s)
check('native all bytes/modes verified', "{key: record[key] for key in ('git_mode', 'git_blob')}" in s
      and "'native_all_git_modes_unchanged': True" in s and "inventory(native) == set(inputs['original'])" in s)
check('queue changes only three selected cells', "== [8, 9, 11]" in s and "b'claimed_solved'" in s
      and "b'1/5'" in s and "b'710'" in s and "'all_unselected_bytes_unchanged': True" in s)
check('isolated objects only, no FETCH_HEAD/refmap/shared index writes', "'GIT_OBJECT_DIRECTORY': str(objects.absolute())" in s
      and "'GIT_ALTERNATE_OBJECT_DIRECTORIES'" in s and "'--no-write-fetch-head'" in s and "'--refmap='" in s
      and not any("git('" + op + "'" in s for op in ('update-ref', 'update-index', 'write-tree', 'read-tree', 'add', 'checkout', 'switch', 'reset', 'stash', 'pull')))
check('transport suppresses hooks, graph writes, submodules and signing', all(token in s for token in (
      'core.hooksPath=/dev/null', 'fetch.writeCommitGraph=false', '--no-recurse-submodules',
      'commit.gpgsign=false', 'push.gpgsign=false')))
check('push uses verified URL ordinary refspec, one call', s.count("git('push',") == 1
      and "git('push', origin_url(push=True), commit + ':refs/heads/' + BRANCH)" in s
      and '--force' not in s and '--force-with-lease' not in s)
main = next(n for n in trees['prepare_integration.py'].body if isinstance(n, ast.FunctionDef) and n.name == 'main')
push_if = [n for n in ast.walk(main) if isinstance(n, ast.If) and ast.unparse(n.test) == 'args.push']
check('sole push nested in explicit --push branch', len(push_if) == 1
      and sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'git'
              and bool(n.args) and isinstance(n.args[0], ast.Constant) and n.args[0].value == 'push'
              for n in ast.walk(push_if[0])) == 1)
check('fresh head/main comparisons and sticky push dispatch precede push', s.index("final_gate = validate_live_write_gate('integration'")
      < s.index("require(remote_oid('refs/heads/' + BRANCH) == head")
      < s.index('write_json(PUSH_INTENT,') < s.index("git('push',"))
check('durable intents use fsync/atomic replace and O_EXCL', 'os.fsync(stream.fileno())' in s
      and 'os.fsync(directory)' in s and 'os.replace(temporary, path)' in s and 'os.O_EXCL' in s)
check('all accepted captured sources rechecked before writes', 'def recheck_sources(validation)' in s
      and "recheck_sources(validation)" in s and "recheck_sources(inputs['validation'])" in s)
check('tracker exact destination and headers', "GID = 1254632077" in t
      and "TAB = 'Math Puzzles'" in t and "['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']" in t
      and '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' in t)
check('tracker original primary source and blank solution chat', "return ['https://ems.press/content/serial-article-files/46724', '', 'https://doi.org/' + doi" in t)
check('tracker row disclosures and exact degree/rank boundaries', all(token in t for token in (
      'D_n(5) != A_n(5) for every n >= 4', 'D_n(6) != A_n(6) for every n >= 3',
      'integral free-group lower central series', 'Burde/Razmyslov', 'original 2018 equality',
      '2017/2021', '2025/2026', 'firstness', 'current-openness', 'AI tools used extensively',
      'unrefereed', 'not human peer review', 'https://github.com/AlecKriebel/Math/pull/681')))
check('tracker checks duplicate DOI and exact existing row', "require(len(matches) <= 1" in t
      and "(values[matches[0] - 1] + [''] * 4)[:4] == row" in t)
check('tracker pending marker forbids absence-based retry', "require(old is None, 'a prior append was dispatched" in t)
check('tracker final gate and durable intent precede sole append', t.index("final_gate = validate_live_write_gate('tracker'")
      < t.index('write_json(PENDING, pending)') < t.index("response = call('spreadsheets.values', 'append'"))
check('tracker exact A:D response/range/raw/readback/global DOI uniqueness', all(token in t for token in (
      "'valueInputOption': 'RAW'", "('updatedRows', 1), ('updatedColumns', 4), ('updatedCells', 4)",
      "updates.get('updatedData', {}).get('values') == [row]", "require(actual == [row]", "matches == [int(matched.group(1))]")))
snapshot = json.loads((A / 'SCOPE_AND_SNAPSHOT.json').read_bytes())
native_root = A / 'native' / constants['PREFIX']
records = snapshot['original_blobs']
check('actual native capture static inventory and all 23 hashes', len(records) == 23
      and {path.relative_to(native_root).as_posix() for path in native_root.rglob('*') if path.is_file()}
          == {name[len(constants['PREFIX']):] for name in records}
      and all(record['git_mode'] == '100644' and len((A / 'native' / name).read_bytes()) == record['size']
              and hashlib.sha256((A / 'native' / name).read_bytes()).hexdigest() == record['sha256']
              for name, record in records.items()))
scope_node = next(n.value for n in trees['prepare_integration.py'].body if isinstance(n, ast.Assign)
                  and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'EXPECTED_SCOPE')
expected_scope = {}
for key, value in zip(scope_node.keys, scope_node.values):
    if key is None:
        check('scope expansion uses explicit false flags only', isinstance(value, ast.DictComp)
              and isinstance(value.value, ast.Constant) and value.value.value is False)
        expected_scope.update({flag: False for flag in constants['FALSE_FLAGS']})
    else:
        expected_scope[ast.literal_eval(key)] = constants[value.id] if isinstance(value, ast.Name) else ast.literal_eval(value)
check('actual parent CLAIM_SCOPE matches exact helper scope', json.loads((A / 'publication/CLAIM_SCOPE.json').read_bytes()) == expected_scope)
(HERE / 'EXPECTED_SCOPE.json').write_text(json.dumps(expected_scope, indent=2) + '\n')
deposit = json.loads((A / 'publication/zenodo-deposit.json').read_bytes())
check('actual parent deposit title/upload order matches helper', deposit['metadata']['title'] == constants['TITLE']
      and deposit['files'] == [{'path': name} for name in constants['UPLOAD_NAMES']])
check('actual parent metadata disclosure vocabulary satisfies helper', all(token in deposit['metadata']['description']
      for token in ('rational', 'integral', 'Burde', 'Razmyslov', '2018', '2017', '2021', '2025', '2026', 'unrefereed', 'AI tools', 'firstness'))
      and any(token in deposit['metadata']['description'] for token in ('current-openness', 'continuously open status')))
result = {'schema': 'pr681-operations-author-static-checks-v1',
          'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS',
          'scope': 'Static author checks only; helper code was parsed and compiled in memory, never executed.',
          'checks': checks, 'check_count': len(checks),
          'source_pins': {name: {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} for name, raw in sources.items()},
          'no_remote_reads_or_writes_by_test': True, 'no_shared_git_writes': True,
          'subtask_completion_estimate_percent': 100,
          'independent_whole_package_approval': False}
(HERE / 'STATIC_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'check_count': len(checks), 'source_pins': result['source_pins']}))
