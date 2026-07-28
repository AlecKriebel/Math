# The canonical QQ1 completion is saturated and has no cold witness

## Status and exact scope

Date: 2026-07-28 (PDT)

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\tag{0.1}
\]

let \(\mathcal K\) be the literal greatest one-guard eternal family of
dominating triples, and retain the accepted C-158 canonical rank-one QQ1
normal form.  Thus

\[
 T=\{x,p,q\}\in\mathcal K,\qquad
 B=\{u,p,q\}\notin\mathcal K,\qquad \rho(B)=1,
\tag{0.2}
\]

\[
 u\mathrel{\triangleright}x,\qquad
 x\not\mathrel{\triangleright}u,
\tag{0.3}
\]

and \(r\) is the rank-one deleting attack.  The two side private witnesses
are \(b,c\).  The exact named incidence is

\[
\begin{array}{c|l}
\text{\(G\)-edges}
 &ux,ur,pr,qr,pb,qc,xb,xc,bc,up,uq,\\
\text{\(G\)-nonedges}
 &xp,xq,pq,xr,\ bu,br,bq,\ cu,cr,cp .
\end{array}
\tag{0.4}
\]

Accepted C-158 also gives

\[
 U=\{u,b,c\}\in\mathcal K
\tag{0.5}
\]

and a nonempty \(G\)-clique

\[
 C_{xr}=\{d\notin\{x,r\}:dx,dr\notin E(G)\}
\tag{0.6}
\]

whose members are adjacent to \(p,q\).

This note proves three further conclusions.

1. Every \(d\in C_{xr}\) is adjacent to all four vertices
   \(p,q,b,c\).
2. Every triple \(\{u,x,d\}\), \(d\in C_{xr}\), dominates \(G\).
   Equivalently, no vertex outside this triple can miss all three of
   \(u,x,d\).
3. The reverse state \(\{u,r,d\}\) and two mixed states form an exact
   deletion-rank diamond of height at most three.

Consequently, if \(\gamma(G)=3\), the pair \(\{u,d\}\) has an external
missed vertex \(w\), but every such vertex is **hot**:

\[
 wu,wd\notin E(G),\qquad wx,wr\in E(G),\qquad
 wb\in E(G)\ \text{or}\ wc\in E(G).
\tag{0.7}
\]

The two accepted \(\gamma=2\) QQ1 controls stop exactly before this new
layer: in each, \(\{u,d\}\) dominates.  The hot layer is not eliminated
here.  This note does not prove reciprocity, complete \(k=3\), or the
gamma--theta conjecture.

## 1. Every completion also hits both side witnesses

Fix an arbitrary

\[
 d\in C_{xr}.
\tag{1.1}
\]

Then

\[
 I_d=\{x,r,d\}
\tag{1.2}
\]

is an independent triple, hence belongs to \(\mathcal K\).  Its
complementary reverse endpoint is

\[
 R_d=I_d-x+u=\{u,r,d\}.
\tag{1.3}
\]

Accepted C-143 says that \(R_d\) dominates \(G\).  Both \(u\) and \(r\)
miss \(b\), by (0.4), so domination of \(b\) forces

\[
 db\in E(G).
\tag{1.4}
\]

The same argument at \(c\) gives

\[
 dc\in E(G).
\tag{1.5}
\]

Together with C-158, this proves:

> **Theorem 1.1 (four-hit completion clique) — PROVED.**
> The set \(C_{xr}\) is a nonempty \(G\)-clique complete to
> \(\{p,q,b,c\}\).

The use of C-143 is essential.  The conclusion does not follow merely
from the static fact that \(\{x,r,d\}\) is independent.

## 2. No completion has a cold common witness

### Theorem 2.1 (completion-triple domination) — PROVED

For every \(d\in C_{xr}\),

\[
 \boxed{\{u,x,d\}\text{ dominates }G.}
\tag{2.1}
\]

#### Proof

Suppose instead that an outside vertex \(w\) misses all three guards:

\[
 wu,wx,wd\notin E(G).
\tag{2.2}
\]

Call such a vertex a **cold witness**.  The triple

\[
 J_d=\{x,w,d\}
\tag{2.3}
\]

is independent and therefore retained.  Its \(x\)-successor at the
unoccupied attack \(u\) is

\[
 J_d-x+u=\{u,w,d\}.
\tag{2.4}
\]

It is not retained, because (0.3) and accepted C-108 say that \(x\)
cannot answer an attack at \(u\) from any maximum independent triple
containing \(x\).  The guard \(w\) is graph-ineligible by (2.2).
Eternal closure of \(J_d\) consequently forces the only remaining
response:

\[
 d\longrightarrow u,\qquad
 \{x,w,u\}\in\mathcal K.
\tag{2.5}
\]

In particular \(du\in E(G)\), and the exact family-response list is

\[
 L_{J_d}(u)=\{d\}.
\tag{2.6}
\]

