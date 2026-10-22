# Independently checkable geometry and cusp derivations

This artifact was formed from the frozen candidate and primary papers without reading original or other fresh review verdicts. It checks the physical and imported-theorem parts of the route. It does not replace a separate audit of the affine angle-index lemma.

## 1. Why a physical reflection lands in a translate of the half-turn polygon

Center the regular polygon P at the origin. Let its j-th side midpoint be c_j, and let H_j denote reflection in the line through 0 and c_j. This is a symmetry of P. Reflection in the parallel-to-side line through 0 is -H_j; reflection in the actual side line is therefore

    S_j(z) = 2 c_j - H_j z.

Consequently S_j(P)=2c_j-P. More generally, reflecting a developed copy t+epsilon P, epsilon in {+1,-1}, across its j-th side produces

    (t+2 epsilon c_j) - epsilon P.

The shapes alternate between translates of P and -P. At the common side, the two coordinate representatives differ by a translation. If that side has endpoints p_j,p_{j+1}, translation by p_j+p_{j+1}=2c_j takes the side with endpoints -p_j,-p_{j+1} to the side with endpoints p_{j+1},p_j. This proves exactly the reversed-endpoint translation gluing used in the candidate.

A side-interior encounter is a regular point of the glued surface. All polygon corner images are the vertex set Sigma. Thus a physical path whose next vertex encounter is its endpoint projects to a straight segment from Sigma to Sigma with no interior point of Sigma. Conversely, every local corner germ on the doubled surface folds to a billiard germ, with its first Sigma encounter corresponding to the first physical vertex. Length is preserved because every developed-copy chart is an isometry. For n=3,4 the images of corners must be kept as marked regular points; calling them ordinary singularities would be incorrect.

The construction does not require the full labelled Katok-Zemlyakov unfolding to consist of only two polygons. It uses its translation quotient; forgetting the reflected vertex labels is harmless for the stopping condition, but the physical orientation frame must be retained when recovering source type.

## 2. Corner cycles and exceptional surfaces

With clockwise compatible labels, gluing P_jP_{j+1} to Q_jQ_{j+1} identifies P_j with Q_{j+1} and P_{j+1} with Q_j. The successor permutation in the cone cycle is

    (sheet,j) -> (1-sheet,j+1 mod n).

For odd n this has one cycle of length 2n. For even n it has two cycles of length n. Multiplication by the corner angle (n-2)pi/n gives cone angles 2pi(n-2) and pi(n-2), respectively. With two faces and n edge classes, Euler characteristic gives genus (n-1)/2 and (n-2)/2, respectively.

Examples worth preserving:

| n | double-surface genus | vertex classes | angle at each vertex class |
|---|---:|---:|---:|
| 3 | 1 | 1 | 2pi (regular, marked) |
| 4 | 1 | 2 | 2pi (regular, marked) |
| 5 | 2 | 1 | 6pi |
| 6 | 2 | 2 | 4pi |
| 8 | 3 | 2 | 6pi |
| 10 | 4 | 2 | 8pi |

In particular the doubled octagon has genus 3 and two singularities; the opposite-side single octagon has genus 2 and one singularity. Their Veech group equality does not identify their vertex data. No proof of source type may silently substitute the smaller surface.

The half-turn exchanging sheets sends (sheet,j) to (1-sheet,j). It fixes the odd vertex class and exchanges the two even vertex classes. Its regular fixed points are exactly the n glued side midpoints. Together with the odd vertex point, these give 2g+2 fixed points for n>=5. This corroborates the candidate's hyperelliptic-surface setup without checking its subsequent angle-index identification.

## 3. Exact model-direction exhaustion by chords

Let ell be a reflection axis of a convex regular polygon and let d be perpendicular to ell. For each vertex v not on ell, its reflected vertex H(v) is distinct and H(v)-v is parallel to d. The line through these two vertices intersects the convex polygon exactly in the segment [v,H(v)]: strict convexity of the regular polygon at vertices excludes any continuation within the polygon past either endpoint. Therefore the unique inward or boundary ray from v parallel to d reaches H(v) without hitting any side interior first.

