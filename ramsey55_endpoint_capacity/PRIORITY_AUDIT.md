# Focused priority and scope audit

Audit date: **24 July 2026**.

This is a bounded primary-source review, not proof of worldwide priority.
Unindexed code, unpublished filters, and differently phrased antecedents may
exist.

## Bottom line

The review found a **positive but moderate novelty signal**.

No reviewed source contains the exact profile inequality

    sum_b q_(d_H(b)-5)(A) <= 4 i_3(A),

its equality-rigidity argument, or the exclusion of the regular degree-18
endpoint `(e(A),e(H))=(85,128)`.

The ingredients are not wholly new. The two-column covering condition is the
classical \(E_2\) feasible-cone constraint; the one-column condition is its
immediate forbidden-set analogue. The summation step is elementary incidence
double counting.

The defensible candidate contribution is:

1. the exact minimum-miss profile `q_s(A)` over fixed-size transversals;
2. its aggregate use across graph-indexed cross-neighborhood columns;
3. equality forcing through a unique size-six minimizer; and
4. the resulting complete endpoint exclusion with a compact verifier.

## Closest prior art

- McKay and Radziszowski, *R(4,5)=25*, Journal of Graph Theory 19
  (1995), 309-322. Their `E_2` feasible-cone condition is the direct
  antecedent of the two-column rule. The one-column rule is its immediate
  forbidden-set analogue but is not explicitly listed there because that case
  is vacuous in their setup.
- McKay and Radziszowski, *Linear Programming in Some Ramsey Problems*,
  Journal of Combinatorial Theory B 61 (1994), 125-132. This is an earlier
  aggregation and linear-programming antecedent.
- McKay and Radziszowski, *Subgraph Counting Identities and Ramsey Numbers*,
  Journal of Combinatorial Theory B 69 (1997), 193-209. This supplies global
  neighborhood-count identities and size-aware propagation antecedents.
- Angeltveit and McKay, *R(5,5) <= 48*, Journal of Graph Theory 89
  (2018), 5-13, completes the extremal `R(4,5)` catalog and uses large gluing
  computations.
- Angeltveit and McKay, *R(5,5) <= 46*, Journal of Graph Theory 112
  (2026), 198-208, uses catalog generation, linear programming, and extensive
  gluing. It does not state the present endpoint theorem.
- Gauthier and Brown, *A Formal Proof of R(4,5)=25*, ITP 2024, formalizes
  catalog gluing and SAT-based covering in HOL4 but does not introduce the
  minimum-miss capacity profile.

## Permitted language

Safe wording:

> We formulate a minimum-miss capacity profile for feasible
> cross-neighborhoods and use an elementary incidence bound, together with
> equality rigidity, to exclude the regular degree-18 endpoint
> `(e(A),e(H))=(85,128)`.

Avoid:

- claiming a new general double-counting principle;
- claiming invention of feasible-cone or two-column covering constraints;
- claiming the first use of hypergraph transversals in Ramsey computation;
- claiming a new bound for `R(5,5)`; or
- claiming unconditional priority.

## Publication assessment

The abstract lemma alone is too elementary for a standalone paper. The
capacity profile, catalog-conditional endpoint theorem, equality-rigidity
argument, pinned inputs, and independent verifier form a defensible short
computational-combinatorics note.

The theorem remains narrow. A stronger journal paper would likely require a
weighted or correlated multi-column refinement that closes another complete
layer or global branch.
