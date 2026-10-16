# Independent derivation before historical audit labels

UTC: 2026-10-14. The authenticated claim files were read before the historical
MATHEMATICAL_AUDIT, SOURCE_REVIEW, STATUS, ACCEPTANCE or another review's outputs.
The words “accepted” in the claim document are not used as evidence. Nine
submitted files were compared byte for byte with Git head
f37a3ff66595fcf75bb18bf859be8594c3662242.

## Exact statement

HALTING is NP-complete on explicitly finite conservative loopless simple
strongly connected directed graphs with N >= 2, nonnegative binary chips and
ordinary asynchronous legal firing. The main graph can have antiparallel arcs;
the appendix forbids them. Both hardness constructions have a distinguished
root whose deletion leaves only counter-to-return arcs, and polynomial numeric
total chip counts. No Eulerian assertion or priority assertion is needed.

## Storage encoding

For p >= 2 and h the periodic indicator of a nonempty A, let
c_a = 1 + h(-a-1) - h(-a). Each c_a is 0, 1 or 2 and their sum is p.
They denote separate vertices, not parallel arcs. Define
S(k) = sum_a c_a ((a+k) mod p). Only offset -k-1 wraps, hence
S(k+1)-S(k) = p-p c_{-k-1} = p(h(k+1)-h(k)).
The mean of S is p(p-1)/2 and that of p h is |A|, so
S(k) = p(p-1)/2-|A|+p h(k). Its maximum K+p is attained precisely on A
(including full A, where every k attains it). The empty A is not used: it
would have constant storage K and never attain the chosen K+p.

Relabel the distinct variables actually appearing in a valid 3-CNF input,
discard tautological clauses, remove duplicated literals, and detect empty
clauses. This makes n at most the input length even if a representation's
declared variable count is enormous. Malformed strings and empty clauses map
to a fixed NO halting instance; an empty conjunction maps to a fixed YES.
Assign distinct primes >= 3 to the remaining variables. Variable banks allow
0 and 1. Clause periods are products of at most three distinct primes; allowed
residues are the at most eight CRT representatives of satisfying local Boolean
assignments. Thus clause sets are nonempty and proper. All bank predicates have
a simultaneous solution if and only if the formula is satisfiable. The global
CRT product can be exponential, but it is used only in a mathematical existence
argument, not to output vertices or to compute a firing sequence.

## Conservative realization and exact checkpoints

There are Q = sum q_b counter vertices, root r of outdegree Q, and P-1 return
vertices for P = max q_b. Root sends one chip to each counter. Each q-counter
sends one chip to root and to the first q-1 returns; each return sends one chip
to root. Outdegrees are Q, q and 1. Distinct vertices even when offsets repeat
give simple ordered pairs. A largest-period bank reaches all returns, so all
vertices communicate through r. After removing r, only counter-to-return edges
remain. There are Q+P vertices and Q+sum q_b^2+P-1 arcs.

Initialize offset a counters with a chips, returns with zero, and root with
R = Q+B-1-S(0), where B=sum (K_b+q_b). Since S(0)<=B, R>=Q-1.
The invariant total is C=Q+B-1. At a checkpoint after k root firings, the
counters contain their residues (a+k) mod q and all returns are empty.
One legal root firing makes each counter fire either zero or one time; returns
then fire finitely often and receive no further chips after the counter stage.
This is a legal schedule on the conservative graph, not a sink stabilization.
The root has C-S(k), and is stable precisely when S(k)=B, since both quantities
are integers and S(k)<=B. Equality holds precisely when every bank predicate
holds. A satisfying CRT representative implies a stable checkpoint, unless an
earlier stable checkpoint has already stopped the process. If unsatisfiable,
root is legal at every checkpoint and these finite blocks concatenate into an
infinite legal word.

## Asynchrony, least action and absence of fairness assumptions

Let f>=0 be any stabilizing firing vector: z=x-Delta f has z_v<d_v for all v.
For any legal word, consider a first firing that would exceed f in one
coordinate v. Immediately before it, its own count is f_v, every other count
is <=f_u, and incoming arcs have nonnegative multiplicities. The chips at v
are therefore <=z_v<d_v, a contradiction. Every legal word is bounded by f.
This proof does not require the hypothetical vector f itself to be legally
realizable and does not require fairness. In particular, existence of an
infinite legal word rules out every legal stabilization; existence of a stable
checkpoint supplies f and rules out every infinite legal word. A maximal legal
word is then finite and stable. Arbitrarily stopping a legal word early is not
a terminating maximal play.

## Polynomial reduction size

The first n primes starting at 3 are bounded by U=O(n log(n+1)) and a sieve up
to a polynomial bound finds them. There are H=O(L) banks, each q<=U^3.
Therefore Q<=HU^3, P<=U^3, N=Q+P, and E=Q+sum q^2+P-1 are polynomial.
CRT needs polynomial-bit arithmetic and each expanded offset loop has a
polynomial numeric bound. C <= Q+sum q(q+1)/2 is also polynomial numeric.
The algorithm never enumerates the global period. Sparse or explicit adjacency
matrix output both have polynomial length. Variable-index relabeling handles
unusual declarations without relying on an exponentially large declared n.

## NP membership and the direction of every bound

Use column firing convention: Delta_{vv}=d_v and Delta_{vu}=-1 for u->v.
A nonnegative vector f with 0<=x-Delta f<d coordinatewise is a certificate;
least action proves its soundness. For a halting instance choose its actual
legal firing vector f. The primitive positive integer kernel vector pi is the
rooted directed tree count vector divided by its gcd, so
1<=pi_v<=(N-1)^(N-1). Each non-root vertex in a directed in-tree has one of at
most N-1 choices of outgoing neighbor; this upper bound counts even invalid
choices, so is valid without a determinant estimate.

Some w has f_w<pi_w. If not, f-pi is nonnegative and gives the same stable
configuration; the already performed legal word of count f would exceed it,
contradicting least action. For every arc u->v, the balance equation is
sum_{a->v} f_a = d_v f_v+z_v-x_v. All summands are nonnegative, x_v>=0,
and z_v<=d_v-1. Hence f_u+1<=d_v(f_v+1). Follow a simple directed path
FROM u TO w, not in the opposite direction; multiply the bounds for its
successive heads. Its length is at most N-1, every head degree <=N-1, and
f_w+1<=pi_w. Therefore f_u+1<=(N-1)^(2N-2). Every coordinate has
O(N log N) bits, and checking the balance against binary x is polynomial.
For N=2 the only loopless simple strongly connected graph is the two-cycle;
its stable capacity is zero, so a halting nonnegative input is x=0 and f=0.
The formula yields f+1<=1, correctly. No total-chip bound on arbitrary inputs
is assumed for membership.

## Oriented strengthening

Replace P-1 returns by P returns and counter->root by counter->t_q, keeping
counter->t_1,...,t_{q-1}. All arcs run root->counter->return->root; opposite
arcs are absent. Outdegrees and returned chip quantities are identical, so
every storage, checkpoint, asynchrony and polynomial argument survives. There
are 1+Q+P vertices and Q+sum q^2+P arcs. Fixed three-cycle 000/100 supplies
the trivial YES/NO instances. Deleting root still leaves depth-one edges.

## Independent provisional conclusion

The proof is complete as a mathematical argument with the above ordinary input
encoding conventions. Primary-source hypotheses, exact target scope and fresh
computational controls remain to be checked. No historical acceptance, claimed
novelty, publisher identity or contemporary openness is adopted here.