The independent triples \(I_d=\{x,r,d\}\) and
\(J_d=\{x,w,d\}\) share the ridge \(\{x,d\}\).  Accepted C-064 transports
their complete response lists under the transposition \(r\leftrightarrow
w\).  Since \(d\) is fixed by that transposition, (2.6) gives

\[
 L_{I_d}(u)=\{d\}.
\tag{2.7}
\]

In particular the \(r\)-successor

\[
 A=\{u,x,d\}
\tag{2.8}
\]

is not in \(\mathcal K\).  Notice that this is a family omission, not a
graph nonedge.

Now attack the unoccupied vertex \(d\) from the retained state
\(U=\{u,b,c\}\).  All three guards are graph-eligible: \(du\) follows
from (2.5), while \(db,dc\) follow from Theorem 1.1.

The \(u\)-successor

\[
 \{d,b,c\}
\tag{2.9}
\]

misses \(r\), because \(dr,br,cr\notin E(G)\).

The \(b\)-successor

\[
 D_b=\{u,d,c\}
\tag{2.10}
\]

cannot be retained.  Attack the unoccupied vertex \(x\).  The guard
\(d\) misses \(x\), and the other two possible moves have successors

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{obstruction}\\ \hline
u&\{x,d,c\}&\text{misses }r,\\
c&\{u,d,x\}=A&\text{omitted by (2.7).}
\end{array}
\tag{2.11}
\]

Thus \(D_b\) has no retained response at \(x\).  Symmetrically, the
\(c\)-successor

\[
 D_c=\{u,b,d\}
\tag{2.12}
\]

has, at the attack \(x\), only the non-dominating successor
\(\{x,b,d\}\), which misses \(r\), and the same omitted state \(A\).
Therefore \(D_c\notin\mathcal K\).

All three possible responses from \(U\) at \(d\) have now been excluded:
one is non-dominating and the other two fail at a displayed further
unoccupied attack.  This contradicts \(U\in\mathcal K\).  Hence no cold
witness exists, proving (2.1). \(\square\)

### Model audit

The proof never converts the missing transition (2.8) into a graph
nonedge.  It uses the omission only as one branch obstruction at the
later attack \(x\).  Every graph-ineligible mover and every
non-dominating successor is identified separately.

The only attacks are at \(u,d,x\), and each is unoccupied in its source
state.  Exactly one guard moves along one graph edge at every retained
transition.

## 3. The forced hot witness layer

Assume the full equality hypothesis (0.1).  Since \(\gamma(G)=3\), no
pair dominates.  For every \(d\in C_{xr}\), choose a vertex

\[
 w\notin\{u,d\},\qquad wu,wd\notin E(G).
\tag{3.1}
\]

Theorem 2.1 forces

\[
 wx\in E(G).
\tag{3.2}
\]

The reverse state \(R_d=\{u,r,d\}\) dominates.  Its guards \(u,d\) miss
\(w\), so

\[
 wr\in E(G).
\tag{3.3}
\]

Finally \(U=\{u,b,c\}\) dominates \(w\), while \(u\) misses it.  Hence

\[
 wb\in E(G)\quad\text{or}\quad wc\in E(G).
\tag{3.4}
\]

All such \(w\) are outside the canonical seven-vertex core and outside
\(\{d\}\): each named collision is excluded by one of (0.4), (1.4), or
(1.5).  This proves (0.7).

There are two additional useful formulations of Theorem 2.1.

1. Every outside common nonneighbor of \(u,x\) is adjacent to every
   \(d\in C_{xr}\).
2. Every outside common nonneighbor of \(x,d\) is adjacent to \(u\).

Thus the three pair-witness classes around \(\{u,x,d\}\) cannot overlap
outside that triple.

### Conditional repair-square self-similarity

If, in addition,

\[
 ud\notin E(G),
\tag{3.5}
\]

then the hot witness in (3.1) gives two independent triples

\[
 K=\{u,d,w\},\qquad I_d=\{x,d,r\}.
\tag{3.6}
\]

Activity \(u\triangleright x\) retains

\[
 K-u+x=\{x,d,w\}.
\tag{3.7}
\]

Since \(wr\in E(G)\), the independent state \(I_d\) witnesses

\[
 r\mathrel{\triangleright}w.
\tag{3.8}
\]

On the other hand, a \(w\to r\) response from the independent state
\(K\) would land in the omitted reverse endpoint

\[
 K-w+r=\{u,d,r\}=R_d,
\tag{3.9}
\]

so

\[
 w\not\mathrel{\triangleright}r.
\tag{3.10}
\]

This is exactly the accepted fixed-pivot repair square with pivot \(d\):
in the complement link \(L_d\), the two completion edges are \(u-w\)
and \(x-r\).  Accepted C-161 conserves the tracked omitted-corner rank.
Thus this branch recreates asymmetry at the same rank; it is not a
descent and not a contradiction.

When \(ud\in E(G)\), the set \(K\) in (3.6) is not independent and this
repair-square conclusion is not asserted.

