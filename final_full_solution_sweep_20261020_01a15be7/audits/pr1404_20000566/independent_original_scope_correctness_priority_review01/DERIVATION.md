# Independent derivation: universal finite strict paving

Fix n≥1, 1≤r≤n and an admissible vector d∈[0,1]^n with integer sum. Admissibility ensures that both its real and complex orthogonal-projection fibers are nonempty, by real Schur–Horn. Set q=1−d and m=Σq_i. For a projection P with diagonal d write Q=I−P. A coordinate compression satisfies 0≤Q[J]≤I_J and P[J]=I_J−Q[J]. Hence ||P[J]||<1 precisely when Q[J] is positive definite. Since Q[J] is the Gram matrix of the columns Qe_i for i∈J, this is precisely their independence.

The finite Edmonds/Rado–Horn partition criterion therefore says

    π_r(P)<1 iff |J|≤r rank Q[J] for every J⊆[n].

Zero columns are legitimate matroid loops and immediately obstruct any partition into independent sets. The theorem initially supplies at most r parts, allowing empty parts. If fewer than r are occupied and r≤n, repeatedly split a part of size at least two. Independence is hereditary, so this terminates with exactly r nonempty parts. No infinite-dimensional Gram lower bound is inferred from algebraic independence.

## Exact minimum compression rank

For any fixed subset J of size s, put t=n−s and a=Σ_Jq_i. Since Q[J] is a positive contraction,

    rank Q[J] ≥ ceil(a).

The lower bound is attainable by a real projection with the entire prescribed diagonal q. Write a=f+θ, with f=floor(a) and 0≤θ<1.

If θ=0, each side has an integer total mass, f and m−f. Its entries are between zero and one, so its vector is majorized by a vector of that many ones and the remaining zeros. Real Schur–Horn produces projections on the two coordinate blocks with those diagonals. Their direct sum has the required total diagonal and compression rank f. This includes empty blocks, all coordinates, rank zero, full rank, and coordinates equal to zero or one.

If 0<θ<1, a≤s gives f+1≤s. The complementary mass b=m−f−θ lies in [0,t]. It is nonintegral, so b>0, m−f−1≥0 and m−f≤t. Thus the block sizes support compression spectra

    λ_J=(1 repeated f, θ, zeros),
    λ_Jc=(1 repeated m−f−1, 1−θ, zeros).

Start with f ones on the first block, m−f−1 ones on the second, zeros elsewhere, and the rank-one coupling

    [[θ, sqrt(θ(1−θ))], [sqrt(θ(1−θ)), 1−θ]]

on one unused coordinate from each block. Its square equals itself and its trace is one, so the total matrix Q₀ is a real orthogonal projection of rank m. Each proposed spectrum majorizes the desired block diagonal. Before the last nonzero eigenvalue, any target partial sum is at most its number of entries because each entry is ≤1. At and after that index, it is at most the total mass. Equal total sums complete the majorization check.

Apply the real symmetric Schur–Horn theorem separately to each block. Block-diagonal orthogonal conjugation of Q₀ realizes both desired diagonals at once, preserving projectionhood, spectra and compression ranks. This attains f+1=ceil(a). No independent choice of two arbitrary compressions is being glued: the complementary fractional eigenvalues are paired first in one global projection, then both sides are conjugated within their blocks. This addresses the main potential compatibility gap.

## Universal criterion and quantifiers

For every projection with this diagonal, the matroid inequalities follow if |J|≤r ceil(Σ_Jq_i) for every J. Conversely, if one J violates that condition, its independently constructed attaining projection is a counterexample to universal strict paving. One projection for that one J suffices. Simultaneously minimizing all compression ranks is neither required nor asserted.

For s=|J|≥1,

    s≤r ceil(a) iff a>floor((s−1)/r).

The strict inequality is essential: a equal to the right side has ceiling too small. Sorting q increasingly minimizes the trace for each cardinality. Between cardinalities kr+1 and (k+1)r, the right side equals k, while the sorted prefix mass is nondecreasing. It therefore suffices, and is necessary, to check

    Σ_{i≤kr+1}q_i>k   whenever kr+1≤n.

For d sorted decreasingly this is exactly

    Σ_{i≤kr+1}d_i<(r−1)k+1.

