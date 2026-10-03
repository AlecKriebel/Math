# Independent adversarial audit: massive double-cone modular generators

**Target:** 30005723, OWR-14298009-001, “Modular Generators for Massive Double Cones”  
**Audit date:** 3 October 2026  
**Verdict:** **PASS_PARTIAL**  
**Source problem:** **UNRESOLVED** after the five recorded attempts

## 1. Decision and limits

The frozen package passes as a carefully delimited partial research note. No
material mathematical error was found in the claims it actually makes. In
particular, the main Schwartz-space identity and its conditional global-ansatz
obstruction are valid; the finite-dimensional examples are genuine standard,
factorial one-particle examples. They are not continuum counterexamples.

This verdict does **not** certify either mass dependence or nonmultiplication
for the continuum massive double cone. It does not certify a continuum
approximation, the domain assumptions of an unspecified candidate generator,
or the absence of a solution anywhere in the literature. There is no complete
candidate proof to approve. Keep the original problem unsolved and the attempt
count at five. The audit itself authorizes no publication or remote write.

The author and auditor checks are distinguished below. Their counts are a
reproducibility record, not a numerical measure of proof strength.

## 2. Frozen input and reproducibility

The manifest `audit/FROZEN_INPUTS.json` has SHA-256

    19cf0e95e43fd4fb82ce6debdc99e98aeb7ff288b4e26decd8f955bce9e43004

Its 12 listed files match both their byte counts and SHA-256 hashes before and
after the audit. The report, all five attempts, source-check summary, research
log, README, and verification materials were read. No frozen file was changed.

The author's verifier was executed from an isolated temporary copy because
running it at its original location would rewrite its adjacent results file.
The replay output equals the frozen `verification/results.json` exactly:

- 37 exact symbolic/rational assertions
- 5 high-precision finite numerical replays
- 6 negative controls

The independent program `audit_controls.py` also passes:

- 23 exact assertions, including a construction from Tomita's defining map
- 5 supplementary numerical checks at 70 decimal digits
- 11 negative controls

The largest error in the independent non-special finite Tomita/arcoth
comparison is approximately 1.21 × 10⁻⁶⁷; the resolvent-integral derivative
comparison differs by approximately 8.23 × 10⁻⁶⁹. These are ordinary
high-precision floating-point checks, **not interval certificates**. Exact
finite proofs and analytical arguments are given separately below.

The reproducible results and versions are in `control_results.json`. That file
also binds the independent verifier by its SHA-256. The independent verifier
writes only its own results and temporary replay files.

## 3. Primary-source and scope audit

The original question was checked against the official MFO report, including
the displayed equations and the image of printed p. 2862. The question asks
both whether M₋ is mass independent and whether it is a multiplication operator.
The numerical-approximation disclaimer appears on that same printed page;
the figures and interpretation continue on p. 2863. The catalogue fragment's
p. 2863 label is not the precise location of the questions. This does not alter
the author's reconstructed target. [Cadamuro, OWR 50/2023, pp. 2861–2864](https://publications.mfo.de/bitstream/handle/mfo/4092/OWR_2023_50.pdf?isAllowed=y&sequence=4).