## 4. Exact deletion-rank diamond

Continue with arbitrary \(d\in C_{xr}\), and put

\[
 R_d=\{u,r,d\},\qquad
 P_d=\{u,p,d\},\qquad
 Q_d=\{u,q,d\}.
\tag{4.1}
\]

By C-143 and C-108, \(R_d\) dominates but does not survive.  Let

\[
 h=\rho(R_d).
\tag{4.2}
\]

The endpoint triples \(T=\{x,p,q\}\) and
\(I_d=\{x,r,d\}\) share \(x\) and differ in two positions.  C-146
therefore gives

\[
 1\le h\le3,
\tag{4.3}
\]

because \(\rho(B)=1\).

The attack at \(p\) from \(R_d\) has three graph-eligible movers, but two
successors are rank zero:

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{missed vertex}\\ \hline
u&\{p,r,d\}&x,\\
r&P_d&\text{not prescribed},\\
d&\{u,r,p\}&c.
\end{array}
\tag{4.4}
\]

Thus \(P_d\) is the only possibly positive-rank successor at \(p\).
Symmetrically, \(Q_d\) is the only possibly positive-rank successor at
the attack \(q\) from \(R_d\).

Next attack \(q\) from \(P_d\).  The only eligible movers are \(u,d\):

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{rank}\\ \hline
u&\{p,q,d\}&0\quad(\text{misses }x),\\
d&B=\{u,p,q\}&1.
\end{array}
\tag{4.5}
\]

Consequently

\[
 \rho(P_d)\le2.
\tag{4.6}
\]

The symmetric attack \(p\) from \(Q_d\) gives

\[
 \rho(Q_d)\le2.
\tag{4.7}
\]

If \(h\ge2\), membership \(R_d\in\mathcal K_{h-1}\) and the unique
possibly positive successors in (4.4) force

\[
 P_d,Q_d\in\mathcal K_{h-2}.
\tag{4.8}
\]

Combining (4.3), (4.6)--(4.8) gives the exact top case:

\[
 \boxed{
 h=3\quad\Longrightarrow\quad
 \rho(P_d)=\rho(Q_d)=2,
 }
\tag{4.9}
\]

and both mixed states feed uniquely into the original rank-one state
\(B\).  More generally,

\[
 h\le1+\min\{\rho(P_d),\rho(Q_d)\}.
\tag{4.10}
\]

The two C-159 boundary controls attain

\[
 (\rho(B),\rho(P_d),\rho(Q_d),\rho(R_d))=(1,2,2,3).
\tag{4.11}
\]

Thus neither the two-level diamond nor the maximal C-146 rank jump is
itself contradictory.  Under \(\gamma=3\), the genuinely new obligation
is the external hot layer from Section 3.

## 5. Relation to complement-link separation

Accepted C-161 says that for every common complement neighbor \(z\) of
the asymmetric endpoints \(u,x\), those endpoints lie in different
components of the complement link \(L_z\).  Applied to the canonical
seven-vertex complement core, it yields the four path caps

\[
\begin{aligned}
 zb\in E(G)&\ \text{or}\ zq\in E(G),\\
 zb\in E(G)&\ \text{or}\ zr\in E(G),\\
 zc\in E(G)&\ \text{or}\ zp\in E(G),\\
 zc\in E(G)&\ \text{or}\ zr\in E(G).
\end{aligned}
\tag{5.1}
\]

Theorem 2.1 adds that every such outside \(z\) is adjacent to every
completion \(d\in C_{xr}\).  Hence the completion vertices are expelled
from the relevant complement links instead of joining their two
separated components.  The link caps and the four-hit completion theorem
are therefore compatible; they do not by themselves close QQ1.

The remaining universal gate is now sharper:

> eliminate the external hot-witness layer (0.7), or show that its
> iteration through the separated complement-link components forces a
> dominating pair or a forbidden rank-one return.

This is a strictly smaller target than the original seven-vertex QQ1
core, but it remains open.

## 6. Dependencies and reproduction

The symbolic proof uses only the accepted results:

1. C-010, to retain every independent triple;
2. C-064, for exact response covariance across one independent ridge;
3. C-108, for the inactive reverse orientation;
4. C-143, to make every complementary reverse endpoint dominate;
5. C-146, for the rank bound;
6. C-158, for the canonical QQ1 normal form and initial completion
   theorem; and
7. C-161 only in Sections 3 and 5, not in Theorems 1.1, 2.1, or the
   rank diamond.

The finite bookkeeping checker audits all \(16\) assignments to the four
incidences of a hypothetical cold witness with \(p,q,b,c\).  It verifies
that none changes the forced response lists or the terminal attack on
\(U\).  It also decodes both C-159 controls and checks their exact
completion vertex, four-hit saturation, rank diamond, and
\(\{u,d\}\)-dominating boundary.

From the campaign root:

```text
sh math/working/qq1_completion_dynamics/verify_strict.sh
```

