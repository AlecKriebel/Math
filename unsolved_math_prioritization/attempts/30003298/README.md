# Mapping-class cohomology: accepted genus-two corollary

Problem 30003298 / OWR-15177-016, rank 997. **Unsolved, 5/5 approaches.**

The accepted theorem gives infinite rational rank of H^(4g-5)(Gamma; H_(2g-2)(C_g; Z)) for every g>=2 and every torsion-free finite-index subgroup Gamma of orientation-preserving Mod_g. It answers the requested degree 2g-1 exactly when g=2. The higher-genus requested degree remains unresolved.

The proof is a corollary of published Harer/Bieri–Eckmann duality and Fullarton–Putman finite-image quotients. No mathematical correction patch is required. The Avramidi boundary route is conditional and its manuscript's recorded under-revision status is disclosed; it is not an input to the main theorem. No novelty claim is made.

## Contents

- `public/`: byte-identical ten-file author freeze, including the historical pending-review field.
- `audit/`: byte-identical seven-file independent audit and acceptance. This sibling layout preserves the scripts' relative-path bindings.
- `PUBLICATION_ACCEPTANCE.md`: publication disposition and limitations.
- `VERIFY_PUBLICATION.py`: strict source-free inventories, independent frozen anchors, and replay.
- `TEST_MUTATIONS.py`: disposable-copy malformed-input and external-wrapper-bootstrap controls.
- `MUTATION_RESULTS.json`: observed mutation results.
- `PUBLICATION_MANIFEST.json`: exact file hashes, sizes, and baseline modes, excluding itself.

No source PDFs, source extracts, dataset contents, private sources, personal data, or coordination files are included. Authored exposition, public bibliographic links, and verification metadata are included.

## Reproduction and trust boundary

Use Python 3.10+ with only its standard library. Obtain the wrapper SHA-256 and publication-manifest SHA-256 from the independently retained PR description or receipt, outside the packet. Authenticate `VERIFY_PUBLICATION.py` **before execution**, then run:

    python -I -B VERIFY_PUBLICATION.py --expected-manifest EXTERNAL_MANIFEST_SHA256

Default replay runs normal, -O and -OO. To optimize the outer wrapper too, repeat with `python -O -I -B` and `python -OO -I -B`. `--mode=normal`, `--mode=-O`, and `--mode=-OO` select one child mode. `--check-only` checks identity without executing the frozen diagnostics.

Baseline files are 0644 and directories 0755. For a separately relocated read-only packet with files 0444 and directories 0555, add `--filesystem-profile readonly`. Its contents and all frozen manifest pins remain identical. Full replay executes the frozen verifiers on a temporary read-only copy and performs actual rejected file-creation and append probes. The historical mutation harness starts from a separate temporary writable copy because it preserves source modes when preparing mutations; its own read-only relocation probes remain enabled. Both copies retain the frozen bytes and anchors. Run under a non-root user so write permissions are meaningfully enforced. Scripts write only in temporary directories.

After authenticating the test harness from the verified inventory, run:

    python -I -B TEST_MUTATIONS.py --packet . --expected-manifest EXTERNAL_MANIFEST_SHA256 --expected-wrapper EXTERNAL_WRAPPER_SHA256

The bootstrap checks the external wrapper digest before executing candidate wrapper bytes. Manifest-only rebinding cannot authorize a changed frozen proof or audit. Replacement of both independently trusted anchors is outside the threat model. These controls do not turn arbitrary prose into a machine-checked theorem.

The diagnostic counts are 13,830 author checks and 4,398 independent checks per mode. The historical independent harness includes 40 hostile controls per mode and the author harness's 20 per mode. AI-assisted and unrefereed; no human peer review or formal proof-assistant verification is claimed.
