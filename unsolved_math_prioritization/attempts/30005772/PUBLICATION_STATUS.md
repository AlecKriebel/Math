# Scope clarification and audited partial status

Publication checkpoint: 3 October 2026 (UTC).

**The original all-size negative-color interpretation problem remains unsolved after five approaches.** The fresh independent audit returns **PASS_PARTIAL**, with no blocking mathematical defect. Its full report and portable controls are included in [audit/AUDIT_REPORT.md](audit/AUDIT_REPORT.md). The frozen author files are preserved byte for byte; this separate addendum qualifies their presentation.

## Formula-seeded eventual model

**The eventual walk model is formula-seeded, not seed-free.** In the notation of PROOF.md, its terminal multiplicity satisfies

`v_0^(t) = c(s+t,0;k) = A(s+t,k)`.

For the first block `s <= N < 2s`, the walk length is zero. The model therefore consists simply of one of those prescribed terminal colors. The explicit finite coefficient formula computes these numbers without an A-oracle, but this is not an intrinsic combinatorial explanation of the seed interval. Any statement that the construction does not use A as a prescribed multiplicity must be understood only in that formula-computation sense. The nonnegative-transfer theorem and counting identity remain correct; they do not give a seed-free structural solution.

## Global even-size cancellation

The even-size construction is an explicit finite-set model and transported sign-reversing involution for all integer parameters. Its survivors come from globally ordering and cancelling signed prefixes. It is generic, potentially expensive, and dependent on the chosen order. It is a weak algorithmic answer to the even-size subquestion; it is not an established natural local arrangement interpretation. No unqualified all-size solution is claimed.

The local `k=-1` graph and its finite terminal vector have their stated domains. The negative-cycle result obstructs only diagonal sign switching of the squared Jacobi matrix. Neither point removes the preceding limitations.

## Validation and release scope

- Frozen author program: 124,917 exact assertions; independent replay byte-identical.
- Separately implemented audit: 245,193 exact assertions and seven rejected mutations.
- Full independent report and every portable audit file are included unchanged.
- No historical-novelty, human-peer-review, naturalness, or full-resolution claim.
- No source PDFs, full extracted source text, source-page images, raw corpus records, or private history are included.
- The queue change is confined to this problem's Status and Turns cells: `unsolved`, `5/5`. Existing header, other rows, links, and findings remain unchanged.

The author README and research log describe the pre-audit handoff; this addendum records the later completed audit. It is a publication clarification, not a sixth mathematical approach. Subjective research completion estimate: approximately 35% toward a structural all-size answer, with the five-approach budget and requested reproducibility work complete. This estimate is a planning judgment, not a mathematical result or probability claim.

AI tools were used extensively in the research, writing, checking, and adversarial audit. The work is unrefereed.
