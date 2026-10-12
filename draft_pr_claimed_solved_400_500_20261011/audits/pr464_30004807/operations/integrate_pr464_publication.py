#!/usr/bin/env python3
"""Install the accepted PR464 packet on its existing branch over captured main.

Default is read-only preflight. --apply writes Git objects and makes one
nonforced branch update. --reconcile only reads a previously saved operation.
The shared checkout and index are never touched.
"""
import argparse
import base64
import json
import subprocess
from urllib.parse import quote
import common as c


def preflight_operation_outputs():
    c.preflight_outputs(('BRANCH_INTEGRATION_PREFLIGHT.json', 'BRANCH_INTEGRATION_OPERATION.json',
                         'BRANCH_INTEGRATION_RECEIPT.json', 'PR_BODY_CURRENT.md',
                         'ZENODO_PUBLIC_FILE_READBACK.json'))


def current_note(metadata, pub):
    return f'''# Published research note: regular ZAS and weak Bianchi defect

Problem 30004807 / OWR-8415343-010. Current authoritative version 1.0.

**{metadata['title']}**, Alec Kriebel, Independent researcher.
ORCID: https://orcid.org/0009-0001-9320-500X.
Published preprint: [{pub['doi']}]({pub['doi_url']}); [Zenodo record]({pub['record_url']}).

The static metric g = -(1-a/rho)^(-2) dt^2 + (1-a/rho)^4 delta,
on rho > a > 0, has harmonically regular zero-area singularities of mass -2a
on its static spacelike slices. For every smooth compactly supported vector
field reaching the retained inner boundary, the complete weak Bianchi scalar
is absolutely integrable. A normalized radial vector gives defect -8 pi.
This is a counterexample to the report's geometric implication under the
cited static-slice and BKTZ boundary-vector-test convention.

The metric and tensor formulas belong to the known Dadhich–Kar–Mukherjee–Visser
family (Phys. Rev. D 65, 064004; https://doi.org/10.1103/PhysRevD.65.064004),
with (m, bar r, kappa, lambda) = (-2a, rho, A, B) and A=B=1/2 here.
Their positive-mass wormhole parameter analysis is not asserted to study this
negative-mass ZAS application. The existing BKTZ boundary-flux method is
credited; direct convergence and cancellation are proved, without invoking
a sufficient theorem whose stronger hypotheses the example does not meet.
No new metric, tensor formula, general boundary theorem, historical first
priority, or certificate of continued openness is claimed.

The example violates the null energy condition. Added energy assumptions,
prescribed matter models, arbitrary tilted-slice regularity, collapsed-point
test conventions, and the wider physical evolution program are outside the claim.

The [paper](preprint_20261012/manuscript.pdf),
[source](preprint_20261012/manuscript.tex), and
[verification archive](preprint_20261012/regular_zas_bianchi_verification_v1.zip)
are the accepted current materials. See [verification instructions](preprint_20261012/verification/README.md)
for the guarded portable entry point.
Finite checks provide consistency/falsification evidence; the analytic proof
establishes the quantified claim. Priority coverage is extensive but bounded.

All thirteen original source files are preserved byte-identically under
preprint_20261012/verification/frozen_history. Original release/ and audit/
files retain their historical bytes; the current landing note supersedes the
original PUBLICATION_NOTES.md, whose original is also in frozen_history.
The old standalone author-manifest hash has no supplied bytes or path and
remains unattested. It is not confused with the independently verified
thirteen-file snapshot or its eleven available internal file references.
PUBLICATION_MANIFEST.json binds the installed accepted materials.

AI tools were used extensively in solving, drafting, independently auditing,
checking computations, and preparing the package. This is an unrefereed
preprint with no independent human peer review. Successive fresh AI-assisted
complete-package audits found no remaining blocking or required correction
within the stated scope; these reviews are not formal certification.

QUEUE remains claimed_solved with the original 1/5 research attempts.
Canonical metadata and confirmed publication/tracker receipts accompany the
accepted packet. No GitHub release or journal submission is created here.
'''


