# Completion fans after a trapped rank-zero full-list escape

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate C-173 theorem package awaiting hostile review**.  It
continues accepted C-149, C-157, C-168, C-170, and C-171 in the standard
one-guard-moves model.

The new theorem identifies the first place where the hypothesis
\(\gamma=3\) changes the sharp MMV-027 rank-preserving escape.  Two
independent pairs that dominate MMV-027 must instead have nonempty
completion cliques.  Eternal closure turns those cliques into retained
independent completion fans.  Every completion in the second fan, and
every noncolliding completion in the first, is either in the restricted
kernel or has deletion rank at least one.  Thus a rank-zero to rank-zero
trapped escape necessarily rebounds into a positive-rank controlled layer
when the restricted kernel is empty.

Two collision branches have exact dynamics.  A missing witness--escape
edge produces a reciprocal two-state hinge.  An overlap of the two
completion cliques forces that edge and produces a reciprocal four-state
square.

This does **not** force a restricted kernel.  The exact 13-vertex control

```text
LEhbtnm~D]xln{
```

has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4),
\]

all three restricted kernels empty, source and escape rank zero, and two
disjoint singleton completion fans whose completion states both have
source-color rank two.  Its four remaining dominating pairs show the next
equality layer.  It is not a counterexample to the gamma--theta
conjecture.

No complete \(k=3\) theorem, universal theorem, or literature-priority
claim is made.

## 1. Exact setup

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad
 \mathcal F^\star=
 \text{the literal greatest eternal family of dominating triples}.
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

For source color \(u\), the C-149 ban is

\[
 \mathcal B_u(x)=
 \{\{v,t,b\}:b\in B\}.
\tag{1.4}
\]

Fix the C-171 trapped rank-zero corridor:

\[
\begin{aligned}
 T&=\{v,t,q\}\in\mathcal F^\star,\\
 E&=\{v,t,r\}\in\mathcal F^\star,
\end{aligned}
\qquad
 r\in B,\quad q\notin B,
\tag{1.5}
\]

where the deleting attack at \(T\) is answered by \(q\to r\).  Let
\(v\) be a secondary root color at \(r\).  Its nondominating alternate is

\[
 A_v=\{t,q,r\},
\tag{1.6}
\]

and let \(w\) be any vertex missed by \(A_v\).  Accepted C-168 gives

\[
 uw,vw\in E(G),\qquad
 wt,wq,wr\notin E(G),
\tag{1.7}
\]

and retains

\[
 L_q=\{w,t,q\},\qquad L_r=\{w,t,r\}.
\tag{1.8}
\]

Assume the trapped case

\[
 w\in B,\qquad xw\notin E(G).
\tag{1.9}
\]

Accepted C-171 then gives

\[
 tr\in E(G)
\tag{1.10}
\]

and says that

\[
 H=\{v,q,r\}
\tag{1.11}
\]

is nondominating.  Fix any vertex \(y\) missed by \(H\).  Then

\[
\begin{aligned}
 &yv,yq,yr\notin E(G),\\
 &yu,yt,yx\in E(G),
\end{aligned}
\tag{1.12}
\]

and the unbanned source-color escape

\[
 Y=\{v,t,y\}\in\mathcal F^\star
\tag{1.13}
\]

is retained.  In particular, \(q,w\) and \(r,y\) are independent pairs.

For an independent pair \(a,b\), write

\[
 C_{ab}
 =
 V(G)\setminus\bigl(N_G[a]\cup N_G[b]\bigr).
\tag{1.14}
\]

Thus \(C_{ab}\) is the set of vertices missed by the pair.  Closed
neighborhoods make (1.14) collision-safe.

## 2. Completion fans and rank rebound

### Lemma 2.1 (Johnson-distance rank floor) — PROVED

This preliminary statement holds for every guard number \(k\).  Let
\(\mathcal F\) be an eternal family of \(k\)-sets, let \(\mathcal B\) be
any nonempty set of banned \(k\)-configurations, and peel the universe of all
dominating \(k\)-sets outside \(\mathcal B\).  Write

