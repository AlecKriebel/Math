# Horikawa surface equivalence: five approaches and the remaining gaps

**Problem:** 2970 / KP-4.94. **Assessment:** partial results; both requested equivalences remain unresolved. **Research date:** 2026-10-08.

This report does not claim a new solution or a new diffeomorphism invariant. It supplies complete proofs of several restricted statements, a conditional symplectic obstruction, and explicit counterexamples to two proposed shortcuts. Several ingredients and the underlying strategies are already present in the literature; the purpose is to delimit what they actually prove. Source retrieval, literature review, and computation checks are not counted as approaches.

## 1. Exact target and conventions

The target is the comparison of the two deformation components of minimal complex surfaces on the Noether line, when their underlying spaces are homotopy equivalent. Use the complex orientation throughout. Write

- X_r = H(r): a double cover of F_0 branched over a smooth divisor of class 6s + 4rf, where s²=f²=0 and s·f=1;
- Y_r = H′(r): a double cover of F_{2r} branched over a smooth member C of |5Δ_0| together with Δ_∞, where Δ_∞²=−2r, Δ_0=Δ_∞+2rf, and C is disjoint from Δ_∞.

The unresolved comparison is **odd r≥3**, separately for smooth diffeomorphism and for the canonical symplectic structures. Even r gives different intersection-form parity and is outside the homotopy-equivalent question. The parameter r=1 is not part of this general-type family. The relevant invariants are

K²=8r−8, p_g=4r−2, χ(O)=4r−1, e=40r−4,
σ=−24r, b_2^+=8r−3, b_2^−=32r−3.

The family identification and open question are in [K3], Problem 4.94, pp. 267–268. The displayed AIM workshop-summary URL sometimes attached to this problem is not the full problem list.

The symplectic question uses the canonical structures normalized by [ω]=c_1(K), not arbitrary independent rescalings or arbitrary symplectic structures. Catanese's Theorem 1.3 [Cat] supplies their deformation invariance. This does not assert that every symplectic form in that cohomology class is isotopic to the canonical form.

An orientation-reversing diffeomorphism between X_r and Y_r cannot exist: it would give −24r=24r by invariance of the signature. Consequently allowing an unspecified orientation does not produce an extra positive case. A symplectomorphism would in particular give an orientation-preserving diffeomorphism. Equality of Seiberg–Witten or Donaldson invariants, as recorded in [K3], gives neither map.

## 2. Approach 1: retain the branched-cover marking and compute its integral lattice

**Attempt.** Try to distinguish the two smooth manifolds by the rank-two lattices visible in their canonical double covers. The outcome is an obstruction for marked manifolds, not yet for unmarked manifolds.

Let L_X=H²(X_r;Z), L_Y=H²(Y_r;Z), with their unimodular intersection pairings; the surfaces are simply connected. Set

U=π_X* s, V=π_X* f, Λ_X=ZU+ZV,
F=π_Y* f, R=[π_Y^{-1}(Δ_∞)], Λ_Y=π_Y*H²(F_{2r};Z).

Here all curve classes are identified with their Poincaré duals. The pullback of a branch component is twice its ramification curve. Therefore

U²=V²=0, U·V=2;
π_Y*Δ_∞=2R, R²=−r, R·F=1, F²=0;
Λ_Y=Z(2R)+ZF.

The canonical double-cover formula gives

K_X=U+(2r−2)V,
K_Y=2R+(3r−2)F.                                      (2.1)

### Proposition 2.1: saturation distinguishes the marked lattices

Λ_X is primitive in L_X. The saturation of Λ_Y is M_Y=ZR+ZF, and [M_Y:Λ_Y]=2. In particular no integral isometry L_Y→L_X can carry Λ_Y to Λ_X.

**Proof.** Degenerate the branch curve of X_r to six sections H_i in class s and 4r fibers V_j in class f, all meeting transversely. Blow up the 24r crossings. The strict transforms of the branch components are disjoint, so their double cover is smooth. Locally a crossing of the original branch curve yields an A_1 surface singularity; resolving it or smoothing it gives diffeomorphic smooth four-manifolds, with the pullbacks of the original base classes identified. This is the standard nodal double-cover construction used in [Aur, Remark 2.10]; the argument is independent of the number of fibers.

The ramification curves over H_1 and V_1 pair with aU+bV as b and a, respectively, by the projection formula. Hence if a rational combination aU+bV is an integral cohomology class, then a,b are integers. This is precisely primitivity of Λ_X.

