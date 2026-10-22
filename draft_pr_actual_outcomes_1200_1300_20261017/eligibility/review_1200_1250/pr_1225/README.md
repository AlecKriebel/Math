# Infinite modulus for a compact real set and its real complement

Target: 2307058 / AMR-022-7058, Gonchar's question communicated by Vuorinen in Hayman–Lingham Problem 7.58.

Status: accepted_full_stated_target, under the explicit conventions of PROOF.md. Required mathematical corrections: none. Literature priority and external peer review remain unverified.

This is an AI-assisted, unrefereed mathematical edition. Acceptance means an independent internal AI audit of the full theorem under its explicit curve and density conventions. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

The full authored proof and complete mathematical audit are retained in PROOF.md and AUDIT.md. Copied source documents, source text and images, executable code, raw datasets, raw search responses, independent preparatory material and private coordination material are not distributed. This is a written proof-and-audit edition, not a computational reproduction package.

Source retrieval and inspection statements describe the candidate and independent audit of October 11, 2026 UTC. Editorial preparation authenticated their sealed bytes and checked repository publication scope, but performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Hashes authenticate bytes; mathematical acceptance comes from reading the written arguments.

## Exact accepted theorem

For every compact E⊂[0,1] in the real axis, set F=R\E, taking the complement within that axis, and S₂={z:|z|=2}. Then

M₂(Γ(E,S₂))>0 implies M₂(Γ(E,F))=∞.

The families consist of all plane connecting curves under the stated endpoint convention: continuous curves locally rectifiable away from their endpoints, with nonnegative line integrals defined by increasing compact-interior-subcurve limits. Admissibility is required for every curve. Borel densities may take infinity on planar null sets. The proof also applies if only globally rectifiable connectors are used consistently throughout. The precise definitions and all qualifications are in PROOF.md.

No positive-length or interval hypothesis is imposed. In particular, the theorem includes zero-length compact sets of positive capacity. No exceptional curves or positive-capacity exceptional points are silently removed. The result is not extrapolated to other unspecified interpretations of the historical problem.

## Complete proof structure

1. A pointwise lower-semicontinuous finite-energy majorant retains even infinite density values on null sets.
2. Compact weighted-path arguments construct a Borel separating potential with actual plate values. Its line restrictions give Sobolev regularity directly.
3. A proved Fourier trace estimate and an L¹ translation argument force E to have length zero if an E-to-F finite-energy admissible density exists.
4. A separate augmented-density and small-circle concatenation argument handles that length-zero set. It forces every E-to-S₂ curve to have infinite augmented length.
5. Dividing the augmented density by n makes the outer-circle modulus zero, contradicting the hypothesis.

Length zero is only an intermediate conclusion; it is never identified with zero capacity. The argument invokes no touching-plate condenser equivalence or quasicontinuous-representative shortcut. The standard analytic foundations that remain as dependencies are explicitly listed in the manuscript.

## Reading order

- PROOF.md contains the complete frozen 16,705-byte manuscript verbatim after its publication preface. Its old pending-audit status sentence is historical; the current acceptance is stated above it.
- AUDIT.md preserves the entire mathematical acceptance report, including every lemma audit, endpoint case, independent challenge and source qualification. Only publication-context wording and private coordination metadata are edited.
- ACCEPTANCE.md and ACCEPTANCE.json state the exact accepted scope and remaining interpretation, priority and review limitations.
- SOURCES.json records public source identities and historical candidate/audit inspection scopes. VERIFICATION.json records byte authentication, full-content retention and review boundaries. No numerical result is substituted for an argument.
- MANIFEST.json lists exactly eight files and hashes the other seven; its own digest is independently pinned in the publication description.

## Source and interpretation boundary

The authenticated target is Problem 7.58 in the 2018 arXiv version, printed page 178 / PDF page 179. The historical no-progress statement does not establish current worldwide openness. The bounded searches did not locate a directly matching resolution, but establish neither novelty nor priority.

Publisher metadata establishes that a 2019 Springer edition exists. Its relevant problem page was not authenticated. A secondary search-result lead suggesting unclear terminology is recorded only as unauthenticated; no such wording is attributed to the publisher as a verified primary-source statement. The full accepted theorem therefore keeps its endpoint and density conventions explicit.

- Hayman–Lingham record: https://arxiv.org/abs/1809.07200
- Authenticated version's public HTML: https://arxiv.org/html/1809.07200v2
- Later publisher record: https://link.springer.com/book/10.1007/978-3-030-25165-9

The audit also inspected relevant statements in Brezis and Di Nezza–Palatucci–Valdinoci as background corroboration. Those sources supply no unproved problem-specific step: the required special trace and rigidity arguments are proved in the manuscript. No whole-paper audit is claimed.
