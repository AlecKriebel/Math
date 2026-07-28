# The dynamic fate of the all-parameter obstruction \(Y_k\)

## Status and exact boundary

Date: 2026-07-28 (PDT)

This note studies the abstract obstruction

\[
Y_k=K_{k-3}\vee P_4
\]

from C-118 when it is realized by the **static** response lists of an
actual one-guard eternal family.  The conclusion is a proved dichotomy and
an exact explanation of why C-121 does not automatically lift.

Let \(\mathcal F\) be an eternal family of dominating \(k\)-sets in \(G\).
Fix an independent retained state

\[
S=B\mathbin{\dot\cup}D,\qquad
B=\{a,b,c\},\qquad |D|=k-3,
\]

and put \(H=\overline G\).  For \(v\notin S\), write

\[
L_S^{\mathcal F}(v)
=\{u\in S: S-u+v\in\mathcal F\}
\]

and

\[
L_S^{\rm stat}(v)
=\{u\in S:uv\in E(G),\ S-u+v\text{ dominates }G\}.
\]

As usual, membership in the family list includes the legal move edge, and

\[
L_S^{\mathcal F}(v)\subseteq L_S^{\rm stat}(v).
\tag{0.1}
\]

Assume there are vertices

\[
Z=\{z_d:d\in D\},\qquad X=\{x_0,x_1,x_2,x_3\},
\]

such that \(H[Z\cup X]\) is the join of the clique \(Z\) and the induced
path \(x_0x_1x_2x_3\), and the static lists are exactly

\[
L_S^{\rm stat}(z_d)=\{d\}\quad(d\in D),
\tag{0.2}
\]

\[
\begin{array}{c|cccc}
v&x_0&x_1&x_2&x_3\\ \hline
L_S^{\rm stat}(v)&
D\cup\{a\}&D\cup\{a,c\}&D\cup\{b,c\}&D\cup\{b\}.
\end{array}
\tag{0.3}
\]

For \(k=3\), \(D=Z=\varnothing\), and this is exactly C-121.  The new
content concerns \(k\geq4\).

The proved outcomes are:

1. the singleton clique can always be installed simultaneously;
2. the portions of the original family lists in the three base colors are
   forced to be the exact \(Y_3\) pattern;
3. if the installed singleton clique is cleanly separated from
   \(\{a,b,c\}\), freezing it gives an exact equality-three projection with
   the **family-list** \(Y_3\), and C-072 gives
   \[
   |V(G)|\geq 2k+6;
   \]
4. if the projected **static** lists also remain exact, C-121 improves this
   to
   \[
   |V(G)|\geq 2k+8;
   \]
5. there are two precise obstructions to the lift: a dirty singleton forces
   a private buffer, while even a clean replacement can repair a static
   defect and strictly enlarge the projected static list.

The last phenomenon is real.  A seven-vertex exact one-guard control is
checked by `verify.py`.  It has

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,4,4,4),
\]

so it is not an equality-\(4\) graph and not a counterexample.  It shows
that neither eternal closure nor a clean singleton replacement licenses
transporting static lists.

No all-order \(Y_k\) exclusion, no \(\mathsf{GL}(k)\), and no resolution of
the gamma--theta conjecture is claimed.

## 1. Simultaneous singleton installation

The restoration lemma relative to the independent state \(S\) says that
every \(F\in\mathcal F\) satisfies

\[
S-F\subseteq
\bigcup_{v\in F-S}L_S^{\mathcal F}(v).
\tag{1.1}
\]

By (0.1)--(0.2),

\[
L_S^{\mathcal F}(z_d)=\{d\}.
\tag{1.2}
\]

For \(R\subseteq D\), put

\[
T_R=(S-R)\cup\{z_d:d\in R\}.
\tag{1.3}
\]

### Lemma 1.1 (simultaneous singleton installation) — PROVED

For every \(R\subseteq D\),

\[
T_R\in\mathcal F.
\tag{1.4}
\]

In particular,

\[
T:=T_D=B\cup Z\in\mathcal F.
\tag{1.5}
\]

#### Proof

Induct on \(|R|\).  The state \(T_\varnothing=S\) is retained.  Suppose
\(T_R\) is retained and \(e\in D-R\).  Attack \(z_e\).  No installed
singleton \(z_d\), \(d\in R\), can move because \(Z\) is a clique in
\(H\), hence independent in \(G\).

