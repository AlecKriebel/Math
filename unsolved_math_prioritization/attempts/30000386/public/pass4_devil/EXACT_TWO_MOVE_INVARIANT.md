# Exact two-move viability is an invariant with at most sixteen pending bombs

## Result and scope

**Theorem.** In the exact two-dimensional Time-Bomb game, the Angel wins forever against every adaptive Devil whose effective announcement lead is at most 16.

The proof maintains exact two-move online viability. It does not use an arbitrary preloaded sixteen-bomb trap as a reachable forcing strategy. It proves a stronger state implication: for every state containing at most 16 pending pairs, viability for the next two moves implies viability for the next three moves.

This is not an arbitrary-H or unrestricted-game theorem. All sets below contain distinct spatial sites at the specified time; the same site at two times counts twice.

## 1. Geometry

Write N(x)=x+{−1,0,1}². For finite B define

    A_j(B)={x: |N(x)∩B|≥j}.

### Lemma 1: small eighth-neighbor sets

If |B|<8, then A_8(B) is empty. If |B|=8, its cardinality is at most 1. For 9≤|B|≤16,

    |A_8(B)|≤|B|−8.

**Proof.** Put Q=A_8(B), k=|Q|, and assume k>0. Let r,c be the numbers of occupied rows and columns of Q. Horizontal expansion by one adds at least two sites in each occupied row; subsequent vertical expansion adds at least two in each of at least c+2 occupied columns. Therefore

    |N(Q)|≥k+2r+2c+4.

Every neighborhood N(q), q∈Q, misses at most one B-point. Consequently the number of points in N(Q)\B is at most k, and hence

    |B|≥2r+2c+4≥4sqrt(k)+4,

where rc≥k was used. For |B|=8 this gives k≤1. For 9≤|B|≤15, the integer bound k≤(|B|−4)²/16 yields k≤|B|−8.

For |B|=16 it leaves only the exceptional possibility k=9. That possibility forces r=c=3 and Q to contain every point in the Cartesian product of its three occupied rows and columns. Select three corners of that product. Their three 3×3 neighborhoods have union size at least 21: each coordinate span between extreme rows/columns is at least two, and inclusion-exclusion gives this lower bound. Since the three neighborhoods together miss at most three B-points, |B|≥18, a contradiction. Thus k≤8. ∎

### Lemma 2: small seventh-neighbor and common-center sets

- If |B|=7, then |A_7(B)|≤1.
- If |B|=8, then |A_7(B)|≤2.
- Four distinct points have at most four common king-neighbors.
- Five or six distinct points have at most two common king-neighbors.

**Proof.** Two distinct 3×3 neighborhoods intersect in at most six sites, proving the first statement. If three distinct neighborhoods each contain at least seven of eight B-sites, their common intersection contains at least8−3=5 B-sites. But three distinct 3×3 neighborhoods intersect in at most four sites: either their centers vary in both coordinates, or three centers in one row/column span at least two. This proves the second statement.

The set of common neighbors of B is an integer rectangle with side lengths max(0,3−span_x(B)) and max(0,3−span_y(B)). Four distinct points cannot give more than four common neighbors. Five or six points cannot fit in a 2×2 rectangle; if their common-neighbor set is nonempty, the displayed product is therefore at most two. ∎

## 2. What a two-move losing preload of size at most seventeen can look like

Consider two successive future moves, with already announced spatial sets U at the first time and V at the second. One further announcement is permitted between those moves. From a current center x, let

    Q=N(x)\U.

If Q is empty, the first move is already impossible. If Q is nonempty, loss within two moves occurs exactly when

    Q⊆A_8(V).                                                (1)

This is because, after the first move to q, a Devil addition can fill the last missing second-time neighbor exactly when at least eight are already bombed.

**Lemma 3.** If (1) holds, Q is nonempty, and |U|+|V|≤17, then |Q| is 1,2, or 4. The corresponding necessary count bounds are

    |Q|=1: |U|≥8, |V|≥8;
    |Q|=2: |U|≥7, |V|≥10;
    |Q|=4: |U|≥5, |V|≥12.                                  (2)

In particular, a nonimmediate two-move losing preload needs at least 16 pairs.

**Proof.** Write k=|Q|. Necessarily |U|≥9−k. If k=1, |V|≥8. If k=2, the two neighborhoods have union size at least 12 and miss at most two V-sites, giving |V|≥10.

For k=3 their neighborhood union has size at least 15. Indeed, a pair whose centers differ by at least two in one coordinate already has such a union; otherwise the three centers occupy three corners of a 2×2 square, with union size 15. Thus |V|≥12, giving total at least 18.

For k=4 there are two centers differing in both coordinates, whose neighborhoods have union size at least 14. This gives |V|≥12.

For k=5 the row/column expansion argument of Lemma 1 gives |V|≥2r+2c+4≥14, giving total at least 18.

For k=6, if Q occupies three rows and three columns, the same bound gives |V|≥16. Otherwise Q is a full 2×3 or 3×2 Cartesian rectangle. The four corner neighborhoods cover N(Q), whose size is at least 20, and miss at most four V-sites; again |V|≥16.

