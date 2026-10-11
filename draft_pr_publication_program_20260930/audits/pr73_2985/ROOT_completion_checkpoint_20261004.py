#!/usr/bin/env python3
"""Publish a narrow completion checkpoint after all seven actual native phases.

Preparation writes only new untracked files. Execution requires a separately
ROOT-promoted exact content plan and a fresh phase-specific writer ACK. Original
research log and frozen scientific/native inputs remain byte-identical.
"""
from pathlib import Path
import argparse, json, sys, hashlib, stat

A = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr73_2985')
PREP = A / 'native_integration_preparation_20261004'
sys.path.insert(0, str(PREP))
from native_common_v2 import *
from ROOT_native_readback_v2 import foreign_readback, verify_acceptance

D = A / 'ROOT_completion_preparation_20261004'
PROGRESS = ROOT / 'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json'
GATE = A / 'ROOT_native_execution_v1_20261004/ROOT_GATE_ROOT_REVIEWED.json'
ORDER = ('pr-metadata','merge','merge-readback','accept','acceptance-readback','checkpoint','checkpoint-readback')
RECORD = A / 'ROOT_COMPLETED_ATTRIBUTED_PARTIAL_RESULT_20261004.json'
LOG = A / 'RESEARCH_COMPLETION_LOG_20261004.md'
REVIEW = A / 'completion_checkpoint_operational_review_20261004'

def fixed_targets():
    """Independent literal mapping: no arbitrary audit or frozen-log ownership."""
    identity = [GATE, A/'ROOT_native_execution_v1_20261004/FROZEN_PLAN_ROOT_REVIEWED.json',
        A/'ROOT_native_execution_v1_20261004/ROOT_PROMOTION_RECEIPT.json', Path(__file__).resolve(),
        D/'PHASE_RECEIPT_COPY_MAP.json',
        *[D/'phase_receipts'/(phase+'.json') for phase in ORDER],
        D/'operational_review/REPORT.md', D/'operational_review/VERDICT.json']
    result = {str(x.relative_to(ROOT)):str(x.relative_to(ROOT)) for x in identity}
    result.update({str(dst.relative_to(ROOT)):str(src.relative_to(ROOT)) for src,dst in [
        (D/'prepared_completion_record.json',RECORD),(D/'prepared_progress.json',PROGRESS),
        (D/'prepared_completion_log.md',LOG)]})
    return result

def chain(gp):
    receipts = []
    for phase in ORDER:
        candidates = []
        for path in (PREP / 'operations').glob(phase + '_*/RECEIPT.json'):
            r = load(path)
            if r.get('phase') == phase and r.get('gate') == gp:
                candidates.append(path)
        require(len(candidates) == 1, 'Missing or ambiguous actual successful phase: ' + phase)
        path = candidates[0]
        validated_pin = pin(path)
        r = read_receipt(validated_pin, phase, gp)
        controller = load(path.parent / 'CONTROLLER.json')
        if receipts:
            argv = controller['argv']
            require('--predecessor' in argv and Path(argv[argv.index('--predecessor') + 1]).resolve() == receipts[-1][0].resolve(), 'Actual predecessor chain differs')
            require(timestamp(r['UTC']) >= timestamp(receipts[-1][1]['UTC']), 'Actual phase time order differs')
        check_pin(validated_pin)
        receipts.append((path, r, validated_pin))
    return receipts

def check_public_chain(receipts):
    """Bind published receipt copies to the freshly authenticated actual chain."""
    mapping=load(D/'PHASE_RECEIPT_COPY_MAP.json')['copies']
    require(len(mapping)==len(ORDER), 'Public receipt map length differs')
    for (path, r, validated), row in zip(receipts,mapping):
        expected_copy=D/'phase_receipts'/(r['phase']+'.json')
        require(row['source']==validated and row['public_copy']['path']==str(expected_copy.relative_to(ROOT)), 'Public/actual receipt identity or order differs')
        check_pin(validated); check_pin(row['public_copy'])
        require(expected_copy.read_bytes()==path.read_bytes(), 'Public receipt copy differs from validated actual receipt')

