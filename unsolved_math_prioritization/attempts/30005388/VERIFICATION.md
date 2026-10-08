# Current reproduction and trust boundary

Python 3.10+ and the standard library suffice. Review the external BOOTSTRAP.py hash, then place a trusted copy outside the candidate. Its fixed pins authenticate the manifest, verifier, and controls harness before execution. The manifest binds every other delivered file, including acceptance, status, historical evidence, references, and pre-seal receipts. The candidate must contain exactly the listed flat inventory, with no symlinks, hard links, directories, or special files. This is a static artifact-integrity boundary, not protection against the owner concurrently changing its files.

Use a fresh copy with every file mode 0444 and the directory mode 0555. Run as actual UID=EUID=1000, never root. For each of the normal, -O and -OO modes, execute:

    python -I -S -B TRUSTED_BOOTSTRAP.py PACKET_DIRECTORY
    python -I -S -B TRUSTED_BOOTSTRAP.py --controls PACKET_DIRECTORY

Insert -O or -OO before TRUSTED_BOOTSTRAP.py for the optimized modes. The checker enforces real/effective identity, isolation/no-site/no-bytecode flags, every permission bit, denied create/append probes, and unchanged whole-delivery hashes.

Each current mathematical script runs freshly in the selected mode. Its entire stdout and stderr must match its pinned mode-specific reference bytes, with no normalization. A recursive exact-type JSON comparison additionally rejects booleans substituted for integers, floats substituted for integers, missing/extra values, duplicate keys, malformed JSON and nonfinite numbers. The hardened result also matches EXACT_CHECK_RESULTS.json, and the independent result matches INDEPENDENT_EXACT_RESULTS.json.

The controls include each checker’s intended built-in negative controls, actual single-site source-code mutations of the tensor correction and literal maps, long-box differential/parity, surgery and determinant checks. Mathematical source mutants run directly after exact mutation application on disposable read-only copies; a manifest mismatch is not counted as semantic rejection. The exact expected ValueError must be observed.

Other controls change every delivered member, remove/add members, attempt resealing against the fixed external bootstrap, exercise schema and full-output comparisons, and run with hostile working-directory modules and Python environment variables. Hostile baseline stdout and stderr must equal the clean baseline exactly, without a sentinel firing.

PREPARATION_CONTROLS receipts predate the final seal. They are labeled pre-seal and bound by the final manifest. Final whole-delivery receipts remain external and their SHA-256 values are provided in the review/PR body. Neither stage is a proof of all knot-theoretic input theorems.

NOT_RUN: omitted original-verifier replay, historical false-acceptance replay, historical contextual patch application, source-body replay, dataset replay, and formal proof-assistant verification. Source metadata records historical inspection, not a fresh source retrieval or new worldwide-status search. Remote publication/readback/CI are outside local verification and are not implied by PASS.
