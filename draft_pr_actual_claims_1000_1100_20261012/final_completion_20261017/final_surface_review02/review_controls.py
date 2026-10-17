"""Bounded read-only administrative closure checks, with outputs confined here."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import subprocess

D=Path(__file__).resolve().parents[2]
O=Path(__file__).resolve().parent
A=D/'final_completion_20261017/attempt_01'
inputs={}
checks={}

def ident_bytes(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def load_bytes(p):
    p=p if isinstance(p,Path) else D/p
    b=p.read_bytes()
    inputs[str(p.relative_to(D))]=ident_bytes(b)
    return b

def text(p):
    return load_bytes(p).decode()

def read(p):
    return json.loads(text(p))

def check(name,condition):
    checks[name]=bool(condition)

def diffs(before,after,path=()):
    if type(before)!=type(after):
        return [(path,before,after)]
    if isinstance(before,dict):
        out=[]
        for key in before.keys()|after.keys():
            if key not in before or key not in after:
                out.append((path+(key,),before.get(key),after.get(key)))
            else: out.extend(diffs(before[key],after[key],path+(key,)))
        return out
    if isinstance(before,list):
        if len(before)!=len(after): return [(path,before,after)]
        return sum((diffs(b,a,path+(i,)) for i,(b,a) in enumerate(zip(before,after))),[])
    return [] if before==after else [(path,before,after)]

state=read('STATE.json')
registry=read('CLAIM_REGISTRY.json')
report=text('FINAL_REPORT.md')
readme=text('README.md')
ignore=text('.gitignore')
prior=read('final_completion_20261017/final_surface_review01/REVIEW.json')
prior_controls=read('final_completion_20261017/final_surface_review01/CONTROLS.json')
prior_seal=read('final_completion_20261017/final_surface_review01/SEAL.json')
repair=read('final_completion_20261017/navigation_repair01/REPAIR_REPORT.json')
before=read('final_completion_20261017/navigation_repair01/CLAIM_REGISTRY.before.json')
reconciliation=read('final_completion_20261017/closure_20261017/CURRENT_RECONCILIATION.json')
preflight=read('final_completion_20261017/closure_20261017/RELEASE_PREFLIGHT.json')
audit=read(A/'COMPLETION_AUDIT.json')
live=read(A/'LIVE_PUBLICATIONS_AND_EXACT_HEAD_MERGES.json')
tracker=read(A/'FINAL_TRACKER_OWN_ROWS_ONLY.json')
excluded=read(A/'EXCLUDED_CURRENT_SOURCE_CHECK.json')
auditor=text('service_resume_20261016/audit_final_completion.py')
reviewed_auditor=load_bytes(D/'final_completion_20261017/independent_admin_review02/reviewed_auditor.py')
recovered=read('final_completion_20261017/independent_admin_review02/ROOT_RECOVERED_TERMINAL_REVIEW.json')
offline=read('final_completion_20261017/independent_admin_review02/OFFLINE_CONTROLS.json')

records={r['pr']:r for r in registry['records']}
accepted={r['pr']:r for r in state['accepted_results']}
pubs={r['pr']:r for r in live['records']}
rows={r['pr']:r for r in tracker['own_rows']}
cs=state['candidate_full_claim_prs']
ex=state['skipped_as_partial_or_prior_prs']
check('all101_unique_registry_assertions',len(records)==len(registry['records'])==101 and set(records)==set(range(1000,1101)))
check('18_accepted_scope_records_consistent',len(cs)==len(set(cs))==18 and set(cs)==set(accepted)==set(pubs)==set(rows)==set(registry['full_resolution_candidates'])==set(state['completed_prs']))
check('83_excluded_partition',len(ex)==len(set(ex))==83 and not set(ex)&set(cs) and set(ex)|set(cs)==set(range(1000,1101)))
check('classification_counts_exact',dict(collections.Counter(r['classification'] for r in records.values()))==registry['counts'])
check('all83_saved_current_assertions_unchanged',excluded['changed_count']==0 and {r['pr'] for r in excluded['records']}==set(ex) and all(r['assertion_unchanged'] for r in excluded['records']))
check('workflow_ascending_complete_no_cursor',state['direction']=='ascending' and state['range_inclusive']==[1000,1100] and state['next_pr'] is None and all(s in registry['workflow_order'] for s in ['ascending','all18','completed','83','no remaining disposition cursor']))
check('1032_remaining_gate_null',records[1032].get('remaining_gate') is None)
rd=diffs(before,registry)
index1032=next(i for i,r in enumerate(registry['records']) if r['pr']==1032)
expected={('updated_utc',),('workflow_order',),('records',index1032,'remaining_gate')}
check('repair_only_two_operational_fields_and_timestamp',{x[0] for x in rd}==expected)
check('repair_before_after_identity_bound',inputs['final_completion_20261017/navigation_repair01/CLAIM_REGISTRY.before.json']==repair['before'] and inputs['CLAIM_REGISTRY.json']==repair['after'])
check('prior_P3_exactly_repaired',prior['status']=='ONE_ACTIONABLE_P3' and prior['actionable_counts']=={'P0':0,'P1':0,'P2':0,'P3':1} and prior['findings'][0]['id']=='ADMIN-P3-01')
check('prior75_controls_preserved',prior_controls['number_of_passed_checks']==75 and all(prior_controls['checks'].values()))
check('dated_reconciliation_registry_binding_explained',reconciliation['working_outputs']['CLAIM_REGISTRY.json']==repair['before'] and 'dated pre-repair snapshot' in repair['previous_current_reconciliation_identity'])
for p in ['STATE.json','README.md','FINAL_REPORT.md']:
    check('unchanged_reconciliation_surface_'+p,inputs[p]==reconciliation['working_outputs'][p])
check('fresh_audit_qualified_full_scope',audit['status']=='PASS_FULL_CURRENT_RANGE_COMPLETION_AUDIT' and audit['screened_assertions']==101 and audit['accepted_scoped_results']==18 and audit['excluded_partial_prior']==83 and audit['intake_evidence_references_checked']==389)
check('full_native_merge_tracker_reviews_gates',all(audit[k] for k in ['excluded_current_assertions_unchanged','all_live_zenodo_metadata_files_dois_verified','all_live_exact_head_merge_parents_verified','all_tracker_rows_unique_and_exact','all_minimum_two_complete_reviews_latest_no_actionables']))
check('fresh_audit_exact_state_binding',inputs['final_completion_20261017/attempt_01/COMPLETION_AUDIT.json']==state['final_completion_audit_identity']==reconciliation['full_fresh_audit'])
check('fresh_auditor_same_as_independently_reviewed',auditor.encode()==reviewed_auditor and ident_bytes(reviewed_auditor)==recovered['source_identity']=={k:offline['source'][k] for k in ('bytes','sha256')})
check('saved_readonly_github_request_success',live['github_read']['label']=='LIVE_ALL101_PR_SCOPE_AND_MERGES' and live['github_read']['attempts'][-1]['exit']==0)
check('auditor_covers_exact_head_parents_and_reviewed_wording',all(s in auditor for s in ["Live exact audited head parent","Current accepted PR wording differs","intake_evidence_references_checked","z.verify(deposit, entry['metadata'], entry['files'])","Final exact unique tracker row"]))
check('tracker_only_own_exact_rows',tracker['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and tracker['gid']==1254632077 and tracker['sheet_title']=='Math Puzzles' and tracker['unrelated_rows_not_saved'] is True and all(r['exact_unique_row'] for r in rows.values()))
check('18_unique_dois_and_tracker_rows',len({r['doi'] for r in pubs.values()})==len({r['sheet_row'] for r in rows.values()})==18)
table={int(m[0]):m for m in re.findall(r'^\| \[#(\d+)\]\([^\n]+?\) \| ([0-9]+) \| \[([^\n]+?)\]\(https://doi.org/([^\)]+)\) \| (\d+) \| (\d+) \|$',report,re.M)}
check('18_final_report_rows_exact_set',set(table)==set(cs))
for n in cs:
    r=records[n]; a=accepted[n]; p=pubs[n]; t=rows[n]; tr=table.get(n)
    individual=read(A/f'NATIVE_AND_MERGE_PR{n}.json')
    check(f'publication_saved_record_{n}',individual==p and p['state']=='published' and p['doi_resolution']['status']=='resolved' and p['doi_resolution']['http_status']==200 and len(p['files'])==2)
    check(f'exact_head_merge_record_{n}',p['live_merge']['head']==r['head_oid']==a['audited_and_merged_head'] and p['live_merge']['merge_commit']==a['merge_commit'] and a['merged'] is True)
    check(f'accepted_workflow_complete_{n}',r['published'] is True and r['publication_ready'] is True and r['workflow_outcome']=='PUBLISHED_TRACKED_EXACT_HEAD_MERGED' and r['preprint_status']=='PUBLISHED_ZENODO_TRACKED_AND_EXACT_HEAD_MERGED' and not r['actionable_concerns'])
    check(f'review_counts_consistent_{n}',p['whole_reviews']==r['fresh_package_reviews'] and p['whole_reviews']>=2 and (a.get('fresh_whole_package_reviews',p['whole_reviews'])==p['whole_reviews']) and a.get('final_review_actionable_issues',0)==0)
    check(f'tracker_exact_surface_{n}',t['doi']==p['doi']==a['doi'] and t['sheet_row']==a['tracker_row'] and t['values'][2]=='https://doi.org/'+p['doi'] and 'https://github.com/AlecKriebel/Math/pull/'+str(n) in t['values'][3])
    check(f'report_table_surface_{n}',tr is not None and tr[1]==str(r['problem_id']) and tr[2]==p['title'] and tr[3]==p['doi'] and int(tr[4])==p['whole_reviews'] and int(tr[5])==t['sheet_row'])
    check(f'AI_unrefereed_human_qualification_{n}',a['AI_used_extensively'] is True and a['unrefereed'] is True and a['human_peer_review'] is False and re.search(r'AI|artificial intelligence',t['values'][3],re.I) and 'unrefereed' in t['values'][3].lower())
    check(f'accepted_scope_preserved_in_report_{n}',a['scope'] in report)
    if n not in [1001,1024,1025,1031]:
        check(f'accepted_exact_conclusion_in_report_{n}',a['mathematical_outcome'] in report)

pending={k:v for k,v in state.items() if (('pending' in k and isinstance(v,(list,dict))) or k in ['parallel_audit_prs','preprint_preparation_prs','next_required_whole_reviews','in_progress_publication_prs','terminal_admin_execution_active_prs','terminal_admin_execution_next_prs'])}
check('all_current_operational_pending_collections_empty',all(not v for v in pending.values()))
check('current_no_paper_source_cursor',not state['support_case_alias_scope_terminal_report_pending'] and 'No remaining publication cursor or whole-package review is pending' in readme)
check('1032_unknown_user_accepted_nonblocking',state['priority_unresolved_nonblocking_prs']==[1032] and records[1032]['Luo_Zha_overlap']=='UNKNOWN' and not records[1032]['priority_established'] and audit['Luo_Zha_substantive_overlap']=='UNKNOWN_USER_ACCEPTED_NONBLOCKING' and 'UNKNOWN' in accepted[1032]['scope'] and 'human authorized treating that comparison as nonblocking' in report)
check('no_novelty_firstness_worldwide_openness_or_human_certification',audit['priority_novelty_worldwide_openness_certified'] is False and 'no conventional human peer review' in report and 'No firstness or independent-discovery claim is inferred' in report and 'exhaustive novelty or worldwide current-openness guarantee' in report)
check('partial_bundled_scopes_not_promoted',all(s in report for s in ['other bundled clauses remain unresolved','Two-strand orders 3..6','Exact M(g) for g≥3','never a full resolution of the bundled maximum problem']))
check('83_exclusions_source_holds_are_excluded',all(s in report for s in ['#1003 retains normalization/existence bridges','#1005 credits a standard application','#1008 leaves the variable-count main bound unresolved']) and registry['current_workflow_completion']['excluded_partial_prior_or_unsupported_original_full_claim']==83)
check('status_only_rule_explicitly_superseded',all(s in readme for s in ['original status-only pass','actual claims and artifacts']) and 'previous QUEUE-only skip rule no longer governs intake' in state['user_override'])
check('99_percent_pending_release_is_explicit',state['estimated_completion_percent']==99 and audit['final_isolated_checkpoint_still_required'] and 'pending' in state['final_repository_checkpoint_status'] and 'final isolated main push and readback pending' in report)
check('recovered_admin_review_transcription_qualified',recovered['no_fresh_live_completion_audit_claim'] and recovered['whole_package_mathematical_review_credit']==0 and 'ROOT transcription' in recovered['recovered_from'])

# Check names/ignore rules only. Never open authenticated raw journal contents.
private_paths=set(preflight['private_paths'])
private_paths.update(str(p.relative_to(D.parent)) for p in (D/'audits').glob('pr*/service_receipts_20261016/COMMANDS*.jsonl*') if p.is_file())
private_paths.update(D.name+'/'+p for p in ['audits/pr1098_3000018/service_receipts_20261016/COMMANDS.1.jsonl.gz','audits/pr1098_3000018/service_receipts_20261016/COMMANDS20261017.jsonl.gz'])
argv=['git','check-ignore','-v','--no-index',*sorted(private_paths)]
cp=subprocess.run(argv,cwd=D.parent,capture_output=True,text=True,timeout=30)
ignored={line.split('\t',1)[1] for line in cp.stdout.splitlines() if '\t' in line}
check('all_actual_private_journal_sourceimages_and_rotations_ignored',cp.returncode==0 and ignored==private_paths)
check('actual_gitignore_matches_release_preflight',inputs['.gitignore']['sha256']==preflight['ignore_rules_sha256'])

# Snapshot input hashes describe this review, not a future release readback.
check('review_inputs_remained_exact_during_checks',all(ident_bytes((D/name).read_bytes())==pin for name,pin in inputs.items()))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
failed=[k for k,v in checks.items() if not v]
controls={'utc':utc,'checks':checks,'number_of_passed_checks':sum(checks.values()),'failed':failed,'registry_diff': [{'path':list(p),'before':b,'after':a} for p,b,a in rd], 'current_pending_collections_checked':sorted(pending),'privacy_check':{'argv':argv,'exit':cp.returncode,'paths_checked':len(private_paths),'output':cp.stdout,'stderr':cp.stderr},'no_network_or_services':True,'no_credentials_or_raw_sheet_data_read':True,'whole_package_mathematical_review_credit':0}
(O/'CONTROLS.json').write_text(json.dumps(controls,indent=2,ensure_ascii=False)+'\n')
(O/'SOURCE_PINS.json').write_text(json.dumps({'utc':utc,'inputs':inputs},indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'utc':utc,'passed':sum(checks.values()),'failed':failed,'source_pins':len(inputs),'privacy_paths':len(private_paths)},ensure_ascii=False))
