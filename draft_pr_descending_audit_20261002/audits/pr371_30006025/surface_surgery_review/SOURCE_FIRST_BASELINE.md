# Source-first baseline (sealed before candidate proofs)

Frozen candidate: PR 371, head `51fddd150e8da33f4cf17b1a642a0ffd3466bf5d`. Independent family: geometric cut/glue surgery, curvature and area, random-surface applicability. Seal event and hash are in `SEALS.json`.

At sealing, I have read routing manifests and source hash/addendum routing, but no candidate TURN proof, code, output, state, final result, historical review, root review or sibling conclusion. Sources were acquired independently, under ignored `private/sources/`; exact acquisition receipts and hashes are public metadata.

## Original question and target model

Louf's [OWR 2024 report](https://publications.mfo.de/handle/mfo/4255), printed 2405 Question 4, asks for a geometric adaptation of Chapuy's bijection for constructing random surfaces. The precise quoted question is only 19 words: “Is there a nice geometric adaptation of Chapuy’s bijection to construct random surfaces?” The context compares short simple curve counts on closed genus-g hyperbolic surfaces sampled from normalized Weil-Petersson volume with Lebesgue-random genus-g one-face metric ribbon graphs of perimeter 12g. Both limiting intensities are `(cosh(t)-1)/t`. Question 4 does not formalize “nice” or prescribe a unique admissible geometry. Question 3 (spine law), Question 6 (volume ratios), and Conjecture 7 (boundary interpolation) are distinct questions; reproducing a limit intensity is weaker than constructing a coupling or a controlled random hyperbolic polygon law.

[Mirzakhani-Petri](https://webusers.imj-prg.fr/~bram.petri/RandSurf.pdf) defines its probability as WP volume divided by finite total WP volume. Its Theorem 4.1 uses primitive geodesics; Janson-Louf explains that bounded primitive geodesics are simple with high probability. [Janson-Louf](https://arxiv.org/abs/2111.11903) studies uniform unicellular maps with n edges, g tending to infinity and g=o(n), scaled by sqrt(12g/n). This is not the same finite measure as metric ribbon graphs. [Barazer-Giacchetto-Liu](https://arxiv.org/abs/2312.10517) uses normalized Kontsevich volume on metric ribbon graph moduli with fixed perimeter vector; its top-cell volume is proportional to Lebesgue measure. I distinguish all three finite laws.

## Combinatorial input

[Chapuy's direct bijection](https://arxiv.org/abs/1006.5053) slices a trisection into three vertices, changing genus by one; recursively it gives odd marked vertex sets. [CFF Theorem 5](https://arxiv.org/abs/1202.3252) gives `2^(n+1) E_g(n) ≃ T_g(n)` and preserves underlying graphs after identifying each odd C-permutation cycle. Section 2.5 gives an effective stochastic version; the deterministic matching extraction is not asserted polynomial. These are established inputs, not a new bijection proved by this audit. The original OWR citation is Chapuy's older dominant-subset result, [arXiv:0804.0546](https://arxiv.org/abs/0804.0546), rather than the universal direct identity; I will credit both if relevant.

## Geometry definitions and boundary cases

A genuine cone metric is a path metric on a topological surface. Interior total angle Theta>0 has defect `2pi-Theta`; Theta=2pi is smooth. Boundary sector angles are positive and finite; angle pi is smooth. A sector angle above 2pi is allowed intrinsically, although its development can overlap. Angle zero is a degeneracy outside this metric class, not a harmless limiting case to include in a universal theorem. Full turns must be read intrinsically; developed direction modulo 2pi loses information.

[Izmestiev arXiv:1409.7681](https://arxiv.org/abs/1409.7681), Theorem 1, assumes a topological disk and negative curvature at its interior cone points. It does **not** impose a boundary-angle lower bound. Smooth interior points are allowed. It gives `L^2 >= 4pi A` in Euclidean geometry and `L^2 >= 4pi A+A^2` for curvature -1. Sections 1.2-1.3 credit Weil/Beckenbach-Rado, Bol and Alexandrov. Section 1.4 explicitly warns about self-overlap of developments. Any proof here that merely invokes a planar simple polygon inequality without handling this warning has a gap. A disjoint union is not a disk. However, adding componentwise inequalities yields valid coarser bounds when each component separately qualifies.

## Independent deductions to test against candidate

1. With n edges and one face, `V=n+1-2g`. If k vertices are identified and edges/faces unchanged, Euler characteristic falls by k-1; for an orientable connected surface, genus rises by `(k-1)/2`. Odd k is necessary. Combinatorial vertex identification alone does not prescribe cone angles or polygon charts.
2. Pure subdivision/identification that conserves all sector angles gives `sum defect_after - sum defect_before = -2pi(k-1)`. This agrees with a genus increase `(k-1)/2` at unchanged constant-curvature area. Its inverse splits one angle among k vertices and raises total defect by `2pi(k-1)`. Smooth source/target points cannot all coexist at unchanged face area.
3. For a smooth genus-g closed surface of curvature -1, Gauss-Bonnet gives `A=4pi(g-1)`. Changing genus without changing the hyperbolic face area forces cone defects or a global deformation. A local angle-conserving mechanism is therefore restricted, not a no-go theorem for all geometric adaptations.
4. For a cone-surface disk of curvature -1 with piecewise geodesic boundary, `-A + sum_interior(2pi-Theta) + sum_boundary(pi-alpha)=2pi`. Boundary angles have a different reference value from interior cone angles. A geodesic disk with reentrant boundary can still meet interior curvature assumptions.
5. If a disk has no positive interior cone defects, combining its intrinsic inequality with total smooth closed-surface area may force a perimeter or edge-count growth condition. All constants must be reconstructed, all area allocation hypotheses stated, and strict/equality cases checked; a finite sample cannot prove this.
6. Quotient graph distances can shorten by switching between identified preimages. A graph systole counts graph cycles, whereas a filled surface admits interior paths and geodesics. A graph bijection is insufficient to control continuum distances, homotopy, lengths, or WP law.

## Success criteria and falsifiable checks

Accept a restricted theorem only if every object exists as an intrinsic metric surface, side pairing creates manifold neighborhoods, disk topology and all interior curvature assumptions are justified, angle and Euler changes agree, and stated random-model conclusions follow from the exact pushed-forward law. Check zero angle, full turn, singular and smooth endpoints, empty/trivial graphs, genus 0/1 versus g>=2, disconnectivity, self-overlap, equality limits, and continuum shortcuts.

A strong partial result may be correct without solving Question 4. A purported universal obstruction is rejected if it excludes global reparameterization, changed face geometry, cone points, or broader random laws without proving those are forbidden by the question. Novelty remains unverified unless an exact new claim is distinguished from the primary source inputs.
