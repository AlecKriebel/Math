# Sum-free subsets of positive integer grids

Authored mathematical audit and finite attempts for Green Problem 6 (dataset ID 98). Prepared 2026-10-20; no novelty claim.

The target is the maximum cardinality f_d(N) of a subset of {1,…,N}^d containing no x+y=z, including x=y, with ordinary componentwise integer addition.

Full finite-target disposition: **UNSOLVED after five substantive attempts (5/5)**. This status does not negate the separate qualified asymptotic result.

## Two different scopes

- **Asymptotic:** qualified pass for the fixed-d leading-density theorem of Keevash–Lim v2, with the explicit proof repairs and independent rational checks in [REVIEW.md](REVIEW.md) and [REPAIR_AUDIT.md](REPAIR_AUDIT.md). The manuscript was publicly listed as submitted; journal acceptance and peer-reviewed status were not verified.
- **Exact finite:** the general formula is not established by this package. Finite certificates, exact families, reductions, and lower-bound improvements must not be presented as a complete solution. See [SCOPE.md](SCOPE.md).

## Reading order

1. [SOURCE_GATE.md](SOURCE_GATE.md): original target, manuscript versions, publication-status evidence, and positive/zero-based grid comparison.
2. [REVIEW.md](REVIEW.md), then [REPAIR_AUDIT.md](REPAIR_AUDIT.md): corrected asymptotic argument, numerical obligations, dependencies and qualifications.
3. [EXACT_ATTEMPT_1.md](EXACT_ATTEMPT_1.md) through [EXACT_ATTEMPT_5.md](EXACT_ATTEMPT_5.md): chronological finite investigations. Later results supersede earlier uncertainty where explicitly indicated.
4. [FINITE_AUDIT.md](FINITE_AUDIT.md): independent finite audit.
5. [REPRODUCIBILITY.md](REPRODUCIBILITY.md): portable replay instructions. All scripts, authored results, and compressed-certificate transport files are in `computation/`.

## Certificate transport

First run `python computation/reconstruct_certificates.py`. The largest certificate, `finite_certificate_d3_n5.json.gz`, is shipped as 47 numbered base64 text files in `computation/certificate_parts/`, not as a large binary file. The standard-library reconstructor verifies every part and the original byte count and SHA-256 before writing the identical gzip bytes. The other eleven gzip certificates are shipped unchanged. This is a transport-only change, not a new certificate or a mathematical change.

[SOURCES.md](SOURCES.md) lists public references. The SHA-256 manifest records byte counts and hashes of the shipped publication files, including the text parts and reconstructor but excluding the manifest itself and the reconstructed (not shipped) gzip file. Source PDFs, copied third-party scripts, source text extracts, dataset contents and private coordination material are not included.
