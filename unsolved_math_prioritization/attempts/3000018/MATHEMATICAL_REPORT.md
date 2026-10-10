# Simple directed chip-firing halting is NP-complete

**Status:** complete proof accepted by the accompanying independent mathematical audit, 10 October 2026. Target: problem 3000018 / AMR-029-0018. The separately accepted [oriented-graph appendix](ORIENTED_APPENDIX.md) strengthens the graph restriction. This AI-assisted manuscript is unrefereed; acceptance denotes the accompanying audit, not external human peer review, journal acceptance, or formal proof-assistant certification. No first-in-literature priority claim is made.

## 1. Exact language and theorem

An instance consists of a finite loopless simple strongly connected directed graph with at least two vertices and a nonnegative integer configuration, written in binary. Antiparallel arcs are allowed. Firing a vertex with at least its outdegree chips sends one chip along each outgoing arc. No vertex is a dissipative sink.

**Theorem.** Deciding whether such a configuration halts is NP-complete under polynomial-time many-one reductions. Hardness already holds for graphs with a distinguished vertex r such that deleting r leaves an acyclic graph of depth at most one (counter-to-relay arcs). All constructed chip counts, as well as their total, are polynomially bounded in the 3-SAT instance size.

NP membership is prior work of Farrell and Levine, *CoEulerian graphs*, Section 3, https://arxiv.org/abs/1502.04690v3 . Their Section 3.1 explicitly leaves the simple case as a question. The construction below supplies a direct reduction from 3-SAT, not an expansion of their large binary multiplicities. A self-contained specialization of their certificate bound is given in Section 7.

## 2. A bank realizing an arbitrary modular predicate

Let p>=2 be an integer and let A be a nonempty subset of Z/pZ. Write h(k)=1 if k mod p lies in A, and h(k)=0 otherwise. For each a in {0,...,p-1}, put

    c_a = 1 + h(-a-1) - h(-a).

All arguments of h are read modulo p. Each c_a belongs to {0,1,2}, and telescoping gives sum_a c_a=p. Make c_a distinct counters with initial count a; thus the bank has exactly p counters. Each counter will receive one chip whenever r fires, and will have outdegree p, with all of its outgoing chips eventually returned to r. At a checkpoint at which r has fired k times and all other vertices have been stabilized, its count is (a+k) mod p.

Define the bank storage

    S_A(k) = sum_a c_a ((a+k) mod p).

**Bank identity.** For every integer k,

    S_A(k) = K_A + p h(k),
    K_A = p(p-1)/2 - |A|.

Proof. On incrementing k, each of the p counters gains one, except that each counter whose residue was p-1 loses p. Those are exactly the counters with a=-k-1 mod p. Therefore

    S_A(k+1)-S_A(k)
      = p - p c_{-k-1}
      = p (h(k+1)-h(k)).

So S_A(k)-p h(k) is constant. Averaging over a complete period, each counter has average (p-1)/2 chips, while p h(k) has average |A|. This gives K_A. In particular, the bank maximum is

    B_A = K_A+p,

and S_A(k)=B_A exactly when k mod p belongs to A. The identity is valid for A equal to the full residue set as well. (Our reduction uses proper nonempty sets.)

## 3. Encoding 3-SAT by simultaneous modular predicates

Start with a Boolean formula on n variables with clauses of length at most three. Remove tautological clauses and repeated literals. An empty clause is a recognized NO instance and can be sent to a fixed nonhalting directed two-cycle with configuration (1,0). If no clauses remain, send the instance to the same two-cycle with configuration (0,0), which halts. Thus assume n>=1 and every clause contains one to three distinct variables and is nonempty.

Choose distinct primes p_1,...,p_n, all at least 3, each O(n log(n+1)). The first n primes starting at 3 suffice and can be found in polynomial time by a sieve; the standard polynomial bound on the nth prime is enough here.

For variable i make a bank with modulus p_i and allowed set {0,1}. For a clause on the distinct variable set I, where 1<=|I|<=3, put

    p_I = product_{i in I} p_i.

Make a bank of this modulus. Its allowed set A_I consists of the Chinese-remainder residues corresponding to the Boolean assignments on I that satisfy the clause. Specifically, b=(b_i) in {0,1}^I contributes the unique a in {0,...,p_I-1} satisfying a=b_i mod p_i for all i in I if b satisfies the clause. At most eight assignments are inspected, and A_I is nonempty. It has 2^{|I|}-1 elements for a non-tautological clause with distinct variables.

