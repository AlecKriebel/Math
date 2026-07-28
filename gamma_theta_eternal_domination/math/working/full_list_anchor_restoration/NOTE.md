# Rank-zero full-list anchor restoration: exact palette split and a sharp equality control

## Status and exact scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  Every
statement uses the standard one-guard-moves model: attacks are made only at
unoccupied vertices, exactly one adjacent guard moves, and every retained
successor stays in the same eternal family.

The package resolves one bookkeeping gap inside the four residual C-163
full-list terminal cases.

1. At a rank-zero anchor-restoration entry with a nonsingleton terminal
   root palette, the secondary color has an exact dichotomy.  If it is not
   the attacked anchor, then it is the shared anchor and arbitrary-state
   restoration forces the attacked anchor into the mover's root palette.
   Thus the superficially possible "shared secondary, but neither outside
   vertex restores the attacked anchor" subcase is impossible.
2. The only physical alternate is classified exactly by its move edge and
   ban status.  If that alternate is legal and unbanned, rank zero forces it
   to be nondominating.  In the shared-secondary branch, every missed
   witness then produces a two-attack restoration ladder unless it is the
   omitted root anchor itself.
3. A new 16-vertex equality control proves the sharp obstruction.  Even
   under
   \[
      \gamma=i=\alpha=\gamma^\infty=\theta=3,
   \]
   a legal dominating **banned** alternate at a rank-zero anchor restoration
   can be absent from the literal greatest eternal family.  The same graph
   realizes the attacked-secondary and shared-secondary rows with one
   common omitted alternate.

Accordingly, the implication

\[
 \text{dominating lower-rank or banned alternate}
 \Longrightarrow
 \text{retained alternate}
\]

cannot eliminate C-163's restoration branch, even when the equality
hypothesis is used.  A future proof must couple the three color bans or use
additional global structure.

This note does **not** prove that one restricted kernel survives, does not
eliminate rank-zero anchor restoration as a whole, does not prove complete
\(k=3\), and does not resolve the gamma--theta conjecture.  No
literature-priority claim is made.

## 1. Setup

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad \mathcal F^\star
  =\text{the literal greatest eternal family of triples}.
\tag{1.1}
\]

Let

\[
 S=\{u,a,c\}\in\mathcal F^\star
\tag{1.2}
\]

be independent, and fix a full target \(x\notin S\).  Thus all three root
swaps through \(x\) belong to \(\mathcal F^\star\).  Put

\[
 B=N_{\overline G}(x)
\tag{1.3}
\]

and use the exact greatest-family root palette

\[
 Q(z)=
 \{s\in S:sz\in E(G),\ S-s+z\in\mathcal F^\star\}.
\tag{1.4}
\]

For the selected color \(u\), ban the states

\[
 \mathcal B_u(x)=\{S-u+b:b\in B\}.
\tag{1.5}
\]

The restricted initial state space consists of all dominating triples
outside this ban.  Its synchronous greatest-fixed-point deletion ranks are
those of C-149 and C-163.

Consider a rank-zero anchor-restoration terminal:

\[
 T=\{c,r,q\}\in\mathcal F^\star-\mathcal B_u(x),
 \qquad
 E=\{a,c,r\}=S-u+r
       \in\mathcal F^\star\cap\mathcal B_u(x),
\tag{1.6}
\]

where \(r\in B\), the deletion-witness attack at \(T\) is the unoccupied
anchor \(a\), and the selected response is

\[
 q\longrightarrow a.
\tag{1.7}
\]

Assume the terminal palette is nonsingleton:

\[
 |Q(r)|\ge2.
\tag{1.8}
\]

Palette membership always includes both a graph edge and membership of the
corresponding root swap in \(\mathcal F^\star\).  Palette nonmembership will
never be used as a graph nonedge.

We use the accepted arbitrary-state restoration theorem in its exact
family form:

