# Independent adversarial audit: Degree Bounds for Degenerate Herman Rings

Problem 30001391 / OWR-4137-007. Audit date: 2026-10-04 UTC.

## Verdict

**Retain `unsolved` for the intended unrestricted periodic problem.** The frozen packet does not prove a bound, or finiteness, for all periods. It correctly declines to turn the literal-definition counterexample into a resolution of that intended problem.

**Accept the restricted mathematical conclusions A–E at the level of an independent written proof review.** In particular, A's bound of `d-1` for individually invariant Julia Jordan curves survives the adversarial checks below. B's bound of one periodic spherical circle also survives. There is one concrete citation-locator correction and several useful precision edits; none changes either restricted conclusion. This is not formal verification, a novelty certificate, or evidence that the unrestricted target is solved.

The exact author manifest audited has SHA-256:

`63df37afcb5592e0bde27cf8e66383025710e5fcc685d38afb954a37275d48b8`.

All 13 manifest-listed files were read and their bytes verified. `SHA256SUMS.json` was also inspected and bound separately by the hash above. The author originals were not edited. This audit is separate, contains no redistributed source articles or extractions, and makes no remote changes.

## A. Individually invariant curves: detailed attack and reconstruction

### A1. Disjointness and complementary regions

For the theorem as stated, every orbit on each curve is dense. A shared point between two curves consequently has an orbit whose closure is both curves; they are equal. This proves pairwise disjointness without regularity assumptions.

For a finite family of disjoint Jordan curves on the sphere, the Jordan separation theorem, applied inductively, gives `N+1` connected complementary components. After a point outside the curves is designated infinity, one component is unbounded and exactly `N` are bounded. A component may have several boundary curves. It must not be replaced by a union of bounded components, and a region with holes must not be treated as simply connected. The submission makes neither mistake.

A rational self-map of the sphere has a fixed point. No such point lies on an irrationally rotating curve. Möbius conjugation can therefore make one fixed point infinity without moving any curve through infinity. Since infinity is fixed, it belongs to the pole fiber with positive local multiplicity. The other pole multiplicities sum to at most `d-1`. This is a count of a fiber with multiplicity; critical poles are not lost.

### A2. A winding proof requiring no rectifiable boundary

Here is a more explicit replacement for A(d)'s appeal to a Jordan-region argument principle. It uses only finite rational factorization and winding of continuous loops.

Fix a bounded complementary component `U`. Orient each component `gamma_j` of its boundary positively relative to `U`: the outer boundary is counterclockwise and the hole boundaries clockwise. For any point `a` off the boundary, Jordan separation gives

`sum_j ind(gamma_j,a) = 1_U(a)`.

Suppose `U` contains no pole. There is also no pole on its boundary, because every boundary curve is mapped to itself and avoids infinity. Take a finite `w` off the boundary. Factor the nonzero rational function `f(z)-w` over the complex numbers into its finite zeros and poles with their multiplicities. Additivity of winding under products and quotients gives

`sum_j ind(f o gamma_j,w) = Z_U(w)-P_U`.

All factors corresponding to points in holes or outside the region contribute zero after the signed boundary sum. This directly accounts for disconnected parts of the complement and does not require a contour integral. Because `f` restricts to an orientation-preserving homeomorphism of each boundary curve, `f o gamma_j` has the same winding as `gamma_j`. Hence

`Z_U(w)-P_U = 1_U(w)`.

As `P_U=0`, every target in `U` has exactly one preimage in `U`, counted with multiplicity, and every target outside the closure has none. If an interior point mapped to the boundary, openness of a nonconstant holomorphic map would produce image points outside the closure. Every boundary point of this finite Jordan region is approached by such exterior points. That is impossible. Thus `f(U)=U`, each fiber in `U` is a singleton of multiplicity one, and `f:U -> U` is a conformal automorphism.

This argument needs neither smoothness of the Jordan curves nor nonvanishing derivative on them. A critical point in `U` is excluded by the multiplicity-one conclusion, not assumed away. Boundary critical points do not invalidate the winding calculation. Rationality already supplies holomorphic continuation near the compact pole-free closure; no extension of a Riemann map or rotation conjugacy to the boundary is invoked.

### A3. Is the region a whole Fatou component?

Yes. Iterates are uniformly bounded on `U` because they remain in that bounded region. Thus `U` is contained in a Fatou component `V`. Its boundary is a union of the assumed Julia curves. If the connected open set `V` contained a point outside `U`, a path in `V` from `U` to that point would meet this boundary. That would put a Julia point in `V`, a contradiction. Hence `V=U` and it is invariant.

