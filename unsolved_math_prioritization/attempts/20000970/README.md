# Maximal parking functions: an exact simplicial-core reduction

Problem 20000970. Accepted scoped partial progress; the unrestricted efficient
sampling problem remains unresolved by this work. Novelty is not established.

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

## What is established

For a finite connected undirected simple graph with a prescribed root, a
nonroot simplicial vertex of degree d gives a bijection between rooted acyclic
orientations before deletion and rooted acyclic orientations after deletion
times its d surviving neighbor labels. The correspondence as presented by
Benson, Chakrabarty and Tetali then transfers the construction to maximal
parking functions, with the root coordinate -1.

Iterating these constant fibers gives:

- Exact uniform reconstruction from a uniform core orientation and independent
  exactly uniform neighbor-label pivots.
- An exact fixed-parameter sampler in the b edges of the computed residual
  core, with a 2^b enumeration fallback. The parameter is not an optimized core.
- Exact equality of total-variation error for a law supported on valid core
  states and exactly uniform independent pivots, under a certificate fixed
  independently of sampling randomness.
- A self-contained polynomial-time sampler for every chordal graph, retaining
  the prescribed root throughout.

The exact sampling law uses an ideal independent-fair-bit interface. Integer
rejection terminates almost surely and has expected cost; expected sparse
hashing, output sorting, and arbitrary-precision costs are retained. The stated
low-level valid-plan contract does not promise validation of untrusted plans.

## Prior work and limits

The chordal existence conclusion already follows from the stated 2022
Bezáková–Sun bipolar-orientation theorem by adding a universal sink. The
inspected 12-page proceedings PDF omits the detailed appendix referenced in
Section 4; neither the candidate nor audit verified that missing appendix or
its claimed linear-time implementation. The self-contained polynomial proof
here does not depend on it. Correspondence attribution implies no priority.

No general efficient exact sampler, FPAUS, mixing bound or impossibility theorem
is proved. The arbitrary residual core can be large and its fallback is
exponential. Source inspection was bounded and does not establish exhaustive
current literature status or novelty.

## Files and evidence

- RESULT.md retains the complete substantive mathematical proof, all hypotheses,
  complexity qualifications, examples, obstructions and public references.
- AUDIT.md retains the complete substantive independent mathematical audit and
  its historically recorded implementation checks.
- ACCEPTANCE.md and ACCEPTANCE.json record the scoped decision and exact
  result/audit identities. CORRECTIONS.md records that no blocking correction
  was needed and describes the adopted optional editorial clarifications.
- SOURCES.json records public source titles, URLs, PDF hashes/byte counts and
  historical inspection/retrieval limits. Failed fresh NSF/DOI audit requests
  are distinguished from inspection of the authenticated retained PDF.
- VERIFICATION.json reports historical finite-check counts, match results,
  normal/-O/-OO agreement and receipt identity. Finite checks corroborate the
  implementation; the written proofs establish general mathematical statements.
- MANIFEST.json lists all nine public files and hashes the other eight. Its
  own digest is independently pinned in the proposed publication metadata.

Source documents, extracted source text and images, executable code, detailed
test receipts, computational certificates and raw datasets are omitted. This
is a prose-only edition, not an executable reproduction package. Edition
preparation added no new mathematical test run or scholarly-source inspection.
