# Additional adversarial preprint review — version 1.0.1

Completed: 2026-09-23T13:48:05Z. **Verdict: preprint-ready, with no remaining actionable issue identified.** Completion of the requested mathematical/preprint review: **100%**. Publication refresh is recorded separately in the repository's DEPLOYMENT.md.

## Sequential independent reviews

The user requested fresh adversarial review, warranted repairs across all materials, and another new reviewer after repairs, continuing until no actionable issue remained. Two fresh AI subagents reviewed the proof independently before consulting prior verdicts.

| Round | Reviewed version | Finding and disposition |
| --- | --- | --- |
| [Round one](https://github.com/AlecKriebel/Math/blob/main/owr_3389_016_strict_gap/audit/preprint-adversarial-round1.md) | 1.0.0 | No new actionable issue in the full proof, source normalization, claims, references, PDF, or verifier. Two minor parent presentation findings were then repaired. |
| [Round two](https://github.com/AlecKriebel/Math/blob/main/owr_3389_016_strict_gap/audit/preprint-adversarial-round2.md) | 1.0.1 | Fresh independent reconstruction and attempted falsification found no actionable mathematical, scope, attribution, reproducibility, or PDF issue. No further manuscript revision requested. |

The second clean round meets the requested stopping criterion. No mathematical finding was dismissed or left unresolved.

## Repairs and global consistency

1. **Supporting-material discoverability:** the standalone paper referred to an accompanying package without linking it. Its provenance paragraph now links the public package landing page.
2. **PDF metadata:** title and author fields were empty. Title, author, subject, and keywords are now populated.

The paper is labeled version 1.0.1. No theorem, hypothesis, proof step, or bibliographic claim changed. The README, citation data, website, Zenodo fields, source archive, upload kit, and checksum manifests are synchronized. Both full new reports are included in the source archive. Earlier audits retain their original versions and hashes as historical records.

## What withstood attempted falsification

Both reviewers checked the form-defined Dirichlet operator on arbitrary bounded open sets; coordinate multiplier domain preservation; the finite-spectral-support contradiction; absolute convergence and pair cancellation; the exact remainder's sign; strictness at every real threshold above the ground eigenvalue; and the quadratic endpoint argument including repeated ground eigenvalues and J=1. Neither found a hidden smoothness, connectedness, simplicity, or boundary-condition assumption. The original report's missing square remains explicit, and the claim remains restricted to the corrected saturation question.

The second reviewer additionally checked interval threshold-deficit formulas in 300 bands and 1,500 interior rational thresholds. These model checks supplement the proof and are not presented as a formal verification of the general theorem.

## Final reviewed manuscript

- TeX SHA-256: `073f7e31a0037fa09ead605b5028d7c921e0188d2117734c7d1ba12a4b1ef051`.
- PDF SHA-256: `ff07b62aa5905544ab62b6cb04b5aa6ca528ccc61f18221fb2a0aa8c1e54f7b9`.
- Three pages; all freshly rendered pages inspected by the parent and second reviewer. No clipping, overlap, missing glyph, or broken reference found.
- The unchanged verifier passes 7,016 exact checks, including with Python optimization enabled, and reproduces the recorded JSON byte-for-byte.
- The second reviewer independently extracted the source package and rebuilt both ZIPs byte-for-byte. After incorporating both reports, the parent also passed the final manifest, metadata, archive, link, and deployment-copy checks; both ZIPs again rebuilt byte-for-byte from an extracted copy.

## Scope of the verdict

Ready to circulate as an AI-assisted mathematics preprint within the documented review scope. This is not external peer review, proof-assistant certification, journal acceptance, or an exhaustive priority guarantee. The manuscript supplies the analytic proof; computations check finite algebra and model spectra. No earlier conflicting resolution was identified in the scoped literature work. No journal submission, external outreach, Zenodo submission, or DOI creation was performed.
