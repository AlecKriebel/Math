# A rigorous reference-path correction transfer criterion

Status: a conditional proof bridge, not a construction of the required correction policy and not a solution of the unrestricted Time-Bomb game. All moves, announcement timing, and repeated-timestamp allowances are those of the original contract.

## 1. Reference and corrected processes

Let 1=S_1<S_2<... be integer block boundaries tending to infinity, with L_j=S_(j+1)−S_j. Set the reference location X_1=0. In block j, an independent vector D_j is uniform on [−L_j,L_j]². A prescribed legal block path has total displacement D_j, so X_(S_(j+1))=X_(S_j)+D_j. Its within-block position may be any fixed function F_j(u,D_j), 0≤u≤L_j, with F_j(0,D_j)=0 and F_j(L_j,D_j)=D_j. The move-then-hold reference from the preceding pass is one example.

The corrected Angel Y takes legal king moves. It may react arbitrarily to observed announcements and all reference draws whose blocks have started. It must not inspect a draw D_i before time S_i. Additional private randomness may be used, provided it is independent of the future D_i. Presampling the draws is harmless only if the correction policy cannot access them before their block starts.

Fix any legal adaptive Devil. Continue both processes hypothetically after a first collision, extending the Devil and correction policy legally and nonanticipatingly. This is only for event bookkeeping; before a first collision the hypothetical and actual plays coincide.

An effective announcement made at n has t_n>n. If n belongs to block j, call it long when t_n≥S_(j+2), and short when n<t_n<S_(j+2). Ineffective announcements have no hit event.

## 2. The good-event hypotheses

Let r(t) be a deterministic nonnegative integer radius for every positive integer time t. Assume that, against every legal adaptive Devil, the corrected policy has an event G with probability at least 1−epsilon on which both hold:

1. No short announcement ever hits Y.
2. ||Y_t−X_t||_infinity≤r(t) for every t.

The event may depend on the full random history. In particular, G need not be independent of any reference draw. The radius is an a priori deterministic envelope, rather than a radius selected after seeing the target or future reference randomness.

For n and t with t≥S_(j(n)+2), define

L*(n,t)=max{L_i : S_i>n and S_(i+1)≤t}.

The set is nonempty: it contains block j(n)+1. Define

q_n = sup_(integer t≥S_(j(n)+2)) min{1, (2r(t)+1)²/(2L*(n,t)+1)²}.

**Transfer theorem.** If epsilon+sum_(n≥1)q_n<1, then the full original Time-Bomb game has a deterministic infinite Angel-winning strategy.

This is a sufficient condition. The present report does not establish its good-event hypotheses for any useful full-game correction policy.

## 3. Proof without independent correction errors

Condition on the observed history through the round-n Angel move and on the Devil's chosen pair (p_n,t_n). For a long announcement, choose a completed fresh block i attaining L*(n,t_n). Since S_i>n, the corrected history has not accessed D_i. The draw remains uniform and independent of all other reference displacements even after this conditioning. At the now-fixed target time,

X_(t_n)=D_i+Z,

where Z is conditionally independent of D_i. This decomposition concerns the reference path only; no independence assertion is made about Y_(t_n)−X_(t_n).

On the event that G holds and the announcement hits Y,

X_(t_n) belongs to p_n+[−r(t_n),r(t_n)]².

The conditional probability of the latter event is at most (2r(t_n)+1)²/(2L_i+1)², capped at one. Thus

P[G and this long announcement hits Y]≤q_n.

There is no conditioning on G in this calculation; the hit-and-good event is merely contained in a small reference-location event. This is why arbitrary dependence of the correction error and G on the hidden displacement is allowed.

On G, short announcements cannot cause a collision. Consequently

P[any lethal collision]≤epsilon+sum_(n≥1)q_n<1.

The bound is uniform over adaptive Devils. Every finite-horizon losing Devil would defeat every realization of this corrected randomized policy, a contradiction. Exact finite-horizon determinacy followed by the accepted compactness argument over the nine Angel moves gives one deterministic infinite winning strategy for the full game.

## 4. What the theorem repairs, and what it leaves open

A correction error need not remain independent of an earlier hidden displacement. A geometric error envelope is enough to replace that invalid independence step by a correct set-cardinality bound. However, this does not supply a policy that both avoids all short threats and satisfies a sufficiently small envelope with high probability. The companion obstruction proves that the accepted move-then-hold reference cannot furnish this bridge with the preceding cubic or logarithmic block schedules.