The Gram matrix of R,F is [[−r,1],[1,0]], of determinant −1. An integral unimodular sublattice M of a unimodular lattice L is primitive: pairing any element of L with a basis of M gives an integral orthogonal projection to M, so L=M⊕M^⊥. Thus M_Y is primitive and, having the same rational span as Λ_Y, is its saturation. The displayed bases give index two. Isometries preserve saturation and its index. ∎

This general-parameter computation extends the particular r=3 calculation in [Aur, Proposition 2.11]; novelty is not claimed.

### Corollaries and limits

1. K_X is primitive. The divisibility of K_Y is gcd(2,3r−2), because M_Y is an integral direct summand. Thus Y_r is spin exactly when r is even, while X_r is non-spin for all r. This rederives the even-r obstruction without treating it as an answer in the odd-r range.
2. For odd r, F≡K_Y modulo 2, so the natural genus-two fiber F is characteristic. In contrast, V is not characteristic: primitivity of Λ_X makes U+V nonzero modulo 2, while K_X≡U. Therefore an oriented diffeomorphism cannot carry V to F. This is an obstruction for fiber-preserving maps, requiring no inference that every diffeomorphism preserves a chosen fibration.
3. The deck involutions are not conjugate. The fixed set on X_r is connected, of genus 20r−5; the fixed set on Y_r has two components, of genera 0 and 20r−4. Conjugacy would preserve the fixed-set components. Both fixed sets have Euler characteristic 12−40r, so the Euler characteristic alone misses the distinction. The genera follow directly from adjunction on the ruled bases.

**Remaining gap.** Neither a diffeomorphism nor a canonical symplectomorphism is known to preserve the canonical covering involution, Λ, or the natural genus-two fiber. Treating any of these as intrinsic to the smooth or symplectic manifold would assume the missing theorem.

## 3. Approach 2: replace the complex marking by the span of Lagrangian spheres

**Attempt.** Recover the lattice of Approach 1 using a symplectically defined collection. This leads to a precise conditional negative answer.

For a canonical symplectic surface (Z,ω), let E(Z,ω) be the rational span in H²(Z;Q) of the classes of all smoothly embedded Lagrangian two-spheres. A symplectomorphism carries E to E. Each such class A has A²=−2 and K·A=0: the normal bundle is identified by a compatible almost complex structure with the tangent bundle with reversed induced orientation, and ∫_Aω=0.

Put N_X=Λ_X^⊥ and N_Y=Λ_Y^⊥=M_Y^⊥, taking orthogonals in integral cohomology.

### Proposition 3.1: an exact missing hypothesis would distinguish the pair

If, for a fixed odd r≥3,

E(X_r,ω_X)=N_X⊗Q and E(Y_r,ω_Y)=N_Y⊗Q,                (3.1)

then the canonical symplectic manifolds are not symplectomorphic.

**Proof.** A symplectomorphism induces an integral isometry. Under (3.1), it carries the rational subspaces N_Y⊗Q and N_X⊗Q to one another, and hence their intersections with the integral lattices to one another. These intersections are exactly N_Y and N_X because integral orthogonal complements are saturated.

For a primitive nondegenerate sublattice M of a unimodular lattice L, |det M|=|det M^⊥|. For completeness, let N=M^⊥. Restriction of pairings gives an injection L/(M⊕N) into M*/M, and it is onto: every homomorphism M→Z extends to L→Z since L/M is free, and unimodularity identifies L with L*. Thus the index is |det M|. The same argument with N gives |det N|, proving the identity.

By Proposition 2.1, |det N_X|=4, while |det N_Y|=1. These lattices cannot be isometric. ∎

The saturation step matters. The unsaturated Λ_Y itself has determinant −4, just like Λ_X. Taking orthogonal complements first, or replacing Λ_Y by its saturation, is essential.

The Lagrangian-sphere strategy already appears in [Aur, Remark 2.12 and Section 8]. The present result is the explicit discriminant consequence, not a proof of that strategy's geometric hypothesis. In particular, a set of algebraic vanishing cycles is not automatically the set of all embedded Lagrangian spheres. A relation among Dehn twists or an immersed sphere does not give the required embedded sphere.

**Remaining gap.** Prove (3.1), or another intrinsic symplectic characterization that distinguishes the two saturated lattices. The elementary constraints A²=−2 and K·A=0 do not prove the required containment or span. No such identification is established here, even for r=3.