Suppose a guard \(g\in S-R\), \(g\ne e\), moved.  The successor would miss
\(R\cup\{g\}\) from \(S\), while its outside positions would be
\(\{z_d:d\in R\}\cup\{z_e\}\).  By (1.2), the union of their family lists
is only \(R\cup\{e\}\), contradicting (1.1) at \(g\).  Thus \(e\) is the
unique possible responder, and the successor is \(T_{R\cup\{e\}}\).
\(\square\)

The state \(T\) need not be independent: a singleton vertex \(z_d\) may be
adjacent in \(G\) to a base anchor even though that anchor is excluded from
its static list.

## 2. The base portions of the original family lists are rigid

Put

\[
A_0=\{a\},\quad A_1=\{a,c\},\quad
A_2=\{b,c\},\quad A_3=\{b\}.
\tag{2.1}
\]

### Theorem 2.1 (all-\(k\) carried rigidity) — PROVED

Under (0.2)--(0.3),

\[
\boxed{
L_S^{\mathcal F}(x_i)\cap B=A_i
\quad(0\leq i\leq3).
}
\tag{2.2}
\]

The family lists may additionally contain colors in \(D\).

#### Proof

Attack \(x_0\) from \(T\).  No member of \(Z\) is adjacent to \(x_0\).
Thus a base guard \(u\in B\) responds and \(T-u+x_0\) is retained.
Restoration relative to \(S\) says that the missing base color \(u\) occurs
in \(L_S^{\mathcal F}(x_0)\).  By (0.1) and (0.3), \(u=a\).
Consequently

\[
a\in L_S^{\mathcal F}(x_0),\qquad
Z\cup\{b,c,x_0\}\in\mathcal F.
\tag{2.3}
\]

Reflection gives the corresponding statement with \(b,x_3\).

Attack \(x_1\) from the state in (2.3).  Neither \(Z\) nor \(x_0\) can
move.  If \(b\) moved, the successor
\[
Z\cup\{c,x_0,x_1\}
\]
would miss \(D\cup\{a,b\}\) from \(S\), while the union of the original
family lists of its outside positions is contained in
\[
D\cup\{a,c\}.
\]
This violates (1.1).  Hence \(c\) moves and

\[
Z\cup\{b,x_0,x_1\}\in\mathcal F.
\tag{2.4}
\]

Restoration at (2.4) forces
\[
c\in L_S^{\mathcal F}(x_1).
\tag{2.5}
\]
Reflection forces
\[
c\in L_S^{\mathcal F}(x_2),\qquad
Z\cup\{a,x_2,x_3\}\in\mathcal F.
\tag{2.6}
\]

Suppose \(b\notin L_S^{\mathcal F}(x_2)\).  Then the base portion of that
list is exactly \(\{c\}\).  Attack \(x_0\) from the state in (2.6).
The possible graph movers are \(a,x_2,x_3\).  Moving \(x_2\) produces a
state whose outside-list union is contained in
\(D\cup\{a,b\}\), but which misses \(c\).  Moving \(x_3\) produces a state
whose outside-list union is contained in \(D\cup\{a,c\}\), but which misses
\(b\).  Restoration excludes both, so \(a\) moves and

\[
Z\cup\{x_0,x_2,x_3\}\in\mathcal F.
\tag{2.7}
\]

Attack \(x_1\).  The path nonedges in \(G\) block \(x_0,x_2\), and every
member of \(Z\) is also blocked.  Thus \(x_3\) is the unique graph mover,
giving
\[
Z\cup\{x_0,x_1,x_2\}\in\mathcal F.
\]
This state misses all of \(S\), but under the supposition its
outside-list union is contained in \(D\cup\{a,c\}\), a contradiction.
Therefore \(b\in L_S^{\mathcal F}(x_2)\).  Reflection gives
\(a\in L_S^{\mathcal F}(x_1)\), completing (2.2). \(\square\)

This theorem carefully preserves the distinction between the original
family lists and the static lists.  It does **not** assert that the response
lists at \(T\), or in a later projection, equal the lists at \(S\).

## 3. Dirty singleton vertices force private buffers

For \(u\in S\), let

\[
P_S(u)=\{p:N_G[p]\cap S=\{u\}\}
\tag{3.1}
\]

be the closed private block of \(u\) relative to \(S\).

### Lemma 3.1 (private-buffer obstruction) — PROVED

If \(u\in S-\{d\}\) and \(uz_d\in E(G)\), then

\[
P_S(u)\cap N_H(z_d)\ne\varnothing.
\tag{3.2}
\]

#### Proof

Since \(u\notin L_S^{\rm stat}(z_d)\) but \(uz_d\in E(G)\), the state
\(S-u+z_d\) does not dominate.  Choose a missed vertex \(p\).  It is
nonadjacent in \(G\) to \(z_d\) and to every member of \(S-\{u\}\).