\[
 \delta_{\mathcal B}(D)
 =
 \min_{B'\in\mathcal B}\bigl(k-|D\cap B'|\bigr)
\tag{2.1}
\]

for Johnson distance to the ban.  If \(D\in\mathcal F\) has finite
restricted deletion rank \(\rho(D)\), then

\[
 \boxed{\rho(D)\ge \delta_{\mathcal B}(D)-1.}
\tag{2.2}
\]

Equivalently, a retained state at distance at least \(h+1\) from the ban
survives the first \(h\) deletion rounds.

#### Proof

Let \(\Omega_0\) be the initial universe and
\(\Omega_{j+1}=\Phi(\Omega_j)\) the synchronous one-guard peeling.  We
prove by induction on \(h\) that

\[
 D\in\mathcal F,\quad \delta_{\mathcal B}(D)\ge h+1
 \quad\Longrightarrow\quad D\in\Omega_h.
\tag{2.3}
\]

For \(h=0\), positive distance means \(D\notin\mathcal B\), and every
member of \(\mathcal F\) dominates, so \(D\in\Omega_0\).

For the induction step, consider any unoccupied attack at \(D\).
Eternal closure supplies a one-guard successor \(D'\in\mathcal F\).
One guard move changes Johnson distance to a fixed \(k\)-set by at most
one, and hence

\[
 \delta_{\mathcal B}(D')
 \ge \delta_{\mathcal B}(D)-1
 \ge h+1.
\tag{2.4}
\]

The induction hypothesis puts \(D'\) in \(\Omega_h\).  This works for
every attack, so \(D\in\Phi(\Omega_h)=\Omega_{h+1}\).

Taking \(h=\delta_{\mathcal B}(D)-1\) proves (2.2). \(\square\)

For the source-color ban (1.4), any retained triple containing neither
\(v\) nor \(t\) has Johnson distance at least two from the ban.  It is
therefore either in the restricted kernel or has deletion rank at least
one.

### Theorem 2.1 (completion fans and rank rebound) — PROVED

Under (1.1)--(1.14):

1. Both \(C_{qw}\) and \(C_{ry}\) are nonempty cliques of \(G\).

2. The first completion clique satisfies

   \[
   \boxed{C_{qw}\subseteq N_G[t].}
   \tag{2.5}
   \]

   For every \(d\in C_{qw}\setminus\{t\}\), the attack at \(d\) from
   \(L_q\) has the unique response

   \[
   \{w,t,q\}
      \xrightarrow[\text{attack }d]{t\to d}
   I_d=\{q,w,d\}\in\mathcal F^\star.
   \tag{2.6}
   \]

   The state \(I_d\) is a maximum independent set and is either in the
   restricted kernel or has source-color deletion rank at least one.
   The excluded collision \(d=t\) says simply that \(L_q\) itself is
   independent; no occupied attack at \(t\) is asserted.

3. Eternal closure uniquely retains

   \[
   J=\{v,r,y\}\in\mathcal F^\star
   \tag{2.7}
   \]

   by attacking \(y\) from \(E\) and moving \(t\to y\).  The second
   completion clique satisfies

   \[
   C_{ry}\subseteq N_G(v).
   \tag{2.8}
   \]

   For every \(e\in C_{ry}\), the attack at \(e\) from \(J\) has the
   unique response

   \[
   \{v,r,y\}
      \xrightarrow[\text{attack }e]{v\to e}
   K_e=\{r,y,e\}\in\mathcal F^\star.
   \tag{2.9}
   \]

   Every \(K_e\) is a maximum independent set and is either in the
   restricted kernel or has source-color deletion rank at least one.

Consequently, if the color-\(u\) restricted kernel is empty, every
\(K_e\), and every \(I_d\) with \(d\ne t\), has finite rank at least one.
In particular, even when the C-171 escape \(Y\) has rank zero, its
forced completion layer cannot consist solely of rank-zero states.

#### Proof

The pairs \(q,w\) and \(r,y\) are nonadjacent by (1.7) and (1.12).
Because \(\gamma(G)=3\), neither pair dominates, so both missed sets in
(1.14) are nonempty.

If two distinct vertices of \(C_{qw}\) were nonadjacent, they together
with \(q,w\) would form an independent four-set.  This contradicts
\(\alpha(G)=3\), so \(C_{qw}\) is a clique.  The same argument with
\(r,y\) proves that \(C_{ry}\) is a clique.

Take \(d\in C_{qw}\).  If \(d=t\), then \(d\in N_G[t]\) by the closed
neighborhood convention.  Otherwise \(d\) is an unoccupied vertex
missed by the \(q\)-guard and the \(w\)-guard of the retained dominating
state \(L_q=\{w,t,q\}\).  Therefore \(td\in E(G)\), proving (2.5), and
\(t\to d\) is the unique physical response.  Eternal closure proves
(2.6).  The endpoint is independent by the definition of \(C_{qw}\).

For the rank claim, \(I_d\) contains neither \(v\) nor \(t\).  Indeed
\(d\ne t\), while \(d\ne v\) because \(vw\in E(G)\).  Lemma 2.1
applies.

Next attack the unoccupied vertex \(y\) from the retained terminal
\(E=\{v,t,r\}\).  Equations (1.12) say that \(v,r\) miss \(y\), while
\(t\) hits it.  Thus \(t\to y\) is unique and closure retains
\(J=\{v,r,y\}\).

Take \(e\in C_{ry}\).  The retained state \(J\) dominates \(e\), while
its \(r\)- and \(y\)-guards miss \(e\).  Hence \(ve\in E(G)\), proving
(2.8), and \(v\to e\) is the unique response to the attack at \(e\).
This proves (2.9), whose endpoint is independent by definition.

Finally, \(K_e\) contains neither \(v\) nor \(t\).  The completion vertex
cannot equal \(v\) because \(vr\in E(G)\), and it cannot equal \(t\)
because \(tr,ty\in E(G)\).  Lemma 2.1 applies again.  When the restricted
kernel is empty, all these nonzero ranks are finite. \(\square\)

No family-palette omission is converted into a graph nonedge in this
proof.

### Corollary 2.2 (minimum-rank fan exit) — PROVED

Assume the color-\(u\) restricted kernel is empty.  Choose
\(e\in C_{ry}\) so that

\[
 h=\operatorname{rank}_u(K_e)
\tag{2.10}
\]

is minimum over the second completion fan.  Then \(h\ge1\), and no
deletion-witness attack for \(K_e\) lies in
\(C_{ry}\setminus\{e\}\).  Every such attack is therefore adjacent in
\(G\) to \(r\) or \(y\).  Every retained response to it remains
unbanned and has source-color rank strictly below \(h\).

#### Proof

Theorem 2.1 gives \(h\ge1\).  For any
\(e'\in C_{ry}\setminus\{e\}\), the clique property gives
\(ee'\in E(G)\), while \(r,e'\) and \(y,e'\) are nonedges.  Thus the
attack at \(e'\) from \(K_e=\{r,y,e\}\) has the unique response

\[
 e\to e',\qquad K_e\longrightarrow K_{e'}.
\tag{2.11}
\]

The endpoint has rank at least \(h\) by the choice of \(e\), so this
attack cannot witness deletion at rank \(h\).

An unoccupied vertex outside \(C_{ry}\) belongs to
\(N_G(r)\cup N_G(y)\).  Finally, \(K_e\) contains neither fixed ban
anchor.  Any one-guard successor is still outside the ban; at a
deletion-witness attack every dominating unbanned response has smaller
rank, in particular every retained response supplied by
\(\mathcal F^\star\). \(\square\)

## 3. Exact collision dynamics

### Corollary 3.1 (reciprocal two-state hinge) — PROVED

If

\[
 wy\notin E(G),
\tag{3.1}
\]

then

\[
 y\in C_{qw},\qquad w\in C_{ry},
\tag{3.2}
\]

and the two maximum independent states

\[
 P=\{q,w,y\},\qquad R'=\{r,w,y\}
\tag{3.3}
\]

are retained.  They form a reciprocal two-state hinge:

\[
 P\xrightarrow[\text{attack }r]{q\to r}R',
 \qquad
 R'\xrightarrow[\text{attack }q]{r\to q}P,
\tag{3.4}
\]

with both responses unique.  Both states are either in the restricted
kernel or have rank at least one.

#### Proof

The memberships in (3.2) follow from \(qy,rw,ry,qw\notin E(G)\) and
(3.1).  Theorem 2.1 retains both states.  In \(P\), only \(q\) hits
\(r\); in \(R'\), only \(r\) hits \(q\).  This proves the unique
reciprocal moves.  Neither state contains \(v\) or \(t\), so Lemma 2.1
gives the rank statement. \(\square\)

### Corollary 3.2 (reciprocal four-state square) — PROVED

If

\[
 d\in C_{qw}\cap C_{ry},
\tag{3.5}
\]

then \(wy\in E(G)\), and the four maximum independent states

\[
\{q,w,d\},\quad
\{q,y,d\},\quad
\{r,y,d\},\quad
\{r,w,d\}
\tag{3.6}
\]

are retained.  Consecutive states in the displayed cyclic order are
joined by the unique moves

\[
 w\to y,\quad q\to r,\quad y\to w,\quad r\to q.
\tag{3.7}
\]

The reverse attacks give the reverse cycle.  This is a reciprocal
four-state square.  All four states are either in the restricted kernel
or have rank at least one.

#### Proof

If \(wy\) were a nonedge, then \(q,w,y,d\) would be an independent
four-set: \(d\) misses \(q,w,y\), and \(q,w,y\) would be pairwise
nonadjacent.  Thus \(\alpha(G)=3\) forces \(wy\in E(G)\).

Theorem 2.1 retains \(\{q,w,d\}\).  Attack \(y\).  The vertices \(q,d\)
miss \(y\), while \(w\) hits it, so the first move in (3.7) is unique
and retains \(\{q,y,d\}\).  Now attack \(r\), then \(w\), then \(q\).
At each step the displayed mover is the only guard adjacent to the
attacked vertex, using respectively \(qr,wy,qr\in E(G)\) and the four
common-nonneighbor incidences of \(d\).  Closure retains all four states
and the reverse attacks are symmetric.

Membership in \(C_{ry}\) excludes \(d=v,t\), so none of the four states
contains \(v\) or \(t\).  Apply Lemma 2.1. \(\square\)

### The separated branch

If \(wy\in E(G)\) and the two completion cliques are disjoint, the two
fans of Theorem 2.1 remain separate.  If also \(qt\in E(G)\), neither
fan can be supplied by any vertex already named in

\[
\{u,v,t,x,q,r,w,y\}.
\tag{3.8}
\]

Indeed, the positive edges in (1.5)--(1.12), together with \(wy,qt\),
exclude every named vertex from the corresponding common-nonneighbor
set.  The two nonempty disjoint fans therefore contribute at least two
additional vertices.  Their independent completion states lie beyond
rank zero by Theorem 2.1.

This is an order/structure statement, not a contradiction.

## 4. Exact separated-fan boundary control

Consider

```text
LEhbtnm~D]xln{
```

with

\[
\begin{aligned}
S&=\{0,5,6\},&x&=8,\\
u&=6,&v&=0,&t&=5,\\
q&=2,&r&=10,&w&=3,&y&=1.
\end{aligned}
\tag{4.1}
\]

The last two vertices have neighborhoods

\[
\begin{aligned}
N(11)&=\{0,1,4,5,7,8,10\},\\
N(12)&=\{0,2,3,4,5,6,7,8,9\}.
\end{aligned}
\tag{4.2}
\]

The standalone verifier reconstructs

\[
 |V|=13,\qquad |E|=50,
\tag{4.3}
\]

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)
 =(2,2,3,3,4),
 \qquad |\mathcal F^\star|=200.
\tag{4.4}
\]

The target is full at \(S\), and

\[
 B=\{3,7,9,10\}.
\tag{4.5}
\]

All three restricted kernels are empty.  Their deletion-round sizes in
color order \(0,5,6\) are

\[
\begin{array}{c|c}
0&(27,49,74,46)\\
5&(20,30,53,74,20)\\
6&(20,53,90,34).
\end{array}
\tag{4.6}
\]

For source color \(6\),

\[
\operatorname{rank}_6\{0,2,5\}
=
\operatorname{rank}_6\{0,1,5\}
=0.
\tag{4.7}
\]

The unique deleting attacks are respectively \(r=10\) and \(w=3\).
Thus the C-171 escape genuinely preserves rank zero.

Unlike MMV-027, the two equality-critical pairs do not dominate:

\[
C_{2,3}=\{11\},\qquad C_{10,1}=\{12\}.
\tag{4.8}
\]

The fans are disjoint, \(wy,qt\in E(G)\), and the unique exchanges retain

\[
\{2,3,11\},\qquad \{1,10,12\}.
\tag{4.9}
\]

Both states have color-6 deletion rank two.  Hence the exact local
effect is the rank rebound proved in Theorem 2.1, not survival of a
restricted kernel.

The complete dominating-pair list is

\[
\{0,8\},\quad\{5,12\},\quad\{6,10\},\quad\{11,12\}.
\tag{4.10}
\]

These are precisely where the control still violates \(\gamma=3\).
The control therefore shows that both completion fans, all three empty
kernels, and a rank-zero to rank-zero escape do not by themselves close
the equality proof.  It does not refute any statement assuming
\(\gamma=3\).

The graph6 SHA-256 is

```text
f589427f022392a6a5527951d65445e740fd63e76ecea1a870bd8658766c5428
```

and the sorted edge-list SHA-256 is

```text
511e0296f81a58a19134a4b118422e111fd5127889c8cfda159cec880cde7a58
```

The verifier decodes and re-encodes the graph, computes all five
parameters, constructs the literal greatest family, performs all four
restricted peelings used above, and checks every named unique response,
completion set, rank, and dominating pair.

## 5. Exact frontier after the theorem

### PROVED in this candidate

- The all-\(k\) Johnson-distance lower bound on restricted deletion rank.
- Both equality-mandated pair-completion sets are nonempty \(G\)-cliques.
- The first is covered by the closed neighborhood of \(t\), with a
  unique completion exchange away from the collision \(d=t\).
- The second is covered by \(v\) and every completion has a unique
  exchange from an explicitly retained source.
- Every second-fan completion, and every noncolliding first-fan
  completion, is in the restricted kernel or has deletion rank at least
  one.
- A minimum-rank second-fan state must exit its completion clique through
  an attack adjacent to \(r\) or \(y\), with strictly lower-rank
  unbanned retained responses.
- The \(wy\)-nonedge branch gives a reciprocal two-state hinge.
- An overlap of the completion cliques gives a reciprocal four-state
  square.

### EXACT finite control

- The graph in Section 4 realizes the collision-free separated branch,
  two singleton fans, all three empty kernels, and source/escape ranks
  \(0/0\), while both completion ranks are \(2\).

### OPEN

- Convert the positive-rank completion layer into a surviving restricted
  kernel or a contradiction.
- Use the four remaining non-dominating-pair obligations in (4.10)
  without assuming fresh witnesses.
- Eliminate the remaining positive-rank and anchor-restoration terminal
  branches.
- Prove a safe color, complete \(k=3\), or resolve the universal
  gamma--theta conjecture.