## 4. Approach 3: cancel the canonical-pencil partial conjugation

**Attempt.** In the smallest case, use the known partial twist to construct a Hurwitz equivalence. We tested whether membership of the conjugating element in the common monodromy group could justify cancellation. It cannot, as a group-theoretic principle.

For r=3, [Aur, Theorems 1.2–1.4] gives two canonical-pencil tuples of length 196, one obtained by conjugating a block of 64 factors by φ. The monodromy groups agree after identification, and analogous group equality survives degree doubling. These are source inputs, not new results of this report.

### Proposition 4.1: a finite exact counterexample to the cancellation principle

There exist two identity factorizations, with the same generated group, related by partial conjugation by an element of that group, which are inequivalent under Hurwitz moves and simultaneous conjugation.

**Proof.** Work in SL(2,F_3), and let G=SL(2,F_3)/{±I}. All matrices below have entries modulo 3. Define

A=[[1,1],[0,1]], B=[[1,0],[1,1]], P=[[0,1],[2,0]], C=AB.

Then A and B have order 3, C²=P²=−I, and PCP^{-1}=−C. The group generated by A,B is SL(2,F_3); this follows directly by elementary row operations, or from the exhaustive 24-element closure verified by the accompanying script. Let a,b,p denote their images in G, which has order 12.

Consider the tuples

T=(a,b,b^{-1},a^{-1}),
T′=(pap^{-1},pbp^{-1},b^{-1},a^{-1}).

Both have product 1, because p commutes with ab in G. Both generate G because the last two entries already generate G. Also p belongs to this same generated group. All factors have order 3.

Every order-three element of G has a unique lift of order 3 to SL(2,F_3): if Q³=I, then (−Q)³=−I. Thus the product of these distinguished lifts is an invariant of a tuple of order-three elements under Hurwitz moves. Indeed, the lift of xyx^{-1} is the conjugate of the distinguished lift of y by any lift of x, and the elementary Hurwitz replacement (x,y)↦(xyx^{-1},x) preserves the lift product. Simultaneous conjugation conjugates the lift product; when the product downstairs is 1, its lift product lies in the central group {±I}, so it is unchanged.

The distinguished-lift products of T and T′ are respectively

ABB^{-1}A^{-1}=I,
PABP^{-1}B^{-1}A^{-1}=−CC^{-1}=−I.

Therefore T and T′ are not Hurwitz-and-conjugation equivalent. ∎

This example does not claim to be a quotient of the actual Horikawa monodromy tuples. It disproves the proposed general implication, and identifies what additional information a real cancellation proof must use.

For orientation, a pencil in |kK| has

g_k=1+k(k+1)K²/2, n_k=k²K²,
N_k=e+K²(3k²+2k),

whenever the generic pencil is Lefschetz. Adjunction gives g_k, intersection gives its n_k base points, and e(blowup)=4−4g_k+N_k gives the last expression. For r=3,k=1 these are 17,16,196. These numerical data also agree and do not classify the tuples.

By [Aur, Corollary 2.5], the symplectic comparison can be made using equivalence of a suitable pluricanonical pencil. A proof of non-equivalence for only one low-degree pencil would not suffice for a negative symplectic answer; an obstruction must survive an unbounded sequence of degrees (or use another intrinsic symplectic invariant).

**Remaining gap.** Produce an actual Hurwitz equivalence for some pluricanonical degree, or an obstruction for the actual tuples that persists through arbitrarily high degrees. No homomorphism carrying the Horikawa tuples to the example above has been constructed. The finite example is a failed-shortcut certificate, not an obstruction for X_3 versus Y_3.

## 5. Approach 4: distinguish the manifolds by the negative ramification sphere

**Attempt.** The surface Y_r has the evident sphere R with

R²=−r, K_Y·R=r−2,

so one might try to prove that X_r has no sphere with these data. At r=3 this particular smooth obstruction fails explicitly.

### Proposition 5.1: both X_3 and Y_3 contain a smooth −3 sphere of canonical pairing 1

**Proof.** The assertion for Y_3 is immediate from (2.1). For X_r, use the nodal branch model from Proposition 2.1. A fiber V_j meets each of the six sections H_i, so its strict transform on the blown-up base has square −6. It is a smooth rational component of the now-disjoint branch divisor. Its ramification preimage S_j is a smooth rational curve, and

(2S_j)²=2(−6), hence S_j²=−3.

