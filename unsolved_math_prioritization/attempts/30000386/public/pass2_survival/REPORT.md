# Shared PASS2: delayed announcements, deadline awareness, and nonlinear density

## Outcome and exact scope

The unrestricted speed-one two-dimensional Time-Bomb conjecture remains unresolved. The principal positive result here is a winning theorem for arbitrary adaptive mixtures of detonation times subject to an explicit minimum announcement lead. The required lead can be chosen of order sqrt(n) log n at announcement round n. This is a proper restriction of the original Devil, not a solution of the original game.

The proof is online in its information structure. A randomized legal Angel is used as a proof device; it survives with a uniformly positive probability against every adaptive nonanticipating Devil satisfying the lead restriction. Exact finite-horizon determinacy and the previously accepted finite-Angel-action compactness argument then imply a deterministic infinite winning strategy for that restricted game. This is an existence theorem, not an algorithm for computing the extracted deterministic strategy.

Additional results show that retaining only a fixed number of earliest raw pending deadlines is insufficient, and that an exact nonlinear bad-center operation can still inflate spatial mass by a factor tending to 9/8.

Original contract SHA-256: `1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c`.

## 1. A general hidden-block criterion

Choose strictly increasing integer times

1=S_1<S_2<S_3<...,

with S_j tending to infinity. Write L_j=S_(j+1)−S_j. The restricted Devil is required to satisfy:

If S_j≤n<S_(j+1), then every effective announcement (p_n,t_n) made in round n has t_n≥S_(j+2).

Past/current-time announcements are harmless and may also be permitted. Put

Q = sum_(j≥1) L_j / (2L_(j+1)+1)².

**Theorem 1.** If Q<1, the Angel has a deterministic infinite winning strategy against every adaptive Devil obeying this restriction.

### 1.1 Randomized legal motion

Set a_1=(0,0). For each block j, independently choose a random vector D_j uniformly from the integer square [−L_j,L_j]². Starting at time S_j, execute a fixed legal sequence of L_j king steps with total displacement D_j. For example, for each coordinate separately, move by its sign for the first |D_j^(coordinate)| steps, and then use zero increments for that coordinate. Combining the two coordinate increments gives legal king moves, including stays. Thus

a_(S_(j+1))=a_(S_j)+D_j.

The choices for future blocks are independent of all previously observed motion. They can be sampled when the block starts. The Devil sees every actual Angel move and can adapt every announcement to the entire observed history; it does not observe future random variables.

For probability bookkeeping, continue this hypothetical random path even after an eventual collision, and extend the Devil's rule after such a collision by any legal nonanticipating rule. Before the first collision this is precisely the legal play. This convention makes all future announced-pair hit events well-defined.

### 1.2 Conditional probability of one hit

Fix a round n with S_j≤n<S_(j+1), and define the effective hit event E_n={t_n>n and a_(t_n)=p_n}. Conditional on the entire observed history through the round-n Angel move and on the Devil's round-n choice, p_n and t_n are fixed. If t_n≤n, the conditional probability of E_n is zero; such an announcement cannot kill retroactively. In the rest of this paragraph assume t_n>n, so the lead restriction applies. The vector D_(j+1) is still independent and uniform: its block has not started at n. The lead restriction ensures that its whole block is completed by t_n.

Consequently the random location at the chosen detonation time has the form

a_(t_n)=D_(j+1)+Z,

where, conditional on that history and choice of t_n, Z is independent of D_(j+1). It contains any unrevealed part of the current block and all other complete or partial blocks contributing to a_(t_n). The Devil's later actions do not affect the hypothetical Angel path, which ignores announcements.

Convolution with a probability distribution cannot increase the largest point mass of a uniform distribution. Therefore

P[E_n | history and the round-n choice] ≤ 1/(2L_(j+1)+1)².

The same inequality holds unconditionally. It remains valid when the Devil chooses the position and time adaptively, since both are fixed by the conditioning. A randomized Devil can also be handled by conditioning on its independent random choices.

### 1.3 Positive survival probability and deterministic extraction

There are L_j announcement rounds n in the interval [S_j,S_(j+1)). The countable union bound gives

P[union_(n≥1) E_n] ≤ Q<1.

This union contains exactly the possible lethal collisions; ineffective current/past-time announcements are excluded.

Thus this randomized Angel survives forever with probability at least 1−Q, uniformly against every admissible adaptive Devil.

