#!/usr/bin/env python3
"""NEW exact MAIN findings object/GET/empty-remote-proof/CAS source proposal.

No execution occurred in preparation. Each explicit stage requires a NEW Root
promotion pinning the final frozen selection and independent whole reviews.
No PR mutation, canonical target/QUEUE write, release, DOI, or GWS operation.
"""
from pathlib import Path
import hashlib, os, stat, sys, types
sys.dont_write_bytecode = True
COMMON_SHA = 'fa1f5d4611e75a53848d56afccdfd1cd7582eaa912e1e882ffa9e5d92f1c5b5e'
helper = Path(__file__).absolute().parent / 'checkpoint_common.py'
for component in reversed([helper, *helper.parents]):
    if os.path.lexists(component):
        if stat.S_ISLNK(component.lstat().st_mode): raise RuntimeError('Source symlink rejected')
if os.path.lexists(helper.parent / '__pycache__'): raise RuntimeError('Source cache rejected')
common_body = helper.read_bytes()
if hashlib.sha256(common_body).hexdigest() != COMMON_SHA: raise RuntimeError('Exact helper pin differs')
common = types.ModuleType('sealed_checkpoint_common'); common.__file__ = str(helper)
exec(compile(common_body, str(helper), 'exec'), common.__dict__)
globals().update({k: v for k, v in common.__dict__.items() if not k.startswith('__')})

BUILD = CHECKPOINT / 'private_candidate_v04'
EXECUTION = CHECKPOINT / 'actual_execution_v04'
BUILD_NAMES = {'proof': 'PROOF.json', 'raw_commit': 'COMMIT.raw', 'trees': 'TREE_OBJECTS.json',
               'blobs': 'BLOB_PAYLOADS.json', 'tree_payload': 'TREE_PAYLOAD.json',
               'commit_payload': 'COMMIT_PAYLOAD.json', 'full_rows': 'CANDIDATE_FULL_ROWS.nul.gz',
               'validation': 'SOURCE_INPUT_VALIDATION.json', 'completion': 'STAGE_COMPLETED.json'}

