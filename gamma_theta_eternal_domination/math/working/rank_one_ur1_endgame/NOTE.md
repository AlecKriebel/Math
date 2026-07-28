# The two rank-one \(ur=1\) rows collapse to one QQ1 normal form

## Status and exact boundary

Date: 2026-07-28 (PDT)

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\tag{0.1}
\]

let \(\mathcal K\) be the literal greatest eternal family of dominating
triples in the one-guard-moves model, and suppose

\[
 u\triangleright x,\qquad x\not\triangleright u.
\tag{0.2}
\]

Let

\[
 T=\{x,p,q\},\qquad B=\{u,p,q\},
\tag{0.3}
\]

where \(T\) is maximum independent and \(B\) has deletion rank one.
Suppose a deleting attack \(r\) on \(B\) satisfies

\[
 ur,pr,qr\in E(G),
\tag{0.4}
\]

and is in one of the two still-open \(ur=1\) rows of accepted C-150:

\[
\begin{array}{c|c}
\text{row}&N(r)\cap T\\ \hline
\mathrm{QQ1}&\{p,q\},\\
\mathrm{AQ1}&\{x,p,q\}.
\end{array}
\tag{0.5}
\]

For the three non-dominating successors at \(r\), let

\[
 a=y_u,\qquad b=y_p,\qquad c=y_q
\tag{0.6}
\]

be private witnesses.  In QQ1 we make the canonical choice

\[
 a=x.
\tag{0.7}
\]

This is always legitimate: \(x\) is adjacent to the removed guard \(u\)
and misses the successor \(\{r,p,q\}\).  In AQ1, every \(u\)-witness
\(a\) is fresh, because \(ar\notin E(G)\) whereas \(xr\in E(G)\).

The new conclusion is:

> **Theorem (rank-one \(ur=1\) normalization) — PROVED.**
> In both QQ1 and AQ1,
> \[
>  ab,ac,bc,xb,xc,up,uq\in E(G),
> \tag{0.8}
> \]
> with the repetitions \(a=x\) understood in QQ1.  Moreover
> \[
>  u\triangleright a,\qquad a\not\triangleright u.
> \tag{0.9}
> \]
> The state
> \[
>  S=\{a,p,q\}
> \tag{0.10}
> \]
> is maximum independent and retained, its complementary reverse state is
> the same rank-one state \(B\), and the same attack \(r\) is QQ1 relative
> to \(S\):
> \[
>  N(r)\cap S=\{p,q\},\qquad ur\in E(G).
> \tag{0.11}
> \]
> Thus every rank-one AQ1 collision produces a rank-one QQ1 collision.

There is also a sharpened completion obstruction:

> **Theorem (full-hit completion clique) — PROVED.**
> The common-nonneighbor set
> \[
>  C_{ar}=\{d\in V(G)-\{a,r\}:ad,rd\notin E(G)\}
> \tag{0.12}
> \]
> is a nonempty \(G\)-clique, and every \(d\in C_{ar}\) satisfies
> \[
>  dp,dq\in E(G).
> \tag{0.13}
> \]

The normalization is not an exclusion of QQ1.  The surviving canonical
QQ1 collision is exactly the row realized outside equality by the accepted
\(\gamma=2\) control `GEjbug`.  This note does not eliminate any
higher-rank collision, prove reciprocity, prove the complete \(k=3\)
case, or resolve the gamma--theta conjecture.

## 1. Private-witness ledger and collision audit

Rank one means that all three legal successors of \(B\) at \(r\) are
non-dominating:

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{private witness}\\ \hline
u&\{r,p,q\}&a,\\
p&\{u,r,q\}&b,\\
q&\{u,p,r\}&c.
\end{array}
\tag{1.1}
\]

The exact incidence supplied by the private-witness rule is

\[
\begin{array}{c|c|ccc}
 &\text{private edge}&\multicolumn{3}{c}{\text{missed successor}}\\ \hline
a&au&ar&ap&aq\\
b&bp&bu&br&bq\\
c&cq&cu&cr&cp.
\end{array}
\tag{1.2}
\]

Thus every private edge in the second column is present and every entry
in the last three columns is absent.

The vertices \(b,c\) are distinct from one another and from
\(u,x,p,q,r\).  For example, \(bp\in E(G)\), whereas \(cp,xp\notin
E(G)\), and \(br\notin E(G)\), whereas \(pr\in E(G)\).  The witness
\(a\) is distinct from \(u,p,q,r,b,c\).  It may equal \(x\) exactly in
QQ1.  The AQ1 edge \(xr\) and nonedge \(ar\) exclude that collision.

