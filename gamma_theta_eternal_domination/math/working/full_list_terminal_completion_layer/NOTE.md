# The rank-zero terminal completion layer

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It
continues accepted C-149, C-157, and C-168.  Every family below uses the
standard one-guard-moves model: an attack is made only at an unoccupied
vertex, exactly one guard moves along one graph edge to that vertex, and
the successor remains in the same eternal family.

The new theorem describes every independent completion of the
target--terminal pair in a C-157 rank-zero corridor.  Eternal closure
forces a two-way completion split.  A branch selected through a secondary
color must meet that color's private witness, and an attack at the full
target uniquely returns to the independent completion.

With two secondary colors, the entire completion clique is covered by
the two closed witness neighborhoods.  This is an exact local theorem,
but it does not force one color-restricted kernel to survive and it does
not compare deletion ranks belonging to different bans.

Three finite controls mark the boundary:

1. an equality graph shows that the unique completion return can go from
   restricted rank zero to rank three and that the layer does not force a
   dominating pair;
2. an 11-vertex gamma-two graph has a completion in all three corridor
   rows while all three restricted kernels are empty; and
3. a 9-vertex gamma-two graph realizes the full-terminal, two-witness
   overlap case with both completion branches retained.

No safe-color theorem, complete parameter-three theorem, or resolution
of the gamma--theta conjecture is claimed.  No literature-priority claim
is made.

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

be independent, let \(x\notin S\) be full at \(S\), and put

\[
 B=N_{\overline G}(x).
\tag{1.3}
\]

Use the root response palette

\[
 Q(z)=
 \{s\in S:sz\in E(G),\ S-s+z\in\mathcal F^\star\}.
\tag{1.4}
\]

Fix a C-157 rank-zero nonroot corridor for primary color \(u\):

\[
 T=\{v,t,q\}=S-u+q,\qquad
 E=\{v,t,r\}=S-u+r,
\tag{1.5}
\]

where \(T,E\in\mathcal F^\star\), \(r\in B\), \(q\notin B\), and the
deleting attack at \(T\) is answered by \(q\to r\).

Let \(v\) be a secondary terminal color:

\[
 v\in Q(r)-\{u\}.
\tag{1.6}
\]

Then C-157 says that the alternate response

\[
 A_v=\{t,q,r\}
\tag{1.7}
\]

is legal and unbanned but nondominating.  Fix any vertex \(w_v\) missed
by it.  Accepted C-157 and C-168 give

\[
 uw_v,vw_v\in E(G),\qquad
 tw_v,qw_v,rw_v\notin E(G),
\tag{1.8}
\]

and retain the two witness states

\[
 \{w_v,t,q\},\qquad \{w_v,t,r\}.
\tag{1.9}
\]

Define the common-nonneighbor completion set

\[
 C_{xr}=
 \{d\in V(G)-\{x,r\}:dx,dr\notin E(G)\}.
\tag{1.10}
\]

Because \(\gamma(G)=3\), the independent pair \(\{x,r\}\) is not
dominating, so \(C_{xr}\ne\varnothing\).  Because \(\alpha(G)=3\),
\(C_{xr}\) is a clique in \(G\): two nonadjacent members together with
\(x,r\) would form an independent four-set.  Every

\[
 I_d=\{x,r,d\}\qquad(d\in C_{xr})
\tag{1.11}
\]

is a maximum independent set and therefore belongs to
\(\mathcal F^\star\).

The proof below actually recovers the retention of \(I_d\) dynamically
from either surviving completion branch.

## 2. Exact completion split and return

### Theorem 2.1 (one-secondary completion split) — PROVED

For every \(d\in C_{xr}\), at least one of

\[
 D_v(d)=\{d,t,r\},\qquad
 D_t(d)=\{v,d,r\}
\tag{2.1}
\]

belongs to \(\mathcal F^\star\).

Whenever \(D_v(d)\in\mathcal F^\star\), one has

\[
 d\in N_G[w_v].
\tag{2.2}
\]

Equivalently, either \(d=w_v\) or \(dw_v\in E(G)\).  Moreover the attack
at the unoccupied vertex \(x\) from \(D_v(d)\) has exactly one physical
responder:

\[
 D_v(d)
   \xrightarrow[\text{attack }x]{t\to x}
 I_d=\{x,r,d\}\in\mathcal F^\star.
\tag{2.3}
\]

Thus a completion outside \(N_G[w_v]\) cannot use the \(v\to d\)
branch; closure then forces the other branch \(D_t(d)\).

#### Proof

The vertex \(d\) is outside \(E=\{v,t,r\}\).  Indeed, \(d\ne r\), while
fullness of \(x\) gives \(xv,xt\in E(G)\), and \(d\) misses \(x\).
Therefore attacking \(d\) from the retained state \(E\) is an
unoccupied attack.

