# EP252: credited prior-proof audit, formal reproducibility hold

The audited target is irrationality of the convergent series

    alpha_k = sum_{n>=1} sigma_k(n)/n!,
    sigma_k(n) = sum_{d|n, d>0} d^k,

for every integer k >= 0. Credit for the prior all-degree argument belongs to
Tokengrinder. The pinned claim is at commit
46b9fd26361faf669bcd7e4495e63678bfa6a735 of the public Erdos252 repository.

## Disposition

Mathematical and static-source inspection: PASS within the stated scope, with
no mathematical gap found. FORMAL REPRODUCIBILITY HOLD remains in force.
There was no independent Lean build, transitive compiler/dependency/kernel
closure verification, or independently obtained final axiom report. A source
file containing an axiom-print command does not establish what a fresh run
would print. No formal acceptance, novelty, human peer review, or journal
acceptance is claimed. This AI-assisted audit is unrefereed.

## Contents

- MATHEMATICAL_AUDIT.md retains the complete seven-step mathematical reconstruction, statement/convergence checks, positive-degree and zero-degree arguments, source boundary, historical controls, and formal-hold requirements.
- ACCEPTANCE.md distinguishes mathematical acceptance within scope from the remaining formal reproducibility hold.
- STATUS.json gives the same disposition in machine-readable form.
- SOURCE_METADATA.json preserves pinned source identities, public URLs, scholarly titles, dependency versions, and recorded retrieval/inspection limits.
- VERIFICATION_SUMMARY.md states what was and was not checked.
- MANIFEST.json lists all seven public files and hashes the six other files. Its own hash must be obtained from an independently trusted publication record.

## Scope and evidence

The proof uses exact factorial tails, a scaled Stirling remainder, ordinary
CRT progressions, progression means for k >= 1, a fixed finite-difference grid
and squared CRT moduli. The k = 0 case has its own positive-tail argument.
No simultaneous-prime-values hypothesis or uniformity in k is used.

The complete manuscript and main Lean source were read in the recorded audit;
ten direct mathlib imports and key interfaces were checked statically. The
historical papers were inspected for relevant statements and hypotheses, not
as complete independent historical-proof audits. The historical frontier is
not an exhaustive current-literature or priority certificate.

The advertised SHA256SUMS path returned 404 at the pinned commit. This is a
documentation/reproducibility defect, not a mathematical counterexample. The
retrieved main-source hash agrees with the hash printed on manuscript page 20.

The finite exact checks reported here are historical, bounded corroboration.
Edition preparation did not rerun the omitted mathematical programs or fetch
and inspect new scholarly sources. Local byte-integrity and publication-plan
checks are distinct from mathematical testing and formal proof verification.

This is a prose-only edition of authored analysis and public verification
metadata. It contains no copied PDFs or source extracts, Lean/library code,
executable checks, detailed test outputs, raw datasets, private sources,
personal data, or private coordination material.

## Public claim

- [Pinned proof manuscript](https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/PROOF.pdf)
- [Pinned main Lean source](https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/Erdos252/Solution.lean)
- [Author verification boundary](https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/VERIFICATION.md)