The operator convention was checked against Definition 2.1, Lemma 2.2 and
Proposition 2.3 of Bostelmann–Cadamuro–Minz (BCM). The report correctly uses the
Sobolev cutting projections, essential self-adjointness and closure in the B
construction. It does not silently replace them by a bounded characteristic-
function multiplier on the critical Sobolev spaces. BCM's Sections 3 and 7
explicitly distinguish their finite numerical procedure from a convergence
proof. Their full-space construction is also distinguished from a
restricted-region entanglement Hamiltonian. [BCM, arXiv:2209.04681v3](https://arxiv.org/abs/2209.04681v3).

The Longo–Morsella final erratum was read. Its earlier positive-mass analysis
was removed after a gap; the retained result is massless. The current primary
arXiv record independently confirms this change. The frozen package does not
reuse the withdrawn massive claim. [Longo–Morsella, arXiv:2012.00565v4](https://arxiv.org/abs/2012.00565v4).

The following narrower source distinctions were also checked:

- Figliolini–Guido, Theorems 4.1 and 4.4, concern strong generalized/resolvent
  continuity and modular-group continuity in their common realization. They
  do not, by themselves, supply a derivative of the unbounded time-zero block
  on a prescribed common domain. [Primary archive](https://www.numdam.org/item/AIHPA_1989__51_4_419_0/).
- Fröb's equations (1.7)–(1.9) express restricted modular data using two-point
  functions. An unevaluated spectral expression is not an evaluation of the
  massive-ball block. [arXiv:2501.09669](https://arxiv.org/abs/2501.09669).
- Arias et al.'s scalar discussion concerns leading local terms and high-energy
  information. It is not equality of the entire scalar kernel.
  [arXiv:1611.08517](https://arxiv.org/abs/1611.08517).
- Hollands–Longo–Morsella's 2026 paper gives bounds and still describes the
  explicit massive-ball Hamiltonian as unavailable in its introduction.
  [arXiv:2602.03606v1](https://arxiv.org/abs/2602.03606v1).

The current primary records for BCM, Longo–Morsella and Hollands–Longo–Morsella
were checked on the audit date. The DOI resolver was inaccessible through the
web tool, but the official MFO PDF was accessible. The pinned target and prior-
result summaries were read locally. A fresh comprehensive repository/corpus
duplicate search was not undertaken in this mathematical audit; those
administrative search claims are not used as premises of a theorem. No source
PDF, full-text corpus, private record, or search dump is included in this audit
folder.

## 4. Main identity: independently verified

Set A = −Δ + m², ω = A¹ᐟ² and q = 1 − |x|², with m > 0. The claim is

    ω q ω = −div(q grad) + m² q + (n−1)I + m² A⁻¹              (A)

on Schwartz space. It is correct in every integer spatial dimension n ≥ 1.

### A separate derivation

For any operators for which the products below are defined,

    ω q ω = ½{A,q} − ½[ω,[ω,q]].

Under the Fourier convention ∂ₓ ↦ ip and x ↦ i∂ₚ, q becomes 1 + Δₚ.
Therefore

    [ω,[ω,q]] = 2 |gradₚ ω|² = 2|p|²/(|p|²+m²).

Meanwhile, in position space the product rule gives

    ½{A,q} = −div(q grad) + m² q − ½Δq
           = −div(q grad) + m² q + nI.

Subtracting the double commutator gives (A), including the positive sign and
coefficient of m²A⁻¹ and the constant n−1. The independent symbolic tests
additionally apply both full Fourier differential expressions to an arbitrary
symbolic test function in dimensions 1, 2 and 3. They check derivative terms
on both sides, rather than only the derivatives of ω. The same tests allow
q = R² − |x|²; the residual is unchanged.

### Domain and normalization checks

For m > 0, the Fourier multipliers ω and ω⁻¹ are smooth with all derivatives
polynomially controlled. Each preserves Schwartz space. Polynomial
multiplication, differentiation, and the compositions in (A) are consequently
well-defined there. No closure or global self-adjoint-extension identity is
inferred just from this calculation.

The inverse A⁻¹ is convolution with the heat-kernel integral

    Gₘ(z) = integral from 0 to infinity of
            exp(−m²t)(4πt)^(−n/2) exp(−|z|²/(4t)) dt.

It is strictly positive for z ≠ 0. The familiar special cases are
exp(−m|z|)/(2m) in dimension 1 and exp(−m|z|)/(4π|z|) in dimension 3.
The independent quadratures agree with these normalizations; the positivity
argument itself is analytical, not numerical.

If h is nonnegative, nonzero and smooth with compact support in D, all local
terms in (A) vanish outside the closed ball. The remaining convolution is
strictly positive there. Its integrals converge because the observation point
is separated from supp(h), and because m > 0 controls the large-t part.

The m = 0 endpoint is not inserted into a proof using Schwartz preservation
of ω⁻¹. In particular, no one-spatial-dimensional massless scalar vacuum is
assumed. The frozen package explicitly respects this limit.

## 5. Localization obstruction: valid with exactly the stated hypotheses

Let L be the closed real local standard subspace. For v in L ∩ dom(log Δ),
modular invariance ΔⁱᵗL = L gives

    lim as t → 0 of (Δⁱᵗv − v)/t = i log Δ v ∈ L.

In the report's convention K = −i log Δ, so K v also belongs to L. The sign
change is immaterial; using log Δ alone instead would be incorrect because L
is a real subspace. The report uses the appropriate real generator.

The Sobolev spaces embed continuously in distributions. Limits of local data
therefore remain distributionally supported in the closed ball. This step
needs only support containment, not an unproved identification of all
boundary-supported Sobolev distributions with the closure of interior tests.

Now impose the report's actual hypotheses: M₋ equals cq globally, c ≠ 0;
the conjugation M₊ = ωM₋ω is valid on the indicated local smooth tests; and
(h,0) belongs to the generator domain. Then K(h,0) has second component
−cωqωh, which has a nonzero exterior tail by (A). This contradicts the support
condition. The conditional obstruction follows.

The following attempted upgrades are **not** justified, and the frozen note
correctly does not make them:

1. Specifying a multiplier only inside D does not specify its action on ωh,
   which is not supported in D. Thus the calculation does not exclude a
   parabolic *interior restriction* with a different exterior action.
2. Schwartz membership does not establish membership of an unspecified
   modular-generator domain. That membership remains an explicit hypothesis.
3. Ruling out cq does not rule out arbitrary radial or nonpolynomial
   multipliers, including mass-dependent ones.
4. Positive-mass constancy does not identify an m = 0 block without a theorem
   controlling the chosen realization and unbounded block limit.

The quadratic extension in Attempt 2 also checks out within its stated global
multiplier and domain framework. Symmetry gives a+b|x|²; the interior and
complementary entropy signs force its boundary value to vanish, leaving cq
with c ≥ 0. For c = 0 both blocks vanish. If Δ = I, the Tomita involution is a
conjugation and its real fixed space equals its symplectic complement; a
nonzero factorial standard subspace cannot have this property. This argument
is not asserted for arbitrary multipliers or informal kernels.

## 6. Other analytical claims

### Mass derivative

In finite dimension with A(λ) = A₀+λI, differentiating the outside factors is
essential. For E = A⁻¹ᐟ⁴, C = A¹ᐟ⁴χA⁻¹ᐟ⁴, B = C+C*−I and F = arcoth B,
the identities in Attempt 1 are correct:

    B′ = ¼[A⁻¹,C−C*],
    M′ = −¼(A⁻¹M+MA⁻¹) + 2E DF_B(B′)E.

The resolvent integral for DF has the stated negative sign and factor ½.
Multiplying on both sides by E⁻¹ gives the reported cancellation criterion.
The independent check uses a non-special four-dimensional A and χ, directly
integrates the resolvent derivative, and compares it with differentiation of
the spectral expression. Omitting the outside-factor derivative is detected.
Nothing here licenses differentiating the critical-Sobolev continuum formula
or passing through the arcoth endpoints.

### Dilation, symmetry and positivity

AₘU_R = R⁻²U_RAₘR and χ_RU_R = U_Rχ₁ imply cancellation of the dilation
factors within B and a factor R in M₋. Thus

    M₋(m,R) = R U_R M₋(mR,1) U_R⁻¹

has the right direction and units. The unit-ball massless parabola becomes
π(R²−|x|²)/R. This avoids importing the general-radius normalization ambiguity
in the source prose.

A multiplication realization inherits rotational covariance and hence a radial
representative, with reflection supplying evenness in dimension 1. The
conditional entropy signs and containing-wedge bound have the correct direction.
Using a countable dense set of tangent-wedge normals before taking a pointwise
infimum justifies

    0 ≤ f(x) ≤ 2π(1−|x|)  almost everywhere in D.

The frozen text correctly treats these as necessary conditions. They do not
select one multiplier; the displayed convex-combination examples satisfy the
bound without being claimed to be modular generators.

### Witnesses and spectral endpoints

A nonzero disjoint-support continuum pairing, with justified form/operator
domains, rules out multiplication. Vanishing of all such tested pairings alone
does not distinguish multiplication from a local differential operator.
Likewise, a nonzero common-realization pairing difference between two masses
would suffice to disprove independence. A radial multiplier acts identically
on normalized angular-momentum sectors with the same radial tests. The source
package keeps the requisite continuum/domain qualifications in each criterion.

The scalar arcoth endpoint example has the correct nonzero limit, ½ log 2.
Its conclusion is a lack of a *uniform* modulus of norm continuity as the
spectral gap closes, not discontinuity at a fixed operator with a positive
gap. The report's resolvent bound 1/[a(a−1)] is valid for the stated two-sided
gapped spectra and does not require commutation.

There is one optional sharpening, not a blocking correction: the better
constant 1/(a²−1) is also valid here by a separate inverse-power-series proof.
Indeed,

    arcoth B = sum over k ≥ 0 of B^(−2k−1)/(2k+1),

converges in norm when ||B⁻¹|| ≤ 1/a < 1. The inverse identity and telescoping
products give

    ||B^(−j)−C^(−j)|| ≤ j a^(−j−1)||B−C||,

including noncommuting B,C and spectra of either sign. Summing gives
1/(a²−1). The frozen warning against simply replacing a resolvent bound by a
scalar derivative estimate is a valid caution about that argument, but should
not be read as saying the sharper operator bound is false. Both bounds diverge
as a approaches 1, so this sharpening closes none of the continuum gaps.

Finally, the verified-interval criterion with a separate continuum error η is
valid, and error bounds add for differences of masses or sectors. No such
field-specific η was supplied. Stable plots or extra precision do not supply it.

## 7. Finite models: checked from the definition

This was audited independently of the author's B-matrix computation. Write

    T = ½ [[α+β, α−β], [α−β, α+β]],   E = T⁻¹,

with 0 < α < β. In the normalized real Hilbert space R⁴, let

    J = [[0,I], [−I,0]],
    W = columns (T e₁,0) and (0,E e₁).

The local real subspace is range(W). Direct symbolic computation gives

    det[W,JW] = (α²−β²)²/(4α²β²) > 0,
    WᵀJW = [[0,1], [−1,0]].

The first equality establishes standardness; the second establishes
factoriality. The conditions involving the complementary coordinate also
follow directly or from the same computation with e₂. At α = β the determinant
vanishes and B reaches ±1, so that degenerate parameter choice cannot be
silently retained as a standard finite example.

Define the Tomita involution by S = [W,JW] diag(I,−I)[W,JW]⁻¹. It satisfies
S²=I, SJ=−JS and SW=W. Its modular operator is exactly

    Δ = SᵀS = diag(d,d⁻¹,d,d⁻¹),
    d = ((β−α)/(β+α))².

Transporting −J log Δ back by diag(T,E) yields

    M₋ = [2/(αβ)] log((β+α)/(β−α)) diag(1,−1),

with precisely the report's sign and factor 2. This direct derivation verifies
that the finite example is a genuine modular construction, not merely a formal
substitution into the cited spectral formula.

Adding λI to A changes α and β as stated. The exact asymptotics give c(λ) → 0
while c(0) > 0; hence the coefficient is nonconstant without reliance on decimal
differences. Combining the (1,2) and (3,4) blocks and conjugating by the
inside-coordinate rotation preserves χ and standardness. The resulting M₋ has
a nonzero commutator with an individual coordinate projection. Its nonzero
entry is certified by 3⁶ > 7, so it is not a multiplier in the fixed four-point
position algebra.

None of those matrices is the continuum Helmholtz operator, and no convergence
map to that operator is supplied. The examples refute an alleged consequence
of the abstract algebra alone; they do not answer the original field-theory
question. The report consistently maintains that distinction.

## 8. Publication-safe disposition

No mathematical HOLD is required for the frozen package as a **partial note**.
The global-ansatz domain/support conditions and the finite-versus-continuum
warnings must remain visible in any summary. A title or queue entry asserting
that the original problem is solved would contradict this audit.

The independent audit folder contains only this report, its README, the
independent control program, its results, and a small verdict record. It
contains no primary-source PDF, full source text, private catalogue/corpus
content, credentials, or remote-operation artifact. No remote write, release,
external researcher communication, or publication occurred during this audit.

**Final classification: PASS_PARTIAL; original continuum target UNRESOLVED.**