\[
 S-D\subseteq\bigcup_{z\in D-S}Q(z)
 \qquad(D\in\mathcal F^\star).
\tag{1.9}
\]

## 2. The exact secondary-palette split

### Lemma 2.1 (primary color and mover externality) — PROVED

In (1.6)--(1.8),

\[
 u\in Q(r)
 \qquad\text{and}\qquad
 q\notin S.
\tag{2.1}
\]

#### Proof

The retained state \(E=\{a,c,r\}\) dominates the unoccupied anchor \(u\).
The root anchors \(a,c\) miss \(u\), because \(S\) is independent.
Therefore \(ru\in E(G)\).  Together with
\(E=S-u+r\in\mathcal F^\star\), this says \(u\in Q(r)\).

The mover is distinct from \(a,c,r\).  Suppose \(q=u\).  Apply restoration
(1.9) to \(T=\{u,c,r\}\).  Its only missing root anchor is \(a\), and its
only outside vertex is \(r\), so \(a\in Q(r)\).  Hence \(ar\in E(G)\).
At the deletion-witness attack \(a\) from \(T\), the guard \(r\) could then
move to \(a\), reaching

\[
 T-r+a=S.
\]

The root is dominating and is outside the ban, contradicting that \(T\)
has rank zero for this attack.  Thus \(q\notin S\). \(\square\)

### Theorem 2.2 (attacked versus shared secondary) — PROVED

Exactly one of the following two cases holds.

1. **Attacked-anchor secondary.**
   \[
      a\in Q(r),
   \tag{2.2}
   \]
   while \(c\) may or may not also lie in \(Q(r)\).
2. **Shared-anchor only.**
   \[
      Q(r)=\{u,c\},
      \qquad
      a\in Q(q).
   \tag{2.3}
   \]

In particular, the case

\[
 a\notin Q(r)\cup Q(q)
\tag{2.4}
\]

is impossible at a nonsingleton rank-zero anchor restoration.

#### Proof

Lemma 2.1 gives \(u\in Q(r)\).  Since \(Q(r)\subseteq S\) and is
nonsingleton, it contains \(a\) or \(c\).  If it contains \(a\), case 1
holds.

Suppose it does not contain \(a\).  It must then contain \(c\), and hence
is exactly \(\{u,c\}\).  By Lemma 2.1, the state \(T\) misses precisely
\(\{u,a\}\) from \(S\), while its outside vertices are \(\{r,q\}\).
Restoration (1.9) gives

\[
 \{u,a\}\subseteq Q(r)\cup Q(q).
\]

The color \(a\) is absent from \(Q(r)\), so \(a\in Q(q)\).  This proves
(2.3) and excludes (2.4). \(\square\)

The conclusion \(a\in Q(q)\) is a retained root incidence, not merely the
already known move edge \(qa\).  Conversely, \(a\notin Q(r)\) says nothing
by itself about the physical edge \(ar\).

## 3. The physical alternate and its exact rank-zero boundary

Put

\[
 R=T-r+a=\{a,c,q\}=S-u+q.
\tag{3.1}
\]

The guard \(c\) cannot answer the attack at \(a\), because \(S\) is
independent.  Apart from the selected mover \(q\), the only possible mover
is therefore \(r\).

### Proposition 3.1 (complete alternate table) — PROVED

The status of \(R\) is exactly as follows.

| condition | one-guard status of \(R\) at the attack \(a\) | rank-zero consequence |
|---|---|---|
| \(ar\notin E(G)\) | not a legal successor | none |
| \(ar\in E(G)\), \(q\in B\) | legal but banned | none |
| \(ar\in E(G)\), \(q\notin B\) | legal and unbanned | \(R\) is nondominating |

Moreover, case (2.2) always has \(ar\in E(G)\), while case (2.3) permits
either physical status of \(ar\).

#### Proof

