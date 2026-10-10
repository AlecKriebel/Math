# 30001631: Takhtajan–Zograf curvature partials

**Unsolved, 5/5 attempted approach families. Independent AI audit: pass with controlling clarifications C1 and C2. NO RESOLUTION.**

The original Obitsu question is item 3 on printed page 3130 of [OWR 53/2010](https://doi.org/10.4171/OWR/2010/53). It does not specify the curvature type. The neighboring item about the negative Ricci form is a separate question. This record proves no curvature sign or counterexample for an actual positive-dimensional finite-type Takhtajan–Zograf (TZ) tangent metric, under any of the distinguished curvature conventions. It makes no novelty, exhaustive-literature, or global-openness claim.

## Controlling interpretation

The following clarifications from [the independent audit](audit/AUDIT.md#2-controlling-clarifications-and-affected-dependencies) are explicitly adopted and control all readings of the preserved author packet:

- **C1:** At a fixed surface and normalized cusp, the tangent-to-quadratic-differential map defined by `mu = y^2 conjugate(q)` is complex-antilinear. Conjugating the Fourier coefficients gives a complex-linear fiber isometry into its finite-dimensional image in the sequence Hilbert space. It does not establish holomorphic variation in moduli, even though the conditional Gram-frame curvature lemma is valid. No later proof uses an invalid promotion to a holomorphic tangent embedding; that attempted application stops at the unproved hypothesis.
- **C2:** The author's phrase “finite-group Bers maps” means Bers maps in the finite-type/cofinite Fuchsian-group setting. Such groups are generally infinite. It is not a finite-group assertion or a finite-type curvature-negativity theorem imported from a special universal result.

The frozen author files remain unchanged, including the historical pending-audit and publication-not-performed fields. The completed audit is a separate preserved object. The original audit's no-publication fields likewise describe its own freeze.

## What the record establishes

- The normalized cusp Fourier norm identity, including its exact coefficient, convergence argument, and conditional Gram-frame reduction
- A curvature-of-a-sum identity applicable to the cuspidal metric decomposition, with the nonnegative defect subtracted
- Potential/fourth-derivative and WP-ratio/Ricci-Hessian reductions, without the missing actual derivative bounds
- Degeneration models and countermodels explaining why zeroth-order asymptotics and slice curvature do not prove an ambient TZ sign; the published normal upper estimate also supports the known incompleteness deduction

These are partial deductions and conditional reductions. They are not a solution of the target. The five approach families have been investigated; this does not mean every method or paper has been exhausted.

## Reading guide

- [Author research and proofs](author/RESEARCH.md) and [five-approach log](author/APPROACH_LOG.md)
- [Complete independent adversarial audit](audit/AUDIT.md) and [audit disposition](audit/STATUS.json)
- [Author source metadata](author/SOURCE_VERIFICATION.json) and [independent retrieval/inspection metadata](audit/SOURCE_AUDIT.json)

The audit independently retrieved six public scholarly PDFs, matched their recorded hashes and byte counts, and inspected relevant passages. The live selected problem page returned HTTP 403. The original raw statement and AI-report corpora were unavailable, so their selected record hashes and complete corpus identity were not independently recomputed. Source hashes identify inspected bytes; they do not certify an unavailable dataset record. Repository and literature searches are bounded observations, not exhaustive absence claims.

## Portable offline replay

Use Python **3.12.14**, with the pinned dependencies in this directory's requirements file:

    python3 -m pip install -r unsolved_math_prioritization/attempts/30001631/requirements.txt
    python3 -B unsolved_math_prioritization/attempts/30001631/verify_publication.py

After dependencies are available, verification requires no network or source PDFs and works from any current directory. The wrapper verifies the exact file allowlist, hashes, frozen manifests, both ZIPs and every archive member; then replays the original eleven controls and the independent 23 check groups byte-for-byte. The latter include eight deliberately incorrect mathematical alternatives that must be rejected. Their supplementary high-precision quadrature is not an exact proof. The scripts do not construct or evaluate the curvature of an actual finite-type TZ surface. The written arguments, rather than finite test results, establish the partial mathematical statements.

Byte-for-byte output replay uses the recorded interpreter and dependency versions; other versions may produce different presentation strings. The wrapper fails rather than claiming an exact replay if the environment or recorded output differs. The publication manifest excludes itself; its digest is externally recorded in the publication verification receipt. Independent delivery tests additionally execute the wrapper on corrupted copied files and archive inputs.

Frozen fingerprints:

- Author manifest: `793eff4aec0c86808289fa1ce17d32d95f52c03dd09219d13538a6fa6527d5cd`
- Author ZIP: 21,262 bytes; `c9a370d76b6ef5cb98214f49098e812eb9c470adfa9e3a694bcbea4bd006298f`
- Audit manifest: `25337b329f8cb087a391cd161014e614707582fcb5feb71304218470964fc9b0`
- Audit ZIP: 24,319 bytes; `79fac578564f0939a154925154892c7a940f5dc947004d1c23a4947e93beb3bb`
- Audit report: `972dda0eaeae5654823ca98a23b75614b70bc71462a6f66fed98a16732365f9f`

## Publication scope

The queue changes only this problem's Status from `queued` to `unsolved` and Turns from `0/5` to `5/5`. Findings, Chat, DOI, every other row and byte, and the existing stale embedded header are preserved. No queue regeneration is used.

This draft contains authored mathematics, authored code, audits, public verification metadata, and byte-preserved public-safe archives. Source PDFs, source extracts, source images, raw dataset records, and private coordination files are excluded. This is an independent AI audit, not human peer review or formal proof verification. Publication does not merge, release, create a DOI, or contact third parties.
