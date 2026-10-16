"""Prepare a reviewable qualified historical credit correction; no provider writes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

D=Path(__file__).resolve().parent
S=D/'submitted/unsolved_math_prioritization/attempts/30002291'
C=D/'corrected_packet'
C.mkdir(exist_ok=False)
t=datetime.now(timezone.utc).isoformat()
intake=json.loads((D/'INTAKE.json').read_text())
assert json.loads((D/'ROOT_FULL_PRIORITY_PACKET_VALIDATION.json').read_text())['status']=='PASS_FIVE_COMPLETED_PRIORITY_PACKETS'
for row in intake['original_source_files']:
    rel=row['native_path'].split('attempts/30002291/',1)[1]
    raw=(S/rel).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    target=C/'original_submission'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)

old=(S/'PROOF.md').read_text()
core=old.split('## 2. Driver and kernel assumptions',1)[1].split('## 8. Disposition and limitations',1)[0]
header='''# Quadratic variation limits under bounded pure-jump characteristics

30002291 / OWR-12337-002. **Mathematics verified. Qualified historical
classification: already_solved, because the original open-ended request
already had a substantial sufficient-conditions answer.** Author turn1/5.
This does **not** assert that the exact arbitrary-predictable-kernel theorem
below was proved earlier. Its exact novelty remains unresolved.

No certified new solution of a previously unanswered original target is
claimed. See [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md) for the precise historical
meaning, nonnested classes, mesh qualification and unresolved extension
priority. All17 original files and historical reviews/manifests are preserved
byte for byte under original_submission/. Mathematical Sections2–7 below
are unchanged. The current introduction and disposition supply updated credit.

AI tools were used extensively in solving, checking and auditing. This work
is unrefereed; AI adversarial reviews are not human peer review. This credited
packet is not a preprint and has no Zenodo deposit or tracker entry.

## 1. Known results and exact scope

The original OWR2013 contribution asks for an analogous limit for a rather
general pure-jump semimartingale under sufficient conditions; it defines no
maximal class. A broad adapted scalar-volatility answer is already in
Basse-O'Connor–Heinrich–Podolskij, arXiv1604.02307v2 (14October2016),
Theorem1.2(i), associated with Bernoulli24(4A) (2018),3117–3146,
DOI10.3150/17-BEJ956. At p=2,k=1 the jump coefficients agree exactly,
and reflection of independent uniforms reindexes its phase weight into
W_alpha. The prior result has a functionalM1 statement at its printed1/n
mesh; do not silently attribute an arbitrary-mesh theorem to that statement.

The2015 preprint associated with the2017 AOP paper10.1214/16-AOP1170
supplies the Levy antecedent. A2014 survey already announced that Levy
phase law. The2018 primary general-function preprint arXiv1806.10352,
associated with EJP24 (2019), article79, DOI10.1214/19-EJP336,
Theorem2.1(i) and Proposition2.3(i), formally covers nonsymmetric Levy
drivers below index2. These originals and the established truncation method
must be credited. Exact final-publisher PDF comparison was unavailable;
dated complete primary preprints control the theorem comparisons here.

The verified theorem below permits arbitrary predictable jump kernels and
some finite-quadratic-rate index2 drivers. Those are real distinctions from
the inspected predecessor hypotheses, but do not certify novelty. Its global
moment assumptions also exclude some earlier heavy-tail examples, so the
classes are nonnested. The original question's breadth is qualitative; the
historical catalog judgment concerns a prior substantive affirmative answer,
not proof of complete containment of the present class in an old theorem.

## 2. Driver and kernel assumptions'''
end='''## 8. Disposition and limitations

The theorem under its explicit hypotheses passes independent mathematical
reconstruction, three fresh adversarial mathematical families and source-scope
review. The finite controls supplement the analytic proof. Its sufficient
conditions are not necessary or maximal, and no functional topology is
proved here. The restrictions and deterministic-time counterexample in the
preceding sections remain essential.

For the original open-ended request, a substantial earlier semimartingale
sufficient answer exists. The current catalog status already_solved has
that qualified historical meaning. It does not mean that the exact theorem
above is known, nor that every possible generalization of the original
question is settled. Independent priority searches did not establish either
full anticipation or novelty of this exact bounded-rate class. The remaining
question is a separately scoped extension-priority investigation.

Under the active claimed_solved-only publication workflow, skip this
corrected open draft. No new paper, DOI, deposit, tracker row, merge, closure
or PR comment accompanies this credit correction. The broader goal remains
active and incomplete. The original proof and older verdicts remain in the
immutable original_submission archive; current manifests bind this packet.
'''
(C/'PROOF.md').write_text(header+core+end)
audit='''# Priority audit and precise credited disposition

The classification **already_solved** means that the original open-ended
sufficient-conditions request already had a substantial affirmative answer.
It does **not** mean that an earlier theorem covers the entire exact candidate.
Novelty of the bounded-rate arbitrary-predictable-kernel theorem remains
unresolved. This distinction is required wherever the status is displayed.

## Positive earlier answer and direct mathematical bridge

The complete OWR09/2013 contribution, printed491–493, was independently read.
It asks for a similar limit for a rather general pure-jump semimartingale
under sufficient conditions and fixes no maximal class. This does not demand
a universal result for every semimartingale. The word general is qualitative;
the historical classification is a documented judgment about a substantial
prior answer, not an assertion of a source-defined maximal theorem.

The complete arXiv1604.02307v2 model(1.2), assumptions(A),(B1),
Theorem1.2(i), Remark1.4 and the relevant proof§4.1 were read directly.
That original allows dY=sigma_-dL with L symmetric pure-jump Levy relative
to the filtration and sigma adapted cadlag, without independence. Taking
p=2,k=1 gives exactly the rough range alpha<1/2. The jump atT is
J_T=sigma_(T-)Delta L_T. With h(x)=x_+^alpha-(x-1)_+^alpha,

`sum_(l>=0) h(l+U)^2 = W_alpha(1-U)`.

Reflection preserves independent uniforms and full-original-field independence.
The g0 subtraction is constant in observation time and cancels in increments.
The prior functionalM1 limit gives joint deterministic fixed-time convergence,
since no fixed time carries a driver jump. Its statement uses mesh1/n;
arbitrary deterministic meshes are a literal statement difference. Rounding
frequencies does not give pathwise closeness of phase weights. The established
density/Fourier proof mechanism extends naturally, but this audit does not
retroactively attribute the candidate's exact quantifier to the old theorem.

The prior class is substantial: for g=x_+^alpha exp(-x), take symmetric
tempered stable noise of index1 and bounded adapted cadlag volatility. Its
quadratic rate is finite, and exponential tails give(A),(B1). Such volatility
may depend on the past. For an explicit legal example use sigma_s=2 for s<0,
sigma_s=2+sin(L_s) for s>=0; L0=0 makes it cadlag at0. Do not assume
negative-time Levy levels themselves are adapted. These drivers include
genuine non-Levy infinite-activity semimartingales. The source request cannot
responsibly be promoted as having had no semimartingale sufficient answer.

## Additional prior overlap and chronology

- Podolskij's arXiv1405.1531v1, public7May2014, Theorem4.8(i), announces
  the Levy phase limit and cites a2014 working paper. It is an announcement
  anchor, not a substitute for a retrieved full proof.
- Basse-O'Connor–Lachieze-Rey–Podolskij arXiv1506.06679v1, public
  22June2015, Theorem1.1(i), provides the full Levy proof; associated AOP
  publication is45(6B),4477–4528 (2017), DOI10.1214/16-AOP1170.
- Basse-O'Connor–Heinrich–Podolskij arXiv1604.02307v1, public8April2016,
  already includes the scalar-volatility result but assertsJ1. The14October2016
  v2 corrects the functional statement toM1 and rejectsJ1/J2. Usev2 for
  the corrected functional claim. Associated publication is Bernoulli24(4A),
  3117–3146 (2018), DOI10.3150/17-BEJ956. Conflicting institutional
  pagination is not used.
- Their arXiv1806.10352v1, public27June2018, Theorem2.1(i) and
  Proposition2.3(i), allows nonsymmetric Levy drivers. For statisticF(x)=x²
  choose the auxiliary smoothness exponent r strictly between
  max(beta,1/(1-alpha)) and2. Then floor(r)=1 andF(0)=F'(0)=0;
  the theorem and itsM1 sign condition apply. Do not confuse r with the
  quadratic statistic's power. Associated EJP24 (2019), article79,
  DOI10.1214/19-EJP336. Nonsymmetry alone is therefore not new.

Primary arXiv histories, not regenerated TeX title dates, control these
preprint dates. Full primary preprints were acquired and read; blocked final
publisher-PDF retrievals are not counted as successful inspections.

## Exact class differences and unresolved priority

The symmetric measure with density
`1_(0<|z|<exp(-1)) |z|^-3 log^-2(1/|z|)` has quadratic rate2.
Substitution v=log(1/|z|) makes each r-moment with r<2 equal to
`2 int_1^infinity exp((2-r)v)/v² dv=infinity`. Its BG index is2.
It is excluded by the inspected strict-beta-below2 theorems and included
by the current isometry proof. A deterministic compensator changing from
delta1 to delta1+delta2 has bounded quadratic rate but cannot be a scalar
pushforward of one fixed measure in the same ambient filtration: nonzero
scaling preserves total jump intensity, whereas the displayed intensity changes.
Conversely, symmetric stable heavy-tail drivers in prior classes can have
infinite large-jump second moment and violate the current global rate bound.
The classes are therefore nonnested. These witnesses are noncontainment
proofs, not literature-wide novelty proofs.

General Poisson embeddings allow predictable mark-dependent amplitudes, but
do not turn them into a single scalar volatility. Ordinary quadratic variation
of a driver or weak-Dirichlet convolution does not determine this nonzero
rescaled statistic. Applying an unspecified lifting theorem, conditioning on
the full random coefficients, or changing physical clocks leaves a real proof
obligation. The existing truncation mechanism and elementary smooth-kernel
perturbations also must not be marketed as a new limit mechanism.

Five independent priority lanes examined classical statements/proofs, general
Volterra/martingale convolutions, the index2 and shape boundaries, historical
citation descendants, and novelty-saving/original-target interpretations.
They establish extensive prior overlap and a prior substantial sufficient
answer, but neither full anticipation nor exact-candidate novelty. Bounded
search nonfinding is not proof of absence. These originals remain unclosed
for the extension-priority question:

- Liu–Zhang2011, DOI10.1016/j.spl.2011.01.016.
- Liu–Zhang–Fang2017, DOI10.1080/03610926.2016.1217019.
- Liu–Tang–Zhang2014, DOI10.1007/s11425-013-4736-4.
- Ambit Stochastics2018 chapter3, DOI10.1007/978-3-319-94129-5_3.

Only metadata/abstracts were available for these leads; no theorem-level
anticipation or exclusion follows. Exact final-publisher version comparison
for the main preprints also remains incomplete. No outside input was requested
and no outreach was prepared. Full external reading copies stay private.

## Consequence for this workflow

Mathematics PASS under exact written hypotheses; author turn1/5 preserved.
Keep the verified theorem and every original artifact. Record the qualified
historical prior-answer finding and unresolved extension novelty. Under the
user's claimed_solved-only scope, skip the corrected open draft. There is no
new preprint, deposit, tracker row, merge, closure or PR comment. This is not
a negative mathematical verdict or an assertion that the exact extension is
unpublishable under a separately authorized, properly motivated program.
'''
(C/'PRIORITY_AUDIT.md').write_text(audit)
(C/'README.md').write_text('''# 30002291 / OWR-12337-002

**Mathematics PASS. Qualified historical already_solved:** the original
open-ended request already had a substantial sufficient-conditions answer.
This does not assert that the exact current theorem was previously proved;
its extension novelty remains unresolved. Author turn1/5.

[PROOF.md](PROOF.md) retains mathematical Sections2–7 unchanged.
[PRIORITY_AUDIT.md](PRIORITY_AUDIT.md) explains the scope and unresolved
leads. All17 original files, checks and historical manifests/reviews are in
original_submission/, byte for byte. Current manifests bind this packet.

Skip the corrected open draft under the active claimed_solved-only workflow.
No preprint, DOI, deposit, tracker row, merge, closure or PR comment.
AI tools were used extensively; unrefereed, without human peer review.
''')
(C/'SOURCE_SCOPE.md').write_text('''# Original target and present scope

The complete official OWR2013 contribution, printed491–493, asks for
sufficient conditions for a rather general pure-jump semimartingale limit.
It specifies no maximal characteristic class. The bounded-rate theorem in
PROOF.md is a mathematically valid, nonvacuous sufficient theorem.

A substantial earlier semimartingale sufficient answer exists in
arXiv1604.02307v2 Theorem1.2(i). Therefore catalog status already_solved
has a qualified historical meaning; it does not assert full earlier coverage
of the current arbitrary-predictable-kernel/index2 theorem. Exact extension
novelty is unresolved. See PRIORITY_AUDIT.md for the reciprocal-mesh
qualification, nonnested classes and complete source-access limits.

The source's contextual nonsemimartingale remark is not universal:
controlled finite-activity moving averages can be absolutely continuous.
The deterministic-time counterexample tests a universal claim outside the
source's sufficient-conditions request. No maximal-class or functional
convergence claim is made. Whole source texts remain private.
''')
(C/'KNOWN_RESULTS.md').write_text('''# Current priority status

Qualified historical already_solved: the original sufficient-conditions
request already had a substantial answer. The exact bounded-rate theorem
is mathematically verified, with novelty unresolved. These are distinct claims.

PRIORITY_AUDIT.md supplies the complete bridges and source limits for:

- The2014 Levy-phase announcement and2015 full Levy proof.
- The2016v2/2018 adapted scalar-volatility semimartingale theorem.
- The2018/2019 formal nonsymmetric Levy general-function theorem.

Neither noncontainment in these classes nor a failed search proves novelty.
The index2 and changing-kernel witnesses establish real class differences;
the classes are nonnested. General embeddings and ordinary variation
theorems do not automatically supply the required rescaled stable law.

All previous literature notes and older review verdicts remain unchanged in
original_submission/. Do not use their historical manifests to certify the
current contextual edits. No new first-solution claim or preprint is made.
''')
(C/'DISPOSITION.md').write_text('''# Qualified historical disposition

Status already_solved means a prior substantial sufficient-conditions answer
to the original open-ended request. It does not mean the entire exact candidate
was previously proved. Mathematics PASS; exact extension novelty unresolved.

Preserve author turn1/5, original17-file archive and verified proof. Skip the
corrected open draft under the current goal. No new paper, upload, tracker row,
merge, closure or PR comment. AI audits are not human peer review.
''')
(C/'PUBLICATION_STATUS.md').write_text('''# Publication status

Qualified historical already_solved; mathematical theorem verified; exact
extension novelty unresolved. No preprint clearance, manuscript, DOI, Zenodo
record or tracker entry. The corrected draft remains open and is skipped under
the active claimed_solved-only goal. No human peer review is claimed.
''')
(C/'VERIFICATION.md').write_text('''# Verification and historical inputs

Mathematical Sections2–7 are unchanged from the independently verified proof.
The17-file original submission, old reviews and manifests are byte-identical
under original_submission/. Those historical manifests bind that archive,
not the current contextual introduction and disposition. Current FROZEN and
PUBLICATION manifests bind the current packet separately.

The original SymPy controls reproduce2571+227=2798 finite assertions with
byte-identical output. Their unchanged scripts are in original_submission/
checks/verify_exact.py and original_submission/independent_review/
independent_checks.py. They require SymPy; the root audit records the actual
runtime. Three fresh analytic mathematical adversaries and a source-scope
adversary pass. Fresh supplements include2448 exact geometry cases, five
kernel controls and17 phase controls; these do not replace the analytic proof.
Five priority families and root exact scope replays are in the dedicated
campaign audit folder on main. Finite floating-point series comparisons are
diagnostics, not interval certificates or novelty evidence.
''')
turn=json.loads((S/'TURN_STATE.json').read_text())
turn.update(status='already_solved: qualified historical prior sufficient-answer finding',
            outcome='verified theorem; exact extension novelty unresolved; scope skip',
            mathematical_audit='PASS',historical_prior_answer=True,
            entire_exact_candidate_previously_proved_established=False,
            exact_extension_novelty='unresolved',native_application_record='See campaign classification receipt',
            estimated_completion_percent=None)
(C/'TURN_STATE.json').write_text(json.dumps(turn,indent=2)+'\n')
(C/'metadata.json').write_text(json.dumps(dict(problem_id=30002291,code='OWR-12337-002',status='already_solved',
    classification_meaning='Qualified historical prior sufficient answer to original open-ended request; not full candidate anticipation',
    mathematical_audit='PASS',exact_extension_priority='unresolved',author_turns=1,
    entire_exact_candidate_anticipation_established=False,novelty_certified=False,preprint_clearance=False,
    AI_tools_used_extensively=True,human_peer_review=False,DOI=None,Zenodo_record=None,
    author='Alec Kriebel',ORCID='https://orcid.org/0009-0001-9320-500X',original_head=intake['head']),indent=2)+'\n')
sources=json.loads((S/'source_manifest.json').read_text())
sources.update(original_three_source_pins_preserved=True,accessed_UTC_date='2026-10-15',
               source_identity_caution='lma2017 filename denotes2015 arXiv preprint, not a verified final publisher PDF',
               classification='qualified historical prior answer; exact extension novelty unresolved')
for name,url in [('bhp2018_functionals.pdf','https://arxiv.org/pdf/1806.10352'),('podolskij2014_survey.pdf','https://arxiv.org/pdf/1405.1531v1')]:
    q=D/'root_priority_01/private_reading'/name
    sources['sources'].append(dict(reading_filename=name,url=url,bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
(C/'source_manifest.json').write_text(json.dumps(sources,indent=2)+'\n')
(C/'RESEARCH_LOG.md').write_text('# Current credited packet log\n\n'+t+' — Local proposal prepared at65% of eligible-intake disposition. Mathematics PASS, exact extension novelty unresolved. Prior substantive sufficient answer to historical target authenticated. All17 originals archived and mathematical Sections2–7 retained byte for byte. No native status change yet; final independent synthesis/packet review and guarded application/readback remain. No paper/deposit/tracker/merge.\n')

def pin(q):
    raw=q.read_bytes();return dict(path=q.relative_to(C).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

assert (C/'PROOF.md').read_text().split('## 2. Driver and kernel assumptions',1)[1].split('## 8. Disposition and limitations',1)[0]==core
for name in ['FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json']:
    files=[pin(q) for q in sorted(C.rglob('*')) if q.is_file()]
    (C/name).write_text(json.dumps(dict(status='already_solved',classification_qualified_historical=True,
        exact_candidate_priority='unresolved',author_turns=1,utc=t,
        scope='Current credited audit packet including entire17-file original archive; self hash excluded',files=files),indent=2)+'\n')
files=[pin(q) for q in sorted(C.rglob('*')) if q.is_file()]
out=dict(utc=t,PR=234,original_head=intake['head'],native_changes_performed=False,
         proposed_classification='already_solved: qualified historical prior answer, not full exact candidate anticipation',
         exact_extension_priority='unresolved',original_archive_files=17,unchanged_mathematical_sections='2–7',
         core_sha256=hashlib.sha256(core.encode()).hexdigest(),files=files,final_independent_packet_review_pending=True)
(D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='files'},indent=2))
