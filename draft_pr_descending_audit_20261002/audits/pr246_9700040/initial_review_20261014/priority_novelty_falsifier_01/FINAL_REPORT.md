# Adversarial test of prior mathematical coverage

Audit completed 2026-10-15 UTC. Completion estimate: 100% of this assigned adversarial audit, not a percentage for the broader research program. This report does not assign a workflow status or make a firstness or proposer-acceptance claim.

## Finding and its limit

I tried to preserve novelty of the submitted mathematical resolution by finding a central missing identification in the proposed earlier covering combination. I found no such mathematical gap. The simultaneous stationary rank representation in the 1993 notes, the exact pile-top/RSK identity in the 1999 published paper, and explicit pre-2018 joint tableau laws yield the submitted all-threshold law. This is an exact finite-dimensional specialization with a checkable bridge, not an inference from one-point marginals or an appeal to a toolkit that might eventually solve a new problem.

That conclusion is narrower than saying the 2018 question was historically acknowledged as solved. None of the inspected primary sources expressly identifies its theorem as an answer to the later question. The problem page itself still asks for a “fairly explicit” stationary description and says it was posted in February 2018. That chronology is real evidence against inventing acknowledgement, intent, or an established community credit assignment. It is not a mathematical obstruction to older equivalent laws. The candidate's explicit finite determinant presentation, corrected direct construction, and rational certificate remain useful authored work; an earlier appearance of that exact certificate was not established in this audit.

The strongest defensible mathematical claim is therefore: **the candidate's joint stationary probabilities are explicit consequences of identifiable earlier joint laws and the earlier rank representation; no unresolved central probabilistic identification is being supplied by the new formula.** Any broader historical wording needs the qualification above. See [the primary claim table](CLAIM_TO_SOURCE.md) for precise anchors.

## Exact bridge from the old stationary object

Write `P_n` for the RSK insertion tableau of a uniform permutation of `1,...,n`. The 1999 source identifies its entire first row with all the patience-sorting pile tops. A prescribed standard tableau `T` of shape `lambda` has probability `f^lambda/n!`: the RSK bijection permits exactly `f^lambda` choices of the recording tableau.

There is a pathwise restriction property, rather than a mere equality of one-dimensional distributions. Restricting `P_n` to entries at most `q` gives the insertion tableau of the original permutation with entries above `q` deleted. To see this directly, insert the letters in order. A letter above `q` never displaces an entry at most `q`. When a letter at most `q` bumps a larger entry above `q`, it appends at the end of that row of the restricted tableau; the subsequently bumped larger letter cannot affect any restricted lower row. This proves the property by induction. The filtered relative order is uniform on `q` letters. Hence these tableaux are coherent jointly in `q`.

Let `T_infinity` have this coherent law and let `B_r` be its `r`th first-row entry. These are precisely the limiting pile-top labels denoted `B(i)` in the 1993 notes, including their joint dependence. This is more information than a distribution for the first-row length at a single size. Finiteness also follows without an unproved infinite-tableau boundary condition: for `n` labels, disjoint blocks of `r` successive values have independent uniform relative orders, and an increasing block gives an increasing subsequence of length `r`. Thus

`P(B_r>n) = P(L_n<r) <= (1-1/r!)^floor(n/r) -> 0`.

Since `B_r>=r`, applying an independent unit-rate Poisson arrival sequence `Gamma` yields a locally finite sequence. The 1993 equation (42) already asserts the simultaneous stationary representation `X_r=Gamma(B_r)`. Its preceding equation (41) is a joint rank limit, not separate marginal limits.

If `N(x)` is the count process belonging to `Gamma`, then, jointly for any finite list of indices and thresholds,

`Gamma(B_r)>x <=> B_r>N(x) <=> shape(T_infinity restricted to 1,...,N(x))_1<=r-1`.

Conditional on the Poisson counts at finitely many thresholds, only the tableau restricted to the largest finite count is used. Consequently no exchange of an infinite-volume limit with a probability or determinant is needed. RSK symmetry alternatively identifies this coherent value-restriction chain with the usual recording-tableau prefix chain. The direct counting argument just given already avoids relying on that symmetry.

## Two older exact joint-law routes

**BO2004.** The admissible horizontal curve is `C(x)=(x,1)`. It has birth rate one and death rate zero by equation (1.9), and Remark 1.5 expressly includes this ascending case. Theorem 2.3 identifies its whole trajectory with RSK on nested Poisson rectangles. The old up probabilities give, from `mu` of size `n` to `nu` of size `n+d`,

