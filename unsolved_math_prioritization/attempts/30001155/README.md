# Area-refined Dirichlet spectral gap: audited partial results

Target **30001155 / OWR-3389-006**, rank 667. Disposition: **unsolved after five substantive approaches (5/5)**. The unrestricted area-refined lower bound, global equality classification, and classification of normalized extremizing sequences remain unresolved. No historical novelty or exhaustive current-literature-open claim is made.

## Accepted scope

- The inequality holds strictly for all nondegenerate rectangles and all triangles. The triangle implication uses the credited Lu–Rowlett theorem.
- It holds for ellipses with minor/major semiaxis ratio at least √15/4, with equality only for the circle within this range.
- Elongated rectangles attain the limiting constant in relative or diameter-normalized terms.
- A convex strip-limit example, using the credited Friedlander–Solomyak theorem, shows that local convergence to a strip alone does not imply normalized saturation. It is not a counterexample to the inequality.

Read [the complete authored proof](author/PROOF_AND_PARTIALS.md), [five-approach log](author/APPROACH_LOG.md), [full independent audit](independent-audit/AUDIT.md), and [corrections and guardrails](independent-audit/CORRECTIONS.md). The audit found no mandatory mathematical correction and accepted exactly these scoped deductions. All 14 author files, seven safe audit files, and both frozen archives are preserved byte-for-byte. Historical “audit pending” wording in the author freeze describes its earlier state; the separately supplied, hash-bound audit is complete.

## Numerical limitations

All 28 floating-point FEM runs had positive computed Ritz-gap margins, but differences of individual Ritz upper bounds do not bound the PDE gap from below. Matrix residuals concern only the finite-dimensional problems. The long-stadium sequence is explicitly underresolved, with normalized values about 132.02, 63.56, 41.25 and 33.66 as resolution changes. Boundary polygons change with refinement. No rigorous PDE enclosure, universal proof, or certified counterexample follows from these diagnostics.

## Portable replay

From this directory, with Python 3.10 or later:

    python verify_release.py

This standard-library check validates the exact file allowlist, hashes and sizes, both frozen archives against expanded files, the author and audit manifests, the author's 2,031 exact assertions, and the independent Bessel, Bernstein, π and ellipse-margin controls. Exact results are compared with the frozen outputs. For integrity checks alone:

    python verify_release.py --integrity-only

The optional numerical replay uses installed NumPy and SciPy, one OpenBLAS thread, and temporary copies:

    python verify_release.py --numerical

It requires byte-identical replay against the frozen numerical outputs, observed with Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0. Other numerical builds may differ. Numerical reproducibility is not PDE certification. The audit relies on published source theorems and did not independently re-fetch the complete external dataset or reconstruct prior repository searches. Literature searches are bounded. This is AI-assisted, unrefereed research, not a formal proof-assistant certificate.

## Frozen bindings and publication scope

- Author archive: 25,174 bytes; SHA-256 `02d7ebf85303b54d4643a79c266f0273d7881d80cddc0ddd215db2be2d35e6d9`.
- Audit archive: 13,179 bytes; SHA-256 `36542ded137aa3171c48f46a9bd659534cbf4d9567f2d3f4bb411a5551971b46`.

`PUBLICATION_MANIFEST.json` covers all other files in this directory. Only authored mathematics/code, the full safe audit, and public verification metadata are included. No source PDFs/text, source corpora, private sources, or private coordination files are included. The separate queue edit changes this target's Status and Turns only, preserving Findings, links, header and every other byte of the actual base blob. No queue command, merge, release, DOI or outreach is part of this draft.
