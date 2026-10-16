"""Offline AST/fixture audit. No production module imports or remote calls."""
from pathlib import Path
import ast, copy, datetime, difflib, hashlib, io, json, re, shutil, tempfile, types, zipfile
from contextlib import redirect_stdout

D = Path(__file__).resolve().parent
A = D.parent
SCRIPTS = ['run_zenodo_step.py', 'record_tracker.py', 'prepare_native_final_01.py',
           'prepare_final_main_scope.py', 'prepare_final_scoped_merge.py',
           'prepare_factual_completion.py', 'run_review_repair_checkpoint_02.py']

def require(value, message):
    if not value:
        raise RuntimeError(message)

def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def function(path, name, env):
    tree = ast.parse(path.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), str(path), 'exec'), env)
    return env[name]

out = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(),
       'audit_mode': 'AST functions and disposable fixtures only; no production imports, subprocesses, Git, APIs, or environment access',
       'script_pins': {n: pin(A/n) for n in SCRIPTS}}
for n in SCRIPTS:
    ast.parse((A/n).read_text())
out['all_seven_scripts_parse'] = True
out['publication_gate_currently_absent'] = not (A/'ROOT_PUBLICATION_GATE.json').exists()

# Derive the real existing authored scope using only the two scope functions.
scope_env = {'A': A, 'Path': Path, 'json': json, 'require': require}
math_scope = function(A/'prepare_mathematical_checkpoint.py', 'scope', scope_env)
dummy_spec = types.SimpleNamespace(loader=types.SimpleNamespace(exec_module=lambda module: None))
dummy_importlib = types.SimpleNamespace(util=types.SimpleNamespace(
    spec_from_file_location=lambda *args: dummy_spec,
    module_from_spec=lambda spec: types.SimpleNamespace(scope=math_scope)))
own_env = {'A': A, 'Path': Path, 'json': json, 'require': require, 'importlib': dummy_importlib}
names = function(A/'run_review_repair_checkpoint_02.py', 'own_paths', own_env)()
bad_paths = [n for n in names if any(x in n.lower() for x in ['private', 'chrome', '.zenodo', '__pycache__', 'preappend_fresh_read']) or '..' in Path(n).parts]
require(not bad_paths, 'Unexpected unsafe scope path')
out['current_checkpoint_scope'] = {'case_files': len(names), 'bad_paths': bad_paths,
    'all_paths_within_case': all((A/n).resolve().is_relative_to(A.resolve()) for n in names),
    'all_existing_files': all((A/n).is_file() for n in names),
    'symlinks': [n for n in names if (A/n).is_symlink()]}
out['authored_scope_names_sha256'] = hashlib.sha256(('\n'.join(names)+'\n').encode()).hexdigest()
(D/'CHECKED_SCOPE_PATHS.json').write_text(json.dumps(names, indent=2)+'\n')
secret_rx = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer [A-Za-z0-9_-]{20,})')
secrets=[]; suspect=[]; zip_bad=[]
for n in names:
    p=A/n
    if secret_rx.search(p.read_bytes()):secrets.append(n)
    if any(t in n.lower() for t in ['primary_body','fulltext','full_text','source.pdf','raw_response','preappend','cache','token','secret']):suspect.append(n)
    if p.suffix=='.zip':
        with zipfile.ZipFile(p) as archive:
            for member in archive.namelist():
                if any(t in member.lower() for t in ['private','chrome','.zenodo','__pycache__','preappend_fresh_read','primary_body','fulltext','full_text']):zip_bad.append([n,member])
safety={'selected_case_files':len(names),'high_specificity_secret_pattern_matches':secrets,
    'suspicious_name_candidates':suspect,'forbidden_archive_member_names':zip_bad,
    'scope':'Current authored scope and archive member names only; private source directories and full spreadsheet read were not opened. Heuristics do not prove universal absence of secrets.'}
