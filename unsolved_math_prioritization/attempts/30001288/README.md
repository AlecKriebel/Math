# Motivic Albanese and Walker Abel–Jacobi targets

Problem **30001288 / OWR-3481-005**, queue rank **973**. Disposition: **unsolved, 5/5**. This is an accepted, scoped unresolved investigation with a verifier-only correction. It does not establish the general connected rational comparison, historical novelty, global open status, or external human peer review.

## Strongest accepted results and exact gap

The literal full-rational-sheaf formula has a projective-line component defect. This is separate from the intended connected rational question. The accepted investigation establishes transfer-compatible component splitting, the Albanese-unit epimorphism, connected rational divisor and zero-cycle cases, curve–projective-space products, and the open-curve boundary-period calculation. It identifies the precise common-presentation relation-kernel criterion and retains the full rational Lawson kernel, including the additional contribution in Walker's examples.

Neither inclusion between the two relation kernels is established in general. General connected rational, singular, and higher-dimensional nonproper comparisons remain unresolved. Finite linear-algebra controls do not prove motivic, Lawson, Chow, or Hodge-theoretic assertions.

## Preserved record and accepted copy

- `original/`: the unchanged 12-file author snapshot, including its historical pending-review language.
- `audit/`: the complete 12-file independent audit, acceptance, correction patch, source metadata, exact controls, and frozen normal/optimized results.
- `corrected/`: a separate 12-file copy reconstructed by applying `audit/CORRECTION.patch` exactly. Only `checks.py` and `AUTHOR_MANIFEST.json` change. There is no mathematical correction.

The original verifier falsely prints `Manifest integrity: PASS` under `python -O` for four corruption classes. Its optimized integrity claims must not be trusted. The exception patch repairs the claimed payload-integrity and rectangularity checks; it alone does not authenticate a manifest or enforce a complete inventory. `verify_publication.py` supplies the separate externally pinned, closed-inventory check and rejects extra or missing members, symlinks, unsafe names, duplicates, and self-consistent rehashes against a trusted external digest.

## Portable replay

Requires Python 3.10+ and its standard library, with no network, copied sources, third-party packages, or local research-directory assumptions. Obtain the SHA-256 of `PUBLIC_MANIFEST.json` from the independently retained PR description or receipt; do not derive the expected value from the untrusted package you are validating.

```sh
python3 -I -S -B verify_publication.py --expected-manifest-sha256 TRUSTED_SHA256
python3 -I -S -B -O verify_publication.py --expected-manifest-sha256 TRUSTED_SHA256
python3 -I -S -B mutation_tests.py --expected-manifest-sha256 TRUSTED_SHA256
python3 -I -S -B -O mutation_tests.py --expected-manifest-sha256 TRUSTED_SHA256
```

Each full publication replay explicitly launches both normal and optimized audit wrappers; each audit wrapper explicitly launches both normal and optimized author children. Each audit wrapper checks 57,135 exact conditions and 56 regression cases, preserves 73,323 author controls, confirms the original optimized defect, and matches its frozen result exactly. The publication mutation suite has 38 normal/optimized trials, including two valid baselines and 36 expected rejections. Checks use temporary copies and do not change frozen files.

All material is authored analysis/code or permitted public verification metadata. Scholarly PDFs, source extracts, dataset contents, private gates, and coordination records are excluded. Public source titles, URLs, hashes, sizes, and actual historical inspection scope are retained in the frozen source records; publication replay does not download or independently re-inspect those sources.