`P_Delta(mu,nu)=e^(-Delta) Delta^d/d! * f^(nu/mu) * (f^nu/f^mu) * n!/(n+d)!`.

Indeed, each saturated Young-lattice path telescopes to the displayed dimension/factorial ratio; `f^(nu/mu)` counts the paths. Multiplication across thresholds telescopes every intermediate ratio. This gives exactly

`e^(-M) [f^(lambda^m)/|lambda^m|!] product_j [Delta_j^d_j f^(lambda^j/lambda^(j-1))/d_j!]`.

Its parameter `x` is spatial threshold at one physical stationary time. It is not the physical drift time, and this argument does not substitute a hyperbolic diagram process for the desired law. The theorem supplies the required joint coupling, not only the Poissonized Plancherel law at each `x`.

**Nica2014/2015.** Let `M=x_m` and `theta=sqrt(M)`. Map the original rectangle `0<u<=M, 0<v<=1` to Nica's square by

`(a,b)=(theta*v,u/theta)`.

The absolute Jacobian is one and increasing chains are preserved. The pile-top tableau is now the decorated insertion tableau with entries `b`. Its restriction at original spatial threshold `x_j` occurs at negative-branch parameter

`t_j=x_j/theta-theta`, with terminal `t_m=0`.

In Nica v1 Theorem 3.2, take these negative times, terminal shape `nu=lambda^m`, and no internal positive-time observations. Equivalently one can include the deterministic empty endpoint. The formula is

`e^(-theta^2) s_nu(rho_theta) product_j s_(lambda^j/lambda^(j-1))(rho_(Delta_j/theta))`.

The skew exponential specialization, already explicit in v1 Remark 3.3, makes the powers of `theta` cancel because `sum_j d_j=|nu|`. The resulting weight is the preceding BO weight and the candidate weight. Summing it over each barrier `lambda^j_1<=r_j-1` gives the candidate's simultaneous survival probability for arbitrary index lists. This finite-square argument requires no asymptotic theorem, row-process degeneration, or infinite-prefix limit.

The determinant form follows from the classical skew Jacobi–Trudi specialization. Transposition bounds the determinant dimension by the largest index barrier because standard skew tableaux transpose bijectively. Normalization by terminal size gives Poisson weights `e^(-M)M^n/n!`, so a computable tail bound follows immediately. These observations support mathematical coverage; they do not show that an older source printed the same rational enclosure or implementation.

## Checks and remaining cautions

The finite exhaustive check [check_rank_bridge.py](check_rank_bridge.py) passes all 5,913 permutations through size seven, 46,232 small-label restrictions, and 140 selected shape chains. It checks the entire pile-top/P-row identity, the pathwise small-label restriction, tableau preimage multiplicities, and the skew-factor chain count. These computations are falsification checks, not substitutes for the general argument above. The result is recorded in [RANK_BRIDGE_CHECKS.json](RANK_BRIDGE_CHECKS.json).

The 1993 draft is visibly unfinished and has unsafe printed scaling and coupling-rate statements. Its rough derivation should not be promoted as an error-free standalone proof. Here its correct model and static representation are the historical anchor, and the candidate's independently verified corrected construction removes doubt about that anchor. Repairing the elementary coordinate sign or quantifying the coupling does not create a previously unknown joint rank law. A claim that the draft alone already supplied the desired explicit all-index answer would be too strong.

The Nica v4 probability display contains a `mu/lambda` exponent typo; its correct Schur display and proof are not affected. I used the correct explicit theorem in v1 and its independent v3 counterpart for chronology. The retrieved PDFs display later title dates (v1: December 2024; v3: May 2022; v4: September 2021) despite their arXiv version labels (2014, 2015, 2017). Independently downloaded v1/v3 source packages use the article class and contain no date declaration. This supports the inference that the title dates are automatic compilation dates. The canonical version histories and immutable-version source content establish the relevant earlier formula; title dates were not silently treated as publication dates.

The BO2013 first-row dynamics are not evidence for any rigorous covering theorem here. No step uses them. An apparently matching generator in that heuristic source cannot replace the explicit old stationary-rank and finite joint-law bridge.

The exact remaining gap is historical and descriptive: whether an earlier author explicitly connected these formulas to the drift-jump question, or whether the proposer would regard this level of partition-sum description as satisfying the descriptive aim, is not established. No outreach was attempted or prepared. It would be inappropriate to turn that evidential gap into either acceptance or a worldwide firstness assertion.