(D/'SAFE_SCOPE_CHECK.json').write_text(json.dumps(safety,indent=2)+'\n')
out['safe_scope_check']=safety

# Check existing packet pins, native pins and historical custody without executing science.
cur = json.loads((A/'integration_preparation/CURRENT_TEMPLATE.json').read_text())
native = A/'integration_preparation'/cur['current_template']
require(cur['current_template'] == 'native_template_pending_02', 'Predecessor changed')
require(all(pin(native/n) == x for n,x in cur['files'].items()), 'Native manifest drift')
original = json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
require(len(original['files']) == 22, 'Original custody count')
for x in original['files']:
    n = Path(x['path']).relative_to('unsolved_math_prioritization/attempts/5000007')
    require(pin(native/'historical_original'/n) == {'bytes': x['bytes'], 'sha256': x['sha256']}, 'Original custody drift')
packet = json.loads((A/'publication_package_v2/FINAL_REVIEW_PACKET_MANIFEST.json').read_text())
require(all(pin(A/'publication_package_v2'/n) == x for n,x in packet['payloads'].items()), 'Packet drift')
out['native_and_packet_identity'] = {'native_files': len(cur['files']), 'historical_original_files': 22,
    'all_49_native_pins_match': True, 'all_22_original_pins_match': True, 'all_5_packet_pins_match': True}
tree = ast.parse((A/'prepare_native_final_01.py').read_text())
counts = {}
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'replace':
        n, needle = map(ast.literal_eval, node.args[:2])
        counts[n] = (native/n).read_text().count(needle)
require(list(counts.values()) == [1,1,1], 'Nonunique replacement')
out['native_replacement_counts'] = counts

# Execute the exact factual native propagator only in a disposable local copy.
with tempfile.TemporaryDirectory(prefix='native_fixture_', dir=D) as temp:
    F = Path(temp)
    (F/'integration_preparation').mkdir()
    shutil.copytree(native, F/'integration_preparation'/native.name)
    (F/'integration_preparation/CURRENT_TEMPLATE.json').write_text(json.dumps(cur))
    (F/'ORIGINAL_FILE_MANIFEST.json').write_text(json.dumps(original))
    gate = {'status': 'READY_FOR_AUTHORIZED_PUBLICATION', 'package_name': str(A/'publication_package_v2'),
            'payloads': {n:{'SHA256': x['sha256']} for n,x in packet['payloads'].items()}}
    (F/'ROOT_PUBLICATION_GATE.json').write_text(json.dumps(gate))
    (F/'ZENODO_PUBLICATION_READBACK.json').write_text(json.dumps({'state':'published','doi':'10.0000/AUDIT-MOCK',
         'doi_url':'https://example.invalid/AUDIT-MOCK','record_url':'https://example.invalid/AUDIT-MOCK-RECORD'}))
    (F/'TRACKER_ACCEPTANCE.json').write_text(json.dumps({'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED',
         'DOI':'10.0000/AUDIT-MOCK','range':"'Math Puzzles'!A999:D999"}))
    with redirect_stdout(io.StringIO()):
        exec(compile((A/'prepare_native_final_01.py').read_text(), str(A/'prepare_native_final_01.py'), 'exec'),
             {'__file__': str(F/'prepare_native_final_01.py'), '__name__':'audit_fixture'})
    final = json.loads((F/'integration_preparation/CURRENT_TEMPLATE.json').read_text())
    changed = [n for n,x in cur['files'].items() if pin(F/'integration_preparation/native_template_final_01'/n) != x]
    new = sorted(set(final['files'])-set(cur['files']))
    require(changed == sorted(final['only_factual_status_documents_changed'][:-1]) or set(changed) == set(final['only_factual_status_documents_changed'])-set(new), 'Unexpected factual changes')
    require(all(not n.startswith('historical_original/') for n in changed), 'Historical bytes changed')
    out['native_final_fixture'] = {'changed_existing': sorted(changed), 'new_files': new,
        'unchanged_existing_count':len(cur['files'])-len(changed), 'all_22_historical_originals_unchanged':True,
        'scientific_proof_scripts_outputs_and_data_unchanged': all(n not in changed for n in cur['files'] if n.endswith('.py') or n in ['PROOF_V2.md','check_certificate_output.json','check_half_turn_output.json','independent_review/reviewer_exact_check_output.json']),
        'actual_packet_pins_after_fixture_match':all(pin(A/'publication_package_v2'/n) == x for n,x in packet['payloads'].items())}

