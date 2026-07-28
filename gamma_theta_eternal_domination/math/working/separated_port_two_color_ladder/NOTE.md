# Two-color completion of the separated-port cap ladder

## Status and exact scope

Date: 2026-07-27 (PDT)

All statements use the standard one-guard-moves eternal domination model.
The family \(\mathcal F\) is arbitrary and is not assumed to be the
greatest eternal family.

The human results in this note are:

1. **PROVED:** after the first \(a\)-positive cap and \(a\)-omitting
   escape, every outside completion of the escape edge has an exact
   five-vertex bow-tie form.  That form has no complement \(K_4\), gives
   an \(H\)-common neighbor to every one of its vertex pairs, and need not
   contain the odd fan of C-079.
2. **PROVED:** in the exact old response-list pattern, no vertex can be a
   common complement cap of the two consecutive \(c\)-omitting edges
   \(rs\) and \(sq\).
3. **PROVED:** the two \(c\)-caps are therefore distinct from one another
   and from the previously forced \(a\)-cap and \(a\)-escape.  Hence the
   exact list pattern has order at least thirteen.  At order thirteen the
   next \(c\)-escape must equal the \(a\)-escape and must have singleton
   response list \(\{b\}\); otherwise the order is at least fourteen.
4. **CERTIFIED-FINITE CONTROL:** the graph
   `JFzvvn{~fM?` has an exact 109-state eternal family realizing the safe
   bow-tie return, with
   \[
     (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
   \]
   Thus the bow-tie is compatible with literal one-guard closure, but the
   control does not satisfy domination equality.

The note does **not** eliminate the exact separated-port pattern under
\(\gamma=3\).  In particular, the order-thirteen singleton branch and
longer alternating link cycles remain open.  No claim here resolves the
\(k=3\) slice or the gamma--theta conjecture.

The accepted prerequisites are C-079, C-082, C-083, and the full-link
no-isolate theorem in:

- `math/working/k3_long_bicycle_connectors/NOTE.md`;
- `math/working/dynamic_connector_edge_caps/NOTE.md`;
- `math/working/gamma3_port_identification_proof/NOTE.md`; and
- `math/working/k3_full_list_slice/NOTE.md`.

## 1. Exact setup

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad H=\overline G,
\tag{1.1}
\]

let \(\mathcal F\) be an eternal family of triples, and fix the independent
state

\[
 S=\{a,b,c\}\in\mathcal F.
\tag{1.2}
\]

For \(v\notin S\), write

\[
 L(v)=\{u\in S:S-u+v\in\mathcal F\}.
\tag{1.3}
\]

The graph edge \(uv\in E(G)\) is automatic whenever \(u\in L(v)\).
For a fixed anchor \(a\), put

\[
 P_a=\{v\notin S:a\in L(v)\},
 \qquad
 W_a=\{v\notin S:a\notin L(v)\}.
\tag{1.4}
\]

The exact old response lists are

\[
\begin{array}{c|cccccc}
v&x&r&s&q&v_0&v_1\\ \hline
L(v)&
\{a,b,c\}&\{a,b\}&\{a,b\}&\{a,b\}&\{b,c\}&\{b,c\}.
\end{array}
\tag{1.5}
\]

The nine old vertices induce exactly

\[
\begin{split}
E(H)=\{&
ab,ac,bc,\ xr,rs,sq,qv_1,v_1v_0,v_0r
\}.
\end{split}
\tag{1.6}
\]

In particular, every old outside vertex is adjacent in \(G\) to every
anchor.

C-083 supplies two new vertices \(z,w\), distinct from the old nine and
from one another, such that

\[
\begin{aligned}
 &zv_0,zv_1\in E(H),\qquad a\in L(z),\\
 &zx,zr,zs,zq\in E(G),\\
 &wx,wz\in E(H),\qquad a\notin L(w),
\end{aligned}
\tag{1.7}
\]

and \(w\) is adjacent in \(H\) to at most one of \(v_0,v_1\).

## 2. Positive-tail neighborhood independence

### Lemma 2.1

Let \(p,q\notin S\) be distinct, suppose

\[
 p\in P_a,\qquad pq\in E(H).
\tag{2.1}
\]

