# Fresh cross-cutting adversarial mathematical review

PR 948; problem 30004549 / OWR-2654829-012. Frozen submitted head:
`be4313efafa1af5962394e07d8a4debff2e94d92`.
Frozen candidate: 9,997 bytes, SHA-256
`50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e`.

## Verdict

**The unchanged submitted construction is a valid counterexample to the
integrability implication in its stated smooth compact four-dimensional
scope. No central mathematical correction is required.** It constructs a
smooth nonintegrable almost complex structure on the closed connected
product of the specified genus-two curve and an elliptic curve, preserving
three independent real de Rham classes with closed anti-invariant
representatives. The structure equals the initial product complex structure
outside a coordinate ball and converges to it in the full smooth topology.

This is a mathematical verification of the exact saved proof and an exact
source-scope comparison. It is not a priority certificate, a present-openness
assertion, a human peer review, a formal proof-assistant certificate, or
authorization for publication. No new author proof response, central repair,
generalization, or further construction was performed. The author count is
**PR-declared 4/5; native historical events remain unverified**.

## Actual sequence and input authentication

My first command read current PR metadata and unnecessarily listed global
Git-status filenames. No other PR source or mathematical content was read;
the filename inventory was not repeated. I then read the allowed gate,
identity, and original-record metadata. The first authentication script
mistakenly expected an ORIGINAL_SNAPSHOT directory; the actual layout is
ORIGINAL_SNAPSHOT.json plus original/. That script failed before any
dependent source or mathematical reading. I repaired the path and completed
the full authentication at 2026-10-16T06:54:34.912451Z.

Current PR metadata was independently read before and after authentication:
OPEN, draft, base main, exact head above, unchanged. The immutable Git queue
row contains exactly problem 30004549, claimed_solved, 4/5. Its SHA-256
without an appended newline is
`14e26d488e321d3047b1aa4b2b68b56c29321b4942333804634c58a2b4d4b489`,
matching the gate. All 24 originals matched disk byte counts, SHA-256,
recorded disk permission modes, immutable tree modes, immutable blob IDs,
and direct pinned Git bytes before I read mathematical content. The full
private record is 4,190 bytes, SHA-256
`5df3868e802d9da72bced3f4606c3ccd9b6610208bcc2a086bf25e082239b34f`;
the nested statement UTF-8 hash is
`a5ce90b9c2087f20cd09cb33d9d92ca40039c19a08de3b1c098d10bf75b9179b`.
The carried review hash matches the assigned value and prior_research is
empty. I did not independently reconstruct the native SQLite review-hash
algorithm or historical author events; those remain separate provenance
questions. Raw source bodies are excluded from this review's allowlist.

Only after that gate did I read the entire source, charter and author
candidate. I saved INDEPENDENT_DERIVATION.md at
2026-10-16T06:56:12.576257Z before reading root/family/old-audit judgments.
That document contains the full independent global and local reconstruction.
I then wrote independent exterior-algebra and real-matrix checks, inspected
the primary source pages, and only then compared root/family material and
the entire original audit A/B reports. Their conclusions were challenged,
not treated as premises. Truncated compound outputs were supplemented by
dedicated complete report reads. Family seals were independently validated.

## Mathematical reconstruction and falsification

The smooth compactification uses s=1/z, q=y s^3, giving q^2=1-s^6 and two
smooth unbranched infinity points. Six simple finite branch points and the
nonsquare polynomial give a connected double cover of genus two.
At a finite branch root, dz/y=dy/(3z^5), and at infinity the two forms are
-s ds/q and -ds/q. Thus eta_0 and eta_1 are global holomorphic independent
one-forms; their ratio is the nonconstant meromorphic function z. No
singular naive projective closure is substituted for the smooth completion.

For the three real classes, let F=Re H with
H=(a-i b)Omega_0+c Omega_1. If F is exact, Stokes gives integral F^2=0,
while F^2=H wedge conjugate(H)/2 is nonnegative and positive wherever H is
nonzero. Hence H=0 and a=b=c=0. This independently confirms the submitted
harmonic-form argument. Exact perturbations then preserve these independent
classes without a continuity assumption.

The simultaneous chart zeta=z, xi=w/y(z) has Jacobian 1/y. Its extra
derivative term disappears on wedging with dz, giving both
Omega_0=d zeta wedge d xi and Omega_1=zeta Omega_0. With
zeta=u+i v and xi=x+i t, the real forms are exactly

    alpha = du wedge dx - dv wedge dt,
    beta  = du wedge dt + dv wedge dx,
    gamma = u alpha - v beta.

For arbitrary smooth compactly supported R, not just on the constant-cutoff
core, d(R v dv)=v d(R dv). Both primitive one-forms extend smoothly by zero
and therefore give global exact changes. The exact relation
gamma_e=u alpha-v beta_e survives the entire transition region, including
all derivatives of the fixed cutoff. It is consistent for three independent
global classes to have values in a rank-two real bundle.

The complete perturbed beta contains the R_u term. Its Gram identities are

    alpha^2 = 2V,
    alpha wedge beta_e = R_t V,
    beta_e^2 = 2(1-R_x)V,
    D = 1-R_x-R_t^2/4.

