# Recursive bounds for cyclic fixed subgroups

Problem 1101206 / AMR-010-1206, Bestvina's Question 12.6.

For a fixed ordered free basis of F_n and M(alpha)=max_i |alpha(x_i)|, there is a total recursive function B(n,L) equal to the largest based reduced length of a generator of a nontrivial cyclic Fix(alpha) among automorphisms with M(alpha)<=L. The empty maximum is zero. The construction is uniform in finite rank n and yields a recursive bound in explicit total input length.

The deep input is the established Bogopolski–Maslakova fixed-subgroup basis algorithm, Theorem 1.1 of arXiv:1204.6728v6. Its correctness and termination are explicitly imported. The authored proof supplies the terminating folding recognizer, finite enumeration and exact maximum, boundary cases, fixed/variable-rank and encoding qualifications, justified recursive norm conversions, and a based-versus-outer counterexample.

Disposition: PRIOR_RESULT_VERIFIED_SCOPED. This accepts the computable-bound interpretation as a consequence of prior results. It does not claim a new solution of the algorithm problem or an unqualified resolution of every quantitative interpretation of the original question. No polynomial, exponential, elementary, primitive-recursive or other specified rate is proved. No novelty, priority or claim that stronger bounds are unknown is made.

## Contents and provenance

- [PROOF.md](PROOF.md): the complete authored proof and source-dependency boundary.
- [AUDIT.md](AUDIT.md): the complete accepted mathematical audit, including its source reading and inspection limits. It contains the same original mathematical argument as PROOF.md; their duplication provides standalone documents and does not constitute a second independent audit.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): exact accepted consequences and exclusions.
- [SOURCES.json](SOURCES.json): public scholarly titles/URLs, PDF sizes/hashes, versions, retrieval/inspection history and limitations.
- [VERIFICATION.json](VERIFICATION.json): historical finite-check summary, artifact integrity scope and distribution boundary.
- [MANIFEST.json](MANIFEST.json): the exact eight-file list, with byte counts and SHA-256 hashes of the other seven.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance concerns only the recursive-bound consequence of the imported Bogopolski–Maslakova basis algorithm; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and elementary finite checks were performed during the preceding investigation on 11 October 2026. Edition preparation authenticates retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.

The inspected prior input is an exactly closed eight-file selected bundle. That fact is not a claim of closure for its parent retained directory and does not permit distributing the original programs or raw outputs. This edition includes authored complete mathematical prose and public source/verification metadata only. No programs, raw check outputs, dataset contents, source PDFs/extracts/images, private sources, private personal data or private coordination material are distributed.
