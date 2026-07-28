# Canonical rank-one QQ1 collision: exact boundary controls

## Status

Date: 2026-07-28 (PDT)

This note independently audits the canonical rank-one QQ1 normal form and
freezes two exact controls at its sharp \(\gamma=2\) boundary.  It does
**not** eliminate QQ1 under \(\gamma=3\), certify an all-order UNSAT
statement, prove the complete \(k=3\) case, or resolve the
\(\gamma\)--\(\theta\) conjecture.

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and let \(\mathcal K\) be the literal greatest eternal family of
dominating triples.  In the canonical collision, use distinct vertices

\[
 u,x,p,q,r,b,c
\tag{0.2}
\]

with

\[
 T=\{x,p,q\}\in\mathcal K,\qquad
 B=\{u,p,q\}\notin\mathcal K.
\tag{0.3}
\]

The state \(T\) is independent, \(u\triangleright x\) but
\(x\not\triangleright u\), and \(B\) has deletion rank one.  Its deleting
attack \(r\) is QQ1:

\[
 ur,pr,qr\in E(G),\qquad xr\notin E(G).
\tag{0.4}
\]

The three legal successors are non-dominating.  Their private witnesses
are \(x,b,c\), respectively:

\[
\begin{array}{c|c|ccc}
\text{removed guard}&\text{private edge}&
 \multicolumn{3}{c}{\text{missed successor}}\\ \hline
u&xu&xr&xp&xq\\
p&bp&bu&br&bq\\
q&cq&cu&cr&cp .
\end{array}
\tag{0.5}
\]

Thus the \(u\)-successor witness is the already named endpoint \(x\);
it is not a fresh eighth vertex.

## 1. Independent audit of the forced collision core

The private-witness transfer and the forced \(U\to R\) chain give

\[
 M_p=\{x,b,q\},\quad
 M_q=\{x,p,c\},\quad
 U=\{u,b,c\},\quad
 R=\{r,b,c\}
\tag{1.1}
\]

in \(\mathcal K\).

### Lemma 1.1

Every canonical collision satisfies

\[
 xb,xc,bc,up,uq\in E(G).
\tag{1.2}
\]

#### Proof

Suppose \(xb\notin E(G)\).  Then

\[
 \{r,b,x\}\longrightarrow\{q,b,x\}\longrightarrow\{p,q,x\}=T
\tag{1.3}
\]

is a path of independent ridge exchanges, first \(r\leftrightarrow q\)
and then \(b\leftrightarrow p\).  At the external target \(c\), the guard
\(q\) responds from \(T\), since its successor is \(M_q\).  Exact ridge
response covariance (C-064) transports that response backwards to the
guard \(r\) in \(\{r,b,x\}\), contradicting \(rc\notin E(G)\).  Hence
\(xb\in E(G)\).  Interchanging \(p,b\) with \(q,c\) proves
\(xc\in E(G)\).

If \(bc\notin E(G)\), then both \(U\) and \(R\) are independent triples.
They are ridge neighbors exchanging \(u\) and \(r\).  Activity
\(u\triangleright x\) makes \(u\) a responder at \(x\) from \(U\).
C-064 transports that response to \(r\) from \(R\), contradicting
\(rx\notin E(G)\).  Thus \(bc\in E(G)\).

For \(up\), suppose instead that \(up\notin E(G)\) and attack \(b\) from
the retained state \(M_q=\{x,p,c\}\).  All three graph-eligible
successors fail:

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{missed vertex}\\ \hline
x&\{b,p,c\}&u\\
p&\{x,b,c\}&r\\
c&\{x,p,b\}&q .
\end{array}
\tag{1.4}
\]

Every displayed miss follows directly from (0.4)--(0.5), the assumption
\(up\notin E(G)\), and the already proved \(xb,xc,bc\) edges.  Hence no
successor is dominating, contradicting closure of \(M_q\).  Therefore
\(up\in E(G)\).  The symmetric attack at \(c\) from \(M_p\) proves
\(uq\in E(G)\). \(\square\)

This proof treats omitted family transitions and graph nonedges
separately.  A successor in (1.4) is excluded only by its displayed
missed vertex.

## 2. Audit of the fresh-to-collision normalization

In a fresh QQ1 or AQ1 presentation, let \(a=y_u\ne x\) be the private
witness for the \(u\)-successor.  The already derived chain gives
\[
 V=\{a,p,q\}\in\mathcal K,
\tag{2.1}
\]
and private-witness incidence gives
\[
 au,ax\in E(G),\qquad ar,ap,aq\notin E(G).
\tag{2.2}
\]

