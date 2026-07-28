# Retained QQ1 completion corners and hot-layer bow-tie saturation

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

and, for the rank-one deleting attack \(r\) with side witnesses \(b,c\),

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

complete to \(p,q\).  Fix \(d\in C_{xr}\), put

\[
 I=\{x,r,d\},\qquad O=\{u,r,d\},
\tag{0.7}
\]

and recall from C-143 that \(O\) dominates, although
\(O\notin\mathcal K\).

This note proves the following stronger normal form.

1. The state
   \[
     A=\{u,x,d\}
   \]
   is retained, not merely dominating.  This gives a shorter proof of
   the no-cold-witness conclusion in the completion-dynamics note.
2. The nonempty common-nonneighbor set
   \[
     W_d=\{w\notin\{u,d\}:wu,wd\notin E(G)\}
   \]
   is a \(G\)-clique.  Every \(w\in W_d\) is adjacent to \(x,r\) and to
   one globally fixed side witness \(b\) or \(c\).  Five of the six
   repair-corner states over \(d,w\) are retained; the sixth is always
   the same omitted state \(O\).
3. If \(ud\notin E(G)\), this is the accepted C-145 repair square.
4. For either value of \(ud\), every further completion bow-tie over
   \(w\) is retained.  A four-attack argument from
   \(U=\{u,b,c\}\) rules out even one omitted mixed state.  Thus all
   nondegenerate outer bow-tie edges are reciprocal; the tempting
   self-similar omitted branch does not exist.

The \(ud\in E(G)\) retained branch is not eliminated.  The result is a
strict structural advance, not a proof of QQ1 impossibility, full
reciprocity, complete \(k=3\), or the gamma--theta conjecture.

## 1. Every completion hits all four witnesses

The independent triple \(I=\{x,r,d\}\) belongs to \(\mathcal K\).
The active edge \(u\triangleright x\) and C-143 say that its
complementary reverse endpoint \(O=\{u,r,d\}\) dominates.  Both \(u,r\)
miss \(b\), so

\[
 db\in E(G).
\tag{1.1}
\]

Similarly,

\[
 dc\in E(G).
\tag{1.2}
\]

Together with C-158 this gives

\[
 d\text{ is adjacent to }p,q,b,c.
\tag{1.3}
\]

This is the four-hit completion conclusion of the completion-dynamics
candidate.  Only C-143, not any inference from a missing family
transition, is used.

## 2. The missing corner forces a retained opposite corner

### Theorem 2.1 (retained completion corner) — PROVED CANDIDATE

For every \(d\in C_{xr}\),

\[
 \boxed{A=\{u,x,d\}\in\mathcal K.}
\tag{2.1}
\]

#### Proof

Attack the unoccupied vertex \(d\) from the retained state
\(U=\{u,b,c\}\).  The guards \(b,c\) are graph-eligible by (1.1)--(1.2).
If \(u\) is also eligible, its successor

\[
 U-u+d=\{d,b,c\}
\tag{2.2}
\]

misses \(r\), since \(dr,br,cr\notin E(G)\).  Hence closure of \(U\)
forces at least one of the two side successors

\[
 U-b+d=\{u,d,c\},\qquad
 U-c+d=\{u,b,d\}
\tag{2.3}
\]

to be retained.

Suppose first that \(\{u,d,c\}\in\mathcal K\).  Attack the unoccupied
vertex \(x\).  The guard \(d\) is ineligible.  The \(u\)-successor

\[
 \{x,d,c\}
\tag{2.4}
\]

misses \(r\), because \(xr,dr,cr\notin E(G)\).  The only possible
retained response is therefore \(c\to x\), with successor \(A\).
The case \(\{u,b,d\}\in\mathcal K\) is symmetric: its attack at \(x\)
uniquely forces \(b\to x\), again reaching \(A\).  Thus
\(A\in\mathcal K\). \(\square\)

