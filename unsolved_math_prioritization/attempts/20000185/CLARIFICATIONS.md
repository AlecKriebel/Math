# Clarifications accompanying the frozen author packet

4 October 2026. The eleven author files and nine audit files are preserved byte-for-byte. This addendum adopts the three nonblocking clarifications in `audit/CORRECTIONS.json` without replacing or editing the reviewed proof.

1. **Zero epipole orders.** In Theorem 1, when both local divisor coefficients U,V are zero, the coordinates x,y need not be units. The basepoint-free pencil provides a unit among S,T, and the third or fourth triangulation coordinate supplies common order zero. If exactly one of U,V is positive, its corresponding epipole coordinate is a unit. The common order is min(U,V) in every case. No formula changes.

2. **Computational input model.** The finite procedure in Section 5 assumes characteristic-zero coefficient fields equipped with effective arithmetic and geometric factorization/primary-decomposition algorithms, for example algebraic-number input. Computable field arithmetic alone is not a promise of effective geometric decomposition. The algebraic component criterion does not change.

3. **Example saturation.** The author verifier saturates by the single coordinate t only for the three selected examples. No proper component of those examples lies in t=0, so deleting t=0 and taking closure removes the baseline component and retains every proper component. This validates those example calculations; the helper is not a general implementation of saturation by the full ideal (s,t). The independent quartic test explicitly computes full baseline saturation.

The published conclusion remains scoped: integral reduced images, rank-three fixed cameras, an algebraically closed characteristic-zero field, and nonconstant pencil maps for the component/degree theorems. Constant-pencil and coincident-center weak-existence cases are treated separately. Real visibility and general nonreduced/reducible interpretations are not resolved. The gcd component bound, epipolar fiber-product foundation and 40-cover count retain their prior-work credit. No novelty or full-source-resolution claim is made.
