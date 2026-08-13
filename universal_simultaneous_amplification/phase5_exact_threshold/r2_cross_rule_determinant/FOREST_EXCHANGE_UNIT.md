# The first nonlocal forest-exchange unit

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note expands only the exact `s^2` coefficient from
`ROOT_KILLING_PHASE_BLOCK.md`.  It gives two proof-first advances.

1. The bad complete-triangle star is not a terminal obstruction: one
   weight-preserving fundamental-cycle pivot cancels it exactly.
2. A single-cycle (even one cycle in each member of the paired trees) cannot
   be the universal involution.  On the exact weighted three-path there is a
   negative paired atom for which every such neighbour is still negative.
   The closest positive atom requires two successive pivots in the `D` tree.

The latter two pivots form a three-component, or bicyclic, completion unit.
An exact two-deletion identity below lifts the whole coefficient to such
units without duplicating tree weight.  Individual units can still be
negative, so the remaining theorem requires an exchange *between*
three-component units.  This sharply separates the surviving global route
from the now-refuted one-cycle and packetwise-sign routes.

No literature search or external communication was used.

## 1. The literal paired-tree coefficient

Let `T_L(A)` denote the in-arborescences of `Q_L` rooted at the nonempty
subset `A`, and let `T_D(B)` denote the in-arborescences of the ordinary dB
generator rooted at the proper nonempty subset `B`.  Write `w(T)` for the
product of its directed edge rates.  Row-scaling dB by `1/|B|` gives the
event generator used by the common phase block.  The cofactor scaling rule

\[
 \theta_D(B)=\left\{\prod_C {|C|}^{-1}\right\}|B|\tau_D(B)                 \tag{1}
\]

shows that the event coefficient and the ordinary paired-tree coefficient
differ by one positive constant.  Consequently the coefficient sign is

\[
 \boxed{
 \mathfrak P=
 \sum_{T_L,T_D}w(T_L)w(T_D)
       \{b_nd_n-|r(T_L)|\,|r(T_D)|\}.}                    \tag{2}
\]

This is exactly `b_n d_n Z_L Z_D-Y_LY_D`, hence exactly `PAPT_n`; no
stronger inequality has been introduced.

There is also a useful integer-decoration form.  Put

\[
 D_b=2^n-1,\quad N_b=n2^{n-1},\qquad
 D_d=2^{n-1}-1,\quad N_d=(n-1)2^{n-2}.                    \tag{3}
\]

Thus `b_n=N_b/D_b` and `d_n=N_d/D_d`.  Let
`S_m` be the nonempty subsets of an `m`-set and let
`M_m={(U,u): U in S_m, u in U}`.  After multiplying `(2)` by
`D_bD_d`, its positive and negative masses are precisely the weighted
cardinalities of

\[
 \begin{aligned}
 \mathcal P={}&\{(T_L,T_D,(U,u),(W,w)):(U,u)\in M_n,
                                        (W,w)\in M_{n-1}\},\\
 \mathcal N={}&\{(T_L,T_D,u,w,U,W):u\in r(T_L),\ w\in r(T_D),
                                  U\in S_n,\ W\in S_{n-1}\}.
 \end{aligned}                                             \tag{4}
\]

Every atom in `(4)` carries only the tree-product weight.  Therefore a
nonduplicating common-arrow proof has a completely concrete target: a
weight-nondecreasing injection `mathcal N -> mathcal P`.  The decorations
record exactly the multiplicities hidden in the complete baselines; they
are not an auxiliary inequality.

## 2. Complete `K_3`: the bad star has an exact cycle mate

Use masks `1,...,6` for the proper nonempty subsets of three vertices.  For
the event dB generator on unweighted `K_3`, consider

\[
 T_-:\quad 2\to1,\ 3\to1,\ 4\to1,\ 5\to1,\ 1\to6.          \tag{5}
\]

It is rooted at mask `6`, has rank two, and has weight `1/972`.  Add the
edge `6->3`.  It closes the directed cycle

\[
                         1\to6\to3\to1 .                   \tag{6}
\]

Deleting `1->6` gives

\[
 T_+:\quad 2\to1,\ 3\to1,\ 4\to1,\ 5\to1,\ 6\to3,          \tag{7}
\]

which is rooted at mask `1`, has rank one, and again has weight `1/972`.
The reverse pivot recovers `(5)`, so this is a genuine weight-preserving
involution on the two atoms.

Every supported `L` skeleton at complete `K_3` has conditional root mean
`b_3=12/7`.  Since `d_3=4/3`, the conditional event costs of `(5)` and
`(7)` are respectively

\[
 {b_3d_3\over2}-b_3=-{4\over7},\qquad
 b_3d_3-b_3={4\over7}.                                    \tag{8}
\]

Thus the exact star obstruction is cancelled by one nonduplicating cycle
switch.  This explains why the star is a refutation of skeletonwise signs,
but not a refutation of a global exchange proof.

## 3. Weighted `P_3`: one cycle in each tree is still insufficient

Now take the three-path with

\[
                         w_{01}=1,\qquad w_{02}=2.           \tag{9}
\]

For `L`, take the in-tree

\[
 \begin{split}
 T_L^-:\quad&1\to2,\ 2\to3,\ 3\to6,\\
             &4\to1,\ 5\to6,\ 7\to3,
 \end{split}                                               \tag{10}
\]

rooted at mask `6`, of rank two and weight `4/27`.  For event dB take

\[
 T_D^-:\quad1\to6,\ 2\to1,\ 3\to6,\ 4\to1,\ 5\to6,       \tag{11}
\]

