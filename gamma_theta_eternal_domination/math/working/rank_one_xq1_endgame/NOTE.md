# The rank-one XQ1 collision is impossible

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
Suppose an attack \(r\) deleting \(B\) lies in the XQ1 row of accepted
C-150:

\[
 N(r)\cap T=\{x,p\},\qquad ur\in E(G).
\tag{0.4}
\]

The new conclusion is:

> **Theorem (rank-one XQ1 exclusion) — PROVED.**
> No configuration satisfying (0.1)--(0.4) exists.

The proof uses the two private witnesses and four independent facets
already forced by C-150.  Exact ridge response-covariance turns that path
into one omitted mixed state.  Completing one independent pair at the
first private witness then forces the same state into \(\mathcal K\).

This closes only rank-one XQ1.  It does not close QQ, AQ, XQ0 above rank
one, any higher-rank collision, greatest-family reciprocity, complete
\(k=3\), or the gamma--theta conjecture.

## 1. Accepted XQ1 data and the complete named incidence

The legal movers from \(B\) at \(r\) are \(u,p\).  Since \(B\) has rank
one, the two successors

\[
 C_u=\{r,p,q\},\qquad C_p=\{u,r,q\}
\tag{1.1}
\]

are non-dominating.  Let

\[
 z=y_u,\qquad y=y_p
\tag{1.2}
\]

be the private witnesses supplied by C-150.  Thus

\[
\begin{array}{c|cccc}
 &\text{private edge}&\multicolumn{3}{c}{\text{missed successor}}\\ \hline
y&yp&yu&yr&yq\\
z&zu&zr&zp&zq
\end{array}
\tag{1.3}
\]

has the private edge present and the three entries in the last columns
absent.

Accepted C-150 further gives

\[
 xy,xz,yz\in E(G)
\tag{1.4}
\]

and the retained independent-facet path

\[
\begin{aligned}
 J_y&=\{y,r,q\},\\
 J_z&=\{z,r,q\},\\
 K_z&=\{z,p,q\},\\
 T&=\{x,p,q\},
\end{aligned}
\qquad
J_y\longleftrightarrow J_z
\longleftrightarrow K_z
\longleftrightarrow T.
\tag{1.5}
\]

The three ridge exchanges are respectively

\[
 y\leftrightarrow z,\qquad
 r\leftrightarrow p,\qquad
 z\leftrightarrow x.
\tag{1.6}
\]

### Lemma 1.1 (collision and pair audit) — PROVED

The seven vertices

\[
 u,x,p,q,r,y,z
\tag{1.7}
\]

are pairwise distinct.  Among their \(21\) unordered pairs, exactly nine
are forced edges, ten are forced nonedges, and only \(up,uq\) remain
undetermined:

\[
\begin{array}{c|ccccccc}
 &u&x&p&q&r&y&z\\ \hline
u&-&1&?&?&1&0&1\\
x&1&-&0&0&1&1&1\\
p&?&0&-&0&1&1&0\\
q&?&0&0&-&0&0&0\\
r&1&1&1&0&-&0&0\\
y&0&1&1&0&0&-&1\\
z&1&1&0&0&0&1&-
\end{array}
\tag{1.8}
\]

Here \(1\) means a graph edge, \(0\) a graph nonedge, and \(?\) an
undetermined pair.

#### Proof

The endpoint state \(T\) gives

\[
 xp=xq=pq=0.
\]

The active edge and XQ1 row give

\[
 ux=ur=xr=pr=1,\qquad qr=0.
\]

The private-witness incidence (1.3) and C-150 consequences (1.4) supply
all remaining entries of (1.8).

The vertices \(u,x,p,q,r\) are distinct by the state and attack
definitions; in particular \(r\ne x\), since \(rp=1\) but \(xp=0\).
The witness \(y\) is outside \(C_p\), differs from its removed guard
\(p\) because \(pr=1\) but \(yr=0\), and differs from \(x\) because
\(yp=1\) but \(xp=0\).  Similarly \(z\) is outside \(C_u\), differs
from \(u\) because \(ur=1\) but \(zr=0\), and differs from \(x\)
because \(xr=1\) but \(zr=0\).  Finally \(y\ne z\), since \(yp=1\)
while \(zp=0\).  This exhausts all named collisions. \(\square\)

## 2. Covariance omits the missing sixth grid state

For a retained independent state \(I\) and an unoccupied target \(v\),
write

\[
 L_I(v)=\{g\in I:I-g+v\in\mathcal K\}.
\tag{2.1}
\]

### Lemma 2.1 (exact transported singleton) — PROVED

The response list at \(T\) for an attack at \(y\) is

\[
 \boxed{L_T(y)=\{x\}.}
\tag{2.2}
\]

Consequently

\[
 K_y=\{y,p,q\}\in\mathcal K,
\qquad
 M=\{x,y,q\}\notin\mathcal K.
\tag{2.3}
\]

#### Proof

Start at the second facet

\[
 J_z=\{z,r,q\}.
\]

