# Tight-shell exits and target crossings after a rank-zero escape

## Status and scope

Date: 2026-07-28 (PDT)

This is a **provisional theorem package awaiting independent hostile
review**.  It uses accepted C-149, C-170, C-171, and C-172.  It also
reproves the two elementary pieces it needs from the still-provisional
completion-fan packages at commits `faff3d28` and `f7eb54c7`, so neither
candidate is silently treated as accepted.

The main result gives an exact next-layer normal form after the trapped
rank-zero escape of C-171:

1. a completion state of the second fan lies exactly two Johnson steps
   from the source-color ban;
2. if its restricted deletion rank is the floor value one, every
   deletion-witness attack is at one of the two ban anchors;
3. each forced completion fan either lies completely across the full
   target, making a natural cross triple dominating, or a trapped fan
   vertex creates a reciprocal two-state hinge on a named target edge.

The statements do not force a restricted kernel.  The exact gamma-two
boundary

```text
LEhbtnm~D]xln{
```

has both completion fans completely across the target, both cross
triples retained and dominating, all three restricted kernels empty,
and minimum second-fan rank two.  A nonanchor deletion witness then
occurs.  Thus the rank-one qualification is sharp, and even retained
dominating cross triples do not by themselves produce a safe color.

No complete parameter-three theorem, universal theorem, finite
exclusion, counterexample, or literature-priority claim is made.

## 1. Restricted peeling and the tight-shell lemma

Let \(\mathcal F\) be an eternal family of dominating \(k\)-sets.  Fix a
set \(\mathcal B\) of banned \(k\)-sets, and synchronously peel the
universe of all dominating \(k\)-sets outside \(\mathcal B\):

\[
 \Omega_0=\{D:|D|=k,\ D\text{ dominates},\ D\notin\mathcal B\},
 \qquad
 \Omega_{j+1}=\Phi(\Omega_j).
\tag{1.1}
\]

For a state of finite deletion rank, write \(\rho(D)=j\) when
\(D\in\Omega_j-\Omega_{j+1}\).  Put

\[
 \delta_{\mathcal B}(D)
 =
 \min_{B'\in\mathcal B}\bigl(k-|D\cap B'|\bigr).
\tag{1.2}
\]

The Johnson-distance floor

\[
 \rho(D)\ge \delta_{\mathcal B}(D)-1
\tag{1.3}
\]

for retained states is proved directly in the provisional
completion-fan package at `faff3d28`: one guard move changes
\(\delta_{\mathcal B}\) by at most one, and induction through the
eternal responses proves survival through the first
\(\delta_{\mathcal B}(D)-1\) rounds.

### Lemma 1.1 (tight-shell descent) — PROVED

Suppose \(D\in\mathcal F\) has

\[
 \delta_{\mathcal B}(D)=s\ge2,
 \qquad
 \rho(D)=s-1.
\tag{1.4}
\]

