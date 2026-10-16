"""Prepare a two-parent reviewed overlay on the actual explicitly granted MAIN."""
from pathlib import Path
import base64, datetime, hashlib, importlib.util, json, re, sys

A = Path(__file__).resolve().parent
C = A.parents[2]
P = A.parents[1]
spec = importlib.util.spec_from_file_location('api152', P / 'audits/pr152_5000006/prepare_scoped_merge.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
api, require, save, lookup, changed_leaves, body_at = m.api, m.require, m.save, m.lookup, m.changed_leaves, m.body_at
ORIGINAL = 'aec31742f3f26c5b1e533404da57539d17dc94a1'

def main():
    require(len(sys.argv) == 2 and re.fullmatch('[0-9a-f]{40}', sys.argv[1]), 'Pass actual freshly granted MAIN')
    expected = sys.argv[1]
    grant = json.loads((A / 'private/MERGE_WRITER_RETURN.json').read_text())
    require(grant['explicit_return_received'] and grant['returned_MAIN'] == expected, 'No actual bounded writer grant')
    plan_path = A / 'SCOPED_MERGE_SCOPE_PLAN.json'
    require(hashlib.sha256(plan_path.read_bytes()).hexdigest() == grant['scope_plan_sha256'], 'Granted scope changed')
    plan = json.loads(plan_path.read_text())
    gate = json.loads((A / 'ROOT_PUBLICATION_GATE.json').read_text())
    pub = json.loads((A / 'ZENODO_PUBLICATION_READBACK.json').read_text())
    tracker = json.loads((A / 'TRACKER_ACCEPTANCE.json').read_text())
    require(gate['status'] == 'READY_FOR_AUTHORIZED_PUBLICATION' and gate['fresh_seal_first_review_clean'], 'Scientific gate missing')
    require(pub['state'] == 'published' and tracker['DOI'] == pub['doi'] and tracker['DOI_count'] == 1, 'Publication/tracker not actually accepted')
    require(api('git/ref/heads/main')['object']['sha'] == expected, 'MAIN advanced; no stale object preparation')
    pr = api('pulls/156')
    require(pr['state'] == 'open' and not pr['draft'] and pr['head']['sha'] == ORIGINAL, 'Original PR state/head changed')
    require(pr['body'] == (A / 'PR_BODY_ACCEPTED.md').read_text(), 'Actual PR metadata differs')
    parent = api('git/commits/' + expected)
    overlay = {}
    for name, pin in plan['selected_files'].items():
        path = Path(pin['local_path'])
        data = path.read_bytes()
        require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Frozen selected bytes changed: ' + name)
        overlay[name] = path
    out = A / 'merge_checkpoint'
    require(not out.exists(), 'Inspect an existing preparation rather than replacing it')
    out.mkdir()
    now = datetime.datetime.now(datetime.UTC).isoformat()
    queue_path = 'unsolved_math_prioritization/QUEUE.md'
    old = body_at(queue_path, expected).decode()
    lines = old.splitlines(keepends=True)
    indices = [i for i, line in enumerate(lines) if '| 30005432 /' in line]
    require(len(indices) == 1, 'Target QUEUE row is not unique')
    i = indices[0]
    cells = lines[i].rstrip('\n').split('|')
    require(len(cells) == 14, 'QUEUE schema changed')
    cells[8] = ' claimed_solved '
    cells[9] = ' 2/5 '
    cells[11] = (' Verified unrestricted property-(s) ideal-closure counterexample on Z x Z/4Z; full S=Z x {0,1}, witness indices2/2 and additive double both infinite. '
                 'Known construction and FC antecedents credited; original Sept30 proof unchanged, exact FerudunOct11 overlap DOI10.5281/zenodo.23292254. '
                 'Contemporaneous separate disclosures; historical priority and mutual independence unresolved, publisher-body gaps disclosed. '
                 'Raised checker33512 per mode, corruptions rejected; two fresh full-package reviews clean, final seal-first. Extensive AI; unrefereed. ')
    cells[12] = ' [' + pub['doi'] + '](' + pub['doi_url'] + ') '
    lines[i] = '|'.join(cells) + '\n'
    new = ''.join(lines)
    require(len(old.splitlines()) == len(new.splitlines()) and sum(x != y for x, y in zip(old.splitlines(), new.splitlines())) == 1, 'Other QUEUE rows changed')
    queue = out / 'QUEUE.accepted.md'
    queue.write_text(new)
    overlay[queue_path] = queue
    prefix = 'draft_pr_publication_program_20260930/'
    j = json.loads(body_at(prefix + 'CURRENT_PROGRESS.json', expected))
    require(j['fully_completed_count'] == 30 and j['published_count'] == 17 and j['current_PR'] == 156, 'Actual ascending census differs')
    j.setdefault('historical_preparation_snapshots', []).append({'UTC': now, 'fields': {key: value for key, value in j.items() if key.startswith('current_')}, 'note': 'Previous dated PR156 prepublication findings retained; superseded by actual accepted publication/tracker and clean full-package reviews.'})
    require(156 not in j['published_PRs'] and len(j['published_PRs']) == 17, 'Prior publication list differs')
    j['published_PRs'].append(156)
    j['published_count'] = 18
    j.update({'UTC': now, 'updated_UTC': now, 'current_status': 'PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGE_PENDING',
              'current_PR_workflow_percent': 90, 'current_workflow_estimate_percent': 90, 'current_priority_clearance': False,
              'current_historical_novelty_or_exclusive_priority_certified': False, 'current_mutual_independence_certified': False,
              'current_publication_ready': True, 'current_publication_package_reviews_complete': True, 'current_publication_package_reviews_required': False,
              'current_publication_package_review_round': 2, 'current_publication_package_review_status': 'Two fresh scientific passes clean; final R2 direct-input seal preceded verdict summaries.',
              'current_publication_package_version': 'publication_package_v1', 'current_publication_package_review_clearance': True,
              'current_Zenodo_published': True, 'current_DOI': pub['doi'], 'current_tracker_updated': True, 'current_tracker_range': tracker['range'],
              'current_original_PR_merged': False, 'current_publication_disposition_pending': True,
              'current_remaining_required_steps': 'Actual scoped original-head merge and fresh full-scope/provider readbacks, then factual completion metadata.',
              'current_publication_gate': 'audits/pr156_30005432/ROOT_PUBLICATION_GATE.json',
              'current_priority_status': 'Qualified research note: known construction ancestry, exact later overlap and bounded access gaps credited. No historical priority or independence certificate.',
              'next_numeric_intake_cursor': 157, 'advance_to_next_PR_authorized_now': False,
              'persistent_goal_status': 'active', 'persistent_goal_complete': False,
              'program_snapshot_semantics': 'Actual PR156 publication and one tracker row accepted; merge is pending at this prepared snapshot. Fully completed cases remain30/99; actual published count is18, including156. Completion awaits actual disposition.',
              'program_snapshot_authority_condition': 'MERGE_AND_NATIVE_ACCEPTANCE.json must authenticate actual MAIN/tree/parents and provider merged state.',
              'active_checkpoint_commit': None, 'active_checkpoint_acceptance_receipt': 'audits/pr156_30005432/MERGE_AND_NATIVE_ACCEPTANCE.json',
              'completion_metadata_checkpoint_pending_at_snapshot': True, 'next_step': 'Complete actual PR156 original-head merge/readbacks and final factual metadata; no157 intake yet.'})
    save(out / 'CURRENT_PROGRESS.json', j)
    overlay[prefix + 'CURRENT_PROGRESS.json'] = out / 'CURRENT_PROGRESS.json'
    note = ('\n\n' + now + ' — PR156 qualified note published and tracked, original-head merge pending. Self-contained all-integer property-(s) counterexample, exact full set and both indices verified; old ingredients, exact later overlap and September30/October11 chronology credited. Historical priority/independence unresolved with material source-body gaps. Fresh R1 and new seal-first R2 complete-package reviews clean; frozen PDF/support and exact metadata accepted at ' + pub['doi_url'] + ', one tracker ' + tracker['range'] + '. Only target native/QUEUE and authored audit/programme paths overlaid; other actual MAIN paths preserved. Case90%, programme30/dated99=30.30%,18 actual publications; goalactive. Actual merge/provider/scope and factual completion metadata remain.\n')
    for name in ['CURRENT_PROGRESS.md', 'RESEARCH_LOG.md']:
        path = out / name
        path.write_bytes(body_at(prefix + name, expected) + note.encode())
        overlay[prefix + name] = path
    originals = {item['repository_path']: item for item in json.loads((A / 'ORIGINAL_FILE_MANIFEST.json').read_text())['files']}
    deletions = []
    for name in plan['conditional_original_native_deletions']:
        existing = lookup(parent['tree']['sha'], name)
        if existing is not None:
            require(existing == ('100644', 'blob', originals[name]['Git_blob']), 'Original native body changed; inspect before relocation: ' + name)
            deletions.append(name)
    entries = [{'path': name, 'mode': '100644', 'type': 'blob', 'sha': None} for name in deletions]
    pins = {}
    for name, path in sorted(overlay.items()):
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        pins[name] = {'local_path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': blob}
        entry = {'path': name, 'mode': '100644', 'type': 'blob'}
        try:
            entry['content'] = data.decode('utf8')
        except UnicodeDecodeError:
            remote = api('git/blobs', 'POST', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
            require(remote['sha'] == blob, 'Binary blob differs')
            entry['sha'] = blob
        entries.append(entry)
    tree = api('git/trees', 'POST', {'base_tree': parent['tree']['sha'], 'tree': entries})
    anticipated = {name for name, pin in pins.items() if lookup(parent['tree']['sha'], name) != ('100644', 'blob', pin['git_blob'])} | set(deletions)
    require(changed_leaves(parent['tree']['sha'], tree['sha']) == anticipated, 'Actual full-tree scope differs')
    for name, pin in pins.items():
        require(lookup(tree['sha'], name) == ('100644', 'blob', pin['git_blob']), 'Selected blob differs: ' + name)
    for name in deletions:
        require(lookup(tree['sha'], name) is None, 'Relocated obsolete native file remains')
    commit = api('git/commits', 'POST', {'message': 'Merge PR156: verified property-(s) counterexample and qualified publication\n\nSelf-contained negative answer, complete S and original indices; known ingredients and exact later overlap credited, dated September30/October11 disclosures distinguished from unresolved historical priority and independence. Two fresh complete-package reviews clean, final assessment sealed before verdicts. Exact publication ' + pub['doi_url'] + '; one tracker ' + tracker['range'] + '. Preserve original22 in historical folder and every other actual MAIN path.', 'tree': tree['sha'], 'parents': [expected, ORIGINAL]})
    actual = api('git/commits/' + commit['sha'])
    require(actual['tree']['sha'] == tree['sha'] and [item['sha'] for item in actual['parents']] == [expected, ORIGINAL], 'Actual commit tree/parents differ')
    require(api('git/ref/heads/main')['object']['sha'] == expected, 'MAIN advanced; never apply stale lease')
    result = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'status': 'SCOPED_TWO_PARENT_MERGE_PREPARED_MAIN_NOT_UPDATED', 'expected_main': expected, 'parent_tree': parent['tree']['sha'], 'tree': tree['sha'], 'commit': commit['sha'], 'original_PR_head': ORIGINAL, 'selected_files': pins, 'actual_changed_paths': sorted(anticipated), 'conditional_native_deletions_applied': deletions, 'QUEUE_rows_changed': 1, 'native_paths': sum(name.startswith('unsolved_math_prioritization/attempts/30005432/') for name in pins), 'DOI': pub['doi'], 'tracker_range': tracker['range'], 'all_other_actual_base_tree_paths_preserved': True, 'local_Git_index_ref_checkout_mutated': False}
    save(A / 'SCOPED_MERGE_PREPARATION.json', result)
    print(json.dumps({key: result[key] for key in ['status', 'expected_main', 'tree', 'commit', 'native_paths', 'DOI', 'tracker_range']}))
    print('Selected paths', len(pins), 'actual changed', len(anticipated))

if __name__ == '__main__':
    main()