A vertex on ell lies at an extremum of the coordinate along ell. Its perpendicular line is supporting, so neither ray has an interior portion in the polygon. For a boundary ray along a side, the side endpoint is the next marked vertex; it cannot continue through that endpoint as a short trajectory.

Every outgoing cone germ belongs to one of the polygon corners in a cone cycle. Applying the argument to each such corner of P and Q exhausts all short connections in direction d. A model connection can never pass from one polygon interior to another through a side interior: it already reaches the reflected vertex in its first polygon. Boundary germs give the glued side connections. This is a geometric exhaustion proof, independent of an unlabelled length spectrum.

The chord joining vertices separated by j steps has length 2R sin(j pi/n). Fuchs's own direct-chord example on p.503 assigns it type A_(j-1), with the two side cases j=1,n-1 both yielding A_0 after residue reduction. Thus the model connection length is 2R w_n(k). A chord placed in Q can be folded by a Euclidean reflection; the physical type may have its orientation convention reversed, but its sine weight agrees because the chord and its folded image have the same step separation up to j -> n-j.

## 4. Imported cusp data and why it applies to the doubled even surface

Primary source verification:

- Finster, *A series of coverings of the regular n-gon*, arXiv:1005.4588v3, section3.1, printed pp.4-6: the odd double polygon is the surface obtained by translation gluing parallel sides; group generators are R (rotation pi/n) and T=[[1,2cot(pi/n)],[0,1]], and Remark3.2 gives signature (2,n,infinity). This is one cusp.
- Finster section3.2, printed pp.7-8: its even X_n is the smaller opposite-side polygon, but the paragraph invoking Hubert-Schmidt LemmaJ explicitly states equality with Veech's double-n-gon group for even n>=8. The group is generated by T and R^2, and Remark3.5 gives signature (n/2,infinity,infinity). This is two cusps. This explicit equality is stronger than an unjustified inference from the existence of a cover.
- Finster printed p.20, proof of Corollary4.4: the BASE group Gamma(X_n)=<T,R^2> has cusp representatives infinity and {-cot(pi/n),cot(pi/n)}. The later cover group Gamma_n, which has (n+2)/2 cusps, is a different group.
- Boulanger-Lanneau-Massart, *Algebraic intersection for a family of Veech surfaces*, section1.4, printed p.791: the correspondence between saddle-connection directions and cusps is stated for Veech surfaces generally. Its subsequent one-cusp family statement concerns its odd double-polygon family, and must not be applied as an even one-cusp theorem.
- Hubert-Schmidt, *Invariants of translation surfaces*, Ann. Inst. Fourier51(2),2001, LemmaJ, printed p.473: the opposite-side regular 2n-gon is balanced translation double covered by the (1,1,2n-2) triangle surface, with isomorphic Veech groups. This is the direct primary statement behind Finster's cited equality. TheoremA (printed p.470) records the corresponding Veech triangle signatures.

To convert Finster's boundary coordinates to directions, use the convention [x:y] -> x/y. Infinity is the horizontal vector (1,0). The point cot(a), a=pi/n, is the vector (cos a,sin a), at angle a from horizontal. T sends -cot(a) to +cot(a), so the two signs are the same second cusp. Both directions are perpendicular to axes of reflection of the regular polygon in the relevant orientation. Conjugating polygon orientation conjugates the Veech group and rotates both directions together.

For any saddle-connection direction, the general cusp theorem places its projective direction in a parabolic fixed-point orbit. The one or two cusp representatives above therefore give an orientation-preserving affine map carrying that direction to a model direction. By definition of Veech group its derivative is realized by an affine automorphism of the doubled surface. The same automorphism acts on every connection in that direction. If their unoriented direction is represented by v, their lengths are all multiplied by ||Av||. This supports the reduction, subject to the separately checked preservation of the source type weight.

