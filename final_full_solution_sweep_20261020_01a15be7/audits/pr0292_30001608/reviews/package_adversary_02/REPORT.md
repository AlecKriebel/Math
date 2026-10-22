# Full publication-package adversarial review 02

**Verdict: PASS for the candidate's exact, bounded scope. No mandatory repair and
no surviving material objection were identified.** The complete all-state proof
establishes positive recurrence for each fixed real lambda > 0 for the displayed
six-rate chain. The source identity, reproducibility, presentation, metadata and
qualified historical-conjecture contribution survive this review. This is an
independent AI falsification attempt, not formal independent human peer review,
publication authority, or a worldwide-firstness certificate.

The final reviewed identities are:

| Candidate | SHA-256 |
|---|---|
| dfc_stability_verification.zip | 38664f12e8d2e74fa46b3f11363a071ec100aad62ece713b578293a6593d9a0e |
| standalone dfc_stability.pdf | bee5abffcfdb1ce8bc50f706480c81c4a80e8d609bec2a9d99c6aa4e9b805036 |
| zenodo-deposit.json | 262bf696ced2ccbf5c26fd59333af616a6d832260dc6d1bc91b08d1f213a04b7 |
| extracted main.tex | 9949c92633f1654cceadfc40f6988e3e2363db4ed229face05eb2d1b681a7611 |

`FINAL_SEAL.json` binds these actual files and this review's evidence. The
candidate was neither modified nor repackaged. No Git, PR, spreadsheet, Zenodo,
or other external state was changed, and no individual was contacted.

## Independence and success criterion

I matched the three supplied seals, extracted the ZIP into this review folder,
read the complete six-page main.tex, and independently reconstructed its
mathematics. `INDEPENDENT_INITIAL_DERIVATION.md` and checkpoint 2 were written
before reading supporting mathematical verdicts/checkers. The earlier full
package reviewer's report/verdict was never read. Existing bundled reviews and
controls were inspected only after that independent derivation; their later
reproduction is labeled reuse, not a new proof.

The target is the CTMC on nonnegative integer (a,b,x,y), with D=x+y+1, arrivals
lambda/2 into each empty committed class, transfers a(x+1)/D and b(y+1)/D into
their singleton classes, and departures x(y+1)/D and y(x+1)/D. The seed is
permanent; empties are invisible to the denominator; completed peers leave
immediately. The claim is nonexplosion, irreducibility, and finite-mean
regeneration in this physical time, for each fixed real lambda > 0.

A failure of any all-state drift implication, uncovered interface, invalid
localization, clock substitution, original-model mismatch, authenticated prior
exact all-load theorem, reproducibility failure, materially misleading metadata,
or unsupported priority rhetoric would have required a repair or adverse
verdict. Finite samples alone were never accepted as proof of recurrence.

## Analytic attacks and disposition

**Generator and rounding.** Direct application of the six events gives
`L W=2lambda-u-d`, `L Z=(y-x)/D`, and Z quadratic variation rate `lambda+d`.
The rounded absolute value's derivative is clipped z/m and globally
1/m-Lipschitz. Integrating this bound proves the displayed quadratic remainder
across either join, including noninteger m. Since m=4c, the second-order term is
exactly `(lambda+d)/8`, producing beta=17lambda/8 and q=7/8. No lost factor or
sign change was found. If Z>=m and x>=3(y+1), then `(x-y)/D>=1/2`, giving the
needed `-c/2`; the proof establishes Z's sign before using that estimate.

**Finite corrector, especially the terminal state.** Detailed balance gives
weights gamma^k. The finite geometric means strictly increase to theta+1, so a
finite integer R meeting both strict requirements exists at every fixed real
lambda. The prefix mean is below the full mean, making every t_k negative.
Telescoping proves the finite Poisson equation, with terminal equation
`R g(R-1)=R-mu`. The normalization g(R)=0 and zero extension imply
g(R+1)=0, so a departure from R+1 does not create an omitted correction.
For the actual chain, increasing its birth rate multiplies a nonpositive
increment, while reducing its death rate multiplies a nonnegative increment;
both replacements give the stated upper bound. At R, the upward increment is
zero. This is a pointwise generator comparison using an explicitly solved finite
auxiliary equation, not stationary averaging in the DFC chain.

