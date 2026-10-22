# Independent lead-sixteen audit and a continuous-invariant proof

Status: PASS4 independent acceptance of the bounded-lead result in ../pass4_invariant/LEAD16_RESCUE.md, SHA256 fbcf3b299034bff78871b5b61b77f74f873f0a7cd9b963863c0c26a613f09438. The alternative proof below establishes the same result, not a second advance. The unrestricted conjecture remains unresolved.

## 1. Audit of the supplied rescue proof

The small-set A8 bound is valid. The union expansion and missing-point injection imply |B|>=4 sqrt(|A8(B)|)+4. For 9<=|B|<=15 the strict integer bound follows from (b-8)(b-16)<0. At b=16, the possible equality with nine bad centers forces a consecutive side-three square; its four corner neighborhoods cover twenty-five sites with at most four missing, requiring twenty-one bombs and contradicting b=16.

The four cases in the three-move rescue are also valid. In particular, seven old terminal points contained in a side-three square have a unique possible center because they occupy all three coordinate values in both directions. The b=8 and b>=9 cases use the augmented A8 bound with the correct one-announcement reserve. Every lethal move, including the first rescue move, is protected.

The trigger chronology accounts for exactly the fifteen announcement rounds immediately preceding the rescue. At most one older announcement can be currently lethal. All old future bombs belong to the two trigger layers, so after the rescue only its three newly made announcements can remain pending. The ordinary-failure contradiction uses the trigger at the preceding move and correctly handles a rescue's final move. No reachability assumption about a preloaded trap is used.

No correction requested. This is an infinite online win for maximum announcement lead sixteen from the empty history.

## 2. Two elementary local bounds

Write N(a)=a+{-1,0,1}^2. We use the accepted local lemma: if Q is a nonempty subset of N(a) and every q in Q has at least eight neighbors in B, then |B|>=|Q|+7.

A stronger observation is useful when |Q|>=7. Such a Q occupies three rows and three columns. Horizontal and vertical expansion gives

    |N(Q)|>=|Q|+16.

At most |Q| points of this union can be missing from B, by assigning a missing point to a containing neighborhood. Hence |B|>=16.

If Q=N(a), its four corner neighborhoods cover the full side-five square N(Q). Each is missing at most one point of B, so at most four of the twenty-five sites are missing. Thus |B|>=21.

## 3. Three robust first choices for fifteen future preloads

Suppose the known sets at the next two times are A and B with |A|+|B|=15. Call q robust if after every single new announcement at either of those two times, the next two Angel moves are survivable from q. Equivalently, writing A',B' for the augmented sets, there must be a point r in N(q) minus A' with |B' intersect N(r)|<=7. A subsequent announcement can then cover at most one further terminal neighbor.

**Lemma.** Among N(a), at least three choices q are robust. Each of the choices constructed below also has at most seven known A-neighbors.

If 2<=|A|<=7, every q has at most seven A-neighbors. The centers q for which all A-points lie in N(q) form the intersection of the neighborhoods of the A-points. Two distinct points have at most six common king-neighbor centers. Therefore at least three q in N(a) have an A-point outside N(q).

If 8<=|A|<=15, at most six q in N(a) can have eight or more A-neighbors. Otherwise seven such centers would force |A|>=16 by Section 2. Thus at least three q have at most seven A-neighbors; since |A|>=8, each also has an A-point outside N(q).

For all these q, the permanently outside old A-point remains outside after a new announcement. Consequently

    |A' intersect N(q)|<=8,
    |A' intersect N(q)|+|B'|<=15.

The accepted local lemma then supplies a safe r with at most seven B'-neighbors, proving robustness.

Finally suppose |A|<=1. After any new announcement, |A'|<=2 and |A'|+|B'|<=16. If |A'|>=1, then at least seven positions of N(q) are not in A', while |B'|<=15. The first stronger bound in Section 2 guarantees that one of those positions has at most seven B'-neighbors. If A' is empty, all nine positions are available and |B'|<=16<21; the four-corner bound gives the same conclusion. Thus every q is robust in this final case.

## 4. Continuous two-layer invariant

For the exact maximum-lead-sixteen game, maintain before each move n the property I_n:

    There is a q in N(a_(n-1)) avoiding all known time-n bombs
    and having at most seven known time-(n+1) bombs in N(q).

This is the exact two-move safety property with one new announcement between the moves. It holds initially.

Let A,B be the known bomb sets at times n+1,n+2, and put F=|A|+|B|. A bomb at either time was announced in rounds n-15,...,n-1, so F<=15.

- If F<=14, choose any move given by I_n. It is safe now, and at most seven A-neighbors surround the new position. After the next announcement there are at most eight such neighbors, and the new A/B total is at most fifteen. The local geometric lemma therefore reestablishes I_(n+1).
- If F=15, the chronology leaves at most one known current-time bomb: all still-current/future pairs have distinct witnesses within the sixteen rounds n-16,...,n-1, and fifteen are already used by A and B. The robust-choice lemma supplies at least three possible q. Choose one avoiding the at-most-one current-time bomb. It is safe now, and its robustness gives I_(n+1) after every Devil announcement.

This defines an infinite online strategy with continuous invariant preservation; it needs no rescue mode or reset. It uses the same additional next-two-layer information as the accepted rescue result, and responds before the local lead-sixteen trap can form.

## 5. Boundary

For larger maximum lead H, F may exceed fifteen and the number of currently lethal sites can exceed one. The robust-choice lemma and chronology count no longer suffice. This proof does not infer arbitrary finite-H survival or claim that all full-history traps are unreachable.
