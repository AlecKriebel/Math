# Cartan centralizers: the separable theorem and its boundary

**30001626 / OWR-4533-004. Complete first-author-turn candidate for independent review.** The intended separable question has an affirmative answer by a direct consequence of the classical Hilbert root decomposition and Baire's theorem. No novelty claim is made. An unqualified extension without separability is false, as shown separately below.

## 1. Statement and conventions

Let g be a real or complex separable semisimple L*-algebra, and let h be a Cartan subalgebra in the source sense: maximal among abelian *-stable subalgebras. Then there exists H in h such that

    z_g(H)={X in g:[H,X]=0}=h.                         (1)

Indeed the set of such H contains a dense G-delta subset of h. In the complex case it is exactly the complement of the nonzero root kernels. Simplicity is unnecessary for this implication, so the theorem applies in particular to the simple separable algebras in Tumpach's OWR question.

The star operation is the adjoint involution for the Hilbert Lie structure, not an arbitrary algebraic conjugation. The source's root decomposition is a **completed orthogonal Hilbert sum**. No algebraic finite-support restriction on H or X is imposed. The statement concerns a centralizer inside g, not a stabilizer subgroup under inner automorphisms.

## 2. Completeness and ordinary maximal abelianness

First, h is closed. Its norm closure is again abelian, since the bracket is continuous, and is *-stable by continuity of the involution. Maximality therefore makes the closure equal to h. Thus h, with its real or complex Hilbert norm, is a complete metric vector space.

We also have z_g(h)=h. For X commuting with h, X* commutes with h because h is *-stable and the star is an involutive anti-automorphism of the bracket. Decompose X into star-eigenparts:

    X=(X+X*)/2+(X-X*)/2.

Each part separately commutes with h and is respectively self-adjoint or skew-adjoint. Adjoining either part to h gives an abelian *-stable real subalgebra in the real case. In the complex case its complex linear span with h is likewise *-stable. Maximality puts both parts in h, hence X in h. This also proves the ordinary maximal-abelian property rather than assuming it from a finite-dimensional analogy.

The continuity used here is part of the Hilbert Lie structure. Equivalently, for fixed X the everywhere-defined adjoint identity (ad X)*=ad(X*) makes ad X bounded by the closed-graph theorem; joint bracket continuity follows by uniform boundedness. No unbounded-operator domain is being overlooked.

## 3. Complex separable case

The classical Schue root theorem, stated with these conventions in Tumpach's Section2, equation(3), supplies

    g=h Hilbert-direct-sum (sum over alpha in Delta of g_alpha),    (2)

where Delta consists of the nonzero roots and

    [K,X]=alpha(K)X for K in h, X in g_alpha.

The nonzero mutually orthogonal root spaces make Delta at most countable, since g is separable. This is also explicitly stated beside equation(3) in the cited source. We do not claim the same countability for an arbitrary nonseparable algebra.

Each alpha is a nonzero continuous complex linear functional on h. Its continuity can also be checked directly: choose a nonzero v in g_alpha; then

    |alpha(K)| ||v|| = ||[K,v]|| <= ||ad(v)|| ||K||.

Therefore ker(alpha) is a proper closed linear subspace of h, with empty interior. By Baire's theorem,

    h_regular = intersection_(alpha in Delta) (h minus ker(alpha))    (3)

is a dense G-delta subset of h. The finite-root case is included. Choose H in h_regular.

To evaluate its centralizer, let P_alpha be the continuous orthogonal projection onto g_alpha. On the dense algebraic sum in (2),

    P_alpha ad(H)=alpha(H) P_alpha.

Both sides are bounded linear operators, so the identity holds on all of g. If [H,X]=0, then alpha(H)P_alpha X=0 for every alpha. All alpha(H) are nonzero, so all nonzero-root projections vanish. The complete decomposition (2) now gives X in h. Conversely every X in h commutes with H. This proves (1) without exchanging an unjustified infinite series or requiring an inverse bound on the possibly small numbers alpha(H).

It also proves the exact regular-set characterization in the complex case: if alpha(H)=0 for some nonzero root, a nonzero vector of g_alpha centralizes H and lies outside h. Thus h_regular is precisely the set satisfying (1). No claim that this dense G-delta is open is made.

## 4. Real separable case

Form the Hilbert complexification g_C=g plus i g with complex-bilinear bracket and conjugate-linear extension of the star. The L*-adjoint identity extends, and separability is preserved. Its center is the complexification of z(g): if X+iY commutes with every real Z, then [X,Z]=[Y,Z]=0. Since g is semisimple, its center is zero; therefore g_C is semisimple in the L*-sense as well. Here we use the standard center/semisimple orthogonal decomposition for L*-algebras, recalled in the same source.

The space h_C=h plus i h is closed, abelian and *-stable. By Section2, z_g(h)=h. If X+iY lies in z_(g_C)(h_C), then X and Y commute with h and hence belong to h. Thus

    z_(g_C)(h_C)=h_C,

