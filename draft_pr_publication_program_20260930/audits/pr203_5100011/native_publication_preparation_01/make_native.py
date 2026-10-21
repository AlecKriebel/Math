"""Pure PR203 presentation; no mutations, publication facts required at invocation."""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent.parent
HEAD='8edca9d773c085adb4ed0611357a7a2957e3395d'
CASE='draft_pr_publication_program_20260930/audits/pr203_5100011/'
NATIVE='unsolved_math_prioritization/attempts/5100011/'
def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
def originals():
 j=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
 assert j['original_head']==HEAD and j['original_QUEUE_status']=='claimed_solved' and len(j['files'])==18
 out={}
 for n,p in j['files'].items():
  q=A/'original_submitted_head'/n;b=q.read_bytes()
  assert not q.is_symlink() and len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p['git_blob']
  out[n]=b
 return out
def construct(stage,f):
 assert stage in ['published_pending_merge','actual_merge_accepted','factual_checkpoint_accepted']
 assert f['publication_ready_gate_accepted'] and f['actual_publication_verified'] and f['actual_tracker_row_verified'] and not f['historical_priority_established']
 assert f['DOI']=='10.5281/zenodo.'+str(f['record_id']) and len(f['whole_package_review_events'])>=2
 if stage!='published_pending_merge':assert f['actual_merge_receipt']['accepted'] and f['actual_merge_receipt']['original_head']==HEAD
 if stage=='factual_checkpoint_accepted':assert f['actual_factual_receipt']['accepted']
 old=originals();out=dict(old);url='https://doi.org/'+f['DOI']
 state={'published_pending_merge':'Published and tracked; original-HEAD-safe merge pending.','actual_merge_accepted':'Original-HEAD-safe merge accepted; factual completion pending.','factual_checkpoint_accepted':'Published, tracked and merged; actual factual checkpoint accepted.'}[stage]
 theorem='For a>b>0,0<lambda<b^2, fix the outer ellipse and proper confocal elliptical caustic. If the physical family has least N divisible by four, its signed original-trajectory area times signed area of perpendicular feet of each fixed finite real M on the original complete side lines is phase independent. All admitted coprime primitive stars and both traversal orientations; zero or negative pedal areas allowed.'
 overlap='Alper Ferudun, Pedal Areas of Periodic Elliptic Billiard Trajectories with Respect to an Arbitrary Point, v1.0,15October2026, DOI10.5281/zenodo.23400541, TheoremA: the same theorem, with stronger complex-M allowance; also radial dependence, four-period value and repeated-orbit caveat. Section4 uses complementary poles and reversal zeros; the example here is a rescaling of his Table2.'
 scope='Reznik-Garcia-Koiller journal DOI10.1007/s40598-021-00174-y Section3.3/Table3p346 and arxiv2004.12497v11 Table3p6 give k203,a as signed original-side pedal product,allM,N0mod4. They do not literally print primitive or least period. This note imposes that necessary explicit interpretation; doubling primitive-six trajectories gives a nominal12-entry counterexample to the unrestricted interpretation. The historic question mark is not a current-openness certificate.'
 timeline='The currently public original PR203 record gives server creation2026-10-01T05:24:27Z and original HEAD8edca9d773c085adb4ed0611357a7a2957e3395d contains the preserved proof. Ferudun record23400541 was created2026-10-15T16:11:42.588744Z and DataCite registered16:11:43Z. These are verified object-record dates, not authenticated discovery times, historical visibility at every instant, earliest disclosure or certified independent discovery. Separate contemporary records; no firstness claim. The current manuscript and later audits are dated16October2026, not backdated.'
 method='This is an attributed incidence-curve presentation using explicit branch charts and complementary pole/zero cancellation. Established Poncelet flag curves/involutions/meromorphic methods are credited to Schwartz-Tabachnikov, AST and Chavez-Caliz; Steiner radiality and the Bialy-Tabachnikov earlier four-period implication are credited. Neither theorem nor proof method is claimed novel. The published proof does not require the original Jacobi/contact-trace route or the separate credited AA-prime theorem; those original inputs were independently audited and are preserved as provenance.'
 effort='Original author metadata/log report two substantive turns, originalQUEUE2/5. Actual model/reasoning effort and historical optimized/ordinary runtime are unverified. Shared central-pedal mechanism was author input, not independent review. Later distinct mathematical families, bounded priority and whole-package reviews are separate AI work; the direct Euclidean route is partial for general N and is not counted as a full additional proof.'
 common={'UTC':f['UTC'],'problem_id':5100011,'original_head':HEAD,'status':'claimed_solved','publication_lifecycle_stage':stage,'state':state,'mathematical_result_valid':True,'exact_theorem':theorem,'publication_form':'Attributed alternative incidence-curve proof research note','exact_contemporary_overlap':overlap,'source_contract':scope,'timeline_limits':timeline,'method_credit_and_limits':method,'historical_priority_established':False,'independent_discovery_certified':False,'theorem_novelty_cleared':False,'proof_method_novelty_cleared':False,'current_worldwide_openness_certified':False,'extensive_AI_use':True,'conventional_human_peer_review':False,'unrefereed':True,'formal_proof_assistant_certification':False,'DOI':f['DOI'],'record_id':f['record_id'],'actual_publication_verified':True,'tracker_range':f['tracker_range'],'actual_tracker_row_verified':True,'publication_package':CASE+f['package'],'whole_package_review_events':f['whole_package_review_events'],'author_effort':effort,'actual_merge_receipt':f.get('actual_merge_receipt'),'actual_factual_receipt':f.get('actual_factual_receipt')}
 out['CURRENT_STATUS.json']=enc(common)
 out['README.md']=f'''# 5100011 / k203,a: an attributed original-side pedal proof
{state}

Research note: [{f['DOI']}]({url}). Alec Kriebel, ORCID0009-0001-9320-500X. Extensive AI use; unrefereed; no conventional human peer review or formal proof-assistant certification.

{theorem}

{overlap}

{method}

{scope}

{timeline}

CURRENT_PROOF.md indexes the complete published incidence-curve proof. PROOF.md retains the original submitted Jacobi/contact-trace argument byte-for-byte; its mathematical content was separately verified, and current scope/attribution/lifecycle are governed by CURRENT_STATUS.json and CURRENT_SOURCE_AND_PRIORITY.json. SOURCES.md records the current bounded priority audit; its historical version remains in the archive.

All18 original files are byte-exact in [the immutable custody archive](../../../{CASE}original_submitted_head/). MANIFEST.json wraps the historical original manifest and explicitly targets that archive. Original source_manifest, turn logs, continuity, verification JSON and independent_review records are dated provenance, not current novelty/publication claims. Their original hashes refer to the archive; SHA256SUMS authenticates the current native presentation.

Original checkers use removable Python assertions. Fresh ordinary replays enforce24,110 author and20,578 reviewer checks and match archived stdout bytes. Under Python-O they advertise the counts while enforcing zero assertions and allow deliberately false identities. Historical runtime is unknown. Use the supported portable exception-based runner in the reviewed verification package, which rejects wrong coefficients and false guards under ordinary and optimized Python; run historical scripts only in a disposable copy with ordinary Python. Finite noninterval diagnostics do not prove the theorem.

{effort}

Complete paper, exact metadata, all18 original files, independent derivations/reproduction and source records are in [the reviewed package](../../../{CASE}{f['package']}/). Full third-party PDFs/OCR, credentials, dependency implementations and private operational caches are excluded.
'''.encode()
 out['CURRENT_PROOF.md']=('# Current verified publication proof\n\n'+theorem+'\n\nPublished note: '+url+'. Exact source: '+CASE+f['package']+'/original_pedal_flag.tex. Sections2-4 give the complete incidence-curve proof, including real half-period for primitive stars, physical-step identification, explicit ramification charts, branch double-to-simple pole reduction includingN4, parity-separated supports and complementary signed zeros. Section5 credits classical radial dependence/four-period implications and gives exact boundary controls. The proof does not divide by areas or coefficients depending onM.\n\n'+method+'\n\nOriginal PROOF.md is retained byte-for-byte as the independently audited submitted Jacobi/contact-trace proof. Current source/scope/priority qualifications here supersede dated historical openness/search statements, without altering original provenance.\n').encode()
 out['CURRENT_SOURCE_AND_PRIORITY.json']=enc({**common,'bounded_priority_audit_complete':True,'priority_ledgers':CASE+f['package']+'/materials/audit/','original18_unchanged_archive':CASE+'original_submitted_head/','unrestricted_repeated_list_unsigned_hyperbolic_degenerate_extension':False})
 out['SOURCES.md']=('# Current source, credit and bounded priority audit\n\n'+scope+'\n\n'+overlap+'\n\n'+method+'\n\n'+timeline+'\n\n'+effort+'\n\nCurrent published note: '+url+'. '+state+'\n\nOriginal SOURCES.md and its listed author-input/source claims are preserved unchanged in the custody archive. The earlier bounded search did not find the now-credited exact Ferudun theorem. The current complete source/priority records are under '+CASE+f['package']+'/materials/audit/. No exhaustive novelty or worldwide openness certificate is claimed. Historical priority decision follows as dated preparation evidence; CURRENT_STATUS.json governs actual publication/integration.\n\n').encode()+(A/'ROOT_PRIORITY_AND_EDITORIAL_DECISION_01.md').read_bytes()
 out['QUALIFIED_PRIORITY.md']=(A/'ROOT_PRIORITY_AND_EDITORIAL_DECISION_01.md').read_bytes()+('\n\nCurrent published note: '+url+'. '+state+' The dated decision above predates actual publication. CURRENT_STATUS.json supplies current verified facts.\n').encode()
 out['MANIFEST.json']=enc({'scope':'Historical original manifest targets immutable archive, not current edited presentation.','files_root':CASE+'original_submitted_head/','historical_original_manifest':json.loads(old['MANIFEST.json']),'current_native_hashes':'SHA256SUMS'})
 out['readiness.json']=enc({'historical_original_readiness':json.loads(old['readiness.json']),'historical_claims_not_current_priority_or_publication':True,'current_publication':common})
 pct=100 if stage=='factual_checkpoint_accepted' else 95
 out['RESEARCH_LOG.md']=old['RESEARCH_LOG.md']+('\n\n'+f['UTC']+' — Current publication: '+state+' DOI '+f['DOI']+'; tracker '+f['tracker_range']+'. Signed original-side/leastN0mod4 theorem verified; exact contemporary theorem and classical methods credited; no theorem/method novelty, firstness or certified independence. All18 originals archived,13 native scientific/historical files retained byte-for-byte including PROOF.md; original two-turn2/5 report retained, actual model/effort unknown. Math100percent; case workflow'+str(pct)+'percent. Completion postimage effective only after actual full-scope MAIN acceptance.\n').encode()
 out['SHA256SUMS']=''.join(hashlib.sha256(b).hexdigest()+'  '+n+'\n' for n,b in sorted(out.items()) if n!='SHA256SUMS').encode()
 changed={'README.md','SOURCES.md','MANIFEST.json','readiness.json','RESEARCH_LOG.md'}
 assert len(set(old)-changed)==13 and all(out[n]==old[n] for n in set(old)-changed)
 assert set(out)==set(old)|{'CURRENT_STATUS.json','CURRENT_PROOF.md','CURRENT_SOURCE_AND_PRIORITY.json','QUALIFIED_PRIORITY.md','SHA256SUMS'} and len(out)==23
 return {NATIVE+n:b for n,b in out.items()}