def candidate_gate():
    selection, promotion, bodies, inputs, certificate, context = freeze_gate('execute', Path(__file__).absolute())
    current_commit,current_tree=certificate['current_commit'],certificate['current_tree']
    require(set(promotion['candidate_artifacts']) == set(BUILD_NAMES), 'Whole prepared artifact closure missing')
    artifacts = {}
    for role, name in BUILD_NAMES.items():
        pin = promotion['candidate_artifacts'][role]
        require(Path(pin['path']) == BUILD / name, 'Unexpected private artifact alias')
        artifacts[role] = file_pin(pin, base=BUILD)
    proof = json.loads(artifacts['proof'])
    require(proof['schema'] == 'pr262-new-main-findings-private-proof-v4' and proof['source_version']==SOURCE_VERSION and proof['baseline'] == current_commit and
            proof['before_tree'] == current_tree and proof['sole_parent'] == current_commit and
            proof['selection_sha256'] == promotion['selection_sha256'], 'Candidate proof baseline differs')
    require(proof['selected_count'] == selection['selected_count'] and
            proof['baseline_leaf_count'] == certificate['current_counts']['leaves'] and
            proof['baseline_directory_count'] == certificate['current_counts']['directories'] and
            proof['baseline_certificate_sha256']==selection['current_baseline_certificate_sha256'] and
            proof['baseline_counts']==certificate_counts(certificate,context['protected_paths']) and
            proof['peer76_all_unselected_modes_paths_oids_preserved'] is True and
            proof['all_current_foreign_entries_preserved'] is True and proof['all_protected_leaf_paths_preserved'] is True and
            proof['all_unselected_main_leaves_preserved'] is True and
            proof['all_unrewritten_main_directories_preserved'] is True, 'Whole preservation proof differs')
    for role, key in [('trees', 'tree_objects_sha256'), ('blobs', 'blob_payloads_sha256'),
                      ('tree_payload', 'tree_payload_sha256'), ('commit_payload', 'commit_payload_sha256')]:
        require(sha(artifacts[role]) == proof[key], 'Prepared artifact digest differs')
    raw = artifacts['raw_commit']; tree, parents, message = commit_header(raw)
    require(oid('commit', raw) == proof['candidate_commit'] and tree == proof['candidate_tree'] and parents == [current_commit] and
            len(raw) == proof['raw_commit_bytes'] and sha(raw) == proof['raw_commit_sha256'], 'Exact raw candidate differs')
    cp = json.loads(artifacts['commit_payload'])
    expected_cp = {'tree': tree, 'parents': [current_commit], 'message': selection['commit_message'],
                   'author': dict(ACTOR, date=selection['commit_date_utc']),
                   'committer': dict(ACTOR, date=selection['commit_date_utc'])}
    require(cp == expected_cp and message == selection['commit_message'].encode(), 'Prepared metadata/date/message differs')
    actor_header = b'Alec Kriebel <me@aleckriebel.com> ' + str(selection['commit_unix_seconds']).encode() + b' +0000'
    expected_raw = b'tree ' + tree.encode() + b'\nparent ' + current_commit.encode() + b'\nauthor ' + actor_header + b'\ncommitter ' + actor_header + b'\n\n' + selection['commit_message'].encode()
    require(raw == expected_raw, 'Complete raw actor/date/header bytes differ')
    rows = parse_census(gzip.decompress(artifacts['full_rows']))
    require(sha(census(rows)) == proof['after_full_raw_census_sha256'] and
            sum(v[0] != b'40000' for v in rows.values()) == proof['candidate_leaf_count'] and
            sum(v[0] == b'40000' for v in rows.values()) == proof['candidate_directory_count'], 'Candidate whole census differs')
    blobs = json.loads(artifacts['blobs']); trees = json.loads(artifacts['trees'])
    require(len(blobs) == len(bodies) and len(trees) == proof['rewritten_ancestor_count'], 'Prepared object closure count differs')
    for row, (name, value) in zip(blobs, bodies.items()):
        require(row == {'path': name.decode(), 'oid': value[1], 'payload':
                        {'content': base64.b64encode(value[2]).decode(), 'encoding': 'base64'}}, 'Prepared full blob differs')
    expected_tree_payload = {'base_tree': current_tree, 'tree': [{'path': name.decode(), 'mode': value[0].decode(),
                             'type': 'blob', 'sha': value[1]} for name, value in bodies.items()]}
    require(json.loads(artifacts['tree_payload']) == expected_tree_payload, 'Tree payload changes an unselected path/mode/body')
    before_rows = parse_census(gzip.decompress(inputs['main_full_rows']))
    require(sha(census(before_rows)) == proof['before_full_raw_census_sha256'] and
            sum(v[0] != b'40000' for v in before_rows.values()) == certificate['current_counts']['leaves'] and
            sum(v[0] == b'40000' for v in before_rows.values()) == certificate['current_counts']['directories'], 'Whole baseline census differs')
    require({p:v for p,v in rows.items() if v[0] != b'40000' and p not in bodies} ==
            {p:v for p,v in before_rows.items() if v[0] != b'40000' and p not in bodies}, 'Candidate changes unselected leaves')
    require(all(rows.get(p) == value[:2] for p,value in bodies.items()), 'Candidate selected path/mode/body census differs')
    context=validate_baseline_context(selection,inputs,set(bodies),certificate)
    require(all(rows.get(p)==before_rows.get(p) for p in context['protected_paths']), 'Protected current identities/absences changed')
    foreign_current_entries_preserved(before_rows,rows,context['foreign_all_paths'],set(bodies))
    rewritten_paths={base64.b64decode(v['directory_b64']) for v in trees}
    require({p:v for p,v in rows.items() if v[0]==b'40000' and p not in rewritten_paths}==
            {p:v for p,v in before_rows.items() if v[0]==b'40000' and p not in rewritten_paths}, 'Unrewritten directories changed')
    require(proof['foreign_delta_literal_paths_sha256']==sha(dump(selection['foreign_delta_literal_paths'])) and
            proof['foreign_delta_record_sha256']==sha(inputs['foreign_delta']), 'Foreign proof ledger binding differs')
    distinct_raw_trees = validate_changed_tree_records(trees, before_rows, rows, tree, current_tree)
    require(proof['distinct_rewritten_tree_object_count'] == len(distinct_raw_trees), 'Distinct raw tree count differs')
    require(any(v['after'] == tree and v['directory_b64'] == '' for v in trees), 'Full root rewrite omitted')
    review_closure(promotion['candidate_review'], 'GO_NEW_MAIN_FINDINGS_EXACT_CANDIDATE_V04_ONLY',
        {'selection_sha256': promotion['selection_sha256'], 'proof_sha256': sha(artifacts['proof']),
         'candidate_commit': proof['candidate_commit'], 'candidate_tree': tree, 'sole_parent': current_commit,
         'selected_count': len(bodies), 'complete_all_current_baseline_leaves_and_directories_checked': True,
         'source_version':SOURCE_VERSION,'all_protected_leaf_paths_and_current_foreign_entries_checked':True,
         'baseline_certificate_sha256':selection['current_baseline_certificate_sha256'], 'baseline_counts':certificate_counts(certificate,context['protected_paths'])})
    return selection, promotion, bodies, proof, artifacts, blobs, trees

