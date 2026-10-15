# Single highest-impact follow-on: Dirichlet GRH through the quasi-RH machinery

Decision date: 2026-10-06, America/Los_Angeles. Source snapshot: `adc7f1241b42e322a6451854ab7e4b4c146bf78a` in `/Users/alec/Desktop/math`.

## Recommendation

Take on the **generalized Riemann hypothesis for Dirichlet L-functions, including classical RH**, by extending family 003's zero-free-region machinery toward the critical line. Conditional impact on the user's rubric: **10/10**. Research risk: extreme. This choice maximizes importance conditional on success; it is not the highest expected-value project or a claim that the remaining proof is straightforward.

The exact target is: for every primitive Dirichlet character χ, every zero ρ of L(s,χ) in 0<Re(ρ)<1 has Re(ρ)=1/2. An equivalent sufficient target, using the functional equations for the conjugation-closed family, is zero-freeness in Re(s)>1/2+ε for every ε>0. No claim about all automorphic L-functions is included.

The execution should retain the source's auxiliary family of all finite-order Hecke characters over Q(sqrt(-3)). The source explicitly explains that even its zeta consequence uses this family because Poisson transformation introduces twists. Discarding those twists to make a superficially simpler zeta-only proof would break the mechanism.

## Why this is newly worth attacking

The main input is the September 30 manuscript [The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s)>7/8](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf), not the October 5 alternate proof, whose conclusion is the weaker 11/12 threshold.

The new opportunity lies in the proof, not only its final theorem:

1. Its **continuation-from-a-common-signal proposition** permits any boundary σ₀ in (1/2,1). It compares one physical character sum with a Mellin integral involving Hη(s)/Lη(s). Holomorphy/nonvanishing of Hη and two positive power savings give a contradiction to zeros beyond σ₀. This analytic interface is already parameterized.
2. The paper actually performs **two different stages, 11/12 to 7/8**. The second changes the arithmetic probe through prime compensation, unequal averaging scales, and separate inverse/plain moment recursions. It is evidence of an adaptable construction, not a demonstrated indefinitely repeatable contraction.
3. Both the limiting domains and the local arithmetic errors are explicit. A research stream can identify precisely which estimate fails, modify that part of the construction, and test a quantitative new threshold.

