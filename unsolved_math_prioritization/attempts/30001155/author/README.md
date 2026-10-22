# 30001155 / OWR-3389-006: area-refined spectral gaps

**Outcome: unresolved after five substantive approaches. Independent audit pending.**

The exact target is a proposed diameter-and-area lower bound for the first Dirichlet Laplacian gap of a planar convex domain. It is stronger than the already-proved fundamental-gap theorem. The source's π⁻² factor in the radicand was checked in the publisher PDF.

## Checked partial results

- The proposed inequality holds strictly for every nondegenerate rectangle; increasingly elongated rectangles attain its normalized limiting constant.
- It holds strictly for every triangle, as a corollary of the credited Lu–Rowlett theorem.
- A self-contained min–max comparison plus exact rational Bessel certificates proves it for ellipses whose minor/major semiaxis ratio is at least √15/4; equality in this range occurs only for circles.
- An explicit convex family, analyzed through the credited Friedlander–Solomyak theorem, converges locally to a strip yet has divergent diameter-normalized gap. Thus local strip convergence alone is not a saturation criterion.
- Twenty-eight floating-point FEM runs on convex polygons found no negative Ritz-gap margin. They are exploratory, not rigorous eigenvalue enclosures. The long-stadium sequence is underresolved, and its large refinement changes are preserved.

The full inequality, all non-disk equality exclusions, and classification of normalized extremizing sequences remain unresolved. These are scoped deductions and controls, without a historical novelty claim.

## Replay

Python 3, standard library only for the exact controls:

    python3 verify_exact.py
    python3 verify_manifest.py

The first command produces 2,031 exact rational assertions and should match exact_results.json. For the optional numerical experiments, install/use NumPy and SciPy from the normal environment, then run:

    OPENBLAS_NUM_THREADS=1 python3 numerical_challenge.py
    OPENBLAS_NUM_THREADS=1 python3 refine_stadium.py

Those numerical scripts recreate their JSON result files. Small floating-point variation is expected across BLAS/SciPy versions; exact byte identity is required only for the frozen artifacts, not regenerated floating-point output. Numerical replay after an author freeze should be performed on a copy if preserving the original manifest is required.

## Files

PROOF_AND_PARTIALS.md contains the exact target, complete authored partial proofs, literature dependencies, constant certificates and limitations. APPROACH_LOG.md records the five approaches and remaining gaps. SOURCE_VERIFICATION.json contains public URLs, titles, PDF byte counts/hashes and inspection metadata. DATA_PROVENANCE.json contains public dataset verification metadata. No source PDFs, extracted source text, source corpora or private coordination records are included in this packet.

This research is AI-assisted and unrefereed. The exact controls are not a formal proof assistant. An independent audit must assess the analytic reasoning and cited theorem applications.
