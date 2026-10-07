# Author self-check and limitations

## Mathematical checks

* The resistance defect uses a probability measure and unit velocities. Its coefficient is 1/4, not 1/2. The exposed-boundary integral is 2/3, giving L₀/(3P), not a dimension-independent constant.
* Non-normal one-reflection rays fail exact reversal. Exact normal incidence itself retroreflects and is never used as a failure example; it is the center of a clear cone from which non-normal rays are chosen.
* The finite-polygon lemma assumes a simple finite polygon, a genuine hull vertex with cone angle below π, and an exact local sector. It does not cover arbitrary singular boundary accumulation or every interpretation of piecewise smooth.
* The two-collision endpoint-coordinate argument uses transversality, a distinct second collision, regular arcs and an open itinerary set. It is not inferred from a lone ray or a numerical set of samples.
* The aperture coordinates use the physical outgoing tangential momentum P. Reversal gives P=−p; the Jacobian determinant is +1 because X_x=−1 too. The incorrect +x branch is explicitly rejected by the checker.
* The compactness lemma requires clear finite regular itineraries and local C¹ geometric convergence; bare Hausdorff convergence does not meet those hypotheses. The counterexample uses real finite polygonal billiards, not an arbitrary invented scattering kernel.
* The sawtooth exceptional coordinates, apex hit, and grazing/opening endpoint possibilities are excluded before tracing. Exact rational intersections with every polygon edge check both collision order and full escape for the finite controls. The general all-real formulas are proved in Turn 5.
* No extension from a fixed angular direction to almost-everywhere full incidence is assumed. Turn 5 explicitly uses a whole angular band to refute convergence in measure.

## Actual computational checks

The standard-library exact verifier passed 9,280 assertions. It checks 1,298 nonsingular sawtooth trajectories across body sizes n=1,2,3,5 and rational entrance positions/angles, with 649 one-bounce and 649 two-bounce cases. Eleven singular parameter tuples were deliberately excluded from those trajectories. Norm, reflection-composition, determinant, defect, exit-position and reflection-count controls pass.

Two actual faulty subprocess variants were run: the incorrect symplectic +x sign and the claim that every sawtooth ray retroreflects. Both terminate with a failed assertion. An optimized-Python invocation is also rejected. Their exact results are recorded in negative_control_results.json and replayed.

This author reviewed the written arguments and corrected differentiability hypotheses before the freeze: Turn 3 uses C² arcs for its local coordinate argument, and Turn 4 uses C³ arcs/C² scattering branches for the displayed exterior differentiations. No earlier frozen version was overwritten. No helper or separate reviewer was used; this is not an independent audit.

## Unresolved matters

The central existence/nonexistence question is unresolved by the packet. The proofs do not supply a universal boundary-regularity reduction, a classification of all multi-bounce branches, or stable compactness for an asymptotically perfect family. Finite verification cannot certify those missing statements. The current literature check is bounded and cannot certify exhaustive novelty or the absence of an unknown later theorem.
