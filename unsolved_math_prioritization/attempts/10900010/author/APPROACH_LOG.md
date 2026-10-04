# Five approaches to the fixed edge-cover question

Status after five substantive approaches: **NO RESOLUTION**. The count records distinct arguments explored; it is not a count of computational proof certificates.

## Approach 1 Dual surfaces and compression

Constructed the action class via an equivariant map, proved compactness modulo the edge stabilizer, proved injective descent, and proved map-independence by compact bordism. Tested whether removing compressions closes the norm problem. The product example with a three-crossing PL height function gives an essential dual surface with triple the minimum complexity. Exact roots and orientations are reproduced by verify.py. Outcome: the class and a descending upper bound are certified; essentialness alone fails to prove optimality. See PROOF.md §§2–3.

## Approach 2 Singular norm and homological pushforward

Applied Gabai's singular/embedded norm inequality to every upstairs representative. Derived the rigorous sandwich x_M(p_*α)≤x_N(α)≤μ_e. This yields a certificate when a downstairs taut surface lifts in the correct class. Completed the argument for every translation action on a line using a circle-valued map with a prescribed taut regular fiber. Then tested the stronger identity for arbitrary actions: the explicit orientable double-twisted-I-bundle family has x_N(α)=2g−2 but p_*α=0. Outcome: a positive special case and a strict obstruction to the naïve generalization. See PROOF.md §§4–5,7.

## Approach 3 Surface groups and a homotopy retraction

Sought an intrinsic lower bound in the edge cover, even when the pushed-forward class vanishes. Proved a retraction criterion using nonzero degree and injectivity of rational H¹ through the cup pairing. Applied it when the edge group is exactly carried by a connected embedded incompressible surface in an aspherical manifold. Checked disconnected degree decompositions explicitly; total degree one does not imply that one component has degree one. Outcome: geometric surface splittings are covered, but arbitrary overgroups of the surface group are not. See PROOF.md §6.

## Approach 4 Least area and equivariant uncrossing

Inspected Freedman–Hass–Scott's actual embedding and disjointness hypotheses, and Scott–Swarup's compatibility/intersection-number statements. Derived the exact universal-cover condition U∩gU=∅ for every g outside H. The norm-minimizer's component groups can be proper subgroups of H, so the original splitting does not provide the necessary homotopy-to-embedding input. Tested two invalid shortcuts: checking only the normalizer deck group, and replacing χ_- by the total Euler characteristic during exchange. Outcome: neither shortcut is valid; a simultaneous norm-preserving uncrossing theorem remains unproved. See PROOF.md §§8–9.

## Approach 5 Normal surfaces finite covers and splitting complexity

Inspected Cooper–Tillmann's finite normal-surface norm construction, Cigna's July 2026 sutured-hierarchy version, and Jaikin-Zapirain–Kudlinska–Sánchez-Peralta's August 2026 splitting-complexity result. Tried to formulate a finite optimization with both homology and descent constraints. No exhaustion theorem or certified compact search region for the arbitrary infinite edge cover was supplied, and no finite encoding of every translate condition was obtained. Finite-cover embedding does not descend automatically. The 2026 algebraic theorem varies the splitting dual to a character and does not preserve the chosen H-cover. Outcome: no algorithmic certificate or new general implication was obtained. No computer enumeration of triangulated 3-manifolds is claimed.

## Stop condition and remaining task

Five distinct approaches are complete at the depth stated. No exact-target published resolution was located in the checked sources. This is a bounded negative search result, not a proof that the question remains open everywhere. The remaining mathematical task is either a theorem enforcing all translate-disjointness conditions without increasing χ_-, or a verified example where the descending minimum exceeds the upstairs norm.
