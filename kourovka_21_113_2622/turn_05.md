# Attempt 5: Can proper-centralizer projectives be split off globally?

Status: no general resolution after five mathematical attempts. This final route derives the exact local-to-global subtraction problem, verifies it in A5, and identifies the unproved summand inequality. It reconstructs and analyzes a centralizer identity already present in Robinson's paper, rather than claiming that identity as new.

## The larger truncated conjugation character

Let Lambda_G(x)=|C_G(x)| on p-regular elements and 0 on p-singular elements. Unlike the target Psi_G, this larger function is known to be a genuine projective character for every finite group. This is the truncated-conjugation construction in Robinson's paper and, in different notation, the p'-case of Schroeder's Theorem 3.3.

Here is the standard modular mechanism. If S_i are the simple modules over a splitting field of characteristic p and P_i their projective covers, then the modules P_i tensor S_i^* are projective. The sum of their Brauer characters is |C_G(x)| on p-regular elements, by projective/Brauer column orthogonality. Their direct sum has a projective lift whose ordinary character vanishes on p-singular elements and is Lambda_G. This construction concerns tensor products over the field followed by projective lifting; it does not assert that an arbitrary simple modular module has an ordinary irreducible lift.

Let Y be representatives for the p-regular conjugacy classes of G. There is an exact identity

Lambda_G = sum_{y in Y} Ind_{C_G(y)}^G Psi_{C_G(y)}.    (1)

## Direct verification of the identity

All terms vanish on p-singular elements. Fix a p-regular x. The contribution of the class of y to the right-hand side is

sum_{z in y^G intersect C_G(x)} |C_{C_G(x)}(z)_p|.

To see this, expand the induced class function and group the conjugating elements according to z=aya^{-1}; their fiber sizes cancel the denominator |C_G(y)|. Summing over all y in Y gives

sum_{z in C_G(x)_{p'}} |C_{C_G(x)}(z)_p| = |C_G(x)|.

The last equality is exactly the primary-part fiber partition, now inside C_G(x). This proves (1) without assuming the conjecture.

## Minimal-counterexample induction reaches a subtraction

Attempt 1 shows that a least-order counterexample to projective positivity may be taken centerless. In such a group, C_G(y) is proper whenever y != 1. If part (b) holds for all proper subgroups, define the genuine projective character

D_G = sum_{y in Y, y != 1} Ind_{C_G(y)}^G Psi_{C_G(y)}.

Induction of a projective module is projective because RG is free as a right R[C_G(y)]-module. Equation (1) becomes

Psi_G = Lambda_G - D_G.    (2)

This is not a proof of positivity: the difference of two genuine projective characters need not be genuine. To make the issue numerical, let phi be an irreducible Brauer character of G and let r_phi be its projective coefficient in Lambda_G. Then

r_phi = sum_{z in Y} conjugate(phi(z)).

For each y != 1, decompose the restriction of phi to C=C_G(y) into irreducible Brauer characters beta, with nonnegative composition multiplicities m_{y,phi,beta}. Let c_{beta,C}=<Psi_C,beta>. By Frobenius reciprocity the coefficient in D_G is

d_phi = sum_{y != 1} sum_beta m_{y,phi,beta} c_{beta,C_G(y)}.

Consequently the conjectured coefficient is exactly

c_{phi,G} = r_phi - d_phi.    (3)

Under the minimality assumption r_phi and d_phi are nonnegative integers. What is missing is the componentwise inequality d_phi <= r_phi. Neither their individual nonnegativity nor the total dimension inequality proves it.

Equivalently, if T_G is a projective module affording Lambda_G and L_G is the direct sum of the induced projectives affording D_G, the required step is to exhibit L_G as a direct summand of T_G. Krull–Schmidt decomposition shows that this is precisely the set of inequalities in (3). Merely rephrasing (3) as a summand assertion does not advance the proof unless an actual split embedding is constructed.

## Exact A5 balance

For A5 at p=2 the nonidentity p-regular classes have centralizers C3,C5,C5, respectively. Each is a p'-group, so its Psi is the trivial character. Thus

D = Ind_{C3}^{A5} 1 + 2 Ind_{C5}^{A5} 1.

In the Brauer basis of degrees 1,2,2,4 used in Attempt 4, the exact vectors are

r = (4,0,0,3),    d = (3,0,0,2),    r-d = (1,0,0,1).

The checker derives d by averaging each restricted Brauer character over C3 and C5. For example, the degree-4 Brauer character has C3-fixed multiplicity (4+2)/3=2 and C5-fixed multiplicity (4-4)/5=0. The two degree-2 characters have no fixed points for either cyclic subgroup. This verifies the subtraction formula and its normalization in a nonabelian simple group, but A5 is already a known positive case.

## Why the obvious conjugation module does not supply the embedding

The modular conjugation module on the set G has Brauer character |C_G(x)| on p-regular elements, the same Brauer character as T_G. It need not be projective. Its basis vector indexed by the identity spans a direct trivial summand, with the other group elements spanning an invariant complement. If p divides |G|, that trivial summand is not projective, so the conjugation module is not projective either.

Likewise, the conjugation permutation module on G_p has the same Brauer character as Psi_G, but contains the same direct trivial summand and is not projective when p divides |G|. Equality of Brauer characters describes composition factors; it does not determine module projectivity. Consequently a partition of conjugation bases by primary parts does not automatically become the required split embedding between projective replacements.

## Final remaining gap

The full ordinary-character and projective-module assertions remain unresolved here. No counterexample to either assertion was found. The strongest outcomes are the explicitly proved reductions and induced-character formula, exact small-group certificates, and counterexamples to two overstrong proof shortcuts. The final local-to-global approach is blocked at the unproved domination d_phi <= r_phi, or equivalently a split embedding that has not been constructed. This is a substantive unsolved remainder, not an omitted routine step.
