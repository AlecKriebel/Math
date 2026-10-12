"""Prepare concrete publication acceptance bytes only after actual receipts."""
import datetime, hashlib, json, stat
from pathlib import Path
from capture import capture
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr80_30000177'
F=Path(__file__).parent
def load(p): return json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
gate=load(A/'ROOT_FINAL_PACKAGE_GATE_20261004.json')
pub=load(A/'ROOT_PUBLICATION_VERIFICATION_20261004.json')
track=load(A/'ROOT_TRACKER_VERIFICATION_20261004.json')
assert gate['publication_clearance'] is True and pub['all8_public_bytes_identical'] and pub['intended_metadata_exact'] and track['fresh_full_table_exactly_one_pair'] and pub['DOI']==track['DOI']
assert gate['whole_preprint_rounds_completed']==2
doi,record=pub['DOI'],pub['record_url']
P=A/'native_preparation_20261004'; P.mkdir(exist_ok=False)
exact_claim='The symmetric W4 state is LOCC-DC in the original independent-sender split-receiver asymptotic local-unitary model: C_LOCC(W4)>=3/2+h2(1/4)>2, including rates(9/8,9/8) with vanishing uniform average error.'
result=f'''# Current accepted result: OWR-785-003 / 30000177

{exact_claim}

Each sender transmits one qubit per resource copy to its designated receiver. Receiver1 makes a complete Bell measurement and forwards every classical outcome. Receiver2 retains its quantum output and uses a local block decoder. The finite cqMAC has conditional Holevo quantities3/2 each and joint quantity3/2+h2(1/4). Winter's established independent-message coding theorem and a probability-preserving classical-register pinching implement the decoder by allowed LOCC. The finite exact verifier supports the algebra; coding achievability is analytical.

The Bell decomposition and forwarding protocols and general multiple-access framework are credited to earlier authors. The bounded primary-literature audit found no earlier explicit or established-equivalent achievement of this exact target in the inspected corpus; documented auxiliary-body access/version limits remain. Categorical worldwide firstness and continued openness in every later source are not certified. This is the specific W-state application, not a new general Bell or coding theorem.

The current paper is [Asymptotic LOCC dense coding with the symmetric four-qubit W state](https://doi.org/{doi}), Alec Kriebel (ORCID0009-0001-9320-500X), version1.0, dated4October2026. Record: {record}. The complete eight-file package contains PDF, standalone LaTeX, standard-library rational verifier, results, priority supplement, README, license and digests. Two sequential independent whole-package AI reviewers audited it; round1's minor formula-domain and citation corrections were propagated to the frozen internal v2, and the new round2 found no required issue. Internal audit revisionv2 remains the first published version1.0. AI tools were used extensively; this is an unrefereed preprint without conventional human peer review.

No exact optimal capacity, one-copy advantage, zero-error/maximal-error code, constructive finite-blocklength bound or experimental implementation is asserted. The strict achieved rate proves the source's asymptotic classification; two measured Bell outputs alone have information2 for this particular ensemble, not a general converse.

The original19 submitted files, including status.json, readiness.json and turns.jsonl, are preserved as dated September30 inputs. Their novelty-unestablished caveats describe that historical stage. Original proof budget1/5; new central proof search0. Current acceptance.json and the single present-day state/history import record the later audited publication without inventing historical lifecycle transitions. Original head dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3.

Audit evidence: draft_pr_publication_program_20260930/audits/pr80_30000177/ROOT_FINAL_PACKAGE_GATE_20261004.json, both whole_preprint review folders, ROOT_PUBLICATION_VERIFICATION_20261004.json and ROOT_TRACKER_VERIFICATION_20261004.json. Tracker range: {track['range']}. Mathematical and bounded priority audit100%; preprint/publication/tracker gates complete. Repository acceptance is recorded separately after the exact-head merge.
'''
priority=f'''# Current bounded priority assessment

The specific original-model W4 asymptotic achievability and classification pass the bounded priority gate. Cao-Song's2006 paired Bell decomposition, Pradhan-Agrawal-Pati's2007 Bell forwarding/two-bit protocol, Winter's cqMAC theorem and Huang-Zhang-Hou's general multiple-access dense coding are established and expressly credited. The contribution is the retained local cq output, its exact independent-message information quantities and the strict achieved W4 rate in the original receiver cut.

Closest-source comparisons distinguish sender message disclosure/different ownership, Bell-to-Bell one-copy decoding, common quantum-receiver routing, LOCC upper bounds and Hayashi-Wang's different fixed-helper/multiplicity assumptions. MWW2008 permits product isotropic measurements in arbitrary dimensions; its lower bound and the supplement's separate instrument-specific upper comparison are not general LOCC converses. The obsolete2xn exclusion is preserved only as a corrected historical audit issue.

The inspected corpus and exact access/version limits are in the published PRIORITY_AUDIT.md at {record}. No global firstness, optimal-capacity or assertion that every auxiliary paper has been read is made. Specific unread bodies and unconfirmed journal/preprint identities are disclosed; no identified source supplies an explicit or established-equivalent strict-rate resolution of the exact original target. This is ordinary bounded literature clearance, not an extension of PR50's priority-unresolved publication exception.

Canonical ROOT priority gate and three independent priority families reside in draft_pr_publication_program_20260930/audits/pr80_30000177/. Two sequential whole-package reviews independently scrutinized the model, closest prior-equivalence comparisons and stated limitations. Publication DOI: {doi}. Original1/5; new central proof search0; no conventional human peer review.
'''
body=f'''The symmetric four-qubit W state is LOCC dense-codeable in the original asymptotic model: two independent senders each transmit one qubit to a separate receiver and achieve rates9/8 bits per copy each with vanishing uniform average error. The stronger sum-rate supremum lower bound is3/2+h2(1/4)=2.311278... bits per copy. Receiver1's complete Bell instrument forwards only a classical string; receiver2's block decoder stays local. The optimal capacity and one-copy behavior remain unresolved.

Published research note: [Asymptotic LOCC dense coding with the symmetric four-qubit W state](https://doi.org/{doi}), Alec Kriebel, v1.0. The eight-file package includes a standalone manuscript, exact rational verifier and documented bounded priority audit. Earlier Bell protocols and the established cqMAC coding theorem are credited; no categorical worldwide firstness is asserted.

Validation: three distinct mathematical audit families; bounded primary-source priority audit; two sequential whole-package adversarial AI reviews, with round1 minor corrections applied before the new clean round2;551 exact finite verifier checks and independent determinant reconstruction; complete PDF/source/metadata checks. Public payload bytes and intended Zenodo metadata were verified, and the DOI tracker row was independently read back at {track['range']}.

AI tools were used extensively; this is an unrefereed preprint without conventional human peer review. All19 original submitted scientific files and the original1/5 proof ledger are preserved as dated inputs; present-day acceptance records the later publication. New central proof search0.
'''
for name,text in [('CURRENT_RESULT.md',result),('CURRENT_PRIORITY.md',priority),('PR_BODY.md',body)]: (P/name).write_text(text)
old_rows=[x for x in (R/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines(keepends=True) if '| 30000177 /' in x]
assert len(old_rows)==1
cells=old_rows[0].split('|'); assert len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5'
cells[8]=' preprint_published ';cells[9]=' 1/5 ';cells[11]=' Verified original-model W4 LOCC-DC: independent9/8 rates, sum lower bound3/2+h2(1/4)>2; bounded priority, credited prior methods, two sequential AI package reviews; unrefereed preprint. ';cells[12]=f' [{doi}](https://doi.org/{doi}) '
after='|'.join(cells)
assert after.endswith('\n')
checkpoints=[]
for directory in (A/'publication_package_v1',A/'publication_package_v2'):
    checkpoints.extend(directory/item['path'] for item in load(A/('PUBLICATION_PACKAGE_V1_REVIEW_SNAPSHOT_20261004.json' if directory.name.endswith('v1') else 'PUBLICATION_PACKAGE_V2_REVIEW_SNAPSHOT_20261004.json'))['files'])
roots=['ROOT_PRIORITY_GATE_20261004.md','ROOT_PRIORITY_ADJUDICATOR_READBACK_20261004.json','PRIORITY_AND_PUBLICATION_RESEARCH_LOG_20261004.md','PUBLICATION_AND_INTEGRATION_PLAN_20261004.md','PUBLICATION_PACKAGE_V1_REVIEW_SNAPSHOT_20261004.json','PUBLICATION_PACKAGE_V2_REPAIR_RECEIPT_20261004.json','PUBLICATION_PACKAGE_V2_REVIEW_SNAPSHOT_20261004.json','ROOT_V2_VISUAL_AND_REPAIR_ADJUDICATION_20261004.json','ROOT_FINAL_PACKAGE_GATE_20261004.json','ROOT_PUBLICATION_VERIFICATION_20261004.json','ROOT_TRACKER_VERIFICATION_20261004.json','ROOT_MATHEMATICAL_CHECKPOINT_COMMIT_RECEIPT_20261004.json','ROOT_MATH_CHECKPOINT_WINDOW_RELEASE_20261004.json']
checkpoints.extend(A/name for name in roots)
for directory in ('target_priority_family_20261004','mechanism_priority_family_20261004','priority_gate_adjudicator_20261004','whole_preprint_round1_20261004','whole_preprint_round2_20261004','operational_review_20261004'):
    for name in ('REPORT.md','VERDICT.json','SOURCE_READ_SCOPE_LEDGER.md','SOURCE_READ_SCOPE_LEDGER.json','FIRST.md','SOURCE_FIRST.md','SCOPE_FIRST.md','RESEARCH_LOG.md','MANIFEST.json','EVIDENCE_MANIFEST.json','SOURCE_PINS.json','PROOF_RECONSTRUCTION.md'):
        path=A/directory/name
        if path.is_file(): checkpoints.append(path)
checkpoints.extend(P/name for name in ('CURRENT_RESULT.md','CURRENT_PRIORITY.md','PR_BODY.md'))
checkpoint_files={pin(p)['path']:pin(p) for p in checkpoints}
originals=[x for x in load(A/'original_source_authentication_20261004/ORIGINAL_BLOB_MANIFEST.json')['files'] if x['path'].startswith('unsolved_math_prioritization/attempts/30000177/')]
owned={x['path'] for x in originals}|{'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}|{'unsolved_math_prioritization/attempts/30000177/'+n for n in ('acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md')}|set(checkpoint_files)
response,out,err=capture('native_plan_current_PR_metadata',['/opt/homebrew/bin/gh','pr','view','80','--repo','AlecKriebel/Math','--json','title,body,headRefOid,state,isDraft'])
assert response['exit_code']==0
submitted=json.loads(out); assert submitted['headRefOid']=='dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3' and submitted['state']=='OPEN' and submitted['isDraft'] is True
bound=list(checkpoint_files.values())+[pin(F/'native_integrate.py'),pin(F/'capture.py'),pin(A/'original_source_authentication_20261004/ORIGINAL_BLOB_MANIFEST.json')]
plan={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CONCRETE_PLAN_AWAITING_ROOT_AND_OPERATIONAL_READBACK','ROOT_reviewed_for_execution':False,'PR':80,'head':submitted['headRefOid'],'DOI':doi,'record_url':record,'tracker_range':track['range'],'exact_claim':exact_claim,'submitted_title':submitted['title'],'submitted_body_sha256':hashlib.sha256(submitted['body'].encode()).hexdigest(),'current_title':'research(30000177): publish verified W-state LOCC dense-coding resolution','queue_after_row':after,'checkpoint_files':checkpoint_files,'bound_inputs':bound,'exact_owned_paths':sorted(owned),'phase_order':['merge','accept','checkpoint'],'completion_progress_update':'Separate actual-receipt checkpoint after this lease release; no future commit IDs or progress completion are asserted by this plan','original_budget':'1/5','new_central_proof_search_turns':0}
(A/'ROOT_NATIVE_PLAN_PREPARED_20261004.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'status':plan['status'],'owned_path_count':len(owned),'checkpoint_path_count':len(checkpoint_files),'DOI':doi,'tracker':track['range']},indent=2))