def prepare():
    context = c.validate_gate()
    preflight_operation_outputs()
    pub = c.confirm_live_publication(context)
    c.confirm_live_tracker(context, pub)
    pr, original_queue, reader = c.live_eligibility()
    _, _, source_cells, columns = c.queue_row(original_queue)
    _, sources = c.validate_source_local()
    files = dict(sources)
    files.update(context['installs'])
    names = ['ZENODO_PUBLISH_RECEIPT.json', 'ZENODO_PUBLIC_FILE_READBACK.json',
             'TRACKER_APPEND_RECEIPT.json', 'FINAL_ACCEPTANCE_GATE.json',
             'MATHEMATICAL_ACCEPTANCE_GATE.json', 'SOURCE_RECEIPT.json',
             'BRANCH_INSTALL_PLAN.json', context['manifest_name']]
    names += [x['path'] for x in context['gate']['complete_package_reviews']]
    names.append(context['gate']['operations_review']['path'])
    c.require(len(set(names)) == len(names), 'Duplicate publication receipt selection')
    for name in names:
        c.relative(name)
        destination = c.PREPRINT + 'publication_receipts/' + name
        c.require(destination not in files, 'Receipt destination collides with package file')
        files[destination] = c.safe_file(c.AUDIT, name).read_bytes()
    files[c.PREFIX + 'PUBLICATION_NOTES.md'] = current_note(context['metadata'], pub).encode()
    manifest = {'problem_id': c.PROBLEM, 'version': '1.0', 'date_utc': '2026-10-12',
                'doi': pub['doi'], 'doi_url': pub['doi_url'],
                'historical_files_preserved': 13,
                'historical_bundle': 'preprint_20261012/verification/frozen_history/',
                'unattested_standalone_historical_author_manifest_sha_explicitly_disclosed': True,
                'payload_files': [{'path': p.removeprefix(c.PREFIX), 'bytes': len(b), 'sha256': c.sha(b)}
                                  for p, b in sorted(files.items())]}
    files[c.PREFIX + 'PUBLICATION_MANIFEST.json'] = c.json_bytes(manifest)
    main_sha = c.github('git/ref/heads/main')['object']['sha']
    main_commit = reader.commit(main_sha)
    main_queue = reader.read(c.QUEUE, main_sha)
    lines, i, cells, main_columns = c.queue_row(main_queue)
    c.require(columns == main_columns, 'QUEUE schema changed')
    c.require(cells[columns.index('Status')].strip() in {'queued', 'claimed_solved'},
              'Main selected disposition changed; do not overwrite')
    c.require(cells[columns.index('DOI')].strip() in {'', pub['doi_url']}, 'Main records a different DOI')
    # Check every proposed destination, including generated publication
    # receipts and the manifest. The known frozen landing note is the only
    # existing different payload intentionally superseded by this workflow.
    for path, data in files.items():
        if reader.entry(path, main_sha) is not None:
            allowed = {data}
            if path == c.PREFIX + 'PUBLICATION_NOTES.md':
                allowed.add(sources[path])
            c.require(reader.read(path, main_sha) in allowed, 'Current main installation destination conflicts: ' + path)
    cells[columns.index('Status')] = ' claimed_solved '
    cells[columns.index('Turns')] = source_cells[columns.index('Turns')]
    c.require(cells[columns.index('Turns')].strip() == '1/5', 'Original attempt count changed')
    cells[columns.index('DOI')] = ' ' + pub['doi_url'] + ' '
    cells[columns.index('Findings')] = (
        ' 2026-10-12: Regular-ZAS counterexample under static-slice/BKTZ retained-boundary vector-test scope; '
        'absolutely convergent defect -8 pi. Known Dadhich–Kar–Mukherjee–Visser metric/tensor and BKTZ flux credited. '
        'NEC violated; arbitrary tilted slices, prescribed matter models and collapsed-point tests excluded. '
        'Successive fresh AI-assisted package audits PASS; unrefereed, no independent human peer review or first-priority claim. '
        '[' + context['metadata']['title'] + '](' + pub['doi_url'] + '). '
        '[Paper, verification, receipts](attempts/30004807/PUBLICATION_NOTES.md). ')
    ending = '\r\n' if lines[i].endswith('\r\n') else '\n' if lines[i].endswith('\n') else ''
    lines[i] = '|' + '|'.join(cells) + '|' + ending
    updated_queue = ''.join(lines).encode()
    before = main_queue.decode().splitlines(keepends=True)
    after = updated_queue.decode().splitlines(keepends=True)
    c.require(len(before) == len(after) and [n for n, (a, b) in enumerate(zip(before, after)) if a != b] == [i],
              'QUEUE edit is not exactly the selected row')
    files[c.QUEUE] = updated_queue
    expected_changed = set()
    for path, data in files.items():
        entry = reader.entry(path, main_sha)
        if entry is None or entry.get('sha') != c.git_sha(data) or entry.get('mode') != '100644':
            expected_changed.add(path)
    c.require(0 < len(expected_changed) < 300, 'Compare file limit would make exact change validation impossible')
    summary = {'prepared_at_utc': c.now(), 'state': 'read_only_preflight', 'pr': c.PR,
               'original_pr_head': c.ORIGINAL, 'parent_main_sha': main_sha, 'branch': pr['head']['ref'],
               'doi': pub['doi'], 'doi_url': pub['doi_url'], 'file_count': len(files),
               'files': {p: {'sha256': c.sha(b), 'bytes': len(b), 'git_blob_sha': c.git_sha(b)}
                         for p, b in files.items()}, 'expected_changed_paths': sorted(expected_changed),
               'queue_changed_rows': 1, 'shared_checkout_and_index': 'untouched',
               'concurrency_scope': 'Nonforced update after fresh head/base/ref checks; no atomic expected-old-SHA GitHub ref API.'}
    c.dump('BRANCH_INTEGRATION_PREFLIGHT.json', summary)
    return context, files, summary, reader, main_commit


