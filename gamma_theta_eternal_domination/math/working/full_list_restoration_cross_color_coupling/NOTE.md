# Completion rebound and cross-color barriers after attacked-anchor restoration

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting independent hostile review**.
It continues accepted C-165, C-168, C-173, C-175, and C-176 in the
parameter-three equality setting.

The package does not eliminate attacked-anchor restoration.  It gives an
exact next-layer split.

1. In the C-176 branch \(e\in B\), the reciprocal \(xy\)-hinge sits inside
   a whole retained completion clique on the independent pair \(\{r,e\}\).
   Every state in that clique has positive source-color rank.
2. In the branch \(e\notin B\), every missed witness \(p\) of the explicit
   nondominating alternate forces a two-attack ladder back to a source-color
   root state.  An external witness has exact singleton palette
   \(Q(p)=\{u\}\) and produces a state of positive rank for both other
   colors.
3. If also \(p\notin B\), every noncolliding completion of the independent
   pair \(\{p,e\}\) has source-color rank at least two (or lies in the
   restricted kernel).  Thus rank one cannot recur immediately.

An exact 16-vertex equality control realizes twelve local
attacked-secondary restoration rows with \(e\notin B\).  It is not claimed
that every one has the upstream C-176 rank-one-corridor ancestry.  Its nineteen witness
incidences include the collision \(p=u\), and every noncolliding completion
has source rank three.  The rebound therefore does not itself force a safe
kernel.

No cross-ban ranks are compared.  No omitted family state is converted
into a graph nonedge.  No safe color, complete \(k=3\) theorem, finite
exclusion, or universal gamma--theta resolution is claimed.

## 1. Accepted setup

Assume

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{1.1}
\]

and let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples.  Let

\[
S=\{u,v,t\}
\tag{1.2}
\]

be independent, let \(x\) be full at \(S\), and put

\[
B=N_{\overline G}(x).
\tag{1.3}
\]

For source color \(u\), ban

\[
\mathcal B_u(x)=\{\{v,t,b\}:b\in B\}.
\tag{1.4}
\]

Use the C-171/C-176 trapped corridor notation.  In particular,

\[
r\in B,\qquad y\notin B,\qquad e\in C_{ry},
\tag{1.5}
\]

where

\[
C_{ry}=V(G)\setminus(N_G[r]\cup N_G[y]).
\tag{1.6}
\]

The rank-one independent state

\[
K_e=\{r,y,e\}
\tag{1.7}
\]

has a deleting attack at \(t\).  C-176 forces the unique retained response

\[
K_e\xrightarrow[\text{attack }t]{y\to t}
D_e=\{r,t,e\},
\qquad \rho_u(D_e)=0.
\tag{1.8}
\]

The only deleting attack at \(D_e\) is \(v\).  Its selected response

\[
e\to v,\qquad E=\{v,t,r\}
\tag{1.9}
\]

is retained and banned.  The sole other physical response is

\[
r\to v,\qquad R_e=\{v,t,e\}.
\tag{1.10}
\]

If \(e\in B\), this alternate is banned and C-175 gives reciprocal activity
on \(xy\).  If \(e\notin B\), then \(R_e\) is unbanned and nondominating.

We use only the named incidences

\[
vr,ve,tr,ty,ur,uy,xy\in E(G)
\tag{1.11}
\]

and

\[
vt,yr,ye,re,xr\notin E(G),
\tag{1.12}
\]

together with \(xe\notin E(G)\) in the first branch and
\(xe\in E(G)\) in the second.

## 2. The trapped \(e\in B\) branch

### Theorem 2.1 (reciprocal completion bow tie) — PROVED CANDIDATE

Suppose \(e\in B\).  Put

\[
C_{re}=V(G)\setminus(N_G[r]\cup N_G[e]).
\tag{2.1}
\]

Then:

1. \(C_{re}\) is a nonempty \(G\)-clique containing both \(x\) and \(y\);
2. for every \(d\in C_{re}\), the maximum independent triple
   \[
   I_d=\{r,e,d\}
   \tag{2.2}
   \]
   belongs to \(\mathcal F^\star\);
