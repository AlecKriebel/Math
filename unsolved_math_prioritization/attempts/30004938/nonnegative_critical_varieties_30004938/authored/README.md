# Totally nonnegative critical varieties: five author approaches

Problem 30004938 / OWR-8415362-003.

**Disposition: unresolved after five substantive author approaches.** The source target is a homeomorphism preserving the specified boundary stratification, for every loopless bounded affine permutation. No proof or counterexample to that universal target is claimed. This package has not yet received independent acceptance review.

## Results worth preserving

1. `01_rank_extreme_reduction.md`: connected rank-2 and corank-1 diagrams must be top cells; all connected cases with at most four strands reduce to the established theorem. A connected non-top five-strand example blocks the attempted induction.
2. `02_bowtie_product_topology.md`: an exact Plücker calculation proves that the critical closure for fbar=(3,1,5,2,4) is homeomorphic to Δ₂,₃×Δ₂,₃. The required stratification identification is deliberately not claimed.
3. `03_failure_of_global_hypersimplex_quotient.md`: two explicit admissible sequences have the same global side-length quotient limit but distinct lower-cell critical limits. This rules out an unmodified extension of the top-cell quotient method, not polytopality itself.
4. `04_concave_energy_attempt.md`: a proved strict-concavity lemma for cyclic angle polygons yields a conditional interior-injectivity criterion. Its all-graph combinatorial hypotheses remain unproved, and it does not address the full boundary question.
5. `05_boundary_face_quotient_attempt.md`: a complete finite tube enumeration for the bowtie finds 37 facet tubes. A separately labeled exploratory tubing calculation predicts 49 product-face types. Universal surjectivity of individual face images and the global stratified claim remain open.

`SOURCE_AUDIT.md` fixes the exact scope, genericity conditions, primary-source versions and bounded current-literature findings. Source research and verification runs are not extra author approaches.

## Reproduction

The adjacent `checks/` folder contains portable Python scripts. `bowtie_minors.py` requires SymPy; the other scripts use the Python standard library. Run each script from any working directory. Outputs are written beside the scripts.

- `bowtie_minors.py`: all ten symbolic minors and the sine identity pass exact assertions.
- `verify_product_model.py`: inverse and projective-scale formulas pass at 225 pairs of rational triangle-grid points, including boundary points; two distinct boundary limits are checked numerically. The all-point proof is in approach 2, not inferred from the grid.
- `enumerate_strands.py`: exact integer chord enumeration through eight strands.
- `enumerate_bowtie_tubes.py`: exhaustive tube enumeration using a proved span bound.
- `enumerate_bowtie_faces.py`: exploratory finite-window acyclicity and image-type assignment only. Its limitations are carried in both the script output and approach 5.

## Acceptance checks requested

Independently verify the necklace sets and signs in approach 2, the common-factor/continuity argument, the reconstruction formulas on the entire product including its boundary, and the strict-concavity proof. Keep the exploratory face counts and conditional energy criterion out of any statement of established general polytopality. Do not change the problem's status to solved.
