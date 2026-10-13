#!/usr/bin/env python3
"""Small local mechanism controls. No subprocess/network/provider/Git dispatch.

The exact NI Reader parses real raw framing/tree bodies through a mock pipe.
The executor's actual empty_remote_readback method runs; its two Git transports
alone are mocked. Temporary owned fixtures are removed rather than published.
"""
import base64, hashlib, io, json, os, stat, sys, tempfile, types
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).absolute().parent

def load(name):
    path = ROOT / name
    module = types.ModuleType('control_' + name.removesuffix('.py')); module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

C = load('checkpoint_common.py')
B = load('private_builder.py')
E = load('provider_executor.py')
results = []; dispatches = []

def check(name, action):
    action(); results.append({'name': name, 'outcome': 'PASS'})

def reject(action):
    try: action()
    except (ValueError, RuntimeError, FileExistsError): return
    raise AssertionError('Invalid input unexpectedly accepted')

class OutputPipe:
    def __init__(self): self.body = bytearray(); self.position = 0
    def append(self, body): self.body.extend(body)
    def read(self, n):
        value = bytes(self.body[self.position:self.position + n]); self.position += len(value); return value
    def readline(self):
        end = self.body.index(10, self.position) + 1
        return self.read(end - self.position)

class FakeProcess:
    def __init__(self, objects):
        self.objects = objects; self.stdout = OutputPipe(); self.stderr = io.BytesIO(); self.closed = False
        process = self
        class InputPipe:
            def write(self, body):
                ident = body.strip().decode(); kind, raw = process.objects[ident]
                process.stdout.append(ident.encode() + b' ' + kind.encode() + b' ' + str(len(raw)).encode() + b'\n' + raw + b'\n')
            def flush(self): pass
            def close(self): process.closed = True
        self.stdin = InputPipe()
    def wait(self, timeout): assert self.closed; return 0

raw_objects = {}
def object_body(kind, body):
    ident = C.oid(kind, body); raw_objects[ident] = kind, body; return ident

hello = object_body('blob', b'hello\n')
link = object_body('blob', b'../safe')
sub = object_body('tree', C.tree_encode({b'child': (b'100644', hello)}))
root = object_body('tree', C.tree_encode({b'a': (b'100644', hello), b'dir': (b'40000', sub),
                         b'link': (b'120000', link), b'module': (b'160000', '3' * 40)}))
fixture_parent = '9' * 40
empty_root = object_body('tree',b'')
raw_commit = b'tree ' + root.encode() + b'\nparent ' + fixture_parent.encode() + b'\nauthor A <a@example.test> 1 +0000\ncommitter A <a@example.test> 1 +0000\n\nfixture\n'
commit = object_body('commit', raw_commit)
processes = []
class FakePopen:
    @staticmethod
    def Popen(args, **kwargs):
        # Mock only the transport; use the exact Reader.get/tree/walk/close.
        dispatches.append({'mock': 'exact_reader_pipe', 'argv': args})
        process = FakeProcess(raw_objects); processes.append(process); return process

def full_pin(path):
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'sha256': C.sha(body),
            'filesystem_mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

selection = {'source_dependencies': {'owned_reader': full_pin(ROOT / 'baseline_reader_v02.py')},
             'tools': {'git': {'path': '/inert/mock/git'}, 'gh': {'path': '/inert/mock/gh'}}}

