# Turn 2: sparse-support relations and a logarithmic support barrier

## Outcome and scope

The sharp upper growth of the unrestricted finite-prefix maximum M(D) remains unresolved. This turn proves a structural upper control on the relations that can create its multiplicities.

A nontrivial relation means a finitely supported vector epsilon_i in {-1,0,1}, not identically zero, with sum_i epsilon_i i=0 and every support element in A. Equivalently it is an equality between two disjoint nonempty finite subsets. Its length is the size ell of the support, and its scale m is the largest support element. When two representations share elements, those are cancelled before ell and m are measured.

**Theorem A.** For every fixed ell, almost surely there are only finitely many such relations of length ell. Quantitatively, the expected number with largest support element at least X is at most

    C_ell (1+log X)^(ell-2) / X,   X>=2.                    (1)

**Theorem B.** For every c in (0,1) satisfying

    c log(2e/c)<1,

almost surely all sufficiently large-scale relations have

    ell>c log m.                                           (2)

The condition permits c=1/4. More generally it permits all c below the unique root in (0,1) of c log(2e/c)=1. This is a sufficient constant from the present estimate, not an optimal support threshold.

**Corollary.** For every fixed h, the representation count restricted to subsets of cardinality at most h has an almost-sure finite global maximum. Its finite-prefix maximum eventually stabilizes. No such bound for unrestricted cardinality is asserted; turn 1 already gives almost-sure divergence there.

These are elementary first-moment and Borel–Cantelli arguments. They do not establish an upper logarithmic exponent for M(D), and no novelty claim is made.

## 1. Expose the largest two entries

Count each relation in the unique orientation in which the sign of its largest entry m is +1. Let n be the second-largest entry. Lengths one and two are impossible because the entries are positive and distinct, so ell>=3. The relation gives

    m <= sum of all other support entries <= (ell-1)n,

hence n>=m/(ell-1). Let R be the set of the other ell-2 entries. For any fixed m,R and choices of the ell-1 signs on n and R, the equation determines n uniquely:

    n=-epsilon_n (m+sum_{r in R} epsilon_r r).              (3)

Only choices for which n is a valid distinct integer with max R<n<m contribute. For every valid choice the selection probability is

    1/(mn) product_{r in R}1/r
       <= (ell-1)m^{-2} product_{r in R}1/r.

There are at most 2^(ell-1) sign choices. Dropping the restrictions on R other than R subset {1,...,m-1} and |R|=ell-2, and using the elementary-symmetric bound, yields

    E(number of oriented length-ell relations at scale m)
       <= [2^(ell-1)(ell-1)/(ell-2)!]
                H_{m-1}^{ell-2}/m^2,                     (4)

where H_j=sum_{i=1}^j1/i. The bound does not multiply by a second free choice of n; (3) is what saves that factor. Independence is applied only after distinctness has been verified for actual contributing tuples. Repeated tuples introduced in the harmonic-power upper bound merely increase that bound.

## 2. Fixed length is summable

For integer X>=2, split the m-tail into the intervals [2^r X,2^(r+1)X), r>=0. Put u=1+log X and j=ell-2. Since H_{m-1}<=1+log m,

    sum_{m>=X} H_{m-1}^j/m^2
       <= (u^j/X) sum_{r>=0}2^{-r}(1+(r+1)log 2)^j.        (5)

The last series is finite for every fixed j. Combining (4)–(5) proves (1), with an explicit finite constant obtained from their displayed factors. It also shows that the expected total number of length-ell relations is finite. Therefore their total number is finite almost surely. A countable intersection gives this simultaneously for every fixed ell.

The length is fixed in this statement; (5)'s constant is not treated as uniform in ell. A separate calculation is required for growing lengths, which follows next.

## 3. Uniform growing-length calculation

Fix c in (0,1) with c log(2e/c)<1. In the dyadic scale D<=m<2D, set

    L=floor(c log(2D)),   u=1+log(2D).