**Post-jump product rule and unbounded waiting rooms.** The exact identity is
`Delta(fg)=f_pre Delta g+g_post Delta f`. On either first download D increases
and neither waiting numerator increases. Thus both cutoff increments and each
whole correction product are nonpositive, irrespective of a and b. The large
first-download rates therefore do not generate a hidden positive interface
cost. At arrivals, the summed bound is lambda ell G/D. At departures D>=2;
outside saturation, `w<eta D` gives `Delta f<=ell w/[D(D-1)]<=2ell/D`.
Two correction terms yield the stated `4d ell G/D`. At D=1 no departure is
possible. The independent coarse bound `LJ<=G(lambda+2d)` is also valid.
My mutation control confirms that replacing g_post by g_pre is false and can
underestimate the increment; the candidate uses the correct identity.

**All regions, ramp, corners and integer thresholds.** If both singleton counts
are at least R+1, every current and successor correction vanishes, including a
departure to R. The elementary identity `D(d-y)=y(x-y)+x` when x>=y gives
d>=min(x,y), and the selected R forces drift below -2. In the corner y<=R,
x>=N, the opposite corrector and successors vanish. The stated inequalities
d<=2R+1, `(x-y)/D>=1/2`, and qd>=y hold. The N choice makes the interface
remainder at most one. A saturated cutoff gives drift at most
`beta+c-mu+1<-3`; an unsaturated cutoff, including the entire ramp, forces
Z>=m and gives `beta-c/2+1-u=-3-u`. The symmetric corner is identical.
If neither of those cases applies, one singleton count is <=R and the other
is <N, so x+y<=N+R. The lower bound on u then controls arbitrary waiting
populations once a+b>B. R, R+1, N-1, N, gamma, eta, and a+b=B are consistently
assigned. A noninteger B causes no problem on the integer state space.
There is no circular dependence: R fixes g and G; these fix N and then B.

**Coercivity and all real loads.** The actual function is single and global:
`W<=V<=(1+c)W+cm/2+2G`, with V>=total population. Its sublevel sets are
finite and every jump has a finite uniform bound at the fixed load. All
parameters are finite for arbitrary real lambda>0. The analytic existence of
R, N and B is independent of rational test parameters. No inference from a
finite load grid, no uniformity as lambda grows, and no stationary moment claim
is used. Lambda=0 is correctly outside the irreducibility theorem.

**Nonexplosion and irreducibility.** Every internal event spends one unit of W;
an arrival contributes two. Thus the actual jump count is at most
W(0)+3P_lambda(t), even though internal rates are state-dependent. Prescribing
seed-supported downloads/departures gives a finite positive-rate path to zero;
prescribing arrivals and first downloads builds any finite target from zero.
These arguments cover zero coordinates and do not rely on simulation.

**Localization and finite-mean return, rather than embedded recurrence.** Stop
Dynkin's identity at the first hit of F, time t, and a finite population exit.
The localized state set and its one-step exit boundary are finite. Discarding
nonnegative terminal V gives the stopped-time bound before taking any limit.
Nonexplosion makes population exits tend to infinity; Fatou, then monotone
convergence in t, give E_s tau_F<=V(s). No unproved uniform integrability of
terminal V or invariant law is required. From finite F, a finite collection of
positive-probability paths to zero has a common finite horizon and success
probability bounded away from zero. The Poisson workload bound and the linear
upper bound on V uniformly bound the expected duration of a horizon trial
followed by return to F. Strong Markov repetition bounds the total expected
time by a geometric series. Together with the holding mean 1/lambda at zero
and the two finite-return exit neighbors, this is a finite-mean physical-time
regeneration cycle. The stationary occupation measure and uniqueness follow.

**Strongest verified mathematical result:** the displayed V satisfies
`L V<=-1` off the stated finite F and proves the full theorem. The exact
remaining mathematical gap identified by this review is **none**.

