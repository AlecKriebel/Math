# Frozen scoped fast-diffusion audit: row 1909 / ID 30001941

Qualified partial mathematical audit, not a solution, novelty certificate, or certification of current openness. The original six reviewed analysis files are preserved byte-for-byte. Source metadata is a projection of the recorded recovery gate: public scholarly identity, PDF hashes and byte sizes, inspection history, and limitations only. No copied source documents, dataset contents, private paths, or coordination material are included.

## Offline replay

Requires CPython 3 and mpmath 1.3.0 already installed. No network is needed or used.

    python -B replay.py
    python -O -B replay.py
    python -B mutation_tests.py
    python -O -B mutation_tests.py

The replay first inventories all entries using lstat-equivalent calls, including MANIFEST.json, before opening content. It rejects extra or missing files, directories, links, FIFOs and other nonregular entries. JSON duplicate keys are rejected. Manifest integer fields accept exact integers only, not bools or floats. Every listed payload is byte-count and SHA-256 verified. The external receipt pins MANIFEST.json and the ZIP; this external trust anchor is necessary because a manifest cannot authenticate itself.

Both diagnostic modes must reproduce the recorded JSON bytes exactly. Whole-module AST provenance is also checked; no assert transformation was necessary. Mutation tests run only in temporary writable copies and include both filesystem/schema rejection controls and direct mathematical mutants that bypass manifest rejection to test the substantive diagnostic. No actual sockets are created. This is not protection against an actively malicious concurrent filesystem owner or malicious replacement of the trusted Python runtime/dependencies.

## Boundaries

The diagnostic tests one explicit smooth anisotropic profile. It is not a formal PDE proof checker and does not independently certify the cited literature. The mathematical reports preserve the known logistic bound, scale positivity, tail-hypothesis separation, fixed/adaptive clock conversion, and conditional spectral-entry splice. Initial Fisher information can be infinite; positive-time identities and entropy continuity remain necessary. Apparent 2013 Remark 4 normalization inconsistencies do not invalidate the cited main inequality. The full sharp unrestricted target remains unproved by this packet; no claim about whether others have resolved it is made.

No repository publication or queue edit is performed by these scripts. The external receipt and test outputs describe packaging acceptance only, separate from the original mathematical acceptance report.
