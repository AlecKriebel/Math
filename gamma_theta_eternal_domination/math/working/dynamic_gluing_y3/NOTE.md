# The dynamic fate of the abstract \(Y_3=P_4\) gluing obstruction

## Status and scope

Date: 2026-07-28 (PDT)

Let \(G\) be a finite simple graph, let \(\mathcal F\) be an arbitrary
one-guard eternal family of triples, and let

\[
S=\{a,b,c\}\in\mathcal F
\]

be independent.  Put \(H=\overline G\).  Family and static response lists
at \(S\) are denoted by

\[
L^{\mathcal F}(x)
=\{u\in S:S-u+x\in\mathcal F\},
\]

\[
L^{\rm stat}(x)
=\{u\in S:ux\in E(G),\ S-u+x\text{ dominates }G\}.
\]

For an independent reference state, membership of \(S-u+x\) in
\(\mathcal F\) already forces \(ux\in E(G)\), so

\[
L^{\mathcal F}(x)\subseteq L^{\rm stat}(x).
\tag{0.1}
\]

This note answers the first dynamic question raised by C-118 at \(k=3\).
The abstract instance \(Y_3\) is the complement path

\[
x_0x_1x_2x_3
\tag{0.2}
\]

with lists

\[
\{a\},\qquad \{a,c\},\qquad \{b,c\},\qquad \{b\}.
\tag{0.3}
\]

The outcomes are:

1. **Literal realization is impossible:** if these are all four vertices
   outside \(S\), then \(\{x_1,x_2\}\) dominates \(G\), so
   \(\gamma(G)\leq2\).
2. **PROVED:** if (0.3) is realized by the *static* lists on an induced
   complement \(P_4\), full one-guard closure forces the *family* lists on
   those four vertices to equal (0.3) exactly.  Thus the static C-117/C-118
   gluing gap really enters the already studied dynamic mixed-\(P_4\)
   branch; it cannot hide behind a smaller family list.
3. **PROVED, finite local lemma:** the two endpoint failures of the omitted
   middle-color static swaps cannot share one witness.  The proof checks
   all \(16\) remaining adjacencies of an eight-vertex core using the
   greatest restoration-compatible one-guard kernel.
4. **PROVED conditional order bound:** under
   \(\gamma=\alpha=\gamma^\infty=3\), every embedded exact static
   \(Y_3\) forces two new, distinct static-defect vertices in addition to
   the five separated dynamic witness systems of C-070/C-072.  Hence

   \[
   \boxed{|V(G)|\geq14.}
   \tag{0.4}
   \]

The embedded pattern has **not** been excluded at arbitrary order.  Since
the exact static \(Y_3\) is itself uncolorable, any equality graph realizing
it would already have \(\theta(G)>3\), hence would be a genuine
counterexample.  Accordingly, (0.4) is a structural obstruction to one
minimal gluing core, not a proof of \(\mathsf{GL}(3)\), the complete
\(k=3\) case, or the universal gamma--theta conjecture.

The accepted dependencies used below are restoration, independent-state
forcing, ridge response covariance, and C-067/C-070/C-072.  No
greatest-family hypothesis is used in the proofs.

## 1. The literal seven-vertex instance has a dominating pair

### Proposition 1.1 — PROVED

Suppose

\[
V(G)=S\cup\{x_0,x_1,x_2,x_3\},
\]

\(x_0x_1x_2x_3\) is an induced path in \(H\), and the positive static
incidences in (0.3) hold.  Then

\[
\gamma(G)\leq2.
\]

#### Proof

The pair \(\{x_1,x_2\}\) dominates the two occupied vertices.  It sees all
three anchors: \(a,c\) see \(x_1\), and \(b,c\) see \(x_2\), by the
positive incidences in (0.3).  Finally, inducedness of the complement path
gives

\[
x_0x_2,\ x_1x_3\in E(G).
\]

