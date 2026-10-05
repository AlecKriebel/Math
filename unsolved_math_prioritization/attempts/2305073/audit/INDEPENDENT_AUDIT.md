# Independent adversarial audit: Korenblum's Riesz-majorant problem

## Verdict

**PASS as a packet of partial results. Recommend campaign status `unsolved`, with five substantive approaches completed (`5/5`).** No blocking mathematical correction was found. This is not a complete characterization of arbitrary measurable pointwise obstacles, not a claimed new solution, and not certification that no later solution exists in the literature.

The audit independently reviewed every proof in the frozen packet. The original 11,515 exact finite controls replayed successfully, with output identical byte-for-byte to the frozen result. A separately written suite passed 12,073 additional exact checks. These counts measure finite regression checks, not mathematical proof depth; the analytic arguments were reviewed directly as described below.

## Frozen inputs and independence

The six authored payload files total **42,200 bytes**. Their manifest has SHA-256:

`5e1638e7589229caf8667fbcd6af98b2c92f5281e32b95e690d315ea9a39cf8e`.

All six file sizes and hashes match that manifest. The manifest itself is 1,025 bytes. The seven-file authored directory was left byte-for-byte unchanged, including its historical statements that independent audit had not yet occurred. This separate report supplies the later audit record; those frozen fields should not be rewritten to suggest that the author had already completed this review.

The reviewer used no helper reviewers, did not edit the authored packet, and performed no remote writes. The additional tests do not import the author's control functions. They execute the author's program only for the explicitly identified original replay.

## Primary source and target quantifiers