3. for distinct \(d,d'\in C_{re}\), the attack at \(d'\) from \(I_d\)
   has the unique response
   \[
   d\to d',\qquad I_d\to I_{d'};
   \tag{2.3}
   \]
4. every \(I_d\) has source-ban distance exactly two and is therefore
   either in the source restricted kernel or has source rank at least one.

In particular, \(I_y=K_e\) and \(I_x=\{r,e,x\}\) are the two states of the
C-175 reciprocal \(xy\)-hinge.  If the source restricted kernel is empty,
the whole bow-tie fan has finite positive source rank.

#### Proof

The vertices \(r,e\) are nonadjacent because \(e\in C_{ry}\).  Since both
lie in \(B\), the target \(x\) misses both.  The vertex \(y\) misses both
by the definition of \(C_{ry}\).  Hence \(x,y\in C_{re}\).

If two vertices of \(C_{re}\) were nonadjacent, those two vertices together
with \(r,e\) would form an independent four-set, contradicting
\(\alpha(G)=3\).  Thus \(C_{re}\) is a clique; in particular the already
known edge \(xy\) is also forced by this clique.

Every \(I_d\) is an independent triple.  It is maximum and therefore
maximal, so it dominates.  Every maximum independent triple belongs to
every eternal triple-family, hence to \(\mathcal F^\star\).  For a distinct
completion \(d'\), the guards \(r,e\) miss \(d'\), while the clique edge
\(dd'\) is present.  This proves the unique exchange (2.3).

No \(I_d\) contains \(v\) or \(t\): the edges \(vr,tr\) exclude both
anchors from \(C_{re}\), and \(r,e\) are external.  A source-banned triple
contains \(v,t\) and only one vertex of \(B\).  The state \(I_d\) shares
at most one token with any banned triple and shares \(r\) with
\(\{v,t,r\}\).  Its Johnson distance is exactly two.  C-173 gives the rank
claim. \(\square\)

This is a finite retained object, not a contradiction.  It neither
compares its ranks with another color nor forces a clique cover.

## 3. The external \(e\notin B\) branch

Assume from now on

\[
e\notin B.
\tag{3.1}
\]

Then \(R_e=\{v,t,e\}\) is nondominating.  Let \(p\) be any missed vertex:

\[
N_G[p]\cap R_e=\varnothing.
\tag{3.2}
\]

Thus

\[
pv,pt,pe\notin E(G).
\tag{3.3}
\]

The collision

\[
p=u
\tag{3.4}
\]

is possible and must not be discarded.

### Lemma 3.1 (restoration-witness ladder) — PROVED CANDIDATE

Every missed vertex \(p\) satisfies

\[
pr\in E(G).
\tag{3.5}
\]

The following response is unique and retained:

\[
D_e=\{r,t,e\}
\xrightarrow[\text{attack }p]{r\to p}
P_e(p)=\{p,t,e\}.
\tag{3.6}
\]

The attack at \(v\) from \(P_e(p)\) is also unique and retains

\[
P_e(p)
\xrightarrow[\text{attack }v]{e\to v}
Z_p=\{p,t,v\}.
\tag{3.7}
\]

If \(p=u\), then \(Z_p=S\).  If \(p\ne u\), then

\[
pu\in E(G),\qquad
Z_p=S-u+p\in\mathcal F^\star,\qquad
\boxed{Q(p)=\{u\}}.
\tag{3.8}
\]

For every external witness \(p\ne u\), the state \(Z_p\) is unbanned for
the color-\(v\) and color-\(t\) restricted peelings and is not rank zero
in either peeling.  If all three restricted kernels are empty, \(Z_p\)
has finite positive rank for both recipient colors.

#### Proof

The retained state \(D_e\) dominates \(p\).  Its \(t\)- and \(e\)-guards
miss \(p\) by (3.3), so \(r\) must hit \(p\).  This proves (3.5), makes
\(r\to p\) the unique response, and gives (3.6).

From \(P_e(p)\), the guards \(p,t\) miss \(v\), while \(e\) hits \(v\) by
the selected restoration move.  Hence (3.7) is unique and retained.

If \(p=u\), its endpoint is literally the root; no loop \(uu\) is
asserted.  Suppose \(p\ne u\).  The independent root dominates \(p\).
Its \(v,t\)-guards miss \(p\), so \(up\) is an edge.  The state \(Z_p\)
is exactly the retained root swap \(S-u+p\), proving \(u\in Q(p)\).
Equation (3.3) excludes \(v,t\) from the palette even at the graph-edge
level.  Thus \(Q(p)=\{u\}\).

For the color-\(v\) ban, the two fixed anchors are \(u,t\).  The state
\(Z_p=\{p,t,v\}\) contains \(t\) and lacks \(u\).  Every attack other than
\(u\) has every successor still lacking \(u\), so unrestricted eternal
closure supplies a retained dominating unbanned response.  At the attack
\(u\), the unique response \(p\to u\) returns to the retained root \(S\),
which is unbanned.  Thus \(Z_p\) survives the first color-\(v\) deletion
round.  The color-\(t\) argument is identical, with fixed anchors \(u,v\).
\(\square\)

The last paragraph is a cross-color conclusion, but only a sign
comparison: two recipient ranks are positive.  It does not compare their
values with the source rank.

### Lemma 3.2 (the completion fan over a missed witness) — PROVED CANDIDATE

Put

\[
C_{pe}=V(G)\setminus(N_G[p]\cup N_G[e]).
\tag{3.9}
\]

Then \(C_{pe}\) is a nonempty \(G\)-clique.  Moreover,

\[
C_{pe}\subseteq N_G[t]
\tag{3.10}
\]

with the closed-neighborhood convention.  For every
\(f\in C_{pe}-\{t\}\), the attack at \(f\) from \(P_e(p)\) uniquely
retains the maximum independent triple

\[
I_f=\{p,e,f\}.
\tag{3.11}
\]

#### Proof

The pair \(p,e\) is independent.  It cannot dominate because
\(\gamma(G)=3\), so \(C_{pe}\) is nonempty.  Two nonadjacent vertices in
the completion set would join \(p,e\) to form an independent four-set.
Thus it is a clique.

The retained state \(P_e(p)=\{p,t,e\}\) dominates every completion.  Away
from the occupied collision \(f=t\), the \(p,e\)-guards miss \(f\), so
\(t\) is the unique defender and responder.  The endpoint is independent
by definition and hence is a retained maximum independent triple.
\(\square\)

The state \(\{v,t,p\}\) also independently belongs to
\(\mathcal F^\star\), because it is a maximum independent triple.
Attacking \(e\) from that state has the retained response \(v\to e\) to
\(P_e(p)\), but that response need not be physically unique: the edge
\(te\) is unconstrained.

### Theorem 3.3 (no immediate rank-one recurrence) — PROVED CANDIDATE

Suppose in addition that

\[
p\notin B.
\tag{3.12}
\]

For every \(f\in C_{pe}-\{t\}\), the retained independent completion
\(I_f=\{p,e,f\}\) is either in the source restricted kernel or has

\[
\boxed{\rho_u(I_f)\ge2.}
\tag{3.13}
\]

Consequently, if the source restricted kernel is empty, either

\[
C_{pe}=\{t\},
\tag{3.14}
\]

or every noncolliding completion has finite source rank at least two.

#### Proof

The state \(I_f\) contains neither fixed source-ban anchor \(v,t\).
Indeed \(f\ne t\), while \(v\notin C_{pe}\) because \(ve\) is an edge.
The vertices \(p,e\) are outside \(B\).

If \(f\notin B\), the state shares no token with any
\(\{v,t,b\}\), so its ban distance is three.  C-173 directly gives
\(\rho_u(I_f)\ge2\).

It remains to exclude rank one when \(f\in B\).  Then the ban distance is
exactly two.  Suppose for contradiction that \(\rho_u(I_f)=1\).
The all-\(k\) tight-shell part of C-175 says that every deleting attack is
\(v\) or \(t\), and every retained response at such an attack has rank
zero.

First consider an attack at \(t\).  Lemma 3.2 gives \(ft\in E(G)\), and
the response

\[
f\to t,\qquad I_f\to P_e(p)
\tag{3.15}
\]

is retained.  But \(P_e(p)\) is not rank zero.  It contains \(t\) and
lacks \(v\); every non-\(v\) attack has an unbanned retained response,
while the attack at \(v\) has the unique response

\[
e\to v,\qquad P_e(p)\to Z_p=\{p,t,v\}.
\tag{3.16}
\]

The endpoint is retained and unbanned because \(p\notin B\).  Thus the
attack \(t\) cannot delete \(I_f\).

Now consider an attack at \(v\).  The edge \(ev\) makes

\[
B_f:=I_f-e+v=\{p,f,v\}
\tag{3.17}
\]

a physical response.  If retained, \(B_f\) would not have rank zero: it
contains \(v\) and lacks \(t\), every non-\(t\) attack remains unbanned,
and the attack at \(t\) uniquely moves \(f\to t\) to the retained unbanned
state \(Z_p\).  Hence \(B_f\) is not retained at the deleting attack.

Eternal closure therefore forces a different retained response.  The
guard \(p\) misses \(v\), so necessarily \(fv\in E(G)\) and the retained
endpoint is

\[
A_f:=I_f-f+v=\{p,e,v\}.
\tag{3.18}
\]

Tight-shell descent would make \(A_f\) rank zero.  If \(et\in E(G)\),
then \(A_f\) survives round one: at its only possibly banning attack \(t\),
the unique move \(e\to t\) reaches the retained unbanned state \(Z_p\).
If \(et\notin E(G)\), then all three guards \(p,e,v\) miss the unoccupied
vertex \(t\), so \(A_f\) is not even dominating.  Either alternative
contradicts retention of a rank-zero \(A_f\).

Neither fixed anchor can delete \(I_f\), contradicting its assumed finite
rank one.  This proves (3.13). \(\square\)

Every named attack is unoccupied.  In particular, \(f\ne p,e,t,v\);
\(p=u\) is allowed and simply makes \(Z_p=S\).

## 4. Exact equality control

The graph

```text
OYifur}UO]}iTij]tpo]v
```

with root

\[
S=\{0,1,10\},\qquad x=6
\tag{4.1}
\]

has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
\qquad |\mathcal F^\star|=304.
\tag{4.2}
\]

