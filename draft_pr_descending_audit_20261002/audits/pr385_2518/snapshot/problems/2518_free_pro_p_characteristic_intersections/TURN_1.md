# Turn 1: the abelianization lattice obstruction

Completed2026-10-02 UTC. Original unresolved,1/5 substantive turns. Subjective progress toward the original question:8%. This is a necessary-condition result for possible common characteristic subgroups, not a family with trivial common characteristic core.

Throughout, F is free pro-p of finite rank d>=2, and U is open. All automorphisms invoked are continuous. Write G_ab for G/closure([G,G]). The source's standard free-pro-p basis, Schreier and automorphism facts are recorded in Barnea et al., arXiv:2507.04120v3, Sections3.3–3.4 and Notation7.8. In particular F_ab=Z_p^d and Aut(F) maps onto GL_d(Z_p). The same applies to U, whose rank is D=1+[F:U](d-1)>=2. These are credited classical inputs.

## 1. Scalar invariance, without a closedness assumption

**Lemma.** If an additive subgroup M of Z_p^r, r>=2, is invariant under every element of GL_r(Z_p), then M is either0 or p^a Z_p^r for an integer a>=0. M is not assumed closed.

For v in M, i!=j and any c in Z_p, subtract v from its image under the elementary transvection adding c times coordinate j to coordinate i. This puts c v_j e_i in M. Coordinate permutations give c v_j e_k in M for every k. Let I={b in Z_p : b e_1 in M}. It is an additive subgroup, and the same transvection/permutation argument makes it closed under multiplication by any c in Z_p. Thus I is an ideal and M=I^r. Every nonzero ideal of Z_p is p^a Z_p: take a nonzero element of minimal finite p-adic valuation, multiply by the inverse of its unit factor, and compare all valuations. Hence the asserted classification. In particular this invariance itself forces M to be closed. QED.

This argument needs r>=2; no scalar-invariance or closedness is inferred merely from invariance under a finite subgroup of GL_r.

## 2. A general nonscalar-image criterion

Let j:U_ab -> F_ab be induced by inclusion and set L=j(U_ab), an open Z_p-submodule of Z_p^d. Openness follows because U contains an open normal subgroup and hence contains all p^e-th powers for some e, so p^e Z_p^d <= L.

**Theorem.** Suppose L is not p^a Z_p^d for any integer a>=0. If K<=U is characteristic in both F and U, then K is contained in closure([U,U]). No closedness of K is required.

Let M_U be the image of K in U_ab and M_F its image in F_ab. Characteristicity and the epimorphisms onto the relevant general linear groups make each image invariant under the entire GL action. By Section1 they are0 or scalar lattices. If M_U is nonzero, write M_U=p^b Z_p^D. Then

    M_F=j(M_U)=p^b L.

Since L has full rank, M_F is nonzero. Thus it equals p^c Z_p^d. Equality p^b L=p^c Z_p^d implies c>=b (L is integral) and L=p^{c-b}Z_p^d, contrary to the hypothesis. Therefore M_U=0, proving the theorem. QED.

This is equality of actual images, not merely their closures. The invariant-image lemma is why no closure gap enters. The theorem would be invalid if one treated an arbitrary finite-index inclusion lattice as necessarily scalar.

## 3. Every index-p subgroup has this obstruction

Let U be any subgroup of index p. Such a subgroup is the kernel of a nonzero F->C_p character. Choose a basis x_1,...,x_d so that U is the kernel of the x_1 exponent modulo p. A pro-p Schreier basis is

    x_1^p,
    x_1^j x_i x_1^{-j}, 2<=i<=d, 0<=j<p.

Its size is1+p(d-1). On abelianizations, x_1^p maps to p e_1 and every displayed conjugate of x_i maps to e_i. Consequently

    L=p Z_p e_1 direct-sum Z_p e_2 direct-sum ... direct-sum Z_p e_d,

which is nonscalar because d>=2. Hence every subgroup K characteristic in F and U satisfies

    K <= closure([U,U]) <= closure([F,F]).

**Consequences.** Such a K cannot be open: U_ab=Z_p^D is infinite, whereas a subgroup containing an open K would have finite index. It contains no nonidentity p-adic power of a primitive element of U, because a primitive element maps to a basis vector of U_ab and Z_p is torsion-free as a Z_p-module. It also contains no nonidentity p-adic power of a primitive element of F: use an automorphism of F to move that primitive element to x_2, which is primitive in U, and use characteristicity of K in F. For an arbitrary nonclosed K, membership of an individual power is all that is used; K is not assumed closed under p-adic powering.

The absence of primitive powers is stronger than just the absence of an open common subgroup, but does not rule out a subgroup living entirely in the commutator layer.

## 4. One index-p subgroup already represents all of them

Aut(F) acts transitively on index-p subgroups: in the Frattini quotient F/Φ(F)=F_p^d these are kernels of nonzero linear forms, up to scalar, and GL_d(F_p) acts transitively on the corresponding hyperplanes. The relevant linear automorphisms lift to Aut(F).

If K is characteristic in F and in one such U, let V=alpha(U) for alpha in Aut(F). Then alpha(K)=K. For beta in Aut(V), alpha^{-1} beta alpha is in Aut(U), so beta(K)=K. Thus K is characteristic in every index-p subgroup V. In particular

    K <= intersection_{[F:V]=p} closure([V,V]).

Therefore adding more index-p subgroups to a family already containing F and one index-p subgroup imposes **no extra condition** on K. The full family of all index-p subgroups, of cardinality (p^d-1)/(p-1), is equivalent to the pair {F,U} for this question. It might or might not have trivial common core; this turn does not decide that. A materially different finite-family search needs another Aut(F)-orbit, for instance a suitable higher-index subgroup, rather than more copies of this same orbit.

## 5. Exact checks and gap

verify_turn1.py checks the coordinate-extraction identities over bounded rings Z/p^e, the unequal inclusion-lattice exponents for several primes/ranks, and transitivity on finite Frattini hyperplanes. These exact finite controls supplement the all-prime p-adic proofs; they cannot certify that a common characteristic subgroup is trivial.

The original source asks for a family excluding every nontrivial K, including closed infinitely generated subgroups deep in the commutator structure. This turn only localizes a possible survivor and removes redundant index-p choices. It does not transfer the source paper's discrete-free result to free pro-p groups.
