from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, stat
A=Path(__file__).resolve().parents[1]
O=A/'original_submission/files/unsolved_math_prioritization/attempts/30002720'
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(p.stat().st_mode),'04o'))
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
utc=datetime.now(timezone.utc).isoformat()
auth=A/'root_math/MATH_FAMILY_MANIFEST_AUTHENTICATION.json'
j=json.loads(auth.read_text())
require(j['status']=='ALL_THREE_MATH_FAMILY_EXACT_MANIFESTS_AUTHENTICATED','family artifacts')
require(pin(O/'COUNTEREXAMPLE.md')['sha256']=='c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c','original proof')
candidate=A/'repaired_candidate_v1';candidate.mkdir(exist_ok=True)
shutil.copyfile(O/'COUNTEREXAMPLE.md',candidate/'COUNTEREXAMPLE.md')
shutil.copyfile(A/'root_reproduction/verify_raised.py',candidate/'verify.py')
require((candidate/'COUNTEREXAMPLE.md').read_bytes()==(O/'COUNTEREXAMPLE.md').read_bytes(),'proof preserved')
require((candidate/'verify.py').read_bytes()==(A/'root_reproduction/verify_raised.py').read_bytes(),'repair preserved')
(candidate/'REPAIR_NOTE.md').write_text("""# Supporting-verifier repair
The mathematical proof is preserved byte for byte from original head efc3f35a72543ad9ae76fd31a860116f1ffd4a32. The only checker repair replaces its check helper's Python assertion with an explicit RuntimeError. Ordinary and optimized execution of this exact repaired code pass 16,642 finite controls; three deliberate semantic mutations fail in both modes (six negative executions). Original optimized assertions let all three false variants pass.
The exact executions and mutations are preserved in ../root_reproduction/REPRODUCTION_AND_NEGATIVE_CONTROLS.json. Finite diagnostics supplement, and do not prove, the universal theorem. File relocation does not change its arithmetic or stopping algorithm; its receipt paths resolve relative to the checker.
""")
reports=[]
for fam in ['cylinder_geometry_adversary','literal_source_scope_adversary','probabilistic_asymptotics_adversary']:
    r=json.loads((A/fam/'RESULT.json').read_text())
    expected={'cylinder_geometry_adversary':'independently_verified_with_stated_scope','literal_source_scope_adversary':'PASS_EXACT_MATHEMATICAL_CLAIM_WITH_SOURCE_SCOPE_QUALIFICATIONS','probabilistic_asymptotics_adversary':'PASS'}
    require(r.get('verdict')==expected[fam],'family not passing: '+fam)
    reports.append(dict(family=fam,review=pin(A/fam/'REVIEW.md'),result=pin(A/fam/'RESULT.json'),
                        derivation=pin(A/fam/('INDEPENDENT_DERIVATION.md' if fam=='cylinder_geometry_adversary' else 'DERIVATION.md')),
                        root_read_entire_review_result_and_derivation=True))
gate=dict(
 UTC=utc,status='ROOT_MATH_GATE_PASS_EXACT_NONBOUNDARY_THEOREM_WITH_SOURCE_SCOPE_QUALIFICATION',
 pr=166,problem_id=30002720,original_head='efc3f35a72543ad9ae76fd31a860116f1ffd4a32',
 original_QUEUE_status='claimed_solved',original_effort='1/5',
 mathematical_clearance=True,mathematical_completion_percent=100,
 exact_verified_claim='For independent stationary binary Markov strings with initial probabilities (1/2,1/2) and transitions ((3/4,1/4),(1/4,3/4)), the fixed rank t=F(v), with ones at square positions j^2 for j>=2, is nonboundary and a continuity point of the first-order profile. At rank floor(nt)+1 the singleton-stopping cost, divided by sqrt(n), is non-tight under every deterministic real centering sequence.',
 proof=pin(O/'COUNTEREXAMPLE.md'),repaired_candidate_proof=pin(candidate/'COUNTEREXAMPLE.md'),
 repaired_checker=pin(candidate/'verify.py'),repair_note=pin(candidate/'REPAIR_NOTE.md'),
 independent_family_reports=reports,family_manifest_authentication=pin(auth),
 root_independent_reconstruction=pin(A/'ROOT_PRELIMINARY_MATH_ANALYSIS.md'),
 root_reproduction_receipt=pin(A/'root_reproduction/REPRODUCTION_AND_NEGATIVE_CONTROLS.json'),
 independent_scope=dict(geometry='All-index probability-cylinder geometry, nonboundary continuity and exact singleton cost; 8,191 cylinder controls, 49 square indices, 9,216 operational cases, six detected false mutations.',
                        probability='Uniform empirical-CDF and height estimates, triangular binomial CLT, same-data event dependence, arbitrary-center tightness quantifiers; all-j>=80 explicit relative error envelope; 12,235 explicit controls in each mode and seven negative mutations.',
                        literal_sources='Independently acquired OWR contribution and 2014/process manuscripts; exact source model and mathematically stated marginal distinction.'),
 remaining_mathematical_gaps=[],
 source_resolution_qualification=dict(
  literal_universal_fixed_rank_negative_already_known=True,
  primary_evidence='Leckey-Neininger-Sulzbach process manuscript Proposition 2.9 gives existing boundary fixed-marginal non-tightness.',
  additional_candidate_theorem='Explicit nonboundary continuity-rank failure under every deterministic center.',
  nonboundary_restriction_explicitly_printed_in_open_question=False,
  restriction_motivation='The 2014 first-order expected-cost theorem excludes cylinder endpoints; this does not insert an unprinted restriction into the open marginal question.',
  publication_wording='Describe a nonboundary refinement and credit the earlier boundary obstruction; do not claim this is the first universal fixed-rank negative result.',
  publisher_version_full_text_checked=False),
 limitations=['No classification of all ranks or almost-everywhere behavior','No theorem about data-dependent centering','No priority or novelty clearance yet','No exact final publisher wording recovered'],
 priority_clearance=False,publication_clearance=False,MAIN_writer_authority=False,
 completion_estimates=dict(case_percent=33,fully_completed_programme=32,dated_denominator=99,published=18),
 no_remote_or_publication_mutation=True)
target=A/'ROOT_MATH_GATE.json';target.write_text(json.dumps(gate,indent=2)+'\n')
status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
status.update(UTC=utc,status=gate['status'],case_percent=33,mathematical_clearance=True,mathematical_percent=100,
 priority_started=False,priority_clearance=False,publication_clearance=False,math_gate=pin(target),MAIN_writer_authority=False)
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n## '+utc+' — mathematical gate complete; case 33%, programme 32/99, 18 published\n\nROOT read all three independent complete reviews, machine results and universal derivations. All 79 retained artifacts and 16 external input identities authenticate against the externally supplied manifests, with immutable first seals and explicit private-source exclusion. Exact nonboundary/every-deterministic-center theorem passes. Verifier optimization robustness repaired; mathematical proof unchanged. Source qualification retained: boundary universal failure was already known, and no nonboundary restriction is printed in the open-question sentence. Priority and original-target openness are the next research stage. No MAIN writer authority or publication action.\n')
print(json.dumps(dict(gate=pin(target),status=gate['status'],case_percent=33,mathematical_percent=100),indent=2))
