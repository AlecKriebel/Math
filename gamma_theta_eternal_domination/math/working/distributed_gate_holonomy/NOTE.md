# Distributed gate holonomy: a two-projection parity theorem

## Status and exact boundary

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination
model.  Attacks are made only at unoccupied vertices, exactly one
adjacent guard moves, and every retained state dominates.

This note proves a new arbitrary-length attack theorem.

1. **PROVED:** two vertex-disjoint omitted-color paths whose endpoint
   triples have the same two dead boundary states must have equal parity.
   The proof uses only one retained direct response, the one-guard
   closure axiom, and three elementary dead-state lemmas.
2. **PROVED COROLLARY:** two tight third-color gates cannot be joined at
   their corresponding type-\(c\) and type-\(a\) physical ports by
   vertex-disjoint projection paths of opposite parity.  Thus an
   odd-holonomy **bigon** distributed across two distinct free connector
   components is impossible, even when all four physical ports are
   separated.
3. The theorem needs no hypothesis on \(\gamma(G)\), no clique-coloring
   assumption, and no inference from a missing family response to a graph
   nonedge.  Arbitrary additional complement edges are allowed.

This closes the first separated-port case left open by the accepted
third-color gate odd-return theorem.  It does **not** eliminate a general
unit-free 2-SAT bicycle.  A longer gate cycle can visit three or more
tight gates with only one connector between successive gates; the
complementary route between two ports then changes omitted colors and is
not one path inside a single frozen projection.  No universal \(k=3\)
theorem or resolution of the gamma--theta conjecture is claimed.

No literature-priority claim is made.

## 1. Setup and three dead-state facts

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(t\notin S\), write

\[
 L(t)=\{u\in S:S-u+t\in\mathcal F\}.
\tag{1.1}
\]

If \(u\in L(t)\), the retained successor \(S-u+t\) must dominate the
omitted anchor \(u\).  The other two anchors miss \(u\), so
\(ut\in E(G)\).  We use only this forward implication.

For an anchor \(u\), put

\[
 W_u=\{t\notin S:u\notin L(t)\}.
\tag{1.2}
\]

The following facts are restated for a self-contained proof.

### Lemma 1.1 (one anchor and two avoiding vertices)

If \(r,s\in W_u\) are distinct and
\(h\in S-\{u\}\), then

\[
 \{h,r,s\}\notin\mathcal F.
\tag{1.3}
\]

#### Proof

Let \(d\) be the other member of \(S-\{u,h\}\).  Attack \(d\).
The guard at \(h\) cannot move because \(S\) is independent.  Moving
\(r\) would give \(S-u+s\), and moving \(s\) would give \(S-u+r\).
Both states are absent by \(r,s\in W_u\).  A missing move edge only
removes an option.  Thus no retained response exists. \(\square\)

### Lemma 1.2 (three avoiding vertices)

If \(r,s,t\in W_u\) are distinct, then

\[
 \{r,s,t\}\notin\mathcal F.
\tag{1.4}
\]

#### Proof

Attack either anchor \(h\in S-\{u\}\).  Every possible successor
contains \(h\) and two of \(r,s,t\), so Lemma 1.1 excludes it.
\(\square\)

### Lemma 1.3 (same-side path endpoints)

Let

\[
 v_0v_1\ldots v_{2r}\qquad(r\geq1)
\tag{1.5}
\]

be a vertex-distinct path in \(H\), with every \(v_i\in W_u\).
If \(p\) is outside the path, then

\[
 \{p,v_0,v_{2r}\}\notin\mathcal F.
\tag{1.6}
\]

#### Proof

For \(r=1\), attack \(v_1\).  Neither endpoint guard can move along a
graph edge, because both displayed path edges lie in \(H\).  Moving
\(p\), if legal, gives a state of three \(u\)-avoiding vertices, excluded
by Lemma 1.2.

For \(r\geq2\), assume the result for shorter even paths and attack
\(v_{2r-2}\) from a hypothetical state
\(\{p,v_0,v_{2r}\}\).

- Moving \(p\) gives three \(u\)-avoiding vertices.
- Moving \(v_0\) gives
  \(\{p,v_{2r-2},v_{2r}\}\), excluded by the length-two case.
- Moving \(v_{2r}\) gives
  \(\{p,v_0,v_{2r-2}\}\), excluded by induction.

All possible responses are absent. \(\square\)

The lemmas concern family membership.  They never interpret
\(u\notin L(v)\) as the graph nonedge \(uv\in E(H)\).

## 2. The two-projection parity theorem

### Theorem 2.1 (boundary parity synchronization) — PROVED

Let

\[
 P:x_0x_1\ldots x_m,\qquad
 Q:y_0y_1\ldots y_n
\tag{2.1}
\]

be vertex-distinct paths in \(H\), of lengths \(m,n\geq0\), whose
vertex sets are disjoint and lie outside \(S\).  Suppose

