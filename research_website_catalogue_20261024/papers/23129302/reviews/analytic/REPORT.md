# Independent analytic proof review — 23129302

## Disposition

**The review task is complete. The full original theorem is not independently cleared: a load-bearing imported source prerequisite remains unverified at the proof level.** The new open-map, probability-space contraction, backward transport and variation arguments withstand this review. They prove the claimed finite-preimage approximation for every central-basin density, without regularity restrictions. Completing the unconditional closure and common-boundary identities uses older global three-limit and boundary-seed facts on the entire prescribed parameter rectangle. The accessible older proof assumes a condition whose parameter verification is numerical, while the current supplement does not certify that condition.

This is a source-proof coverage gap, not a counterexample to the current theorem or to the older asserted result. An unconditional exact-range theorem is indeed printed in Keller's published OWR contribution; it is not merely metadata or a snippet. That contribution gives no independent proof of the disputed parameter verification. The final journal proof has not been obtained or compared. Its coverage therefore remains unknown. I do not infer that a rigorous verification exists nowhere.

The original target remains the full identity on all densities stated below. The conditional result is the strongest result this lane has verified, not a replacement theorem for promotion. No extended repair was attempted. Root retains the mathematical and publication decisions. No current sibling or root review was read.

## Inputs and independence

I read the entire actual six-page `sources/common_basin_boundaries.pdf`, all six rendered pages and the complete 18,361-byte published TeX. The exact source bindings are:

| Input | SHA-256 |
|---|---|
| 94,713-byte original PDF | `5c44dd3cc2cbdea38eb0da0c03bd42dd409ae78334ce47f3956f827caa0032cb` |
| 162,121-byte original verification ZIP | `1251fcb97b28cc15e72a65195757dd20029f5695f06e3d4de97d64077bd21005` |
| `published-source/basin-boundaries-verification/paper/common_basin_boundaries.tex` | `665ef241d04e22680416afcdbc734e7a1f74bd55fb8d8ea0ea65995c3792c982` |

The paper is **Common L1 basin boundaries for a bistable mean-field interval map**, version **1.0**, dated **3 October 2026**, an unrefereed preprint by Alec Kriebel. No source asset was edited, rebuilt or replaced.

The complete independent initial reconstruction was sealed at **2026-10-25T06:08:16.917009+00:00**, before reading historical support opinions or any current sibling/root opinion: `independent-initial-seal.json`, SHA-256 **702d6f420d16b1b07ee77488f12aa5108052b12f38de796dd16b31cb99ea6900**. That seal identified all steps of the full original target and explicitly left old theorem applicability to be checked. Later reading of submitted proof-support and checker files did not determine the initial reconstruction or serve as a fresh favorable verdict.

The full member/authority read ledger distinguishes complete readings, static program readings, parsed JSON structures, targeted search hits, and merely inventoried historical opinions. No submitted program was run, imported or compiled. All fresh mathematical controls are owned code under this review directory. The full initial source baseline is rehashed at the final checkpoint.

## Exact target and the load-bearing source interface

Let `I=[−1/2,1/2]` and `D={u∈L1(I):u≥0 a.e., ∫u=1}`, with its **relative L1 topology**. For `0<A≤2/5`, `6<B≤16`, put `G(m)=A tanh(Bm/A)`, `φ(u)=∫xu(x)dx`,

`f_r(x)=((r+4)x+r+1)/(2rx+2)`,

`T_r(x)=f_r(x)` to the left of `−r/4`, and `f_r(x)−1` to its right. Let `F(u)=P_(G(φ(u)))u`. The target is

`W = closure_D(⋃_(n≥0) F^(−n)({1})) = ∂_D B+ = ∂_D B−`,

where `W={u:F^n u→1 in L1}` and `B±` are the noncentral fixed-density basins. No boundedness, BV, positive lower bound or L2-density assumption is allowed. The finite-preimage closure is part of the original target, not an optional corollary.

The following distinctions are decisive:

| Actual source evidence | What is established in the inspected body | What it does not certify |
|---|---|---|
| BKZ arXiv `0812.4040v1`, actual 36-page body, Theorem 2, pp.7–8 | The global theorem is stated **assuming I and II**. Example 1 asserts that tanh feedback up to `A≤0.4, B≤18` satisfies the results. | Example 1's assertion is not itself an all-parameter certificate for II. |
| BKZ author-hosted actual manuscript, dated 19 December 2008, corresponding theorem and Appendix A.2 | The same conditional theorem and asserted example occur. Appendix A.2, pp.34–35, motivates the bounds on `ψ(r)=φ(u_r)` and `ψ″/(ψ′)^2` with numerical evidence and says the tanh check can be done numerically. | Neither body supplies a rigorous interval enclosure, remainder estimate or exact continuous certificate for this verification. The author body is not authenticated as the final journal proof. |
| Keller's complete contribution, OWR49/2009, printed pp.2713–2715 | Theorem 2 on p.2714 explicitly and unconditionally states the all-D trichotomy and openness for `0<A≤0.4, 6<B≤16`; the next page states the common-boundary conjecture. This is an actual published theorem statement. | The short contribution reports the earlier work and does not prove the missing S-shape/parameter step. Its unconditional wording does not supply a new proof certificate. |
| Fresh ordinary Springer journal article/PDF routes | Both return the subscription preview; the PDF route does not yield a PDF. | The final CMP proof was not read, so possible repairs or different hypotheses there are unknown. |
| Current paper and relevant full mathematical support/checkers | They prove inverse contraction, distortion, fiber sections, and rough-density controls, and exact bounds for source Assumption I. | No exact all-parameter certificate for source Assumption II, or a sufficient weaker fixed-point dichotomy, was found. The old and new contraction certificates are about different quantities. |

Source Assumption I is `G′(m)≤25−50|G(m)|`. It does have a direct exact margin here: if `a=|r|`, the feedback relation gives `G′≤16−100a²`, and

`(25−50a)−(16−100a²)=100(a−1/4)²+11/4>0`.

