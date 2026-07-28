# Rank-zero corridor transfer and the exact three-color coupling gate

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It
continues accepted C-149, C-154, C-157, C-163, and C-165.  Every statement
uses the standard one-guard-moves model: attacks are made only at
unoccupied vertices, exactly one adjacent guard moves, and a retained
successor remains in the same eternal family.

The new human theorem strengthens C-157's rank-zero corridor witness.
That witness forces a two-state retained ladder and an exact palette
transfer: every secondary terminal color must reappear at the corridor
mover or at its private witness.

For three simultaneous nonsingleton corridor rows, the secondary-color
map has only two possible orbit types, a directed 3-cycle or a 2-cycle
with a tail.  The transfer theorem realizes every arrow by a retained
one-guard ladder.  This is a finite reduction, but it is not yet a
contradiction.  The remaining missing statement is a **cross-ban rank
inequality**: the ladders give finite ranks in the recipient color when
their endpoints lie outside the physical link, but do not make any of
those ranks strictly smaller.

Two exact controls mark the boundary.

- A 16-vertex equality graph realizes the cyclic terminal palettes and two
  forced witness transfers, while the third color is safe.
- MMV-001 realizes the complete three-witness transfer cycle and has all
  three restricted kernels empty, but \(\gamma=2\).

Thus neither palette incidence nor the three ladders alone can finish the
proof.  This package does **not** prove that a safe color exists, does not
complete \(k=3\), and does not resolve the gamma--theta conjecture.

No literature-priority claim is made.

## 1. Setup

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad
 \mathcal F^\star
   =\text{the literal greatest eternal family of dominating triples}.
\tag{1.1}
\]

Let

\[
 S=\{u,v,t\}\in\mathcal F^\star
\tag{1.2}
\]

be independent, and let \(x\notin S\) be full at \(S\).  Put

\[
 B=N_{\overline G}(x)
\tag{1.3}
\]

and use the greatest-family root palette

\[
 Q(z)=
 \{s\in S:sz\in E(G),\ S-s+z\in\mathcal F^\star\}.
\tag{1.4}
\]

For color \(u\), the C-149 ban is

\[
 \mathcal B_u(x)=\{S-u+b:b\in B\}.
\tag{1.5}
\]

Consider a rank-zero nonroot corridor terminal:

\[
 T=\{v,t,q\}=S-u+q,
 \qquad
 E=\{v,t,r\}=S-u+r,
\tag{1.6}
\]

where

\[
 r\in B,\qquad q\notin B,
\tag{1.7}
\]

the deletion-witness attack at \(T\) is the unoccupied vertex \(r\), and
the selected retained response is

\[
 q\longrightarrow r,\qquad E\in\mathcal F^\star.
\tag{1.8}
\]

The corridor is nonroot, so C-149 gives

\[
 q\notin S\cup B\cup\{x\}
\tag{1.9}
\]

and the diamond on \(\{x,u,q,r\}\), with \(xr\) its only missing
edge.

Assume that \(v\) is a secondary terminal color:

\[
 v\in Q(r)-\{u\}.
\tag{1.10}
\]

Then the alternate response to the attack \(r\) is

\[
 A_v=T-v+r=\{t,q,r\}.
\tag{1.11}
\]

C-157 says that \(A_v\) is legal and unbanned but nondominating.  Let
\(w\) be any missed witness:

\[
 N_G[w]\cap A_v=\varnothing.
\tag{1.12}
\]

It also gives

\[
 vw\in E(G),\qquad
 w\notin S\cup\{x,q,r\}.
\tag{1.13}
\]

No palette nonmembership will be converted into a graph nonedge.

## 2. The corridor witness ladder

### Theorem 2.1 (two forced states and palette transfer) — PROVED

Under (1.1)--(1.13), all of the following hold.

First,

\[
 uw,vw\in E(G),\qquad
 wt,wq,wr\notin E(G).
\tag{2.1}
\]

Second, the following two one-guard responses are unique and retained:

\[
 \{v,t,q\}
   \xrightarrow[\text{attack }w]{v\to w}
 \{w,t,q\},
\tag{2.2}
\]

\[
 \{u,t,r\}
   \xrightarrow[\text{attack }w]{u\to w}
 \{w,t,r\}.
\tag{2.3}
\]