Let \(z\) be a deletion-witness attack at \(D\).  Then every retained
response \(D'\in\mathcal F\) to that attack satisfies

\[
 \boxed{
 \delta_{\mathcal B}(D')=s-1,
 \qquad
 \rho(D')=s-2.}
\tag{1.5}
\]

#### Proof

A one-guard move gives

\[
 \delta_{\mathcal B}(D')\ge s-1\ge1,
\tag{1.6}
\]

so every response in the statement is unbanned.  It dominates because
it belongs to the eternal family.  Since \(z\) witnesses deletion of
the rank-\((s-1)\) state \(D\), every such unbanned dominating response
has finite rank strictly below \(s-1\):

\[
 \rho(D')\le s-2.
\tag{1.7}
\]

The Johnson-distance floor (1.3) gives

\[
 \rho(D')\ge\delta_{\mathcal B}(D')-1\ge s-2.
\tag{1.8}
\]

All inequalities are equalities, proving (1.5). \(\square\)

This is an all-\(k\) statement.  It concerns retained responses, not all
physical moves, and it never converts absence from a family into a
graph nonedge.

## 2. The trapped rank-zero corridor

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{2.1}
\]

and let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples.  Use the accepted C-171 setup:

\[
 S=\{u,v,t\}\in\mathcal F^\star
\tag{2.2}
\]

is independent, \(x\) is full at \(S\), and

\[
 B=N_{\overline G}(x).
\tag{2.3}
\]

For source color \(u\), ban

\[
 \mathcal B_u(x)
 =
 \{\{v,t,b\}:b\in B\}.
\tag{2.4}
\]

The rank-zero corridor has retained states

\[
 T=\{v,t,q\},
 \qquad
 E=\{v,t,r\},
\tag{2.5}
\]

where \(r\in B\), \(q\notin B\), and \(q\to r\) is the deleting
response.  Choose a secondary color \(v\), let \(w\in B\) be a missed
witness of the associated nondominating alternate, and let \(y\) be a
missed witness of

\[
 H=\{v,q,r\}.
\tag{2.6}
\]

Accepted C-171 gives

\[
\begin{aligned}
 &xw,qw,tw,rw\notin E(G),\\
 &xq,qr,uw,vw,tr\in E(G),\\
 &yv,yq,yr\notin E(G),\\
 &yu,yt,yx\in E(G),
\end{aligned}
\tag{2.7}
\]

and retains

\[
 L_q=\{w,t,q\},\quad
 L_r=\{w,t,r\},\quad
 Y=\{v,t,y\}.
\tag{2.8}
\]

Attacking \(y\) from \(E\) has the unique response \(t\to y\), so

\[
 J=\{v,r,y\}\in\mathcal F^\star.
\tag{2.9}
\]

For a pair \(a,b\), put

\[
 C_{ab}
 =
 V(G)\setminus\bigl(N_G[a]\cup N_G[b]\bigr).
\tag{2.10}
\]

The pairs \(q,w\) and \(r,y\) are independent.  Since
\(\gamma(G)=3\), their completion sets \(C_{qw}\) and \(C_{ry}\) are
nonempty.

### Lemma 2.1 (the two retained completion fans) — PROVED

The sets \(C_{qw}\) and \(C_{ry}\) are \(G\)-cliques.  Moreover:

\[
 C_{qw}\subseteq N_G[t],
\tag{2.11}
\]

and, for every \(d\in C_{qw}-\{t\}\), the unique response to attack
\(d\) from \(L_q\) is

\[
 t\to d,\qquad
 I_d=\{q,w,d\}\in\mathcal F^\star.
\tag{2.12}
\]

Also

\[
 C_{ry}\subseteq N_G(v),
\tag{2.13}
\]

and, for every \(e\in C_{ry}\), the unique response to attack \(e\)
from \(J\) is

\[
 v\to e,\qquad
 K_e=\{r,y,e\}\in\mathcal F^\star.
\tag{2.14}
\]

#### Proof

Two nonadjacent vertices in \(C_{qw}\), together with \(q,w\), would be
an independent four-set.  Hence \(C_{qw}\) is a clique; the argument for
\(C_{ry}\) is identical.

The retained state \(L_q\) dominates every \(d\in C_{qw}\).  Away from
the occupied collision \(d=t\), only \(t\) can dominate and respond at
\(d\), proving (2.11)--(2.12).  Similarly, the retained state \(J\)
dominates each \(e\in C_{ry}\), while its \(r\)- and \(y\)-guards miss
\(e\).  Thus \(v\) is the unique responder, proving
(2.13)--(2.14). \(\square\)

The proof handles the possible collision \(t\in C_{qw}\) through the
closed neighborhood in (2.11); it does not attack an occupied vertex.

## 3. Minimum-rank second-fan exit

Assume the color-\(u\) restricted kernel is empty.  Choose
\(e\in C_{ry}\) so that

\[
 h=\rho_u(K_e)
\tag{3.1}
\]

is minimum over the second fan.  The completion state contains neither
\(v\) nor \(t\), and it contains \(r\in B\).  A banned state contains
both \(v,t\) and only one vertex of \(B\).  Therefore

\[
 \boxed{\delta_{\mathcal B_u(x)}(K_e)=2.}
\tag{3.2}
\]

The Johnson-distance floor gives \(h\ge1\).

Any other \(e'\in C_{ry}-\{e\}\) is adjacent to \(e\), while \(r,y\)
miss it.  Hence the attack at \(e'\) uniquely exchanges

\[
 e\to e',\qquad K_e\to K_{e'}.
\tag{3.3}
\]

By minimum choice, this cannot witness deletion of \(K_e\).  Thus every
deletion-witness attack lies outside \(C_{ry}\), and so is adjacent to
\(r\) or \(y\).

### Theorem 3.1 (rank-one anchor exit) — PROVED

If the minimum second-fan rank is

\[
 h=1,
\tag{3.4}
\]

then every deletion-witness attack \(z\) for \(K_e\) satisfies

\[
 \boxed{z\in\{v,t\}.}
\tag{3.5}
\]

Every retained response to that attack has source-color rank zero and
Johnson distance one from the ban.

More precisely:

- if \(z=v\), then the already retained response
  \[
  K_e\xrightarrow{e\to v}J=\{v,r,y\}
  \tag{3.6}
  \]
  has rank zero;
- if \(z=t\), eternal closure retains at least one physical response to
  the attack, and every retained response has rank zero.

#### Proof

Equations (3.2) and (3.4) put \(K_e\) on the tight shell of Lemma 1.1
with \(s=2\).  Consequently every retained response \(D'\) at a
deletion-witness attack has

\[
 \delta_{\mathcal B_u(x)}(D')=1,\qquad \rho_u(D')=0.
\tag{3.7}
\]

The starting state \(K_e=\{r,y,e\}\) contains neither ban anchor
\(v,t\).  To move from Johnson distance two to distance one in a single
guard move, the attacked vertex must therefore be \(v\) or \(t\).
This proves (3.5).

If \(z=v\), (2.13) gives \(ve\in E(G)\), so \(e\to v\) is a legal
response with endpoint \(J\), already retained by (2.9).  Equation
(3.7) gives its rank.  If \(z=t\), eternal closure supplies at least one
retained physical response, and (3.7) applies to every one. \(\square\)

The theorem does not say that an arbitrary positive-rank fan state
exits at an anchor.  Section 5 gives an exact rank-two countermodel to
that strengthening.

## 4. Exact target-crossing alternatives

Say that an edge \(ab\) is **reciprocal in**
\(\mathcal F^\star\) when there is an independent retained state
realizing \(a\to b\) and another realizing \(b\to a\), as in accepted
C-172.

Define the two cross triples

\[
 P=\{x,q,w\},
\qquad
 R=\{x,r,y\}.
\tag{4.1}
\]

### Theorem 4.1 (two-fan target crossing) — PROVED

In the setup of Section 2:

\[
\boxed{
\begin{aligned}
P\text{ dominates}
&\Longleftrightarrow C_{qw}\cap B=\varnothing,\\
R\text{ dominates}
&\Longleftrightarrow C_{ry}\cap B=\varnothing.
\end{aligned}}
\tag{4.2}
\]

If \(C_{qw}\cap B\ne\varnothing\), then \(xq\) is reciprocal in
\(\mathcal F^\star\).  If \(C_{ry}\cap B\ne\varnothing\), then \(xy\)
is reciprocal in \(\mathcal F^\star\).

Equivalently, each fan has the exact target-location split

\[
\boxed{
\begin{array}{ll}
C_{qw}\subseteq N_G(x)
 &\Longrightarrow P\text{ dominates},\\
C_{qw}\not\subseteq N_G(x)
 &\Longrightarrow xq\text{ is reciprocal},
\end{array}}
\tag{4.3}
\]

and

\[
\boxed{
\begin{array}{ll}
C_{ry}\subseteq N_G(x)
 &\Longrightarrow R\text{ dominates},\\
C_{ry}\not\subseteq N_G(x)
 &\Longrightarrow xy\text{ is reciprocal}.
\end{array}}
\tag{4.4}
\]

Reciprocity may also occur in the dominating branch; the alternatives
are exact by fan location, not mutually exclusive by edge activity.

#### Proof

The pair \(\{q,w\}\) misses exactly \(C_{qw}\), so adding \(x\) makes
\(P\) dominating exactly when \(x\) sees every member of \(C_{qw}\).
The vertex \(x\) itself is not in \(C_{qw}\), because \(xq\) is an
edge.  Thus the failure set is exactly \(C_{qw}\cap B\), proving the
first equivalence.

Choose \(d\in C_{qw}\cap B\).  Lemma 2.1 retains the independent state

\[
 I_d=\{q,w,d\}.
\tag{4.5}
\]

The triple

\[
 I'_d=\{x,w,d\}
\tag{4.6}
\]

is independent, because \(x,w,d\) are pairwise nonadjacent.  It is a
maximum independent set, so it belongs to every eternal triple-family.
From \(I_d\), the attack at \(x\) has the unique response \(q\to x\);
from \(I'_d\), the attack at \(q\) has the unique response \(x\to q\).
This is reciprocal activity on \(xq\).

The pair \(\{r,y\}\) misses exactly \(C_{ry}\), and \(x\notin C_{ry}\)
because \(xy\) is an edge.  This proves the second equivalence in
(4.2).  If \(e\in C_{ry}\cap B\), Lemma 2.1 retains

\[
 K_e=\{r,y,e\},
\tag{4.7}
\]

while

\[
 K'_e=\{x,r,e\}
\tag{4.8}
\]

is a retained maximum independent set.  The attacks at \(x\) and \(y\)
uniquely exchange

\[
 K_e\xrightarrow{y\to x}K'_e,
\qquad
 K'_e\xrightarrow{x\to y}K_e.
\tag{4.9}
\]

Hence \(xy\) is reciprocal.  Statements (4.3)--(4.4) are the same
conclusions rewritten using \(B=N_{\overline G}(x)\). \(\square\)

Theorem 4.1 is consistent with, and is a specialized direct proof of,
the fan--reciprocity mechanism in the provisional package at
`f7eb54c7`.  It makes no inference from a missing family response.

### Corollary 4.2 (minimum-exit normal form) — PROVED

For a minimum-rank second-fan state \(K_e\), the next layer has two
independent exact splits:

1. if \(h=1\), every deleting attack is at \(v\) or \(t\), and every
   retained response lands at rank zero one Johnson step from the ban;
2. either the cross triple \(R=\{x,r,y\}\) dominates, or \(xy\) is
   reciprocal.

The second alternative is inclusive: \(R\) may dominate while \(xy\)
is also reciprocal.

## 5. Sharp gamma-two boundary

The graph

```text
LEhbtnm~D]xln{
```

with

\[
\begin{aligned}
S&=\{0,5,6\},&x&=8,\\
u&=6,&v&=0,&t&=5,\\
q&=2,&r&=10,&w&=3,&y&=1
\end{aligned}
\tag{5.1}
\]

has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)
=(2,2,3,3,4),
\qquad |\mathcal F^\star|=200.
\tag{5.2}
\]

It is not a gamma--theta counterexample.  It realizes every local
configuration in Sections 2--4 except the equality condition
\(\gamma=3\).  Its completion fans are

\[
C_{2,3}=\{11\},\qquad C_{10,1}=\{12\}.
\tag{5.3}
\]

Both lie completely in \(N_G(x)\).  Accordingly, both cross triples

\[
\{8,2,3\},\qquad \{8,10,1\}
\tag{5.4}
\]

dominate.  In fact both are retained, with source-color ranks three and
two respectively.

All three restricted kernels are empty.  The source and escape ranks
are \(0/0\), while both completion ranks are two.  For the minimum
second-fan state

\[
K_{12}=\{1,10,12\}
\tag{5.5}
\]

the deletion-witness attacks are

\[
\{0,3,5\}.
\tag{5.6}
\]

The attack \(3=w\) is not a ban anchor.  Its retained responses

\[
\{3,10,12\},\qquad \{1,3,10\}
\tag{5.7}
\]

both have rank one.  This proves two sharp boundaries:

- the anchor-exit conclusion in Theorem 3.1 cannot be extended from
  rank one to arbitrary positive rank by local dynamics alone;
- even both cross triples being dominating and retained does not force
  a nonempty restricted kernel.

The graph6 SHA-256 is

```text
f589427f022392a6a5527951d65445e740fd63e76ecea1a870bd8658766c5428
```

and the sorted edge-list SHA-256 is

```text
511e0296f81a58a19134a4b118422e111fd5127889c8cfda159cec880cde7a58
```

The verifier recomputes all five parameters, the literal greatest
family, all restricted kernels and ranks, both fans and cross triples,
and every named deletion response.

## 6. Exact frontier

### PROVED in this provisional package

- Tight states at the Johnson-distance rank floor descend by exactly
  one distance shell and one rank layer at every deletion-witness
  response.
- Every minimum second-fan state has Johnson distance exactly two and
  rank at least one.
- If its rank is one, every deletion-witness attack is at a ban anchor
  and every retained response has rank zero.
- Each forced completion fan either lies completely across the target,
  making its cross triple dominating, or a trapped completion gives an
  explicit reciprocal hinge on \(xq\) or \(xy\).

### EXACT finite boundary

- The 13-vertex graph in Section 5 has minimum second-fan rank two and
  a nonanchor deletion witness, while both cross triples dominate and
  are retained and all restricted kernels remain empty.

### OPEN

- Exclude or control the rank-one anchor exits under the full equality
  hypothesis.
- Couple reciprocal edges from distinct terminal rows.
- Promote a retained dominating cross triple or a reciprocal hinge to a
  safe color.
- Prove the complete \(k=3\) case or resolve the universal conjecture.
