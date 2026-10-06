"""Prepare explicit ROOT-reviewed data after a separate final scientific decision.

This writes local preparation only. It performs no Git or GitHub mutation.
The native operators still require fresh phase-specific writer acknowledgments.
"""
from pathlib import Path
import argparse, base64, json, os, stat, subprocess, sys, uuid

A = Path(__file__).resolve().parent
sys.path.insert(0, str(A / 'native_integration_preparation_20261004'))
from native_common_v2 import *

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--authority', required=True)
    ap.add_argument('--directory', required=True)
    args = ap.parse_args()
    require(not sys.flags.optimize and sys.flags.ignore_environment and sys.flags.dont_write_bytecode, 'Use python3 -E -B')
    require(Path.cwd().resolve() == ROOT.resolve(), 'ROOT preparation cwd differs')
    authority_path = Path(args.authority).resolve()
    authority = load(authority_path)
    require(authority_path.is_relative_to(A.resolve()) and authority['status'] == 'PASS' and authority['authorizer'] == 'ROOT', 'Final personally reviewed ROOT authority missing')
    require(authority['PR'] == PR and authority['reviewed_head'] == HEAD and authority['native_current_status'] == 'partial', 'Final identity/partial disposition differs')
    require(authority['ROOT_certified_attributed_partial_disposition'] is True, 'Exact ROOT-certified partial receipt marker missing')
    require(authority['ROOT_personally_read_final_reports'] is True and authority['final_fresh_adversarial_review_clean'] is True and authority['mathematics_validated'] is True, 'Final scientific readback is incomplete')
    require(authority['novelty_clearance'] is False and authority['no_prior_target_resolution_inferred'] is True and authority['new_paper'] is False and authority['publication_DOI'] is None and authority['tracker_append'] is False, 'No-novelty/no-publication partial route differs')
    for row in authority['bound_evidence'] + authority['bound_operators'] + authority['frozen_packet']:
        check_pin(row)
    dest = A / args.directory
    require(dest.resolve().parent == A.resolve(), 'Unique preparation directory escaped audit')
    dest.mkdir(mode=0o700, exist_ok=False)
    commands = []
    def measured(argv):
        started = now()
        c = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = c.communicate()
        n = '%03d' % (len(commands) + 1)
        for name, body in [('stdout', out), ('stderr', err)]:
            (dest / (n + '.' + name + '.bin')).write_bytes(body)
        row = {'PID': c.pid, 'cwd': str(ROOT), 'argv': argv, 'started_utc': started, 'finished_utc': now(), 'exit': c.returncode,
               'stdout': pin(dest / (n + '.stdout.bin')), 'stderr': pin(dest / (n + '.stderr.bin'))}
        commands.append(row)
        (dest / 'ACTUAL_PREPARATION_COMMANDS.json').write_bytes(json_bytes(commands))
        require(c.returncode == 0, 'Read-only preparation command failed')
        return out
    (dest / 'PREPARATION_PRELAUNCH.json').write_bytes(json_bytes({'UTC': now(), 'PID': os.getpid(), 'cwd': os.getcwd(), 'argv': sys.argv,
        'authority': pin(authority_path), 'operator': pin(Path(__file__)), 'bound_input_pins': authority['bound_evidence'] + authority['bound_operators'] + authority['frozen_packet']}))
    git = lambda *v: measured(['git', '--no-optional-locks', *v])
    require(git('branch', '--show-current').strip() == b'main', 'Stay on main')
    base = git('rev-parse', 'HEAD').decode().strip()
    require(git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == base, 'Current main is not pushed')
    require(not git('diff', '--cached', '--name-only', '-z'), 'Shared index is not empty')
    require(not (ROOT / '.git/MERGE_HEAD').exists(), 'Existing merge state')
    metadata = json.loads(measured(['gh', 'pr', 'view', '73', '--repo', REPO, '--json', 'number,state,isDraft,headRefOid,headRefName,baseRefName,title,body']))
    require(metadata['number'] == PR and metadata['state'] == 'OPEN' and metadata['isDraft'] is True and metadata['headRefOid'] == HEAD and metadata['headRefName'] == 'dot/math-2985' and metadata['baseRefName'] == 'main', 'Fresh submitted PR identity differs')
    before = safe_path(QUEUE).read_bytes()
    require(before == git('show', base + ':' + QUEUE), 'Current QUEUE is dirty')
    old = target_row(before)
    cells = old.decode().split('|')
    require(cells[8].strip() == 'queued' and cells[9].strip() == '0/5', 'Current untouched native target differs')
    proposal_pin = next(x for x in authority['frozen_packet'] if Path(x['path']).name == 'DISPOSITION_PROPOSAL.json')
    proposal = load(safe_path(proposal_pin['path']))
    require(proposal['proposed_current_status'] == 'partial' and proposal['submitted_head'] == HEAD, 'Reviewed proposal differs')
    cells[8], cells[9], cells[11], cells[12] = ' partial ', ' 1/5 ', ' ' + proposal['QUEUE_summary'] + ' ', '  '
    new = '|'.join(cells).encode()
    catalog_rows = [x for x in load(ROOT / 'unsolved_math_prioritization/catalog.json') if str(x['id']) == ID]
    require(len(catalog_rows) == 1, 'Current catalog target is not unique')
    ready = {'schema': 'pr73-current-separate-readiness-review/v1', 'status': 'PASS', 'UTC': now(), 'PR': PR, 'reviewed_head': HEAD,
             'mathematics_validated': True, 'native_current_status': 'partial', 'original_readiness_preserved': True,
             'original_budget': '1/5', 'new_original_proof_turns': 0, 'review_hash': catalog_rows[0]['review_hash'],
             'scope_interpretation': authority['scope_interpretation'], 'novelty_clearance': False,
             'final_ROOT_scientific_authority': pin(authority_path), 'historical_transitions_asserted': False}
    ready_path = dest / 'ROOT_CURRENT_READINESS.json'
    ready_path.write_bytes(json_bytes(ready))
    science = {'status': 'partial', 'accepted_as': authority['accepted_as'], 'scope_interpretation': authority['scope_interpretation'],
               'credited_prior_disposition': None, 'attributed_partial_disposition': pin(authority_path), 'novelty_clearance': False,
               'new_paper': False, 'publication_DOI': None, 'tracker_append': False, 'scientific_claims': authority['scientific_claims']}
    checkpoint = []
    for rel in authority['public_safe_files']:
        public_safe(rel)
        p = safe_path(rel)
        require(stat.S_IMODE(p.stat().st_mode) == 0o644, 'Explicit public file mode must be 0644')
        checkpoint.append({'pin': pin(p), 'ROOT_certifies_public_safe': True, 'git_mode': '100644'})
    plan = {'schema': 'pr73-frozen-native-plan/v2', 'stage': 'LOCAL_DATA_PENDING_ROOT_EXACT_BYTE_REVIEW', 'PR': PR, 'problem_id': ID,
            'expected_submitted_head': HEAD, 'execution_id': str(uuid.uuid4()), 'audited_outcome': 'partial', 'scope_interpretation': authority['scope_interpretation'],
            'expected_base_main': base, 'packet': authority['frozen_packet'], 'pr_title': proposal['PR_title'],
            'submitted_pr_title': metadata['title'], 'submitted_pr_body_sha256': sha(metadata['body'].encode()),
            'queue_before_row_sha256': sha(old), 'queue_after_row_base64': base64.b64encode(new).decode(), 'acceptance_scientific_fields': science,
            'merge_commit_message': 'Merge PR73: verified connected example; priority remains unestablished',
            'acceptance_commit_message': 'Record PR73 attributed partial audit with original attempt history preserved',
            'checkpoint_commit_message': 'Checkpoint PR73 independent mathematical and priority audits', 'checkpoint_files': checkpoint}
    plan_path = dest / 'FROZEN_PLAN.json'
    plan_path.write_bytes(json_bytes(plan))
    gate_utc = now()
    gate = {'schema': 'pr73-root-scientific-native-gate/v2', 'stage': 'LOCAL_PREPARATION_PENDING_ROOT_EXACT_BYTE_REVIEW', 'UTC': gate_utc,
            'authorizer': 'ROOT', 'PR': PR, 'problem_id': ID, 'expected_submitted_head': HEAD, 'audited_outcome': 'partial',
            'ROOT_authorizes_sequential_native_integration': False, 'ROOT_personally_read_required_reports': True, 'mathematics_validated': True,
            'historical_classification_certified': True, 'historical_classification_meaning': 'precise_bounded_classification_without_inferred_prior_target_resolution',
            'final_adversarial_review_clean': True, 'explicit_scope_interpretation_approved': True, 'scope_interpretation': authority['scope_interpretation'],
            'original_proof_turns': '1/5', 'new_original_proof_turns': 0, 'ROOT_reviewed_frozen_exact_plan': False,
            'exact_plan': pin(plan_path), 'bound_evidence': authority['bound_evidence'] + [pin(authority_path)], 'bound_operators': authority['bound_operators'],
            'current_readiness_evidence': pin(ready_path), 'minimum_writer_ack_utc': gate_utc, 'claimed_solved_gates': None, 'already_solved_gates': None,
            'partial_gates': {'certified_attributed_partial_disposition': pin(authority_path), 'no_novelty_clearance': True,
                             'no_new_paper': True, 'no_publication_action': True, 'no_tracker_append': True}}
    gate_path = dest / 'ROOT_GATE.json'
    gate_path.write_bytes(json_bytes(gate))
    require(load(plan_path) == plan and load(gate_path) == gate, 'Local plan/gate bytes do not round-trip')
    try:
        validate_gate(gate_path)
    except RuntimeError:
        pass
    else:
        raise RuntimeError('Unreviewed local preparation must not authorize operations')
    receipt = {'status': 'PASS_LOCAL_PREPARATION_ONLY', 'UTC': now(), 'actual_PID': os.getpid(), 'actual_cwd': os.getcwd(), 'actual_argv': sys.argv,
               'authority': pin(authority_path), 'gate': pin(gate_path), 'plan': pin(plan_path), 'readiness': pin(ready_path),
               'execution_id': plan['execution_id'], 'base': base, 'actual_read_only_child_commands': len(commands),
               'shared_mutation_performed': False, 'ROOT_exact_byte_review_and_promotion_still_required': True, 'actual_writer_ack_still_required': True}
    (dest / 'PREPARATION_RECEIPT.json').write_bytes(json_bytes(receipt))
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
