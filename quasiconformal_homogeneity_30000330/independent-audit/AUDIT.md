# Independent audit: quasiconformal homogeneity gaps

Problem 30000330 / OWR-1106-004, rank 497. Audit date: 3 October 2026.

## Verdict

**PASS, partial research only. The proposed disposition remains `unsolved`, `5/5`.**

The five approaches have genuine, distinct mathematical content and accurately identify their missing steps. The displayed necessary conditions do not solve the universal-gap question. The audit finds no fatal error in those conditions, with the precision notes below. In particular, neither nearly constant injectivity radius nor the strong-homogeneity constant supplies an unrestricted answer.

All six files listed in the frozen author manifest match their recorded byte counts and SHA-256 hashes. The manifest itself has SHA-256 `a0551bf9c2e75444178fcb771606180216b5a096b33f793ac364fb169f2d33ee`. No frozen file was edited. The original arithmetic script reproduces its recorded 915 cases; a separate implementation also passes 915 rational parameter cases, five deliberately incorrect-formula controls, and an integral intersection-form check. These are algebra checks, not formal proofs of the imported analytic theorems.

This is an independent mathematical review of the frozen packet, not a referee certification, priority claim, or exhaustive search of later literature. The repository-history claims in SOURCE_GATE.md were not independently repeated: they are not used to establish a mathematical conclusion.

## Precision notes that should accompany the packet

1. **Upper injectivity radius is finite for each surface, not uniformly bounded by K alone.** The first established-input sentence in REPORT.md is potentially misleading. The accurate statement is that the lower bound depends only on K, while the upper estimate is `d(S) <= K ell(S) + 2K log 4`. Its right-hand side also depends on the surface's systole. The regular covers in Attempt 2 have a common homogeneity upper bound but unbounded systole, so a K-only upper injectivity bound would be false. No later argument in the packet uses that false reading.
2. **Use closed balls in the covering equation.** A displacement estimate `distance <= D0(K^2)` initially gives a cover by closed balls. Their areas obey the same bound. Alternatively enlarge the radius by any positive epsilon and take a limit. If B in REPORT.md denotes an open ball, the exact set equality needs this harmless adjustment.
3. **Restrict the count when applying a subgroup theorem.** For homogeneity using H, repeat the covering argument with the number of admissible classes in H. Do not bound the unrestricted N_S(K) by |H| merely because one transitive family lies in H.
4. **Infima are not an obstruction.** The cited literature establishes attainment of K(S). Independently, all sequential deductions can use actual admissible homogeneity constants k_j > K(S_j) with k_j-K(S_j) tending to zero. Equations about N_S(k_j) or m_S(k_j,gamma_j) then concern those actual constants.

These clarifications preserve all asserted partial conclusions. They are not permission to label the target solved.

## Primary source and scope audit

### The exact target

The publisher gives Oberwolfach Reports 2 (2005), no. 4, pages 2519–2570, with publication on 30 September 2006. The audit visually checked printed page 2534 of Canary's contribution: the higher-dimensional theorem is stated for n >= 3, followed by the unresolved dimension-two extension. No compactness or fixed-genus hypothesis is inserted. The appropriate target includes complete orientable hyperbolic surfaces of infinite type and excludes the hyperbolic plane. The question is one universal lower bound, not a separate positive gap for each surface. [EMS Press record](https://ems.press/journals/owr/articles/1106)

### Inputs actually used

