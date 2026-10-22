# Exact fixed-point criterion and a scalable fixed-depth obstruction

Shared final PASS5. These are structural statements and an obstruction to a
particular universal invariant scheme. They do not settle the full Time-Bomb
game and do not introduce another fixed-H search.

## 1. Exact bounded-lead arena and notation

Fix an integer H>=1. A state is taken immediately after a Devil announcement,
with the Angel's position translated to zero. The initial state at time zero
is the empty set, without a fictitious announcement. Write

C_H={(q,t): q in Z^2, 1<=t<=H, ||q||_infinity<=t}.

The exact normalized arena K_H consists of subsets B of C_H satisfying

#{(q,t) in B: t>=j} <= H-j+1,    1<=j<=H.

The previously accepted proof establishes both closure under all legal moves
and existential reachability of every such B. Existential reachability is
not adversarial forceability from the empty state.

At B, the Angel first chooses delta in {-1,0,1}^2. It dies immediately if
(delta,1) belongs to B. For any safe delta, shift unexpired old pairs by
(q,t) -> (q-delta,t-1), discard permanently unreachable pairs, and let the
Devil add any one pair of C_H or a null action. Call the resulting state
T_H(B,delta,d). The Devil's action is chosen after seeing delta.

For X subset K_H, define the robust predecessor

F_H(X)={B: there is a safe delta such that, for every Devil action d,
                  T_H(B,delta,d) belongs to X}.

Let W_0^H=K_H and W_(r+1)^H=F_H(W_r^H). Then W_r^H is exactly the set of
states from which the Angel can survive its next r moves against all adaptive
bounded-lead Devils. Every intermediate death check is represented in F_H;
no assertion refers only to the final position.

## 2. Necessary and sufficient invariant criteria

The following statements are equivalent for fixed H:

1. The Angel wins forever from the empty state in the lead-H game.
2. The empty state belongs to W_infinity^H=intersection_r W_r^H.
3. There is a subset Y_H of K_H containing the empty state such that
   Y_H is a subset of F_H(Y_H).
4. For some r, the empty state belongs to W_r^H and
   W_r^H=W_(r+1)^H.

The sets W_r^H descend and stabilize because K_H is finite. Their stable
value is a fixed point and hence a valid Y_H. Conversely, an invariant Y_H
supplies a legal move at every state whose every adaptive Devil successor
remains in Y_H. Choosing one such move at each state gives a positional
infinite strategy. An invariant also lies in every W_r^H by induction.
These facts prove all the equivalences.

Two qualifications prevent circular or excessive uses of this criterion:

- Stabilization at some depth is automatic for every fixed H, whether the
  empty state wins or loses. It proves survival only if the empty state is
  still present at that depth. The base membership cannot be omitted.
- Proving W_r implies W_(r+1) on every arbitrary state with at most H pending
  pairs is a sufficient stronger method, provided the empty base is proved.
  It is not necessary. Such arbitrary states need not satisfy the lag bound,
  cone, or tail-age constraints, and even in K_H a smaller robust invariant
  Y_H can exclude strategically avoidable losing preloads.

Thus the accepted H=16, r=2 implication is a useful sufficient certificate.
It is not a necessary form for an arbitrary-H proof. A residual-state scheme
may use an H-dependent depth, a stricter family Y_H, or controller memory,
but it must establish actual robust closure and initial membership. Memory
can be included in the state during a construction; the exact finite arena
still guarantees that some positional winning strategy exists if it succeeds.

By the accepted all-finite-leads reduction, the unrestricted original game
is Angel-winning if and only if statement 1 holds for every finite H. No
compatibility or quantitative uniformity between the different H-strategies
is needed. This does not remove the need to prove each empty-state claim.

## 3. Terminal-carpet obstruction to one fixed viability depth

Fix k>=1 and put

M_k=(2k+3)^2,
H_k=M_k+k,
B_k={(q,k+1): ||q||_infinity<=k+1}.

The state B_k belongs to K_H for every H>=H_k. It lies inside the cone,
contains M_k distinct pairs, and its tail count is M_k for 1<=j<=k+1
and zero afterward. The strongest nonzero tail constraint is at j=k+1,
where it reads M_k<=H-k. This is exactly the asserted H threshold.

