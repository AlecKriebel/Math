# Primary v1.1.0 proof-hardening report

Status at checkpoint `a121b4a8`: **READY FOR INDEPENDENT ADVERSARIAL REVIEW**.

This report records what the revision changed.  It is not the independent
release verdict.

## Mathematical repairs

1. The fixed-mixed-graph no-omnian equivalence is now a numbered lemma.  Its
   proof treats ordinary tails with two reticulation children, reticulation
   stacks, roots on ordinary edges, roots adjacent to retained edges, LSA
   validity, and the excluded bidirected root artifact.
2. Root reduction precedes the core theorem.  A hand proof identifies the
   unique incoming source, rules out a source at a theta pole, and derives the
   four source/sink event placements without a census.
3. A noncut-preserving compression lemma selects actual taxa, retains one
   complete repair and every path-sink child, and uses at most eight ports.
4. The two-active cut proof now uses a single central-normalized chart.  The
   four minors have explicit Fourier blocks, rows, columns, determinants, and
   exact algebraic identities.
5. Marginalization is justified by descriptor-product submersions and the
   constant-rank theorem on a dense regular source locus.
6. Projective peeling now states a local product chart, a finite
   semialgebraic-cover lemma, and a simultaneous physical-gluing lemma.  It
   claims normalized effective scales, not physical bridge recovery.
7. The machine boundary is one boxed finite decorated-relation theorem;
   primitive exhaustiveness, restoration, arbitrary words, localization, and
   gluing remain human arguments.

## Independent bounded checks added

- `verify_noncut_compression.py` independently covers every strong bounded
  two-colour occupancy on the five primitive cores and rejects duplicate,
  missing-repair, missing-sink, and singleton-colour mutations.
- `verify_endpoint_and_analytic_regressions.py` independently reconstructs
  the four cut minors, checks endpoint homogeneity, and rejects incorrect
  block, descriptor-partition, and boundary-rank mutations.
- The pre-existing standard-library zero-sum descriptor replay now locates
  its two historical failure witnesses by immutable content ID in the active
  graph inventory.  This repairs a missing-file packaging defect without
  changing either witness or the mathematical certificate.

## Exposition and release scope

- The unified positive classification, all-taxon Omega family, and all-taxon
  Theta family remain in one manuscript.
- Detailed finite-atlas counts moved to the supplement.
- The complete Theta target point and isolating interval are printed.
- Omega is explicitly binary, simple, stack-free, triangle-free, level two,
  weakly but not strongly tree-child, and distinguished from known results.
- Figure 4 was respaced; the printed author header contains no ORCID.  ORCID
  remains appropriate in submission metadata.

No theorem statement or network class was broadened in this revision.
