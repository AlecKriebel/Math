"""Record completed root reading; does not mutate Git, PRs or native records."""
from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent
D=A/'root_priority_audit_20261006'
def pin(path):
    body=path.read_bytes()
    return {'path':str(path),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
source=A/'original_question_priority_adversary_20261006/private_sources'
published=pin(source/'takagi_adjoint2013.pdf')
earlier=pin(source/'takagi_1105.0072v1.pdf')
if published['sha256']!='6ada6b6669124acda5bb4b0bd25a98d07b39808c07e7d41c1f0ae1ba49e085e5':
    raise ValueError('Published body changed')
if earlier['sha256']!='24f38aecbf9b40edfa7ec223a08694f60934c41f13e213e9549883a8111eaa7c':
    raise ValueError('Earlier version body changed')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'schema':'pr117-root-exact-prior-reading/v1','UTC':now,'actual_operator_PID':os.getpid(),
 'PR':117,'immutable_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8',
 'published_source':published,'published_DOI':'10.2140/ant.2013.7.917',
 'root_actual_published_read_boundary':'Full operative matrix definition p937, full Remark4.3 p939, full Example4.4 p940; actual high-resolution pixels of all three pages viewed.',
 'earlier_source':earlier,'earlier_primary_url':'https://arxiv.org/pdf/1105.0072v1',
 'earlier_primary_metadata_url':'https://arxiv.org/abs/1105.0072v1',
 'earlier_posted_UTC':'2011-04-30T10:42:16Z',
 'root_actual_earlier_read_boundary':'Full Remark4.3 across p18-19 and full Example4.4 p19; actual high-resolution pixels of both full pages viewed; actual arXiv version metadata read.',
 'exact_prior_same_ideal_and_singleton_fiber_condition':True,
 'published_from_candidate_zero_based_indices':[0,3,1,4,5,2],
 'ambient_c_zero_equality_vacuous':True,'third_generator_unit_minus_one':True,
 'complete_face_and_verification_valid_expository_additions':True,
 'substantive_new_open_problem_resolution_established':False,
 'bounded_priority_by_2011_not_absolute_earliest_claim':True,
 'additive_citation_glyph_correction':'Published p937 matrix tag is a triangle glyph, not equation(4); extracted text and sealed determinantal report numeral4 are an OCR/transcription citation error. Exact matrix, scope and result unaffected. Historical sealed report remains preserved; all current citations use page/Remark/Example.',
 'rejected_2006_scope_lead':'Yuen Corollary5.3 assumes r>s>=3 and excludes2-by-3 even after transposition; not used to date this exact result.',
 'rejected_wrong_guessed_MSP_URL':'Earlier p05 URL was a different paper; only actual p06-s body is used.',
 'proposal':pin(D/'ROOT_PROPOSED_DISPOSITION.md'),
 'prepared_comment':pin(D/'PROPOSED_CLOSURE_COMMENT.md'),
 'fresh_adversarial_disposition_review_pending':True,'closure_or_native_action_performed':False,
 'math_source_percent':100,'exact_priority_percent':95,'workflow_percent':55,
 'completed_PRs':19,'dated_eligible_total':99,'program_percent':19/99*100,
 'goal_active':True,'main_index_writer_released':True,'new_central_proof_turns':0}
out=D/'ROOT_EXACT_PRIOR_REASONING_20261006.json'
if out.exists():raise ValueError('Existing reading receipt; inspect before repeat')
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as handle:
    handle.write('\n'+now+': Root actually read and visually inspected the exact same Takagi Example4.4 in formal2013 pp937/939/940 and earlier arXivv1 pp18-19; primary arXiv history dates it2011-04-30. Exact c=0/sign/coordinate bridge identifies explicit prior negative answer. Useful full-face exposition preserved; novel original-target resolution not established. Small triangle-versus-OCR4 citation correction additive, historical report preserved. Fresh independent disposition reviewer running; closure/native still unperformed; main/index writer released. Math/source100%, priority95%, workflow55%, program19/99=19.19%, published11; goal active.\n')
print(json.dumps({'UTC':now,'PID':os.getpid(),'receipt':pin(out),'math_source_percent':100,'priority_percent':95,'workflow_percent':55,'remote_mutations':False}))