The actual primary routes are [BKZ v1](https://arxiv.org/pdf/0812.4040v1), the [author manuscript](https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf), [Keller's published OWR volume](https://ems.press/content/serial-article-files/46250), and the [journal subscription preview](https://link.springer.com/article/10.1007/s00220-009-0854-9). Raw bodies, exact read extents and response identities are bound in the ledger.

Source Assumption II is S-shapedness of `H(r)=G(φ(u_r))`; the source says it uses this through the stable/bistable fixed-point dichotomy. This is not the rank-one inverse estimate. The displayed polynomial and Bernstein certificates in the current supplement control inverse norms as functions of `a=|r|`; they contain no certified `ψ`, `ψ′`, `ψ″` or composition-concavity enclosure. Finite feedback or Gram-matrix tests cannot supply II. The two inspected exact algebra JSON certificates were read in full, their code was read completely, all mathematical checker families were inspected statically, and all 31 support JSON documents were parsed and structurally inventoried. Targeted source-wide searches identified the stated generic source hypotheses, but no additional II certificate. This is a bounded inspection of this complete submitted package, not an absence claim about all literature.

I read the complete relevant BKZ Proposition 3 proof of global convergence/openness and Proposition 4 proof of boundary contact, including their supporting discussion in pp.23–30. Their hypotheses and dependence on the earlier dynamical classification are not removed by the current paper. At the seed `1=w_0`, the old compact analytic class does suffice to give a full-D boundary seed; it need not be dense. The uncertainty is the parameter verification underlying the imported classification, not a mistaken extension of core density.

Therefore the exact remaining obligation is one of: authenticate and inspect a rigorous final-source proof that supplies these global facts for the whole rectangle; supply a rigorous continuous verification of the source condition or sufficient weaker dichotomy; or explicitly treat the needed global facts as assumptions. The last choice would change the original unconditional claim and is not adopted here. Merely citing the unconditional OWR announcement while claiming its proof coverage has been checked is insufficient for this review's verification standard.

## Analytic reconstruction: openness and topology

The factorization `T_r=T_0∘h_r`, with `h_r(x)=(x+r/4)/(1+rx)`, is exact away from null cut choices. Each `h_r` is an increasing smooth interval bijection fixing endpoints, with inverse `h_(−r)`. Its density pushforward `Q_r` is a signed-L1 isometry. Joint strong continuity follows for continuous functions by smooth inverse Jacobians and for L1 functions by approximation and isometry. Consequently the moving cut causes no hidden continuity assumption on the density.

For `K(u)=Q_(G(φ(u)))u`, solve `r=G(∫h_(−r)v)` to invert K. The scalar residual increases by at least the parameter increment, because `∂_r h_(−r)=(x²−1/4)/(1−rx)²≤0`, and has opposite signs at `±A`. Its root is unique and changes by at most `(B/2)||v−w||1`. The inverse `Q_(−ρ(v))v` is continuous; checking the mean proves it is a two-sided inverse. This establishes a homeomorphism on **all D**, without differentiating a nonlinear L1 map.

For `v=P0w`, the positive section uses `q(x)=w(x)/v(T0x)` on nonzero fibers and `q=1` on zero fibers. Nonnegativity forces both old branch values to vanish on a zero fiber. Thus `0≤q≤2`, `P0q=1`, and `R_w(z)=q·z∘T0` is a positive exact section with `R_w(v)=w` and `||R_w(z)−w||1=||z−v||1`. The value assigned on zero fibers is essential when z puts new mass there. This proves P0 is relatively open and onto, hence F is continuous, open and onto.

For an **open** basin B with `F^(−1)B=B`, continuity maps its boundary into itself: boundary points are outside B and in its closure. Conversely an open image of every neighborhood of a point above the boundary meets B, so complete invariance pulls the boundary back. Thus `F^(−1)(∂_D B)=∂_D B`. This part correctly uses relative topology and basin openness; the latter is one of the imported facts for the eventual application.

## Analytic reconstruction: probability-space inverse contraction

For every `|r|≤2/5`, the lifted inverse `b_r(z)=(2z−r−1)/(r+4−2rz)` maps `J=[−1/2,3/2]` bijectively onto I. Its derivative in r is `−(1−4b_r²)/(4−r²)≤0`. For any bounded J-valued random variable Z on any probability space, the root `r=G(E b_r(Z))` is unique by the same residual argument. Endpoints of J are allowed. This does not require the probability space to have a density.

Along a convex bounded path `Z_t`, implicit differentiation is legitimate for each fixed `A>0`: the rational inverse and all needed derivatives are bounded on the compact rectangle, and the residual derivative is at least 1. The path may be differentiated under expectation. It is not necessary to assert Fréchet differentiability on an unrestricted L2 neighborhood. With `X=V(Z_t)`, `q=1−4X²∈[0,1]`, `β=G′(EX)/(4−r²)` and D multiplication by `f′_r(X)`, differentiation gives

`dot X = (Id−βqE/(1+βEq)) D^(−1) dot Z`.

Write `m=Eq` and `s=Eq²`; then `m²≤s≤m`. On the span of1 and centered q, the rank-one factor has the stated triangular 2×2 matrix, and is identity on its orthogonal complement. Setting `C=1+β/4`, the lower minor of `CId−L*L` is `β/4`; the determinant is

`β²[(Cm−1/4)²+C(m−s)]/(1+βm)²≥0`.

For `β>0` this implies positive semidefiniteness. For `β=0`, it is the identity. If q is constant, constants are contracted by `1/(1+βm)` and the remaining space is unchanged; if the probability space has dimension 1, the absent orthogonal complement causes no issue. Thus all degenerate cases omitted from the generic 2×2 basis are covered.

The feedback identity yields `0≤g=B(1−r²/A²)≤16−100a²`, `a=|r|`, and `||D^(−1)||≤(2+a)/(2(2−a))`. The resulting squared bound is

`U(a)=(2+a)(4−13a²)/(2(2−a)³)<7/10` for `0≤a≤2/5`.

The proof is continuous on the entire closed interval, since

`7(2−a)³−5(2+a)(4−13a²)=172(a−13/43)²+12/43+58a³>0`.

All denominators are positive there, and `7/10<(21/25)²`. Integrating the path derivative therefore proves the uniform contraction `||V(Z)−V(Z′)||2≤(21/25)||Z−Z′||2`. No sample or source decimal expansion estimate is used in this proof. Small positive A causes no gap: differentiation is justified separately for each A, while the final first-derivative bound is uniform. The excluded `A=0` is never substituted. Endpoints `A=2/5` and `B=16` are included; `B=6` is excluded from the basin statement.

## Analytic reconstruction: terminal transport and self-consistent lifting

Fix any `u∈W` on the probability space `(I,u dx)`. The coordinates `X_j` are bounded even when u is unbounded or not in L2. Each nonlinear orbit law `u_j dx` is absolutely continuous. The CDF transport `H_n(y)=−1/2+∫_(−1/2)^y u_n` is absolutely continuous, nondecreasing, onto and endpoint-fixing, with displacement at most `ε=||u_n−1||1`. Since the law is atomless, the probability-integral transform sends `X_n` to uniform `Y_n`, including when the CDF has flats.

Keep the original branch labels `a_j`. Define backward `Y_j=V(Y_(j+1)+a_j)`, with `ρ_j=G(EY_j)`. The input remains J-valued. On each branch event the later sublaw is dominated by the total absolutely continuous law; pushing it through a smooth inverse branch preserves absolute continuity. Induction therefore gives densities for every Y_j. Interior points of the later interval map into the indicated branch, while endpoints and cuts are null for these laws. Hence `T_(ρ_j)Y_j=Y_(j+1)` almost surely. The parameters are the actual feedback of these laws, not an external shadow. No independence between labels and coordinates is used.

Uniqueness of the scalar inverse also writes the old coordinates through V. The common old labels cancel in the difference of inputs. Thus the contraction gives `||Y_j−X_j||2≤κ^(n−j)ε`, `Δ_j=|ρ_j−r_j|≤16κ^(n−j)ε`, and `Σ_(j<n)Δ_j≤84ε`, where `κ=21/25`. These L2 norms are on a probability space of coordinates, not on a space of densities. The law `v_n dx` of Y0 satisfies **exactly** `F^n v_n=1`.

The deterministic transports use the old branch at each argument: `H_j(x)=b_(ρ_j)(H_(j+1)(T_(r_j)x)+a_j(x))`. Since both endpoint limits inside the old cut equal 1/2 after the branch offset, they glue at the new cut `−ρ_j/4`. All H_j are continuous, nondecreasing, onto and endpoint-fixing. They can have flats. Absolute continuity follows branchwise from a smooth bi-Lipschitz inner map, an absolutely continuous later map and a smooth Lipschitz outer inverse, followed by finite continuous gluing. The proof does not use the false general rule that arbitrary compositions of absolutely continuous maps are absolutely continuous.

## Analytic reconstruction: distortion and full variation convergence

The elementary uniform sensitivities are correct: inverse spatial derivative at most 3/4, inverse parameter sensitivity at most 25/96, and logarithmic forward sensitivities at most 1 and 35/24. They imply

`d0≤183ε/8`, `Σ_(j<n)d_j≤181ε/2`, and `|log R_n|≤213ε`.

The constants follow exactly from the geometric parameter sum. On each finite old cylinder, the old composition is smooth bi-Lipschitz onto its image. It therefore pulls derivative-exceptional null sets back to null sets. The resulting almost-everywhere chain rule is legitimate for merely integrable terminal u_n and gives `H0′(x)=u_n(X_n(x))R_n(x)`. It divides by no density. Zero sets and unbounded terminal values introduce no division or L2 requirement.

A crucial measure distinction is respected: this derivative is integrated against **Lebesgue measure**, not `u dx`. For the fixed old parameter sequence, `c_n=P_(r_(n−1))…P_(r0)1≤2`. The convex-family identity for `w_y=(1−y²/4)/(1−xy)²`, `|y|≤2/3`, follows from exact branch substitution. Its weights stay nonnegative and its two new parameters stay in the same interval, so the kernel family bounds 1/2 and 2 propagate from `w0=1`. This is valid for every external parameter sequence in the rectangle; it does not falsely call that sequence a new nonlinear orbit. Transfer duality and monotone truncation yield `∫|u_n(X_n)−1|dx≤2ε`, hence

`||H0′−1||1≤2ε exp(213ε)+exp(213ε)−1`.

For every absolutely continuous nondecreasing onto H, including flats, `H_*(H′dx)=dx` follows by the fundamental theorem of calculus applied to antiderivatives of continuous tests. Pushforward contracts the **full** variation norm. Therefore

`||H_*(g dx)−g dx||TV≤ω_g(||H−id||∞)+||g||∞||H′−1||1`

for continuous g. This remains a measure inequality even if `H_*(g dx)` has atoms; no unjustified density assumption is imposed on that intermediate measure. The actual corrected law `H0_*(u dx)` is already absolutely continuous by backward induction. Approximating the fixed u by continuous g, first sending n to infinity and then the approximation error to zero, proves `||v_n−u||1→0`. No attraction rate is assumed.

Thus **for every u in W, finite preimages of1 approach u in L1**. This is a valid full-density analytic conclusion on the stated rectangle, independently of the disputed older classification. Every finite preimage also belongs to W. However, asserting that the closure of those preimages lies in W additionally uses closedness of W, supplied here through the imported exhaustive trichotomy and open noncentral basins.

If the imported global facts and boundary seed are granted on the whole rectangle, W is closed; open boundary pullback places every finite preimage in both boundaries; closedness passes this inclusion to W; and the exhaustive partition into W and two disjoint open stable basins gives the reverse inclusion. This completes the original theorem **conditionally on that source interface**. The argument does not use the older L1-hyperbolicity discussion or a nonlinear differentiable stable-manifold theorem.

## Independent controls and their limits

`check_exact.py` uses SymPy1.14.0 and standard-library fractions, importing no submitted checker. Its32 controls include exact inverse/conjugacy/sensitivity identities, the rank-one determinant, the positive polynomial, all distortion arithmetic, both normalized branch identities, continuous invariant-range certificates using proved monotonicity, positive fiber sections with zero fibers, and an exact unbounded non-L2 symmetric density with a whole zero interval. These support the proof; their finite count is not an infinite-dimensional proof.

`check_probability.py` independently exercises 288 weighted probability-space inverse pairs, including one-point spaces, heavily correlated common labels, `A=0.4,0.001,10^(−12)` and `B` just above6 or equal16. All 2376 checked branch assignments were legal. The maximum observed squared contraction ratio was about 0.559063 and maximum feedback residual below4.72×10^(−16). An exogenous-zero-feedback negative control is rejected with residual about−0.4. These floating experiments are corroboration, not interval certificates or source Assumption-II verification. Exact rational CDF interval controls cover364 target intervals with flat source pieces, and a deterministic flat backward gluing example is checked.

The first owned symbolic run spent too long simplifying the sum of two rational branch expressions and was terminated as a process group after about 30 seconds. Splitting the identity into its two exact normalized branch identities removed this computation issue. The final owned runs completed successfully under 45-second timeout wrappers with process-group termination/escalation on timeout. No mathematical assertion was relaxed and no submitted program ran. No source programs, virtual environment or dependency installation were created.

## Final finding and handoff

There is **no demonstrated defect in the new analytic construction**. The exact all-density approximation mechanism is substantiated, including unbounded densities, zero fibers, CDF flats, moving cuts and every degenerate rank-one case. The full original unconditional theorem is nevertheless **not independently verified in this lane**, because the old full-range classification/seed interface lacks an inspected rigorous parameter certificate. OWR's exact unconditional theorem statement and BKZ's conditional proof coverage must remain separate facts.

`verdict.json` records `CONDITIONAL_ANALYTIC_CORE_VERIFIED_SOURCE_PREREQUISITE_OPEN`, false full-original-theorem clearance and false publication clearance. It preserves the whole original target and exact remaining gap. `read-ledger.json` records all actual extents and unknown final-journal proof status. `custody-before-after.json` binds all initial source files unchanged. `SEAL.json` and its SHA-256 manifest bind this handoff.

This task changed only `reviews/analytic/`. It did not modify sources, historical or sibling reviews, shared scripts, site/configuration/native Sheet/Git/release/UI state, or the prior Langlands scope seal. No individual was contacted and no outreach prepared. Completion is 100% of this bounded analytic review task, with no claim that the paper or the overall programme is cleared.
