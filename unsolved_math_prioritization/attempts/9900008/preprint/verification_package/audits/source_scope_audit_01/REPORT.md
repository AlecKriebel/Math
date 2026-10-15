# PR883 source/scope adversarial audit

Decision: **PASS for the source/scope gate and the exact negative implication proved in the frozen candidate.** No mathematical repair or scope correction is required for that bounded claim. This is not a publication, merge, priority, or global novelty decision.

Target: PR883, PID 9900008 / AMR-098-0008, frozen head `af25d26e21945a1a132aace5e600485152777070`. Author effort remains 1/5. This review added no central proof-search turn.

## 1. Independence, reading order, and evidence boundary

I first read Thorisson's actual §4 and the complete native target record, and then the Last–Thorisson (2009) setting, allocation definition, mass-stationarity definition, and §7. The initial batched read also displayed the complete native **prior literature/status report before the source contract**. That ordering error was immediately disclosed to the parent, which instructed continuation with explicit disclosure. This is therefore an independent source/scope audit with prior status exposure, **not a pristine blind reconstruction**. The prior report's verdict is not evidence for this decision.

`SOURCE_CONTRACT.md` was fixed before opening the author proof, current README/addendum, or old audits/acceptances. I then read the full author proof, historical author source audit, current README and credit addendum; checked the central primary antecedents; derived the allocation and mass-resampling checks below; and only afterward inspected old audit source/math/credit discussions. Old acceptance labels and historical execution claims are not premises. Some combined old-audit tool output was truncated; this audit does not claim a complete independent artifact/execution audit of those packages.

All writes were confined to `source_scope_audit_01/`. Source PDFs, text extracts, native records, and page renders remain private. The frozen source snapshot contains exactly 26 regular files totaling 211,771 bytes; every member still matches `SOURCE_MANIFEST.json` (SHA-256 `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`). No source script was executed. The native complete record/report pair was independently reserialized to the specified 5,255-byte canonical array and its hash matched `5ccf640125437cbff98966972b50bc5f73f19e1ae1735dff8a49829cfbcdc42a`; the statement UTF-8 hash matched `85140471a18e2a6974b1e984ead6f94e6954f1d619201d414dc8be50244c8c54`. No other PR or project chat was opened, including PR284. No external individual was contacted, and no GitHub, Zenodo, or sheet write occurred.

## 2. Exact source contract and page/formula map

The problem asks whether every diffuse pair passing all original-state preserving-allocation tests must be mass-stationary. A single admissible counterexample refutes that universal implication. The source does not require the counterexample to satisfy stronger tests using independent stationary spatial information.

| Primary source location | Operative content | Effect on the candidate |
|---|---|---|
| Thorisson, *Some Open Probability Problems*, printed p. 5, §4 setup | LCSC Abelian group; arbitrary random element in a G-space paired with a random measure | R² and a constant X with trivial action are allowed |
| Same, p. 5, Theorem 4.2 and (4.1), following displacement/allocation formula | Measurable π of the pair; τ_z(s)=s+π(θ_s z); τ pushes ξ to itself; test the law after the origin shift | The tested class is all such measurable pair-based allocations, without an injectivity requirement |
| Same, p. 6, Theorem 4.3 and Problem 4.1 | Diffuse R^d characterization with every independent stationary field; asks whether field can be omitted | Background-free and augmented-state premises are explicitly different |
| Same, p. 6, Theorem 4.4/(4.2), Problem 4.2 | Bounded weighted preserving kernels; separate Markov-kernel restriction problem | An allocation counterexample is not a negative answer to the Markov problem |
| Last–Thorisson (2009), reprint pp. 4–5, §2/(2.1)–(2.2) | Locally finite measures, evaluation σ-field, jointly measurable flow and flow-adapted ξ; Hausdorff LCSC Abelian G | The phase model meets the full measurable setting; nonstationarity of Q is permitted |
| Same, p. 8, (3.3), and p. 9, Example 3.4/(3.6) | All-state balancing; explicitly also defines a measure-a.e. variant; exact covariance for every state, s,t | The candidate handles either all-state or Q-a.e. preservation; spatial null sets cannot free the root under exact covariance |
| Same, pp. 17–18, (6.1), Definition 6.1/(6.2), Remark 6.2/(6.3) | Nonzero ξ; C relatively compact, positive Haar measure, Haar-null boundary; joint identity of (θ_V state,U+V) and (state,U) | The chosen unit square qualifies, its sampled mass is 3, and its first marginal already fails |
| Same, pp. 22–24, Example 7.1, Theorem 7.2, Problems 7.3/7.5/7.6 | Unequal-atom obstruction, weighted-kernel theorem, diffuse allocation question, stationary-background variant | The exact earlier analogue is Problem 7.5, not Problem 7.3 |