with tempfile.TemporaryDirectory(prefix='small_mock_controls_', dir=ROOT) as temporary:
    fixture = Path(temporary)
    git_fixture = fixture / 'inert_git_tool'; git_fixture.write_bytes(b'inert fixture only; never executable dispatch\n')
    gh_fixture = fixture / 'inert_gh_tool'; gh_fixture.write_bytes(b'inert fixture only; never executable dispatch\n')
    selection['tools'] = {'git':full_pin(git_fixture), 'gh':full_pin(gh_fixture)}
    baseline = fixture / 'baseline'; baseline.mkdir()
    driver = baseline / 'reader.git'; driver.mkdir()
    objects = baseline / 'objects'; objects.mkdir()
    config = b'[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = true\n'
    (driver / 'config').write_bytes(config)
    baseline_module, baseline_reader = C.owned_reader(selection, driver, objects, baseline,
                                      config_sha=C.sha(config), process_module=FakePopen)
    def tool_positive():
        assert selection['tools']['git']==full_pin(git_fixture)
        assert dispatches[-1]['argv'][0]==selection['tools']['git']['path']
    check('V04_actual_Reader_Popen_checks_complete_tool_pin_at_dispatch_positive',tool_positive)
    saved_tool_body=git_fixture.read_bytes(); saved_tool_mode=stat.S_IMODE(git_fixture.stat().st_mode)
    for label,mutation in [('changed_tool_body',lambda:git_fixture.write_bytes(saved_tool_body+b'changed')),
                           ('changed_tool_mode',lambda:git_fixture.chmod(0o600))]:
        mutation(); before_dispatch=len(dispatches)
        check('V04_actual_Reader_Popen_'+label+'_rejected_before_mock_transport',lambda:
              reject(lambda:C.owned_reader(selection,driver,objects,baseline,config_sha=C.sha(config),process_module=FakePopen)))
        assert len(dispatches)==before_dispatch
        git_fixture.write_bytes(saved_tool_body);git_fixture.chmod(saved_tool_mode)
    saved_driver_context = (baseline_module.ROOT, baseline_module.DRIVER, baseline_module.OBJECTS)
    original_payload_entries = {'historical/proof': ('100644', hello)}
    before_payload = dict(original_payload_entries)
    def raw_reader_walk():
        assert baseline_reader.get(commit) == ('commit', raw_commit)
        rows = baseline_reader.walk(root)
        assert len(rows) == 5 and rows[b'dir/child'] == (b'100644', hello)
        assert rows[b'link'] == (b'120000', link) and rows[b'module'] == (b'160000', '3' * 40)
        assert C.parse_census(C.census(rows)) == rows
    check('exact_e8_reader_raw_commit_framing_and_recursive_walk_positive', raw_reader_walk)
    def preserve_and_rewrite():
        blob = object_body('blob', b'new authored result\n')
        selected = {b'new/deep/check.md': (b'100644', blob, b'new authored result\n')}
        changed = []; after_root = B.rewrite_tree(baseline_reader, root, selected, rewritten=changed)
        before = baseline_reader.walk(root); after = B.MemoryTrees(baseline_reader, changed).walk(after_root)
        assert {p:v for p,v in after.items() if v[0] != b'40000' and p not in selected} == {p:v for p,v in before.items() if v[0] != b'40000'}
        assert after[b'new/deep/check.md'] == (b'100644', blob)
        assert after[b'dir'] == before[b'dir'] and len(changed) == 3
    check('raw_rewrite_preserves_link_submodule_existing_leaf_and_unrewritten_directory', preserve_and_rewrite)
    check('file_directory_collision_rejected', lambda: reject(lambda: B.rewrite_tree(baseline_reader, root,
          {b'a/new': (b'100644', hello, b'hello\n')})))
    check('selected_ancestor_collision_rejected', lambda: reject(lambda: B.rewrite_tree(baseline_reader, root,
          {b'x': (b'100644', hello, b'hello\n'), b'x/y': (b'100644', hello, b'hello\n')})))
    check('canonical_attempt_destination_rejected', lambda: reject(lambda: C.allowed_repo_path('unsolved_math_prioritization/attempts/30005044/PROOF.md')))
    check('peer_audit_destination_rejected', lambda: reject(lambda: C.allowed_repo_path('draft_pr_descending_audit_20261002/audits/pr263_30000170/X.md')))
    check('retired_checkpoint_destination_rejected', lambda: reject(lambda: C.allowed_repo_path('draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/research_checkpoint_20261012/X.md')))
    check('fixture_destination_rejected', lambda: reject(lambda: C.allowed_repo_path('draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/fixtures/X.md')))
    check('third_party_media_destination_rejected', lambda: reject(lambda: C.allowed_repo_path('draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/source.pdf')))
    # F2 uses the actual new freeze_gate early source check: a copied sibling
    # cannot inherit the reviewed canonical builder/executor full-source pins.
    for stage_role, name in [('build', 'private_builder.py'), ('execute', 'provider_executor.py')]:
        # An actual byte-identical sibling exists. Its path still cannot borrow
        # the reviewed canonical role or its source pin; remove it after testing.
        alternate = fixture / ('sibling_' + name)
        alternate.write_bytes((ROOT / name).read_bytes())
        assert alternate.read_bytes() == (ROOT / name).read_bytes()
        count = len(dispatches)
        check('S2_actual_freeze_gate_rejects_byte_identical_sibling_' + stage_role + '_before_authority_or_dispatch',
              lambda stage_role=stage_role: reject(lambda: C.freeze_gate(stage_role, alternate)))
        assert len(dispatches) == count
        pin = full_pin(ROOT / name)
        check('S2_exact_canonical_' + stage_role + '_path_and_full_pin_positive',
              lambda stage_role=stage_role,name=name,pin=pin: C.stage_source_identity(stage_role, ROOT / name, pin))
        bad = dict(pin, sha256='0' * 64)
        check('S2_wrong_full_source_SHA_' + stage_role + '_rejected',
              lambda stage_role=stage_role,name=name,bad=bad: reject(lambda: C.stage_source_identity(stage_role, ROOT / name, bad)))
        bad_mode = dict(pin, filesystem_mode='0444' if pin['filesystem_mode'] != '0444' else '0644')
        check('S2_wrong_full_source_mode_' + stage_role + '_rejected',
              lambda stage_role=stage_role,name=name,bad_mode=bad_mode: reject(lambda: C.stage_source_identity(stage_role, ROOT / name, bad_mode)))
        aliased_pin = dict(pin, path=str(alternate))
        check('S2_pin_path_alias_' + stage_role + '_rejected',
              lambda stage_role=stage_role,name=name,aliased_pin=aliased_pin: reject(lambda: C.stage_source_identity(stage_role, ROOT / name, aliased_pin)))
        alternate.unlink()
    check('F2_unknown_source_role_rejected', lambda: reject(lambda: C.stage_source_identity('objects', ROOT / 'provider_executor.py')))

    # Exact accepted F1 raw tree: five C3 independent-review leaves are identical
    # at independent_review and historical_submission/independent_review.
    shared_raw = base64.b64decode('MTAwNjQ0IEhBU0hfQU5EX1JFUExBWV9SRUNFSVBULmpzb24AvBD4qXCRU4WK9QXE2hjhHWT1QvsxMDA2NDQgSU5ERVBFTkRFTlRfQ0hFQ0tTLmpzb24ARyZmmAgUmOYrRs5ysA2MRUEF0LYxMDA2NDQgSU5ERVBFTkRFTlRfUkVWSUVXLm1kAOCWli7s9YZ7rFPn6KXk7Kc0cWDkMTAwNjQ0IFJFVklFV19NQU5JRkVTVC5qc29uAI8xwcuBvTEhSwc/xderTBOK294mMTAwNjQ0IGluZGVwZW5kZW50X2NoZWNrcy5weQB+8F2/TxasoVH1Y+upamfXZ7dK1g==', validate=True)
    shared_oid = object_body('tree', shared_raw)
    assert len(shared_raw) == 253 and C.sha(shared_raw) == '581ba96cff4cf5014dc5e4469550a277fc1375c989029b86402ec751d9b9760f'
    assert shared_oid == '33935aba930fe702cfdeb19ab1c5c8968ce2e12c'
    shared_entries = baseline_reader.tree(shared_oid)
    hist = object_body('tree', C.tree_encode({b'independent_review': (b'40000', shared_oid)}))
    core = object_body('tree', C.tree_encode({b'independent_review': (b'40000', shared_oid), b'historical_submission': (b'40000', hist)}))
    duplicated_root = object_body('tree', C.tree_encode({b'core_C3': (b'40000', core)}))
    after_duplicate_rows = baseline_reader.walk(duplicated_root)
    def record(path, ident):
        raw = raw_objects[ident][1]
        return {'directory_b64':base64.b64encode(path).decode(), 'before':empty_root if not path else None,
                'after':ident,'raw_bytes':len(raw),'sha256':C.sha(raw),'body_base64':base64.b64encode(raw).decode()}
    duplicate_records = [record(b'core_C3/independent_review', shared_oid),
                         record(b'core_C3/historical_submission/independent_review', shared_oid),
                         record(b'core_C3/historical_submission', hist),record(b'core_C3',core),record(b'',duplicated_root)]
    def duplicate_positive():
        groups = C.validate_changed_tree_records(duplicate_records, {}, after_duplicate_rows, duplicated_root, empty_root)
        assert len(duplicate_records) == 5 and len(groups) == 4 and groups[shared_oid] == shared_raw
        memory = B.MemoryTrees(baseline_reader, duplicate_records)
        assert memory.walk(duplicated_root) == after_duplicate_rows
    check('F1_exact253byte_accepted_C3_tree_positive_at_two_distinct_paths', duplicate_positive)
    check('F1_missing_distinct_path_record_rejected', lambda: reject(lambda:
          C.validate_changed_tree_records(duplicate_records[1:], {}, after_duplicate_rows, duplicated_root, empty_root)))
    duplicate_path = [dict(v) for v in duplicate_records]; duplicate_path[1]['directory_b64'] = duplicate_path[0]['directory_b64']
    check('F1_duplicate_directory_path_record_rejected', lambda: reject(lambda:
          C.validate_changed_tree_records(duplicate_path, {}, after_duplicate_rows, duplicated_root, empty_root)))
    wrong_binding = [dict(v) for v in duplicate_records]; wrong_binding[0]['directory_b64'] = base64.b64encode(b'core_C3/nonexistent').decode()
    check('F1_wrong_directory_census_binding_rejected', lambda: reject(lambda:
          C.validate_changed_tree_records(wrong_binding, {}, after_duplicate_rows, duplicated_root, empty_root)))
    wrong_before = [dict(v) for v in duplicate_records]; wrong_before[1]['before'] = '4' * 40
    check('F1_wrong_per_path_before_OID_rejected', lambda: reject(lambda:
          C.validate_changed_tree_records(wrong_before, {}, after_duplicate_rows, duplicated_root, empty_root)))
    bad_raw = [dict(v) for v in duplicate_records]; bad_raw[1]['body_base64'] = base64.b64encode(shared_raw + b'x').decode()
    check('F1_nonidentical_repeated_raw_body_rejected', lambda: reject(lambda:
          C.validate_changed_tree_records(bad_raw, {}, after_duplicate_rows, duplicated_root, empty_root)))
    check('F1_MemoryTrees_rejects_nonidentical_repeated_body', lambda: reject(lambda: B.MemoryTrees(baseline_reader, bad_raw)))
    wrong_child_rows = dict(after_duplicate_rows)
    wrong_child_rows[b'core_C3/historical_submission/independent_review/INDEPENDENT_CHECKS.json'] = (b'100644', '5' * 40)
    check('F1_each_repeated_raw_tree_checked_against_own_direct_children', lambda: reject(lambda:
          C.validate_changed_tree_records(duplicate_records, {}, wrong_child_rows, duplicated_root, empty_root)))
    # The complete accepted 38-file C3 selection, with its literal accepted
    # modes/OIDs, runs through the actual rewrite, MemoryTrees and per-path gate.
    # The synthetic empty raw tree has its valid object identity. This is not
    # evidence for an actual full MAIN candidate or any provider acceptance.
    proposal = json.loads((ROOT / 'ALLOWLIST_PROPOSAL.json').read_bytes())
    core_rows = [row for row in proposal['files'] if 'accepted_exact_core_body' in row]
    core_prefix = 'draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/research_findings_checkpoint_20261012/core_C3/'
    accepted = [dict(path='unsolved_math_prioritization/attempts/30005044/' + row['repository_path'].removeprefix(core_prefix),
                     **row['accepted_exact_core_body']) for row in core_rows]
    assert len(accepted) == 38 and C.sha(C.dump(accepted)) == '844922cb8d940fff1980835b80740a909292c53f0cbbb1dd7b90de42361ee55b'
    selected38 = {row['repository_path'].encode(): (row['accepted_exact_core_body']['mode'].encode(),
                   row['accepted_exact_core_body']['oid'], b'') for row in core_rows}
    class EmptyDirectoryProjection:
        def tree(self, ident):
            assert ident == empty_root
            return {}
    changed38 = []
    root38 = B.rewrite_tree(EmptyDirectoryProjection(), empty_root, selected38, rewritten=changed38)
    after38 = B.MemoryTrees(EmptyDirectoryProjection(), changed38).walk(root38)
    def complete38_positive():
        groups = C.validate_changed_tree_records(changed38, {}, after38, root38, empty_root)
        leaves = {p:v for p,v in after38.items() if v[0] != b'40000'}
        assert leaves == {p:v[:2] for p,v in selected38.items()} and len(leaves) == 38
        repeated = [row for row in changed38 if row['after'] == shared_oid]
        expected_paths = {core_prefix.encode().rstrip(b'/') + b'/independent_review',
                          core_prefix.encode().rstrip(b'/') + b'/historical_submission/independent_review'}
        assert len(repeated) == 2 and {base64.b64decode(row['directory_b64']) for row in repeated} == expected_paths
        assert all(base64.b64decode(row['body_base64']) == shared_raw for row in repeated)
        assert len(changed38) == len({row['directory_b64'] for row in changed38})
        assert len(groups) < len(changed38)
    check('S1_complete_exact38_accepted_C3_builder_and_path_gate_positive_with_two_identical_raw_trees', complete38_positive)
    duplicate38 = [dict(row) for row in changed38]
    duplicate38.append(dict(changed38[0]))
    check('S1_complete_exact38_duplicate_directory_path_rejected', lambda: reject(lambda:
          C.validate_changed_tree_records(duplicate38, {}, after38, root38, empty_root)))
    inconsistent38 = [dict(row) for row in changed38]
    shared_index = next(i for i,row in enumerate(inconsistent38) if row['after'] == shared_oid)
    invalid_body = shared_raw + b'x'
    inconsistent38[shared_index].update(body_base64=base64.b64encode(invalid_body).decode(),
                                      raw_bytes=len(invalid_body), sha256=C.sha(invalid_body))
    check('S1_complete_exact38_inconsistent_same_raw_OID_rejected_despite_valid_size_SHA', lambda: reject(lambda:
          C.validate_changed_tree_records(inconsistent38, {}, after38, root38, empty_root)))
    # Fully verify Root's exact dated saved snapshot, with zero actual dispatch.
    certificate_pin=proposal['Root_current_certificate_dated_control_input']
    certificate_selection={'current_baseline_certificate':certificate_pin,
            'current_baseline_certificate_sha256':certificate_pin['sha256']}
    certificate=C.read_current_certificate(certificate_selection)
    closed_inputs={role:C.file_pin(pin,base=C.AUDIT) for role,pin in C.CLOSED_HISTORICAL_INPUT_PINS.items()}
    closed_inputs.update({role:C.file_pin(pin,base=C.AUDIT) for role,pin in certificate['input_pins'].items()})
    peer_payload=json.loads(closed_inputs['peer_delta']);foreign_payload=json.loads(closed_inputs['foreign_delta'])
    protected={row['path'].encode() for row in peer_payload['changes']+foreign_payload['changes']}
    current_selection={'baseline_counts':C.certificate_counts(certificate,protected),
        'peer_delta_literal_paths':[row['path'] for row in peer_payload['changes']],
        'foreign_delta_literal_paths':[row['path'] for row in foreign_payload['changes']],
        'foreign_delta_all_entry_paths':[row['path'] for row in foreign_payload['all_entry_changes']],
        'peer_delta_record_sha256':C.sha(closed_inputs['peer_delta']),
        'foreign_delta_record_sha256':C.sha(closed_inputs['foreign_delta'])}
    def saved_full_baseline_positive():
        context=C.validate_baseline_context(current_selection,closed_inputs,
                     {row['repository_path'].encode() for row in proposal['files']},certificate)
        assert len(context['current_rows'])==certificate['current_counts']['all_entries']
        assert len(context['protected_paths'])==len(protected) and len(context['peer_paths'])==76
        assert len(context['foreign_paths'])==certificate['foreign_leaf_count']
        assert len(context['foreign_all_paths'])==certificate['foreign_all_entry_count']
    check('V04_complete_saved_actual_current_ADC_1de_censuses_nested_support_and_exact_delta_positive',saved_full_baseline_positive)
    def wrong_cert_digest():
        invalid=dict(certificate_selection,current_baseline_certificate_sha256='0'*64)
        C.read_current_certificate(invalid)
    check('V04_certificate_selection_digest_mismatch_rejected',lambda:reject(wrong_cert_digest))
    invalid_cert_pin=dict(certificate_pin,filesystem_mode='0644')
    check('V04_certificate_full_mode_mismatch_rejected',lambda:reject(lambda:
        C.read_current_certificate(dict(certificate_selection,current_baseline_certificate=invalid_cert_pin))))
    invalid_cert=json.loads(json.dumps(certificate));invalid_cert['current_counts']['leaves']+=1
    check('V04_certificate_wrong_current_count_rejected_by_actual_full_census',lambda:reject(lambda:
        C.validate_baseline_context(current_selection,closed_inputs,set(),invalid_cert)))
    invalid_cert=json.loads(json.dumps(certificate));invalid_cert['current_tree']='8'*40
    check('V04_certificate_wrong_current_root_rejected_by_full_raw_commit',lambda:reject(lambda:
        C.validate_baseline_context(current_selection,closed_inputs,set(),invalid_cert)))
    actual_guard=json.loads(closed_inputs['main_continuation_guard'])
    invalid_guard=json.loads(json.dumps(actual_guard));invalid_guard['ancestry_path']=invalid_guard['ancestry_path'][::2]+[C.ADC]
    check('V04_incomplete_or_nonedge_raw_ancestry_rejected',lambda:reject(lambda:
        C.validate_snapshot_support(invalid_guard,certificate,closed_inputs,Path(certificate['reader_context']['root']))))
    invalid_guard=json.loads(json.dumps(actual_guard));invalid_guard['ancestry_raw_commit_pins'][C.ADC]['sha256']='0'*64
    check('V04_nested_ancestry_full_SHA_mismatch_rejected',lambda:reject(lambda:
        C.validate_snapshot_support(invalid_guard,certificate,closed_inputs,Path(certificate['reader_context']['root']))))
    terminal_body=b'tree '+empty_root.encode()+b'\nauthor A <a@example.test> 1 +0000\ncommitter A <a@example.test> 1 +0000\n\nterminal\n'
    terminal_oid=C.oid('commit',terminal_body)
    merge_body=b'tree '+empty_root.encode()+b'\nparent '+('7'*40).encode()+b'\nparent '+terminal_oid.encode()+b'\nauthor A <a@example.test> 2 +0000\ncommitter A <a@example.test> 2 +0000\n\nmerge\n'
    merge_oid=C.oid('commit',merge_body);raw_ancestry={merge_oid:merge_body,terminal_oid:terminal_body}
    check('V04_raw_ancestry_valid_second_parent_edge_and_ordered_multi_parent_positive',lambda:
        C.validate_raw_ancestry([merge_oid,terminal_oid],raw_ancestry))
    bad_edge_body=merge_body.replace(terminal_oid.encode(),('8'*40).encode());bad_edge_oid=C.oid('commit',bad_edge_body)
    check('V04_raw_ancestry_non_parent_edge_rejected',lambda:reject(lambda:
        C.validate_raw_ancestry([bad_edge_oid,terminal_oid],{bad_edge_oid:bad_edge_body,terminal_oid:terminal_body})))
    wrong_census=dict(baseline_reader.walk(root));wrong_census[b'dir/child']=(b'100644','7'*40)
    check('V04_complete_census_changed_inner_leaf_rejected_by_directory_Merkle',lambda:reject(lambda:
        C.validate_complete_census(wrong_census,root)))
    check('V04_complete_raw_fixture_census_Merkle_positive',lambda:
        C.validate_complete_census(baseline_reader.walk(root),root))
    # Old peer paths may validly change or disappear before the current snapshot;
    # a checkpoint conserves these current values/absences, never restores ADC.
    overlapping_peer={b'keep',b'delete',b'mode'};overlapping_foreign={b'delete',b'mode',b'add'}
    current_foreign={b'keep':(b'100644','1'*40),b'mode':(b'100755','3'*40),b'add':(b'100644','4'*40)}
    def overlap_current_positive():
        union=C.protected_current_paths(overlapping_peer,overlapping_foreign,{b'own/new'},current_foreign)
        assert len(union)==4 and b'delete' not in current_foreign and current_foreign[b'mode'][0]==b'100755'
        assert C.certificate_counts(certificate,union)['protected_leaf_paths']==4
    check('V04_historical_peer_overlap_current_modification_deletion_and_union_positive',overlap_current_positive)
    check('V04_selected_deleted_protected_path_recreation_rejected',lambda:reject(lambda:
        C.protected_current_paths(overlapping_peer,overlapping_foreign,{b'delete'},current_foreign)))
    check('V04_selected_descendant_of_protected_current_absence_rejected',lambda:reject(lambda:
        C.protected_current_paths(overlapping_peer,overlapping_foreign,{b'delete/new'},current_foreign)))
    delta_before={b'keep':(b'100644','1'*40),b'delete':(b'120000','2'*40),b'mode':(b'100644','3'*40)}
    delta_after={b'keep':(b'100644','1'*40),b'add':(b'100644','4'*40),b'mode':(b'100755','3'*40)}
    delta_rows=C.entry_delta(delta_before,delta_after)
    check('V04_delta_records_include_add_delete_and_mode_changes_positive',lambda:
          C.validate_delta_records(delta_rows,delta_before,delta_after,3))
    check('V04_delta_missing_deletion_rejected',lambda:reject(lambda:
          C.validate_delta_records([row for row in delta_rows if row['path']!='delete'],delta_before,delta_after,3)))
    check('V04_delta_duplicate_path_rejected',lambda:reject(lambda:
          C.validate_delta_records(delta_rows+[dict(delta_rows[0])],delta_before,delta_after,3)))
    bad_mode_rows=json.loads(json.dumps(delta_rows));bad_mode_rows[-1]['after']['mode']='100644'
    check('V04_delta_wrong_mode_rejected',lambda:reject(lambda:
          C.validate_delta_records(bad_mode_rows,delta_before,delta_after,3)))
    check('V04_delta_wrong_total_count_rejected',lambda:reject(lambda:
          C.validate_delta_records(delta_rows,delta_before,delta_after,2)))
    fake_actual={'schema':'pr262-root-actual-corrected-draft-acceptance-v4','checkpoint_source_version':'preparation_v04',
         'actual_corrected_author_commit':'b0331c437befd85331056097974a630b41621e1d',
         'full_provider_readback_accepted':True,'actual_ref_verified':True,
         'actual_MAIN_unchanged':C.ADC,'actual_MAIN_root':C.ADC_TREE,
         'fresh_author_stage_main_guard_accepted':True,'PR_OPEN_DRAFT_unmerged_unclosed':True,
         'full_metadata_readback_accepted':True,'accepted_PR_title':'Inert accepted fixture',
         'accepted_PR_body_sha256':C.sha(b'inert accepted body'),
         'actual_provider_acceptance_support':[full_pin(gh_fixture)]}
    acceptance_selection={'corrected_author_head':fake_actual['actual_corrected_author_commit'],
        'corrected_PR_metadata':{'title':fake_actual['accepted_PR_title'],'body_sha256':fake_actual['accepted_PR_body_sha256']}}
    check('V04_actual_author_metadata_interface_separate_from_later_current_MAIN_positive',lambda:
          C.validate_actual_author_acceptance(fake_actual,acceptance_selection,certificate))
    for label,change in [('unaccepted_metadata',{'full_metadata_readback_accepted':False}),
                         ('wrong_accepted_title',{'accepted_PR_title':'changed'}),
                         ('old_source_version',{'checkpoint_source_version':'preparation_v03'}),
                         ('unaccepted_author_guard',{'fresh_author_stage_main_guard_accepted':False}),
                         ('missing_actual_support',{'actual_provider_acceptance_support':[]})]:
        invalid_actual=dict(fake_actual,**change)
        check('V04_mock_actual_acceptance_'+label+'_rejected',lambda invalid_actual=invalid_actual:
              reject(lambda:C.validate_actual_author_acceptance(invalid_actual,acceptance_selection,certificate)))
    saved_api=C.api
    accepted_pr={'number':262,'state':'open','draft':True,'merged':False,'merged_at':None,
        'title':fake_actual['accepted_PR_title'],'body':'inert accepted body',
        'head':{'sha':fake_actual['actual_corrected_author_commit'],'ref':'dot/math-30005044','repo':{'full_name':C.REPO}},
        'base':{'ref':'main','sha':'historical base only','repo':{'full_name':C.REPO}}}
    C.api=lambda *args:accepted_pr
    check('V04_live_PR_corrected_author_and_title_body_positive_historical_base_not_MAIN',lambda:
        C.fresh_pr(acceptance_selection,None,'INERT_PR'))
    accepted_pr['body']='changed body'
    check('V04_live_PR_body_drift_rejected',lambda:reject(lambda:C.fresh_pr(acceptance_selection,None,'INERT_PR')))
    accepted_pr['body']='inert accepted body';accepted_pr['title']='changed title'
    check('V04_live_PR_title_drift_rejected',lambda:reject(lambda:C.fresh_pr(acceptance_selection,None,'INERT_PR')))
    C.api=saved_api
    foreign_before={b'foreign':(b'40000','1'*40),b'foreign/keep':(b'100644','2'*40)}
    foreign_after=dict(foreign_before);foreign_after[b'foreign']=(b'40000','3'*40)
    check('V04_foreign_shared_ancestor_rewrite_preserves_current_foreign_leaf_positive',lambda:
        C.foreign_current_entries_preserved(foreign_before,foreign_after,set(foreign_before),{b'foreign/own_new'}))
    foreign_after[b'foreign/keep']=(b'100644','4'*40)
    check('V04_foreign_leaf_changed_under_shared_ancestor_rejected',lambda:reject(lambda:
        C.foreign_current_entries_preserved(foreign_before,foreign_after,set(foreign_before),{b'foreign/own_new'})))
    binding_proof={'selection_sha256':C.sha(b'inert final selection'),
                   'baseline_certificate_sha256':certificate_pin['sha256']}
    for stage_schema in ['pr262-main-findings-created-objects-v4','pr262-main-findings-full-readback-v4']:
        stage_acceptance=dict(binding_proof,schema=stage_schema,source_version='preparation_v04')
        check('V04_'+stage_schema+'_exact_source_selection_certificate_binding_positive',lambda:
            E.validate_stage_binding(stage_acceptance,binding_proof,stage_schema))
        for field,value in [('source_version','preparation_v03'),('selection_sha256','0'*64),
                            ('baseline_certificate_sha256','0'*64)]:
            invalid=dict(stage_acceptance,**{field:value})
            check('V04_'+stage_schema+'_'+field+'_mismatch_rejected',lambda invalid=invalid:
                reject(lambda:E.validate_stage_binding(invalid,binding_proof,stage_schema)))
    for namespace in ['actual_execution_v04','root_final_freeze_v04','private_candidate_v04','remote_objects']:
        check('V04_private_namespace_'+namespace+'_excluded_from_publication',lambda namespace=namespace:
              reject(lambda:C.allowed_repo_path('draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/research_findings_checkpoint_20261012/'+namespace+'/capture.json')))
    # A preexisting later capture means the whole stage root is occupied; zero
    # provider/Git calls occur before rejection, even with safe earlier captures.
    for late in ['later.stderr', 'MAIN_CAS.STARTED.json', 'FINAL_ACCEPTANCE.json', 'remote.git/config']:
        occupied = fixture / ('occupied_' + str(len(results))); (occupied / late).parent.mkdir(parents=True)
        (occupied / late).write_bytes(b'occupied')
        count = len(dispatches)
        check('D5_late_' + late.replace('/', '_') + '_zero_dispatch', lambda occupied=occupied:
              reject(lambda: C.Stage(occupied, ['early.stdout', 'later.stderr', 'MAIN_CAS.STARTED.json', 'FINAL_ACCEPTANCE.json', 'STAGE_COMPLETED.json'], ['remote.git'])))
        assert len(dispatches) == count
    unsafe = fixture / 'unsafe'; unsafe.mkdir(); (unsafe / 'late.stderr').symlink_to(fixture / 'canary')
    count = len(dispatches)
    check('D5_dangling_late_output_symlink_zero_dispatch', lambda:
          reject(lambda: C.Stage(unsafe, ['early.stdout', 'late.stderr', 'STAGE_COMPLETED.json'])))
    assert len(dispatches) == count and not (fixture / 'canary').exists()
    positive = C.Stage(fixture / 'reservation_positive', ['A.stdout', 'A.stderr', 'A.STARTED.json', 'FINAL.json', 'STAGE_COMPLETED.json'])
    check('whole_capture_set_held_exclusive_before_mock_first_dispatch', lambda:
          C.require(all((positive.root / n).is_file() and (positive.root / n).stat().st_size == 0 for n in positive.handles), 'Not all capture handles reserved'))
    positive.json('A.STARTED.json', {'inert': True}); positive.write('A.stdout', b'OK'); positive.write('A.stderr', b'')
    positive.json('FINAL.json', {'inert': True}); positive.finish()
    check('occupied_stage_tombstone_prohibits_retry', lambda: reject(lambda: C.Stage(positive.root, ['STAGE_COMPLETED.json'])))
    replace_stage = C.Stage(fixture / 'replacement', ['capture', 'STAGE_COMPLETED.json'])
    (replace_stage.root / 'capture').unlink(); (replace_stage.root / 'capture').write_bytes(b'replacement')
    check('held_capture_inode_replacement_rejected', lambda: reject(lambda: replace_stage.write('capture', b'new')))
    for fd, _ in replace_stage.handles.values(): os.close(fd)
    rows = baseline_reader.walk(root)
    proof = {'sole_parent':fixture_parent,'candidate_commit': commit, 'candidate_tree': root, 'candidate_leaf_count': 4,
             'candidate_directory_count': 1, 'after_full_raw_census_sha256': C.sha(C.census(rows))}
    artifacts = {'raw_commit': raw_commit, 'full_rows': C.gzip.compress(C.census(rows), mtime=0)}
    names = ['EMPTY_STORE_BEFORE_INIT.json', 'REMOTE_INIT.stdout', 'REMOTE_INIT.stderr', 'REMOTE_FETCH.stdout',
             'REMOTE_FETCH.stderr', 'REMOTE_COMMIT.raw', 'REMOTE_FULL_ROWS.nul.gz', 'REMOTE_PROOF.json', 'STAGE_COMPLETED.json']
    remote_stage = C.Stage(fixture / 'remote_positive', names, ['remote.git', 'remote_objects', 'templates'])
    def mock_git_capture(selection_arg, stage, name, args, env, input_body=None, timeout=60):
        # This mock performs no actual Git operation. All future captures and the
        # full initially empty namespace must already exist at the first call.
        assert all((stage.root / n).is_file() for n in names)
        assert env.get('GIT_NO_LAZY_FETCH') == '1' and 'GIT_ALTERNATE_OBJECT_DIRECTORIES' not in env
        dispatches.append({'mock': name, 'argv': args})
        if name == 'REMOTE_INIT': (stage.root / 'remote.git/config').write_bytes(config)
        stage.write(name + '.stdout', b''); stage.write(name + '.stderr', b''); return b''
    E.run_capture = mock_git_capture
    E.owned_reader = lambda s, d, o, r: C.owned_reader(s, d, o, r, process_module=FakePopen)
    check('actual_empty_remote_readback_method_full_exact_Reader_walk_positive', lambda:
          E.empty_remote_readback(selection, remote_stage, proof, artifacts))
    check('baseline_reader_context_unchanged_after_remote_positive', lambda:
          C.require((baseline_module.ROOT, baseline_module.DRIVER, baseline_module.OBJECTS) == saved_driver_context,
                    'Fresh remote context corrupted baseline context'))
    check('historical_payload_map_unchanged_no_restoration_alias', lambda:
          C.require(original_payload_entries == before_payload, 'Original payload map overwritten'))
    check('remote_pipe_closed_after_full_positive', lambda: C.require(processes[-1].closed, 'Remote reader not closed'))
    assert remote_stage.root.joinpath('REMOTE_COMMIT.raw').read_bytes() == raw_commit
    assert C.gzip.decompress(remote_stage.root.joinpath('REMOTE_FULL_ROWS.nul.gz').read_bytes()) == C.census(rows)
    remote_stage.finish(); baseline_reader.close()
    check('all_exact_Reader_pipes_closed', lambda: C.require(all(p.closed for p in processes), 'Pipe leaked'))
    # Fail through the actual remote method when the prepared full census differs.
    bad_stage = C.Stage(fixture / 'remote_bad', names, ['remote.git', 'remote_objects', 'templates'])
    wrong = dict(artifacts, full_rows=C.gzip.compress(b'wrong', mtime=0))
    check('actual_remote_method_census_mismatch_fails_and_closes_reader', lambda:
          reject(lambda: E.empty_remote_readback(selection, bad_stage, proof, wrong)))
    assert processes[-1].closed
    for fd, _ in bad_stage.handles.values(): os.close(fd)