def verify_commit_metadata(value, proof, payload):
    require(value['sha'] == proof['candidate_commit'] and value['tree']['sha'] == proof['candidate_tree'] and
            [v['sha'] for v in value['parents']] == [proof['sole_parent']], 'Actual candidate metadata identity differs')
    require(value['message'] in (payload['message'], payload['message'].removesuffix('\n')), 'API message differs')
    for role in ('author', 'committer'):
        require(all(value[role][k] == payload[role][k] for k in ('name', 'email', 'date')), 'Actual metadata actor/date differs')

def objects():
    selection, promotion, bodies, proof, artifacts, blobs, trees = candidate_gate()
    outputs = ['BEGIN.json', 'OBJECT_CREATION_ACCEPTANCE.json', 'STAGE_COMPLETED.json']
    for name in ('MAIN_BEFORE', 'PR_BEFORE'): outputs += api_outputs(name)
    for i, row in enumerate(blobs): outputs += api_outputs('BLOB_' + str(i), write=True)
    for name in ('TREE_CREATE', 'COMMIT_CREATE'): outputs += api_outputs(name, write=True)
    stage = Stage(EXECUTION / 'objects', outputs)
    stage.json('BEGIN.json', {'UTC': utc(), 'whole_future_output_count': len(outputs),
               'whole_preflight_before_first_GET_POST_Git_or_ref_dispatch': True, 'automatic_retry_prohibited': True})
    fresh_main(selection, stage, 'MAIN_BEFORE', proof['sole_parent']); fresh_pr(selection, stage, 'PR_BEFORE')
    for i, row in enumerate(blobs):
        value = api(selection, stage, 'POST', 'repos/' + REPO + '/git/blobs', 'BLOB_' + str(i), dump(row['payload']))
        require(value['sha'] == row['oid'], 'Created blob OID differs; no retry')
    value = api(selection, stage, 'POST', 'repos/' + REPO + '/git/trees', 'TREE_CREATE', artifacts['tree_payload'])
    require(value['sha'] == proof['candidate_tree'], 'Created full tree differs; no retry')
    value = api(selection, stage, 'POST', 'repos/' + REPO + '/git/commits', 'COMMIT_CREATE', artifacts['commit_payload'])
    verify_commit_metadata(value, proof, json.loads(artifacts['commit_payload']))
    stage.json('OBJECT_CREATION_ACCEPTANCE.json', {'schema': 'pr262-main-findings-created-objects-v4', 'UTC': utc(),
               'source_version':SOURCE_VERSION,'selection_sha256':proof['selection_sha256'],
               'baseline_certificate_sha256':proof['baseline_certificate_sha256'],
               'candidate_commit': proof['candidate_commit'], 'candidate_tree': proof['candidate_tree'], 'sole_parent': proof['sole_parent'],
               'selected_blob_POSTs': len(blobs), 'tree_POSTs': 1, 'commit_POSTs': 1, 'ref_updates': 0,
               'full_GET_and_empty_independent_remote_proof_pending': True})
    stage.finish()
    print('Actual checkpoint objects created. Reference update remains pending.')

def saved(root, name):
    return literal(root / name, base=CHECKPOINT, kind='file').read_bytes()

