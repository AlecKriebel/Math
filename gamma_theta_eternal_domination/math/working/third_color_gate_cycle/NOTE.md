# Third-color gate cycles: chirality, odd holonomy, and an odd-return exclusion

## Status and exact boundary

Date: 2026-07-28 (PDT)

All graph statements use the standard one-guard-moves eternal-domination
model: attacks are made only at unoccupied vertices, exactly one adjacent
guard moves to the attacked vertex, and every retained state dominates.

This note continues the accepted original-edge incidence theorem.  Its
outcomes are:

1. **PROVED:** exact two-list ports have a canonical binary chirality.
   Every tight third-color virtual-rainbow gate preserves chirality, while
   a path inside one frozen projection flips chirality by its length
   parity.
2. **PROVED:** the connector parities along an implication walk have a
   simple type-word description.  A closed literal-preserving walk has
   even holonomy.  Closing a path from a literal to its complement changes
   exactly one connector parity and gives odd holonomy.
3. **PROVED:** an odd two-cap fork is impossible in an arbitrary eternal
   triple-family.  As a consequence, a tight gate cannot return through
   an odd path in one omitted-color projection to a physical cap of a
   second tight gate sharing the first gate's opposite port.  The proof
   covers every odd subdivision and does not require
   \(\gamma(G)=3\).
4. **EXACT EQUALITY CONTROL:** the connected graph
   `MEXrtIdmdjLQqztC?` (canonical graph6
   `MGEFK~cfJLBi]f]Z?`) has
   \[
     \gamma=i=\alpha=\gamma^\infty=\theta=3.
   \]
   Its greatest eternal triple-family has 172 states and realizes two
   tight gates sharing one physical port with trivial/even holonomy.
   Thus the two-gate incidence alone is not a contradiction; odd return
   parity is essential.

The odd-return theorem is a genuine universal attack lemma, but it does
**not** eliminate an arbitrary unit-free 2-SAT bicycle.  A longer bicycle
can distribute its odd holonomy among several connector components,
can use separated physical ports, and need not contain two gates sharing
the vertex required in Corollary 4.4.  No conjecture resolution or
universal \(k=3\) theorem is claimed.

No literature-priority claim is made.

## 1. Setup

Let \(\mathcal F\) be an eternal family of triples, let