receipt = {'schema': 'pr262-new-main-findings-small-mechanism-controls-v4', 'UTC': C.utc(),
           'status': 'V04_NEW_BASELINE_SOURCE_CONTROLS_ONLY_NEW_WHOLE_INDEPENDENT_REVIEW_REQUIRED',
           'control_count': len(results), 'all_controls_pass': True, 'controls': results,
           'source_pins': {n: full_pin(ROOT / n) for n in ['checkpoint_common.py','private_builder.py','provider_executor.py','baseline_reader_v02.py','mock_controls.py']},
           'control_input_pins': {'allowlist_proposal': full_pin(ROOT / 'ALLOWLIST_PROPOSAL.json'),
                                  'fixed_historical_baseline':C.CLOSED_HISTORICAL_INPUT_PINS,
                                  'dated_actual_current_certificate':certificate_pin},
           'exact38_projection': {'accepted_leaf_count':38, 'complete_target_list_sha256':C.sha(C.dump(accepted)),
               'per_path_ancestor_count':len(changed38), 'distinct_tree_object_count':len({row['after'] for row in changed38}),
               'repeated_tree_OID':shared_oid, 'repeated_paths_checked':2, 'synthetic_empty_baseline_projection_only':True},
           'mock_transport_events': len(dispatches), 'actual_subprocess_Git_network_provider_dispatches': 0,
           'primary_git_access': 0, 'temporary_fixtures_removed': True,
           'independent_review': False, 'actual_full_current_candidate_or_provider_acceptance': False,
           'future_Root_new_whole_source_and_candidate_reviews_required': True}
output = ROOT / 'CONTROL_RESULTS.json'
assert not os.path.lexists(output), 'No control receipt overwrite'
with output.open('xb') as f: f.write(C.dump(receipt))
print(json.dumps({'controls': len(results), 'all_pass': True, 'actual_dispatches': 0}))