There exists an integer k satisfying every bank predicate if and only if the formula is satisfiable:

- If k satisfies all variable predicates, b_i=k mod p_i is a Boolean assignment. Each clause predicate says exactly that its restriction satisfies the clause.
- Conversely, any satisfying assignment b has a simultaneous CRT representative k modulo M=product_i p_i. That representative satisfies every variable and clause bank.

Only the individual moduli p_i and products of at most three such primes are expanded in the graph. The global product M may be exponential but is never expanded, stored as a number of vertices, or used as a simulation length in the reduction algorithm.

## 4. A simple strongly connected graph implementing the banks

Index all variable and clause banks by b. Let their moduli be q_b and their allowed sets A_b. Let

    Q = sum_b q_b,
    P = max_b q_b.

There are exactly Q counter vertices, namely the distinct copies specified by the bank multiplicities c_a. Create one distinguished vertex r and P-1 additional return vertices t_1,...,t_{P-1}. The arcs are:

1. r -> v for every counter v.
2. For a counter v belonging to a modulus-q_b bank: v -> r and v -> t_j for j=1,...,q_b-1.
3. t_j -> r for every return vertex.

The outdegrees are d(r)=Q, d(v)=q_b for each counter in bank b, and d(t_j)=1. Every ordered pair occurs at most once; no loops occur. Distinct counters with the same offset remain distinct vertices, so c_a=2 does not create parallel arcs. Antiparallel r/v arcs are legitimate in the specified simple directed language.

The graph is strongly connected: r reaches every counter directly and reaches every t_j through a counter from a modulus-P bank; each counter and return vertex has an arc to r. Deleting r leaves only arcs from counters to return vertices. The return vertices do not destroy chips: each firing returns one chip to r.

For each bank define

    K_b=q_b(q_b-1)/2-|A_b|,
    B_b=K_b+q_b,
    S(k)=sum_b [K_b+q_b 1_{k mod q_b in A_b}],
    B=sum_b B_b.

Put a chips on each offset-a counter, zero on every return vertex, and

    R = Q+B-1-S(0)

chips on r. All initial counts are nonnegative: counter offsets lie in [0,q_b-1], and S(0)<=B gives R>=Q-1>=0. The total number of chips is

    C=R+S(0)=Q+B-1.

## 5. Exact asynchronous legal evolution

Use the following legal scheduling rule for analysis only: keep all non-r vertices stable; if r is legal, fire r once, then stabilize all counter and return vertices before considering r again. This is not a different game or a sink convention. It is one allowed asynchronous firing order on the original conservative graph.

A non-r stabilization is always finite and legal. Each counter has no incoming arcs except the one from r. At a checkpoint it has between 0 and q_b-1 chips; after one r firing it has between 1 and q_b chips. It therefore fires zero or one times, exactly when its count reaches q_b. Once all such counters have been handled, fire each return vertex once for every chip it holds, returning all those chips to r. No non-r vertex can receive further chips until r fires again.

Inductively, after k firings of r and the intervening non-r stabilizations, every offset-a counter holds (a+k) mod q_b and every return vertex is zero. Thus the counters hold exactly S(k) chips and conservation gives

    chips at r = C-S(k)=Q+B-1-S(k).

Consequently, at a checkpoint:

    r is stable
      iff Q+B-1-S(k)<Q
      iff S(k)>B-1
      iff S(k)=B
      iff every bank predicate holds at k.

All implications use integers and the pointwise upper bound S(k)<=B. If a bank predicate fails, its deficit from its own maximum is exactly its positive modulus, so S(k)<B. All other vertices are already stable at the checkpoint.

If the formula is satisfiable, choose a CRT representative k>=0 satisfying all predicates. If the canonical legal process has already stopped before its k-th checkpoint, it has halted. Otherwise it reaches that checkpoint and is stable there. Equivalently, its first stopping checkpoint is the least nonnegative simultaneous solution. Therefore the chip-firing configuration halts.

If the formula is unsatisfiable, no checkpoint can be stable. At every checkpoint r is legal, and the finite legal non-r stabilization creates the next checkpoint. Iterating gives an infinite legal firing sequence. By the standard abelian halting dichotomy / least action principle, a configuration admitting this infinite legal sequence has no terminating legal sequence. Therefore it does not halt.

