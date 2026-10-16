# Full target as a corollary of the published BGT bad-sequence bound

This is a priority/model-mapping deduction from already published estimates, not an additional C1–C4 proof-search attempt. It corrects the initially incomplete priority assessment in BGT_MODEL_MAP.md. The direct identification with ordinary FPP remains false; the usable input is the larger combinatorial sum evaluated inside the published proof.

## 1. Published inputs and inspection scope

Let BGT denote Basdevant–Gouéré–Théret, *First-order behavior of the time constant in Bernoulli first-passage percolation*, arXiv:2106.12266 (2021), journal DOI 10.1214/22-AAP1795 (2022). The retained primary PDF has SHA256 9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba. Operative locations: the sequence extraction in §2.5; its geometric bound (19); bond Lemma 19 and (33) in §3.3; the evaluation of the nonnegative sum (33), PDF pp. 23–24. The other-coordinate term is the sum of the negative parts of the individual increments, not the negative part of their sum. These pages and the relevant site-counting proof have been read; this is not a certification of every proof in BGT.

The key input is stronger than the literal statement of their time-constant theorem: their evaluated union bound charges arbitrary distinct open-site sequences satisfying the displayed five deterministic conditions. In (33), put m=0. Its probability weight is then barε^p, where p is the number of distinct open sites; no doubly-open site is prescribed. The proof bounds this entire nonnegative sum, not merely the subset of sequences produced by ordinary FPP geodesics. It tends to zero as n→∞ for each sufficiently small fixed sparse-edge parameter and each fixed positive excess parameter. Their subsequent summation over m≥0 only enlarges the m=0 term.

For the sharp monotone shape, either BGT Lemmas 10 and 13 or the explicit strict Bernoulli-chain formula in Basdevant–Enriquez–Gerin–Gouéré, *Discrete Hammersley's lines with sources and sinks*, Theorem 1.1 (2016), suffices. The latter gives the exact formula used below.

## 2. Target and independent site grouping

Use the exact canonical dual square Q_N={0,…,N}². Independent forward-edge marks have probability q=1−p; a forward marked step earns one, an unmarked forward step zero, and every backward step costs one. Let D_N be the maximal reward. The supplied finite duality and fixed-q flow limit give

g(q)=1−v(1−q)=lim_N E D_N/(2N).

A maximum can be chosen simple: in every directed cycle the number of forward and backward steps agrees, so its reward is nonpositive. A monotone path has nonnegative reward.

Extend the edge-mark field independently outside Q_N. At vertex x let Y_x indicate that at least one of the two forward edges starting at x is marked. Different vertices use disjoint original edge variables. Thus the Y_x are iid Bernoulli with

r=1−(1−q)²=2q−q².

Let S_r(a,a) be the maximal length of a strict coordinatewise increasing chain of Y-open sites w with 0≤w_i<a, allowing an open origin. Its mean shape is

σ_r := lim_a E S_r(a,a)/a = 2 sqrt(r)/(1+sqrt(r)).

The endpoint convention has exactly the distribution of the strict-chain model on an a×a site square, by translation.

## 3. Lower comparison, exactly at finite volume

Every strict Y-chain counted by S_r(N,N) can be visited by a monotone target path. At each chain site choose one marked outgoing edge. Both outgoing edges remain inside Q_N because the site's coordinates are below N. The next chain site is at least one lattice unit larger in both coordinates, so the chosen edge can be traversed before padding monotonically to that next site. Pad finally to (N,N). Other forward rewards are nonnegative. Hence

D_N ≥ S_r(N,N), and therefore g(q) ≥ σ_r/2.

This also independently identifies the previously reported lower-bound formula sqrt(1−p²)/(1+sqrt(1−p²)).

## 4. The larger published event contains every target upper violation

Put n=N+1 and use BGT's direction z=(1,1). A target path to (N,N) is a BGT “nice” path to (nz)^−: all its vertices are strictly below (n,n) in each coordinate. Let P be a simple target maximizer, with B backward steps and K marked forward steps, so D_N=K−B.

List, in visit order, all Y-open sites of P except its terminal vertex; distinguish the origin separately. In BGT notation write b(0)=0, b(1),…,b(p), b(p+1)=(n,n), with I_0 indicating that the origin is Y-open. Each actual marked forward step starts at a distinct listed open site or the origin, so

K≤p+I_0.

Apply precisely BGT's extraction: i_0=0 and i_{k+1} is the first later index strictly larger in both coordinates; eventually i_Q=p+1. Set ℓ_k=i_{k+1}−i_k−1. Then p=Q−1+Σℓ_k. The extracted open sites form a legal strict Y-chain, including the origin if open, so

