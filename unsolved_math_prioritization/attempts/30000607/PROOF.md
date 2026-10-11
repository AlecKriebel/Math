# Repaired extremal proof and bounded finite-n coverage

Problem 30000607 / OWR-1386-014. Authored edition, 11 October 2026 UTC.

AI-assisted, unrefereed authored reconstruction and editorial acceptance. This edition is based on one source/proof reconstruction plus an internal AI review of its three reports; it does not claim a second independent mathematical audit, external human peer review, or formal proof-assistant certification. It is not a computational reproduction package.

The original all-n target remains unresolved by this work. The two full reports below retain the repaired existing asymptotic theorem and the separate incomplete finite-n approach.

## Detailed replacement for Han's extremal bookkeeping

This is an authored proof reconstruction of an existing sufficiently-large-n theorem. It does not claim novelty or all-n coverage. It uses the notation and construction of Han v3, Theorem 1.5, PDF pages 5–7, and records corrections rather than silently altering the source.

Fix k≥3. Put c_k=(2k)^{k−1}/(k−1)! and choose
 0<α≤min{1/(100k²),1/(100k c_k)}, ε=α².
Take n sufficiently large in terms of k,α; in particular n≥k/ε and large enough for every reserve count below. Write n=kq+r with 1≤r≤k−1. Suppose δ_{k−1}(H)≥q and H has an independent set of size at least (1−ε)(k−1)n/k.

## Partition and small matchings

Let C be a maximum independent set. Let A contain those vertices x outside C whose link contains at least (1−α)binom(|C|,k−1) of the (k−1)-sets in C, and put B=V\(A∪C).

Every (k−1)-set S in C has its ≥q neighbors outside C. Thus |C|≤n−q, and
 h:=n−|C|−q ≤ ε(k−1)n/k+r/k ≤ εn,
where the last inequality follows from εn≥r. Counting pairs (S,x) with S⊆C, |S|=k−1 and S∪{x} an edge gives
 q≤|A|+(1−α)|B|,
so α|B|≤h≤εn and |B|≤αn; also |A|≥q−αn. This keeps all rounding terms visible.

If t=q−|A|>0, select t disjoint (k−1)-sets in C. There are enough because t≤αn and C is linear in n. Each such set has at least t neighbors in B, so sequentially choose distinct neighbors and form a matching M_1 of size t, with one B vertex in each edge. If t≤0 set M_1 empty.

While a B vertex remains uncovered, take it together with k−2 unused C vertices and extend to an edge using an uncovered neighbor. The total number of already covered vertices stays below k|B|≤kαn<q, so a neighbor exists. This forms M_2 and covers all B. Each M_2 edge uses at most one A vertex. Because every edge of M_1∪M_2 covers a new B vertex, let a=|M_1∪M_2|≤|B|≤αn. At this point, with n_2=n−ka,
 |A_2|≥(n_2−r)/k=q−a,
 s:=|A_2|−(n_2−r)/k≤h+a≤2αn.

Now form M_3 while the current surplus c=|A'|−(n'−r)/k exceeds 1. If c≥k−1, select k−1 unused A vertices and extend. The edge uses k−1 or k A vertices and lowers the surplus by k−2 or k−1. If 2≤c<k−1, select c A vertices and k−c−1 C vertices, then extend. The surplus becomes 1 or 0. In every step the total number of covered vertices is at most 3kαn<q, so an uncovered extension exists; linear reserves of A and C ensure the prescribed partial set can be chosen. More explicitly, A'≥(n'−r)/k and n'≥n−3kαn, while C'≥[(1−ε)(k−1)/k−3kα]n, both linear and positive. Each step reduces the surplus by at least 1, so b:=|M_3|≤s≤2αn.

Let c_3 be the final surplus, either 0 or 1. If c_3=0, delete r unused C vertices; if c_3=1, delete one unused A vertex and r−1 unused C vertices. Nondivisibility ensures r−1≥0. Denote the remaining sets by A_* and C_*.

## Correct size identity

Exactly r vertices have now been set aside and all B vertices are already covered. Both cases give
 |C_*|=(k−1)|A_*|,
 m:=|A_*|=(n−k(a+b)−r)/k=q−a−b≥q−3αn≥n/(2k).
This identity replaces the unsupported source display that subtracts only one A vertex per M_3 edge. It also ensures m is sufficiently large for any fixed-k auxiliary lemma when n is large.

Partition C_* arbitrarily into k−1 equal parts of size m. Let J be the crossing k-partite subhypergraph with A_* as its first part. A crossing tuple from the C parts has at most h≤εn≤2kεm non-neighbors in A_*: all its neighbors in H lie outside the independent set C and it has at least q of them. Thus its degree into A_* is at least (1−η)m, η=2kε.

For any x∈A_*, the number of absent crossing C tuples is at most the total number of absent (k−1)-sets in C, bounded by
 α binom(|C|,k−1)≤α n^{k−1}/(k−1)!≤θm^{k−1}, θ=α c_k≤1/(100k).
This avoids the false unrounded upper bound |C|≤(k−1)n/k in the source. Consequently x has at least (1−θ)m^{k−1} crossing neighbors.

These two degree bounds already suffice for Han's Pikhurko application, since θ+η<1/2. The following self-contained special lemma also supplies the final matching without that deeper dependency.

## Elementary dense partite lemma