In AQ1, the retained independent state \(T\) dominates the fresh vertex
\(a\).  Since \(a\) misses \(p,q\), it follows that

\[
 ax\in E(G).
\tag{1.3}
\]

In QQ1 this is replaced by the identity \(a=x\), not by a loop.

## 2. The two transferred witness states

### Lemma 2.1 (private-witness transfer) — PROVED

The greatest family contains

\[
 M_p=\{x,b,q\},\qquad M_q=\{x,p,c\}.
\tag{2.1}
\]

#### Proof

We prove the first statement.  The equality collapse gives
\(i(G)=\alpha(G)=3\).  The independent pair \(\{u,b\}\) therefore
extends to a maximum independent triple

\[
 I=\{u,b,s\}.
\tag{2.2}
\]

Every independent triple belongs to \(\mathcal K\).  Accepted C-108
transports the active response \(u\to x\), giving

\[
 J=\{x,b,s\}\in\mathcal K.
\tag{2.3}
\]

If \(s=q\), then \(J=M_p\).  Otherwise attack the unoccupied vertex
\(q\).  The guards \(x,b\) miss \(q\), so domination and eternal closure
force the unique response \(s\to q\), producing \(M_p\).  The proof of
\(M_q\) is symmetric. \(\square\)

This proof does not infer any nonedge from a missing family transition.

## 3. A forced six-state chain

### Lemma 3.1 (the \(U,R,S\) chain) — PROVED

Put

\[
 U=\{u,b,c\},\qquad R=\{r,b,c\}.
\tag{3.1}
\]

Then

\[
 U,R,S\in\mathcal K.
\tag{3.2}
\]

In AQ1, where \(S=\{a,p,q\}\) is not \(T\), the state \(S\) is
independent and the unique response from \(S\) at \(x\) is \(a\to x\),
returning to \(T\).

#### Proof

Attack the unoccupied vertex \(b\) from
\(M_q=\{x,p,c\}\).  A \(c\to b\) successor
\(\{x,p,b\}\) misses \(q\).  If \(p\to b\) produces a retained state
\(\{x,b,c\}\), then its attack at \(u\) uniquely moves \(x\to u\), because
\(b,c\) miss \(u\), and reaches \(U\).  If \(x\to b\) produces a retained
state \(\{b,p,c\}\), then that state's attack at \(u\) can only move
\(p\to u\) and again reaches \(U\); if \(pu\) is absent, the intermediate
state is already non-dominating at \(u\).  These are all possible movers,
so closure of \(M_q\) forces \(U\in\mathcal K\).

At the unoccupied attack \(r\) from \(U\), the guards \(b,c\) miss \(r\)
and \(ur\) is an edge.  The unique response is

\[
 U\xrightarrow{u\to r}R.
\tag{3.3}
\]

In QQ1, \(a=x\) and \(S=T\), so only the AQ1 case remains.  The state
\(R\) must answer the attack at the fresh vertex \(a\).  Its guard \(r\)
misses \(a\), so choose a retained response by \(b\) or \(c\).
If \(b\to a\), three subsequent unique attacks give

\[
 \{r,b,c\}
 \xrightarrow{b\to a}
 \{r,a,c\}
 \xrightarrow{r\to p}
 \{p,a,c\}
 \xrightarrow{c\to q}
 \{p,a,q\}=S.
\tag{3.4}
\]

If \(c\to a\), the symmetric path is

\[
 \{r,b,c\}
 \xrightarrow{c\to a}
 \{r,a,b\}
 \xrightarrow{r\to q}
 \{q,a,b\}
 \xrightarrow{b\to p}
 \{q,a,p\}=S.
\tag{3.5}
\]

Every displayed attack is unoccupied, and the stated uniqueness follows
from (1.2), \(pq\notin E(G)\), and \(pr,qr\in E(G)\).
Finally, \(S\) is independent by (1.2), and its attack at \(x\) uniquely
moves \(a\), by (1.3), returning to \(T\). \(\square\)

## 4. Two private-marker ridge arguments

### Lemma 4.1 (the fresh witness hits both side witnesses) — PROVED

In AQ1,

\[
 ab,ac\in E(G).
\tag{4.1}
\]

#### Proof

The attack at \(a\) from \(R\) has a retained response by \(b\) or \(c\).
Suppose first that it uses \(b\to a\), so \(ab\in E(G)\), and assume for
contradiction that \(ac\notin E(G)\).  The last four states of (3.4),

\[
 \{r,a,c\},\quad
 \{p,a,c\},\quad
 \{p,a,q\},\quad
 \{p,x,q\}=T,
\tag{4.2}
\]