No use is made of the n=6 extension of these nonarithmetic group computations. No use is made of Fuchs Conjectures2.3,2.4,2.6.

## 5. Elementary n=3,4,6 proofs

For n=3, reflection tiling is the triangular lattice. Every straight ray through two lattice points has a unique primitive integer direction v; its next vertex is v. The relevant rotations and reflections preserve both its norm and primitivity, so parallel short trajectories have equal lengths. Type has a single value.

For n=4, use the square lattice and primitive v=(p,q). Its next vertex is v. Under square direction symmetries, (p,q) changes by signed coordinate permutations, preserving norm, gcd and the condition that both coordinates are odd. Fuchs p.506 assigns A_1 precisely to that condition and A_0 otherwise. Every parallel family therefore has the same length and same weight.

For n=6, in the 120-degree basis u=(1,0),v=(-1/2,sqrt(3)/2), the squared norm of (p,q) is Q=p^2+q^2-pq. The honeycomb vertices based at the initial vertex satisfy p+q !=2 mod3. A primitive triangular-lattice ray has all its lattice points at integral multiples of its primitive vector. Therefore its first honeycomb vertex is the primitive vector when s=p+q is0 or1 mod3, and twice that vector when s=2 mod3.

The source's type rules then give:

| primitive s mod3 | first vertex | source type | w_6^2 | L^2/w_6^2 |
|---|---|---|---|---|
| 0 | v | A_1 or A_3 | 3/4 | 4Q/3 |
| 1 | v | A_0 | 1/4 | 4Q |
| 2 | 2v | A_2 | 1 | 4Q |

A primitive vector with s=0 cannot have both coordinates divisible by3, so its residues are(1,2) or(2,1). A primitive vector with s=1 is not both even. For s=2,2v has both coordinates even and coordinate sum1 mod3. These are exactly the p.506 rules.

The generators (p,q)->(q,p) and (p,q)->(p-q,p) preserve Q and gcd. They send s to s or -s modulo3. Thus s=0 remains its own family, while s=1 and2 may interchange. The displayed L^2/w^2 is invariant in both situations; positivity gives the desired length-weight ratio. This establishes n=6 directly with the true honeycomb marked-vertex set, rather than falsely treating every triangular-lattice point as a vertex.

## 6. Reproducible controls and their limits

Run the two programs from this directory's parent case:

    python3 geometric_cusp_review/artifacts/check_geometry.py
    python3 geometric_cusp_review/artifacts/physical_billiard_smoke.py

The first uses exact integer and rational operations. It checks all corner cycles and reflection-orbit partitions for 3<=n<=200, and primitive lattice vectors with coordinates bounded by100. Its results are recorded in `artifacts/geometry_checks.json`. The second implements physical reflection at side interiors, classifies endpoints from the literal source Definition2.1 branches with the segment-parity filter, and compares L/w for selected common slopes. It checks704 paths for n=5,7,8,9,10,11,12,14, with up to17 segments; worst relative spread is less than2e-14. It uses floating point and is only a falsification smoke control, recorded in `artifacts/physical_billiard_smoke.json`.

The all-n conclusions in sections1-5 come from the analytic derivations and explicitly identified classical theorems. Neither finite program proves the Veech/cusp imports, and neither independently certifies the affine-invariant index identification in the candidate's section3.

## 7. Required repair: physical source type versus intrinsic cone index

After the independent mechanism above was formed, the coordinating reviewer supplied an independently found reversal witness. The following is a direct geometric derivation of the repair; it is not an assumption of an unproved new invariant.

Let k denote the physical Fuchs type, and let kappa denote the candidate's cone index (the right-hand side of equation(8)). The candidate's corner calculation normalizes the initial corner to P_0; its asserted identification should be restricted to P-starting connections. A connection starting in Q has a different physical orientation frame.