The Thorisson pp. 5–6 and 2009 pp. 9, 18, 24 were also visually inspected from local renders. The source's notation for the open-problem resampling identity is abbreviated; the full joint formula in 2009 removes any ambiguity. No raw page image is part of this public audit.

There is no source assumption of absolute continuity, positive intensity, full Haar support, full-dimensional support, finite total mass, nonperiodicity, freeness, or absence of invariant directions. On an LCSC Hausdorff group local finiteness gives the Radon/σ-finite setting used here. Diffuseness excludes atoms; it does not exclude line-length measures. These are properties of the actual source domain, not concessions inferred from an old audit.

## 3. Independent check of the model and allocation quantifier

Use the author's notation

    ν = Σ_n δ_n + 2Σ_n δ_(n+1/2),  μ = λ₁ ⊗ ν,
    Ω = R/Z,  θ_(a,b)u = u+b mod 1,  ξ(u)=θ_(0,u)μ,  Q=δ_0.

Take X constant. The group is the usual R². Every compact set fits in a bounded rectangle intersecting finitely many support lines, so μ is a nonzero locally finite Radon measure. Its countable line-length components are atomless: any positive-measure set has positive one-dimensional Lebesgue mass on a slice and can be split there. In particular every singleton has mass zero. The origin lies in supp μ; the model avoids the zero-measure and unsupported-root degeneracies.

The action is jointly continuous and ξ is flow-adapted with θ_tη(B)=η(B+t). For compactly supported continuous f, integrating horizontally reduces ∫f dξ(u) to a locally finite sum of continuous translates of a compactly supported continuous function of height. Thus u↦ξ(u) is vaguely continuous. Its density-1 line family distinguishes phase modulo one, so it is injective. The compact-circle orbit in the Hausdorff Radon-measure space is a Borel isomorphic copy of Ω. Hence σ(ξ)=B(Ω): the state has no latent random coordinate unavailable in the pair. Its exact translation stabilizer is R×Z.

Let π be **any** measurable displacement; no regularity, locality, injectivity, or invertibility is assumed. Write π(0)=(a₀,b₀) and π(1/2)=(a₁,b₁). Exact covariance, or equivalently the source's induced-allocation formula, gives

    τ_0(x,n) = (x+a₀,n+b₀),
    τ_0(x,n+1/2) = (x+a₁,n+1/2+b₁)

for every real x and integer n. These formulas are forced on all support lines. They exclude splitting one source line into pieces or using its integer index as extra observable information. Off-support values of π remain arbitrary.

Preservation at u=0 implies equality of the vertical line-weight measures. A direct, finite test on each segment [0,1)×{r}, r∈[0,1), yields

    1{[b₀]=r} + 2·1{[1/2+b₁]=r}
        = 1{r=0} + 2·1{r=1/2}.