Then

\[
 H[N_H(q)\cap W_a]
\tag{2.2}
\]

is edgeless.

#### Proof

If distinct \(u,v\in N_H(q)\cap W_a\) had \(uv\in E(H)\), then the four
distinct outside vertices \(p,q,u,v\) would satisfy

\[
 pq,qu,qv,uv\in E(H),
 \qquad
 a\in L(p),
 \qquad
 a\notin L(u)\cup L(v).
\]

This is C-079 with path length one. \(\square\)

The exact core has \(r\in P_a\) and \(rx\in E(H)\).  Consequently,

\[
 H[N_H(x)\cap W_a]
\quad\text{is edgeless.}
\tag{2.3}
\]

This is stronger than bipartiteness for the \(a\)-omitting part of the
full link.

## 3. First-return bow-tie classification

Put

\[
 J_x=H[N_H(x)].
\tag{3.1}
\]

The full-link theorem says that \(J_x\) is bipartite with no isolated
vertices.  Since \(w\in N_H(x)\), choose

\[
 p\in N_{J_x}(w).
\tag{3.2}
\]

Thus

\[
 xp,wp\in E(H).
\tag{3.3}
\]

Equation (2.3) and \(w\in W_a\) give

\[
 p\in P_a.
\tag{3.4}
\]

The \(a\)-cap \(z\) is \(G\)-complete to every other outside member of
\(P_a\), by C-083.  Hence

\[
 zp\in E(G).
\tag{3.5}
\]

Among the old vertices, only \(r\) lies in \(N_H(x)\), so either

\[
 p=r
\quad\text{or}\quad
 p\text{ is new.}
\tag{3.6}
\]

### Theorem 3.1 (outside completion is a bow-tie)

Let

\[
 t\in N_H(z)\cap N_H(w).
\tag{3.7}
\]

Such a \(t\) exists because \(\gamma(G)=3\).  Then:

1. \(t\in\{b,c\}\cup W_a\);
2. if \(t\notin S\), then
   \[
   xt,pt\in E(G);
   \tag{3.8}
   \]
3. in the outside case, the induced complement on
   \(\{x,p,w,z,t\}\) consists exactly of the two triangles
   \[
   xpw,\qquad zwt,
   \tag{3.9}
   \]
   sharing the vertex \(w\).

#### Proof

The vertices \(a,x\) cannot be \(t\), since \(az,xz\in E(G)\).
If an outside \(t\) belonged to \(P_a\), cap completeness would give
\(zt\in E(G)\), contrary to (3.7).  This proves item 1.

Now suppose \(t\) is outside.  Then \(w,t\in W_a\) and \(wt\in E(H)\).
If \(xt\in E(H)\), the edge \(wt\) would contradict (2.3).  Thus
\(xt\in E(G)\).

If \(pt\in E(H)\), apply Lemma 2.1 with positive vertex \(x\) and hub
\(p\).  Both \(w,t\) lie in \(N_H(p)\cap W_a\), and \(wt\in E(H)\), a
contradiction.  Hence \(pt\in E(G)\).

The six complement edges in the two triangles are

\[
 xp,xw,pw,\qquad zw,zt,wt.
\]

The four remaining pairs are in \(G\): \(xz\) comes from (1.7), \(zp\)
from (3.5), and \(xt,pt\) from item 2.  This proves item 3. \(\square\)

Every pair of vertices in the bow-tie has an \(H\)-common neighbor:
pairs internal to a triangle use its third vertex, and every cross pair
uses \(w\).  Thus the bow-tie itself creates no dominating pair.  Its
largest \(H\)-cliques are its two triangles, and it contains no forced
C-079 instance.

### Proposition 3.2 (anchor completion)

At most one of \(b,c\) can lie in \(N_H(z)\cap N_H(w)\).  If that anchor
is \(h\), and \(d\) is the other member of \(\{b,c\}\), then

\[
 L(w)=\{d\}.
\tag{3.10}
\]

Moreover, the independent state \(\{h,z,w\}\) attacked at \(d\) has the
forced response

\[
 w\longrightarrow d,
 \qquad
 \{h,d,z\}=S-a+z\in\mathcal F.
\tag{3.11}
\]