This proof is shorter and stronger than proving only that \(A\)
dominates.  It uses neither C-064 nor a hypothetical cold vertex.
Every attack is unoccupied, and every excluded successor is rejected
because the displayed vertex \(r\) is undominated.

### Corollary 2.2 (exact side-response polarization) — PROVED CANDIDATE

Let

\[
 \Lambda_d=
 \{\,b:\{u,d,c\}\in\mathcal K\,\}
 \mathbin{\cup}
 \{\,c:\{u,b,d\}\in\mathcal K\,\}.
\tag{2.5}
\]

Then \(\varnothing\ne\Lambda_d\subseteq\{b,c\}\).  Moreover, for every
vertex \(w\) missing \(u,d\),

\[
\begin{array}{lll}
 b\in\Lambda_d&\Longrightarrow&wc\in E(G),\\
 c\in\Lambda_d&\Longrightarrow&wb\in E(G).
\end{array}
\tag{2.6}
\]

Indeed, each retained state in (2.3) must dominate \(w\), while \(w\)
misses \(u,d\).  Thus at least one of \(b,c\) is adjacent to every
common nonneighbor of \(u,d\).  If both side responses survive, then
every such vertex hits both \(b,c\).

The response at \(x\) from either retained state in (2.3) is exact:
the side guard opposite the element of \(\Lambda_d\) is the unique
retained responder and reaches \(A\).

## 3. The hot set is a retained clique

Since \(\gamma(G)=3\), the pair \(\{u,d\}\) does not dominate.  Therefore

\[
 W_d\ne\varnothing.
\tag{3.1}
\]

Fix \(w\in W_d\).  The retained state \(A\) dominates \(w\), and \(w\)
misses \(u,d\), so

\[
 wx\in E(G).
\tag{3.2}
\]

The dominating reverse state \(O=\{u,r,d\}\) similarly forces

\[
 wr\in E(G).
\tag{3.3}
\]

Finally \(U\) dominates \(w\), so \(w\) hits \(b\) or \(c\); Corollary
2.2 strengthens this to the uniform side condition (2.6).

Define

\[
\begin{array}{lll}
 K_w=\{u,d,w\},&
 E_w=\{x,d,w\},&
 F_w=\{r,d,w\}.
\end{array}
\tag{3.4}
\]

### Theorem 3.1 (five retained corners) — PROVED CANDIDATE

For every \(w\in W_d\),

\[
 \boxed{I,A,K_w,E_w,F_w\in\mathcal K,\qquad O\notin\mathcal K.}
\tag{3.5}
\]

#### Proof

The states \(I,A\) are retained by independence and Theorem 2.1,
respectively.  Attack \(w\) from \(A\).  By the definition of \(W_d\)
and (3.2), the only eligible guard is \(x\), so

\[
 A\xrightarrow{x\to w}K_w
\tag{3.6}
\]

is forced.

Next attack \(r\) from \(K_w\).  The guards \(u,w\) are eligible and
\(d\) is not.  The \(w\)-successor is exactly the omitted state \(O\).
Closure therefore forces

\[
 K_w\xrightarrow{u\to r}F_w.
\tag{3.7}
\]

At an attack \(x\) from \(F_w\), only \(w\) is eligible, and the unique
successor is \(I\).

It remains to prove retention of \(E_w\).  The proof splits at \(ud\).

If \(ud\notin E(G)\), then \(K_w\) is a maximum independent triple.
The active relation \(u\triangleright x\) and C-108 give

\[
 K_w-u+x=E_w\in\mathcal K.
\tag{3.8}
\]

If \(ud\in E(G)\), extend the independent pair \(\{u,w\}\) to a
maximum independent triple

\[
 S_s=\{u,w,s\}.
\tag{3.9}
\]

C-108 retains

\[
 D_s=S_s-u+x=\{x,w,s\}.
\tag{3.10}
\]

