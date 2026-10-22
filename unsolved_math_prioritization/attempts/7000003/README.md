# Fixed-boundary annulus rigidity: audited partial results

Problem 7000003 / AMR-069-0003, queue rank 748. **Unsolved, 5/5 turns.**

The full question asks for global extrinsic isometric rigidity of negatively curved annuli with two fixed convex planar boundary curves. Global rigidity means uniqueness up to Euclidean congruence. This packet does not prove that statement or provide a qualifying counterexample. Infinitesimal rigidity and the absence of one particular flex are weaker conclusions. No novelty, priority, human peer-review, or formal proof-assistant certification is claimed.

## Retained scope

The five approaches supply a boundary rotation-field lemma; an all-Fourier-mode infinitesimal theorem for a rotational base with nowhere-zero meridian height derivative; the exact catenoid–helicoid period obstruction; a graph/projection obstruction; and a characteristic return multiplier with an explicit negatively curved ribbon control. The nonlinear rotational comparison stays within its fixed-axis, fixed-coordinate class. No arbitrary isometric immersion is assumed rotational.

Both boundaries of the explicit ribbon are nonplanar, so it is not a counterexample. Its Frenet director N differs from the ribbon surface normal, which is B on the core. The independent repeated-binormal computation makes the interior Gauss map noninjective. That excludes extensions containing this exact ribbon from the narrower 2025 tangent-boundary class, not from every annulus with merely convex planar boundaries. The global and boundary-realization gaps remain unresolved.

## Preserved evidence

All seven author files in `geometry_7000003/`, all eight audit files in `geometry_7000003_independent_audit/`, and the 15,539-byte author archive are unchanged. The audit gives a scoped pass with no mandatory corrections. References to pending audit or no remote writes in frozen artifacts are historical. The completed review is `geometry_7000003_independent_audit/AUDIT.md`.

The author replay has 24 algebraic assertions and 8 rejected corrupted controls. The independent replay has 45 assertions, including integrity checks, and 9 rejected mutations. Analytic proof review is distinct from these finite checks. Four public PDF hashes and byte counts were independently matched during the audit; only public bibliographic and inspection metadata are included. A bounded literature search does not certify that no resolution exists elsewhere.

## Offline verification

Requires Python 3 and SymPy (tested with 1.14.0). From this directory, or using the absolute script path from another working directory:

    python3 -B verify_publication.py
    python3 -B -O verify_publication.py
    python3 -B verify_publication.py --integrity-only

The wrapper checks the exact inventory, pinned frozen manifests/archive, archive members, unchanged status, and both replay outputs, without network access. It uses explicit failures rather than assertions for publication-integrity enforcement, including under Python optimization. The original author manifest checker is replayed without optimization because it uses assertions; its frozen bytes are not edited.

This publication contains authored proofs/code, audit, and public verification metadata. It excludes source PDFs, extracts, raw datasets, and private coordination. The separate queue patch changes only this row's Status and Turns; all other bytes, including Findings, Chat, DOI, and the embedded historical header, remain unchanged.