The exact physical transformation laws follow directly from the endpoint angles:

1. **Physical trajectory reversal.** Its angles become alpha'=pi-beta and beta'=pi-alpha. If N is even, beta'-alpha'=beta-alpha, hence k'=k. If N is odd, alpha'+beta'=2pi-(alpha+beta), hence s'=n-s in the sum branch and k'=-k modulo n-2. Thus k'=(-1)^N k; the candidate's unconditional physical reversal rule k'=-k is false.
2. **Physical polygon reflection.** Put delta=(n-2)pi/n. Reflection reverses the local orientation frame, giving alpha'=delta-alpha and beta'=(n+2)pi/n-beta. For odd N, s'=n-s, so k'=-k. For even N, s'=2-s, so k'=1-s=-k. Thus global polygon reflection changes physical k to -k for both parities. Polygon rotations preserve physical k.

Now let gamma begin in Q. A physical folding map from its initial Q copy to the original P is S=-H, where H is a reflection symmetry of P (section1). The half-turn iota maps Q to P by -I, and

    S = H compose iota.

Consequently the folded physical billiard path of gamma is a polygon reflection H of the physical billiard path of iota(gamma), which starts in P. This holds for the entire path: their initial germs agree after H, and billiard reflection in side interiors is equivariant under a polygon isometry and determines subsequent segments uniquely until the first vertex.

Assume the separately audited P-starting identification k(iota(gamma))=kappa(iota(gamma)). The candidate's cone invariant is preserved by iota, as by every orientation-preserving affine map. The polygon-reflection law just proved then gives

    physical k(gamma) = -kappa(gamma) if gamma starts in Q,
    physical k(gamma) = +kappa(gamma) if gamma starts in P.

An equivalent formal description uses a starting-sheet sign epsilon=+1 on P and -1 on Q, so k=epsilon*kappa. Since w_n(-k)=w_n(k), the physical and intrinsic weights agree in either sheet. Therefore an affine map preserving kappa preserves the physical type **weight**, even if it moves the initial corner into Q and reverses the exact physical residue. This is all that the model-direction length-ratio argument requires.

Intrinsic connection reversal sends kappa to -kappa. The terminal sheet is the starting sheet for odd N and the opposite sheet for even N. Thus epsilon_end/epsilon_start=(-1)^(N-1); combining sheet sign and cone reversal gives physical k'=(-1)^N k, exactly matching the endpoint-angle calculation. No contradiction remains after distinguishing k from kappa.

**Concrete pentagon witness.** Take the unit-side regular clockwise pentagon with P_0=(0,0), P_4=(1,0), and send a ray vertically upward from P_0. Put B=(0,2sin(pi/5)), the intersection with side1 (P_1P_2). The reflected direction is -pi/10, and it meets side3 (P_3P_4) at C=(5/4,tan(2pi/5)/4). That encounter is perpendicular to side3, so the path retraces to B and then to P_0. The path is

    P_0 -> B -> C -> B -> P_0,

with N=4 segments, side-interior reflection word[1,3,1], and alpha=beta=pi/2. Its physical type is k=-1 mod3=2. Its physical reverse is the same billiard path, still type2; the candidate's blanket rule would predict type1. Both weights coincide, sin(3pi/5)=sin(2pi/5). This falsifies an intermediate exact-type assertion, not Conjecture2.7.

**Required candidate edits.** Introduce separate notation kappa for the intrinsic cone index; state equation(8) as k=kappa for P starts and k=-kappa for Q starts under physical folding; replace unconditional physical type invariance by weight invariance; state physical reversal k'=(-1)^N k. Keep cone reversal kappa'=-kappa. In section4, after applying an affine map, use the just-proved weight equality to compare the model chord's physical weight with the original path. The geometric/cusp route then needs no additional central theorem beyond the P-starting angle-index identification already claimed in section3.
