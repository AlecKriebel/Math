# Shared PASS1: online survival reductions and partial results

## Status and scope

The full Time-Bomb conjecture is **not resolved here**. These results use exactly the shared contract: Angel moves first by one king step, including staying; a surviving round permits one adaptive Devil announcement; several announcements may have the same future detonation time. Results below are authored arguments, not claims of novelty or current literature status.

Contract SHA-256: `1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c`.

The positive result is one explicitly defined online strategy surviving through round 17 against every legal adaptive Devil. The general reduction proves that winning all finite horizons would imply one infinite winning strategy, even though Devil choices are unbounded. A separate one-dimensional counterexample defeats a simple proposed restriction of the Angel's motion.

## 1. Exact finite-horizon recursion

Use a state immediately before an Angel move. Translate the current Angel position to the origin and its current time to zero. Let B be the finite set of still-future announced pairs (p,k), with p in Z² and integer k≥1. Repeated announcements have the same effect as one, and expired announcements can be discarded. Put M={−1,0,1}².

After choosing δ in M, the move survives exactly when (δ,1) is not in B. The remaining old bombs become

Sδ(B) = { (p−δ,k−1) : (p,k) in B, k≥2 }.

The Devil can then add any one pair q in Z²×{1,2,...}, or make an irrelevant announcement, represented by the symbol ⊥. Let B+⊥ mean B. Define W₀(B)=true, and for h≥1 define

W_h(B) ⇔ there exists δ in M such that (δ,1) is not in B and, for every legal q or ⊥, W_(h−1)(Sδ(B)+q).

This is the exact online game recursion. The existential choice precedes the universal announcement choice at every round. Induction on h proves that W_h(B) is equivalent to having a history-dependent strategy surviving the next h moves from B. In particular, the original empty-board horizon-h problem is W_h(∅).

### Finite-cone reduction

For h remaining moves, retain only

C_h = { (p,k) : 1≤k≤h, ||p||∞≤k }.

A discarded pair cannot be reached before the horizon: every legal path from the current location has displacement at most k at time k. Once a bomb is outside this forward cone, a later legal move cannot bring it back into the descendant cone, by the triangle inequality. Thus W_h(B) depends only on B∩C_h.

After the Angel move the Devil's universally quantified choices can be reduced exactly to C_(h−1)∪{⊥}, followed by the same truncation of old bombs. All other announcements have identical effects through the horizon. Therefore each fixed horizon is an exact finite game, not a bounded approximation to the relevant spatial choices. Its cone size is

|C_h| = sum_(k=1)^h (2k+1)² = 4h(h+1)(h+2)/3+h.

The finite-state reduction makes no assumption that there is at most one bomb per detonation time.

## 2. Finite horizons imply an infinite online strategy

Let W_h also denote the set of finite states satisfying the preceding predicate. These sets are nested: W_(h+1)⊆W_h. Put W_∞=intersection_(h≥0) W_h.

For B in W_∞, let A_h(B) be the Angel moves δ that are safe immediately and have every legal Devil successor in W_h. Membership B in W_(h+1) says that A_h(B) is nonempty. Nesting of the W_h implies A_(h+1)(B)⊆A_h(B). Each A_h(B) is a subset of the same nine-element set M. Hence their intersection is nonempty.

Choose, for example, the first move in that intersection under a fixed ordering of M. Every Devil successor is then again in W_∞. Repeat this state-based rule. Induction shows that the Angel never takes a fatal move, against every adaptive Devil strategy.

Consequently:

- If W_h(∅) holds for every finite h, the full conjecture follows.
- If the Devil wins the full game from the empty state, it wins some finite-horizon game from that state.

The second statement follows contrapositively from the first, or directly by finite-horizon determinacy. This argument does **not** replace the online quantifiers by the existence of a path against a fixed completed bomb schedule. The finite set of Angel moves, not finite branching of Devil moves, is the key compactness input.

## 3. A geometric covering lemma

For x in Z² write N(x)=x+{−1,0,1}². Suppose ∅≠Q⊆N(a) and B⊆Z² is finite, with

|B∩N(q)|≥8 for every q in Q.

Then

|B|≥|Q|+7.

Here is an elementary expansion proof, supplied by the independent finite-game audit. Translate a to zero, write k=|Q|, and let r and c be the numbers of occupied rows and columns of Q. Thus 1≤r,c≤3 and k≤rc.

Let U=Q+{−1,0,1}² be the union of the neighborhoods N(q). Expanding Q horizontally adds at least two points in each occupied row, so the horizontally expanded set has at least k+2r points. It occupies at least c+2 columns. Expanding it vertically therefore adds at least 2(c+2) points. Consequently

|U|≥k+2r+2c+4.

For 1≤r,c≤3 one has rc≤2r+2c−3: equivalently, (r−2)(c−2)≤1. Therefore k≤2r+2c−3 and

|U|≥2k+7.

Every N(q) is missing at most one point of B. For each point of U\B choose a center q whose neighborhood contains that point. No center can be chosen for two different missing points, because that would give two holes in its neighborhood. This is an injection from U\B into Q. Hence |U\B|≤k, and

