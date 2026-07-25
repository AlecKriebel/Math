# Hostile review: one-vertex-extension kill-test scope

## Verdict

**ACCEPTED as a mathematically complete cover of the stated universe of
connected one-vertex extensions of the 55 MMV near-miss hosts, and ACCEPTED
as an exact counterexample test within that universe.**

This is not yet a certified negative finite result: after the full run, a
separate coverage audit must check the origin manifest and the
raw-to-canonical isomorphism claims.  That is an artifact requirement, not a
defect in the mathematical reduction.

No critical, high-, or medium-severity mathematical error was found.  Two
publication/certification corrections are listed below.

Review date: 2026-07-25.

Reviewed artifacts and SHA-256 digests:

- `math/extension_search_scope.md`:
  `252faa90b377fce52efb0daf5235f1f73aae81d2b0028103703ebec199a36cb0`;
- `instances/mmv2022_table9.csv`:
  `801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d`;
- `results/mmv2022_parameters.csv`:
  `ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6`;
- `src/search/extension_killtest.py`:
  `3fbc4a11b86925ec34aa08a76299c9c1e73d903be1b31fa50479425fdf1a64a0`;
- `tests/test_extension_killtest.py`:
  `b0ffca8441f3d73e50b08afdefc7bd532f6974099aa6514602a224a33609e9e2`.

## Independent catalog cross-check

The catalog and parameter files each contain 56 records.  Their catalog IDs
and Graph6 strings agree row-for-row, and both the IDs and Graph6 strings are
unique.

Exactly one record, `MMV-003` (`JQyurj]yt|?`), is outside the host universe
because its parameter tuple is

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,2,3,4).
\]

The other 55 records all satisfy

\[
\alpha(H)=\gamma^\infty(H)=3<4=\theta(H).
\]

Their independently recounted distribution is:

| order | \(\gamma(H)\) | number |
|---:|---:|---:|
| 10 | 2 | 2 |
| 11 | 2 | 51 |
| 11 | 1 | 2 |

A separate direct Graph6 connectivity traversal found all 55 selected hosts
connected.  The two domination-one hosts are `MMV-024` and `MMV-047`.

## Coverage proof audit

Fix one selected labeled host \(H\) and a new vertex \(x\).  Any simple
one-vertex extension in which the old vertices induce \(H\) is determined
uniquely by \(N_G(x)\subseteq V(H)\): the old-old edges are fixed, and the
new-old edges are exactly the members of that subset.  Since \(H\) is
connected, the extension is connected exactly when this subset is nonempty.
Thus the masks

\[
1,\ldots,2^{|V(H)|}-1
\]

are a complete labeled cover, with neither a missing extension nor a
duplicate for a fixed labeled host.

The arithmetic in the scope note is exact:

\[
\begin{aligned}
2(2^{10}-1)+53(2^{11}-1)&=110{,}537,\\
2(2^{11}-1)&=4{,}094,\\
2(2^{10}-1)+51(2^{11}-1)&=106{,}443.
\end{aligned}
\]

The last line is the decisive universe after the two domination-one hosts
are pruned.  The 4,094 pruned extensions cannot be counterexamples: if
\(\gamma(H)=1\), adjoining \(x\) to a dominating set of \(H\) proves
\(\gamma(G)\leq2\), whereas the inherited independent 3-set gives
\(\alpha(G)\geq3\), and every counterexample has
\(\gamma(G)=\alpha(G)\).

The 55 empty-neighborhood masks are correctly outside the *connected*
extension universe.  Any eventual finite-result statement should retain the
word “connected.”  Alternatively, the omitted disconnected cases can be
disposed of directly by additivity:

\[
\gamma(H\mathbin{\dot\cup}K_1)=\gamma(H)+1
<\gamma^\infty(H)+1
=\gamma^\infty(H\mathbin{\dot\cup}K_1).
\]

## Parameter monotonicity audit

Both inherited lower bounds are sound but use different elementary
arguments:

- an independent 3-set of the induced subgraph \(H\) remains independent in
  \(G\), so \(\alpha(G)\geq3\);
