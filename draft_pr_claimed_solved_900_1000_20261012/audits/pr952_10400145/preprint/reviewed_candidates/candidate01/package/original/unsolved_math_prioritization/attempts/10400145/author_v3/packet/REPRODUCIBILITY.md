# Replay and trust boundaries

This packet contains authored analysis, public source metadata and a finite algebra checker. No source PDFs, extracted third-party text, dataset contents or private coordination files are included.

The final release has an external AUTHOR_MANIFEST.json, bootstrap.py and a separate EXTERNAL_PINS.json. Obtain the manifest and bootstrap SHA-256 pins independently from the delivery/audit record. Do not treat a mutable pin file delivered beside mutable code as a self-authenticating trust anchor. After checking the bootstrap SHA-256 against that independent record, run:

    python -I -S -B bootstrap.py packet
    python -I -S -B -O bootstrap.py packet
    python -I -S -B -OO bootstrap.py packet

The bootstrap pins the manifest hash, rejects malformed metadata and unexpected/symlink payloads, checks the exact file inventory, byte counts and SHA-256 hashes, and only then invokes the pinned checker with isolated Python, without site imports or bytecode output. The checker uses explicit exceptions rather than assertions. Normal, -O and -OO outcomes must agree byte for byte with DIAGNOSTICS.json.

The finite computations check the generic three-node first-jet identity, the −6 linear Poincare coefficient, eight illustrative higher-order summands, and the nonzero second difference −12. The paper proves the general vanishing of all remaining summands; the finite sample is not its proof. The program does not establish correctness of any primary-source theorem or normalization bridge.

The external replay harness runs the actual final read-only release as a non-root user, tests that writes fail, and makes only disposable mutation copies writable before changing them. It also tests stale hashes, altered checker/bootstrap, missing and extra payloads, symlinks, duplicate keys, bad JSON types, wrong mathematical data, malformed manifests, hostile imports and hostile working directories. Control receipts describe observed execution, not a formal verification of the mathematics or a claim of tamper resistance against a process concurrently replacing already-checked files. SHA-256 integrity checks require a trusted initial bootstrap hash and a non-concurrently-mutated filesystem.