Uniform first-derivative bounds on the fixed smooth cutoff give D>=1/2 on
the whole patch for a common sufficiently small epsilon interval of either
sign. This is not a core-only or sampled positivity argument. Normalizing
B=(beta_e-(R_t/2)alpha)/sqrt(D) gives a decomposable Psi=alpha+i B with
Psi wedge conjugate(Psi)=4V. The contraction kernel and its conjugate are
complementary. Declaring the first kernel T^(0,1) supplies a real smooth J
with the correct sign, equal to J_0 at epsilon zero.

An additional independent algebraic verification reconstructs
J=-A^(-1)Bmat, where A and Bmat represent alpha and B. For arbitrary
R_u,R_x,R_t it verifies J^2=-Id, J-transpose A J=-A, and the analogous
beta_e anti-invariance. This checks the full transition-region realization,
not merely its normalized Gram determinant. It agrees with the local
family matrix after comparison.

Compact support gives a full equality collar with all jets, so gluing J_0
outside the ball is smooth. Zeros of Omega_0 on the two infinity fibers are
outside the kernel construction and cause no division or extension problem.
Every finite derivative of epsilon times the fixed cutoff tends uniformly
to zero, while D stays away from zero. Smooth algebraic dependence of J
therefore gives convergence in each C^m norm, hence in C-infinity. There is
no analyticity assumption. Epsilon zero is explicitly the integrable limit;
D=0 and large epsilon are outside the construction.

On the core, k=1-epsilon x and

    phi_1=du+i sqrt(k)dv,
    phi_2=dx+i k^(-1/2)dt.

Direct exterior multiplication gives
d phi_1 wedge phi_1 wedge phi_2=k_prime/(2k)V. Independently the submitted
Nijenhuis convention gives
N(partial_u,partial_x)=k_prime/(2k)partial_u, equal at the origin to
-epsilon/2 partial_u. My program computes all six coordinate pairs and
agrees with the local family. Nonzero N for every small nonzero epsilon
proves nonintegrability. Conjugation or a common alternative normalization
of N cannot erase this nonvanishing.

Unique continuation does not turn the compactly supported differences into
zero: the original beta is not anti-invariant for the new J, so their exact
difference is not a closed anti-invariant form for one fixed J. None of the
retained nonzero forms vanishes on an open set. The Nijenhuis tensor is not
subject to an elliptic continuation theorem forcing an arbitrary smooth
deformation integrable merely from integrability outside the ball.

## Explicit tests against hidden integrability restrictions

The normalized B need not be closed. On the core,

    B=k^(-1/2)du wedge dt+sqrt(k)dv wedge dx,
    dB=-k_prime/(2 k^(3/2)) dx wedge du wedge dt,

which is nonzero. Thus the closed-alpha-and-closed-Jalpha integrability
criterion from DLZ does not apply: Jalpha=B, rather than beta_e. Closedness
of both unnormalized real generators is insufficient. No closed complex
volume form is asserted.

DLZ Theorem 1.1 requires a common compatible metric with the original
integrable structure. On the core invariant plane spanned by partial_u and
partial_v, J_0 compatibility requires g_uu=g_vv; the new J requires
g_uu=k^(-1)g_vv. At a nearby core point with epsilon*x nonzero these are
inconsistent with positivity. Therefore closeness to J_0 does not put this
example in that theorem's metric-related class. The original audit A's
alternative square-zero-form obstruction and audit B's restricted-plane
argument are both valid.

The product has b_1=6, b_2=10 and signature zero, hence b^+=5. These follow
from the product cohomology and its four hyperbolic tensor pairs plus the
factor hyperbolic pair. Thus the positive cohomology subspace and the known
tamed bound h-minus<=b^+-1 permit the claimed lower bound. Smallness also
allows taming by the original Kähler form, but no fixed-form compatibility
or almost Kähler claim is used or inferred. The canonical bundle has the
stated zero divisor and is not being trivialized globally.

## Primary-source scope

After the independent reconstruction, I used the source-scope family's
primary PDF copies and independently checked their SHA-256 values against
its retrieval map. I extracted complete relevant pages and personally
rendered/read three decisive pages: MFO OWR PDF p.31/printed p.1687,
DLZ p.5, and Tan-Wang-Zhang-Zhu v3 p.2. PRIMARY_INPUTS.json records the
precise bytes/pages and the private renders are excluded from publication.
The neighboring OWR pp.1686-1689 and DLZ definitions/metric theorem pp.2-4
were also read in context.

OWR Conjecture 2.5 and DLZ Conjecture 2.5 both state the integrability
implication on compact real four-manifolds, without an attached fixed
metric, symplectic, product-exclusion or real-analytic qualification. DLZ
defines forms as smooth sections and uses the -1 anti-invariant convention.
OWR's one reversed-sign prose sentence conflicts with its own displayed
formula; that formula, its real (2,0)+(0,2) identity and DLZ resolve the
intended convention. The candidate meets both the real closed-form and
real cohomology definitions. It is connected and boundaryless, so no
ambiguity over implicit connectedness or boundary conventions weakens it.

