"""PR209 native packet derivation and once-only preparation; import is inert.

Provider mutations are confined to main().  --reconcile only reads providers and
can promote a fully observed prior attempt; it never repeats an uncertain write.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Optimized Python prohibited')
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import base64
import hashlib
import json
import subprocess
import zipfile
from release_binding import (context, binding, unchanged, publication, tracker,
    acquire, exclusive_json, pr_identity, require, digest, durable_mkdir,
    public_exports)

ROOT = Path('/Users/alec/Documents/Math')
PUB = Path(__file__).resolve().parent
R = PUB.parent / 'preprint'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
API = 'repos/AlecKriebel/Math/'
OLD = 'fd09a95b479f376234835a4494693bb1316c85ec'
PREFIX = 'unsolved_math_prioritization/attempts/5100015/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
ZIPROOT = 'k303b_outer_center_pedal_product/'
BRANCH = 'dot/math-5100015'
PUBLIC_ADMIN = ('STAGE_ATTEMPT.json', 'ZENODO_STAGED_VERIFIED.json',
    'ZENODO_PREPUBLICATION_INSPECT.json', 'PUBLISH_ATTEMPT.json',
    'ZENODO_TOOL_PUBLICATION_RECEIPT.json', 'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json',
    'ZENODO_VERIFIED_PUBLICATION.json', 'TRACKER_VERIFIED_APPEND.json')


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def safe_name(name):
    require(type(name) is str and name and '\\' not in name and '\0' not in name,
            'Unsafe payload path')
    parts = PurePosixPath(name).parts
    require(not name.startswith('/') and '/'.join(parts) == name and
            all(x not in {'.', '..'} for x in parts), 'Noncanonical payload path')
    require(not any((x.startswith('.') and x != '.gitignore') or
            x.lower().startswith('private') or x in {'__pycache__', 'node_modules',
            'reproduction_environment'} or x.lower().endswith(('.env', '.pyc'))
            for x in parts), 'Private or cache payload path')
    return name


def safe_read(base, name):
    safe_name(name)
    base = Path(base)
    p = base / name
    require(p.is_file() and not p.is_symlink() and
            not any(q.is_symlink() for q in [p, *p.parents] if q != base.parent) and
            p.resolve().is_relative_to(base.resolve()), 'Missing/symlinked owned payload')
    return p.read_bytes()


def pins(files):
    return [dict(path=p, bytes=len(raw), sha256=sha(raw), git_blob_sha1=blob(raw))
            for p, raw in sorted(files.items())]


def pinned_bytes(base, row):
    require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'Invalid pin')
    raw = safe_read(base, row['path'])
    require(type(row['bytes']) is int and len(raw) == row['bytes'] and
            sha(raw) == row['sha256'], 'Pinned bytes changed')
    return raw


def release_time(value):
    require(type(value) is str, 'Missing durable release time')
    dt = datetime.fromisoformat(value)
    require(dt.tzinfo is not None and dt.utcoffset().total_seconds() == 0,
            'Release time must be UTC')
    require(dt <= datetime.now(timezone.utc), 'Future release time is not evidence')
    return value


def frozen_source(r):
    """Authenticate every ZIP entry against the frozen local source manifest."""
    manifest_raw = safe_read(r, 'SOURCE_MANIFEST.json')
    manifest = json.loads(manifest_raw)
    rows = manifest['files']
    require(type(rows) is list and rows and
            len({x['path'] for x in rows}) == len(rows), 'Empty/duplicate source manifest')
    source = {row['path']: pinned_bytes(r, row) for row in rows}
    source['SOURCE_MANIFEST.json'] = manifest_raw
    with zipfile.ZipFile(Path(r) / 'k303b-source-verification.zip') as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and
                set(names) == {ZIPROOT + p for p in source}, 'Exact frozen ZIP set differs')
        for info in archive.infolist():
            safe_name(info.filename)
            require(not info.is_dir() and (info.external_attr >> 16) & 0o170000
                    in {0, 0o100000}, 'Nonregular ZIP payload')
            require(archive.read(info.filename) == source[info.filename[len(ZIPROOT):]],
                    'ZIP/source bytes differ')
    return source


def expected_native_packet(r, pub, ctx, z, t, release_utc):
    """Derive the complete byte packet without relying on prepared pins/directories.

    The only changes inside the reviewed scientific presentation are enumerated
    administrative files. All other files, including PROOF and all 23 history
    members, retain the exact reviewed bytes.
    """
    release_time(release_utc)
    r, pub = Path(r), Path(pub)
    case = pub.parent
    case_path = case.relative_to(ROOT).as_posix() + '/'
    exports = public_exports(r, pub, ctx)
    source = frozen_source(r)
    minimum = {'preprint/' + p: raw for p, raw in source.items()}
    for name in ['k303b-source-verification.zip', 'PACKAGE_MANIFEST.json', 'deposit.json']:
        minimum['preprint/' + name] = safe_read(r, name)
    for name, raw in minimum.items():
        require(exports.get(name) == raw, 'Public export omits/differs from frozen source: ' + name)
    intake_raw = safe_read(case, 'initial_review_20261016/INTAKE.json')
    require(exports.get('initial_review_20261016/INTAKE.json') == intake_raw,
            'Intake must be explicitly sealed for public export')
    intake = json.loads(intake_raw)
    require(intake.get('head') == OLD and intake.get('branch') == BRANCH and
            intake.get('native_source_prefix') == PREFIX, 'Wrong archived intake identity')
    baseline_pin = ctx['clear'].get('progress_baseline')
    require(type(baseline_pin) is dict and baseline_pin.get('path') ==
            'publication/PROGRESS_BASELINE.json', 'Cleared progress baseline required')
    baseline_raw = pinned_bytes(case, baseline_pin)
    require(exports.get(baseline_pin['path']) == baseline_raw, 'Progress baseline must be sealed for public export')
    baseline = json.loads(baseline_raw)
    for field in ['previous_case_acceptance', 'previous_native_checkpoint_receipt']:
        require(exports.get(baseline[field]['path']) == pinned_bytes(case, baseline[field]),
                'Prior progress authority must be explicitly exported')
    native_prefix = 'pr_update/5100015/'
    original = {p[len(native_prefix):]: raw for p, raw in source.items()
                if p.startswith(native_prefix)}
    require({'PROOF.md', 'STATUS.md', 'README.md', 'readiness.json', 'RESEARCH_LOG.md'}
            <= set(original), 'Incomplete scientific presentation')
    original_pins = intake['original_source_files']
    require(type(original_pins) is list and len(original_pins) == 23 and
            len({x['native_path'] for x in original_pins}) == 23, 'Exactly 23 originals required')
    history = 'history/original_submission_20261016/'
    expected_history = set()
    for row in original_pins:
        require(row['native_path'].startswith(PREFIX), 'Original outside native subtree')
        name = history + row['native_path'][len(PREFIX):]
        safe_name(name)
        expected_history.add(name)
        raw = original.get(name)
        require(raw is not None and len(raw) == row['bytes'] and sha(raw) == row['sha256']
                and blob(raw) == row['native_blob'] and row['native_mode'] == '100644',
                'Original archive pin mismatch')
    require({p for p in original if p.startswith(history)} == expected_history,
            'Original history set differs from all 23 original pins')
    current = dict(original)
    ready = json.loads(original['readiness.json'])
    ready.update(current_assessment='claimed_solved audited and published; historical priority unestablished',
        preprint_upload_cleared=True, whole_package_reviews_completed=ctx['clear']['fresh_manuscript_reviews'],
        published_DOI=z['doi'], publication_record=z['record_url'], current_release_receipt='RELEASE_RECEIPT.json')
    current['readiness.json'] = encoded(ready)
    release = dict(utc=release_utc, status='claimed_solved', author_proof_turns='1/5',
        mathematical_verdict='PASS full signed outer/center-pedal product for strict confocal elliptical caustics and periods not divisible by 4, admitted stars/reversal/repetitions',
        priority='Exact contemporary Ferudun v1.1 Theorem 2/Section 6 and classical KLS/KS/AST/BT/Stachel/Jacobi/conic/meromorphic inputs credited; historical ordering/non-derivation/novelty undetermined; no first/exclusive/new-identity claim',
        source_year=2021, source_year_role='Published original conjecture edition; arXiv first appeared 2020',
        original_native_head=OLD, original23files_archived_byte_identical=True,
        release_binding=binding(ctx), publication=z, tracker=t,
        unrefereed=True, extensive_AI_assistance=True, independent_human_peer_review=False,
        native_merge_at_receipt_creation='Pending separately verified actual GitHub merge event')
    for name in ['FINAL_ACCEPTANCE.json', 'RELEASE_RECEIPT.json']:
        current[name] = encoded(release)
    current['PUBLICATION_RECEIPT.json'] = encoded(dict(publication=z, tracker=t))
    current['PUBLICATION_METADATA.json'] = encoded(z['metadata'])
    update = ('\n\nActual publication: ' + z['doi_url'] + '; one verified four-cell tracker row ' +
        t['updated_range'] + '. Required sequential whole-package and source reviews and all required repairs '
        'are complete under the bound final clearance. Dated preparation text is historical. '
        'Exact contemporary/classical credits, priority limitations, extensive AI assistance and unrefereed '
        'status remain. All 23 originals and reviewed mathematical proof bytes are unchanged. '
        'The native merge is pending its separate verified event. See RELEASE_RECEIPT.json.\n')
    for name in ['PUBLICATION_STATUS.md', 'FINAL_DISPOSITION.md']:
        current[name] = b'# Accepted outer center-pedal area product: claimed_solved\n\n' + original['STATUS.md'] + update.encode()
    current['README.md'] = original['README.md'] + update.encode()
    current['RESEARCH_LOG.md'] = original['RESEARCH_LOG.md'] + ('\n' + release_utc +
        ' — case 95%: exact reviewed preprint published; four-cell tracker verified. '
        'Native readback and merge pending; author 1/5 and 23 originals retained.\n').encode()
    current['MANIFEST.json'] = encoded(dict(scope='Accepted administrative presentation; reviewed mathematics/history unchanged',
        files=[{k: v for k, v in p.items() if k != 'git_blob_sha1'} for p in pins({
            p: raw for p, raw in current.items() if '/' not in p and p not in {'MANIFEST.json', 'CURRENT_PACKET_MANIFEST.json'}})]))
    current['CURRENT_PACKET_MANIFEST.json'] = encoded(dict(schema='pr209-current-packet-v1',
        self_excluded=True, source_head=OLD,
        files=[{k: v for k, v in p.items() if k != 'git_blob_sha1'} for p in pins({
            p: raw for p, raw in current.items() if p != 'CURRENT_PACKET_MANIFEST.json'})],
        release_delta='Actual review/DOI/tracker administrative facts only'))
    packet = {PREFIX + p: raw for p, raw in current.items()}
    for name, raw in exports.items():
        safe_name(name)
        packet[case_path + name] = raw
    # Each post-clearance addition has an exact name and validated lineage, never
    # a filesystem enumeration. publication()/tracker() validate that lineage.
    additions = {'preprint/FINAL_CLEARANCE.json': safe_read(r, 'FINAL_CLEARANCE.json'),
                 'publication/PUBLIC_EXPORT_MANIFEST.json': pinned_bytes(case, ctx['clear']['public_export_manifest'])}
    for name in PUBLIC_ADMIN:
        additions['publication/' + name] = safe_read(pub, name)
    for name, raw in additions.items():
        require(name not in exports, 'Static public exports contain post-clearance administrative records')
        packet[case_path + name] = raw
    require(len(packet) == len(current) + len(exports) + len(additions), 'Native packet path collision')
    return packet


def expected_pr_metadata(z, t):
    return dict(title='5100015: audited outer center-pedal area product and published preprint',
        body='Proves k303,b: signed product of the OUTER tangent-polygon area and actual center-perpendicular-foot area on its boundary tangent side lines, for strict confocal elliptical caustics and periods not divisible by four, admitted coprime stars/reversal/fixed repeats. All 23 original artifacts and author turn 1/5 preserved.\n\n'
        'The fixed-linear edge-vector map, signed-area traces and classical odd Jacobi identity give the full proof and invariant value. KLS2002/KS2003-2004/AST-BT2020/Stachel/Jacobi/conic and established meromorphic methods credited. A. Ferudun 2026 v1.1 Theorem 2/Section 6 is the exact contemporary full theorem; v1.0 primitive-even subset distinguished. Historical ordering, non-derivation and novelty undetermined; no first/exclusive/new-identity/current-worldwide-open claim.\n\n'
        'Bounded source/priority reproduction, required NEW sequential whole-package and helper-source reviews and all required repairs completed. Exact controls and labelled uncertified diagnostics accompany the note. Extensive AI use; unrefereed, no independent human peer review or formal verification.\n\n'
        'Verified preprint/source archive: ' + z['doi_url'] + '. One GWS append/all four cells verified ' + t['updated_range'] + '.')


def check_metadata(pr, metadata):
    require(all(pr.get(k) == v for k, v in metadata.items()), 'Actual canonical PR title/body differs')


def patch_queue(raw, intake, z):
    text = raw.decode('utf-8')
    rows = [x for x in text.splitlines() if '5100015 / AMR-050-0015' in x]
    original = intake['queue_row']
    fields = original.split('|')
    require(len(fields) == 14 and fields[7].strip() == '2021' and
            fields[8].strip() == 'claimed_solved' and fields[9].strip() == '1/5', 'Wrong original eligibility')
    placeholder = fields.copy()
    placeholder[8], placeholder[9] = ' queued ', ' 0/5 '
    for n in [10, 11, 12]:
        placeholder[n] = '  '
    require(len(rows) == 1 and rows[0] in {original, '|'.join(placeholder)} and
            text.count(rows[0]) == 1, 'Main row differs from exact original/queued placeholder')
    fields = rows[0].split('|')
    fields[8], fields[9] = ' claimed_solved ', ' 1/5 '
    fields[11] = ' [Audited outer center-pedal product; credited preprint](attempts/5100015/FINAL_DISPOSITION.md) '
    fields[12] = ' ' + z['doi_url'] + ' '
    row = '|'.join(fields)
    return text.replace(rows[0], row).encode(), row


class NativeAPI:
    def __init__(self, pub, label, readonly=False):
        self.transport = Path(pub) / 'private_transport' / datetime.now(timezone.utc).strftime(label + '_%Y%m%dT%H%M%S%fZ')
        durable_mkdir(self.transport, exist_ok=False)
        self.seq, self.readonly = 0, readonly

    def __call__(self, method, path, payload=None, graphql=False):
        require(not self.readonly or method == 'GET', 'Read-only reconciliation forbids mutation')
        self.seq += 1
        args = [GH, 'api', '--method', method, path if graphql else API + path]
        if payload is not None:
            q = self.transport / f'{self.seq:04d}-request.json'
            q.write_bytes(encoded(payload))
            args += ['--input', str(q)]
        try:
            run = subprocess.run(args, capture_output=True, timeout=90)
        except Exception as error:
            # Timeouts/launch failures can carry partial binary provider output.
            # Preserve it without decoding loss; the durable pre-write intent
            # remains the once-only anchor even when no response was received.
            for attr in ['stdout', 'stderr']:
                partial = getattr(error, attr, None)
                if partial is not None:
                    if isinstance(partial, str):
                        partial = partial.encode('utf-8', errors='surrogatepass')
                    (self.transport / f'{self.seq:04d}-partial-{attr}.bin').write_bytes(partial)
            (self.transport / f'{self.seq:04d}-exception.json').write_bytes(encoded(
                dict(type=type(error).__name__, message=str(error), method=method, path=path)))
            raise RuntimeError('Native outcome unknown; retain intent and reconcile read-only') from error
        (self.transport / f'{self.seq:04d}-stdout.json').write_bytes(run.stdout)
        (self.transport / f'{self.seq:04d}-stderr.txt').write_bytes(run.stderr)
        require(run.returncode == 0, 'Native outcome failed/unknown; retain intent and reconcile read-only')
        return json.loads(run.stdout)


class NativeTrees:
    def __init__(self, api):
        self.api, self.cache, self.bodies = api, {}, {}

    def listing(self, tree):
        if tree not in self.cache:
            result = self.api('GET', 'git/trees/' + tree)
            rows = result['tree']
            require(result.get('truncated') is False and len({r['path'] for r in rows}) == len(rows), 'Incomplete native tree')
            for row in rows:
                require('/' not in row['path'] and row['path'] not in {'.', '..'}, 'Noncanonical native entry')
                require((row['type'], row['mode']) in {('tree', '040000'), ('blob', '100644'),
                    ('blob', '100755'), ('blob', '120000'), ('commit', '160000')}, 'Unknown native mode/type')
            self.cache[tree] = {r['path']: r for r in rows}
        return self.cache[tree]

    def lookup(self, tree, path):
        parts = path.split('/')
        for n, part in enumerate(parts):
            row = self.listing(tree).get(part)
            if row is None:
                return None
            if n == len(parts) - 1:
                return row
            require(row['type'] == 'tree' and row['mode'] == '040000', 'Native ancestor is not directory')
            tree = row['sha']

    def flatten(self, tree, prefix=''):
        out = {}
        for name, row in self.listing(tree).items():
            path = prefix + name
            if row['type'] == 'tree':
                out.update(self.flatten(row['sha'], path + '/'))
            else:
                out[path] = {k: row[k] for k in ['sha', 'type', 'mode']}
        return out

    def difference(self, left, right, prefix=''):
        """Complete tree delta, independent of GitHub compare pagination/caps."""
        if left == right:
            return {}
        a, b = self.listing(left) if left else {}, self.listing(right) if right else {}
        out = {}
        for name in sorted(set(a) | set(b)):
            x, y = a.get(name), b.get(name)
            if x == y:
                continue
            path = prefix + name
            if (x is None or x['type'] == 'tree') and (y is None or y['type'] == 'tree'):
                out.update(self.difference(x['sha'] if x else None, y['sha'] if y else None, path + '/'))
            else:
                if x and x['type'] == 'tree':
                    out.update({p: (v, None) for p, v in self.flatten(x['sha'], path + '/').items()})
                if y and y['type'] == 'tree':
                    out.update({p: (None, v) for p, v in self.flatten(y['sha'], path + '/').items()})
                xx = {k: x[k] for k in ['sha', 'type', 'mode']} if x and x['type'] != 'tree' else None
                yy = {k: y[k] for k in ['sha', 'type', 'mode']} if y and y['type'] != 'tree' else None
                if xx or yy:
                    out[path] = (xx, yy)
        return out

    def read(self, tree, path):
        row = self.lookup(tree, path)
        require(row and row['type'] == 'blob' and row['mode'] == '100644', 'Expected native regular file missing')
        key = row['sha']
        if key not in self.bodies:
            item = self.api('GET', 'git/blobs/' + key)
            require(item.get('encoding') == 'base64' and item.get('sha') == key, 'Native blob identity/encoding differs')
            raw = base64.b64decode(item['content'], validate=False)
            require(blob(raw) == key and item.get('size') == len(raw), 'Native blob body/hash differs')
            self.bodies[key] = raw
        return self.bodies[key]

    def verify_overlay(self, base_tree, actual_tree, files):
        expected_delta = {}
        for path, raw in files.items():
            target = dict(sha=blob(raw), mode='100644', type='blob')
            old = self.lookup(base_tree, path)
            old = {k: old[k] for k in ['sha', 'mode', 'type']} if old else None
            if old != target:
                expected_delta[path] = (old, target)
            require(self.read(actual_tree, path) == raw, 'Native body differs from independently expected bytes: ' + path)
        require(self.difference(base_tree, actual_tree) == expected_delta, 'Native full changed scope differs')
        require(self.lookup(base_tree, PREFIX.rstrip('/')) is None, 'Base scientific subtree already exists')
        row = self.lookup(actual_tree, PREFIX.rstrip('/'))
        require(row and row['type'] == 'tree', 'Scientific subtree missing')
        require(set(self.flatten(row['sha'], PREFIX)) == {p for p in files if p.startswith(PREFIX)}, 'Scientific subtree has missing/extra members')
        return pins(files)


def verify_original(trees, api, intake):
    commit = api('GET', 'git/commits/' + OLD)
    tree = commit['tree']['sha']
    raw = trees.read(tree, QUEUE)
    require(blob(raw) == intake['Queue_blob'] and sha(raw) == intake['Queue_sha256'] and
            [x for x in raw.decode().splitlines() if '5100015 / AMR-050-0015' in x] == [intake['queue_row']], 'Original native QUEUE differs')
    row = trees.lookup(tree, PREFIX.rstrip('/'))
    require(row and row['type'] == 'tree', 'Original source subtree missing')
    original = trees.flatten(row['sha'], PREFIX)
    require(set(original) == {r['native_path'] for r in intake['original_source_files']}, 'Original native 23-file set differs')
    for pin in intake['original_source_files']:
        raw = trees.read(tree, pin['native_path'])
        require(blob(raw) == pin['native_blob'] and sha(raw) == pin['sha256'] and len(raw) == pin['bytes'] and pin['native_mode'] == '100644', 'Original native body differs')


def no_active_rules(api, branch):
    from urllib.parse import quote
    name = quote(branch, safe='')
    branch_info = api('GET', 'branches/' + name)
    require(branch_info.get('protected') is False and api('GET', 'rules/branches/' + name) == [] and
            api('GET', 'rulesets') == [], 'Native ref update cannot establish repository rules compliance; no bypass')


def upload_overlay(api, base_tree, files):
    entries = []
    for path, raw in sorted(files.items()):
        safe_name(path)
        try:
            entry = dict(path=path, mode='100644', type='blob', content=raw.decode('utf-8'))
        except UnicodeDecodeError:
            response = api('POST', 'git/blobs', dict(content=base64.b64encode(raw).decode(), encoding='base64'))
            require(response['sha'] == blob(raw), 'Uploaded blob identity differs')
            entry = dict(path=path, mode='100644', type='blob', sha=blob(raw))
        entries.append(entry)
    return api('POST', 'git/trees', dict(base_tree=base_tree, tree=entries))['sha']


def read_record(pub, name):
    return json.loads(safe_read(pub, name))


def prepare_spec(ctx, pub, main, main_tree, files, release_utc, metadata):
    return dict(schema='pr209-native-object-intent-v2', release_utc=release_utc,
        original_head=OLD, main_parent=main, base_tree=main_tree, parents=[OLD, main],
        branch=BRANCH, expected_pins=pins(files), pr_metadata=metadata,
        release_binding=binding(ctx), publication_receipt_sha256=digest(Path(pub) / 'ZENODO_VERIFIED_PUBLICATION.json'),
        tracker_receipt_sha256=digest(Path(pub) / 'TRACKER_VERIFIED_APPEND.json'))


def load_preparation(r, pub, ctx, z, t, api, trees):
    """Validate all durable ancestry, deriving pins rather than trusting a receipt."""
    intent = read_record(pub, 'NATIVE_OBJECT_BUILD_INTENT.json')
    main = intent['main_parent']
    main_commit = api('GET', 'git/commits/' + main)
    files = expected_native_packet(r, pub, ctx, z, t, intent['release_utc'])
    intake = json.loads(safe_read(Path(pub).parent, 'initial_review_20261016/INTAKE.json'))
    newq, row = patch_queue(trees.read(main_commit['tree']['sha'], QUEUE), intake, z)
    files[QUEUE] = newq
    require(intent == prepare_spec(ctx, pub, main, main_commit['tree']['sha'], files,
            intent['release_utc'], expected_pr_metadata(z, t)), 'Object preparation intent differs from derived authority')
    built = read_record(pub, 'NATIVE_OBJECTS_BUILT.json')
    require(built.get('schema') == 'pr209-native-objects-built-v2' and
            built.get('object_intent_sha256') == digest(Path(pub) / 'NATIVE_OBJECT_BUILD_INTENT.json') and
            built.get('parents') == [OLD, main], 'Built object ancestry differs')
    commit = api('GET', 'git/commits/' + built['head'])
    require(commit['tree']['sha'] == built['tree'] and [x['sha'] for x in commit['parents']] == [OLD, main], 'Prepared commit tree/parents differ')
    ref = read_record(pub, 'NATIVE_PREPARE_ATTEMPT.json')
    require(ref == dict(schema='pr209-native-ref-intent-v2', old=OLD, head=built['head'],
        branch=BRANCH, nonforce=True, tree=built['tree'], release_binding=binding(ctx),
        object_build_receipt_sha256=digest(Path(pub) / 'NATIVE_OBJECTS_BUILT.json')), 'Ref intent differs')
    meta = read_record(pub, 'NATIVE_METADATA_ATTEMPT.json')
    require(meta == dict(schema='pr209-native-metadata-intent-v2', head=built['head'],
        metadata=expected_pr_metadata(z, t), ref_intent_sha256=digest(Path(pub) / 'NATIVE_PREPARE_ATTEMPT.json'),
        release_binding=binding(ctx)), 'Metadata intent differs')
    verify_original(trees, api, intake)
    trees.verify_overlay(main_commit['tree']['sha'], built['tree'], files)
    return intent, built, files, row


def prepared_record(pub, ctx, intent, built, row):
    return dict(schema='pr209-prepared-v2', status='COMPLETED', release_utc=intent['release_utc'],
        prepared_head=built['head'], original_head=OLD, main_parent=intent['main_parent'],
        tree=built['tree'], parents=intent['parents'], target_queue_row=row,
        included_owned_pins=intent['expected_pins'], pr_metadata=intent['pr_metadata'],
        release_binding=binding(ctx), object_intent_sha256=digest(Path(pub) / 'NATIVE_OBJECT_BUILD_INTENT.json'),
        object_build_receipt_sha256=digest(Path(pub) / 'NATIVE_OBJECTS_BUILT.json'),
        ref_intent_sha256=digest(Path(pub) / 'NATIVE_PREPARE_ATTEMPT.json'),
        metadata_intent_sha256=digest(Path(pub) / 'NATIVE_METADATA_ATTEMPT.json'),
        publication_receipt_sha256=intent['publication_receipt_sha256'],
        tracker_receipt_sha256=intent['tracker_receipt_sha256'],
        native_merge='Pending independently derived readback and actual GitHub merge event',
        local_Git_index_ref_mutations=0)


def live_release(r, pub, ctx, z, t):
    from verify_published_readonly import verify_publication_live
    from append_verified_tracker import verify_tracker_live
    unchanged(r, ctx)
    require(publication(r, pub, ctx) == z and tracker(r, pub, ctx, z) == t, 'Accepted release receipts changed')
    evidence = dict(publication=verify_publication_live(r, pub, ctx),
                    tracker=verify_tracker_live(r, pub, ctx, z))
    unchanged(r, ctx)
    require(publication(r, pub, ctx) == z and tracker(r, pub, ctx, z) == t, 'Release changed during actual public readback')
    return evidence


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(argv in [[], ['--reconcile']], 'Only --reconcile is supported')
    reconcile = bool(argv)
    with acquire(PUB):
        ctx = context(R)
        z, t = publication(R, PUB, ctx), tracker(R, PUB, ctx)
        api = NativeAPI(PUB, 'native_prepare', readonly=reconcile)
        trees = NativeTrees(api)
        if not reconcile:
            require(not any((PUB / n).exists() for n in ['PR_PREPARED.json', 'NATIVE_OBJECT_BUILD_INTENT.json',
                'NATIVE_OBJECTS_BUILT.json', 'NATIVE_PREPARE_ATTEMPT.json', 'NATIVE_METADATA_ATTEMPT.json']),
                'Prior native preparation exists; use read-only --reconcile')
            release_utc = datetime.now(timezone.utc).isoformat()
            files = expected_native_packet(R, PUB, ctx, z, t, release_utc)
            intake = json.loads(safe_read(PUB.parent, 'initial_review_20261016/INTAKE.json'))
            pr = api('GET', 'pulls/209')
            pr_identity(pr, OLD, True)
            verify_original(trees, api, intake)
            main_head = api('GET', 'git/ref/heads/main')['object']['sha']
            mc = api('GET', 'git/commits/' + main_head)
            require(trees.lookup(mc['tree']['sha'], PREFIX.rstrip('/')) is None, 'Main scientific subtree exists; reconcile')
            newq, row = patch_queue(trees.read(mc['tree']['sha'], QUEUE), intake, z)
            files[QUEUE] = newq
            metadata = expected_pr_metadata(z, t)
            live_release(R, PUB, ctx, z, t)
            # The exact object payload and its full binding are durable BEFORE
            # the first blob/tree/commit POST, including uncertain outcomes.
            intent = prepare_spec(ctx, PUB, main_head, mc['tree']['sha'], files, release_utc, metadata)
            exclusive_json(PUB / 'NATIVE_OBJECT_BUILD_INTENT.json', intent)
            tree = upload_overlay(api, mc['tree']['sha'], files)
            head = api('POST', 'git/commits', dict(message='Integrate PR209 audited outer center-pedal publication; preserve 23 originals', tree=tree, parents=[OLD, main_head]))['sha']
            commit = api('GET', 'git/commits/' + head)
            require(commit['tree']['sha'] == tree and [x['sha'] for x in commit['parents']] == [OLD, main_head], 'Created commit differs')
            trees.verify_overlay(mc['tree']['sha'], tree, files)
            built = dict(schema='pr209-native-objects-built-v2', head=head, tree=tree,
                parents=[OLD, main_head], object_intent_sha256=digest(PUB / 'NATIVE_OBJECT_BUILD_INTENT.json'))
            exclusive_json(PUB / 'NATIVE_OBJECTS_BUILT.json', built)
            pr_identity(api('GET', 'pulls/209'), OLD, True)
            live_release(R, PUB, ctx, z, t)
            require(expected_native_packet(R, PUB, ctx, z, t, release_utc) == {p: b for p, b in files.items() if p != QUEUE}, 'Public packet changed before ref update')
            no_active_rules(api, BRANCH)
            exclusive_json(PUB / 'NATIVE_PREPARE_ATTEMPT.json', dict(schema='pr209-native-ref-intent-v2',
                old=OLD, head=head, branch=BRANCH, nonforce=True, tree=tree,
                release_binding=binding(ctx), object_build_receipt_sha256=digest(PUB / 'NATIVE_OBJECTS_BUILT.json')))
            api('PATCH', 'git/refs/heads/' + BRANCH, dict(sha=head, force=False))
            require(api('GET', 'git/ref/heads/' + BRANCH)['object']['sha'] == head, 'Branch readback differs')
            exclusive_json(PUB / 'NATIVE_METADATA_ATTEMPT.json', dict(schema='pr209-native-metadata-intent-v2',
                head=head, metadata=metadata, ref_intent_sha256=digest(PUB / 'NATIVE_PREPARE_ATTEMPT.json'), release_binding=binding(ctx)))
            api('PATCH', 'pulls/209', metadata)
        intent, built, files, row = load_preparation(R, PUB, ctx, z, t, api, trees)
        pr = api('GET', 'pulls/209')
        pr_identity(pr, built['head'], True)
        check_metadata(pr, expected_pr_metadata(z, t))
        require(api('GET', 'git/ref/heads/' + BRANCH)['object']['sha'] == built['head'], 'Actual ref differs')
        live_release(R, PUB, ctx, z, t)
        # Public readbacks can be lengthy; observe metadata/ref again last.
        pr = api('GET', 'pulls/209')
        pr_identity(pr, built['head'], True)
        check_metadata(pr, expected_pr_metadata(z, t))
        require(api('GET', 'git/ref/heads/' + BRANCH)['object']['sha'] == built['head'], 'Actual ref changed before completion')
        receipt = prepared_record(PUB, ctx, intent, built, row)
        if (PUB / 'PR_PREPARED.json').exists():
            require(read_record(PUB, 'PR_PREPARED.json') == receipt, 'Completed preparation record differs')
        else:
            exclusive_json(PUB / 'PR_PREPARED.json', receipt)
        print(json.dumps({k: v for k, v in receipt.items() if k != 'included_owned_pins'}, indent=2))


if __name__ == '__main__':
    main()
