# Independent geometric derivation

Scope: characteristic zero, k containing the field of definition of the Hurwitz datum, r >= 3 distinct branch points, coarse inner spaces. Let H=PGL2(kbar), let Y be the unreduced coarse space, and let x be a k-point of its reduced quotient.

## 1. The geometric fiber and its stabilizer

By the coarse-moduli property, the geometric fiber over x is a single H-orbit of geometric coarse points. This is also consistent with the algebraic quotient: the equivariant finite branch-divisor map has finite point stabilizers for r>=3. All H-orbits therefore have dimension3; a nonclosed orbit would have a smaller-dimensional orbit in its boundary, contrary to the same finite-stabilizer property. The source's geometric quotient identifies these orbits, rather than merely identifying a cover after forgetting its G-marking.

Choose y over x. Its stabilizer E acts faithfully on its r distinct branch points. A transformation fixing them individually is identity, since three distinct points determine a projective transformation. E embeds in the permutation group of this finite set; in characteristic zero it is a finite reduced subgroup of PGL2. Classifying E does not classify the branch-divisor stabilizer instead: E may be a proper subgroup of that stabilizer.

Conjugate y so E is a Galois-stable standard representative from Cadoret Lemma2.1. If sigma(y)=a_sigma^{-1}y, then both sides have stabilizer E, so a_sigma is in N=N_H(E). Its class c_sigma in Q=N/E is uniquely determined. Direct computation gives

    (sigma tau)(y)=sigma(a_tau)^{-1} a_sigma^{-1} y,
    c_(sigma tau)=c_sigma sigma(c_tau).

This direction uses the left action; commuting the two factors is not allowed. The cocycle is continuous: y has a finite field of definition; its finitely many conjugates determine finitely many cosets, and all selected representatives have algebraic coefficients in a finite extension.

If b_sigma=h^{-1}sigma(h) is in N and has class c_sigma, then

    sigma(hy)=sigma(h)a_sigma^{-1}y
              =h b_sigma a_sigma^{-1}y=hy.

Thus hy is a k-rational point of Y. This uses descent of coordinates of a coarse point, not descent of a chosen cover object or a choice of compatible source isomorphisms. A possible central gerbe of G-cover models causes no additional obstruction to this implication.

If c is a Q-coboundary q^{-1}sigma(q), choose n in N mapping to q. Its coboundary n^{-1}sigma(n) suffices; n need not belong to N(k). More generally equality of Q-cohomology classes is enough after changing h by a geometric lift in N.

## 2. Stabilizer cases and the same-extension issue

For E=1, the N-cocycle is an H-cocycle. Descending the projective line gives a smooth conic B/k. A transverse k-line in its anticanonical plane model intersects it in a degree2 etale zero-cycle. k is infinite, so a transverse line exists. At least one point has residue degree1 or2. Over that residue field B is the projective line and the cocycle is a coboundary. There is no assertion that an arbitrary Brauer class of period2 has index2.

For E=A5 or S4, N=E and Q=1, so y is already fixed. The standard representative may have nontrivial Galois action; pointwise rationality of E is unnecessary.

For E=A4 or a dihedral group D_(2n) of order2n, n>=3, Q is the group of order2. Every action on that group by automorphisms is trivial. A Q-cocycle is a quadratic character, killed by its kernel's fixed field of degree<=2. No equivariant splitting of N->Q is needed. The dihedral group D4 is V4 and must be treated separately. Odd dihedral cases admit sharper prior conclusions, irrelevant to the uniform bound.

For E=C_n, n>=2, N is G_m semidirect C2, with inversion action and Galois action on the G_m factor. The quotient map (a,epsilon)->(a^n,epsilon) identifies Q with the same Galois module. Restrict to the kernel of c's component character, a field K of degree<=2. On Gamma_K the torus component is an ordinary multiplicative cocycle with its usual action, so Hilbert90 kills it over K itself. The proof does not first spend a quadratic extension on a torus and then spend another on the component group. C2 is included here and C1 belongs to E=1.

