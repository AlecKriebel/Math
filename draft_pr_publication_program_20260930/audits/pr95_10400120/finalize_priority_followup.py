from pathlib import Path
import datetime, hashlib, json, os, urllib.parse
A = Path(__file__).resolve().parent
P = A.parents[1]
D = A / 'priority_later_version_followup_20261005'
T = A / 'priority_thesis_repository_followup_20261005'
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(f, obj):
    f.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def pin(f):
    b = f.read_bytes()
    return {'file':str(f.relative_to(P)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
def public_url(url):
    u = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((u.scheme,u.netloc,u.path,'',''))
ledger = json.loads((D / 'SOURCE_LEDGER.json').read_text())
for src in ledger['sources']:
    retrieval = src.get('retrieval')
    if isinstance(retrieval, dict) and 'effective_url' in retrieval:
        retrieval['effective_url'] = public_url(retrieval['effective_url'])
ledger['projection_note'] = 'Read scopes and byte pins only; raw primary source content, HTTP headers and transient publisher error query strings excluded.'
write(A / 'ROOT_PRIORITY_LATER_SOURCE_SCOPES_20261005.json', ledger)
retrievals = []
for f in sorted((D / 'processes').glob('retrieval_*.json')):
    source = json.loads(f.read_text())
    r = {k:v for k,v in source.items() if k in ['operator_PID','UTC_start','UTC_finish','requested_url','url','effective_url','status','path','bytes','sha256','PDF','error','exception']}
    for k in ['effective_url','requested_url','url']:
        if k in r:
            r[k] = public_url(r[k])
    r['private_record'] = str(f.relative_to(A))
    retrievals.append(r)
write(A / 'ROOT_PRIORITY_LATER_RETRIEVAL_METADATA_20261005.json', {'UTC':utc, 'actual_operator_PID':os.getpid(), 'projection_only':True, 'raw_HTTP_headers_excluded':True, 'records':retrievals})
auth = json.loads((A / 'ROOT_AUTHENTICATED_PRIORITY_LATER_FOLLOWUP_20261005.json').read_text())
if auth['integrity_checks'] != 116 or auth['publication_clearance']:
    raise RuntimeError('unexpected integrity receipt')
closed = json.loads((D / 'CLOSURE.json').read_text())
if closed['manifest_members'] != 65 or closed['priority_clearance'] or closed['publication_clearance']:
    raise RuntimeError('unexpected family closure')
inputs = [pin(f) for f in [D/'REPORT.md', D/'CLOSED_MANIFEST.json', D/'CLOSURE.json', D/'adversarial_review/report.md', T/'REPORT.md', T/'CLOSED_AUTHORED_MANIFEST.json', T/'CLOSURE.json', A/'ROOT_AUTHENTICATED_PRIORITY_LATER_FOLLOWUP_20261005.json']]
record = {'schema':'PR95-priority-followup-adjudication/v1','UTC':utc,'actual_operator_PID':os.getpid(),'PR':95,'immutable_source_head':'6534ad01e519c719628a18984b108e73cf2e8ead','mathematical_gate_unchanged':True,'bounded_followups_complete':True,'later_packet_files':65,'family_integrity_checks':59,'ROOT_integrity_checks':116,'thesis_retrieval_documents_obtained':0,'earlier_qualifying_result_authenticated_in_new_read_scopes':False,'priority_requirement_complete':False,'priority_clearance':False,'publication_clearance':False,'may_advance_to_next_PR':False,'new_central_proof_search_turns':0,'original_author_effort':'2/5','main_gap':'Complete Kuriya GP-preprint conclusions and hypotheses still unavailable; compare to ordinary full SU(5), WZW k=5, shifted r=10, same pi1 and unequal positive magnitudes.','human_source_question_already_pending':True,'corrections':['Kubo–Yokoyama later SU(N) WZNW comparison is explicitly spin-independent; proposed background-field effects must not be conflated with ordinary spin dependence.','Relative phase ratio can be one for even shifted k; do not infer a universal magnitude discrepancy.','Gang journal pagination is 1119–1128, correcting the earlier historical ledger endpoint 1130.'],'historical_closed_packets_unchanged':True,'publication_exception_applied':False,'outside_outreach':False,'primary_checkout_mutated':False,'goal_blocked_audit':{'consecutive_goal_turns_retaining_this_condition':2,'meaningful_new_progress_this_turn':True,'all_current_bounded_agents_complete':True,'blocked_status_set':False},'PR95_workflow_estimate_percent':45,'mathematical_audit_percent':100,'priority_workflow_estimate_percent':85,'program_completed_dispositions':12,'dated_eligible_total':99,'program_workflow_estimate_percent':12/99*100,'inputs':inputs}
write(A / 'ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json', record)
root = json.loads((A / 'ROOT_PRIORITY_DISPOSITION_20261005.json').read_text())
root['UTC'] = utc
root['actual_operator_PID'] = os.getpid()
root['later_followup_adjudication'] = 'audits/pr95_10400120/ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json'
root['later_version_read_scope_gap_partially_closed'] = True
root['other_read_scope_gaps'] = ['Sokolov 1997 propositions unread.','HT final journal version/errata and unlocated Gauss-sum follow-up remain unavailable; prior printed example discrepancy unresolved.','Takata 1996 projective-category full text and reliably readable full Zhang–Carey 1996 source remain gaps.','Gang final 2019 text, unexamined later-paper portions and literature outside bounded searches remain unread.']
root['current_bounded_priority_followups_complete'] = True
root['new_source_corrections'] = record['corrections']
write(A / 'ROOT_PRIORITY_DISPOSITION_20261005.json', root)
progress = json.loads((P / 'CURRENT_PROGRESS.json').read_text())
progress['UTC'] = utc
progress['current_priority_followups_complete'] = True
progress['current_priority_followup_record'] = 'audits/pr95_10400120/ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json'
progress['remaining_current_step'] = 'Complete the directly relevant Kuriya full-text/scope comparison. Bounded thesis/repository and independent later-version follow-ups are closed; mathematical result verified, novelty unestablished. Existing human source question remains pending; no publication, merge or ordered advance yet.'
write(P / 'CURRENT_PROGRESS.json', progress)
with (A / 'PRIORITY_STATUS.md').open('a') as f:
    f.write('\nFurther bounded source checks closed at '+utc+'. The thesis/repository trail recovered no missing GP theorem text. An independent later-version family and fresh source adversary read Gang v2 and Kubo–Yokoyama v2/final within explicitly recorded boundaries. Their SU(N) and phase qualifications, and corrected Gang pagination, supersede overly broad wording in historical reports; those sealed historical records are preserved. No earlier qualifying counterexample was authenticated. ROOT verified the 65-file closed packet and the thesis records, with 116 byte-integrity checks. The direct Kuriya gap and all publication restrictions remain. See ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json.\n')
with (A / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### '+utc+' — new bounded priority follow-ups closed; PR95 workflow 45%, mathematics 100%, priority workflow 85%\nROOT read the final independent family and child reports, source/read-boundary ledgers, actual capture limitations and closure. An actual ROOT process authenticated 65 later-source packet files plus additional ledgers, child and thesis pins (116 checks). The new SU(N)/phase and Gang bibliography qualifications are propagated to the current disposition; sealed historicals remain intact. The three actual institution-linked PDFs all timed out, and other LMO metadata/abstracts did not supply the missing GP conclusions. No earlier qualifying result was authenticated; direct Kuriya source question already pending. No new central proof-search turns, paper, upload, tracker write, merge, PR disposition, next-PR advance, shared lease, primary checkout/index edit, outreach or cache cleanup occurred. Program 12/99 (12.12%). This is the second consecutive goal turn retaining the source condition, with new meaningful work completed; the persistent goal remains active.\n')
print(json.dumps({'UTC':utc,'actual_operator_PID':os.getpid(),'bounded_followups_closed':True,'priority_clearance':False,'publication_clearance':False,'program_dispositions':'12/99'}))