Every relation violating ell>c log m has ell<=L. Summing (4) first over m in that block, using sum_{D<=m<2D}m^{-2}<=1/D, then over ell gives

    E(number of such short relations in [D,2D))
       <= (2/D) sum_{j=1}^{L-2}(j+1)(2u)^j/j!             (6)

when L>=3; otherwise the count is zero. For sufficiently large D, L<2u and the terms (2u)^j/j! are nondecreasing for 0<=j<=L. Thus (6) is at most

    [2L(L+1)/D] (2u)^L/L!
       <= [2L(L+1)/D] (2eu/L)^L.                          (7)

The factorial estimate L!>=(L/e)^L follows, for example, by summing log j and comparing with the integral of log t. Because L=c log D+O(1) and u=log D+O(1), the logarithm of (7), divided by log D, tends to

    -1+c log(2e/c)<0.

Choose delta>0 smaller than its negation. For large D the probability of at least one short relation in that block is at most D^{-delta}, by Markov's inequality. On D=2^n these probabilities are summable. Borel–Cantelli proves that only finitely many blocks contain a violation, giving (2).

No independence between different relation events or blocks is needed for this first Borel–Cantelli application. The random set indicators were used independently only for the support selection weights in (4).

The function c log(2e/c) is continuous and strictly increasing on (0,1), since its derivative is log(2/c)>0. It tends to zero at zero and exceeds one at c=1, so the stated critical root is unique. In particular c=1/4 is admissible because

    (1/4)log(8e)=(1+3log2)/4<1.

The logarithmic scale in (2) measures the largest differing entry, not a common large entry that could be adjoined to both sides of an old relation.

## 4. Fixed-cardinality multiplicity is uniformly finite

For fixed h>=1 define

    r_{A,<=h}(x)=#{B subset A: |B|<=h, sum B=x}.

By Theorem A, the union of supports of all relations of length at most 2h is almost surely finite. Choose a finite integer N_h containing that union; if there are no such relations, take N_h=0.

Fix x with at least one representation B_0 of size at most h. For any other such representation B, cancel B intersect B_0. Their nontrivial symmetric difference, if nonempty, is a relation of length at most 2h, so lies in [1,N_h]. Hence

    B outside [1,N_h] = B_0 outside [1,N_h].

All representations of x therefore share the same outside part. Their inside parts are subsets of the one fixed finite set A intersect [1,N_h], and have one common sum. Consequently

    r_{A,<=h}(x)<=m(A intersect [1,N_h])<=2^{N_h}           (8)

for every x, with the sharper first bound often much smaller. This is a finite random bound depending on A and h, not a deterministic universal constant. Since finite-prefix maxima are nondecreasing integers bounded by (8), they eventually stabilize almost surely. The argument applies simultaneously to all integer h by a countable intersection.

This shows that the large multiplicities from turn 1 cannot be explained by any fixed-cardinality family of representations. It does not bound the number of long-support representations in one fiber.

## 5. Relative support in the selected prefix

The standard count N(D)=|A intersect [1,D]| satisfies N(D)/log D->1 almost surely. One direct proof uses E N(D)=log D+O(1), Var N(D)<=log D+O(1), Chebyshev and Borel–Cantelli at D_j=floor(exp(j^2)), followed by monotonicity between adjacent D_j. Their logarithms have ratio tending to one.

Thus (2) also says that any sufficiently large relation uses a positive proportion, at least c-o(1), of all selected entries up to its largest differing element. The count law alone does not convert this support barrier into a sharp upper bound for the size of a same-sum fiber: families of binary vectors can have many codewords despite a positive relative-distance condition. No such unjustified combinatorial conversion is asserted.

## Remaining gap at 2/5

We have ruled out bounded-support and small-relative-support mechanisms for persistent late relations. The desired upper bound must still control the number and organization of long, overlapping relations that create a large representation fiber. The proved lower exponent from turn 1 remains unmatched. No convergence theorem or exact growth constant has been obtained.

verify_turn2.py enumerates all oriented signed relations through small scales and checks the exact weighted bound (4), plus fixed-cardinality core implications in finite controls. It does not test the infinite Borel–Cantelli conclusion by simulation.
