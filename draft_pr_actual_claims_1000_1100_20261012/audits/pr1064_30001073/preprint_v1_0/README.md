# Credited Frobenius corollary support kit, version 1.0

Read `paper.pdf` or `paper.tex` for the self-contained research note. Author: Alec Kriebel, ORCID 0009-0001-9320-500X; CC BY 4.0. Extensive AI assistance; unrefereed; no external human peer review or formal certification.

For every nonnegative row-stochastic A of positive integer order n and unnormalized S=sum a_ij^2, per(A)<=exp(-n+e^4 sum a_ij^2 log(e/a_ij))<=exp(-n+e^4 S(1+log n)), with continuous zero terms. The fixed-gamma all-n bound retains e^(e^4 gamma); the prefactor-free n^(3e^4 gamma)e^(-n) bound is only for n>=2. The source's prior van der Waerden lower bound applies to doubly stochastic inputs. The stronger entrywise gamma/n hypothesis is not used. Equal uniform blocks require some polynomial loss, without establishing a sharp exponent.

The mechanism is explicitly a corollary of Anari-Rezaei 1811.02933v2 section 4 equation (6), also implied by Anari 2608.28031v2 Lemma 7 and Dong-Jain 2609.02017v1 Theorem 3.1 (g=4). Sequential permutation KL differs from matrix entry-mass KL. The scalar estimate is explicit here; historical novelty and priority remain UNKNOWN. Full Soules 2000/2003/2005 bodies were inaccessible and broader Orlicz, Roos and optimized lp consequences were not exhaustively classified. No first-solution, new-method, worldwide-open or independent-discovery certificate.

The dated preparation snapshot is `STATUS.json` (14 October 2026). It records zero new whole-package reviews, requires at least two, and sets publication_ready=false and issues_updated=false. The ascending publication gate is held after PR1032. These are preparation gates, not premises of the proof.

Run the following from this directory, either in the preparation folder or a clean archive extraction. Python 3 with its standard library suffices for verification and checks. Temporary outputs stay below ignored `tmp/`.

```sh
python3 -I -B verify_package.py
python3 -I -B run_checks.py --out-dir tmp/recheck
python3 -I -B build_archive.py --output tmp/rebuilt.zip
python3 -I -B verify_package.py --archive tmp/rebuilt.zip
python3 -I -B build_pdf.py --out-dir tmp/recompiled
```

Archive rebuilding is byte-identical with the recorded Python/zlib environment and the same frozen inputs. Fixed timestamps (2026-10-14 00:00:00), Unix regular-file mode 0644, sorted names and deflate level 9 are enforced. ZIP compressor versions can differ across environments; file identities and member verification are independent of that qualification. The PDF command uses Tectonic and may need its TeX bundle cache or network on first use. It exports to the specified directory and does not rewrite the canonical PDF; byte equality of PDFs from different compiler environments is not promised.

In a preparation/deposit pair the external `publication/DEPOSIT_BINDING.json` binds both canonical PDF and ZIP and is excluded from the ZIP to avoid a hash cycle. A present descriptor is always strictly checked. Clean extraction works without it. To require one explicitly, use:

```sh
python3 -I -B verify_package.py --archive tmp/rebuilt.zip --deposit-binding publication/DEPOSIT_BINDING.json --require-deposit-binding
```

That last command intentionally fails in an extraction where the external descriptor was not separately supplied. Copy the actual descriptor beside the delivery or pass its path when requiring this mode.

`support/history/submitted/` contains all nine exact original snapshots. Selected authored full root and family reports, derivations, source metadata, programs and finite outputs are frozen under `support/history/`. `COPY_MAP.json` and `SAFE_INPUT_PINS.json` bind every copy. Historical records describe their own editions and dates; their verdicts do not certify this new paper or its whole-package readiness. Seals may refer to excluded local artifacts; the present `SUPPORT_MANIFEST.json` alone defines archive member hashes. Original pre-edition identity assertions and omitted historical programs are not newly authenticated or replayed.

The original reviewer `finite_checks.py` is distributed unchanged and is rerun only in normal mode, with assertions active; results match the root baseline after declared runtime-only projection. The new `fresh_guard_checker.py` is a disclosed explicit-guard adaptation with added source-identity tests. Its normal and optimized runs agree, and six deliberately faulty variants fail in both modes. Selected finite Fraction/Decimal diagnostics corroborate support, chain entropy, conditional Jensen, Gibbs identities, KL mass cancellation, source expansions, endpoints and the norm estimate. They are not interval-certified computations or universal proofs. `support/CHECKS.json` records their execution scope.

All member paths are explicitly allowlisted. Third-party full PDFs, copied text, source images, raw search extracts, full repository tree/commit captures and unrelated filenames are excluded. `EXCLUSION_LEDGER.json` describes these boundaries. Full input custody, final preparation report, final verification, output pins, archive and external binding remain separate local delivery records.
