"""Closed helpers for the NEW MAIN findings proposal. No dispatcher here."""
import base64, datetime, gzip, hashlib, json, os, re, stat, subprocess, sys, types
from pathlib import Path

WORKSPACE = Path('/Users/alec/Documents/Math')
PROGRAM = WORKSPACE / 'draft_pr_descending_audit_20261002'
AUDIT = PROGRAM / 'audits/pr262_30005044/initial_review_20261011'
PREPARATION = Path(__file__).absolute().parent
CHECKPOINT = PREPARATION.parent
NI = AUDIT / 'credited_integration_preparation_20261012'
ADC = 'adc6d1441ea42af49a9fe296e52358257c087993'
ADC_TREE = '26ab7153f7589e1b70e67603c3ae74cd33e480cb'
ADC_PARENT = '1de8c8d02861ffd90f91c351fbf603fd39764a5f'
SOURCE_VERSION = 'preparation_v04'
FREEZE_ROOT = CHECKPOINT / 'root_final_freeze_v04'
CLOSED_HISTORICAL_INPUT_PINS = {'adc_raw_commit': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/MAIN_COMMIT.raw', 'bytes': 544, 'sha256': 'a05534f5c918402a8a13b58db8cfe9f097ff833c3ed7703344430558f8419630', 'filesystem_mode': '0644'}, 'adc_raw_root_tree': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/MAIN_ROOT_TREE.raw', 'bytes': 8473, 'sha256': 'b07e6a554ea6f312baafbf9faf6ec6097a2b729aa631202c340620f9fec58109', 'filesystem_mode': '0644'}, 'adc_full_rows': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/MAIN_FULL_RAW_TREES_AND_LEAVES.nul.gz', 'bytes': 4261897, 'sha256': '186b8fa794edd75800cfd3ac576dde7bfa5cc2a6137969d47b86e65da5daa76d', 'filesystem_mode': '0644'}, 'historical_parent_raw_commit': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/PARENT_COMMIT.raw', 'bytes': 635, 'sha256': '19dab2b10b4be3162c95655a97bff3e3a9f9c0e3544fbddd19555b6ab37465c7', 'filesystem_mode': '0644'}, 'historical_parent_full_rows': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/PARENT_FULL_RAW_TREES_AND_LEAVES.nul.gz', 'bytes': 4259160, 'sha256': 'ac31f1b815e99ac8e00f7c55386c663ba51378b645c5ad18e24c9659b6f9cf36', 'filesystem_mode': '0644'}, 'peer_delta': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/PEER_76_PATH_DELTA.json', 'bytes': 20340, 'sha256': '60981555e2b7414bd1c654fbf4d81bb5f24dca2b40c3fbbebad6dfa758df0680', 'filesystem_mode': '0644'}, 'historical_driver_config': {'path': '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012/reader.git/config', 'bytes': 211, 'sha256': '946bdf13031ddc8d4b17a7bc67c6811da543ce2d9ccf9f5372a481fc3e38e154', 'filesystem_mode': '0644'}}
ACTOR = {'name': 'Alec Kriebel', 'email': 'me@aleckriebel.com'}
READER_SHA = 'e8ce82f5e444095be08fe771963ff24b2c4ce9fa0285f52d4da88d9cd218cd1e'
REPO = 'AlecKriebel/Math'
URL = 'https://github.com/AlecKriebel/Math.git'
HEX40 = re.compile('[0-9a-f]{40}')
REQUIRED_CLAIM_ROLES = {'program_scope', 'program_log', 'pr262_log', 'family_status',
    'complete_credited_C3', 'original_math_numerical_verification', 'independent_probability',
    'graphical_adversary', 'source_model_repair', 'priority_author_versions',
    'priority_contact_literature', 'priority_branching_explosion', 'whole_C3_clean_review',
    'consolidated_priority_review', 'Root_content_acceptance', 'Root_process_supersession',
    'actual_corrected_draft_acceptance'}

def require(test, message):
    if not test:
        raise ValueError(message)