Thus the pair also sees \(x_0,x_3\), and dominates all seven vertices.
\(\square\)

Consequently the literal abstract \(Y_3\) cannot be the whole response
instance of a graph with \(\gamma(G)=3\).  Any equality realization of its
minimal obstruction structure must contain vertices outside the displayed
seven.

## 2. Static \(Y_3\) is dynamically rigid

We use arbitrary-state restoration in the form

\[
S-D\subseteq
\bigcup_{v\in D-S}L^{\mathcal F}(v)
\qquad(D\in\mathcal F).
\tag{2.1}
\]

### Theorem 2.1 (static-to-family \(Y_3\) rigidity) — PROVED

Suppose \(x_0x_1x_2x_3\) is an induced path in \(H\) and

\[
\begin{array}{c|cccc}
x&x_0&x_1&x_2&x_3\\ \hline
L^{\rm stat}(x)&
\{a\}&\{a,c\}&\{b,c\}&\{b\}.
\end{array}
\tag{2.2}
\]

Then

\[
\boxed{
L^{\mathcal F}(x_i)=L^{\rm stat}(x_i)
\quad(0\leq i\leq3).
}
\tag{2.3}
\]

This statement needs neither \(\gamma(G)=3\) nor
\(\alpha(G)=3\).

#### Proof

Every family list is nonempty because \(x_i\) can be attacked from \(S\).
By (0.1), the endpoint lists are therefore already forced:

\[
L^{\mathcal F}(x_0)=\{a\},\qquad
L^{\mathcal F}(x_3)=\{b\}.
\tag{2.4}
\]

The attack at \(x_0\) from \(S\) uniquely retains

\[
A_0=\{b,c,x_0\}\in\mathcal F.
\tag{2.5}
\]

Attack \(x_1\) from \(A_0\).  The guard at \(x_0\) cannot move because
\(x_0x_1\in E(H)\).  Moving \(b\), if its graph edge exists, would give

\[
\{c,x_0,x_1\}.
\]

This state violates restoration: it misses \(a,b\), whereas

\[
L^{\mathcal F}(x_0)\cup L^{\mathcal F}(x_1)
\subseteq\{a,c\}.
\]

Hence closure moves \(c\) and retains

\[
Q_L=\{b,x_0,x_1\}\in\mathcal F.
\tag{2.6}
\]

Restoration at \(Q_L\) misses \(a,c\).  The endpoint \(x_0\) supplies
only \(a\), so

\[
c\in L^{\mathcal F}(x_1).
\tag{2.7}
\]

Reflection under

\[
a\leftrightarrow b,\qquad
x_0\leftrightarrow x_3,\qquad
x_1\leftrightarrow x_2,\qquad c\mapsto c
\tag{2.8}
\]

gives

\[
c\in L^{\mathcal F}(x_2),\qquad
Q_R=\{a,x_2,x_3\}\in\mathcal F.
\tag{2.9}
\]

Suppose now that \(b\notin L^{\mathcal F}(x_2)\).  Equations (0.1) and
(2.9) give

\[
L^{\mathcal F}(x_2)=\{c\}.
\tag{2.10}
\]

Attack \(x_0\) from \(Q_R\).  The three graph moves are available from
\(a,x_2,x_3\), because \(ax_0\) is a positive response incidence and
\(x_0x_2,x_0x_3\in E(G)\).  The \(x_2\)-successor

\[
\{a,x_0,x_3\}
\]

misses \(b,c\), but its outside lists have union \(\{a,b\}\), so it
violates restoration.  The \(x_3\)-successor

\[
\{a,x_0,x_2\}
\]

also misses \(b,c\), but under (2.10) its outside lists have union
\(\{a,c\}\), so it too violates restoration.  Closure therefore uniquely
moves \(a\) and retains

\[
R=\{x_0,x_2,x_3\}\in\mathcal F.
\tag{2.11}
\]

