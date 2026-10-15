#!/usr/bin/env python3
"""Draft exact-head QUEUE-only correction. Requires a genuine final evidence gate."""
import argparse
import base64
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.parse

PROGRAM = Path(__file__).resolve().parent
AUDIT = PROGRAM / 'audits/pr458_20000693'
REPO = 'AlecKriebel/Math'
ORIGINAL = '87a39f7b4e5ef81aacf98464f86586cc95684d7f'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
FORBIDDEN = {'private', 'private_sources', 'private_cases', 'mutation_fixtures',
             'venv', '.venv', '__pycache__', '.secrets', '.zenodo-state'}
RAW = {
    'source_admissibility': ('reviewer', 'problem_id', 'blocking_issues', 0, 0, 'unresolved_mathematical_gaps'),
    'euler_adversary': ('reviewer', 'problem_id', 'blocking_issues', 1, 1, 'unresolved_mathematical_gaps'),
    'reproduction': ('reviewer', 'problem_id', 'blocking_issues', 1, 3, 'unresolved_mathematical_gaps'),
    'whole_math_adversary': ('reviewer', 'problem_id', 'blocking_issues', 2, 4, 'unresolved_mathematical_gaps'),
    'unprimed_math_adversary': ('reviewer', 'problem_id', 'blocking_issues', 2, 4, 'unresolved_mathematical_gaps'),
    'priority_coverage': ('reviewer_task_identity', 'problem_id', 'blocking_findings', 1, 2, 'central_mathematical_gaps'),
    'priority_adversary': ('reviewer_task', 'problem', 'blocking_findings', 1, 5, 'central_mathematical_gaps'),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def integer(value, expected, message):
    require(type(value) is int and value == expected, message)


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def input_path(relative):
    require(type(relative) is str and relative != '' and not Path(relative).is_absolute()
            and '..' not in Path(relative).parts and not FORBIDDEN.intersection(Path(relative).parts)
            and Path(relative).as_posix() == relative and Path(relative).suffix != '.pyc', 'Unsafe evidence path')
    path = AUDIT / relative
    require(AUDIT.resolve() == AUDIT and path.resolve() == path and path.is_file()
            and not path.is_symlink() and path.stat().st_nlink == 1, 'Evidence topology')
    return path


def load(relative):
    return json.loads(input_path(relative).read_text())


def output_path(name):
    require(name in {'STATUS_REPAIR_PREFLIGHT.json', 'STATUS_REPAIR_OPERATION.json',
                     'STATUS_REPAIR_RECEIPT.json'}, 'Unknown output')
    path = AUDIT / name
    require(AUDIT.resolve() == AUDIT and not AUDIT.is_symlink()
            and path.resolve() == path and not path.is_symlink(), 'Output alias')
    if path.exists():
        require(path.is_file() and path.stat().st_nlink == 1, 'Nonregular/hardlinked output')
    return path


def dump(name, value):
    output_path(name).write_text(json.dumps(value, indent=2) + '\n')


def api(endpoint, payload=None, method='POST'):
    cmd = ['gh', 'api', 'repos/' + REPO + '/' + endpoint]
    if payload is not None:
        cmd += ['--method', method, '--input', '-']
    result = subprocess.run(cmd, input=None if payload is None else json.dumps(payload),
                            capture_output=True, text=True)
    require(result.returncode == 0, result.stderr.strip())
    return json.loads(result.stdout)


def eligible(branch):
    pr = api('pulls/458')
    require(pr['state'] == 'open' and pr['draft'] is True and pr['head']['sha'] == ORIGINAL
            and pr['head']['ref'] == branch and pr['head']['repo']['full_name'] == REPO
            and pr['base']['ref'] == 'main' and pr['base']['repo']['full_name'] == REPO,
            'Original open draft head/repository/base changed')
    require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == ORIGINAL,
            'Original branch ref changed')


