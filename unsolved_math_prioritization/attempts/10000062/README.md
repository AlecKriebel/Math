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
The exact original PR changes these16 attempt files and the selected QUEUE.md row from queued0/5 to unsolved1/5. Current acceptance also records the program audit and a present accepted-state mirror after verified remote integration; the original1/5 is preserved. Historical scope/model statements are archived, not rewritten as current attestations.

Current complete family/root audit PASS: full-ball geometry, all ambient symmetry classes and exact primary/prior scope checked. Root original16-case and212-assertion receipts reproduce byte identically; fresh family controls1398/888/158 pass. NEW complete adversary and root107 fresh controls PASS for the exact corrected package. Remote acceptance is verified; the parent records the present accepted-state mirror separately. See CURRENT_AUDIT_SCOPE.md; no paper, deposit/DOI or tracker row.
