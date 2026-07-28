# Signed balance in the physical exact-two-list branch

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination
model.  Attacks are made only at unoccupied vertices, exactly one
adjacent guard moves, and every retained successor remains in the
eternal family.

> **PROVED CANDIDATE, pending hostile review.**  Let
> \(\mathcal F\) be an eternal family of dominating triples, let
> \(S=\{a,b,c\}\in\mathcal F\) be independent, assume
> \(\gamma(G)=3\), and suppose every outside response list at \(S\) has
> size exactly two.  Then \(H=\overline G\) is three-colorable.
> Consequently \(\theta(G)=3\).

This settles the **unit-free, no-full, exact-two-list branch** at
parameter three.  It does not handle a singleton or full response list,
prove the complete \(k=3\) case, prove the conjecture at higher
parameters, or resolve the universal gamma--theta conjecture.

The accepted inputs are:

1. C-111, which gives the physical identity
   \[
      L(x)=N_G(x)\cap S
      \qquad(x\notin S);
   \tag{0.1}
   \]
2. the frozen-projection theorem C-063, which makes each omitted-color
   complement projection bipartite; and
3. the C-079 side-purity consequence C-086.

Sections 1--3 rederive the signed reduction and its shortening
self-containedly from those inputs.  Section 4 gives explicit
one-guard attack trees for every residual type skeleton.  No missing
family response is interpreted as a graph nonedge, and no outside-edge
transport is used.

No literature-priority claim is made.

## 1. Types, mates, and transversal triangles

Put \(H=\overline G\).  For \(x\notin S\), let

\[
  L(x)=\{s\in S:S-s+x\in\mathcal F\}.
\tag{1.1}
\]

Since \(|L(x)|=2\), there is a unique omitted anchor

\[
  \tau(x)=S-L(x),
\tag{1.2}
\]

called the **type** of \(x\).  For \(t\in S\), write

\[
  W_t=\{x\notin S:\tau(x)=t\}.
\tag{1.3}
\]

Accepted C-111 says exactly that a type-\(t\) vertex is joined in \(H\)
to anchor \(t\) and in \(G\) to the other two anchors:

\[
  tx\in E(H),\qquad
  sx\in E(G)\quad(s\in S-\{t\}).
\tag{1.4}
\]

The accepted frozen-projection theorem makes every \(H[W_t]\)
bipartite.

### Lemma 1.1 (same-type mate)

