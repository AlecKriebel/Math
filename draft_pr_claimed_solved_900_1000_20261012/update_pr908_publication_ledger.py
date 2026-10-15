"""Record the verified publication in remote main without touching shared files."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[1]
EFFORT = Path(__file__).resolve().parent
AUDIT = EFFORT / 'audits/pr908_30006191'
KEY = '30006191'
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

def main():
    publication = json.loads((AUDIT / 'publication/ZENODO_PUBLISH.json').read_text())
    tracker = json.loads((AUDIT / 'TRACKER_RECEIPT.json').read_text())
    merge = json.loads((AUDIT / 'PR_MERGE_RECEIPT.json').read_text())
    accepted = json.loads((AUDIT / 'ACCEPTANCE.json').read_text())
    source = json.loads((AUDIT / 'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    if not (publication['state'] == 'published' and type(publication['id']) is int and (publication['id'] > 0)):
        raise RuntimeError("Publication ledger guard: publication['state'] == 'published' and type(publication['id']) is int and (publication['id'] > 0)")
    if not publication['doi'] == f"10.5281/zenodo.{publication['id']}":
        raise RuntimeError('Publication ledger guard: publication[\'doi\'] == f"10.5281/zenodo.{publication[\'id\']}"')
    EVENT_ID = f"pr908_zenodo{publication['id']}_v1.0"
    if not (tracker['confirmed'] and tracker['readback_matches']):
        raise RuntimeError("Publication ledger guard: tracker['confirmed'] and tracker['readback_matches']")
    if not (merge['state'] == 'MERGED' and accepted['accepted']):
        raise RuntimeError("Publication ledger guard: merge['state'] == 'MERGED' and accepted['accepted']")
    note = f"Accepted and merged PR #908 after independent continuum-proof, operator-algebra, finite-computation, source/model and deep primary priority audits plus sequential fresh full-package reviews. Explicit d3 fixed smooth pair potential, fixed bounded interaction region and fixed annihilation mode; both unsmeared orderings give changing Slater vector/operator norm2 and state value4. Every fixed vector/normal state remains continuous. Earlier Siebert arxiv2609.34402v1 cluster/phase mechanism and direct qualitative cutoff adaptation credited; an audit-time energy bootstrap also recovers maximal cutoff limit and is not attributed as a stated prior theorem. First priority, quantitative novelty and continued openness not asserted; bounded coverage gaps disclosed. Unrefereed extensively AI-assisted v1.0 five-page note and source/verification archive: {publication['doi']}; tracker {tracker['updated_range']} read back. Literal OWR7/2025 p371 and norm topology p365. Original1/5 preserved."
    for attempt in range(1, 7):
        parent = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
        run(['git', 'fetch', '--no-write-fetch-head', 'origin', parent])
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
        hits = [i for i, s in enumerate(lines) if '| 30006191 /' in s]
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
        event = {**prior, 'at': datetime.now(timezone.utc).isoformat(), 'id': KEY, 'status': 'preprint_published', 'note': note, 'doi': publication['doi'], 'pr': 908, 'event': 'audited_imported_candidate_publication', 'event_id': EVENT_ID, 'statement_hash': source['statement_hash'], 'review_hash': source['review_hash'], 'turns_used': 1, 'turn_limit': 5, 'original_pr_head': accepted['original_pr_head'], 'evidence': {'accepted_artifacts': EFFORT.relative_to(ROOT).as_posix() + '/audits/pr908_30006191/ACCEPTANCE.json', 'zenodo_record': publication['record_url'], 'tracker_range': tracker['updated_range'], 'source_free_archive_sha256': publication['files'][1]['sha256'], 'priority_limit': 'First priority unverified and not asserted', 'original_candidate_turns': '1/5; imported PR proposal, not a new proof attempt'}}
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
                  input='Record verified PR908 preprint DOI and tracker publication ledger\n')
        push = subprocess.run(['git', 'push', 'origin', sha + ':refs/heads/main'], cwd=ROOT, text=True, capture_output=True)
        if push.returncode == 0:
            receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'parent': parent, 'commit': sha, 'paths': changed_paths, 'published_event': event, 'push_confirmed': True, 'other_queue_rows_and_state_entries_preserved': True, 'shared_checkout_index_and_local_head_untouched': True, 'attempt': attempt}
            (AUDIT / 'NATIVE_PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps({'commit': sha, 'paths': changed_paths, 'doi': publication['doi']}, indent=2))
            return
        if 'non-fast-forward' not in push.stderr and 'fetch first' not in push.stderr:
            raise RuntimeError(push.stderr)
    raise RuntimeError('main advanced in every attempt; native publication ledger still pending')
if __name__ == '__main__':
    main()