For k=7, Q occupies three rows and columns, so |V|≥16 and the total is at least 18. For k=8 or 9, Q contains three corners of N(x). Their neighborhoods have union size 21 and miss at most three V-sites, so |V|≥18. These cases also exceed total 17. The surviving possibilities and their bounds are exactly (2). ∎

## 3. Centers that one new announcement can make two-move losing

For finite B,C, let D(B,C) be the set of centers x from which the next two moves can be made losing by one new announcement added to B or C, or by an irrelevant announcement. Here B concerns the first of those two moves and C the second. Thus the new announcement occurs before either of the two moves; another adaptive announcement will still be available between them.

**Lemma 4.**

    |B|+|C|≤14  ⇒  D(B,C)=A_8(B);
    |B|+|C|≤15  ⇒  |D(B,C)|≤7;
    |B|+|C|≤16  ⇒  |D(B,C)|≤8.

For the first conclusion, only an immediate nine-neighbor trap can be completed: after adding one pair, fewer than16 pairs remain, which Lemma 3 excludes for a nonimmediate loss. Such an immediate trap is possible exactly at A_8(B).

For the other conclusions, write b=|B|, c=|C|. Any nonimmediate trap after the new announcement has at most 17 pairs, so Lemma 3 applies. The following necessary inclusions exhaust all possibilities when b+c≤16:

- b≥9: D(B,C)⊆A_8(B). Here c≤7; only the first case of (2) can arise beyond an immediate trap, and it still requires at least eight existing B-sites around the center.
- b=8: D(B,C)⊆A_7(B), of size at most two.
- b=7: D(B,C)⊆A_7(B), of size at most one.
- b=6: only the second case of (2) can arise, by adding to B with c=10. Every B-site must already lie in N(x), so there are at most two such centers.
- b=5: only the third case of (2) can arise, by adding to C with c=11. There are at most two common centers of B.
- b=4: only the third case of (2) can arise, by adding to B with c=12. There are at most four common centers of B.
- b≤3: no immediate or nonimmediate trap is possible.

The first row and Lemma 1 give at most eight centers; every other row gives at most four. This proves the16-pair bound.

If b+c≤15, the b≥9 row gives at most b−8≤7. For b=8 the only nonimmediate possibility adds to C with c=7, and its centers already lie in A_8(B), of size at most one. For b=7 the only possibility adds to B with c=8, again leaving at most one common center. For b≤6 there is no nonimmediate possibility. This proves the15-pair bound. ∎

## 4. The exact viability implication

At a state immediately before an Angel move, let A,B,C be the pending sites for the current, next, and following times. Other later pairs may be present. Let W_r mean that the Angel has a strategy surviving the next r moves against every intervening adaptive announcement.

For W_2, the exact test is

    there exists q∈N(a)\A with |N(q)∩B|≤7.                  (3)

Indeed, the intervening Devil can add one next-time bomb. For W_3, a sufficient and exact test is to choose a current-safe q outside D(B,C).

**Theorem 5.** If the complete pending set has at most 16 pairs, then

    W_2 ⇒ W_3.

**Proof.** Put m=|A|, b=|B|, c=|C|; then m+b+c≤16.

If m=0, Lemma 4 leaves at most eight dangerous centers among the nine moves. If m=1, the future pair has size at most 15, leaving at most seven dangerous centers; together with the one current bomb they still exclude at most eight moves.

Suppose m≥2. Then b+c≤14 and D(B,C)=A_8(B). If b≥9, Lemma 1 gives

    m+|D(B,C)|≤m+b−8≤8.

If b≤7 there is no danger center, and W_2 already ensures a current-safe move. If b=8, there is at most one danger center. When m≤7 the total exclusions are at most eight. The only remaining case is m=b=8,c=0. If all nine current choices were excluded by A together with D(B,C), condition (3) would fail, contradicting W_2. Thus a current-safe q outside D always exists. ∎

## 5. Infinite bounded-lead strategy

Start with no pending bombs, which satisfies W_2. Before each Angel move, choose a safe q outside D(B,C), for example the first under a fixed ordering. Theorem 5 says such a move exists. By the definition of D, after every possible Devil announcement the new state again satisfies W_2.

With maximum effective lead 16, every still-future announced pair was announced within the preceding sixteen rounds. Hence there are always at most 16 distinct pending pairs; past/current-time announcements and repetitions do not increase this number. Theorem 5 can therefore be reapplied indefinitely. Every selected current move is safe, proving the theorem.

The controller uses the exact next-three-layer transition test, rather than blindly extending the old two-layer density guard. It can act on the third layer before the old policy's sixteen-pair trap closes.

## 6. General recurrence boundary

More generally, if for some H and r one proves W_r⇒W_(r+1) on every state with at most H pending pairs, then the same argument gives infinite survival for maximum lead H. This is a structural invariant criterion, not a claim that the implication holds for all H or some uniformly chosen r. The present proof establishes only (H,r)=(16,2).

A preloaded W_2-losing sixteen-pair configuration is outside the maintained invariant. Its existence does not contradict the theorem and does not establish that a legal Devil can force it from the empty initial state.
