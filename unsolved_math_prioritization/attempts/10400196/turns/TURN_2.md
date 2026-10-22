# Turn 2: a canonical odd-primary construction and a non-torsion obstruction

**Original unrestricted target remains unresolved.** The positive theorem below covers every Spin^c structure on a rational homology sphere of odd first-homology order. It is a genuine degree-one construction using the classical spin Rochlin invariant, not a branch choice for a degree-zero phase. All classical inputs are credited; no novelty assertion is made.

## 1. Fixing the sign and target before constructing the lift

The source sentence uses the convention that the spin Gauss–Brown invariant B is R modulo8. Massuyeau's *Spin Borromean surgeries*, Lemma12, instead writes B(phi_s)=-R(M,s) modulo8, with his linking-pairing convention; the published Deloup–Massuyeau construction agrees with that phi_s. The discriminant and boundary-linking conventions differ by a sign. The two conventions must not be silently mixed.

We therefore use a fixed sign epsilon∈{+1,-1} and choose the quadratic convention so that

    B(q_s)=epsilon R(M,s) modulo8.

Taking epsilon=+1 matches the relationship stated in Ohtsuki's Question10.21 discussion. Taking epsilon=-1 uses the published Massuyeau/Deloup–Massuyeau quadratic convention without changing it. Negating all quadratic functions exchanges the conventions. The theorem is valid in either convention with this sign retained.

The target is Q/16Z and reduction to B∈Q/8Z. In the source's normalized phase language this is the same as lifting phi∈Q/Z to Q/2Z, then multiplying by eight.

## 2. The canonical odd-primary lift of a scalar

Let T_odd⊂Q/Z be the subgroup of elements of odd order. Reduction

    pi:Q/2Z → Q/Z

restricts to an isomorphism on odd-order torsion subgroups: its kernel has order2, while multiplication by2 is invertible on each finite odd-order group. Denote its inverse by eta:T_odd→Q/2Z. This is a canonical group homomorphism, not an arbitrary set-theoretic section on all rational phases.

Concretely, for x=m/n modulo1 with n odd, eta(x) is represented by 2j/n, where 2j≡m modulo n. Changing j changes the representative by an even integer. Changing the presentation m/n does not change the unique odd-order preimage. Thus eta is compatible with addition, negation and every group isomorphism. There is no analogous group-homomorphic section on all of Q/Z: the unique nonzero order-two element cannot be lifted to an element of order at most two reducing to it.

## 3. Completing the quadratic square on odd-order homology

Let M be a closed connected oriented rational homology three-sphere with |H1(M;Z)| odd. Since H1(M;Z/2)=0, there is a unique spin structure s0. Its Spin^c image is a canonical basepoint. Let G=H1(M;Z), let q0=q_s0, and let b be its nonsingular linking pairing in the fixed epsilon convention.

For an arbitrary Spin^c structure sigma, the difference q_sigma-q0 is a character of G. Nonsingularity gives a unique a∈G satisfying

    q_sigma(x)-q0(x)=b(a,x)  for every x∈G.       (1)

This definition avoids any sign convention for the affine Poincare-duality identification. The affine embedding of Spin^c structures into quadratic functions is Deloup–Massuyeau Theorem2.3. Its hypotheses hold here because the homology is finite; no section of a nonfinite radical is chosen.

Homogeneity of q0 gives

    q_sigma(x)=q0(x+a)-q0(a).

Translation permutes G, so

    gamma(q_sigma)=exp(-2 pi i q0(a)) gamma(q0),
    B(q_sigma)=epsilon R(M,s0)-8q0(a) modulo8.   (2)

The scalar q0(a) belongs to T_odd. If a has odd order n, homogeneity gives n²q0(a)=q0(na)=0; hence its order is odd. Thus the canonical eta from Section2 applies.

## 4. The positive theorem

**Theorem 2.1.** On the class of oriented rational homology Spin^c three-spheres with odd-order first homology, the formula

    R_odd(M,sigma)
       = epsilon R(M,s0)-8 eta(q0(a)) in Q/16Z  (3)

is a well-defined orientation-preserving diffeomorphism invariant. It reduces to B(q_sigma) modulo8, restricts to epsilon R on the spin-induced structure, is additive under connected sum, and is of degree exactly one in the Spin^c Goussarov–Habiro theory restricted to this class.

**Proof.** All ingredients are canonical: s0 is unique, q0 and q_sigma are natural quadratic functions, a is uniquely characterized by (1), and eta is the uniquely specified odd-order group section. Therefore no labelling, presentation or choice of spin origin remains. Reduction of (3) gives (2), and a=0 in the spin-induced case.

