# Modern K3 4.122: audited branching-surface obstructions

**UnsolvedMath ID 2998, rank 695. Disposition: unsolved, 5/5 approaches.**
This draft retains necessary conditions and failed construction routes. It does
not settle the existence of a fixed universal branching surface, certify novelty,
or establish that the original problem is globally open in the literature.

## Controlling scope and results

The deductions apply to a fixed finite disjoint union of closed, embedded,
locally flat surfaces in the four-sphere, in the ordinary smooth/locally flat PL
branched-cover category with standard transverse power-map models. The surface
is the **exact active branch locus**: every downstairs component has nonidentity
meridional monodromy in each cover. Unbranched sheets over an active component
are permitted. Covers of the connected test manifolds have connected total space.
No singular, immersed, wild, arbitrary two-complex, or inactive-dummy-component
extension is claimed.

In that scope, universality would require:

- Components with both positive and negative normal Euler number.
- Positive Euler-characteristic mass at least three, hence at least three components.
- A large complement group: a finite-index subgroup must surject onto the rank-two free group.
- Unbounded degrees; simple covers alone cannot suffice.

Doubling the known orientable universal ribbon surface from the four-ball
produces only zero-signature covers and cannot establish the closed universal
surface theorem. These are necessary conditions and obstructions, not sufficient
conditions or a general nonexistence theorem. Surviving scalar profiles do not
construct an embedding, a complement representation, or a manifold.

Read [the authored arguments](author/RESULTS.md),
[five approach records](author/APPROACH_LOG.md), and
[the independent audit](audit/AUDIT.md). Imported theorems of Viro,
Geske–Kjuchukova–Shaneson, Iori–Piergallini, Piergallini–Zuddas, and
Bais–Piergallini–Zuddas are credited dependencies with the inspection limits
recorded in the packets. The variable-surface representation and relative
four-ball theorems do not provide one fixed embedded closed surface.

The GKS proof's final display retains upstairs self-intersection notation but
has a denominator inconsistent with its theorem and Viro's formulas. The
upstairs coefficient has denominator 3; the downstairs immersion formulation
has denominator 3k. The frozen author packet already uses the correct conversion.
The audit found no substantive mathematical correction to make and does not
claim an official erratum.

## Controlling release verification

The author and audit directories are exact frozen snapshots: nine author files
and twelve audit files. Their historical statements describe those earlier
stages; the audit has now been completed and accompanies this release.

**The audit's `binding_checks.py` and `verify_audit.py` are controlling.** The
historical `author/verify_manifest.py` incorrectly excludes any file with the
basename `AUTHOR_MANIFEST.json`, including an unexpected nested manifest. It is
preserved unchanged for history and is not a release gate. The strict replacement
rejects the exact `unlisted/AUTHOR_MANIFEST.json` case, missing or altered bytes,
payload and manifest symlinks, and every unlisted file. No mathematical correction
is needed because the actual frozen tree contains no such extra file.

From this directory, with standard-library Python 3:

```sh
python -B verify_release.py
```

This checks the release file set and digests, pins both original manifests,
runs the controlling audit verifiers, exercises seven temporary-copy integrity
attacks, and replays both arithmetic scripts with byte-identical outputs. The
author script runs only in a temporary copy because it writes its result file.
No original frozen bytes are rewritten. The independent controls include ten
mathematical negative controls. Do not use `python -O`; optimized execution is
deliberately rejected because the preserved scripts use assertions.

The underlying read-only binding checks are also directly reproducible:

```sh
python -B audit/verify_audit.py --author author
python -B audit/binding_checks.py --author author --negative-controls
```

Finite arithmetic checks are not geometric realization, proof of the imported
topology theorems, formal verification, human peer review, or a CI result.

## Distribution

Only authored work, audit/code and public verification metadata are included.
No source PDFs, extracted source text, page images, raw dataset records, or
private coordination are included. Scholarly titles, public URLs, source hashes,
sizes and bounded retrieval/inspection history are retained for provenance.
The separate queue edit changes only ID 2998's Status and Turns; all other queue
bytes, including Findings, Chat, DOI and its existing embedded header, are preserved.
No merge, release, DOI or outside outreach is part of this draft.
