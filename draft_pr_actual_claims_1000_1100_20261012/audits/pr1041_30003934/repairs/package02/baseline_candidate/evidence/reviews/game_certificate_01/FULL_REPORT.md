# Fresh independent game, penalty, and membership review

Review date: 2026-10-13 UTC. Input PR 1041, problem 30003934, submitted head `ad138ddd5bd1a51c0f225f03342c0c058873f790`. All 11 files matched `SUBMITTED_PINS.json` on initial capture; final recheck is recorded separately. The complete submitted `PROOF.md` and `certificates/LEMMA_REPORT.md` were read. No original manuscript, Git index, branch, queue, PR, external service, or other worker's files were modified. No outreach occurred.

**Assigned-scope verdict: PASS for the downstream game/penalty construction and the rational membership proof, conditional on the source-flow interface. No mathematical blocker was found in the assigned scope.** This is not a verdict that the DS source interface has been independently established by this family, nor a global novelty or publication determination.

`DERIVATION.md` records the independent deductions before the old audit and acceptance were read. The derivation and first exact run preceded those reads. The old verdicts were subsequently compared for consistency, not used as a proof premise. Completion toward this family's review goal: 100%; overall discovery completion is not estimated by this family.

## Exact conditional dependency

The needed interface is a polynomially encoded DAG with positive rational costs, positive capacities, maximum flow F, and a zero-e maximum flow. For every real q in [0,F], the optimum must exist. No PARTITION instance: every optimum has e-flow zero. Yes instance: an optimum has e-flow 1/2 at q<=F-3/2. The submitted perturbation must establish these properties for its actual costs; a selected original SSP execution alone is insufficient. All deductions below are conditional exactly on that interface, and would fail if its all-optimal no quantifier were replaced by an existential one.

There is no circular use of the game theorem to certify the network. The original optimizer's uniqueness is stronger than what the downstream no proof needs: retaining one original optimum gives equality of restricted/original values; **all** restricted optima are then original optima, and the interface's universal no property excludes e-flow 1/2.

## Obligation table

| Submitted locator | Adversarial issue | Independent conclusion |
|---|---|---|
| PROOF.md §2, line38 | Affine versus linear h; simplex slack multiplicity | h=F sum(nonzero coordinates). Inverse map is unique; no slack-coordinate continuum represents the same (f,h). |
| §2 | q may become negative at infeasible simplex points | q coefficient is 0 at x0, F at star/non-e, F/2 at e. Thus q>=h/2, and q>0 away from x0, even before conservation/capacity feasibility. |
| §2 | Feasibility at every real lambda including endpoints | Scale zero-e max flow by lambda/F. DAG path decomposition gives sum f<=Lq<=Lh. Works for the entire closed [0,F]. |
| §2 / §6 | YES witness clipped by h<=F or lambda<=F-eps | eps=1/(4L)<=1/4. q<=F-3/2 gives h=q+eps<F and q<=F-eps. |
| PROOF.md §3, line65 | Dual signs and optimal vertex existence for all real parameters | Correct dual; nonempty and pointed. The attained optimal face is pointed, hence has a vertex, which is a whole-polyhedron vertex. No genericity required. |
| §3 | Uniform mu bound may depend on lambda or denominator of an irrational lambda | Lambda appears only in the objective. The rational feasible polyhedron is fixed. A common integer coefficient clearing and Cramer bound apply uniformly to every selectable optimal vertex. |
| §3 | Existence of a feasible minimizer versus **all** minimizers | phi(x)>=opt+(M-C)delta with M=C+1. Every infeasible x is strictly worse. This proves equality of the entire minimizer set and the original optimum set. |
| §3 / §7 | Huge numerical M conceals exponential encoding | log M<=O(k log k+k log H0). Clearing polynomially many polynomial-bit denominators preserves polynomial size. M is computed directly; dual vertices are not enumerated. |
| PROOF.md §4, line84 | Min/max or b sign error | A_lambda=-G-lambda b, with b=-Ms, gives row payoff `-c-M(Rx-r-slambda)` at each column. Row minimax is exactly min phi. |
| §4 | Rank only at most one | Parameter equality supplies b entries +M and -M; a0=-eps<0. Both factors are nonzero, so exact rank one. |
| §4 | Correspondence loses boundary supports or degenerate y | At a^T x=lambda all column expected payoffs agree; each row payoff shifts by the same scalar. This preserves complete best-response sets both ways, without support hypotheses. |
| PROOF.md §5, line106 | Extra negative-lambda crossings or optimal slack rows | Costs are nonnegative and q>0 away from x0. x0 is the unique row optimum at every negative parameter; hyperplane forces -eps. |
| §5 | Row uniqueness confused with pair uniqueness | At -eps the single q-lambda column strictly beats all other columns at x0; the original pair is strict for both players. All opposing strategies are therefore its pure column. |
| PROOF.md §6, line114 | Endpoint lambda0, upper tail, extra opposing strategies | All candidate lambda lie in [-eps,F-eps]. At lambda>=0 exactness forces q=lambda and fe=1/2. At 0 the only DAG zero-value flow is zero. No upper tail lies outside the penalty lemma's interval. |
| §6 | Continuum or duplicate equilibria in no cases | Every possible pair passes through the full auxiliary correspondence; all candidate row minimizers have been controlled. Degenerate y cannot rescue a missing crossing. At the sole crossing y is unique. |
| §7, line126 | Output dimensions and omitted conservation redundancy | m=p+2=8n+9; columns=p+2V+3=16n+22. Redundant conservation inequalities remain harmless for pointed dual and coefficient bounds. |
| LEMMA_REPORT.md §1, line15 | Closed support cells include zero coordinates | Every product member remains a best-response pair. Actual supports supply the reverse inclusion. Closed cells add no false equilibria. |
| §2, line37 | Vertices unavailable in lower-dimensional/degenerate cells | Active normals span ambient space at a vertex, including implicit equality normals. Hadamard/Cramer bounds both numerator and denominator polynomially. |
| §2 | Irrational or positive-dimensional witnesses lack rational certificates | A nonsingleton finite union of compact product polytopes must contain two distinct cell vertex pairs. Their supports can shrink; they still are equilibria and satisfy the same bit bound. |
| §3, line64 | Verifier only necessary, duplicate witnesses accepted | Nonnegative unit vectors and all pure payoffs <=average payoff are necessary and sufficient. A distinct-coordinate test rejects duplicate pairs. All arithmetic is exact and polynomial. |
| §3, line84 | Ordinary language versus rank promise | Rank-invalid complement branch is polynomial-time; rank-valid nonsingleton branch has two-pair NP certificates. Thus ordinary rank-one UNIQUENESS is in coNP. |
| §3 | Existence silently assumed | Finite-game existence holds by the gain-renormalization Brouwer argument recorded in DERIVATION.md. Hence “at most one” and “exactly one” coincide. |
| §§5–6 | Fixed fiber/support uniqueness promoted to a global LP | The fiber formulation and its compactness are valid; the submitted example has three singleton fibers and a nonmonotone residual. No global-LP inference is made. |