The state \(D_s\) must dominate \(d\).  Since \(x,w\) both miss \(d\),
one has \(sd\in E(G)\).  At the unoccupied attack \(d\) from \(D_s\),
the only eligible guard is \(s\), and its successor is \(E_w\).
Therefore \(E_w\in\mathcal K\) in the edge branch as well. \(\square\)

The edge-branch argument in the last paragraph is essential.  One may
not infer (3.8) merely from closure of the non-independent state \(K_w\):
at its attack \(x\), the move \(w\to x\) already returns to \(A\).

The retained transitions include

\[
\begin{array}{rcl}
A&\xrightarrow{x\to w}&K_w,\\
K_w&\xrightarrow{u\to r}&F_w,\\
F_w&\xrightarrow{w\to x}&I,\\
I&\xrightarrow{r\to u}&A,
\end{array}
\tag{3.11}
\]

and also

\[
 K_w-u+x=E_w,\qquad
 I-x+w=F_w,\qquad
 I-r+w=E_w.
\tag{3.12}
\]

The state \(I=\{x,r,d\}\) is maximum independent.  Its three displayed
retained successors witness, respectively,

\[
 x\triangleright w,\qquad
 r\triangleright w,\qquad
 r\triangleright u,
\tag{3.13}
\]

where the last successor is \(I-r+u=A\).  Thus every activity claim in
(3.13) is sourced at the independent state \(I\).  No reverse activity
is asserted in the \(ud\in E(G)\) branch merely from a transition whose
source is non-independent.

### Theorem 3.2 (hot-clique saturation) — PROVED CANDIDATE

The set \(W_d\) is a \(G\)-clique.

#### Proof

Let \(w,y\in W_d\) be distinct.  The retained state \(K_w\) dominates
\(y\).  Since \(y\) misses \(u,d\), it must be adjacent to \(w\).
\(\square\)

The clique conclusion is new in the \(ud\in E(G)\) branch.  If \(ud\)
is a nonedge, it also follows statically from \(\alpha(G)=3\), but the
retained-state proof works uniformly.

## 4. The nonedge branch is an exact repair square

Assume in this section that

\[
 ud\notin E(G).
\tag{4.1}
\]

Then \(K_w\) and \(I\) are independent triples.  With pivot \(d\), they
are exactly the two endpoint states in C-145.  The six corner states are

\[
\begin{array}{c|c}
\text{state}&\text{status}\\ \hline
K_w=\{u,d,w\}&\text{retained and independent}\\
I=\{x,d,r\}&\text{retained and independent}\\
E_w=\{x,d,w\}&\text{retained}\\
A=\{u,x,d\}&\text{retained}\\
F_w=\{r,d,w\}&\text{retained}\\
O=\{u,r,d\}&\text{omitted}.
\end{array}
\tag{4.2}
\]

The induced \(G\)-cycle is

\[
 u-x-w-r-u,
\tag{4.3}
\]

and its activity is

\[
\begin{array}{c|c}
ux&u\triangleright x,\quad x\not\triangleright u,\\
rw&r\triangleright w,\quad w\not\triangleright r,\\
xw&x\leftrightarrow w,\\
ur&u\leftrightarrow r.
\end{array}
\tag{4.4}
\]

Accepted C-161 places \(u,w\) in one component of the complement link
\(L_d\) and \(x,r\) in another, with the checkerboard orientations
shown in (4.4).  The omitted corner is literally \(O\) for both
one-sided edges, so its deletion rank is conserved.  This is exact
self-similarity, not a contradiction.

## 5. Completion bow-ties over a hot vertex

Fix \(w\in W_d\) and define the two maximum-independent completion sets

\[
\begin{aligned}
 \mathcal S_w
   &=\{s\notin\{u,w\}:su,sw\notin E(G)\},\\
 \mathcal T_w
   &=\{t\notin\{d,w\}:td,tw\notin E(G)\}.
\end{aligned}
\tag{5.1}
\]

