# The least-period criterion for outer focal products in elliptic billiards

Alec Kriebel, ORCID 0009-0001-9320-500X. Research note dated 16 October 2026.

The paper proves the following precise classification. For a noncircular ellipse, a fixed proper nested nondegenerate confocal elliptical caustic, and least period N at least three, the ordinary product of the distances from consecutive boundary-tangent intersections to either original focus is phase independent if and only if four divides N. All admissible coprime windings are included. Repetition cannot restore phase independence. The circle and hyperbolic or degenerate caustics are excluded from this classification.

The positive direction is the primitive interpretation of k115 and is also proved by Alper Ferudun, *Focal Distance Products of Outer Elliptic Billiard Polygons*, DOI https://doi.org/10.5281/zenodo.23093258. Its proof mechanism and explicit constant overlap substantially and are credited in the note. The original submitted positive proof is retained as historical text; the converse was added and audited on 16 October. The October 1 GitHub PR creation and October 2 competing deposit/registration are observed records, not proof of first disclosure or independent discovery. Historical novelty remains unestablished. Read the paper for the current theorem and qualifications; dated audit/historical texts do not supersede it.

AI tools were used extensively in discovery, extension, drafting, source checks and adversarial audits. This is an unrefereed preprint with no conventional independent human peer review or formal proof-assistant certification claimed.

## Files and scope

- `outer_focal_period.tex` is the self-contained LaTeX manuscript, using a credited published canonical billiard parametrization and standard Jacobi facts. The PDF is a separate upload.
- `verification/exact_certificates.py` has 306 explicit-guard exact checks. It verifies coefficient identities and physical Euclidean reflection/tangency at two phases each for N4, N8 and N6. It verifies the unequal N6 products 20736/343 and 6912/125 and their repetition obstruction. The N8 fixture is a rescaling of Ferudun's fixture and is a control, not a novelty claim.
- `verification/parity_controls.py` has exact symbolic factorization checks, 1,521 exact rational divisor cases (primitive windings, N3 through N100), and 117 numerical families (all primitive windings for N3 through N16, three moduli, 13 phases and both foci). It solves the two actual tangent equations. Numerical precision is 100 decimal digits. These samples are diagnostics, not a proof of a universal theorem or historical novelty.
- `expected/` contains the retained results for the pinned dependency versions.
- `proofs/`, `history/` and `priority/` contain selected authored derivations, historical proof and bounded audit/source/query ledgers. They are unaltered copies. Relative paths and platform-specific commands in those historical audit texts describe the original working environment; use the portable commands below for this deposit. `SOURCE_ORIGINS.json` authenticates their exact repository origins and bytes. Third-party PDFs, raw source extracts, credentials, API responses and dependency packages are excluded.
- `provenance/` records editorial scope and the observed chronology, with its limits. Earlier frozen audit decisions are preparation checkpoints, not a representation that a public upload had already occurred.
- `metadata.json` is the intended deposit metadata; `MANIFEST.json` hashes all ZIP payload files except itself. The repository retains an external SHA-256 seal for the three upload files; that seal is not included in this ZIP.

## Reproduction

Python 3.10 or later and these pinned packages are required:

    python3 -m venv /tmp/outer-focal-venv
    /tmp/outer-focal-venv/bin/python -m pip install -r verification/requirements.txt
    /tmp/outer-focal-venv/bin/python -B verification/exact_certificates.py --output-dir /tmp/outer-focal-exact
    /tmp/outer-focal-venv/bin/python -B verification/parity_controls.py --output-dir /tmp/outer-focal-parity

Use fresh output directories if preserving previous replays. Both scripts use explicit exceptions for substantive checks; neither relies on `assert`. Repeat with `-O` to check the same behavior under optimization. In either mode, adding `--self-test-failure` must exit nonzero with `deliberate explicit-guard failure`. This is a diagnostic guard test, not an expected successful verification run. The scripts require no repository checkout, network access after installation, or local audit folders. They write only to the chosen output directory and print a result summary (the exact checker prints its full certificate).

Compare the generated JSON semantically with the corresponding `expected/` file. Root replays using SymPy 1.14.0 and mpmath 1.3.0 matched every field in both normal and optimized modes. Arbitrary-precision floating-point results are not interval certificates. Near the circular limit a nonconstant product can have very small sampled variation; the proof's nonzero-divisor argument establishes nonconstancy without a numerical detection threshold.

Legacy original-submission verifiers used Python assertions and could display a misleading PASS under `-O`; they are not the portable verifiers in this deposit. Their original bytes and the audit of that limitation remain in the GitHub research archive rather than being silently rewritten.

Compile the manuscript with a standard LaTeX installation (for example, `latexmk -pdf outer_focal_period.tex`) or Tectonic. No additional figure or bibliography files are required. Checksums establish file identity, not mathematical correctness; the written proof must still be assessed.

## License

The manuscript, authored supporting text and verification code in this deposit are made available under Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/. Retained references and facts about third-party works do not transfer ownership of those works. No third-party full text or dependency implementation is redistributed.
