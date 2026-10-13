# Two low-multiplicity distances: audited scoped partial results

**ID 30006556 / OWR-14299905-031, rank 774: unsolved, 5/5 approaches. No full-solution, novelty, or priority claim.**

For n>4 distinct planar points, the target asks for two distinct occurring distances, each determined by at most n unordered pairs. The first part of EP-132 / ID 1949 is equivalent once its contextual n>=5 condition is restored; its additional diverging-number assertion is outside this target and remains unresolved here.

The strongest authored partial is Theorem 4: for every n>=5, the conclusion holds if at least n-1 points are cocircular. The independent audit passes this all-n proof without mathematical repairs. Other results include a collinear-subset criterion, a credited CDL hull-layer corollary, and an exact 61-point specialization of CDL's obstruction to using just the minimum and second-largest distances. That construction is a candidate-selection countercontrol, not a counterexample to the problem.

## Read in context

- [Publication audit addendum](AUDIT_ADDENDUM.md) and [current verdict](VERDICT.json)
- [Frozen authored proofs](author/PROOFS.md), [five-approach research log](author/RESEARCH_LOG.md), and [limitations](author/LIMITATIONS.md)
- [Complete independent proof audit](audit/AUDIT.md), including corrections in section 6, and [independent source verification](audit/SOURCE_AUDIT.json)

The CDL journal title is singular, *On multiplicities of interpoint distance*; the arXiv title is plural. The external Zeraoulia working draft contains a false graph lemma, independently counterchecked here, and is not a dependency of the circle theorem. Its n=7 classification input and n=8 reduction are not established by this package.

## Reproduce

Run `python3 verify_package.py` from this directory, or use its absolute path from another working directory. Python 3 and its standard library suffice. The runner verifies the complete recursive inventory, byte hashes, both ZIP archives and every extracted member, frozen author/audit manifests, and both mathematical result streams byte for byte. It launches the frozen checkers with assertions active even if the wrapper is invoked with `-O` or `PYTHONOPTIMIZE`.

The independent finite controls cover 30,827 grid subsets, 186,053 circle/outlier configurations, 63,019 cyclic subsets, exact center/moment controls, an exact rational-interval/modular-index certificate for the 61-point example, and the external graph-lemma countercontrol. These support the separately audited proof; they do not classify all planar sets or establish novelty.

## Preserved history

The `author/`, `audit/` and `archives/` files preserve both original freezes exactly. The author's historical “audit pending” statements and both receipts' “no remote writes” statements refer to the times those records were frozen. The later independent audit and publication addendum supply the present assessment. The publication manifest excludes itself; its exact bytes are externally bound by the Git commit and remote verification receipt.

Only the target queue row's Status and Turns change to unsolved and 5/5. Every other queue byte, including the existing stale header and blank Findings cell, is retained. There is no new proof-search turn in this publication checkpoint.

This draft includes authored work and public verification metadata only. Source PDFs, source text extracts, source images, raw datasets, selected source records and private coordination are excluded. No merge, release, DOI or outreach is part of this publication.