Finally,

\[
 \boxed{v\in Q(q)\cup Q(w).}
\tag{2.4}
\]

More precisely, from the retained state \(K=\{w,t,q\}\), the attack at
the unoccupied anchor \(u\) has exactly the two physical responders
\(w,q\), and their endpoints are

\[
 K-w+u=S-v+q,\qquad
 K-q+u=S-v+w.
\tag{2.5}
\]

Thus, if \(v\notin Q(q)\), closure forces

\[
 q\to u,\qquad S-v+w\in\mathcal F^\star,
\qquad v\in Q(w).
\tag{2.6}
\]

#### Proof

The state

\[
 F_v:=S-v+r=\{u,t,r\}
\tag{2.7}
\]

belongs to \(\mathcal F^\star\) by (1.10).  It dominates \(w\).
The vertices \(t,r\) both miss \(w\) by (1.12), so \(u\) must hit \(w\).
Together with the C-157 edge \(vw\), this proves the positive part of
(2.1); the three negative edges are exactly (1.12).

Attack the unoccupied vertex \(w\) from \(T=\{v,t,q\}\).  The guards
\(t,q\) miss \(w\), while \(v\) hits it.  Hence \(v\to w\) is the unique
legal response, and eternal closure gives (2.2).

Likewise, attack \(w\) from \(F_v=\{u,t,r\}\).  The guards \(t,r\) miss
\(w\), while \(u\) hits it.  Hence \(u\to w\) is unique and closure gives
(2.3).  Both attacks are unoccupied by (1.13), and exactly one guard moves
in each.

The retained predecessor \(T=S-u+q\) dominates the omitted anchor \(u\).
The anchors \(v,t\) miss \(u\), so \(qu\in E(G)\); together with the
retained root swap, this says

\[
 u\in Q(q).
\tag{2.8}
\]

Now attack the unoccupied anchor \(u\) from

\[
 K=\{w,t,q\}\in\mathcal F^\star.
\]

The root nonedge \(tu\notin E(G)\) blocks \(t\).  Equations (2.1) and
(2.8) show that \(w,q\) are exactly the two physical responders, with the
endpoints in (2.5).

If the first endpoint \(S-v+q\) is retained, then it dominates the omitted
anchor \(v\).  The two root anchors in that state miss \(v\), so \(qv\)
is an edge and \(v\in Q(q)\).  Consequently, when \(v\notin Q(q)\), the
first endpoint is absent from \(\mathcal F^\star\).  Closure then forces
the second endpoint \(S-v+w\), and (1.13) supplies the edge \(vw\).
Therefore \(v\in Q(w)\).  This proves (2.4)--(2.6). \(\square\)

The proof uses palette nonmembership only to exclude a family state after
showing that retention of that state would itself imply palette
membership.  It does not infer \(qv\notin E(G)\).

### Corollary 2.2 (a full terminal palette) — PROVED

If \(Q(r)=S\), let \(w_v,w_t\) be C-157 missed witnesses for the two
secondary colors.  They are distinct, and

\[
 v\in Q(q)\cup Q(w_v),\qquad
 t\in Q(q)\cup Q(w_t).
\tag{2.9}
\]

In particular:

- if both secondary colors transfer to \(q\), then \(Q(q)=S\);
- if exactly one transfers to \(q\), the other transfers to its witness;
- if neither transfers to \(q\), the two distinct witnesses receive the
  two respective secondary colors.

#### Proof

C-157 proves \(w_v\ne w_t\).  Apply Theorem 2.1 separately to the two
secondary colors.  Equation (2.8) always gives \(u\in Q(q)\), so both
secondary memberships at \(q\) make its palette full. \(\square\)

## 3. Finite three-color reduction

Assume conditionally that all three selected minimum-terminal entries
have rank zero, are nonroot corridors, and have nonsingleton terminal
palettes.  For each \(u\in S\), choose one secondary color

\[
 \sigma(u)\in Q(r_u)-\{u\}.
\tag{3.1}
\]

### Proposition 3.1 (only two color-cycle types) — PROVED

Up to permuting the three root colors, the functional digraph of
\(\sigma\) is exactly one of:

\[
 a\longrightarrow b\longrightarrow c\longrightarrow a,
\tag{3.2}
\]