- **B05:** Theorem 1.1 has the one-sided uniformity described in precision note 1. Corollary 1.2 excludes nonclosed finite-type surfaces from uniform homogeneity, apart from the plane. Lemma 6.2 concerns finite regular covers with d/ell tending to one; it does not assert that K tends to one. The bounded-geometry and regular-cover statements were checked directly. [Author manuscript](https://websites.umich.edu/~canary/quasi.pdf)
- **B07:** Proposition 3.2 supplies systole escape as K tends to one. The main fixed-point theorem assumes a closed surface and a fixed c in (0,2], with at least c(g+1) fixed points of a nonidentity conformal automorphism. The case c>2 is vacuous, since 2g+2 is maximal. Proposition 6.2 gives a universal increasing displacement-to-dilatation function psi for a disk map fixing its ideal boundary; its inverse may serve as D0. [Author manuscript](https://websites.umich.edu/~canary/full.pdf)
- **KM:** Theorem A applies to genus-zero surfaces, including infinite type, other than the disk. Lemma 2.3 controls the length of the geodesic representative, not the possibly rough image curve's length. Lemma 2.5 gives uniform closeness to that representative tending to zero with K-1. Lemma 2.1's separation and even-intersection assertions have a genus-zero hypothesis. [Primary preprint](https://arxiv.org/pdf/0910.1050)
- **BMRT:** Theorem 2.3 concerns K_aut, explicitly defined using maps homotopic to conformal automorphisms. It identifies an unattained sharp infimum near 1.36138. This is not a lower bound for unrestricted K. [Author manuscript](https://web.ma.utexas.edu/users/areid/Kautfinal07.pdf)
- **Vlamis:** Theorems 1.2, 1.5, and 1.6 retain their closed-surface and subgroup hypotheses. Theorem 1.3 assumes a genus-linear bound on mapping classes moving a Teichmuller point a bounded distance; it does not establish that assumption. Its Teichmuller convention is distance = one-half log of extremal dilatation, hence a radius R corresponds to K = exp(2R). [Primary text](https://arxiv.org/html/1309.7026)

The survey's distinction between the full question and its restricted cases was also checked. Targeted current searches did not identify a full resolution. Failure to locate one is only a bounded search result; crawl timestamps are not publication dates. The recent Fletcher–Hahn paper was not needed for any proof here, and its publisher page could not be freshly retrieved during this audit. The audit therefore does not use that paper as affirmative evidence of open status. [Survey](https://arxiv.org/html/1401.3662)

## Independent derivations and adversarial tests

### Attempt 1: compactness and disappearing topology

Write ell(S) for the infimum of essential closed-loop lengths. At each p, `2 inj(p)` is the infimum of lengths of based essential loops at p, so inj(p) >= ell/2. A radius-r disk with r < ell/2 embeds. For a closed orientable genus-g surface of curvature -1,

`2 pi (cosh r - 1) <= area(S) = 4 pi (g - 1)`.

Letting r tend upward to ell/2 gives `cosh(ell/2) <= 2g - 1`, hence

`ell <= 2 arccosh(2g - 1)`.

The factor two on the radius is essential. The estimate is valid even though different pointwise injectivity radii need not agree. Combining this estimate with the escape theorem proves that every closed near-1 sequence has genus tending to infinity. More generally, a class with a common finite systole upper bound has its own gap: otherwise choose a member with an admissible homogeneity constant below 1+1/j.

The attempted compactness contradiction reverses the actual outcome. Since inj(p) >= ell/2 at every point, every fixed-radius ball is eventually a genuine hyperbolic disk. No nontrivial topology need remain in a pointed limit. The limit plane is compatible with all the necessary conditions. This disposes of the bounded-topology argument without proving that such a homogeneous sequence exists.

**Result:** valid bounded-systole/fixed-genus reduction; no topology-independent obstruction.

### Attempt 2: normal covers and injectivity-radius ratios

Let a finite regular cover M -> S have base diameter D. Compactness guarantees a systolic geodesic. At a point p on it, inj_M(p)=ell(M)/2. Given q in M, lift a shortest base path from the image of q to the image of p. Its endpoint p' is within D of q, and normality supplies a deck isometry taking p to p'.

For completeness, the injectivity-radius Lipschitz estimate follows by joining q to p', traversing a based essential loop at p', and returning: a loop of length approximately 2 inj(p') becomes one of length at most 2 inj(p')+2 distance(q,p'). The induced change of basepoint preserves nontriviality. Therefore inj(q) <= inj(p')+D. Taking extrema gives

`ell <= d := 2 sup inj <= ell + 2D`,

and `0 <= d/ell - 1 <= 2D/ell`.

Residual finiteness must be applied to all short conjugacy classes, including relevant powers. There are finitely many below a fixed length on the compact base. For each choose a finite quotient separating its representative from the identity, and intersect the kernels. The intersection is finite-index and normal. Normality excludes the whole conjugacy class, so its cover has no short essential geodesic. Letting the cutoff grow produces ell tending to infinity. Nestedness can also be arranged by taking successive intersections, but is unnecessary here.

The common finite K upper bound lifts for a separate reason. A compact base has a uniformly controlled transitive family isotopic to the identity. Lift its isotopies to the cover, then use a deck transformation to choose the target in the required fiber. Lifting and deck isometries preserve dilatation. This does not make that common bound approach one.

**Result:** the ratio obstruction is invalidated; no quasiconformal counterexample is constructed. Regularity, compactness of the base, and finite-cover compactness were used explicitly.

### Attempt 3: the missing conformal homotopy class

Suppose f is homotopic to a conformal automorphism a of a closed hyperbolic surface. Put h=a^{-1}f. The lift of h associated with its identity homotopy commutes with the covering group. It fixes ideal endpoints of its hyperbolic elements; these endpoints are dense in the boundary, so the lift fixes the whole boundary. Applying the disk displacement bound and projecting gives

`distance(f(x), a(x)) <= D0(K(f))`.

Under strong K-homogeneity this implies that the conformal quotient has diameter at most D0(K). Its orbifold diameter has a universal positive lower bound, yielding a strong gap. The boundary-fixing argument has no unrestricted substitute: a low-dilatation map may represent a different mapping class.

The ordering is `K <= K_aut <= K_0`. A lower bound on the larger quantity does not lower-bound the smaller one. This is a logical obstruction, not a shortage of numerical precision.

As a separate numerical cross-check, the triangle with angles pi/2, pi/3, pi/7 has largest side

`d_* = arccosh(cot(pi/3) cot(pi/7)) = 0.6206717375563859...`.

With `mu(r) = (pi/2) K_elliptic(1-r^2)/K_elliptic(r^2)` in the parameter convention for the complete elliptic integral, substitution into

`psi(d) = coth^2(pi^2/(4 mu(exp(-d))))`

gives `psi(d_*) = 1.3613826121756994...`. The portable diagnostic reproduces this with the arithmetic-geometric mean; a separate 50-decimal evaluation agrees. This checks the printed rounding and modulus convention, not the geometric theorem that this orbifold minimizes diameter or the theorem's sharpness. No decimal here is an ordinary-homogeneity bound.

**Result:** valid restricted argument and constant identification; the unrestricted rigidity step remains absent.

### Attempt 4: low-dilatation mapping-class counts

Fix one point x and a representative f_i for each admissible mapping class. Finiteness holds for a fixed closed S: a bounded closed Teichmuller ball is compact, and proper discontinuity with finite stabilizers gives only finitely many mapping classes in the displacement ball. This finiteness is not uniform in genus.

If f(x)=y and f has the same class as f_i, then h=f f_i^{-1} is identity-isotopic and has dilatation at most K^2. Thus y lies in the closed ball about f_i(x) of radius r=D0(K^2). This is the correct composition order and the correct squared budget. Each quotient ball has area at most `2 pi(cosh r - 1)`: it is the image of a disk of that radius under the universal covering projection. It need not be embedded. No isodiametric theorem for arbitrary subsets of a quotient is needed.

Area subadditivity now gives

`N_S(K) >= 2(g-1)/(cosh D0(K^2)-1)`.

For any sequence of actual admissible K_j tending to one, the denominator tends to zero, hence `N_{S_j}(K_j)/(g_j-1)` tends to infinity. This conclusion concerns the low-dilatation count at its moving threshold K_j. The count at any fixed larger threshold is at least as large.

If a fixed K_*>1 admitted a bound `N_S(K_*) <= C(g-1)` on every sufficiently large-systole closed surface, monotonicity would contradict that divergence. The packet does not prove this bound. In the finite-subgroup specialization, the restricted count is at most `84(g-1)` by realization and Hurwitz, so `cosh r-1 >= 1/42`, or `r >= arccosh(43/42)`. This is intentionally weaker than a sharper diameter-based covering estimate.

**Result:** the necessary superlinear-in-genus count is correct, with closed-surface scope. Finiteness and subgroup index arguments do not supply the missing upper bound.

### Attempt 5: tube coverage and genus-zero topology

A closed surface has a simple systolic geodesic gamma. Its images have simple geodesic representatives of length at most K ell. Only finitely many distinct closed geodesics have length below that bound on this fixed compact surface. For every y, move a fixed x on gamma to y; the straightening estimate puts y within C(K) of one of the m relevant representatives. The direction of containment used here is from f(gamma) into the tube.

For a simple closed geodesic of length L, the normal exponential map from `[0,L] x [-r,r]` covers its radius-r tube. The Fermi-coordinate Jacobian is cosh(t). Its domain area is `2L sinh r`; when the map overlaps, the image area can only be smaller. Compactness supplies minimizing normal segments to the geodesic, so there is no missing part of the tube.

Consequently,

`4 pi(g-1) <= 2 m K ell sinh C(K)`,

`m >= 2 pi(g-1)/(K ell sinh C(K))`,

`m >= pi(g-1)/(K arccosh(2g-1) sinh C(K))`.

In particular `m ell/(g-1) >= 2 pi/(K sinh C(K))` tends to infinity along a near-1 sequence. C may be enlarged slightly if needed to be positive for K>1. Note what is not proved: this does not by itself imply m/(g-1) tends to infinity, because ell may diverge too.

The topological countercheck is exact. In a one-holed torus inside a genus-two surface, a meridian a and longitude b have one transverse crossing. Their algebraic intersection is one, so their geometric intersection cannot be zero; the displayed representatives realize one. They are also nonseparating. The symplectic homology calculation in the control script records this witness. It disproves a wholesale transfer of planar separation/evenness, without requiring those two curves to be actual systoles or disproving the gap conjecture.

**Result:** the tube inequalities and proliferation condition are correct. A disjoint pants decomposition does not bound this orbit, whose geodesics may intersect. Infinite-area surfaces require a different argument.

## Reproducibility and interpretation of the 915 controls

Run from this directory:

`python3 verify_audit.py`

For optional frozen-integrity verification and replay of the author's already-verified script:

`python3 verify_audit.py --author-dir ../public --replay-author`

The independent implementation uses factored rational parametrizations and inequality comparisons below, at, and above each threshold. It does not import the author's formula functions. There are 50 ball cases, 50 finite-subgroup cases, 200 class-count cases, 600 tube cases, and 15 cover cases, totaling 915 parameter cases. Each case can contain several assertions; the report does not pretend that 915 means 915 independent theorems. The author's count has the same limitation.

The script deliberately tests incorrect factors and thresholds and verifies that rational witnesses reject them. Its additional genus-two homology calculation is exact. The elliptic-integral calculation is separately labeled floating-point diagnostic and is excluded from the exact count. Standard-library execution succeeds both normally and under Python's optimization flag; the audit's checks do not disappear under `python -O`.

The controls do not prove normal-family compactness, boundary extension, Wolpert's inequality, geodesic straightening, residual finiteness, orbifold diameter minimization, or any uniform gap. Those mathematical ingredients and their hypotheses were inspected separately above.

## Final publication boundary

The audit deliverables contain original analysis, bibliographic links, the independent script, its output, and file-integrity metadata. They contain no downloaded papers, source-page images, copied source corpus, private discussion, credentials, or remote-mutation records. No remote state was changed during this review.

The acceptable claim is that five substantive attempts were independently reviewed and yield valid partial reductions, with the stated precision notes. The unacceptable claims remain: a universal ordinary constant, a near-1 homogeneous counterexample sequence, completion of the closed case, or completion of the infinite-type case.