def sha(body): return hashlib.sha256(body).hexdigest()
def oid(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()
def dump(value): return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def literal(path, base=None, kind=None, absent=False):
    path = Path(path)
    require(path.is_absolute() and str(path) == os.path.normpath(str(path)), 'Nonliteral path')
    require('.git' not in path.parts and '__pycache__' not in path.parts, 'Forbidden metadata/cache path')
    if base is not None: require(path.is_relative_to(base), 'Path leaves allowed root')
    prefix = Path(path.anchor)
    missing = False
    for index, name in enumerate(path.parts[1:], 1):
        prefix = prefix / name
        try: mode = prefix.lstat().st_mode
        except FileNotFoundError:
            missing = True
            continue
        require(not missing, 'Unexpected existent descendant')
        require(not stat.S_ISLNK(mode), 'Symlink rejected before access: ' + str(prefix))
        if index < len(path.parts) - 1: require(stat.S_ISDIR(mode), 'Ancestor is not directory')
        elif kind == 'file': require(stat.S_ISREG(mode), 'Input is not regular file')
        elif kind == 'directory': require(stat.S_ISDIR(mode), 'Input is not directory')
    if absent: require(not os.path.lexists(path), 'Output already occupied: ' + str(path))
    else: require(not missing, 'Required path missing: ' + str(path))
    return path

def file_pin(row, base=PROGRAM):
    require(set(row) == {'path', 'bytes', 'sha256', 'filesystem_mode'}, 'Incomplete/full pin schema')
    path = literal(row['path'], base=base, kind='file')
    require(stat.S_IMODE(path.lstat().st_mode) == int(row['filesystem_mode'], 8), 'Filesystem mode changed')
    body = path.read_bytes()
    require(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Full input bytes changed')
    return body

def allowed_repo_path(name):
    require(isinstance(name, str) and name and not name.startswith('/'), 'Nonliteral repository path')
    parts = name.split('/')
    require(all(p and p not in ('.', '..', '.git', '__pycache__') for p in parts), 'Unsafe path component')
    require(name in ('draft_pr_descending_audit_20261002/CURRENT_SCOPE.json',
                     'draft_pr_descending_audit_20261002/RESEARCH_LOG.md') or
            name.startswith('draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/'),
            'Out-of-program or peer/canonical target write rejected')
    banned = re.compile(r'(^|/)(fixtures?[^/]*|inert[^/]*|cache[^/]*|case_evidence|private_objects|'
                        r'objects|reader\.git|fetch\.git|remote[^/]*\.git|renders?|rendered|visual[^/]*|primary_pages|'
                        r'actual_execution[^/]*|private_execution[^/]*|provider|remote_objects|private_candidate[^/]*|root_final_freeze[^/]*)(/|$)', re.I)
    require(not banned.search(name), 'Bulky private/provider/fixture path excluded')
    require(not name.lower().endswith(('.pdf', '.html', '.htm', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.pyc', '.pyo')),
            'Third-party media/bytecode excluded')
    require(not any(p.lower() in ('.env', 'credentials', 'secrets', 'tokens') for p in parts), 'Secret path excluded')
    require('/research_checkpoint_20261012/' not in name, 'Retired checkpoint must remain untouched')
    require('/scoped_candidate' not in name and '/candidate_snapshot/' not in name, 'Historical duplicate package excluded')
    require('/author_correction_20261012/root_freeze_v01/bodies/' not in name, 'Author transport copies excluded')
    return name.encode('utf-8')

def review_closure(record, expected_status, bindings):
    # Root pins this COMPLETE explicit authored list; no mutable directory scan.
    required = {'decision', 'report', 'inputs', 'authored_manifest'}
    require(set(record['core']) == required, 'Review core closure incomplete')
    core = {role: file_pin(pin, base=AUDIT) for role, pin in record['core'].items()}
    decision = json.loads(core['decision'])
    require(decision['status'] == expected_status and decision['blocking_findings'] == [], 'Review not clean')
    require(decision['whole_fresh_review_complete'] is True, 'Whole fresh review missing')
    for key, value in bindings.items(): require(decision[key] == value, 'Review binding differs: ' + key)
    manifest = json.loads(core['authored_manifest'])
    require(manifest['schema'] == 'pr262-explicit-authored-review-closure-v1' and
            manifest['complete_authored_output_list'] is True and manifest['manifest_self_excluded'] is True,
            'Review manifest is not a full declared authored closure')
    rows = manifest['files']
    require(rows and len({r['path'] for r in rows}) == len(rows), 'Review closure duplicates/empty')
    parent = Path(record['core']['authored_manifest']['path']).parent
    covered = set()
    for row in rows:
        file_pin(row, base=parent); covered.add(row['path'])
    require({record['core'][k]['path'] for k in ('decision', 'report', 'inputs')} <= covered,
            'Review closure omits report/decision/input manifest')
    require(record['root_complete_read_and_fresh_rehash'] is True, 'Root review acceptance missing')

def stage_source_identity(stage, source_path, source_pin=None):
    """Bind the caller's actual source path AND full bytes to the reviewed role.

    A sibling source may not inherit the stored canonical dependency pins.
    No symlink resolution/relative aliases substitute for the exact source path.
    """
    require(stage in ('build', 'execute'), 'Unknown reviewed source role')
    role = 'builder' if stage == 'build' else 'executor'
    expected = PREPARATION / ('private_builder.py' if stage == 'build' else 'provider_executor.py')
    actual = Path(source_path)
    require(actual == expected and actual.is_absolute(), 'Actual stage source is not the exact reviewed canonical path')
    literal(actual, base=PREPARATION, kind='file')
    if source_pin is not None:
        require(Path(source_pin['path']) == actual, 'Reviewed source pin aliases actual stage source')
        file_pin(source_pin, base=PREPARATION)
    return role

def freeze_gate(stage, source_path):
    require(sys.flags.isolated and sys.flags.dont_write_bytecode and not sys.flags.optimize,
            'Launch only with python3 -I -B, without optimization')
    literal(PREPARATION, base=AUDIT, kind='directory')
    actual_source_role = stage_source_identity(stage, source_path)
    require(not os.path.lexists(PREPARATION / '__pycache__'), 'Source cache rejected')
    freeze_path = literal(FREEZE_ROOT / 'SELECTION.json', base=CHECKPOINT, kind='file')
    approval_name = 'ROOT_BUILD_APPROVAL_V04.json' if stage == 'build' else 'ROOT_EXECUTION_PROMOTION_V04.json'
    approval = json.loads(literal(CHECKPOINT / approval_name, base=CHECKPOINT, kind='file').read_bytes())
    body = freeze_path.read_bytes(); require(sha(body) == approval['selection_sha256'], 'Root exact selection differs')
    selection = json.loads(body)
    require(selection['schema'] == 'pr262-main-findings-final-freeze-v4' and selection['source_version'] == SOURCE_VERSION and
            selection['root_explicit_final_freeze'] is True, 'Proposal cannot authorize execution')
    certificate = read_current_certificate(selection)
    require((selection['baseline_commit'],selection['baseline_tree'],selection['sole_parent'])==
            (certificate['current_commit'],certificate['current_tree'],certificate['current_commit']), 'Frozen current baseline/sole findings parent differs')
    require(selection['actor'] == ACTOR and selection['actor_verified_source_commit'] == ADC,
            'Only verified actual actor is authorized')
    require(isinstance(selection['commit_unix_seconds'], int) and selection['commit_unix_seconds'] > 0 and
            selection['commit_date_utc'] == datetime.datetime.fromtimestamp(selection['commit_unix_seconds'],
                datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'Root chosen UTC/date differs')
    require(selection['commit_message'].endswith('\n') and '\0' not in selection['commit_message'], 'Exact final message required')
    require(selection['qualitative_assessment'] == 'already_solved' and selection['native_PR_merge'] is False and
            selection['paper_DOI_GWS'] is False and selection['added_author_attempt_turns'] == 0,
            'Research findings scope changed')
    require(approval['root_authorized_stage'] == stage and approval['new_independent_review_required_completed'] is True,
            'Root new stage acceptance missing')
    deps = selection['source_dependencies']
    require(set(deps) == {'common', 'builder', 'executor', 'owned_reader'}, 'Source dependency closure incomplete')
    expected = {'common': PREPARATION / 'checkpoint_common.py', 'builder': PREPARATION / 'private_builder.py',
                'executor': PREPARATION / 'provider_executor.py', 'owned_reader': PREPARATION / 'baseline_reader_v02.py'}
    for role, pin in deps.items():
        require(Path(pin['path']) == expected[role], 'Unexpected dependency alias')
        value = file_pin(pin, base=PREPARATION)
        if role == 'owned_reader': require(len(value) == 20648 and sha(value) == READER_SHA, 'NI reader is not exact e8ce version')
    stage_source_identity(stage, source_path, deps[actual_source_role])
    for tool in ('git', 'gh'): file_pin(selection['tools'][tool], base=None)
    inputs = selection['inputs']
    require(set(inputs) == set(CLOSED_HISTORICAL_INPUT_PINS) | {'actual_author_correction'},
            'Exact V04 historical and actual-author input role list required')
    for role, expected_pin in CLOSED_HISTORICAL_INPUT_PINS.items():
        require(inputs[role] == expected_pin, 'Literal Root current/historical input pin differs: ' + role)
    values = {role: file_pin(pin, base=AUDIT) for role, pin in inputs.items()}
    require(not (set(values) & set(certificate['input_pins'])), 'Historical/current input role aliases')
    values.update({role:file_pin(pin,base=Path(certificate['reader_context']['root'])) for role,pin in certificate['input_pins'].items()})
    actual = json.loads(values['actual_author_correction'])
    validate_actual_author_acceptance(actual, selection, certificate)
    require(HEX40.fullmatch(selection['corrected_author_head']) is not None, 'Corrected author head invalid')
    files = selection['files']
    require(files and len(files) == selection['selected_count'] and
            len({v['repository_path'] for v in files}) == len(files), 'Frozen selection count/list differs')
    require(sha(dump(files)) == selection['complete_selected_list_sha256'], 'Explicit selected list digest differs')
    require(set(selection['required_claim_roles']) == REQUIRED_CLAIM_ROLES and
            REQUIRED_CLAIM_ROLES <= {role for row in files for role in row['claim_roles']},
            'Meaningful claim/verification closure omitted')
    core = selection['complete_C3_target_files']
    require(len(core) == 38 and len({v['path'] for v in core}) == 38 and
            sha(dump(core)) == selection['complete_C3_target_files_sha256'] ==
            '844922cb8d940fff1980835b80740a909292c53f0cbbb1dd7b90de42361ee55b', 'Complete accepted C3 exact list missing')
    require(selection['C3_manifest_sha256'] == 'e3ab9c075ad00a7d97651b9218d2c4a83acc366cec847d0783d1eed2a63c3353',
            'Whole accepted C3 manifest differs')
    bodies = {}
    for row in files:
        name = allowed_repo_path(row['repository_path'])
        require(row['git_mode'] in ('100644', '100755'), 'Only literal authored regular bodies accepted')
        frozen = file_pin(row['frozen_body'], base=FREEZE_ROOT)
        current_path = Path(row['current_full_source']['path'])
        require(current_path.is_relative_to(AUDIT) or current_path in
                (PROGRAM / 'CURRENT_SCOPE.json', PROGRAM / 'RESEARCH_LOG.md'), 'Shared/peer current source rejected')
        current = file_pin(row['current_full_source'], base=PROGRAM)
        require(current == frozen and row['current_full_source']['sha256'] == row['frozen_body']['sha256'],
                'Current full source differs from Root literal frozen bytebody')
        require(oid('blob', frozen) == row['git_blob'], 'Selected raw blob identity differs')
        bodies[name] = (row['git_mode'].encode(), row['git_blob'], frozen)
    core_prefix = 'draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/research_findings_checkpoint_20261012/core_C3/'
    for row in core:
        require(row['path'].startswith('unsolved_math_prioritization/attempts/30005044/'), 'C3 list leaves target')
        relative = row['path'].removeprefix('unsolved_math_prioritization/attempts/30005044/')
        selected = next((v for v in files if v['repository_path'] == core_prefix + relative), None)
        require(selected is not None and selected['git_mode'] == row['mode'] and selected['git_blob'] == row['oid'] and
                selected['frozen_body']['bytes'] == row['bytes'] and selected['frozen_body']['sha256'] == row['sha256'],
                'Exact complete core C3 copy missing/different')
    require({v['repository_path'] for v in files if v['repository_path'].startswith(core_prefix)} ==
            {core_prefix + v['path'].removeprefix('unsolved_math_prioritization/attempts/30005044/') for v in core},
            'Unapproved core C3 extras')
    actual_selected = [v for v in files if 'actual_corrected_draft_acceptance' in v['claim_roles']]
    require(len(actual_selected)==1 and actual_selected[0]['current_full_source']==inputs['actual_author_correction'],
            'Selected actual corrected-draft receipt is not the closed accepted input')
    context = validate_baseline_context(selection, values, set(bodies), certificate)
    review_closure(approval['source_review'], 'GO_NEW_MAIN_FINDINGS_SOURCE_V04_ONLY',
        {'selection_sha256': sha(body), 'source_version':SOURCE_VERSION, 'baseline_certificate_sha256':selection['current_baseline_certificate_sha256'],
         'baseline_commit':certificate['current_commit'], 'baseline_tree':certificate['current_tree'], 'baseline_counts':certificate_counts(certificate,context['protected_paths']), 'builder_sha256': deps['builder']['sha256'],
         'executor_sha256': deps['executor']['sha256']})
    return selection, approval, bodies, values, certificate, context

def read_current_certificate(selection):
    pin = selection['current_baseline_certificate']
    body = file_pin(pin,base=AUDIT/'writer_coordination')
    require(pin['sha256']==selection['current_baseline_certificate_sha256'], 'Exact current certificate digest differs')
    value = json.loads(body)
    required={'schema','source_version','root_explicit_current_baseline_acceptance',
        'actual_full_raw_walk_and_fresh_ref_read_complete','current_commit','current_tree','current_parents',
        'current_counts','comparison_ADC','comparison_ADC_tree','foreign_leaf_count','foreign_all_entry_count',
        'reader_context','input_pins','snapshot_collection_source',
        'branch_guard_is_dated_provenance_not_current_author_correction_acceptance',
        'source_does_not_require_all_old_ADC_leaves_or76_historical_OIDs_unchanged'}
    require(set(value)==required and value['schema']=='pr262-main-findings-current-baseline-certificate-v4' and
            value['source_version']==SOURCE_VERSION and value['root_explicit_current_baseline_acceptance'] is True and
            value['actual_full_raw_walk_and_fresh_ref_read_complete'] is True and
            value['branch_guard_is_dated_provenance_not_current_author_correction_acceptance'] is True and
            value['source_does_not_require_all_old_ADC_leaves_or76_historical_OIDs_unchanged'] is True, 'Unchecked/incorrect current certificate')
    require(HEX40.fullmatch(value['current_commit']) and HEX40.fullmatch(value['current_tree']) and
            isinstance(value['current_parents'],list) and value['current_parents'] and
            len(set(value['current_parents']))==len(value['current_parents']) and
            all(HEX40.fullmatch(p) and p!=value['current_commit'] for p in value['current_parents']),
            'Exact current commit/tree/historical-parent identities required')
    counts=value['current_counts']
    require(set(counts)=={'leaves','directories','all_entries'} and
            all(type(v) is int and v>0 for v in counts.values()) and counts['all_entries']==counts['leaves']+counts['directories'],
            'Full actual current integer census counts required')
    require((value['comparison_ADC'],value['comparison_ADC_tree'])==(ADC,ADC_TREE) and
            type(value['foreign_leaf_count']) is int and value['foreign_leaf_count']>=0 and
            type(value['foreign_all_entry_count']) is int and value['foreign_all_entry_count']>=value['foreign_leaf_count'],
            'Fixed ADC comparison/count certificate differs')
    reader=value['reader_context'];require(set(reader)=={'root','driver','objects'}, 'Closed owned reader context required')
    root=literal(reader['root'],base=AUDIT/'writer_coordination',kind='directory')
    require(Path(pin['path']).parent==root and Path(reader['driver'])==root/'remote_reader.git' and
            Path(reader['objects'])==root/'remote_objects', 'Current reader/certificate path aliases')
    literal(reader['driver'],base=root,kind='directory');literal(reader['objects'],base=root,kind='directory')
    inputs=value['input_pins']
    require(set(inputs)=={'main_raw_commit','main_raw_root_tree','main_full_rows','foreign_delta',
                         'main_continuation_guard','baseline_driver_config'}, 'Current certificate input closure incomplete')
    require(Path(inputs['baseline_driver_config']['path'])==Path(reader['driver'])/'config', 'Current driver config alias')
    require(len({p['path'] for p in inputs.values()})==len(inputs), 'Current input path aliases')
    for row in inputs.values():file_pin(row,base=root)
    file_pin(value['snapshot_collection_source'],base=AUDIT/'writer_coordination')
    return value

def certificate_counts(certificate, protected_paths):
    return dict(certificate['current_counts'],peer_delta_paths=76,
                foreign_delta_leaf_paths=certificate['foreign_leaf_count'],
                foreign_delta_all_entries=certificate['foreign_all_entry_count'],
                protected_leaf_paths=len(protected_paths))

def validate_actual_author_acceptance(actual, selection, certificate):
    # Earlier actual author-stage MAIN and later findings MAIN are separate.
    require(actual['schema']=='pr262-root-actual-corrected-draft-acceptance-v4' and
            actual['checkpoint_source_version']==SOURCE_VERSION and
            actual['actual_corrected_author_commit']==selection['corrected_author_head'] and
            actual['full_provider_readback_accepted'] is True and actual['actual_ref_verified'] is True and
            actual['full_metadata_readback_accepted'] is True and
            actual['fresh_author_stage_main_guard_accepted'] is True and actual['PR_OPEN_DRAFT_unmerged_unclosed'] is True,
            'Actual corrected author/ref/metadata acceptance missing; planned OID is not authority')
    require(selection['corrected_PR_metadata']=={'title':actual['accepted_PR_title'],
                'body_sha256':actual['accepted_PR_body_sha256']} and
            isinstance(actual['accepted_PR_title'],str) and
            re.fullmatch('[0-9a-f]{64}',actual['accepted_PR_body_sha256']), 'Accepted actual corrected PR metadata differs')
    support=actual['actual_provider_acceptance_support']
    require(support and len({p['path'] for p in support})==len(support), 'Actual acceptance full support closure missing')
    for pin in support:file_pin(pin,base=AUDIT)

def protected_current_paths(peer_paths, foreign_paths, selected_paths, current_rows):
    # Historical paths remain protected, but their current value/absence wins.
    protected=peer_paths|foreign_paths
    require(not (protected & selected_paths), 'Selection touches historical-peer/current-delta path')
    for target in selected_paths:
        require(not any(target.startswith(p+b'/') or p.startswith(target+b'/') for p in protected),
                'Selection structurally aliases a protected current path or absence')
    return protected

def foreign_current_entries_preserved(before, after, paths, selected_paths):
    for p in paths:
        value=before.get(p)
        selected_ancestor=value is not None and value[0]==b'40000' and any(q.startswith(p+b'/') for q in selected_paths)
        if selected_ancestor:
            require(after.get(p,(None,None))[0]==b'40000', 'Foreign ancestor directory replaced by selected leaf')
        else:require(after.get(p)==value, 'Current foreign entry identity or absence changed')

def validate_complete_census(rows, root):
    children={b'':{}}
    for p,(mode,ident) in rows.items():
        require(mode in (b'40000',b'100644',b'100755',b'120000',b'160000') and
                p and all(v and v not in (b'.',b'..') for v in p.split(b'/')), 'Unsafe census path/mode')
        parent,_,name=p.rpartition(b'/')
        require(not parent or rows.get(parent,(None,None))[0]==b'40000', 'Census omits directory ancestor')
        children.setdefault(parent,{})[name]=(mode,ident)
        if mode==b'40000':children.setdefault(p,{})
    for path,entries in children.items():
        expected=root if not path else rows[path][1]
        require(oid('tree',tree_encode(entries))==expected, 'Complete census directory Merkle identity differs')

def entry_delta(before, after):
    def value(item):
        return None if item is None else {'mode':item[0].decode(), 'oid':item[1]}
    return [{'path':p.decode(), 'before':value(before.get(p)), 'after':value(after.get(p))}
            for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]

def validate_delta_records(records, before, after, expected_count):
    expected = entry_delta(before, after)
    require(len(expected) == expected_count and records == expected,
            'Complete raw delta paths/modes/OIDs/order/additions/deletions differ')
    return {row['path'].encode() for row in records}

def validate_baseline_context(selection, inputs, selected_paths, certificate):
    """Verify the ONE frozen current certificate, never refresh or absorb drift."""
    current_commit,current_tree=certificate['current_commit'],certificate['current_tree']
    require(oid('commit',inputs['main_raw_commit'])==current_commit and
            commit_header(inputs['main_raw_commit'])[:2]==(current_tree,certificate['current_parents']), 'Certified raw current identity differs')
    require(oid('commit',inputs['adc_raw_commit'])==ADC and
            commit_header(inputs['adc_raw_commit'])[:2]==(ADC_TREE,[ADC_PARENT]), 'Fixed raw ADC identity differs')
    require(oid('commit',inputs['historical_parent_raw_commit'])==ADC_PARENT, 'Fixed raw 1de identity differs')
    actor_rows=[v for v in inputs['adc_raw_commit'].split(b'\n\n')[0].splitlines() if v.startswith((b'author ',b'committer '))]
    require(len(actor_rows)==2 and all(b'Alec Kriebel <me@aleckriebel.com> ' in v for v in actor_rows), 'Fixed verified ADC actor differs')
    current=parse_census(gzip.decompress(inputs['main_full_rows']))
    adc=parse_census(gzip.decompress(inputs['adc_full_rows']))
    historical=parse_census(gzip.decompress(inputs['historical_parent_full_rows']))
    count_rows=lambda rows:{'leaves':sum(v[0]!=b'40000' for v in rows.values()),
                           'directories':sum(v[0]==b'40000' for v in rows.values()),'all_entries':len(rows)}
    require(count_rows(current)==certificate['current_counts'], 'Every certified current census count must match')
    require(count_rows(adc)=={'leaves':160040,'directories':21132,'all_entries':181172}, 'Fixed ADC census counts differ')
    top=lambda rows:{p:v for p,v in rows.items() if b'/' not in p}
    require(inputs['main_raw_root_tree']==tree_encode(top(current)) and oid('tree',inputs['main_raw_root_tree'])==current_tree,
            'Certified complete current root/census binding differs')
    require(inputs['adc_raw_root_tree']==tree_encode(top(adc)) and oid('tree',inputs['adc_raw_root_tree'])==ADC_TREE,
            'Fixed complete ADC root/census binding differs')
    historical_root=commit_header(inputs['historical_parent_raw_commit'])[0]
    require(oid('tree',tree_encode(top(historical)))==historical_root,'Fixed historical root/census binding differs')
    leaves=lambda rows:{p:v for p,v in rows.items() if v[0]!=b'40000'}
    validate_complete_census(current,current_tree);validate_complete_census(adc,ADC_TREE)
    validate_complete_census(historical,historical_root)
    current_leaves,adc_leaves,historical_leaves=leaves(current),leaves(adc),leaves(historical)
    peer=json.loads(inputs['peer_delta'])
    require(peer['MAIN']==ADC and peer['parent']==ADC_PARENT and peer['changed_leaf_count']==76 and
            peer['independently_raw_derived'] is True and peer['all76_must_be_preserved_in_prepared_root'] is True,
            'Original peer76 ledger identity differs')
    peer_paths=validate_delta_records(peer['changes'],historical_leaves,adc_leaves,76)
    foreign=json.loads(inputs['foreign_delta'])
    require(foreign['schema']=='pr262-full-literal-main-advance-delta-v2-reviewed-data' and foreign['actual_commit']==current_commit and
            foreign['baseline_commit']==ADC and foreign['actual_full_raw_git_derived'] is True and
            foreign['changed_leaf_count']==certificate['foreign_leaf_count'] and
            foreign['all_entries_changed']==certificate['foreign_all_entry_count'], 'Exact certified foreign delta identity differs')
    foreign_paths=validate_delta_records(foreign['changes'],adc_leaves,current_leaves,certificate['foreign_leaf_count'])
    foreign_all_paths=validate_delta_records(foreign['all_entry_changes'],adc,current,certificate['foreign_all_entry_count'])
    require(foreign['actual_root']==current_tree and foreign['actual_ordered_parents']==certificate['current_parents'],
            'Complete foreign delta root/ordered-parent binding differs')
    protected=protected_current_paths(peer_paths,foreign_paths,selected_paths,current)
    # A selected leaf cannot replace a foreign directory/subtree or hide a leaf.
    require(not (foreign_all_paths & selected_paths) and not any(
            p.startswith(target+b'/') or (target.startswith(p+b'/') and current.get(p,(None,None))[0]!=b'40000')
            for p in foreign_all_paths for target in selected_paths), 'Selection structurally aliases current foreign entries')
    require(selection['baseline_counts']==certificate_counts(certificate,protected) and
            selection['peer_delta_literal_paths']==sorted(p.decode() for p in peer_paths) and
            selection['foreign_delta_literal_paths']==sorted(p.decode() for p in foreign_paths) and
            selection['foreign_delta_all_entry_paths']==sorted(p.decode() for p in foreign_all_paths) and
            selection['peer_delta_record_sha256']==sha(inputs['peer_delta']) and
            selection['foreign_delta_record_sha256']==sha(inputs['foreign_delta']), 'Frozen exact delta lists/hashes differ')
    root=Path(certificate['reader_context']['root']);guard=json.loads(inputs['main_continuation_guard'])
    require(guard['schema']=='pr262-root-current-main-findings-snapshot-acceptance-v4' and
            guard['status']=='ACCEPTED_CURRENT_MAIN_FINDINGS_SNAPSHOT_DATA_ONLY' and
            (guard['current_commit'],guard['current_tree'],guard['current_parents'])==
            (current_commit,current_tree,certificate['current_parents']) and
            guard['current_counts']==certificate['current_counts'] and
            (guard['comparison_ADC'],guard['comparison_ADC_tree'])==(ADC,ADC_TREE) and
            guard['delta_leaf_count']==certificate['foreign_leaf_count'] and
            guard['delta_all_entry_count']==certificate['foreign_all_entry_count'] and
            guard['root_full_raw_census_and_commit_checked'] is True and
            guard['root_fresh_direct_MAIN_ref_matches_snapshot'] is True and
            guard['no_author_or_MAIN_provider_mutation_authority'] is True and
            guard['current_author_or_metadata_constraint'] is False and
            guard['all_historical_ADC_leaf_OIDs_unchanged_required_for_future_Main_certificates'] is False and
            guard['current_foreign_identities_and_absences_must_be_preserved_in_candidate'] is True and
            guard['full_current_certificate_selection_review_and_separate_stage_authority_required'] is True and
            guard['saved_PR_base_sha_not_used_as_current_MAIN_ref'] is True,
            'Root exact MAIN-specific snapshot acceptance differs')
    raw_roles={'raw_commit':'main_raw_commit','raw_root_tree':'main_raw_root_tree',
               'full_trees_and_leaves':'main_full_rows','full_delta':'foreign_delta'}
    require(set(guard['raw_input_pins'])==set(raw_roles)|{'full_leaves','plan_baseline_trees_and_leaves'}, 'Root nested raw dependency closure differs')
    for role,input_role in raw_roles.items():
        require(guard['raw_input_pins'][role]==certificate['input_pins'][input_role], 'Certified nested raw pin alias differs')
        require(file_pin(guard['raw_input_pins'][role],base=root)==inputs[input_role], 'Root complete raw support differs')
    require(gzip.decompress(file_pin(guard['raw_input_pins']['full_leaves'],base=root))==census(current_leaves), 'Root full leaf-only support differs')
    require(gzip.decompress(file_pin(guard['raw_input_pins']['plan_baseline_trees_and_leaves'],base=root))==census(adc), 'Root full fixed ADC comparison support differs')
    validate_snapshot_support(guard,certificate,inputs,root)
    # Historical author/39-preimage guard is read only as pinned dated provenance.
    file_pin(guard['branch_guard_dated_provenance_only'],base=root)
    body_rows=foreign['new_foreign_body_pins']
    surviving_blobs={p for p in foreign_paths if p in current_leaves and current_leaves[p][0]!=b'160000'}
    require(len(body_rows)==len(surviving_blobs) and len({v['repository_path'] for v in body_rows})==len(body_rows) and
            {v['repository_path'].encode() for v in body_rows}==surviving_blobs,
            'Every surviving changed foreign blob body provenance required, no deleted-body substitution')
    for row in body_rows:
        body=file_pin(row['body'],base=root)
        require(oid('blob',body)==row['git_blob']==current_leaves[row['repository_path'].encode()][1], 'Complete foreign body identity differs')
    return {'current_rows':current,'adc_rows':adc,'historical_rows':historical,
            'peer_paths':peer_paths,'foreign_paths':foreign_paths,'foreign_all_paths':foreign_all_paths,'protected_paths':protected}

def validate_raw_ancestry(ancestry, raw):
    require(ancestry and len(set(ancestry))==len(ancestry) and set(raw)==set(ancestry), 'Raw ancestry path/map closure differs')
    for index,ident in enumerate(ancestry):
        require(HEX40.fullmatch(ident) and oid('commit',raw[ident])==ident,'Full ancestry raw commit identity differs')
        tree,parents,_=commit_header(raw[ident])
        require(HEX40.fullmatch(tree) and len(set(parents))==len(parents) and all(HEX40.fullmatch(p) for p in parents),
                'Raw ancestry root/ordered parent framing differs')
        if index+1<len(ancestry):require(ancestry[index+1] in parents,'Ancestry path skips a raw parent edge')
def validate_snapshot_support(guard,certificate,inputs,root):
    ancestry=guard['ancestry_path'];pins=guard['ancestry_raw_commit_pins']
    require(ancestry and ancestry[0]==certificate['current_commit'] and ancestry[-1]==ADC and
            len(set(ancestry))==len(ancestry) and set(pins)==set(ancestry), 'Complete exact ADC ancestry path/pin map differs')
    raw={ident:file_pin(pins[ident],base=root) for ident in ancestry}
    validate_raw_ancestry(ancestry,raw)
    require(raw[ancestry[0]]==inputs['main_raw_commit'] and raw[ADC]==inputs['adc_raw_commit'], 'Ancestry terminal full bodies differ')
    refs=guard['fresh_direct_provider_pins']
    require(len(refs)==3 and len({p['path'] for p in refs})==3, 'Complete saved direct MAIN/author/PR support required')
    main,author,pr=[json.loads(file_pin(p,base=root)) for p in refs]
    require(main['ref']=='refs/heads/main' and main['object']['type']=='commit' and
            main['object']['sha']==certificate['current_commit'], 'Saved direct MAIN ref does not match current snapshot')
    # Author and PR are saved provenance here; live correction checks are separate.
    require(author['ref']=='refs/heads/dot/math-30005044' and author['object']['type']=='commit' and
            HEX40.fullmatch(author['object']['sha']) and pr['number']==262, 'Saved author/PR identity provenance differs')
    providers=guard['whole_provider_commit_and_root_pins']
    require(len(providers)==2 and len({p['path'] for p in providers})==2, 'Complete provider commit/root support required')
    commit,tree=[json.loads(file_pin(p,base=root)) for p in providers]
    require(commit['sha']==certificate['current_commit'] and commit['tree']['sha']==certificate['current_tree'] and
            [p['sha'] for p in commit['parents']]==certificate['current_parents'], 'Provider current commit ordered identity differs')
    require(tree['sha']==certificate['current_tree'] and provider_tree_raw(tree)==inputs['main_raw_root_tree'],
            'Whole nonrecursive provider current root differs from exact raw root')

class Stage:
    """Reserve the WHOLE future capture set before any dispatch, including GET/Git.

    An existing stage directory is a no-retry tombstone. All capture handles are
    exclusive and held open; every write also checks current path/inode identity.
    """
    def __init__(self, root, names, directories=()):
        self.root = Path(root); self.handles = {}; self.completed = False
        literal(self.root, base=CHECKPOINT, absent=True)
        require(len(set(names)) == len(names), 'Output aliases rejected')
        require('STAGE_COMPLETED.json' in names, 'Final future acceptance capture omitted')
        allnames = list(names) + list(directories)
        require(len(set(allnames)) == len(allnames), 'Future capture/directory aliases rejected before mutation')
        for name in allnames:
            require(name and not name.startswith('/') and all(p not in ('', '.', '..', '.git', '__pycache__')
                    for p in name.split('/')), 'Unsafe future output')
            literal(self.root / name, base=CHECKPOINT, absent=True)
        files = {self.root / n for n in names}
        require(not any(p in q.parents for p in files for q in files | {self.root / d for d in directories}),
                'Future file/directory overlap')
        # No filesystem mutation, subprocess, GET, POST or reference dispatch above.
        if os.path.lexists(self.root.parent): literal(self.root.parent, base=CHECKPOINT, kind='directory')
        else: literal(self.root.parent, base=CHECKPOINT, absent=True)
        self.root.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.root.mkdir(mode=0o700)
        for name in directories:
            (self.root / name).mkdir(mode=0o700, parents=True, exist_ok=False)
        for name in names:
            path = self.root / name
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            self.handles[name] = (fd, os.fstat(fd))
    def write(self, name, body):
        require(name in self.handles, 'Output not in whole-stage reservation')
        path = literal(self.root / name, base=self.root, kind='file')
        fd, initial = self.handles[name]; current = path.lstat()
        require((current.st_dev, current.st_ino) == (initial.st_dev, initial.st_ino) and current.st_nlink == 1,
                'Reserved output path replaced/aliased')
        require(os.fstat(fd).st_size == 0, 'Capture already written; no overwrite/retry')
        offset = 0
        while offset < len(body): offset += os.write(fd, body[offset:])
        os.fsync(fd)
    def json(self, name, value): self.write(name, dump(value))
    def finish(self):
        self.json('STAGE_COMPLETED.json', {'UTC': utc(), 'whole_future_capture_set_reserved_before_dispatch': True,
                  'automatic_retry_prohibited': True})
        self.completed = True
        for fd, _ in self.handles.values(): os.close(fd)

def clean_env(objects=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0',
               GIT_OPTIONAL_LOCKS='0', GIT_ATTR_NOSYSTEM='1', GH_REPO=REPO, GH_HOST='github.com')
    if objects is not None: env['GIT_OBJECT_DIRECTORY'] = str(objects)
    return env

def owned_reader(selection, driver, objects, root, config_sha=None, process_module=subprocess):
    """Fresh exact reader module per context; no global rebinding/restoration alias."""
    source = file_pin(selection['source_dependencies']['owned_reader'], base=PREPARATION)
    require(sha(source) == READER_SHA, 'Reader SHA differs')
    module = types.ModuleType('exact_ni_reader'); module.__file__ = str(PREPARATION / 'baseline_reader_v02.py')
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    module.ROOT, module.DRIVER, module.OBJECTS = Path(root), Path(driver), Path(objects)
    module.ALTERNATES = []
    require(not os.path.lexists(Path(root) / '__pycache__'), 'Reader source cache rejected')
    literal(driver, base=AUDIT, kind='directory'); literal(objects, base=AUDIT, kind='directory')
    literal(Path(driver) / 'refs/replace', base=AUDIT, absent=True)
    if config_sha is not None:
        require(sha(literal(Path(driver) / 'config', base=AUDIT, kind='file').read_bytes()) == config_sha,
                'Exact baseline driver config changed')
    module.inspect_driver()
    git_pin = dict(selection['tools']['git']); git_exe = git_pin['path']
    class BoundProcess:
        PIPE = subprocess.PIPE
        @staticmethod
        def Popen(args, **kwargs):
            require(args == ['git', '--no-replace-objects', '--git-dir', str(driver), 'cat-file', '--batch'],
                    'Unapproved reader process')
            require(kwargs['env'] == clean_env(objects) and kwargs['cwd'] == Path(root), 'Reader environment/root differs')
            require(selection['tools']['git'] == git_pin, 'Reader executable pin binding changed')
            file_pin(git_pin, base=None)  # Fresh complete tool pin at this actual spawn boundary.
            return process_module.Popen([git_exe, *args[1:]], **kwargs)
    module.subprocess = BoundProcess
    reader = module.Reader(clean_env(objects))
    require(reader.cache == {}, 'New raw reader cache not empty')
    return module, reader

def tree_encode(entries):
    keys = sorted(entries, key=lambda n: n + (b'/' if entries[n][0] == b'40000' else b''))
    return b''.join(entries[n][0] + b' ' + n + b'\0' + bytes.fromhex(entries[n][1]) for n in keys)

def validate_changed_tree_records(records, before_rows, after_rows, candidate_tree, before_root):
    """Keep one complete record per directory path; equal OIDs may repeat.

    Repeated raw object identities are accepted only for byte-identical validated
    bodies. Every path binds separately to its old/new complete census entries,
    and its raw body must encode EXACTLY that path's direct census children.
    """
    require(records and HEX40.fullmatch(candidate_tree), 'Empty/invalid changed-tree closure')
    changed_paths = {p for p, value in after_rows.items()
                     if value[0] == b'40000' and before_rows.get(p) != value}
    if candidate_tree != before_root: changed_paths.add(b'')
    paths = set(); raw_by_oid = {}
    for row in records:
        path = base64.b64decode(row['directory_b64'], validate=True)
        require(base64.b64encode(path).decode() == row['directory_b64'] and
                (not path or all(part and part not in (b'.', b'..') for part in path.split(b'/'))) and
                path not in paths, 'Duplicate/unsafe/noncanonical directory-path record')
        paths.add(path)
        old = before_root if not path else before_rows.get(path, (None, None))[1]
        new = candidate_tree if not path else after_rows.get(path)
        if path:
            require(new == (b'40000', row['after']) and
                    (path not in before_rows or before_rows[path][0] == b'40000'), 'Changed tree has wrong directory binding')
        else: require(row['after'] == new, 'Changed raw root differs')
        require(row['before'] == old and row['before'] != row['after'], 'Changed tree old/path identity differs')
        body = base64.b64decode(row['body_base64'], validate=True)
        require(oid('tree', body) == row['after'] and len(body) == row['raw_bytes'] and sha(body) == row['sha256'],
                'Complete changed raw tree body/hash/size differs')
        prefix = path + b'/' if path else b''
        direct_children = {p[len(prefix):]: value for p, value in after_rows.items()
                           if p.startswith(prefix) and b'/' not in p[len(prefix):]}
        require(direct_children and body == tree_encode(direct_children), 'Raw tree does not match every direct child at its own path')
        if row['after'] in raw_by_oid:
            require(raw_by_oid[row['after']] == body, 'Repeated raw tree OID has nonidentical complete bodies')
        else: raw_by_oid[row['after']] = body
    require(paths == changed_paths, 'Per-path changed ancestor closure is incomplete or contains extras')
    return raw_by_oid

def census(rows):
    return b''.join(m + b' ' + h.encode() + b'\t' + p + b'\0' for p, (m, h) in sorted(rows.items()))
def parse_census(body):
    result = {}
    for line in body.split(b'\0'):
        if not line: continue
        prefix, name = line.split(b'\t', 1); mode, ident = prefix.split(b' ')
        require(name not in result and HEX40.fullmatch(ident.decode()), 'Duplicate/malformed raw census')
        result[name] = mode, ident.decode()
    require(census(result) == body, 'Noncanonical raw census')
    return result
def commit_header(body):
    require(b'\n\n' in body, 'Raw commit framing missing')
    headers, message = body.split(b'\n\n', 1)
    lines = headers.splitlines(); require(lines[0].startswith(b'tree '), 'Raw root missing')
    return lines[0][5:].decode(), [v[7:].decode() for v in lines if v.startswith(b'parent ')], message

def provider_tree_raw(value):
    require(value['truncated'] is False, 'Truncated provider tree rejected')
    entries = {}
    for row in value['tree']:
        name = row['path'].encode(); mode = row['mode'].lstrip('0').encode()
        require(name and name not in entries and b'/' not in name and b'\0' not in name and
                name not in (b'.', b'..') and mode in (b'40000', b'100644', b'100755', b'120000', b'160000') and
                HEX40.fullmatch(row['sha']), 'Invalid provider raw tree entry')
        entries[name] = mode, row['sha']
    return tree_encode(entries)

def run_capture(selection, stage, name, args, env, input_body=None, timeout=60):
    # All possible outputs were reserved by Stage before this call.
    tool = args[0]; require(tool in (selection['tools']['git']['path'], selection['tools']['gh']['path']), 'Unapproved binary')
    file_pin(selection['tools']['git' if tool == selection['tools']['git']['path'] else 'gh'], base=None)
    result = subprocess.run(args, input=input_body, env=env, cwd=stage.root,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    stage.write(name + '.stdout', result.stdout); stage.write(name + '.stderr', result.stderr)
    require(result.returncode == 0, 'Dispatch failed/unknown; inspect captures; never retry this stage')
    return result.stdout

def api(selection, stage, method, endpoint, name, payload=None):
    require(method in ('GET', 'POST'), 'Unsupported provider action')
    if method == 'GET': require(payload is None and endpoint.startswith('repos/' + REPO + '/'), 'GET scope differs')
    else:
        require(endpoint in ('repos/' + REPO + '/git/blobs', 'repos/' + REPO + '/git/trees',
                             'repos/' + REPO + '/git/commits', 'graphql'), 'Provider write outside exact checkpoint objects/CAS')
        stage.json(name + '.STARTED.json', {'UTC': utc(), 'method': method, 'endpoint': endpoint,
                   'payload_sha256': sha(payload), 'automatic_retry_prohibited': True})
    args = [selection['tools']['gh']['path'], 'api', '--method', method, '--hostname', 'github.com', endpoint]
    if payload is not None: args += ['--input', '-']
    body = run_capture(selection, stage, name, args, clean_env(), payload)
    value = json.loads(body); require(not isinstance(value, dict) or not value.get('errors'), 'Provider errors; no automatic retry')
    return value

def api_outputs(name, write=False):
    return [name + '.stdout', name + '.stderr'] + ([name + '.STARTED.json'] if write else [])
def fresh_main(selection, stage, name, expected):
    value = api(selection, stage, 'GET', 'repos/' + REPO + '/git/ref/heads/main', name)
    require(value['ref'] == 'refs/heads/main' and value['object']['type'] == 'commit' and
            value['object']['sha'] == expected, 'Fresh MAIN differs; re-freeze/re-review required')
def fresh_pr(selection, stage, name):
    value = api(selection, stage, 'GET', 'repos/' + REPO + '/pulls/262', name)
    require(value['state'] == 'open' and value['draft'] is True and value['merged'] is False and
            value['merged_at'] is None and value['head']['sha'] == selection['corrected_author_head'] and
            value['head']['ref'] == 'dot/math-30005044' and value['head']['repo']['full_name'] == REPO and
            value['base']['ref'] == 'main' and value['base']['repo']['full_name'] == REPO,
            'PR corrected head/disposition differs')
    require(value['title']==selection['corrected_PR_metadata']['title'] and
            sha((value['body'] or '').encode())==selection['corrected_PR_metadata']['body_sha256'],
            'PR actual accepted corrected title/body differs')