The move \(r\to a\) is legal exactly when \(ar\in E(G)\), and its successor
is (3.1).  Because \(q\notin S\), the state \(R=S-u+q\) belongs to the ban
exactly when \(q\in B\).  A rank-zero deletion-witness attack has no legal
dominating successor outside the ban.  Thus, in the third row, \(R\) cannot
dominate.  The first two rows create no unbanned legal successor and impose
no domination conclusion.

Finally, \(a\in Q(r)\) includes the edge \(ar\).  If
\(a\notin Q(r)\), no edge conclusion follows in either direction.
\(\square\)

This table is exhaustive.  In particular, it is invalid to replace the
last sentence by the false implication

\[
 a\notin Q(r)\Longrightarrow ar\notin E(G).
\]

### Proposition 3.2 (shared-secondary witness ladder) — PROVED

Assume the shared-anchor-only branch (2.3), and suppose \(R\) is
nondominating.  Let \(w\) be any vertex missed by \(R\):

\[
 N_G[w]\cap R=\varnothing.
\tag{3.2}
\]

Then either

\[
 w=u,\qquad uq\notin E(G),
\tag{3.3}
\]

or \(w\ne u\) and the following two unique one-guard responses are retained:

\[
 \{u,c,q\}
   \xrightarrow[\text{attack }w]{u\to w}
 \{w,c,q\}
   \xrightarrow[\text{attack }a]{q\to a}
 \{w,c,a\}.
\tag{3.4}
\]

Consequently,

\[
 u\in Q(w).
\tag{3.5}
\]

If additionally \(ar\in E(G)\), then \(w\notin
\{a,c,q,r,x\}\), so the second alternative supplies an external root
incidence unless the missed vertex is \(u\).

#### Proof

Theorem 2.2 gives

\[
 a\in Q(q),
\qquad
 U:=S-a+q=\{u,c,q\}\in\mathcal F^\star.
\tag{3.6}
\]

If \(w=u\), then (3.2) and the root nonedges \(ua,uc\notin E(G)\) give
\(uq\notin E(G)\), proving (3.3).

Suppose \(w\ne u\).  The state \(U\) dominates \(w\).  Both \(c\) and
\(q\) miss \(w\) by (3.2), so the only possible defender is \(u\).
The attack is unoccupied, and eternal closure forces the first unique move
in (3.4).

From \(\{w,c,q\}\), attack the unoccupied anchor \(a\).  The guard \(c\)
misses \(a\) because \(S\) is independent, and \(w\) misses \(a\) by
(3.2).  The original selected move (1.7) supplies \(qa\in E(G)\).
Thus \(q\to a\) is unique and closure forces the second state in (3.4).
The first move gives \(uw\in E(G)\), while the final state is exactly
\(S-u+w\).  Hence \(u\in Q(w)\).

Every missed vertex lies outside \(R=\{a,c,q\}\), and \(x\) is dominated
by \(a\) because \(x\) is full at \(S\).  If \(ar\in E(G)\), then \(R\)
also dominates \(r\).  This gives the final externality statement.
\(\square\)

The ladder is useful new structure, but it does not contradict equality:
the next section gives a sharp equality realization of the complementary
dominating branch.

## 4. A two-row equality control

Consider the graph

```text
OYifur}UO]}iTij]tpo]v
```

with

\[
 S=\{0,1,10\},\qquad x=6,\qquad u=0.
\tag{4.1}
\]

The independent verifier reconstructs

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)
   =(3,3,3,3,3),
\tag{4.2}
\]

a greatest eternal triple-family of 304 states, and the explicit
three-clique partition

\[
 \{0,2,5,11,14\},\quad
 \{1,3,6,8,12\},\quad
 \{4,7,9,10,13,15\}.
\tag{4.3}
\]

The target is full:

\[
 Q(6)=\{0,1,10\},
\tag{4.4}
\]

and

\[
 B=N_{\overline G}(6)=\{5,7,9,11,13\}.
\tag{4.5}
\]

The color-\(0\) restricted kernel is empty.  Its deletion-rank counts are

\[
 28,\ 81,\ 132,\ 62
\tag{4.6}
\]

