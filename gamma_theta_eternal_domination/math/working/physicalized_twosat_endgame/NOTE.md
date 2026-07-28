# Physicalizing \(k=3\) response literals does not physicalize clauses

## Status and exact boundary

Date: 2026-07-27 (PDT)

All statements use the standard one-guard-moves eternal domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained state dominates.

This note has one human theorem and one exact equality control.

1. **PROVED:** every exact two-list port has a representative with the
   same exact list, a genuine graph nonedge to the omitted anchor, and the
   same Boolean sign in the omitted-color projection.  If the original
   omission is dynamic, the representative is joined to the original port
   by an explicit length-two complement path.
2. **PROVED (logical corollary):** every occurrence of that port literal
   in the response 2-CNF can be rewritten using the physical
   representative, because the two port events are literally the same
   Boolean event.
3. **EXACT EQUALITY CONTROL:** the connected 13-vertex graph
   `LFzJbZYhdrDZdM` has an explicit 142-state eternal triple-family and
   \[
     (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3).
   \]
   It has a complement cross-clause edge \(qv\), but the only same-sign
   physical representative \(r\) of \(q\) satisfies \(rv\in E(G)\).

Thus physicalization is exact at the **literal** level and false at the
**clause-edge** level, even under the full equality hypothesis.  A clause
may be rewritten algebraically with the representative, but the rewritten
clause cannot be fed to a graph attack proof as though its supporting
complement edge had moved.

The control is colorable and is not a gamma--theta counterexample.  It
does not realize an unsatisfiable response 2-CNF.  Its purpose is to
refute connector transport, not to refute the conjecture.

The accepted prerequisites used below are:

- `math/working/k3_projection_gluing.md`;
- `math/working/separated_core_n14_attack/NOTE.md`, especially the
  two-response replication lemma; and
- the frozen-color bipartiteness theorem recorded in
  `math/working/k3_cross_state_attack.md`.

## 1. Setup

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, and suppose

\[
 \gamma(G)\geq3.
\tag{1.1}
\]

The family gives \(\gamma^\infty(G)\leq3\), while the independent state
gives

\[
 3\leq\alpha(G)\leq\gamma^\infty(G).
\]

Consequently all three parameters in this display equal three, and
\(\gamma(G)=3\) as well.

Put \(H=\overline G\), and for \(t\notin S\) write

\[
 L(t)=\{i\in S:S-i+t\in\mathcal F\}.
\tag{1.2}
\]

Membership \(i\in L(t)\) forces \(it\in E(G)\), because the retained
successor \(S-i+t\) must dominate the omitted anchor \(i\).

For the omitted color \(c\), put

\[
 W_c=\{t\notin S:c\notin L(t)\}.
\tag{1.3}
\]

The accepted frozen-color theorem makes

\[
 B_c=H[\{a,b\}\cup W_c]
\tag{1.4}
\]

bipartite.

## 2. Every two-list literal has a physical representative

### Theorem 2.1 (same-sign physical representative) — PROVED

Suppose

\[
 L(t)=\{a,b\}.
\tag{2.1}
\]

There is a vertex \(r\notin S\) such that

\[
 L(r)=\{a,b\},\qquad cr\in E(H),
\tag{2.2}
\]

and \(t,r\) lie in the same component and on the same bipartition side of
\(B_c\).

More precisely, exactly one of the following constructions applies.

1. If \(ct\in E(H)\), one may take \(r=t\).
2. If \(ct\in E(G)\), there are distinct vertices \(y,r\notin S\) with
   \[
   ty,yr,cy,cr\in E(H),\qquad tr\in E(G),
   \tag{2.3}
   \]
   and
   \[
   L(r)=\{a,b\}.
   \tag{2.4}
   \]
   In particular,
   \[
   t-y-r
   \tag{2.5}
   \]
   is a length-two path in \(H[W_c]\).

#### Proof

If \(ct\in E(H)\), equation (2.1) already makes \(t\) a physical
representative, and the conclusion with \(r=t\) is immediate.

Suppose \(ct\in E(G)\).  Equation (2.1) also forces

\[
 at,bt\in E(G).
\]

Thus \(t\) is \(G\)-complete to \(S\).  Apply the accepted pure
omitted-color pair lemma to \(t\), with positive responses \(a,b\) and
omitted anchor \(c\).  It supplies distinct \(y,r\) satisfying (2.3),

\[
 N_H(y)\cap S=N_H(r)\cap S=\{c\},
\tag{2.6}
\]

and

\[
 a,b\in L(r).
\tag{2.7}
\]

The graph nonedge \(cr\in E(H)\) excludes \(c\) from \(L(r)\).
Together with (2.7), this proves (2.4).