or

\[
 a\longleftrightarrow b,\qquad c\longrightarrow a.
\tag{3.3}
\]

For every arrow \(u\to\sigma(u)\), Theorem 2.1 supplies a physical
transfer endpoint

\[
 z_u\in\{q_u,w_u\}
\quad\text{such that}\quad
\sigma(u)\in Q(z_u).
\tag{3.4}
\]

No distinctness between vertices belonging to different rows is required.

#### Proof

The map \(\sigma\) has three vertices and no fixed point.  Every finite
functional digraph contains a directed cycle.  Its cycle therefore has
length two or three.  A 3-cycle gives (3.2).  A 2-cycle uses two colors,
and the third color points to one of its two vertices; relabeling gives
(3.3).  These are exhaustive.  Equation (3.4) is Theorem 2.1. \(\square\)

There are eight labeled choices of \(\sigma\): two are directed
3-cycles and six are 2-cycle-with-tail maps.  This elementary count is
replayed by the checker.

### Collision audit

Within one row, all attacks above are literally unoccupied:

- \(r\in B\) and fullness keep \(r\) outside \(S\cup\{x\}\);
- the nonroot corridor gives
  \(q\notin S\cup B\cup\{x,r\}\);
- C-157 gives \(w\notin S\cup\{x,q,r\}\).

Thus \(T,F_v,K\), and the two ladder endpoints are genuine triples.

Across different rows, no collision is silently excluded.  In particular:

- terminal vertices \(r_u,r_v\) may coincide, in which case their common
  palette contains both primary colors;
- a witness in one row may be a mover or witness in another;
- transfer endpoints \(z_u\) may coincide; and
- the complete MMV-001 control below has
  \(w_u=q_{\sigma(u)}\) around a directed 3-cycle.

Proposition 3.1 concerns the three root-color labels, not a claim that
the realizing graph vertices are distinct.

## 4. Why the transfer cycle does not yet descend

Now restore the actual all-three-empty hypothesis.  Every retained
unbanned state has a finite deletion rank in each relevant restricted
peeling.

For a row \(u\to v=\sigma(u)\):

- the mover satisfies \(q_u\notin B\);
- if the transfer lands at \(q_u\), then
  \(S-v+q_u\in\mathcal F^\star\) is unbanned for color \(v\), and hence
  has finite \(v\)-rank;
- if the transfer lands at \(w_u\notin B\), then
  \(S-v+w_u\in\mathcal F^\star\) is likewise unbanned and has finite
  \(v\)-rank;
- if \(w_u\in B\), the transferred root state is banned for color \(v\)
  and has no restricted rank.

The two attacks in Theorem 2.1 occur inside the unrestricted family.
They do not say that either named attack is a deletion-witness attack for
the **recipient** color.  Consequently they supply no strict inequality
between the recipient rank and the source row's rank.

This is the exact coupling gate:

> **Open cross-ban rank gate.**  Prove that, around one of the directed
> cycles in Proposition 3.1, some transferred unbanned root state has
> recipient deletion rank strictly below the selected minimum terminal
> rank; or prove that a transfer trapped inside \(B\) forces a dominating
> pair or a surviving restricted kernel.

Without such a statement, following the palette arrows merely walks among
finite ranks belonging to different peelings.  Ranks from different bans
have no accepted monotonic comparison.

The other C-163/C-165 terminal types remain separate irreducible exits:

1. a positive-rank corridor or restoration can produce a dominating
   lower-rank state absent from \(\mathcal F^\star\);
2. an attacked-secondary rank-zero restoration need not transfer a color
   to its mover;
3. a shared-secondary restoration can have a blocked or banned physical
   alternate; and
4. C-165's witness ladder transfers a palette only in the legal,
   unbanned, nondominating subcase.

Thus Proposition 3.1 closes the finite color bookkeeping only for the
all-rank-zero nonsingleton-corridor subcase.  It does not discard the
other three minimum-terminal cases.

## 5. Exact boundary controls

### 5.1 Equality: cyclic palettes with one safe color

For

```text
OYifur}UO]}iTij]tpo]v
```

with

\[
 S=\{0,1,10\},\qquad x=6,
\tag{5.1}
\]

the checker recomputes

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
\qquad |\mathcal F^\star|=304,
\tag{5.2}
\]

