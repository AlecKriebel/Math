# Exact acceptance condition for induction over known allowed deadlines

Shared PASS2 structural lemma. The original Time-Bomb rules remain unchanged. This document establishes a necessary-and-sufficient composition gate, not a new survival theorem for arbitrary deadlines.

## 1. What is known, and what remains adversarial

Fix a finite set D={T_1<…<T_k} of allowed positive detonation times. The Angel is told D. The Devil's target positions and choices among D remain adaptive: in round n it observes a_n and then chooses one pair (p,t), with t∈D. Repeated pairs and allowed past/current timestamps are ineffective but legal. An ineffective action is represented by a null symbol. Even before the first allowed deadline, its continuation effect can be realized by targeting a spatial point outside the reachable cone through max D; after the final deadline, every allowed timestamp is past/current. Thus a null action is an exact effective action type for a nonempty finite D. The empty allowed set is immediately harmless.

A strategy must use only D and the already observed finite history. In particular, knowing D is not knowing the completed list of target positions, the multiplicity assigned to each deadline, or the future adaptive choices.

A state at time s is taken immediately after the round-s Devil announcement and consists of (s,a,B), where a is the Angel's current position and B is the finite set of still-future announced pairs. Time zero is a distinguished initial state (0,0,empty), with no fictitious round-zero announcement.

## 2. Exact post-announcement winning sets

For s≤max D, write W_s^D for the set of such states from which the Angel can survive every remaining allowed deadline against every future adaptive Devil. When s≥max D, every surviving state is winning because all allowed timestamps have passed.

The state includes preloaded bombs for every later timestamp. A theorem for the empty-board game with the later timestamps cannot be applied directly to a state containing such preloads.

Let M={−1,0,1}². For a current state (s,a,B), a candidate next position is a'=a+v with v∈M. Its immediate safety condition is

