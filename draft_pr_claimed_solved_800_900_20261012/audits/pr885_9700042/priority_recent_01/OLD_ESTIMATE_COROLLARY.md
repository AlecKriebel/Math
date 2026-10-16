# Exact flow asymptotic from a 2021 weighted-list estimate

Date: 2026-10-15. Scope: PR885 / PID9700042 only.

This is an independently constructed deduction from the intermediate estimates in Anne-Laure Basdevant, Jean-Baptiste Gouéré and Marie Théret (BGT), *First-order behavior of the time constant in Bernoulli first-passage percolation*, arXiv:2106.12266v1 (23 June 2021). It is **not** a claim that those authors explicitly stated the Aldous–Lenderman flow conjecture. The ordinary FPP theorem cannot simply be substituted for the directed-cut model. The deduction below identifies precisely which stronger intermediate estimate is sufficient.

Primary body: [arXiv PDF](https://arxiv.org/pdf/2106.12266v1), especially Section 2.2 (strict site score and mean limit), Lemma 10 (site score scaling), Section 2.5 (sequence notation), and Section 3.3, PDF pp. 23–24, Lemma 19 and the weighted-list sum (33) with its displayed bound W. The PDF was retrieved and the crucial pages visually inspected. Journal bibliographic identity: [DOI](https://doi.org/10.1214/22-AAP1795), AAP 32(6) (2022), 4535–4567; the publisher body was not successfully retrieved in this audit.

## 1. Directed-cut model and independent site field

Use the finite directed dual already supplied by the exact flow model: on Q_N={0,...,N}², forward E/N edges have costs 1−ω_e with iid ω_e~Bernoulli(q), and reverse W/S traversals cost zero. Let T_N be the corner-to-corner minimum cost and D_N=2N−T_N. For a simple minimizing path P, let k be its number of marked forward edges and b its number of backward steps. Then

    D_N = k−b,       0 ≤ D_N ≤ 2N.

The original source's fixed-q L1 limit, together with the finite boundary identity, gives

    lim_N E[D_N]/N = 2g(q),      g(q)=1−v(1−q).

This audit treats that finite dual identity and the source-premised limit as the fixed target contract, not as a new prior-work result.

Extend ω independently to all outgoing E/N edges at all vertices needed below, including boundary vertices. Declare vertex x open when at least one of its two outgoing edges is marked. These vertex events use disjoint pairs of edge variables, so they are iid Bernoulli with parameter

    r = 1−(1−q)² = 2q−q².

Write S_r(M) for BGT's strict increasing open-site score S_r^D((M,M)) with d1=2 and d2=0. A chain can include 0 if it is open; it must stay strictly below its terminal point in both coordinates. BGT's mean limit and site-score scaling imply

    σ_r = lim_M E[S_r(M)]/M,       σ_r / √r → 2  as r↓0.       (A)

Only an expectation limit is required here. BGT's Lemma 5 and Lemma 10, together with the Poisson-chain constant identified in Proposition 3 / Section 3.4, supply (A).

## 2. The lower comparison is pathwise

Every strict open-site chain in [0,N)² can be visited by a monotone path in Q_N that takes one marked outgoing edge at each chain vertex. Both coordinates between successive chain vertices increase by at least one, so either choice of marked outgoing edge fits before the next vertex; the same applies before the endpoint (N,N). Chosen edges are distinct. Hence

    D_N ≥ S_r(N),       and therefore       2g(q) ≥ σ_r.       (B)

No interchange of limits is used in (B).

## 3. Exact deterministic implication for the upper comparison

Set M=N+1, N≥1. Choose a simple minimizing dual path P in Q_N; nonnegative costs permit cycle removal. Its vertices are strictly below (M,M) coordinatewise. List its open visited vertices excluding its final vertex (N,N). Use BGT's convention b(0)=0, b(1),...,b(p) for the open vertices other than 0, and the auxiliary terminal b(p+1)=(M,M). Thus k≤p+I_0, where I_0 indicates that 0 is open.

Apply exactly the greedy strict monotone subsequence construction in BGT Section 2.5. Let a≥1 be its number of gaps (BGT calls this integer q; it is renamed here to avoid conflict with the edge-mark probability). Let ℓ_j be the number of intervening open sites in gap j, so

    p = a−1 + L,       L=Σ_j ℓ_j.

Use BGT's h(j), g(j,i) and direction j_j for each gap. Put

    G = Σ_j Σ_i |g(j,i)_{j_j}|,
    H = Σ_j Σ_i (g(j,i)_{other coordinate})_−.

The selected subsequence gives a strict open-site chain, so

    S_r(M) ≥ a−1+I_0,       k−S_r(M) ≤ L.                     (C)

### Local optimality and BGT Item 4

For a nonlast gap, its selected endpoints u≺w both lie in Q_N. If u is open, a monotone path from u to w can first take a marked outgoing edge, because each coordinate displacement is at least one. Thus its cost is at most |w−u|_1−I_u. Every marked forward edge on the actual gap starts at one of its ℓ_j intervening open sites or at u, so k_j≤ℓ_j+I_u. The actual gap cost is |w−u|_1+b_j−k_j. Global minimality implies

    |w−u|_1+b_j−k_j ≤ |w−u|_1−I_u,
    b_j ≤ ℓ_j.

This comparison remains valid if replacing the gap creates intersections with the rest of the path: it gives a walk with no greater cost, and nonnegative costs permit removal of every cycle. A coordinate overshoot of the last intervening site beyond w costs at least that many backward steps. Therefore BGT's Item 4 holds, even with ℓ_j in place of its weaker 2(ℓ_j+1). For the last gap, all actual vertices are below the auxiliary terminal (M,M); Item 4 follows geometrically. No local replacement outside Q_N is needed.

### The half-penalty issue and BGT Item 5

For a gap's distinguished coordinate, its intervening increments have nonpositive total by construction. Their total negative variation is therefore at least half their absolute variation. In the other coordinate, each increment between consecutive listed sites is realized by a disjoint subpath; its negative part is bounded by that subpath's actual backward variation. Summing the individual negative parts gives H as defined above. These are disjoint portions of P's coordinate variation, giving

    b ≥ G/2 + H.                                                (D)

For any η>0, if D_N>S_r(M)+ηN√q, (C) implies L−b>ηN√q. Combining with (D) and discarding one nonnegative copy of H gives

    0 ≤ −G−H+2L−2ηN√q.

In particular, because r≤2q and N/(N+1)≥1/2,

    0 ≤ −G−H+1+2L−τM√r,       τ=η/√2.                         (E)

BGT Items 1 and 3 are the same geometric identities as before; Item 2 is vacuous when d2=0. Item 4 was checked above. Equation (E) is precisely the m=0 weighted-list constraint in BGT's Lemma 19 / (33), with the gap parameter expressed in units √r.

Crucial distinction: **m=0 is a specialization of the positive combinatorial list sum, not an assertion that P visits no doubly-open sites.** Every fixed list of p distinct sites is open with probability r^p, regardless of how many of those sites have two marked outgoing edges. This is exactly the m=0 weight in (33). Distinctness holds because P is simple. The state of 0 can be ignored when bounding that probability.

## 4. The old list estimate is sufficient as printed

For clarity, here is its direct d1=2, d2=0, m=0 specialization, rather than an appeal to an unsupported generalization of the ordinary FPP theorem. Define

    K(t)=(1+e^(−t))/(1−e^(−t)),
    A_r = r e² exp(2γ√r) K(β√r) K(γ√r),
    B_r = r exp(2γ√r+2α) e² K(α)
          ·[K(γ√r)+K(α−γ√r)].

BGT's displayed W bound on PDF p.24 bounds the weighted sum for fixed a, ℓ-vector and distinguished-coordinate vector by

    r^(−1) exp(2+α+(2β−ατ)M√r) · A_r^a · B_r^L.              (F)

Expressing the gap as τM√r avoids a harmless ε-versus-bar-ε change of scale in the presentation. Formula (F) is the printed estimate with that positive gap coefficient; it does not change the counting mechanism.

Choose β=2γ and then γ large. Since K(t)~2/t as t↓0,

    A_r → 4e²/(βγ),       B_r → 0.

Choose α with ατ>2β+1. For small enough r, α−γ√r>0 and 2A_r/(1−B_r)≤1/2. There are at most 2^a distinguished-coordinate choices, while summing over ℓ_0,...,ℓ_(a−1)≥0 contributes (1−B_r)^(−a). Sum over a≥1 to get a convergent geometric series at most one. Thus the complete list sum is bounded by

    r^(−1) exp(2+α) exp(−M√r).

Consequently, for each η>0 and all sufficiently small fixed q>0,

    P[D_N>S_r(N+1)+ηN√q] → 0   as N→∞.                       (G)

The order is fixed η, then sufficiently small q, then N→∞. Only the fixed-q large-volume limit is used in (G).

## 5. Expectations and final ordered limits

Using D_N≤2N and S_r≥0, (G) gives

    E[D_N] ≤ E[S_r(N+1)] + ηN√q + 2N·P[the event in (G)].

Let N→∞ at fixed q, using the source's flow-density limit and (A), then combine with (B):

    σ_r ≤ 2g(q) ≤ σ_r+η√q

for all sufficiently small q, with threshold depending on η. Finally r/(2q)→1 and (A) imply

    lim_(q↓0) g(q)/√(2q) = 1.

This establishes the exact source asymptotic from BGT's 2021 strict-site score scaling and its explicitly displayed weighted-list estimate, together with the finite directed-cut identity. The inference above is authored in this audit; an explicit earlier statement of the flow corollary was not located. It is stronger priority evidence than the superficial equality of the ordinary FPP coefficient, and it must be independently checked before the parent promotes the priority verdict.

## Check boundaries

The proof requires q sufficiently small, not every q. It uses edge capacities, not vertex-disjoint flow, and keeps the two outgoing edge types through r=2q−q². The auxiliary terminal M=N+1 handles the square's top/right boundary without changing the n→∞ normalization. No current-openness conclusion follows from Aldous's maintained problem page. No claim about all other possible contributions, first public recognition of this corollary, or the full novelty of C4 is made here.

Source-precision correction: the first draft of this audit misread BGT's other-coordinate penalty as the negative part of a summed increment. The parent independently inspected the original pages and corrected it to the sum of the individual negative parts. The definition and its deterministic variation argument above use the correct, stronger quantity. The event inclusion and geometric-series deduction survive this correction; finite geometry checks were rerun with the stronger H.
