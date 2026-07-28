# Hostile audit: the dynamic fate of \(Y_k\)

## Verdict

Date: 2026-07-28 PDT

Candidate reviewed:

```text
math/working/all_k_yk_dynamic/
```

Candidate manifest SHA-256:

```text
ae7ec69d98efa2386704912782b3c61083ec2d29c493eb1b38327e696a812e98
```

The candidate passed this audit, with the following exact scope.

| Candidate statement | Verdict | Scope |
|---|---|---|
| Simultaneous singleton installation, Lemma 1.1 | **PROVED** | Unconditional under (0.2) and the stated \(Y_k\) incidence pattern. |
| Carried base-list rigidity, Theorem 2.1 | **PROVED** | The base portions of the original family lists are exactly the \(Y_3\) caps.  Colors in \(D\) may also occur. |
| Dirty-edge private buffer, Lemma 3.1 | **PROVED** | Every wrong graph edge \(uz_d\) produces a closed private witness for \(u\) which misses \(z_d\). |
| Clean equality-three projection, Lemma 4.1 | **PROVED** | Requires cleanliness and \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=k\). |
| Clean order floor \(n\geq2k+6\), Theorem 4.2 | **PROVED** | Requires an exact static \(Y_k\), cleanliness, equality, and accepted C-072. |
| Improved floor \(n\geq2k+8\), Corollary 5.1 | **PROVED, CONDITIONAL** | Requires, in addition, that all projected forbidden static roles remain forbidden, equivalently \(\widehat L_i=A_i\).  This does **not** follow from the original exact static lists. |
| Seven-vertex static-repair control | **INDEPENDENTLY VERIFIED FINITE CONTROL** | Parameters are \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,4,4,4)\); the projection has \((2,2,3,3,3)\).  It is neither an equality-\(4\) graph nor a conjecture counterexample. |
| Automatic transport of static lists through a clean replacement | **REFUTED WITHOUT THE EQUALITY HYPOTHESIS** | The control enlarges the projected static list from \(\{0\}\) to \(\{0,2\}\).  An equality-specific transport theorem remains open. |
| All-order exclusion of \(Y_k\), \(\mathsf{GL}(k)\), or the universal conjecture | **OPEN** | None follows from this note. |

No mathematical correction to the candidate note is required.  In
particular, the phrase “\(n\geq2k+8\)” must always travel with the
projected-static-defect-survival hypothesis; it is not an unconditional
all-\(k\) floor.

## 1. Independent proof audit

### 1.1 Simultaneous installation

For each \(d\in D\), an attack on \(z_d\) from \(S\), together with

\[
L_S^{\mathcal F}(z_d)\subseteq L_S^{\rm stat}(z_d)=\{d\},
\]

first proves

\[
L_S^{\mathcal F}(z_d)=\{d\}.
\]

Suppose \(T_R\) is retained and \(e\in D-R\).  A guard already at some
\(z_d\), \(d\in R\), cannot answer an attack at \(z_e\), because \(Z\) is
a clique in \(H=\overline G\).  If a guard
\(g\in S-R-\{e\}\) answered, the successor would miss
\(R\cup\{g\}\) from \(S\), whereas its outside vertices
\(Z_R\cup\{z_e\}\) have original family-list union exactly
\(R\cup\{e\}\).  Arbitrary-state restoration fails at \(g\).
Consequently only \(e\) can move.  Induction installs every subset \(R\),
including all of \(Z\).  The attack is always at an unoccupied vertex and
exactly one guard moves along a graph edge.

This proof does not assume that the installed state is independent.

### 1.2 Carried rigidity

The installed state \(T=B\cup Z\) is retained.  Since every \(z_d\) is a
graph nonneighbor of every path vertex, an attack at \(x_0\) must be
answered by a base guard.  Restoration relative to the original state
\(S\) rules out \(b,c\), because \(Z\cup\{x_0\}\) supplies only the
missing colors \(D\cup\{a\}\).  Hence the first successor is

\[
Z\cup\{b,c,x_0\}.
\]

At \(x_1\), the guards in \(Z\) and the guard at \(x_0\) are graph
nonneighbors of the attack.  A move by \(b\) would produce a state whose
outside original-list union omits the missing color \(b\).  Thus \(c\)
moves, and restoration at the successor forces
\(c\in L_S^{\mathcal F}(x_1)\).  Reflection forces the analogous
\(x_2\) state and color.

Under the supposition
\(b\notin L_S^{\mathcal F}(x_2)\), attack \(x_0\) from
\(Z\cup\{a,x_2,x_3\}\).  Restoration separately rules out the
\(x_2\)- and \(x_3\)-successors, so \(a\) moves.  An attack at \(x_1\)
then has the unique graph responder \(x_3\).  The resulting state's
outside original-list union is contained in \(D\cup\{a,c\}\), although
all of \(S\), including \(b\), is missing.  This contradicts restoration.
Reflection completes the exact four base caps.

As a second check, `independent_check.py` exhausts all \(64\) choices of
the unspecified base-to-path graph edges.  For each choice it tests all
eight nonexact nonempty subpatterns of the two mixed family lists in a
greatest local kernel which deliberately overapproximates an actual family
by enforcing only restoration and the relevant one-guard path attacks.
The installed base state is deleted in all \(512\) cases.  This finite
check is corroborative; the argument above is the general proof.

### 1.3 Dirty edges