def verify_commit(summary, reader=None):
    reader = reader or c.GitReader()
    commit = summary['commit_sha']
    commit_obj = reader.commit(commit)
    c.require([x['sha'] for x in commit_obj.get('parents', [])]
              == [c.ORIGINAL, summary['parent_main_sha']], 'Integration commit parents differ')
    comparison = c.github('compare/' + summary['parent_main_sha'] + '...' + commit)
    observed = comparison.get('files')
    c.require(type(observed) is list and len(observed) < 300
              and len({x['filename'] for x in observed}) == len(observed)
              and {x['filename'] for x in observed} == set(summary['expected_changed_paths'])
              and all(x.get('status') in {'added', 'modified'} and 'previous_filename' not in x for x in observed),
              'Commit changed-file set differs or compare may be truncated')
    c.require(comparison.get('base_commit', {}).get('sha') == summary['parent_main_sha']
              and comparison.get('merge_base_commit', {}).get('sha') == summary['parent_main_sha'],
              'Unexpected Git compare base/merge base')
    for path, spec in summary['files'].items():
        data = reader.read(path, commit)
        c.require(len(data) == spec['bytes'] and c.sha(data) == spec['sha256']
                  and c.git_sha(data) == spec['git_blob_sha'], 'Immutable whole-file readback differs: ' + path)
    _, _, cells, columns = c.queue_row(reader.read(c.QUEUE, commit))
    c.require(cells[columns.index('Status')].strip() == 'claimed_solved'
              and cells[columns.index('Turns')].strip() == '1/5'
              and cells[columns.index('DOI')].strip() == summary['doi_url'], 'Installed selected row differs')


def reconcile():
    context = c.validate_gate()
    preflight_operation_outputs()
    pub = c.confirm_live_publication(context)
    c.confirm_live_tracker(context, pub)
    summary = c.read_json(c.AUDIT, 'BRANCH_INTEGRATION_OPERATION.json')
    c.require(summary.get('pr') == c.PR and summary.get('original_pr_head') == c.ORIGINAL
              and summary.get('branch') == c.BRANCH and summary.get('doi') == pub['doi']
              and summary.get('doi_url') == pub['doi_url'] and summary.get('commit_sha'), 'Invalid saved integration operation')
    c.live_eligibility(expected_head=summary['commit_sha'])
    verify_commit(summary)
    summary.update(state='branch_updated_verified', verified_at_utc=c.now(), reconciled_read_only=True)
    c.dump('BRANCH_INTEGRATION_RECEIPT.json', summary)
    c.dump('BRANCH_INTEGRATION_OPERATION.json', summary)
    return {'state': summary['state'], 'commit_sha': summary['commit_sha'], 'file_count': len(summary['files'])}


