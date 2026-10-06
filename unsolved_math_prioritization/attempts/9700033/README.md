# SIRSN unbounded components: corrected exterior-covering partial result

Problem 9700033 / AMR-096-0033, rank 935. **UNSOLVED; 3 of at most 5 substantive approaches used.** This is an AI-assisted, unrefereed mathematical submission with an independent AI audit, not human peer review, formal verification, or a novelty certificate.

## Read the accepted derivative

- [Corrected proof](audit/corrected/RESULT.md)
- [Independent mathematical audit](audit/AUDIT.md)
- [Exact-byte acceptance](audit/ACCEPTANCE.json)
- [Actual correction patch](audit/MEASURABILITY_CORRECTION.patch)
- [Publication verification](PUBLICATION_VERIFICATION.md)

For each fixed r > 0, almost surely a finite family of unbounded components of E(infinity,r) comes within infimum distance 2r of every sufficiently distant point. The family has at most H_r distinct components, where H_r is an explicitly measurable route-witness count and E[H_r] <= 8p(1). Different witnesses may lie in the same component. The statement takes no expectation of the exact topological-component count.

General unbounded-component uniqueness remains unproved. The cover need not capture all unbounded components. The auxiliary marked parallel-line process is not a SIRSN counterexample. No common probability-one event for all real r is claimed; the fixed-r events can be intersected over positive rational r. No present literature-openness or historical-priority claim is made.

## Original and corrected versions

The author/ directory and the author archive preserve the exact original five-file submission. The audit/ directory and audit archive preserve the independently reviewed correction, originals, patch, and exact acceptance. Only audit/corrected/RESULT.md is the accepted mathematical derivative. Applying the actual patch to an exact copy of the original reproduces all five corrected files byte-for-byte.

The public package contains authored proof, code, audit, correction, acceptance, and public verification metadata. Full corpus data, third-party PDFs and text, and private coordination material are not included. Source metadata distinguishes existing local copies from fresh web inspections; it does not claim fresh remote PDF byte identity.

## Trust and reproduction

Use PUBLICATION_BOOTSTRAP.py with a separately retained SHA-256 pin for PUBLICATION_MANIFEST.json and all mandatory local corpus and source inputs. The verification document gives the invocation. The bootstrap checks external pins, strict inventories, archives and archive members before running archived code; it recomputes the complete corpus and canonical-pair binding and re-extracts the source PDFs.

The original verifier is only an integrity and finite-diagnostic checker. Coherent rewriting of its internal corpus metadata and certificate can pass it by design. The publication gate rejects such rewriting against an independently retained external anchor. Replacing both a package and the trusted pin is outside this integrity model. Finite diagnostics do not prove the continuum theorem.

## Queue scope

This draft changes only this problem's queue Status from queued to unsolved and Turns from 0/5 to 3/5. Its Findings cell and every unrelated byte, including existing notes, links, and the preexisting file prefix, are preserved.

## Primary sources

- David Aldous, [Scale-invariant random spatial networks](https://doi.org/10.1214/EJP.v19-2920), Electronic Journal of Probability 19 (2014), paper 15. The target is published Open Problem 7, section 8.4.2; it is Open Problem 33 in the long 2012 preprint.
- Jonas Kahn, [Improper Poisson line process as SIRSN in any dimension](https://doi.org/10.1214/15-AOP1032), Annals of Probability 44 (2016), 2694–2725.
- Guillaume Blanc, Nicolas Curien, Jonas Kahn, [Geodesics in planar Poisson road random metric](https://doi.org/10.1112/plms.70070), Proceedings of the London Mathematical Society 131 (2025), e70070. Its special-model results are not promoted to the general SIRSN target.

Publication checkpoint, 2026-10-06 UTC: the corrected partial result and exact-byte audit acceptance are preserved for draft review. Full-target completion is unknown; this package establishes a scoped partial consequence and records the remaining uniqueness gap. No merge, release, DOI, or external outreach is part of this submission.
