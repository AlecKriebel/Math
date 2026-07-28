# Audit of the resumed external AI report

Date: 2026-07-27 PDT

## Status

This file is a claim-by-claim intake audit.  The pasted report arrived
without source files, graph records, manifests, solver proofs, or checker
logs.  Nothing computational in it is promoted merely from prose.

## Useful statements that were already established

The following items agree with accepted campaign work but do not advance
the current frontier:

- the parameter chain and equality collapse: C-001--C-002;
- maximum independent configurations in every optimal eternal family:
  C-010;
- greatest-fixed-point deletion and finite losing attack trees: the two
  accepted evaluator specifications;
- component reduction: C-003;
- the absence of simplicial vertices in a minimum counterexample: C-048;
- the parameter-\(k\leq2\) theorem: accepted reductions and prior work;
- bipartite complement links of \((k-2)\)-cliques: C-051 and C-063;
- local response-list/2-SAT reduction at \(k=3\), including the full-list
  branch and the lollipop/bicycle trichotomy: C-073--C-075.

The report's certified-through-order-nine statement is strictly weaker
than C-050, which excludes counterexamples through order twelve relative
to the explicitly stated published through-order-eleven premise.

## Valid elementary reformulations

Let \(H=\overline G\).  The report states that
\(\gamma(G)=\alpha(G)=k\) is equivalent to

1. \(\omega(H)=k\); and
2. every \((k-1)\)-set \(X\) has a common \(H\)-neighbor outside \(X\).

This is correct.  The first condition is exactly \(\alpha(G)=k\).  A
\((k-1)\)-set \(X\) fails to dominate \(G\) exactly when some
\(v\notin X\) is nonadjacent in \(G\) to every member of \(X\), equivalently
complete in \(H\) to \(X\).  The maximum independent set supplies a
dominating \(k\)-set.  This is an elementary restatement of the static
constraints already used by the synthesis encodings, not a resolution.

For an isolate-free graph, the reported inequality
\[
  \gamma(G)\leq |V(G)|-\alpha(G)
\]
is also correct: the complement of a maximum independent set dominates.
The corresponding \(2k\leq n\) bound under equality is weaker than the
accepted counterexample bound \(n\geq2k+1\) in C-036 and, for a
minimum-order counterexample, the accepted C-049 bound
\(n\geq\lceil5k/2\rceil\).

The conclusion that the half-order case \(n=2k\) cannot be a
counterexample is already C-036.  The report's phrase that a maximum
independent set and its complement are “forced to be the two parts of a
balanced bipartite graph” is not valid as written: the complement of the
independent set need not itself be independent.  The conclusion remains
true by the classical half-order domination characterization used and
audited in C-036.  It can alternatively be derived from the perfect
matching theorem for very well-covered graphs.

## One usable new reduction

The report asserts that a minimum counterexample has no adjacent true
twins.  A fresh proof, independent of the prose report, is given in
`math/lemmas/adjacent_true_twin_reduction.md`.  Deleting one of a pair of
adjacent true twins preserves \(\gamma,\alpha,\theta\); under
\(\gamma=\gamma^\infty\), restricting an eternal family to configurations
avoiding the deleted twin gives an eternal family because a maximum
independent state guarantees nonemptiness.  An independent hostile review
accepted the universal proof and found zero failures among 6,279 twin-pair
incidences through connected order eight.  This is accepted claim C-078,
with no novelty or priority claim.

The report's forbidden complement configuration consisting of a
\((k-2)\)-clique completely joined to an induced odd cycle is not new: it
is exactly ruled out by the accepted bipartite-link conclusion of C-051.

## Computational statements not accepted

The claimed 15-vertex near-miss is identifiable from its numerical
fingerprint.  It is the already accepted Petersen member of C-060:
\[
  G=\overline{L(\mathrm{Petersen})}.
\]
The existing two-evaluator record has canonical graph6
`NzjEry{lz|Z{Z~nvZ~?`, parameters
\((\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,4)\), and exactly 395
dominating triples, all of which form the greatest eternal family.  Thus
this part of the imported report is correct but duplicates the accepted
parameterized line-graph theorem and its Petersen certificate.

No supporting artifacts were found in either research workspace for:

- the order-10--12 attack-horizon table;
- the 5,799, 5,005, 960, or 865 case counts;
- the depth-six survivor deleted at depth seven;
- the reported split trees, DRUP/LRAT proofs, or independent formula
  reconstruction; or
- the retracted augmentation branch with an unsorted-vector binary search.

The order-12 narrative is also obsolete relative to C-050: the campaign
has already certified the entire order-12 exclusion, including
\((12,3)\), rather than leaving that slice open.  These unsupported
computations will not be merged into `CLAIMS.md`.

## Proof routes retained or rejected

The proposed arbitrary-bicycle dichotomy

> every inclusion-minimal unsatisfiable response 2-CNF contains an already
> forbidden canonical attack configuration or yields a dominating pair

is a precise and useful conjectural target.  It matches the campaign's
current C-075 boundary.  It is not yet proved.

The warning against contracting a long connector solely from an omitted
family response is correct and important: absence from a family-response
list may reflect dynamic kernel failure rather than graph nonadjacency.

The “global facet holonomy” language is not retained as an independent
route.  C-060 and its hostile audit already show that local response
covariance and nontrivial global coloring obstruction can coexist with a
full one-guard eternal family when \(\gamma<\alpha\).  Any successful
argument must use the missing equality \(\gamma=\alpha\), not holonomy
alone.

Finally, proving the complete \(k=3\) case would be a major proper-class
theorem but would not automatically prove all parameters.  C-063 supplies
parameter-\((k-1)\) frozen projections only on restricted induced
subgraphs; a separate global gluing theorem would still be required.

## Follow-up generated by the intake

The useful warning about connector contraction led to three independently
checked advances rather than to acceptance of the imported theorem.

1. C-079 proves a literal one-guard attack theorem excluding every odd
   physical subdivision of the canonical one-unit lollipop when its two
   terminal clauses use one common complement port and its connector stays
   in one omitted-color projection.
2. C-080 gives an exact deletion/Kempe/augmented-2-SAT reduction for the
   unique-full-list branch of a minimum \(k=3\) counterexample.
3. C-081 refutes the automatic lift from a logical lollipop to the physical
   fan.  A clean-room-checked nine-vertex gamma-two family has separated
   physical ports, a minimally unsatisfiable augmented formula, and no fan
   embedding.  Because its domination number is two, the exact remaining
   question was whether \(\gamma=3\) forces port recurrence or a different
   contradiction.
4. C-082--C-083 answer the first layer of that question.  Every dynamic
   connector edge acquires a positive triangle cap, and the exact separated
   core forces an alternating cap-and-escape pair and an 11-vertex pattern
   floor.  The escape avoids immediate fan closure, so global iteration of
   the ladder remains open.

These outcomes materially narrow the prover target but do not prove the
\(k=3\) case or the universal conjecture.