def run(apply=False):
    c.validate_gate()
    preflight_operation_outputs()
    previous = c.AUDIT / 'BRANCH_INTEGRATION_OPERATION.json'
    if previous.exists():
        prior = c.read_json(c.AUDIT, previous.name)
        c.require(not apply or prior.get('state') == 'read_only_preflight',
                  'Prior integration write exists; use --reconcile read-only, never blindly repeat --apply')
    context, files, summary, reader, main_commit = prepare()
    if not apply:
        return {'state': 'read_only_preflight', 'file_count': len(files), 'main': summary['parent_main_sha']}
    summary['state'] = 'git_object_creation_attempted_once'
    c.dump('BRANCH_INTEGRATION_OPERATION.json', summary)
    entries = []
    for path, data in files.items():
        result = c.github('git/blobs', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
        c.require(result.get('sha') == c.git_sha(data), 'Created Git blob differs from local bytes')
        entries.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': result['sha']})
    c.live_eligibility()
    tree = c.github('git/trees', {'base_tree': main_commit['tree']['sha'], 'tree': entries})['sha']
    commit = c.github('git/commits', {'message': 'Publish reviewed regular-ZAS weak Bianchi counterexample note',
                                   'tree': tree, 'parents': [c.ORIGINAL, summary['parent_main_sha']]})['sha']
    summary.update(commit_sha=commit, tree_sha=tree, state='commit_created_before_ref_update')
    c.dump('BRANCH_INTEGRATION_OPERATION.json', summary)
    verify_commit(summary)
    c.validate_gate()
    current_pub = c.confirm_live_publication(context)
    c.confirm_live_tracker(context, current_pub)
    c.live_eligibility()
    c.require(c.github('git/ref/heads/main')['object']['sha'] == summary['parent_main_sha'],
              'Main advanced during preparation; saved commit must be reconciled before a new integration')
    summary['state'] = 'ref_update_attempted_once'
    c.dump('BRANCH_INTEGRATION_OPERATION.json', summary)
    try:
        c.github('git/refs/heads/' + quote(c.BRANCH, safe='/'), {'sha': commit, 'force': False}, method='PATCH')
    except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError):
        c.require(c.github('git/ref/heads/' + quote(c.BRANCH, safe='/'))['object']['sha'] == commit,
                  'Branch write outcome unconfirmed or rejected; use saved operation and read-only reconciliation')
    c.live_eligibility(expected_head=commit)
    verify_commit(summary)
    summary.update(state='branch_updated_verified', verified_at_utc=c.now())
    c.dump('BRANCH_INTEGRATION_RECEIPT.json', summary)
    c.dump('BRANCH_INTEGRATION_OPERATION.json', summary)
    body = (
        'The accepted research note gives a regular negative-mass ZAS counterexample in the explicit '
        'static-slice and retained-boundary vector-test convention: the full weak Bianchi scalar is '
        'absolutely integrable for every permitted test, and a normalized radial field gives -8 pi. '
        'It uses the known Dadhich–Kar–Mukherjee–Visser metric/tensor and credits the BKTZ boundary-flux method.\n\n'
        'Published preprint: [' + context['metadata']['title'] + '](' + summary['doi_url'] + '). '
        'The PR installs the exact accepted source, PDF, canonical metadata, portable verification package '
        'and confirmed publication/tracker receipts. All thirteen original source files remain frozen historical inputs.\n\n'
        'The example violates the null energy condition. Added energy conditions, prescribed matter models, '
        'arbitrary tilted slices and collapsed-point tests are outside the claim. No new metric, tensor formula, '
        'general boundary theorem or first-priority claim is made. The note is unrefereed, AI tools were used '
        'extensively, and there has been no independent human peer review.\n\n'
        'Validation includes independent mathematical families, bounded priority investigation, guarded '
        'normal/optimized reproductions and successive fresh complete-package adversarial reviews. '
        'Only this attempt folder and the selected QUEUE row differ from captured main.\n')
    c.write_output('PR_BODY_CURRENT.md', body.encode())
    return {'state': summary['state'], 'commit_sha': commit, 'file_count': len(files)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--reconcile', action='store_true')
    args = parser.parse_args()
    print(json.dumps(reconcile() if args.reconcile else run(args.apply), indent=2))


if __name__ == '__main__':
    main()