- every clique partition of \(G\), restricted to \(V(H)\) and with empty
  parts deleted, is a clique partition of \(H\), so
  \(\theta(G)\geq\theta(H)=4\).

If \(D\) is a minimum dominating set of \(H\), then \(D\cup\{x\}\) dominates
all of \(G\), including \(x\).  Hence

\[
\gamma(G)\leq\gamma(H)+1.
\]

For the 53 decisive hosts this gives \(\gamma(G)\leq3\).  Adding one vertex
also gives the unused but correctly enforced implementation invariant
\(\alpha(G)\leq\alpha(H)+1=4\).

## Audit of the three-condition equivalence

For an extension of a domination-two host, the three conditions in the note
are sufficient:

1. no dominating 2-set, together with \(\gamma(G)\leq3\), gives
   \(\gamma(G)=3\).  A dominating singleton would extend to a dominating
   pair, so “no pair” also excludes \(\gamma=1\);
2. the inherited independent 3-set and absence of an independent 4-set give
   \(\alpha(G)=3\); any larger independent set would contain a 4-set;
3. a one-guard eternal family of 3-sets gives
   \(\gamma^\infty(G)\leq3\), while
   \(\alpha(G)\leq\gamma^\infty(G)\) gives the reverse inequality.

Together with \(\theta(G)\geq4\), these imply

\[
\gamma(G)=\gamma^\infty(G)=3<\theta(G),
\]

and \(\gamma\leq i\leq\alpha\) gives \(i(G)=3\).

They are also necessary.  If such an extension is a counterexample, equality
collapse gives

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G).
\]

The inherited \(\alpha(G)\geq3\) and the extension bound
\(\gamma(G)\leq3\) force every displayed parameter to equal 3.  Conditions
1--3 follow immediately.

The implementation applies exactly these tests: it computes exact
\(\gamma\) and \(\alpha\), stops before the eternal-game solvers unless both
equal 3, and then requires agreement of two independent size-3 eternal-family
decisions.  All five extension-specific unit tests passed in this review,
including the bounded resume/dedup test.

## Canonicalization and deduplication audit

At the mathematical level, replacing each graph by an isomorphic canonical
representative is sound because all tested parameters and the
counterexample property are isomorphism invariant.  Global deduplication is
also sound even across different hosts: one retained representative is
enough, while origin multiplicities preserve coverage provenance.

The implementation deduplicates by the full canonical Graph6 string as a
SQLite primary key, not by a cryptographic digest, so hash collisions cannot
silently merge cases.  It retains a separate origin row for every
`(host_id, neighborhood_mask)` and advances the next mask in the same
transaction.  This is the right resumability invariant.

For a certificate-backed empty result, however, trusting that `labelg`
preserved order and edge count is not by itself a proof that each output is
isomorphic to its input.  The independent post-run coverage audit must
verify all of the following:

1. for every host, the origin masks are exactly the integer interval
   \(1,\ldots,2^{|V(H)|}-1\), with no gap or repetition;
2. the total number of origin rows and the sum of canonical origin
   multiplicities are both 110,537;
3. every stored raw Graph6 record reconstructs from its recorded host and
   mask;
4. every raw record is isomorphic to its stored canonical record, checked
   independently of the search's `labelg` call;
5. every unique canonical record has exactly one stored exact evaluation,
   and the category totals sum to the number of unique records.

The stored canonical-stream hashes and output-file hashes bind the audit
artifacts, but do not replace these checks.

## Exact corrections

1. **Low, proof exposition:** the scope note's paragraph beginning “Indeed”
   explicitly proves only the sufficient direction of its “if and only if.”
   Add the necessity argument above: equality collapse, inherited
   \(\alpha\geq3\), and \(\gamma\leq3\) force the common value to be 3.

2. **Certification gate, not a mathematical flaw:** qualify the statement
   that canonicalization “remove[s] only isomorphic copies” by citing the
   pinned canonical-labeling procedure, and require the independent
   five-part post-run coverage audit above before labeling an empty run
   `CERTIFIED-FINITE`.

Subject to those presentation and artifact requirements, the finite-universe
reduction and exact candidate criterion survive hostile review.
