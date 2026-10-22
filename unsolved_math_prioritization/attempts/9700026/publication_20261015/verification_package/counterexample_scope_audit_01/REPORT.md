# Counterexample and scaling-scope audit of PR #880

Target: problem 9700026 / AMR-096-0026. Frozen original head: `fba74a301786f9648e48722e76f440097b0746c2`. Audit family: independent counterexample/scaling scope. Date: 15 October 2026.

## Decision and strongest verified result

**ACCEPT the unchanged author proof as a full negative answer to the literal unrestricted 2007 collapse clause and therefore to the catalog conjunction containing that clause.** There is no mathematical repair condition for this scope. The strongest verified theorem is that, for every finite collection of at least two distinct strictly interior sites and every positive initial probability vector, every global solution of the hard influence-cell ODE remains uniformly inside the positive simplex whenever `beta > 2 alpha > 0`. For the permitted pair `alpha=2, beta=8`, this contradicts the literal assertion that `alpha>1` forces a coordinate to tend to one.

This is an actual all-time counterexample mechanism. Ratio invariance alone would show an incompatibility between two conjectured clauses without identifying which failed. Here an independent geometric inequality and scalar integrating factor establish that the collapse clause itself fails, without assuming the convergence clause.

The rational witness has every weight in `[1/4096,2047/2048]` at every nonnegative time. An independently certified open box around its geometry, normalized initial state, and parameters has the common weaker all-time bounds `[1/8192,4095/4096]`. Thus no ordinary general-position exclusion of symmetry or a measure-zero exceptional set can save the stated universal collapse assertion.

No conclusion about convergence, uniqueness of a positive equilibrium, collapse for `beta<2alpha`, the critical boundary `beta=2alpha`, or the stochastic model with new city formation follows. The intended restricted research problems remain unresolved here. Novelty, exhaustive literature status, journal acceptance, human peer review, and formal proof-assistant verification are outside this verdict.

## Independence and exact inputs

Before opening author mathematics or inherited reviews, I read the 2007 primary model conventions on printed pages 2 and 7 and the complete associated-system page 40, read the entire 11-page 2012 paper text, and visually inspected the relevant primary model pages. I then wrote `INDEPENDENT_ATTACK_MEMO.md`, separating ratio invariance from a direct falsification and independently deriving a disk-based persistence inequality. The assignment disclosed the proposed parameter choice and claimed bounds; the memo does not claim blindness to those facts.

Only after saving that memo did I read the frozen author `PROOF.md`, certificate, checker, and source-scope claims. Independent exact arithmetic and the open perturbation certificate were completed before reading inherited audit A and review B. Those earlier reviews were then compared for disagreements; none affecting the accepted theorem or scope was found. Their verdicts were not premises of the independent argument.

The accepted author proof is 5,736 bytes, SHA256 `8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767`. The 40-file source manifest is SHA256 `b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b`; all 40 listed paths, lengths, and digests were independently checked successfully. The author certificate digest is `47c22a2bdded9ef999d02079ca782f92654218d9793bdeadaa7c0e19c9752ab3`, and checker digest is `ea32cb10ec774debeffd8ccfe2541fc833bb958f93650a56d8c16448b15cdf07`. Primary PDF fingerprints and new execution receipts are in `REPLAY_RECEIPTS.json`.

## Primary question and catalog mapping

The [25 April 2007 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf) permit all positive alpha and beta globally. Printed section 6.4, page 40, fixes finitely many city positions, uses nonnegative weights summing to one, and explicitly gives

`z_i' = area(S_i(z)) - z_i`,

where `S_i` consists of the points in the unit square at which city i maximizes `z_i^alpha |y-x_i|^(-beta)`. This is hard maximum allocation. It is not a normalized soft probability or an integral of influence divided by a sum of influences. The conjecture requires positive initial coordinates and describes positions and initial values as in general position, without defining that phrase. Its collapse hypothesis contains the disjunction `alpha>1 OR 0<beta<2alpha`; the second clause concerns positive, initial-value-independent limiting weights in `0<alpha<1, beta>2alpha`.