The official [arXiv version page](https://arxiv.org/abs/1809.07200v2) and [primary PDF](https://arxiv.org/pdf/1809.07200v2) were opened during this audit. The full statement and update for Problem 5.73 were inspected in the web-reader text, and the available page renders of printed pages 111 and 112 were visually inspected. The definition is the unnormalized real-line kernel with exponent `-alpha`, for `0 < alpha < 1`, and finite positive Borel measures. The pointwise reading preserves the source's unqualified domination; the adjacent problem explicitly introduces an almost-everywhere qualification.

The official version history identifies v2, dated 21 September 2018, as the latest listed version. That volume's update reports no progress for this problem. This is historical source status, not proof of current global unsolved status. Four fresh targeted searches located no verified exact resolution; they are not an exhaustive literature search. No external resolution theorem or uninspected capacity theorem is relied upon in the accepted proofs.

A previously retrieved copy of the PDF was independently hashed: **1,706,228 bytes**, SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`. This validates the stated cached bytes; it is not a fresh remote-byte equality check. No source PDF, source-page image, extracted source text, catalogue record, or dataset contents is included in this audit deliverable.

The source leaves some representative conventions implicit. The packet responsibly states its conventions: the singular kernel value is infinity, zero measure has zero potential, finite measures may have atoms, and potentials may take infinity. All separating examples are finite-valued Borel functions. Allowing the zero measure is needed for the least-mass formulation and does not change majorant existence. The a.e. theorem allows Lebesgue-measurable obstacles; pairings with singular measures are asserted only for Borel obstacles. This prevents a hidden completion or representative change.

## 1. Universal integral and test-measure bounds

**Accepted.** For a measurable set of finite length, layer cake gives the integral of the minimum of its length and the kernel superlevel-set length. Splitting at the crossing value yields exactly `2^alpha/(1-alpha)` times the length to power `1-alpha`. Translation does not affect the calculation. The zero-length case is correct even though the kernel is infinite at one point, since integration is with respect to Lebesgue measure.

Tonelli then proves local integrability and a.e. finiteness of each finite-measure potential. The weak endpoint bound is justified by first intersecting the superlevel set with a bounded interval and only then increasing the interval. There is no assumption that the superlevel set was already finite.

The bounded-potential test follows from nonnegative Tonelli with the symmetric kernel. It is valid with infinities and singular measures for Borel obstacles. For a.e. domination, absolute continuity of the testing measure is genuinely required. This distinction is observed everywhere the test is used.

## 2. Opposite outcomes with identical rearrangements

**Accepted for every `0 < alpha < 1`.** The chosen geometric ratio is below one half. Separated spike intervals therefore do not overlap, and their height-length products form a summable series. The weighted test mass on each interval is precisely the reciprocal of its height, giving finite total test mass but infinite obstacle pairing.

The uniform potential bound on that testing measure was checked independently. The neighborhoods of the interval left endpoints are disjoint. Inside one neighborhood, every other spike interval is more than one unit away; outside every neighborhood, all spike intervals are at least one half unit away. At most one local singular contribution remains, controlled by the set-integral lemma. Neighborhood boundary points fall in the second case. No unproved summation of infinitely many uniform bounds is used.

Placing intervals end-to-end near zero preserves every Lebesgue level-set length and gives a pointwise atomic majorant, because height times the right endpoint to power alpha is uniformly bounded. The assigned value at zero is finite, and a positive atom there permits it. Both examples are Borel, finite-valued, integrable, and in the weak endpoint space. The conclusion excludes a rearrangement-only characterization without claiming that all spatially sensitive criteria fail.

## 3. Exact a.e. duality, separation, and mass escape

**Accepted, including least-mass attainment and the zero-mass case.** This is the most important infinite-dimensional step in the packet.

1. A smooth nonnegative compactly supported density has a transformed potential in `C_0(R)`. Local kernel integrability proves boundedness and continuity; a compact-support tail estimate proves vanishing at infinity. A positive smooth cutoff on any prescribed compact interval shows that finite dual value forces local integrability of the obstacle.
2. Positive measures with mass **at most** the prescribed bound form a weak-star compact subset of the dual of `C_0(R)`. Positivity is closed. The measures are finite Borel measures by the Riesz representation theorem. There is no unsupported assertion of tightness or compactness of an exact-mass probability class.
3. Each smooth-test constraint is continuous in this topology, because its transformed test lies in `C_0(R)`. Every right-hand side is finite when the dual value is finite.
4. For finitely many tests, the vector image is compact and convex. Separation from a translate of the positive orthant gives a nonnegative separating vector. A negative coefficient would make the infimum on that orthant unbounded below, contradicting strict separation. Combining the tests with those coefficients produces another allowable nonnegative smooth test.
5. The support function of the positive mass ball is the mass bound times the sup norm of that combined transformed test. A nonzero, nonnegative `C_0` function attains its positive maximum; the zero function and zero mass bound cause no exception. Scaling the combined test contradicts strict separation.
6. The finite-intersection property supplies one measure satisfying all smooth tests. Tonelli and local integrability turn those inequalities into nonnegativity in distributions, hence a.e. domination. Taking the mass bound equal to the finite dual value proves attainment and equality of primal and dual values.

Mass may escape to infinity along approximating measures. This is harmless here: the class imposes only an upper bound on mass, and every constraint is paired against `C_0`. Lost mass has no unaccounted residual contribution. The proof invokes neither a minimax interchange with an unverified hypothesis nor a general infinite-program duality theorem.

The same argument would not work with point-evaluation constraints. The packet's explicit small atom sequence correctly demonstrates that failure; this is a substantive boundary of the proof, not a cosmetic qualification.

## 4. Local averages and the l.s.c. pointwise upgrade

**Accepted at every point, including infinite potential values.** The kernel-average inequality uses two exhaustive cases. If the distance from the singularity is at least twice the averaging radius, the kernel is bounded by its central value times `2^alpha`. In the other case, the interval integral bound gives the stated larger uniform constant. At the singularity the domination inequality has an infinite right side, which is legitimate.

At a finite potential value, the kernel at the central point is an integrable dominating function for the measure, so dominated convergence applies. Any atom at that point is necessarily absent. At an infinite potential value, Fatou gives an infinite lower limit for the averages. Since this argument holds along every sequence of radii tending to zero, it proves the full limit, not only a selected subsequence.

For a nonnegative lower semicontinuous obstacle, every strict finite lower bound at a point persists in some neighborhood. This gives the needed lower bound by local averages, including when the obstacle is infinite. Integrating an a.e. majorization over each averaging interval and taking the every-point potential limit proves pointwise domination by the same measure. The least-mass value and attainment are therefore unchanged in this l.s.c. case.

The proof does not merely use lower semicontinuity of the potential. That alone would not recover lower bounds from a dense set. Likewise an upper semicontinuous or arbitrary Borel obstacle cannot replace the l.s.c. hypothesis: the singleton example already distinguishes the mass-attainment assertions. The existential l.s.c.-envelope reformulation is correctly labeled a reformulation, not an intrinsic solution.

## 5. Countable repair and the compact null-set obstruction

**Accepted for every allowed alpha.** An enumerated countable set receives a positive atom at every listed point with arbitrarily small total mass. Repetitions and non-discreteness do not invalidate this measure construction. The potential is infinite at each listed point; the remaining a.e. finite set is not required to be a topologically open complement.

For the Cantor construction, an admissible contraction ratio exists because `2^(-1/alpha) < 1/2`. Distinct level cylinders have the asserted minimal gap. A ball of radius equal to cylinder length can meet only a uniformly bounded number of cylinders; the stated noninteger bound is a legitimate upper bound on the integer count. The use of only the internal gaps makes the estimate conservative. It applies to centers anywhere on the real line.

The consistent cylinder probability measure is atomless, and the Cantor set is compact and Lebesgue-null. The annular potential estimate is uniform because the geometric ratio is strictly below one. Boundary distances can be allocated to either adjacent annulus without changing the bound. No diagonal atom survives. This directly proves bounded potential and avoids any hidden capacity theorem.

The first-right-digit cylinders are disjoint Borel sets of the asserted masses, covering the Cantor set except for the leftmost point. Assigning reciprocal-mass heights gives a finite-valued Borel function supported on this compact null set with divergent pairing. The bounded-potential test rules out every pointwise finite-measure majorant. Its smooth-test dual value is zero because it vanishes Lebesgue-a.e. Thus the claimed distinction is actual failure of an a.e. reduction, not merely a missing proof. The illustrative bound below 57 at alpha one half was also checked.

## 6. Constructive interval majorants and nonnecessity

**Accepted.** Each positive coefficient times the interval indicator is dominated by the atom at the center with mass equal to that coefficient times the half-length to power alpha. The worst finite value occurs at the endpoints. Zero coefficients may be discarded, avoiding an indeterminate symbolic product with infinity. Summing positive measures and kernels is legitimate by monotone convergence, and the exact total mass is the claimed scalar cost.

The proposed counterexample to necessity is pointwise dominated by one atom. Pairing it with the locally integrable truncated power weight gives a divergent logarithmic integral. Every interval has weight bounded by a fixed multiple of its length to power alpha, so any finite-cost cover would instead force finite pairing. This contradiction remains valid after any countable repair, because that changes nothing in the Lebesgue integral. The sufficient cover condition is therefore genuinely stronger than majorizability.

## 7. General dual route and status accounting

**Accepted as a necessary condition only.** The all-finite-bounded-potential-measure test catches the Cantor example. The packet does not claim its sufficiency, a capacitary duality theorem, or a polar exceptional-set repair theorem.

The point-constraint set is not weak-star closed: positive atoms of decreasing mass have infinite potential at their location but converge to the zero measure. Every countable family of point constraints is feasible with arbitrarily small mass, whereas the constant obstacle on the whole line violates the growing-interval integral bound for any finite mass. The singleton obstacle has mass infimum zero with no zero-mass pointwise majorant. These independently refute finite-sampling and unrestricted-attainment extensions.

The five approaches count as substantive: endpoint/rearrangement analysis; constructive interval covers; functional separation for smooth tests; singular exceptional-set constructions; and general measure duality with topology/nonattainment obstructions. Although they share lemmas, they test distinct proposed routes and yield separate positive or negative conclusions. This supports five completed attempts, not five resolutions of the original question.

## 8. Independent controls and their limits

Run `python3 audit/verify_audit.py --author-dir author` from the parent directory containing the two folders. The standard-library-only suite checks the frozen binding and byte-exact author replay, then independently tests:

- Exact antiderivative averages for many rational exponents, on intervals crossing, avoiding, or touching the singularity; the uniform average constant is checked using positive integer powers, without floating point.
- Diverging averages at the center of an atom.
- Cantor cylinder geometry for five distinct contraction/exponent pairs, including an exponent close to one; all interval-overlap breakpoints at eight finite depths are checked.
- Separate rational vertex enumerations of both sides of 486 finite positive-matrix mass/dual programs, including zero and one-sided obstacles, plus positive-combination separation controls.
- Rational-exponent spike variants, exact atomic repair budgets, finite lower sums for the logarithmic divergence, and `C_0` tests of mass escaping to infinity.

The finite programs are nonsingular analogues only. They do not discretize away the infinite-dimensional proof obligation, justify a pointwise duality theorem, or validate an arbitrary-real-parameter assertion by sampling. Those assertions are accepted only within the proof scopes reviewed above.

## Publication boundary

The audited mathematical disposition is **partial results, original pointwise target unresolved, 5/5 approaches**. Keep the scope qualifiers on the exact dual theorem, the singular-measure necessary condition, and every status claim. The audit's current literature observations are bounded and do not establish novelty. Historical queue and duplicate checks in the author packet were not independently repeated as part of this mathematical review.

The safe deliverable contains authored mathematics, authored tests, hashes, byte counts, inspection metadata, and this audit. It contains no source contents, dataset contents, private sources, private coordination records, or personal data. No remote state was changed by the reviewer.