This proves the required many-one equivalence:

    formula is satisfiable iff the constructed simple graph configuration halts.

For completeness, the relevant order-independence implication can be proved directly: if a legal word stabilizes with firing count f, then no legal word can ever exceed f in any coordinate. At a first excess firing at v, all other firing counts are <=f and the current count at v equals f_v, so v has at most its final stable chip count and cannot legally fire. Thus an infinite legal word rules out stabilization. This applies to all graphs above without a fairness assumption.

## 6. Polynomial size, including all expanded counters and arcs

Let L denote the 3-SAT input length and let H be its number of variable and clause banks. Then n,H=O(L). Put U=max_i p_i=O(n log(n+1)). Each bank modulus is at most U^3, so P=O(U^3) and Q<=HP.

The graph has exactly

    N=1+Q+(P-1)=Q+P

vertices and

    E=Q+sum_b q_b^2+(P-1)

arcs: each bank has q_b counters, each with q_b outgoing arcs. Thus N=O(HP) and E=O(HP^2), both polynomial in L. An adjacency matrix of N^2 bits is also polynomial-size. Shared return vertices do not introduce repeated arcs.

Each bank can be constructed by iterating through its q_b offsets and evaluating the explicit 0/1/2 multiplicity formula. Its allowed set has at most eight elements and is computed with polynomial-bit CRT arithmetic. The total chip count satisfies

    0<=C=Q+B-1 <= Q+sum_b q_b(q_b+1)/2,

which is polynomial in L. Initial counts and their unary encodings are therefore polynomially bounded as well. No exponential multiplicity, unary expansion of an exponential integer, exponential output, oracle query, or run of the chip-firing process is part of the reduction.

The fixed two-cycle instances for trivial preprocessing cases satisfy all graph and configuration conventions.

## 7. NP membership, credited and with an explicit simple-graph bound

Membership is established in Farrell–Levine, Section 3, for the larger binary directed-multigraph language. Here is a specialization, retaining attribution to their least-action / period-vector method.

Let G be a simple strongly connected loopless graph on N>=2 vertices. Let Delta have diagonal outdegrees and off-diagonal entry Delta_{v,u}=-1 for u->v. A certificate is a nonnegative integer vector f such that z=x-Delta f is stable (and we may require z>=0). Verification is polynomial in the bit length. Least action shows that any such f bounds all legal firing words coordinatewise and hence proves halting.

A halting instance has its actual firing vector f. Let pi be the primitive positive integer vector in ker Delta. By the directed matrix-tree theorem, pi_v is the number of trees oriented toward v divided by their common gcd, so

    1<=pi_v<=(N-1)^{N-1}.

Some vertex w satisfies f_w<pi_w. Otherwise f-pi is another nonnegative stabilizing vector, contradicting least action applied to the actual legal word with count f.

For each arc u->v, the final chip balance and nonnegativity of the initial chips give

    f_u <= d_v f_v+z_v-x_v <= d_v(f_v+1)-1.

Hence f_u+1<=d_v(f_v+1). Follow a simple directed path from any u to w, of length at most N-1. Since d_v<=N-1 and f_w+1<=pi_w,

    f_u+1 <= (N-1)^{N-1} pi_w <= (N-1)^{2N-2}.

Thus every certificate coordinate has O(N log N) bits (with the N=2 bound interpreted directly). The whole certificate and its verification are polynomial-size. Combined with Sections 2–6, this establishes the NP-completeness theorem.

## 8. Scope and prior-work boundaries

The construction is entirely finite and conservative. It uses no dissipative sink and no claim about an infinite sandpile. It differs from the separate accepted multigraph reachability reduction for problem 3000016, whose exponentially large binary multiplicities do not solve this target. It does not settle the Eulerian-multigraph halting problem: these constructed graphs are generally non-Eulerian. The main construction permits antiparallel arcs. The separately accepted [ORIENTED_APPENDIX.md](ORIENTED_APPENDIX.md) proves the stronger restriction to simple oriented graphs forbidding antiparallel arcs, with the same depth and polynomial-chip bounds.

The preliminary observation that any halting simple instance has total chips <=E-N is already present in Farrell–Levine, PDF page 2, and is not claimed as a new result. The present construction obeys that restriction in every YES case and does not exploit large binary chip counts.
