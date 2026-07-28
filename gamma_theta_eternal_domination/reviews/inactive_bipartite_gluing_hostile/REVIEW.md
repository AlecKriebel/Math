# Hostile review: bipartite inactivity does not by itself solve gluing

## Verdict

**UNCONDITIONAL PASS**, with the candidate's explicit scope warnings.

The marked graph `HEhbtjK` is a valid countermodel to the following
purely static implication:

> deletion equality, pure maximal triangles, every-pair
> common-neighbor, facet hitting, formal ridge covariance, a full active
> root, and bipartite inactive graph force a deletion three-coloring
> that omits one color on the inactive set.

They do not.  Every deletion three-coloring of this graph uses all three
colors on the inactive set.

This does **not** refute a theorem that also assumes the target extension
has \(\gamma=3\), that its displayed response states belong to an eternal
triple-family, or that uses multi-step one-guard closure.  The explicit
extension has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,4,4).
\]

It is not a counterexample to the gamma--theta conjecture.  The complete
parameter-three case and the universal conjecture remain open.  The
candidate's minimum-order observation and order-ten strengthened absence
remain `OBSERVED`; this review did not promote either bounded search.

## 1. Independent graph reconstruction

The checker did not consume the candidate edge table.  It reconstructed
\(K_{3,3}\) from the nine displayed incidence labels and joined two line
vertices exactly when their underlying bipartite edges share an endpoint.
The resulting line graph has order \(9\), size \(18\), degree sequence
\(4^9\), and graph6 record

```text
HEhbtjK
```

Thus the claimed identification

\[
H'=L(K_{3,3})
\]

is exact.

In a line graph of a triangle-free cubic graph, every maximal clique is
the three-edge star at one original vertex.  Direct exhaustive clique
enumeration found exactly the six claimed triangles:

\[
037,\quad048,\quad136,\quad158,\quad246,\quad257.
\]

The common-neighbor assertion also holds for all 36 unordered vertex
pairs.  If the underlying \(K_{3,3}\) edges meet, the third edge at their
common endpoint supplies a line-graph common neighbor.  If they are
disjoint, either cross edge supplies one.  The clean-room checker recorded
at least one witness for every pair.

For \(G'=\overline{H'}\), exhaustive evaluation from the definitions gave

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)(G')=(3,3,3,3,3).
\]

