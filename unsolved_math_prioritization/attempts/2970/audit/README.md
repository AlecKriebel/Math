# Independent audit of KP-4.94 / 2970

The frozen mathematical report is accepted as partial/unresolved, with five approaches and no claimed resolution for an odd-r pair. Its nine-file, 67,843-byte input remains unchanged.

- `AUDIT.md`: full mathematical, source-hypothesis, and executable assessment.
- `independent_verify.py`: independent permutation-action reconstruction of the finite example and double-cover arithmetic checks. Run with Python normally, `-O`, or `-OO`.
- `independent_results.json`: deterministic output of the independent checker.
- `run_audit.py`: freeze checks, genuine non-root read-only execution, output comparisons, and fifteen adversarial mutations in three optimization modes.
- `audit_results.json`: complete harness output and all nine frozen-file hashes.
- `source_checks.json`: public bibliographic metadata, seven verified PDF identities, version checks, and inspection scope. No source bodies are included.
- `OPTIONAL_ORBIT_GUARD.patch`: two-line addition making the candidate's exact orbit sizes an explicit always-active check. It has not been applied to the frozen input.
- `optional_patch_results.json`: normal/optimized verification of the optional guard and its rejection of truncated closure.
- `MANIFEST.sha256`: hashes of these audit files, excluding itself.

To reproduce the full harness, run at UID/EUID 1000:

`python run_audit.py /path/to/frozen/public /path/to/new/writable/output > audit_results.json`

Choose a fresh output directory for every harness run. The input directory must be the original frozen candidate with manifest SHA-256 `a8cd4866d04bba62d53083e3e3f353e90974d955f09218f59244687f6d9152e4`.

The finite example is not a Horikawa monodromy computation. Finite parameter checks do not replace the symbolic argument. Source inspection does not prove exhaustive current literature coverage. This audit contains no surface-equivalence solution or unproved geometric realization claim.
