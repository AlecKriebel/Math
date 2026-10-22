# Attempt 5 of 5: glue the two free resolutions over a product ring

**Verdict: NO RESOLUTION after 5/5 substantive attempts.** A constructive equivalence identifies the exact obstruction to merging the two field resolutions: G is FL over F1 x F2 if and only if their Euler characteristics agree. Separate FL hypotheses only give FP over the product ring. The missing implication is exactly the original problem, so this gluing argument must not be presented as a solution.

## The tempting common coefficient ring

Let R=F1 x F2. Then RG is canonically F1G x F2G, and an RG-module is a pair of modules over the two factors. Choose finite free resolutions P,Q of the trivial modules, padding with zero terms to a common maximum degree N. Let

    P_i=(F1G)^{a_i},   Q_i=(F2G)^{b_i}.

The pair complex (P,Q) is a finite resolution of the trivial RG-module R. Each paired term is finitely generated projective: it is a sum of a_i copies of e1 RG and b_i copies of e2 RG, where e1=(1,0),e2=(0,1). Hence G is FP(R).

But a pair of free modules of different ranks is generally not free over the product ring. Applying the two augmentation maps already detects the unequal ranks. Thus FP(R) has not established FL(R). The two original resolutions are finite free over their own factors; no common-rank statement has been supplied.

## Proposition: exact free-resolution synchronization criterion

Under the given FL(F1),FL(F2) hypotheses,

    G is FL(F1 x F2)  <=>  chi_F1(G)=chi_F2(G).             (1)

Necessity: a finite free RG-resolution has a single rank n_i in each degree. Applying the exact factor projections gives free resolutions over F1G,F2G with the same ranks, and therefore equal alternating sums.

Sufficiency is constructive. Suppose

    sum_i (-1)^i a_i = sum_i (-1)^i b_i.

Set delta_i=a_i-b_i, s_{-1}=0 and

    s_i=delta_i-s_{i-1}.

Equivalently s_i=sum_{j=0}^i (-1)^{i-j}delta_j. Equality of Euler sums means s_N=0.

For i=0,...,N-1, adjoin to P a contractible free disk complex with max(-s_i,0) generators in degrees i and i+1 and identity differential between them. Adjoin to Q the analogous disk with max(s_i,0) generators. These direct sums do not alter the augmented homology and remain finite free resolutions. A disk in degrees 0 and 1 has zero augmentation on its degree-zero summand, so the augmentation is preserved as well.

Let a'_i,b'_i denote the resulting ranks. The rank difference in degree i is

    a'_i-b'_i = delta_i-s_i-s_{i-1}=0,

where missing disks below degree zero and above N contribute zero and s_N=0. Thus paired terms are free RG-modules of the same finite rank. Their paired differential gives the required finite free RG-resolution of R. This proves (1).

## Sanity checks and the exact obstruction

The accompanying script verifies the recurrence and nonnegative stabilization for every pair of length-four nonnegative rank vectors with entries at most 3 and equal alternating sums: 8,092 pairs. These numerical checks validate the bookkeeping only. The proof above, rather than the finite test, establishes the unrestricted rank-vector lemma.

If the Euler sums differ, no choice of contractible free disks can synchronize all ranks: every disk contributes equal ranks in adjacent degrees and has Euler sum zero. Some final nonzero difference survives. In the projective Euler class of the paired complex, that difference is represented by

    chi_F1(G)[e1 RG] + chi_F2(G)[e2 RG]

modulo the diagonal class [RG]=[e1 RG]+[e2 RG]. Augmentation to R detects a nonzero pair of unequal component ranks, so it cannot be removed by pretending the paired projective modules are free.

This is a reformulation, not a proof that the obstruction must vanish for trivial group modules. Establishing that it always vanishes would answer the original question negatively; realizing a nonzero obstruction while retaining FL in each factor would answer it positively. Neither has been achieved.

## Why a connected coefficient ring would help, and why it is unavailable

A genuine finite projective resolution over a connected commutative coefficient ring A, after applying augmentation, yields a bounded complex of finitely generated projective A-modules. Their ranks are locally constant on Spec(A), so the alternating rank is constant on a connected spectrum. If the resolution base-changes to both desired field resolutions, it forces the same Euler characteristic in both fibers.

There is no theorem in this attempt constructing such a connected coefficient-ring resolution from the two separate FL assumptions. Using the disconnected product ring is easy precisely because it allows the ranks to vary on its two components. Replacing it by a localization of Z, or declaring the needed base-change exactness, is the unproved step rather than a conclusion.

## Final mathematical status

No group meeting both FL hypotheses with distinct Euler characteristics was constructed, and no universal equality theorem was proved. The five attempts establish only the following scoped facts:

1. Equal characteristic and common finite-rank resolutions force equality.
2. Degreewise finitely generated integral homology forces equality; an example would need a higher-degree non-finite-generation defect.
3. Z[1/p] realizes a homological difference but fails FP1; its natural cyclic-extension repair cancels the difference.
4. Ordinary Bestvina-Brady groups cannot witness the problem, by a credited known chain formula.
5. The product-ring gluing obstruction is exactly the Euler difference; separate FL does not dispose of that obstruction.

All are reductions, exclusions, or explanatory examples. No first-priority claim is made. Retrieval, testing, review and packaging are not additional proof-attempt turns.
