# Hostile review: separated-port gamma-three extensions

## Verdict

**PASS for the exact bounded claim.**

The search correctly proves the following finite statement:

> Among all 512 labeled one-vertex complement-neighborhood extensions of
> the fixed nine-vertex separated-port control, and among all
> \(27\cdot512=13{,}824\) cases formed by also adding exactly one previously
> absent complement edge between two old vertices, every graph satisfying
> the stated exact eternal-family/list-coloring predicate has
> \(\gamma\leq2\).

Thus none of these cases is a \(\gamma=\alpha=\gamma^\infty=3\) control.
This is bounded evidence only.  It proves neither the proposed unbounded
port-identification lemma nor the universal gamma-theta conjecture.

The sole editorial defect found in the first review pass was corrected:
the opening docstring of `explore_edge_additions.py` now agrees with the
code, assertion, output, and research note that the scope is
\(27\cdot2^9\).  The correction changes no executable logic or result.

## Audited target

The principal frozen files had these SHA-256 hashes:

```text
NOTE.md
8f4deb09e0290bbcd6317763704d1dba1040aef22bb56b5cba37ac2e7904bc34

explore.py
14254a041648ae0b18a1c0a9176deebb042ef0475c73977961ae90dab52913ed

explore_edge_additions.py
f17914967915eaa5cfe77536cc6ae7f7080222828763705d7fe1a4e2d2505da6

audit.py
a32bb758492716ce2e84d2ed8a2654e1c04620d3c15192ee7c4bc1e542901311

extensions.csv
b8a08bd73c9e6fc78ea3b8c170762091fe9ccd8854ff557bec7556bced059c00

edge_additions.csv
dbcbd9e1e1da7a0b47937321b68b3f1a043e2f1cc753e1cf344d912606c03a78
```

The note hash above is the final revision that records the two independent
replays and hostile PASS while conservatively retaining the local result as
`OBSERVED`.  That status-only revision changes neither the enumerated
predicate nor any count.

The clean-room checker and its result have hashes:

```text
independent_checker.py
cdef304a8c5bb57ae0d7ff007f172c63e540d138eb3e6c45be19bfece7ee387a

independent_result.json
b60e4947b234e138085bb28df792928d9f0ce0f53b058cb90e07e92887769009
```

## 1. Predicate reconstruction

Let \(H=\overline G\), let \(S=\{0,1,2\}\), and retain the nine base
complement edges

\[
01,02,12,34,45,56,68,78,47.
\]

For an eternal family \(\mathcal F\) of triples containing \(S\), the
family-response list at \(y\notin S\) is

\[
L_{\mathcal F,S}(y)
=
\{u\in S:uy\in E(G),\ S-u+y\in\mathcal F\}.
\]

The audited predicate requires the six old lists

\[
L(3)=012,\quad
L(4)=L(5)=L(6)=01,\quad
L(7)=L(8)=12,
\]

a nonempty proper list at the new vertex 9, a compatible list-coloring of
\(H-3\), and no compatible coloring after vertex 3 is fixed to anchor color
0.

The implementation's bans plus greatest-kernel test quantify over arbitrary
eternal subfamilies exactly.  Start with all dominating triples except the
direct swaps prescribed absent, and repeatedly delete a state having an
unoccupied attack with no one-guard adjacent successor still present.  The
stable set is the greatest closed family inside that allowed universe.
Every admissible family is contained in it by monotonicity.  Conversely, if
\(S\) and every prescribed positive direct swap survive, the stable set is
itself a witnessing eternal family with the required lists.

There is a subtle point when the extra complement edge meets an anchor.
It does not invalidate the equivalence.  Since \(S\) is independent in
\(G\), if \(S-u+y\) dominates then \(y\) must be adjacent to the removed
anchor \(u\); the other two anchors cannot dominate \(u\).  Hence membership
of a dominating direct-swap state already forces the required move edge.
The independent checker additionally reconstructed the actual legal
response lists from every positive kernel and asserted exact equality with
the prescribed lists.

## 2. One-guard semantics

Both the source and clean-room implementations use the model in the
campaign statement:

- every retained configuration is a dominating triple;
- attacks range only over vertices outside the current triple;
- exactly one occupied guard is replaced by the attacked vertex;
- that guard and attacked vertex must be adjacent in \(G\); and
- the resulting triple must remain in the family.

The calculations consistently build \(G\) as the simple complement of
\(H\).  The list-coloring calculation is performed in \(H\), as required
for clique partitions of \(G\).  Fixing colors \(0,1,2\) on \(S\) loses no
three-colorings because \(H[S]\) is a triangle.

No all-guards-move transition, occupied attack, nonedge move, or
\(G/H\) interchange was found.

## 3. Coverage

The first scope is exhaustive because the new vertex 9 has one independently
chosen complement adjacency bit to each of the nine old vertices.  The masks
\(0,\ldots,511\) are exactly all \(2^9=512\) labeled extensions.

Among the old vertices there are

\[
\binom92=36
\]

pairs.  Nine are already base complement edges, leaving exactly 27
previously absent pairs.  The second scope takes each one of those 27 pairs
and every one of the 512 new-vertex masks, giving 13,824 labeled cases.  The
checker verified the Cartesian-product keys against the two CSV manifests,
so there is no omitted or duplicate labeled case.

Here “one non-core complement edge” must be read narrowly as **adding one
previously absent \(H\)-edge among the old vertices**.  Equivalently, it
deletes one \(G\)-edge.  The result says nothing about removing a base
\(H\)-edge, changing two old edges, adding two vertices, or an arbitrary
larger separated-port expansion.

## 4. Independent replay

`independent_checker.py` imports none of the search modules.  It uses tuples,
ordinary sets, a separately written greatest-kernel deletion routine, and
separate backtracking colorers.  It checked every labeled instance and
matched the exact augmentation-sensitive witness count in every CSV row.

The replay obtained:

\[
\begin{array}{c|r|r}
\text{scope}&\text{cases}&\text{predicate-positive}\\ \hline
\text{one-vertex extensions}&512&99\\
\text{one added old }H\text{-edge}&13{,}824&718.
\end{array}
\]

It then computed all four parameters independently for every positive case:

\[
\begin{array}{c|r|r}
(\gamma,\alpha,\gamma^\infty,\theta)
&\text{extensions}&\text{edge additions}\\ \hline
(1,3,3,3)&1&8\\
(2,3,3,3)&98&710.
\end{array}
\]

Consequently every one of the 817 positive labeled cases has
\(\gamma\leq2\), and none has \(\gamma=3\).

As an ancillary check, a fresh `labelg` replay matched every recorded
canonical graph6 string and reproduced 160 and 2,099 total canonical
classes, with 42 and 275 positive classes respectively.  Canonicalization is
not needed for the decisive labeled coverage.

## 5. Claim boundary

This PASS supports a finite, template-restricted exclusion.  Its useful
mathematical content is that the smallest separated-port obstruction does
not become equality-valued after one arbitrary added vertex, even when one
additional old \(G\)-edge is deleted and the exact augmentation-sensitive
response-list pattern remains.

It does **not** establish any contraction or shortening principle for
longer connectors.  In particular, it does not rule out:

- two or more new vertices;
- two or more old-edge changes;
- a different response-list skeleton;
- a separated-port expansion not containing this labeled core; or
- any graph outside the enumerated finite templates.

Those limitations are stated accurately in the source note.
