# Fixed greedy staircase prefixes of uniform 1324-avoiders

## Result and unresolved scope

Let Π_n be exactly uniform on Av_n(1324). In its greedy descending staircase gridding, let m_j(Π_n) be the number of points in the jth cell, setting subsequent m_j to zero after the gridding terminates. Put S_K=sum_{j=1}^K m_j.

**Theorem.** For every fixed positive integer K and every fixed ε∈(0,1], there is r_K(ε)>0 such that

    limsup_{n→∞} (1/n) log P(S_K(Π_n)≥ε n) ≤ −r_K(ε).            (A)

Thus every fixed initial number of greedy cells has vanishing normalized mass, with an exponential tail. In particular, the subfamily whose greedy gridding has at most K nonempty cells has upper exponential growth strictly below the growth rate of the entire class.

This is not a proof that the largest cell is o(n), and it does not yet prove the anti-diagonal permuton limit for 1324. A deterministic family below exhibits the exact missing implication. No counterexample under the uniform law is obtained.

## 1. Exact gridding and credited inputs

Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Proposition 1 and its complete proof, pp.3–4, provide the greedy descending staircase. Primary author manuscript:

https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

The cells alternate between Av(213) and Av(132), proceeding down and right. Consecutive cells share a row or a column; nonconsecutive cells are strictly ordered northwest to southeast. The algorithm can equivalently be expressed by the following alternating peeling operation on the remaining standardized permutation:

- At odd steps, remove the largest possible top-value interval whose induced pattern avoids 213.
- At even steps, remove the longest initial positional segment whose induced pattern avoids 132.

Why this is exactly their greedy algorithm: at an odd step, the first excluded value is the highest point that can serve as the 1 of a 213 in the remaining permutation. All larger values avoid 213, and including that value completes such an occurrence. At an even step, the first excluded position is the earliest point that can serve as the 2 of a 132; it is precisely the endpoint of the first prefix containing 132. The empty forbidden-occurrence case removes the whole remainder. Thus after deleting the previous cells, the next cell is an extreme one-dimensional avoidance frontier in the remaining pattern. The source proves that these cuts give a valid staircase for 1324-avoiders; we do not assume this for arbitrary permutations.

We use the previously proved minimum-insertion frontier lemma in the following precise form. For a fixed α of length at least two, τ=α⊖1, and a uniform Σ_q in Av_q(τ), let L be one plus the length of its longest α-free initial segment. With λ=lim |Av_q(τ)|^(1/q) and

    gamma = log C(1/λ)>0,
    C(z)=(1−sqrt(1−4z))/(2z),

one has, whenever ell_q/q→a∈(0,1],

    limsup (1/q)log P(L(Σ_q)≥ell_q) ≤ −a gamma.                  (1)

Here 4≤λ<∞. The exact descendant inequality underlying this already established lemma is

    |{σ∈Av_q(τ):L(σ)≥ell}| * [ell/(ell+2t)] binom(ell+2t,t)
       ≤ |Av_{q+t}(τ)|.                                      (2)

The parent is uniquely recovered by deleting its t smallest entries, so (2) is a disjoint-descendant count, not a random-generator approximation. Its optimization gives (1), including the stated variable-threshold form. The present theorem uses no ratio asymptotic and no assumed numerical value of λ.

## 2. Two frontiers under the exact uniform 1324 law

Set a_q=|Av_q(1324)| and a_0=1. The pattern 1324 is skew indecomposable, so Av(1324) is skew-sum closed and

    a_k a_{q−k}≤a_q.                                         (3)

Fekete and the fixed-pattern exponential bound give 4≤λ=lim a_q^(1/q)<∞. Symmetries preserve these exact counts.

For σ∈Av_q(1324), let T(σ) be the size of its largest top-value interval avoiding 213, and let P(σ) be the size of its longest prefix avoiding 132. Both have the frontier bound (1), up to the immaterial addition of one:

- For T, take reverse(σ^{-1}). Inversion fixes 1324, reversal sends it to 4231=312⊖1, and the top-value interval becomes the initial prefix. The inverse of 213 is 213 and its reversal is 312.
- For P, take complement(σ). Complement sends 1324 to 4231 and 132 to 312, preserving initial positions.

These transformations are bijections of the complete finite classes, hence preserve the uniform law exactly.

