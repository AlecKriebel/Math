# Attempt 3: Isolate the mixed-order obstruction and test permutation realization

Status: no general resolution. This attempt obtains an exact positive-plus-signed decomposition, reconstructs a credited special case, and disproves two tempting proof mechanisms by explicit small examples. The special case is contained in Robinson's Theorem 7.3, so it is not new progress on the conjecture.

## A positive contribution with one precisely identified remainder

Let chi be an ordinary irreducible character of degree d. The averaging formula of Attempt 1 and ordinary character orthogonality give

< Psi_G, chi > = delta_{chi,1} + |G|^{-1} sum_{x p-singular} conjugate(chi(x_{p'}) - chi(x)).    (1)

Both the set being summed over and the primary-part map are invariant under inversion. Thus the sum is real, and conjugates in (1) may be replaced by real parts. Split the p-singular elements into the nonidentity p-elements U and the mixed-order elements M (those having both nontrivial p-part and nontrivial p'-part). Then

< Psi_G, chi > = delta_{chi,1}
 + |G|^{-1} sum_{u in U} (d - Re chi(u))
 + |G|^{-1} sum_{x in M} (Re chi(x_{p'}) - Re chi(x)).    (2)

Every summand in the first sum is nonnegative: choose a unitary representation affording chi, whose eigenvalues on u have modulus one.

If there are no mixed-order elements, (2) proves that Psi_G is a character. This hypothesis can also be formulated as: the centralizer of every nonidentity p-element is a p-group. Indeed, a nontrivial p'-element in such a centralizer would produce a mixed-order commuting product, and primary decomposition gives the converse. The result is a special case of Robinson's more general normal-p-complement centralizer theorem.

Equation (2) makes the attempted extension exact. One would have to show that the potentially negative mixed-order contribution is dominated by the first sum. It is not valid simply to declare the second sum termwise nonnegative.

## A genuine negative mixed-order contribution

Take G=C6=<g>, p=2, and the faithful linear character lambda(g)=exp(pi i/3). Its real values on g^k, k=0,...,5, are

1, 1/2, -1/2, -1, -1/2, 1/2.

The only nonidentity 2-element is g^3, contributing 1 - Re lambda(g^3)=2 to the first sum in (2). The two mixed elements are g and g^5. Their odd-order parts are g^4 and g^2, respectively, so each contributes -1 to the second sum. The coefficient is (2-1-1)/6=0, in agreement with the independent linear-character calculation in Attempt 1.

This example is not a counterexample to the problem. It demonstrates that the local summands that a termwise-positivity proof would require can be strictly negative, even in an abelian group. The global cancellation is essential.

On a simultaneous eigenline for the commuting matrices representing x_p and x_{p'}, the mixed correction has real part Re(eta(1-zeta)), with eta a p'-root and zeta a p-root. The example above realizes negative values of this expression. Unitarity bounds alone therefore cannot establish the required global domination.

## Why a G-set with exactly |G_p| points cannot be the general construction

The fiber identity also proves

< Psi_G, 1_G > = |G|^{-1} sum_{y p-regular} |C_G(y)_p| = 1.    (3)

Suppose Psi_G were a permutation character. Equation (3), by Burnside's orbit-counting formula, would imply that the underlying G-set has exactly one orbit. It would therefore have the form G/H, of size [G:H]=Psi_G(1)=|G_p|. In particular, |G_p| would divide |G|.

For G=S3 and p=2, there are four 2-elements (identity and the three transpositions), and 4 does not divide 6. Thus Psi_{2,S3} is not a permutation character. It is nevertheless an ordinary character: on the identity, transpositions and 3-cycles its values are (4,0,1), equal to the sum of the trivial, sign and degree-2 irreducible characters. The character table identity is immediate from the natural permutation action on three letters after removing its constant line.

Likewise, A5 has 16 2-elements, while 16 does not divide 60. The exact element enumeration checks the same obstruction there. Thus replacing the conjugation action on G_p by some other action on a set of the same size cannot give a universal proof. A linear-module construction, potentially with non-permutation bases, is required.

## What remains

The first route fails at a concrete domination inequality between the two sums in (2). The second route is impossible as a universal permutation-module construction. Neither argument disproves the ordinary-character or projective-module conjecture. In particular, the two small-group obstructions concern proposed proof mechanisms, not the target statements.