Attack \(x_1\) from \(R\).  Both \(x_0\) and \(x_2\) miss \(x_1\), while
\(x_1x_3\in E(G)\), so the unique graph move gives

\[
\{x_0,x_1,x_2\}\in\mathcal F.
\tag{2.12}
\]

But this state misses all of \(S\), while under (2.10)

\[
L^{\mathcal F}(x_0)\cup
L^{\mathcal F}(x_1)\cup
L^{\mathcal F}(x_2)
\subseteq\{a,c\},
\]

contradicting restoration.  Thus

\[
b\in L^{\mathcal F}(x_2).
\]

Reflection (2.8) proves
\(a\in L^{\mathcal F}(x_1)\).  Together with (0.1), (2.4), (2.7), and
(2.9), this is exactly (2.3). \(\square\)

The theorem is a genuine dynamic bridge between C-117/C-118, which use
static lists, and C-067/C-070/C-072, which were proved for exact family
lists.  The graph `FDzro` in Section 6 shows why this bridge is not
reversible: a family can realize (0.3) while the static lists are larger.

### 2.1 Location in the contracted 2-CNF

The concurrent anchor-component lemma in
`math/working/singleton_fixed_certificates/NOTE.md` is awaiting its
separate hostile audit and is **not used** in the order bound below.  If
accepted, it locates this obstruction exactly:

- the exact-two vertex \(x_1\) lies in a free component of the projection
  omitting \(b\);
- the edge \(x_0x_1\in E(H)\) puts the singleton marker \(x_0\) in that
  same free component;
- symmetrically, \(x_2,x_3\) lie in one free component of the projection
  omitting \(a\); and
- the middle edge \(x_1x_2\) is a genuine clause between two free
  variables.

Thus the canonical \(Y_3\) is a genuine two-free-unit/one-free-clause
obstruction.  It is not an artifact of a misaligned anchor-fixed
component, a fixed/free derived unit, or a fixed/fixed collision.  The
static-to-family rigidity theorem above is what makes the new
anchor-component lemma applicable to the C-117 static gluing problem.

## 3. Two static-defect cliques

Assume from now on

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{3.1}
\]

in addition to (2.2).  By Theorem 2.1, every accepted consequence of the
exact dynamic mixed \(P_4\) applies.  In particular C-070 gives

\[
cx_0,cx_3\in E(G).
\tag{3.2}
\]

But \(c\) is absent from both endpoint *static* lists.  Hence the two
states

\[
\{a,b,x_0\}=S-c+x_0,\qquad
\{a,b,x_3\}=S-c+x_3
\tag{3.3}
\]

fail to dominate \(G\).

Define

\[
D_0=N_H(a)\cap N_H(b)\cap N_H(x_0),
\]

\[
D_3=N_H(a)\cap N_H(b)\cap N_H(x_3).
\tag{3.4}
\]

### Lemma 3.1 (static-defect ridge) — PROVED

The sets \(D_0,D_3\) are nonempty.  Their union lies in the \(G\)-clique

\[
U=N_H(a)\cap N_H(b).
\tag{3.5}
\]

Every \(d\in D_0\cup D_3\) satisfies

\[
\boxed{L^{\mathcal F}(d)=\{c\},\qquad
dx_1,dx_2\in E(G).}
\tag{3.6}
\]

#### Proof

A vertex missed by the first state in (3.3) belongs to \(D_0\), and a
vertex missed by the second belongs to \(D_3\), proving nonemptiness.

If distinct \(u,v\in U\) were nonadjacent in \(G\), then
\(\{a,b,u,v\}\) would be an independent four-set, contradicting
\(\alpha(G)=3\).  Thus \(G[U]\) is a clique.

For \(d\in U\), the triple \(\{a,b,d\}\) is independent, hence maximum.
Independent-state forcing puts it in every eternal triple-family.  This is
the direct \(c\)-swap at \(S\), so

\[
c\in L^{\mathcal F}(d).
\]