def validate_stage_binding(value, proof, schema):
    require(value['schema']==schema and value['source_version']==SOURCE_VERSION and
            value['selection_sha256']==proof['selection_sha256'] and
            value['baseline_certificate_sha256']==proof['baseline_certificate_sha256'],
            'Actual stage source/selection/certificate binding differs')

def accept_object_stage(proof, count):
    root = EXECUTION / 'objects'
    require(json.loads(saved(root, 'STAGE_COMPLETED.json'))['automatic_retry_prohibited'] is True, 'Objects stage incomplete')
    value = json.loads(saved(root, 'OBJECT_CREATION_ACCEPTANCE.json'))
    validate_stage_binding(value,proof,'pr262-main-findings-created-objects-v4')
    require(value['schema'] == 'pr262-main-findings-created-objects-v4' and
            value['candidate_commit'] == proof['candidate_commit'] and value['candidate_tree'] == proof['candidate_tree'] and
            value['sole_parent'] == proof['sole_parent'] and value['selected_blob_POSTs'] == count and value['tree_POSTs'] == 1 and
            value['commit_POSTs'] == 1 and value['ref_updates'] == 0, 'Actual object acceptance differs')

def empty_remote_readback(selection, stage, proof, artifacts):
    """Full raw commit AND recursive tree census from a provably empty own store.

    A fresh exact reader module gets independent context; no global save/restore
    tuple and no original-payload-map alias can corrupt cleanup or its proof.
    """
    driver = stage.root / 'remote.git'; objects_dir = stage.root / 'remote_objects'
    templates = stage.root / 'templates'
    for path in (driver, objects_dir, templates):
        literal(path, base=stage.root, kind='directory'); require(not list(path.iterdir()), 'Independent store/template not empty')
    stage.json('EMPTY_STORE_BEFORE_INIT.json', {'remote_driver': str(driver), 'object_store': str(objects_dir),
               'all_empty_before_init': True, 'no_prepared_alternates_or_candidate_object_cache': True})
    env = clean_env(objects_dir); git_exe = selection['tools']['git']['path']
    run_capture(selection, stage, 'REMOTE_INIT', [git_exe, '--no-replace-objects', '-c', 'core.hooksPath=/dev/null',
        'init', '--bare', '--initial-branch=main', '--template=' + str(templates), str(driver)], env)
    run_capture(selection, stage, 'REMOTE_FETCH', [git_exe, '--no-replace-objects', '-c', 'core.hooksPath=/dev/null',
        '--git-dir', str(driver), 'fetch', '--no-tags', '--no-write-fetch-head', '--depth=1', '--filter=blob:none',
        URL, proof['candidate_commit']], env)
    # blob:none retains every raw tree. Lazy fetching is disabled; every selected
    # full blob has a separate complete GET; no tree:0/recursive API shortcut.
    module, reader = owned_reader(selection, driver, objects_dir, stage.root)
    try:
        kind, raw_commit = reader.get(proof['candidate_commit'])
        require(kind == 'commit' and raw_commit == artifacts['raw_commit'], 'Empty remote full raw commit differs')
        tree, parents, _ = commit_header(raw_commit)
        require(tree == proof['candidate_tree'] and parents == [proof['sole_parent']], 'Remote raw parent/root differs')
        rows = reader.walk(tree)
        require(census(rows) == gzip.decompress(artifacts['full_rows']), 'Empty remote whole raw census differs')
        require(sha(census(rows)) == proof['after_full_raw_census_sha256'] and
                sum(v[0] != b'40000' for v in rows.values()) == proof['candidate_leaf_count'] and
                sum(v[0] == b'40000' for v in rows.values()) == proof['candidate_directory_count'], 'Remote counts differ')
        stage.write('REMOTE_COMMIT.raw', raw_commit)
        stage.write('REMOTE_FULL_ROWS.nul.gz', gzip.compress(census(rows), mtime=0))
        stage.json('REMOTE_PROOF.json', {'candidate_commit': proof['candidate_commit'], 'candidate_tree': tree,
                   'sole_parent': proof['sole_parent'], 'raw_commit_sha256': sha(raw_commit),
                   'full_raw_census_sha256': sha(census(rows)), 'leaf_count': proof['candidate_leaf_count'],
                   'directory_count': proof['candidate_directory_count'], 'every_tree_raw_hash_checked': True,
                   'no_alternates_lazy_fetch_replacements_or_prepared_cache': True})
    finally:
        reader.close()

