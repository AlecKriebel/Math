# Independent audit: periodic basin-boundary accessibility

Problem 5300048 / AMR-052-0048. Audit date: 7 October 2026 (UTC).

## Verdict

**Accept the corrected reading copy as an unresolved, auxiliary-results research note. One explicit explanatory correction is required in the frozen original.** All twelve numbered results pass this mathematical audit under their stated hypotheses. None settles the full accessibility question. This is an independent mathematical review by an automated assistant, not human peer review or formal proof verification.

The correction is in Approach 4's proposed sufficient bridge from impression membership to identification of a ray's landing point. A singleton principal set by itself is insufficient. This does not invalidate Lemma 9, Proposition 10, or an achieved accessibility theorem: Approach 4 never established the missing bridge. The accompanying patch changes only this explanatory passage and explicitly says that none of the proposed bridges has been established.

The main retained conclusion is the comb rigidity theorem: every proper holomorphic self-map of the specified slit-comb domain that extends across its closure is affine, hence degree one. The transported degree-two disk map consequently fails the extension requirement. This is an obstruction to the attempted example, not a counterexample to the original problem.

### Exact reviewed bytes

- Original `PROOF.md`: 24,992 bytes; SHA-256 `2b723d96cca5e1415f09dee97567c2711259e16c062cc6818d84b5a93bb9a4b8`.
- Original `AUTHOR_MANIFEST.json`: 1,731 bytes; SHA-256 `c2dbe9efd1dcd44ee5621da4e1341ac0be078d5ccbfce614fa5f4532ab8ec048`.
- `PROOF_CORRECTED_READING_COPY.md`: 25,121 bytes; SHA-256 `83f24e659b0527695c756f3e29600722f7b15409afe87e85007aaf3e8f2c7e4f`.
- `PRIME_END_WORDING.patch` records the complete difference. The original submission has not been overwritten.

The author manifest's eight content-file hashes and byte counts were independently recomputed and matched. Its ninth packet file is the manifest itself, appropriately excluded from its own entries. Source documents and dataset contents are absent from the public author and audit packets.

## Scope and method

I read the complete frozen proof, its approach ledger, source notes, README, manifest, target metadata, control code and results. I reconstructed each numbered argument, with particular attention to the global-versus-local inverse-component issue, the exact hyperbolic normalization, symbolic shift surjectivity, and the two identity-principle steps in the comb theorem. I did not use other mathematical audit workers.

I inspected the recovered primary page-30 image, inspected the relevant recovered scholarly text and PDF identities, freshly extracted all eight PDFs locally, and reopened the applicable primary sources on the public web. Public-source reopening supports textual/version checks; it does not establish equality of the recovered PDF bytes to current downloads. All eight recorded PDF hashes, sizes, and recorded text-extraction hashes/sizes matched their local files. `SOURCE_AUDIT_METADATA.json` records those checks.

This review independently establishes the primary problem label, scope, theorem-use boundaries, and mathematical deductions. It does not independently re-download the large source corpora or re-establish their full-row equality assertions in `TARGET_VERIFICATION.json`. Those remain the author packet's recorded verification outcomes. No fresh remote repository duplicate scan, priority determination, or exhaustive modern-literature search is certified.

## Required correction: principal set versus impression

Original lines 343–347 correctly distinguish an impression from a radial landing point, but then propose a singleton principal set as a sufficient identification condition. Let I be the impression of an address whose radial ray lands at p. Its radial principal set is already {p}; knowing q belongs to I does not imply q=p when I can contain additional points. Thus replacing a missing singleton-impression argument with a singleton-principal-set statement would repeat the identification gap.

The patch states the legitimate sufficient alternatives: a singleton impression; proof that q belongs to the principal set of that landing ray; or another separation/identification argument. No necessity claim is intended. It then expressly records that none has been supplied here.