|B|≥|B∩U|=|U|−|U\B|≥(2k+7)−k=k+7.

This proves the lemma. The independent audit also checked the earlier elementary case-split proof; the expansion proof replaces it only for clarity.

## 4. An online strategy surviving 17 rounds

At the start of round n let a be the current location. Let A be the set of positions already announced to explode at time n, and let B be the positions already announced to explode at time n+1. Maintain the invariant that at most eight points of N(a) belong to A.

The invariant holds initially. Suppose n≤16, so at most n−1≤15 announcements have been made altogether. The legal next locations form the nonempty set Q=N(a)\A. The geometric lemma shows that some q in Q satisfies |B∩N(q)|≤7. Indeed, if all q failed, the lemma would give |B|≥|Q|+7, while |A|≥9−|Q|. Because A and B concern different times, they require at least |A|+|B|≥16 distinct earlier announcements, a contradiction.

The strategy chooses the first such q under a fixed ordering. It is a safe move. The Devil can then add at most one new bomb at time n+1, so at most eight announced next-time bombs lie in N(q). This reestablishes the invariant for round n+1.

Apply the rule for rounds 1 through 16. At round 17 the invariant leaves at least one safe next location, so the Angel survives that round as well. Every choice uses only already observed announcements; arbitrary adaptive choices and repeated detonation times are included.

A slightly more general statement is immediate: the same local rule survives forever against any restricted Devil for which, before every Angel move n, the number of distinct already-announced pairs with detonation times n or n+1 is at most 15. This extra restriction is **not** part of the original conjecture.

### Exact obstruction to this local invariant

The threshold 16 cannot be improved for arbitrary states with an immediately legal move. Choose q in N(a). Announce bombs at time n on the other eight points of N(a), and announce bombs at time n+1 on eight of the nine points of N(q). This uses 16 prior pairs. The Angel's only safe move at time n is q; the Devil then announces the ninth point of N(q) for time n+1 and kills the Angel on its next move.

This is a valid two-move trap **from that preloaded state**, not a proof that a Devil can force the unrestricted initial game into it. Avoiding such states before they form is the unresolved step for this particular invariant.

The survival-17 theorem and this geometric mechanism were independently derived in the Devil-side lane during the same shared pass. They are one shared result, not two distinct advances or an independent additional pass.

## 5. A one-dimensional obstruction to reducing the motion

Consider instead the line Z with legal moves −1,0,1, with the same round order and announcement budget. Restrict the Devil to the single detonation time 6. The Devil can force a loss on move 6.

After the first Angel move a₁, announce (a₁,6). Translation makes the remaining state h=5, B={0}, where h is the number of moves left and B records terminal-bomb positions relative to the current location. The file `terminal_1d_horizon6_certificate.json` supplies a finite strategy for every subsequent Angel choice. It contains eight canonical states and one lethal terminal state, B={−1,0,1}.

Reflection and translation are the only symmetries used. At each state all three possible Angel moves appear, followed by one explicit Devil announcement. Positions too distant to reach by time 6 are discarded; such positions cannot later re-enter the remaining cone. The certificate verifier checks every edge without invoking the minimax solver, and checks that all terminal moves are bombed. The output is retained in `terminal_1d_horizon6_replay.json`.

The exact terminal-game solver also finds that horizons 1 through 5 are Angel wins. Its recurrence is the one-dimensional specialization of Section 1 with all bombs at the one terminal time. It omits an explicit irrelevant-announcement option: this is sound because adding a forbidden pair cannot improve the Angel’s winning value, so winning against every in-cone addition implies winning against a null announcement. The terminal h=1 case handles the empty successor cone. The loss certificate alone is sufficient for the stated obstruction.

This counterexample applies to Angel policies restricted to a fixed lattice line on which the legal positions have exactly those three one-dimensional moves. It also applies if one coordinate is a deterministic, known prescribed function of time and the other coordinate has only the three line moves: the Devil attaches the prescribed coordinate at time 6 to each one-dimensional bomb. This extension does not assert knowledge of an unknown privately randomized coordinate. It does not apply to an unrestricted two-dimensional Angel.

## 6. Remaining mathematical gap

Neither the finite-horizon reduction nor survival through 17 proves W_h(∅) for all h. The geometric strategy only protects against two consecutive explosion layers; a Devil can eventually have 16 or more earlier announcements relevant to those layers. No argument here prevents the formation of all larger multitime trap configurations. No infinite invariant, winning strategy, or reachable full-game Devil trap is asserted.

The one-dimensional loss also shows why an apparent simplification to a predetermined eastward (or any fixed-coordinate) path is unsafe. Ordinary permanent-deletion results with a larger move set and offline path existence do not fill the gap.

## Verification note

The independent finite-game audit accepted the exact recurrence, cone count, compactness argument, survival-17 timing, and the preloaded 16-bomb obstruction. It also replayed the one-dimensional strategy on all 729 complete six-move Angel words using absolute coordinates, retaining all actual bombs and importing none of the construction code. All words lost at move 6 and all eight certificate states were reached. The local verifier additionally rejects six malformed-certificate negative controls.
