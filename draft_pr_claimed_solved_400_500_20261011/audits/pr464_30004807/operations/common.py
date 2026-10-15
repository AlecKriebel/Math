#!/usr/bin/env python3
"""Strict local gates and read-only services for the PR464 publication helpers.

No service write is performed at import. These helpers do not grant atomic
multi-runner protection; they save uncertain writes and refuse blind retries.
"""
import base64
import datetime
import hashlib
import json
import os
import stat
import tempfile
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit

AUDIT = Path(__file__).resolve().parent.parent
REPOSITORY = AUDIT.parents[2]
PACKAGE = AUDIT / 'package'
REPO = 'AlecKriebel/Math'
PR = 464
PROBLEM = '30004807'
ORIGINAL = '97b2ed225574ca61bd03cb8db021a533e04938dc'
BRANCH = 'weak-bianchi-zas-30004807-20261003'
PREFIX = 'unsolved_math_prioritization/attempts/30004807/'
PREPRINT = PREFIX + 'preprint_20261012/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB = 'Math Puzzles'
TAB_ID = 1254632077
GWS = '/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
ZIP_NAME = 'regular_zas_bianchi_verification_v1.zip'
UPLOADS = {'regular_zas_bianchi_defect.pdf': 'manuscript.pdf', ZIP_NAME: ZIP_NAME}
FORBIDDEN = {'private_sources', 'private_cases', 'mutation_fixtures', '.secrets',
             '.zenodo-state', '__pycache__', 'venv', '.venv'}
HELPERS = ('operations/common.py', 'operations/zenodo_pr464.py',
           'operations/register_pr464_tracker.py', 'operations/integrate_pr464_publication.py')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
HEX40 = re.compile(r'^[0-9a-f]{40}$')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def relative(value):
    require(type(value) is str and value and '\\' not in value and '\x00' not in value,
            'Invalid path representation')
    p = PurePosixPath(value)
    require(not p.is_absolute() and str(p) == value and all(x not in {'', '.', '..'} for x in p.parts),
            'Path is not a canonical safe relative path: ' + value)
    require(not FORBIDDEN.intersection(p.parts) and p.suffix != '.pyc',
            'Private or generated path excluded: ' + value)
    return p


def safe_file(root, name):
    p = relative(name)
    root = Path(root)
    require(not root.is_symlink() and root.resolve() == root, 'Unsafe file root')
    direct = root / p
    # Check the unresolved source and every ancestor before resolving. Checking
    # only the resolved leaf misses a direct or intermediate symlink.
    cursor = root
    for part in p.parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), 'Symlink excluded: ' + name)
    resolved = direct.resolve()
    require(resolved.is_relative_to(root) and resolved.is_file(), 'Missing or escaping file: ' + name)
    return resolved


def read_json(root, name):
    value = json.loads(safe_file(root, name).read_text())
    require(type(value) is dict, 'Expected JSON object: ' + name)
    return value


def checked_bytes(root, name, spec):
    require(type(spec) is dict and type(spec.get('sha256')) is str
            and HEX64.fullmatch(spec['sha256']), 'Invalid SHA-256 binding: ' + name)
    require(type(spec.get('bytes')) is int and spec['bytes'] >= 0, 'Invalid byte count: ' + name)
    data = safe_file(root, name).read_bytes()
    require(len(data) == spec['bytes'] and sha(data) == spec['sha256'], 'Frozen bytes changed: ' + name)
    return data


def output_destination(name):
    """Preflight an owned output without following links or opening special files."""
    parts = relative(name).parts
    root = Path(AUDIT)
    require(root.is_absolute() and not root.is_symlink() and root.resolve() == root
            and root.is_dir(), 'Unsafe receipt destination: audit root')
    destination = root.joinpath(*parts)
    cursor = root
    for part in parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), 'Unsafe receipt destination: symlink')
    require(destination.parent.is_dir() and destination.parent.resolve().is_relative_to(root),
            'Unsafe receipt destination: parent')
    if destination.exists():
        info = destination.stat()
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                'Unsafe receipt destination: nonregular or hard-linked output')
    return destination