For completeness, this implies the asserted deterministic strategy without assuming that private randomness itself is the final strategy. If the initial state failed some finite-horizon winning predicate, finite perfect-information backward induction would give an admissible Devil strategy forcing loss by that horizon against every Angel move sequence, including every realization of the random path. That contradicts the strictly positive survival probability just proved. Hence every finite-horizon predicate holds. The compactness argument using nested nonempty subsets of the nine Angel moves now yields one deterministic infinite winning strategy. Absolute time is included in the state so that the announcement restriction is respected.

This reasoning does not commute an offline path-existence quantifier with an adaptive strategy quantifier. It directly bounds a randomized online policy against each adaptive Devil, then invokes exact game determinacy.

## 2. Explicit minimum-lead families

### 2.1 Cubic blocks and a simple power-law bound

Take S_j=j³ for j≥1. Then

L_j=3j²+3j+1,

and L_(j+1)>L_j≥3j². Hence

Q < sum_(j≥1) 1/(4L_j) ≤ (1/12) sum_(j≥1) 1/j² ≤ 1/6.

The last inequality follows from 1+integral_1^infinity x^(−2) dx=2. The randomized survival probability is therefore greater than 5/6.

The exact restriction is:

If j³≤n<(j+1)³, then t_n≥(j+2)³.

A simpler sufficient condition is

t_n−n ≥ 26 n^(2/3).

Indeed, n≥j³, and

(j+2)³−n ≤ (j+2)³−j³ = 6j²+12j+8 ≤ 26j² ≤ 26n^(2/3)

for j≥1. For integer time coordinates, the right side can be rounded up. Thus the Angel wins against arbitrary mixed deadlines whenever every effective bomb is announced at least ceil(26n^(2/3)) rounds before its detonation.

### 2.2 An explicit lead of order sqrt(n) log n

Let

b(j)=1+floor(log₂j),
L_j=j b(j)²,
S_1=1,
S_(j+1)=S_j+L_j.

The lengths are nondecreasing. Therefore

Q < (1/4) sum_(j≥1) 1/L_j.

For j in the dyadic group 2^k≤j<2^(k+1), b(j)=k+1, and

sum_(j=2^k)^(2^(k+1)−1) 1/[j b(j)²] ≤ 1/(k+1)².

Summing and again using sum_(m≥1)1/m²≤2 gives Q<1/2. The randomized survival probability is greater than 1/2.

Define the explicit integer lead function

g(n)=S_(j+2)−n whenever S_j≤n<S_(j+1).

Theorem 1 proves a deterministic win whenever every effective announcement satisfies t_n−n≥g(n). These times may otherwise be mixed arbitrarily and chosen adaptively.

Here is an explicit conversion, including small n:

g(n)≤21 sqrt(n) [1+log₂n] for every integer n≥1.

For j≥2, take the floor(j/2) terms with ceil(j/2)≤i<j in the sum defining S_j. Each satisfies i≥ceil(j/2) and b(i)≥b(j)−1≥b(j)/2. Also floor(j/2) ceil(j/2)≥j²/5 for j≥2. Consequently

n≥S_j≥j² b(j)²/20.

Furthermore j+1≤3j/2 and b(j+1)≤b(j)+1≤3b(j)/2, so L_(j+1)≤27L_j/8. Therefore

g(n)≤L_j+L_(j+1)≤35L_j/8≤(9/2)j b(j)²

≤(9/2)sqrt(20n) b(j)<21 sqrt(n) [1+log₂n],

where b(j)≤1+log₂j≤1+log₂n because S_j≥j. The only block-j=1 time is n=1; then S_2=2, S_3=10, and g(1)=9≤21. This proves the displayed bound for every n.

Thus t_n−n≥ceil(21 sqrt(n)[1+log₂n]) is a simple sufficient delay, and the exact block rule g is usually smaller. In particular the required lead is O(sqrt(n) log(n+1)). The theorem asserts these explicit lead rules, not that every unspecified constant in such an O-bound suffices.

### What this does not cover

The original Devil may announce a bomb for the very next Angel move, or for any other shorter lead. Such announcements are excluded by the hypotheses above. The random path ignores bombs and would not have this union-bound guarantee in their presence. There is no claimed method here to combine the hidden-block theorem with unrestricted short-lead protection while preserving its conditional independence.

## 3. Fixed-size earliest-deadline memory is insufficient

This obstruction concerns a precisely restricted deterministic policy. At Angel move n, call a deadline pending when t≥n. The policy retains only the k earliest distinct raw pending deadlines and the bombs at those deadlines. Its move may depend on time, its previous moves, and the successive retained-history projections, but not on discarded deadline data or hidden summaries of those data. If two histories have identical such projections, the policy makes the same move. This definition does not cover a policy that first removes spatially irrelevant bombs and then selects k remaining deadlines.