No old pair in B_k can affect the first k moves. Consequently

B_k belongs to W_k^H  if and only if  empty belongs to W_k^H.       (1)

This is equality of finite decision games after deleting irrelevant old
pairs, not an offline-path argument. The bounded-lead Devil has the same
one-announcement action domain and sees each actual Angel move in both
games. A strategy in either game can internally supply or suppress the fixed
old carpet while simulating the other history. Its effect is outside the
k-move horizon, so every death check through that horizon is unchanged.

On move k+1, every legal position reachable from the present origin lies
in the radius-(k+1) square. Every such position has an old bomb at time k+1.
Therefore

B_k does not belong to W_(k+1)^H.                              (2)

The Devil need only make irrelevant announcements; the terminal death is
unavoidable, regardless of any earlier adaptive choices or earlier death.

Equations (1)--(2) prove the exact dichotomy:

- If empty is not in W_k^H, a proposed W_k^H invariant cannot be initialized.
- If empty is in W_k^H, W_k^H is not a subset of W_(k+1)^H, because B_k is
  an explicit counterexample.

Hence no single fixed k can establish all bounded-lead games by universal
closure of the full W_k^H family. For any H and k where this scheme works,
one necessarily has H<(2k+3)^2+k=4k^2+13k+9. An H-dependent depth may grow
at least on the square-root scale; this is only a necessary restriction on
this scheme, not a sufficient depth or an obstruction to a smaller invariant.

### Legal realization of the obstruction state

To make legality explicit, start at the empty state and have the Angel stay
at zero for H rounds. Enumerate the M_k carpet sites as q_1,...,q_M. Announce
(q_i,H+k+1) in round r_i=H-i+1. Its lead is k+i, which lies between one and
H because i<=M_k and H>=M_k+k. Use current-time null announcements in unused
rounds. All carpet detonations occur after H, so this preparation is a legal
surviving history. At time H its normalized pending state is exactly B_k.

This realization requires a cooperating preparation path. It is not a Devil
strategy forcing B_k against an Angel that may move elsewhere. The example
refutes the universal closure premise, not empty-state survival for that H.

## 4. Canonical form of a genuine negative certificate

If the empty state is outside W_infinity^H for some H, define the removal
rank of each losing state B by

rho(B)=min{r>=1: B is not in W_r^H}.

For rho(B)=1, every Angel move is immediately lethal. For rho(B)>1, every
safe Angel move delta has a legal Devil reply d for which

rho(T_H(B,delta,d)) <= rho(B)-1.

This follows directly from B not belonging to F_H(W_(rho(B)-1)^H).
A finite certificate can therefore consist of normalized states with positive
integer ranks, rooted at the empty state, and for each safe Angel move a
legal Devil action and a referenced smaller-rank successor. Every current
lethal move and every shifted/deleted/added pair is checked exactly. At rank
one the certificate checks all nine immediate deaths. Strict rank decrease
then proves a finite loss on every branch, including adaptive Angel play.
The certificate can be represented as a finite directed acyclic graph.

Conversely, any such well-formed certificate rooted at the empty state is
a genuine legal bounded-lead forcing strategy, hence also a negative result
for the unrestricted original game. A certificate rooted at another preload
proves only a local losing-state statement unless forceability of that root
from the empty state is separately certified.

For a canonical choice, order H, all finite arena states and legal actions
lexicographically, take the least losing H if one exists, use the exact
removal ranks, and choose the least rank-decreasing reply for each safe move.
This specifies the form of an exact obstruction; it does not claim to have
found one. Computing K_H for a fixed H is finite, while searching unbounded H
has no asserted terminating bound.

## 5. Remaining full-target obligation

The structural alternatives are exact. A positive resolution needs a robust
empty-containing invariant for every H, or another proof of the equivalent
empty-state fixed-point membership. A negative resolution needs a finite
forcing certificate rooted at the empty state (equivalently, a bounded-lead
counterexample after finite-horizon extraction). The accepted local preload
examples, failures of a candidate W_k closure, and failed quantitative
certificates do not settle this alternative.

No full-target resolution is asserted in this document.