Complete the independent pair \(\{u,b\}\) to
\[
 I=\{u,b,s\}.
\tag{2.3}
\]
Activity \(u\triangleright x\) retains
\[
 J=\{x,b,s\}.
\tag{2.4}
\]
Attack \(a\) from \(J\).  The \(s\)-successor \(\{x,b,a\}\) misses
\(q\).  If \(b\) is adjacent to \(a\), its successor
\(E=\{x,a,s\}\) either misses \(q\) when \(sq\) is absent, or has a
unique response to \(q\) reaching \(\{x,a,q\}\), which misses \(p\).
Thus neither non-\(x\) successor can be retained; a missing move edge
only makes the corresponding guard ineligible.  Closure forces
\[
 x\longrightarrow a,\qquad
 J-x+a=\{a,b,s\}=I-u+a\in\mathcal K.
\tag{2.5}
\]
By C-108 this proves \(u\triangleright a\).

On the independent endpoint \(V\), an \(a\to u\) move would land in the
omitted state \(B\), so \(a\not\triangleright u\).  Relative to the new
endpoint \(V=\{a,p,q\}\), the same reverse state \(B\), the same deleting
attack \(r\), and the private witness \(a\) are exactly the canonical
QQ1 collision (0.2)--(0.5), with \(a\) in the role of \(x\).

Consequently the fresh AQ1 and QQ1 presentations introduce no separate
rank-one endgame once this normalization is accepted.

## 3. Two exact sharp-boundary controls

The standalone checker `verify_control.py` imports no search code and
recomputes domination, independent domination, independence, clique
cover, and the literal greatest one-guard kernels.  It verifies both
fixed graph6 records below.

### Control A: the asymmetric pair dominates

```text
Mslamztl~fnny~]~_
```

It has

\[
 (n,m)=(14,67),\qquad
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3).
\tag{3.1}
\]

Its greatest triple family has 284 states.  The named \(B\) has rank one,
all three \(r\)-successors are non-dominating, and the complete canonical
QQ1 incidence is present.  The pair \(\{u,x\}\) dominates.

### Control B: the asymmetric pair does not dominate

```text
NslalntvXzn^{~n||^w
```

It has

\[
 (n,m)=(15,78),\qquad
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3).
\tag{3.2}
\]

Its greatest triple family has 285 states.  Again \(B\) has literal rank
one and all three deleting successors are non-dominating.  This time
\(\{u,x\}\) is non-dominating, with unique common nonneighbor \(10\), but
23 other vertex pairs dominate.

The unique repair-square completions over \(w=10\) are

\[
 t=6=c\in N_{\overline G}(u)\cap N_{\overline G}(w),
 \qquad
 z=13\in N_{\overline G}(x)\cap N_{\overline G}(w).
\tag{3.3}
\]

They induce the \(G\)-cycle
\[
 u-x-t-z-u
\tag{3.4}
\]
with pivot \(w\) missing all four cycle vertices.  The five usual square
states survive, while
\[
 O=\{u,w,z\}\notin\mathcal K
\tag{3.5}
\]
has deletion rank three.  Thus the opposite edge satisfies
\[
 z\triangleright t,\qquad t\not\triangleright z.
\tag{3.6}
\]
This is a particularly useful sharp warning: repairing the dominating
pair does not kill the asymmetry; it can propagate it to an omitted
corner of *higher* rank.

Control B proves that merely requiring the asymmetric pair
\(\{u,x\}\) to be non-dominating cannot eliminate canonical QQ1.  The
full condition \(\gamma=3\), not just the one pair, is essential.

## 4. Discovery-only SAT boundary

The collision-specific script `probe_collision.py` uses the collision
identification \(y_u=x\), the forced core (1.2), exact subset constraints,
and a literal one-guard eternal family.  CaDiCaL 3.0.1 gave:

| order | no pair constraints | only \(\{u,x\}\) non-dominating | every pair non-dominating |
|---:|:---:|:---:|:---:|
| 7--13 | UNSAT | UNSAT | UNSAT |
| 14 | SAT | UNSAT | UNSAT |
| 15--16 | SAT | SAT | UNSAT |

These are **OBSERVED** one-solver runs.  There are no DRAT/LRAT logs or
order-independent coverage proof.  In particular:

1. the \(n\le14\) exclusion with only \(\{u,x\}\) non-dominating is a
   finite-order artifact, explicitly refuted by Control B at order 15;
2. full-\(\gamma\) UNSAT through order 16 is not a theorem; and
3. absence of a SAT model does not resolve QQ1 or the conjecture.

The exact machine-readable table is in `OBSERVED_RESULTS.json`.

## 5. Reproduction

From the campaign root:

```text
sh math/working/rank_one_ur1_pair_core/verify_strict.sh
```

The strict script reruns the standalone verifier in isolated Python mode
and checks the exact output hash.  `probe_collision.py` is retained only
for discovery; its solver outputs are not consumed by the verifier.
