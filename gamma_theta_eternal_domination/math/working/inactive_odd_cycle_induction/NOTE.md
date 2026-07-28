# A length-independent exclusion of inactive odd cycles

## Status and exact scope

This note proves a local one-guard attack theorem and applies it to the
accepted C-108 inactive set.

> **Main result (PROVED, pending independent hostile audit).**  
> Let \(G\) be a graph with a one-guard eternal family
> \(\mathcal F\) of triples.  Fix \(x\).  Along a witnessed path
> \(r_0r_1\ldots r_n\) in \(\overline G-x\), suppose every named
> independent triple
> \[
> T_i=\{r_i,r_{i+1},p_i\}\qquad(0\leq i<n)
> \]
> belongs to \(\mathcal F\), and neither rim endpoint can answer the
> attack at \(x\) from \(T_i\).  If \(n\) is odd, then
> \[
> \{r_0,r_n,x\}\in\mathcal F.
> \]
> The witnesses may coincide arbitrarily.

Together with the accepted private-star distance-two exclusion, this
rules out a witnessed inactive odd cycle of every length.  Consequently,
under
\[
\alpha(G)=\gamma^\infty(G)=3,\qquad \gamma(G-x)\geq3,
\]
the C-108 inactive graph
\[
\overline{G-x}[R_x]
\]
is bipartite.

This is **not** a proof of the complete \(k=3\) case or of the universal
\(\gamma\)--\(\theta\) conjecture.  Bipartiteness of the induced inactive
graph does not imply that some global three-coloring of
\(\overline{G-x}\) uses only two colors on \(R_x\).  Outside vertices and
active ridge components can still force all three colors on \(R_x\).
Thus the separate global precoloring/gluing obstruction remains open.

The proof below is human and length-independent.  The checker
`verify_induction.py` independently audits its five-layer leaf recurrence,
the exact local kernels through a selectable path length, and the
even-parity controls.  Those finite checks support the proof but are not
used in place of it.

## 1. Local setup and the response principle

All attacks below are at unoccupied vertices, and exactly one guard may
move along one edge.

Let
\[
P=r_0r_1\ldots r_n
\tag{1.1}
\]
be a path of distinct vertices in \(H=\overline G\), let
\(x\notin V(P)\), and let
\[
p_i\notin V(P)\cup\{x\}
\tag{1.2}
\]
for \(0\leq i<n\).  At first assume that the \(p_i\) are pairwise
distinct.  Suppose
\[
T_i=\{r_i,r_{i+1},p_i\}\in\mathcal F
\tag{1.3}
\]
and \(T_i\) is independent in \(G\).  Finally suppose
\[
\{r_i,p_i,x\}\notin\mathcal F,\qquad
\{r_{i+1},p_i,x\}\notin\mathcal F
\tag{1.4}
\]
for every \(i\).  These are exactly the two forbidden endpoint responses
at \(x\) from \(T_i\).

Only the following immediate consequence of one-guard closure is used.

### Blocked-or-absent response principle

Let \(S\) be a triple and let \(v\notin S\).  If, for every \(u\in S\),
either
\[
uv\notin E(G)
\]
or
\[
S-u+v\notin\mathcal F,
\]
then \(S\notin\mathcal F\).

Indeed, if \(S\) were retained, the attack at \(v\) would have no legal
response.  Notice that an unspecified adjacency never causes a problem:
if the move edge is absent, that response is blocked; if it is present,
the displayed successor is absent.  This is why all arguments below are
valid in every completion of the local template.

Put
\[
A_n=\{r_i:i\ \text{is even}\},\quad
B_n=\{r_i:i\ \text{is odd}\},\quad
N_n=\{x,p_0,\ldots,p_{n-1}\}.
\tag{1.5}
\]

## 2. The parity-support lemma

### Lemma 2.1 (parity support)

Under (1.1)--(1.4), every retained triple contained in
\[
V(P)\cup N_n
\]
meets both \(A_n\) and \(B_n\).

### Proof

We induct on \(n\).

For \(n=1\), the local vertex set is
\(\{r_0,r_1,p_0,x\}\).  Its only triple missing \(B_1\) is
\(\{r_0,p_0,x\}\), and its only triple missing \(A_1\) is
\(\{r_1,p_0,x\}\).  Both are absent by (1.4).

Suppose the assertion holds for the prefix of length \(n-1\), where
\(n\geq2\).  Relabel the two prefix parity classes, if necessary, so that
\[
z=r_{n-1}\in A,\qquad
w=r_{n-2}\in B.
\]
Write
\[
h=p_{n-2},\qquad y=r_n,\qquad p=p_{n-1},
\]
and let \(N\) be the old neutral set.  Thus \(y\in B\), \(p\) is a new
neutral vertex, and
\[
\{w,z,h\},\qquad \{z,y,p\}
\tag{2.1}
\]
are independent triples in \(G\).  In particular, \(z\) is nonadjacent
in \(G\) to every vertex of
\[
\{w,h,y,p\}.
\tag{2.2}
\]

