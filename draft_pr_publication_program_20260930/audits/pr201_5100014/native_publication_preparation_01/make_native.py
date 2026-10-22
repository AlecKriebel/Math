"""Pure current PR201 presentation; requires verified publication/tracker facts."""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent.parent
HEAD='90bdb85235979f2ffa7496b9b689036654e55200'
CASE='draft_pr_publication_program_20260930/audits/pr201_5100014/'
NATIVE='unsolved_math_prioritization/attempts/5100014/'
def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
def originals():
    j=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
    assert j['original_head']==HEAD and j['original_QUEUE_status']=='claimed_solved' and len(j['files'])==24
    out={}
    for name,x in j['files'].items():
        f=A/'original_submitted_head'/name;b=f.read_bytes()
        assert not f.is_symlink() and len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
        out[name]=b
    return out
def construct(stage,f):
    assert stage in ['published_pending_merge','actual_merge_accepted','factual_checkpoint_accepted']
    assert f['publication_ready_gate_accepted'] and f['actual_publication_verified'] and f['actual_tracker_row_verified'] and not f['historical_priority_established']
    assert f['DOI']=='10.5281/zenodo.'+str(f['record_id']) and len(f['whole_package_review_events'])>=2
    if stage!='published_pending_merge':assert f['actual_merge_receipt']['accepted'] and f['actual_merge_receipt']['original_head']==HEAD
    if stage=='factual_checkpoint_accepted':assert f['actual_factual_receipt']['accepted']
    old=originals();out=dict(old);url='https://doi.org/'+f['DOI']
    state={'published_pending_merge':'Published and tracked; original-HEAD-safe merge pending.','actual_merge_accepted':'Original-HEAD-safe merge accepted; factual completion pending.','factual_checkpoint_accepted':'Published, tracked and merged; actual factual checkpoint accepted.'}[stage]
    theorem='For a>b>0 and a fixed proper nested nondegenerate confocal elliptical caustic with primitive least N=2mod4>=6, the signed area of consecutive boundary-tangent intersections times the signed area of their pedal polygon is phase independent for every fixed finite real M. All admitted coprime star windings and reversal; zero or negative pedal area allowed.'
    overlap='Alper Ferudun, Outer-Pedal Area Products in Elliptic Billiards, v1.0 DOI10.5281/zenodo.23087221, retained in v1.1 DOI10.5281/zenodo.23088516: exact theorem, radial dependence, general six-period constant and repeated-triangle caveat.'
    scope='RGK arxiv2004.12497v11 Sec3.4/Table4p6 and distinct2021journal DOI10.1007/s40598-021-00174-y Table4p346: signed outer-pedal product, allM,N2mod4. The rows do not literally print primitive or least period. Least period is an explicit necessary interpretation; repeated odd trajectories listed an even number of times can fail. Historical proof? is not current openness.'
    timeline='Observed PR201 creation2026-10-01T05:18:49Z at original HEAD precedes current Zenodo v1.0 created16:56:14.316216Z/registered16:56:15Z and v1.1 created18:12:36.529602Z/registered18:12:37Z on that date. These are contemporaneous separate records, not first-public-visibility or independence certificates; earlier website disclosure unexcluded.'
    common={'UTC':f['UTC'],'problem_id':5100014,'original_head':HEAD,'status':'claimed_solved','publication_lifecycle_stage':stage,'state':state,'mathematical_result_valid':True,'exact_theorem':theorem,'publication_form':'Attributed alternative flag-curve proof research note','exact_contemporary_overlap':overlap,'source_contract':scope,'timeline_limits':timeline,'historical_priority_established':False,'independent_discovery_certified':False,'theorem_novelty_cleared':False,'proof_method_novelty_cleared':False,'current_worldwide_openness_certified':False,'classical_Steiner_radiality_Poncelet_framework_Chavez_AA_prime_credited':True,'extensive_AI_use':True,'conventional_human_peer_review':False,'unrefereed':True,'formal_proof_assistant_certification':False,'DOI':f['DOI'],'record_id':f['record_id'],'actual_publication_verified':True,'tracker_range':f['tracker_range'],'actual_tracker_row_verified':True,'publication_package':CASE+f['package'],'whole_package_review_events':f['whole_package_review_events'],'author_effort':'Original metadata/log report one substantive author turn, originalQUEUE1/5; actual model/reasoning effort unverified. Later mathematical, priority, package audits and publication separate.','actual_merge_receipt':f.get('actual_merge_receipt'),'actual_factual_receipt':f.get('actual_factual_receipt')}
    out['CURRENT_STATUS.json']=enc(common)
    out['README.md']=f'''# 5100014 / k303,a: an attributed flag-curve proof
{state}

Research note: [{f['DOI']}]({url}). Alec Kriebel, ORCID0009-0001-9320-500X. Extensive AI use; unrefereed; no conventional independent human peer review or formal proof-assistant certification.

{theorem}

{overlap} The note supplies a quotient/two-pole Riemann-Roch presentation and a self-contained target-parity verification of the already credited AA-prime law. Neither the theorem, its rewritten proportionality, ancillary formulas/caveat nor broad pole-cancellation methods are claimed novel. Steiner radiality, established genus-one Poncelet geometry and Chavez-Caliz's AA-prime theorem are credited.

{scope}

{timeline} The manuscript and expanded checks are dated16October2026, not backdated to the author submission.

CANDIDATE.md is the original mathematical proof with current attribution, source interpretation and publication status corrected. CURRENT_PROOF.md indexes the complete publication proof and its verified AA-prime dependency. CURRENT_STATUS.json and CURRENT_SOURCE_AND_PRIORITY.json govern current lifecycle and scope. SOURCE_AUDIT.md supersedes the original literal-primitive overstatement. Original source_record, source_manifest, prior_imported_report, turns and review files are dated provenance, not current priority or publication claims.

All24 original submitted files are byte-exact in [the immutable archive](../../../{CASE}original_submitted_head/). The historical FROZEN_MANIFEST and independent_review hashes target that archive. Original reviewer scripts are historical assertion-based controls; use a disposable copy of the archived layout and ordinary Python. Python-O prints legacy PASS with zero enforced assertions. The current portable verification package uses explicit exceptions and rejects deliberate false identities in both modes. SHA256SUMS authenticates this current native presentation.

Original substantive author effort is one turn, QUEUE1/5; actual model and reasoning effort unverified. Three later mathematical families include a partial Euclidean reduction, not three independent full proofs. Priority and successive whole-package reviews are separate later AI work. All later receipts and exact payload hashes are in [the reviewed package](../../../{CASE}{f['package']}/).
'''.encode()
    candidate=old['CANDIDATE.md'].decode()
    candidate=candidate.replace('# k303,a: a two-pole proof candidate','# k303,a: an attributed two-pole proof',1)
    candidate=candidate.replace('Complete candidate, pending separate adversarial review.','Current verified mathematical presentation; extensive AI review, unrefereed.',1)
    candidate=candidate.replace('This is precisely Table 4, k303,a,','This is an explicit least-period interpretation of Table 4, k303,a,',1)
    candidate=candidate.replace('This proves the exact k303,a assertion if the preceding pole argument passes separate review.','This proves the scoped k303,a assertion. The local pole argument and credited dependency were separately audited; historical novelty and independence are not certified.',1)
    candidate=candidate.replace('## 7. Finish the proof candidate','## 7. Finish the proof',1)
    candidate=candidate.replace('## 9. Review targets','## 9. Verification targets',1)
    notice='\n\nCurrent publication: '+url+'. '+state+' '+overlap+' '+scope+' This is an alternative presentation, with no theorem/method novelty, firstness or certified independence claim. The original submitted version is preserved unchanged in the custody archive.\n\n'
    pos=candidate.index('\n');candidate=candidate[:pos]+notice+candidate[pos+1:]
    out['CANDIDATE.md']=candidate.encode()
    out['CURRENT_PROOF.md']=('# Current publication proof\n\n'+theorem+'\n\nPublished note: '+url+'. Exact source: '+CASE+f['package']+'/outer_pedal_flag.tex. The full two-pole proof is in CANDIDATE.md and the manuscript. The following verification is of the credited Chavez-Caliz product under target parity; it is not a new theorem. The separate supplemental source-family audit and completed publication reviews accepted the verification.\n\n').encode()+(A/'ROOT_AREA_PRODUCT_DEPENDENCY_VERIFICATION_01.md').read_text().replace('Adversarial review of this supplemental verification is pending.','The supplemental source-family audit accepted this verification; current whole-package review and lifecycle facts are recorded in CURRENT_STATUS.json.').encode()
    out['CURRENT_SOURCE_AND_PRIORITY.json']=enc({**common,'bounded_priority_audit_complete':True,'Root_source_correction':CASE+'ROOT_SOURCE_SCOPE_CORRECTION_01.md','priority_ledgers':CASE+f['package']+'/materials/audit/','original24_unchanged_archive':CASE+'original_submitted_head/','unrestricted_repeat_or_unsigned_extension':False})
    out['SOURCE_AUDIT.md']=('# Current literal source and attribution\n\n'+scope+'\n\n'+overlap+'\n\n'+timeline+'\n\nCurrent published note: '+url+'. '+state+'\n\n').encode()+(A/'ROOT_SOURCE_SCOPE_CORRECTION_01.md').read_bytes()
    out['QUALIFIED_PRIORITY.md']=(A/'ROOT_PRIORITY_AND_EDITORIAL_DECISION_01.md').read_bytes()+('\n\nCurrent published note: '+url+'. '+state+' The60percent decision above is dated preparation evidence. CURRENT_STATUS.json supplies actual lifecycle facts.\n').encode()
    out['PUBLICATION_STATUS.json']=enc({**common,'historical_original_publication_status':json.loads(old['PUBLICATION_STATUS.json'])})
    out['FROZEN_MANIFEST.json']=enc({'scope':'Historical original manifest; targets immutable archive, not current native presentation.','files_root':CASE+'original_submitted_head/','historical_original_manifest':json.loads(old['FROZEN_MANIFEST.json']),'current_native_hashes':'SHA256SUMS'})
    out['CANDIDATE_REVISION.json']=enc({'historical_original_revision':json.loads(old['CANDIDATE_REVISION.json']),'current_candidate_sha256':hashlib.sha256(out['CANDIDATE.md']).hexdigest(),'current_revision_scope':'Presentation and attribution/source/status corrections; original core mathematical argument retained, original24 archived unchanged.','current_publication':common})
    out['readiness.json']=enc({'historical_original_readiness':json.loads(old['readiness.json']),'current_publication':common,'original_source_literal_primitive_claim_superseded':True})
    pct=100 if stage=='factual_checkpoint_accepted' else 95
    out['RESEARCH_LOG.md']=old['RESEARCH_LOG.md']+('\n\n'+f['UTC']+' — Current publication checkpoint: '+state+' DOI '+f['DOI']+'; tracker '+f['tracker_range']+'. Exact contemporary theorem and classical inputs credited, original literal source wording corrected; no theorem/method novelty, firstness or certified independence. Original24 archived unchanged; original one-author-turn report retained, actual model/effort unknown. Estimate math100percent, case workflow'+str(pct)+'percent. Completion postimage effective only after actual full-scope MAIN acceptance.\n').encode()
    out['SHA256SUMS']=''.join(hashlib.sha256(b).hexdigest()+'  '+name+'\n' for name,b in sorted(out.items()) if name!='SHA256SUMS').encode()
    assert set(out)==set(old)|{'CURRENT_STATUS.json','CURRENT_PROOF.md','CURRENT_SOURCE_AND_PRIORITY.json','QUALIFIED_PRIORITY.md','SHA256SUMS'} and len(out)==29
    changed={'README.md','CANDIDATE.md','SOURCE_AUDIT.md','PUBLICATION_STATUS.json','FROZEN_MANIFEST.json','CANDIDATE_REVISION.json','readiness.json','RESEARCH_LOG.md'}
    unchanged=set(old)-changed
    assert len(unchanged)==16 and all(out[n]==old[n] for n in unchanged)
    return {NATIVE+name:b for name,b in out.items()}
