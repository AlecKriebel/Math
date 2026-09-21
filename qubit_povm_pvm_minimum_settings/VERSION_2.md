# Version 2 local release candidate

This is a concrete local package for review, not a published immutable release. No version-2 DOI has been assigned here. Existing Zenodo records refer to the historical version 1.1.0 artifacts.

## Changes from the current public archive

The principal conclusions now have Lean proofs, with explicit stochastic-output, arbitrary finite-label, and arbitrary complex-Hilbert-space dimension-at-most-two correspondences. The new proofs preserve actual Born behaviors and ordinary finite convex hulls. A common selector chooses complete state-and-measurement strategies across all inputs and both parties.

The manuscript now identifies the formal replacement arguments: deterministic score gaps replace the general duality/KKT route; feasible curves and an exact score-gap identity replace the full manifold/Hessian/inertia route; an operator sum-of-squares certificate proves the global PVM bound. Retained auxiliary manuscript mathematics is identified separately in the coverage map. The Lorentz signature condition remains explicit. The related-work attribution and comparison, deterministic-reset positivity proof, and cone-circuit exposition have been corrected.

See [the formal coverage](bell_lean/docs/CERTIFIED_COVERAGE.md), [model conventions](bell_lean/docs/MODEL_CONVENTIONS.md), and [verification certificate](bell_lean/CERTIFICATION.md). The direct current-archive comparison and file hashes are in [archive evidence](version2_completion_20260921/ARCHIVE_COMPARISON.md).

## Reproduce from a clean extraction

Install the pinned Lean 4.19.0 toolchain, Git, Bash, Python (reference 3.14.6), and Tectonic 0.16.9. Install `requirements.txt` and `bell_lean/requirements-preflight.txt` into a virtual environment. Put the pinned Lean/Lake binaries on PATH. The archive includes no compiler or dependency cache.

With online dependency acquisition:

```sh
python reproduce.py --bootstrap
```

With a separately prepared directory containing the nine pinned dependency checkouts and their compiled cache:

```sh
python reproduce.py --dependency-cache /absolute/path/to/prepared/.lake/packages
```

The second command reuses only dependency artifacts. It creates fresh project build outputs and verifies dependency commits and tracked-file cleanliness. Compiler/runtime and dependency-cache producers remain trusted; this is not an independent rebuild of Mathlib. The command does not impose network isolation.

The wrapper first checks the exact shipment file membership and SHA-256 manifest, then runs the exact manuscript artifacts, compiler-free verifier tests/algebra, the complete fresh Lean build, every statement contract, all public theorem axiom audits, source/dependency stability checks, and warning-free builds of publication and review PDFs. Each step must succeed. `reproduction_runs/<timestamp>/receipt.json` and the identified `bell_lean/reports/runs/<id>/` contain authoritative output. Reproduction rewrites reports and PDFs; verify shipment hashes before running, and use a new extraction for another shipment-integrity check. PDF byte identity is not promised across TeX environments; rebuilt source and warning checks are recorded.

## Contents and exclusions

The source, PDFs, exact artifacts, Lean proofs, verifier, pinned manifests, historical input archives required by audits, and public review evidence are included. The root SHA-256 manifest binds all shipped files. Historical run receipts remain historical and are not evidence for changed inputs. Local build caches, compiler binaries, virtual environments, discovery work directories, and private submission correspondence are excluded. Source code including Lean is MIT licensed; manuscript and mathematical data are CC BY 4.0; the bundled lineno package retains its own LPPL notice.