By the induction hypothesis, every old triple contained in
\[
C=B\cup N
\tag{2.3}
\]
is absent, as is every old triple contained in
\[
D=A\cup N.
\tag{2.4}
\]
We now add the leaf triangle in five elementary layers.

**Layer 1: the private star of \(z\).**  
Every three-set contained in \(\{w,h,y,p\}\) is absent: attack \(z\);
all three guards are blocked by (2.2).

**Layer 2: four bridge forms.**  
For every \(t\in C\), each well-defined three-set among
\[
\{t,h,p\},\quad \{t,h,y\},\quad
\{t,w,p\},\quad \{t,w,y\}
\tag{2.5}
\]
is absent.

For the first two sets, attack \(w\).  The guard at \(h\) is blocked.
Moving the guard at \(t\) gives respectively
\(\{w,h,p\}\) or \(\{w,h,y\}\), absent by Layer 1; moving the remaining
guard gives \(\{t,h,w\}\), an old triple contained in \(C\).

For the last two sets, attack \(h\).  The guard at \(w\) is blocked.
The two possible successors are respectively a Layer-1 state and the old
state \(\{t,w,h\}\).  Coincident displayed entries either do not form a
three-set or reduce to Layer 1.

**Layer 3: all new triples missing \(A\).**  
Let
\[
S\subseteq C\cup\{p,y\},\qquad |S|=3,
\tag{2.6}
\]
and suppose \(S\) contains \(p\) or \(y\).  If \(w\in S\), then \(S\)
is a Layer-1 or Layer-2 state.  Otherwise attack \(w\).  Moving a new
guard produces either an old triple in \(C\) or a Layer-2 state; moving
an old guard produces a Layer-1 or Layer-2 state.  Hence every response
is blocked or absent, so \(S\) is absent.

This proves the required assertion for triples missing the new \(A\)
class.

**Layer 4: a seed on the other side.**  
First,
\[
\{z,h,p\}\notin\mathcal F.
\tag{2.7}
\]
Attack \(x\).  The three possible successors are
\[
\{x,h,p\},\qquad \{z,x,p\},\qquad \{z,h,x\}.
\tag{2.8}
\]
The first is absent by Layer 3, the second by (1.4) on the new edge, and
the third by (2.4).

It follows that
\[
\{z,p,d\}\notin\mathcal F
\qquad(d\in D,\ d\ne z).
\tag{2.9}
\]
If \(d=h\), this is (2.7).  Otherwise attack \(h\).  The guard at \(z\)
is blocked.  The two possible successors are \(\{z,h,d\}\), an old
triple in \(D\), and the seed \(\{z,h,p\}\).

**Layer 5: all new triples missing \(B\).**  
Every new triple missing \(B\) has the form
\[
S=\{p,s,t\},\qquad s,t\in D.
\tag{2.10}
\]
If \(z\in S\), (2.9) applies.  Otherwise attack \(z\).  The guard at
\(p\) is blocked by (2.1), and either remaining move gives a state of
the form (2.9).  Thus \(S\) is absent.

Layers 3 and 5 establish the induction step. \(\square\)

The five layers use no path-length bound and no domination-number,
independence-number, coloring, or planarity assumption.

## 3. Odd endpoint forcing

### Lemma 3.1 (neutral replacement)

Assume the conclusion of Lemma 2.1.  Fix \(a\in A_n\) and \(b\in B_n\).
If
\[
\{a,b,q_0\}\notin\mathcal F
\tag{3.1}
\]
for one \(q_0\in N_n\), then
\[
\{a,b,q\}\notin\mathcal F
\tag{3.2}
\]
for every \(q\in N_n\).

### Proof

For \(q\ne q_0\), attack \(q_0\) from \(\{a,b,q\}\).  Moving \(a\) or
\(b\) produces a state missing one rim parity, hence absent by
Lemma 2.1.  Moving \(q\) produces (3.1). \(\square\)

### Theorem 3.2 (odd witnessed-path endpoint theorem)

Under (1.1)--(1.4), if \(n\) is odd, then
\[
\boxed{\{r_0,r_n,x\}\in\mathcal F.}
\tag{3.3}
\]

### Proof for distinct witnesses

Suppose instead that
\[
\{r_0,r_n,x\}\notin\mathcal F.
\tag{3.4}
\]
Write
\[
a_0=r_0\in A_n,\qquad b_\ast=r_n\in B_n.
\]
By Lemma 3.1,
\[
\{a_0,b_\ast,q\}\notin\mathcal F
\qquad(q\in N_n).
\tag{3.5}
\]