so h_C is a Cartan subalgebra of g_C. This verifies the complexification step for all real forms; no assumption that g_C is simple is required.

Apply the complex Hilbert root decomposition to (g_C,h_C). Its nonzero roots form a countable set Delta. For each alpha, the restriction alpha|h is a continuous real-linear map to C and is not identically zero: otherwise complex linearity would make alpha vanish on h_C. Its kernel in the real Banach space h is proper, closed and nowhere dense, whether its real codimension is one or two.

Baire's theorem on h therefore supplies a real H with alpha(H) nonzero for every alpha. The bounded-projection argument in Section3 gives z_(g_C)(H)=h_C. Intersecting with g gives z_g(H)=h. The same countable-kernel complement is a dense G-delta of real h, proving the asserted real conclusion.

## 5. A separate operator description

For the classical Hilbert–Schmidt realizations in Alagia's cited paper, one can see the same argument without root notation. A Cartan is a commuting *-stable family of compact normal operators. The underlying separable Hilbert space splits into countably many simultaneous eigenspaces H_mu, including a possible common-zero eigenspace. Each mu is continuous. A Baire choice of H in h outside all kernels of mu−nu for distinct joint characters gives distinct scalar values on distinct joint eigenspaces. Any bounded operator commuting with H then preserves those eigenspaces and commutes with all of h. Intersect with g and use z_g(h)=h.

This is a consistency check and a credited application of the simultaneous spectral decomposition, not a claim that ad(H) itself is compact. It need not be compact. No choice of an infinite diagonal coefficient sequence outside the Hilbert norm is used.

## 6. Why dropping separability changes the answer

This section addresses only the stronger, unqualified nonseparable reading of the short imported statement. It is not substituted for the affirmative source-scoped theorem.

Let I be uncountable, let K=ell2(I), and let g=S2(K), the complex Hilbert–Schmidt operators with bracket [A,B]=AB−BA, adjoint star and inner product Tr(A*B). This is an L*-algebra: products and brackets are well-defined in S2, the bracket norm is bounded by 2||A||2||B||2, and trace cyclicity gives the L*-adjoint identity.

For completeness, g is topologically simple. Let J be a nonzero closed Lie ideal and A a nonzero element of J. Write P_i=E_ii for the basis projections. If A has an off-diagonal entry A_ij nonzero, i≠j, then

    B=[P_i,[A,P_j]]=A_ij E_ij+A_ji E_ji,
    (B+[P_i,B])/2=A_ij E_ij,

so E_ij belongs to J. If A is diagonal, some diagonal value a_i is nonzero, while some a_j is zero: a Hilbert–Schmidt diagonal has at most countably many nonzero entries, whereas I is uncountable. Then [A,E_ij]=(a_i−a_j)E_ij puts an off-diagonal matrix unit in J.

Bracketing that unit with arbitrary finite matrix units yields every off-diagonal unit and every difference P_k−P_l. For example, [E_ij,E_ji]=P_i−P_j yields E_ji on one more bracket; [E_ij,E_jk]=E_ik and [E_ki,E_ij]=E_kj introduce any third index, and further such brackets give all pairs. Hence J contains all finite-support trace-zero matrices.

For any fixed i and distinct indices j_1,...,j_n different from i, the trace-zero operators

    P_i-(1/n) sum_(r=1)^n P_(j_r)

lie in J and converge in Hilbert–Schmidt norm to P_i, with error1/sqrt(n). Thus every finite-support matrix lies in J. These matrices are dense in S2(K): any square-summable matrix over I×I has countable support and finite subsets approximate its squared norm. Therefore J=g. This proves topological simplicity, rather than presuming that an uncountable operator ideal is algebraically simple.

Let d be the diagonal Hilbert–Schmidt subalgebra. It is closed, abelian and *-stable, and commuting with every P_i forces all off-diagonal matrix entries to vanish. Therefore z_g(d)=d, so d is a Cartan subalgebra.

For every H in d, its diagonal sequence has countable support. Choose distinct i,j outside that support. Then E_ij commutes with H but is not diagonal. Consequently z_g(H) strictly contains d for every H in d. This d cannot be the centralizer of one of its elements.

The example explains why the countable-root/Baire step cannot simply be extended to arbitrary cardinality. It supplies a negative answer to the statement with no separability condition, while Section3–4 supplies the affirmative answer in the actual source's separable setting.

## 7. Disposition and credit

The intended OWR question is resolved affirmatively by a classical-consequence proof: every Cartan of a simple separable real or complex L*-algebra contains a centralizer-realizing element, in fact a dense G-delta set of such elements. The omitted-separability variant is separately false. These conclusions do not settle the adjacent inner-conjugacy classification question.

Schue's Hilbert root decomposition, its statement in Tumpach's work, Alagia's real operator framework, the spectral theorem and Baire category are established inputs. This package makes their immediate consequence and the missing separability boundary explicit. It is not a new classification or a claim of mathematical priority. One substantive author turn has produced the complete candidate; separate adversarial source-and-proof review is required before any result PR.