are independent triples joined by ridge exchanges.  The composite
canonical permutation maps

\[
 r\longmapsto p,\qquad c\longmapsto q,\qquad a\longmapsto x
\tag{4.3}
\]

and fixes \(b\).  Lemma 2.1 says

\[
 p\in L_T(b),
\tag{4.4}
\]

because \(T-p+b=M_p\in\mathcal K\).  Accepted C-064 path covariance
therefore transports (4.4) backwards to

\[
 r\in L_{\{r,a,c\}}(b).
\tag{4.5}
\]

This is impossible because \(rb\notin E(G)\).

Thus a retained \(b\to a\) branch forces \(ac\in E(G)\).  Symmetrically,
a retained \(c\to a\) branch forces \(ab\in E(G)\), using the path in
(3.5) and the marker \(q\in L_T(c)\).  The mover edge in either retained
branch supplies one of \(ab,ac\), and the marker argument supplies the
other. \(\square\)

### Lemma 4.2 (the QQ collision hits both side witnesses) — PROVED

In QQ1, with the canonical choice \(a=x\),

\[
 xb,xc\in E(G).
\tag{4.6}
\]

#### Proof

Assume \(xb\notin E(G)\).  At the attack \(x\) from \(R\), both \(r\)
and \(b\) miss \(x\).  Eternal closure therefore forces \(cx\in E(G)\)
and retains

\[
 A=\{r,b,x\}.
\tag{4.7}
\]

The three states

\[
 A=\{r,b,x\},\qquad
 M_p=\{q,b,x\},\qquad
 T=\{q,p,x\}
\tag{4.8}
\]

are independent.  The first ridge exchange is forced by the unique attack
\(q\) on \(A\), moving \(r\to q\); the second is the ridge exchange
\(b\to p\).  Their composite permutation maps \(r\) to \(q\) and fixes
the outside target \(c\).  Since

\[
 q\in L_T(c)
\tag{4.9}
\]

by Lemma 2.1, C-064 path covariance would force

\[
 r\in L_A(c),
\tag{4.10}
\]

contrary to \(rc\notin E(G)\).  Hence \(xb\in E(G)\).  Interchanging
\((p,b)\) with \((q,c)\) proves \(xc\in E(G)\). \(\square\)

## 5. The named core saturates

Put

\[
 W=\{x,b,c\}.
\tag{5.1}
\]

### Lemma 5.1 (the \(W\)-state is excluded) — PROVED

In both rows,

\[
 W\notin\mathcal K.
\tag{5.2}
\]

#### Proof

In QQ1, all three guards \(x,b,c\) miss \(r\), so \(W\) is
non-dominating.

In AQ1, Lemmas 4.1 and the edge \(ax\) make all three guards of \(W\)
adjacent to the unoccupied target \(a\).  The three possible successors
are nevertheless non-dominating:

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{missed vertex}\\ \hline
x&\{a,b,c\}&r,\\
b&\{x,a,c\}&p,\\
c&\{x,a,b\}&q.
\end{array}
\tag{5.3}
\]

Thus \(W\) has no retained response to the attack at \(a\). \(\square\)

### Lemma 5.2 (both side witnesses hit \(x\)) — PROVED

In AQ1,

\[
 xb,xc\in E(G).
\tag{5.4}
\]

Together with Lemma 4.2, (5.4) holds in both rows.

#### Proof

Assume \(xb\notin E(G)\) and attack \(b\) from
\(M_q=\{x,p,c\}\).  The \(p\)-successor is \(W\), excluded by Lemma
5.1.  A possible \(c\)-successor is \(\{x,p,b\}\), which misses \(q\).
The guard \(x\) is ineligible by the assumed nonedge.  Hence \(M_q\)
has no retained response, a contradiction.  The proof of \(xc\in E(G)\)
uses the attack at \(c\) from \(M_p\). \(\square\)

### Lemma 5.3 (the side witnesses are adjacent) — PROVED

In both rows,

\[
 bc\in E(G).
\tag{5.5}
\]

#### Proof

Suppose \(bc\notin E(G)\).  Then \(U=\{u,b,c\}\) is an independent
triple.  The active orientation \(u\triangleright x\) and C-108 force

\[
 U-u+x=W\in\mathcal K,
\tag{5.6}
\]

contrary to Lemma 5.1. \(\square\)

### Lemma 5.4 (the reverse endpoint has both side edges) — PROVED

In both rows,

\[
 up,uq\in E(G).
\tag{5.7}
\]

#### Proof