def preflight_outputs(names):
    for name in names:
        output_destination(name)


def write_output(name, data):
    """Install complete bytes by one same-directory replacement.

    Each file replacement is atomic; this is not a group transaction or a
    lock against hostile concurrent ancestor changes.
    """
    require(type(data) is bytes, 'Output must be complete bytes')
    destination = output_destination(name)
    fd, temporary = tempfile.mkstemp(prefix='.pr464-output-', dir=destination.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
        require(output_destination(name) == destination, 'Unsafe receipt destination: changed output')
        os.replace(temporary, destination)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def dump(name, obj):
    write_output(name, json_bytes(obj))


def zero_count(value, name):
    require(type(value) is int and value == 0, 'Nonzero or invalid ' + name)


def hash_bound_file(root, name, expected):
    require(type(expected) is str and HEX64.fullmatch(expected), 'Missing SHA binding: ' + name)
    data = safe_file(root, name).read_bytes()
    require(sha(data) == expected, 'Bound file changed: ' + name)
    return data


def validate_source_local():
    receipt = read_json(AUDIT, 'SOURCE_RECEIPT.json')
    require(receipt.get('pr') == PR and receipt.get('problem_id') == PROBLEM
            and receipt.get('head_sha') == ORIGINAL and receipt.get('scope_gate') == 'exact claimed_solved',
            'Original eligible source capture is absent')
    records = receipt.get('files')
    require(type(records) is list and len(records) == 13, 'Expected exactly 13 historical source files')
    out = {}
    for item in records:
        require(type(item) is dict and item.get('path', '').startswith(PREFIX), 'Unsafe source path')
        path = item['path']
        relative(path)
        require(path not in out and not path.startswith(PREPRINT), 'Duplicate or unexpected historical path')
        out[path] = checked_bytes(AUDIT / 'source_snapshot', path, item)
    require(receipt.get('other_changed_paths') == [QUEUE], 'Unexpected source changed paths')
    line = receipt.get('selected_queue_row')
    require(type(line) is str and '| claimed_solved | 1/5 |' in line,
            'Historical selected row is not exact claimed_solved with original attempt count')
    return receipt, out


def validate_gate(require_operations=True):
    gate = read_json(AUDIT, 'FINAL_ACCEPTANCE_GATE.json')
    require(gate.get('verdict') == 'ACCEPTED_FOR_PREPRINT_PUBLICATION'
            and gate.get('pr') == PR and gate.get('problem_id') == PROBLEM
            and gate.get('original_pr_head') == ORIGINAL and gate.get('status_gate') == 'claimed_solved',
            'Final PR464 publication acceptance absent')
    zero_count(gate.get('remaining_package_issues'), 'remaining_package_issues')
    require(gate.get('root_read_entire_final_report') is True, 'Root full final report read is absent')
    hash_bound_file(AUDIT, 'SOURCE_RECEIPT.json', gate.get('source_receipt_sha256'))
    validate_source_local()
    math = json.loads(hash_bound_file(AUDIT, 'MATHEMATICAL_ACCEPTANCE_GATE.json',
                                    gate.get('mathematical_acceptance_gate_sha256')))
    require(math.get('pr') == PR and math.get('problem') == PROBLEM
            and math.get('eligible_head') == ORIGINAL
            and math.get('verdict') == 'ACCEPTED_FOR_PREPRINT_PREPARATION_ONLY'
            and math.get('classical_attribution_verified_current') is True
            and math.get('new_metric_or_first_priority_claim') is False,
            'Mathematical and bounded-priority acceptance absent')
    families = math.get('mathematical_families')
    require(type(families) is list and {x.get('family') for x in families}
            == {'source_geometry', 'curvature_flux', 'reproduction'}, 'Independent mathematical families absent')
    for item in families + [math.get('bounded_priority', {})]:
        family = item.get('family')
        require(family in {'source_geometry', 'curvature_flux', 'reproduction', 'priority'},
                'Unknown mathematical/priority family')
        hash_bound_file(AUDIT, 'reviews/' + family + '/REPORT.md', item.get('report_sha256'))
        hash_bound_file(AUDIT, 'reviews/' + family + '/PUBLIC_OUTPUT_WHITELIST.json',
                        item.get('whitelist_sha256'))
    whole = math.get('whole_candidate_report', {})
    zero_count(whole.get('blocking_count'), 'mathematical blocking_count')
    zero_count(whole.get('unresolved_count'), 'mathematical unresolved_count')
    hash_bound_file(AUDIT, whole.get('path'), whole.get('sha256'))
    manifest_name = gate.get('review_input_manifest')
    require(type(manifest_name) is str and re.fullmatch(r'PACKAGE_REVIEW_INPUT_[1-9][0-9]*\.json', manifest_name),
            'Invalid package input-manifest path')
    manifest_bytes = hash_bound_file(AUDIT, manifest_name, gate.get('review_input_manifest_sha256'))
    freeze = json.loads(manifest_bytes)
    require(type(freeze) is dict and freeze.get('pr') == PR
            and freeze.get('problem') == PROBLEM and freeze.get('original_head') == ORIGINAL,
            'Reviewed freeze PR/problem/original-head identity differs from accepted target')
    for name in ('source_receipt_sha256', 'mathematical_acceptance_gate_sha256', 'branch_install_plan_sha256'):
        require(type(freeze.get(name)) is str and HEX64.fullmatch(freeze[name])
                and freeze[name] == gate.get(name), 'Reviewed freeze cross-binding differs: ' + name)
    frozen_files = freeze.get('files')
    require(type(frozen_files) is dict and set(frozen_files) >=
            {'manuscript.tex', 'manuscript.pdf', 'metadata.json', 'deposit.json', 'README.md',
             'SHA256SUMS.json', ZIP_NAME}, 'Incomplete frozen package')
    require(gate.get('final_files') == frozen_files, 'Final-file gate differs from accepted manifest')
    for name, spec in frozen_files.items():
        checked_bytes(PACKAGE, name, spec)
    reviews = gate.get('complete_package_reviews')
    require(type(reviews) is list and len(reviews) >= 2, 'Two successive fresh package reviews absent')
    identities = set()
    rounds = []
    for review in reviews:
        require(type(review) is dict and review.get('verdict') == 'PASS', 'Package review is not PASS')
        zero_count(review.get('blocking_issue_count'), 'blocking_issue_count')
        zero_count(review.get('required_correction_count'), 'required_correction_count')
        identity = review.get('identity') or review.get('reviewer')
        require(type(identity) is str and identity and identity not in identities, 'Package reviewers must be fresh and distinct')
        identities.add(identity)
        require(type(review.get('round')) is int and review['round'] >= 1, 'Invalid package review round')
        rounds.append(review['round'])
        hash_bound_file(AUDIT, review.get('path'), review.get('sha256'))
    require(rounds == sorted(set(rounds)) and rounds[-1] == rounds[-2] + 1,
            'Final reviews are not successive distinct rounds')
    require(all(x.get('input_manifest_sha256') == sha(manifest_bytes) for x in reviews[-2:]),
            'Final two clean reviews do not bind the exact accepted package')
    plan = json.loads(hash_bound_file(AUDIT, 'BRANCH_INSTALL_PLAN.json', gate.get('branch_install_plan_sha256')))
    entries = plan.get('entries')
    require(type(entries) is list and entries, 'Positive branch-install list absent')
    installs = {}
    for item in entries:
        require(type(item) is dict, 'Invalid install item')
        local = item.get('local_program_path')
        destination = item.get('repository_destination')
        relative(local)
        relative(destination)
        require(destination.startswith(PREPRINT) and destination not in installs, 'Unsafe or duplicate install destination')
        local_path = safe_file(REPOSITORY, local)
        require(local_path.is_relative_to(PACKAGE), 'Install source is outside accepted package')
        package_name = local_path.relative_to(PACKAGE).as_posix()
        require(destination == PREPRINT + package_name, 'Install mapping must preserve exact package-relative path')
        installs[destination] = checked_bytes(REPOSITORY, local, item)
    require(all(PREPRINT + name in installs for name in frozen_files), 'Frozen package output omitted from install plan')
    archive_payloads = {}
    with zipfile.ZipFile(safe_file(PACKAGE, ZIP_NAME)) as archive:
        members = archive.infolist()
        require(members and len({x.filename for x in members}) == len(members), 'Empty or duplicate ZIP entries')
        for member in members:
            require(not member.is_dir(), 'ZIP must list only explicit file payloads')
            relative(member.filename)
            require((member.external_attr >> 16) & 0o170000 != 0o120000, 'ZIP symlink excluded')
            require(member.filename not in {'manuscript.pdf', ZIP_NAME, 'deposit.json', 'ARCHIVE_RECEIPT.json'},
                    'ZIP contains an external/circular publication output')
            data = archive.read(member)
            require(safe_file(PACKAGE, member.filename).read_bytes() == data, 'ZIP payload differs from installed source')
            archive_payloads[member.filename] = data
    require(set(installs) == {PREPRINT + name for name in set(archive_payloads) | set(frozen_files)},
            'Positive install list does not match exactly ZIP payloads plus frozen external outputs')
    history_prefix = PREPRINT + 'verification/frozen_history/'
    _, sources = validate_source_local()
    for path, data in sources.items():
        historic = history_prefix + path.removeprefix(PREFIX)
        require(installs.get(historic) == data, 'Historical source not preserved in install plan: ' + path)
    metadata = read_json(PACKAGE, 'metadata.json')
    deposit = read_json(PACKAGE, 'deposit.json')
    require(deposit.get('metadata') == metadata, 'Deposit metadata differs from canonical metadata')
    uploads = deposit.get('files')
    require(type(uploads) is list and len(uploads) == len(UPLOADS), 'Unexpected Zenodo upload list')
    mapped = {}
    for item in uploads:
        require(type(item) is dict and set(item) in ({'path'}, {'path', 'name'}), 'Unexpected deposit file fields')
        relative(item['path'])
        name = item.get('name', Path(item['path']).name)
        require(name not in mapped and UPLOADS.get(name) == item['path'], 'Incorrect public upload mapping')
        checked_bytes(PACKAGE, item['path'], frozen_files[item['path']])
        mapped[name] = item['path']
    require(mapped == UPLOADS, 'Public uploads differ from expected PDF/archive')
    kit = REPOSITORY / 'zenodo_deposit_tool/zenodo.py'
    hash_bound_file(REPOSITORY, 'zenodo_deposit_tool/zenodo.py', gate.get('zenodo_kit_sha256'))
    if require_operations:
        op = gate.get('operations_review', {})
        require(op.get('verdict') == 'PASS', 'Fresh operations acceptance absent')
        zero_count(op.get('blocking_issue_count'), 'operations blocking_issue_count')
        zero_count(op.get('required_correction_count'), 'operations required_correction_count')
        hash_bound_file(AUDIT, op.get('path'), op.get('sha256'))
        require(type(op.get('helpers')) is dict and set(op['helpers']) == set(HELPERS), 'Operations helper hash set is incomplete')
        for name, expected in op['helpers'].items():
            hash_bound_file(AUDIT, name, expected)
    return {'gate': gate, 'freeze': freeze, 'manifest_name': manifest_name,
            'installs': installs, 'metadata': metadata, 'deposit': deposit, 'kit': kit}


def github(endpoint, payload=None, method=None):
    args = ['gh', 'api', 'repos/' + REPO + '/' + endpoint]
    if payload is not None:
        args += ['--method', method or 'POST', '--input', '-']
    result = subprocess.run(args, input=None if payload is None else json.dumps(payload).encode(),
                            capture_output=True, timeout=60)
    require(result.returncode == 0, 'GitHub operation failed; reconcile saved operation before retrying a write')
    return json.loads(result.stdout)


class GitReader:
    """Read immutable Git trees/blobs; never use the binary Contents endpoint."""
    def __init__(self):
        self.trees = {}
        self.blobs = {}
        self.commits = {}

    def commit(self, revision):
        require(type(revision) is str and HEX40.fullmatch(revision), 'Invalid immutable revision')
        if revision not in self.commits:
            result = github('git/commits/' + revision)
            require(result.get('sha') == revision, 'Immutable commit identity changed')
            self.commits[revision] = result
        return self.commits[revision]

    def tree(self, tree_sha):
        if tree_sha not in self.trees:
            result = github('git/trees/' + tree_sha)
            require(result.get('sha') == tree_sha and result.get('truncated') is False
                    and type(result.get('tree')) is list, 'Truncated or invalid Git tree')
            require(len({x['path'] for x in result['tree']}) == len(result['tree']), 'Duplicate Git tree path')
            self.trees[tree_sha] = result['tree']
        return self.trees[tree_sha]

    def entry(self, path, revision):
        parts = relative(path).parts
        tree_sha = self.commit(revision)['tree']['sha']
        for index, part in enumerate(parts):
            selected = [x for x in self.tree(tree_sha) if x['path'] == part]
            if not selected:
                return None
            require(len(selected) == 1, 'Ambiguous Git tree component')
            entry = selected[0]
            if index == len(parts) - 1:
                return entry
            require(entry['type'] == 'tree' and entry['mode'] == '040000', 'Symlink or nontree Git ancestor')
            tree_sha = entry['sha']

    def read(self, path, revision):
        entry = self.entry(path, revision)
        require(entry is not None and entry['type'] == 'blob' and entry['mode'] == '100644',
                'Missing, executable, or symlinked Git blob: ' + path)
        blob_sha = entry['sha']
        if blob_sha not in self.blobs:
            result = github('git/blobs/' + blob_sha)
            require(result.get('sha') == blob_sha and result.get('encoding') == 'base64', 'Invalid Git blob')
            data = base64.b64decode(result['content'], validate=False)
            require(type(result.get('size')) is int and len(data) == result['size']
                    and git_sha(data) == blob_sha, 'Git blob content does not match immutable object')
            self.blobs[blob_sha] = data
        return self.blobs[blob_sha]


def queue_row(data):
    lines = data.decode().splitlines(keepends=True)
    headers = [x for x in lines if x.startswith('|') and 'ID / code' in x and 'Status' in x]
    require(len(headers) == 1, 'QUEUE header is not unique')
    columns = [x.strip() for x in headers[0].split('|')[1:-1]]
    require(len(set(columns)) == len(columns) and {'ID / code', 'Status', 'Turns', 'Findings', 'DOI'} <= set(columns),
            'QUEUE schema is invalid')
    matches = []
    for i, line in enumerate(lines):
        if line.startswith('|'):
            cells = line.rstrip('\r\n').split('|')[1:-1]
            if len(cells) == len(columns) and cells[columns.index('ID / code')].strip().startswith(PROBLEM + ' /'):
                matches.append((i, cells))
    require(len(matches) == 1, 'Selected QUEUE row is not unique')
    i, cells = matches[0]
    return lines, i, cells, columns


def live_eligibility(reader=None, expected_head=ORIGINAL, draft=True):
    reader = reader or GitReader()
    pr = github('pulls/' + str(PR))
    require(pr.get('number') == PR and pr.get('state') == 'open' and pr.get('draft') is draft
            and pr.get('head', {}).get('sha') == expected_head
            and pr.get('head', {}).get('ref') == BRANCH
            and pr.get('head', {}).get('repo', {}).get('full_name') == REPO
            and pr.get('base', {}).get('ref') == 'main'
            and pr.get('base', {}).get('repo', {}).get('full_name') == REPO,
            'PR identity, base, open/draft state, branch, or exact eligible head changed')
    ref = github('git/ref/heads/' + quote(BRANCH, safe='/'))
    require(ref.get('object', {}).get('sha') == expected_head, 'PR branch ref moved')
    queue = reader.read(QUEUE, expected_head)
    _, _, cells, columns = queue_row(queue)
    require(cells[columns.index('Status')].strip() == 'claimed_solved'
            and cells[columns.index('Turns')].strip() == '1/5', 'Selected problem is excluded or original attempts changed')
    if expected_head == ORIGINAL:
        receipt, sources = validate_source_local()
        require(sha(queue) == receipt['queue_sha256'], 'Original source QUEUE changed')
        changed = github('pulls/' + str(PR) + '/files?per_page=100&page=1')
        require(type(pr.get('changed_files')) is int and pr['changed_files'] == 14
                and type(changed) is list and len(changed) == pr['changed_files'], 'Original changed-file list is truncated or changed')
        require({x['filename'] for x in changed} == set(sources) | {QUEUE}
                and len({x['filename'] for x in changed}) == len(changed), 'Original PR changed-file set differs from frozen source')
        require(all(x.get('status') == ('modified' if x['filename'] == QUEUE else 'added')
                    and 'previous_filename' not in x for x in changed), 'Original PR has unexpected change/rename semantics')
        for path, data in sources.items():
            require(reader.read(path, ORIGINAL) == data, 'Original source bytes differ: ' + path)
    return pr, queue, reader


def expected_public_files(context):
    return {name: {'name': name, 'sha256': context['freeze']['files'][local]['sha256'],
                   'size': context['freeze']['files'][local]['bytes']} for name, local in UPLOADS.items()}


def validate_publication(context):
    pub = read_json(AUDIT, 'ZENODO_PUBLISH_RECEIPT.json')
    require(pub.get('state') == 'published' and pub.get('environment') == 'production', 'Confirmed production publication absent')
    require(type(pub.get('id')) is int and pub['id'] > 0 and pub.get('doi') == '10.5281/zenodo.' + str(pub['id'])
            and pub.get('doi_url') == 'https://doi.org/' + pub['doi']
            and pub.get('record_url') == 'https://zenodo.org/records/' + str(pub['id']), 'Production record/DOI identity is invalid')
    require(pub.get('title') == context['metadata']['title'] and pub.get('metadata_normalizations') == [], 'Canonical publication metadata drift')
    require(pub.get('canonical_metadata_sha256') == sha(safe_file(PACKAGE, 'metadata.json').read_bytes())
            and pub.get('accepted_input_manifest_sha256') == context['gate']['review_input_manifest_sha256'],
            'Publication is not bound to exact accepted canonical metadata/package')
    files = pub.get('files')
    require(type(files) is list and len(files) == len(UPLOADS), 'Unexpected published file count')
    require({x['name']: {'name': x['name'], 'sha256': x['sha256'], 'size': x['size']} for x in files}
            == expected_public_files(context), 'Published files differ from reviewed packet')
    public = read_json(AUDIT, 'ZENODO_PUBLIC_FILE_READBACK.json')
    require(public.get('verified') is True and public.get('authenticated') is False
            and public.get('id') == pub['id'] and public.get('doi') == pub['doi']
            and public.get('files') == list(expected_public_files(context).values()),
            'Actual unauthenticated public-file readback absent or different')
    return pub


def confirm_live_publication(context):
    """Revalidate saved publication by actual read-only kit and public reads."""
    from zenodo_pr464 import kit_cli, public_readback
    saved = validate_publication(context)
    inspected = kit_cli(context, 'inspect')
    require(inspected.get('state') == 'published' and inspected.get('id') == saved['id']
            and inspected.get('doi') == saved['doi']
            and inspected.get('doi_url') == saved['doi_url']
            and inspected.get('record_url') == saved['record_url'], 'Actual live publication differs from saved receipt')
    public_readback(context, inspected)
    return validate_publication(context)


def tracker_values(metadata, doi):
    return [[
        '30004807 / OWR-8415343-010 — Weak Bianchi Identities Across Timelike Singularities; '
        'original geometric conjecture: https://doi.org/10.4171/OWR/2021/40 (pp. 2232–2233)',
        '', doi,
        metadata['title'] + '; Alec Kriebel; version 1.0, 12 October 2026; '
        'https://github.com/AlecKriebel/Math/pull/464. Counterexample in the static-slice regular-ZAS '
        'and boundary-reaching vector-test scope: absolutely convergent defect -8 pi. '
        'Known Dadhich–Kar–Mukherjee–Visser metric/tensor and BKTZ boundary-flux method credited. '
        'NEC violated; arbitrary tilted slices, prescribed matter models and collapsed-point tests excluded. '
        'Extensive AI use; unrefereed; no independent human peer review, new-metric or first-priority claim. '
        'Paper and verification archive at DOI.'
    ]]


def validate_tracker(context, pub):
    tracker = read_json(AUDIT, 'TRACKER_APPEND_RECEIPT.json')
    require(tracker.get('verified') is True and tracker.get('spreadsheet_id') == SHEET
            and tracker.get('sheet_id') == TAB_ID and tracker.get('tab') == TAB
            and tracker.get('values') == tracker_values(context['metadata'], pub['doi_url'])
            and tracker.get('doi') == pub['doi_url'] and tracker.get('unique_doi_row_at_final_snapshot') is True,
            'Exact verified tracker record absent')
    require(type(tracker.get('updated_range')) is str
            and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1", tracker['updated_range']), 'Invalid exact tracker range')
    return tracker


def confirm_live_tracker(context, pub):
    tracker = validate_tracker(context, pub)
    check_sheet()
    rows = sheet_get("'Math Puzzles'!A:D").get('values', [])
    matching = doi_matches(pub['doi_url'], rows)
    values = tracker_values(context['metadata'], pub['doi_url'])
    require(len(matching) == 1 and rows[matching[0] - 1] == values[0], 'Actual live tracker record is not exact and unique')
    expected_range = f"'Math Puzzles'!A{matching[0]}:D{matching[0]}"
    require(expected_range == tracker['updated_range']
            and sheet_get(expected_range).get('values') == values, 'Actual live tracker range differs from saved receipt')
    return tracker


def gws(action, params, body=None, resource='values'):
    args = [GWS, 'sheets', 'spreadsheets']
    if resource == 'values':
        args += ['values']
    args += [action, '--params', json.dumps(params)]
    if body is not None:
        args += ['--json', json.dumps(body)]
    run = subprocess.run(args, capture_output=True, text=True, timeout=60)
    require(run.returncode == 0, 'Google Workspace operation failed; reconcile before retrying a write')
    return json.loads(run.stdout)


def sheet_get(range_name):
    return gws('get', {'spreadsheetId': SHEET, 'range': range_name})


def check_sheet():
    response = gws('get', {'spreadsheetId': SHEET, 'fields': 'spreadsheetId,sheets.properties'}, resource='spreadsheets')
    require(response.get('spreadsheetId') == SHEET, 'Wrong tracker spreadsheet')
    matching = [x['properties'] for x in response.get('sheets', []) if x.get('properties', {}).get('sheetId') == TAB_ID]
    require(len(matching) == 1 and matching[0].get('title') == TAB, 'Requested gid does not match tracker tab')
    require(sheet_get("'Math Puzzles'!A1:D1").get('values')
            == [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']], 'Tracker header changed')


def doi_matches(doi, rows):
    token = doi.removeprefix('https://doi.org/')
    return [i + 1 for i, row in enumerate(rows)
            if len(row) >= 3 and type(row[2]) is str and row[2].strip() in {doi, token}]
