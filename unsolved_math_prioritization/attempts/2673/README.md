# Universal nonabelian SU(2) surgery slopes: accepted partial packet

**KP-1.14 · record 2673 · rank 1039 · unsolved · 5/5 approaches**

Start with [ACCEPTANCE.md](ACCEPTANCE.md), the unchanged [author report](author/REPORT.md), and the [independent audit](audit/AUDIT.md).

The published-input result covers reduced 0 < |p/q| < 7 with |p| = 4ℓ^e for an odd prime ℓ. Exact trefoil exclusions and a published-input sequence proving nonclosure are included. The extension through |r| ≤ 8 remains conditional on identified 2025 preprints and their foundations. The universal classification is not solved, and 15/4 and 24/5 remain unresolved by these methods.

## Evidence inventory

- author/: eight unchanged files, including full mathematical analysis, code, public source pins, and historical validation.
- audit/: nine unchanged files, including independent mathematical review, nonclosure supplement, code, public source-inspection metadata, and historical validation.
- This directory: the acceptance summary, strict publication verifier, mutation controls, publication manifest, and bootstrap.

Source-status observations are dated 2026-10-08. Source PDFs, extracted source text, datasets, and coordination records are omitted. The source-free replay does not re-download or rehash scholarly documents. Eleven historical public-PDF hash matches are recorded as historical evidence only.

## Reproduction and trust

Use Python 3.11 or later, standard library only, running as real UID/EUID 1000. The scripts require isolated execution, no site initialization, and no bytecode writes. No package installation or network access is needed.

Before running anything, obtain the SHA-256 of BOOTSTRAP.py from a trusted external publication receipt, verify its bytes with an independent hash tool, and review the file. Do not substitute a freshly calculated hash of an untrusted file as your trust anchor. The authenticated bootstrap pins the verifier and publication manifest, which pins all payload files. BOOTSTRAP.py is excluded from that manifest to avoid a circular hash and is externally pinned instead.

Then run each mode:

```
python -I -S -B BOOTSTRAP.py .
python -I -S -B -O BOOTSTRAP.py .
python -I -S -B -OO BOOTSTRAP.py .
```

For the additional publication-boundary controls, authenticate mutation_tests.py via the pinned manifest before executing it, and supply the same external bootstrap pin:

```
python -I -S -B mutation_tests.py --root . --bootstrap-sha256 EXTERNAL_BOOTSTRAP_SHA256
python -I -S -B -O mutation_tests.py --root . --bootstrap-sha256 EXTERNAL_BOOTSTRAP_SHA256
python -I -S -B -OO mutation_tests.py --root . --bootstrap-sha256 EXTERNAL_BOOTSTRAP_SHA256
```

The top-level scripts write JSON only to stdout. They create disposable temporary fixtures and verify that inputs are unchanged. Actual read-only fixtures have 0555 directories and 0444 files, with attempted writes checked for denial. Native mutation harnesses receive a separate writable temporary source copy because copytree retains permissions; their arithmetic/verification read-only fixtures remain read-only. Publication controls also test relocation and a hostile import environment.

Each wrapper replay runs both native mutation suites. The author suite internally covers normal/-O with 50 total negative rejections; the independent suite internally covers normal/-O/-OO with 276. Repeating the wrapper in three modes repeats those native matrices rather than adding new distinct mathematical cases.

## Scope of verification

Byte authentication is separate from mathematical acceptance. Finite checks cover exact rational arithmetic, trefoil congruences, cyclotomic restrictions, low-genus determinant evaluations, and bounded regression cases. They do not certify gauge theory, universal knot statements, source-search completeness, or priority. The fixed-file verifier is not a race-safe hostile-filesystem sandbox. Fresh source-byte validation is NOT_RUN.

Original manifest SHA-256: 7d5d62eaa2d96d5f67383b8f0f7d9ec1888c337f7ff8982d55c0a9fc9f0b97ca

Independent audit manifest SHA-256: 3212febefd0554e915e7cc352c8be9404dcf406e6c6fc0cd3dc254210b9640b8