#### Proof

If both anchors were common neighbors, then
\(\{b,c,z,w\}\) would induce a complement \(K_4\).

Now let \(h\) be one common anchor.  Since \(w\in W_a\), the color \(a\)
is absent from \(L(w)\), and the graph nonedge \(hw\in E(H)\) excludes
\(h\).  Closure at the attack \(w\) from \(S\) makes \(L(w)\) nonempty,
so its only possible member is \(d\).

The complement triangle \(\{h,z,w\}\) is a maximum independent triple,
hence belongs to \(\mathcal F\).  On attack \(d\), the guard \(h\) cannot
move.  A move by \(z\), if present, lands in
\(\{h,d,w\}=S-a+w\), which is absent.  Closure therefore forces the move
by \(w\), proving (3.11). \(\square\)

Thus the anchor case is absent, for example, whenever
\(L(w)=\{b,c\}\).

### Corollary 3.3 (exact old return)

Assume \(p=r\) in (3.6), and suppose the outside common neighbor \(t\)
from Theorem 3.1 is one of the old \(a\)-omitting endpoints.  Then

\[
 t=v_1.
\tag{3.12}
\]

Indeed, Theorem 3.1 gives \(rt\in E(G)\), whereas
\(rv_0\in E(H)\) and \(rv_1\in E(G)\).

In this surviving return,

\[
 v_0-v_1-w
\tag{3.13}
\]

is an even \(W_a\)-path.  The same cap \(z\) caps both edges
\(v_0v_1\) and \(v_1w\), while \(x-r-w\) is the positive link triangle.
Thus all of the local cap, escape, and link obligations can repeat
without a new vertex.

By contrast:

- if \(w\) sees both \(v_0,v_1\), then
  \(H[\{z,w,v_0,v_1\}]=K_4\);
- if \(p=r\) and \(wv_0\in E(H)\), C-079 applies with positive vertex
  \(x\), hub \(r\), and path \(w-v_0\).

The far-terminal return \(wv_1\) is the parity-compatible exception.

## 4. The second omitted color

The exact lists (1.5) give

\[
 r,s,q\in W_c,
\qquad
 rs,sq\in E(H).
\tag{4.1}
\]

Both omissions are dynamic because all old outside vertices are adjacent
in \(G\) to every anchor.

### Lemma 4.1 (no common cap over the two-edge connector)

There is no vertex \(y\) satisfying

\[
 yr,ys,yq\in E(H).
\tag{4.2}
\]

#### Proof

Fullness of \(x\) gives

\[
 D_0=S-a+x=\{b,c,x\}\in\mathcal F.
\]

Attack \(v_0\).  A response by \(x\) lands in
\(S-a+v_0\), which is absent because \(v_0\in W_a\).  Hence closure gives

\[
 D_1=\{h,x,v_0\}\in\mathcal F
\tag{4.3}
\]

for some \(h\in\{b,c\}\).

Attack \(v_1\).  The guard at \(v_0\) cannot move because
\(v_0v_1\in E(H)\).  A move by \(x\), if available, lands in
\(\{h,v_0,v_1\}\), which is absent by the C-079 dead-state lemma.
Closure therefore forces

\[
 D_2=\{x,v_0,v_1\}\in\mathcal F.
\tag{4.4}
\]

Attack \(s\) from \(D_2\).  The three possible successor states are all
absent:

1. \(\{x,s,v_0\}\) does not dominate \(r\), since
   \(rx,rs,rv_0\in E(H)\).
2. The state \(\{s,v_0,v_1\}\) cannot answer an attack at \(y\).
   The guard at \(s\) cannot move.  A move by \(v_0\) gives
   \(\{s,y,v_1\}\), which misses \(q\), while a move by \(v_1\) gives
   \(\{s,y,v_0\}\), which misses \(r\).
3. The state \(\{x,s,v_1\}\) also cannot answer \(y\).  The guard at
   \(s\) cannot move.  Moving \(x\) gives \(\{y,s,v_1\}\), which misses
   \(q\), while moving \(v_1\) gives \(\{x,s,y\}\), which misses \(r\).

Thus \(D_2\) has no retained response to the attack \(s\), contradicting
closure. \(\square\)