Suppose \(up\notin E(G)\) and attack \(b\) from
\(M_q=\{x,p,c\}\).  By Lemmas 5.2 and 5.3 all three guards are eligible,
but all three successors are excluded:

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{obstruction}\\ \hline
x&\{b,p,c\}&\text{misses }u,\\
p&W&\text{Lemma 5.1},\\
c&\{x,p,b\}&\text{misses }q.
\end{array}
\tag{5.8}
\]

This contradicts retention of \(M_q\).  Hence \(up\in E(G)\).
The proof of \(uq\in E(G)\) attacks \(c\) from \(M_p\). \(\square\)

Equations (4.1), (4.6), (5.4), (5.5), and (5.7) prove the complete
named saturation (0.8).

## 6. AQ1 recreates QQ1

### Lemma 6.1 (the new active orientation) — PROVED

In AQ1,

\[
 u\triangleright a,\qquad a\not\triangleright u.
\tag{6.1}
\]

#### Proof

Extend the independent pair \(\{u,b\}\) to a maximum independent triple

\[
 I=\{u,b,s\}.
\tag{6.2}
\]

The active response \(u\to x\) gives

\[
 J=\{x,b,s\}\in\mathcal K.
\tag{6.3}
\]

Attack the unoccupied vertex \(a\) from \(J\).  The successor from
\(s\to a\), if that edge exists, is \(\{x,b,a\}\), which misses \(q\).
The successor from \(b\to a\) is

\[
 E=\{x,a,s\}.
\tag{6.4}
\]

If \(sq\notin E(G)\), then \(E\) misses \(q\).  If \(sq\in E(G)\), its
attack at \(q\) uniquely moves \(s\) and reaches
\(\{x,a,q\}\), which misses \(p\).  Thus \(E\notin\mathcal K\) in
either case.

The only retained response at \(a\) is consequently \(x\to a\), giving

\[
 D=\{a,b,s\}=I-u+a\in\mathcal K.
\tag{6.5}
\]

Since \(ua\in E(G)\), this proves \(u\triangleright a\).

On the other hand, \(S=\{a,p,q\}\) is independent.  At its attack \(u\),
the \(a\)-successor is exactly the omitted state \(B\).  C-108 says the
ability of \(a\) to answer \(u\) is invariant over all maximum independent
triples containing \(a\), so \(a\not\triangleright u\). \(\square\)

In QQ1, (6.1) is the original assumption (0.2), because \(a=x\).

### Proof of rank-one normalization

The named saturation was proved in Section 5.  In QQ1, \(S=T\).  In
AQ1, Lemma 3.1 puts the independent state \(S\) in \(\mathcal K\), and
Lemma 6.1 supplies the one-sided active edge \(u\triangleright a\).

In both cases,

\[
 ar,ap,aq\notin E(G),\qquad ur,pr,qr\in E(G).
\tag{6.6}
\]

The complementary reverse endpoint of \(S\) is

\[
 S-a+u=\{u,p,q\}=B.
\tag{6.7}
\]

It is the same state of deletion rank one.  The same attack \(r\) has
the same three non-dominating successors and is QQ1 relative to \(S\).
This proves (0.9)--(0.11) and the normalization theorem. \(\square\)

## 7. Every \(a,r\)-completion fully hits \(p,q\)

### Proof of the full-hit completion theorem

The pair \(\{a,r\}\) is independent.  Since \(i(G)=\alpha(G)=3\), it
extends to at least one maximum independent triple

\[
 I=\{a,r,d\}.
\tag{7.1}
\]

Any two distinct completion vertices \(d,e\in C_{ar}\) must be adjacent;
otherwise \(\{a,r,d,e\}\) would be an independent set of size four.
Thus \(C_{ar}\) is nonempty and is a \(G\)-clique.

Recall the independent state \(S=\{a,p,q\}\).  It dominates \(d\), while
\(ad\notin E(G)\), so \(d\) is adjacent to at least one of \(p,q\).
We show that it cannot hit exactly one.

First note the two private markers

\[
 p\in L_S(b),\qquad q\in L_S(c).
\tag{7.2}
\]

In QQ1 this is Lemma 2.1 with \(S=T\).  In AQ1, the independent states
\(T=\{x,p,q\}\) and \(S=\{a,p,q\}\) share the ridge \(\{p,q\}\);
C-064 transports the same two markers across the exchange \(x\leftrightarrow
a\).

Suppose \(dp\in E(G)\) and \(dq\notin E(G)\).  The two unique attacks

\[
 S=\{a,p,q\}
 \xrightarrow{p\to d}
 \{a,d,q\}
 \xrightarrow{q\to r}
 \{a,d,r\}=I
\tag{7.3}
\]

