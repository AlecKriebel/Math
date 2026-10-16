# Verification materials: intermediate cylinder areas

These materials accompany the credited consequence note for problem 30006020 / OWR-14298589-005 (repository PR 218). They provide reproducible **finite algebraic controls**, source provenance, and an explicit map of what computation checks. The mathematical limit arguments and imported geometric theorems require the written proof and cited primary sources. A successful run is not a proof certificate, a novelty certificate, human peer review, or publication clearance.

From this directory, run:

```sh
python3 run_checks.py
```

Python 3.9 or later and its standard library suffice. No package installation, network request, credentials, external service, or source-PDF download is needed. The default command writes a JSON receipt to standard output and temporary files that are removed automatically. To retain a fresh receipt without modifying this sealed package:

```sh
python3 run_checks.py --receipt /absolute/path/outside-this-package/pr218-run.json
```

The runner first checks each listed payload's SHA-256 and size. It executes each preserved checker separately with assertions enabled, ignores `PYTHON*` environment settings, and compares its exact output to the recorded receipt. The bundled `RECORDED_RUN.json` describes an actual preparation run; a new run has its own time and environment fields. The static manifest excludes itself and that timestamped receipt to avoid self-reference. A changed or missing listed payload causes failure. The runner is intended to check accidental changes; an adversary who rewrites both a file and its manifest can also rewrite this local integrity record.

| Control | Mechanism and finite coverage |
|---|---|
| `controls/author_exact.py` | 3,439 rational assertions: ordered compositions through total size 10 for two truncated-height weight families; factorial and marked moments, simplex factors, graph prefactors and elementary identities. |
| `controls/partition_exact.py` | 2,032 rational assertions: full infinite-height zeta weights with common powers of pi cancelled, partitions through size 14, factorial moments, rational Beta-window means and Dirichlet normalization. |
| `controls/labelled_permutations.py` | 1,629 rational assertions after traversing all 46,233 labelled permutations of sizes 1 through 8; cotangent-derived true zeta weights, repeated ordered selectors through order 3, and a bivariate probability-generating function. |
| `controls/dvv_geometry.py` | Independent string/dilaton/DVV recursion and rational intersection numbers; 123 ordered composition cases in genus 2 through 5 with at most 3 loops, positive coefficients and agreement of pre- and post-integration factors. Additional finite rational identities and known low-genus values are checked. |

The first three totals sum to **7,100** exact assertions. The 123 DVV composition cases are reported separately rather than mixed into that assertion count. The unmodified DVV script also runs two floating-point sign checks and prints large-genus prefactor diagnostics. Those ordinary floating-point outputs are explicitly labelled and are **not** validated numerical enclosures or proofs of asymptotic estimates. The runner compares its rational records exactly; floating outputs are reported separately. No Monte Carlo estimate is required.

The four programs are unchanged copies of archived author and independent audit controls. `PROVENANCE.json` records their original paths, byte counts and hashes; `expected/` contains their frozen exact receipts. Historical program comments may refer to `CANDIDATE.md` or to an inherited review. Those refer to the original repository artifacts, not to an additional manuscript bundled here. The controlling accompanying note supplies the credited current presentation. `CLAIM_AND_EVIDENCE_MAP.md` explains the limits of these controls. `PRIMARY_INPUTS.json` contains only bibliographic metadata, URLs, source-byte hashes and read locations; no third-party PDF, extracted text or HTML is redistributed.

The theorem's scope is the principal holomorphic quadratic stratum `Q(1^(4g−4))`, uniform square-tiled isomorphism classes at fixed genus with the square cutoff tending to infinity **before** genus, unbounded cylinder heights, and maximal horizontal cylinders counted once and normalized by the entire surface area. Vertical cylinders have the same marginal law. At every `s_g → 0` with `g s_g → infinity`, compact-window counts converge to the Poisson process of intensity `dx/(2x)`, including fixed joint moments. The original window has limit `Poisson((log 2)/2)`. No claim is made for other strata, all directions simultaneously, diagonal square-count/genus limits, or either microscopic or macroscopic endpoints under this mesoscopic theorem.

The weighted permutation law is due to Delecroix–Goujard–Zograf–Zorich; the geometric formulas and uniformity come from their work and Delecroix–Liu, including the underlying intersection-number estimates credited there. Arratia–Barbour–Tavaré already provide the unmarked every-rate Poisson approximation; Arratia–Tavaré provide the factorial identity. The note derives the geometric moving-window consequence and its count-moment justification from these inputs. Self-contained controls do not remove those earlier attributions.

Delecroix–Liu's announced *Small components* project, Liu's 2022 thesis and the 2025 primitive-ensemble slides receive explicit credit. A complete public manuscript under the announced title was not located in the bounded audit as of 15 October 2026; that is a retained priority uncertainty, not proof of universal first priority. Fixed microscopic windows and the density's tail do not by themselves imply moving-window uniformity. The thesis's all-multiplicity law and the slides' primitive law differ. The OWR report's separate microscopic multiplier `4g−4` is not silently identified with the exact model's `6g−6`; no new microscopic law or correction is claimed.

AI tools were used extensively in development, drafting, literature review and adversarial checking. These computational and AI checks are not human peer review. This package does not establish that the accompanying preprint has passed its separately required final reviews, and it does not imply participation or endorsement by the cited researchers.