This lemma uses only the exact old induced complement, fullness of \(x\),
and the two \(a\)-omitting lists at \(v_0,v_1\).  It does not assume any
response list for \(y\).

### Theorem 4.2 (two distinct \(c\)-caps)

C-082 applied to the two edges in (4.1) gives nonempty cap sets

\[
 C_{rs}=N_H(r)\cap N_H(s),
 \qquad
 C_{sq}=N_H(s)\cap N_H(q),
\tag{4.5}
\]

whose members are outside \(P_c\)-vertices.  These sets satisfy

\[
\begin{aligned}
 &C_{rs}\cap C_{sq}=\varnothing,\\
 &C_{rs}\subseteq N_G(q),\\
 &C_{sq}\subseteq N_G(r).
\end{aligned}
\tag{4.6}
\]

#### Proof

A vertex in both cap sets, a member of \(C_{rs}\) adjacent in \(H\) to
\(q\), or a member of \(C_{sq}\) adjacent in \(H\) to \(r\), would
satisfy (4.2).  Lemma 4.1 excludes all three possibilities. \(\square\)

Choose

\[
 y_0\in C_{rs},
 \qquad
 y_1\in C_{sq}.
\tag{4.7}
\]

Both vertices are new: the exact old common neighborhoods of \(rs\) and
\(sq\) are empty.  They are distinct by (4.6).

They are also distinct from the \(a\)-cap \(z\), because (1.7) makes
\(z\) adjacent in \(G\) to \(r,s,q\).  Finally they are distinct from
the \(a\)-escape \(w\): cap completeness for color \(c\) gives

\[
 xy_0,xy_1\in E(G),
\tag{4.8}
\]

because \(x\in P_c\), whereas \(xw\in E(H)\).

The four vertices

\[
 z,w,y_0,y_1
\tag{4.9}
\]

are therefore pairwise distinct and new relative to the exact old
nine-vertex core.

### Corollary 4.3 (order floor and cross-color identification)

Every equality realization of the exact induced core and exact response
lists (1.5) has

\[
 |V(G)|\geq 13.
\tag{4.10}
\]

Moreover, either

\[
 |V(G)|\geq14,
\tag{4.11}
\]

or the \(a\)-escape has the singleton list

\[
 L(w)=\{b\}.
\tag{4.12}
\]

#### Proof

The old core has nine vertices, and (4.9) supplies four distinct new
vertices, proving (4.10).

Consider the cap \(y_1\) of \(sq\).  Equation (4.8) and
\(\gamma(G)=3\) give

\[
 u\in N_H(x)\cap N_H(y_1).
\tag{4.13}
\]

The full vertex \(x\) is adjacent in \(G\) to every anchor, so
\(u\notin S\).  Cap completeness for \(y_1\) excludes every outside
member of \(P_c\), hence

\[
 u\in W_c.
\tag{4.14}
\]

Among the old vertices, only \(r\) belongs to \(N_H(x)\), but
\(ry_1\in E(G)\) by (4.6).  The previously forced vertices
\(z,y_0\) are also adjacent to \(x\) in \(G\).  Therefore

\[
 u=w
\quad\text{or}\quad
 u\text{ is a fifth new vertex.}
\tag{4.15}
\]

The second alternative gives (4.11).  In the first,
\(w\in W_a\cap W_c\), so \(L(w)\subseteq\{b\}\).  The attack at \(w\)
from \(S\) forces at least one direct response, hence \(L(w)\ne\varnothing\)
and (4.12) follows. \(\square\)

Thus an order-thirteen realization, if one exists, must identify the
first escapes in the two omitted-color systems at one singleton-\(b\)
vertex.

## 5. The genuine alternating-cycle boundary

Equation (2.3) implies that every link edge incident with an
\(a\)-omitting vertex has its other endpoint in \(P_a\).  Therefore any
strictly role-alternating nonbacktracking link walk has the form

\[
 W_a-P_a-W_a-P_a-\cdots.
\tag{5.1}
\]