In particular, the greatest fixed point on dominating triples contains
48 states and deletes none.  No dominating set of size at most two
exists, every maximal \(H'\)-clique has size three, and
\(\chi(H')=3\).  These calculations independently confirm all five
parameters rather than inferring eternal domination from a candidate
transition table.

## 2. Marking, covariance, and the exact caveat

The marking is

\[
A=\{1,2,5,7,8\},\qquad R=\{0,3,4,6\}.
\]

Every one of the six facets meets \(A\), and
\(\{1,5,8\}\) is a full active facet.  The inactive induced edge set is

\[
\{03,36,64,40\},
\]

so

\[
H'[R]\cong C_4.
\]

The ridge-covariance assertion is true **vacuously**.  Two star triangles
of \(L(K_{3,3})\) share at most one line vertex, so no two facets share a
two-vertex ridge.  There are therefore zero tip-pairs on which the formal
covariance rule can be tested.  This is logically sufficient for the
stated static countermodel, and the candidate note explicitly discloses
it, but the example supplies no nontrivial ridge transport.

There is a second closely related scope point.  Because the target
extension has no eternal triple-family, this marked control is not itself
an instance of the full family-relative hypotheses of C-108.  It
satisfies the extracted static facet-hitting and covariance conditions.
Accordingly it refutes only the proposed static shortcut, not C-108 or a
dynamic strengthening.

## 3. Complete coloring audit

Canonical restricted-growth enumeration, which eliminates color-name
permutations before recording a solution, found exactly two proper
three-color partitions:

\[
\begin{split}
012\mid345\mid678,\\
056\mid147\mid238.
\end{split}
\]

For the first coloring, \(R\) meets the three classes in
\(\{0\},\{3,4\},\{6\}\).  For the second, it meets them in
\(\{0,6\},\{4\},\{3\}\).  Thus every proper three-coloring of \(H'\)
uses all three colors on \(R\), even though \(H'[R]\) is bipartite.
This is the exact obstruction required by the candidate's static
boundary theorem.

## 4. Target extension and exact parameters

Adjoining \(x=9\) with

\[
N_H(x)=R
\]

produces the labeled records

```text
H = IEhbtjKe_
G = IxU[ISrXW
```

and, in the guard graph,

\[
N_G(x)=A.
\]

Independent graph6 decoding and re-encoding reproduced both strings.
Exhaustive subset, coloring, and greatest-fixed-point calculations gave

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)(G)=(2,3,3,4,4).
\]

The only dominating pair is \(\{5,9\}\).  The two-guard kernel starts
with that one state and deletes it.  The three-guard kernel starts with
58 dominating triples and deletes \(36\) in round one and the remaining
\(22\) in round two.  The four-guard kernel starts with 184 dominating
states, deletes 8, and stabilizes with 176 states.  This independently
proves \(\gamma^\infty(G)=4\).

For each of the six deletion facets, the reviewer enumerated every guard
in its intersection with \(A=N_G(x)\).  All 10 resulting one-guard
successors at \(x\) dominate \(G\).  Every deletion facet has
three-kernel deletion rank two.  In particular, the full root passes all
of these one-step domination checks.

## 5. Literal adaptive two-attack certificate

Starting from \(158\), attack the unoccupied target \(9\).  Its three
possible guard moves, and the attacker's certified second attacks, are:

| first move | first successor | second attack | only legal second move | missed vertex |
|---|---|---|---|---|
| \(1\to9\) | \(589\) | \(0\) | \(5\to0\), giving \(089\) | \(4\) |
| \(5\to9\) | \(189\) | \(0\) | \(1\to0\), giving \(089\) | \(4\) |
| \(8\to9\) | \(159\) | \(3\) | \(5\to3\), giving \(139\) | \(6\) |

Both attacks in each branch are at unoccupied vertices.  Every displayed
move changes exactly one guard and follows an edge of \(G\).  The first
successors all dominate.  At the second attack, the table lists every
adjacent guard, not a selected subset, and its successor fails to
dominate the displayed missed vertex.  Hence no eternal triple-family can
contain \(158\).  This literal tree agrees with the independent
synchronous deletion ranks: the first successors have rank one and the
root has rank two.

## 6. Model and claim-boundary audit

All dynamic checks used the standard one-guard-moves definition:

- attacks were restricted to \(V-D\);
- exactly one guard moved;
- the mover was adjacent in \(G\) to the attacked vertex;
- every retained configuration dominated \(G\); and
- greatest-family membership, not mere physical adjacency, decided
  eternal survival.

No all-guards-move rule, occupied attack, complement-side move, or clique
cover/complement-coloring reversal appears.

The accepted conclusion is deliberately narrow:

| statement | status after review |
|---|---|
| explicit static gluing countermodel | `PROVED` |
| exact target extension and two-attack failure | `PROVED` |
| smaller-order minimality of the static control | `OBSERVED` |
| no \(\gamma=3\) control through deletion order ten | `OBSERVED` |
| equality-specific dynamic gluing theorem | `OPEN` |
| complete \(k=3\) conjecture | `OPEN` |
| universal gamma--theta conjecture | `OPEN` |

The correct next theorem may use the missing common-neighbor witness for
\(\{x,5\}\), the full multi-step family constraints, or nontrivial ridge
connectivity.  This example shows that bipartiteness of \(R\) alone
cannot supply the global color synchronization.

## 7. Reproducibility and packaging

The clean-room checker imports no candidate or campaign implementation.
It uses set-valued graph states, canonical set-partition colorings, and a
fresh synchronous deletion implementation.  Run from the repository
root:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/inactive_bipartite_gluing_hostile/independent_check.py
```

Its byte-identical output is `result.json`.

An initially future-dated `frozen_at` metadata value was detected before
the verdict.  The candidate owner corrected only that timestamp.  The
review pins the corrected candidate manifest at

```text
c4d13fbd5834f261e786d9088843ef3e40ef9a90e552d565417ae2df87a51d4a
```

All eight artifact hashes listed there were rechecked.  The candidate
verifier was also rerun separately and reproduced
`countermodel_verification.json` with SHA-256

```text
014315e1ca9c189a3be550b588ba84006d8f7b15e131931778a691f0b672eaa4
```

The clean-room result SHA-256 is

```text
600e152878fc7670b4fe3822cdcb6017d85d80bc3e768aa7a4f6300905c6beed
```