If \(n=1\), (3.5) with \(q=p_0\) contradicts
\(T_0\in\mathcal F\).  Hence assume \(n\geq3\).

Let \(q_L=p_0\).  It is nonadjacent in \(G\) to \(a_0\).  For any
\(a\in A_n-\{a_0\}\), first attack \(q_L\) from
\(\{a_0,a,b_\ast\}\).  The guard at \(a_0\) is blocked; the other two
successors are \(\{a_0,b_\ast,q_L\}\), absent by (3.5), and a state
missing \(B_n\).  Thus \(\{a_0,a,b_\ast\}\) is absent.

Now attack \(a_0\) from \(\{a,b_\ast,q_L\}\).  The guard at \(q_L\) is
blocked, and the other successors are again
\(\{a_0,b_\ast,q_L\}\) and a state missing \(B_n\).  Lemma 3.1 then
gives
\[
\{a,b_\ast,q\}\notin\mathcal F
\quad
(a\in A_n,\ q\in N_n).
\tag{3.6}
\]

Put
\[
a_\ast=r_{n-1}\in A_n,\qquad q_R=p_{n-1}.
\]
Both \(a_\ast\) and \(b_\ast\) are nonadjacent in \(G\) to \(q_R\).
For any \(b\in B_n-\{b_\ast\}\), attack \(q_R\) from
\(\{a_\ast,b_\ast,b\}\).  The two endpoint guards are blocked, and the
only possible successor is \(\{a_\ast,b_\ast,q_R\}\), absent by (3.6).
Next attack \(b_\ast\) from \(\{a_\ast,b,q_R\}\).  The guards at
\(a_\ast\) and \(q_R\) are blocked, and the remaining successor is the
same absent state.  By neutral replacement,
\[
\{a_\ast,b,q\}\notin\mathcal F
\quad
(b\in B_n,\ q\in N_n).
\tag{3.7}
\]

Finally fix \(b\in B_n\) and repeat the first propagation with
\(a_\ast,q_R\) in place of \(a_0,q_L\).  For
\(a\in A_n-\{a_\ast\}\), attack \(q_R\) from
\(\{a_\ast,a,b\}\), and then attack \(a_\ast\) from
\(\{a,b,q_R\}\).  Every possible response is either blocked, a state
from (3.7), or a state missing \(B_n\).  Lemma 3.1 gives
\[
\{a,b,q\}\notin\mathcal F
\quad
(a\in A_n,\ b\in B_n,\ q\in N_n).
\tag{3.8}
\]

But every named state \(T_i\) has one rim vertex in each parity class and
one neutral witness.  Equation (3.8) therefore says
\(T_i\notin\mathcal F\) for all \(i\), contradicting (1.3). \(\square\)

## 4. Repeated witnesses: adjacent-true-twin lifting

The preceding proof assumed distinct witness occurrences.  That loses no
generality.

### Lemma 4.1 (witness splitting)

If (1.1)--(1.4) exists with repeated witnesses, then it exists with
pairwise distinct witnesses.

### Proof