## Reproduction and deliberate false-green challenges

The clean wrapper completed successfully from the extraction. It checked all 91
manifested payloads (92 distributed files including the manifest) and reproduced
all four historical control rounds, the portable reviewer, fresh tridiagonal
controls, source/model controls, seeded finite-horizon diagnostic and protocol
controls. The deliberate false Common-Chunk=DFC identity was rejected.
`reproduction.stdout.json` records every completed stage; stderr is empty.

I read the programs and wrapper. The wrapper uses temporary child copies,
compares actual execution results with frozen outputs, rejects optimized Python,
and verifies the original extraction again afterward. Only the explicitly
labeled simulation floats receive a stated tolerance; exact controls are
compared exactly. The old absolute-path reviewer is preserved, while its
portable copy is exactly the one-path adaptation. Original historical status
files are identified as historical. The checks do not compare only a test to
its own expected constant and do not treat a count of assertions as a proof.

My new `independent_controls.py` imports no candidate code. It solves g and mu
simultaneously from every finite Poisson row plus g(R)=0 using generic Gaussian
elimination. At loads 1/19, 17/11 and 7/2 it checks 572 states each: 1,716
total, including 276 both-large states, 432 corners, and 54 bounded-visible
states beyond B. The region controls are explicitly nonvacuous. It checks the
post-jump identity, first-download signs, departure bound, both correction bounds,
rounding joins, actual full V drift, coercivity, the paper's exact linear upper
bound, terminal R equation and R+1 extension. Nine deliberate mutations are
detected: wrong pre-jump product factor, nonzero g(R) extension, and clock
normalization, at each load. These are supplementary exact finite controls.

`wrapper_controls.py` separately accepts a valid package and rejects source
tampering, an unlisted extra file, a missing file, a symlink, and Python -O.
`priority_controls.py` independently enumerates the three-sample protocol,
checks an older potential's failure on DFC, and verifies the reaction-network
realization obstruction. All completed successfully. Reproduction commands are
listed in `REPRODUCE_REVIEW.md`; generated receipts are inspectable JSON.

All 40 original files also match direct `git show` bytes, original Git blob IDs
and the snapshot SHA-256 records at head
`1198534928f4c2bf8bf758c9ceb16edaa3a496e8`. This check is independent of the
package's self-recorded manifest. Test counts in different generations overlap
and are not summed as independent proof evidence.

## Primary sources, priority and old theorem transfers

