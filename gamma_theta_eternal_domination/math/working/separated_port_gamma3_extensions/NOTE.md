# One-vertex extensions of the separated-port lollipop control

## Status

Date: 2026-07-27 (PDT)

**OBSERVED with two independent exact replays and a hostile-review `PASS`;
not a theorem and not a resolution of the gamma--theta conjecture.**

No equality-valued gamma-3 control occurs among:

1. all \(2^9=512\) labeled one-vertex extensions of `HFzvvn{`; or
2. all \(27\cdot2^9=13,824\) cases obtained by additionally adding one
   non-core complement edge among the nine old vertices.

The second scope is the relevant one-edge local neighborhood: changing an
edge incident with the new vertex is already another one-vertex extension,
while deleting one of the nine literal core edges destroys the specified
separated-port lollipop rather than extending it.

The finite result is positive evidence for the proposed
"minimal lollipop or dominating pair" route: every case retaining the exact
augmentation-sensitive family pattern has \(\gamma\le2\).  It does not prove
that conclusion for arbitrary extensions.

## 1. Exact predicate

The base labels and response lists are those of
`math/working/full_list_odd_lollipop_integration/NOTE.md`:

\[
S=\{0,1,2\},\qquad x=3,
\]

\[
\begin{array}{c|cccccc}
y&3&4&5&6&7&8\\ \hline
L(y)&012&01&01&01&12&12.
\end{array}
\]

For every derived graph, the program existentially quantifies the new
vertex's response list over all nonempty proper subsets of \(S\).  A case is
positive exactly when there is an eternal triple-family \(\mathcal F\) such
that:

1. \(S\in\mathcal F\);
2. the six old response lists are exactly those displayed above;
3. the new response list is nonempty and proper, so \(x=3\) is the unique
   full-list target;
4. the full list-coloring instance with \(x\) removed is satisfiable; and
5. fixing \(x\) to anchor color \(0\) makes the full instance
   unsatisfiable.

The family quantifier allows arbitrary proper subfamilies.  For each proposed
new list, the search bans precisely the excluded direct swaps and computes
the greatest eternal kernel of all remaining dominating triples.  There is
an admissible subfamily if and only if \(S\) and every required direct swap
survive that kernel: any admissible family is contained in the kernel, and
the kernel itself supplies a witness in the converse direction.

This is stronger than merely retaining the old induced Boolean core.  The
new vertex and the extra complement edge participate in the global base and
augmented list-coloring checks.

## 2. One-vertex extensions

Extension masks record the complement neighbors of the new vertex \(9\).
Nauty's `labelg` was used only for canonical deduplication; every labeled
mask was evaluated before deduplication.

\[
\begin{array}{l|r}
\text{quantity}&\text{count}\\ \hline
\text{labeled extensions}&512\\
\text{canonical graphs}&160\\
\text{predicate-positive labeled extensions}&99\\
\text{predicate-positive canonical graphs}&42.
\end{array}
\]

The exact parameter distribution among the 99 positive labeled extensions
is

\[
\begin{array}{c|r|r}
(\gamma,\alpha,\gamma^\infty,\theta)&\text{labeled}&\text{canonical}\\ \hline
(1,3,3,3)&1&1\\
(2,3,3,3)&98&41.
\end{array}
\]

In particular, no positive extension has \(\gamma=3\).

## 3. One further local edge change

The base complement has 9 edges among its 9 vertices, leaving 27 old pairs
that can be added while preserving every literal edge of the lollipop core.
For each of these 27 choices, all 512 complement neighborhoods of the new
vertex were scanned.

\[
\begin{array}{l|r}
\text{quantity}&\text{count}\\ \hline
\text{labeled cases}&13,824\\
\text{canonical graphs}&2,099\\
\text{predicate-positive labeled cases}&718\\
\text{predicate-positive canonical graphs}&275.
\end{array}
\]

The positive-case parameter distribution is

\[
\begin{array}{c|r|r}
(\gamma,\alpha,\gamma^\infty,\theta)&\text{labeled}&\text{canonical}\\ \hline
(1,3,3,3)&8&5\\
(2,3,3,3)&710&270.
\end{array}
\]

Again, no positive case has \(\gamma=3\).

## 4. Verification

`explore.py` uses integer bitsets for exact domination, independence,
one-guard eternal kernels, and complement coloring.  It writes
`extensions.csv` and `summary.json`.

`explore_edge_additions.py` evaluates the second scope and writes
`edge_additions.csv` and `edge_additions_summary.json`.

`audit.py` is an independent ordinary-set replay of the critical negative
claim.  It imports no search logic, reconstructs both finite scopes with
frozensets, re-evaluates the safe-kernel/list-coloring predicate, and directly
finds a dominating singleton or pair in every positive case.  Its exact
replay counts are in `audit_result.json`.

The hostile review in
`reviews/separated_port_gamma3_extensions_hostile/` supplies a second
clean-room tuple/set implementation.  It replays every labeled case, every
positive witness count, all four parameters on every positive graph, and
the canonical class counts.  The bounded conclusion receives `PASS`.  We
retain the conservative `OBSERVED` label because this is a deliberately
local diagnostic rather than a counterexample-order exclusion or a general
graph-class theorem.

Run:

```text
python3 explore.py
python3 explore_edge_additions.py
python3 audit.py
```

Recorded data hashes:

```text
extensions.csv
b8a08bd73c9e6fc78ea3b8c170762091fe9ccd8854ff557bec7556bced059c00

edge_additions.csv
dbcbd9e1e1da7a0b47937321b68b3f1a043e2f1cc753e1cf344d912606c03a78
```

## 5. Mathematical interpretation and boundary

The original nine-vertex control showed that Boolean recurrence does not
identify two physical ports.  The present scan shows that simply adjoining
one arbitrary vertex does not repair its sole defect
\(\gamma=2<3\), even when one additional old graph edge is deleted and the
exact augmentation-sensitive eternal-family pattern survives.

This is precisely the behavior predicted by the strengthened proof target:
an equality-compatible minimal lollipop should either collapse to the
canonical attack geometry or yield a dominating pair.  Here the latter
alternative occurs in all 817 positive labeled cases across the two scopes.

What remains open is the unbounded step.  The scan gives no license to
contract longer connectors and does not show that two or more added
complement edges, more added vertices, or a different separated-port
expansion must still leave a dominating pair.
