# A Karp reduction from nonhalting to chip-firing reachability

Status: complete proof accepted by the accompanying independent mathematical audit, 10 October 2026. Target: AMR-029-0016 / problem 3000016. This AI-assisted manuscript is unrefereed; acceptance denotes the accompanying audit, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty or first-in-literature claim is made. The explicit many-one reduction is distinct from Tóthmérész's 2022 polynomial-hierarchy barrier.

## Statement

Legal chip-firing reachability for finite loopless directed multigraphs with binary-encoded multiplicities is coNP-hard under polynomial-time many-one reductions, even for strongly connected graphs and nonnegative initial/target configurations. Together with Hujter–Kiss–Tóthmérész, Theorem 12, this establishes coNP-completeness of that nonnegative restricted language. The broader Egres language permits signed configurations; the hardness subclass suffices for its question.

## Source problem and conventions

Use the complement of the NP-complete halting problem of Farrell and Levine, *CoEulerian graphs*, Proc. Amer. Math. Soc. 144 (2016), 2847–2860, Corollary 3.2; https://arxiv.org/abs/1502.04690 . The problem definition on PDF p.2 requires a finite strongly connected multigraph, given by its adjacency matrix, and a nonnegative configuration. The paper allows loops. Remove loops by the relay construction below. We use source graphs on at least two vertices, so all outdegrees are positive. This is a valid hard restriction: a one-vertex instance with ell loops is nonhalting exactly when its chip count is at least ell, and can be replaced by the directed two-cycle with configuration (1,0) in the nonhalting case or (0,0) in the halting case. The latter are fixed nonhalting and halting instances, respectively.

Let G have n vertices, no loops, a_{uv} parallel arcs from u to v, d_v=sum_w a_{vw}, D=max_v d_v, and a nonnegative integer initial configuration x. Let C=sum_v x_v and

N=(C+1)^n, M=N+1, B=N(MD+1).

All three integers have polynomial bit length in the binary input size.

## Construction

Add two new vertices g (gate) and m (marker). Form H as follows:

1. Replace every old arc multiplicity a_{uv} by M a_{uv}.
2. Add one arc v->g for every old vertex v.
3. Add B parallel arcs g->v for every old vertex v.
4. Add one arc g->m and one arc m->g.

The graph H is loopless and strongly connected. Old vertices have outdegree M d_v+1; g has outdegree nB+1; m has outdegree 1.

The initial configuration X is

X_v=M x_v+N for old v;
X_g=nB+1-N;
X_m=0.

Prescribe the firing-count vector f_v=N for old v, f_g=1, f_m=0, and define the target Y=X+L_H f, using the negative-diagonal, incoming-off-diagonal Laplacian convention. Explicitly, with i_v=sum_u a_{uv},

Y_v=M x_v+MN(i_v-d_v)+B;
Y_g=(n-1)N;
Y_m=1.

Both configurations are nonnegative: X_g>=1, and Y_v>=B-MND=N. Other coordinates are manifestly nonnegative. In particular X != Y.

## Lemma 1: a finite cutoff characterizes nonhalting

The source configuration x is nonhalting if and only if some legal sequence on G has N firings.

Proof. There are at most (C+1)^n=N nonnegative configurations with total chip count C. A legal sequence of N firings visits N+1 configurations, so it repeats a configuration, giving a nonempty legal cycle. Repeating this cycle gives an infinite legal game. By the standard abelian halting dichotomy, this excludes termination. Conversely a nonhalting game can always be continued and therefore has a prefix of N firings. This argument needs no bound on a period vector.

## Lemma 2: exact simulation before the gate

Before the first gate firing, the marker has no chips and cannot fire. If t_v is the number of old-vertex firings so far, and z is the source configuration after the same projected sequence, then

H_v=M z_v+N-t_v.

This follows by comparing chip changes: all old-to-old transfers are multiplied by M, and each old firing additionally sends one chip to g. For a prefix with fewer than N total firings, 0<=t_v<=N-1. Consequently an old vertex v is legal in H exactly when it is legal in G:

- If z_v>=d_v, then H_v>=M d_v+N-t_v>=M d_v+1.
- If z_v<=d_v-1, then H_v<=M(d_v-1)+N=M d_v-1<M d_v+1.

Meanwhile the gate has nB+1-N+t chips after t old-vertex firings, hence cannot fire for t<N and can fire at t=N. Thus the first N old firings, if they exist, simulate the original game exactly, regardless of the chosen order.

