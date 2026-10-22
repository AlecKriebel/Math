# Attempt 4: Ordinary positivity does not imply projective positivity

Status: no general resolution. This attempt produces a fully explicit obstruction to treating part (b) as automatic once part (a) is established. The obstruction is a different character, not Robinson's Psi. The calculations concern classical A5 representations; no new solution or historical-priority claim is made.

## An ordinary character that passes several necessary tests

Use G=A5, p=2, with class order (1,2A,3A,5A,5B) and class sizes (1,15,20,12,12). Put

a=(sqrt(5)-1)/2, b=(-sqrt(5)-1)/2.

Thus a+b=-1, ab=-1, and a^2+a=1. One of the ordinary degree-3 characters is

chi_3 = (3,-1,0,1+a,1+b).

It is afforded by the icosahedral rotation representation, with the two 5-cycle classes distinguished by rotation angles 72 and 144 degrees. The character values and the full ordinary table are derived in Goodman–Wallach, *Symmetry, Representations, and Invariants*, Appendix G, Table G.3: https://sites.math.rutgers.edu/~goodman/pub/symmetry/appg.pdf .

Let alpha=1_G+chi_3. Its values are

alpha=(4,0,1,2+a,2+b).

This is an actual ordinary character, is zero on all 2-singular elements, has degree divisible by |G|_2=4, has trivial-character multiplicity 1, and is nonnegative as a real-valued function. Indeed 2+b=(3-sqrt(5))/2>0.

Nevertheless, alpha is not the character of a projective RG-module in characteristic 2.

## A negative Brauer pairing certifies nonprojectivity

Identify A5 with SL(2,4). This can be seen from its faithful action on the five points of the projective line over F4: SL(2,4) has order 60, its projective kernel is trivial, and its image is the index-two subgroup A5 of S5.

The natural 2-dimensional F4-module, after extension to an algebraic closure, is irreducible. An invariant line for the upper unipotent matrix with off-diagonal entry 1 would have to be its unique eigenline; the analogous lower unipotent matrix does not preserve that line. Its Frobenius twist is another irreducible module. Their Brauer characters on (1,3A,5A,5B) are

phi=(2,-1,a,b),    phi'=(2,-1,b,a).

These values follow directly by lifting their eigenvalues: an order-3 semisimple matrix has reciprocal nontrivial cube roots as eigenvalues, and an order-5 matrix has reciprocal primitive fifth roots. Squaring eigenvalues interchanges the two fifth-root pair sums. Choose the 5-class labels so that chi_3 above corresponds to phi.

The projective/Brauer pairing is

<alpha,phi'> = [8 - 20 + 12((2+a)b+(2+b)a)]/60.

Using a+b=-1 and ab=-1, the expression in parentheses is -4. The pairing is therefore -1.

If alpha were afforded by a projective RG-module, its pairing with every irreducible Brauer character would be the nonnegative multiplicity of the corresponding projective indecomposable summand. The negative value proves nonprojectivity. This is an exact algebraic certificate; no floating-point sign test is used.

## Psi itself succeeds in this example

The actual target function has values

Psi_{2,A5}=(16,0,1,1,1).

The degree 16 counts the identity and the fifteen double transpositions. Centralizers of 3- and 5-elements have orders 3 and 5, so only the identity contributes as a 2-element there.

There is a direct projective construction. Let W be the rank-4 augmentation lattice of the permutation lattice on five letters. Its ordinary character is

chi_4=(4,0,1,-1,-1).

A Sylow 2-subgroup P is a Klein four group. In the five-letter action it fixes one point and acts regularly on the remaining four. Consequently W restricted to P is the regular RP-lattice: the coordinates on the regular orbit are arbitrary, and the fixed-point coordinate is minus their sum. Thus W is projective over RP and therefore over RG, since [G:P]=15 is a unit in R. The latter implication follows by averaging a P-linear splitting over the cosets of P to obtain a G-linear splitting.

The tensor product of a projective RG-lattice with an R-free RG-lattice is projective for the diagonal action. For a free module this follows from the isomorphism that sends g tensor v to g tensor g^{-1}v, and the general case follows by passing to a direct summand. Therefore W tensor W is projective. Its character is chi_4^2=(16,0,1,1,1), exactly Psi_{2,A5}.

This is a concrete reconstruction of the known defining-characteristic case, not a new case beyond Robinson's paper.

## Exact table checks

The second checker works in Q(a) with the relation a^2+a=1. It checks all 25 ordinary-character inner products, 20 decomposition identities, and the following coefficient vectors:

- Psi in the ordinary basis of degrees 1,3,3,4,5: (1,1,1,1,1).
- Psi in the projective basis dual to Brauer degrees 1,2,2,4: (1,0,0,1).
- alpha in that projective basis: (1,0,-1,0).

The modular degree-4 character is the defect-zero reduction of chi_4; together with the trivial module and the natural module and its twist, these are the four irreducible Brauer characters. The explicit construction above already proves Psi is projective without relying on the decomposition-matrix calculation.

## Remaining obstruction

A successful universal proof of part (a) would still leave part (b): ordinary coefficients can all be nonnegative while a projective coefficient is negative. Even nonnegative function values, the required p-divisibility of the degree, and trivial multiplicity 1 do not repair that implication. For Psi itself, one must establish nonnegativity of the Brauer averages A_G(phi); this example gives no negative such average for Psi.
