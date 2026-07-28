# Hostile certification review: order-13 full-response branch

Date: 2026-07-27 PDT

## Verdict

**PASS — CERTIFIED-FINITE, with the branch boundary stated below.**

The frozen CNF, its coverage argument, and its RUP proof jointly certify:

> **Order-13 full-response exclusion.** There is no graph \(G\) on 13
> vertices, eternal family \(\mathcal F\) of triples, maximum independent
> triple \(S\in\mathcal F\), and vertex \(x\notin S\) with full
> family-response list \(L_S^{\mathcal F}(x)=S\), such that
> \[
> \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G).
> \]

The full target is not assumed unique. Connectivity is not assumed. The
formula does not use the five- or six-witness bound, does not force all
maximum independent triples into the represented family, and does not use an
odd-hole template.

This does **not** exclude an order-13 counterexample for which every
family-response list at every maximum independent triple has size at most
two. It does not raise the unconditional finite frontier past order 12 and
does not resolve the universal conjecture.

## Independence of this review

The review checker in this directory does not import the discovery
`search.py`. It allocates the four variable families anew and reconstructs
each clause family directly from the graph and one-guard definitions. Its
output is byte-for-byte identical to the frozen 4,808,845-byte DIMACS file:

```text
variables  9,802
clauses   85,409
SHA-256   d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13
```

This stronger comparison subsumes a normalized clause-multiset comparison.
The reduced 11,846-clause input is also a multiplicity-respecting
submultiset of the independently reconstructed formula.

## Coverage proof

Suppose a graph and family satisfying the displayed theorem existed.

1. Relabel the maximum independent triple as
   \(S=\{0,1,2\}\), and relabel the specified full target as \(x=3\).
   This is legitimate because the theorem assumes a full-response incidence,
   not a canonical or unique vertex. The remaining nine vertices remain
   freely permutable.
2. Let each edge variable represent an edge of \(H=\overline G\). Since
   \(\alpha(G)=3\), \(H\) contains no \(K_4\). Since \(\gamma(G)=3\), every
   two-set fails to dominate \(G\), so it has an outside common neighbor in
   \(H\); choose one corresponding witness variable.
3. Set \(f_D\) true exactly for \(D\in\mathcal F\). Every such \(D\)
   dominates. For each unoccupied attack \(r\notin D\), eternal closure
   supplies one guard \(u\in D\) with \(ur\in E(G)\) and retained successor
   \((D-\{u\})\cup\{r\}\); set the corresponding response variable true.
   All other response variables may be false.
4. The fixed anchor units say that \(S\) is an \(H\)-triangle and is
   retained. Fullness at \(x\) gives all three \(G\)-edges from \(x\) to
   \(S\) and all three retained one-guard successors.
5. Because \(\theta(G)=\chi(H)>3\), the complete anchored coloring bank is
   satisfied. In any proper 3-coloring of \(H\), the anchor triangle uses
   three different colors; permuting color names makes these \(0,1,2\).
   The bank contains all \(3^{10}=59{,}049\) assignments on the remaining
   vertices and blocks each by requiring a monochromatic \(H\)-edge.
6. Finally permute vertices \(4,\ldots,12\) to put their four-bit
   \(H\)-adjacency signatures to \(0,1,2,3\) in nondecreasing order.
   Every nonsorter clause family is covariant under this \(S_9\): witness,
   family, and response variables are transported along with vertices, and
   the complete coloring bank is invariant as a set. Thus every unrestricted
   object has a sorted representative.

The checker exhaustively evaluated all \(8\cdot16^2=2{,}048\) local
signature pairs. Each 120-clause comparator block accepts exactly
\(\sigma(v)\leq\sigma(v+1)\), including ties. Hence the sorter omits no
isomorphism orbit.

Conversely, any satisfying assignment gives an \(H\)-triangle \(S\), no
\(H\)-\(K_4\), a dominating retained \(S\), no dominating pair, a nonempty
literal one-guard eternal family of triples, a full target \(x\), and a
non-3-colorable \(H\). Therefore
\[
\gamma=\alpha=\gamma^\infty=3<\theta.
\]
The encoding is exact for the stated labeled branch.

## One-guard model audit

The closure bank contains obligations only for \(r\notin D\). Each response
variable names one occupied guard \(u\in D\), and its two implications
require:

- \(ur\notin E(H)\), equivalently the guard traverses the one graph edge
  \(ur\in E(G)\); and
- the unique successor \((D-\{u\})\cup\{r\}\) is retained.

The separate selected-state clauses force every retained successor to
dominate. The encoding does not move multiple guards, does not attack an
occupied vertex, and never substitutes an \(H\)-edge for a \(G\)-edge.
Multiple response variables may be true, which correctly represents several
available one-guard choices rather than a simultaneous move.