Here brackets mean residues modulo one. This test is valid for arbitrary real displacements. It does not push an infinite measure onto a compact quotient. Positivity first excludes all other residues. A collision creates mass 3 at one target. A swap creates target weights 2 and 1. Neither equals the required 1 and 2. Only retention is possible, so b₀,b₁∈Z. Within each family n maps to n plus a fixed shift; two light lines cannot supply the same heavy line. This verifies the noninjective case instead of assuming it away.

Therefore π(0) belongs to R×Z, θ_{π(0)}0=0, and the **entire observed state**, including X, is unchanged. Since π was arbitrary, Q passes every original-state preserving-allocation test.

Only preservation at the Q-supported state 0 was needed, so Q-a.e. preservation does not enlarge the class enough to escape the argument. Conversely the resulting integer shifts preserve every phase: at phase u the support heights n−u and n+1/2−u still root respectively at phases 0 and 1/2. Thus the global/all-state convention also causes no obstruction. Identity supplies a preserving allocation, so the premise is nonvacuous.

The origin is a μ-null singleton, but its image cannot be modified independently. Altering π(0) alters the image of every point on every light line, including positive-mass horizontal segments. Thus no spatial-null-set loophole exists under the exact primary convention. A theory which specifies only an allocation equivalence class modulo spatial ξ-null sets and leaves its representative at the origin arbitrary is a different, underspecified test; it is not the source's definition.

There is also no canonical-space restriction hidden in Ω. Every allocation on the full canonical measure space restricts to one of the allocations handled above. In the reverse direction the compact orbit is Borel and invariant; a Borel displacement can be extended by zero off that orbit. It gives the identity off the orbit and preserves all measures there. The submitted phase-state example is consequently legitimate as a pair-state example, not an ambient-space trick.

## 4. Direct falsification of mass-stationarity

Take C=[0,1)² and U uniform on C independently of the deterministic μ. It is relatively compact, has Haar measure one, and has Haar-null boundary. For Haar-a.e. U, C−U contains the light line at height 0 and exactly one heavy line at height 1/2 or −1/2, each over a horizontal interval of length one. The total mass is 3. The conditional normalized μ-sample V therefore lies on a light line with probability 1/3 and a heavy line with probability 2/3.

The evaluation H(η)=η([0,1)×{0}) is measurable in the source's evaluation σ-field. It equals 1 under Q. Horizontal shifts do not matter; a heavy vertical shift brings a density-2 line to the origin. Thus

    Q[H(ξ)=2] = 0,
    P[H(θ_Vξ)=2] = 2/3.

The first marginals disagree, so the full required joint laws of (θ_Vξ,U+V) and (ξ,U) disagree. This is a valid disproof of the joint condition, not an attempt to prove mass-stationarity from marginal invariance. No fallback on a zero-mass window is used.

The optional stationary-phase Palm calculation is consistent: uniform phase is stationary, its intensity is 3, and its normalized Palm law has weights (1/3,2/3) on phases (0,1/2). The proof does not infer failure merely from comparison with one Palm law; the displayed measurable event already establishes failure independently.

## 5. Adversarial checks of the declared exclusions

The kernel distinction is substantive. On rooted phase v=u+s₂, define a Markov transport to send s to s+(0,1/2) when v=0; send half to s−(0,1/2) and retain half when v=1/2; and retain mass at other phases. This is a measurable invariant kernel. Every heavy target receives light mass 1 plus retained heavy mass 1; every light target receives heavy mass 1. It therefore preserves ξ at every phase. From Q's root it moves to phase 1/2 with probability one, so Q fails this Markov test. The candidate does not meet the all-Markov premise. Nothing here verifies a Cox-projected claim.

Adding an independent stationary field changes the state on which π may depend and can destroy its horizontal stabilizer. The proof cannot carry its two-value reduction over to that augmented class, and does not attempt to do so. Theorem 4.3/2015 Theorem 7 supplies precisely that stronger characterization. A constant X in the original problem is not a hidden license to add an arbitrary Y.