\[
  S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(t\notin S\), write

\[
  L(t)=\{u\in S:S-u+t\in\mathcal F\}.
\tag{1.1}
\]

For an independent reference state, membership in (1.1) forces the
corresponding graph edge.  Indeed, the retained state \(S-u+t\) must
dominate the omitted anchor \(u\), while neither member of
\(S-\{u\}\) sees \(u\).  Hence

\[
  S-u+t\in\mathcal F
  \quad\Longleftrightarrow\quad
  u\in L(t),
\tag{1.2}
\]

and the forward implication also gives \(ut\in E(G)\).

In the no-full branch every outside list is nonempty and proper.  A
two-list port has a unique **type**

\[
  \tau(t)=S-L(t),
\tag{1.3}
\]

which we identify with the omitted anchor.

## 2. Chirality of a tight third-color gate

Identify the three anchor colors with \(\mathbb Z_3\).  If a type-\(u\)
two-list port is assigned one of its two allowed colors, define its
chirality by

\[
 \chi(t)=
 \begin{cases}
  0,&\kappa(t)=u-1,\\
  1,&\kappa(t)=u+1.
 \end{cases}
\tag{2.1}
\]

The definition depends only on the fixed cyclic order of \(S\).  Reversing
that order complements every chirality and changes no parity statement.

### Proposition 2.1 (one cross implication preserves chirality) — PROVED

Let \(x,y\) be exact two-list ports of distinct types, and let \(w\) be
their unique common allowed color.  The complement edge supporting their
cross clause gives the implications

\[
  [\kappa(x)=w]\longrightarrow[\kappa(y)\ne w],
  \qquad
  [\kappa(y)=w]\longrightarrow[\kappa(x)\ne w].
\tag{2.2}
\]

Each implication in (2.2) sends one chirality value at its tail to the
same chirality value at its head.

#### Proof

If the endpoint types are \(u,u+1\), their common color is \(u-1\).
At the type-\(u\) endpoint this is chirality zero, while at the
type-\(u+1\) endpoint it is chirality one.  Therefore forcing the second
endpoint away from the common color gives chirality zero.  This proves
the first implication preserves chirality; the second preserves
chirality one.  The case \(u,u-1\) is the same calculation with the two
endpoints exchanged. \(\square\)

### Proposition 2.2 (a tight gate is chirality equality) — PROVED

Consider the tight third-color gate from the accepted original-edge
incidence theorem.  After cyclic relabeling its three physical ports have

\[
  L(x)=\{a,b\},\qquad
  L(y)=\{b,c\},\qquad
  L(z)=\{a,c\}.
\tag{2.3}
\]

The original clause forbids \(x=y=b\), while the two literal cap edges
forbid \(x=z=a\) and \(y=z=c\).  The only compatible assignments are

\[
  (x,y,z)=(b,c,a)
  \quad\text{and}\quad
  (a,b,c).
\tag{2.4}
\]

Equivalently,

\[
  \boxed{\chi(x)=\chi(y)=\chi(z).}
\tag{2.5}
\]

#### Proof

The three displayed constraints make the colors of \(x,y,z\) pairwise
distinct.  Intersecting the six permutations of \(a,b,c\) with the lists
in (2.3) leaves exactly (2.4).  In the first assignment every port chooses
the predecessor of its omitted color; in the second every port chooses
the successor.  This is (2.5). \(\square\)

### Proposition 2.3 (connector sign) — PROVED

Let \(P\) be a path of length \(\ell\) in one frozen projection
\(B_u\), with exact type-\(u\) ports \(x,y\) at its ends.  Then every
oriented bipartition coloring satisfies

\[
  \chi(y)=\chi(x)\oplus(\ell\bmod2).
\tag{2.6}
\]

#### Proof

Both endpoints have the same two allowed colors.  A proper two-coloring
alternates those colors at every edge of the bipartite path.  For a fixed
type, exchanging the two colors complements chirality. \(\square\)

Thus a network of tight gates and same-type connectors is a signed graph:
each gate identifies its three port chiralities, and a connector has sign
equal to its path-length parity.  A cycle has a compatible chirality
exactly when the xor of its connector signs is zero.

## 3. Type words and the parity of a bicycle

Consider a physical expansion of an implication walk.  Let

\[
  u_0,u_1,\ldots,u_m\in\mathbb Z_3
\tag{3.1}
\]

be the types of its successive component variables.  Consecutive types
are distinct.  At an internal type \(u_i\), the two neighboring clauses
have the same collision color exactly when

\[
  u_{i-1}=u_{i+1}.
\tag{3.2}
\]

The accepted component-connector parity law therefore gives

\[
  \delta_i
  =
  \begin{cases}
   1,&u_{i-1}=u_{i+1},\\
   0,&\{u_{i-1},u_i,u_{i+1}\}=\mathbb Z_3.
  \end{cases}
\tag{3.3}
\]

### Theorem 3.1 (type-word holonomy) — PROVED

Put

\[
 \varepsilon_i=u_{i+1}-u_i\in\{+1,-1\}\pmod3.
\tag{3.4}
\]

Then:

1. an internal connector is odd exactly when
   \(\varepsilon_i=-\varepsilon_{i-1}\);
2. in a cyclic type word, the number of odd connectors is even;
3. if an implication path begins at a port event \(p\) and ends at
   \(\bar p\), closing its two physical endpoint ports reverses the
   ordinary connector parity at that one closure, so the resulting signed
   gate cycle has holonomy one.

#### Proof

Equation (3.2) says that the type walk immediately reverses direction,
which is exactly
\(\varepsilon_i=-\varepsilon_{i-1}\).  This proves item 1.

Around a cyclic binary word
\(\varepsilon_0,\ldots,\varepsilon_{m-1}\), the number of sign changes is
even: every change from \(+1\) to \(-1\) must be matched by a later change
back, and conversely.  By item 1 this is item 2.

At an ordinary internal continuation, the next port event is the
complement of the event reached through the preceding clause.  This is
the parity in (3.3).  At the end of a path
\(p\leadsto\bar p\), however, the final clause reaches \(\bar p\), so its
underlying endpoint event equals \(p\), rather than its complement.
For equal collision colors, event equality needs an even connector and
event complementation an odd one; for different collision colors the two
parities are reversed.  Thus the closing connector differs from (3.3) by
exactly one.  Item 2 now gives total xor one. \(\square\)

This calculation identifies the obstruction precisely.  It does not
itself contradict eternal domination: an unsatisfiable response formula
is exactly what an odd holonomy cycle records.  A graph attack is still
needed.  The next section supplies one for the first nontrivial return
geometry and all of its odd subdivisions.

## 4. The odd two-cap fork

We first record two dead-state facts in a form that does not infer graph
nonedges from missing family responses.

### Lemma 4.1 (two \(a\)-avoiding vertices) — PROVED

If \(a\notin L(r)\cup L(s)\), then for either
\(h\in\{b,c\}\),

\[
  \{h,r,s\}\notin\mathcal F.
\tag{4.1}
\]

#### Proof

Let \(d\) be the other member of \(\{b,c\}\), and attack the unoccupied
vertex \(d\).  The guard at \(h\) cannot move because \(S\) is independent.
Moving \(r\) or \(s\), if the corresponding graph edge exists, gives
\(S-a+s\) or \(S-a+r\), respectively.  Both states are absent by
(1.2).  Hence no retained response exists. \(\square\)

### Lemma 4.2 (three \(a\)-avoiding vertices) — PROVED

If \(a\notin L(r)\cup L(s)\cup L(t)\), then

\[
  \{r,s,t\}\notin\mathcal F.
\tag{4.2}
\]

#### Proof

Attack \(b\).  Every possible successor has the form
\(\{b,u,v\}\) for two of \(r,s,t\), and Lemma 4.1 excludes every such
state. \(\square\)

### Lemma 4.3 (even-distance path state) — PROVED

Let

\[
  v_0v_1\ldots v_{2r}\qquad(r\ge1)
\tag{4.3}
\]

be a vertex-distinct path in \(H\), suppose

\[
  a\notin L(v_i)\qquad(0\le i\le2r),
\tag{4.4}
\]

and let \(p\) be any vertex outside the path.  Then

\[
  \boxed{\{p,v_0,v_{2r}\}\notin\mathcal F.}
\tag{4.5}
\]

No response-list assumption on \(p\) is needed.

#### Proof

For \(r=1\), attack \(v_1\).  Neither path endpoint can move along a
graph edge because both displayed path edges lie in \(H\).  Moving \(p\),
if legal, gives the three-\(a\)-avoiding state
\(\{v_0,v_1,v_2\}\), excluded by Lemma 4.2.

Assume \(r\ge2\) and the assertion holds for shorter even paths.  From a
hypothetical state \(\{p,v_0,v_{2r}\}\), attack \(v_{2r-2}\).

- Moving \(p\) gives a three-\(a\)-avoiding state, excluded by
  Lemma 4.2.
- Moving \(v_0\) gives
  \(\{p,v_{2r-2},v_{2r}\}\), excluded by the length-two case.
- Moving \(v_{2r}\) gives
  \(\{p,v_0,v_{2r-2}\}\), excluded by induction.

These are all possible one-guard successors.  A missing move edge only
removes an option, so closure fails. \(\square\)

### Theorem 4.4 (odd two-cap fork exclusion) — PROVED

There do not exist distinct vertices

\[
  x,q,v_0,v_1,\ldots,v_m
\tag{4.6}
\]

outside \(S\), for an odd integer \(m\ge1\), such that

\[
  c\in L(v_0),\qquad c\notin L(x),
\tag{4.7}
\]

\[
  a\notin L(v_i)\qquad(0\le i\le m),
\tag{4.8}
\]

and

\[
  bq,xq,v_0q,\quad
  v_0v_1,v_1v_2,\ldots,v_{m-1}v_m,\quad
  av_m,xv_m
  \in E(H).
\tag{4.9}
\]

Arbitrary additional complement edges among the displayed vertices are
allowed.

#### Proof

By \(c\in L(v_0)\), the state

\[
  D=S-c+v_0=\{a,b,v_0\}
\tag{4.10}
\]

belongs to \(\mathcal F\).  Attack the unoccupied vertex \(x\).

- Moving \(v_0\), if legal, gives
  \(\{a,b,x\}=S-c+x\), absent by \(c\notin L(x)\).
- Moving \(a\), if legal, gives \(\{b,x,v_0\}\), which does not dominate
  \(q\) because \(bq,xq,v_0q\in E(H)\).

Closure therefore forces the only remaining response,

\[
  A=\{a,x,v_0\}\in\mathcal F.
\tag{4.11}
\]

If \(m=1\), the state \(A\) does not dominate \(v_1\), because all three
edges \(av_1,xv_1,v_0v_1\) lie in \(H\).  This is already a
contradiction.

Let \(m\ge3\).  Attack \(v_{m-1}\) from \(A\).

- Moving \(v_0\) gives \(\{a,x,v_{m-1}\}\), which does not dominate
  \(v_m\), by the last path edge and \(av_m,xv_m\in E(H)\).
- Moving \(a\) gives \(\{x,v_0,v_{m-1}\}\).  The path
  \(v_0\ldots v_{m-1}\) has positive even length, so Lemma 4.3 excludes
  this state with \(p=x\).
- Moving \(x\) gives \(\{a,v_0,v_{m-1}\}\), excluded by the same lemma
  with \(p=a\).

Every possible one-guard successor is absent.  This contradicts closure
at \(A\).  Every attack was unoccupied, and every possible response
changed exactly one guard. \(\square\)

### Corollary 4.5 (odd return between two tight gates) — PROVED

Consider a tight gate with

\[
 L(x)=\{a,b\},\quad
 L(y)=\{b,c\},\quad
 L(q)=\{a,c\},
\tag{4.12}
\]

where its failed-incidence cap has

\[
  bq,xq,yq\in E(H).
\tag{4.13}
\]

There is no odd path

\[
  y=v_0,v_1,\ldots,v_m=t
\tag{4.14}
\]

inside the \(a\)-omitting projection such that

\[
  at,xt\in E(H).
\tag{4.15}
\]

In particular, \(t\) cannot be a physical type-\(a\) cap of a second
tight gate sharing the port \(x\).

#### Proof

In (4.12), \(c\in L(y)\) and \(c\notin L(x)\).  Every vertex of
(4.14) omits \(a\), while (4.13) and (4.15) give exactly (4.9).
Apply Theorem 4.4. \(\square\)

This corollary eliminates the one-edge return and every odd subdivision.
It does not apply when consecutive gates use separated same-sign
representatives rather than one shared physical port \(x\), or when the
odd parity is spread across several connector components.

## 5. Sharp equality control for trivial two-gate holonomy

Use vertices \(0,\ldots,13\), with

\[
 (a,b,c,x,q_0,t_0,y_0,z_1,q_1,t_1,y_1,z_0,u,v)
 =
 (0,1,\ldots,13).
\tag{5.1}
\]

The labeled graph6 record of \(G\) is

```text
MEXrtIdmdjLQqztC?
```

and its canonical graph6 record is

```text
MGEFK~cfJLBi]f]Z?
```

The standalone verifier reconstructs the graph from its explicit
complement-edge table.  Its greatest eternal triple-family has 172
states, with no fixed-point deletion round, and satisfies all

\[
  172(14-3)=1892
\tag{5.2}
\]

unoccupied attack obligations.  At \(S=012\), the exact lists are

\[
\begin{array}{c|ccccccccccc}
t&3&4&5&6&7&8&9&10&11&12&13\\ \hline
L(t)&
01&12&12&12&02&02&02&02&12&01&01.
\end{array}
\tag{5.3}
\]

The two gates are:

\[
\begin{array}{c|c|c|c|c}
&\text{original edge}&\text{same-sign path}&
 \text{failed pair}&\text{tight cap}\\ \hline
0&3\,4&4-5-6&3\,6&7\\
1&3\,8&8-9-10&3\,10&11.
\end{array}
\tag{5.4}
\]

All displayed original/path/cap incidences are complement edges; the two
failed pairs are graph edges.  The caps have the required third lists and
physical anchor incidences.  The two same-sign paths have even length.

The potential return pair \(6,11\) is a graph edge, not a complement
edge.  Consequently the two gate equalities are consistent.  There are
exactly two family-compatible anchored list colorings, corresponding to
the two global chirality choices.

The exact parameters are

\[
 \boxed{
 \gamma=i=\alpha=\gamma^\infty=\theta=3.
 }
\tag{5.5}
\]

Thus neither two tight gates nor a shared physical port is forbidden.
The control sharply falsifies that overstrong local lemma.  It is
colorable and is not a gamma--theta counterexample.

## 6. Reproduction

From the campaign directory, run

```text
python3 -I -B -W error \
  math/working/third_color_gate_cycle/verify.py \
  --check math/working/third_color_gate_cycle/result.json
```

The ordinary-set verifier imports no campaign search or evaluation core.
It checks:

- the labeled graph6 record against the displayed labeled graph;
- connectedness and exact \(\gamma,i,\alpha,\theta\);
- the 172-state greatest one-guard kernel and all 1,892 obligations;
- the exact response lists in (5.3);
- both same-sign component paths and both tight gates;
- the absent odd return edge; and
- the two compatible anchored list colorings.

The canonical record displayed above is the output of the campaign's
pinned nauty `labelg` executable applied to the verified labeled record;
canonical labeling is not reimplemented in `verify.py`.

`probe.py` is the independent discovery formula.  It encodes literal
one-guard closure, an independent retained anchor state, exact displayed
lists, and optional odd connectors of prescribed length.  Exact SAT
experiments at lengths \(1,3,5\) exposed the attack pattern; Theorem 4.4
supersedes those bounded observations for every odd length.

The greatest-family serialization hash of the equality control is

```text
f0c587abd7d7123c822235793049623b02165ae134dd98c22bfa316141b1eaad
```

The universal \(k=3\) problem remains open outside the precise branch in
Corollary 4.5.
