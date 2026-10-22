# Regular-pentagon surfaces: independently audited partial

Problem 5500072 / AMR-054-0072, rank 929. **Unsolved, 3/5 approaches used.**

Read [the proof note](author/proof_note.md), [the complete independent audit](audit/INDEPENDENT_AUDIT.md), and [exact acceptance](audit/EXACT_ACCEPTANCE.json).

## Accepted scope and remaining gap

The accepted model is a finite closed edge-to-edge spherical cellulation with isometric planar convex regular-pentagon faces, locally embedded at every abstract point and with distinct faces noncoincident. The accepted partial contains Euler/face-incidence identities, trivalent local rigidity, the obstruction to two cyclically adjacent trivalent neighbors of a four-valent vertex, a minimum-degree-two/cycle consequence in the valence-{3,4} subclass, and a continuous family of embedded local four-pentagon stars.

These facts do not establish a global dodecahedral decomposition or a closed counterexample. Local flexibility is not a global realization. No equivalence with broader geometric conventions, complete resolution, novelty, or exhaustive present-day openness is asserted. The primary 2009 source corrects the older TOPP great-dodecahedron immersion claim; source titles, URLs, hashes and inspection records accompany the authored reports.

## Review provenance correction

This is independent AI review with executable checks, not human peer review or formal verification. Only the UPDATED audit is current. [The correction note](audit/PROVENANCE_CORRECTION.md) and [actual five-file patch](audit/provenance_correction.patch) preserve the correction history. The superseded audit is not redistributed. Removed erroneous language occurs only on the deletion side of that historical patch.

The original author ZIP, external manifest and bootstrap are unchanged. Historical audit-pending/publication-not-performed fields remain preserved as records of their creation, and the updated exact acceptance supplies the later bounded verdict. No author mathematical correction was required. All seven frozen input files and 21 archive-member copies are preserved byte-for-byte.

## Reproduction and trust boundary

Use Python 3's standard library. Before executing publication_bootstrap.py, compare its exact byte count and SHA-256 against the external draft-PR verification receipt. Obtain the separately trusted PUBLICATION_MANIFEST.json SHA-256 there too. A substituted script and self-consistent manifest do not authenticate themselves.

After authenticating the bootstrap externally:

    python -I -S -B publication_bootstrap.py ABSOLUTE_PACKAGE_PATH EXTERNAL_MANIFEST_SHA256

For the complete 81-check audit replay, provide independently obtained read-only inputs:

    python -I -S -B publication_bootstrap.py ABSOLUTE_PACKAGE_PATH EXTERNAL_MANIFEST_SHA256 --catalog CATALOG --problems PROBLEMS --reports REPORTS --source-dir SOURCE_DIRECTORY

The source directory requires the five byte-pinned public files in audit/source_verification.json. Raw source documents/text/images and corpus contents are not included. Without these optional inputs, replay explicitly does not establish complete-corpus/source verification. The original 43 outer provenance tests are recorded in the frozen audit receipt and independently reproduced during publication; publication-boundary rejection controls are also run separately.

The wrapper verifies the exact tree and every file, rejects symlinks, authenticates both archives and every member, and replays authenticated code in relocated unrelated directories in normal and optimized isolated interpreters. Integrity and exact-arithmetic checks do not prove the global geometric claim. CI is reported separately for the exact remote head; zero CI checks is not a pass.