The source's own distinction between the principal ray-limit set and the full impression is consistent with this correction; see the definitions around printed p.4 of [Blokh–Oversteegen](https://arxiv.org/pdf/0809.1071). The correction does not construct a prime end, force a periodic address, or provide an access curve to the requested q.

## Result-by-result mathematical review

### Lemma 1: boundary multiplier restrictions — accepted

The attracting case uses a forward-invariant local neighborhood whose iterates tend to q, chosen disjoint from the interior attractor a. Its intersection with U is nonempty, and an orbit there cannot converge to two distinct points. In the irrationally linearizable case, a sufficiently small invariant linearization disk has compact closure avoiding a; points in its intersection with U cannot converge to a. A locally identity positive iterate likewise contradicts attraction at any intersection point different from a.

The return germ is defined after shrinking neighborhoods around all points of the finite periodic orbit. The spherical case is handled in a local coordinate. The resulting classification leaves repelling, genuinely parabolic, and nonlinearizable irrationally indifferent points; it does not remove neutral periodic points. The Lyapunov-exponent statement is correctly restricted to a periodic orbit.

### Lemma 2: inaccessibility transfer — accepted

An access curve in a domain contained in the complement of L is also an access curve in the complement of K when K is contained in L. This is a direct inclusion argument. The endpoint-boundary assumption prevents a misleading use of accessibility for an unrelated point; the proof does not require local connectivity.

The subsequent proposed polynomial realization is correctly conditional. A connected filled Julia set is a full continuum, its spherical complement is simply connected, the polynomial restricts there to its full-degree proper self-map, and infinity is its attracting fixed point. The needed contained inaccessible compactum and periodic point have not been realized by this argument.

### Lemma 3: direct hedgehog-complement obstruction — accepted

Empty interior of K makes the spherical closure of its complement the entire sphere. An extension as required is therefore a nonconstant rational map. Forward invariance of the complement forces every preimage of any y in K to lie in K. Invariance and injectivity of the local map give precisely one such preimage, with local multiplicity one. The global degree formula then gives degree one, contradicting a degree-at-least-two restriction.

This argument uses the hypothesis that the extension agrees with the specified univalent local map near all of K. It does not rule out a different global construction with K inside a larger filled Julia set. The packet preserves that limit.

### Lemma 4: finite inverse-component criterion — accepted

For the rational return map h, its preimage of U has finitely many components. On each component the restriction is proper: a limit of inverse images of a compact subset of U still lies in the open preimage, so cannot escape through that component's boundary. The restriction is nonconstant and open; properness makes its image closed in U, hence surjective. Counting inverse images of a regular value bounds the number of components and sums their positive degrees to the global degree.

U itself is one such component: any larger connected preimage component containing it lies in the same attracting Fatou basin, contradicting immediacy of U. The hypothesis excluding q from the other boundaries, together with q not belonging to their interiors, excludes q from each other closure. Finiteness supplies a neighborhood missing all of them. The contracting inverse H sends a sufficiently small disk into itself. For z in its U-side, h(H(z))=z forces H(z) into one of those preimage components; only U is available.

Finiteness alone does not provide the boundary exclusion. Intersections of distinct component boundaries are precisely the unremoved possibility. This argument is specifically rational; a finite global degree on the sphere is used.

### Corollary 5: application of Przytycki's good-point theorem — accepted

