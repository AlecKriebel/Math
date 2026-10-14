# Acceptance: two-move deficit reserve and weighted terminal capacity 5/2

Shared PASS3 independent audit. These are sole-terminal-hazard results and robust local preloaded-state bounds. They do not permit an unhandled intermediate lethal timestamp.

## Audited inputs

- `../pass3_invariant/TWO_MOVE_DEFICIT_RESERVE.md`, SHA-256 `853a0f8b7e8ab9ea9179c6177e1a496c8d26397f7b383fd3d024559fbdcef2ea`.
- `../pass3_invariant/FIVE_HALVES_TERMINAL_CAPACITY.md`, SHA-256 `1642e3f1286e5df69403eba81121399fb184fbeda0b4c65c4e3bd919252ae8c2`.

Both are accepted without a mathematical correction.

## 1. Exact two-move adaptive condition

For first move q, the minimum nonnegative update mass that raises every value on N(q) to at least one is exactly

sum_(x in N(q)) (1−g(x))_+.

Therefore an Angel with no intermediate lethal requirement wins the two-move continuation exactly when some legal q has this deficit sum strictly greater than beta. If every q has deficit at most beta, an adversary observing the first move can fill its deficits within budget.

The four corner-centered 3-by-3 neighborhoods cover the full 5-by-5 reachable square. With local mass M, its total deficit is at least 25−M, including when some g values exceed one. If M<25−4beta, the sum of the four corner-window deficits exceeds 4beta, so one window has deficit greater than beta. Moving to its center and then selecting a subunit neighbor after the update is a valid online strategy.

The strict inequality is necessary for this mass-only guarantee. For 0≤beta≤4, put deficit beta/4 at each of the sixteen non-axis cells in the 5-by-5 square and zero on the nine axis cells. Every legal first-move neighborhood contains exactly four non-axis cells, hence has deficit beta. The total mass is 25−4beta and the adaptive update fills that selected window. Nonnegativity holds precisely throughout the stated beta range. No sharpness beyond that range is claimed.

For beta=1 with genuine point bombs, the binary example marking every position except the four extreme corners has mass 21. A legal first-move neighborhood contains at most one of those corners, so one point announcement suffices to fill its last hole, if any. This separately verifies sharpness under the original point-bomb update rule.

## 2. Prior boundary update

A prior update of mass at most beta raises the local mass by at most beta. Thus the pre-boundary condition M<25−5beta implies the post-boundary condition of Section 1. It is universal over that update and is not assumed observed before the earlier terminal move.

For unit point bombs, removing one additional noncorner mark from the 21-mark example leaves 20; the boundary announcement restores it, and the next adaptive announcement completes the terminal trap. Hence the strict pre-boundary threshold 20 is sharp for local point-bomb preloads as well.

These preloaded states are not claimed forceable from the empty board. The fractional sharpness example uses a distributed weighted update and is not mislabeled as a one-point Devil move.

## 3. Endpoint geometry for capacity 5/2

Start with E_0=[−2,2]² and radius R_0=2. For a=2^k, the four translates of E_(k−1) by (±3a/2,±3a/2) have disjoint sign-coordinate ranges. The child radius is 3a/2−1, so its nearest coordinate to either separating axis is one. Cardinality is therefore exactly 25a² and radius exactly 3a−1.

A child center is reached in 3a/2 legal king moves. This leaves precisely R_(k−1) moves from a state with R_k remaining. No speed increase or teleportation is used. Initial waiting w=T−R_k satisfies 0≤w≤3a−1 by maximality of k.

## 4. Average accounting and final adaptive finish

The initial wait contributes average at most beta w/(25a²). A traversal to a child of size 25(a/2)² lasts 3a/2 rounds, including its arrival update, and contributes at most 6beta/(25a). A least-average child inherits no greater current average than its parent.

Summing over the dyadic levels gives base-square average at most

beta[w/(25a²)+(6/25)(1−1/a)].

At this point exactly two moves remain. The two-move deficit lemma applies when this average is below 1−4beta/25, equivalently when

beta[w/(25a²)+2/5−6/(25a)]<1.

Using w≤3a−1 bounds the bracket by 2/5−3/(25a)−1/(25a²), strictly below 2/5. It is nonnegative even at a=1, so beta≤5/2 yields strict success, including beta=5/2. The empty geometric sum for a=1 is correct. The separate T=1 case is safe because no announcement precedes the first move.

Every wait and traversal ends by time T−2 and includes exactly its own post-move updates. The final first move is at T−1, after which the adversary may spend its full mass beta; this is precisely the update reserved by the deficit lemma. The final value is selected after observing that update and before the irrelevant post-T update.

## 5. Intermediate-death boundary

The result cannot be applied across an unhandled allowed timestamp. For example, eight first-time bombs can force the sole safe first move to q=0, while eight terminal bombs in N(0) allow Devil to fill the ninth after that move. The terminal preload is only eight, far below 21, yet that two-deadline state loses. The four-corner choice in the deficit proof is unavailable because those first moves are lethal.

Thus the new mass capacity improves a sole-terminal component. Using it in a mixed-deadline induction still requires the accepted robust predecessor condition for every intermediate deadline and the announcement following each boundary.
