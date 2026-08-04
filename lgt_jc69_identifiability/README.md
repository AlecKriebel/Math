# Global identifiability in a three-taxon LGT model

**Version 0.2 — prepared for author audit — August 2026**

This archive contains a standalone manuscript, two-page technical summary, exact verifier, numerical sanity audit, frozen source metadata, and author-facing materials.

Paper page (unlisted, not linked from the site's paper listing): https://aleckriebel.github.io/Math/papers/lgt-jc69-identifiability/

## Primary theorem

For every fixed known JC69 substitution rate `mu > 0`, the exact three-taxon site-pattern distribution under the ordered-pair Poisson LGT process defined in the manuscript uniquely determines every interior triple

```text
0 < t1 < t2,  lambda > 0.
```

The result is global on the full open domain. The exhaustive process map is injective, its Jacobian has rank three everywhere, the matching species-tree cherry is identified by a strict site-pattern inequality, and there is no exceptional interior set or second interior preimage.

## Three distinct maps

- `F_proc`: the exhaustive stochastic-process map. It includes arbitrarily many noncoalescing movements of sampled ancestry through an ancestrally unoccupied species branch and is globally injective.
- `F_table`: the auxiliary fourteen-history map obtained from the named finite classes, with the two one-transfer density types distinguished and transfer variables interpreted as absolute gene-tree times. A rigorous Krawczyk certificate proves an open set of regular observed distributions with at least two preimages.
- `F_src`: the map implemented by the frozen distributed formula/code. It differs from both other maps and reverses the strict matching-pair inequality at an exact interior point.

The manuscript states each result at the scope proved. It does not treat the process theorem as an unqualified theorem about the displayed source formula.

## Package layout

- `main_manuscript.tex`, `main_manuscript.pdf` — theorem-first paper and appendices.
- `technical_summary.tex`, `technical_summary.pdf` — two-page technical summary.
- `AUTHOR_HANDOFF.md` — concise technical handoff.
- `SOURCE_SNAPSHOT.md` — immutable arXiv/repository identifiers, hashes, and source locations.
- `PROVENANCE.md` — AI-assistance and computational-verification disclosure.
- `CHANGELOG.md` — revision-by-revision record.
- `ENVIRONMENT.md`, `requirements-lock.txt` — archived toolchain and Python lock.
- `verifier/` — symbolic, transition-matrix, source-map, and interval checks.
- `verifier/certificate.json` — machine-readable exact target, rational box, and rational-decimal Krawczyk preconditioner.
- `verifier/source_diagnostic.json` — machine-readable frozen source point and exact diagnostic values.
- `verify_exact_transcript.txt` — deterministic theorem-bearing run.
- `simulation_audit_transcript.txt` — separate fixed-seed Monte Carlo run.
- `clean_unpack_transcript.txt` — clean extraction, compilation, and verification run.
- `MANIFEST.sha256` — per-file checksums for this directory.

## Frozen source version

The source audit is frozen to:

- arXiv `2607.14653v1`, submitted July 16, 2026;
- repository `lkubatko/LGT-Model`;
- commit `1954b2ab92525dfdaf43b50f97dcf46658cab6c9`.

`SOURCE_SNAPSHOT.md` gives every available local SHA-256 hash, Git blob identifier, function/cell location, retrieval date, and the precise source-archive retrieval limitation. No mutable repository state is used as an identifier.

## Exact verification

From the revised package root:

```bash
make verify-exact
```

This command runs only deterministic theorem-bearing checks:

1. exhaustive genealogy normalization and topology probabilities;
2. every symbolic history integration used in the compact maps;
3. Fourier/site-pattern transformations;
4. direct JC69 comparison of all 64 nucleotide patterns;
5. fixed-`(D,M)` and Jacobian-factorization identities;
6. cube bijection, topology inequality, rate-scale ambiguity, and likelihood-Hessian algebra;
7. the exact source-formula reversal and positivity certificate;
8. the 384-bit outward-rounded MPFR Krawczyk certificate.

Expected final line:

```text
ALL EXACT CHECKS PASSED
```

The Krawczyk verifier is logically independent of the numerical root search. It reads only the exact target in `Q(sqrt(10))`, exact decimal-rational box endpoints, and an exact decimal-rational preconditioner. All logarithms, exponentials, powers, matrix products, and determinant bounds are evaluated with directed MPFR rounding.

## Simulation audit

The Monte Carlo comparison is intentionally separate from the proof:

```bash
make audit-simulation
```

Expected final line:

```text
SIMULATION AUDIT PASSED
```

It uses a fixed seed and checks that simulated histories agree with `F_proc` and remain separated from `F_table` at the audited point.

## Combined verification

```bash
make verify
```

Expected final line:

```text
ALL CHECKS PASSED
```

## Compile the documents

```bash
make pdfs
```

This uses `latexmk`, compiles both LaTeX documents, and fails if the final logs contain overfull boxes, missing files, undefined citations or references, or fatal diagnostics.

## Dependencies

The archived successful environment is listed in `ENVIRONMENT.md`. The essential requirements are:

- Python 3.13.5 for the archived transcript;
- SymPy 1.14.0 and mpmath 1.3.0 from `requirements-lock.txt`;
- an MPFR shared library discoverable as `libmpfr.so.6` or through `ctypes.util.find_library("mpfr")`;
- GNU Make;
- `latexmk` and a LaTeX installation with the packages used in the two `.tex` files.

The simulation uses only the Python standard library. NumPy is not required.

## Clean-checkout test

From a fresh clone of the repository:

```bash
cd lgt_jc69_identifiability
sha256sum -c MANIFEST.sha256
make clean
make pdfs
make verify-exact
make audit-simulation
make verify
```

The archived `clean_unpack_transcript.txt` records this sequence against the original author-ready package layout.
