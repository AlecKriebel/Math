# 2141 / EP486: accepted prior logarithmic-density counterexample

Shouqiao Wang's *A Proposed Solution to Erdős Problem 486* constructs one
fixed infinite family A of positive moduli, with arbitrary residue sets X_q,
whose survivor logarithmic averages do not converge. The complete prose
proof of the pinned ten-page manuscript is accepted after independent
mathematical audit:

    liminf L_B(x) <= 177/200 < 49/50 <= limsup L_B(x),
    L_B(x) = (1/log x) sum_{1 <= m < x, m in B} 1/m.

For every installed residue, the defining endpoint satisfies q<m<2q.
Thus every X_q excludes zero, and strict q<m and original inclusive q<=m
activation give exactly the same survivor set, integer by integer.

This is an audit of an identified prior result, with no novelty claim.
The arbitrary-residue construction does not settle singleton-residue EP25.

## Reading order

- AUDIT.md: the complete global prose-proof audit, including periodic
  recovery, skeleton, probability, footprint, epochs, deletion cutoffs,
  original-formulation bridge, and limitations.
- FOCUSED_AUDIT.md: independent complete finite-deletion-lemma analysis and
  exact activation bridge. Its scope does not independently certify every
  step of the global theorem.
- ACCEPTANCE.md and ACCEPTANCE.json: exact accepted claim, review status,
  scope and exclusions.
- SOURCES.json: public citations, byte/hash pins and historical inspection.
- VERIFICATION.json: historical check results and edition boundaries.
- MANIFEST.json: exact eight-file inventory and hashes of the other seven.

## Formal and review limits

Acceptance means independent internal AI review of the specified written
arguments. This AI-assisted work is unrefereed; no external human peer review,
journal acceptance or proof-assistant certification by this audit is claimed.
The retained formal statement was read, but no local Lean replay, build,
full formal dependency audit or axiom computation was performed.

The retained author tree is d28713ac8245ca86a686b8c67370a8d19d81b242.
The external replay report concerns 61325b10bbdc29f4fb5e0618b414b9f2189333ad;
identity between those trees was not established. The inspected formal
implementation uses a four-color biased construction, whereas the accepted
prose proof uses fair bits and a central-subset window. Statement readback
therefore is not a line-for-line formalization claim for this prose proof.

## Publication boundary

This edition preserves both complete general mathematical derivations.
It omits one optional explicit finite-threshold computation from the main
audit and finite toy parameters and numerical computational witnesses from
the focused audit. Historical-check wording is clarified. Those edits are
editorial only; no mathematical proof attempt was added.

Only authored mathematical prose and public verification/source metadata are
included. No code, copied source bodies or PDFs, datasets, raw certificates,
numeric computational witnesses, private sources or private coordination are
published. Analytic constants and their written proofs remain. This is not
an executable reproduction package. The original sealed audits, QUEUE.md
and unrelated repository content are unchanged.

The manuscript is publicly titled a proposed solution. No current tracker
status, exhaustive novelty search or community-wide resolution is asserted.
Primary source: [Wang manuscript](https://multiscalar.ai/results/erdos-486/paper.pdf).
Original: [Erdős, Some unsolved problems (1961), I.26](https://users.renyi.hu/~p_erdos/1961-22.pdf).