at ranks \(0,1,2,3\), respectively.  The exact terminal and mover palettes
are

\[
 Q(5)=\{0,10\},
\qquad
 Q(7)=\{1,10\}.
\tag{4.7}
\]

The same terminal ban state

\[
 E=\{1,5,10\}
\tag{4.8}
\]

is reached from two different rank-zero anchor restorations.

### 4.1 Attacked-anchor secondary

From

\[
 T_A=\{1,5,7\},
\tag{4.9}
\]

attack \(10\).  The selected retained response is

\[
 7\to10,\qquad T_A-7+10=E.
\tag{4.10}
\]

Here \(10\in Q(5)\), so the secondary palette color is the attacked
anchor.  The physical alternate \(5\to10\) is legal and reaches

\[
 R=\{1,7,10\}.
\tag{4.11}
\]

Both \(5,7\in B\), so \(R\) is banned.  It dominates \(G\) but is absent
from the literal greatest eternal family.

Thus even the full equality hypothesis does not imply that a dominating
banned alternate is retained.

### 4.2 Shared-anchor secondary

From

\[
 T_C=\{5,7,10\},
\tag{4.12}
\]

attack \(1\).  Again the selected response is

\[
 7\to1,\qquad T_C-7+1=E.
\tag{4.13}
\]

Now the same palette \(Q(5)=\{0,10\}\) contains the shared anchor \(10\)
but not the attacked anchor \(1\).  Theorem 2.2 predicts
\(1\in Q(7)\), exactly as (4.7) records.  The physical edge \(1\,5\) is
absent in this graph, so \(5\) cannot answer this second attack.

The nonedge \(1\,5\) is read directly from the decoded graph.  It is not
inferred from \(1\notin Q(5)\).

Both rows point at the same dominating nonretained state (4.11): in the
first row it is a legal banned alternate; in the second it is not a
one-move successor.  This is the exact local obstruction boundary.

The other two color-restricted kernel sizes are

\[
 |\mathcal K_1|=150,\qquad |\mathcal K_{10}|=0.
\tag{4.14}
\]

Thus the control has a safe color and is not an all-three-empty example.
It proves only that a single-color local argument cannot promote the
alternate in (4.11).

## 5. Independent replay

The verifier in this directory:

- decodes the graph6 string without a graph library;
- recomputes \(\gamma,i,\alpha,\gamma^\infty,\theta\);
- reconstructs the literal greatest eternal triple-family and checks all
  3,952 unoccupied-attack obligations;
- reconstructs all three color-restricted kernels and every deletion rank;
- verifies both rank-zero rows, every named move edge and nonedge, both
  exact root palettes, domination and nonretention of \(R\), and the
  clique partition (4.3).

Replay:

```text
python3 -I -B -W error \
  math/working/full_list_anchor_restoration/verify_control.py
```

The control graph has order 16, size 71, and graph6 ASCII SHA-256

```text
a987f04ac6308118ae98bd8ce8c97a2f45514dc1e8e3fe02a6935cc5e898f3fa
```

## 6. Exact remaining gate

C-163's rank-zero anchor-restoration branch now has the following complete
local form.

- If the attacked anchor lies in \(Q(r)\), the alternate move edge exists.
  An unbanned alternate is nondominating; a banned alternate may dominate
  and still be absent from \(\mathcal F^\star\).
- If only the shared anchor is secondary, the attacked anchor is forced
  into \(Q(q)\).  An unbanned legal alternate is again nondominating, and
  its missed witnesses satisfy Proposition 3.2.  A missing attacked-anchor
  palette incidence at \(r\) does not determine the move edge \(ar\).

The equality control blocks every purely local attempt to finish by
retaining the dominating banned alternate.  The next meaningful target is
therefore simultaneous: use all three minimum-rank traces to show that
their forced palette transfers, witness ladders, and safe/unsafe color
statuses cannot coexist when all three restricted kernels are empty.