## 3. The exceptional V4 quotient

Take E0={1,z->-z,z->1/z,z->-1/z}. It is pointwise rational. Conjugation identifies N_H(E0)/E0 with the constant S3: its kernel is E0 and its image permutes the three nonidentity elements arbitrarily. The independent finite control constructs the order24 normalizer using z->iz and z->(z+1)/(z-1), verifies kernel4, quotient6 and invariance of the quotient under complex conjugation. Only8 elements are rational over Q; assuming a rational S3 section would therefore be wrong. The proof does not assume one.

A continuous c:Gamma_k->S3 is a degree3 etale algebra. Because k is infinite, there is an element whose three geometric coordinates are distinct: remove the finite union of proper k-linear subspaces on which two embeddings coincide. Its characteristic polynomial F is a separable cubic, including for split and partially split algebras. Write its roots e_i. The smooth genus1 curve Y^2=F(X) has a k-rational origin at infinity. Its nonzero two-torsion translations commute with negation and descend to the split quotient X-line P1_k. They yield E'≅V4 with Galois action c on its nonidentity elements.

For a depressed cubic F=X^3+aX+b and F(e)=0, the elliptic chord law gives

    X(P+(e,0))=F(X)/(X-e)^2-X-e
                =e+(3e^2+a)/(X-e).

The corresponding matrix is M_e=[[e,2e^2+a],[1,-e]], with determinant -F'(e)≠0 and square F'(e)I. The three matrices multiply projectively as V4. This derivation and generic product identities are checked independently by eliminating the third root w=-u-v and a=-(u²+uv+v²). Galois equivariance follows from the coefficients being rational in the singled-out root and the symmetric cubic coefficients, not from finite sampling.

Over kbar choose h with hE0h^-1=E' and the prescribed labeling. All labelings are possible because N/E0=S3. For e∈E0,

    sigma(h e h^-1)=h c_sigma(e) h^-1.

E0 is pointwise rational, so b_sigma=h^-1 sigma(h) normalizes E0 and acts as c_sigma. Its Q-class is exactly c_sigma, whereas its PGL2-class is trivial by construction. The criterion above proves hy rational over k. The auxiliary coefficients of h may lie in an extension of large degree; that is irrelevant to the rationality of the resulting point hy.

Consequently every point with geometric stabilizer V4 lifts already over k. Full S3 action is included, not just cyclic cubic or split cases. This is the decisive improvement over killing the S3-cocycle by its splitting field of degree up to6.

## 4. Boundary and scope checks

Characteristic zero supplies perfectness, separability, the tame finite-subgroup list and ordinary etale two-torsion. The argument has no positive-characteristic conclusion. There are no collision or compactification boundary points because the spaces parameterize r distinct branch points of smooth covers. For r<=2 the stabilizer can be positive dimensional and this proof does not apply.

For r=3, the divisor stabilizer is S3 and E is only a subgroup of it. Cadoret Corollary5.1 gives the stronger all-points degree1 conclusion. The stated upper bound2 remains true; it is not asserted optimal for this branch count. For r=4, divisor stabilizers are the generic V4 and special D8 or A4 groups, but E can be a proper subgroup. Every subgroup falls under the complete case analysis above. In particular, the new V4 argument does not assume that E equals the entire branch-divisor stabilizer, or exclude special elliptic j-invariants.

A k-fixed coarse point has a k-rational branch divisor on the fixed split projective line. However, a k-rational reduced point need initially have only a divisor on a twisted conic; the E=1 case expressly permits that obstruction. Rationality of a cover's coarse moduli point is different from existence of a G-cover object over k when Z(G) is nontrivial. The source's lifting problem asks for the former.

The source asks for an optimal upper bound for m_k(x), and develops bounds depending on r and the base invariant. The result proves the least constant valid simultaneously for all these data is2, provided the lower-bound family is independently verified. It does not compute m_k(x) for every input or claim every fixed datum needs degree2. Publication language must preserve this precise scope.