The imported result is Theorem A, not a direct invocation of the coding-tree theorem. I checked its good-point definition against the paper's printed p.260. The finite-density condition, strict pullback containment, diameter convergence, and basin-side pullback condition are all addressed. No extra complete-invariance hypothesis is silently inserted from the paper's abstract, and no coding-tree shrinking hypothesis is silently omitted from an application of Theorem D. [Przytycki (1994)](https://www.impan.pl/~feliksp/access.pdf)

Here is the independent component and constant check. After shrinking the ball V, H is defined beyond its closure, maps that closure strictly inward, and has Lipschitz constant rho<1 in the chosen local metric. Every H^k is therefore univalent beyond the closure of V. Its image H^k(V) lies in h^(-k)(V), and its boundary maps into the boundary of V. A path in h^(-k)(V) cannot exit through that boundary. Since open connected subsets of a surface are path connected, H^k(V) is exactly the global pullback component containing q, not merely a subset of that component.

Consequently B_(n,l)=H^(n-l)(V). With delta=(1-rho)r/2, one has rho^j r < r-delta for every integer j>=1. Delta is positive and smaller than r. Every positive n is good with Delta=1, so kappa=1/2 is valid for all sufficiently large counting intervals. The diameters are at most 2 rho^n r. Finally, if x in that pullback maps by h^n into U, its image w lies in V intersect U and x=H^n(w). Repeated local backward preservation keeps x in U. The argument checks all required basin-side information.

Passing to h=R^m preserves the relevant invariant immediate attracting basin. Accessibility is therefore justified in this restricted situation. The contrapositive is also correct: an inaccessible repelling boundary periodic point would have to share the boundary of another return-preimage component. The degree deficits D-d and D^m-d^m are correctly stated; zero deficit removes all other components.

### Lemma 6: hyperbolic-ball bound — accepted

With the stated curvature normalization, k_D(0,t)=log((1+t)/(1-t)), so the inverse radius is t=tanh(R/2). The normalized univalent growth estimate gives |w-z| <= |psi'(0)| t/(1-t)^2. Koebe's quarter theorem gives |psi'(0)| <= 4 dist(z,boundary U), in the required direction. Writing E=exp(R) gives t=(E-1)/(E+1), and the coefficient simplifies exactly to E^2-1. Thus the factor exp(2R)-1 is correct. No curvature-normalization factor is missing.

The reduction to a proper plane domain with q finite is legitimate after the empty and singleton-complement cases have been separated. This estimate is a classical analytic consequence, not proved by the finite checks.

### Proposition 7 and Corollary 8: controlled-chain landing — accepted

Hyperbolic geodesics exist in the simply connected hyperbolic domain. Every point of the nth segment is within hyperbolic distance R_n of its initial point. Because q is a boundary point, the Euclidean boundary distance of z_n is at most |z_n-q|. Adding the initial distance to q gives the uniform segment bound exp(2R_n)|z_n-q|. The chosen time intervals form a continuous concatenation; the assumed bound gives continuity at the final endpoint q.

If the ambient distance is at most C rho^n, a number strictly between the stated limsup and -log(rho)/2 makes the exponential upper bound decay. The strict inequality is essential and is preserved. The monomial example has the correct radial hyperbolic-distance formula and limit log(d). Schwarz–Pick yields nondecreasing backward increments; the packet correctly refuses to turn that lower-direction comparison into an upper bound for a merely local inverse.

Neither a suitable orbit staying in U nor the required intrinsic bound has been established in general. The result remains conditional.

### Lemma 9: cluster-address set — accepted

Compactness of the closed disk provides a subsequential inverse-coordinate limit for any sequence approaching q. An interior limit would place q in U by continuity, so the limit lies on the circle. The diagonal witness selection proves closedness. The finite Blaschke extension is available because conjugating a proper disk self-map gives a finite Blaschke product. Continuity of the return extension near the periodic orbit transfers witnesses to witnesses, proving forward invariance under B^m.

Only forward invariance is claimed, not surjectivity on S(q). The set is defined by arbitrary approach sequences; no radial-access assertion is concealed in its definition.

### Proposition 10: compact invariant aperiodic doubling set — accepted

Mechanical digits lie in {0,1}, and shifting the intercept by alpha gives the shift relation. Every original sequence has a predecessor obtained by subtracting alpha. Compactness and continuity extend this surjectivity to the closure X, so sigma(X)=X.

For each finite prefix, the telescoping count differs from N alpha by less than one. This remains strict on the closure: that finite prefix stabilizes along a convergent sequence and is an actual prefix of a generating word. Every member of X therefore has the same irrational limiting frequency of ones and cannot be eventually periodic. The binary-evaluation map is continuous and semiconjugates shift to doubling. Binary ambiguity would require eventual constant tails, which have already been excluded. A periodic doubling point has an eventually periodic binary expansion, yielding the contradiction.

This is a valid counterexample to an abstract circle-dynamic inference. It is not a demonstrated cluster-address set for any admissible holomorphic basin. The corrected subsequent paragraph preserves both missing analytic bridges.

### Lemma 11: slit-comb domain — accepted

The slits form a relatively closed subset of the open rectangle. Each allowed point has a vertical route to the upper corridor; horizontal routes in that corridor prove connectedness. The spherical complement is connected because each closed slit attaches to the connected exterior at the bottom side. The standard planar connected-complement criterion gives simple connectivity.

An access curve to (0,1/4) would eventually remain between heights 1/8 and 3/8. Its x-coordinate must cross one of the reciprocal-integer slit coordinates on the way to zero. The intermediate value theorem then forces a forbidden slit point. This proves inaccessibility without assuming the curve is simple. Conformal transport of z^2 does produce the stated proper attracting degree-two self-map of U, but supplies neither the needed extension nor a periodic boundary value at the inaccessible point.

### Proposition 12: analytic comb rigidity — accepted

A proper self-map is nonconstant, open, and onto U. Continuity of its extension sends every boundary point into the closure. If a boundary point mapped into U, its interior approximating sequence would eventually map into a compact disk contained in U, contradicting compactness of that disk's inverse image. Boundary preservation follows.

The boundary is contained in a countable union of closed supporting lines. For a compact interior subsegment of each slit, the inverse images of these lines form a countable closed cover. Baire gives a nontrivial interval on which one real coordinate of F is constant. Real analyticity extends that constancy along the whole slit subsegment. A nonconstant holomorphic function cannot be constant on a segment, so each subsegment is genuinely of a vertical-image or horizontal-image type.

Infinitely many source slits have the same type. In the vertical-image case differentiation in y gives Im(F')=0 on all of these slits; in the horizontal-image case it gives Re(F')=0. The extension around the compact accumulation segment supplies a uniform open rectangle across x=0. For each fixed y, the corresponding real-analytic function of x has infinitely many zeros accumulating at the interior point zero. It therefore vanishes on that interval. This makes F' real-valued or purely imaginary-valued on an open rectangle. The open mapping theorem forces F' to be constant. That rectangle meets U, and holomorphic continuation forces F to be affine throughout U. Its nonzero slope gives injectivity and hence proper degree one.

All important locations of the identity principles are interior to the extension domain. The proof would fail without extension across the accumulation side; it does not attempt that step merely from a boundary limit. If the extension is sphere-valued, the image of the compact closure is in the bounded closure of U, excluding poles there; shrinking its neighborhood validly reduces to the complex-valued argument.

## Primary-source and status review

- **IMS 1992/7:** printed p.29 supplies the simply connected attracting self-map setting. Printed p.30, Problem 1.1, uses all-periodic wording and includes the polynomial infinity basin in its comment. I checked the page image, including the infinity symbol. The historical comment also asserts a positive polynomial case; the packet preserves it without treating it as a separately verified neutral-point theorem. The catalogue's “Q2” label is not the printed identifier. [Primary collection](https://www.math.stonybrook.edu/preprints/ims92-7.pdf)
- **Przytycki 1994:** Theorem D on printed p.266 explicitly assumes repelling periodic dynamics, coding-tree shrinking and local basin-side preservation. Remark 0.7 discusses the missing preservation assumption. These do not justify deleting neutral points from the original question. Theorem A use is checked above. [Paper](https://www.impan.pl/~feliksp/access.pdf)
- **Roesch–Yin 2008:** Theorem 1 explicitly excludes components eventually mapped to a Siegel disk. Its bounded polynomial Jordan-boundary result supports the introductory imported case. The DOI resolver failed in this review, but the primary Numdam PDF opened successfully. [Primary PDF](https://www.numdam.org/item/10.1016/j.crma.2008.06.004.pdf)
- **Biswas:** The recovered PDF bears the v4 stamp dated 6 May 2013, and its Theorem 1.2 has the local inaccessible-fixed-point conclusion used. The public v4 PDF agrees in that relevant statement. No stronger all-impressions assertion from a different version is used. This local result supplies no global rational realization. [Version 4](https://arxiv.org/pdf/1010.4496v4)
- **Blokh–Oversteegen:** The conditional Lemma 5.3 and the scope of basic uniCremer polynomials are preserved. It is not an existence theorem for red-dwarf polynomials. [Paper](https://arxiv.org/pdf/0809.1071)
- **Blokh–Buff–Chéritat–Oversteegen:** Theorem 1.2 constructs solar examples; the following discussion treats red-dwarf existence as a remaining question. The 19-page recovered author-format copy and 20-page public arXiv version are explicitly distinguished. Both relevant statements were inspected. [Public arXiv paper](https://arxiv.org/pdf/0812.1239)
- **Supplementary sources:** The later Przytycki survey retains shrinking and basin-side conditions. Cheraghi's v5 Remark 8.16 distinguishes special high-type rational hedgehogs from arbitrary local germs; it supplies no general basin-accessibility theorem used here. [Survey](https://www.impan.pl/~feliksp/Siles.pdf), [Cheraghi v5](https://arxiv.org/pdf/1706.02678v5)

These bounded checks support the packet's modest conclusion: the five approaches did not solve the stated problem. They do not certify that no other author has resolved it or that any auxiliary deduction is historically new.

## Computational verification

The frozen author's standard-library program was inspected and rerun with both `--check-result` and `--check-manifest`. Its deterministic result matches: **5,963 assertions in 14 groups pass**, and all author-manifest entries match.

The separate `verify_independent_controls.py` does not import the author script. Its deterministic result has **26,958 assertions in 13 groups**, all passing. It extends the arithmetic and finite diagnostics as follows:

- Independently recomputes mechanical-word floors by binary search and exact squared inequalities, including negative and greater-than-one rational intercepts; checks shifted telescoping and discrepancy bounds.
- Rejects only the explicitly tested finite period candidates; infinite aperiodicity is justified by the written irrational-frequency proof.
- Checks degree deficits through global degree 30 and return exponent 12.
- Checks good-time constants for 99 contraction values and 50 pullback lengths.
- Checks the Koebe coefficient identity and exact disk automorphism test cases using rational Pythagorean directions.
- Builds derivative constraints with an independent binomial formula and full rational Gauss–Jordan elimination through polynomial degree eight. It verifies not only rank/nullity but the exact remaining coefficient freedom: two intercept coordinates and one allowed slope coordinate.

These computations are diagnostic. They do not certify compactness, convergence, Baire category, analytic continuation, any imported theorem, the infinite aperiodic set, or the original universal accessibility question.

## Exact unresolved gaps and publication-safe disposition

1. No global admissible realization of the local inaccessible hedgehog was constructed.
2. Competing inverse-basin component boundaries may still meet the requested repelling periodic point.
3. No general basin-side backward orbit with the required intrinsic-distance growth was found.
4. No periodic address for the requested q was forced, and no impression-to-landing identification bridge was supplied.
5. The explicit comb's degree-two transport does not extend across the closure; it is not an admissible dynamical counterexample.

Accordingly, the full target remains **unresolved in this packet**. Neutral points remain in scope. The corrected auxiliary note, explicit patch, control results, and public-source verification metadata are suitable to accompany that disposition. Original source documents, dataset contents, and private coordination materials must remain excluded. This audit performed no repository mutation or external publication.