The guard at \(r\) cannot move because \(rd\notin E(G)\).  Eternal
closure must use \(v\to d\) or \(t\to d\), with respective successors
exactly \(D_v(d)\) and \(D_t(d)\).  This proves the nonempty split.

Suppose \(D_v(d)\) is retained.  It dominates \(w_v\).  The other two
guards \(t,r\) both miss \(w_v\) by (1.8).  Hence either \(d=w_v\) or
\(dw_v\in E(G)\), which is precisely (2.2).  This closed-neighborhood
form is necessary: the completion vertex has not been proved distinct
from the witness.

Now attack \(x\) from \(D_v(d)\).  It is unoccupied.  The guards \(d,r\)
miss \(x\) by the definition of \(C_{xr}\) and (1.3), while the root
anchor \(t\) hits \(x\) by fullness.  Thus \(t\to x\) is the unique
physical response, its endpoint is \(I_d\), and closure retains that
endpoint. \(\square\)

### Theorem 2.2 (two-secondary completion cover) — PROVED

Assume also that \(t\in Q(r)-\{u\}\).  Its C-157 alternate

\[
 A_t=\{v,q,r\}
\tag{2.4}
\]

has a missed witness \(w_t\), where

\[
 uw_t,tw_t\in E(G),\qquad
 vw_t,qw_t,rw_t\notin E(G),
\tag{2.5}
\]

and \(w_t\ne w_v\).

Whenever \(D_t(d)\in\mathcal F^\star\),

\[
 d\in N_G[w_t],
\tag{2.6}
\]

and the attack at \(x\) has the unique response

\[
 D_t(d)
   \xrightarrow[\text{attack }x]{v\to x}
 I_d.
\tag{2.7}
\]

Consequently

\[
 \boxed{
 C_{xr}\subseteq N_G[w_v]\cup N_G[w_t].
 }
\tag{2.8}
\]

More exactly, if

\[
 R_v=\{d\in C_{xr}:D_v(d)\in\mathcal F^\star\},\qquad
 R_t=\{d\in C_{xr}:D_t(d)\in\mathcal F^\star\},
\tag{2.9}
\]

then

\[
 C_{xr}=R_v\cup R_t,\qquad
 R_v\subseteq N_G[w_v],\qquad
 R_t\subseteq N_G[w_t].
\tag{2.10}
\]

Both branches may survive for the same completion.  If
\(d\notin N_G[w_v]\), the \(t\)-branch is the unique retained response
to the attack at \(d\); the symmetric statement holds after exchanging
\(v,w_v\) with \(t,w_t\).

#### Proof

The proof of Theorem 2.1 is symmetric in the two anchors of \(S-u\).
If \(D_t(d)\) survives, it must dominate \(w_t\); the guards \(v,r\)
miss \(w_t\), proving (2.6).  In \(D_t(d)\), the guards \(d,r\) miss
\(x\), while \(v\) hits \(x\), proving the unique return (2.7).

The nonempty split from Theorem 2.1 gives \(C_{xr}=R_v\cup R_t\).
The two closed-neighborhood containments then give (2.8)--(2.10).
If one containment fails at \(d\), the associated state cannot be
retained, so the nonempty split forces the other state and makes it the
only retained response. \(\square\)

### Collision audit

All attacks above are literally unoccupied.

- \(d\notin\{x,r\}\) by (1.10).
- A full target is adjacent to every root anchor, so
  \(d\notin\{u,v,t\}\).
- The nonroot diamond has \(xq\in E(G)\), so \(d\ne q\).
- The only unresolved named collision is \(d=w_v\), or symmetrically
  \(d=w_t\).  It is handled by the closed neighborhoods in
  (2.2), (2.6), and (2.8); no loop edge is inferred.

The proof never converts absence from a family palette into a graph
nonedge.

## 3. What the layer does not force

The transitions (2.3) and (2.7) occur in the unrestricted greatest
family.  A unique one-guard response does **not** by itself compare the
deletion ranks of its endpoints.  Such a comparison would require the
attacked vertex to witness deletion at a specified peeling round.

Likewise, the clique cover (2.8) does not say that one witness meets all
of \(C_{xr}\), and the nonempty split does not say that exactly one
branch survives.

The exact remaining global gate is:

> Combine completion splits belonging to different primary colors with
> the no-dominating-pair hypothesis so as to force either a surviving
> restricted kernel or a genuine strict rank descent across bans.

The local completion theorem alone supplies neither conclusion.

## 4. Exact boundary controls

The verifier in this directory reconstructs every graph directly from
its graph6 string, computes \(\gamma,i,\alpha,\gamma^\infty,\theta\),
builds the literal greatest eternal triple-family, recomputes every
restricted kernel and deletion rank, and checks every named attack and
successor.

### 4.1 Equality: the unique return reverses the desired rank inequality

For

```text
OYifur}UO]}iTij]tpo]v
```

use

\[
 S=\{0,1,10\},\qquad x=6.
\tag{4.1}
\]

The exact parameters and kernel data are

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
 \qquad |\mathcal F^\star|=304,