# Evaluate the actual update/delete statements, never the network/file operations.
live = json.loads((D/'LIVE_MAIN_ALIAS_OBSERVATION.json').read_text())
j0 = {**live['top_level_scalars'], **live['selected_live_collections']}
common = {'stamp':'AUDIT-MOCK', 'z':{'doi':'10.0000/AUDIT-MOCK','doi_url':'https://example.invalid/AUDIT-MOCK'},
          'tr':{'range':"'Math Puzzles'!A999:D999"}, 'a':{'merge_commit':'AUDIT-MOCK-MERGE'},
          'm':types.SimpleNamespace(HEAD='0c3346c8ebcb3b967a1d8bf9a283f027b44b738c'),
          'comp':{'status':'AUDIT-MOCK-COMPLETE'}, 'require':require}
def update_postimage(script, which):
    nodes = ast.parse((A/script).read_text()).body
    f = next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name == 'prepare')
    selected = []
    for n in f.body:
        text = ast.get_source_segment((A/script).read_text(), n) or ''
        if which == 'integration' and isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id == 'j' and n.value.func.attr == 'update':
            selected.append(n)
        elif which == 'factual' and n.lineno >= 17 and n.lineno <= 22:
            selected.append(n)
    env = {**common, 'j':copy.deepcopy(j0)}
    exec(compile(ast.fix_missing_locations(ast.Module(body=selected,type_ignores=[])),script,'exec'),env)
    return env['j']
integration = update_postimage('prepare_final_scoped_merge.py','integration')
factual = update_postimage('prepare_factual_completion.py','factual')
aliases = ['fully_completed_count','published_count','fully_completed_fraction_percent','workflow_estimate_percent',
 'last_completed_PR','last_completed_actual_final_receipt','last_completed_writer_operation_finished',
 'actual_factual_checkpoint_accepted','active_checkpoint_acceptance_receipt','active_checkpoint_commit',
 'program_snapshot_authority_condition','remaining_current_step','next_step','latest_ordered_intake_record',
 'last_actual_intake_checkpoint_commit','last_actual_intake_checkpoint_release','read_only_next_case','current_PR','next_numeric_intake_cursor',
 'current_publication_package_reviews_complete','advance_to_next_PR_authorized_now']
