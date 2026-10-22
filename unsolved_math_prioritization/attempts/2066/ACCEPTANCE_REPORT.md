# Acceptance report for Erdős Problem 348

## Publication edition and historical evidence

This AI-assisted, unrefereed publication edition preserves the complete substantive
mathematical audit and credits the existing Geneson theorem. No mathematical
correction is required. Acceptance is bounded to eventual completeness and deletion
of indexed occurrences. No novelty, human review, journal acceptance or formal
proof-assistant verification is claimed.

Source retrievals, visual inspections and finite diagnostics described below are
historical records of the accepted audit on 10 October 2026. Edition preparation
performed no new scholarly-source retrieval or inspection and no new mathematical
test execution. This is a prose-only edition: diagnostic programs and raw results
are omitted. The general theorem rests on the complete written argument, not on
finite samples. Public source identities and recorded inspection limits are in
`PUBLIC_SOURCES.json`; public status history and retrieval metadata are in
`FORMAL_HISTORY.json` and `RETRIEVAL_HISTORY.json`.

**Verdict:** accept the existing proof of Theorem 1 in Jesse Geneson, *Deletion thresholds and exponential examples for complete sequences*, [arXiv:2609.25107v1](https://arxiv.org/pdf/2609.25107v1), within the scope below. No repair was required by this audit.

For $0\leq m<n$, a nondecreasing integer sequence that remains eventually complete after every $m$-occurrence deletion and becomes incomplete after every $n$-occurrence deletion exists exactly for $m\leq1$.

The full reconstruction is in `MATHEMATICAL_AUDIT.md`. It checks:

- The original eventual-completeness and indexed-occurrence conventions against the 1980 book and Graham's 1971 question.
- The complete central-interval proof, including repeated-value normalization, the two transitions, divergence of the output cuts, and the finite-potential contradiction on PDF pages 6–11.
- Divergent prefix slack after fixed finite deletions, the long-gap lemma, and the existential extension of a successful deletion.
- The reduction from bounded or signed integer sequences to the positive case.
- Binary and Fibonacci witnesses, all finite deletion sizes, both initial Fibonacci ones, and the zero-based-indexing issue.

The delicate quantifier is preserved: each deletion may have its own eventual-completeness threshold. Pair tolerance implies the existence of a successful deletion of any prescribed finite size; the proof does not claim every finite deletion succeeds. The pair producing long gaps may depend on the required gap length, but remains fixed while the gaps occur arbitrarily far out.

The full version-pinned manuscript was retrieved again and exactly matches the screened source: 423,382 bytes; SHA-256 `9060ebcc3812b9a33bf08cc8dbdf6b5c8714acda2f54ed4ecfca7c152cb8dcc2`. It is a 14-page preprint submitted 20 September 2026. Theorem 1 and its dependencies occupy pages 1–11. Relevant original question pages and all central-proof pages were visually checked as well as text-read.

## Source status reconciliation

The dated August 2026 open assessment predates this September manuscript. A current [Formal Conjectures update](https://github.com/google-deepmind/formal-conjectures/commit/97a729a35de6de358570f9b5d820d6effb11bd43), dated 8 October 2026, records the same answer and cites Geneson. A stale indexed web copy still showed the earlier open statement. The fresh raw file and version-pinned GitHub file agree on the updated source status.

The Formal Conjectures theorem remains `sorry`-backed. Its successful statement build, if cited, is not a Lean proof of the theorem. The earlier [13 September occurrence-convention correction](https://github.com/google-deepmind/formal-conjectures/commit/cd220bc5e26f620517cc031ddf7ab1b6bf5aa12d) is also material: a set of distinct values would lose multiplicities and would not express the target problem.

The author’s separate claims about exponential sequences are not part of this acceptance. The original base-2 Problem 354 remains outside this result. The manuscript's title and abstract alone were not used as mathematical acceptance evidence.

## Bounded nature of acceptance

This is an independently authored mathematical audit of a prior result. It is not a new proof search, a novelty determination, an assertion of human review, journal publication, peer review, or formal verification. Historically recorded computational diagnostics are supplemental; they were not rerun for this publication edition. No source manuscript or copied source text is part of the authored deliverable.
