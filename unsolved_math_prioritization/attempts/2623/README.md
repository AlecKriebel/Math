# Kourovka 21.114: audited scoped partial results

**Unsolved, 5/5 substantive approaches. No solution, novelty, or absolute-priority claim.** The accepted author v2 and independent exact-delta acceptance are controlling. This package preserves the original author and audit history unchanged.

For finite G put a(G)=|G/G′|. The target asks for an absolute derived-length bound when a(H)≤a(G) for every subgroup H≤G. A bound depending on the abelianization size, or unbounded nilpotency class alone, does not settle it.

## Read the work

- [Accepted v2 proofs](author/PROOFS.md), [five-approach log](author/RESEARCH_LOG.md), and [limitations](author/LIMITATIONS.md)
- [Original independent audit](audit/AUDIT_REPORT.md), [exact corrections](audit/CORRECTIONS.json), and [source caveats](audit/SOURCE_AUDIT.json)
- [Later exact-v2 acceptance](acceptance/ACCEPTANCE_REPORT.md) and [current verdict](VERDICT.json)

The partial results include quotient/direct-product reductions, necessary properties of minimal counterexamples, a parameter-dependent derived-length bound, a reconstruction of metabelian cyclic holomorphs, and obstructions to regular wreath products, full unitriangular groups and specified central-product padding. The imported Lisi–Sabatini nilpotency theorem remains an external dependency. Its boundaries and the source-proof caveats are preserved in the audit.

C1 identifies the equivalent question in the 22 March 2022 preprint *Weakly-top groups*, the earliest occurrence identified here, without asserting absolute priority. C2 changes left-coset terminology in prose and a docstring. No executable mathematical statement changed; functional ASTs match after docstring removal.

## Reproduction

From this directory, run `python3 verify_package.py`. It also works by absolute path from another directory or after relocating this whole folder. Only Python's standard library is needed.

The runner verifies the complete recursive publication inventory and hashes, four immutable ZIP archives against all extracted members, the original/v2 author manifests, original audit manifest, acceptance manifest, exact v1-to-v2 delta and patch, accepted author mathematics, and independent mathematics/results. It forces assertions on in all frozen checkers, including when the wrapper is invoked with `-O` or PYTHONOPTIMIZE.

The finite controls cover 11 groups, nine exhaustive subgroup lattices with 578 subgroups, 21,347,492 associativity triples, and 114 matching author/independent comparisons. Two further cases have exact disqualifying-subgroup certificates rather than full lattices. Finite checks support the authored arguments; they do not solve the uniform problem.

## Preserved history and boundary

`author_v1/`, `audit/`, `author/`, `acceptance/` and the adjacent files in `archives/` are byte-preserved frozen records. Historical “pending” and “no remote write” fields describe the time each was created. The later [acceptance](acceptance/ACCEPTANCE.json) supplies the current decision for exactly the v2 archive SHA-256 897360dd152d57c8d3ac10043fdb28b889e7206509eec56f6cb9a1dadbd71823. The acceptance archive SHA-256 is 59a71a8519620b34073a699d3bdb0e2b61bea5823fda48622d5cdf2fcae582cd.

Only the target queue row's Status and Turns are changed to unsolved and 5/5. Every other queue byte, including the preexisting stale header and blank Findings cell, is retained. No queue regeneration or extra proof attempt is included.

This draft contains authored work and public verification metadata only. No source PDFs, extracts, source images, raw datasets or private coordination files are included. No merge, release, DOI or outreach is part of this checkpoint.
