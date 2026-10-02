# Turn 4: a universal same-type route and its critical exponent

Problem 30003472 / OWR-15427-014. Substantive author turn **4 of 5**.
Status: **the unrestricted route is rigorous but does not close the probability gap**.

## 1. A current primary theorem changes the available route

Bukh and Vasileuski, [New Bounds for the Same-Type Lemma](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v31i2p60), Electronic Journal of Combinatorics 31(2), P2.60 (28 June 2024), Theorem 1, prove for dimension d and m colors the lower bound

    c(m,d) ≥ d^(−50d³) m^(−d²).

In particular, for n disjoint planar finite sets in joint general position, each with M points, there are subsets of at least γ_n M points in each color such that every colorful transversal has the same order type, where

    γ_n = 2^(−400) n^(−4).                              (1)

This is an existing theorem, not a result of this attempt. The primary PDF was read, including its polynomial-partition/Local-Lemma proof of the lower bound, and the formula was checked against the author's current publication page. The theorem improves older exponentially small fractions. Searches through 2026-10-02 did not identify a better planar exponent in this setting. The same paper's upper bound is 4n^(−2), so exponent 4 is not established as optimal.

The theorem concerns finite colored sets. Applying it directly to a singular measure would require an unjustified continuum partition step. The following finite-cloud argument avoids that problem completely.

## 2. From colored sets to disjoint subsets of one set

Fix n≥3 and let P be an M-point planar set in general position, with M so large that γ_n M>n. Replace P by n separately colored, sufficiently small perturbed copies X_1,...,X_n, each with one copy of every point of P. Choose the perturbations so that their union is in general position and every triple whose three underlying points in P are distinct keeps its original orientation. This is possible because there are finitely many nonzero determinants to preserve.

Apply the colored theorem to obtain Y_i⊂X_i of size at least γ_n M and a common transversal orientation pattern. Project Y_i back to its underlying subset Z_i⊂P; this projection is injective within each color.

**Overlap claim:** |Z_i∩Z_j|≤1 for distinct i,j. Otherwise take two distinct underlying points p,q in that intersection. Choose a third color k and a point r∈Z_k outside {p,q}; this is possible because |Z_k|>2. The colorful triples formed from (p_i,q_j,r_k) and (q_i,p_j,r_k) have opposite orientations: small perturbations preserve the opposite original orientations of (p,q,r) and (q,p,r). This contradicts the same-type property.

Remove from each Z_i every point shared with another Z_j. At most n−1 points are removed from any one set. The resulting sets W_i are pairwise disjoint, have

    |W_i| ≥ γ_n M−(n−1),                                (2)

and retain the common transversal order type Ω. The same-type property is not required to survive collapsed repeated underlying points; they were removed first.

Let p_P denote sampling independently with replacement from the uniform empirical measure on P, declaring repeated-point tuples non-simple. The n! assignments of sample labels to the disjoint W_i are disjoint events, all giving the same unlabeled type. Therefore

    max_ω p_P(ω) ≥ n! [γ_n−(n−1)/M]^n.                 (3)

This explicit disjointness step is essential for the factorial gain.

## 3. Transfer to every line-null probability measure

Let μ be any Borel planar probability measure charging no line. Sample an M-point pool P_M independently from μ. It is in general position almost surely. For a fixed n-point simple type ω, let q_M(ω) be its empirical with-replacement sampling probability.

A direct bounded-kernel calculation gives

    E q_M(ω) = ((M)_n/M^n) p_μ(ω),
    Var(q_M(ω)) ≤ n²/M.                                 (4)

For the expectation, only tuples of distinct pool indices contribute. For the variance, covariance vanishes for two index-tuples with disjoint underlying pool indices. The fraction of pairs sharing an index is at most n²/M, by a union bound over their n² possible cross-index equalities; each covariance has absolute value at most one. These arguments allow internal repetitions in the index tuples, whose kernel value is zero.

There are finitely many n-point order types. Chebyshev's inequality and a finite union bound therefore give deterministic general-position pools with M→∞ for which all q_M(ω) converge simultaneously to p_μ(ω). The finite maximum also converges. Passing to the limit in (3) proves the universal statement

**Theorem.** For every line-null planar probability measure μ and every n≥3,

    max_ω p_μ(ω) ≥ n! (2^(−400) n^(−4))^n.             (5)

No absolute continuity, bounded support, or full type support is used. No fixed geometric family of homogeneous continuum regions is assumed to exist. The finite clouds and the empirical pools are mathematical existence devices, not a proposed feasible exhaustive computation.

## 4. Why the universal estimate does not solve the target

Combine (5) with the Turn 1 lower bound T_n≥1024(n!)³/128^n. The resulting ratio lower bound is only

    max p / min p ≥ 1024 (n!)^4 (2^(−400)/(128 n^4))^n
                  ≥ 1024 (2^(−407) e^(−4))^n.          (6)

For n≥3 this is smaller than one. Thus this comparison supplies no useful gap at all, beyond the trivial ratio bound. Equation (5) has the correct n^(−3n) scale for a heavy type, but an exponentially unfavorable constant. The standard counting bound alone already gives a heavy-type lower bound on this logarithmic scale; the useful new information here is the precise structural sufficient criterion below, not a claimed new resolution.

More generally, suppose a uniform same-type construction supplied γ_n≥a n^(−p), with a>0 independent of the measure and finite pool. The same transfer would give

    max p / min p ≥ 1024 [a n^(4−p)/(128e^4)]^n.        (7)

Any exponent p<4 would therefore imply the **strong uniform-threshold interpretation** of the original question. A bound γ_n n^4→∞ would also suffice. The cited p=4 result is exactly critical for this method. Its upper bound of order n^(−2) leaves room for an improvement but does not prove one.

This is a conditional reduction, not an equivalence and not a proof that no other route can work.

## 5. Attempts at an improvement and the sharp remaining obstruction

The polynomial-partition argument has a geometric bad-transversal hypergraph. In the planar case the available edge control naturally leads to an independent-transversal exponent corresponding to four. Merely hoping for a logarithmic improvement in an abstract hypergraph independence estimate is insufficient: an additional geometric/codegree hypothesis must be proved and checked quantitatively. No such hypothesis has been established here.

Likewise, iid independence of six-point blocks cannot supply the missing factor without controlling how many full types realize each block word; this is the fiber gap identified in Turn 1. The present cloud construction solves a different transfer issue and does not repair that missing comparison.

The last remaining author turn will test whether the convex-position statistic itself can be forced away from the critical n^(−3n) scale for arbitrary singular full-support measures. If it cannot, the final packet will record that obstruction and retain the original unresolved disposition.

Completion estimate toward the unrestricted goal: **25%**, subjective and unchanged. Author count **4/5**. One substantive turn remains.