def validate_gate():
    gate = load('PRIORITY_DISPOSITION_GATE.json')
    require(gate.get('verdict') == 'ACCEPTED_PRIORITY_CLASSIFICATION'
            and type(gate.get('pr')) is int and gate['pr'] == 458
            and gate.get('problem_id') == '20000693' and gate.get('original_head') == ORIGINAL
            and gate.get('recommended_status') == 'already_solved'
            and gate.get('acceptance_scope') == 'one_row_priority_correction_then_immediate_skip'
            and gate.get('root_read_entire_final_reports') is True
            and gate.get('publication_accepted') is False
            and gate.get('helper_sha256') == digest(Path(__file__))['sha256'],
            'Final exact classification/helper gate absent')
    require(gate.get('retained_original_publication_blockers') == ['H1', 'V1']
            and gate.get('retained_original_publication_correction_groups') == ['H1', 'V1', 'P2', 'C3']
            and gate.get('priority_coverage_already_solved_recommendation') is False,
            'Raw publication findings or distinct priority recommendation erased')
    evidence = {}
    require(type(gate.get('reviewed_files')) is list and len(gate['reviewed_files']) > 0, 'Empty evidence gate')
    for entry in gate['reviewed_files']:
        path = input_path(entry['path'])
        require(entry['path'] not in evidence and type(entry.get('bytes')) is int and entry['bytes'] > 0
                and type(entry.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}', entry['sha256'])
                and digest(path) == {'bytes': entry['bytes'], 'sha256': entry['sha256']},
                'Evidence duplicate/type/byte binding differs')
        evidence[entry['path']] = entry
    mandatory = {'SOURCE_RECEIPT.json', 'pr_metadata.json', 'selected_queue_row.md',
                 'DISPOSITION_SYNTHESIS.md', 'DRAFT_PRIORITY_DISPOSITION.md', 'MATHEMATICAL_REVIEW_SUMMARY.md',
                 'PRIORITY_REVIEW_SUMMARY.md', 'ROOT_PRIORITY_RECONSTRUCTION.md',
                 'HYBRID_LOCAL_CLARIFICATION.md', 'CONTEXT_INDEPENDENCE_CAVEAT.md',
                 'PRIORITY_ADVERSARY_FAMILY_READBACK.json', 'PRIORITY_COVERAGE_FAMILY_READBACK.json',
                 'CLASSIFICATION_FAMILY_READBACK.json'}
    require(mandatory <= evidence.keys(), 'Mandatory complete source/decision evidence absent')
    source = load('SOURCE_RECEIPT.json')
    require(source.get('pr') == 458 and source.get('problem_id') == '20000693'
            and source.get('head_sha') == ORIGINAL and source.get('scope_gate') == 'exact claimed_solved'
            and type(source.get('files')) is list and len(source['files']) == 27, 'Frozen source identity')
    seen_sources = set()
    for record in source['files']:
        require(record['path'].startswith('unsolved_math_prioritization/attempts/20000693/'), 'Other problem source')
        relative = 'source_snapshot/' + record['path']
        require(relative not in seen_sources and relative in evidence
                and digest(input_path(relative)) == {'bytes': record['bytes'], 'sha256': record['sha256']},
                'Original source absent or changed')
        seen_sources.add(relative)
    metadata = load('pr_metadata.json')
    require(type(metadata.get('number')) is int and metadata['number'] == 458
            and metadata.get('headRefOid') == ORIGINAL and metadata.get('state') == 'OPEN'
            and metadata.get('isDraft') is True and metadata.get('baseRefName') == 'main', 'Metadata identity')
    require(type(gate.get('reviews')) is list and len(gate['reviews']) == 9, 'Nine actual complete reviews required')
    families = set()
    for review in gate['reviews']:
        family = review['family']
        require(family in set(RAW) | {'classification_adversary', 'disposition_adversary'}
                and family not in families, 'Unknown/duplicate family')
        families.add(family)
        directory = family
        if family == 'disposition_adversary':
            match = re.fullmatch('/root/pr458_(disposition_adversary[1-9][0-9]*)', review['reviewer'])
            require(match is not None, 'Fresh numbered final operations reviewer required')
            directory = match.group(1)
        else:
            require(review['reviewer'] == '/root/pr458_' + family, 'Reviewer provenance')
        report = 'reviews/' + directory + '/REPORT.md'
        result_path = 'reviews/' + directory + '/RESULT.json'
        manifest_path = 'reviews/' + directory + '/PUBLIC_FILES.json'
        require(review['report_path'] == report and review['result_path'] == result_path
                and {report, result_path, manifest_path} <= evidence.keys(), 'Report/result/manifest disconnected')
        manifest = load(manifest_path)
        require(type(manifest.get('files')) is list and len(manifest['files']) > 0, 'Empty positive manifest')
        payloads = set()
        for record in manifest['files']:
            require(type(record.get('path')) is str and record['path'] != ''
                    and not Path(record['path']).is_absolute()
                    and Path(record['path']).as_posix() == record['path'], 'Manifest relative path')
            relative = 'reviews/' + directory + '/' + record['path']
            require(relative not in payloads and relative != manifest_path and relative in evidence
                    and digest(input_path(relative)) == {'bytes': record['bytes'], 'sha256': record['sha256']},
                    'Complete public payload disconnected or drifted')
            payloads.add(relative)
        result = load(result_path)
        if family in RAW:
            reviewer_key, problem_key, blocker_key, blockers, repairs, gap_key = RAW[family]
        else:
            reviewer_key = 'reviewer_task_identity' if family == 'classification_adversary' else 'reviewer'
            problem_key = 'problem_id'
        require(type(result.get('pr')) is int and result['pr'] == 458
                and result.get(problem_key) == '20000693' and result.get('frozen_head') == ORIGINAL
                and result.get(reviewer_key) == review['reviewer'], 'Actual reviewer result identity')
        integer(review.get('unresolved_disposition_issues'), 0, 'Accepted classification has unresolved issues')
        if family in RAW:
            integer(result.get(blocker_key), blockers, 'Raw family blockers changed')
            integer(result.get('required_repairs'), repairs, 'Raw family repairs changed')
            integer(result.get(gap_key), 0, 'Central heuristic gap')
            integer(review.get('raw_blocking_findings'), blockers, 'Gate erased raw blockers')
            integer(review.get('raw_required_repairs'), repairs, 'Gate erased raw repairs')
            for key in ['unresolved_central_arithmetic_gaps', 'unresolved_central_model_application_gaps',
                        'unresolved_central_model_construction_gaps', 'required_original_proof_repairs']:
                if key in result:
                    integer(result[key], 0, 'Additional central/proof gap: ' + key)
            if family == 'unprimed_math_adversary':
                integer(result.get('blocking_findings'), 2, 'Unprimed blocker aliases differ')
            if family == 'priority_adversary':
                require(result.get('status_recommendation') == 'already_solved'
                        and len(result.get('blocking_issues', [])) == 1
                        and len(result.get('raw_required_repairs', [])) == 5
                        and len(result.get('unresolved_mathematical_gaps', [])) == 3,
                        'Priority-adversary recommendation/theorem gaps differ')
            elif family == 'priority_coverage':
                require(result.get('status_recommendation') ==
                        'conditionally_accept_clarified_heuristic_after_required_repairs; do_not_approve_frozen_packet_as_written; novelty_not_demonstrated'
                        and result.get('acceptance_scope', {}).get('publication_or_gate_authorization') is False
                        and len(result.get('unresolved_mathematical_gaps', [])) == 3,
                        'Distinct conditional-heuristic recommendation relabeled')
            continue
        integer(review.get('raw_blocking_findings'), 0, 'Final scope blockers')
        integer(review.get('raw_required_repairs'), 0, 'Final scope repairs')
        for key in ['blocking_findings', 'required_repairs']:
            integer(result.get(key), 0, 'Unresolved final classification/operations ' + key)
        require(result.get('status_recommendation') == 'already_solved', 'Final classification recommendation')
        if family == 'classification_adversary':
            integer(result.get('central_mathematical_gaps'), 0, 'Classification central heuristic gap')
            require(result.get('recommendation_action') ==
                    'scope_qualified_status_and_findings_only_correction_then_immediate_exclusion'
                    and result.get('authority', {}).get('operational_action_authorized_by_this_review') is False
                    and result.get('limits', {}).get('publication_readiness_certified') is False,
                    'Conceptual reviewer misrepresented as operations approval')
            later = load('reviews/classification_adversary/LATER_EXPOSURE_BINDINGS.json')
            draft = [entry for entry in later['files'] if entry['path'] == 'DRAFT_PRIORITY_DISPOSITION.md']
            require(len(draft) == 1 and draft[0]['sha256'] == evidence['DRAFT_PRIORITY_DISPOSITION.md']['sha256'],
                    'Classification reviewer binds different draft')
        else:
            integer(result.get('unresolved_disposition_issues'), 0, 'Operations disposition issues')
            require(result.get('acceptance_scope') == 'one_row_priority_correction_then_immediate_skip'
                    and result.get('publication_accepted') is False, 'Operations acceptance scope')
            require(result.get('reviewed_helper_sha256') == gate['helper_sha256']
                    and result.get('reviewed_synthesis_sha256') == evidence['DISPOSITION_SYNTHESIS.md']['sha256'],
                    'Final operations reviewer binds different helper/synthesis')
    require(families == set(RAW) | {'classification_adversary', 'disposition_adversary'}, 'Missing review family')
    parsed = urllib.parse.urlsplit(gate['published_disposition_url'])
    relative = str((AUDIT / 'DISPOSITION_SYNTHESIS.md').relative_to(PROGRAM.parent))
    match = re.fullmatch('/AlecKriebel/Math/blob/([0-9a-f]{40})/' + re.escape(relative), parsed.path)
    require(parsed.scheme == 'https' and parsed.netloc == 'github.com' and not parsed.query
            and not parsed.fragment and match is not None
            and gate.get('published_disposition_sha256') == evidence['DISPOSITION_SYNTHESIS.md']['sha256'],
            'Exact immutable published disposition URL/hash absent')
    return gate, match.group(1), relative


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    for name in ['STATUS_REPAIR_PREFLIGHT.json', 'STATUS_REPAIR_OPERATION.json', 'STATUS_REPAIR_RECEIPT.json']:
        output_path(name)
    if args.apply:
        require(not (AUDIT / 'STATUS_REPAIR_OPERATION.json').exists(), 'Prior operation: no repeated mutation')
    # Administrative fresh-head/status gate precedes any mathematical-evidence reread.
    branch = load('pr_metadata.json')['headRefName']
    eligible(branch)
    original = api('git/commits/' + ORIGINAL)
    tree_sha = original['tree']['sha']
    for part in QUEUE.split('/'):
        matches = [x for x in api('git/trees/' + tree_sha)['tree'] if x['path'] == part]
        require(len(matches) == 1, 'QUEUE Git tree path not unique')
        item = matches[0]
        tree_sha = item['sha']
    require(item['type'] == 'blob' and item['mode'] == '100644', 'QUEUE not regular Git blob')
    before = base64.b64decode(api('git/blobs/' + tree_sha)['content'])
    source = load('SOURCE_RECEIPT.json')
    require(hashlib.sha256(before).hexdigest() == source['queue_sha256'], 'Frozen original QUEUE mismatch')
    lines = before.decode().splitlines(keepends=True)
    headers = [x for x in lines if x.startswith('|') and 'ID / code' in x and 'Status' in x]
    require(len(headers) == 1, 'QUEUE header not unique')
    columns = [x.strip() for x in headers[0].split('|')[1:-1]]
    require(len(set(columns)) == len(columns) and {'Status', 'Turns', 'DOI', 'Findings'} <= set(columns), 'QUEUE schema')
    indices = [i for i, x in enumerate(lines) if x.startswith('|')
               and len(x.split('|')) > 2 and x.split('|')[2].strip().startswith('20000693 /')]
    require(len(indices) == 1, 'Selected row not unique')
    index = indices[0]
    old_row = lines[index].rstrip('\r\n')
    require(old_row == source['selected_queue_row'], 'Selected frozen row bytes differ')
    cells = old_row.split('|')[1:-1]
    require(len(cells) == len(columns), 'Selected row schema')
    require(cells[columns.index('Status')].strip() == 'claimed_solved', 'Excluded status: stop without processing')
    require(cells[columns.index('Turns')].strip() == '1/5'
            and cells[columns.index('DOI')].strip() == '', 'Author turns/DOI drift')
    gate, published_commit, published_path = validate_gate()
    published = api('contents/' + published_path + '?ref=' + published_commit)
    require(published['type'] == 'file' and published['path'] == published_path
            and published['encoding'] == 'base64', 'Published synthesis not a file')
    require(base64.b64decode(''.join(published['content'].split()), validate=True)
            == input_path('DISPOSITION_SYNTHESIS.md').read_bytes(),
            'Immutable published synthesis bytes differ')
    old_cells = list(cells)
    cells[columns.index('Status')] = ' already_solved '
    finding = ('2026-10-12: Priority correction at the source leading fixed-Dirichlet heuristic level: '
               'Heap2013 Conjecture4/section7 already gives the constituent product mechanism and joint Euler/Barnes '
               'constant for integer multiplicities/common real weight; Milinovich--Turnage-Butterbaugh2014 gives '
               'the independent-real exponent; Sahay2021v1 gives common-modulus integer Dirichlet tuples with deletions. '
               'Valid credited synthesis; actual general asymptotic unproved. No single full independent-real/differing-'
               'imprimitive-level prior statement, earlier explicit numbered answer, first solver, exhaustive search or '
               'universal imprimitive resolution certified. Raw original publication H1/V1 blockers and H1/V1/P2/C3 '
               'correction groups retained. [Independent disposition audit](' + gate['published_disposition_url'] + '). '
               'Corrected to already_solved and immediately skipped; no paper, DOI or merge.')
    require('|' not in finding and '\n' not in finding and '\r' not in finding, 'Invalid finding cell')
    cells[columns.index('Findings')] = ' ' + finding + ' '
    require([i for i, (a, b) in enumerate(zip(old_cells, cells)) if a != b]
            == sorted([columns.index('Status'), columns.index('Findings')]), 'Unexpected cell alteration')
    ending = '\r\n' if lines[index].endswith('\r\n') else '\n' if lines[index].endswith('\n') else ''
    lines[index] = '|' + '|'.join(cells) + '|' + ending
    after = ''.join(lines).encode()
    require(len(before.decode().splitlines()) == len(after.decode().splitlines())
            and [i for i, (a, b) in enumerate(zip(before.decode().splitlines(), after.decode().splitlines())) if a != b] == indices,
            'Nonselected QUEUE alteration')
    summary = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pr': 458,
               'problem_id': '20000693', 'old_status': 'claimed_solved', 'new_status': 'already_solved',
               'old_head': ORIGINAL, 'branch': branch, 'files_changed': [QUEUE],
               'old_queue_sha256': hashlib.sha256(before).hexdigest(), 'new_queue_sha256': hashlib.sha256(after).hexdigest(),
               'selected_old_row': old_row, 'selected_new_row': lines[index].rstrip('\r\n'),
               'state': 'read_only_preflight', 'shared_checkout_index': 'untouched main',
               'subsequent_scope': 'immediate skip: no further audit/repair/paper/Zenodo/tracker/merge/close/comment'}
    dump('STATUS_REPAIR_PREFLIGHT.json', summary)
    if not args.apply:
        print(json.dumps(summary, indent=2))
        return
    require(not (AUDIT / 'STATUS_REPAIR_OPERATION.json').exists(), 'Prior operation: no repeated mutation')
    blob = api('git/blobs', {'content': base64.b64encode(after).decode(), 'encoding': 'base64'})['sha']
    new_tree = api('git/trees', {'base_tree': original['tree']['sha'],
                    'tree': [{'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': blob}]})['sha']
    eligible(branch)
    commit = api('git/commits', {'message': 'Correct prior Dirichlet-product heuristic classification after independent audit',
                               'tree': new_tree, 'parents': [ORIGINAL]})['sha']
    comparison = api('compare/' + ORIGINAL + '...' + commit)
    require([x['filename'] for x in comparison['files']] == [QUEUE], 'Commit changed other paths')
    summary.update(state='commit_created_before_ref_update', repair_commit=commit, queue_git_blob_sha=blob)
    dump('STATUS_REPAIR_OPERATION.json', summary)
    eligible(branch)
    ref = 'git/refs/heads/' + urllib.parse.quote(branch, safe='')
    try:
        api(ref, {'sha': commit, 'force': False}, method='PATCH')
    except RuntimeError:
        require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == commit,
                'Branch update uncertain; no retry')
    require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == commit,
            'Branch readback differs')
    require(base64.b64decode(api('git/blobs/' + blob)['content']) == after, 'QUEUE blob exact bytes differ')
    summary.update(state='status_repair_verified_immediately_excluded',
                   verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   readback='Exact selected branch ref and immutable QUEUE blob bytes matched',
                   basis='Prior source-level fixed-Dirichlet leading heuristic; enlarged literal tuple gap and raw original publication issues retained',
                   concurrency_scope='Original head/ref checked before nonforced PATCH; this is not atomic expected-old-SHA CAS')
    dump('STATUS_REPAIR_RECEIPT.json', summary)
    print(json.dumps({'pr': 458, 'new_status': 'already_solved', 'repair_commit': commit,
                      'state': summary['state'], 'subsequent_scope': summary['subsequent_scope']}, indent=2))


if __name__ == '__main__':
    main()