Let q be the blowdown to F_0. If L=3s+2rf is the half-branch line bundle on F_0, then on the blown-up base the half-branch class is q*L−ΣE and the canonical class is q*K_{F_0}+ΣE. Their sum is q*(s+(2r−2)f). The double-cover canonical formula and projection formula therefore give

K·S_j=(s+(2r−2)f)·f=1.

The resolution of the double-cover nodes is a smooth minimal Horikawa surface in the X_r deformation component; the ordinary-double-point smoothing/resolution identification preserves the canonical class. Thus this is a smooth sphere in the underlying manifold X_r with square −3 and pairing 1. Set r=3. ∎

There are 4r mutually disjoint curves S_j in this special model. This count is a property of that construction; it is not a proved maximality statement or a proposed smooth invariant.

There is a further numerical warning in every odd-r case. In the odd diagonal unimodular lattice I_{8r−3,32r−3}, take the characteristic vector K with coefficient 3 on 4r−1 positive basis vectors, coefficient 1 on the remaining 4r−2 positive vectors, and coefficient 1 on every negative basis vector. Its square is 8r−8. On r negative basis vectors choose A to have r−1 coefficients −1 and one coefficient +1. Then

A²=−r, K·A=r−2, A²+K·A=−2.

This exhibits formal sphere data compatible with the lattice and adjunction. It does not assert that this particular marked vector K has been identified with the actual canonical class, or that A is smoothly or symplectically representable. The explicit geometric −3 sphere above does not depend on that identification.

**Remaining gap.** A stronger representability or configuration invariant might still work, but simple smooth existence of the ramification sphere's numerical type cannot distinguish the smallest pair. The argument does not prove that S_j is symplectic for the normalized canonical form: the resolution model has canonical degree zero on its exceptional −2 curves, and replacing a Kähler form by the canonical symplectic form is a genuine additional issue. For r>3 no matching −r sphere construction or nonexistence result on X_r is claimed.

## 6. Approach 5: cross a common degeneration and compare the relative fillings

**Attempt.** Try to obtain a diffeomorphism by passing through the boundary of the moduli space. Two mathematically different obstacles occur: the proposed T-singular central fiber is unavailable for the target pairs, and a non-normal common central fiber does not itself determine the smoothing's smooth type.

For odd r≥3, p_g=4r−2≥10 and K²=8(r−1)>8. [MNU, Theorem 5.12] restricts KSBA limits with only T-singularities and at least one non-Du-Val singularity to the Lee–Park cases. Its Theorem 5.8 then puts the smoothings in the component whose general canonical image is F_0. That precise component description is preferable here to the paper's shorthand “nonspin component”: both of our odd-r smooth components are non-spin. Hence this route cannot provide a common T-degeneration for X_r and Y_r under those hypotheses. The theorem does not forbid arbitrary singularities or purely symplectic surgeries. Purely Du-Val canonical limits do not join the two smooth deformation components, since simultaneous resolution after base change stays in one smooth deformation class.

A later source changes the available degeneration route in the smallest case. [AEHK, Theorem 1.17] studies the moduli space of Q-Gorenstein smoothable **normal** stable Horikawa surfaces: it is connected exactly when p_g=6, p_g=10, or p_g−2 is not divisible by 4. For the present odd-r family this singles out r=3. Example 1.23 constructs a normal common limit at p_g=10 with an elliptic double cone singularity and smoothings to types (0) and (6). Section 1.5 explicitly leaves the differential-topological effect unresolved. For odd r≥5, the two components remain disconnected within this normal locus. This source is a preprint, not a claimed solution of the comparison problem.

The semi-smooth non-normal common degenerations in [RR, Theorem A and Theorem 3.4] give another route, outside the hypotheses of [MNU]. Neither kind of common central fiber by itself supplies a diffeomorphism.

### Proposition 6.1: this same degeneration mechanism cannot generally imply diffeomorphism

There are two Horikawa deformation components whose closures meet in the semi-smooth locus described in [RR], while their smooth members are not even homotopy equivalent.

**Proof.** Set r=4. Then K²=24=8·3, so [RR, Theorem A] applies, even if one uses the more restrictive ℓ>2 stated in the abstract instead of ℓ>1 in Theorem A. The two components have a common semi-smooth degeneration. But Proposition 2.1 and (2.1) show that X_4 is non-spin and Y_4 is spin. Their integral forms are odd and even respectively, so their smooth members are not homotopy equivalent, and a fortiori not diffeomorphic. ∎