def readback_outputs(blobs, trees):
    outputs = ['BEGIN.json', 'EMPTY_STORE_BEFORE_INIT.json', 'REMOTE_INIT.stdout', 'REMOTE_INIT.stderr',
               'REMOTE_FETCH.stdout', 'REMOTE_FETCH.stderr', 'REMOTE_COMMIT.raw', 'REMOTE_FULL_ROWS.nul.gz',
               'REMOTE_PROOF.json', 'FULL_READBACK_ACCEPTANCE.json', 'STAGE_COMPLETED.json']
    for i, row in enumerate(blobs): outputs += api_outputs('BLOB_GET_' + str(i))
    for i, row in enumerate(trees): outputs += api_outputs('TREE_GET_' + str(i))
    for name in ('COMMIT_GET', 'MAIN_BEFORE', 'PR_BEFORE'): outputs += api_outputs(name)
    return outputs

def readback():
    selection, promotion, bodies, proof, artifacts, blobs, trees = candidate_gate()
    accept_object_stage(proof, len(blobs))
    outputs = readback_outputs(blobs, trees)
    stage = Stage(EXECUTION / 'readback', outputs, ['remote.git', 'remote_objects', 'templates'])
    stage.json('BEGIN.json', {'UTC': utc(), 'whole_future_output_count': len(outputs),
               'whole_preflight_before_first_GET_or_Git_dispatch': True, 'automatic_retry_prohibited': True})
    fresh_main(selection, stage, 'MAIN_BEFORE', proof['sole_parent']); fresh_pr(selection, stage, 'PR_BEFORE')
    for i, row in enumerate(blobs):
        value = api(selection, stage, 'GET', 'repos/' + REPO + '/git/blobs/' + row['oid'], 'BLOB_GET_' + str(i))
        require(value['sha'] == row['oid'] and value['encoding'] == 'base64', 'Full GET blob identity differs')
        body = base64.b64decode(value['content'], validate=False)
        frozen = bodies[row['path'].encode()][2]
        require(len(body) == value['size'] == len(frozen) and body == frozen and oid('blob', body) == row['oid'], 'Full GET bytes differ')
    for i, row in enumerate(trees):
        value = api(selection, stage, 'GET', 'repos/' + REPO + '/git/trees/' + row['after'], 'TREE_GET_' + str(i))
        body = provider_tree_raw(value)
        require(value['sha'] == row['after'] and oid('tree', body) == row['after'] and
                body == base64.b64decode(row['body_base64'], validate=True), 'Full nonrecursive ancestor GET differs')
    value = api(selection, stage, 'GET', 'repos/' + REPO + '/git/commits/' + proof['candidate_commit'], 'COMMIT_GET')
    verify_commit_metadata(value, proof, json.loads(artifacts['commit_payload']))
    empty_remote_readback(selection, stage, proof, artifacts)
    stage.json('FULL_READBACK_ACCEPTANCE.json', {'schema': 'pr262-main-findings-full-readback-v4', 'UTC': utc(),
               'source_version':SOURCE_VERSION,'selection_sha256':proof['selection_sha256'],
               'candidate_commit': proof['candidate_commit'], 'candidate_tree': proof['candidate_tree'], 'sole_parent': proof['sole_parent'],
               'selected_full_provider_bodies': len(blobs), 'complete_nonrecursive_rewritten_trees': len(trees),
               'independent_empty_remote_full_raw_commit_and_whole_census_verified': True,
               'all_certified_current_entries_and_protected_paths_accounted_for': True,
               'baseline_certificate_sha256':proof['baseline_certificate_sha256'],
               'ref_updates': 0})
    stage.finish()
    print('All full selected bodies, full changed trees, empty remote raw commit and census verified before CAS.')