The upstream theorem and pivotal proof remain inputs requiring validation. This selection did not independently reprove them or rebuild formalizations. [Clay's current RH page](https://www.claymath.org/millennium/riemann-hypothesis/) still lists the classical problem as unsolved; the upstream manuscript itself explicitly says it does not establish RH or GRH.

## The central obstruction, rather than a vague instruction to improve constants

The present local Euler-product, contour and principal-residue interfaces impose domains involving σ₀≥7/8. The ordinary continuation proposition does not remove these hypotheses.

There is a further concrete warning. The local proof bounds one Euler error by a term of order

`Q^(4−6σ−6z+θ)`.

At the principal residue z=1/6, this becomes `Q^(3−6σ+θ)`. Summing this absolute majorant over prime ideals requires σ>2/3 (with θ small). Consequently, even successful optimization past 7/8 cannot take this unchanged absolute estimate to 1/2. This is a limitation of the bound, not proof that the actual correction product has a singularity at 2/3 or that every version of the method fails there.

The substantive research question is whether higher-order prime compensation, an explicitly factored correction, or a different completed probe can remove the obstructing local contributions while preserving **all** of:

- the same character sum in the direct and Mellin comparisons;
- a holomorphic, nonvanishing target factor;
- a nonzero principal reciprocal signal;
- rigorous contour moves and all-height tail estimates;
- both moment bounds and positive exponent margins independent of the target character.

Fixed-character constants and lower scale thresholds are allowed to depend on that character, as in the source. Requiring uniform conductor constants would add an unnecessary stronger task. Conversely, character-dependent power savings are insufficient for the source's supremum-of-zero-locations argument.

No construction meeting these requirements down to 1/2 has been identified. Simply asserting a stronger moment estimate, reusing a lemma outside its proven domain, or assuming a contraction of zero-free boundaries is blocked as a route; each would relocate the central difficulty into an unsupported claim.

## First research order

**Gate 1 — make one strict improvement.** Extract every actual exponent, convergence, holomorphy, nonvanishing and contour-domain constraint into a dependency ledger. Recover 11/12 and 7/8 from the source. Then prove the complete continuation criterion at **7/8−δ for one explicit rational δ>0**, throughout the same Hecke-character family. A symbolic optimizer proposing parameters is only a diagnostic; every strengthened analytic premise must have a proof. A better intermediate estimate alone does not pass this gate.

**Gate 2 — expose or remove the local obstruction.** Compute the principal local factor and the exact coefficient responsible for the problematic error. Test a concrete second/higher-order compensation or refactorization. Establish the resulting holomorphic domain and nonvanishing without importing an equivalent zero-free claim as a premise. Produce either a verified new identity with usable estimates or a precise barrier for that attempted construction.

**Gate 3 — prove a family approaching the critical line.** Only after successful finite improvements, seek an actual sequence of validated thresholds σ_j decreasing to 1/2. Prove the recursions and all needed positive margins for each stage; do not infer indefinite iteration from one improvement. With the full family zero-free in every Re(s)>1/2+ε, the functional equations give the stated Dirichlet GRH conclusion.

Give the first gate and the proposed local correction to separate adversarial reviewers. A failed route should preserve its exact obstruction and be reopened only for a materially new identity or estimate. The objective is a mathematical breakthrough, not an accumulating list of conditional restatements of RH.

## Comparison that led to the choice

Six independent domain scans examined both the release and the first-batch work. The linked example [Zenodo 23203334](https://zenodo.org/records/23203334) was retrieved through the public API after the browser fetch failed; its title, DOI, scope and file list match the local multispecies Vlasov–Maxwell project. Its result concerns fixed finite positive-mass species on flat spacetime, not Yang–Mills or gravitating matter.

| Serious alternative | Conditional impact judgment | Why it did not win under this request |
|---|---:|---|
| NL not contained in L/poly, via polynomial-length versions of the new automata obstruction | 9.7–10 | A genuine new rank-amplification method exists, but its idempotent/minimum-rank constructions currently require unbounded word lengths; the needed localization may contain the entire separation problem. |
| Uniform gap from Laughlin V1 to physical LLL Coulomb at filling 1/3 | about 9.3 for the gap alone | Substantial new local stability machinery, but order-one long-range two-body interactions need a new screening/relative-bound argument. Broader fractional-response claims would add further targets. |
| One-ended vacuum-collapse strong cosmic censorship | about 9.3 | New Kerr obstruction plus horizon gluing is promising; regularity, genericity transfer and full-development extension exclusion remain separate gaps. |
| Full pointwise Furstenberg theorem for arbitrary transformations and all finite lengths | about 9.2 | A precise new selector/packing mechanism exists, but weak mixing gives weaker exceptional-pair control than the proof uses. |
| All-dimensional Kakeya or full Wall PD3 recognition | about 9.3–9.5 | Important new low-dimensional or hyperbolic inputs; no comparably explicit general induction/decomposition bridge was identified. |

Other misleading candidates were rejected: full Tate for finite-field abelian varieties is already included in source 032; recent primary preprints already claim KLS; naive Gaussian thermal-loss capacity formulas conflict with published non-Gaussian counterexamples; the forced Navier–Stokes computation result supplies no verified transfer to unforced blowup. These are priority/scope screens, not audits accepting every new preprint as correct.

## Audit and confidence

The arithmetic reviewer independently inspected the actual continuation theorem, both stages, local Euler identity and domain restrictions. A fresh cross-domain adversarial reviewer checked whether the connection justified the recommendation and accepted it **only with the strict-improvement gate above**. Its strongest objection—absence of any proven arbitrary-boundary contraction—is explicitly retained here.

Thus the conclusion is: **the highest-impact source-grounded research bet identified is Dirichlet GRH through a redesigned cubic-theta compensation/moment argument.** There is a concrete new starting point and a measurable first gate. There is not yet a complete route to the critical line, a success probability, a proof claim, or a guarantee of priority.

Evidence: [arithmetic assessment](agent_notes/arithmetic_geometry.md), [independent attack on the recommendation](agent_notes/quantum.md), [complexity comparison](agent_notes/complexity.md), [PDE comparison](agent_notes/pde.md), [analysis comparison](agent_notes/geometry_analysis.md), [topology comparison](agent_notes/topology_groups.md).