For connected sums, the unique spin structures and Spin^c structures combine naturally. The homology, linking pairing and quadratic functions split as orthogonal direct sums, and the vector a is the direct sum of the two vectors. Rochlin is additive by boundary connected sum of spin four-manifolds and signature additivity. Eta is a homomorphism. Every term in (3) is therefore additive. Reversing orientation negates the quadratic functions and Rochlin, so the formula has the corresponding signed behavior.

A Spin^c Y-surgery preserves first homology and hence the odd-order class. It canonically transports the unique spin structure, compatibly with the Spin→Spin^c map; see Deloup–Massuyeau Remark3.5. The spin quadratic q0, the Spin^c quadratic q_sigma and their difference are transported by the canonical homology isomorphism. Equation (1) then transports a, so q0(a), and hence eta(q0(a)), are unchanged by each such surgery. The correction term is of degree zero. Massuyeau Proposition1 and Corollary1 prove that Rochlin has degree at most one for spin Y-surgeries, using the locality of the induced spin structure on the surgery torus. For any two disjoint Y-graphs the alternating second difference of the first term is zero, and that of the correction is also zero. This proves degree at most one directly in the source's finite-type convention.

It is not degree zero. On integral homology spheres a=0, so (3) is epsilon R. The Poincare homology sphere has Rochlin value8 modulo16 from its even E8 plumbing, whereas S3 has value0. They are Y-equivalent with their unique spin structures; Massuyeau's proof of Theorem1 explicitly realizes this by the trefoil surgery presentation. Thus the invariant distinguishes two objects in one Y1 class. This proves exact degree one. ∎

This is a complete theorem on the stated odd-order domain. The restriction is genuine: it provides both a unique spin basepoint and the unique odd-primary lift of q0(a). Neither assertion holds for arbitrary even-primary data or positive first Betti number.

## 5. A stronger obstruction if connected-sum additivity is demanded on all Spin^c manifolds

The source does not explicitly spell out connected-sum additivity. The following theorem is therefore conditional on that natural extra requirement, and is not silently substituted for the original question.

**Theorem 2.2.** There is no connected-sum additive invariant F of all closed connected oriented Spin^c three-manifolds with values in Q/16Z whose reduction modulo8 agrees with the finite Gauss–Brown invariant on every torsion-Chern Spin^c structure. No finite-type assumption is needed for this nonexistence statement.

**Proof.** Let X=S2×S1 carry the Spin^c structure tau with Chern class2 in a chosen generator of H²(X;Z). Let sigma_+,sigma_- be the two Spin^c structures on oriented RP3 with Gauss–Brown values1 and-1, in one convention; reversing the convention exchanges them.

Deloup–Massuyeau Example3.3 states that

    (X#RP3, tau#sigma_+) and (X#RP3, tau#sigma_-)

are orientation-preservingly Spin^c-diffeomorphic. The example explicitly states that the listed Y^c-equivalence classes coincide with the diffeomorphism classes, so this is stronger than a degree-zero classification. Their Spin^c Kirby calculus, Theorem2.2, explains it algebraically: for the split surgery matrix diag(0,2), the basis change P=[[1,1],[0,1]] preserves the matrix and sends the characteristic covector (2,0) to (2,2), modulo twice the matrix image. The two torsion labels are exchanged when the free Chern coordinate is twice an odd integer, as in their example.

Diffeomorphism invariance and connected-sum additivity would give

    F(X,tau)+F(RP3,sigma_+)
      =F(X,tau)+F(RP3,sigma_-).

Cancellation in the target group forces equal RP3 values, whereas their reductions modulo8 are1 and-1. These are unequal. Contradiction. ∎

This obstruction allows F to use all topological information, not only quadratic data, and it applies to every finite type degree. It does not contradict Theorem2.1: the absorbing X has non-torsion Chern class and lies outside that theorem's domain. It also explains why the naive finite phase cannot be extended additively across arbitrary non-torsion structures, even before asking for the additional mod16 information.

## 6. Remaining gap

Theorem2.1 constructs the intended kind of genuinely order-one invariant on the odd-order rational-homology domain. Theorem2.2 rules out one precise unrestricted additive extension. Neither proves a full answer to the abbreviated original question without deciding its unstated domain/naturality requirements. The primary source's general wording and the canonical finite-phase restriction remain visible.

The main unresolved mathematical route is the torsion-Chern, even-primary case: different spin origins and possible half-phase choices must be reconciled while retaining diffeomorphism naturality, the surgery degree bound, and any asserted additivity. A bare branch section remains uninformative; the next turn should compute the spin-change obstruction and test it on explicit even-primary surgery forms. No independent full review has yet been performed on these partial results.
