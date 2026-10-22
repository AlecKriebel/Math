# Convex-hull curve area: audited partial results

Problem **7000022 / AMR-069-0022**, rank **749**. Queue status **unsolved**, **5/5** substantive approaches used. Independent audit: **PASS for the frozen partial-results package**, with no required mathematical corrections. The full target remains unresolved. No novelty is claimed.

## Exact scope and conclusions

For a continuous rectifiable closed parametrized curve in Euclidean three-space, let L be its traversal length, including multiplicity. Its convex-hull surface area is ordinary boundary area in dimension three, **twice planar area** in dimension two, and zero in dimensions at most one. The unresolved target is S <= L^2/(2*pi), with equality for a circle.

- The proved universal partial bound is S <= pi*L^2/16, about 23.37% above the target coefficient. This is not claimed as a new or best-known bound.
- For hulls with at most four vertices, the stronger sharp bound S <= L^2/8 is proved; a square attains equality under the doubled-planar-area convention.
- The exact flattened-octahedron example refutes a length-nonincreasing fixed-hull boundary replacement. It does **not** refute the target inequality.
- A closed three-arm tree walk has positive convex-hull area and a zero-area Lipschitz disk filling. It refutes a spanning-disk-only reduction for the full nonsimple class, not the target inequality or a separately restricted simple-Jordan comparison.
- The **simple polygonal hull-boundary case is proved**, using an imported intrinsic disk inequality. The wider boundary regime is attributed to Zalgaller/Ghomi; its full regularity and nonsimplicity extensions are not independently proved here. This distinction is part of the audit scope.

Read [the authored proofs](geometry_7000022/PROOFS.md), [five approach families](geometry_7000022/RESEARCH_LOG.md), [independent adversarial audit](geometry_7000022_independent_audit/INDEPENDENT_AUDIT.md), and [current status](CURRENT_STATUS.json).

## Reproduce

Run `python3 verify_publication.py` from any working directory, using Python 3.10 or later and its standard library. The wrapper checks the strict file inventory, hashes, unchanged ZIP archives, all frozen members and manifests, current scope, author replay, independent replay with twelve author-certificate cross-checks, eight rejected false surrogate claims, and six rejected implementation mutations. Replays use temporary copies and do not overwrite frozen files. No source corpus or network is needed.

The wrapper also works under `python3 -O verify_publication.py`: explicit wrapper checks remain active and assertion-based verifiers always run in separate unoptimized Python processes. An optimized direct execution of the frozen scripts is not treated as verification. These are finite arithmetic and consistency checks, not formal certification of all analytic arguments or a proof of the general conjecture.

## Provenance and release boundary

Both nine-file freezes and their original archives are unchanged. Historical pending-audit and no-remote-write statements describe their preparation stage, superseded by the independent audit and this publication wrapper. Public source metadata records exact retrieval and inspection limits; bounded negative searches do not certify current openness. Source PDFs, extracts, raw corpus records and private coordination material are excluded.

The queue patch changes only this row's Status to `unsolved` and Turns to `5/5`. Every other queue byte, including Findings, Chat, DOI and the stale embedded header, is preserved. The publication manifest excludes its own hash; the final external receipt records it. Hashes establish byte consistency, not mathematical truth, novelty or authorship. No merge, release or external outreach is part of this publication.
