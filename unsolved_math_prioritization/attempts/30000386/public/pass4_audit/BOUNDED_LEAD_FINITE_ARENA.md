# Exact finite arena and age-budget constraints for a bounded maximum lead

Shared PASS4 structural lemma. No large search is performed and no bounded-H winning claim beyond previously accepted cases is made.

## 1. State and effective action domain

Fix maximum effective lead H≥1. Immediately after a Devil announcement at absolute time s, translate the Angel's current position to zero and record each still-future announced pair as (q,k), with k=t−s.

A relevant pair has 1≤k≤H and ||q||∞≤k. Let

C_H={(q,k):1≤k≤H, ||q||∞≤k}.

Expired pairs and pairs outside this reachable cone never affect a later move from the state; the triangle inequality ensures an unreachable pair cannot reenter a descendant cone. Duplicate pairs are collapsed.

Thus a normalized state is a finite set B⊆C_H. The cone size is 4H(H+1)(H+2)/3+H. This is a finite, exact state domain rather than a spatial approximation.

## 2. Exact tail-age budget

Every genuinely reachable normalized state obeys, for each j=1,…,H,

N_j(B):=number of pairs in B with k≥j ≤ H−j+1.                 (1)

Indeed, a bomb of remaining time k was announced in a round r with t−r≤H, so r≥s+k−H≥s+j−H. At most H−j+1 announcement rounds lie between that lower bound and s, inclusive. Distinct pairs require distinct witnesses. Near the initial time there may be fewer available rounds, only strengthening the bound.

These are tail counts across timestamps, not a one-bomb-per-timestamp rule. Many bombs may still share one target time. In particular N_1≤H bounds the total pending count, while N_H≤1 reflects that only the latest announcement can have remaining lead H.

Define K_H to be all B⊆C_H satisfying (1). It is finite.

## 3. Exact transition and closure

From post-announcement state B, Angel chooses delta∈{−1,0,1}². It loses immediately exactly when (delta,1)∈B. If safe, shift every unexpired old pair to (q−delta,k−1) and discard pairs outside the new reachable cone. Devil then chooses one new effective pair d∈C_H or a null action, after observing delta.

For the shifted old set, the tail count at j is at most N_(j+1)(B)≤H−j. Adding one new pair gives at most H−j+1. Therefore K_H is closed under every surviving transition, including repetitions and null announcements.

Every actual Devil pair has one of these effects. Conversely each d∈C_H is a legal announcement with effective lead at most H at that time, and a null action is realized by a current-time announcement. The transition preserves the exact Angel-first adaptive quantifiers.

## 4. Sufficiency of the age constraints for existential reachability

Every B∈K_H can occur as a normalized state after H rounds of some legal play from the empty board. This is existential reachability, not forceability against an Angel trying to win.

List its m≤H distinct pairs (q_i,k_i) with k_1≥…≥k_m. Assign pair i to announcement round

r_i=H−i+1

with absolute target time H+k_i. The tail constraint at j=k_i gives i≤H−k_i+1, hence

(H+k_i)−r_i=k_i+i−1≤H.

Each lead is at least one and each assigned announcement round is distinct. All target times exceed H. Have the Angel stay at zero through round H and use ineffective announcements in unused rounds. No previous target detonates during these H moves, and the final normalized pending set is exactly B.

This also proves the nested-interval assignment condition directly; no extra unrecorded age information is needed in the normalized state.

Consequently, an example satisfying (1) may be a perfectly legal reachable history while still irrelevant to a negative result if Angel can choose a different history. The distinction is strategic reachability, not merely legality.

## 5. Greatest-fixed-point solution of each fixed-H game

For X⊆K_H, define F_H(X) as the states B for which some immediately safe king move has every legal post-move Devil successor in X. Starting with X_0=K_H, iterate

X_(r+1)=F_H(X_r).

These sets descend and stabilize after at most |K_H| strict-removal steps. The stabilized set is the exact infinite safety-winning region. From each state in it, a fixed selected safe move keeps every successor inside it, so a normalized-state positional strategy suffices.

A state removed at finite rank r admits a Devil response after every safe Angel choice that lowers the remaining rank; if no safe move exists, loss is immediate. Thus outside the fixed point Devil can force finite loss, with a bound no larger than the number of arena states.

This establishes decidability for each fixed finite H by finite exhaustive game solving. The arena is enormous, and no practical complexity or completed large-H computation is asserted. The actual question is whether the empty state belongs to the fixed point for every H.

## 6. The H=16 local trap illustrates the distinction

The familiar sixteen-pair preload has eight bombs at relative time one leaving only the center safe, and eight at relative time two surrounding that forced center. It satisfies (1) when H=16. The construction above realizes it after sixteen staying moves using legal leads at most sixteen. After the next forced move, Devil adds the ninth relative-time-one neighbor and forces a loss.

This state is outside the safety-winning region. Its existence does not show the empty state is outside that region: staying for the sixteen preparation rounds was a cooperating Angel choice. An H=16 negative theorem would need an adaptive strategy forcing a losing state despite all alternative earlier moves.

For H=15, the sixteen pending pairs already violate N_1≤15. This explains the local count boundary of the earlier guard, but says nothing by itself about whether another strategy handles H≥16.