def revalidate_readback(proof, artifacts, blobs, trees, bodies):
    root = EXECUTION / 'readback'
    require(json.loads(saved(root, 'STAGE_COMPLETED.json'))['automatic_retry_prohibited'] is True, 'Readback stage incomplete')
    value = json.loads(saved(root, 'FULL_READBACK_ACCEPTANCE.json'))
    validate_stage_binding(value,proof,'pr262-main-findings-full-readback-v4')
    require(value['schema'] == 'pr262-main-findings-full-readback-v4' and
            value['candidate_commit'] == proof['candidate_commit'] and value['candidate_tree'] == proof['candidate_tree'] and
            value['sole_parent'] == proof['sole_parent'] and value['selected_full_provider_bodies'] == len(blobs) and
            value['complete_nonrecursive_rewritten_trees'] == len(trees) and value['ref_updates'] == 0 and
            value['independent_empty_remote_full_raw_commit_and_whole_census_verified'] is True,
            'Full readback acceptance differs')
    for i, row in enumerate(blobs):
        value = json.loads(saved(root, 'BLOB_GET_' + str(i) + '.stdout'))
        body = base64.b64decode(value['content'], validate=False)
        require(value['sha'] == row['oid'] and value['encoding'] == 'base64' and len(body) == value['size'] and
                body == bodies[row['path'].encode()][2] and oid('blob', body) == row['oid'], 'Saved full blob receipt differs')
    for i, row in enumerate(trees):
        value = json.loads(saved(root, 'TREE_GET_' + str(i) + '.stdout')); body = provider_tree_raw(value)
        require(value['sha'] == row['after'] and body == base64.b64decode(row['body_base64'], validate=True) and
                oid('tree', body) == row['after'], 'Saved raw tree receipt differs')
    verify_commit_metadata(json.loads(saved(root, 'COMMIT_GET.stdout')), proof, json.loads(artifacts['commit_payload']))
    require(saved(root, 'REMOTE_COMMIT.raw') == artifacts['raw_commit'] and
            gzip.decompress(saved(root, 'REMOTE_FULL_ROWS.nul.gz')) == gzip.decompress(artifacts['full_rows']),
            'Saved independent full raw proof differs')
    empty = json.loads(saved(root, 'EMPTY_STORE_BEFORE_INIT.json'))
    require(empty['all_empty_before_init'] is True and empty['no_prepared_alternates_or_candidate_object_cache'] is True, 'Empty origin proof missing')
    remote = json.loads(saved(root, 'REMOTE_PROOF.json'))
    require(remote['candidate_commit'] == proof['candidate_commit'] and remote['candidate_tree'] == proof['candidate_tree'] and
            remote['sole_parent'] == proof['sole_parent'] and remote['raw_commit_sha256'] == proof['raw_commit_sha256'] and
            remote['full_raw_census_sha256'] == proof['after_full_raw_census_sha256'] and
            remote['every_tree_raw_hash_checked'] is True and remote['no_alternates_lazy_fetch_replacements_or_prepared_cache'] is True,
            'Independent remote proof differs')