def prepare():
    require(not D.exists(), 'Preserve existing preparation; do not overwrite')
    review=load(REVIEW/'VERDICT.json')
    require(review.get('status')=='PASS_COMPLETION_CODE_REVIEW' and review.get('reviewed_completion_operator_sha256')==sha(Path(__file__).read_bytes()) and review.get('remaining_substantive_findings')==[], 'Independent operational review does not clear this exact completion source')
    g, plan, packet, science, gp = validate_gate(GATE)
    require(science['status'] == 'partial' and science['novelty_clearance'] is False and science['publication_DOI'] is None, 'Only the certified partial disposition is in scope')
    receipts = chain(gp)
    last = receipts[-1][1]
    require(last.get('status') == 'PASS', 'Final actual readback did not pass')
    merge, acceptance, audit = receipts[1][1]['merge_commit'], receipts[3][1]['acceptance_commit'], receipts[5][1]['current_commit']
    require(last['current_commit'] == audit, 'Final readback/checkpoint head differs')
    D.mkdir()
    copies = D / 'phase_receipts'; copies.mkdir()
    reviewcopies = D / 'operational_review'; reviewcopies.mkdir()
    for name in ('REPORT.md','VERDICT.json'):
        dst=reviewcopies/name; dst.write_bytes((REVIEW/name).read_bytes()); dst.chmod(0o644)
    mapping = []
    for source, r, validated_pin in receipts:
        copy = copies / (r['phase'] + '.json')
        check_pin(validated_pin)
        raw=source.read_bytes()
        require(len(raw)==validated_pin['bytes'] and sha(raw)==validated_pin['sha256'], 'Validated actual receipt drift before copy')
        copy.write_bytes(raw); copy.chmod(0o644)
        require(copy.read_bytes()==raw, 'Actual receipt copy differs')
        mapping.append({'source':validated_pin, 'public_copy':pin(copy)})
    (D / 'PHASE_RECEIPT_COPY_MAP.json').write_bytes(json_bytes({'UTC':now(),'copies':mapping,'scope':'Byte-identical phase receipts only. Referenced private streams and inventories remain local; no assertion that those files are published.'}))
    record = {
        'schema':'pr73-verified-partial-native-completion/v1','UTC':now(),'PR':PR,'problem_id':ID,
        'original_head':HEAD,'initial_literal_status':'claimed_solved','original_budget':'1/5',
        'original_turn_events':[1],'original19_bodies_modes_blobs_preserved':True,'new_original_proof_turns':0,
        'complete_connected_theorem_verified':True,'bounded_priority_audit_complete':True,
        'novelty_clearance':False,'prior_resolution_of_intended_connected_target_certified':False,
        'disconnected_version_prior_verified':True,'audited_outcome':'partial','accepted_as':science['accepted_as'],
        'scope_interpretation':science['scope_interpretation'],
        'partial_meaning':'Historical novelty/target-priority determination remains incomplete. The connected mathematical theorem is fully proved.',
        'all_seven_actual_native_phases_passed':True,'mathematical_audit_percent':100,
        'bounded_priority_audit_percent':100,'native_workflow_percent':100,
        'merge_commit':merge,'acceptance_commit':acceptance,'audit_checkpoint_commit':audit,
        'final_ROOT_gate':gp,'frozen_exact_plan':g['exact_plan'],
        'phase_receipts':[x['public_copy'] for x in mapping],
        'new_paper':False,'new_DOI':None,'Zenodo_upload':False,'tracker_append':False,
        'exclusive_writer_window_release_pending':True,
        'completion_checkpoint_push_confirmation':'Actual completion operator receipt is retained locally after its successful commit/push; this record does not contain a self-referential commit hash.',
        'program_completed_eligible_PRs':[9,16,18,50,55,57,65,66,73],
        'dated_program_fraction_percent':9/99*100,'goal_complete':False,
    }
    pending_record = D / 'prepared_completion_record.json'; pending_record.write_bytes(json_bytes(record))
    old = PROGRESS.read_bytes(); p = json.loads(old)
    require(p['fully_completed_eligible_PRs'] == [9,16,18,50,55,57,65,66] and p['current_PR'] == 73, 'Progress baseline differs')
    p.update(UTC=now(),fully_completed_eligible_PRs=record['program_completed_eligible_PRs'],fully_completed_count=9,
        fully_completed_fraction_percent=9/99*100,workflow_estimate_percent=9/99*100,
        workflow_estimate_definition='Five published workflows, three eligible-at-intake credited prior-result dispositions, and one verified partial disposition with connected-target priority unestablished, divided by the dated99-PR census.',
        current_PR_workflow_percent=100,current_merge_commit=merge,current_acceptance_commit=acceptance,
        current_last_audit_checkpoint_commit=audit,current_native_seven_phase_readback_complete=True,
        remaining_current_step='Seven native phases and final readback passed. Completion checkpoint publication and subsequent intake remain conditional on its successful actual receipt and explicit shared-writer release.',
        advance_to_next_PR_authorized_now=False,last_completed_PR=73,last_completed_PR_workflow_percent=100,
        last_completed_DOI=None,last_completed_merge_commit=merge,last_completed_acceptance_commit=acceptance,
        last_completed_tracker_range=None,last_completed_record=str(RECORD.relative_to(ROOT / 'draft_pr_publication_program_20260930')),
        last_completed_priority_hold='Connected-target novelty and historical priority unestablished.',
        last_completed_mathematical_and_package_review_percent=100,last_completed_priority_audit_percent=100,
        last_completed_priority_clearance=False,last_completed_publication_authorization=False,
        last_completed_outcome='verified_attributed_partial_result_priority_unestablished',last_completed_full_source_solved=True,
        last_completed_scientific_disposition_record=str((A/'ROOT_FINAL_SCIENTIFIC_PARTIAL_DISPOSITION_20261004.json').relative_to(ROOT / 'draft_pr_publication_program_20260930')),
        last_completed_final_audit_checkpoint_commit=audit,next_numeric_intake_cursor=74,
        last_completed_audit_checkpoint_push_pending=False,
        accepted_partial_priority_unestablished_PRs=[73],persistent_goal_complete=False,
        next_intake_requires_actual_completion_receipt_and_explicit_writer_release=True)
    pending_progress = D / 'prepared_progress.json'; pending_progress.write_bytes(json_bytes(p))
    pending_log = D / 'prepared_completion_log.md'
    pending_log.write_text(now()+' — PR73: all seven actual native integration/readback phases passed. The complete connected genus-three counterexample is verified; historical novelty and priority for the intended connected target remain unestablished. Earlier disconnected constructions and ingredients are credited. Accepted as partial without a paper, DOI, upload or tracker row. Original 19 files, 1/5 accounting and one turn1 event preserved; no new proof-search turn. Math 100%; bounded priority audit 100%; native workflow 100%; program 9/99 ≈ 9.09%. Completion checkpoint push and writer release require their actual subsequent evidence. Original frozen RESEARCH_LOG.md remains unchanged.\n')
    existing = [GATE, safe_path(g['exact_plan']['path']), A/'ROOT_native_execution_v1_20261004/ROOT_PROMOTION_RECEIPT.json', Path(__file__).resolve(), D/'PHASE_RECEIPT_COPY_MAP.json', *sorted(copies.glob('*.json')),reviewcopies/'REPORT.md',reviewcopies/'VERDICT.json']
    targets = [{'input':pin(x),'target':str(x.relative_to(ROOT))} for x in existing]
    targets += [{'input':pin(x),'target':str(y.relative_to(ROOT))} for x,y in [(pending_record,RECORD),(pending_progress,PROGRESS),(pending_log,LOG)]]
    pending = {'schema':'pr73-completion-checkpoint-content-plan/v1','stage':'PENDING_ROOT_PUBLIC_CONTENT_REVIEW','UTC':now(),
        'gate':gp,'predecessor':receipts[-1][2],'expected_base':audit,'progress_before_sha256':sha(old),
        'targets':targets,'ROOT_certifies_all_whole_bodies_public_safe':False,
        'no_raw_datasets_primary_sources_streams_foreign_snapshots':True,'preserve_frozen_research_log':True}
    check_public_chain(receipts)
    (D/'PENDING_CONTENT_PLAN.json').write_bytes(json_bytes(pending))
    print(json.dumps({'status':'PREPARED_ONLY','pending_plan':str(D/'PENDING_CONTENT_PLAN.json'),'target_count':len(targets),'native_base':audit},indent=2))

