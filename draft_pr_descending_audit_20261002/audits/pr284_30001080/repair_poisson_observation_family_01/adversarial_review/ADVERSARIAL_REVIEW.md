# Independent adversarial review of the frozen Cox-observation candidate

**Verdict: PASS for the exact separately scoped theorem.** No fatal mathematical gap or counterexample was identified. The conclusion verified here is that the probability law of a nonzero locally finite Radon measure is mass-stationary if its law is invariant under every projected, point-configuration-only, invariant, counting-preserving Markov transport in the candidate's hypothesis (H). The sufficient observable family in the frozen proof belongs to that class.

This does **not** certify the deterministic-allocation subclass, the isolated-singleton matching subclass, a general sigma-finite law of the random intensity, a theorem with nontrivial auxiliary X, coverage of the entire original OWR target, novelty, or publication readiness. These are scope boundaries, not failures of the theorem reviewed.

Mathematical checks completed at **2026-10-06T03:01:06Z**; report and final frozen-hash recheck completed at **2026-10-06T03:03:36Z**. Best-guess completion: **100% of this frozen-candidate verification task**, and **100% of the scoped theorem's proof**. Completion of a broader discovery/publication goal is not assessed. Verification confidence: high; standard measurable-kernel, Haar-uniqueness, and countable-determining-class facts remain credited mathematical inputs.

## 1. Frozen evidence and constraints

Candidate: `../POISSON_OBSERVATION_REPAIR.md`.

Candidate SHA-256 checked before review:

    bd5eb9048439f6e6cac903e0b44b0277180e360dc94439f8eab34fac19efeeef

Operative source: `../../ROOT_final_Cox_source_01/FINAL_2011_Cox.txt`, SHA-256:

    e40bb13739b6c6eb1ec501290b864aad0edebf1a879a01604032b07ac3f8ee2a

Source locations used: lines 141--150 (group and translation convention), 187--203 (Mecke characterization (2.5)), 216--247 (transport definitions and transport invariance), 524--543 (Poisson/Cox setup and Remark 4.2), and 632--665 (Remark 4.8, constant-X finiteness in Remark 4.10, and equations (4.8)--(4.9)). The source convention is theta_s alpha(B)=alpha(B+s).

Root and queue AGENTS instructions were read. Queue README and record 30001080 were read as context; its imported prior-research field is empty. The compressed imported statement is not treated as the exact scoped theorem. No original-author proof, sibling report, external contact, external literature search, Git action, publisher action, branch/ref action, or primary-index mutation was used. This is verification of a frozen turn-3/5 candidate, not an additional proof-search turn.

## 2. Transport admissibility — passes

For every locally finite nu, compactness of C gives finite positive denominators. Since b is between zero and one,

    r_b(nu,s) <= nu(s+C)/(1+nu(s+C)) <= 1.

Consequently T_b has nonnegative entries and row mass one, including at empty input, at starting locations outside the support, and with multiple atoms. All its inputs are the observed nu and the start location s. No background alpha or extra mark is smuggled into b.

The observation involution satisfies

    J(theta_s nu,t-s) = (theta_t nu,s-t).

Together with symmetry of C and the denominator, this proves j_b(nu;s,t)=j_b(nu;t,s). Translation covariance follows from theta_r nu(s-r+C)=nu(s+C) and theta_{s-r} theta_r nu=theta_s nu.

Preservation does not require an illegal subtraction of infinite masses. For every Borel A, Tonelli gives the incoming off-diagonal mass as integral_A r_b(nu,t) nu(dt). Adding integral_A (1-r_b(nu,t)) nu(dt) yields nu(A) pointwise under the integral. Thus even when nu(A) is infinite, preservation is valid as an equality of positive measures.

The usual evaluation-field facts make (nu,s,t) -> nu(s+C), j_b, r_b, and T_b measurable: nu(s+C) is the kernel integral of 1_C(x-s). Hence this is an actual invariant Markov transport, not merely a formal symmetric flow. It preserves every locally finite Radon measure and therefore every counting configuration required by the hypothesis.

## 3. Poisson Mecke and finite holding subtraction — pass

For nu=eta+delta_0, an off-diagonal destination s is chosen from eta(ds); the inserted atom at zero contributes only to holding. Applying the ordinary conditional Poisson Campbell--Mecke identity inserts delta_s, producing exactly

    alpha(ds) integral a_C(eta+delta_0+delta_s;0,s)
                       b(eta+delta_0+delta_s,s) Pi_alpha(deta),  s != 0.

Both endpoint insertions are necessary and present. An atom already at an endpoint is not erased; the formula accommodates non-simple configurations.

