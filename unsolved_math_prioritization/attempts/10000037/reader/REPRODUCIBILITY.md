# Reproducibility and integrity

## What is proved and what is tested

The authored analytic proof and its independent audits establish the infinite-event theorem. The two retained Python checking scripts recompute exact rational inequalities and finite graph examples. Finite tests do not establish infinite survival, the general dual crosscut lemma, global separation, novelty, or a literature-completeness claim.

Python 3.10 or newer and its standard library suffice. No network, source PDF, corpus, third-party package or stochastic simulation is needed. A Python interpreter and operating system compatible with the recorded version are recommended for byte-identical printed floating-point diagnostics; all mathematical pass/fail arithmetic uses exact integers or rationals.

## Replay after extracting the archive

From the extracted public directory:

1. Run `python3 -I -B verify_package.py`.
2. To authenticate against a separately trusted receipt, also supply `--manifest-sha256 HASH` using that receipt's manifest hash.
3. Run `python3 -I -B run_checks.py`.
4. Run `python3 -I -B check_tamper_controls.py`.

Redirect output outside the public directory. The package enforces an exact file set, so writing new logs inside it will correctly fail integrity verification. The supplied CHECK_REPLAY.json and TAMPER_CONTROLS.json are recorded baselines.

The replay runner first verifies package integrity, then executes the two original checkers in isolated temporary copies under normal, -O and -OO Python. All six outputs must match their retained baselines byte-for-byte. The generated validation report must match too. Both checkers use explicit exceptions rather than optimization-sensitive assert statements, and the runner statically checks that property. It verifies that the delivered source files remain unchanged. Tests can safely rewrite their own output files only within temporary copies.

## Fail-closed controls

The manifest verifier rejects missing, extra or modified files; extra directories; symlinks; nonregular filesystem objects; unsafe, duplicate, unsorted or self-referential paths; invalid hashes or byte counts; duplicate JSON keys; and a noncanonical manifest encoding. With an external pin it also rejects a replaced manifest.

The tamper checker exercises 15 cases in all three Python modes, including same-size byte changes, a FIFO, a replaced external pin, and malformed manifest variants. It works only in temporary copies. A successful integrity check does not prove the mathematics, and an unauthenticated replacement of both package and manifest is not defeated by internal hashing. Trust must ultimately come from a separately authenticated archive or manifest identity.

## Identity and version conventions

ORIGINAL_IDENTITIES.json records the reviewed original and delivered public byte count and SHA-256 for each selected input. Canonical construction, probability proof, validation, acceptance and checking files retain their exact reviewed bytes. The source contract and geometry report have clearly identified ancillary public-edition edits, with no changed mathematical content. The final acceptance audit's geometry pin refers to its original, not the adapted public copy; the identity record makes both explicit. The historical geometry cross-check is retained, while the final parity proof governs the survival claim.

The nested audit and validation manifests preserve their original reviewed identities. They are historical input records, not replacements for the complete public MANIFEST.json. The root manifest binds every delivered file except itself. Its canonical bytes are JSON with sorted keys, two-space indentation and one final newline. A separate archive receipt pins the root manifest and deterministic archive without a circular self-hash.

The archive contains only regular files under public/, with normalized ownership, file mode and timestamps. It excludes source documents, source text, corpus contents, superseded drafts and private records. Package preparation makes no repository or publication changes.