## Lemma 3: nonhalting implies target reachability

If x is nonhalting, take a legal sequence of exactly N old firings and perform it in H using Lemma 2. Fire g once, which is now legal. Each old vertex receives B chips. Let t_v be its previous number of firings, so 0<=t_v<=N. Complete each old vertex's count to N, in any order, firing neither g nor m again. These moves are legal: immediately after the gate firing every old vertex has at least B chips, all incoming transfers are nonnegative, and

B=N(MD+1)>=N(Md_v+1)

is enough to pay for all its at most N remaining firings even without any further receipts. The final firing-count vector is exactly f, so the resulting configuration is Y.

## Lemma 4: target reachability implies nonhalting

Suppose a legal sequence from X reaches Y. Since the marker starts with zero and ends with one chip, and receives chips only from the gate, the gate must have fired. More explicitly, the marker balance is k_g-k_m=1, implying k_g>=1.

Before the first gate firing the marker cannot fire, and the gate must receive at least N chips from old vertices to become legal. Hence at least N old firings occur before that gate firing. By Lemma 2, their first N projected firings form a legal source sequence. Lemma 1 now implies that x is nonhalting.

## Complexity

The construction has n+2 vertices. Writing s for the source input length, n<=s, log(C+1)=O(s+log n), log D=O(s+log n). Thus log N=O(n log(C+1)), log M=O(log N), and log B=O(log N+log M+log D), all polynomial in s. Every adjacency entry and every coordinate of X,Y is formed by polynomially many exact integer arithmetic operations on polynomial-bit integers. The map is a polynomial-time Karp reduction, with the YES equivalence

(G,x) is NONHALTING  iff  (H,X,Y) is REACHABLE.

No oracle calls, output simulation, unary expansion, sink dissipation, or rotor states are used.

## Loop-removal lemma for the source problem

For each source vertex v with ell_v>0 self-loops, replace its ell_v loops by ell_v arcs v->r_v and ell_v arcs r_v->v, where r_v is a fresh relay initially holding zero chips. Keep every other arc and every old initial chip count unchanged. The original vertex's outdegree is unchanged. The relay has outdegree ell_v, and its chip count is always ell_v times the number of still-unreturned packets. Original legal sequences lift by firing r_v immediately after each firing of v. Conversely, project any legal sequence to original vertices, reinserting each omitted relay return immediately after its source firing: compared with the expanded execution, the projected original configuration has only more chips at each vertex, namely the still-pending loop returns. Every projected original firing is legal. An infinite execution of the expanded graph has infinitely many original firings, since relay firing counts are at most their corresponding original firing counts. Thus nonhalting is preserved in both directions, and hence so is halting by the abelian dichotomy. The expansion remains strongly connected and binary encoded, with at most twice as many vertices, and is loopless. (The zero-loop one-vertex source case is elementary.)

## Signed-input normalization (optional robustness check)

The cited source decision problem is stated for nonnegative configurations. If instead starting from a signed intermediate configuration, its signs can be removed without changing legal sequences: for every vertex v add k_v=max(0,-x_v) self-loops and k_v initial chips. A self-loop changes the firing threshold but cancels out of the net chip change. Thus the new chip count is always the old chip count plus k_v, and the new threshold is the old threshold plus k_v. The legal moves coincide exactly. The initial configuration is nonnegative. Applying the preceding relay construction then removes these loops in polynomial time. This observation also makes explicit how to normalize any signed intermediate representative used in a lattice-based proof of source hardness.

## Prior-results boundary

- Hujter, Kiss, and Tóthmérész, *On the complexity of the chip-firing reachability problem*, Proc. Amer. Math. Soc. 145 (2017), 3343–3356, https://arxiv.org/abs/1507.03209 : nonnegative configurations, binary adjacency, loopless graphs; Theorem 12 gives coNP membership. Their Eulerian and recurrent-target algorithms are prior results.
- Tóthmérész, *Rotor-routing reachability is easy, chip-firing reachability is hard*, European J. Combin. 101 (2022), 103466, https://arxiv.org/abs/2102.11970 , Theorem 2.3: a polynomial reachability algorithm would collapse PH to NP. That proof uses recurrence and certificates for nonhalting and does not establish the many-one reduction above.
- The current argument relies on the published NP-completeness of halting and supplies an explicit many-one reduction from its complement. It does not assert a novel proof of the source theorem or a first-in-literature status.
