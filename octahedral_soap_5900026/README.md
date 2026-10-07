# Octahedral soap-film problem: accepted corrected partial results

Problem **5900026 / AMR-058-0026**, queue rank **955**. **UNSOLVED, 5/5 substantive approaches completed.** Neither unrestricted ordinary nor real-coefficient minimum is determined.

## Accepted reading order

Start with the [corrected mathematical note](audit/MATHEMATICAL_NOTE_CORRECTED.md) and [full independent mathematical audit](audit/AUDIT_REPORT.md). The [original note](authored/MATHEMATICAL_NOTE.md), all frozen author artifacts, [original archive](AUTHOR_FROZEN.zip), [exact correction patch](audit/CORRECTION.patch), and all audit artifacts are preserved byte for byte. The original historical pending-review wording remains unchanged; the subsequent audit accepts the corrected formulation and the five scoped partial results. This was AI-assisted mathematical work and an independent AI-assisted audit, not human peer review or formal proof-assistant certification. No novelty claim is made.

The Section 0 correction is essential. In the relaxation, real normal chamber 3-currents V_s and real finite-mass pair 2-currents T_st are all supported in K = closure(Ω). The corrected text supplies the classical divergence-free-field pairing argument, with a cutoff equal to one near K. Generalized bounded fields require their own compatible trace or cochain pairing. The affine norm bounds are proved on K, not throughout ambient space.

## Accepted mathematical scope

For Ω = {x in R³ : |x₁| + |x₂| + |x₃| < 1}, with eight fixed labeled boundary-face traces and frame vertices ±e_i:

1. The candidate has six central kites, twelve outer triangles, five interior tetrahedral junctions, and area **4√2**. Its apex parameter a = 1/6 uniquely minimizes the specified one-parameter family.
2. It minimizes area among finite-perimeter partitions whose positive-area adjacencies lie in an explicitly specified **eighteen-edge graph**. Ten other pair bounds fail. This restricted theorem does not prove unrestricted minimality.
3. The full-pair constant and affine divergence-free dual optima are exactly **2√3** and **2√2 + 2/√3**, respectively. The affine proof covers the entire affine class by symmetry averaging.
4. The half-density mixture of the two parity candidates has mass **4√2**, with no positive-area cancellation. It is an admissible fractional competitor in the stated supported model, not a cheaper competitor or an integrality-gap theorem.
5. A sharp full-pair calibration cannot have all eight fields continuous at the center, subject to the stated comparison and compatible saturation hypotheses. Discontinuous calibrations and other proof methods remain open.

Thus, in the stated compact partition model and supported current relaxation,

    2√2 + 2/√3 ≤ inf A_real ≤ inf A_ordinary ≤ 4√2.

No equivalence with every Plateau spanning convention or unspecified mod-v model is asserted. For wire-edge length ℓ, areas scale by ℓ²/2, so the candidate area is 2√2 ℓ².

## Sources and access limits

The target is Problem 26 in Sullivan and Morgan, [Open problems in soap bubble geometry](https://doi.org/10.1142/S0129167X9600044X). Its exact item was inspected in indexed primary text. **No fresh verified original-problem PDF was obtained**; the retained file named soap-prob.pdf was HTML and was rejected as PDF evidence. No original-problem PDF hash is claimed.

The [source record](authored/SOURCES.md) and [independent source verification](audit/SOURCE_VERIFICATION.json) distinguish fresh verified PDFs, rehashed retained material, indexed text, and failed retrievals. Brakke's [dual paper](https://emis.de/ft/51988) and [Covers, soap films and BV functions](https://cvgmt.sns.it/media/doc/paper/3596/proc_pisa_2017_bpps.pdf) were freshly retrieved and inspected during the audit. Brakke's [example gallery](https://kenbrakke.com/evolver/examples/octa/octafilm.htm) makes a comparison only among displayed examples. The searches are bounded, not an exhaustive current-openness certification.

## Portable source-free verification

From any working directory, run these commands with the independently retained PUBLIC_MANIFEST.json SHA-256 printed in the draft PR description:

    python3 /path/to/packet/verify_publication.py --manifest-sha256 ANCHOR
    python3 -O /path/to/packet/verify_publication.py --manifest-sha256 ANCHOR
    python3 /path/to/packet/mutation_tests.py --manifest-sha256 ANCHOR

The wrapper uses only the Python standard library and no network, corpus files, source PDFs, or external patch program. It checks exact file and directory inventory, all byte counts and hashes, separately pinned original and audit manifests, the original ZIP contents, and exact zero-offset application of the preserved Section 0 patch. It replays the **884 author checks** and **1,075 independent checks** in normal and optimized Python and compares outputs byte for byte. It also replays the original fourteen integrity-mutation rejections. The publication mutation driver rejects changed payloads, manifests, patch and corrected copy, missing/extra files, an extra directory, and a symlink in both interpreter modes.

These are integrity and finite exact diagnostics supporting the written proof audit. They do not certify geometric measure theory, historical novelty, or an unrestricted minimizer. A manifest altered along with its files is not a trusted anchor; retain the published manifest hash separately.

Only authored mathematics, audit/correction text, replay code, public citations, and public verification metadata are included. Source documents, extracted source text, figures, dataset contents, and private coordination material are excluded. Outside this packet, only the existing queue's target Status, Turns, and Findings cells are changed; all other queue bytes are preserved.