and restricted-kernel sizes

\[
 (|\mathcal K_0|,|\mathcal K_1|,|\mathcal K_{10}|)
 =(0,150,0).
\tag{5.3}
\]

The three corridor terminal palettes form the directed color cycle

\[
 Q(11)=\{0,1\},\qquad
 Q(7)=\{1,10\},\qquad
 Q(5)=\{0,10\}.
\tag{5.4}
\]

The two annihilated colors have the exact rank-zero witness ladders

\[
\begin{array}{c|c|c|c|c}
u&v&q&r&w\\ \hline
0&1&14&11&8\\
10&0&12&5&4.
\end{array}
\tag{5.5}
\]

In both rows the secondary color is absent from \(Q(q)\) and present in
\(Q(w)\), so (2.6) is sharp.  The third row,

\[
 u=1,\quad v=10,\quad q=3,\quad r=7,
\tag{5.6}
\]

has a dominating secondary alternate \(\{0,3,7\}\) inside the
150-state color-1 kernel.  This is precisely where the would-be third
witness ladder stops.

Thus equality permits the entire cyclic **color** pattern and two sharp
transfers.  The missing third transfer is exactly the safe color, not a
static palette obstruction.

### 5.2 Gamma two: the complete three-witness cycle

For MMV-001

```text
IEhbtj{ro
```

with

\[
 S=\{0,1,2\},\qquad x=8,
\tag{5.7}
\]

the exact parameters are

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4),
\tag{5.8}
\]

and all three restricted kernels are empty.  The following three
rank-zero corridor rows form the complete witness-mover cycle:

\[
\begin{array}{c|c|c|c|c}
u&v&q_u&r_u&w_u\\ \hline
0&1&4&9&3\\
1&2&3&6&5\\
2&0&5&7&4.
\end{array}
\tag{5.9}
\]

Thus

\[
 w_0=q_1,\qquad w_1=q_2,\qquad w_2=q_0.
\tag{5.10}
\]

Every alternate \(\{t,q_u,r_u\}\) misses the displayed \(w_u\), both
ladder states survive, and the secondary transfer lands at \(w_u\).
The graph has the dominating pair \(\{8,9\}\), so it fails exactly the
\(\gamma=3\) hypothesis and is not a gamma--theta counterexample.

This proves that the complete three-ladder cycle is a valid one-guard
configuration and that any universal exclusion must genuinely use
domination equality.

## 6. Exploratory cyclic-core search

The discovery script in this directory encodes the complete named
three-witness corridor cycle, an arbitrary eternal triple-family,
\(\alpha\le3\), and \(\gamma\ge3\).  With pinned CaDiCaL 3.0.1 it
reported:

\[
\begin{array}{c|cccccc}
n&10&11&12&13&14&15\\ \hline
\text{status}&
\mathrm{UNSAT}&\mathrm{UNSAT}&\mathrm{UNSAT}&
\mathrm{UNSAT}&\mathrm{UNSAT}&\mathrm{UNSAT}.
\end{array}
\tag{6.1}
\]

The \(n=16\) run was stopped at the five-minute cap without a result.
Dropping \(\gamma\ge3\) is SAT already at order 10, agreeing with the
gamma-two boundary.

These rows are **OBSERVED only**.  There are no proof logs, no independent
CNF reconstruction, and no coverage argument beyond the stated named
encoding.  They are not a finite exclusion and are not used in any proof
above.

## 7. Exact checkpoint

### PROVED in this candidate

- The rank-zero corridor witness ladder, Theorem 2.1.
- The full-terminal two-witness split, Corollary 2.2.
- The two orbit types for three selected secondary colors and their
  physical transfer realization, Proposition 3.1.

### EXACT finite controls

- The equality cyclic-palette/two-transfer boundary (5.1)--(5.6).
- The gamma-two all-empty/full-three-transfer boundary (5.7)--(5.10).

### OPEN

- Any strict comparison between deletion ranks belonging to two different
  color bans.
- Transfer endpoints that lie in \(B\).
- Attacked-secondary restoration rows and blocked/banned alternates.
- Positive-rank nonretained alternates.
- Existence of a safe color, the complete \(k=3\) theorem, and the
  universal gamma--theta conjecture.