I read the official [OWR contribution](https://ems.press/content/serial-article-files/46306),
the relevant [2009 arXiv v1](https://arxiv.org/pdf/0910.5577v1) definitions,
diagram and contrary conjecture, and the retained [2011 author proof](https://hal.science/hal-00781341).
The 2011 diagram and invisible-room paragraph agree exactly with the candidate.
The 2009 opposite conjecture, 2010 stability conjecture, and 2011 Conjecture 3.6
are distinguished correctly. The final [Springer record](https://link.springer.com/article/10.1007/s11134-011-9209-2)
confirms the bibliography but exposes subscription preview; I did not inspect
its final body. Fresh HAL web access failed; the actual retained author-proof
PDF, its header, diagram and conjecture were read and rendered locally.

The complete five-page Allerton proceedings body was read in text and visually,
including all of its proof and conclusion. It samples three from the whole
population and protects rare-chunk departure. Common Chunk's singleton exit
rate is 7/8 where DFC's is 1/2; its sole-empty first-download rate is 3/8 where
DFC's is 1. Their ratios preclude direct clock identification. More strongly,
the actual Allerton high-load Foster function has DFC drift divided by M tending
to `1-exp(-1)>0` at lambda=1 and `(1,0,M,1)`, for every finite C. Its theorem
does not directly transfer. The conclusion's unresolved rare-chunk conjecture
is a different algorithm. The author bibliography independently corroborates
the proceedings identity. The archived PDF is not claimed byte-equal to a
live IEEE download. Details are in `PRIORITY_AND_TRANSFER_DERIVATIONS.md`.

I also checked the operative two-chunk proof and Common Chunk definitions in
Oguz's [Berkeley 2012 technical report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-6.html).
Its three-sample minority first-chunk rule is different. Its older two-chunk
potential, evaluated directly on DFC at `(M,0,M,0)`, has drift asymptotic to
`2M^2>0`. Later [Group Suppression](https://arxiv.org/pdf/1708.09087) and
[Mode Suppression](https://arxiv.org/pdf/1904.04191) model/theorem sections
also impose distinct suppression and finite seed-upload rules. Their inspected
theorems do not identify the DFC generator; this is not an exclusion of every
unread ancillary result.

One new general-theorem lead was supplied after the independent derivation:
the public [single-linkage bimolecular reaction-network paper](https://zenodo.org/records/22089551).
I independently retrieved the actual v1.2.4 paper and read its model definitions
and Theorem 2.1. Clearing DFC's denominator gives the forced channel
`A+X -> 2X`, with no possible nonnull outgoing `2X` channel: any such channel
would add a positive x(x-1) off-diagonal rate absent from DFC. Weak reversibility,
an essential theorem hypothesis, fails. Nonnegative alternative realizations on
these coordinates cannot cancel that forbidden rate. A state-clock transfer
would separately need an unbounded stationary integrability condition. No exact
all-load duplication by this public theorem was established.

The fresh bounded search included exact algorithm names, Conjecture 3.6,
source DOI/title, two-chunk positive recurrence, all-load protocols and old
Foster-function transfer routes. It authenticated no earlier exact all-load DFC
theorem. The elementary small-load deduction is credited in the candidate.
The final 2015 journal body remains uninspected: its
[institutional abstract](https://cris.vtt.fi/en/publications/stable-distributed-p2p-protocols-based-on-random-peer-sampling/)
and metadata describe a different sampling/incentive family but do not rule out
an ancillary DFC result. IEEE PDF routes and a later full-thesis lead did not
yield inspected bodies. Those limits remain explicit in `READING_LEDGER.json`.

The actual paper claims a bounded all-load extension of a stated historical
conjecture. It does not claim worldwide firstness, continuing openness through
2026, novelty of general Foster/Poisson tools, or the first small-load stable
example. Given that scope and the actual primary-body checks, the remaining
uninspected editions are acknowledged historical limits, not an unresolved
material objection to the candidate's stated contribution. They cannot be used
as evidence either of duplication or of absence. A later authenticated exact
prior theorem would require updating attribution and novelty framing.

## PDF, metadata, license and disclosure

I inspected every rendered page. Equations, symbols, references and page breaks
are readable, with no material clipping or overlap. The exact extracted source
rebuilt offline with the available Tectonic 0.17.0 runtime; all six raster-page
hashes and the complete extracted text equal the supplied PDF. PDF byte identity
differs as expected for a fresh build, and is not presented as a build
requirement. The embedded paper.pdf equals the standalone PDF byte for byte.

The inner publication metadata equals the outer deposit's metadata payload.
The outer wrapper lists the actual PDF and ZIP. Title, author, ORCID,
independent-researcher affiliation, date, version, preprint type, scope and
bibliography agree with the paper and README. The README grants CC BY 4.0 for
the original authored materials. The candidate ZIP contains no redistributed
third-party paper bodies; citations and source hashes are distinguished from
owned text. Extensive AI use is disclosed in the paper, README and metadata.
The paper is expressly an unrefereed draft and says internal AI reviews are not
formal independent human peer review. No fabricated human review or DOI claim
was found.

## Final disposition and exact remaining boundary

Mandatory repairs: **none**. Surviving material objections: **none**. Strongest
verified claim: the full fixed-real-positive-load theorem for the exact six-rate
physical-time chain, supported by the analytic certificate and a legitimate
finite-mean regeneration argument.

Remaining historical uncertainty is limited to uninspected final editions and
unlocated possible prior work; the candidate states this boundary correctly.
This review does not turn that uncertainty into a worldwide novelty guarantee.
It also does not supply formal proof-assistant verification, independent human
peer review, stationary population moments or performance bounds. Those are
outside the paper's actual claim. The bounded full-package review is complete.