def cas():
    selection, promotion, bodies, proof, artifacts, blobs, trees = candidate_gate()
    accept_object_stage(proof, len(blobs)); revalidate_readback(proof, artifacts, blobs, trees, bodies)
    root_pin = promotion['actual_readback_acceptance']
    require(Path(root_pin['path']) == CHECKPOINT / 'ROOT_PRECAS_ACTUAL_READBACK_ACCEPTANCE_V04.json', 'Root actual acceptance alias differs')
    root_acceptance = json.loads(file_pin(root_pin, base=CHECKPOINT))
    require(root_acceptance['schema'] == 'pr262-root-full-actual-readback-acceptance-v4' and root_acceptance['source_version']==SOURCE_VERSION and
            root_acceptance['root_full_actual_readback_read_and_fresh_rehash'] is True and
            root_acceptance['no_unknown_outcomes'] is True and
            root_acceptance['candidate_commit'] == proof['candidate_commit'] and
            root_acceptance['candidate_tree'] == proof['candidate_tree'] and
            root_acceptance['proof_sha256'] == sha(artifacts['proof']) and
            root_acceptance['baseline_certificate_sha256']==proof['baseline_certificate_sha256'], 'Root whole actual readback acceptance missing')
    receipt_rows = root_acceptance['files']
    require(len(receipt_rows) == len(readback_outputs(blobs, trees)) and
            {v['path'] for v in receipt_rows} == {str(EXECUTION / 'readback' / n) for n in readback_outputs(blobs, trees)},
            'Root actual acceptance omits a complete readback capture')
    for row in receipt_rows: file_pin(row, base=EXECUTION / 'readback')
    payload = {'query': 'mutation ScopedResearchCheckpoint($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}',
               'variables': {'input': {'repositoryId': 'R_kgDOTfIvPw', 'refUpdates': [{'name': 'refs/heads/main',
               'beforeOid': proof['sole_parent'], 'afterOid': proof['candidate_commit'], 'force': False}]}}}
    require(promotion['exact_MAIN_CAS_payload_sha256'] == sha(dump(payload)), 'Root exact one-update/nonforce CAS pin differs')
    outputs = ['BEGIN.json', 'CAS_PAYLOAD.json', 'ROOT_ACTUAL_MAIN_FINDINGS_ACCEPTANCE.json', 'STAGE_COMPLETED.json']
    for name in ('MAIN_BEFORE', 'PR_BEFORE', 'MAIN_AFTER', 'COMMIT_AFTER', 'ROOT_AFTER', 'PR_AFTER'): outputs += api_outputs(name)
    outputs += api_outputs('MAIN_CAS', write=True)
    stage = Stage(EXECUTION / 'cas', outputs)
    stage.json('BEGIN.json', {'UTC': utc(), 'whole_future_output_count': len(outputs),
               'whole_preflight_before_first_GET_POST_or_ref_dispatch': True, 'automatic_retry_prohibited': True})
    stage.json('CAS_PAYLOAD.json', payload)
    fresh_main(selection, stage, 'MAIN_BEFORE', proof['sole_parent']); fresh_pr(selection, stage, 'PR_BEFORE')
    value = api(selection, stage, 'POST', 'graphql', 'MAIN_CAS', dump(payload))
    require(value.get('data', {}).get('updateRefs') is not None and not value.get('errors'), 'CAS failed/unknown; never retry')
    fresh_main(selection, stage, 'MAIN_AFTER', proof['candidate_commit'])
    value = api(selection, stage, 'GET', 'repos/' + REPO + '/git/commits/' + proof['candidate_commit'], 'COMMIT_AFTER')
    verify_commit_metadata(value, proof, json.loads(artifacts['commit_payload']))
    value = api(selection, stage, 'GET', 'repos/' + REPO + '/git/trees/' + proof['candidate_tree'], 'ROOT_AFTER')
    expected_root = next(v for v in trees if v['directory_b64'] == '')
    require(value['sha'] == proof['candidate_tree'] and provider_tree_raw(value) ==
            base64.b64decode(expected_root['body_base64'], validate=True), 'Actual MAIN raw root differs')
    fresh_pr(selection, stage, 'PR_AFTER')
    stage.json('ROOT_ACTUAL_MAIN_FINDINGS_ACCEPTANCE.json', {'schema': 'pr262-root-actual-main-findings-acceptance-v4',
               'UTC': utc(),'source_version':SOURCE_VERSION,'selection_sha256':proof['selection_sha256'],
               'baseline_certificate_sha256':proof['baseline_certificate_sha256'], 'actual_MAIN': proof['candidate_commit'], 'actual_tree': proof['candidate_tree'], 'sole_parent': proof['sole_parent'],
               'exact_one_expected_old_graphql_MAIN_ref_update_force_false': True,
               'full_body_ancestor_GET_and_empty_independent_raw_commit_census_proof_preceded_CAS': True,
               'PR_OPEN_DRAFT_unmerged_unclosed': True, 'PR_metadata_writes': 0, 'Zenodo_DOI_GWS_actions': 0,
               'primary_git_access': 0, 'selected_count': len(bodies),
               'completion_percent_owned_by_later_Root_log_checkpoint': True})
    stage.finish()
    print('Actual MAIN checkpoint and unchanged corrected draft verified. Root may record completion.')

if __name__ == '__main__':
    require(len(sys.argv) == 2 and sys.argv[1] in ('objects', 'readback', 'cas'), 'Choose exactly one reviewed explicit stage')
    {'objects': objects, 'readback': readback, 'cas': cas}[sys.argv[1]]()
