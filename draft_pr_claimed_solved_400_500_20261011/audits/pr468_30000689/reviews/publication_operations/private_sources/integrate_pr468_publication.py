#!/usr/bin/env python3
"""Install only the accepted PR468 packet over current remote main.

Uses the existing PR branch; never changes the shared checkout or Git index.
Requires completed publication and tracker receipts, and a final review gate.
"""
import argparse
import base64
import concurrent.futures
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

PROGRAM = Path(__file__).resolve().parent
REPOSITORY = PROGRAM.parent
AUDIT = PROGRAM / 'audits/pr468_30000689'
PREFIX = 'unsolved_math_prioritization/attempts/30000689/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
REPO = 'AlecKriebel/Math'
ORIGINAL = '8527ccdba064bca52035fc6c8d96caa750ac9c00'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def api(endpoint, payload=None, method=None, raw=False):
    cmd = ['gh', 'api', 'repos/' + REPO + '/' + endpoint]
    if raw:
        cmd += ['-H', 'Accept: application/vnd.github.raw+json']
    if payload is not None:
        cmd += ['--method', method or 'POST', '--input', '-']
    p = subprocess.run(cmd, input=None if payload is None else json.dumps(payload).encode(),
                       capture_output=True)
    require(p.returncode == 0, p.stderr.decode().strip())
    return p.stdout if raw else json.loads(p.stdout)


