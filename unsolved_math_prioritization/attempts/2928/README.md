# Kirby 4.52: stable normal invariants, ID 2928

**Unsolved partial results, 3/5 substantive approaches.** This packet accepts only the orientation-clarified reduction and restricted consequences of cited prior results. It does not establish general Wall-orbit realization, a counterexample, novelty, or global open status. Independent AI review is not human peer review or formal proof certification.

## Read first

- [Corrected proof](corrected/PROOF.md) and [report](corrected/REPORT.md)
- [Complete independent audit](audit/AUDIT.md)
- [Exact acceptance](acceptance/ACCEPTANCE.md)
- [Actual orientation correction patch](audit/orientation_clarification.patch)
- [Source verification and inspection limits](audit/source_verification.json)

The literal orientable problem allows all simple self-equivalences. The orientation-preserving subgroup applies only to the separately fixed-oriented variant; the two branches are not identified. Normal-invariant composition uses an affine inverse-pullback convention, not naive addition. The good-group and stated Whitehead-group hypotheses are retained. General unstabilized realization or cancellation by a simple self-equivalence remains the exact gap.

## Preserved byte identities

The `original/` directory is the historical author freeze, including its then-pending audit wording. `corrected/` is the accepted derivative. `audit/` and `acceptance/` reproduce their respective frozen archives. Every ZIP, external manifest and historical receipt in `releases/` is preserved without modification. Historical `publication_performed: false` and pending-audit receipt fields describe their original checkpoint, not this later publication.

The original, corrected, audit and exact-acceptance archive SHA-256 values are respectively:

- `184e4e995b419213860f36e8b250aa56bd606b7fd9e6eb8076726dc94524a2bc` (11695 bytes)
- `6eb61d12048125141eedb429845a1bced6c930a660ab17ecebb969b4c2cc7f1d` (12239 bytes)
- `5272356d6dfb202b53258ab11df6400929566c6c2ca3aefe179d7a290be4391e` (18051 bytes)
- `40ff9c08dca065ed48865333903c4085d0c6f74c7051b3f68b4cd2683950b067` (4067 bytes)

## Reproduce safely

Requires Python 3.10+ and the standard `patch` command. Authenticate the entrypoint itself from a trusted commit and the publication receipt before executing it. The wrapper pins the manifest, checks the complete file allowlist, authenticates every frozen archive/member and expanded copy before executing packet code, replays the real correction, and runs normal/optimized acceptance and audit drivers.

```sh
python -B verify_publication.py
python -O -B verify_publication.py
```

Each audit driver invocation checks four positive runs, 96 tamper-mode rejections and eight trust-boundary probes. Those probes deliberately reseal altered unchecked rank/prose: the local checker accepts them, while independent external member pins reject them. A locally modifiable manifest is not a trust root. All checks are finite integrity and scope checks, not theorem certification.

The portable source-input verifier hashes the complete three corpus files, checks unique target identity and full-record/report-pair digests, and rehashes six cited PDF inputs, historical KL v2 and KT. Source files must be supplied separately; none are included here.

```sh
python -B verify_publication.py --catalog /path/to/catalog.json --problems /path/to/problems.json --reports /path/to/research_results.json --pdf-directory /path/to/pdf-inputs --kt-pdf /path/to/kt_v1.pdf
```

The PDF directory uses the original acquisition basenames: `k3.pdf`, `knv_v2.pdf`, `hu_v1.pdf`, `kp_v2.pdf`, `hkpr_v1.pdf`, `kl_v3.pdf`, and `kl_v2.pdf`. Without those five input arguments the wrapper explicitly reports source-input replay as not run. The published audit retains the original source-reading evidence and its limits; hash replay is not a new literature review.

## Publication scope

The target is rank 919, numeric ID 2928, KP-4.52. This publication changes only that queue row's Status to `unsolved` and Turns to `3/5`; Findings and all other queue bytes are preserved. Completion toward a full solution is not established; 3/5 counts approaches, not a completion percentage. No additional mathematical search turn is claimed.

No copied source PDFs/text, corpus contents, private sources, private personal data or private coordination material are included. Public scholarly titles/URLs, hashes, byte counts and inspection history are included for reproducibility.