S_r(n,n) ≥ Q−1+I_0.

It follows without approximation that

D_N−S_r(n,n) ≤ Σℓ_k−B.                         (A)

For each block use BGT's h(k), g(k,i), and distinguished coordinate j_k. In dimension two write j'_k for the other coordinate, and set

C=Σ_k Σ_i |g(k,i)_{j_k}| + Σ_k Σ_i (g(k,i)_{j'_k})_−.

Here C is the quantity subtracted in BGT Lemma 19 item 5. The geometry in published (19) gives C≤2B. Directly: in the distinguished coordinate the last unextracted site is no larger than the block's first site, so the internal absolute variation is at most twice that coordinate's negative variation. The sum of the negative parts of the other coordinate's individual marked-site increments is at most its actual backward variation along the path. Summing over disjoint path blocks gives C≤2B. The virtual endpoint may be reached by two extra monotone steps, which add no negative variation.

Thus, on D_N>S_r(n,n)+η n sqrt(r), (A) implies

C < 2Σℓ_k−2η n sqrt(r).                       (B)

This is stronger than item 5 of *bond* Lemma 19 with m=0, including its harmless +1 and a fixed positive excess parameter. Since r≥q, it also implies that condition if the excess there is written using sqrt(q) instead of sqrt(r); any fixed-factor reparameterization of η is harmless.

The other four conditions hold as follows.

1. The positive h(k) telescope to (n,n), hence Σ||h(k)||_1=2n, exactly item 1.
2. There are no vertical coordinates in BGT's terminology: d_1=2, d_2=0. Item 2 is vacuous.
3. The chosen j_k satisfies Σ_i g(k,i)_{j_k}≤0 by the extraction rule, exactly item 3.
4. For a nonlast block, local optimality of P gives B_k≤K_k: replacing the segment between its two strictly ordered extracted endpoints by a monotone segment gives nonnegative reward. Such replacement may create a walk, but removing nonpositive cycles cannot reduce reward, so this comparison is valid for a simple global maximizer. Its marked forward steps start at the ℓ_k internal open sites or its first site, so K_k≤ℓ_k+1. The other-coordinate overshoot of the last internal site beyond the next extracted endpoint is at most B_k≤ℓ_k+1. Therefore the weaker bound 2(ℓ_k+1) in item 4 holds. For the last block it holds automatically because every listed site is strictly below (n,n).

The target path thus supplies distinct open sites satisfying the very same deterministic predicate already counted in (33), with m=0. Grouped site marks have exactly BGT's barε=r when its bond parameter ε=q. In the m=0 summand no double-open condition is required: the r^p weight only requests these distinct sites to be open, and places no restriction on other sites or on how many of the requested sites have two marked outgoing edges. One does not need to realize P as an ordinary-FPP geodesic.

Consequently the published evaluation of (33) yields, for every η>0 and all sufficiently small fixed q,

Pr{D_N>S_r(N+1,N+1)+η(N+1)sqrt(r)} → 0 as N→∞. (C)

This uses the already evaluated larger sum; no detour coefficient in their summation needs changing. An application of only their literal Theorem 1, Proposition 6, or Lemma 18 without this inclusion would remain incomplete.

## 5. Taking exactly the required limits

Since 0≤D_N≤2N and S_r≥0, (C) gives

E D_N ≤ E S_r(N+1,N+1) + η(N+1)sqrt(r) + 2N Pr{upper violation}.

First send N→∞ at fixed sufficiently small q. With the source-premised flow limit,

σ_r/2 ≤ g(q) ≤ σ_r/2 + (η/2)sqrt(r).

Now q→0, using σ_r/(2sqrt(r))→1 and r/(2q)→1; finally η→0. This proves the entire canonical statement

g(q) ~ sqrt(2q).

The published constant-shape and bad-sequence inputs predate the current C1/C4 argument. The statement that the exact Aldous conjecture follows after this explicit elementary model map is checkable. It is different from asserting that BGT explicitly announced a solution of Aldous's named problem, or from establishing who first noticed this corollary. No claim about that historical first notice is made.

## Source-precision correction

The first draft incorrectly wrote the negative part of the other-coordinate net sum. The parent identified the error, and a higher-resolution reinspection of actual PDF p.16 confirmed that the printed term is Σ_i (g(k,i)_j)_−. The definition and explanation above have been corrected. The needed bound is unchanged: the sum of individual negative marked-site increments is bounded by actual backward variation. All conclusions here use the corrected, stronger printed predicate.