def read(path, head):
    return api('contents/' + path + '?ref=' + head, raw=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def queue_row(data):
    lines = data.decode().splitlines(keepends=True)
    header = next(x for x in lines if x.startswith('|') and 'ID / code' in x and 'Status' in x)
    columns = [x.strip() for x in header.split('|')[1:-1]]
    found = []
    for i, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = line.rstrip('\r\n').split('|')[1:-1]
        if len(cells) == len(columns) and cells[1].strip().startswith('30000689 /'):
            found.append((i, cells))
    require(len(found) == 1, 'Selected QUEUE row is not unique')
    i, cells = found[0]
    return lines, i, cells, columns


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    gate = json.loads((AUDIT / 'FINAL_ACCEPTANCE_GATE.json').read_text())
    require(gate['verdict'] == 'ACCEPTED_FOR_PREPRINT_PUBLICATION' and gate['pr'] == 468,
            'Final complete-package acceptance is absent')
    require(len(gate['complete_package_reviews']) >= 2, 'Successive fresh reviews absent')
    for report in gate['complete_package_reviews']:
        require(report['verdict'] == 'PASS' and report['blocking_issue_count'] == 0,
                'A complete-package review has a blocking finding')
        p = (AUDIT / report['path']).resolve()
        require(p.is_relative_to(AUDIT) and digest(p.read_bytes()) == report['sha256'],
                'Accepted review report changed')
    input_name = gate['review_input_manifest']
    require(input_name.startswith('PACKAGE_REVIEW_INPUT_') and Path(input_name).name == input_name,
            'Invalid accepted input-manifest path')
    freeze = json.loads((AUDIT / input_name).read_text())
    for name, item in freeze['files'].items():
        require(digest((AUDIT / 'package' / name).read_bytes()) == item['sha256'],
                'Accepted package changed: ' + name)
    published = json.loads((AUDIT / 'ZENODO_PUBLISH_RECEIPT.json').read_text())
    require(published['state'] == 'published' and published['environment'] == 'production',
            'Confirmed production publication absent')
    metadata = json.loads((AUDIT / 'package/metadata.json').read_text())
    require(published['title'] == metadata['title'], 'Published title drift')
    expected_uploads = {
        'missing_faces_and_sphere_skeleta.pdf': freeze['files']['manuscript.pdf']['sha256'],
        'missing_faces_verification_v1.zip': freeze['files']['missing_faces_verification_v1.zip']['sha256']}
    require({x['name']: x['sha256'] for x in published['files']} == expected_uploads,
            'Published files do not match reviewed packet')
    doi = published['doi_url']
    require(isinstance(doi, str) and doi.startswith('https://doi.org/10.'), 'Confirmed DOI absent')
    tracker = json.loads((AUDIT / 'TRACKER_APPEND_RECEIPT.json').read_text())
    require(tracker['verified'] is True and tracker['values'][0][2] == doi,
            'Verified tracker append absent')

    pr = api('pulls/468')
    require(pr['state'] == 'open' and pr['draft'] is True and pr['head']['sha'] == ORIGINAL
            and pr['head']['repo']['full_name'] == REPO,
            'Original open draft head changed; stop and reconcile')
    branch = pr['head']['ref']
    original_queue = read(QUEUE, ORIGINAL)
    _, _, source_cells, columns = queue_row(original_queue)
    require(source_cells[columns.index('Status')].strip() == 'claimed_solved',
            'Selected PR is outside claimed_solved scope')
    changed = api('pulls/468/files?per_page=100')
    require(all(x['filename'] == QUEUE or x['filename'].startswith(PREFIX) for x in changed),
            'Original PR includes unrelated changes')
    receipt = json.loads((AUDIT / 'SOURCE_RECEIPT.json').read_text())
    files = {}
    for item in receipt['files']:
        data = read(item['path'], ORIGINAL)
        require(digest(data) == item['sha256'], 'Original source changed: ' + item['path'])
        files[item['path']] = data
    plan = json.loads((AUDIT / 'BRANCH_INSTALL_PLAN.json').read_text())
    for item in plan['entries']:
        p = (REPOSITORY / item['local_program_path']).resolve()
        destination = item['repository_destination']
        require(p.is_relative_to(AUDIT / 'package') and p.is_file() and not p.is_symlink(),
                'Unsafe package source')
        require(destination.startswith(PREFIX + 'preprint_20261012/'), 'Unsafe package destination')
        data = p.read_bytes()
        require(digest(data) == item['sha256'], 'Install-plan byte drift')
        files[destination] = data
    for name in ('ZENODO_PUBLISH_RECEIPT.json', 'TRACKER_APPEND_RECEIPT.json',
                 'FINAL_ACCEPTANCE_GATE.json', input_name):
        files[PREFIX + 'preprint_20261012/publication_receipts/' + name] = (AUDIT / name).read_bytes()
    for report in gate['complete_package_reviews']:
        files[PREFIX + 'preprint_20261012/publication_receipts/' + report['path']] = (AUDIT / report['path']).read_bytes()

    note = f'''# Published research note: missing-face embedding obstruction

Problem 30000689 / OWR-1455-008. Current authoritative version 1.0.

**{metadata['title']}**, Alec Kriebel (ORCID 0009-0001-9320-500X).
Published preprint: [{published['doi']}]({doi}); [Zenodo record]({published['record_url']}).

For every finite triangulation S of the topological sphere S^(2d), adjoining
a missing d-face on its actual vertices to S^(d) prevents every topological
embedding into S^(2d). The d=0 case is vacuous. The note provides a credited
synthesis for d>=3 and an explicit dimension-four extension in the actual
PL class, without assuming a standard PL 4-sphere or complementary 4-ball.

The [current paper](preprint_20261012/manuscript.pdf),
[source](preprint_20261012/manuscript.tex), and
[verification archive](preprint_20261012/missing_faces_verification_v1.zip)
supersede the earlier candidate presentation. Current computations are in
[the supplement](preprint_20261012/verification/README.md); run
`python3 reproduce.py` from its verification folder. The three programs
reproduce recorded finite examples normally and with optimized Python.
These controls do not establish the universal theorem or certify priority.

Separate algebra/topology/reproduction and bounded priority audits, followed
by successive fresh complete-package adversaries, found no remaining
blocking issue in the accepted package. The original frozen author/audit
files remain unchanged under release/ and audit/ as historical inputs.
Their removable assertions and pending-review wording are not current
verification instructions. All 15 original files, including this landing
note's earlier form and manifest, are also preserved byte-identically in
preprint_20261012/verification/historical/. PUBLICATION_MANIFEST.json now
binds the current landing note and installed accepted materials.

AI tools were used extensively in solving, drafting, independently auditing,
checking finite computations, and preparing the package. This is an
unrefereed preprint with no independent human peer review. The audits are
bounded AI-assisted reviews, not formal certification. Established inputs
and the earlier conjecture are credited; first priority, a new general
method, and the problem's open status in 2026 are not certified.

QUEUE remains claimed_solved with the original 3/5 research attempts.
Canonical metadata is in preprint_20261012/metadata.json. Verified publication
and tracker receipts are in preprint_20261012/publication_receipts/.
'''
    files[PREFIX + 'PUBLICATION_NOTES.md'] = note.encode()
    manifest = {'problem_id': 30000689, 'version': '1.0', 'date_utc': '2026-10-12',
                'doi': published['doi'], 'doi_url': doi,
                'historical_author_and_audit_files_preserved': True,
                'historical_original_publication_manifest': 'preprint_20261012/verification/historical/PUBLICATION_MANIFEST.json',
                'public_payload_files': [{'path': path.removeprefix(PREFIX), 'bytes': len(data),
                                         'sha256': digest(data)} for path, data in sorted(files.items())
                                        if path != PREFIX + 'PUBLICATION_MANIFEST.json']}
    files[PREFIX + 'PUBLICATION_MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()

    main_sha = api('git/ref/heads/main')['object']['sha']
    main_commit = api('git/commits/' + main_sha)
    main_queue = read(QUEUE, main_sha)
    lines, i, cells, main_columns = queue_row(main_queue)
    require(columns == main_columns, 'QUEUE schema changed')
    require(cells[columns.index('Status')].strip() in {'queued', 'claimed_solved'},
            'Main selected disposition changed; do not overwrite')
    cells[columns.index('Status')] = ' claimed_solved '
    cells[columns.index('Turns')] = source_cells[columns.index('Turns')]
    require(cells[columns.index('Turns')].strip() == '3/5', 'Original attempt count changed')
    finding_col = columns.index('Findings')
    cells[finding_col] = (' 2026-10-12: Full TOP-source/TOP-embedding missing-face theorem; '
                         'credited synthesis and actual-PL-class dimension-four extension. '
                         'Successive fresh AI-assisted package audits PASS; unrefereed, no independent human review '
                         'or first-priority claim. [' + metadata['title'] + '](' + doi + '). '
                         '[Paper, verification, publication receipts](attempts/30000689/PUBLICATION_NOTES.md). ')
    doi_col = columns.index('DOI')
    require(cells[doi_col].strip() in {'', doi}, 'Main already records a different publication DOI')
    cells[doi_col] = ' ' + doi + ' '
    ending = '\r\n' if lines[i].endswith('\r\n') else '\n' if lines[i].endswith('\n') else ''
    lines[i] = '|' + '|'.join(cells) + '|' + ending
    files[QUEUE] = ''.join(lines).encode()
    require(len([1 for a, b in zip(main_queue.decode().splitlines(), files[QUEUE].decode().splitlines())
                 if a != b]) == 1, 'QUEUE changed beyond selected row')
    require(len(main_queue.decode().splitlines()) == len(files[QUEUE].decode().splitlines()),
            'QUEUE line count changed')
    summary = {'prepared_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'original_pr_head': ORIGINAL, 'parent_main_sha': main_sha, 'branch': branch,
               'doi': published['doi'], 'files_sha256': {p: digest(b) for p, b in files.items()},
               'queue_changed_rows': 1, 'shared_checkout_and_index': 'untouched'}
    dump(AUDIT / 'BRANCH_INTEGRATION_PREFLIGHT.json', summary)
    if not args.apply:
        print(json.dumps({'state': 'preflight_only', 'file_count': len(files), 'main': main_sha}, indent=2))
        return

    def blob(item):
        path, data = item
        sha = api('git/blobs', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})['sha']
        return {'path': path, 'mode': '100644', 'type': 'blob', 'sha': sha}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        entries = list(pool.map(blob, files.items()))
    require(api('pulls/468')['head']['sha'] == ORIGINAL, 'PR moved while installing blobs')
    tree = api('git/trees', {'base_tree': main_commit['tree']['sha'], 'tree': entries})['sha']
    commit = api('git/commits', {'message': 'Publish reviewed missing-face embedding preprint and verification',
                               'tree': tree, 'parents': [ORIGINAL, main_sha]})['sha']
    diff = api('compare/' + main_sha + '...' + commit)
    require(all(x['filename'] == QUEUE or x['filename'].startswith(PREFIX) for x in diff['files']),
            'Proposed branch commit changes unrelated main paths')
    require(read(QUEUE, commit) == files[QUEUE], 'QUEUE commit readback differs')
    summary.update(commit_sha=commit, state='commit_created_before_ref_update',
                   files_git_blob_sha={x['path']: x['sha'] for x in entries})
    dump(AUDIT / 'BRANCH_INTEGRATION_RECEIPT.json', summary)
    try:
        api('git/refs/heads/' + branch, {'sha': commit, 'force': False}, method='PATCH')
    except RuntimeError:
        require(api('git/ref/heads/' + branch)['object']['sha'] == commit,
                'Branch update uncertain or rejected; inspect saved commit before retrying')
    require(api('git/ref/heads/' + branch)['object']['sha'] == commit, 'Branch readback changed')
    for name in ('manuscript.tex', 'manuscript.pdf', 'metadata.json', 'missing_faces_verification_v1.zip'):
        path = PREFIX + 'preprint_20261012/' + name
        require(digest(read(path, commit)) == digest(files[path]), 'Installed package byte drift: ' + name)
    summary.update(state='branch_updated_verified', verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   url='https://github.com/' + REPO + '/commit/' + commit)
    dump(AUDIT / 'BRANCH_INTEGRATION_RECEIPT.json', summary)
    (AUDIT / 'PR_BODY_CURRENT.md').write_text(
        'Adjoining a missing middle-dimensional simplex to the middle skeleton of any finite triangulation '
        'of a topological even sphere prevents every topological embedding into that sphere. The research '
        'note proves the precise Nevo–Wagner conjecture statement by a credited synthesis and an explicit '
        'dimension-four argument in the actual PL class.\n\n'
        'Published preprint: [' + metadata['title'] + '](' + doi + '). The PR includes the exact accepted '
        'paper, source, canonical metadata, reproducible verification supplement and confirmed publication/tracker receipts. '
        'The original author/audit files remain frozen historical inputs, with the current landing note superseding them.\n\n'
        'Validation: separate mathematical and priority families, successive fresh complete-package adversaries, '
        'normal/optimized finite reproductions and actual fault controls. The preprint is unrefereed; AI tools were used '
        'extensively. No independent human peer review, formal certification, first-priority or new-method claim is made. '
        'Only this problem’s QUEUE row and attempt folder differ from current main.\n')
    print(json.dumps({'state': summary['state'], 'commit_sha': commit, 'file_count': len(files)}, indent=2))


if __name__ == '__main__':
    main()
