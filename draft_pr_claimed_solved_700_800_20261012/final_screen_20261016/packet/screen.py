"""Read-only complete-number PR screen; examines only each open draft's own row.

Only network operations are authenticated GraphQL queries and immutable raw GETs.
Only Git operation is cat-file on already-present objects.  All writes are local
to this dedicated screen directory.  This does not audit mathematical work.
"""
import collections
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
PROGRAM = HERE.parent
REPO = PROGRAM.parent
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PROCESSED = [718, 734, 742, 764, 765, 767, 778, 781, 786, 788, 789]
CURRENT = [799]
FIELDS = 'number title state isDraft merged headRefOid headRefName closedAt url mergeCommit { oid }'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob_oid(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def require(test, message):
    if not test:
        raise RuntimeError(message)


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def query(query_text, label):
    require(query_text.startswith('query '), 'Only GraphQL queries permitted')
    started = now()
    result = subprocess.run(['gh', 'api', 'graphql', '--input', '-'],
                            input=json.dumps({'query': query_text}), text=True,
                            capture_output=True, cwd=REPO, check=True)
    response = json.loads(result.stdout)
    require(not response.get('errors'), 'GraphQL errors')
    record = {'started_at': started, 'finished_at': now(),
              'transport': 'authenticated gh api graphql; query only',
              'query': query_text, 'response': response}
    write(label + '.json', record)
    return response['data']['repository']


def inventory(prefix):
    rows = []
    for index, start in enumerate(range(700, 801, 25)):
        numbers = list(range(start, min(start + 25, 801)))
        aliases = ' '.join(f'p{n}:pullRequest(number:{n}){{{FIELDS}}}' for n in numbers)
        result = query('query { repository(owner:"AlecKriebel",name:"Math") { ' +
                       aliases + ' } }', prefix + f'_{index:02d}')
        require(set(result) == {f'p{n}' for n in numbers}, 'Incomplete alias set')
        for number in numbers:
            row = result[f'p{number}']
            require(row is not None and row['number'] == number, 'Missing/misnumbered PR')
            rows.append(row)
    require([r['number'] for r in rows] == list(range(700, 801)), 'Coverage mismatch')
    return rows


def extract_own_row(raw, problem):
    # Deliberately match only the requested numeric problem key.  Do not parse
    # statuses of other problems carried in the same immutable queue blob.
    pattern = re.compile(rb'^\|\s*\d+\s*\|\s*' + problem.encode() + rb'\s*(?:/|\|)')
    matches = [line.decode('utf-8') for line in raw.splitlines() if pattern.match(line)]
    require(len(matches) == 1, 'Ambiguous/missing own queue row for ' + problem)
    cells = [c.strip() for c in matches[0].strip('|').split('|')]
    require(len(cells) == 12 and re.match(r'^' + problem + r'\s*(?:/|$)', cells[1]),
            'Unexpected own-row schema/key')
    return matches[0], cells[7], cells[8]


def main():
    started = now()
    source_raw = (PROGRAM / 'pr_inventory.json').read_bytes()
    initial = json.loads(source_raw)
    initial_map = {row['number']: row for row in initial['range_prs']}
    require(set(initial_map) == set(range(700, 801)), 'Initial mapping incomplete')
    before = inventory('metadata_before')
    open_drafts = [r for r in before if r['state'] == 'OPEN' and r['isDraft']]
    sources = {}
    for index, start in enumerate(range(0, len(open_drafts), 20)):
        group = open_drafts[start:start + 20]
        aliases = ' '.join(f'q{r["number"]}:object(expression:"{r["headRefOid"]}:{QUEUE}")'
                           '{ ... on Blob { oid byteSize } }' for r in group)
        response = query('query { repository(owner:"AlecKriebel",name:"Math") { ' +
                         aliases + ' } }', f'queue_oids_{index:02d}')
        require(set(response) == {f'q{r["number"]}' for r in group}, 'Queue alias mismatch')
        for pr in group:
            sources[pr['number']] = response[f'q{pr["number"]}']
    screened = []
    for pr in before:
        record = dict(pr)
        record['problem_id'] = initial_map[pr['number']]['problem_id']
        if pr['state'] != 'OPEN' or not pr['isDraft']:
            record.update(disposition='not_open_draft_metadata_only', queue_inspected=False)
            screened.append(record)
            continue
        problem = record['problem_id']
        require(problem in re.findall(r'(?<!\d)\d{4,8}(?!\d)', pr['headRefName']),
                'Initial problem mapping not authenticated by current branch key')
        oid_record = sources[pr['number']]
        require(oid_record is not None and re.fullmatch('[0-9a-f]{40}', oid_record['oid']),
                'No authenticated immutable queue blob')
        result = subprocess.run(['git', 'cat-file', 'blob', pr['headRefOid'] + ':' + QUEUE],
                                capture_output=True, cwd=REPO)
        method = 'git cat-file blob; existing immutable local object; no fetch/write'
        if result.returncode == 0:
            raw = result.stdout
        else:
            method = 'immutable raw.githubusercontent.com HTTPS GET; no Git writes'
            url = 'https://raw.githubusercontent.com/AlecKriebel/Math/' + pr['headRefOid'] + '/' + QUEUE
            with urllib.request.urlopen(url, timeout=45) as response:
                raw = response.read()
        require(blob_oid(raw) == oid_record['oid'] and len(raw) == oid_record['byteSize'],
                'Source blob identity/length mismatch')
        own_row, status, turns = extract_own_row(raw, problem)
        eligible = status == 'claimed_solved'
        record.update(queue_inspected=True, observed_at=now(), queue_path=QUEUE,
                      queue_blob_oid=oid_record['oid'], queue_blob_sha256=sha(raw),
                      queue_blob_bytes=len(raw), own_row=own_row,
                      own_row_sha256=sha(own_row.encode()), queue_status=status,
                      queue_turns=turns, source_read_method=method,
                      disposition='eligible_current' if eligible else 'skipped_out_of_scope',
                      initial_head_unchanged=pr['headRefOid'] == initial_map[pr['number']]['headRefOid'],
                      initial_status_unchanged=status == initial_map[pr['number']]['queue_status'])
        screened.append(record)
    after = inventory('metadata_after')
    require(before == after, 'Metadata changed during screen; preserve evidence and obtain a new screen')
    current_eligible = [r['number'] for r in screened if r['disposition'] == 'eligible_current']
    unprocessed = sorted(set(current_eligible) - set(PROCESSED))
    new_eligible = sorted(set(unprocessed) - set(CURRENT))
    summary = {
        'schema': 'read-only-final-eligibility-screen-v1', 'started_at': started,
        'finished_at': now(), 'repository': 'AlecKriebel/Math',
        'range_inclusive': [700, 800], 'order': 'ascending',
        'expected_numbers': list(range(700, 801)), 'coverage_complete': True,
        'metadata_stable_across_complete_before_after_inventories': True,
        'initial_mapping_sha256': sha(source_raw), 'numbers_accounted': len(screened),
        'metadata_state_counts': dict(collections.Counter(r['state'] for r in screened)),
        'merged_numbers': [r['number'] for r in screened if r['merged']],
        'closed_unmerged_numbers': [r['number'] for r in screened if r['state'] == 'CLOSED' and not r['merged']],
        'open_draft_count': len(open_drafts),
        'open_draft_status_counts': dict(collections.Counter(r['queue_status'] for r in screened if r['queue_inspected'])),
        'current_exact_claimed_solved_numbers': current_eligible,
        'already_processed_numbers_supplied_by_parent': PROCESSED,
        'currently_in_review_numbers_supplied_by_parent': CURRENT,
        'eligible_not_yet_processed_numbers': unprocessed,
        'newly_eligible_outside_known_current_case_numbers': new_eligible,
        'scope': 'Metadata for every integer PR number; own exact-head QUEUE row for OPEN DRAFT PRs only. No mathematical files read or reviewed. No external mutations.',
        'authentication': 'GitHub authenticated GraphQL query response binds every exact commit expression to its QUEUE blob Git OID; full read bytes reproduce this Git OID and length before extracting only the own row.',
        'limitations': 'Point-in-time metadata screen. GitHub API responses are authenticated transport evidence, not independently signed attestations. Later PR edits require a new check.',
        'rows': screened}
    write('CERTIFICATE.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