We need a uniform version of the tail estimate. For fixed δ∈[0,1) and fixed η∈(0,1−δ], and F equal to T or P,

    limsup_{n→∞} max_{0≤k≤δ n}
      (1/n)log P_{n−k}(F≥η n) ≤ −η gamma.                     (4)

To justify the uniformity, suppose (4) fails. Select offending k_n and a subsequence along which (n−k_n)/n→theta∈[1−δ,1]. Apply (1) to lengths q_n=n−k_n and thresholds eta n+O(1). Their ratio tends to eta/theta∈(0,1]. Multiplying the bound by q_n/n gives −eta gamma, a contradiction. The lengths q_n tend to infinity; the same variable-threshold statement is valid on this subsequence. Impossible thresholds have probability zero and can be discarded. This proves (4) rather than assuming that a pointwise error term is uniform.

The slightly more general range eta≤1 is also harmless: if q_n<eta n+O(1) the event is impossible, and every subsequence with nonzero probability again has theta≥eta. We use this extension in Section 4.

## 3. Small deletion preserves frontier rarity, with all weights retained

Suppose a deterministic rule deletes k entries of π∈Av_n(1324) and returns a standardized remainder σ∈Av_{n−k}(1324). For any specified remainder σ, at most

    binom(n,k)^2 a_k                                         (5)

original permutations can return it. Indeed, choose the k deleted positions, the k deleted values, and the standardized permutation induced by the deleted points. The latter avoids 1324 by heredity, so there are at most a_k choices. These data and σ determine π uniquely. Some data combinations are invalid, which only makes (5) an upper bound.

For a family B of remainders of size n−k, (3) and (5) yield the exact probability inequality

    P_n(deletion size=k and remainder∈B)
      ≤ binom(n,k)^2 * [a_k a_{n−k}/a_n] * P_{n−k}(B)
      ≤ binom(n,k)^2 P_{n−k}(B).                              (6)

This inequality does not claim that the remainder is uniform. Its completion multiplicity is explicitly bounded before comparison with the uniform law of that smaller class.

For δ<1/2 and the frontier event B={F≥eta n}, summing (6) over **all** k≤δn, using (4) and the binomial entropy estimate, gives

    P_n(deletion size≤δn and remainder frontier≥eta n)
      ≤ exp{n[2h(δ)−eta gamma+o(1)]},                         (7)

where h(x)=−x log x−(1−x)log(1−x). The at-most n+1 deletion sizes contribute only o(n) to the logarithm. This includes all combinatorial and normalization costs.

## 4. Proof of the fixed-prefix theorem

For K=1, the first cell has size T(Π_n), so (A) holds with r_1(ε)=ε gamma.

Suppose the result holds for K−1 at every positive threshold. Fix ε∈(0,1]. Choose

    0<δ<min(ε/2,1/2),    2h(δ)<ε gamma/4.                    (8)

Such δ exists since h(δ)→0. If S_K≥εn, either S_{K−1}>δn or the Kth cell has at least (ε−δ)n points. On the latter event delete the first K−1 cells. Their total size is at most δn, and the Kth cell is exactly the appropriate frontier, T or P, of the remainder by Section 1.

Use (7) with eta=ε−δ to obtain

    P_n(S_K≥εn)
      ≤ P_n(S_{K−1}>δn)
          + exp{n[2h(δ)−(ε−δ)gamma+o(1)]}.                    (9)

Because ε−δ>ε/2 and (8) holds, the second exponential rate is strictly less than −ε gamma/4. The first term has a strictly negative rate by the induction hypothesis. Thus, for example, we may take

    r_K(ε)=min(r_{K−1}(δ), ε gamma/4)>0.                       (10)

Rounding thresholds changes nothing in these rates. This proves (A) for each fixed K. No rate uniform in growing K is claimed.

Let N(π) be the number of nonempty greedy cells. If N(π)≤K then S_K=n. Consequently

    limsup |{π∈Av_n(1324):N(π)≤K}|^(1/n)
      ≤ λ exp(−r_K(1)) < λ.                                 (11)

This is a statement about the specified greedy-gridding subfamily. We have not asserted that greedy cell count is minimal among all possible griddings or that this subfamily is hereditary.

## 5. The missing geometry: largest cell, not first fixed cells

