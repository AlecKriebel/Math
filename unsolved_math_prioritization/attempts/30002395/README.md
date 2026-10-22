# Dini spaces as primitive spectra: corrected partials

Problem 30002395 / OWR-12591-005, rank 985. **UNSOLVED, 5/5 substantive approaches.**

Read [the corrected complete proof](independent_audit/corrected/PROOF.md), [the independent AI audit](independent_audit/AUDIT.md), and [the acceptance boundary](ACCEPTANCE.md). The original packet remains under public/; its unqualified Turn 2 sentence is historical and must be read with the supplied correction. CORRECTION.patch is the actual two-file patch, retained in independent_audit/ alongside a separately manifested corrected packet. Historical statements about no remote publication describe the pre-publication snapshots.

Accepted partials include Alexandrov realization, open-cover permanence and its locally Hausdorff subclass, the credited doubled-limit AF example, and obstructions to particular proposed constructions. No universal answer or novelty is claimed. Sobriety, second countability and local quasicompactness remain part of the intended Dini assumptions. Harnisch–Kirchberg's realization theorem is an external dependency.

## Portable verification

Use a trusted Python 3 interpreter and the standard `patch` utility. No third-party Python package, network, source PDF, source extraction or dataset is required. First authenticate verify_publication.py, mutation_tests.py and PUBLIC_MANIFEST.json against independently retained SHA-256 pins, such as the accompanying PR description. A script cannot establish its own trust. An attacker replacing both a script and its local manifest is outside that self-authentication boundary.

From any working directory, run:

    python3 -I -S -B /path/to/verify_publication.py EXTERNAL_MANIFEST_SHA256 /path/to/packet
    python3 -I -S -B -O /path/to/verify_publication.py EXTERNAL_MANIFEST_SHA256 /path/to/packet
    python3 -I -S -B -OO /path/to/verify_publication.py EXTERNAL_MANIFEST_SHA256 /path/to/packet
    python3 -I -S -B /path/to/mutation_tests.py EXTERNAL_MANIFEST_SHA256 /path/to/packet

The closed inventory checks recursive membership, permitted directories, regular files, duplicates, paths, byte counts and digests, including separately frozen original/audit/corrected identities. Replay occurs in a temporary copy. Actual child-process probes verify optimization, isolation, site suppression and no-bytecode flags. Author, independent and correction-scope results are compared with frozen receipts; only explicitly checked nonnegative timing measurements are removed from the independent comparison. The correction replay actually applies the unified patch.

The author's legacy manifest verifier uses assert and loses those statements under -O/-OO. The publication wrapper's explicit guards, independent checks and mathematical check helpers stay active. Optimized runs are supplementary and never replace the normal run. Finite checks do not prove infinite compactness, sobriety, Polish completeness, operator-algebra realization, or novelty. PDF metadata is cross-compared; absent PDF bytes are not revalidated.

The mutation suite verifies original and relocated packets at all three optimization levels, then rejects payload, inventory, symlink, path, manifest and frozen-manifest laundering corruptions. Keep output outside the frozen packet. See [research log](RESEARCH_LOG.md) for scope and checkpoints. No source documents, copied source extracts, datasets or private coordination material are included.
