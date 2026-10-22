# High-frequency coercivity: corrected auxiliary results

Problem 30003533 / OWR-15576-002, rank 1000. **Unsolved, 5/5.**

Read PUBLICATION_ACCEPTANCE.md, corrected/PROOFS.md, and independent_audit/AUDIT_REPORT.md. The source-free original and audit remain unchanged. corrected/ is reproduced exactly from original/ by independent_audit/CORRECTIONS.patch. Historical pending-review metadata in the author packet is preserved.

## Reproduction and trust

Python 3 standard library suffices. The full historical audit replay additionally needs the standard patch utility. No network, installation, or downloaded executable is used. Run as an unprivileged user; genuine read-only write-denial is tested. Baseline files must be mode 0644 and directories 0755; the separate read-only profile uses 0444 and 0555. Executable file bits are neither needed nor accepted.

Obtain the publication-manifest and BOOTSTRAP.py SHA-256 digests independently, for example from the draft PR's pinned metadata. Authenticate BOOTSTRAP.py, then copy it outside the packet. It pins VERIFY_PUBLICATION.py before execution. Run:

    python -I -B /trusted/BOOTSTRAP.py --packet /absolute/path/to/packet --expected-manifest <publication-manifest-sha256>

The default runs normal, -O and -OO replays and preserves packet bytes and modes. A selected mode uses --mode=normal, --mode=-O, or --mode=-OO. A fully read-only copy requires --filesystem-profile readonly. --check-only verifies strict identity, schemas and exact patch replay without invoking the control suites.

VERIFY_PUBLICATION.py validates an exact safe-path regular-file inventory, strict JSON and integer/Boolean distinctions, baseline/read-only modes, all nested frozen hashes and exact patch application before executing any delivered scripts. The original self-test's known read-only failure and permissive Boolean ordinal are reproduced by the unchanged historical audit runner in disposable fixtures. Corrected author replays and separate independent exact/numerical controls are tested. The historical runner's output-producing files are confined to disposable copies and compared with the frozen audit.

TEST_MUTATIONS.py is an external hostile-control driver. Authenticate and copy it and BOOTSTRAP.py outside the packet before testing; provide the independently trusted manifest. It tests malformed schema, inventories, modes, content, rehashed false claims, nested-manifest changes and a replaced verifier through that external bootstrap in normal, -O and -OO. The corresponding fixed receipt is MUTATION_RESULTS.json.

The scripts do not certify the boundary PDE or supply a smooth counterexample. Finite numerical checks are not exact checks. These AI-assisted, unrefereed partial results make no formal-proof, novelty, or exhaustive-current-literature claim.
