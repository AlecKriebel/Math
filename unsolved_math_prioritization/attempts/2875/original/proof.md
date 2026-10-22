# Rational homology spheres as orientable geometric boundaries

## 1. Exact target and disposition

This is catalog ID 2875, modern K3 Problem 3.77, rank 916. The target is the existence of a connected closed hyperbolic 3-manifold M with H_*(M;Q) isomorphic to H_*(S^3;Q), and a compact orientable hyperbolic 4-manifold W whose entire boundary is M and is totally geodesic. One may require W connected by retaining the component containing M. Curvature is normalized to -1. There is no assumption that W is a rational homology ball, simply connected, or arithmetic.

The relevant problem is the modern K3 question on printed p.186, not the differently numbered problem in the 1997 list. A boundary component among several components, a cusped filling, a flat cusp section, an immersed hypersurface, or a smooth separating hypersurface without the totally geodesic condition does not satisfy the target.

**Disposition: unsolved in this investigation, four substantive approaches.** The results below are structural obstructions to specific proposed constructions and necessary conditions. No general nonexistence theorem, example satisfying the target, novelty claim, or exhaustive current-literature claim is made.

## 2. Attempt 1: the one-boundary involution construction

Ferrari, Kolpakov and Reid [FKR, Theorem A] construct infinitely many rational homology 3-spheres bounding compact hyperbolic 4-manifolds. Their introduction explicitly retains nonorientability of the 4-manifolds as the gap. Their Lemma 3.1 cuts along an embedded hypersurface and, in the two-boundary case, identifies one boundary component with itself by a free isometric involution. The resulting manifold is orientable precisely when this involution reverses orientation. The following standard obstruction is already explained in [FKR, Introduction and Lemma 7.10]; it is included with proof to make the failure exact.

### Proposition 2.1 (credited free-involution obstruction)

A closed rational homology 3-sphere M has no fixed-point-free orientation-reversing involution.

Proof. Suppose tau is such an involution and let X=M/<tau>. This is a closed connected nonorientable 3-manifold and M -> X is a two-sheeted covering. The transfer on rational homology has composite with projection equal to multiplication by 2. Consequently H_i(X;Q) injects into H_i(M;Q), so b_1(X)=b_2(X)=0. Since X is connected and nonorientable, b_0(X)=1 and b_3(X)=0. Thus chi(X)=1. On the other hand Euler characteristic is multiplicative under a finite covering, and chi(M)=0, giving 2 chi(X)=0. Contradiction. All these assertions apply to compact smooth manifolds with their finite CW structures. QED.

For completeness, the orientability test in the gluing construction is local. In a collar of the identified boundary the transition between the two incident half-collars reverses the normal coordinate and acts on the tangential coordinates by tau. Its total orientation sign is -deg(tau). The existing orientation extends across this identification exactly when deg(tau)=-1. A free involution avoids fixed-point singularities, but Proposition 2.1 rules out the sign needed here.

This does not show that M cannot geometrically bound an orientable W by a different construction. In particular, if a geodesic embedding is already separating, the desired side exists without any self-identification.

## 3. Attempt 2: orientable covers and boundary-pair gluing

### Proposition 3.1 (cover obstruction)

Let W be a connected compact nonorientable manifold with a single connected orientable boundary M. Every connected orientable finite covering V -> W has at least two boundary components. The orientation double cover W^+ -> W has boundary consisting of exactly two copies of M.

Proof. A collar gives TW restricted to M as TM plus a trivial normal line. Its first Stiefel-Whitney class restricts to zero because M is orientable. The orientation cover restricted to M is therefore the trivial two-sheeted cover M disjoint-union M. The orientation cover W^+ is connected because W is nonorientable.

Write the orientation character as w:pi_1(W)->Z/2. An orientable covering V corresponds to a subgroup contained in ker(w), so it factors through W^+. The intermediate map V->W^+ is a nonempty connected covering of a connected manifold, hence is onto. Both components of the boundary of W^+ therefore have nonempty inverse images. These are disjoint open-and-closed subsets of the boundary of V, so that boundary cannot be connected. QED.

For the nonorientable compact FKR examples, W^+ inherits a hyperbolic metric and two totally geodesic boundary copies of the original rational homology sphere. Thus passing to the orientation double cover repairs orientability but loses the single-boundary requirement. Proposition 3.1 excludes repairing this merely by any further connected orientable finite covering of the original W.

It does not say that every such higher cover has an even number of boundary components, or that each lifted component is a rational homology sphere. Neither additional claim is needed or made.

### Proposition 3.2 (even-boundary gluing obstruction)

