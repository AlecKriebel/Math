"""Create explicit native PR179 templates; no Git/index/ref or remote mutation."""
from pathlib import Path
import datetime,hashlib,json,shutil,sys
A=Path(__file__).resolve().parent
D=A/'integration_preparation'
ORIGINAL='090b45356f5d6829f755fbc7c5b1fde5565de695'
O=A/'original_submission/files/unsolved_math_prioritization/attempts/10800007'
PK=A/'publication_package_v2'
def require(x,k):
 if not x:raise RuntimeError(k)
def read(p):return json.loads(p.read_text())
def save(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
final=sys.argv[1]=='final'
require(sys.argv[1] in ['pending','final'],'Unknown mode')
stage='native_template_final_01' if final else 'native_template_pending_01'
T=D/stage;require(not T.exists(),'Never overwrite template generation')
D.mkdir(exist_ok=True);T.mkdir()
stamp=datetime.datetime.now(datetime.UTC).isoformat()
files=sorted(p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file())
require(len(files)==20,'Original native scope changed')
for n in files:
 for target in [T/n,T/'historical_original'/n]:target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(O/n,target)
# Original frozen proof remains canonical; its original pending header is explicitly superseded.
repair=A/'mathematical_repair_v1'
for n in ['verify.py','verification.json','review/independent_checks.py','review/independent_results.json']:
 shutil.copyfile(repair/n,T/n)
shutil.copyfile(repair/'verify.py',T/'review/author_replay/verify.py')
for n in ['review/author_replay/verification.json','review/author_replay_stdout.json']:
 shutil.copyfile(repair/'verification.json',T/n)
require(sha(T/'NO_COVER.md')=='d88322ab825acd97914b898018116f2544dc92c460fe3c37ac86eeab331a8448','Original proof drift')
shutil.copytree(PK/'verification',T/'exact_verification')
shutil.copyfile(PK/'no_open_root_cover.tex',T/'no_open_root_cover.tex')
publication={'state':'not_published','DOI':None,'review02_pending':True}
if final:
 gate=read(A/'ROOT_PUBLICATION_GATE.json');pub=read(A/'ZENODO_PUBLICATION_READBACK.json');track=read(A/'TRACKER_ACCEPTANCE.json')
 require(gate['status']=='READY_FOR_AUTHORIZED_PUBLICATION' and pub['state']=='published','Actual publication gate absent')
 require(track['status']=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and track['DOI']==pub['doi'],'Actual tracker gate absent')
 publication={'state':'published','DOI':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'tracker_range':track['range'],'review02_pending':False}
save(T/'PUBLICATION.json',{'UTC':stamp,**publication,'PR':179,'original_head':ORIGINAL,'package':'publication_package_v2','mathematical_scope':'Complete negative answer to literal allR6 ordinaryopen exactcontinuousrootselection Problem2A; no admissible cover at anycardinality.','classical_method_credited':True,'historical_firstness_or_guaranteed_novelty_certified':False,'approximate_2B_or_unprinted_repaired_problem_resolved':False,'extensive_AI':True,'conventional_human_peer_review':False})
(T/'README.md').write_text("""# PR179: the literal exact-root question

The original NO_COVER.md proof remains byte-identical. Its original pending-review header is a dated historical statement superseded by this current record. The verified conclusion is that no ordinary-open cover of all R6 supports point-valued continuous exact real-root selections at any cardinality. The translated family in no_open_root_cover.tex shows that deleting only the zero vector does not repair the family. The source's intended modified question and approximate Problem2B are not resolved.

This is an explicit formulation note using classical topology and the source's own square-root slice. Historical firstness and guaranteed novelty are not established. SOURCE_AUDIT.md and exact_verification/PRIORITY_AUDIT.md record the bounded body/version/search limits. AI tools were used extensively; unrefereed, no conventional human peer review.

The current sampled author and rational-circle reviewer diagnostics use explicit guards active with optimization; they retain their limited finite-check scope. Run python3 verify.py or python3 review/independent_checks.py; the first writes a new local verification.json. Finite samples are supplementary and do not prove topology.

The stronger exact-rational supported-polynomial certificate is under exact_verification, byte-identical to the reviewed publication code/models. Python 3.11 or later is required. From that directory run python3 run_controls.py --output fresh-results.json. Its two valid orientations pass and thirteen invalid/unsupported controls fail, in ordinary and optimized modes. High-degree positivity is unsupported. The written proof supplies continuity and connectedness. The historical REPRODUCTION.json records actual v1 runs on unchanged v2 scientific inputs, not new native-location runs.

PUBLICATION.json states actual publication/tracker state. Original author-source metadata and unsafe pre-repair scripts are preserved verbatim only under historical_original; they are dated evidence, not current execution advice or priority clearance.
"""+('\nPublished preprint: '+publication['doi_url']+'\n' if final else '\nSecond fresh package review and publication/disposition remain pending.\n'))
shutil.copyfile(PK/'verification/PRIORITY_AUDIT.md',T/'SOURCE_AUDIT.md')
status=read(O/'status.json');status.update({'UTC':stamp,'status':'claimed_solved','current_review':'ROOT literal theorem/source/math gate passed; bounded credited publication-scope priority audit complete','current_publication':publication,'original_prior_review_fields':'Other author-model/counter fields originate in the original submission, preserved as historical data; current catalogue reproduced separately.','independent_review':'Fresh full package review01 required a documentation fix, applied globally in v2; review02 '+('clean, actualRootgateaccepted' if final else 'pending'),'novelty_claim':False,'human_peer_review':False})
save(T/'status.json',status)
save(T/'gate.json',{'UTC':stamp,'original_gate':'historical_original/gate.json','current_math_gate':'ROOT_MATH_GATE.json in repositoryauditpr179','mathematical_clearance':True,'bounded_priority_claim_scope_supported':True,'historical_firstness_certified':False,'publication':publication,'workflow_complete':False,'original_head':ORIGINAL})
problem=read(O/'problem.json');problem.update({'current_audit_UTC':stamp,'original_dataset_snapshot':'historical_original/problem.json','research_classification':'VERIFIED_LITERAL_FORMULATION_NO_COVER','research_summary':'No local exact root section at zero, hence no admissible open cover of allR6 at anycardinality. Classical obstruction credited; no firstness/newmethod, unprinted repaired finitegenus or approximate2B claim.','status':'claimed_solved_for_literal_printed_statement'});save(T/'problem.json',problem)
save(T/'upstream_report.json',{'UTC':stamp,'original_upstream_triage':'historical_original/upstream_report.json','current_result':'Literal no-cover theorem; original finite-number triage not adopted','priority_scope':'Bounded credited formulationnote, nohistoricalfirstnesscertificate'})
save(T/'source_manifest.json',{'UTC':stamp,'source_manifest_original':'historical_original/source_manifest.json','source_final_SHA256':'5d5e81d87118ba8d06685e49dd6619af204956631b1abeb2edd7dfd2d53d3042','source_v1_SHA256':'44b1666fbdef55dfd2a58648008dc0199e7fbfaf676adab50c7dd935c61c9c5b','actual_read_limits':'RepositoryRootprimaryledger plus complete sourcefamilies; bounded priorityaudit inexact_verification/PRIORITY_AUDIT.md. No thirdpartybody distributed.','current_priority_scope_supported':True,'historical_firstness_or_guaranteed_novelty_certified':False})
(T/'RESEARCH_LOG.md').write_text('# PR179 accepted-record preparation\n\n'+stamp+' — '+('95%' if final else '70%')+'workflow checkpoint. Original20nativefilespreserved inhistorical_original. Current sampledscientificguards corrected; frozenproof unchanged. Exactv2verification packagecopied byteforbyte. '+('Actualpreprint/trackeraccepted, MAINintegrationpending.' if final else 'Freshsecondreview/publication/dispositionpending.')+' No new central proofsearchroute, originaleffort1/5unchanged. AIassisted/unrefereed, nofirstnesscertificate.\n')
(T/'turns.jsonl').write_text(json.dumps({'UTC':stamp,'original_turns':'historical_original/turns.jsonl','workflow_percent':95 if final else 70,'original_substantive_routes':1,'publication':publication})+'\n')
(T/'review/REVIEW.md').write_text('# Current review record\n\nOriginal report in ../historical_original/review/REVIEW.md. The mathematical/source theorem was independently re-audited through three distinct families and Root symbolic/topological checks. Original scripts lost scientific assertion guards under optimization; current sampled copies replace those guards by explicit exceptions and retain finite-sampling limitations. The universal supported-polynomial certificate under ../exact_verification is supplementary to the written no-section proof.\n\nFresh package review01 found only a Pythonminimum documentation defect; corrected globally in v2. Secondnewwholepackagereview '+('clean and authenticated by Root.' if final else 'pending.')+' No certification of worldwide priority. PUBLICATION.json and SOURCE_AUDIT.md govern current scope/publicationfacts; old report timestamps/counters are not relabelled.\n')
summary=read(O/'review/review_summary.json');summary.update({'UTC':stamp,'historical_report':'historical_original/review/review_summary.json','original_counts_are_historical':True,'current_corrected_sampled_code_sha256':sha(T/'review/independent_checks.py'),'current_publication':publication,'mandatory_corrections_current':['Scientific assertguards replaced explicitexceptions','VerificationminimumPython3.11+','Current source/priority/publicationclaimcalibration'], 'current_whole_package_review02':'clean' if final else 'pending','verdict':'COMPLETE_LITERAL_THEOREM_VALID_CURRENT_PACKAGE_REVIEW_PENDING' if not final else 'COMPLETE_LITERAL_THEOREM_VALID_CLEAN_PACKAGE_PUBLISHED_TRACKED','file_sha256':{n:sha(T/'review'/n) for n in ['REVIEW.md','author_replay/NO_COVER.md','author_replay/verification.json','author_replay/verify.py','author_replay_stdout.json','independent_checks.py','independent_results.json']}});save(T/'review/review_summary.json',summary)
save(T/'frozen_artifacts.json',{'NO_COVER.md':sha(T/'NO_COVER.md'),'verify.py':sha(T/'verify.py'),'verification.json':sha(T/'verification.json'),'no_open_root_cover.tex':sha(T/'no_open_root_cover.tex')})
for p in T.rglob('*'):
 if p.is_file():p.chmod(0o444)
allfiles={p.relative_to(T).as_posix():pin(p) for p in sorted(T.rglob('*')) if p.is_file()}
save(D/'CURRENT_TEMPLATE.json',{'UTC':stamp,'current_template':stage,'files':allfiles,'original_native_files':20,'historical_native_files':20,'publication':publication,'source_and_exact_verification_byteidentical_to_reviewedpackage':True,'current_proof_byteidentical_to_original':True,'native_location_new_scientific_replay_claimed':False,'MAIN_updated':False})
print(json.dumps({'status':'EXPLICIT_NATIVE_TEMPLATE_PREPARED_NO_REMOTE_MUTATION','template':stage,'files':len(allfiles),'publication':publication}))