also rooted at mask `6`, with weight `3/100`.  Their event cost is

\[
 {b_3d_3\over2}-2=-{6\over7},                              \tag{12}
\]

so the signed atom has mass

\[
             -{6\over7}{4\over27}{3\over100}=-{2\over525}.
                                                                    \tag{13}
\]

A fundamental-cycle pivot replaces one directed edge of an arborescence by
one directed edge and may change its root.  Exact enumeration of *only the
one-pivot neighbourhoods* of `(10)--(11)` gives

\[
 \begin{array}{c|c}
 \text{tree}&\text{ranks of all roots at pivot distance at most one}\\ \hline
 T_L^-&2\text{ or }3,\\
 T_D^-&2.
 \end{array}                                                \tag{14}
\]

But the event cost `b_3d_3/k-a` is positive only for

\[
                       (a,k)=(1,1),(2,1),(1,2).             \tag{15}
\]

It follows immediately from `(14)--(15)` that there is no positive paired
atom obtainable by at most one pivot in each tree.  This is stronger than a
bad weight ratio: the required positive target does not exist.

The distance is sharp.  In `T_D^-`, perform the ordered pivots

\[
 5\to6\ \mapsto\ 6\to5,qquad
 1\to6\ \mapsto\ 5\to1.                                  \tag{16}
\]

The intermediate root is mask `5`; the final root is mask `1`.  The final
tree has weight `1/10`.  Keeping `(10)` fixed, its positive cost is `2/7`
and its positive mass is

\[
 {2\over7}{4\over27}{1\over10}={4\over945}
      ={10\over9}{2\over525}.                              \tag{17}
\]

Thus two pivots can dominate the displayed negative atom, whereas one
pivot in each factor cannot.  The union of the old and new `D` edges has
two independent fundamental cycles.  This is the first possible local
exchange unit on the hostile path.

The domination `(17)` is deliberately **not** called an injection.  Other
negative trees can have the same positive completion.  Nonduplication
forces all siblings of a common deleted forest to be accounted for, which
leads to the exact identity in the next section.

## 4. Exact two-deletion / three-component identity

Let `Q` be any irreducible generator on `N` states and let `mathscr T` be
its directed in-arborescences.  For a function `f` of the root, write

\[
                         H(f)=\sum_{T\in\mathscr T}w(T)f(r(T)). \tag{18}
\]

Let `mathscr F_2` contain every directed forest obtained from an
arborescence by deleting two edges, and put

\[
 H_F(f)=\sum_{T\supset F}w(T)f(r(T)).                       \tag{19}
\]

Every tree has exactly `binom(N-1,2)` two-edge deletions.  Double counting
the pairs `(T,F subset T)` proves the exact, reversible identity

\[
 \boxed{\sum_{F\in\mathscr F_2}H_F(f)
        ={N-1\choose2}H(f).}                               \tag{20}
\]

Apply `(20)` independently to `L` and ordinary dB.  If their state-space
sizes are `N_L,N_D`, then the coefficient `(2)` obeys

\[
 \boxed{
 {N_L-1\choose2}{N_D-1\choose2}\mathfrak P
  =\sum_{F,G}\{b_nd_nH_F^L(1)H_G^D(1)
                    -H_F^L(|r|)H_G^D(|r|)\}.}              \tag{21}
\]

Each `F` or `G` has three directed components.  Contracting the fixed
components reduces its completion polynomial to arborescences on three
component sinks.  Thus `(21)` is the exact deletion-contraction form of the
minimal bicyclic exchange suggested by `(16)`; it is not a search ansatz.

For the path witness, delete `2->3,3->6` from `(10)` and delete
`1->6,5->6` from `(11)`.  The `L` completion class has seven trees, with
root-rank weight totals

\[
                         L_1={80\over81},\qquad L_2={32\over81}, \tag{22}
\]

and the event-`D` completion class has six trees, with

\[
                         D_1={3\over20},\qquad D_2={9\over50}.  \tag{23}
\]

Its exact event packet is positive:

\[
 b_3d_3\left({112\over81}\right)
             \left({6\over25}\right)
 -\left({16\over9}\right)\left({33\over100}\right)
 ={116\over675}>0.                                         \tag{24}
\]

This is a genuine `7 x 6=42`-atom completion packet and contains the
two-pivot repair `(16)` without assigning its target twice.

However, packetwise positivity is false.  With the same `D` forest, other
two-edge deletions of `(10)` give negative packets; for example deleting
`7->3,5->6` gives exactly

\[
                            -{362\over525}<0.                \tag{25}
\]

Hence `(21)` is an exact global reorganization, but not yet the theorem.
A successful proof must perform a nonduplicating crabwalk/cycle exchange
between distinct three-component pairs `(F,G)`.  The complete-triangle
one-cycle involution and the path two-cycle packet identify its boundary
conditions:

- it must reduce to `(5)<->(7)` at the symmetric kernel;
- it must be allowed to move two pivots in the same history tree;
- and its inverse data must distinguish completion siblings, as in `(21)`.

## 5. Exact audit

`verify_forest_exchange_unit.py` checks over `QQ`:

- the ordinary/event cofactor scaling and the literal coefficient `(2)`;
- the complete-`K_3` weight-preserving involution `(5)--(8)`;
- every one-pivot neighbour in `(14)`;
- the sharp two-pivot repair and ratio `10/9` in `(16)--(17)`;
- the general double-counting identity `(20)` on the weighted path; and
- the positive and negative completion packets `(24)--(25)`.

The finite audits refute local exchange strengthenings; they are not a
finite-search proof of `PAPT_n`.