For bounded f, probability of P and row mass one make every term in (H) finite. If q_b(alpha) is the total off-diagonal projected mass, the holding contribution is f(alpha)(1-q_b(alpha)). Subtracting it yields

    integral [f(theta_s alpha)-f(alpha)] b(nu,s) a_C(nu;0,s) L(dalpha,dnu,ds)=0.

This subtraction uses finite quantities. No finite Campbell expectation is assumed. With b=1 the same row bound implies M(total)<=1; pushing forward by R preserves that finiteness.

## 4. R and J signs — pass

Under R, theta_s transforms eta's Poisson intensity to theta_s alpha. It transforms the inserted endpoints {0,s} to {-s,0}. Thus at an output base point (alpha,s), R_*L has base marginal c^R and residual kernel Pi_alpha. This confirms candidate (3).

Under observation-only J, alpha is unchanged. An output edge s comes from the input edge -s. The translated residual is theta_{-s} eta and therefore has intensity theta_{-s} alpha. The deterministic endpoints again become {0,s}. Hence the residual kernel of J_*L is Pi_{theta_{-s} alpha}, with base marginal c^I. Applying the same argument to R_*L gives base marginal (c^R)^I and the same shifted residual kernel.

The weight a_C(nu;0,s) is unchanged under both R and J, because its two denominators exchange and C=-C. The observable gate b is also unchanged under the observed reversal. These facts give (4) with the permitted intensity test f and no intensity-dependent gate.

## 5. Positive observable symmetrization and deweighting — pass

For any observation event E, b_E=(1_E+1_E composed with J)/2 is Borel, J-invariant, and valued in [0,1]. Using f=1_A gives equality on the rectangles A x E of

    M+J_*M  and  R_*M+J_*R_*M.

These are finite positive measures on the product of the intensity space and the observation space. Rectangle uniqueness therefore yields their equality on the entire product field. J fixes alpha, which is exactly why the intensity factor remains 1_A under this symmetrization.

On D_C={s in C, s != 0}, the common weight is strictly positive and D_C is stable under both reversals. Multiplying the weighted equality by min(n,1/a_C)1_B, for an arbitrary Borel B subset D_C, and taking monotone limits gives the unweighted equality of positive measures. The resulting integrals may be infinite; no signed cancellation or finite/infinite subtraction is used. Values of a_C equal to zero outside D_C are irrelevant to this restriction.

## 6. Sigma-finiteness, residual removal, and RN coefficients — pass

The Campbell base c=P(dalpha)alpha(ds) has a countable finite cover

    F_nk = {alpha: alpha(C_n)<=k} x C_n,

where C_n is a compact exhaustion. On F_nk, c(F_nk)<=k because P is a probability law. R_0 and I are Borel involutions, so their images of the finite cover are measurable finite covers for c^R, c^I, and (c^R)^I. Restriction to D_C keeps these measures sigma-finite. A common finite cover for their sum is obtained by intersecting one cover set from each of the four covers; the countable four-index family covers the space. Thus lambda is indeed sigma-finite, and each constituent's RN density lies in [0,1].

The endpoint-removal map nu -> nu-delta_0-delta_s is well-defined and Borel on the common support of all four observed measures. On that support both distinct endpoint masses are at least one. The map can be set to the zero configuration elsewhere, without changing any measure under review. Atomic multiplicities create no ambiguity: exactly one unit at each distinct endpoint is subtracted.

After this pushforward, equality on a base set of finite lambda mass and a residual-configuration event reads

    integral [u Pi_alpha(F)+v Pi_{theta_{-s}alpha}(F)] dlambda
      = integral [u' Pi_alpha(F)+v' Pi_{theta_{-s}alpha}(F)] dlambda.

Each integrand is bounded by two. RN uniqueness therefore applies on the common finite cover. A countable determining pi-system for the standard Borel configuration space, including its whole space, produces a single exceptional lambda-null set. On its complement the finite conditional measures agree for every residual event, giving (7) and (8). This argument does not presume a disintegration of an arbitrary non-sigma-finite measure.

## 7. Separation of two Poisson laws — passes

Distinct locally finite Radon intensities are distinguished by a set B in a countable relatively compact generating ring. Both intensity values on B are finite. Consequently the void probabilities exp(-alpha(B)) and exp(-beta(B)) differ.

Set d=u-u'. Equation (8) gives v-v'=-d. Applying (7) to this distinguishing void event then gives

    d [Pi_alpha(eta(B)=0)-Pi_beta(eta(B)=0)]=0,

so d=0. This proves c=c^R on the nonperiodic locus. The countable determining-class step has already supplied one common null set; no measurable choice of a distinguishing B is required. The equivalence theta_s alpha != alpha iff theta_{-s} alpha != alpha is immediate from inverse translations.

