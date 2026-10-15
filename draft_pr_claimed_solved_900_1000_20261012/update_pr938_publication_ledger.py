"""Record the verified publication in remote main without touching shared files."""
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[1]
EFFORT = Path(__file__).resolve().parent
AUDIT = EFFORT / 'audits/pr938_30003634'
KEY = '30003634'
if not __debug__:
    raise RuntimeError('This internal ledger writer must run without Python optimization')

def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True, **kwargs).stdout.strip()

def blob(ref, path):
    # Decode exact Git bytes without subprocess universal-newline conversion.
    return subprocess.run(['git', 'show', ref + ':' + path], cwd=ROOT,
                          check=True, capture_output=True).stdout.decode('utf-8')

def replace_entry(raw, key, value):
    """Keep all other JSON object entries byte-identical."""
    parsed = json.loads(raw)
    if key not in parsed:
        end = raw.rfind('}')
        entry = json.dumps({key: value}, ensure_ascii=False, indent=2)[2:-2]
        prefix = raw[:end].rstrip()
        result = prefix + (',\n' if parsed else '\n') + entry + '\n}' + raw[end + 1:]
    else:
        dec = json.JSONDecoder()
        pos = raw.index('{') + 1
        while True:
            while raw[pos].isspace() or raw[pos] == ',':
                pos += 1
            name, pos = dec.raw_decode(raw, pos)
            while raw[pos].isspace():
                pos += 1
            if not raw[pos] == ':':
                raise RuntimeError("Publication ledger guard: raw[pos] == ':'")
            pos += 1
            while raw[pos].isspace():
                pos += 1
            start = pos
            _, pos = dec.raw_decode(raw, pos)
            if name == key:
                replacement = json.dumps(value, ensure_ascii=False, indent=2).replace('\n', '\n  ')
                result = raw[:start] + replacement + raw[pos:]
                break
    changed = json.loads(result)
    if not changed[key] == value:
        raise RuntimeError('Publication ledger guard: changed[key] == value')
    if not {k: v for k, v in parsed.items() if k != key} == {k: v for k, v in changed.items() if k != key}:
        raise RuntimeError('Publication ledger guard: {k: v for k, v in parsed.items() if k != key} == {k: v for k, v in changed.items() if k != key}')
    return result

def explicit_tree(parent, replacements):
    """Replace only the three declared native blobs; allocate no index."""
    allowed = {'unsolved_math_prioritization/QUEUE.md',
               'unsolved_math_prioritization/state.json',
               'unsolved_math_prioritization/history.jsonl'}
    if set(replacements) != allowed:
        raise RuntimeError('Unexpected native publication replacement set')
    updates = {}
    for path, text in replacements.items():
        oid = run(['git', 'hash-object', '-w', '--stdin'], input=text)
        old_mode = run(['git', 'ls-tree', parent, '--', path]).split()[0].encode('ascii')
        if old_mode not in (b'100644', b'100755'):
            raise RuntimeError('Unexpected native publication file mode')
        cursor = updates
        parts = path.split('/')
        for part in parts[:-1]:
            cursor = cursor.setdefault(part.encode('utf-8'), {})
        cursor[parts[-1].encode('utf-8')] = (old_mode, b'blob', oid.encode('ascii'))
    def rebuild(old, changes):
        entries = {}
        raw = subprocess.run(['git', 'ls-tree', '-z', old], cwd=ROOT,
                             check=True, capture_output=True).stdout
        for row in raw.split(b'\0'):
            if row:
                header, name = row.split(b'\t', 1)
                entries[name] = tuple(header.split(b' '))
        for name, replacement in changes.items():
            if isinstance(replacement, dict):
                prior = entries[name]
                if prior[1] != b'tree':
                    raise RuntimeError('Non-tree native ancestor')
                child = rebuild(prior[2].decode('ascii'), replacement)
                entries[name] = (prior[0], b'tree', child.encode('ascii'))
            else:
                entries[name] = replacement
        payload = b''.join(b' '.join(header)+b'\t'+name+b'\0'
                           for name, header in entries.items())
        return subprocess.run(['git', 'mktree', '-z'], cwd=ROOT, input=payload,
                              check=True, capture_output=True).stdout.decode('ascii').strip()
    return rebuild(parent, updates)