The criterion is identical over R and C: the rank lower bound works in both, and every violation has a real witness. Its quantifiers are ∀P in one fixed finite diagonal fiber, ∃a partition depending on P, with a common norm bound obtained below. It is not a characterization of existence of just one good member, nor a per-projection test from the diagonal alone.

## Fiber-dependent gap and boundaries

The finite fiber is closed and bounded in the real finite-dimensional vector space of symmetric/Hermitian matrices, hence compact. For a fixed coordinate partition each compression norm is continuous and 1-Lipschitz in P. The maximum over its r blocks and then the minimum over finitely many partitions remain continuous and 1-Lipschitz. Thus if π_r(P)<1 everywhere on this fiber, its attained maximum is below one. This gives exactly a common positive ε_d. Compactness is applied after fixing n and d, not to an unbounded family of dimensions.

For r=1, the criterion and integer total force d=0, which is exactly the sole strictly one-pavable projection. For r=n, only the length-one condition remains: max d_i<1, equivalent to paving by singletons. The zero projection is included; the identity is rejected. Zero entries of d are not forbidden in general. Equality at the constant threshold α=1−1/r is allowed whenever the diagonal is admissible: q=1/r gives every subset rank at least |J|/r. Replacing the prefix inequalities by weak ones is nevertheless false; these are different equalities.

The proof is an existence construction using Schur–Horn. Its finite-dimensional induction terminates by reducing dimension; the PR makes no bit-complexity claim, effective exact-real comparison promise, or formula for the best ε_d. No such claim is needed for the source's finite-fiber question.

## Independent exact certificates

The independent script uses only Fraction arithmetic, rather than the author's programs or an unavailable symbolic dependency. It checked 15 real rational projections obtained by a nontrivial rational orthogonal pair and the fractional couplings θ=0,9/25,1/2,16/25,1, including three different integer-spectrum configurations. Idempotence, symmetry, trace/rank and attained compression rank were verified exactly.

Its strict-violation example has

    q=(1/25,4/25,4/25,24/25,21/25,21/25),   m=3,
    J={1,2,3},   Σ_Jq_i=9/25,   rank Q[J]=1.

It arises from u=(1,2,2)/3 and

    Q=[[θuuᵀ, (12/25)uuᵀ],[(12/25)uuᵀ,I−θuuᵀ]], θ=9/25.

All diagonal entries lie strictly between zero and one, and n=2m, so the elementary max-diagonal-one and total-rank obstructions do not explain failure. Nevertheless all 31 unordered nonempty two-partitions have a singular Q-compression. This is a direct certificate for the strict-violation case beyond the older equality obstruction. It is an independent verification example, not a separate novelty claim.

The program also checked 34 subset/prefix equivalences and 232 majorization subsets of selected admissible diagonals, rejected the weak-inequality mutant at a genuine equality obstruction, and verified an actual positive half-diagonal paired projection. These are small exact checks supplementing the general proof. A first script run stopped on a tuple/list concatenation TypeError before any mathematical check; the builder was corrected, then the entire check completed successfully. No failed mathematical condition was hidden or interpreted as a theorem counterexample.

## Other approaches and priority distinction

The M4 formula follows from the four projection row-square identities, complementary off-diagonal magnitudes and enumeration of the seven two-partitions. The complex family squares to the identity after centering; the real zero-entry obstruction follows from the three off-diagonal equations. The Bloch scaling and centered/direct normalization are correct. These are prior-attributed specializations, and are not the general solution's novelty basis.

The CFMT reconstruction has unit row norms and B*B=2I. Any two-partition puts at least m of its first 2m rows together. A coefficient vector annihilating the first m−1 columns leaves a squared norm ≤2/(m+1), giving a complementary projection compression with norm ≥m/(m+1). This proves absence of a dimension-uniform gap, while every fixed half-diagonal fiber satisfies the finite strict theorem. The source proposition and its proof were read; the distinction is valid.

Casazza–Edidin proposition 9.6 gives the sufficient prefix inequalities and problem 9.7 asks necessity. Proposition 9.8 handles equality by an integer block construction; it does not cover every strict violation. The fractional minimum-rank construction supplies exactly that missing implication. These older statements cannot simply be labeled an already published full answer. On the other hand, Schur–Horn and matroid partition are classical, and no new general method follows from this proof. A later theorem or equivalent moment-polytope result could establish priority elsewhere. No verified such complete prior result was identified in this bounded review, and current novelty remains a separate unresolved gate.