Every \(x\in W_t\) has a distinct vertex \(x'\in W_t\) with

\[
  xx'\in E(H).
\tag{1.5}
\]

#### Proof

The pair \(\{t,x\}\) does not dominate \(G\), so it has a common
complement neighbor \(x'\).  Neither other anchor can be \(x'\), because
both are adjacent to \(x\) in \(G\) by (1.4).  Hence \(x'\notin S\).
The edge \(tx'\in E(H)\) and (0.1) give \(\tau(x')=t\). \(\square\)

### Lemma 1.2 (universal side-purity)

Let \(K\) be a component of \(H[W_t]\), and let \(x\notin S\).  All
vertices of \(N_H(x)\cap K\) lie on one side of the bipartition of
\(K\).

#### Proof

If \(x\in W_t\), this is the ordinary bipartition property.  Suppose
\(\tau(x)=r\ne t\).  Lemma 1.1 supplies a same-type mate
\(x'\in W_r\) with \(xx'\in E(H)\).  Since \(r\ne t\), one has
\(t\in L(x')\).  Apply the accepted C-079 side-purity theorem with
positive vertex \(x'\), hub \(x\), and component \(K\). \(\square\)

### Lemma 1.3 (transversal completion)

If \(xy\in E(H)\) and \(\tau(x),\tau(y)\) are distinct, then every
common \(H\)-neighbor of \(x,y\) outside \(S\) has the third type.  In
particular, \(\gamma(G)=3\) supplies a third-type vertex \(z\) such that

\[
  xy,xz,yz\in E(H).
\tag{1.6}
\]

#### Proof

No anchor is a common \(H\)-neighbor of two outside vertices of distinct
types: each endpoint has exactly one anchor neighbor in \(H\), and
those anchors differ.  Thus a common neighbor supplied by
\(\gamma(G)=3\) lies outside \(S\).

Write \(\tau(x)=r\) and \(\tau(y)=s\).  If a common neighbor \(z\) had
type \(r\), then the same-type edge \(xz\) would put \(x,z\) on opposite
sides of one component of \(H[W_r]\), while \(y\) sees both.  This
contradicts Lemma 1.2.  Type \(s\) is symmetric.  Only the third type
remains. \(\square\)

This argument uses literal complement edges only.  The common neighbor
in (1.6) can collide with another transversal witness, but cannot
collide with either endpoint or with an anchor.

## 2. The signed coloring problem

Identify \(a,b,c\) cyclically with \(\mathbb Z_3\).  For an outside
vertex \(x\) of type \(t\), its two allowed anchor colors are
\(t-1,t+1\).  Encode a choice by its chirality

\[
 \chi(x)=
 \begin{cases}
 0,&\kappa(x)=t-1,\\
 1,&\kappa(x)=t+1.
 \end{cases}
\tag{2.1}
\]

Give every outside complement edge the sign

\[
 \epsilon(xy)=
 \begin{cases}
 1,&\tau(x)=\tau(y),\\
 0,&\tau(x)\ne\tau(y).
 \end{cases}
\tag{2.2}
\]

For a same-type edge, proper coloring is exactly chirality reversal.
For a cross-type edge, Lemma 1.3 completes the edge to a transversal
triangle.  The two list-compatible colorings of that triangle give one
color of each kind and equal chirality at all three vertices.  Hence a
proper three-coloring extending the three distinct anchor colors is
equivalent to

\[
  \chi(x)\oplus\chi(y)=\epsilon(xy)
  \qquad(xy\in E(H-S)).
\tag{2.3}
\]

Conversely, (2.3) directly gives distinct allowed colors on every
outside edge: opposite chiralities separate a same-type pair, and equal
chiralities separate a distinct-type pair.  Equation (1.4) handles every
anchor spoke.

Thus failure of three-colorability is equivalent to an **unbalanced**
cycle of \(H-S\), meaning a cycle containing an odd number of
same-type edges.

## 3. Shortening and the five residual words

### Lemma 3.1 (shortest unbalanced cycle has length at most five)

If \(H-S\) has an unbalanced cycle, it has a chordless unbalanced cycle
of length at most five.

#### Proof

Choose a shortest simple unbalanced cycle \(C\).  It is chordless: a
chord splits it into two strictly shorter simple cycles, and the xor of
their signed parities is the parity of \(C\).

Suppose two vertices \(x,y\in V(C)\) have distinct types and both
\(x\)--\(y\) arcs of \(C\) have length at least three.  Since
\(\gamma(G)=3\), they have a common \(H\)-neighbor \(z\).  No anchor is
common to distinct types, so \(z\notin S\).  Also \(z\notin V(C)\):
otherwise chordlessness would force both \(xz\) and \(yz\) to be cycle
edges, putting \(x,y\) at cyclic distance two.

Let \(P,Q\) be the two cycle arcs.  The two cycles
\(P+xzy\) and \(Q+xzy\) are simple.  Each is strictly shorter than
\(C\), because each arc has length at most \(|C|-3\).  Their signed
parities xor to the parity of \(C\), since the two-edge path occurs
twice.  One is therefore a shorter unbalanced cycle, a contradiction.
Consequently every pair whose two cyclic distances are at least three
has the same type.

If \(|C|\ge7\), distances three and four both qualify.  For cyclic
indices,

\[
  \tau(x_i)=\tau(x_{i+3})=\tau(x_{i+4}),
\]

so consecutive vertices have the same type and the whole cycle lies in
one bipartite \(H[W_t]\), impossible.

If \(|C|=6\), opposite vertices have the same type:
\(\tau(x_i)=\tau(x_{i+3})\).  The three edge signs are therefore
repeated in opposite pairs, making the total parity even.  This is also
a contradiction.  Hence \(|C|\le5\). \(\square\)

Every endpoint and the middle vertex of the shortening path are
distinct, and both new cycles are strictly shorter; no closed walk is
silently substituted for a simple cycle.

### Lemma 3.2 (residual type words)

Up to a permutation of the three types, cyclic rotation, and reversal,
the only unbalanced type words not already contradicted by bipartiteness
or side-purity are

\[
 \begin{array}{c|c}
 |C|&\text{word}\\ \hline
 4&0012\\
 5&00011,\quad00101,\quad00102,\quad00121.
 \end{array}
\tag{3.1}
\]

#### Proof

Direct enumeration through length five gives

\[
\begin{array}{c|l}
3&000,\ 001\\
4&0012\\
5&00000,\ 00001,\ 00011,\ 00101,\ 00102,\ 00121.
\end{array}
\tag{3.2}
\]

The one-type words `000` and `00000` are odd cycles in one bipartite
\(H[W_t]\).  In `001`, the different-type vertex sees both ends of a
same-type edge.  In `00001`, the different-type vertex sees both ends
of a same-type path of length three.  Those endpoints lie on opposite
bipartition sides, contradicting Lemma 1.2. \(\square\)

The standalone checker enumerates (3.2) independently.

## 4. Explicit attack exclusions

In every diagram below, a displayed cycle is induced because it was
chosen shortest and therefore chordless.  However, the attack trees
never require a chord to be a graph edge.  If an undisplayed guard move
is absent, that merely removes a response.  Every claimed domination
miss is supported by three displayed literal \(H\)-edges.

The phrase “forces \(D'\)” means that closure from a retained state
\(D\), under the displayed unoccupied attack, has no possible retained
successor other than \(D'\).  If the corresponding move edge is absent,
closure already fails; otherwise \(D'\in\mathcal F\).

### 4.1 The four-cycle `0012`

Let

\[
  p-q-u-v-p
\tag{4.1}
\]

be an induced complement cycle with types

\[
  \tau(p)=\tau(q)=a,\qquad
  \tau(u)=b,\qquad
  \tau(v)=c.
\tag{4.2}
\]

The direct response

\[
  D=\{a,c,p\}=S-b+p
\]

is retained because \(b\in L(p)\).  Attack \(u\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
a&\{c,p,u\}&\text{misses }v:\ cv,pv,uv\in E(H)\\
c&\{a,p,u\}&\text{misses }q:\ aq,pq,uq\in E(H)\\
p&\{a,c,u\}=S-b+u&b\notin L(u).
\end{array}
\tag{4.3}
\]

There is no retained response, a contradiction.

### 4.2 The five-cycle `00011`

Let

\[
  p-q-r-u-v-p
\tag{4.4}
\]

have types \(a,a,a,b,b\), respectively.  The state

\[
 D_0=\{a,b,p\}=S-c+p
\]

is retained.  Attack \(v\).  Guards \(b,p\) are blocked by the literal
edges \(bv,pv\in E(H)\), so closure forces

\[
 D_1=\{b,p,v\}.
\tag{4.5}
\]

Attack \(r\) from \(D_1\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
p&\{b,r,v\}&\text{misses }u:\ bu,ru,vu\in E(H)\\
v&\{b,p,r\}&\text{misses }a:\ ab,ap,ar\in E(H).
\end{array}
\]

Thus closure forces

\[
 D_2=\{p,r,v\}.
\tag{4.6}
\]

Attack \(a\).  Guards \(p,r\) are blocked by \(ap,ar\in E(H)\).
The only remaining successor shape is \(\{a,p,r\}\), which misses
\(q\) because \(aq,pq,rq\in E(H)\).  Contradiction.

### 4.3 The five-cycle `00121`

Let

\[
  p-q-u-v-w-p
\tag{4.7}
\]

have types \(a,a,b,c,b\), respectively.  The state

\[
 D_0=\{b,c,v\}=S-a+v
\]

is retained.  Attack \(p\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
c&\{b,p,v\}&\text{misses }w:\ bw,pw,vw\in E(H)\\
v&\{b,c,p\}=S-a+p&a\notin L(p).
\end{array}
\]

Hence closure forces

\[
 D_1=\{c,p,v\}.
\tag{4.8}
\]

Attack \(q\).  Guard \(p\) is blocked by \(pq\in E(H)\), while moving
\(v\) gives \(\{c,p,q\}\), which misses \(a\) by
\(ac,ap,aq\in E(H)\).  Thus closure forces

\[
 D_2=\{p,q,v\}.
\tag{4.9}
\]

Attack \(b\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
p&\{b,q,v\}&\text{misses }u:\ bu,qu,vu\in E(H)\\
q&\{b,p,v\}&\text{misses }w:\ bw,pw,vw\in E(H)\\
v&\{b,p,q\}&\text{misses }a:\ ab,ap,aq\in E(H).
\end{array}
\]

No retained response exists.

### 4.4 The five-cycle `00102`

Let

\[
  x_0-x_1-y-x_2-z-x_0
\tag{4.10}
\]

have types \(a,a,b,a,c\), respectively.  Apply Lemma 1.3 to the
cross edge \(x_1y\).  It supplies a type-\(c\) vertex \(q\) with

\[
  qx_1,qy\in E(H).
\tag{4.11}
\]

The witness \(q\) is distinct from every cycle vertex: no cycle vertex
other than \(z\) has type \(c\), and inducedness gives
\(zy\notin E(H)\), so \(z\) cannot be the common neighbor.  It is also
outside \(S\).

The direct response

\[
  D_0=\{a,c,z\}=S-b+z
\]

is retained.  Attack \(x_0\).  Guards \(a,z\) are blocked by
\(ax_0,zx_0\in E(H)\), so closure forces

\[
  D_1=\{a,x_0,z\}.
\tag{4.12}
\]

Attack \(y\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
x_0&\{a,y,z\}&\text{misses }x_2:\ ax_2,yx_2,zx_2\in E(H)\\
z&\{a,x_0,y\}&\text{misses }x_1:\ ax_1,x_0x_1,yx_1\in E(H).
\end{array}
\tag{4.13}
\]

Thus closure forces

\[
  D_2=\{x_0,y,z\}.
\tag{4.14}
\]

Attack \(q\).  Guard \(y\) is blocked by \(yq\in E(H)\).  Moving
\(z\) gives \(\{x_0,y,q\}\), which misses \(x_1\) because
\(x_0x_1,yx_1,qx_1\in E(H)\).  Therefore closure forces

\[
  D_3=\{y,z,q\}.
\tag{4.15}
\]

Finally attack \(a\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
y&\{a,z,q\}&\text{misses }c:\ ac,zc,qc\in E(H)\\
z&\{a,y,q\}&\text{misses }x_1:\ ax_1,yx_1,qx_1\in E(H)\\
q&\{a,y,z\}&\text{misses }x_2:\ ax_2,yx_2,zx_2\in E(H).
\end{array}
\tag{4.16}
\]

No retained response exists.  Notice in particular the exact pairing
in (4.13): \(\{a,y,z\}\) misses \(x_2\), while
\(\{a,x_0,y\}\) misses \(x_1\).

### 4.5 The five-cycle `00101`

Let

\[
  p-q-u-r-v-p
\tag{4.17}
\]

have types \(a,a,b,a,b\), respectively.  Lemma 1.3 applied to the two
adjacent cross edges \(qu\) and \(ur\) supplies type-\(c\) vertices
\(t,s\) such that

\[
  tq,tu\in E(H),\qquad su,sr\in E(H).
\tag{4.18}
\]

No cycle vertex has type \(c\), so \(t,s\) lie outside the cycle and
outside \(S\).  There are exactly two collision cases: \(t=s\) and
\(t\ne s\).

The direct response

\[
  D_0=\{a,b,v\}=S-c+v
\]

is retained.  Attack \(r\).  Guards \(a,v\) are blocked by
\(ar,vr\in E(H)\), so closure forces

\[
  D_1=\{a,r,v\}.
\tag{4.19}
\]

Attack \(q\).  Guard \(a\) is blocked by \(aq\in E(H)\).  Moving \(r\)
gives \(\{a,q,v\}\), which misses \(p\) by
\(ap,qp,vp\in E(H)\).  Hence closure forces

\[
  D_2=\{a,q,r\}.
\tag{4.20}
\]

Attack \(u\).  Guards \(q,r\) are blocked by \(qu,ru\in E(H)\), so
closure forces

\[
  D_3=\{q,u,r\}.
\tag{4.21}
\]

If \(t=s\), the state \(D_3\) does not dominate \(t\), because

\[
  tq,tu,tr\in E(H).
\]

Suppose \(t\ne s\).  Attack the unoccupied anchor \(c\) from \(D_3\).

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{reason invalid}\\ \hline
q&\{c,u,r\}&\text{misses }s:\ cs,us,rs\in E(H)\\
u&\{c,q,r\}&\text{misses }a:\ ca,qa,ra\in E(H)\\
r&\{c,q,u\}&\text{misses }t:\ ct,qt,ut\in E(H).
\end{array}
\tag{4.22}
\]

There is no retained response.  The equality and inequality cases
exhaust every possible collision between the two gamma witnesses.

## 5. Signed balance and coloring

### Theorem 5.1 (signed balance)

Every cycle of \(H-S\) contains an even number of same-type edges.

#### Proof

Otherwise Lemma 3.1 gives a shortest unbalanced cycle of length at most
five.  Lemma 3.2 reduces it to one of the five words in (3.1).
Sections 4.1--4.5 exclude all five. \(\square\)

Choose one vertex in each connected component of \(H-S\), give it an
arbitrary chirality, and propagate (2.3) along paths.  Theorem 5.1 makes
the result path-independent.  Convert chirality to the allowed anchor
color by (2.1), and give \(a,b,c\) their three distinct colors.  Section
2 proves this is a proper three-coloring of \(H\).  Therefore

\[
  \theta(G)=\chi(H)\le3.
\]

Since \(S\) is independent in \(G\), it is a triangle in \(H\), so
\(\chi(H)\ge3\).  Consequently

\[
  \boxed{\theta(G)=3.}
\tag{5.1}
\]

## 6. Reproduction and audit boundary

Run

```text
python3 -I -B -W error \
  math/working/signed_balance_endgame/verify_symbolic.py
```

The checker:

- enumerates the unbalanced type-word orbits through length five;
- verifies the bipartite/side-purity reductions;
- checks every root as an exact-list direct response;
- checks every attack is unoccupied;
- checks each blocked move from a literal \(H\)-edge;
- checks every claimed domination miss from three literal \(H\)-edges;
- checks both collision cases in `00101`; and
- checks the final coloring truth table.

The checker is a symbolic audit of the written attack trees, not a
substitute for hostile line-by-line proof review.  No bounded SAT result
is promoted as an arbitrary-order theorem.
