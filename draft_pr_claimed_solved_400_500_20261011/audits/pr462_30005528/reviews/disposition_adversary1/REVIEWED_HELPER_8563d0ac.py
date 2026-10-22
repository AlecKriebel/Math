#!/usr/bin/env python3
"""Exact-head one-row priority correction; no action without a final review gate."""
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
AUDIT = PROGRAM / 'audits/pr462_30005528'
REPO = 'AlecKriebel/Math'
ORIGINAL = '3d5701d67e18745715d384c3db3fbee588b42a98'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def api(endpoint, payload=None, method='POST'):
    cmd = ['gh', 'api', 'repos/' + REPO + '/' + endpoint]
    if payload is not None:
        cmd += ['--method', method, '--input', '-']
    result = subprocess.run(cmd, input=None if payload is None else json.dumps(payload), capture_output=True, text=True)
    require(result.returncode == 0, result.stderr.strip())
    return json.loads(result.stdout)

def output_path(name):
    path = AUDIT / name
    require(AUDIT.resolve() == AUDIT and not AUDIT.is_symlink(), 'Output directory alias')
    require(not path.is_symlink(), 'Output symlink')
    if path.exists():
        require(path.is_file() and path.stat().st_nlink == 1, 'Nonregular or hardlinked output')
    return path

def dump(name, value):
    path = output_path(name)
    # Each fixed destination was checked before dispatch; writes stay in the audit folder.
    path.write_text(json.dumps(value, indent=2) + '\n')

def eligible(branch):
    pr = api('pulls/462')
    require(pr['state'] == 'open' and pr['draft'] is True and pr['head']['sha'] == ORIGINAL
            and pr['head']['ref'] == branch and pr['head']['repo']['full_name'] == REPO
            and pr['base']['ref'] == 'main' and pr['base']['repo']['full_name'] == REPO,
            'Original open draft head/repository/base changed')
    require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == ORIGINAL,
            'Original branch ref changed')
    return pr

def zero(value, message):
    require(type(value) is int and value == 0, message)

