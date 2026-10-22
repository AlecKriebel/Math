# Contact-process threshold separation: five-approach partial investigation

**Problem:** 30004594 / OWR-4990373-008, rank 780.

**Disposition:** unresolved, five substantive approaches used. No candidate solution, novelty claim, external acceptance, or independent-review pass is asserted.

The original question asks whether the nearest-neighbor contact process on each Z^d, d>=2, survives at some rate for which the infected set in the upper invariant measure has no infinite nearest-neighbor spatial component. A September 2026 [Fernley-Jacob preprint](https://arxiv.org/abs/2609.09972) explicitly retains this lattice question as open while proving a regular-tree result. The [Rath-Valesin theorem](https://arxiv.org/abs/1912.09825) addresses sufficiently spread-out infection and does not settle the classical kernel.

## What is established here

- An authored proof of a credited standard Bernoulli upper comparison and the one-dimensional boundary case
- The exact stationary occupied-set moment hierarchy and adjacent-site conditional identity
- A symmetric, translation-ergodic, positively associated percolating field whose density tends to zero, illustrating an invalid inference rather than a contact-process counterexample
- A rigorous finite-radius graphical criterion and proof that this particular coloring/union-bound criterion cannot certify nonpercolation at any lambda>=1, hence at any supercritical rate
- A geometric obstruction to a bounded-length injective regular-tree embedding shortcut
- A 511-state finite dual-exit calculation reduced to 101 dihedral orbits, solved and checked using exact rational arithmetic

The proof's remaining gap is explicit: no supercritical rate has been certified spatially nonpercolating in the actual nearest-neighbor process.

## Reproduce the finite checks

Python 3.10 or later, standard library only:

    python verify.py --output replay.json
    cmp replay.json verification_results.json
    python verify_manifest.py

The recorded run passes 72,940 exact assertions. These include pointwise generator algebra, a counterexample cylinder distribution, disjoint graphical interiors, a radius-criterion obstruction, all full-state residuals of the finite exit chain, and monotonicity. The assertions corroborate the written proofs; they do not certify the unsolved infinite-volume target. A replay generated inside this folder is an untracked convenience file and is not part of the frozen manifest.

## Sources and scope

The exact OWR question is on printed p. 175 of [OWR 4/2021](https://ems.press/content/serial-article-files/46882). The earliest checked formulation is Section 8, Question 2, p. 242 of [Liggett-Steif (2006)](https://www.numdam.org/item/10.1016/j.anihpb.2005.04.002.pdf). The complete public corpus files were rehashed against the repository's immutable dataset manifest, and the selected statement hash matches the descriptor. No prior report entry exists under the exact problem code. Actual repository-tree inspection and targeted PR, commit and branch searches did not locate a prior attempt on this target; limitations are recorded.

The [all-dimensional Beekenkamp sharpness preprint](https://arxiv.org/abs/1807.05591) is withdrawn and is not a theorem input. The valid [van den Berg two-dimensional sharpness theorem](https://arxiv.org/abs/0907.2843) does not establish that the interval between thresholds is nonempty.

SOURCE_VERIFICATION.json records public URLs, PDF hashes and sizes, source versions, inspected portions, retrieval failures, model distinctions, and limits of literature and prior-attempt checks. The original landing page was requested first but returned an access error; no successful live-page reading is claimed. Live dataset filtering failed, while the complete pinned local corpus was independently hash-verified.

This packet contains only authored mathematics, authored code, finite-control outputs and public verification metadata. It excludes scholarly PDFs, screenshots, extracts, imported dataset contents and coordination records. Independent review is pending.
