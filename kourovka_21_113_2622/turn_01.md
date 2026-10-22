# Attempt 1: Push the averaging functional through quotients

Status: no general resolution. This attempt establishes exact reductions and identifies what quotient induction does not control. Root-count and virtual-projective facts below are credited to Robinson, Sections 1–3; no novelty is claimed for their reconstruction.

## The common functional

Write x = x_p x_{p'} = x_{p'} x_p for the primary decomposition of an element of a finite group G. Define

A_G(f) = |G|^{-1} sum_{x in G} conjugate(f(x_{p'}))

for a class function f on the p-regular elements. The fiber of x -> x_{p'} above y is exactly {uy : u is a p-element of C_G(y)}. Indeed every such product has p'-part y, and the primary decomposition gives the converse and uniqueness. Consequently

A_G(f) = |G|^{-1} sum_{y p-regular} Psi_{p,G}(y) conjugate(f(y)).    (1)

For ordinary irreducible characters this is their multiplicity in Psi; for irreducible Brauer characters it is the coefficient of the corresponding projective indecomposable character in the unique virtual-projective expansion. The latter coefficients are integers, by the virtual-projectivity theorem; their signs are the substantive issue in part (b).

Let N be any normal subgroup and Q = G/N. Primary decomposition commutes with the quotient map: (xN)_{p'} = x_{p'}N. Uniform fibers then prove

A_G(Infl_Q^G f) = A_Q(f).    (2)

No assumption that N is a p-group is needed for this identity.

## Ordinary counterexample reduction

Suppose an ordinary irreducible character chi has negative coefficient. If N is its kernel, chi inflates an irreducible character of G/N, and (2) gives exactly the same negative coefficient there. A group of least order violating part (a) therefore has a faithful negative-coefficient irreducible character.

It must be nonlinear. For a linear character lambda, separate its p-power and p'-order factors, lambda = lambda_p lambda_{p'}. On x_{p'}, lambda_p is 1, while lambda_{p'}(x_{p'}) = lambda_{p'}(x). Thus A_G(lambda) is the average of the linear character conjugate(lambda_{p'}), and is 1 when lambda_{p'} is trivial and 0 otherwise.

This avoids an incorrect use of positivity of a weighted average of roots of unity: the linear case works because the p'-part of a linear character is itself a homomorphism on all of G.

## Projective counterexample reduction

Now take N normal and a p-group. Every irreducible Brauer character of G inflates uniquely from G/N. Equation (2) therefore says that the entire vector of projective coefficients is unchanged on passage from Q to G. In particular, part (b) holds for G if and only if it holds for G/N. This is the coefficient form of Robinson's normal-p-subgroup lifting result (Theorem 3.2(iii)). A least-order projective counterexample has O_p(G) = 1.

There is also an elementary central p'-quotient reduction. Let Z be a central p'-subgroup. Every p-element of G/Z has a unique p-element lift: in the inverse image of its cyclic p-subgroup, the central Hall p'-subgroup Z has a unique complement, since all complements are conjugate and Z is central. If y is p-regular, such a p-lift u centralizes y whenever uZ centralizes yZ. In fact [u,y] is central and lies in Z, and its order divides the p-power order of u, so it is trivial. Thus the numbers of centralizing p-elements agree in G and G/Z. Multiplication by Z cannot change p-singularity. It follows that Psi_G is the inflation of Psi_{G/Z}.

Inflation preserves ordinary character positivity. It also preserves projectivity here: the central idempotent e_Z = |Z|^{-1} sum_{z in Z} z belongs to RG, and the algebra RG e_Z is isomorphic to R[G/Z]. A projective module for the quotient is a projective RG-module in this direct summand. Conversely, the coefficients in the trivial-Z block agree. Therefore both questions are invariant under a central p'-quotient.

A least-order counterexample to part (b) is consequently centerless: its central p-subgroup is in O_p(G), and its central p'-subgroup can be factored out.

## Direct products

Centralizers and primary decomposition are coordinatewise. Therefore Psi_{p,G x H} = Psi_{p,G} tensor Psi_{p,H}, and both ordinary and projective coefficient vectors are outer products. Each factor's trivial coefficient is 1, by (1) applied to the trivial character. Consequently either positivity assertion holds for G x H if and only if it holds for both factors. A least-order counterexample is directly indecomposable.

## Why this does not finish the proof

Equation (2) controls inflated characters only. For a general non-p normal subgroup, irreducible Brauer characters need not factor through the quotient. Clifford-theoretic constituents lying nontrivially above that subgroup remain uncontrolled. A minimality argument cannot replace their coefficients with quotient coefficients. The surviving target is a centerless, directly indecomposable group with O_p(G)=1, and a possibly faithful nonlinear character with negative average (1). No argument here proves that this target is empty.