If such a walk is forced to continue and first repeats a vertex, its
shortest repeated segment is an even cycle.  The complement graph induced
by that cycle and \(x\) has no \(K_4\): the link is bipartite.  Every pair
of cycle vertices has common \(H\)-neighbor \(x\), and \(x\) with a cycle
vertex has one of its cycle neighbors as a common \(H\)-neighbor.  No
edge of the cycle has two \(W_a\)-endpoints, so C-079 does not apply
directly.

This is only a stopping-boundary classification.  The present lemmas do
not force a \(P_a\)-link vertex to have a second \(W_a\)-neighbor, so an
alternating walk may stop or backtrack before making a cycle.

## 6. Exact finite safe-return control

Use the labels

\[
0=a,\ 1=b,\ 2=c,\ 3=x,\ 4=r,\ 5=s,\ 6=q,
7=v_0,\ 8=v_1,\ 9=z,\ 10=w.
\tag{6.1}
\]

Let \(G\) have labeled graph6 record

```text
JFzvvn{~fM?
```

and complement edges

\[
\begin{split}
E(H)=\{&
01,02,12,\ 34,45,56,68,78,47,\\
&79,89,9\,10,3\,10,4\,10,8\,10
\}.
\end{split}
\tag{6.2}
\]

Define \(\mathcal F\) reproducibly as follows:

1. begin with every dominating triple except the direct swaps forbidden
   by
   \[
   \begin{array}{c|cccccccc}
   v&x&r&s&q&v_0&v_1&z&w\\ \hline
   L(v)&012&01&01&01&12&12&01&12;
   \end{array}
   \tag{6.3}
   \]
2. simultaneously delete every state having an unoccupied attack with no
   one-guard successor remaining;
3. repeat to the fixed point.

The independent verifier obtains:

\[
\begin{aligned}
 |\mathcal F|&=109,\\
 \text{deletion-round sizes}&=(20,4,5,5,2),\\
 \text{attack obligations}&=109(11-3)=872,
\end{aligned}
\tag{6.4}
\]

and all obligations pass.  The exact lists are those in (6.3).

The anchor triangle and absence of a complement \(K_4\) give
\(\alpha=3\).  The eternal family gives \(\gamma^\infty=3\).  The pair
\(\{a,x\}\) dominates and no vertex is universal, so \(\gamma=2\).
The proper complement coloring

\[
\{a,r,v_1\}\mid
\{b,s,v_0,w\}\mid
\{c,x,q,z\}
\tag{6.5}
\]

gives \(\theta=3\).  Hence

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{6.6}
\]

For color \(a\), the cap \(z\) covers both \(v_0v_1\) and \(v_1w\), and
the two complement triangles

\[
xrw,\qquad zv_1w
\tag{6.7}
\]

form the bow-tie of Theorem 3.1.  The verifier finds no C-079 embedding
for any omitted color.  For color \(c\), however,

\[
N_H(r)\cap N_H(s)
=
N_H(s)\cap N_H(q)
=\varnothing.
\tag{6.8}
\]

Thus, in the part of the geometry governed by Theorem 4.2, the control
stops before the two \(c\)-caps forced by domination equality.  It also
has other dominating pairs; no claim is made that the two displayed pairs
are its only failures of \(\gamma=3\).

Classification: **CERTIFIED-FINITE CONTROL**, not an equality
countermodel and not a universal theorem.

## 7. Reproduction and pinned hashes

From the repository root:

```text
python3 math/working/separated_port_two_color_ladder/verify.py \
  > /tmp/separated_port_two_color_ladder_result.json
cmp /tmp/separated_port_two_color_ladder_result.json \
  math/working/separated_port_two_color_ladder/result.json
shasum -a 256 \
  math/working/separated_port_two_color_ladder/verify.py \
  math/working/separated_port_two_color_ladder/result.json
```

Expected SHA-256 values:

```text
a2f5a63f15f6c2808cd190b83fcc07b172eddcca385b679c0cbf92eacb4fb059  verify.py
4faceb740ee28d22db17c8544e21b80e6720a858f637df996250c7859169a1e0  result.json
```

The exact 109-state family, serialized as sorted comma-separated triples
with one state per line, has SHA-256

```text
34ad69cf11195558c2743fcb6332c2d4cef0750f7eb95be715aa892fd9733eb6
```

No novelty or literature-priority claim is made.