Likewise \(cy\in E(H)\) gives \(c\notin L(y)\).  Hence

\[
 t,y,r\in W_c,
\]

and (2.3) gives the path (2.5).  Its even length puts \(t,r\) on the
same side of their common bipartite component in \(B_c\). \(\square\)

The theorem is cyclically symmetric in \(a,b,c\).

### Corollary 2.2 (literal physicalization) — PROVED

Fix a bipartition coordinate \(\pi_c\) on the component in Theorem 2.1
and its flip variable \(z_{c,K}\).  For either \(w\in\{a,b\}\), let

\[
 P(t,w):
 z_{c,K}=\pi_c(t)\oplus\iota_c(w)
\tag{2.8}
\]

be the usual port event.  Then

\[
 \boxed{P(t,w)=P(r,w)}
\tag{2.9}
\]

as Boolean events.

Consequently, if a complement edge \(tq\) supplies a cross clause

\[
 \neg P(t,w)\lor\neg P(q,w),
\tag{2.10}
\]

the same logical clause can be written

\[
 \neg P(r,w)\lor\neg P(q,w).
\tag{2.11}
\]

#### Proof

Theorem 2.1 puts \(t,r\) on the same side of one component, so

\[
 \pi_c(t)=\pi_c(r).
\]

Substitution in (2.8) proves (2.9), and replacing equal Boolean events in
(2.10) gives (2.11). \(\square\)

Corollary 2.2 is a statement about one component variable.  It does
**not** assert

\[
 rq\in E(H).
\tag{2.12}
\]

The next section shows that (2.12) can fail for every same-sign physical
representative even when all four equality parameters are three.

## 3. An equality control with no physical clause transport

### 3.1 The graph

Use the vertices

\[
 (a,b,c,q,v,z,u,v',r,d,e,c',a')=(0,1,\ldots,12).
\]

Assign each vertex the two-coordinate word in the following table.

\[
\begin{array}{c|ccccccccccccc}
x&a&b&c&q&v&z&u&v'&r&d&e&c'&a'\\ \hline
\lambda_0(x)&0&1&2&0&1&1&2&1&0&2&0&2&0\\
\lambda_1(x)&0&1&2&1&2&0&1&2&1&0&2&2&0
\end{array}
\tag{3.1}
\]

Two distinct vertices are adjacent in \(G\) when they agree in at least
one coordinate, together with the three extra edges

\[
 cq,\qquad av,\qquad vr.
\tag{3.2}
\]

The resulting labeled graph6 record is

```text
LFzJbZYhdrDZdM
```

and it has 43 edges.

For \(j\in\{0,1\}\) and \(i\in\{0,1,2\}\), put

\[
 C_i^j=\{x:\lambda_j(x)=i\}.
\tag{3.3}
\]

Each \(C_i^j\) is a clique of \(G\).

### 3.2 The eternal family

Let \(\mathcal F_j\) be the family of all transversals

\[
 \{x_0,x_1,x_2\},
 \qquad x_i\in C_i^j,
\tag{3.4}
\]

and put

\[
 \mathcal F=\mathcal F_0\cup\mathcal F_1.
\tag{3.5}
\]

The two class-size triples are

\[
 (|C_0^0|,|C_1^0|,|C_2^0|)=(5,4,4),
\qquad
 (|C_0^1|,|C_1^1|,|C_2^1|)=(4,4,5).
\tag{3.6}
\]

Thus each \(\mathcal F_j\) has 80 states, while their union has

\[
 |\mathcal F|=142.
\tag{3.7}
\]

Every transversal dominates \(G\): it has one guard in each clique
\(C_i^j\).  From a transversal in \(\mathcal F_j\), an attack at an
unoccupied vertex of \(C_i^j\) is answered by moving the guard already in
that clique.  The successor is again a transversal in
\(\mathcal F_j\).  Hence each \(\mathcal F_j\), and therefore their
union, is an eternal family.

The state

\[
 S=\{a,b,c\}
\tag{3.8}
\]

is a transversal in both families and is independent.  Directly from
(3.4),

\[
 S-i+x\in\mathcal F
 \quad\Longleftrightarrow\quad
 \lambda_0(x)=i\ \text{or}\ \lambda_1(x)=i.
\tag{3.9}
\]

The response list of a vertex is therefore exactly the set of symbols
appearing in its word.  In particular,

\[
 L(q)=L(z)=L(r)=\{a,b\},
\qquad
 L(v)=\{b,c\}.
\tag{3.10}
\]

The extra edges in (3.2) make both \(q\) and \(v\) \(G\)-complete to
\(S\), without adding the dynamically omitted colors \(c\) and \(a\) to
their lists.

### 3.3 Exact parameters

The partition

\[
 C_0^0\mid C_1^0\mid C_2^0
\tag{3.11}
\]

is a three-clique partition of \(G\), so \(\theta(G)\leq3\) and
\(\alpha(G)\leq3\).  The independent state \(S\) gives the reverse
inequality for \(\alpha\), and the standard
\(\alpha\leq\theta\) gives

\[
 \alpha(G)=\theta(G)=3.
\tag{3.12}
\]

The verifier records, for every pair of vertices, one common neighbor in
\(H\).  For compact human checking, the following triangular table gives
the witness names.  In the row of \(x_i\), entries correspond in order to
the later columns \(x_{i+1},\ldots,x_{12}\) in

\[
 a,b,c,q,v,z,u,v',r,d,e,c',a'.
\]

```text
a : c b v' u c v' u c b b b b
b : a d d c a a c e d a c
c : z a' r a a z b b a b
q : d c' v d z v z z v
v : q a' q d q u q u
z : e q c q u q c
u : a z v z a v
v': d q u a u
r : v' z z c
d : b b b
e : b b
c': b
```

Thus no pair dominates \(G\), while \(S\) dominates, proving

\[
 \gamma(G)=3.
\tag{3.13}
\]

The eternal family proves \(\gamma^\infty(G)\leq3\), and
\(\alpha(G)\leq\gamma^\infty(G)\) proves

\[
 \gamma^\infty(G)=3.
\tag{3.14}
\]

Therefore

\[
 \boxed{
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3).
 }
\tag{3.15}
\]