The determinant bound is valid with arbitrary redundancy: every dual vertex is defined by enough independent active equations, and the integer determinant's absolute value is at least one. It is not necessary for an optimal face to be a singleton. The reduction's source input can be restricted to nonempty positive-weight PARTITION, retaining NP-completeness; an empty list would otherwise require a trivial fixed yes-output because S=0 makes normalization undefined.

## Fresh computations and deliberate controls

Command from the repository root:

```sh
python3 draft_pr_actual_claims_1000_1100_20261012/audits/pr1041_30003934/reviews/game_certificate_01/check_exact.py
```

The script uses only Python's standard library and `fractions.Fraction`; no floating-point LP solver, submitted verifier, imported submitted fixture, or original test output is used. It builds complete payoff matrices using the same permitted unspecified arc enumeration, a computed topological order, and the stated ternary perturbation. The common denominator clearing uses an lcm, a valid instance of the manuscript's Q choice. It computes the stated determinant-bound M rather than a convenient empirical penalty.

Exact residual shortest-path potentials give a candidate network dual. The script independently checks its lifted simplex-dual feasibility, complementary slackness, and primal/dual equality. It forms a legal auxiliary column distribution from mu/M with remaining mass on the baseline column and then checks the actual whole-game best-response inequalities. This is stronger than merely checking a flow or the rank identity.

| Weights | PARTITION | Game dimensions | M bits | Exact auxiliary pairs checked | Additional original-pair parameters checked |
|---|---|---|---:|---:|---|
| [1] | no | 17 x 38 | 1538 | 12 | none |
| [1,1] | yes | 25 x 54 | 3240 | 24 | 5/2, 7/2, 9/2, 11/2 |
| [1,2] | no | 25 x 54 | 3272 | 24 | none |
| [1,2,3] | yes | 33 x 70 | 5348 | 48 | 13/2, 15/2, 17/2, 19/2 |
| [1,2,4] | no | 33 x 70 | 5364 | 48 | none |
| [2,2,2] | no | 33 x 70 | 5278 | 48 | none |

All six strict pure default pairs pass. All 204 auxiliary pair checks, at integral endpoints and half-step values, pass exact rational inequalities. The tested no instances' SSP segments have zero e-flow. There are 480 exact vertex comparisons across three negative parameters per game, with a unique diagnostic column at x0. Every matrix's outer-product identity and nonzero factors are checked.