The [2012 paper, arXiv:1209.5120v1](https://arxiv.org/abs/1209.5120v1), instead restricts its stochastic model to `0<alpha<=1`. Its process allows new cities. Reading all 11 pages finds no statement or theorem of the frozen fixed-city ODE dichotomy. A deterministic-approximation remark and heuristic stochastic growth claims do not replace the 2007 ODE. The 2012 parameter convention cannot retroactively remove the explicitly permitted alpha>1 branch of the 2007 displayed conjecture.

After completing the independent argument I inspected the source family's private canonical exact record/report pair. Its 4,409-byte canonical SHA256 is `7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193`, the catalog review hash. Its exact target retains the full unrestricted conjunction, including alpha>1 alone as a collapse alternative. Thus the source-to-catalog logical implication is verified, rather than inferred from the title or a historical review summary. No copied dataset record or third-party source text is included in this audit's public manifest.

A universal conjunction is false when one of its constituent universal assertions has a counterexample. Consequently a full negative answer to this literal catalog target is warranted. That does not mean the remaining intended phase classification is complete. Any public summary must retain this distinction.

## Scaling alone: a consistency warning with a definite limitation

For positive weights and away from the finite set of sites, taking the positive beta-th root preserves influence ordering. City i beats j precisely when

`|y-x_i| <= (z_i/z_j)^q |y-x_j|`, where `q=alpha/beta`.

Hence the cells, their areas, and the entire vector field depend only on q. Simultaneously scaling alpha and beta changes neither the right-hand side nor the ODE clock. In particular `(alpha,beta)=(1/2,2)` and `(2,8)` have the same q=1/4 and exactly the same ODE. This invariance is specific to the hard-cell fixed-city equation; it does not imply invariance of the probabilities governing stochastic city formation.

The first parameter pair lies in the conjectured positive-limit regime and the second in the alpha>1 collapse regime. For at least two cities their proposed conclusions cannot both hold for the same initial state and geometry. This proves incompatibility of the two conjectured branches as a conjunction, but it does not identify the false branch unless one supplies additional mathematics. In particular, assuming the positive-limit clause in order to refute collapse would be circular. The direct inequality below supplies the missing evidence.

## Direct geometry, continuation, and all-time comparison

Fix distinct strictly interior sites. Let d>0 be their minimum pairwise distance and rho>0 their minimum distance to the boundary. Put `c=min(rho,d/2)`. For any positive simplex vector and any i, the disk of radius `c z_i^q` centered at x_i lies inside the unit square. Its points have distance at most `c z_i^q` from i, while any competitor has distance at least `d-c z_i^q >= d/2`. Because each competitor's weight is at most one, its reduced influence is at most `2/d`; city i's reduced influence is at least `1/c >= 2/d`. The disk is therefore contained in the actual winning cell, up to measure-zero site and tie conventions. This independently yields

`A_i(z) >= pi c^2 z_i^(2q)`.

The author uses an equally valid rational square version. Choose h_i>0 with its centered square inside the unit square and `8 h_i^2 <= |x_i-x_j|^2` for every competitor. The smaller square of halfwidth `h_i z_i^q` is inside the winning cell by the triangle inequality. Thus

`A_i(z) >= K_i z_i^p`, with `K_i=4h_i^2>0`, `p=2alpha/beta`.

This lower bound holds over the entire positive simplex, rather than only near an equilibrium or along a sampled numerical trajectory.

The ODE is well-defined independently of boundary tie conventions. A pairwise tie is the zero locus of the nonzero polynomial

`|y-x_i|^2 - lambda |y-x_j|^2`, `lambda=(z_i/z_j)^(2q)>0`.

For lambda not equal to one it has a nonzero quadratic part; at lambda=1 the distinct sites give a nonzero linear part. The tie is a circle or line of zero planar area. Almost every point has a unique winner, whose strict ordering persists for sufficiently small positive weight perturbations. Dominated convergence gives continuity of every cell area on the positive orthant, and the almost-everywhere partition gives `sum A_i=1` and `0<=A_i<=1`.

Peano existence therefore applies locally. Along every solution, `s=sum z_i` satisfies `s'=1-s`, so the simplex is preserved from s(0)=1. Also `z_i'>=-z_i` gives `z_i(t)>=e^(-t)z_i(0)>0` before any finite endpoint. On any finite interval the solution is confined to a compact subset of the positive simplex, with bounded derivative. A finite maximal endpoint would have a positive limit state from which local existence extends the solution, a contradiction. Every solution extends globally. Uniqueness is unnecessary for this refutation because every solution satisfies the same persistence estimate; no unsupported smooth dependence on the combinatorial type of the cells is assumed.

When beta>2alpha, 0<p<1. For `u_i=z_i^(1-p)`, differentiability and positivity give

`u_i' >= (1-p)(K_i-u_i)`.

An integrating factor yields the actual-time estimate

`z_i(t) >= [K_i+(z_i(0)^(1-p)-K_i) exp(-(1-p)t)]^(1/(1-p))`.

The bracket is a positive convex combination. In particular

`z_i(t) >= delta_i := min(z_i(0), K_i^(1/(1-p))) > 0`

for every t>=0, and `liminf z_i(t)>=K_i^(1/(1-p))`. Summing the other coordinates' bounds gives `z_i(t)<=1-sum_{j!=i}delta_j<1`. Neither bound depends on a finite integration horizon. The proof does not assert a limit exists.

## Exact asymmetric witness

The certificate uses three sites `(1/5,1/4)`, `(3/4,1/3)`, `(2/5,4/5)` and initial weights `(1/6,1/3,1/2)`. The weights are positive, distinct, normalized, and exceed 1/4096. The sites are strictly interior, distinct, noncollinear, and scalene:

| Quantity | Exact value |
| --- | --- |
| Squared distance 1,2 | 557/1800 |
| Squared distance 1,3 | 137/400 |
| Squared distance 2,3 | 49/144 |
| Signed triangle determinant | 343/1200 |
| Minimum boundary clearance | 1/5 |
| Minimum separation-squared slack over `8h^2` | 2003/7200 |

For common `h=1/16`, all boundary and separation inequalities have strict slack. With alpha=2, beta=8, `p=1/2`, `K=1/64`, and `K^(1/(1-p))=1/4096`. The theorem proves

`1/4096 <= z_i(t) <= 1-2/4096 = 2047/2048`

for all three coordinates at every t>=0. In particular no coordinate tends to one.

Noncollinearity or scaleneness alone does not certify an undefined, arbitrarily chosen genericity convention. The open-family check below provides the stronger relevant protection.

## Explicit robustness under open perturbations

Allow each city coordinate and each initial weight to change by less than `epsilon=1/10000`, intersecting the initial-state box with the affine hyperplane `sum z_i=1`. Independently allow

`199/100 < alpha < 201/100`, `799/100 < beta < 801/100`.

This is an open set in the relevant parameter, position, and simplex topology. Every site remains strictly interior, the original common h=1/16 remains admissible, every initial weight is positive, and no sites coincide. Exact componentwise distance enclosures are in `INDEPENDENT_EXACT_RESULTS.json`; their intervals are disjoint, so every triangle in this whole box remains scalene. The determinant remains at least `2677093/9375000>0`, so every triangle also remains noncollinear. The determinant error bound is `2epsilon(|v_1|+|v_2|+|w_1|+|w_2|)+8epsilon^2`, for original edge vectors v,w; this controls all cross terms, not only sampled vertices of the box.

The full parameter box satisfies alpha>1 and beta>2alpha. Its exponent p is at most `402/799 < 51/100`. Since 0<z_i<=1, the same square estimate gives `A_i>=K z_i^(51/100)` uniformly in the box. Let `L=1/8192=2^(-13)`. With K=2^(-6), the lower comparison field is positive at L because

`L^(1-51/100)=2^(-637/100) < 2^(-6)=K`.

Every perturbed initial weight exceeds L. The same scalar argument now proves, for every trajectory of every system in the open box,

`1/8192 <= z_i(t) <= 4095/4096` for all t>=0.

An exceptional symmetric equilibrium cannot explain this result. Even discarding any lower-dimensional set of positions or initial states leaves counterexamples. More generally the theorem works for every distinct interior geometry and every positive initial vector throughout the entire open parameter region alpha>1, beta>2alpha. An interpretation of general position that deleted this entire region would add a substantive missing parameter restriction, rather than an ordinary genericity qualification.

## Negative controls and precise remaining gap

The independent checker rejects zero initial weights, incorrect normalization, boundary sites, coinciding sites, one-city inputs, an intentionally collinear illustrative witness, incorrect bounds, and the alpha/beta parameter boundaries. These are controls on the advertised certificate and its chosen asymmetric illustration. They are not claims that collinear distinct interior sites violate the broader theorem; the geometric persistence theorem itself also covers them. A one-city system has z_1=1 and supplies no collapse counterexample. Zero initial weights and collisions destroy the particular positive/separated argument. Boundary sites can require truncated neighborhoods and are unnecessary for the exhibited interior counterexample.

At beta=2alpha the exponent p equals one; this integrating-factor transformation no longer gives a positive limiting lower bound. At beta<2alpha, p>1 and `K z^p-z` can be negative near zero. The lower inequality then does not establish persistence. Those controls demonstrate a limitation of this mechanism, not a proof of the conjectured collapse in those regimes. No convergence, unique equilibrium, or unique limiting state is inferred anywhere.

The exact remaining mathematical gap for the originally intended restricted classification is to establish or refute its convergence/initial-state-independence branch, and its beta<2alpha collapse branch, with appropriate precise genericity assumptions. No such gap remains for the narrower claim that the literal unrestricted collapse assertion, and hence its catalog conjunction, is false.

## Reproducibility, publication boundary, and workflow

`independent_exact_check.py` uses only standard-library rational arithmetic and does not import or execute the author checker. It validates the witness and perturbation box, and rejects 11 negative controls. Its normal and optimized outputs are identical. The original author checker was separately replayed successfully, including its optimized adversarial self-test. The independent controls and original samples are supporting arithmetic checks; analytic inequalities establish universal geometric inclusion and all-time behavior. No floating-point integration was used as proof.

All authored work is confined to this assigned audit directory. No author/source files, Git objects, branches, PRs, queue/sheet fields, candidate records, or Zenodo releases were changed. No individual, researcher, or other chat was contacted. Internal audit-team progress updates supplied coordination only. This audit does not initiate a priority campaign or public publication. The explicit `PUBLIC_MANIFEST.json` identifies only authored audit prose, code, mathematical derivations, decisions, and metadata. Downloaded PDFs, extracted source text, renders, and raw catalog/corpus records are excluded.