\[
 x_i\in W_c\quad(0\leq i\leq m),
\qquad
 y_j\in W_a\quad(0\leq j\leq n),
\tag{2.2}
\]

\[
 a\in L(x_0),\qquad c\in L(y_0),
\tag{2.3}
\]

and the two boundary states are absent:

\[
 \{b,x_0,y_0\}\notin\mathcal F,
\qquad
 \{b,x_m,y_n\}\notin\mathcal F.
\tag{2.4}
\]

Then

\[
 \boxed{m\equiv n\pmod2.}
\tag{2.5}
\]

Additional complement edges among the displayed vertices are allowed.

#### Proof

The response \(a\in L(x_0)\) gives the retained direct state

\[
 D_x=S-a+x_0=\{b,c,x_0\}.
\tag{2.6}
\]

Attack \(y_0\) from \(D_x\).

- Moving \(x_0\), if legal, gives
  \(\{b,c,y_0\}=S-a+y_0\), absent because \(y_0\in W_a\).
- Moving \(c\), if legal, gives the first absent boundary state in
  (2.4).

Closure therefore forces

\[
 C_{0,0}:=\{c,x_0,y_0\}\in\mathcal F.
\tag{2.7}
\]

Symmetrically, \(c\in L(y_0)\) gives

\[
 D_y=S-c+y_0=\{a,b,y_0\}\in\mathcal F.
\tag{2.8}
\]

Attack \(x_0\).  Moving \(y_0\) gives the absent direct swap
\(S-c+x_0\), and moving \(a\) gives the first absent boundary state.
Therefore closure forces

\[
 A_{0,0}:=\{a,x_0,y_0\}\in\mathcal F.
\tag{2.9}
\]

Suppose \(n\geq1\).  Attack \(y_1\) from \(C_{0,0}\).  The guard at
\(y_0\) cannot move across the complement edge \(y_0y_1\).  Moving
\(x_0\), if legal, gives \(\{c,y_0,y_1\}\), excluded by Lemma 1.1
with omitted anchor \(a\).  Hence closure forces

\[
 U_0:=\{x_0,y_0,y_1\}\in\mathcal F.
\tag{2.10}
\]

Attack \(b\) from \(U_0\).

- Moving \(x_0\) gives \(\{b,y_0,y_1\}\), excluded by Lemma 1.1.
- Moving \(y_1\) gives the first absent boundary state
  \(\{b,x_0,y_0\}\).

Thus closure forces

\[
 B_{0,1}:=\{b,x_0,y_1\}\in\mathcal F.
\tag{2.11}
\]

The same argument in the other projection starts from \(A_{0,0}\).
If \(m\geq1\), attack \(x_1\).  The guard at \(x_0\) cannot move,
and a move by \(y_0\) gives
\(\{a,x_0,x_1\}\), excluded by Lemma 1.1 with omitted anchor \(c\).
Thus \(\{x_0,x_1,y_0\}\) is retained.  Attack \(b\) there.  Moving
\(y_0\) gives the forbidden state \(\{b,x_0,x_1\}\), while moving
\(x_1\) gives the first absent boundary state.  Closure forces

\[
 B_{1,0}:=\{b,x_1,y_0\}\in\mathcal F.
\tag{2.12}
\]

We now use one common propagation step.  If a retained state contains
one vertex \(v_i\) of an omitted-color path and two vertices outside that
path, attack \(v_{i+2}\).  A move by either outside guard leaves
\(v_i,v_{i+2}\) together and is excluded by Lemma 1.3 on the length-two
subpath.  Hence closure forces the guard at \(v_i\) to move and replaces
it by \(v_{i+2}\).

Consequently,

\[
\begin{aligned}
 n\text{ odd}&\quad\Longrightarrow\quad
   B_{0,n}=\{b,x_0,y_n\}\in\mathcal F,\\
 m\text{ odd}&\quad\Longrightarrow\quad
   B_{m,0}=\{b,x_m,y_0\}\in\mathcal F.
\end{aligned}
\tag{2.13}
\]

If \(m\) is even and \(n\) is odd, apply the same two-step propagation
along \(P\) to \(B_{0,n}\).  It gives

\[
 B_{m,n}=\{b,x_m,y_n\}\in\mathcal F,
\tag{2.14}
\]

including when \(m=0\).  This contradicts the second boundary condition
in (2.4).

If \(m\) is odd and \(n\) is even, propagate \(B_{m,0}\) along \(Q\).
It again gives (2.14), with the same contradiction.  Both parity
mismatches are impossible, proving (2.5). \(\square\)

Every attack in this proof is at an unoccupied vertex.  Whenever a
displayed move edge is absent, the corresponding response option is
merely removed; the forcing argument remains valid.

## 3. Tight-gate consequence

### Corollary 3.1 (separated two-gate odd bigon exclusion) — PROVED

Suppose two tight third-color gates have corresponding physical ports