The two graph nonedges to \(a,b\) exclude those colors, proving the exact
singleton list in (3.6).

The independent states \(S=\{a,b,c\}\) and \(\{a,b,d\}\) share the ridge
\(\{a,b\}\).  Ridge response covariance transports the two retained
\(c\)-roles at \(x_1,x_2\) from Theorem 2.1 to retained \(d\)-roles.
Therefore \(dx_1,dx_2\in E(G)\). \(\square\)

## 4. The double defect is dynamically impossible

A common member \(d\in D_0\cap D_3\) would have

\[
da,db,dx_0,dx_3\in E(H),
\tag{4.1}
\]

while Lemma 3.1 gives

\[
L^{\mathcal F}(d)=\{c\},\qquad
dc,dx_1,dx_2\in E(G).
\tag{4.2}
\]

The next local lemma rules this out.

### Lemma 4.1 (double-defect kernel exclusion) — PROVED, finite

There is no eternal triple-family containing an independent state
\(S=\{a,b,c\}\), an exact family-response mixed \(P_4\)
\(x_0x_1x_2x_3\), and a vertex \(d\) satisfying (4.1)--(4.2), provided
the already proved endpoint saturation

\[
cx_0,cx_3\in E(G)
\tag{4.3}
\]

holds.

#### Coverage proof

On the eight displayed vertices, every adjacency is fixed except

\[
bx_0,\qquad bx_1,\qquad ax_2,\qquad ax_3.
\tag{4.4}
\]

Thus there are exactly \(2^4=16\) induced-core completions.

For one completion let \(\mathcal A\) consist of every triple of displayed
vertices which:

1. dominates the displayed induced subgraph; and
2. satisfies restoration (2.1) using the exact five displayed family
   lists.

If \(\mathcal F\) existed, then the subfamily of its states lying wholly
inside the displayed core would be contained in \(\mathcal A\).  Moreover,
an attack at another displayed vertex from such a state has every
one-guard successor still wholly inside the core.  Therefore that
intersection would be a closed subfamily of \(\mathcal A\).

Starting from \(\mathcal A\), delete any state having a displayed
unoccupied attack with no successor remaining.  Monotonicity makes the
terminal set the greatest possible locally closed subfamily.  The
standalone checker deletes \(S\) for every one of the \(16\) completions.
The initial overapproximations have \(28\)--\(32\) states; \(S\) is
deleted in rounds \(2\)--\(4\).  Hence no actual family can contain \(S\).
\(\square\)

The exhaustive object is only an eight-vertex local kernel, not a bounded
search over graphs of any order.  Arbitrarily many external vertices are
covered by the overapproximation argument above: they cannot be a
one-guard successor when both the source state and attacked vertex already
lie in the displayed core.

### Corollary 4.2 — PROVED

\[
\boxed{D_0\cap D_3=\varnothing.}
\tag{4.5}
\]

Furthermore, neither \(D_0\) nor \(D_3\) meets the closer clique

\[
Z=N_H(x_0)\cap N_H(x_3)
\tag{4.6}
\]

from C-070.

#### Proof

A common defect is exactly the configuration excluded by Lemma 4.1.
If \(d\in D_0\cap Z\), then \(d\) also misses \(x_3\), so
\(d\in D_3\), impossible.  The other assertion is symmetric. \(\square\)

## 5. A conditional analytic order floor of fourteen

C-072 proves that an equality realization of the exact family mixed path
has the original seven vertices together with five mutually distinct
external witnesses

\[
w\in W,\qquad z\in Z,\qquad
p\in P_L,\qquad q\in P_R,\qquad y\in Y_w.
\tag{5.1}
\]

It also proves:

- \(a,b\in L^{\mathcal F}(w)\);
- \(b\in L^{\mathcal F}(p)\);
- \(a\in L^{\mathcal F}(q)\); and
- \(ya,yb\in E(G)\).

