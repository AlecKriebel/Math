# Attempt 1 of 5: Can negated directed relations be eliminated on an additive lattice?

## Target and verdict

Try to extend the existing positive-only fragment toward the full existential theory by handling arbitrary negated R_p-atoms. This attempt proves an exact avoidance theorem and a decision procedure when no positive R_p-atom occurs. It does not decide arbitrary positive conjunctions.

Throughout p is a fixed prime, exponents are in N_0, and R_p(a,b) means b=p^k a for some k≥0. All quantified arithmetic variables range over Z. Integral affine forms are legitimate shorthand: negative coefficients can be moved across additive equalities or represented using extra additive inverse variables.

## Lattice avoidance theorem

Let Λ be a nonempty affine lattice parametrized bijectively by z in Z^r, as obtained by Smith normal form from a system of integral additive equations. Given finitely many pairs of integral affine forms (L_j,M_j) on Z^r and finitely many affine forms F_i, the system

    F_i(z) != 0 for every i,
    not R_p(L_j(z),M_j(z)) for every j

has a solution if and only if no F_i is identically zero and no R_p(L_j,M_j) is identically true on Z^r. This includes r=0, interpreted as a singleton.

For r≥1 we prove more: if the criterion holds, the good points have density 1 in cubes [-N,N]^r.

### When is an R_p-atom identically true?

The criterion is exactly that for some k≥0 the identity of affine forms

    M = p^k L

holds. When L=M=0 this is true for k=0. If L=0 and M is nonzero, it is false. Otherwise choose any nonzero coefficient of the affine coefficient vector of L (including the constant coefficient). The corresponding ratio in M must be a nonnegative integral power of p, and the same ratio must match all coefficients. This is effective rational arithmetic followed by a power test.

One implication is immediate. The converse follows from the density estimate below: an atom with no such affine identity occupies density zero, and therefore cannot be true everywhere.

### Density estimate, including zero and sign cases

Fix an atom with no affine identity M=p^k L. In the cube C_N=[-N,N]^r∩Z^r, let |M(z)|≤C(N+1) for an explicit positive C determined by its coefficients. If R_p(L(z),M(z)) holds and L(z)≠0, then

    1 ≤ p^k = |M(z)|/|L(z)| ≤ C(N+1).

Only O(log(N+2)) nonnegative exponents can occur. For each such k, M-p^k L is a nonzero integral affine form. Its zero set has at most (2N+1)^(r-1) points: fix all coordinates except one with nonzero coefficient, which determines at most one value of that coordinate. If the form is a nonzero constant, its zero set is empty.

The remaining case L(z)=0 requires M(z)=0. If L is a nonzero affine form this lies in one proper affine hyperplane. If L is identically zero, M must be nonzero because the atom is not an identity, and the zero set of M is one proper hyperplane. Thus the atom is true at O(N^(r-1) log(N+2)) points. The estimate applies to negative values as well as positive ones: absolute values were used only after the exact equality M=p^k L, and mismatched signs never give a solution.

Each forbidden equality F_i=0 likewise has O(N^(r-1)) points. A finite union of these exceptional sets has density zero. For all sufficiently large N it cannot cover C_N. Its complement has density 1 and contains an integer solution. Necessity of the criterion is immediate. For r=0, evaluate the sole point directly; the stated identity criterion agrees with that evaluation.

## Effective negative-fragment algorithm

Convert a sentence to DNF. For each conjunction containing additive equalities, additive disequalities and only negative R_p-literals:

1. Solve the additive equalities over Z with Smith normal form. Discard an empty solution lattice.
2. Substitute its affine parametrization into all remaining forms.
3. Reject the conjunction if any disequality is identically false or any negated relation has an identically true positive atom, using the coefficient test above.
4. Otherwise accept. If an explicit witness is wanted, enumerate cube points; the density proof guarantees termination.

This decides the entire stated fragment, with any finite number of negated atoms. The method is uniform in p≥2; primality is unnecessary here. The constructive enumeration is not needed for the decision itself.

## Why this is not the full solution

A positive R_p-atom restricts the additive lattice to an infinite union of sublattices, one for each exponent. The density theorem applies on each fixed-exponent lattice, but it does not yet decide whether some exponent produces a nonempty admissible lattice. Arbitrarily many positive atoms introduce independent exponential parameters. Thus neither full decidability nor a definition of the nonnegative cone has been established.

## Relation to prior work

The previous UnsolvedMath report treated at most one positive atom and no negative ones. The avoidance theorem here is a fresh elementary derivation and addresses its explicitly recorded negation gap. No novelty claim is made; the ingredients are elementary lattice counting.