**Theorem 2.** For each fixed k≥1, every such policy is defeated by a legal Devil, even though the policy may inspect retained timestamps arbitrarily far into the future.

Let M=(2k+1)² and T=2k+M+1. During rounds 1,...,k, announce one fixed decoy bomb at each of the k distinct times T−k,...,T−1. Their positions may all be the origin. There is no detonation during these first k rounds.

For the remaining construction, simulate the policy through its move at time T−k using only this retained decoy history. Up to and including that move all k decoys are still pending under the t≥n convention, so bombs at time T are excluded from the retained history. Thus their positions do not affect this simulated path. If a decoy would kill the policy, the Devil has already succeeded; otherwise let a_* be its simulated position at time T−k.

In rounds k+1,...,k+M, announce the M pairs (p,T) for all p in a_*+[−k,k]², in any fixed order. These announcements are complete by

k+M = T−k−1.

They remain hidden from the restricted policy through its move at T−k. The actual and simulated positions up to that move therefore agree unless there has already been a fatal decoy collision. At the next move the first decoy is expired and deadline T may become retained, but only k moves remain between position a_* at time T−k and time T. Every possible endpoint lies in a_*+[−k,k]², all of which is bombed at T. Hence the policy loses no later than T.

The schedule is determined in advance once the deterministic policy is fixed; no future Angel choices are observed. The argument does not defeat policies capable of using unboundedly many pending deadlines, or randomized policies outside this precise sensitivity class. It supplements, rather than replaces, the earlier bounded time-distance-lookahead obstruction.

## 4. Nonlinear bad centers can also inflate mass

For a finite set B of preloaded terminal bomb positions, consider a state with exactly two Angel moves remaining until that common terminal time and no other lethal time. The Devil may make one new terminal announcement after observing the first of these two moves.

Write

A_8(B)={q: |N(q) intersect B|≥8},
E(C)={a: N(a) is a subset of C},

where N(x)=x+{−1,0,1}².

The exact set of losing starting centers is

L_2(B)=E(A_8(B)).

Indeed, after a first move to q the Devil can fill the last missing terminal neighbor if and only if at least eight of N(q)'s nine points are already bombed. The Angel loses from a precisely when every possible first move has this property. This is an exact online universal-response predecessor, not a sufficient-density surrogate.

Now take m≥2 and let

B_m = {0,...,3m−1}² minus { (x,y): x and y are both divisible by 3 }.

Then |B_m|=8m². Every 3×3 square wholly inside the large square contains exactly eight B_m points, because any three consecutive integers contain exactly one representative of each residue class modulo 3. It follows that A_8(B_m) contains {1,...,3m−2}², and hence L_2(B_m) contains {2,...,3m−3}². Therefore

|L_2(B_m)| / |B_m| ≥ (3m−4)²/(8m²),

whose limit is 9/8.

In particular, for all sufficiently large m this nonlinear losing-center map increases the number of occupied spatial positions. Uniform unweighted mass contraction is therefore unavailable even for this exact nonlinear operation. This agrees with, but is logically separate from, a 9/8 lower bound for local linear hazard certificates.

This is a statement about preloaded states. It does not assert that the Devil can force the initial unrestricted game into one of them. A useful invariant could still exploit the actual reachable Angel position, announcement history, or amortized cost of creating a large cluster.

## 5. A safe transport primitive and its limitation

A small positive ingredient for mixing weak intermediate threats with distant deadlines is the following. Let R_n be a prescribed 2×2 lattice room. Suppose R_(n+1) is R_n translated by one cardinal unit, or is unchanged. From every point of R_n, at least two points of R_(n+1) are reachable in one king move. Thus, whenever at most one already-announced bomb explodes in R_(n+1) at that time, the Angel can stay inside the prescribed moving room by selecting an unbombed reachable point.

This is an online deterministic transport rule. Alternating horizontal and vertical room translations can achieve a prescribed diagonal displacement, at the cost of Manhattan rather than king distance. It does not by itself yield a terminal hazard strategy: selecting a small final room too early permits the Devil to stockpile bombs on all its terminal positions. The multiscale final-step margin remains essential.

## Remaining gap

The hidden-block theorem genuinely uses information timing and allows arbitrarily many adaptive mixed deadlines, but only long-lead announcements. The unrestricted target still needs simultaneous protection against short-lead threats without destroying the future-block spread, or a different history-aware nonlinear invariant. Counting only bad centers, retaining finitely many urgent deadlines, and reusing terminal-only traversals are insufficient in the forms analyzed here.

No novelty or current-openness assertion, publication action, or full-game resolution is claimed.