Both are nonempty, because every independent pair extends to a maximal
independent set and \(i(G)=\alpha(G)=3\).  Each is a \(G\)-clique:
two nonadjacent members together with the underlying independent pair
would form an independent four-set.

The sets are disjoint.  Any common member would miss all three guards
of the retained state \(K_w\).  Domination by \(K_w\) also gives

\[
\begin{array}{lll}
s\in\mathcal S_w-\{d\}&\Longrightarrow&sd\in E(G),\\
t\in\mathcal T_w-\{u\}&\Longrightarrow&tu\in E(G).
\end{array}
\tag{5.2}
\]

For \(s\in\mathcal S_w\) and \(t\in\mathcal T_w\), write

\[
 S_s=\{u,w,s\},\qquad
 J_t=\{d,w,t\},\qquad
 Q_{s,t}=\{s,w,t\}.
\tag{5.3}
\]

The first two states are independent and retained.

### Theorem 5.1 (universal bow-tie saturation) — PROVED CANDIDATE

For either value of \(ud\),

\[
 \boxed{Q_{s,t}\in\mathcal K
 \quad\text{for every }
 s\in\mathcal S_w,\ t\in\mathcal T_w.}
\tag{5.4}
\]

#### Proof

Assume for contradiction that \(Q_{s,t}\notin\mathcal K\) for one
fixed pair \(s,t\).  Start from the retained canonical state

\[
 U=\{u,b,c\}.
\tag{5.5}
\]

At the unoccupied attack \(r\), the side guards \(b,c\) are ineligible,
so the unique response is

\[
 U\xrightarrow{u\to r}R=\{r,b,c\}\in\mathcal K.
\tag{5.6}
\]

Now attack \(w\) from \(R\).  The \(r\)-successor

\[
 \{w,b,c\}
\tag{5.7}
\]

misses \(u\), because \(w,b,c\) all miss \(u\).  Closure must therefore
retain at least one of

\[
 X_b=\{r,b,w\},\qquad X_c=\{r,c,w\}.
\tag{5.8}
\]

This statement remains valid if one of \(b,c\) is graph-ineligible at
\(w\): the corresponding branch is simply absent.

First handle the possible collision with a side guard.  If \(s=b\),
then \(wb\notin E(G)\) by the definition of \(\mathcal S_w\).  Thus
the \(b\to w\) branch at (5.8) is graph-ineligible, and the retained
\(c\to w\) branch lands directly in
\(\{r,b,w\}=\{r,s,w\}\).  The case \(s=c\) is symmetric.

Now suppose \(s\notin\{b,c\}\).  Attack \(s\) from a retained state in
(5.8).  The guard \(w\) is ineligible because
\(s\in\mathcal S_w\).  The \(r\)-successor is either
\(\{s,b,w\}\) or \(\{s,c,w\}\); in both cases it misses \(u\), since
\(s,w,b,c\) all miss \(u\).  Thus the remaining side guard must move
to \(s\).  In the collision and noncollision cases alike, the same
state is retained:

\[
 Y=\{r,w,s\}\in\mathcal K.
\tag{5.9}
\]

Finally attack \(t\) from \(Y\).  The guard \(w\) is ineligible because
\(t\in\mathcal T_w\).  The \(r\)-successor is the assumed omitted state

\[
 Y-r+t=Q_{s,t}.
\tag{5.10}
\]

The only remaining possible successor is

\[
 Y-s+t=\{r,w,t\},
\tag{5.11}
\]

but it misses \(d\), because \(r,w,t\) all miss \(d\).  Therefore \(Y\)
has no retained response at \(t\), a contradiction.  This proves
(5.4). \(\square\)

The proof is an exact adaptive attack tree.  It does not use row-column
covariance, C-145, or the value of \(ud\).  In particular, it rules out
an individual omitted bow-tie state, not merely a globally uniform
omitted matrix.

### Corollary 5.2 (outer reciprocity) — PROVED CANDIDATE

Every nondegenerate edge in (5.2) is active in both directions:

\[
 \boxed{
 s\leftrightarrow d\quad(s\ne d),\qquad
 t\leftrightarrow u\quad(t\ne u).
 }
\tag{5.12}
\]

Indeed, \(s\to d\) from the independent state \(S_s\) reaches \(K_w\),
while \(d\to s\) from \(J_t\) reaches \(Q_{s,t}\).  The other pair is
symmetric.  All activity witnesses here have independent source states.

When \(ud\notin E(G)\), the endpoint completions
\(d\in\mathcal S_w\) and \(u\in\mathcal T_w\) recover the reciprocal
edges of the original C-145 square.  When \(ud\in E(G)\), neither
endpoint is in its opposite completion set, so (5.12) applies to every
outer completion.  The formerly tempting all-omitted polarized branch
is impossible.

## 6. Controls, dependencies, and exact remaining gate

The standalone checker in this directory independently decodes the two
C-159 graph6 controls

```text
Mslamztl~fnny~]~_
NslalntvXzn^{~n||^w
```

and recomputes

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)
\tag{6.1}
\]

for each.  In both controls the unique \(x,r\)-completion \(d\) makes
\(\{u,d\}\) a dominating pair, so \(W_d=\varnothing\).  Thus neither
control enters the hot-layer hypothesis, exactly as required.  They
remain sharp warnings that the canonical seven-vertex QQ1 core and its
rank diamond alone do not imply \(\gamma=3\).

There is also a new exact control for the surviving \(ud\)-edge branch:

```text
Oslally^v{zn{~y~nn~j~
```

The checker recomputes

\[
 (n,m)=(16,91),\qquad
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3),
\tag{6.2}
\]

and a 439-state greatest triple family.  With the labels
\(u,x,p,q,r,b,c,d,w,s,t=0,\ldots,10\), it has

\[
 W_d=\{w\},\qquad
 \mathcal S_w=\{b,s\},\qquad
 \mathcal T_w=\{t\},
\tag{6.3}
\]

\(ud\in E(G)\), and every mixed state
\(\{z,w,t\}\), \(z\in\{b,s\}\), retained.  The canonical state \(B\)
has rank one and \(O=\{u,r,d\}\) has rank three.  The graph has many
dominating pairs, so it is not an equality graph and not a
counterexample.  It proves that the retained \(ud\)-edge branch cannot
be eliminated from the displayed local dynamics alone; genuinely
global \(\gamma=3\) information is still necessary.

The symbolic checker also exhausts:

1. all three nonempty side-response lists and two representative hot
   witnesses, confirming the global side polarization;
2. the complete omitted-state attack tree (5.5)--(5.11), including both
   possible side responses from \(R\); and
3. the two old C-159 controls and the new fixed \(ud\)-edge control with
   exact parameter and greatest-kernel recomputation.

The proof depends on accepted C-010, C-108, C-143, C-145, C-158, and
the exact greatest-family definition.  C-161 is used only to interpret
the separated complement-link geometry after the symbolic results are
proved.  No graph nonedge is inferred from an omitted family state.

The completion-dynamics candidate is not needed for Theorem 2.1:
Sections 1--3 give an independent shorter derivation of its four-hit and
no-cold conclusions, and strengthen the latter to retained-state
saturation.  Its rank diamond remains a compatible separate result.

The exact surviving gate has two \(ud\)-subcases.  When \(ud\) is a
nonedge, the original C-145 square and its separated-link asymmetry
remain, but every outer bow-tie is saturated.  When \(ud\) is an edge,
the five retained corners and every outer bow-tie are saturated, as in
the new boundary control.  Thus neither subcase supplies a new
lower-rank omitted corner.  A future proof must use genuinely global
\(\gamma=3\) information to eliminate these saturated configurations or
couple them back to the original rank-one state.

From the campaign root, reproduce the finite audit with

```text
sh math/working/qq1_hot_layer_endgame/verify_strict.sh
```