The clique-cover direction is also correct:
\(\theta(G)=\chi(\overline G)=\chi(H)\), and the bank proves
\(\chi(H)>3\), not a coloring statement about \(G\).

## Proof binding and replay

The pinned checker is
`tools/drat_trim_2023_05_22/drat-trim`, executable SHA-256
`31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`.
The full proof was replayed against the independently regenerated,
byte-identical DIMACS file with `-U`:

```text
c 11846 of 85409 clauses in core
c 8277 of 123053 lemmas in core using 485709 resolution steps
c 0 RAT lemmas in core; 3558 redundant literals in core lemmas
s VERIFIED
```

The retained reduced pair was replayed separately:

```text
c 11343 of 11846 clauses in core
c 8036 of 8278 lemmas in core using 479565 resolution steps
c 0 RAT lemmas in core; 1181 redundant literals in core lemmas
s VERIFIED
```

Thus both proofs pass in RUP-only mode. The decisive hashes are:

| artifact | SHA-256 |
|---|---|
| `minimal-instance.cnf` | `d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13` |
| `minimal-proof.drat` | `653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910` |
| `minimal-core.cnf` | `dcba47ea9d60afc1cc86672498af39681c3acf02606c728f66cb84f47ee557e7` |
| `minimal-core.drat` | `83f73ee2c2a82ab0a228099f0354abf46e23f3e807561a6d665a43b86b1e273f` |

Exact replay commands and complete outputs are in
`proof_replay_full.log` and `proof_replay_core.log`.

The checker executes the full proof replay, reduced proof replay, and
closure-ablation solve twice before writing any evidence. It requires the
two normalized rounds to be byte-identical. Serialized commands use stable
campaign-relative paths or named clean-room placeholders; random temporary
paths are never serialized, and the checker's volatile wall-clock lines are
replaced by an explicit timing-omitted marker. Consequently `result.json`
and all three logs are byte-stable across complete reruns.

## Positive controls and ablations

The retained SAT assignment for the independently reconstructed formula
without the 59,049 coloring clauses satisfies every one of its 26,360
clauses. A separate exact graph evaluator recovered

```text
Graph6: LF\|ul\XzVsaqJ
(gamma, alpha, gamma-infinity, theta) = (3,3,3,3)
```

It found 157 dominating triples, and independent greatest-fixed-point
deletion retained all 157. The represented SAT family also contains all 157.
At \(S=\{0,1,2\}\), vertex 3 is the unique full target in that greatest
family. An explicit proper 3-coloring of \(H\) was recovered. This is a
genuine positive equality control, not a counterexample.

A newly generated minimal formula with the entire one-guard closure bank
removed has 65,389 clauses and is SAT. Therefore neither the fixed
full-response incidence nor the static parameter clauses alone caused the
decisive contradiction. The old unsorted 120-second timeout remains a
nonclaim. Earlier strengthened-formula ablations not retained as decisive
artifacts are not used in this verdict.

## Human six-witness and cross-response review

The proofs in both
`math/working/order13_single_full_squeeze/NOTE.md` and
`math/working/full_response_disjoint_witnesses/NOTE.md` pass.

For \(p\in A_i=N_H(x)\cap N_H(i)\), domination of the two direct
full-response states omitting the other anchors gives
\(N_H(p)\cap S=\{i\}\). For
\(y\in Y_{i,p}=N_H(i)\cap N_H(p)\), suppose \(y\) also misses another
anchor \(j\). Attack \(y\) from the direct state containing \(i\), the third
anchor, and \(x\). Guard \(i\) has no graph edge to \(y\); moving the third
anchor leaves a triple missing \(p\); moving \(x\) leaves a triple missing
\(j\). This contradiction proves
\[
N_H(y)\cap S=\{i\}.
\]

Equivalently, if one vertex lay in external layers for two anchors, the same
literal attack has no legal dominating successor. Hence the three chosen
external witness layers are pairwise disjoint. Repeating the attack with
only one anchor nonadjacency also forces \(xy\in E(G)\) and both
cross-anchor successor states into the family. Consequently the three
spokes and three external witnesses are six distinct vertices outside
\(S\cup Q_S\), proving
\[
|V(G)-(S\cup Q_S)|\geq6,\qquad |V(G)|\geq |Q_S|+9.
\]

For the exact separated-port core, six named vertices lie in \(Q_S\), so
the corrected floor is \(n\geq15\). The earlier five-witness \(n\geq14\)
bound remains true but is superseded for that exact core.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error reviews/order13_full_target_hostile/checker.py
```

The command reconstructs and binds the formula, checks the positive control,
truth-tables the sorter, replays both proofs twice, reruns and checks the
closure ablation twice, asserts identical normalized rounds, and rewrites
`result.json` and the three deterministic logs.