out['actual_AST_postimage_aliases'] = {k:{'live':j0.get(k),'integration95':integration.get(k),'factual100':factual.get(k)} for k in aliases}
case = json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
f = next(n for n in ast.parse((A/'prepare_factual_completion.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name == 'prepare')
case_update = next(n for n in f.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id == 'case' and n.value.func.attr == 'update')
env = {**common, 'case':copy.deepcopy(case),'comp':{'status':'AUDIT-MOCK-COMPLETE'}}
exec(compile(ast.fix_missing_locations(ast.Module(body=[case_update],type_ignores=[])),'case-update','exec'),env)
out['case_whole_package_reviews_complete_after_factual_update'] = env['case'].get('whole_package_reviews_complete')

# Counterexample: exact accept() passes while an unchecked native file differs at an ahead MAIN tip.
PREFIX='draft_pr_publication_program_20260930/'
CASE=PREFIX+'audits/pr190_5000007/'
NATIVE='unsolved_math_prioritization/attempts/5000007/'
HEAD='0c3346c8ebcb3b967a1d8bf9a283f027b44b738c'
checked=[NATIVE+n for n in ['PROOF_V2.md','check_certificate.py','independent_review/reviewer_exact_check.py','source_record.json','prior_imported_report.json']]+[CASE+'publication_package_v2/'+n for n in ['dodecahedron_endpoint.tex','zenodo-deposit.json']]+[CASE+'TRACKER_ACCEPTANCE.json']
omitted=NATIVE+'check_half_turn.py'
body=b'AUDIT EXPECTED SCIENTIFIC BYTES\n'
ident={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'git_blob':'a'*40}
record={'commit':'prepared','tree':'prepared-tree','expected_main':'old-main','parent_tree':'old-tree',
        'selected_files':{n:ident for n in checked+[omitted]},'changed_paths':checked+[omitted],
        'DOI':'10.0000/AUDIT-MOCK','tracker_range':"'Math Puzzles'!A999:D999"}
class MockPath:
    def __truediv__(self,n):return self
    def read_text(self):return json.dumps(record)
reads=[]; saves=[]
def mock_api(endpoint):
    if endpoint == 'git/commits/prepared':return {'tree':{'sha':'prepared-tree'},'parents':[{'sha':'old-main'},{'sha':HEAD}]}
    if endpoint == 'git/ref/heads/main':return {'object':{'sha':'ahead-main-with-mutated-halfturn'}}
    if endpoint.startswith('compare/'):return {'status':'ahead'}
    if endpoint == 'pulls/190':return {'merged':True,'state':'closed','head':{'sha':HEAD},'merge_commit_sha':'prepared'}
    raise RuntimeError('Unexpected mock endpoint '+endpoint)
def mock_body_at(n,ref):
    reads.append(n)
    return b'WRONG HALF TURN SCIENCE\n' if n == omitted else body
warm=types.SimpleNamespace(warm_selected_directories=lambda *args:None)
env={'A':MockPath(),'json':json,'hashlib':hashlib,'require':require,'api':mock_api,
     'm':types.SimpleNamespace(m=types.SimpleNamespace(h=warm)),
     'lookup':lambda t,n:('100644','blob','a'*40), 'changed_leaves':lambda a,b:set(record['changed_paths']),
     'body_at':mock_body_at,'gates':lambda:({'package_name':'publication_package_v2'},None,None),
     'save':lambda p,j:saves.append(j),'now':lambda:'AUDIT-MOCK','HEAD':HEAD,'NATIVE':NATIVE,'CASE':CASE}
with redirect_stdout(io.StringIO()):
    function(A/'prepare_final_scoped_merge.py','accept',env)()
out['ahead_MAIN_mutated_unchecked_native_counterexample'] = {'accept_returned_success':bool(saves),
    'wrong_file':omitted, 'wrong_file_freshly_read':omitted in reads,
    'acceptance_claim':saves[0]['actual_native_scientific_and_metadata_bytes_accepted'],
    'fresh_body_count':len(reads), 'note':'Mock only, demonstrates absent current-tip identity check; no API called.'}

# Controls for Root's proposed repair. Exact expected identities belong to selected
# paths only; the current tree is authoritative, while unrelated paths may change.
def selected_current_match(expected, actual):
    return all(actual.get(n) == value for n,value in expected.items())
merged_expected = {n:('100644','blob','a'*40) for n in checked+[omitted]}
current_good = dict(merged_expected)
current_good['foreign/unrelated.txt'] = ('100644','blob','b'*40)
current_bad = {**current_good, omitted:('100644','blob','c'*40)}
factual_overlay = {CASE+'CURRENT_CASE_STATUS.json':('100644','blob','d'*40),
                   CASE+'TRACKER_ACCEPTANCE.json':merged_expected[CASE+'TRACKER_ACCEPTANCE.json']}
combined = {**merged_expected, **factual_overlay}
factual_good = {**current_good, **factual_overlay}
factual_bad = {**factual_good, omitted:('100644','blob','c'*40)}
require(selected_current_match(merged_expected,current_good), 'Foreign control failed')
require(not selected_current_match(merged_expected,current_bad), 'Mutated science escaped proposed merge guard')
require(selected_current_match(combined,factual_good), 'Intentional factual override failed')
require(not selected_current_match(combined,factual_bad), 'Mutated science escaped combined factual guard')
out['proposed_current_tip_identity_controls'] = {'merge_rejects_unchecked_science_change':True,
    'merge_allows_unrelated_foreign_change':True, 'factual_prepare_rejects_selected_merge_drift':True,
    'factual_accept_allows_intentional_overlay_override':True,
    'factual_accept_rejects_unexpected_native_change':True,
    'limitation':'Mechanism-level controls only; Root has not yet implemented the repair in the audited scripts.'}

# Allowlists accept the two documented schemas. Whole reviewer 02 is still active.
out['safe_schema_smoke'] = {k:list(j.get('files',j.get('key_files'))) for k,j in {
    'files_list':{'files':['x']},'key_files_list':{'key_files':['x']},'files_map':{'files':{'x':{}}}}.items()}
out['review02_allowlist_currently_absent'] = not (A/'whole_package_review_02/SAFE_AUTHORED_ALLOWLIST.json').exists()
out['tracker_private_full_read_excluded'] = 'sheets_tracking/PREAPPEND_FRESH_READ.stdout.json' not in names

# Rebuild generation helpers into in-memory strings only. The lifecycle utility is
# truncated before its mkdir and external read-only preflight, neither is run.
generated={}
def capture_generated(path, body):generated[path.name]=body
class CaptureWrites(ast.NodeTransformer):
    def visit_Call(self,node):
        self.generic_visit(node)
        if isinstance(node.func,ast.Attribute) and node.func.attr=='write_text':
            return ast.copy_location(ast.Call(func=ast.Name(id='capture_generated',ctx=ast.Load()),args=[node.func.value,*node.args],keywords=[]),node)
        return node
for helper in ['prepare_publication_lifecycle_scripts_02.py','prepare_review_repair_checkpoint_02.py','prepare_lifecycle_utilities_20261015.py']:
    tree=ast.parse((A/helper).read_text())
    if helper=='prepare_lifecycle_utilities_20261015.py':tree.body=[n for n in tree.body if n.lineno<10]
    tree=CaptureWrites().visit(tree)
    with redirect_stdout(io.StringIO()):
        exec(compile(ast.fix_missing_locations(tree),str(A/helper),'exec'),{'__file__':str(A/helper),'capture_generated':capture_generated})
out['generator_comparison']={n:{'equals_actual':body==(A/n).read_text(),
    'generated_sha256':hashlib.sha256(body.encode()).hexdigest(),'actual_sha256':pin(A/n)['sha256']} for n,body in generated.items()}
out['tracker_helper_would_drop_current_DOI_identity_sentence'] = ('Current Ferudun DOI-version files match inspected website copies; older journal-version comparisons remain incomplete.' in (A/'record_tracker.py').read_text() and 'Current Ferudun DOI-version files match inspected website copies; older journal-version comparisons remain incomplete.' not in generated['record_tracker.py'])
(D/'GENERATOR_DIFFS.json').write_text(json.dumps({n:list(difflib.unified_diff(body.splitlines(),(A/n).read_text().splitlines(),fromfile='generator_output',tofile='actual_script',n=0)) for n,body in generated.items() if body!=(A/n).read_text()},indent=2)+'\n')
out['all_target_scripts_unchanged_during_checks'] = all(pin(A/n)==x for n,x in out['script_pins'].items())
(D/'AUDIT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'scripts_parse':True,'scope_files':len(names),'native_fixture':'passed',
 'case_review_alias_after_factual_update':out['case_whole_package_reviews_complete_after_factual_update'],
 'mutated_unchecked_native_acceptance':out['ahead_MAIN_mutated_unchecked_native_counterexample']['accept_returned_success']}))