\[
\begin{array}{c|ccc}
 &\text{type }c&\text{type }a&\text{type }b\text{ cap}\\ \hline
0&x_0&y_0&z_0\\
1&x_1&y_1&z_1
\end{array}
\tag{3.1}
\]

with

\[
 L(x_i)=\{a,b\},\qquad
 L(y_i)=\{b,c\},\qquad
 L(z_i)=\{a,c\},
\tag{3.2}
\]

and literal complement incidences

\[
 bz_i,\ x_iz_i,\ y_iz_i\in E(H)
\qquad(i=0,1).
\tag{3.3}
\]

Let \(P\) be a path from \(x_0\) to \(x_1\) inside \(W_c\), and let
\(Q\) be a path from \(y_0\) to \(y_1\) inside \(W_a\).  If the two
paths are vertex-distinct and vertex-disjoint, then their lengths have
the same parity.

#### Proof

The exact lists give (2.2)--(2.3).  For each \(i\), the state
\(\{b,x_i,y_i\}\) does not dominate \(z_i\), by the three complement
edges in (3.3).  Thus both boundary states are absent from
\(\mathcal F\).  Theorem 2.1 applies. \(\square\)

In the chirality language, a tight gate identifies the chiralities of
its three ports, while each projection path flips chirality by its length
parity.  Opposite path parities would therefore be an odd signed bigon.
Corollary 3.1 supplies the missing graph-game contradiction; it is not
merely a restatement of the unsatisfiable Boolean parity.

The length-zero case handles two **parallel** gates of the same cap type
sharing one failed-pair port.  This is complementary to, rather than a
restatement of, the accepted odd-return theorem, whose second gate can
have a different distinguished cap type.  The positive-length case is
new and allows all four connector endpoints to be distinct.

## 4. What remains open

In the no-full response 2-CNF, a unit-free bicycle uses free bipartite
components and hence contains no singleton-list vertex.  If a path in
\(W_c\) and a path in \(W_a\) intersect at a vertex \(v\), then \(v\)
omits both \(a\) and \(c\); its nonempty proper list is therefore
\(L(v)=\{b\}\), which supplies a unit.  Thus connector components of
different types are vertex-disjoint in the unit-free branch.

Corollary 3.1 consequently removes every two-gate odd bigon in that
branch, including arbitrary subdivisions in both connector components.
Without the unit-free/free-component hypothesis, the corollary asserts
only the displayed vertex-disjoint case.  It does not contract a chain of
gates into a projection path.  In a gate cycle

\[
 g_0-P_0-g_1-P_1-\cdots-g_{r-1}-P_{r-1}-g_0
\qquad(r\geq3),
\tag{4.1}
\]

the complementary route between two successive gates passes through
other tight gates and changes omitted color.  Its internal vertices do
not all lie in one \(W_u\), so Theorem 2.1 cannot be applied to that route.

The exact remaining target is therefore:

> exclude an inclusion-minimal odd signed cycle with at least three tight
> gates after every two-gate odd bigon has been removed, or prove that
> such a cycle yields a dominating pair.

This is strictly narrower than the starting arbitrary-bicycle problem,
but it is still open.

## 5. Exact discovery probes

`probe.py` directly encodes an arbitrary eternal family of triples and
unknown graph edges.  It was used only to discover and falsify candidate
wordings.  With the two boundary states imposed directly, the tested
parity table through path length five was:

\[
\begin{array}{c|c}
(m\bmod2,n\bmod2)&\text{exact SAT status}\\ \hline
(0,0)&\mathrm{SAT}\\
(1,1)&\mathrm{SAT}\\
(0,1)&\mathrm{UNSAT}\\
(1,0)&\mathrm{UNSAT}.
\end{array}
\tag{5.1}
\]

The proof of Theorem 2.1 supersedes the bounded negative probes.  The SAT
rows are abstract family controls, not equality graphs and not
counterexamples to the conjecture.  `fixed_kernel.py` and `ablate.py`
are proof-discovery aids that exposed the boundary-state mechanism.

`verify.py` independently rebuilt the greatest eternal triple-families
of the four accepted equality controls

```text
LFzJbZYhdrDZdM
MFzJbZYhlrDZdMhd_
NFzJbZZhlrDZdMhd|h_
MEXrtIdmdjLQqztC?
```

and exhaustively checked every vertex-disjoint path pair of length at
most fourteen satisfying the hypotheses of Theorem 2.1.  The respective
numbers of path pairs were

\[
 86,\quad150,\quad246,\quad396.
\]

All \(878\) pairs had equal parity.  These counts include the
length-zero cases in Theorem 2.1.  Each control also contains explicit
same-parity examples, so the theorem cannot be strengthened to forbid the
boundary geometry itself.  This is a bounded stress audit of the proof,
not an ingredient in it.

The theorem and corollary, not the finite probe output, are the
mathematical result.
