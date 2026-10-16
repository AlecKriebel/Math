# Audited DGA equivalence partial results

Target 3023 / KP-5.16, rank 1057. Status: exhausted, 5/5. The general graded-commutative decision problem is unresolved. This is an unrefereed partial-results publication, with no novelty claim.

Read `ACCEPTANCE.md`, `evidence/REPORT.md`, `evidence/INDEPENDENT_AUDIT.public.md`, and the mandatory `evidence/PROVENANCE_ADDENDUM.md` together. The addendum identifies earlier same-target Aletheia work and substantial overlap in the valid regular-Koszul intermediate theorem. Five substantive approaches were completed before the audit found it. No validated match in the inherited corpus has been established.

The tensor undecidability theorem is imported from Manolescu–Rozenblyum. Its foundational Bokut input is not re-proved, and Bokut local source bytes remain NOT_RUN. Keep the distinctions among polynomial-exterior and sign-only conventions, augmentation and equivalence, regular Koszul models and arbitrary presentations, positive strict isomorphism and arbitrary-degree equivalence, and rational mixed-degree classification.

## Public files and provenance

- `evidence/REPORT.md`, `APPROACHES.json`, and the two exact checkers: unchanged authored proofs, approach records and code.
- `INDEPENDENT_AUDIT.public.md`: unchanged mathematics with artifact references and reproduction instructions redirected to this public slice.
- `PROVENANCE_ADDENDUM.md`, `PRIOR_SOURCE_METADATA.json`: late prior overlap and exact public provenance.
- `SOURCE_MANIFEST.json`, `SOURCE_COMPARISON.json`, `DATASET_MATCH_METADATA.json`: historical public verification metadata only. Fresh source/corpus replay is NOT_RUN.
- `AUDIT_RUNS.public.json`, `AUTHOR_RUNS.public.json`: complete historical stdout/stderr/exit records, with a source-input directory label generalized. These are historical evidence, not fresh source verification.
- `AUDIT_SUMMARY.public.json`, `STATUS.public.json`, `PUBLIC_SLICE.json`: explicit public metadata derivatives and fresh retained inventory.
- `expected/`: six entire source-free positive outputs for normal, -O and -OO.
- `verify_publication.py`, `mutation_tests.py`, `PUBLICATION_MANIFEST.json`, `BOOTSTRAP.py`: strict authentication, exact replay and negative controls.

No source or dataset body is included. Original full inventory manifests and the source-bearing historical runner are omitted; no stale inventory is presented as this public inventory. The original freezes remain locally preserved. The historical report/audit describe their original source-bearing executions; this README controls reproduction of the public slice.

## Reproduction

Requires Python 3.10+ standard library and real/effective UID 1000. Obtain the fixed BOOTSTRAP.py SHA-256 from the independently reviewed PR description or another trusted channel. Authenticate that file before executing it. A digest newly generated from an untrusted copy does not establish trust. For the controls driver, also authenticate mutation_tests.py against the pinned manifest before running it.

Make every publication directory 0555 and file 0444. Use a separate read-only current working directory; capture outputs outside the publication and working directory. Run each command in normal, -O, and -OO mode:

    python -I -S -B /trusted/copy/BOOTSTRAP.py /absolute/publication
    python -I -S -B /absolute/publication/mutation_tests.py --root /absolute/publication --bootstrap-sha256 TRUSTED_BOOTSTRAP_SHA256

The fixed bootstrap authenticates the verifier and manifest before executing verifier bytes, and requires its own exact copy in the packet. The verifier rejects unexpected members/directories, symlinks, special files, duplicate or extra manifest paths/keys, booleans or floats in integer fields, nonfinite values and altered accepted evidence. The controls driver tests self-consistent rehash substitutions, external bootstrap rejection before substituted wrapper execution, complete-output changes, and hostile imports in a relocated read-only packet.

Every replay compares full stdout and stderr, exact exits, and before/after inventories. In each mode it executes the native and independent positive checks, absent/corrupted-source controls, and all eleven semantic mutations. Mathematical outputs are identical to fixed baselines; each semantic rejection's entire diagnostic is checked. Actual append/create probes must fail. Read-only permissions are ordinary-process protection, not immunity from a privileged owner changing permissions.

All absent source objects and corpus are NOT_RUN. The fabricated corrupt-source marker is only a negative control and does not verify source provenance. Finite checks corroborate the authored proofs; they do not settle the unresolved target.