Let M=max_j m_j for any descending staircase gridding, and let μ_π be the square-spread permuton.

For a point in cell j, every cell indexed at most j−2 lies northwest, and every cell indexed at least j+2 lies southeast. Only cells j−1,j,j+1 can contribute unconstrained relative positions and values. Put

    q_j=m_{j−1}+m_j+m_{j+1},

with missing cells assigned size zero. If there are a points in the earlier nonadjacent cells and b points in the later nonadjacent cells, then a+b+q_j=n and

    a+1≤i≤n−b,     b+1≤π(i)≤n−a.

Hence

    |i+π(i)−(n+1)|≤q_j−1≤3M−1.

Inside the corresponding permutation square this implies |x+y−1|≤3M/n. Coupling (X,Y) with (X,1−X) gives the deterministic estimate

    d_BL(μ_π,Law(U,1−U))≤3M/n.                               (12)

One may also count increasing pairs: they occur only within a cell or between adjacent cells, giving at most (3/2)sum_j m_j²≤(3/2)nM such pairs. Both estimates identify M=o(n) in probability as a sufficient bridge to the desired anti-diagonal limit.

Theorem (A) controls every fixed initial index. It does not bound a cell whose index diverges with n. Applying (A) with K=K_n→∞ is unjustified: the positive constants in (10) can shrink with K, and no uniform bound has been proved.

## 6. Explicit deterministic nonimplication example

Let G=2413, let r≥1 and N≥1, and form

    pi = G⊖...⊖G  (r copies)  ⊖ I_N ⊖ G⊖...⊖G  (r copies).

Both G and I_N avoid 1324, and 1324 is skew indecomposable, so pi avoids 1324. Its size is n=N+8r.

The patterns 132 and 213 are themselves skew indecomposable. Thus an occurrence of either inside this skew sum lies in a single block. In G, the largest top-value interval avoiding 213 consists of its top three values; the longest initial segment avoiding 132 consists of its first three positions. Alternating the greedy peeling operations therefore gives the exact cell-size sequence

    3, [4 repeated r−1 times], N+4,
       [4 repeated r−1 times], 1.                             (13)

For the first step, removing the top three values leaves the singleton minimum. At the next step that singleton precedes the next whole block in skew order, so the relevant frontier comprises the singleton and the next block's three allowable entries. This leaves another singleton and proves the repeated pattern by induction. When the central I_N is reached, it avoids both forbidden triples and is wholly absorbed in that frontier, yielding N+4. The final singleton gives the last cell.

Take r=r_n→∞ with r_n=o(n), adjusting N=n−8r_n>0. Every fixed number of cells at either end contains only O(1) points, yet M=N+4=n−o(n). The middle increasing block has mass 1−o(1), and the remaining entries have vanishing mass, so μ_pi→μ_I, the diagonal permuton. For example the continuous 1-Lipschitz test function |x+y−1|/sqrt(2) separates this limit from the anti-diagonal: its limit integral is 1/(2sqrt(2)).

This family is only a deterministic counterexample to the implication from bounded-index cell control to the desired geometry. It is **not** a counterexample under the exact uniform Av_n(1324) law, and supplies no lower bound on that family's uniform probability.

## 7. Remaining task and source-status check

The outstanding sufficient estimate is

    for every ε>0, P(max_j m_j(Π_n)≥εn)→0.                    (14)

A weaker argument could instead directly control anti-diagonal crossing mass or increasing-pair density. Neither (14) nor such an alternative has been established here. Later greedy cells have potentially biased distributions; (6) only absorbs deletion of a sufficiently small fraction, not an arbitrary earlier macroscopic part of the permutation.

A current primary-source check found Robert Brignall, *Shuffle automata and the growth of 1324-avoiding permutations*, arXiv:2610.02535v1, submitted 1 October 2026, https://arxiv.org/abs/2610.02535v1 . Its inspected introduction and staircase section describe an upper growth bound 13.167248 and refinements of the domino/interleaving encoding. That numerical bound is not used in this theorem, and it is not a uniform-law permuton limit result in the inspected statements. Exact enumeration of 1324 remains unnecessary for (A): the proof uses only finite exponential growth, exact skew closure, and the established frontier amplification inequality.

No source text is reproduced as a deliverable, no new novelty claim is made, and the universal fixed-alpha conjecture remains unresolved by this argument.
