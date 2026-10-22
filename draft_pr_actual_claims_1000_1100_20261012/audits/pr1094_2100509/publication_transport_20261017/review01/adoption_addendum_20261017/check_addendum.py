"""Local prospective-plan validation. Never applies the proposed state patch."""
import ast
import copy
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent
F = PREVIOUS.parent
D = F.parent.parent.parent
EXPECTED = 'audits/pr1094_2100509/publication_transport_20261017/ROOT_TRANSPORT_SEAL.json'

def read(path):
    return json.loads(path.read_text())

def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def need(test, text):
    if not test:
        raise AssertionError(text)

def main():
    old_seal = read(PREVIOUS / 'SEAL.json')
    previous_pins = []
    for row in old_seal['outputs']:
        path = PREVIOUS / row['path']
        need(ident(path) == {key: row[key] for key in ['bytes', 'sha256']}, 'prior output changed')
        previous_pins.append({'path': str(path), **ident(path)})
    previous_pins.append({'path': str(PREVIOUS / 'SEAL.json'), **ident(PREVIOUS / 'SEAL.json')})
    plan = read(F / 'ADOPTION_STATE_PATCH.json')
    need(plan['status'] == 'PROPOSED_ROOT_ADOPTION_BEFORE_SERVICE_ACTION', 'proposal status differs')
    need(plan['state_path'] == 'STATE.json', 'wrong state destination')
    need(plan['required_state_assignment'] == {'current_final_authorities': {'1094': EXPECTED}}, 'required authority assignment differs')
    need(plan['generator_proposal'] == 'proposed_prepare_service_configs.py', 'wrong generator proposal')
    need(set(plan['config_binding_fields']) == {'manifest', 'manifest_identity', 'metadata_sha256', 'final_seal', 'final_seal_identity'}, 'missing config identity gate')
    need(plan['state_alias'] == {'environment': 'production', 'id': 23431313,
                               'new_absolute_manifest': str(F / 'zenodo-deposit-html-transport.json'),
                               'preserve_old_alias': True}, 'wrong alias binding')
    required_readbacks = [
        'STATE current_final_authorities[1094] equals new external transport seal',
        'actual generator equals exact proposed one-literal path change',
        'operative service config manifest and seal hash identities match files',
        'old and new native aliases both bind same production deposit 23431313',
        'source and wire metadata differ only exact paragraph inequality encoding',
        'canonical PDF and ZIP remain byte identical',
        'native inspect using new alias reports ready on deposit 23431313',
    ]
    need(plan['required_readbacks'] == required_readbacks, 'readback gates incomplete')
    need(plan['no_new_whole_review_credit'] is True and plan['no_publication_before_all_readbacks'] is True, 'publication/review gate missing')
    actual_state_path = D / 'STATE.json'
    state_before = ident(actual_state_path)
    state = read(actual_state_path)
    patched = copy.deepcopy(state)
    patched.setdefault('current_final_authorities', {})['1094'] = EXPECTED
    source = (F / 'proposed_prepare_service_configs.py').read_text()
    implementation = F / 'ROOT_ADOPT_TRANSPORT.py'
    implementation_source = implementation.read_text()
    implementation_tree = ast.parse(implementation_source)
    remote_calls = [node.func.attr for node in ast.walk(implementation_tree)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name) and node.func.value.id == 'client']
    need(remote_calls == ['get', 'get'], 'adoption implementation contains unexpected remote action')
    required_fragments = [
        'need(addendum["actionable_issues"]==0',
        'need(old_state["id"]==23431313 and new_state is None',
        'z.validate_record(remote,23431313)',
        'need(remote["submitted"]is False',
        '"whole_reviews_completed":2,"new_whole_review_credit":0',
        'z.save_state(new_state_path,{"manifest":str(new_manifest.resolve()),"environment":"production","id":23431313})',
        'state.setdefault("current_final_authorities",{})["1094"]=str(new_seal.relative_to(D))',
        'need(read(D/"STATE.json")["current_final_authorities"]["1094"]==cfg["final_seal"]',
        'need(z.local_state(old_manifest.resolve(),"production")[1]==old_state',
        'if p==cfg_path:continue',
        'need(z.verify(remote,metadata,files)==[]',
    ]
    need(all(fragment in implementation_source for fragment in required_fragments), 'adoption implementation missing reviewed gate')
    need(implementation_source.index('z.save_state(new_state_path,') < implementation_source.index('save(cfg_path,cfg)'), 'config installed before alias')
    need(implementation_source.index('state.setdefault("current_final_authorities"') < implementation_source.index('save(cfg_path,cfg)'), 'config installed before authority')
    tree = ast.parse(source)
    expressions = [node.value for node in ast.walk(tree)
                   if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == 'sealpath' for target in node.targets)]
    need(len(expressions) == 1, 'ambiguous generator seal selection')
    expression = compile(ast.Expression(expressions[0]), '<isolated reviewed seal-selection expression>', 'eval')
    selected = eval(expression, {'__builtins__': {'str': str}},
                    {'D': D, 'state': patched, 'n': 1094, 'a': F.parent})
    need(selected == D / EXPECTED, 'generator would not choose transport seal')
    need(ident(actual_state_path) == state_before, 'actual state was changed')
    # Import only the already sealed review helper; its main is not called.
    spec = importlib.util.spec_from_file_location('prior_review', PREVIOUS / 'check_transport.py')
    review = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review)
    protected = review.protected_snapshot()
    review.acceptance(read(F / 'zenodo-deposit-html-transport.json'))
    review.generator_acceptance(source)
    for row in previous_pins:
        need(ident(Path(row['path'])) == {key: row[key] for key in ['bytes', 'sha256']}, 'prior output changed during addendum')
    need(ident(actual_state_path) == state_before, 'actual state changed during addendum')
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'verdict': 'ZERO_ACTIONABLE_ISSUES_IN_REVISED_PROSPECTIVE_ADOPTION_PLAN',
              'resolved_previous_actionable_issues': 1, 'remaining_actionable_issues': 0,
              'completion_percent': 100, 'new_whole_package_reviews': 0,
              'adoption_patch': {'path': str(F / 'ADOPTION_STATE_PATCH.json'), **ident(F / 'ADOPTION_STATE_PATCH.json')},
              'implementation_static_read': {'path': str(implementation), **ident(implementation),
                                             'remote_client_actions': remote_calls,
                                             'implementation_executed': False,
                                             'native_inspect_separate_root_gate_still_required': True},
              'previous_output_pins': previous_pins, 'protected_rows_matching': len(protected),
              'generator_selected_after_in_memory_patch': str(selected),
              'actual_state_unchanged': True, 'actual_state_identity_at_review': state_before,
              'actual_authority_at_review': state.get('current_final_authorities', {}).get('1094'),
              'new_seal_and_readbacks_still_prospective': True,
              'source_state_writes_or_service_calls': False,
              'raw_python_orig_argv': sys.orig_argv, 'exit': 0}
    (HERE / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ['verdict', 'remaining_actionable_issues', 'protected_rows_matching', 'actual_state_unchanged']}))

if __name__ == '__main__':
    main()