The following controls are executed, not hypothetical:

- Reversing the outer-product sign in B rejects the positive witness in each tested yes game.
- Substituting the baseline column for the known default column rejects all six default pairs.
- Setting M=0 gives an infeasible zero-flow improvement at lambda=F in all six games, demonstrating why an encoded exact bound is needed.
- A one-dimensional penalty toy with multiplier norm 1 has an infeasible minimizer tie at M=1, and strict exactness at M=2. This specifically tests the **all** minimizers requirement and strict `M>C` choice.
- The exact 2 by 2 example accepts its three equilibria and rejects the uniform midpoint.
- The two-pair certificate accepts distinct pairs and rejects duplicate pairs, nonunit vectors, and negative probabilities; rank-zero and rank-two inputs are recognized as invalid for the rank-one language.
- Rational endpoint witnesses certify a rank-one full-simplex continuum and a 1 by 2 continuum. The proof, rather than numerical sampling of irrational coordinates, handles irrational initial witnesses.

`EXACT_RESULTS.json` records the actual results and source-code hash. `EXACT_STDOUT.json` captures stdout from the final run. These tests do not enumerate every equilibrium of the tested games and do not establish the all-instance network interface. There is no claim that source SSP experiments certify that interface. The original theoretical edition contains no executable, fixtures, or computation logs in its 11-file manifest; the old statements about six games and 39 networks were **not replayed or simulated**.

## Fresh primary-source checks

The raw primary PDFs were freshly downloaded to `sources/rawprivate`, with URL, UTC retrieval time, byte count, and SHA-256 in `SOURCES.json`. All three byte identities match the corresponding submitted `SOURCE_PROVENANCE.json` records. Text extraction was used to read complete relevant bodies; PNG review checked arXiv printed p.8 and OWR printed p.2332. Raw PDFs, extracted text, and rendered page images are private and ignored by Git in this review folder.

[Adsul et al., arXiv:1812.04611v4](https://arxiv.org/pdf/1812.04611v4), revised 22 December 2019, has 39 pages. The inspected bodies include Lemmas 1/3/4/6, Theorem 7 (printed p.8), Theorem 19 and proof (pp.21–22), Section 6/Theorem 20 (pp.22–24), Theorem 21 and proof (p.29), and the second-equilibrium discussion (p.36). Theorem 7 agrees with the independently derived full correspondence; Theorem 19 finds one equilibrium and does not certify uniqueness. Degenerate equilibrium subsets are explicitly treated. The displayed 2 by 2 example is the n=2,p=3 case of Theorem 21 divided by 9.

The [published journal article](https://doi.org/10.1287/opre.2020.1981) is *Operations Research* 69(2), 613–631, March–April 2021, DOI 10.1287/opre.2020.1981; published online 4 June 2020. Its numbering differs: arXiv Theorems 7/19/20/21 correspond to journal Theorems 1/4/5/6. The published PDF's printed p.616 was read for the correspondence. Its Theorem 7 is a different structure theorem; citations must retain the version distinction.

The [EMS report metadata](https://ems.press/journals/owr/articles/16413) identify report 38/2018, *Oberwolfach Reports* 15(3), 2303–2384, DOI 10.4171/OWR/2018/38; workshop 19–25 August 2018, published 27 August 2019. The [primary PDF](https://ems.press/content/serial-article-files/46760), printed p.2332 (PDF page 30), visibly states the uniqueness-hardness question as a conjecture. It is historical motivation, not a hardness proof or a current literature-status determination.

No full literature search, priority conclusion, or novelty determination was attempted. The source-flow family must evaluate the DS primary body and actual perturbation quantifiers separately.

## Repair locators and strongest verified result

No mathematical repair is required in the assigned downstream or certificate arguments. Two optional precision repairs are useful:

1. PROOF.md §1, line15: explicitly say n>=1, or state that empty PARTITION lists are mapped to a fixed yes game. This is a domain clarification, not a hardness obstruction, because nonempty positive-weight PARTITION suffices.
2. PROOF.md §7, line132, and the old audit's computation claims: call the six-game/39-network checks historical development checks whose executables/results are intentionally outside this theoretical edition. The present edition does not itself supply that referenced script. This is a reproducibility/packaging limitation; the quantified proof does not depend on those finite checks.

The strongest independently verified theorem from this family's work is: **every network satisfying the explicit interface yields, by the submitted polynomial encoding, a rational exact-rank-one bimatrix game with a known strict pure equilibrium that is unique exactly in no instances and has an additional pair in yes instances; arbitrary rational bimatrix NONUNIQUENESS has polynomial rational certificates, including degenerate continua.** Closing the source interface promotes that conditional theorem to the claimed coNP-completeness result. This family has not independently closed that remaining interface and does not override the source-flow review.