\tag{4.2}
\]

\[
 (|\mathcal K_0|,|\mathcal K_1|,|\mathcal K_{10}|)
 =(0,150,0).
\tag{4.3}
\]

For the empty color \(u=0\), take

\[
 (v,t,q,r,w_v,d)=(1,10,14,11,8,13).
\tag{4.4}
\]

Here \(C_{6,11}=\{13\}\), both states in (2.1) survive, and the
\(v\)-branch has the unique return

\[
 \{13,10,11\}\xrightarrow{10\to6}\{6,11,13\}.
\tag{4.5}
\]

In the color-0 restricted peeling,

\[
 \operatorname{rank}_0\{13,10,11\}=0,\qquad
 \operatorname{rank}_0\{6,11,13\}=3.
\tag{4.6}
\]

Thus the unique completion return raises rather than lowers the source
rank.  The other empty-color row \(u=10\) has the same \(0\)-to-\(3\)
pattern for both of its completions \(d=7,9\).

This graph has no dominating pair, so one completion split does not
force such a pair.  Its color-1 restricted kernel is nonempty, so it is
an equality boundary control, not an all-three-empty example.

### 4.2 Gamma two: all three completed rows and all kernels empty

The labeled graph

```text
JEhbtj{rvu?
```

is the one-vertex extension of MMV-001 in which the new vertex 10 is
adjacent exactly to

\[
 \{0,1,2,3,4,6,7\}.
\tag{4.7}
\]

With

\[
 S=\{0,1,2\},\qquad x=8,
\tag{4.8}
\]

its exact parameters are

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4),
 \qquad |\mathcal F^\star|=118,
\tag{4.9}
\]

and all three color-restricted kernels are empty.

The three C-168 corridor rows and their unique completion vertices are

\[
\begin{array}{c|c|c|c|c|c|c}
u&v&t&q&r&w_v&C_{xr}\\ \hline
0&1&2&4&9&3&\{10\}\\
1&2&0&3&6&5&\{7\}\\
2&0&1&5&7&4&\{6\}.
\end{array}
\tag{4.10}
\]

In every row both completion branches survive, the completion meets the
displayed witness by an edge, and the primary-color ranks of the
\(v\)-branch and independent completion are respectively \(0\) and
\(3\).

The graph has exactly the two dominating pairs

\[
 \{1,10\},\qquad \{5,10\}.
\tag{4.11}
\]

In particular none of the three named independent target--terminal
pairs is dominating.  This control shows that the complete
three-witness transfer cycle, a completion in every row, and three empty
restricted kernels still do not produce a safe color without the
\(\gamma=3\) hypothesis.

### 4.3 Gamma two: the symmetric overlap is sharp

For

```text
HF~mdfj
```

take

\[
 S=\{0,1,2\},\quad x=3,\quad
 (u,q,r,w_1,w_2,d)=(0,4,5,6,7,8).
\tag{4.12}
\]

The exact parameters are

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3),
 \qquad |\mathcal F^\star|=76.
\tag{4.13}
\]

The predecessor \(\{1,2,4\}\) has color-0 rank zero, the terminal
palette is full,

\[
 Q(5)=S,
\tag{4.14}
\]

and the two alternates have the distinct unique missed witnesses
\(w_1=6\) and \(w_2=7\).  The completion set is the singleton
\(C_{3,5}=\{8\}\).  Both completion branches survive, vertex 8 is
adjacent to both witnesses, and both attacks at \(x\) uniquely return to
\(\{3,5,8\}\).

Hence the two sets \(R_v,R_t\) in (2.9) may coincide with the whole
completion clique.  The theorem cannot be strengthened to an exclusive
branch partition.

## 5. Computational status

A discovery-only SAT encoding of the named full-terminal geometry,
literal eternal-family closure, \(\alpha\le3\), and \(\gamma\ge3\)
reported `UNSAT` at orders 8 through 12.  These runs have no proof logs,
independent CNF reconstruction, or all-order coverage theorem.  They are
**OBSERVED only** and are not used in Theorems 2.1 or 2.2.

## 6. Exact checkpoint

### PROVED in this candidate

- The nonempty completion split for every \(d\in C_{xr}\).
- Closed-witness incidence and the unique return to
  \(\{x,r,d\}\) on every surviving secondary branch.
- The symmetric two-witness cover of the entire completion clique.
- The exact collision-safe formulation using closed neighborhoods.

### EXACT finite controls

- Equality rank reversal \(0\to3\) and absence of a dominating pair.
- Three completed all-empty rows at gamma two.
- Full-terminal two-witness overlap at gamma two.

### OPEN

- A strict rank comparison across different color bans.
- A proof that one color is safe under the simultaneous
  \(\gamma=3\), all-three-empty hypothesis.
- Elimination of the remaining anchor-restoration and positive-rank
  terminal branches.
- Complete \(k=3\) and the universal gamma--theta conjecture.