def validate_gate():
    gate = json.loads((AUDIT / 'PRIORITY_DISPOSITION_GATE.json').read_text())
    require(gate.get('verdict') == 'ACCEPTED_PRIORITY_CLASSIFICATION' and gate.get('pr') == 462
            and gate.get('problem_id') == '30005528' and gate.get('original_head') == ORIGINAL
            and gate.get('recommended_status') == 'already_solved'
            and gate.get('acceptance_scope') == 'one_row_priority_correction_then_immediate_skip',
            'Final exact disposition gate absent')
    require(gate.get('root_read_entire_final_reports') is True and gate.get('helper_sha256') == sha(Path(__file__)),
            'Root acceptance or reviewed helper binding absent')
    evidence = {}
    require(type(gate.get('reviewed_files')) is list and len(gate['reviewed_files']) > 0, 'Empty evidence gate')
    forbidden = {'private_sources', 'private_cases', 'mutation_fixtures', '__pycache__', 'venv', '.venv', '.secrets', '.zenodo-state'}
    for entry in gate['reviewed_files']:
        relative = entry['path']
        require(type(relative) is str and not Path(relative).is_absolute()
                and '..' not in Path(relative).parts and not (set(Path(relative).parts) & forbidden)
                and relative not in evidence, 'Invalid or duplicate evidence path')
        path = AUDIT / relative
        require(path.resolve() == path and path.is_file() and not path.is_symlink(), 'Evidence alias/nonregular file')
        require(type(entry.get('bytes')) is int and entry['bytes'] > 0
                and type(entry.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}', entry['sha256'])
                and path.stat().st_size == entry['bytes'] and sha(path) == entry['sha256'], 'Accepted evidence drift')
        evidence[relative] = entry
    mandatory = {'SOURCE_RECEIPT.json', 'pr_metadata.json', 'selected_queue_row.md', 'DISPOSITION_SYNTHESIS.md',
                 'reviews/priority/APPLICABILITY_CHAIN.md', 'reviews/priority/SOURCE_RECEIPT.json',
                 'reviews/priority/SEARCH_COVERAGE.md', 'MATHEMATICAL_FAMILY_READBACK.json',
                 'PRIORITY_FAMILY_READBACK.json', 'CANDIDATE_FAMILY_READBACK.json'}
    require(mandatory <= evidence.keys(), 'Required source/synthesis/application evidence absent')
    source = json.loads((AUDIT / 'SOURCE_RECEIPT.json').read_text())
    require(source['pr'] == 462 and source['problem_id'] == '30005528' and source['head_sha'] == ORIGINAL
            and source['scope_gate'] == 'exact claimed_solved' and len(source['files']) == 12,
            'Frozen eligible source identity mismatch')
    frozen_paths = set()
    for entry in source['files']:
        require(entry['path'].startswith('unsolved_math_prioritization/attempts/30005528/'), 'Other problem source')
        relative = 'source_snapshot/' + entry['path']
        require(relative not in frozen_paths and relative in evidence
                and evidence[relative]['bytes'] == entry['bytes']
                and evidence[relative]['sha256'] == entry['sha256'], 'Frozen source missing from acceptance')
        frozen_paths.add(relative)
    metadata = json.loads((AUDIT / 'pr_metadata.json').read_text())
    require(metadata['number'] == 462 and metadata['headRefOid'] == ORIGINAL
            and metadata['state'] == 'OPEN' and metadata['isDraft'] is True
            and metadata['baseRefName'] == 'main', 'Original metadata identity mismatch')
    config = {
        'source_admissibility': ('source_admissibility', 'RESULT.json'),
        'dynamical_adversary': ('dynamical_adversary', 'RESULT.json'),
        'reproduction': ('reproduction', 'RESULT.json'),
        'priority': ('priority', 'DECISION.json'),
        'candidate_adversary': ('candidate_adversary', 'RESULT.json'),
        'disposition_adversary': (None, 'RESULT.json'),
    }
    require(type(gate.get('reviews')) is list and len(gate['reviews']) == len(config), 'Six complete reviews required')
    families = set()
    for review in gate['reviews']:
        family = review['family']
        require(family in config and family not in families, 'Duplicate or unknown review family')
        families.add(family)
        directory, result_name = config[family]
        if directory is None:
            match = re.fullmatch('/root/pr462_(disposition_adversary[1-9][0-9]*)', review['reviewer'])
            require(match is not None, 'A fresh numbered final disposition reviewer is required')
            directory = match.group(1)
        else:
            require(review['reviewer'] == '/root/pr462_' + directory, 'Review task provenance mismatch')
        report_path = 'reviews/' + directory + '/REPORT.md'
        result_path = 'reviews/' + directory + '/' + result_name
        require(review['report_path'] == report_path and review['result_path'] == result_path
                and report_path in evidence and result_path in evidence, 'Final report/result evidence disconnected')
        result = json.loads((AUDIT / result_path).read_text())
        require(type(result.get('pr')) is int and result.get('pr') == 462 and str(result.get('problem_id')) == '30005528'
                and result.get('frozen_head') == ORIGINAL, 'Actual result input identity mismatch')
        zero(review.get('unresolved_disposition_issues'), 'Unresolved accepted-disposition issue')
        if family == 'priority':
            require(result.get('reviewer') == review['reviewer']
                    and result.get('status_recommendation') == 'already_solved'
                    and result.get('decision_type') == 'PRIOR_THEOREM_COVERAGE'
                    and result.get('first_priority_certified') is False
                    and result.get('earlier_explicit_numbered_answer_located') is False
                    and result.get('status_action_taken') is False
                    and result.get('math_application_gap', {}).get('literal_target') ==
                    'none identified: all legal words are forced graph orbits; all-path limsup lower bound, attained infimum, continuous positive normalization and every-period exclusion are checked in APPLICABILITY_CHAIN.md.'
                    and review.get('raw_blocking_issues') is None, 'Priority attribution/application drift')
            continue
        actual_identity = ('independent reproduction and adversarial verification subagent'
                           if family == 'reproduction' else review['reviewer'])
        require(result.get('reviewer') == actual_identity, 'Actual result reviewer identity mismatch')
        raw = result.get('blocking_issues')
        require(type(raw) is int and type(review.get('raw_blocking_issues')) is int
                and review['raw_blocking_issues'] == raw, 'Raw report blockers erased or invented')
        if family == 'candidate_adversary':
            proposed = result.get('proposed_disposition_scope', {})
            require(raw == 2 and type(result.get('required_repairs')) is int and result['required_repairs'] == 1
                    and type(result.get('required_changes')) is int and result['required_changes'] == 2
                    and proposed.get('status') == 'already_solved'
                    and proposed.get('basis') == 'PRIOR_THEOREM_COVERAGE'
                    and proposed.get('status_action_taken') is False
                    and proposed.get('immediate_skip_after_already_solved') is True
                    and result.get('operations_approval') is False
                    and result.get('helper_reviewed') is False
                    and result.get('draft_helper_exists_at_sealing') is True
                    and result.get('current_publication_scope', {}).get('accepted') is False
                    and result['current_publication_scope'].get('issues') == ['V1', 'P1'],
                    'Candidate publication finding or conceptual-disposition scope drift')
            for name in ['unresolved_mathematical_gaps', 'unresolved_universal_mathematical_gaps', 'required_proof_repairs']:
                zero(result.get(name), 'Unresolved candidate ' + name)
            for name in ['unresolved_issues', 'unresolved_mathematical_application_gaps']:
                zero(proposed.get(name), 'Unresolved conceptual disposition ' + name)
            synthesis_review = result.get('disposition_synthesis_scope_review', {})
            require(synthesis_review.get('entire_read') is True and synthesis_review.get('operations_approval') is False
                    and synthesis_review.get('sha256') == evidence['DISPOSITION_SYNTHESIS.md']['sha256']
                    and synthesis_review.get('bytes') == evidence['DISPOSITION_SYNTHESIS.md']['bytes'],
                    'Candidate conceptual synthesis binding differs')
            require(type(gate.get('retained_candidate_publication_blockers')) is int
                    and gate['retained_candidate_publication_blockers'] == raw,
                    'Candidate publication blockers not faithfully retained')
        elif family == 'disposition_adversary':
            for name in ['blocking_issues', 'unresolved_disposition_issues', 'required_corrections', 'unresolved_mathematical_gaps']:
                zero(result.get(name), 'Unresolved final disposition ' + name)
            require(result.get('reviewed_helper_sha256') == gate['helper_sha256']
                    and result.get('reviewed_synthesis_sha256') == evidence['DISPOSITION_SYNTHESIS.md']['sha256'],
                    'Final disposition does not bind current helper/synthesis')
        elif family == 'reproduction':
            require(raw == 1 and type(result.get('required_repairs')) is int and result['required_repairs'] == 1
                    and type(gate.get('retained_v1_verification_blockers')) is int
                    and gate['retained_v1_verification_blockers'] == 1
                    and type(gate.get('retained_v1_required_publication_repairs')) is int
                    and gate['retained_v1_required_publication_repairs'] == 1,
                    'Frozen V1 robustness finding erased or misclassified')
            zero(result.get('unresolved_mathematical_gaps'), 'Reproduction mathematical gap')
            require(len(result.get('issue_details', [])) == 1 and result['issue_details'][0]['id'] == 'V1'
                    and result['exact_counts']['author_mutation_rejections_normal'] == 6
                    and result['exact_counts']['author_mutation_rejections_optimized'] == 0
                    and result['exact_counts']['optimized_author_invalid_variants_emitting_original_passed_json'] == 2,
                    'Observed V1 negative-control boundary drift')
        else:
            zero(raw, 'Mathematical family blocker')
            zero(result.get('required_repairs'), 'Required mathematical repair')
            zero(result.get('unresolved_mathematical_gaps'), 'Mathematical gap')
    link = gate['published_disposition_url']
    parsed = urllib.parse.urlsplit(link)
    expected_suffix = '/' + str((AUDIT / 'DISPOSITION_SYNTHESIS.md').relative_to(PROGRAM.parent))
    match = re.fullmatch('/AlecKriebel/Math/blob/([0-9a-f]{40})' + re.escape(expected_suffix), parsed.path)
    require(parsed.scheme == 'https' and parsed.netloc == 'github.com' and not parsed.query
            and not parsed.fragment and match is not None, 'Disposition URL is not the exact immutable synthesis path')
    require(gate.get('published_disposition_sha256') == evidence['DISPOSITION_SYNTHESIS.md']['sha256'],
            'Published synthesis digest not accepted')
    return gate, match.group(1), str((AUDIT / 'DISPOSITION_SYNTHESIS.md').relative_to(PROGRAM.parent))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    for name in ['STATUS_REPAIR_PREFLIGHT.json', 'STATUS_REPAIR_OPERATION.json', 'STATUS_REPAIR_RECEIPT.json']:
        output_path(name)
    if args.apply:
        require(not (AUDIT / 'STATUS_REPAIR_OPERATION.json').exists(), 'Prior operation exists: do not repeat mutation')
    gate, published_commit, published_path = validate_gate()
    published = api('contents/' + published_path + '?ref=' + published_commit)
    require(published['type'] == 'file' and published['path'] == published_path and published['encoding'] == 'base64',
            'Immutable published synthesis unavailable')
    published_bytes = base64.b64decode(published['content'])
    require(published_bytes == (AUDIT / 'DISPOSITION_SYNTHESIS.md').read_bytes()
            and hashlib.sha256(published_bytes).hexdigest() == gate['published_disposition_sha256'],
            'Immutable published synthesis bytes differ')
    link = gate['published_disposition_url']
    branch = json.loads((AUDIT / 'pr_metadata.json').read_text())['headRefName']
    eligible(branch)
    original = api('git/commits/' + ORIGINAL)
    tree_sha = original['tree']['sha']
    for part in QUEUE.split('/'):
        matches = [e for e in api('git/trees/' + tree_sha)['tree'] if e['path'] == part]
        require(len(matches) == 1, 'QUEUE Git tree path not unique')
        item = matches[0]
        tree_sha = item['sha']
    require(item['type'] == 'blob' and item['mode'] == '100644', 'QUEUE not regular Git blob')
    before = base64.b64decode(api('git/blobs/' + tree_sha)['content'])
    source = json.loads((AUDIT / 'SOURCE_RECEIPT.json').read_text())
    require(hashlib.sha256(before).hexdigest() == source['queue_sha256'], 'Frozen original QUEUE mismatch')
    lines = before.decode().splitlines(keepends=True)
    headers = [x for x in lines if x.startswith('|') and 'ID / code' in x and 'Status' in x]
    require(len(headers) == 1, 'QUEUE header not unique')
    columns = [x.strip() for x in headers[0].split('|')[1:-1]]
    indices = [i for i, x in enumerate(lines) if x.startswith('|') and x.split('|')[2].strip().startswith('30005528 /')]
    require(len(indices) == 1, 'Selected row not unique')
    index = indices[0]
    old_row = lines[index].rstrip('\r\n')
    cells = old_row.split('|')[1:-1]
    require(len(cells) == len(columns), 'QUEUE schema mismatch')
    require(cells[columns.index('Status')].strip() == 'claimed_solved', 'Excluded status: stop without processing')
    old_cells = list(cells)
    cells[columns.index('Status')] = ' already_solved '
    finding = ('2026-10-12: Priority correction: the literal compact ordered-pair Question1 (OWR22/2023, printed1254) follows from Bousch2000 irrational minimal Cantor supports for circle doubling and Jenkinson2006 distance-to-support/unique-maximizer results. Graph tiles and continuous positive cost1+distance(x,K) attain minimum1 on K while every periodic orbit has strictly greater mean; the complete older-theorem application covers all legal words and the original limsup normalization. Submitted annulus mathematics independently verified; historical verifier optimization defect V1 retained. No earlier explicit numbered answer or first solver certified; exact stronger-annulus novelty and structured packing Conjecture4 excluded. [Independent disposition audit](' + link + '). Corrected to already_solved and immediately skipped; no paper, DOI or merge.')
    require('|' not in finding and '\n' not in finding, 'Invalid finding cell')
    cells[columns.index('Findings')] = ' ' + finding + ' '
    require([i for i, (a, b) in enumerate(zip(old_cells, cells)) if a != b]
            == sorted([columns.index('Status'), columns.index('Findings')]), 'Unexpected cell alteration')
    ending = '\r\n' if lines[index].endswith('\r\n') else '\n' if lines[index].endswith('\n') else ''
    lines[index] = '|' + '|'.join(cells) + '|' + ending
    after = ''.join(lines).encode()
    require(len(before.decode().splitlines()) == len(after.decode().splitlines())
            and [i for i, (a, b) in enumerate(zip(before.decode().splitlines(), after.decode().splitlines())) if a != b] == indices,
            'Non-target QUEUE alteration')
    summary = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pr': 462,
               'problem_id': '30005528', 'old_status': 'claimed_solved', 'new_status': 'already_solved',
               'old_head': ORIGINAL, 'branch': branch, 'files_changed': [QUEUE],
               'old_queue_sha256': hashlib.sha256(before).hexdigest(), 'new_queue_sha256': hashlib.sha256(after).hexdigest(),
               'selected_old_row': old_row, 'selected_new_row': lines[index].rstrip('\r\n'),
               'state': 'read_only_preflight', 'shared_checkout_index': 'untouched main',
               'subsequent_scope': 'immediate skip: no paper/Zenodo/tracker/merge/close/comment/further audit'}
    dump('STATUS_REPAIR_PREFLIGHT.json', summary)
    if not args.apply:
        print(json.dumps(summary, indent=2))
        return
    require(not (AUDIT / 'STATUS_REPAIR_OPERATION.json').exists(), 'Prior operation exists: do not repeat mutation')
    blob = api('git/blobs', {'content': base64.b64encode(after).decode(), 'encoding': 'base64'})['sha']
    new_tree = api('git/trees', {'base_tree': original['tree']['sha'],
                    'tree': [{'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': blob}]})['sha']
    eligible(branch)
    commit = api('git/commits', {'message': 'Correct compact domino priority after independent primary theorem audit',
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
    require(base64.b64decode(api('git/blobs/' + blob)['content']) == after, 'Status blob exact-byte readback differs')
    summary.update(state='status_repair_verified_immediately_excluded',
                   verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   readback='Exact selected branch ref and immutable QUEUE blob bytes matched',
                   basis='Original abstract Question1 is a routine graph/positive-cost implication of published2000/2006 results; no earlier explicit numbered answer or first solver certified',
                   concurrency_scope='Exact head/ref checked before nonforced update; Git-data PATCH is not atomic expected-old-SHA CAS')
    dump('STATUS_REPAIR_RECEIPT.json', summary)
    print(json.dumps({'pr': 462, 'new_status': 'already_solved', 'repair_commit': commit,
                      'state': summary['state'], 'subsequent_scope': summary['subsequent_scope']}, indent=2))

if __name__ == '__main__':
    main()