For each original vertex \(v\), let \(m_v\) be the number of occurrences
of \(v\) among \(p_0,\ldots,p_{n-1}\), taking \(m_v=1\) when \(v\) is
not repeated.  Replace \(v\) by a clique \(C_v\) of \(m_v\) adjacent
true twins.  Between \(C_u\) and \(C_v\), put all edges when
\(uv\in E(G)\) and no edges otherwise.  Vertices that are not repeated
have singleton fibers.  Let
\[
\pi:V(G')\longrightarrow V(G)
\]
be the fiber projection.

Lift the family by
\[
\mathcal F'
=
\left\{
D'\subseteq V(G'):
|D'|=3,\ \pi\text{ is injective on }D',\
\pi(D')\in\mathcal F
\right\}.
\tag{4.1}
\]
Equivalently, choose one clone independently for each occupied original
vertex.

Every lifted state dominates \(G'\).  If a vertex lies in an unoccupied
fiber, an original guard that dominated its projection dominates every
clone in that fiber.  If it lies in an occupied fiber, it is either
occupied or adjacent to the occupied sibling.

Closure is also exact.  If an attacked clone lies in an unoccupied
fiber, project the attack to \(G\), use the original one-guard response,
and move the corresponding occupied clone to the attacked clone.  If the
attacked clone is an unoccupied sibling in an occupied fiber, move the
occupied sibling directly to it.  In both cases exactly one guard moves
along one edge and the resulting state lies in \(\mathcal F'\).

Assign a different clone to every occurrence of a repeated \(p_i\).
The named triples lift to retained independent triples.  If either lifted
endpoint successor at \(x\) belonged to \(\mathcal F'\), its projection
would be the corresponding forbidden original successor, contrary to
(1.4).  Thus the lifted configuration has distinct witnesses. \(\square\)

Projecting Theorem 3.2 back through \(\pi\) proves its stated
repeated-witness form.

## 5. Excluding every inactive odd cycle

We now make the cycle-to-path reduction with exact indices.

### Corollary 5.1 (local inactive odd-cycle exclusion)

Let
\[
C=r_0r_1\ldots r_{\ell-1}r_0
\tag{5.1}
\]
be an odd cycle in \(H-x\), where \(\ell\geq5\).  Suppose every rim edge
has a named retained independent witness triple satisfying the two
absent endpoint responses (1.4), with witnesses outside
\(V(C)\cup\{x\}\).  Then this configuration does not exist.

### Proof

The accepted private-star distance-two corollary, applied at
\(v=r_{\ell-1}\) with its two \(H\)-neighbors
\[
a=r_0,\qquad b=r_{\ell-2},
\]
gives
\[
\{r_0,r_{\ell-2},x\}\notin\mathcal F.
\tag{5.2}
\]

Now take the witnessed path
\[
r_0r_1\ldots r_{\ell-2}.
\tag{5.3}
\]
It has exactly \(\ell-2\) edges, which is odd.  Its edge witnesses are
\(p_0,\ldots,p_{\ell-3}\), and all its endpoint-response hypotheses are
a subset of the cycle hypotheses.  Theorem 3.2 says that the state in
(5.2) belongs to \(\mathcal F\), a contradiction. \(\square\)

### Corollary 5.2 (bipartite C-108 inactive graph)

Assume
\[
\alpha(G)=\gamma^\infty(G)=3,\qquad \gamma(G-x)\geq3,
\tag{5.4}
\]
let \(\mathcal F\) be an optimal eternal triple-family, and let \(R_x\)
be the C-108 inactive set.  Then
\[
\boxed{\overline{G-x}[R_x]\text{ is bipartite}.}
\tag{5.5}
\]

### Proof

The accepted C-108 consequences make
\(\overline{G-x}[R_x]\) triangle-free.  If it were not bipartite, choose
a shortest odd cycle
\[
r_0r_1\ldots r_{\ell-1}r_0.
\]
It has \(\ell\geq5\) and is induced.

For each rim edge \(r_ir_{i+1}\), the pair
\(\{r_i,r_{i+1}\}\) does not dominate \(G-x\), by
\(\gamma(G-x)\geq3\).  Choose \(p_i\in V(G-x)\) nonadjacent in \(G\)
to both endpoints.  Because the cycle is induced, \(p_i\) is not a rim
vertex: a third rim vertex adjacent in \(H\) to both ends of a rim edge
would create a triangle or a chord.  Hence
\[
T_i=\{r_i,r_{i+1},p_i\}
\]
is an independent triple.  It is maximum by \(\alpha(G)=3\), so
maximum-independent-state forcing puts \(T_i\) in every optimal eternal
family.  Both endpoints lie in \(R_x\), and C-108 therefore makes both
endpoint successors at \(x\) absent.  Corollary 5.1 gives the
contradiction. \(\square\)

## 6. Independent checks and parity controls

Run

```text
python3 -I -B -W error \
  math/working/inactive_odd_cycle_induction/verify_induction.py \
  --max-path-length 25
```

The checker performs three separate audits.

1. It reconstructs the five proof layers on a 15-vertex abstract leaf
   template with three generic representatives in each old class.  It
   verifies every blocked-or-absent response and covers all 265 required
   old-or-new parity-deficient states.
2. Direct greatest-kernel deletion through path length 25 verifies the
   stronger closed form suggested by Lemma 2.1: with only (1.4) forbidden,
   the dead local states are exactly the triples that miss a rim parity.
   Adding a forbidden endpoint state kills every local triple precisely
   at odd path length.
3. For both parities through length 12 it checks the product-family
   control in the maximum-edge completion.  The family consists of all
   triples with one even rim, one odd rim, and one neutral vertex.  Every
   named state is retained, both endpoint-response states are absent, and
   \(\{r_0,r_n,x\}\) belongs to the family exactly when \(n\) is odd.

Thus the theorem has the sharp parity boundary.  The even controls also
guard against accidentally proving a false all-length endpoint assertion.

## 7. What remains open

The new theorem closes the **local inactive odd-cycle** obstruction.  It
does not close the **global deletion-coloring** obstruction.

In particular, even though \(H[R_x]\) is bipartite, a proper
three-coloring of all of \(H-x\) can still be forced by vertices outside
\(R_x\) to use three colors on \(R_x\).  The accepted C-112 equality
control already exhibits this phenomenon.  A proof of the full-list
branch must therefore synchronize the local two-coloring with the active
ridge components; no such synchronization is claimed here.