### 3.4 The failed transport

The ports \(q,v\) satisfy

\[
 qv\in E(H).
\tag{3.16}
\]

Their lists in (3.10) intersect in color \(b\), so (3.16) is a genuine
cross-clause edge.

For the list \(\{a,b\}\), the dynamically omitted color is \(c\).
The relevant complement projection contains

\[
 q-z-r
\tag{3.17}
\]

as a length-two path.  The vertex \(r\) is physical:

\[
 cr\in E(H),
\tag{3.18}
\]

and (3.17) puts \(r\) on the same projection side as \(q\).  The other
physical \(\{a,b\}\)-vertex \(z\) lies on the opposite side.  Hence \(r\)
is the unique same-sign physical representative of \(q\).

But the third extra edge in (3.2) is

\[
 rv\in E(G).
\tag{3.19}
\]

Thus the clause supported by \(qv\in E(H)\) can be rewritten using the
Boolean identity \(P(q,b)=P(r,b)\), but there is no complement edge
\(rv\) supporting the rewritten expression physically.

This proves that connector-clause transport is false under equality.
It also pinpoints the surviving information: the formula retains the
clause because it retains the original edge \(qv\); only a graph attack
argument that substitutes \(r\) for \(q\) is invalid.

## 4. Consequences for the 2-SAT endgame

Theorem 2.1 closes one gap cleanly:

> every two-list Boolean sign can be represented at a vertex whose
> omitted color is a genuine graph nonedge.

It does not close the stronger gap:

> every cross clause incident with that sign can be represented by
> complement edges incident with the physical representative.

The 13-vertex equality control disproves the stronger assertion.  In
particular, a long two-unit chain, lollipop, or bicycle may be rewritten
so that each literal is named by a physical representative, but its
successive clauses can still live on separated original ports.  The
accepted odd-fan and cap attacks require literal complement edges and
therefore cannot be invoked on the rewritten formula alone.

This route should resume only with an additional incidence theorem that
uses more than component-variable equality—for example, a result forcing
one physical representative to retain two specified clause edges in an
inclusion-minimal unsatisfiable core.  The theorem proved here supplies no
such incidence.

## 5. Reproduction

Run:

```text
python3 -I -B -W error \
  math/working/physicalized_twosat_endgame/verify.py
```

The ordinary-set verifier:

- constructs the graph from (3.1)--(3.2);
- reconstructs both transversal families and their union;
- checks all
  \[
  142(13-3)=1420
  \]
  unoccupied one-guard obligations;
- checks \(\gamma=\alpha=\gamma^\infty=\theta=3\);
- reconstructs every list at \(S\);
- verifies the path \(q-z-r\), its projection parity, and uniqueness of
  the same-sign physical representative;
- verifies \(qv\in E(H)\) but \(rv\in E(G)\); and
- emits one common complement neighbor for every vertex pair.

The serialized 142-state family has SHA-256

```text
9e49fca49aceff56168e0aef5cd825b5a55ec73a901985daec7bc03a9022e4aa
```

No literature-priority claim is made.
