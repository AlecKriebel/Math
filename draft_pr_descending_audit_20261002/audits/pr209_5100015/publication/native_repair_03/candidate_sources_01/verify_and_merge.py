"""Derive PR209's bytes independently and complete a guarded native merge.

A two-parent commit uses exactly the fresh main tree plus the reviewed overlay.
Nonforce main update rejects unrelated concurrent advances. Active/unknown
repository rules block this mechanism. --reconcile never repeats a write.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release helpers refuse optimized Python before any action')
from pathlib import Path
from datetime import datetime, timezone
import json
import os
from release_binding import (context, binding, publication, tracker, acquire,
    exclusive_json, pr_identity, require, digest, durable_mkdir,
    pinned as retained_pin, checked_path, sync_directory, utc, tool_publication,
    verify_doi, tracker_properties, tracker_readback, tracker_row_number,
    require_unique_tracker, FULL_RANGE)
from integrate_reviewed_pr import (ROOT, PUB, R, OLD, PREFIX, QUEUE, BRANCH,
    NativeAPI, NativeTrees, expected_native_packet, expected_pr_metadata,
    check_metadata, load_preparation, prepared_record, read_record, safe_read,
    pinned_bytes, patch_queue, pins, blob, sha, upload_overlay, no_active_rules,
    live_release)


def progress_baseline(r, pub, ctx, api, trees):
    """Authenticate the immutable prior acceptance; never recount other work."""
    case = Path(pub).parent
    pin = ctx['clear'].get('progress_baseline')
    require(type(pin) is dict and pin.get('path') == 'publication/PROGRESS_BASELINE.json', 'Missing cleared progress baseline')
    raw = pinned_bytes(case, pin)
    baseline = json.loads(raw)
    require(baseline.get('schema') == 'pr209-descending-progress-baseline-v1' and
            baseline.get('scope') == 'own_descending_shard' and
            baseline.get('previous_completed_PR') == 210 and baseline.get('current_PR') == 209,
            'Wrong progress scope/identity')
    counts = baseline.get('counts')
    require(type(counts) is list and len(counts) == 4 and
            all(type(n) is int and n >= 0 for n in counts), 'Invalid progress counters')
    acceptance_raw = pinned_bytes(case, baseline['previous_case_acceptance'])
    acceptance = json.loads(acceptance_raw)
    require(acceptance.get('PR') == 210 and acceptance.get('case_completion_percent') == 100 and
            acceptance.get('actual_publication_tracker_native_merge_complete') is True and
            acceptance.get('actual_both_public_size_SHA256_verified') is True and
            acceptance.get('single_append_all_four_cells_verified') is True and
            acceptance.get('counts') == counts, 'Prior completed acceptance/counts differ')
    checkpoint = json.loads(pinned_bytes(case, baseline['previous_native_checkpoint_receipt']))
    require(checkpoint.get('commit') == checkpoint.get('main_readback') == baseline.get('authenticated_native_checkpoint') and
            baseline.get('actual_native_acceptance_body_byte_identical') is True and
            blob(acceptance_raw) == baseline.get('authenticated_acceptance_git_blob_sha1'),
            'Prior native checkpoint authority differs')
    rows = [x for x in checkpoint['owned_files'] if x.get('bytes') == len(acceptance_raw) and
            x.get('sha256') == sha(acceptance_raw) and x.get('git_blob_sha1') == blob(acceptance_raw)]
    require(len(rows) == 1, 'Native checkpoint must uniquely pin the exact prior acceptance')
    commit = api('GET', 'git/commits/' + checkpoint['commit'])
    require(trees.read(commit['tree']['sha'], rows[0]['path']) == acceptance_raw, 'Actual pinned native prior acceptance differs')
    return dict(scope=baseline['scope'], baseline_sha256=sha(raw), previous_counts=counts,
                completed_counts=[counts[0] + 1, counts[1] + 1, counts[2] + 1, counts[3]],
                prior_acceptance_sha256=sha(acceptance_raw), prior_native_checkpoint=checkpoint['commit'])


def prepared_authority(r, pub, ctx, z, t, api, trees):
    intent, built, files, row = load_preparation(r, pub, ctx, z, t, api, trees)
    require(read_record(pub, 'PR_PREPARED.json') == prepared_record(pub, ctx, intent, built, row),
            'Prepared receipt is incomplete or differs from independently derived authority')
    return intent, built, files, row


def current_pr(api, head, metadata, draft=None, state='open'):
    pr = api('GET', 'pulls/209')
    pr_identity(pr, head, draft, state=state)
    check_metadata(pr, metadata)
    require(pr.get('merged') is (state == 'closed'), 'Unexpected actual PR merged status')
    require(api('GET', 'git/ref/heads/' + BRANCH)['object']['sha'] == head, 'Actual PR branch ref changed')
    return pr


def guarded_main_tree(trees, base_commit, commit, packet, case_prefix):
    tree = commit['tree']['sha']
    require(trees.lookup(tree, PREFIX.rstrip('/')) is None, 'Current main scientific subtree exists; reconcile without overwrite')
    changes = trees.difference(base_commit['tree']['sha'], tree)
    require(not any(path.startswith(case_prefix) or path.startswith(PREFIX) or
            (path in packet and path != QUEUE) for path in changes), 'Current main changed a case/owned path after preparation')


def fresh_main(api, trees, base_commit, packet, intake, z, case_prefix):
    head = api('GET', 'git/ref/heads/main')['object']['sha']
    commit = api('GET', 'git/commits/' + head)
    guarded_main_tree(trees, base_commit, commit, packet, case_prefix)
    queue, row = patch_queue(trees.read(commit['tree']['sha'], QUEUE), intake, z)
    files = {p: raw for p, raw in packet.items() if p != QUEUE}
    files[QUEUE] = queue
    return head, commit, files, row


def merge_spec(pub, ctx, prepared_head, main, main_tree, files, row, progress,
               number, history):
    ready = read_record(pub, 'NATIVE_READY_ATTEMPT.json')
    require(ready.get('schema') == 'pr209-ready-intent-v2' and
            ready.get('head') == prepared_head and ready.get('release_binding') == binding(ctx) and
            ready.get('prepared_receipt_sha256') == digest(Path(pub) / 'PR_PREPARED.json') and
            ready.get('pr_metadata') == read_record(pub, 'PR_PREPARED.json')['pr_metadata'] and
            type(ready.get('was_draft')) is bool and ready.get('operation') ==
            ('mark_ready' if ready['was_draft'] else 'observed_already_ready'), 'Ready intent ancestry differs')
    return dict(schema='pr209-native-merge-object-intent-v2', main_parent=main,
        attempt_number=number, prior_abandoned_attempts=history,
        reviewed_head=prepared_head, parents=[main, prepared_head], base_tree=main_tree,
        expected_pins=pins(files), target_queue_row=row, progress_baseline=progress,
        prepared_receipt_sha256=digest(Path(pub) / 'PR_PREPARED.json'),
        ready_intent_sha256=digest(Path(pub) / 'NATIVE_READY_ATTEMPT.json'),
        release_binding=binding(ctx), nonforce=True)


def attempt_folders(pub):
    root = Path(pub) / 'private_transport/native_merge_attempts'
    if not root.exists():
        return []
    require(root.is_dir() and not root.is_symlink() and not root.parent.is_symlink(), 'Unsafe merge attempt root')
    folders = sorted(root.iterdir())
    require([p.name for p in folders] == [f'{n:04d}' for n in range(1, len(folders) + 1)],
            'Merge attempts must be consecutive append-only numbered directories')
    for folder in folders:
        require(folder.is_dir() and not folder.is_symlink(), 'Unsafe merge attempt directory')
        require(all(p.is_file() and not p.is_symlink() and p.name in
                {'OBJECT_INTENT.json', 'OBJECTS_BUILT.json', 'ABANDONED_BEFORE_MAIN.json'}
                for p in folder.iterdir()), 'Unexpected merge attempt evidence')
    return folders


def retained_record_pin(path, pub):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'Missing retained native record')
    raw = path.read_bytes()
    return dict(path=path.relative_to(Path(pub).parent).as_posix(), bytes=len(raw), sha256=sha(raw))


def response_pin(api, pub):
    """Durably pin the actual raw provider response just returned by NativeAPI."""
    path = api.transport / f'{api.seq:04d}-stdout.json'
    with path.open('rb') as handle:
        os.fsync(handle.fileno())
    sync_directory(path.parent)
    return retained_record_pin(path, pub)


def load_attempt(folder, pub, ctx, built, packet, intake, z, progress, api, trees,
                 base_commit, case_prefix, history):
    intent = read_record(folder, 'OBJECT_INTENT.json')
    main = intent['main_parent']
    mc = api('GET', 'git/commits/' + main)
    guarded_main_tree(trees, base_commit, mc, packet, case_prefix)
    queue, row = patch_queue(trees.read(mc['tree']['sha'], QUEUE), intake, z)
    files = {p: raw for p, raw in packet.items() if p != QUEUE}
    files[QUEUE] = queue
    require(intent == merge_spec(pub, ctx, built['head'], main, mc['tree']['sha'], files,
            row, progress, int(folder.name), history), 'Merge intent differs from independently derived bytes/history')
    objects = read_record(folder, 'OBJECTS_BUILT.json')
    require(objects.get('schema') == 'pr209-native-merge-objects-built-v2' and
            objects.get('merge_object_intent_sha256') == digest(folder / 'OBJECT_INTENT.json') and
            objects.get('parents') == [main, built['head']], 'Merge object ancestry differs')
    commit = api('GET', 'git/commits/' + objects['head'])
    require(commit['tree']['sha'] == objects['tree'] and
            [x['sha'] for x in commit['parents']] == [main, built['head']], 'Actual merge commit/parents differ')
    trees.verify_overlay(mc['tree']['sha'], objects['tree'], files)
    return intent, objects, files, row


def abandonment_spec(folder, pub, ctx, intent, objects, observed, observed_commit,
                     ref_pin, commit_pin, ancestry_pin, trees, queue, stamp):
    base_tree = intent['base_tree']
    changes = trees.difference(base_tree, observed_commit['tree']['sha'])
    return dict(schema='pr209-abandoned-before-main-v1', utc=stamp,
        attempt_number=int(folder.name), status='TERMINAL_ABANDONED',
        reason='Observed foreign main advance before any durable main-ref request',
        observed_main=observed, observed_tree=observed_commit['tree']['sha'],
        observed_queue_sha256=sha(queue),
        observed_complete_tree_delta=[dict(path=p, before=x, after=y) for p, (x,y) in sorted(changes.items())],
        actual_main_ref_readback=ref_pin, actual_main_commit_readback=commit_pin,
        actual_ancestry_readback=ancestry_pin,
        object_intent_sha256=digest(folder / 'OBJECT_INTENT.json'),
        objects_built_sha256=digest(folder / 'OBJECTS_BUILT.json'), release_binding=binding(ctx))


def validate_abandonment(folder, pub, ctx, intent, objects, packet, intake, z,
                         api, trees, base_commit, case_prefix):
    record = read_record(folder, 'ABANDONED_BEFORE_MAIN.json')
    utc(record.get('utc'))
    case = Path(pub).parent
    ref = json.loads(retained_pin(case, record['actual_main_ref_readback']).read_bytes())
    observed = ref['object']['sha']
    require(observed != intent['main_parent'], 'Abandonment requires an actual main advance')
    retained = json.loads(retained_pin(case, record['actual_main_commit_readback']).read_bytes())
    commit = api('GET', 'git/commits/' + observed)
    require(retained == commit, 'Observed immutable main commit readback differs')
    ancestry = json.loads(retained_pin(case, record['actual_ancestry_readback']).read_bytes())
    require(ancestry.get('status') == 'ahead' and ancestry.get('merge_base_commit', {}).get('sha') == intent['main_parent'],
            'Abandonment main advance must descend from the exact attempted base')
    actual_ancestry = api('GET', 'compare/' + intent['main_parent'] + '...' + observed)
    require(actual_ancestry.get('status') == 'ahead' and
            actual_ancestry.get('merge_base_commit', {}).get('sha') == intent['main_parent'], 'Observed main ancestry no longer verifies')
    guarded_main_tree(trees, base_commit, commit, packet, case_prefix)
    queue = trees.read(commit['tree']['sha'], QUEUE)
    patch_queue(queue, intake, z)
    require(record == abandonment_spec(folder, pub, ctx, intent, objects, observed, commit,
        record['actual_main_ref_readback'], record['actual_main_commit_readback'],
        record['actual_ancestry_readback'], trees, queue, record['utc']), 'Abandonment evidence/lineage differs')
    return record


def abandon_advanced_main(folder, pub, ctx, intent, objects, packet, intake, z,
                          api, trees, base_commit, case_prefix, ref, ref_pin):
    require(not (Path(pub) / 'NATIVE_MERGE_REQUEST.json').exists(), 'A global main-ref intent already exists; read-only recovery only')
    observed = ref['object']['sha']
    require(observed != intent['main_parent'], 'Cannot abandon unchanged main')
    commit = api('GET', 'git/commits/' + observed)
    cp = response_pin(api, pub)
    ancestry = api('GET', 'compare/' + intent['main_parent'] + '...' + observed)
    ap = response_pin(api, pub)
    require(ancestry.get('status') == 'ahead' and ancestry.get('merge_base_commit', {}).get('sha') == intent['main_parent'],
            'Main advance is not a proven descendant; no rebuild authorized')
    guarded_main_tree(trees, base_commit, commit, packet, case_prefix)
    queue = trees.read(commit['tree']['sha'], QUEUE)
    patch_queue(queue, intake, z)
    require(not (Path(pub) / 'NATIVE_MERGE_REQUEST.json').exists(), 'Main-ref intent appeared; no abandonment/rebuild')
    record = abandonment_spec(folder, pub, ctx, intent, objects, observed, commit,
        ref_pin, cp, ap, trees, queue, datetime.now(timezone.utc).isoformat())
    exclusive_json(folder / 'ABANDONED_BEFORE_MAIN.json', record)
    validate_abandonment(folder, pub, ctx, intent, objects, packet, intake, z,
        api, trees, base_commit, case_prefix)


def load_history(pub, ctx, built, packet, intake, z, progress, api, trees,
                 base_commit, case_prefix):
    history, pending = [], None
    folders = attempt_folders(pub)
    for index, folder in enumerate(folders):
        data = load_attempt(folder, pub, ctx, built, packet, intake, z, progress,
            api, trees, base_commit, case_prefix, history)
        intent, objects, files, row = data
        if (folder / 'ABANDONED_BEFORE_MAIN.json').exists():
            validate_abandonment(folder, pub, ctx, intent, objects, packet, intake, z,
                api, trees, base_commit, case_prefix)
            history.append(dict(attempt_number=int(folder.name),
                object_intent=retained_record_pin(folder / 'OBJECT_INTENT.json', pub),
                objects_built=retained_record_pin(folder / 'OBJECTS_BUILT.json', pub),
                abandonment=retained_record_pin(folder / 'ABANDONED_BEFORE_MAIN.json', pub)))
        else:
            require(index == len(folders) - 1, 'Only the last merge attempt may remain pending')
            pending = (folder, *data)
    return history, pending


def main_ref_spec(pub, ctx, folder, intent, objects):
    return dict(schema='pr209-native-main-ref-intent-v3', expected_main=intent['main_parent'],
        sha=objects['head'], force=False, reviewed_head=intent['reviewed_head'],
        attempt_number=int(folder.name), prior_abandoned_attempts=intent['prior_abandoned_attempts'],
        merge_object_intent=retained_record_pin(folder / 'OBJECT_INTENT.json', pub),
        merge_objects_receipt=retained_record_pin(folder / 'OBJECTS_BUILT.json', pub),
        release_binding=binding(ctx))


def load_merge(pub, ctx, built, packet, intake, z, progress, api, trees, base_commit, case_prefix):
    history, pending = load_history(pub, ctx, built, packet, intake, z, progress,
        api, trees, base_commit, case_prefix)
    require(pending is not None, 'No complete pending merge objects; read-only reconciliation cannot issue a first write')
    folder, intent, objects, files, row = pending
    request = read_record(pub, 'NATIVE_MERGE_REQUEST.json')
    require(request == main_ref_spec(pub, ctx, folder, intent, objects), 'Global once-only main-ref intent differs')
    return intent, objects, files, row


def refresh_completion_native(api, intent, objects, z, t):
    """Observe native completion after all lengthy cross-service/local checks.

    Exact commit identity binds the already verified immutable tree and bodies.
    Current main may legitimately advance to any descendant of this merge.
    These are fresh bounded observations, not a global atomic-snapshot claim.
    """
    pr = current_pr(api, intent['reviewed_head'], expected_pr_metadata(z, t), False, state='closed')
    require(pr.get('merge_commit_sha') == objects['head'], 'Final GitHub merge event differs; completion remains pending')
    actual = api('GET', 'git/commits/' + objects['head'])
    require([x['sha'] for x in actual['parents']] == intent['parents'] and
            actual['tree']['sha'] == objects['tree'], 'Final resulting merge commit/tree/parents differ; completion remains pending')
    current = api('GET', 'git/ref/heads/main')['object']['sha']
    if current != objects['head']:
        ancestry = api('GET', 'compare/' + objects['head'] + '...' + current)
        require(ancestry.get('status') == 'ahead' and
                ancestry.get('merge_base_commit', {}).get('sha') == objects['head'],
                'Final main no longer contains the verified merge; completion remains pending')
    return pr


def canonical_json(value):
    """JSON equality must not coerce True, 1 and 1.0 into the same fact."""
    def native(item):
        require(type(item) in {dict, list, str, int, float, bool, type(None)},
                'Completion evidence contains a non-JSON type')
        if type(item) is dict:
            require(all(type(k) is str for k in item), 'Completion evidence keys must be strings')
            for child in item.values():
                native(child)
        elif type(item) is list:
            for child in item:
                native(child)
    native(value)
    try:
        return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
    except (ValueError, TypeError) as error:
        raise RuntimeError('Completion evidence must be finite canonical JSON') from error


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate completion evidence JSON key')
            result[key] = value
        return result
    def constant(value):
        raise RuntimeError('Nonfinite completion evidence JSON constant: ' + value)
    try:
        result = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeError) as error:
        raise RuntimeError('Invalid completion evidence JSON') from error
    canonical_json(result)
    return result


def exact_json(actual, expected, message):
    require(canonical_json(actual) == canonical_json(expected), message)


def exact_keys(value, keys, message):
    require(type(value) is dict and set(value) == set(keys), message)


def live_evidence_file(case, pub, pin, kind, name, folder=None):
    """Only the retained files actually generated by each live stage qualify."""
    path = retained_pin(case, pin)
    prefix = (Path(pub).relative_to(case) / 'private_transport' / kind).parts
    parts = path.relative_to(case).parts
    require(parts[:len(prefix)] == prefix and len(parts) == len(prefix) + 2 and
            path.name == name, 'Unexpected historical live evidence location')
    require(folder is None or path.parent == folder, 'Historical live evidence spans different observations')
    return path


def validate_live_release_evidence(evidence, r, pub, ctx, z, t, release_utc, completed_utc):
    """Authenticate historical observations locally, without equating new paths/times.

    The retained LIVE_VERIFIED record binds the entire returned observation;
    its individually pinned provider bodies/payloads must still satisfy the
    same publication and tracker semantics. These checks issue no provider call.
    """
    case = Path(r).parent
    exact_keys(evidence, {'publication', 'tracker'}, 'Invalid completion live evidence schema')
    p, q = evidence['publication'], evidence['tracker']
    exact_keys(p, {'utc', 'release_binding', 'publication_receipt_sha256', 'id', 'doi_url',
        'doi_resolution', 'inspect_readback', 'actual_public_file_downloads'}, 'Invalid historical publication schema')
    exact_keys(q, {'utc', 'release_binding', 'publication_receipt_sha256', 'tracker_receipt_sha256',
        'updated_range', 'values', 'evidence'}, 'Invalid historical tracker schema')
    require(max(utc(release_utc), utc(z['utc']), utc(t['utc'])) <= utc(p['utc']) <=
            utc(q['utc']) <= utc(completed_utc), 'Historical completion chronology differs')
    for result in [p, q]:
        exact_json(result['release_binding'], binding(ctx), 'Historical live release binding differs')
        exact_json(result['publication_receipt_sha256'], digest(Path(pub) / 'ZENODO_VERIFIED_PUBLICATION.json'),
                   'Historical publication receipt hash differs')
    exact_json(q['tracker_receipt_sha256'], digest(Path(pub) / 'TRACKER_VERIFIED_APPEND.json'),
               'Historical tracker receipt hash differs')
    exact_json({k: p[k] for k in ['id', 'doi_url']}, {k: z[k] for k in ['id', 'doi_url']},
               'Historical publication identity differs')
    inspect = live_evidence_file(case, pub, p['inspect_readback'], 'zenodo_live', 'INSPECT_READBACK.json')
    folder = inspect.parent
    exact_json(strict_json(checked_path(case, (folder / 'LIVE_VERIFIED.json').relative_to(case).as_posix()).read_bytes()),
               p, 'Historical publication observation differs from retained live record')
    v = strict_json(inspect.read_bytes())
    tool_publication(v, ctx, z['id'])
    exact_json(v['files'], ctx['expected_files'], 'Historical provider file types/bytes differ')
    exact_json({k: v.get(k) for k in ['id', 'doi', 'doi_url', 'record_url']},
               {k: z[k] for k in ['id', 'doi', 'doi_url', 'record_url']}, 'Historical provider DOI/version differs')
    verify_doi(v)
    exact_json(p['doi_resolution'], v['doi_resolution'], 'Historical DOI resolution differs')
    downloads = p['actual_public_file_downloads']
    require(type(downloads) is list and len(downloads) == len(ctx['expected_files']),
            'Historical public downloads incomplete')
    for index, (download, expected) in enumerate(zip(downloads, ctx['expected_files']), 1):
        exact_keys(download, {'file', 'url', 'bytes', 'sha256', 'payload',
            'actual_public_download_byte_hash_match'}, 'Invalid historical download schema')
        payload = live_evidence_file(case, pub, download['payload'], 'zenodo_live', expected['name'], folder)
        exact_json({k: download[k] for k in ['file', 'url', 'bytes', 'sha256', 'actual_public_download_byte_hash_match']},
            dict(file=expected['name'], url=z['record_url'] + '/files/' + expected['name'] + '?download=1',
                bytes=expected['size'], sha256=expected['sha256'], actual_public_download_byte_hash_match=True),
            'Historical public download metadata differs')
        require(payload.stat().st_size == expected['size'] and digest(payload) == expected['sha256'],
                'Historical public payload bytes differ from clearance')
        exact_json(strict_json(checked_path(case, (folder / ('DOWNLOAD_' + str(index) + '.json')).relative_to(case).as_posix()).read_bytes()),
                   download, 'Historical download differs from retained observation')
    exact_json(q['updated_range'], t['updated_range'], 'Historical tracker target differs')
    exact_json(q['values'], t['values'], 'Historical tracker values differ')
    exact_keys(q['evidence'], {'properties', 'target_readback', 'after_scan'}, 'Invalid historical tracker pins schema')
    properties = live_evidence_file(case, pub, q['evidence']['properties'], 'tracker_live', '01-properties-readback.json')
    folder = properties.parent
    exact_json(strict_json(checked_path(case, (folder / 'LIVE_VERIFIED.json').relative_to(case).as_posix()).read_bytes()),
               q, 'Historical tracker observation differs from retained live record')
    meta = strict_json(properties.read_bytes())
    tracker_properties(meta)
    observations = {}
    for key, name, target in [('target_readback', '02-target-readback.json', t['updated_range']),
            ('after_scan', '03-after-readback.json', FULL_RANGE)]:
        path = live_evidence_file(case, pub, q['evidence'][key], 'tracker_live', name, folder)
        record = strict_json(path.read_bytes())
        exact_keys(record, {'request', 'response'}, 'Invalid historical tracker readback schema')
        observations[key] = tracker_readback(record, target, meta)
    exact_json(observations['target_readback'], [t['values']], 'Historical target all-four-cell readback differs')
    require_unique_tracker(observations['after_scan'], t['values'], z, tracker_row_number(t['updated_range']))


def validate_completion_receipt(receipt, expected, r, pub, ctx, z, t, release_utc):
    """All fields are authoritative; only original UTC/live observations vary."""
    exact_keys(receipt, expected, 'Completed merge receipt schema differs')
    historical = {'utc', 'live_release_evidence'}
    exact_json({k: v for k, v in receipt.items() if k not in historical},
               {k: v for k, v in expected.items() if k not in historical}, 'Completed merge receipt static facts differ')
    validate_live_release_evidence(receipt['live_release_evidence'], r, pub, ctx, z, t,
                                   release_utc, receipt['utc'])


def complete_merge(r, pub, ctx, z, t, intent, objects, files, row, progress, api, trees):
    # A successful ref PATCH alone is never a merge or completed case.
    pr = current_pr(api, intent['reviewed_head'], expected_pr_metadata(z, t), False, state='closed')
    require(pr.get('merge_commit_sha') == objects['head'], 'Actual GitHub indirect merge event has not identified this exact merge commit')
    actual = api('GET', 'git/commits/' + objects['head'])
    require([x['sha'] for x in actual['parents']] == intent['parents'] and
            actual['tree']['sha'] == objects['tree'], 'Actual resulting merge commit differs')
    parent = api('GET', 'git/commits/' + intent['main_parent'])
    identities = trees.verify_overlay(parent['tree']['sha'], actual['tree']['sha'], files)
    require(trees.read(actual['tree']['sha'], QUEUE) == files[QUEUE] and
            [x for x in files[QUEUE].decode().splitlines() if '5100015 / AMR-050-0015' in x] == [row], 'Merged target/foreign QUEUE bytes differ')
    current = api('GET', 'git/ref/heads/main')['object']['sha']
    if current != objects['head']:
        ancestry = api('GET', 'compare/' + objects['head'] + '...' + current)
        require(ancestry.get('status') == 'ahead' and
                ancestry.get('merge_base_commit', {}).get('sha') == objects['head'], 'Actual main does not contain the verified merge')
    evidence = live_release(r, pub, ctx, z, t)
    require(progress_baseline(r, pub, ctx, api, trees) == progress, 'Progress baseline changed')
    before = {p: raw for p, raw in files.items() if p != QUEUE}
    object_intent = read_record(pub, 'NATIVE_OBJECT_BUILD_INTENT.json')
    require(expected_native_packet(r, pub, ctx, z, t, object_intent['release_utc']) == before, 'Expected native packet changed at completion')
    receipt = dict(schema='pr209-merged-v2', utc=datetime.now(timezone.utc).isoformat(),
        PR=209, url=pr['html_url'], merged=True, merge_commit=objects['head'],
        merge_parents=intent['parents'], verified_merge_tree=objects['tree'],
        reviewed_head=intent['reviewed_head'], doi_url=z['doi_url'], tracker_range=t['updated_range'],
        merge_attempt_number=intent['attempt_number'], prior_abandoned_attempts=intent['prior_abandoned_attempts'],
        actual_publication_tracker_native_merge_complete=True,
        exact_native_body_readbacks=identities, exact_queue_row=row,
        foreign_fresh_main_tree_and_rows_preserved=True,
        case_completion_percent=100, program_count_scope='own_descending_shard',
        program_counts=progress['completed_counts'], progress_baseline=progress,
        full_goal_active_incomplete=True, release_binding=binding(ctx),
        merge_intent_sha256=digest(Path(pub) / 'NATIVE_MERGE_REQUEST.json'),
        live_release_evidence=evidence, local_Git_index_ref_mutations=0)
    old = None
    if (Path(pub) / 'PR_MERGED.json').exists():
        old = strict_json(safe_read(pub, 'PR_MERGED.json'))
    validate_completion_receipt(receipt if old is None else old, receipt,
                                r, pub, ctx, z, t, object_intent['release_utc'])
    # Downloads, tracker scans, baseline authentication and packet derivation
    # above can take minutes. Their success must not promote earlier native
    # observations. Refresh after even the existing-receipt comparison so both
    # creation and read-only acceptance require current native facts.
    final_pr = refresh_completion_native(api, intent, objects, z, t)
    require(final_pr['html_url'] == receipt['url'], 'Final canonical PR URL differs; completion remains pending')
    if old is not None:
        return old
    receipt['utc'] = datetime.now(timezone.utc).isoformat()
    receipt['url'] = final_pr['html_url']
    exclusive_json(Path(pub) / 'PR_MERGED.json', receipt)
    return receipt


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(argv in [[], ['--reconcile'], ['--resume-before-main']], 'Use --reconcile or --resume-before-main')
    reconcile = argv == ['--reconcile']
    resume = argv == ['--resume-before-main']
    with acquire(PUB):
        ctx = context(R)
        z, t = publication(R, PUB, ctx), tracker(R, PUB, ctx)
        if resume:
            require(not (PUB / 'NATIVE_MERGE_REQUEST.json').exists() and not (PUB / 'PR_MERGED.json').exists(),
                    'A global main-ref request was already created; read-only --reconcile only')
            require((PUB / 'NATIVE_READY_ATTEMPT.json').exists() and attempt_folders(PUB),
                    'No prior complete merge-object attempt to resume')
        elif not reconcile:
            require(not any((PUB / n).exists() for n in ['NATIVE_READY_ATTEMPT.json',
                'NATIVE_MERGE_OBJECT_INTENT.json', 'NATIVE_MERGE_OBJECTS_BUILT.json',
                'NATIVE_MERGE_REQUEST.json', 'PR_MERGED.json']) and not attempt_folders(PUB),
                'Prior ready/merge attempt exists; --resume-before-main or read-only --reconcile required')
        api = NativeAPI(PUB, 'native_merge', readonly=reconcile)
        trees = NativeTrees(api)
        intent, built, packet, row = prepared_authority(R, PUB, ctx, z, t, api, trees)
        prepared_sha = digest(PUB / 'PR_PREPARED.json')
        progress = progress_baseline(R, PUB, ctx, api, trees)
        intake = json.loads(safe_read(PUB.parent, 'initial_review_20261016/INTAKE.json'))
        base_commit = api('GET', 'git/commits/' + intent['main_parent'])
        case_prefix = PUB.parent.relative_to(ROOT).as_posix() + '/'
        if not reconcile:
            metadata = expected_pr_metadata(z, t)
            pr = current_pr(api, built['head'], metadata, False if resume else None)
            require(pr.get('mergeable') is True, 'Conflict or unknown PR mergeability; reconcile')
            live_release(R, PUB, ctx, z, t)
            fresh_main(api, trees, base_commit, packet, intake, z, case_prefix)
            if not resume:
                pr = current_pr(api, built['head'], metadata)
                require(pr.get('mergeable') is True, 'PR changed before ready intent')
                exclusive_json(PUB / 'NATIVE_READY_ATTEMPT.json', dict(schema='pr209-ready-intent-v2',
                    head=built['head'], pr_metadata=metadata, prepared_receipt_sha256=prepared_sha,
                    was_draft=pr['draft'], operation='mark_ready' if pr['draft'] else 'observed_already_ready',
                    release_binding=binding(ctx)))
                if pr['draft']:
                    result = api('POST', 'graphql', dict(query='mutation($id: ID!) { markPullRequestReadyForReview(input:{pullRequestId:$id}) { pullRequest { id isDraft } } }',
                        variables={'id': pr['node_id']}), graphql=True)
                    require(not result.get('errors') and result['data']['markPullRequestReadyForReview']['pullRequest']['isDraft'] is False, 'Ready outcome failed/unknown; reconcile read-only')
            current_pr(api, built['head'], metadata, False)
            live_release(R, PUB, ctx, z, t)
            no_active_rules(api, 'main')
            require(digest(PUB / 'PR_PREPARED.json') == prepared_sha, 'Prepared receipt changed')
            history, pending = load_history(PUB, ctx, built, packet, intake, z, progress,
                api, trees, base_commit, case_prefix)
            if pending is not None:
                require(resume, 'Pending objects require explicit --resume-before-main')
                folder, merge_intent, objects, files, row = pending
                actual_ref = api('GET', 'git/ref/heads/main')
                rp = response_pin(api, PUB)
                if actual_ref['object']['sha'] != merge_intent['main_parent']:
                    abandon_advanced_main(folder, PUB, ctx, merge_intent, objects, packet, intake, z,
                        api, trees, base_commit, case_prefix, actual_ref, rp)
                    history, pending = load_history(PUB, ctx, built, packet, intake, z, progress,
                        api, trees, base_commit, case_prefix)
            if pending is None:
                # A new object attempt is allowed only after every predecessor
                # has independently revalidated terminal abandonment evidence.
                require(not (PUB / 'NATIVE_MERGE_REQUEST.json').exists(), 'Global main-ref intent forbids another build')
                main_head, mc, files, row = fresh_main(api, trees, base_commit, packet, intake, z, case_prefix)
                require(expected_native_packet(R, PUB, ctx, z, t, intent['release_utc']) == {p: b for p, b in files.items() if p != QUEUE}, 'Packet changed before merge object build')
                number = len(history) + 1
                folder = PUB / 'private_transport/native_merge_attempts' / f'{number:04d}'
                durable_mkdir(folder, exist_ok=False)
                merge_intent = merge_spec(PUB, ctx, built['head'], main_head, mc['tree']['sha'],
                    files, row, progress, number, history)
                exclusive_json(folder / 'OBJECT_INTENT.json', merge_intent)
                tree = upload_overlay(api, mc['tree']['sha'], files)
                merge_head = api('POST', 'git/commits', dict(message='Merge PR #209: audited outer center-pedal publication',
                    tree=tree, parents=[main_head, built['head']]))['sha']
                commit = api('GET', 'git/commits/' + merge_head)
                require(commit['tree']['sha'] == tree and [x['sha'] for x in commit['parents']] == [main_head, built['head']], 'Created merge object differs')
                trees.verify_overlay(mc['tree']['sha'], tree, files)
                objects = dict(schema='pr209-native-merge-objects-built-v2', head=merge_head, tree=tree,
                    parents=[main_head, built['head']], merge_object_intent_sha256=digest(folder / 'OBJECT_INTENT.json'))
                exclusive_json(folder / 'OBJECTS_BUILT.json', objects)
            else:
                # A known complete object set whose exact base still is main
                # may finish its first ref request; no object write is repeated.
                folder, merge_intent, objects, files, row = pending
            main_head, merge_head = merge_intent['main_parent'], objects['head']
            pr = current_pr(api, built['head'], metadata, False)
            require(pr.get('mergeable') is True, 'PR mergeability changed')
            live_release(R, PUB, ctx, z, t)
            require(digest(PUB / 'PR_PREPARED.json') == prepared_sha and
                    expected_native_packet(R, PUB, ctx, z, t, intent['release_utc']) == {p: b for p, b in files.items() if p != QUEUE}, 'Release/preparation changed before main update')
            no_active_rules(api, 'main')
            pr = current_pr(api, built['head'], metadata, False)
            require(pr.get('mergeable') is True, 'PR changed after public/rules readbacks')
            actual_ref = api('GET', 'git/ref/heads/main')
            rp = response_pin(api, PUB)
            if actual_ref['object']['sha'] != main_head:
                abandon_advanced_main(folder, PUB, ctx, merge_intent, objects, packet, intake, z,
                    api, trees, base_commit, case_prefix, actual_ref, rp)
                raise RuntimeError('Proven foreign main advance; attempt terminally abandoned before any main-ref request. Use --resume-before-main')
            exclusive_json(PUB / 'NATIVE_MERGE_REQUEST.json', main_ref_spec(PUB, ctx, folder, merge_intent, objects))
            api('PATCH', 'git/refs/heads/main', dict(sha=merge_head, force=False))
        merge_intent, objects, files, row = load_merge(PUB, ctx, built, packet, intake, z, progress,
            api, trees, base_commit, case_prefix)
        receipt = complete_merge(R, PUB, ctx, z, t, merge_intent, objects, files, row, progress, api, trees)
        print(json.dumps({k: v for k, v in receipt.items() if k != 'exact_native_body_readbacks'}, indent=2))


if __name__ == '__main__':
    main()