def valid_tracker_range(value):
    if type(value) is not str:
        return False
    match = re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1", value)
    return match is not None and int(match[1]) >= 2


def verify_receipt_links(a, publication, merge, accepted, tracker=None, native=None):
    """Fail on stale/cross-target local receipts before downstream writes."""
    def need(ok, label):
        if not ok:
            raise RuntimeError('PR938 receipt linkage: '+label)
    def read(name):
        return json.loads((a/name).read_text())
    head = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
    need(accepted.get('accepted') is True and accepted.get('original_pr_head') == head
         and len(accepted.get('full_package_reviews', [])) >= 2, 'exact acceptance')
    freeze_raw = (a/'publication/PREPUBLICATION_FREEZE.json').read_bytes()
    pin = hashlib.sha256(freeze_raw).hexdigest()
    freeze = json.loads(freeze_raw)
    need(pin == accepted.get('freeze_sha256') and freeze['original_pr_head'] == head
         and freeze['pr'] == 938 and freeze['problem_id'] == '30003634'
         and freeze['files'] == accepted['files'], 'accepted frozen target')
    need(freeze['future_helpers'] == accepted['future_helpers'], 'accepted operational helper inventory')
    for name, record in freeze['future_helpers'].items():
        helper = Path(__file__).resolve().parent / name
        need(helper.is_file() and not helper.is_symlink() and helper.stat().st_size == record['bytes']
             and hashlib.sha256(helper.read_bytes()).hexdigest() == record['sha256'],
             'reviewed operational helper changed')
    live_head = head
    if (a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists():
        integration = read('ACCEPTANCE_INTEGRATION_ADDENDUM.json')
        need(integration.get('accepted') is True and integration['original_audited_head'] == head,
             'integration acceptance')
        live_head = integration['integrated_head']
    need(merge.get('number') == 938 and merge.get('state') == 'MERGED'
         and merge.get('headRefOid') == live_head and merge.get('baseRefName') == 'main', 'merged PR/head/main destination')
    merged = merge['mergeCommit']['oid']
    ident = publication.get('id')
    need(type(ident) is int and ident > 0 and publication.get('state') == 'published'
         and publication.get('doi') == '10.5281/zenodo.'+str(ident)
         and publication.get('record_url') == 'https://zenodo.org/records/'+str(ident),
         'published ID/DOI/record')
    intent = read('publication/ZENODO_PUBLISH_INTENT.json')
    need(intent.get('action') == 'publish' and intent.get('pr') == 938
         and intent['accepted_freeze_sha256'] == pin and intent['merged_commit'] == merged and intent.get('merged_base') == 'main',
         'publication intent/accepted freeze/merge')
    destination = intent.get('destination_readback', {})
    need(type(destination) is dict, 'main destination evidence object')
    fresh = destination.get('actual_PR_readback', {})
    need(type(fresh) is dict, 'actual main destination readback object')
    need(destination.get('baseRefName') == 'main' and destination.get('merge_commit') == merged
         and destination.get('merge_commit_is_ancestor_of_observed_main') is True
         and type(destination.get('observed_remote_main')) is str
         and re.fullmatch('[0-9a-f]{40}', destination['observed_remote_main']) is not None
         and fresh.get('number') == 938 and fresh.get('state') == 'MERGED'
         and fresh.get('headRefOid') == live_head and fresh.get('baseRefName') == 'main'
         and fresh.get('mergeCommit') == {'oid': merged},
         'actual main destination readback/merge ancestry linkage')
    descriptor_raw = (a/'publication/zenodo-deposit.json').read_bytes()
    need(hashlib.sha256(descriptor_raw).hexdigest() == intent['descriptor_sha256']
         == freeze['files']['zenodo-deposit.json']['sha256'], 'exact descriptor')
    descriptor = json.loads(descriptor_raw)
    expected = []
    for item in descriptor['files']:
        record = freeze['files'][item['path']]
        data = (a/'publication'/item['path']).read_bytes()
        need(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'],
             'current accepted upload bytes')
        expected.append({'name':item['name'], 'size':record['bytes'], 'sha256':record['sha256']})
    need(len(expected) == 2 and publication['files'] == expected, 'published file fingerprints')
    stage = read('publication/ZENODO_STAGE.json')
    inspected = read('publication/ZENODO_INSPECT.json')
    need(stage.get('id') == ident and stage['files'] == expected, 'staged record/files')
    need(inspected.get('id') == ident and inspected.get('doi') == publication['doi']
         and inspected.get('state') == 'published' and inspected['files'] == expected,
         'published readback ID/DOI/files')
    if tracker is not None:
        need(tracker.get('confirmed') is True and tracker.get('readback_matches') is True
             and tracker.get('pr') == 938 and tracker.get('problem_id') == '30003634'
             and tracker.get('original_pr_head') == head and tracker.get('merged_head') == live_head
             and tracker.get('merge_commit') == merged and tracker.get('merged_base') == 'main' and tracker.get('accepted_freeze_sha256') == pin
             and tracker.get('doi') == publication['doi'] and tracker.get('zenodo_record_id') == ident,
             'tracker target/head/freeze/DOI')
        need(valid_tracker_range(tracker.get('updated_range')), 'tracker exact destination/columns/single data row')
        readback = read('TRACKER_READBACK.json')
        need(readback.get('range') == tracker['updated_range'], 'tracker exact returned/readback A1 range')
        need(tracker.get('spreadsheet_id') == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
             and tracker.get('gid') == 1254632077 and tracker.get('tab_title') == 'Math Puzzles'
             and len(tracker['row']) == 4 and tracker['row'][2] == 'https://doi.org/'+publication['doi']
             and read('TRACKER_READBACK.json').get('values') == [tracker['row']],
             'tracker destination/exact row readback')
    if native is not None:
        need(tracker is not None and native.get('push_confirmed') is True, 'native/tracker confirmation')
        event = native['published_event']
        need(event.get('id') == '30003634' and event.get('pr') == 938
             and event.get('doi') == publication['doi'] and event.get('original_pr_head') == head
             and event.get('accepted_freeze_sha256') == pin and event.get('merged_commit') == merged and event.get('merged_base') == 'main'
             and event.get('zenodo_record_id') == ident
             and event['evidence']['tracker_range'] == tracker['updated_range'],
             'native target/head/freeze/DOI/tracker')


def main():
    if (AUDIT/'NATIVE_PUBLICATION_RECEIPT.json').exists():
        raise RuntimeError('Native receipt already exists; inspect/read back instead of repeating the write')
    publication = json.loads((AUDIT / 'publication/ZENODO_PUBLISH.json').read_text())
    tracker = json.loads((AUDIT / 'TRACKER_RECEIPT.json').read_text())
    merge = json.loads((AUDIT / 'PR_MERGE_RECEIPT.json').read_text())
    accepted = json.loads((AUDIT / 'ACCEPTANCE.json').read_text())
    source = json.loads((AUDIT / 'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    verify_receipt_links(AUDIT, publication, merge, accepted, tracker)
    if not (publication['state'] == 'published' and type(publication['id']) is int and (publication['id'] > 0)):
        raise RuntimeError("Publication ledger guard: publication['state'] == 'published' and type(publication['id']) is int and (publication['id'] > 0)")
    if not publication['doi'] == f"10.5281/zenodo.{publication['id']}":
        raise RuntimeError('Publication ledger guard: publication[\'doi\'] == f"10.5281/zenodo.{publication[\'id\']}"')
    EVENT_ID = f"pr938_zenodo{publication['id']}_v1.0"
    if not (tracker['confirmed'] and tracker['readback_matches']):
        raise RuntimeError("Publication ledger guard: tracker['confirmed'] and tracker['readback_matches']")
    if not (merge['state'] == 'MERGED' and accepted['accepted']):
        raise RuntimeError("Publication ledger guard: merge['state'] == 'MERGED' and accepted['accepted']")
    note = f"Accepted and merged PR #938 after independent topology, planarGoeritz, algebraMeyer, source/model and reproducibility audits, two deep priority audits, fresh stronger-mechanism falsification and sequential NEW whole-package reviews. For every m>=3 and finite k>=1, P_m^(k) is not contained in integral smoothF1; hence source containment fails for every n>=1. Different existential witnesses may depend on finite depth. Original104-letter P3''' witness signature-2 preserved; finite checks separate from universal proof. Prior general tools explicitly credited to Gambaudo-Ghys, Calegari, Kawasaki etal2025Lemma7.12, Otto and Toffoli. No new general quasimorphism theorem, firstness or current-openness claim; no complete predecessor established by bounded primary search. Unrefereed extensively AI-assisted4-page v1.0 note and verification archive: {publication['doi']}; tracker {tracker['updated_range']} read back. Immutable original observed1/5 retained; one newly completed strengthening recorded by unmodified native CLI in isolated selected slice; combined known2/5, no verification turn added."



    for attempt in range(1, 7):
        parent = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
        run(['git', 'fetch', '--no-write-fetch-head', 'origin', parent])
        run(['git', 'merge-base', '--is-ancestor', merge['mergeCommit']['oid'], parent])
        catalogue = json.loads(blob(parent, 'unsolved_math_prioritization/catalog.json'))
        target = next((x for x in catalogue if str(x['id']) == KEY))
        if target.get('present') is not True or target.get('holds') != []:
            raise RuntimeError('Current main target absent or has unresolved review holds')
        if not target['statement_hash'] == source['statement_hash']:
            raise RuntimeError("Publication ledger guard: target['statement_hash'] == source['statement_hash']")
        if not target['review_hash'] == source['review_hash']:
            raise RuntimeError("Publication ledger guard: target['review_hash'] == source['review_hash']")
        queue = blob(parent, 'unsolved_math_prioritization/QUEUE.md')
        lines = queue.splitlines(keepends=True)
        hits = [i for i, s in enumerate(lines) if '| 30003634 /' in s]
        if not len(hits) == 1:
            raise RuntimeError('Publication ledger guard: len(hits) == 1')
        idx = hits[0]
        old = lines[idx]
        cells = old.rstrip('\n').split('|')
        if not cells[8].strip() in ['claimed_solved', 'preprint_published']:
            raise RuntimeError("Publication ledger guard: cells[8].strip() in ['claimed_solved', 'preprint_published']")
        if cells[8].strip() == 'preprint_published':
            if not publication['doi'] in old:
                raise RuntimeError("Publication ledger guard: publication['doi'] in old")
        else:
            if not cells[9].strip() == '1/5':
                raise RuntimeError("Publication ledger guard: cells[9].strip() == '1/5'")
            cells[8] = ' preprint_published '
            cells[9] = ' 2/5 '
            cells[11] = ' ' + cells[11].strip() + ' ' + note + ' '
            cells[12] = f" [{publication['doi']}](https://doi.org/{publication['doi']}) "
            lines[idx] = '|'.join(cells) + ('\n' if old.endswith('\n') else '')
        revised_queue = ''.join(lines)
        if not queue.replace(old, '', 1) == revised_queue.replace(lines[idx], '', 1):
            raise RuntimeError("Publication ledger guard: queue.replace(old, '', 1) == revised_queue.replace(lines[idx], '', 1)")
        state_raw = blob(parent, 'unsolved_math_prioritization/state.json')
        states = json.loads(state_raw)
        prior = states.get(KEY, {})
        if prior.get('doi'):
            if not prior['doi'] == publication['doi']:
                raise RuntimeError("Publication ledger guard: prior['doi'] == publication['doi']")
        event = {**prior, 'at': datetime.now(timezone.utc).isoformat(), 'id': KEY, 'status': 'preprint_published', 'note': note, 'doi': publication['doi'], 'pr': 938, 'event': 'audited_imported_candidate_publication', 'event_id': EVENT_ID, 'statement_hash': source['statement_hash'], 'review_hash': source['review_hash'], 'verified_candidate_approaches': 2, 'turn_count_status': 'original_observed_one_plus_one_genuinely_recorded_strengthening', 'original_total_attempt_count_known': False, 'proof_search_turns_added_by_audit': 1, 'turn_limit': 5, 'candidate_turn': 2, 'new_mechanism_native_receipt_sha256': hashlib.sha256((AUDIT/'strengthening/unsolved_math_prioritization/attempts/30003634/NATIVE_TURN_RECEIPT.json').read_bytes()).hexdigest(), 'original_pr_head': accepted['original_pr_head'], 'accepted_freeze_sha256': accepted['freeze_sha256'], 'merged_commit': merge['mergeCommit']['oid'], 'merged_base': 'main', 'zenodo_record_id': publication['id'], 'evidence': {'accepted_artifacts': EFFORT.relative_to(ROOT).as_posix() + '/audits/pr938_30003634/ACCEPTANCE.json', 'zenodo_record': publication['record_url'], 'tracker_range': tracker['updated_range'], 'source_free_archive_sha256': publication['files'][1]['sha256'], 'priority_limit': 'First priority unverified and not asserted', 'original_candidate_turns': 'original observed1/5 preserved; one new complete mechanism, combined known2/5; genuine isolated queue.py turn receipt and original-history absence disclosed'}}
        if 'turns_used' in prior and (type(prior['turns_used']) is not int or prior['turns_used'] > 2):
            raise RuntimeError('Newer target proof counter requires reconciliation')
        if 'turns_used' in prior and prior['turns_used'] != 2:
            event['previous_state_recorded_turns_used'] = prior['turns_used']
        event['turns_used'] = 2
        event['turns_used_interpretation'] = 'Known combined2/5: immutable initial observed1/5 plus one new complete stronger proof response; genuine unmodified isolated CLI history is preserved without backdating. Status event-tag inheritance does not add a turn.'
        revised_state = replace_entry(state_raw, KEY, event)
        history = blob(parent, 'unsolved_math_prioritization/history.jsonl')
        matches = [json.loads(s) for s in history.splitlines() if EVENT_ID in s]
        if matches:
            if not (len(matches) == 1 and matches[0]['doi'] == publication['doi']):
                raise RuntimeError("Publication ledger guard: len(matches) == 1 and matches[0]['doi'] == publication['doi']")
            revised_history = history
        else:
            revised_history = history + ('' if not history or history.endswith('\n') else '\n') + json.dumps(event, ensure_ascii=False) + '\n'
        changes = {'unsolved_math_prioritization/QUEUE.md': revised_queue, 'unsolved_math_prioritization/state.json': revised_state, 'unsolved_math_prioritization/history.jsonl': revised_history}
        tree = explicit_tree(parent, changes)
        changed_paths = run(['git', 'diff', '--name-only', parent, tree]).splitlines()
        if not set(changed_paths) <= set(changes):
            raise RuntimeError('Unexpected native publication path')
        sha = run(['git', 'commit-tree', tree, '-p', parent],
                  input='Record verified PR938 preprint DOI and tracker publication ledger\n')
        push = subprocess.run(['git', 'push', 'origin', sha + ':refs/heads/main'], cwd=ROOT, text=True, capture_output=True)
        if push.returncode == 0:
            receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'parent': parent, 'commit': sha, 'paths': changed_paths, 'published_event': event, 'push_confirmed': True, 'other_queue_rows_and_state_entries_preserved': True, 'shared_checkout_index_and_local_head_untouched': True, 'attempt': attempt}
            (AUDIT / 'NATIVE_PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps({'commit': sha, 'paths': changed_paths, 'doi': publication['doi']}, indent=2))
            return
        import re
        race=re.search(r"cannot lock ref 'refs/heads/main': is at ([0-9a-f]{40}) but expected ([0-9a-f]{40})",push.stderr)
        if 'non-fast-forward' not in push.stderr and 'fetch first' not in push.stderr and not (race and race[2]==parent and race[1]!=parent):
            raise RuntimeError(push.stderr)
    raise RuntimeError('main advanced in every attempt; native publication ledger still pending')
if __name__ == '__main__':
    main()
