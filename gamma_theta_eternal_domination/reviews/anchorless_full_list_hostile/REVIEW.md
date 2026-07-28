# Hostile audit: anchorless vertices at a full response

## Verdict

Date: 2026-07-28 (PDT)

\[
\boxed{\texttt{PASS}}
\]

The component-side palette theorem, its zero/one/two-spoke
classification, the shared-omission reverse state, the
deletion-critical installed clique layer, the layer-multiplicity bound,
and the conditional order bound in
`math/working/anchorless_full_list_structure/NOTE.md` are correct.

The audited candidate manifest has SHA-256

```text
d8f26d91e58f28289c4b38aafe6ca6f0a543b127822991a403ffdd2ae36a7033
```

and all eight files listed in that manifest match their recorded hashes.
The proof uses the standard one-guard model throughout.  No attack is
made at an occupied vertex, every response moves exactly one guard along
an edge of \(G\), and every dynamic palette statement uses membership in
the same eternal family rather than mere domination of a proposed
successor.

This result does **not** eliminate anchorless vertices, synchronize
different physical-link components, close the full-list branch, prove
the complete \(k=3\) case, or resolve the universal conjecture.  The
order-10 scan and the radius-two toggle probe remain `OBSERVED`; this
review does not promote either computation.

## 1. Dependency and quantifier audit

Write \(H=\overline G\), let

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]

let \(\mathcal F\) be an arbitrary optimal eternal family of triples, and
let \(S=\{s_0,s_1,s_2\}\in\mathcal F\) be independent.  Suppose
\(x\notin S\) has all three retained first responses

\[
D_j=S-\{s_j\}+\{x\}\in\mathcal F.
\]

The candidate uses its accepted dependencies within their exact scopes.

### C-073

C-073 applies to the same physical set

\[
B=N_H(x).
\]

It proves that \(H[B]\) is bipartite and has no isolated vertex under the
displayed equality assumptions.  It also proves, for this arbitrary
specified family \(\mathcal F\), that the \(X,U,V\) response-role
signature at an attacked anchor is constant on every connected
component of \(H[B]\).  The candidate neither substitutes the larger
family-inactive set \(R_x\) for \(B\) nor coordinates signatures between
different components.

### C-132

For

\[
P(b)=\{i:\{x,s_i,b\}\in\mathcal F\},
\]

C-132 gives \(|P(b)|\ge2\), gives \(i\in P(b)\) when
\(b\in B_i=B\cap N_H(s_i)\), and gives

\[
i\in P(b)\Longrightarrow
N_{H[B]}(b)\cap B_i=\varnothing.
\]

These are retained-family palettes.  The candidate does not replace
them by the larger static dominating palettes.

### C-127

The external-layer theorem explicitly adds the hypothesis

\[
\gamma(G-x)\ge3.
\]

Only after adding it does the proof use C-127's equivalent complement
condition that every pair in \(H-x\) has a common neighbor in \(H-x\).
The note does not assert that every full target in every equality graph
has deletion domination number three.  Indeed, its order-12 equality
control has \(\gamma(G-x)=2\).

### C-089

C-089 assumes \(\gamma(G)\ge3\) and a full retained response at \(S\);
both hold in the candidate's theorem setup.  Its conclusion is

\[
|V(G)|\ge |Q_S|+9,
\qquad
Q_S=\{q\notin S:q\text{ is \(G\)-adjacent to all of }S\}.
\]

If \(t=|B_*|\), then \(x\in Q_S\), every anchorless
\(b\in B_*\) lies in \(Q_S\), and these \(t+1\) vertices are distinct.
Thus

\[
|V(G)|\ge(t+1)+9=t+10.
\]

No disjointness between the new \(Y_i(b)\) layers and C-089's witnesses
is assumed in this arithmetic.

## 2. Component-side palette uniformity

Fix a component \(C=U\mathbin{\dot\cup}V\) of \(H[B]\) and an edge
\(bc\), where \(b\in U\) and \(c\in V\).  The three vertices

\[
T_{bc}=\{x,b,c\}
\]