Start with finitely many connected compact orientable pieces, each having an even number of boundary components, all closed rational homology 3-spheres. Permit only the following operations: glue two distinct whole boundary components by a diffeomorphism, or identify one whole boundary component by a fixed-point-free involution. If the resulting manifold is orientable, every connected component of it has an even number of remaining boundary components.

Proof. A self-identification of a rational homology sphere cannot preserve orientability by Proposition 2.1 and the collar sign test. An orientation on the final connected component would restrict to an orientation on every original piece in it, so choosing different initial orientation labels cannot avoid that obstruction.

Only pair gluings remain. A final connected component is assembled from some collection of whole initial pieces. If their boundary counts are 2r_1,...,2r_s and e pairs are glued within that collection, its number of remaining boundary components is 2(r_1+...+r_s-e), which is even. Pair gluing within a previously connected piece has the same count. QED.

Consequently finite copies of the orientation double covers, using just these operations, cannot yield one boundary. This is a limitation of the stated operation class, not of arbitrary hyperbolic constructions. Cutting along new hypersurfaces, using pieces with odd boundary counts, or changing the geometric construction lies outside the proposition.

## 4. Attempt 3: separating geodesic embeddings and tubing

### Proposition 4.1 (exact separating-embedding reformulation)

A closed connected hyperbolic 3-manifold M is the entire totally geodesic boundary of a compact orientable hyperbolic 4-manifold if and only if it has an isometric, separating, totally geodesic embedding in a closed orientable hyperbolic 4-manifold.

Proof. Double a connected bounding W along its boundary, using a second copy with reversed orientation. The identity gluing respects the boundary orientations required for an oriented double. Reflection across a totally geodesic hyperplane in the hyperbolic local model shows that the doubled metric is smooth with sectional curvature -1. The result is closed, hence complete, and M separates its two interiors.

Conversely, a separating embedded orientable hypersurface in an orientable manifold is two-sided. The closure of either complementary component of the closed ambient manifold is compact and orientable. Its sole boundary is M because M is connected and the ambient manifold has no other boundary. The inherited metric has curvature -1 and totally geodesic boundary. QED.

The isometric qualifier keeps the prescribed hyperbolic metric visible. This reformulation is elementary and does not construct the required separating embedding.

Battista, Ferrari and Santoro [BFS, Lemma 3.11] have a disconnected separating totally geodesic hypersurface made of 2^k copies of a dodecahedral rational homology sphere. In Proposition 3.13, Step 3, they connect those copies by tubes. The resulting smooth separating hypersurface is a connected sum of 2^(k-1) copies of M and 2^(k-1) oppositely oriented copies. This proves their stated L-space application, but it does not provide the geodesic hypersurface required by Proposition 4.1.

### Proposition 4.2 (tubing loses hyperbolicity)

A connected sum of at least two closed hyperbolic 3-manifolds, with any choices of orientation, is a rational homology 3-sphere if each summand is, but admits no hyperbolic metric.

Proof. Mayer-Vietoris for connected sum gives the direct sum of the summands' rational homology in degrees one and two. Connectedness and orientation give the required degree-zero and degree-three groups. Thus it is a rational homology sphere.

The connected-sum sphere separates two punctured connected sums having nontrivial fundamental groups: each hyperbolic summand has infinite fundamental group, puncturing does not change it, and van Kampen gives free products for additional summands. Neither side can be a 3-ball. The sphere is therefore essential. But a complete hyperbolic 3-manifold is irreducible: its universal cover is H^3, homeomorphic to R^3, and irreducibility descends under coverings (the standard covering criterion recorded by Hatcher [H, Proposition 1.6]). This contradicts the essential sphere. QED.

A totally geodesic hypersurface in a hyperbolic 4-manifold has the induced constant-curvature -1 metric by the Gauss equation. Therefore the connected sum in Proposition 4.2 cannot be made totally geodesic by an isotopy in the same ambient metric, or by assigning it any hyperbolic metric. Merely obtaining a connected smooth separator preserves the rational homology condition but fails the geometric condition. The case of one summand would not have this obstruction and is not claimed excluded.

## 5. Attempt 4: signature, homology, and volume constraints

Let W be a hypothetical connected witness and orient M=boundary(W) by the boundary orientation. Put b_i=dim_Q H_i(W;Q), and use the eta-invariant normalization of Long and Reid [LR].

### Proposition 5.1 (necessary numerical conditions)

The following hold:

- b_3=b_1, and the rational intersection form on H_2(W;Q) is nonsingular;
- chi(W)=1-2b_1+b_2 is a positive integer, so b_2>=2b_1;
- signature(W)=-eta(M), hence eta(M) is an integer;
- b_2>=|eta(M)| and b_2 is congruent to eta(M) modulo 2;
- Vol(W)=(4 pi^2/3) chi(W).

