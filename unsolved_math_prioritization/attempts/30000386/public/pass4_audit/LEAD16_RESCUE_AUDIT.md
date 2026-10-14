# Independent audit: chronology-triggered maximum-lead-sixteen rescue

## Disposition and pin

**Accepted.** The frozen candidate constructs a deterministic online strategy
that survives forever from the empty initial history when every effective
announcement has lead at most sixteen. The full unrestricted game remains
unresolved. This audit is part of shared PASS4, not a new proof pass.

Audited input: `pass4_invariant/LEAD16_RESCUE.md`.
SHA256: `fbcf3b299034bff78871b5b61b77f74f873f0a7cd9b963863c0c26a613f09438`.

The audit below is analytic and does not rely on a search or a replay program.
All choices are made after the applicable previously announced bombs are known;
the Devil's next announcement remains universally quantified.

## 1. Global small-set geometry

Write N(Q)=Q+{-1,0,1}^2. For a finite nonempty set Q with k points,
r occupied rows and c occupied columns, first expand horizontally and then
vertically. This gives

|N(Q)| >= k+2r+2(c+2) >= k+4 sqrt(k)+4.

The first expansion has at least c+2 occupied columns, even when some occupied
columns or rows are nonconsecutive. If Q=A8(B), every N(q) has at most one point
outside B. Assign each missing point of N(Q) to any containing N(q). The
assignment is injective: two distinct missing points cannot both be contained
in the same N(q). Consequently |N(Q)\B|<=k and |B|>=4 sqrt(k)+4.

This proves |A8(B)|<=1 at |B|=8 and, using the strict quadratic inequality and
integrality, |A8(B)|<=|B|-8 for 9<=|B|<=15. The exceptional endpoint b=16 is
also correctly handled. If k=9, the union bound |N(Q)|<=25 forces r+c<=6,
while rc>=9 forces r=c=3. All nine row-column pairs occur. Each one-dimensional
three-point expansion has size at least five, so their product being at most
25 makes both exactly five and the underlying coordinate sets consecutive.
Thus Q is a full 3 by 3 square. Its four corner neighborhoods cover its full
5 by 5 neighborhood, and each can omit at most one point of B. That would
require at least 21 points of B, contradicting b=16. Hence k<=8.

No local confinement of B or of A8(B) was assumed. This global form is needed
in the next lemma and is justified by the proof.

## 2. Exact three-move adversarial quantifiers

Fix a first position q at time s and preloaded sets B1,B2 at s+1,s+2.
After the first new announcement, the remaining two-move game is losing
exactly when

N(q) is contained in B1' union A8(B2').

Indeed, a safe second position outside A8(B2') has at least two terminal
neighbors unbombed, and the subsequent single announcement cannot cover both.
If no such second position exists, every safe second position has at most one
unbombed terminal neighbor, which the adaptive second announcement can cover.
This proves the equivalence with the correct move-then-announcement timing.

With D=B1 union A8(B2), a first update at s+1 gives bad first positions A8(D).
A first update at s+2 gives exactly

union over w of E(B1 union A8(B2 union {w})).

In particular, the candidate does not mistakenly replace newly created A8
centers by the old A8(B2). Updates with irrelevant time coordinates are
covered by E(D), already a subset of A8(D).

I independently checked every cardinality case under m+b<=15:

- b<=6: augmented terminal sets have size at most seven, and all bad first
  positions lie in A8(B1), of size at most seven.
- b=7: m<=8. The first kind contributes at most one center. Every augmented
  A8 center must contain all seven original terminal sites. If such a
  neighborhood exists, those sites span three rows and three columns, so its
  center is uniquely determined independently of w. Thus the entire union in
  the second kind is contained in E(B1 union {v}), of size at most one.
- b=8: m<=7 and the old and augmented A8 sets each have size at most one.
  The first kind contributes at most one; the second kind is empty because
  its argument has at most eight points.
- 9<=b<=15: |D|<=7. The first kind is empty; every augmented terminal A8 set
  has size at most b-7, so the second kind also has an argument of size at
  most eight and is empty.

There are at most seven bad first positions globally. Removing them and the
at most one current lethal position from the nine candidate moves leaves a
legal first move. The choices on the next two moves respond to the actual
new announcements. Other initial timestamps do not kill on these three moves.
The lemma is a genuine three-move strategy, including its first death check.

## 3. Trigger chronology and reset

Before move s, a pending pair at s+1 or s+2 in the lead-sixteen game must have
been announced in one of the fifteen rounds s-15,...,s-1. Fifteen distinct
pairs at those times therefore occupy all fifteen announcement slots, without
duplicates or irrelevant announcements in that interval. An older announcement
can still be lethal at s only if it was made at s-16. There is at most one
such pair. No older pair can remain future-pending. This verifies every rescue
hypothesis, including the absence of other future preloads needed for reset.

After moves s,s+1,s+2, all old trigger pairs have expired. Once the Devil has
also announced in round s+2, only the three announcements in rounds s,s+1,s+2
can remain pending. Thus the next ordinary state, before move s+3, has at most
three pending pairs and satisfies the guard. The endpoint announcement is not
forgotten in this count.

## 4. No first ordinary failure

An ordinary guard permits at most eight current lethal sites in the current
3 by 3 neighborhood. If no ordinary admissible move exists, let Q be the
nonempty set of immediately safe candidates. Every N(q), q in Q, contains
at least eight next-time bombs. The local expansion/missing-point argument
gives |B_next|>=|Q|+7. Together with 9-|Q| current forbidden sites, this
requires at least sixteen distinct current/next spacetime pairs.

The lead bound supplies only sixteen preceding announcement slots, so equality
forces every slot n-16,...,n-1 to target n or n+1. In particular the first
fifteen were already known before move n-1. If that move was ordinary, its
trigger necessarily started a rescue and move n is inside it. If it was
inside a rescue, move n is either still inside or is immediately after its
reset, which leaves at most three pending pairs. Neither permits the alleged
ordinary failure. The required sixteen preceding rounds also exclude an
initial-time exception.

Thus every requested ordinary move exists, preserves the guard after the
next announcement, and every rescue safely returns to guarded ordinary mode.
This establishes the claimed infinite online strategy from the empty history.
No assertion that every existentially reachable preload is forceable is used.

## 5. Boundary of acceptance

The exact sixteen-slot saturation is essential to this proof. Extra older
future bombs at a larger maximum lead would invalidate the clean trigger/reset
argument unless separately accounted for. The accepted statement is H=16,
not arbitrary H, not a uniform-radius tracker, and not the unrestricted game.