are pairwise adjacent in \(H\), hence form an independent triple in
\(G\).  Since \(\alpha(G)=3\), this is a maximum independent set and
therefore belongs to every optimal eternal triple-family, including
\(\mathcal F\).

Attack the unoccupied anchor \(s_i\) from \(T_{bc}\).  The guard at \(c\)
can answer exactly when

\[
cs_i\in E(G)
\quad\text{and}\quad
\{x,b,s_i\}\in\mathcal F.
\]

The second condition is \(i\in P(b)\).  Conversely, if \(i\in P(b)\),
C-132 makes \(b\) \(H[B]\)-anticomplete to \(B_i\).  Since
\(bc\in E(H[B])\), this forces \(c\notin B_i\), equivalently
\(cs_i\in E(G)\).  Thus

\[
c\text{ answers at }s_i\text{ from }T_{bc}
\quad\Longleftrightarrow\quad i\in P(b).
\]

C-073 makes the \(V\)-side response role independent of the chosen edge
of \(C\), so \(P(b)\) is constant on \(U\).  Interchanging the sides
makes \(P(c)\) constant on \(V\).  C-132 supplies the lower bound two on
both side palettes.  This proves Theorem 2.1 with no greatest-family
assumption.

## 3. Exact component types and reverse states

Suppose the \(U\)-side meets \(B_q\).  C-132 puts \(q\) in the
\(U\)-palette.  For an incident edge \(bc\) with \(b\in B_q\), the index
\(q\) cannot lie in the \(V\)-palette: otherwise C-132 would make \(c\)
anticomplete to \(B_q\), contradicting \(bc\in E(H)\).  A subset of
three colors of size at least two which omits \(q\) is exactly
\(\{0,1,2\}-\{q\}\).

If one side met two spokes, the opposite palette would omit two colors,
contradicting its size bound.  If the two sides met the same spoke, one
side's mandatory own-spoke color would contradict the omission forced
by the other side.  Consequently each side meets at most one spoke, the
two occurring spoke labels are distinct, and two occurring labels force
the two complementary palettes exactly.  The zero/one/two-spoke
classification follows.

Now suppose an index \(i\) is absent from both side palettes.  From
\(T_{bc}\), an attack at the unoccupied vertex \(s_i\) cannot be answered
by \(b\) or \(c\), because their two possible successors are precisely
the absent palette states.  Fullness makes \(xs_i\in E(G)\).  Closure
therefore forces the sole remaining responder

\[
x\longrightarrow s_i
\]

and installs

\[
\{s_i,b,c\}\in\mathcal F.
\]

Because each side palette has size at least two, at most one index can
be omitted from both.  This is a family-membership conclusion, not an
inference from a graph nonedge.

## 4. Deletion-critical third attack

Let \(b\in B_*\) and \(i\in P(b)\).  Anchorlessness means that \(b\) is
adjacent in \(G\) to every anchor.  C-127 applied to the pair
\(\{b,s_i\}\subseteq V(H-x)\) makes

\[
Y_i(b)=N_{H-x}(b)\cap N_{H-x}(s_i)
\]

nonempty.

The retained state

\[
E_i(b)=\{x,s_i,b\}\in\mathcal F
\]

dominates \(G\).  If \(y\in Y_i(b)\cap B\), then \(y\) is adjacent in
\(H\) to all three members of \(E_i(b)\), contradicting domination.
Thus \(Y_i(b)\cap B=\varnothing\), and every \(y\in Y_i(b)\) satisfies
\(xy\in E(G)\).

The attack at \(y\) from \(E_i(b)\) is unoccupied.  It cannot equal
\(x,b,s_i\) by the loopless definitions, and it cannot be a different
anchor because \(b\in B_*\) has no \(H\)-edge to any anchor.  The guards
at \(b\) and \(s_i\) are physically blocked by their \(H\)-edges to
\(y\), while the guard at \(x\) is physically able to move.  Hence the
unique response is

\[
x\longrightarrow y,
\qquad
\{b,s_i,y\}\in\mathcal F.
\]

