# 10000062: local metric-ball homogeneity and periodicity

**Status: independently reviewed Euclidean partial result; full source unresolved.**

An explicit specialization of the known Frettlöh–Garber layered family has
congruent full vertex-centered balls of radius√10, all triangle diameters at
most√10, and no cocompact symmetry group. Its translation group is exactly
2Z×{0}: it still has a horizontal period.

The source does not define “periodic.” This result concerns the
cocompact/rank-two interpretation only, and does not settle its hyperbolic
clause. It must not be reported as a strongly aperiodic construction or an
unconditional full resolution. Prior-family attribution and novelty limits
are retained.

- [Complete candidate proof, including boundary faces](CANDIDATE.md)
- [Source and prior-art audit](SOURCES.md)
- [Exact verifier](verify.py) and [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl), [status](status.json)
- [Readiness/scope record](readiness.json), [pinned input](input_record.json)

Run `python3 verify.py`. Only Python's standard library is required.
Sixteen rooted cases cover all neighboring-layer assignments after the
analytic locality reduction. The checker includes edge pieces, face pieces,
and multiplicities of point-only boundary traces.

[Independent adversarial review](review/REVIEW.md) passed for the exact scoped result, with 212 additional exact assertions over 64 rooted cases. The proof is unchanged. Execution model: gpt-6-astra, xhigh.
No shared queue, catalog, or state files are changed.
