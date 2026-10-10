# Acceptance of the scoped partial result

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

Decision: ACCEPTED-PARTIAL-SCOPED.

The independent proof review accepts, for finite connected rooted simple
graphs, the degree-sized constant fibers of nonroot simplicial deletion,
exact independent-pivot lifting, the 2^b times polynomial exact residual-core
sampler, exact preservation of core total-variation distance, and the chordal
polynomial-time specialization. The exact law assumes ideal independent
unbiased bits; runtime includes the manuscript's hashing, sorting and
arbitrary-precision qualifications.

The candidate manuscript and code were authenticated and kept unchanged.
Independent exhaustive and adversarial tests passed in normal, -O and -OO
modes with identical receipts. Finite tests support the implementation; the
separately reviewed proofs establish the universal mathematical statements.
No blocking correction remains.

Not accepted as established: a general efficient exact sampler, a general
approximate sampler, a mixing theorem, an impossibility theorem, originality,
or verification of the 2022 paper's missing appendix. The chordal existence
result is already a consequence of that paper's stated bipolar theorem via
a universal sink. The unrestricted AIM question is unresolved by this work.

The result retains PARTIAL-PROGRESS status. The general efficient sampling
problem remains unresolved by this work.

## Exact prose-edition identities

The accepted mathematical content is retained in the editorial derivative:

- RESULT.md: 21995 bytes; SHA-256 1ad3c34ce579f39300b83b433741c876658faf690e4d97311043c76699998c96.
- AUDIT.md: 18338 bytes; SHA-256 1d0c416904ff447eaf2d57473208bf45dc72928dea0af903018498109c7ceb43.

These are distinct from the original manuscript identity recorded in the audit.
The derivative changes framing, historical implementation/test references, and
correspondence attribution, and adds the optional valid-plan contract. It makes
no mathematical correction and does not distribute the reviewed programs.