(a',s+1) not in B.

Only after that check does Devil announce. Delete expired pairs and then add the new announcement if its time exceeds s+1. Let A_(s+1)^D be the set of all pairs (p,t) with p∈Z² and t∈D, t>s+1, together with the null effective action. Then the exact recursion is

(s,a,B)∈W_s^D

if and only if there exists v∈M such that (a+v,s+1)∉B and, for every d∈A_(s+1)^D,

(s+1,a+v, B restricted to times greater than s+1, plus d)∈W_(s+1)^D.

This is ordinary finite-horizon backward induction. Spatial and time cones may be truncated exactly as in the accepted PASS1 reduction. The universal response depends on the chosen move; it is not a precommitted schedule. Current-time announcements cannot change the just-completed safety check.

## 3. Exact pre-announcement acceptance at a deadline

Fix a deadline U∈D. Immediately before the Angel's move at U, let B^- denote all still-relevant pairs announced through round U−1. Suppose the Angel proposes the terminal position a. Define the robust acceptable-position set G_U^D(B^-) by the following two simultaneous conditions:

1. (a,U)∉B^-.
2. For every legal round-U announcement d, the post-announcement state

   (U,a, B^- restricted to times greater than U, plus d)

   belongs to W_U^D.

Here W_U^D concerns all later allowed timestamps and all preloaded bombs, and the newly chosen d may depend on a. If U is the final allowed deadline, the second condition is vacuous apart from an ineffective update, so acceptance reduces to immediate safety.

This is the exact terminal-state acceptance condition needed to concatenate an earlier-phase strategy with a later-deadline strategy. It is both sufficient and necessary when the continuation set is the exact winning set:

- Sufficiency: survive the move at U, observe the actual d, and then use a winning continuation for that complete post-announcement state.
- Necessity: any strategy that wins from the pre-move state must choose a safe a and must win after every legal d. Otherwise Devil chooses a failing update after observing a.

For a convenient sufficient family P_U⊆W_U^D, replacing W_U^D by P_U gives a sufficient, possibly stronger gate. The requirement remains universal over the boundary update.

### A one-round check that catches missing boundary reserve

Suppose the only later deadline is U+1. From a post-announcement state at U, survival at U+1 is equivalent to at most eight time-(U+1) bombs in N(a)=a+M. Before the round-U announcement, robust acceptance therefore requires at most seven such bombs in N(a): Devil may add the missing eighth or ninth target after observing a.

In particular, a pre-announcement state with eight next-time bombs around a has a safe next step if no further bomb is added, but is not a valid accepted endpoint. Devil can announce the ninth neighbor and kill at U+1. This local example shows why the boundary update cannot be absorbed by saying merely that a continuation is currently possible.

For the accepted two-deadline construction with gap one, its threshold b/8<1 is exactly the needed integer reserve b≤7 before that update, allowing b≤8 afterwards.

## 4. Exact phase-composition lemma, including intermediate deaths

Let s<U and let P_U be any chosen set of acceptable post-announcement states at time U. Define phase values V_m for s≤m≤U by backward induction:

- At m=U, V_U(a,B) is membership of (U,a,B) in P_U.
- At m<U, V_m(a,B) holds if there exists v∈M with (a+v,m+1)∉B such that every legal Devil update at round m+1 leads to a state satisfying V_(m+1).

The final iteration m=U−1 includes both the safety check at U and the round-U Devil update before testing P_U. Every earlier iteration also tests its actual time's lethality before updating. This matters when a proposed phase spans several allowed deadlines.

By induction on U−m, V_s is equivalent to a history-dependent online strategy that survives every move through U and enters P_U after the boundary update, against every adaptive Devil. This remains valid with preloaded bombs and with any allowed times inside the phase.

When U is the very next allowed timestamp after s, no intermediate time lies in D, so the intermediate safety tests happen to be automatic. That simplification is justified by the restriction on allowed timestamps, not by the fact that a construction is called a terminal-time strategy. When a proposed traversal crosses another allowed deadline, the safety test cannot be dropped.

### Induction over a complete allowed set

Let T_0=0. Choose sets P_j of post-announcement states at T_j, with P_k containing every surviving post-final-deadline state. For each j, establish that every state in P_(j−1) admits a phase strategy to P_j, with the exact phase game above. Require that the genuine empty initial state lies in P_0.

The strategies concatenate: at each boundary observe the actual announcement, determine the actual state in P_j, and run its certified next-phase strategy. This is one online strategy for D. There is no requirement that the Devil's future announcements be fixed beforehand.

Taking P_j to be the exact W_(T_j)^D makes these conditions necessary as well as sufficient. Taking tractable subsets P_j is an invariant-based proof route, but every claimed subset membership and every transition must be proved.

## 5. What a terminal hazard must actually certify

A nonnegative terminal field f_U(a;B^-) can be used as a sufficient proxy if it has the implication

f_U(a;B^-)<1 implies a∈G_U^D(B^-).

The right side includes both immediate time-U safety and universal robustness to the following announcement for the complete later-deadline state. Merely bounding the number of later bombs in one square, finding a safe endpoint for each later deadline separately, or proving empty-board survival for the remaining timestamps does not establish this implication.

A weighted-terminal construction also needs an independently proved update bound: each one-bomb announcement, at any allowed timestamp, must change the field by a nonnegative increment with controlled total spatial mass, or some other invariant-specific transition bound. The exact gate does not imply that such a bounded-mass field exists. Smearing a downstream acceptance requirement may increase its total mass; recursively assuming the old mass budget persists is invalid without proof.

For a compositional proof, pin the following five objects explicitly:

1. Whether the state is before or after the boundary Devil announcement.
2. The complete post-announcement continuation family P_j, including every later timestamp's preloads.
3. The implication from the proposed terminal inequality to safe robust acceptance.
4. The response to each intermediate lethal time and each adaptive new announcement.
5. The actual initial state's membership and the final stage's harmless continuation.

These are proof obligations, not an assertion that any presently proposed potential satisfies them.

## 6. Strength of the desired all-finite-sets theorem

The statement

for every finite known D, there exists an online Angel strategy winning against every adaptive Devil whose time coordinates lie in D

would resolve the original unrestricted conjecture. Indeed, for any finite horizon H take D={1,…,H}. Announcements at times greater than H have no effect before H and can be represented by ineffective actions. Thus the theorem gives exact online wins for every finite horizon. The accepted finite-Angel-choice compactness argument then supplies one infinite strategy against unrestricted timestamps.

The converse is immediate by restricting an unrestricted winning strategy. Therefore the universal finite-known-allowed-set theorem is equivalent in strength to the full target; an induction claiming it must genuinely supply the robust terminal gate above. Theorems for one, two, or any fixed number of deadlines do not alone establish that universal induction.