If \(uz_d\in E(G)\) for \(u\ne d\), but
\(u\notin L_S^{\rm stat}(z_d)\), then \(S-u+z_d\) fails domination.
Let \(p\) be missed.  It is nonadjacent to \(z_d\) and to
\(S-\{u\}\).  The state \(S-d+z_d\) does dominate, and its only member
which can dominate \(p\) is \(u\).  Therefore

\[
N_G[p]\cap S=\{u\},\qquad pz_d\in E(H).
\]

The possible closed-neighborhood corner cases are harmless:
\(p\ne u\) because \(uz_d\in E(G)\), and \(p\notin S-\{u\}\) because
those vertices are occupied in the failed swap.

When \(u\in B\), the candidate's asserted externality also checks:
each \(x_i\) sees every member of the nonempty set \(D\), and each
\(z_e\) sees its own anchor \(e\), so none has private block
\(\{u\}\).  Buffers for two distinct base anchors cannot coincide because
their intersections with \(S\) would be two different singletons.

### 1.4 Clean projection and inherited equality

Under cleanliness, \(T=B\cup Z\) is independent.  In the induced common
antineighborhood

\[
J=G[\{v\notin Z:E_G(v,Z)=\varnothing\}],
\]

the residual family

\[
\mathcal P=\{C:Z\cup C\in\mathcal F\}
\]

is nonempty.  On an attack in \(J\), no frozen guard in \(Z\) can move,
so a residual guard answers and the successor stays in \(\mathcal P\).
Every residual state dominates \(J\), since no vertex of \(J\) can be
dominated from \(Z\).

The parameter inheritance is exact:

- \(B\) is an independent triple;
- an independent four-set in \(J\), together with \(Z\), would be an
  independent \((k+1)\)-set in \(G\);
- \(\mathcal P\) gives an eternal triple-family; and
- a dominating pair in \(J\), together with \(Z\), would dominate all of
  \(G\): vertices outside \(J\cup Z\) have a graph neighbor in \(Z\).

Thus

\[
\gamma(J)=\alpha(J)=\gamma^\infty(J)=3.
\]

For each \(x_i\), a response from \(B\) in \(\mathcal P\) lifts to a
retained state \(Z\cup(B-u+x_i)\).  Restoration relative to \(S\) forces
\(u\) into the original base cap \(A_i\).  Applying the already-audited
mixed-path restoration argument inside the genuine triple-family
\(\mathcal P\) forces all four family lists to be exactly

\[
\{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
\]

No equality of original and projected **static** lists has been used.

### 1.5 The two order counts

The hypotheses just established are precisely those of accepted C-072:
an equality-three graph, an independent retained reference triple, an
induced complement \(P_4\), and the exact family-response pattern.
Therefore \(|V(J)|\ge12\).

Every member of \(Z\) is outside \(J\) by definition.  Every
\(d\in D\) is outside \(J\) because \(dz_d\in E(G)\).  The disjoint
sets \(D,Z\) contribute another \(2(k-3)\) vertices, giving

\[
|V(G)|\ge12+2(k-3)=2k+6.
\]

Accepted C-121 has the stronger hypothesis that the four **static**
lists in the equality-three graph are exact.  It therefore applies to
\(J\) only under

\[
\widehat L_i=A_i\qquad(0\le i\le3).
\]

With this additional hypothesis, \(|V(J)|\ge14\) and the same disjoint
count gives

\[
|V(G)|\ge14+2(k-3)=2k+8.
\]

Original static exactness does not supply this additional hypothesis:
an original defect witness can be adjacent to a member of \(Z\), hence
lie outside \(J\), so freezing \(Z\) can repair the failed swap.  This is
exactly the boundary tested by the finite control.

## 2. Independent finite replay

The clean-room checker:

- pins and verifies all four files in the candidate manifest;
- decodes `F?E\`O` directly from graph6 and recovers exactly
  \(05,25,26,34,46\);
- recomputes \(\gamma,i,\alpha,\gamma^\infty,\theta\) by exhaustive
  bit-mask searches;
- computes the eternal kernel by predecessor-support queue deletion,
  rather than importing the candidate's fixed-point routine;
- computes \(\theta\) by direct clique-partition dynamic programming,
  rather than complement coloring;
- checks all \(24\) unoccupied one-guard obligations of the eight-state
  four-guard family;
- checks the original and replacement static/family lists;
- checks vertex \(6\) as the old failed-swap witness and vertex \(4\) as
  its repair; and
- independently checks the common-antineighborhood projection and its
  two-state eternal subfamily.

The independently recovered parameters are

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)(G)=(3,3,4,4,4)
\]

and

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)(J)=(2,2,3,3,3).
\]

Run from the campaign root:

```text
python3 -I -B -W error \
  reviews/all_k_yk_dynamic_hostile/independent_check.py
```

The captured successful replay is `independent_check.stdout`.

## 3. Publication boundary

This note supplies two conditional all-parameter order floors and a
precise diagnostic split:

1. dirty installation produces a private buffer;
2. clean installation gives an equality-three dynamic projection; and
3. the stronger static projection occurs only when defects survive.

It does not eliminate either gate.  In particular, it does not prove an
unconditional lower bound \(2k+6\) or \(2k+8\) for counterexamples, does
not prove that every \(Y_k\) realization is clean, and does not establish
global list gluing at any parameter.
