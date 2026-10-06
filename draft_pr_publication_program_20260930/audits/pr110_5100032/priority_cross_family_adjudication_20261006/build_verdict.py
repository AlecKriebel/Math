#!/usr/bin/env python3
from pathlib import Path
import datetime,json,os,hashlib
D=Path(__file__).resolve().parent;A=D.parent
def pin(p):
    b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
v={'schema':'pr110-independent-cross-family-priority-adjudication/v1',
   'UTC':now,'actual_writer_PID':os.getpid(),'PR':110,'id':5100032,'code':'AMR-050-0032',
   'original_head':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35',
   'original_PROOF_sha256':'8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d',
   'recommended_state':'HOLD_FOR_ESSENTIAL_IDENTIFIED_VERSION_GAP',
   'recommended_gap_id':'M1','already_solved_supported':False,'earlier_full_cover_found':False,'earlier_result_mapping':None,
   'bounded_substantive_novelty_supported':True,'bounded_support_is_not_unrestricted_priority_clearance':True,
   'supported_candidate_contribution':'All-period ordinary-positive focal antipedal norm-difference identification q_plus−q_minus=Gamma Δy and closure proof, including odd primitive orbits and their repeats.',
   'prior_components':['Source-author numerical observation of k603','Classical supporting-line antipedal and circumcenter alias','Negative-pedal/polar-inverse relation','Focal-height product and optical/confocal ingredients','Generic closure telescoping','Centrally symmetric even-primitive case and repeats'],
   'exact_scope':'All regular closed orbits for a>b>0 and strictly nested confocal elliptical caustic0<lambda<b²; original unprimed antipedal vertices; ordinary finite positive Euclidean norms; every admitted period/winding/star/reversal/repeat. No individual-sum constancy, hyperbolic or singular endpoint claim.',
   'source_and_mathematics_clearance_inherited':True,'source_and_math_gate_pin':pin(A/'ROOT_MATHEMATICAL_GATE_20261006.json'),
   'priority_clearance':False,'publication_clearance':False,'absolute_priority_established':False,
   'original_effort':'2/5','new_central_proof_search_turns':0,
   'required_findings':[{'id':'M1','severity':'essential_priority_version_comparison','doi':'10.1007/s10883-022-09608-y','title':'Estimating Elliptic Billiard Invariants with Spatial Integrals','final':'JDCS29:757–767(2023), online10August2022','known_revision':'7April2022','complete_final_body_read':False,'complete_arxiv_2102_10899_v1_read':True,'current_prior_cover_evidence':False,'needed':'Obtain legitimate complete final; inspect actual governing definitions/statements/proofs and explicitly compare with precursor and full k603 scope in separately sealed supplement.','materiality_reason':'Identified direct source-author follow-up with later documented revision and final closed-expression invariant claim; available first page/captions do not authenticate exclusive theorem scope or final-body equivalence. Finite selected-candidate comparison; not a requirement to exhaust all literature.','counterevidence_acknowledged':'Complete precursor explicitly studies three non-k603 averages; available final captions remain consistent with them and do not announce k603 proof. No assertion that final probably contains a solution.','pending_human_question_used_as_evidence':False}],
   'nonessential_bounded_audit_limits':[
      {'id':'IMPA_final_book','full_final_read':False,'authenticated_author_source_commit':'0b5b417fe2ba3185087979749bc8bcf8c702315d','source_date':'7June2021','final_printing':'July2021','authenticated_source_files':145,'relevant_invariant_chapter_independently_read':True,'final_equivalence_certified':False,'effect':'Retain explicit version boundary; bars unqualified final-book exclusion and absolute priority. No identified extra covering mechanism; does not itself negate bounded support.'},
      {'id':'Lockwood_and_historical_corpus','Lockwood_1957_original_full_read':False,'known_mechanism_independently_checked_in':'Salmon1879 Arts121–122 and focal-envelope example','effect':'Nonexhaustive historical bound; no identified full closed-orbit theorem stranded here.'},
      {'id':'source_video_and_low_N_notebook_bodies','bodies_read':False,'effect':'Discovery credit supported by ledger, but no negative full-content claim. Low-N metadata is not prior full-cover evidence.'},
      {'id':'other_scoped_bodies_and_global_search','effect':'Respect all read/version/index limits; no exhaustive literature or every-final-read claim.'}],
   'reporting_conditions_after_gap_resolution':[
      'Credit Reznik–Garcia–Koiller for the observation, with exact source and version.',
      'Credit classical geometry, known focal-height product, generic telescoping and even symmetry; claim the norm-difference/full-period proof as the candidate addition.',
      'Retain exact ordinary metric, parent polygon, period/winding/branch and version boundaries; avoid absolute-first and unread-final-examined claims.',
      'Propagate existing root mathematical gate checksum and optimization package findings in any later package.'],
   'completion_estimate':{'bounded_adjudication_percent':100,'source_math_proof_percent':100,'selected_candidate_priority_clearance_work_percent':90,'estimate_is_probability_of_novelty':False,'overall_publication_workflow_percent':'not assessed by this reviewer'},
   'authentication':{'all_three_reports_and_verdicts_read_in_full':True,'public_sealed_input_payload_bodies':514,'closing_envelopes':3,'private_file_pins':256,'author_book_Git_blob_bodies':145,'actual_normal_optimized_transfer_controls_authenticated':4,'controls_are_universal_novelty_certificates':False,'input_authentication_pin':pin(D/'INPUT_AUTHENTICATION.json'),'custody_read_scope_pin':pin(D/'CUSTODY_AND_READ_SCOPE.json')},
   'independence':{'new_combined_adversarial_adjudication':True,'family_conclusions_treated_as_hypotheses':True,'decisive_primary_statements_and_proofs_independently_inspected':True,'no_other_primary_scope_invented':True,'external_access_searches':0,'external_contact_or_prepared_outreach':False,'mutations_outside_dedicated_output_folder':False,'git_native_status_PR_paper_editor_publication_mutations':False,'initial_git_status_read_only_and_unnecessary':True},
   'status_action':'No unilateral status change. Preserve proof/source/math and hold priority promotion for M1. If a full covering prior is found, supply exact mapping and recommend already_solved; otherwise bounded substantive contribution supported with retained limits.'}
(D/'VERDICT.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — 100% of bounded combined adjudication complete; selected-candidate current-priority work estimate90%, not a probability of novelty. Recommended narrow hold M1; no earlier full cover located; positive bounded substantive novelty support retained. Independently assessed pending human question as irrelevant to materiality. Final IMPA/Lockwood/media/version limits preserved, no already_solved or publication approval. Report/verdict saved; seal remains.\n')
print(json.dumps({'state':v['recommended_state'],'actual_PID':os.getpid(),'bounded_adjudication_percent':100,'priority_gap':'M1'}))