Proof. In the rational long exact sequence of (W,M), the boundary map H_4(W,M)->H_3(M) sends the relative fundamental class to the boundary fundamental class. Both spaces are Q and the map is an isomorphism. Since H_2(M)=0, it follows that H_3(W)->H_3(W,M) is an isomorphism. Poincare-Lefschetz duality identifies the latter with H^1(W), proving b_3=b_1. Also H_2(M)=H_1(M)=0 makes H_2(W)->H_2(W,M) an isomorphism, yielding a nonsingular intersection form. Since b_0=1 and b_4=0, the Euler-characteristic formula follows.

Double W as in Proposition 4.1. Its volume is twice that of W and its Euler characteristic is 2 chi(W)-chi(M)=2 chi(W). The closed hyperbolic four-dimensional Chern-Gauss-Bonnet formula gives Vol(double(W))=(4 pi^2/3) chi(double(W)), proving the volume formula and strict positivity of chi(W).

Long-Reid's proof of Theorem 1.1, printed p.174, applies the signature formula with vanishing hyperbolic Pontryagin form and vanishing totally-geodesic-boundary correction. It gives signature(W)=-eta(M). This is a cited theorem, not a new spectral calculation. A real nonsingular symmetric form with positive and negative indices p,q has rank p+q and signature p-q. Its rank is at least the absolute signature and has the same parity, giving the remaining statements. QED.

These constraints are not sufficient. At the purely numerical level any integer e can satisfy them: take b_1=b_3=0, b_2=|e|, signature=-e, and chi=1+|e|. A diagonal form of the appropriate sign has that rank and signature (use the zero-dimensional form when e=0). This supplies only formal numerical data, not a manifold, metric, eta computation, or candidate solution. In particular one must not add a rational-homology-ball requirement on W, and one must not treat integral eta as a geometric-filling theorem.

## 6. Exact remaining gap and stopping decision

The four approaches do not produce a compact orientable hyperbolic 4-manifold with one rational-homology-sphere geodesic boundary, nor exclude all possible such manifolds. What is missing is a construction realizing all those conditions together, equivalently the connected separating totally geodesic embedding of Proposition 4.1, or a universal obstruction going beyond the necessary conditions above.

The involution obstruction is credited prior work. Covers alone retain multiple boundaries; the narrowly specified even-boundary gluing operations cannot reduce to one; tubing produces a reducible 3-manifold; and the signature/homology/volume constraints leave consistent formal data. No concrete next construction or uniform contradiction was found. The investigation stops at this stalled partial result rather than counting further variants as substantive approaches.

## References and inspection scope

[K3] R. I. Baykur, R. C. Kirby, D. Ruberman (eds.), K3: A New Problem List in Low-Dimensional Topology, author preliminary version, modern Problem 3.77, printed p.186; also Problem 4.126, Remark (3). https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[FKR] L. Ferrari, A. Kolpakov, A. W. Reid, Infinitely many arithmetic hyperbolic rational homology 3-spheres that bound geometrically, Trans. Amer. Math. Soc. 376 (2023), 1979-1997. https://doi.org/10.1090/tran/8816 ; author offprint https://math.rice.edu/~ar99/FKR_Trans.pdf . Inspected introduction, Theorem A, Lemma 3.1 and Lemma 7.10. The paper's group computations were not rerun or independently audited.

[BFS] L. Battista, L. Ferrari, D. Santoro, Dodecahedral L-spaces and hyperbolic 4-manifolds, Commun. Anal. Geom. 32(8) (2024), 2095-2134. https://doi.org/10.4310/CAG.241212004157 ; inspected arXiv:2208.01542v2, pp.1-3 and 18-22, especially Proposition 3.13, Step 3. https://arxiv.org/abs/2208.01542 . Their computer-assisted L-space and manifold calculations were not rerun or independently audited.

[LR] D. D. Long, A. W. Reid, On the geometric boundaries of hyperbolic 4-manifolds, Geom. Topol. 4 (2000), 171-178. https://doi.org/10.2140/gt.2000.4.171 ; published-copy PDF https://arxiv.org/pdf/math/0007197 . Inspected Theorem 1.1 and its oriented signature-formula proof, plus the volume formula on p.175. No eta-invariant was computed here.

[H] A. Hatcher, Notes on Basic 3-Manifold Topology, Proposition 1.6 (irreducibility descends under a covering), standard background. https://pi.math.cornell.edu/~hatcher/3M/3M