On the other hand, \(d\in L_S^{\rm stat}(z_d)\), so
\(S-d+z_d\) dominates.  This latter state contains \(u\), while all its
other members have just been shown nonadjacent to \(p\).  Hence \(up\) is
an edge.  Therefore \(N_G[p]\cap S=\{u\}\) and \(pz_d\in E(H)\).
\(\square\)

In particular, if a base anchor \(u\in B\) is adjacent to any singleton
vertex, the corresponding buffer is outside all \(2k+1\) named vertices
\(S\cup Z\cup X\): every path vertex is adjacent in \(G\) to all anchors
in \(D\), and every \(z_e\) is adjacent to its own anchor \(e\).
Buffers belonging to distinct base anchors are distinct.

This is the first obstruction to replacing \(D\) by \(Z\): such an edge
makes \(T=B\cup Z\) nonindependent, so the frozen-projection theorem cannot
use \(T\) as its independent reference state.

## 4. The clean lift to parameter three

Call the singleton installation **clean** when

\[
E_G(B,Z)=\varnothing.
\tag{4.1}
\]

Then \(T=B\cup Z\) is independent.  Define the common antineighborhood
projection

\[
J=G[\{v\notin Z:E_G(v,Z)=\varnothing\}].
\tag{4.2}
\]

Thus \(B\cup X\subseteq V(J)\).  Let

\[
\mathcal P=
\{C\in {V(J)\choose3}:Z\cup C\in\mathcal F\}.
\tag{4.3}
\]

### Lemma 4.1 (exact clean projection) — PROVED

Assume

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=k
\tag{4.4}
\]

and (4.1).  Then

\[
\gamma(J)=\alpha(J)=\gamma^\infty(J)=3,
\tag{4.5}
\]

\(\mathcal P\) is an eternal triple-family on \(J\), and its family
response lists at \(B\) on the path are exactly