This is a counterexample to the shortcut “common semi-smooth degeneration implies diffeomorphism”; it is not a counterexample to KP-4.94, whose homotopy-equivalence hypothesis excludes r=4.

Here is the exact cut-and-paste requirement a successful odd-r argument could meet. Suppose a chosen smoothing decomposition is

X=E_X∪_{a_X}F_X, Y=E_Y∪_{a_Y}F_Y,

where a_X:∂F_X→∂E_X and a_Y:∂F_Y→∂E_Y are attaching maps. If orientation-preserving diffeomorphisms e:E_X→E_Y and h:F_X→F_Y satisfy e∘a_X=a_Y∘h on their boundaries, after collar adjustment, they glue to an oriented diffeomorphism X→Y. This is proved simply by the common boundary formula and collars. The condition may be weakened to isotopy of these boundary maps, using the isotopy to adjust a collar.

The non-normal singular locus is a curve, so F_X,F_Y here need not be disjoint unions of isolated Milnor fibers. Identifying an exterior, or knowing a common central algebraic surface, leaves both the fillings and the attaching maps to control. For a symplectomorphism one further needs compatible symplectic gluing data; if a resulting diffeomorphism identifies canonical cohomology classes, Moser still needs a path of cohomologous symplectic forms. Equality of cohomology classes alone does not supply such a path.

**Remaining gap.** For the new normal r=3 common limit, compare the smoothings near its elliptic double cone singularity together with their boundary attachments. For the odd-r semi-smooth degenerations, compare the fillings along the non-normal locus. No required relative diffeomorphism has been obtained in either setting. The even-r example proves that compatibility cannot be inferred from the existence of a semi-smooth central fiber alone.

## 7. What has and has not been established

The five approaches were: integral cover-lattice recognition; intrinsic Lagrangian-sphere recovery; canonical-pencil Hurwitz cancellation; negative-sphere representability; and degeneration/relative-filling comparison. They are different mathematical mechanisms. The source review and arithmetic checks are separate supporting work.

**Unconditional results proved here:** the general-r saturation and fiber-characteristic computations; the resulting restrictions on marked equivalences; the finite partial-conjugation counterexample; the matching smooth −3 spheres at r=3; and the even-r counterexample to a common-degeneration shortcut. The lattice argument is a generalization of a known calculation, and the construction and degeneration inputs are cited. No novelty priority is asserted.

**Conditional result:** the Lagrangian rational-span hypothesis (3.1) would obstruct canonical symplectomorphism via discriminants 4 and 1.

**Not established:** a diffeomorphism, a symplectomorphism, or an obstruction to either for any odd-r pair. No number of agreeing numerical invariants fills that gap. No source inspection is treated as a proof of a new theorem or as evidence that an unpublished solution cannot exist.

## References

- [K3] R. İnanç Baykur, Robion C. Kirby, Daniel Ruberman, *K3 — A New Problem List in Low-Dimensional Topology*, author's preliminary book version, Problem 4.94, pp. 267–268. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [Aur] Denis Auroux, *The canonical pencils on Horikawa surfaces*, Geometry & Topology 10 (2006), 2173–2217. https://doi.org/10.2140/gt.2006.10.2173 ; published-version arXiv copy: https://arxiv.org/abs/math/0605692v2
- [Cat] Fabrizio Catanese, *Canonical symplectic structures and deformations of algebraic surfaces*, Communications in Contemporary Mathematics 11 (2009), 481–493. https://doi.org/10.1142/S0219199709003478 ; https://arxiv.org/abs/math/0608110v2
- [MNU] Vicente Monreal, Jaime Negrete, Giancarlo Urzúa, *Classification of Horikawa surfaces with T-singularities*, arXiv:2410.02943v3, revised July 2025. https://arxiv.org/abs/2410.02943v3
- [RR] Julie Rana, Sönke Rollenske, *Standard stable Horikawa surfaces*, Algebraic Geometry 11 (2024), 569–592. https://doi.org/10.14231/AG-2024-017 ; https://api.algebraicgeometry.nl/Article/20577/2024-4-017.pdf

- [AEHK] Hiroto Akaike, Makoto Enokizono, Masafumi Hattori, Yuki Koto, *Normal stable degenerations of Noether-Horikawa surfaces*, arXiv:2507.17633v1, July 2025. https://arxiv.org/abs/2507.17633v1
