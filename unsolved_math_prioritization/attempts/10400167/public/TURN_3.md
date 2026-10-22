# Turn 3: complete reconstruction in the untwisted finite-abelian subcase

Timestamp: 2026-10-03T09:32:00Z. Outcome: declared subcase resolved; general target unresolved.
Completion estimate toward the general converse: 20% (subjective).

## Attempt

Try to recover an input category from closed-manifold values before attempting the harder general associator reconstruction. In the untwisted finite-abelian class this works completely and uses only lens spaces.

For a finite group G, the standard normalized untwisted Dijkgraaf–Witten theory has

    Z_G(M) = |Hom(pi_1(M),G)| / |G|

for a connected closed 3-manifold M. This is the groupoid cardinality of flat G-bundles: conjugacy orbits receive weights 1/|centralizer|, and orbit–stabilizer converts the sum to the formula. It is NOT the unweighted number of conjugacy classes. This distinction matters for normalizations.

Thus Z_G(S^3)=1/|G| and Z_G(L(n,1))=|{g in G:g^n=1}|/|G|. The finite-group state sum agrees with TV_(Vec_G) in the standard normalization; equivalently the trivial 3-cocycle makes every flat coloring contribute one. A connected triangulation with v vertices has |G|^(v-1) flat edge-colorings per homomorphism; the TV vertex factor |G|^(-v) gives exactly the displayed value.

## Reconstruction theorem

Let A and B be finite abelian groups. If their untwisted ordinary 3-dimensional TQFTs are isomorphic, then A and B are isomorphic. In fact, equality on S^3 and on L(p^k,1), for primes p dividing the common order and 1<=k<=v_p(|A|), suffices.

Proof. The sphere value gives the common group order N. Define

    a_p(k) = N Z_A(L(p^k,1)) = |A[p^k]|,
    a_p(0) = 1.

Write the p-primary part as a product of cyclic groups C_(p^j), with m_p(j) factors of order p^j. Then

    a_p(k) = p^(sum_j m_p(j) min(k,j)).

Consequently the integer

    r_p(k) = log_p(a_p(k)/a_p(k-1))

is sum_(j>=k) m_p(j), and

    m_p(k)=r_p(k)-r_p(k+1).

At the endpoint E=v_p(N), put r_p(E+1)=0, since no cyclic factor can exceed p^E. All elementary divisors are therefore recovered from finitely many lens values and N. The classification of finite abelian groups yields A≅B. A group isomorphism relabels the simple gradings and preserves the trivial associator, so Vec_A and Vec_B are tensor equivalent, and in particular categorically Morita equivalent. QED.

## Negative control and limit

Equal group order alone does not suffice. For C_4 and C_2×C_2, both sphere values are 1/4, but the L(2,1) values are 1/2 and 1. These are exact rational values.

This is a proved finite-abelian, untwisted special case. It does not extend the classification to nonabelian groups or nontrivial cocycles. The reconstruction formulas only determine the element-order statistics in a general finite group, not its multiplication law. No novelty claim is made for this elementary consequence of finite gauge theory.