\[
\{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
\tag{4.6}
\]

#### Proof

The family \(\mathcal P\) is nonempty because \(T\in\mathcal F\).  If
\(C\in\mathcal P\) and \(r\in V(J)-C\) is attacked from \(Z\cup C\), no
guard in \(Z\) is adjacent to \(r\).  Thus a guard of \(C\) responds, and
the residual successor remains in \(\mathcal P\).  The same observation
shows that each residual triple dominates \(J\).

The independent triple \(B\) gives \(\alpha(J)\geq3\).  An independent
four-set in \(J\), together with the independent \(Z\), would be an
independent \((k+1)\)-set in \(G\), so \(\alpha(J)=3\).  Hence
\(\gamma^\infty(J)=3\).  If a pair dominated \(J\), adjoining \(Z\) would
dominate \(G\): every vertex outside \(J\cup Z\) has a graph neighbor in
\(Z\).  This would contradict \(\gamma(G)=k\), proving (4.5).

Let \(M_i\) be the family-response list of \(x_i\) at \(B\) in
\(\mathcal P\).  It is nonempty.  A member \(u\in M_i\) gives the retained
state \(T-u+x_i\).  Restoration relative to the original state \(S\)
forces
\[
u\in L_S^{\mathcal F}(x_i)\cap B=A_i.
\]
Thus \(M_i\subseteq A_i\).  Now apply the same restoration/attack argument
as in Theorem 2.1, this time relative to the independent state \(T\)
(equivalently, relative to \(B\) in \(\mathcal P\)).  Nonempty lists
contained respectively in
\[
\{a\},\{a,c\},\{b,c\},\{b\}
\]
are forced to equal those four caps.  This proves (4.6). \(\square\)

### Theorem 4.2 (clean \(Y_k\) order floor) — PROVED

Under (4.4), every clean exact static \(Y_k\) realization satisfies

\[
\boxed{|V(G)|\geq2k+6.}
\tag{4.7}
\]

#### Proof

Lemma 4.1 gives an equality-three graph \(J\) with the exact family-list
mixed \(P_4\).  Accepted C-072 gives \(|V(J)|\geq12\).

No anchor \(d\in D\) belongs to \(J\), because \(dz_d\in E(G)\), and no
member of \(Z\) belongs to \(J\) by definition.  Thus the \(2(k-3)\)
vertices \(D\cup Z\) lie outside \(J\), and
\[
|V(G)|\geq |V(J)|+2(k-3)\geq12+2(k-3)=2k+6.
\]
\(\square\)

This is a genuine all-\(k\) theorem, but it uses C-072, not the stronger
static-defect conclusion of C-121.

## 5. Exactly when C-121 also lifts

Let \(\widehat L_i\) be the static response list of \(x_i\) relative to
the independent triple \(B\) **inside \(J\)**.  Lemma 4.1 gives

\[
A_i\subseteq\widehat L_i.
\tag{5.1}
\]

For \(u\in B-A_i\), the exact criterion is

\[
u\notin\widehat L_i
\quad\Longleftrightarrow\quad
ux_i\notin E(G)
\ \text{or}\
N_{H[J]}\bigl((B-\{u\})\cup\{x_i\}\bigr)\ne\varnothing.
\tag{5.2}
\]

The second alternative is precisely a static defect which survives in the
projection.

### Corollary 5.1 (static-survival improvement) — PROVED

If every forbidden base role in (5.2) remains forbidden, equivalently

\[
\widehat L_i=A_i\qquad(0\leq i\leq3),
\tag{5.3}
\]

then

\[
\boxed{|V(G)|\geq2k+8.}
\tag{5.4}
\]

#### Proof

Now C-121 applies to \(J\) and gives \(|V(J)|\geq14\).  Add the
\(2(k-3)\) excluded vertices \(D\cup Z\). \(\square\)

The original exact static lists do not imply (5.3).  If
\(u\notin A_i\) but \(ux_i\in E(G)\), original exactness supplies a witness
in

\[
N_H\bigl((S-\{u\})\cup\{x_i\}\bigr).
\tag{5.5}
\]

That witness can be adjacent in \(G\) to a frozen singleton vertex and
therefore disappear from \(J\).  Replacing \(D\) by \(Z\) can consequently
repair the failed swap.  Static lists are not functorial under this
projection.

## 6. A sharp static-repair control

Let \(G\) have vertices \(0,\ldots,6\) and edges

\[
05,\quad25,\quad26,\quad34,\quad46.
\tag{6.1}
\]

Its labeled graph6 string is

```text
F?E`O
```

Take

\[
S=\{0,1,2,3\},\quad d=3,\quad z=4,\quad
T=\{0,1,2,4\},\quad x=5.
\]

The greatest eternal four-family consists of the eight states

\[
\begin{split}
&0123,\ 0124,\ 0136,\ 0146,\\
&1235,\ 1245,\ 1356,\ 1456.
\end{split}
\tag{6.2}
\]

Both \(S\) and the clean replacement \(T\) are independent and retained.
At \(S\),

\[
L_S^{\rm stat}(z)=L_S^{\mathcal F}(z)=\{3\},
\qquad
L_S^{\rm stat}(x)=L_S^{\mathcal F}(x)=\{0\}.
\tag{6.3}
\]

But after replacing \(3\) by \(4\),

\[
L_T^{\rm stat}(x)=\{0,2\},
\qquad
L_T^{\mathcal F}(x)=\{0\}.
\tag{6.4}
\]

The original failed \(2\)-swap is witnessed by vertex \(6\); the frozen
singleton \(4\) is adjacent to \(6\), so it repairs that defect.  The
common antineighborhood projection has parameters

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\]

The full graph has

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,4,4,4).
\]

Thus the missing equality \(\gamma=4\) is visible exactly in the projected
domination number.  This control does not refute Theorem 4.2 or any
equality-specific strengthening.  It does refute the unqualified inference
that static response lists survive a clean singleton replacement.

Run

```text
python3 -I -B -W error \
  math/working/all_k_yk_dynamic/verify.py
```

to reconstruct all parameters, the greatest kernel, every unoccupied
one-guard obligation in (6.2), both static/family list systems, and the
projected defect repair.

## 7. Final verdict

The exact all-\(k\) picture reached here is

\[
\boxed{
\begin{array}{l}
\text{exact static }Y_k\\
\quad\Longrightarrow\quad
\text{simultaneous singleton state and exact original base family pattern};\\
\text{clean singleton installation}\\
\quad\Longrightarrow\quad
\text{equality-three projection with exact family }Y_3,\ n\geq2k+6;\\
\text{clean installation plus static-defect survival}\\
\quad\Longrightarrow\quad
\text{C-121 projection},\ n\geq2k+8.
\end{array}}
\]

If cleanliness fails, Lemma 3.1 identifies an explicit private buffer.  If
static-defect survival fails, (5.2) identifies the exact repaired swap.
Those are the two concrete gates left by the current proof technology.
Neither gate is merely a change of notation, and neither can be crossed by
assuming that projected response lists equal the original ones.