Its target is full and

\[
B=\{5,7,9,11,13\}.
\tag{4.3}
\]

The color-\(0\) and color-\(10\) restricted kernels are empty; the
color-\(1\) kernel has 150 states.

The independent verifier enumerates every rank-zero attacked-secondary
restoration for an annihilated color whose alternate mover lies outside
\(B\).  These rows verify the hypotheses and conclusions of the
restoration-local Section 3; the verifier does not assert upstream C-176
ancestry.  It finds:

- 12 restoration rows;
- 19 missed-witness incidences;
- 12 incidences with the collision \(p=u\);
- 7 external incidences, all with exact singleton palette \(Q(p)=\{u\}\);
- one noncolliding completion for every witness incidence; and
- source rank exactly three for all 19 noncolliding completions.

Eight of the completion vertices lie in \(B\) and eleven lie outside, so
both distance-two and distance-three parts of Theorem 3.3 occur.

This equality control proves two boundaries.  The collision \(p=u\) cannot
be erased from Lemma 3.1, and the rank rebound can be strict without
creating a surviving source kernel.

## 5. Exact frontier

### Proved in this candidate

- A trapped \(e\in B\) restoration creates a retained positive-rank
  completion bow tie containing the reciprocal \(x,y\) states.
- Every \(e\notin B\) restoration witness forces a collision-safe
  two-attack ladder back to \(S-u+p\).
- Every external witness has singleton palette \(\{u\}\) and creates a
  positive-rank state under both other color bans.
- If the witness also lies outside \(B\), the next noncolliding completion
  cannot have source rank one; it rebounds to rank at least two or the
  restricted kernel.

### Open

- Exclude the singleton completion \(C_{pe}=\{t\}\).
- Control witnesses \(p\in B\), where the root-swap endpoint is source
  banned.
- Turn the positive ranks under the two recipient colors into a legitimate
  same-ban descent or a surviving kernel.
- Couple the three source rows without comparing ranks from different
  bans.
- Prove complete \(k=3\) or resolve the universal conjecture.