The separate generic clause is prior work. The actual Theorem 1.1 of
Tan, Wang, Zhang and Zhu v3 states open dense vanishing in the C-infinity
topology on the full space of almost complex structures of a closed
four-manifold admitting them. Its statement is not restricted to one fixed
metric, despite the proof's use of compatible metrics. My scope check used
the primary arXiv theorem and the full source-scope review; I do not assert
byte equivalence with a subscription publisher version. A special
nonintegrable family retaining three classes does not contradict generic
vanishing.

Primary links: [MFO OWR 33/2020](https://publications.mfo.de/bitstream/handle/mfo/3805/OWR_2020_33.pdf?isAllowed=y&sequence=4),
[DLZ](https://arxiv.org/abs/1104.2511), and
[Tan-Wang-Zhang-Zhu v3](https://arxiv.org/abs/1112.0768v3).
Fresh web inspection confirmed the two arXiv version/author records; the
DOI resolver failed in the web tool and was not used as independent
evidence. The source-scope family's withdrawn Lejmi-Upmeier record is not
used as a theorem or proof obstruction. No full novelty search was
performed by this reviewer.

## Computation, comparison, and evidence limits

check_math.py is independently authored and imports no candidate or other
review checker. It verifies general-cutoff wedges, third-form closure,
normalization, full real-J square and anti-invariances, core factorization,
coframe obstruction and all Nijenhuis pairs. A wrong gamma correction sign
is rejected by rank three; omission of cutoff derivatives is rejected by
nonclosure. The script uses explicit exceptions, so optimized Python does
not disable it. Both normal and optimized runs pass with SymPy 1.14.0.

One initial run failed because my checker compared rationally equivalent
Nijenhuis expressions structurally. Replacing that comparison by
simplification of their difference repaired my test, not the mathematical
candidate. The actual failure and correction are recorded in the log.
Finite algebra supports the local formulas; the global and uniform claims
are justified by the preceding proofs, rather than inferred from code.

Root reconstruction, the sealed local/global/source reports, and original
audits A/B agree with these independently obtained conclusions. I checked
their scope limits against the original README, scope cover, verification
results and source-verification metadata. Original audit B's full-cutoff
coframe also expands to the claimed normalized form, including R_u. No
additional assumption, circular proof dependency, sign contradiction or
unsupported global extension was found. The computation-family's final
packaging review is a separate dependency; its historical replay and
strict-publication-profile findings must be carried forward by the parent.

## Specific findings and remaining gaps

1. **R948-MATHF-01, required documentary qualification.** The original
   README/scope cover assert a cumulative 4/5 count as one earlier turn plus
   three resumed turns. The root's native selected-target records at the
   original and current-main heads contain no corresponding state or
   history entries. This does not falsify the stated count, but it does
   not authenticate that chronology. Preserve the historical files and
   label 4/5 as PR-declared/native history unknown in new promotion
   material. This audit itself adds zero substantive author responses.
2. **R948-MATHF-02, required future scope and credit.** Any paper or
   promoted cover must credit all four authors of the generic theorem and
   use the correct OWR 2020 report identification. The selected corpus
   source has a 2021 label and an abbreviated attribution omitting Zhu.
   The original PR's README already gives correct credit and report year;
   no original proof edit or source-cache mutation is required.
3. **R948-MATHF-03, required evidentiary limit.** The valid conclusion is
   h-minus at least three in the smooth compact category. Exact dimension,
   fixed symplectic compatibility, analyticity, historical novelty and
   present openness are not certified. The prior audits' bounded negative
   literature searches do not discharge the planned deep priority audit.
   The original package generally states these limits correctly; continue
   to preserve them. This is a condition on promotion, not a mathematical
   defect in the construction.
4. **R948-MATHF-04, optional exposition.** In a new typeset paper distinguish
   the named genus-two curve C from the complex plane in the elliptic
   quotient, and include the explicit no-common-metric and nonclosed-B
   checks. The historical public scope cover already resolves the
   typography ambiguity. These additions help readers test the apparent
   contradiction with nearby integrability criteria without changing the
   proof.
5. **R948-MATHF-05, separate package dependency.** The historic verification
   wrapper is a replay/integrity tool and finite algebra is not a formal
   proof certificate. Preserve computation-family findings about its
   execution assumptions and proposed strict publication profile. I did
   not independently re-audit its full wrapper security/resource envelope;
   that family owns the detailed result.

There is no remaining mathematical gap in the exact counterexample or its
match to the exact conjecture within this review's assigned scope. Deep
priority/current-status review, any new paper and its entire-package
adversarial review, native history authentication if later possible, and
the stricter publication profile remain separate work. This family changed
only its own review directory. It did not alter the checkout/index/HEAD,
branches, shared helpers, originals, other shards, root state, or goals;
it did not checkpoint, merge, publish, or communicate with any external
individual.

Final storage note: two attempts to create RESULT.json hit intermittent
ENOSPC. I removed only my own three temporary inspected page renders
(634608 bytes), whose hashes and inspection record had already been saved.
No original or other family file was deleted. The parent directed
finalization without waiting for the computation-family final seal, which
root will authenticate separately.