The cited [McMullen–Sullivan classification, Theorem 2.1](https://people.math.harvard.edu/~ctm/papers/home/text/papers/qciii/qciii.pdf) applies to periodic Fatou components of rational maps of degree greater than one. It includes attractive, superattractive, parabolic, Siegel, and Herman cases. An automorphism of the bounded hyperbolic domain `U` is an isometry for its hyperbolic metric. At an interior fixed point its derivative therefore has modulus one, ruling out both attractive cases. A parabolic component has a periodic boundary point, contrary to the boundary dynamics. The remaining cases are a Siegel disk or Herman ring. Its boundary components are among the `C_i`, contradicting the stated exclusion.

Consequently each bounded region contains a finite pole. These regions are disjoint, so their charges are distinct. The bound follows. The same finite-family argument excludes an infinite family of individually invariant curves: an infinite family would contain a finite subfamily of size `d`.

### A4. What the proof does not transfer across periods

For a finite family with periods dividing `L`, the applicable map is `F=f^L`, of degree `d^L`. Its Julia and Fatou sets agree with those of `f`. A rotation component for `F` is a periodic rotation component for `f`, and conversely a periodic rotation component becomes invariant under an appropriate iterate. Thus the exclusions transfer if “rotation domain” includes periodic components, as it normally does. The resulting count is `d^L-1`.

This is not a bound depending only on `d` when `L` is unbounded. For example, periods 2, 3, and 5 already use `L=30`; in degree three this gives `205891132094648`. More importantly, finite bounds for each specified period do not imply finiteness of their union. The original pole argument cannot charge every transient stage of a permuted complementary region to a distinct pole of `f`. No such transfer is supplied in the packet.

## B. Periodic spherical circles

The proof is valid with its stated scope. A common return iterate has irrational rotation number on both circles and therefore no periodic point there. Two distinct spherical circles intersect in at most two points. Their intersection would be a nonempty finite forward-invariant set and would contain a periodic point; hence the circles are disjoint. Topological conjugacy to rigid rotation is not required for this step.

For precision, apply the identity principle to the rational maps `g` and `sigma_C o g o sigma_C`. They agree on `C`; therefore they agree globally. This rigorously gives commutation with the anti-Möbius reflection and similarly with the second reflection.

Normalize the first circle to the unit circle, choose its disk side containing the second, and rotate its center to `a>=0`. The second circle has radius `r>0` and `a+r<1`. The displayed matrix in the packet has determinant `r^2`, positive trace, and discriminant

`((1-r)^2-a^2)((1+r)^2-a^2)>0`.

Both eigenvalues are distinct and positive, including the concentric case `a=0`. Their ratio is a positive real number different from one. After conjugation the commutation equation is `G(lambda z)=lambda G(z)`. A rational function has a meromorphic Laurent expansion at zero, even if zero is a pole. Only the coefficient at exponent one can survive. Nonconstancy then makes `G` a degree-one map, contradicting `deg(g)>=2`. There is no omitted pole-at-zero exception.

## C. Critical-point charging

The claim is a count of curves containing critical points of `f`, or of disjoint cycles meeting that finite critical set. A common iterate establishes disjointness. Distinct charged curves or cycles cannot consume the same critical point. The Riemann–Hurwitz total `2d-2` is therefore a valid upper bound. This neither bounds critical-point-free curves nor multiplies into a bound on all component curves of cycles with uncontrolled periods.

The reliance on Yang is appropriately narrow: his constructed smooth examples avoid all critical points, with a direct separation argument in the construction. A broader claim that smooth invariant Jordan curves are automatically critical-point-free must not be inferred. The smooth unit circle of

`B(z)=z^2(z-3)/(1-3z)`

contains the double critical point 1. Indeed `B(z)-1=(z-1)^3/(1-3z)`, while its circle angular derivative is `12(1-cos(t))/(10-6cos(t))`, positive except at that point. Phase choices with irrational rotation are discussed in Yang's example. The packet itself does not make the invalid broader claim.

## D. Analytic conjugacy and a Fatou collar

The conditional result is sound. Shrink the domain of the univalent extension to a circular annulus invariant under multiplication by `lambda`. The identity principle gives the conjugacy throughout it. Rotations form a normal family, so their conjugates do too on the image collar. Normality for an iterate is equivalent to normality for the original rational map: decompose every exponent into a multiple of the iterate length plus one of finitely many remainders. Thus the curve is in the Fatou set.

The hypothesis supplies an analytic linearizing conjugacy, much more than an analytic embedded curve carrying topological irrational dynamics. The submission does not silently equate them. This is an obstruction, not a count or an analytic-existence theorem.

## E. Zero-area support and deformation

A compact `C^1` parametrized curve is Lipschitz in finitely many coordinate patches, giving area zero by the stated covering argument. For spherical curves through infinity, use a finite sphere-chart cover; the same zero-area conclusion holds. A Beltrami coefficient supported on finitely many such curves is zero almost everywhere. A normalized quasiconformal sphere map with that coefficient is the identity. This rules out the proposed *support-only* deformation mechanism; it does not rule out surgery acting in neighborhoods or on other positive-area sets.

The missing simultaneous, degree-preserving thickening theorem remains missing. [Shishikura's Theorems 3 and 5](https://www.numdam.org/item/10.24033/asens.1522.pdf) concern genuine Herman-ring cycles: the cycle bound is `d-2`, and cubic maps can have a cycle of arbitrary specified period. These establish the importance of the cycle/component distinction, not a counterexample for degenerate curves.

## Primary-source and definition audit

- [Oberwolfach Report 54/2009, printed p.2958](https://doi.org/10.4171/OWR/2009/54): the page was checked in the primary PDF and visually against its rendered page. It uses analytic periodic curves and an irrational homeomorphic return map, explicitly excludes the closure of a Herman ring, and does not print a Siegel or Julia exclusion. The preceding problem describes the standard rotation-domain level curves. Treating their intended omission as repaired is an interpretation supported by context, not an extra printed hypothesis.
- [Eremenko, November 22, 2025, p.1](https://www.math.purdue.edu/~eremenko/dvi/invariant.pdf): the printed definition requires Julia membership, excludes spherical circles and rotation-domain boundaries, and states conjugacy for `f` itself. On that literal individually invariant formulation, A applies and supplies the asserted finite bound. This is a substantive scoped conclusion; the audit does not erase it. It also does not identify that formulation with the 2009 periodic question, establish novelty, or adjudicate a possible implicit cycle convention.
- [Yang, arXiv v2, pp.2–3, 5, 26–27](https://arxiv.org/pdf/2207.06770v2): smooth cubic existence and the critical-point-free construction are supported; analytic existence is not asserted by his method. The quadratic linearizer used in the literal counterexample is equation **(2.2)** and its following paragraph, not primarily equations (2.3)–(2.5).
- [Lim, arXiv v5, Definition 1.1, Corollary B, Theorem C](https://arxiv.org/pdf/2302.07794v5): the degree is `d0+d_infinity-1`; prescribed combinatorics describe critical data on a Herman quasicircle in the specified family. This does not provide an unbounded count on a fixed map or simultaneous thickening for arbitrary families.

The five locally available scholarly PDF hashes match the author's source manifest. The classification reference was independently read through web PDF extraction; no local PDF hash is asserted for it. Limited current-source searches disclosed no reason to change the target verdict; search absence is not evidence of openness or novelty. No catalogue page, dataset provenance, prior coordination history, or remote repository state was independently certified by this audit.

## Literal Siegel example

The mathematical construction is correct. Golden-mean continued-fraction denominators grow at least geometrically every two steps and at most exponentially. This proves convergence of the Brjuno series, independently of any finite recurrence test. The quadratic therefore has a local linearizer and a Siegel disk. Images of interior concentric circles are distinct analytic invariant Jordan curves with irrational dynamics. Each is in an open Fatou component, so no point of it lies in the closure of a different Fatou component, including a Herman ring.

There are uncountably many such curves already in degree two under the bare printed conditions. They fail the Julia-set version. The report's treatment as a literal-scope counterexample rather than an intended-target solution is sound.

## Reproducibility, findings, and limits

`verify.py` passed and exactly reproduced `CONTROL_RESULTS.json`. `verify_manifest.py` passed with 13 files. Independent controls check the binding hash, exact signed winding in a two-hole polygonal model, orientation-preserving reparametrizations, wrong-hole-orientation mutations, zero/pole contributions from holes, the critical Blaschke example, Laurent resonance, and a separate common-period calculation. See `INDEPENDENT_CONTROL_RESULTS.json` and `independent_checks.py`.

These controls do not certify Jordan topology, normal families, the Fatou classification, Brjuno linearization, the infinite Laurent argument, or a universal periodic bound. The written proof review supplies those logical checks using standard theorems. The audit has not established sharpness or novelty, and has not searched exhaustively for all subsequent research.

The exact suggested edits are in `EXACT_CORRECTIONS.md`. The portable `AUDIT_MANIFEST.json` binds this audit to the frozen author manifest; its own external SHA-256 receipt is adjacent. Recommended public status remains **unsolved with independently audited restricted results**.