Let k≥3 and m≥max{2,k−1}. Consider a balanced k-partite k-graph with a distinguished part A and k−1 other parts. Suppose every crossing tuple of the other parts has at least (1−η)m neighbors in A, with η≤1/2, and every a∈A misses at most θm^{k−1} crossing tuples, with 0≤θ≤1/(100k). Then there is a perfect matching.

Proof. Independently permute each of the k−1 other parts, and group vertices in the same slot into m disjoint tuples. These tuples partition those parts. For fixed a, let F_a be its missing tuple family and let Y_a count selected tuples in F_a. Put d=k−1 and p_a=|F_a|/m^d≤θ. Each slot is uniformly distributed over the product, so μ_a=E Y_a=mp_a. Two distinct slots form a uniformly random ordered pair of tuples differing in every coordinate. There are [m(m−1)]^d such pairs. At most |F_a|² of them are both missing. Therefore
 E[Y_a(Y_a−1)]≤μ_a² (m/(m−1))^{d−1}.
Using (1+1/(m−1))^{k−2}≤exp((k−2)/(m−1))≤1+2(k−2)/(m−1), valid since m≥k−1, gives
 Var(Y_a)≤μ_a+2(k−2)μ_a²/(m−1)
             ≤[θ+4(k−2)θ²]m.
Since μ_a≤m/4, Chebyshev's inequality implies
 P(Y_a≥m/2)≤16[θ+4(k−2)θ²]/m.
A union bound over the m choices of a makes the probability of any failure at most
 16θ+64(k−2)θ²<1.
Hence there is a tuple partition with Y_a<m/2 for every a.

Construct a bipartite graph between A and these m tuples, joining a to a tuple when they form a hyperedge. Every A vertex has degree >m/2, and every tuple has degree ≥m/2. Their minimum degree sum exceeds m. Hall's condition follows directly: for nonempty X⊆A, if |X|≤δ_A then |N(X)|≥δ_A≥|X|; otherwise every tuple meets X, because |A\X|<m−δ_A≤δ_tuple. Thus |N(X)|=m≥|X|. Hall's theorem gives a perfect matching, proving the lemma.

Applying it to J gives m disjoint edges covering A_*∪C_*. Together with M_1,M_2,M_3 these form q edges in H and leave precisely r vertices uncovered. This completes the repaired extremal branch.

## Scope and foundations

The combinatorial constructions and second-moment calculations above are fully supplied. Standard finite probability identities, Chebyshev's inequality and Hall's theorem are used. The nonextremal branch elsewhere uses the standard binomial Chernoff bound. This is not a formal machine-checked proof, and no priority claim is made. Smallness of α and largeness of n remain indispensable; this proof does not close the literal finite-n remainder.

## Separate finite-n partial coverage

Date: 11 October 2026 UTC. Target: the literal all-n remainder of problem 30000607. Outcome: partial elementary coverage, no counterexample, full target incomplete.

## Proven finite families

If k<n<2k, q=1. Codegree at least 1 guarantees an edge, and the empty hypergraph proves the lower bound. Thus t_k(n)=1.

More generally, if n≥3k−2 and δ_{k−1}(H)≥2, H contains two disjoint edges. Suppose not. There is an edge E, and every edge meets E. Its complement has at least 2(k−1) vertices, so choose disjoint (k−1)-sets S,T outside E. Their neighbor sets lie inside E and each has size at least 2. Choose distinct x∈N(S), y∈N(T). Then S∪{x} and T∪{y} are disjoint edges, contradiction.

In particular, for n=3k−2 and n=3k−1 with k≥3, q=2 and k does not divide n. Together with the space barrier this proves t_k(n)=2. This covers n=7,8 when k=3. It does not prove the two-edge cases n=2k+r for 1≤r≤k−3, or the general q≥3 cases. No novelty claim is made for these elementary observations.

## Bounded diagnostic search

The underlying authored diagnostic search builds one binary variable for each k-subset. It imposes minimum codegree at least 2 for every (k−1)-subset, forbids every pair of disjoint selected edges, and fixes the first k-subset to be an edge (valid by relabeling when codegree is positive). Thus any integral feasible witness on 2k<n<3k would be a counterexample; the script separately checks the raw edge list, minimum codegree and pairwise intersection before calling a witness verified.

SciPy/HiGHS reported infeasibility for (k,n)=(3,7),(3,8),(4,9),(4,10),(4,11),(5,11),(5,12),(5,13). The (6,13) run stopped at its 20-second diagnostic time limit without a witness. Each receipt records dimensions, timing, status and the absence of a proof certificate. These are floating-point MILP outcomes, not independently checkable exact UNSAT certificates. Therefore none is used to certify a new finite instance, let alone a universal statement. The time limit bounds this diagnostic experiment; it is not a claim that the mathematical question is exhausted.

The search was only for matching size two, not for all candidate (n,k). It ran newly authored code, not source-author mathematical code. Only this bounded historical summary is distributed here; neither code nor raw outputs are included.

## Obstruction to a naive completion

The large-n proof reserves C log n absorbers and uses inequalities comparing this deletion to γn. Applying it at arbitrary n removes the quantitative hypothesis that makes the remainder work. Adding universal vertices also does not fix this: the corollary's construction adds only O(k) vertices and loses up to one matching edge per added vertex. It does not lift a small instance to arbitrary size while preserving the claimed matching deficiency. A blow-up would likewise require a separate integral-matching transfer theorem; no such transfer was established.

The bounded finite-n exploration gives no universal proof or exact counterexample. The unresolved family is stated explicitly in AUDIT.md. It must not be labeled solved or silently absorbed into Han's asymptotic theorem.