Order-two displacements cause no defect: if s=-s, the intensity laws may still differ. If they do not differ, this is exactly the period locus handled next.

## 8. Period locus and exhaustion — pass

For a fixed alpha, the continuous translation action in the vague topology makes H_alpha a closed subgroup. Restricting alpha to H_alpha gives a Radon, locally finite measure invariant under every translation by an element of H_alpha. If nonzero, Haar uniqueness makes it a constant multiple of Haar measure on H_alpha; otherwise it is zero. Since H_alpha is Abelian, inversion preserves Haar measure. Thus alpha restricted to H_alpha is inversion-invariant.

On this graph, R_0(alpha,s)=(alpha,-s). The pointwise inversion identity can be integrated against arbitrary Borel functions of (alpha,s), since the period graph is Borel. No measurable normalization of Haar measures is needed. This gives c=c^R on the entire period graph, including graph sections with zero alpha mass. At s=0 reversal is literally the identity.

An increasing symmetric compact-neighborhood exhaustion of the locally compact second-countable group covers all displacements. Positive-measure exhaustion combines the nonperiodic, periodic, and zero-displacement identities to yield c=c^R globally. The resulting identity is exactly the final source's equation (2.5) with a trivial one-point X. The nonzero-law assumption matches the source's mass-stationarity setting.

## 9. Source-class coverage and necessity — pass within stated scope

The observable T_b is an invariant preserving Markov kernel on the point configuration alone. In particular it is sigma-finite as a kernel, and its projection is exactly final Remark 4.8 equation (4.7). The final text calls T a mass-preserving and sigma-finite transport kernel; the candidate explicitly supplies the invariance needed for Poisson covariance. No interpretation of that wording is required to include the constructed kernels, since they have all these properties.

The final Section 2 defines transport kernels as Markovian. The constructed rule is generally not a delta kernel and is not an allocation or a singleton matching. The frozen artifact correctly keeps those narrower class questions open.

For the converse, final Theorem 4.1 and Remark 4.2 make the inserted Cox process jointly mass-stationary with the intensity, so projected invariant preserving Markov kernels preserve the intensity law. If a kernel was originally specified only on counting configurations, it may be set to delta_s outside that invariant Borel subset; this supplies a preserving invariant kernel on all of M without changing the Cox integrals. Thus the theorem's counting-only formulation introduces no necessity gap.

The source's condition P(X in .) sigma-finite, with a trivial constant X, forces total P mass to be finite (Remark 4.10). Probability normalization is therefore a legitimate scope restriction. The review does not infer any general sigma-finite canonical-law result from this.

## 10. Independent boundary controls and strongest verified result

The standard-library script `exact_finite_checks.py` ran successfully and printed:

    PASS: 21136 exact transport fixtures; all row sums, preservation, covariance, endpoint signs, and finite period inversions.

Fixtures use exact rational arithmetic on cyclic groups of orders 1--5, every multiplicity vector with entries 0--3, every symmetric neighborhood containing zero, and four observable gates symmetrized from events. They check Markov row sums, counting preservation, translation covariance, row bounds, both endpoint-removal signs, and inversion on finite period subgroups. These finite controls test formulas and boundary cases; they do not establish the infinite-group theorem.

Additional analytic boundary controls:

- A heavy-tailed finite-group intensity alpha=N(delta_0+2delta_1), with P(N=n)=1/(n(n+1)), has infinite Campbell mass but a probability law. The common-cover/RN argument still applies; the weighted row bound still makes M finite. This confirms the proof never assumes a finite first intensity moment.
- An order-two edge with unequal endpoint intensities has distinct residual Poisson laws; no orbit orientation is needed.
- For a shifted periodic comb on the real line, H_alpha may carry zero alpha mass. The period argument explicitly allows its restricted measure to be zero.
- Haar intensities have H_alpha=G and are settled entirely by inversion; alpha=delta_0 is settled at the zero edge. Nonzero atomic multiplicities require no simplicity hypothesis.

**Strongest verified result:** the entire frozen probability-law, trivial-constant-X, projected point-only Markov characterization is proved, including atomic, diffuse, infinite-total-mass, infinite-expected-local-mass, periodic, and torsion cases allowed by its assumptions.

**Exact remaining mathematical gap within that theorem:** none identified. Remaining gaps outside it are deterministic/isolated-singleton class sufficiency, nontrivial X, general sigma-finite intensity laws, full original-target coverage, and novelty/publication review. This report must not be used to close those gaps by relabeling the scoped result.

No failed check was suppressed or overwritten. No counterexample to the frozen theorem was found.