If two distinct members \(y,z\in Y_i(b)\) were adjacent in \(H\), then
\(z\) would be a common \(H\)-neighbor of the retained state
\(\{b,s_i,y\}\).  That state would not dominate \(G\).  Therefore
\(Y_i(b)\) is independent in \(H\), equivalently a clique in \(G\).

For fixed \(b\), one vertex cannot lie in all three \(Y_i(b)\): it would
form a \(K_4\) in \(H\) with the root triangle \(S\), contradicting
\(\alpha(G)=3\).  Since each indexed layer is nonempty, a palette of
size \(m\) has union size at least \(\lceil m/2\rceil\).  In particular,
a full palette needs at least two installed external vertices.

## 5. Independent reconstruction

The clean-room checker uses a fresh short-graph6 decoder, integer
adjacency masks, exhaustive subset searches, a separate coloring
backtracker, and a synchronous greatest-fixed-point implementation
written directly from the one-guard definition.  It imports no candidate
or campaign evaluator.

It reconstructs all three candidate controls:

| graph | exact \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | family | physical-link result |
|---|---:|---:|---|
| ``Ksv`f\knJVis`` | \((3,3,3,3,3)\) | 127 triples | two two-spoke edge components, no anchorless vertex |
| `EEz_` | \((2,2,3,3,3)\) | 18 triples | one spoke plus one anchorless vertex |
| `EFz_` | \((2,3,3,3,3)\) | 20 triples | two anchorless vertices |

For every retained state in each control, every unoccupied attack has a
one-edge successor in the same family.  The checker verifies all
\(1{,}143\), \(54\), and \(60\) obligations, respectively.  It also
reconstructs every physical link, spoke, retained palette, bipartition,
and component response-role signature.

The reviewer additionally found the eight-vertex scope control

```text
GCXfVg
```

with root \(\{0,1,2\}\), target \(7\), and anchorless physical vertex
\(6\).  It has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3),
\qquad
\gamma(G-7)=3,
\]

and \(P(6)=\{0,1,2\}\).  The independently reconstructed layers are

\[
Y_0(6)=\{5\},\qquad
Y_1(6)=Y_2(6)=\{3\}.
\]

All three forced third-attack states survive, and the union has the
predicted size two.  This control deliberately has \(\gamma(G)=2\) and
isolates in its physical link.  It validates the literal third-attack
mechanism while sharply confirming that C-073's link conclusion and
C-089's order count must not be used after their equality hypotheses are
dropped.

The checker also exhausts the finite palette/spoke truth table behind
Corollary 2.2 and the layer-cover truth table behind Corollary 3.2.

## 6. Computational evidence boundary

The candidate labels its order-10 complement scan and radius-two edit
probe as `OBSERVED`.  Their files are hash-frozen, but this review did
not independently regenerate the 2,894,632 graph stream, audit
canonical coverage, or replay all 8,584 labelled edits.  Those counts
are therefore not certified finite results and are not used in any
proof above.

## 7. Claim ledger

| statement | audit status |
|---|---|
| component-side retained-palette uniformity | `PROVED` |
| zero/one/two-spoke component classification | `PROVED` |
| shared-omission reverse family state | `PROVED` |
| deletion-critical external clique installation | `PROVED` |
| external-layer multiplicity bound | `PROVED` |
| conditional \(n\ge |B_*|+10\) | `PROVED` |
| order-10 no-anchorless-full-root scan | `OBSERVED` |
| radius-two equality-control repair probe | `OBSERVED` |
| elimination of anchorless physical vertices | `OPEN` |
| global component synchronization | `OPEN` |
| complete full-list branch | `OPEN` |
| complete \(k=3\) theorem | `OPEN` |
| universal \(\gamma\)--\(\theta\) conjecture | `OPEN` |

## 8. Reproduction

From the campaign root, run:

```text
python3 -I -B -W error \
  reviews/anchorless_full_list_hostile/independent_checker.py
```

The checker rewrites `result.json` byte-for-byte, prints that JSON, and
then prints its SHA-256.
