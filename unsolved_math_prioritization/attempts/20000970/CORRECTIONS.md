# Corrections and contract clarifications

## Prose-edition and review scope

These AI-assisted authored documents are unrefereed. “Accepted” refers only to
the stated independent internal AI audit; no external human peer review,
journal acceptance, or formal proof-assistant certification is claimed.
The complete mathematical arguments are retained. This edition makes only
framing, attribution, and distribution-related editorial changes; no algorithm
or mathematical claim is changed.

Executable sampler and test programs, detailed test receipts, computational
certificates and raw datasets are omitted. Statements about implementation or
finite checks below record the review of the authenticated original artifacts;
they are not claims that this prose-only edition includes runnable code or
reproducible test receipts. Public verification metadata records the historical
checks and their limits. Hashes identify bytes and do not establish truth.

No blocking correction is required for the sealed candidate's mathematical
proofs or sampler. Its partial-result status and novelty disclaimer must remain.
The following optional wording improvements do not alter the certified result.

1. The original audit recommended adding to the low-level lift and
   sample_from_plan docstrings (the implementation is omitted here): "The plan must
   be produced by peel or otherwise independently verified as a valid
   root-preserving simplicial-deletion certificate. These helpers do not
   validate an arbitrary externally supplied plan."

2. When quoting the runtime, keep the candidate's qualifications together:
   graph-operation counts use a unit-cost adjacency model; Python set lookups
   have the stated expected-cost interpretation; sorting adds
   O(m log(m+1)); fair-bit rejection has expected, almost-surely terminating
   cost. A deterministic total wall-clock bound for the exact Python sampler
   is not asserted.

3. For historical attribution, "the correspondence as presented by Benson,
   Chakrabarty and Tetali" is more precise than implying their priority.
   Their Remark 3.1 itself points to earlier antecedents. Those earlier papers
   were not independently inspected in this audit, so no first-discovery
   attribution is made.

The universal-sink reduction already corrects the prior interpretation that
chordal fixed-source sampling was left open by the bipolar theorem. Retain
that correction and the explicit limit that the proceedings PDF omits its
referenced detailed appendix. Do not describe this audit as verifying that
missing appendix, proving novelty, or solving general efficient sampling.

No changes were applied to the sealed candidate. This prose edition adopts
the valid-plan clarification in RESULT.md, retains the runtime qualifications,
and uses the more precise historical attribution. These editorial changes do
not change the algorithm, mathematical claims, or original audit provenance.