The model is singular and two-dimensional and has a horizontal invariant direction. These are admissible source features. The stronger positive-density/one-dimensional/no-invariant-direction questions are exclusions of the example, not qualifications silently imported into Problem 4.1. The support is not all R², though its affine/convex hull is all R²; a merely full-dimensional convex-hull requirement would not exclude it. A condition of not charging hyperplanes would exclude it.

## 6. Primary antecedents and current presentation

The central product-lift credit in the current `CREDIT_ADDENDUM.md` is accurate. Last–Thorisson, arXiv:1405.7566v2, §8, Proposition 1 (pp. 14–15) explicitly proves that adjoining a Lebesgue coordinate preserves and reflects mass-stationarity; its Theorem 8 (p. 15) uses that diffuse lift with independent stationary backgrounds. The submitted λ₁⊗ν is exactly such a lift after permuting coordinates. The lift is established machinery. Theorem 6 (pp. 9–10) concerns the stated strictly positive density field with line-integrability and infinite half-line-mass hypotheses; it does not cover this singular measure. Theorem 7 (pp. 12–13) retains backgrounds. The p. 16 discussion says the constructed weighted kernels are not Markovian. It cannot be used to identify the allocation and Markov questions.

Last–Thorisson (2009) Example 7.1 (pp. 22–23) already uses unequal atomic weights as an obstruction to deterministic allocations. Its particular Poisson construction uses an irrational relative weight to force class separation. The candidate's periodic (1,2) version obtains class separation through the two-family stabilizer calculation, not through the irrationality argument. That distinction is sound and is shown explicitly above. The credit addendum appropriately does not claim discovery of unequal-weight or product-lift mechanisms.

The later papers are consistent with, but unnecessary to prove, this exact counterexample. Last–Thorisson, arXiv:2112.13053, §8/Remark 8.1 (pp. 15–16), uses parallel-line diffuse measures and the lack of external randomization to obstruct **balancing two different measures**. Khezeli–Mellick, arXiv:2303.05137v2, Theorems 1.1–1.2 (pp. 2–3; definitions p. 4), imposes no-invariant-direction or related sufficient hypotheses for factor-point-process/balancing-allocation existence. This example has a horizontal invariant direction and assigns positive mass to its translates and to affine hyperplanes. It does not satisfy any of that theorem's four alternative sufficient conditions. Those theorems are not a positive solution to the unrestricted self-preserving-allocation question here.

The complete native prior report requires source corrections: the original note numbers this as 4.1, while 7.3/7.5/7.6 are in the 2009 paper; the 2015 introduction and p. 10 attribute the one-dimensional diffuse result to [15], *Unbiased shifts of Brownian motion*; and its broad statement that the higher-dimensional positive-density case remains open ignores the precise Theorem 6. These prior-report defects do not change the native target statement, which matches Problem 4.1. I have not independently verified the full one-dimensional theorem or that cited paper, because neither is used to establish this counterexample.

The current README makes the correct exact claim and carries the addendum. The unchanged historical proof/source audit/author README contain earlier presentation language, but the current presentation expressly preserves those bytes as historical and disclaims novelty/priority. No repair to the current credit presentation is required at this gate. Historical references to PR284 were not followed or independently certified in this review, in accordance with the strict skip instruction. The independent mathematical argument does not depend on them.

## 7. Strongest verified conclusion and remaining gap

The strongest verified result is an admissible deterministic diffuse Radon measure on R², with constant X and a jointly Borel canonical pair action, whose law is fixed under **every** source-defined measurable preserving allocation but fails the defining joint mass-stationarity identity by a measurable-event discrepancy of 2/3. This supplies a negative answer to the exact source implication; the adjective “source-scoped” does not hide a restriction absent from the primary question.

No mathematical or source-scope gap remains in that bounded claim. This family has not certified novelty, historical priority, exhaustive literature absence, current live-page status, final publisher-text identity, executable integrity/reproduction, or permission to merge/publish. The original author effort remains 1/5; none of those separate gates is silently promoted by this PASS.
