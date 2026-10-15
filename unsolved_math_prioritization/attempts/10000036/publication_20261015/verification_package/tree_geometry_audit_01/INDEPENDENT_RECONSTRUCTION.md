# Independent reconstruction before prior verdict access

Frozen head: `ed2de7249953ba0c1afad253adca9b820d7297c5`.
Author proof SHA-256: `c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d`.
Created before reading either historical independent review. No other fresh-family conclusions used.

## Exact conditional theorem

Assume G=(V,E) is countably infinite, connected, simple, maximum degree Δ<∞, and T is a one-ended spanning tree. For independent U_e uniform on [0,1], retain t in T with probability 1−2^{−s(t)} and add e outside T with probability 2^{−M(e)}, where s(t) is the size of the finite component of T−t and M(e)=max_{t in P_T(e)}s(t). Then for every fixed T, with U-probability one, X has a unique infinite component C and its quenched internal bond and site critical probabilities are one. This audit treats availability of an invariant factor-of-iid T and the finite-energy convention as separate-family assumptions.

## Deduction

1. Each T−t has precisely one finite component: two infinite components yield distinct ends by local finiteness, and both finite is impossible. For v's unique ray v=v_0,v_1,..., set t_n=v_nv_{n+1} and S_n=finite side of T−t_n. These finite sets contain v, are nested strictly, and s_n=|S_n|≥n+1. Hence ∑_n f(s_n)≤∑_{m≥1}f(m) for f≥0.
2. An ambient edge e outside T crossing S_n has a tree path containing t_n, because the unique tree boundary of S_n is {t_n}. Therefore M(e)≥s_n. There are at most Δs_n crossing ambient edges, so the probability of any inserted bypass is at most Δs_n2^{−s_n}.
3. Let B_n mean that t_n is deleted or some non-tree edge crossing S_n is inserted. The conditional sum is at most ∑_{m≥1}(1+Δm)2^{−m}=1+2Δ. The first Borel–Cantelli lemma gives an N_v such that for every n≥N_v, t_n is retained and ∂_X S_n={t_n}. No independence among B_n is used. Countably many vertices yield one event on which this conclusion holds for all v.
4. For every v, the tail v_{N_v},v_{N_v+1},... is an infinite retained-tree ray. Rays in a one-ended tree coalesce, so all these retained tails meet and belong to one infinite component C_R of the retained-tree graph. Conversely, any infinite retained-tree component has a ray by local finiteness; that ray is the unique T-ray from its initial vertex, so its tail meets C_R. Thus C_R is the only infinite retained-tree component.
5. If v is in any infinite X-component, for n≥N_v some X-path from v must exit finite S_n. Its only exit is t_n. Both endpoints of t_n lie on the retained infinite ray tail and belong to C_R. Hence v is X-connected to C_R. All infinite X-components coincide, and at least one exists.
6. Fix a good pair (T,X) and any p∈[0,1). If an independent Bernoulli-p bond thinning has v in an infinite component, then it retained each of the distinct cut edges t_n for n≥N_v. For each k its probability is ≤p^k; hence zero. Countably many v imply no infinite thinned component. This argument is deterministic after fixing the pair and works for every p<1, with no interchange of an uncountable family of null sets. At p=1, X percolates. Restricting the cuts to C works because t_n belongs to C and ∂_C(S_n∩C)={t_n} for v∈C.
7. Site thinning requires infinitely many distinct ray vertices retained, giving the same p^k bound. For p=0 choose k≥1; p=1 is outside the destruction claim and gives the original infinite component.

## Initial verdict and open detail

No contradiction is apparent in Sections 2–6. The primary point requiring a fully explicit writeup is passage from the full joint witness event to an almost-sure measurable property of X. It can be formalized by rational-p percolation probabilities or a Borel graph property built from countably many finite singleton cuts. The argument does not require a measurable choice of witness tree from X. This is a verification/detail issue to settle, not an invitation to search for a new central proof.