def execute(path, nonce):
    path=Path(path).resolve()
    require(path == D/'ROOT_REVIEWED_CONTENT_PLAN.json', 'Exact versioned ROOT-promoted completion plan required')
    raw=path.read_bytes(); content = json.loads(raw)
    content_pin={'path':str(path.relative_to(ROOT)),'bytes':len(raw),'sha256':sha(raw)}
    check_pin(content_pin)
    require(content['stage'] == 'ROOT_REVIEWED_PUBLIC_COMPLETION_CONTENT' and content['ROOT_certifies_all_whole_bodies_public_safe'] is True, 'ROOT public content certification absent')
    g, plan, packet, science, gp = validate_gate(GATE)
    require(content['gate'] == gp, 'Frozen scientific gate differs')
    actual_chain=chain(gp)
    check_public_chain(actual_chain)
    require(content['predecessor']==actual_chain[-1][2], 'Completion plan final predecessor differs from validated public/actual chain')
    prior = read_receipt(content['predecessor'], 'checkpoint-readback', gp)
    require(prior['current_commit'] == content['expected_base'], 'Completion predecessor differs')
    targets = content['targets']; owned = {r['target'] for r in targets} | {str(Path(path).resolve().relative_to(ROOT))}
    require(len(owned) == len(targets)+1 and ACK_REL not in owned, 'Completion path scope duplicates or owns ACK')
    require({r['target']:r['input']['path'] for r in targets} == fixed_targets(), 'Literal target/input mapping differs; no frozen scientific/log path may be overwritten')
    require(all(x == str(PROGRESS.relative_to(ROOT)) or x.startswith(str(A.relative_to(ROOT))+'/') for x in owned), 'Completion ownership outside exact audit/progress scope')
    require(all(Path(x).suffix.lower() in ('.json','.md','.py') and not any(t in x for t in ('/operations/','/commands/','/original/','/cache/')) for x in owned), 'Private path in completion allowlist')
    for r in targets: check_pin(r['input'])
    require(sha(PROGRESS.read_bytes()) == content['progress_before_sha256'], 'Current progress drift; preserve and stop')
    s = Session('completion-checkpoint', gp)
    current = current_baseline(s)
    require(current == content['expected_base'], 'Main advanced; preserve and reconcile')
    w = WriterWindow(s,g,current,owned,max(prior['UTC'],content['UTC'],key=timestamp),nonce)
    ack=json.loads(w.ack_bytes)
    require(ack.get('completion_content_plan_sha256')==content_pin['sha256'], 'Fresh completion ACK does not bind ROOT-reviewed completion content')
    (s.dest/'COMPLETION_CONTENT_PLAN.json').write_bytes(raw)
    code_pin=next(r['input'] for r in targets if r['target']==str(Path(__file__).resolve().relative_to(ROOT)))
    check_pin(code_pin); code_bytes=Path(__file__).read_bytes()
    require(len(code_bytes)==code_pin['bytes'] and sha(code_bytes)==code_pin['sha256'], 'Completion operator snapshot differs from ROOT-reviewed source')
    (s.dest/'COMPLETION_OPERATOR_SOURCE.py').write_bytes(code_bytes)
    extra_pins=[pin(s.dest/'COMPLETION_CONTENT_PLAN.json'),pin(s.dest/'COMPLETION_OPERATOR_SOURCE.py')]
    require(extra_pins[0]['bytes']==content_pin['bytes'] and extra_pins[0]['sha256']==content_pin['sha256'] and extra_pins[1]['bytes']==code_pin['bytes'] and extra_pins[1]['sha256']==code_pin['sha256'], 'Retained completion source/plan snapshots differ from reviewed input pins')
    foreign_readback(s,prior,{r['pin']['path'] for r in plan['checkpoint_files']},w)
    m, original, source = originals()
    identity = verify_current_source(s,source)
    a = load(safe_path(PREFIX+'/acceptance.json')); merge = a['merge_commit']
    accepted_commit = s.git('rev-parse',current+'^').decode().strip()
    verify_acceptance(s,g,plan,packet,science,gp,merge,accepted_commit,original,identity)
    native = {x:pin(safe_path(x)) for x in ACCEPT_PATHS | {QUEUE}}
    for r in plan['checkpoint_files']:
        check_pin(r['pin'])
        require(s.git('show',current+':'+r['pin']['path']) == safe_path(r['pin']['path']).read_bytes(), 'Frozen audit checkpoint body differs')
    pr = s.pr(); require(pr['state']=='MERGED' and pr['mergeCommit']['oid']==merge and pr['title']==plan['pr_title'] and pr['body'].encode()==packet['PR_BODY.md'], 'PR merged metadata differs')
    w.check()
    check_pin(content_pin)
    for r in targets:
        check_pin(r['input'])
        src=safe_path(r['input']['path']); dst=safe_path(r['target'])
        reviewed=src.read_bytes()
        require(len(reviewed)==r['input']['bytes'] and sha(reviewed)==r['input']['sha256'], 'Prepared source drift before copy; preserve and stop')
        if src != dst:
            require(not dst.exists() or dst == PROGRESS, 'Unexpected completion destination exists')
            dst.write_bytes(reviewed); dst.chmod(0o644)
        require(dst.read_bytes()==reviewed and stat.S_IMODE(dst.stat().st_mode)==0o644, 'Completion target differs from reviewed whole input/mode')
    expected = {x:pin(safe_path(x)) for x in owned}
    def stable():
        w.check()
        check_public_chain(actual_chain)
        require(validate_gate(GATE)[4]==gp, 'Frozen scientific/native authority drifted')
        for row in identity['whole_current_source_pins']:
            check_pin(row)
            require(stat.S_IMODE(safe_path(row['path']).stat().st_mode)==0o644, 'Whole current raw/SQL source mode drifted')
        check_pin(content_pin)
        for row in extra_pins: check_pin(row)
        for r in targets:
            check_pin(r['input'])
            target=safe_path(r['target']).read_bytes()
            require(len(target)==r['input']['bytes'] and sha(target)==r['input']['sha256'], 'Completion output differs from ROOT-reviewed exact content')
        for row in [*expected.values(),*native.values()]:
            check_pin(row)
            require(stat.S_IMODE(safe_path(row['path']).stat().st_mode)==0o644, 'Owned/native filesystem mode drifted')
        check_original_git(s,w.current,original,native=True)
    def committed(commit):
        for rel,row in expected.items():
            b=safe_path(rel).read_bytes()
            require(s.git('show',commit+':'+rel)==b and s.git('ls-tree',commit,'--',rel).decode().split()[:3]==['100644','blob',git_blob(b)], 'Completion committed body/mode/blob differs')
    stable(); s.git('add','--',*sorted(owned))
    changed=names0(s.git('diff','--cached','--name-only','-z')); require(changed and changed <= owned, 'Completion staged scope differs')
    for rel in changed:
        b=safe_path(rel).read_bytes(); require(s.git('show',':'+rel)==b and s.git('ls-files','--stage','--',rel).decode().split()[:3]==['100644',git_blob(b),'0'], 'Completion staged body/mode/blob differs')
    stable(); s.git('commit','-m','Complete PR73 verified connected result with priority explicitly unestablished')
    commit=s.git('rev-parse','HEAD').decode().strip(); w.current=commit
    require(s.git('show','-s','--format=%P',commit).decode().split()==[current] and names0(s.git('diff','--name-only','-z',current,commit))==changed, 'Completion commit parent/scope differs')
    committed(commit); stable()
    require(not s.git('diff','--cached','--name-only','-z'), 'Shared index not empty after completion')
    s.git('push','origin','main')
    require(s.git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit, 'Completion push did not match main')
    committed(commit); stable()
    require(not s.git('diff','--cached','--name-only','-z'), 'Final shared index not empty')
    s.finish({'current_commit':commit,'parent':current,'completion_checkpoint_commit':commit,'public_owned_paths':sorted(changed),
        'completion_content_plan':content_pin,'actual_completion_source_and_plan_snapshots':extra_pins,
        'owned_whole_bodies_modes_blobs_verified':True,'foreign_tracked_bodies_modes_index_preserved':True,
        'native_acceptance_and_frozen_originals_preserved':True,'remote_main_exact':True,
        'program_completed_count':9,'dated_program_denominator':99,'goal_complete':False,'exclusive_writer_window_release_pending':True})

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase',choices=('prepare','execute')); ap.add_argument('--plan'); ap.add_argument('--writer-ack-nonce')
    args=ap.parse_args()
    require(not sys.flags.optimize and sys.flags.ignore_environment and sys.dont_write_bytecode and Path.cwd().resolve()==ROOT.resolve(), 'Run from repository root with python -E -B')
    if args.phase=='prepare': prepare()
    else:
        require(args.plan and args.writer_ack_nonce,'Explicit reviewed plan and fresh ACK nonce required')
        execute(args.plan,args.writer_ack_nonce)