form an independent ridge path.  Its composite permutation maps \(q\)
to \(r\) and fixes the outside target \(c\).  The second marker in (7.2)
would therefore force

\[
 r\in L_I(c),
\tag{7.4}
\]

contrary to \(rc\notin E(G)\).

If \(dq\in E(G)\) and \(dp\notin E(G)\), the symmetric path

\[
 S
 \xrightarrow{q\to d}
 \{a,p,d\}
 \xrightarrow{p\to r}
 I
\tag{7.5}
\]

transports the marker \(p\in L_S(b)\) to the impossible incidence
\(r\in L_I(b)\).  Therefore every completion \(d\) hits both \(p,q\),
proving (0.13). \(\square\)

## 8. Dependency, model, and scope audit

The proof depends on:

1. the equality collapse \(i=\alpha=3\);
2. accepted C-010, which retains every independent triple;
3. accepted C-064 exact response covariance along independent ridge paths;
4. accepted C-108 active-star transport; and
5. accepted C-150's rank-one private-witness rule and QQ1/AQ1 row table.

It does not use complement coloring, a finite-order computation, an
unproved symmetry assumption, or any inference from an omitted family
transition to a graph nonedge.

The collision \(a=x\) is used only in QQ1 and is handled explicitly.
No attack is made at an occupied vertex.  Every dynamic exclusion in
Sections 3, 5, and 6 ends in a displayed non-dominating state or in a
further unoccupied attack whose complete one-guard response set is
displayed.

The discovery SAT script which originally assigned \(y_u\) a fresh label
does **not** cover the QQ1 collision \(a=x\).  None of its UNSAT outputs
is used here.  The theorem is symbolic and treats the collision directly.

## 9. Exact remaining gate

After this theorem, rank one has only the canonical QQ1 normal form:

\[
\begin{gathered}
 S=\{a,p,q\}\text{ independent},\quad
 B=\{u,p,q\}\text{ of rank one},\\
 u\triangleright a,\quad a\not\triangleright u,\quad
 N(r)\cap S=\{p,q\},\quad ur\in E(G),\\
 \{a,b,c\}\text{ a triangle},\quad
 up,uq\in E(G),\\
 C_{ar}\ne\varnothing,\quad C_{ar}\text{ a clique complete to }\{p,q\}.
\end{gathered}
\tag{9.1}
\]

What is not proved is that (9.1) is impossible under \(\gamma=3\).
Closing that self-similar full-hit QQ1 core, or extracting a lower-rank
reverse endpoint from it, remains the exact rank-one collision gate.

### Complement-core handoff

For the canonical QQ1 core, put \(H=\overline G\) and retain the seven
vertices

\[
 \{u,x,p,q,r,b,c\}.
\tag{9.2}
\]

The complete induced \(H\)-edge ledger is

\[
\begin{aligned}
 E(H[\{u,x,p,q,r,b,c\}])
 ={}&
 \{xp,xq,pq\}\\
 &{}\cup\{rb,bu,uc,cr\}\\
 &{}\cup\{xr,pc,qb\}.
\end{aligned}
\tag{9.3}
\]

Thus \(xpq\) is the root triangle, \(rbucr\) is a bottom 4-cycle, and
\(xr,pc,qb\) are matching spokes.  There are no other core complement
edges.  Each of the seven nonroot edges

\[
 xr,\ rb,\ bu,\ uc,\ cr,\ pc,\ qb
\tag{9.4}
\]

has no common \(H\)-neighbor inside the seven-vertex core.  The static
condition \(\gamma(G)=\alpha(G)=3\) requires every vertex pair to have an
external common \(H\)-neighbor, so each edge in (9.4) requires an external
triangle completion.  For the spoke \(xr\), the full-hit completion
theorem says more: every such external completion is nonadjacent in \(H\)
to both \(p,q\).

This ledger is a handoff to the complement-link and response-holonomy
lanes, not a contradiction.

### Sharp fixed-graph boundary control

The graph

\[
 G_0=\texttt{Hslaghb}
\tag{9.5}
\]

has order \(9\), size \(17\), contains the canonical seven-vertex core
on labels

\[
 (u,x,p,q,r,b,c)=(0,1,2,3,4,5,6),
\tag{9.6}
\]

and has exact parameters

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G_0)=(3,3,3,4,4).
\tag{9.7}
\]

Thus the saturated core is compatible with all static equality
conditions, but the one-guard triple kernel is empty.  Two structurally
independent campaign evaluators agree on (9.7), and the local control
checker independently recomputes the empty greatest triple kernel.
This fixed graph is a sharp logical boundary, not a counterexample and
not an order-minimality claim.