The target \(y\) is unoccupied.  Equations (1.3)--(1.4) give

\[
 zy\in E(G),\qquad ry,qy\notin E(G).
\]

The only adjacency-eligible guard is therefore \(z\), and its successor
is the retained facet \(J_y\).  Hence

\[
 L_{J_z}(y)=\{z\}.
\tag{2.4}
\]

The independent facets \(J_z,K_z\) share \(\{z,q\}\) and exchange
\(r,p\).  The target \(y\) lies outside both states.  Accepted C-064
ridge response-covariance therefore transports (2.4) to

\[
 L_{K_z}(y)=\{z\}.
\tag{2.5}
\]

Next \(K_z,T\) share \(\{p,q\}\) and exchange \(z,x\); again \(y\) is
outside both.  A second application of C-064 gives (2.2).

The \(x\)-successor in (2.2) is \(K_y\), while the excluded
\(p\)-successor is

\[
 T-p+y=\{x,y,q\}=M.
\]

This proves (2.3). \(\square\)

Together with the C-150 state

\[
 D=T-p+r=\{x,r,q\}\in\mathcal K,
\tag{2.6}
\]

Lemma 2.1 fills the exact retained \(3\times2\) grid over \(q\):

\[
 \boxed{
 \{a,b,q\}\in\mathcal K
 \quad
 (a\in\{x,y,z\},\ b\in\{p,r\}).
 }
\tag{2.7}
\]

The point of the lemma is not merely the extra retained state \(K_y\);
it is the exact omission of \(M\).

## 3. Independent completion forces the omitted state

### Proof of the theorem

The private witness \(y\) misses \(u\), so \(\{u,y\}\) is independent.
Equality (0.1) gives \(i(G)=3\).  Extend this pair to a maximal
independent set

\[
 I=\{u,y,s\}.
\tag{3.1}
\]

It is a maximum independent triple and hence a member of \(\mathcal K\).
The edge \(ux\) ensures \(x\notin I\).  By the active orientation
\(u\triangleright x\), transported over the \(u\)-star by accepted C-108,

\[
 I-u+x=\{x,y,s\}\in\mathcal K.
\tag{3.2}
\]

There are exactly two cases.

1. If \(s=q\), the retained state in (3.2) is
   \[
   \{x,y,q\}=M,
   \]
   contradicting (2.3).

2. Suppose \(s\ne q\).  Then \(q\) is unoccupied in (3.2).  The retained
   state must dominate \(q\), but
   \[
   qx,qy\notin E(G)
   \]
   by (1.8).  Therefore \(sq\in E(G)\).  Attack the unoccupied vertex
   \(q\) from (3.2).  The unique adjacent guard is \(s\), so eternal
   closure forces the one-edge, one-guard move
   \[
   s\longrightarrow q,
   \qquad
   \{x,y,s\}-s+q=\{x,y,q\}=M\in\mathcal K,
   \]
   again contradicting (2.3).

The two cases exhaust the completion collision.  Indeed (1.8) shows that
the completion vertex \(s\) cannot equal \(x,p,r,z\): each is adjacent
to \(u\) or \(y\).  Thus \(q\) is its only possible collision with a
previously named vertex.  Every attack used in the second case is
unoccupied, and its response moves exactly one guard along the forced
edge \(sq\).  This proves the theorem. \(\square\)

## 4. Proved result versus computational observation

The exclusion in Sections 1--3 is symbolic.  It depends only on accepted
C-108 star transport, accepted C-064 ridge response-covariance, and the
accepted C-150 rank-one XQ1 witness ladder.

`verify_implication.py` is a separate ordinary-set bookkeeping audit.  It
checks:

- all \(21\) named pairs in (1.8);
- all named witness collisions;
- both ridge transpositions used in Lemma 2.1;
- the transported exact list \(L_T(y)=\{x\}\);
- the six retained grid states; and
- all four choices of the optional pairs \(up,uq\), including the only
  named completion collision \(s=q\) and the external-completion attack.

It does not re-prove C-064 or C-150.

`synthesize_control.py` independently encodes an unknown graph and an
explicit eternal triple-family with the full rank-one XQ1 incidence.  The
completion of \(\{u,y\}\) is existential and includes \(s=q\) and every
external choice.  CaDiCaL reported `UNSAT` at the tested orders \(7\)
through \(22\) listed in `OBSERVED_RESULTS.json`.  Those solver runs have
no proof certificates or independent formula audit and are labeled
**OBSERVED** only.  They are not used in the theorem.

## 5. Reproduction

From the campaign root:

```text
python3 -I -B -W error \
  math/working/rank_one_xq1_endgame/verify_implication.py
```

The output must match `expected_result.json`.

A representative discovery-only synthesis run is:

```text
python3 -I -B -W error \
  math/working/rank_one_xq1_endgame/synthesize_control.py \
  --order 12 \
  --solver tools/cadical_3_0_1/build/cadical \
  --cnf /tmp/rank-one-XQ1-order12.cnf \
  --result /tmp/rank-one-XQ1-order12.json
```
