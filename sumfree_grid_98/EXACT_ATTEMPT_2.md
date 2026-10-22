# Exact finite-grid attempt 2: the three-point alphabet

Date: 2026-10-20. All grids here are positive {1,…,N}^d. This attempt produces an exact reduction for N=3, a theorem for infinitely many dimensions, and an exhaustive integer proof of f_6(3)=706. It does not solve arbitrary N.

## 1. Exact Boolean-family reduction

Let I be the set of vectors in {1,2,3}^d that have both a coordinate 1 and a coordinate 3. Such a vector cannot be a sum (because of its 1 coordinate) or a summand in a grid-internal sum (because of its 3 coordinate). Thus every extremizer includes I, and

|I|=3^d−2^(d+1)+1.

All remaining points belong to the two binary cubes

L_A=1⃗+1_A, U_C=2⃗+1_C, A,C⊆[d].

Their only overlap is L_[d]=U_∅=2⃗. Every sum relation is exactly

L_A+L_B=U_(A∪B), where A∩B=∅.

This includes A=B=∅, giving L_∅+L_∅=U_∅.

For a lower selected family F define D(F)={A∪B:A,B∈F, A∩B=∅}. The selected upper family must avoid D(F).

If ∅∈F, then D(F)⊇F and [d]∉F because the repeated-summand relation forbids the center. Hence the active portion has size at most 2^d+|F|−|D(F)|≤2^d.

If ∅∉F, then ∅∉D(F). We can require [d]∈F without loss: adding [d] creates no disjoint pair in F and adds the center if it was absent. Saturating the upper family with every C∉D(F), the active size is

|F|+2^d−|D(F)|−1,

where the minus one counts the shared center only once. It is at least 2^d by taking F={[d]}, so the ∅∈F case cannot improve the maximum. Therefore the following exact identity holds for every d≥1:

f_d(3)=3^d−2^d+M_d,

M_d=max{|F|−|D(F)|: F⊆2^[d], ∅∉F, [d]∈F}.

## 2. A primary set-family theorem gives infinitely many exact values

Let p(d) be the maximum size of a partition-free family, meaning a family with no A,B,C satisfying A∩B=∅ and A∪B=C. For every F, the family F\D(F) is partition-free. Consequently

|F|−|D(F)|≤|F\D(F)|≤p(d).

On the other hand, if F={A:|A|≥k}, then D(F)={C:|C|≥2k}. Indeed, any set of size at least 2k can be partitioned into two pieces each of size at least k. Thus

M_d≥max_k Σ_{j=k}^{min(2k−1,d)} binomial(d,j).

The primary source is Frankl–Kupavskii, *Partition-free families of sets*, arXiv:1706.00215v1, Theorems 1 and 2: https://arxiv.org/html/1706.00215v1 . The arXiv submission history lists only v1. An institutional PDF reproduces the same hypotheses: https://real.mtak.hu/90051/1/Partition-free_families_of_sets.pdf .

**Important restriction:** Theorem 1 (Kleitman) covers d=3m+1, m≥1. Theorem 2 covers d=3m or 3m+2 only when m≥6. The abstract omits that size restriction; do not infer the missing small cases from it. The retrieved full theorem, not the broad abstract, controls this application.

In those stated ranges, with m=floor(d/3),

p(d)=Σ_{j=m+1}^{2m+1} binomial(d,j).

Taking k=m+1 attains this value in the Boolean reduction, proving

f_d(3)=3^d−2^d+Σ_{j=floor(d/3)+1}^{2floor(d/3)+1} binomial(d,j)

for all d≡1 (mod 3), d≥4, and every d≥18. Dimensions 1,…,6 are additionally verified below. The remaining dimensions 8,9,11,12,14,15,17 are not settled by the source theorem and computations in this report. No claim of novelty for this derived corollary is made.

## 3. Upward compression gives an exact finite enumeration

For coordinate i, whenever A∈F has i∉A but A∪{i}∉F, replace A by A∪{i}, simultaneously over all such A. This preserves |F| and does not increase D(F); in fact D(new F)⊆D(old F).

Proof of the last assertion: consider a disjoint pair in new F. If both members were old, its union is already old. Otherwise its new member is A∪{i}, where A was old, and the other member B avoids i. Since B survived unshifted, B∪{i} was old. Then A and B∪{i} are an old disjoint pair with precisely the same union. Two new members both contain i and cannot be disjoint.

The compression preserves exclusion of ∅ and inclusion of [d]. Whenever it changes the family, the sum of all member cardinalities strictly increases. Repeating until no coordinate changes yields an upward-closed family without lowering the deficiency |F|−|D(F)|. Thus the maximum M_d can be obtained among Boolean upsets.

Every upset on d coordinates decomposes uniquely as F_0 on subsets avoiding the last coordinate and F_1 on subsets containing it, with both families upsets on d−1 coordinates and F_0⊆F_1. Conversely every such pair defines an upset. This gives an exhaustive recursion, not a heuristic generator.

For a pair F_0⊆F_1, the disjoint-union family has lower part D(F_0) and upper part

E(F_0,F_1)={A∪B:A∈F_0, B∈F_1, A∩B=∅}.

Therefore its deficiency can be computed exactly with bit operations. `enumerate_upsets.cpp` enumerates all upsets through d=6 using this recurrence and no floating-point arithmetic. Results:

| d | upsets enumerated | M_d | f_d(3) |
|---|---:|---:|---:|
| 1 | 3 | 1 | 2 |
| 2 | 6 | 2 | 7 |
| 3 | 20 | 4 | 23 |
| 4 | 168 | 10 | 75 |
| 5 | 7,581 | 20 | 231 |
| 6 | 7,828,354 | 41 | 706 |

The d=6 enumeration runs through all comparable pairs of 7,581 five-coordinate upsets. This proves the upper value 41 for the deficiency without relying on MILP termination. The explicit rank-threshold family |A|≥3 gives 41, hence f_6(3)=729−64+41=706.

A separate Python implementation, `verify_upset_bound.py`, checks the upper bound using only actual disjoint-union witnesses. It includes explicit fail-closed exception checks and is run with python -OO so assert elision cannot bypass its validation. It need not compute every D fully: once enough distinct forbidden unions have been exhibited to bound the deficiency, that pair is already certified. It still visits every comparable pair. The machine-readable result is `UPSET_INDEPENDENT_CHECK.json`; the C++ output is `UPSET_ENUMERATION_RESULTS.txt`.

## 4. Scope and next step

The exact 706 result repairs the finite slice conjecture rather than the asymptotic theorem. The entire N=3 problem is now reduced to a small-alphabet extremal-set problem, with exact formulas in the ranges above. The generic finite target with N≥4 remains unresolved. Attempt 3 should test whether isolated-vertex completion suffices for larger alphabets and seek a structural upper-bound reduction; mere agreement with a slice lower bound is not enough.