### Theorem 5.1 (exact static \(Y_3\) needs at least fourteen vertices)
— PROVED

Under (3.1) and (2.2),

\[
\boxed{|V(G)|\geq14.}
\tag{5.2}
\]

#### Proof

Choose \(d_0\in D_0\) and \(d_3\in D_3\).  Lemma 3.1 and Corollary 4.2
make \(d_0,d_3\) distinct from one another and from \(z\in Z\).

Both defects miss \(a,b\).  They therefore cannot equal \(w\), since
\(a,b\) are positive response colors at \(w\); cannot equal \(p\), since
\(b\) is positive there; cannot equal \(q\), since \(a\) is positive
there; and cannot equal \(y\), which sees both \(a,b\) in \(G\).
They are also external to the original seven by (3.2), the positive
path-list incidences, and Lemma 3.1.

Thus \(d_0,d_3\) are two new vertices beyond the twelve already separated
in C-072, giving \(12+2=14\). \(\square\)

This is a human coverage theorem plus a \(16\)-case local kernel, not a
global order-\(13\) counterexample exclusion.  It applies only when one
specified maximum independent state contains the exact static
\(Y_3\) obstruction.

## 6. Sharp gamma-two control

The graph

\[
G=\texttt{FDzro}
\]

has

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\]

Deleting the six forbidden direct swaps and taking the greatest
restoration-compatible kernel gives a \(21\)-state eternal family.  At
\(S=\{0,1,2\}\) and path \(3\,4\,5\,6\), its exact family lists are

\[
\{0\},\quad\{0,2\},\quad\{1,2\},\quad\{1\}.
\tag{6.1}
\]

All \(21(7-3)=84\) unoccupied attack obligations pass.  But its static
lists are

\[
\{0,2\},\quad\{0,1,2\},\quad
\{0,1,2\},\quad\{1,2\}.
\tag{6.2}
\]

Thus full dynamics alone can realize the abstract family-list
obstruction; domination equality and exact *static* lists are doing real
work above.  This control is not a gamma--theta counterexample.

### 6.1 A graph-specific static negative control

The ten-vertex graph

```text
G = IzM]XTR`W
H = ICp`eik]_
```

has

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,3,4,4).
\]

Its complement \(H\) is \(K_4\)-free, every vertex neighborhood in \(H\)
is bipartite, and every pair of vertices has a common \(H\)-neighbor.
These are the principal static local conditions behind the gluing
program.  Nevertheless, the one-guard triple kernel deletes all \(77\)
dominating triples in synchronous round sizes

\[
10,\ 20,\ 40,\ 7.
\]

There are seven maximum-independent triples: two are deleted in round
three and five in round four.  This is an exact check of one graph, not a
claim about the exploratory order-\(10\) scan from which it arose.  It is a
useful negative control: the static complement conditions can come very
close, but the one-guard dynamics still detect the obstruction at a small
finite horizon.

## 7. Reproduction and exact boundary

Run

```text
python3 -I -B -W error \
  math/working/dynamic_gluing_y3/verify.py
```

The checker:

1. scans all \(64\cdot9=576\) seven-vertex adjacency/list
   subpatterns and confirms that only the four completions with the exact
   full internal family lists survive;
2. replays all \(16\) double-defect deletion kernels; and
3. independently reconstructs `FDzro`, its parameters, its \(21\)-state
   constrained family, all \(84\) obligations, and both list systems; and
4. reconstructs the ten-vertex static negative control and its complete
   four-round triple-kernel deletion.

The exact unresolved branch is now:

\[
\boxed{
\text{an embedded static }Y_3\text{, if it exists, has }n\geq14
\text{ and two separated singleton-}c\text{ defect ridges.}
}
\]

No realization was found or claimed.  No theorem excludes longer
two-unit chains, lollipops, residual bicycles, full response lists, or
higher-parameter \(Y_k\) systems.
