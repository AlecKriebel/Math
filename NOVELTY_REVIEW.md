# Focused novelty review

Review date: 2026-07-24

## Verdict

The review found a **positive but moderate novelty signal**.

No reviewed source contains the exact profile inequality

\[
\sum_{b\in V(H)}q_{d_H(b)-5}(A)\le4i_3(A),
\]

its equality-rigidity argument, or the exclusion of the regular degree-18
endpoint \((e(A),e(H))=(85,128)\).

The ingredients are not wholly new. The one- and two-column covering
conditions are classical feasible-cone gluing constraints, and the summation
step is elementary incidence double counting. The defensible contribution is
the **minimum-miss profile \(q_s(A)\), its aggregate use across graph-indexed
columns, and the equality rigidity that closes the endpoint**.

This was a focused primary-source review, not a proof of global priority.
Unindexed code, unpublished filters, or differently phrased antecedents may
exist.

## Classification

| Result or ingredient | Assessment |
|---|---|
| A column hits every independent four-set | Exact prior analogue in feasible-cone gluing |
| Two columns on an appropriate edge jointly hit every independent triple | Exact prior analogue after complement/orientation translation |
| Minimum-miss profile \(q_s(A)\) over exact-size transversals | No exact match found |
| Aggregate comparison with \(4i_3(A)\) | No exact match found; generic double-counting antecedent |
| Equality forcing through a unique size-six minimizer | No exact match found; close size-aware collapsing analogues |
| Exclusion of all 62,382 pairs at \((85,128)\) | No prior evidence found; strongest novelty candidate |
| Fixed weighted version \(q_s^w\) | Immediate extension; not priority-safe as a novelty claim |

## Closest prior art

### Feasible-cone gluing

McKay and Radziszowski's
[\(R(4,5)=25\)](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
([DOI](https://doi.org/10.1002/jgt.3190190304)), J. Graph Theory 19
(1995), 309–322, defines feasible cones and requires that unions of cones
indexed by independent sets not miss the complementary forbidden set. Its
\(t=2\) condition is the direct ancestor of the present two-column
independent-triple condition. The one-column independent-four-set condition
is likewise part of the extension framework.

The formal reconstruction by Gauthier and Brown,
[A Formal Proof of \(R(4,5)=25\)](https://arxiv.org/abs/2404.01761),
formalizes catalog gluing using SAT and generalization covers. It does not
introduce a capacity profile or aggregate missed-set inequality.

### Subgraph counting and size-aware propagation

McKay and Radziszowski,
[Subgraph Counting Identities and Ramsey Numbers](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)
([DOI](https://doi.org/10.1006/jctb.1996.1741)), J. Combin. Theory B 69
(1997), 193–209, supplies two close but distinct antecedents:

- global identities obtained by summing neighborhood and
  complementary-neighborhood subgraph counts;
- size-aware feasible-cone collapsing rules.

Those methods do not minimize a missed-set penalty over exact-size
cross-neighborhoods, sum the resulting profiles against the independence
capacity of the indexing graph, or contain the present equality argument.

Earlier global counting and linear-programming antecedents include:

- McKay and Radziszowski,
  [A New Upper Bound for the Ramsey Number \(R(5,5)\)](https://repository.rit.edu/article/645/),
  Australasian J. Combin. 5 (1992), 13–20;
- McKay and Radziszowski,
  [Linear Programming in Some Ramsey Problems](https://www.cs.rit.edu/~spr/PUBL/paper29.pdf)
  ([DOI](https://doi.org/10.1006/jctb.1994.1038)), J. Combin. Theory B 61
  (1994), 125–132.

They aggregate classified local contributions but, in the sources reviewed,
do not use the present minimum-miss transversal profile.

### Current \(R(5,5)\) computations

Angeltveit and McKay's
[\(R(5,5)\le48\)](https://arxiv.org/abs/1703.08768)
([DOI](https://doi.org/10.1002/jgt.22235)) completed the extremal
\(R(4,5)\) catalog and used large gluing computations.

Their current
[\(R(5,5)\le46\)](https://arxiv.org/abs/2409.15709)
([journal DOI](https://doi.org/10.1002/jgt.70029)) uses linear programming,
catalog generation, and extensive gluing. It records the relevant edge-128
order-24 catalog layer but does not state the paired endpoint theorem or the
capacity inequality.

McKay's
[Ramsey graph data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
publishes the complete order-24 and extreme smaller-order catalogs. It
contains no theorem excluding the \((85,128)\) pairing.

Angeltveit's
[An exact value for \(R(K_5,K_{5-e})\)](https://arxiv.org/abs/2602.11459)
is a recent descendant of the feasible-cone method, again using extenders,
local collapsing, and SAT. No aggregate minimum-miss capacity construction
was found there.

Targeted searches for the pair \((85,128)\), the counts 62,382 and 61,939,
and the notation \(q_s(A)\) found no relevant primary-source match.

## Safe novelty statement

> We introduce a minimum-miss capacity profile for feasible
> cross-neighborhoods and use an elementary incidence bound, together with
> equality rigidity, to exclude the regular-degree-18 endpoint
> \((e(A),e(H))=(85,128)\).

The following claims would overstate the evidence:

- a new general double-counting principle;
- invention of the one- or two-column covering constraints;
- the first use of hypergraph transversals in Ramsey computation;
- unconditional priority over unpublished work.

## Publication assessment

The abstract lemma alone is probably too elementary for a standalone paper.
The credible short-note unit is:

1. the capacity-profile lemma;
2. explicit attribution of classical feasible-cone constraints;
3. the catalog-conditional endpoint theorem;
4. the unique-minimizer equality argument;
5. pinned inputs and an independent compact verifier.

The endpoint theorem appears new within this review, but it is narrow and
does not improve the bound on \(R(5,5)\). A short computational-combinatorics
note is plausible. A stronger paper would likely require a weighted or
correlated multi-column refinement that closes another layer.
