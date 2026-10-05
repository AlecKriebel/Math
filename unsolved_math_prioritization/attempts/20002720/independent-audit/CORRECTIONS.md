# Corrections and scope guardrails

No blocking correction to the frozen author packet was found.

## Additional source correction: derived subgroup of the normalized group

Friedrich--McKay, *Almost Commutative Probability Theory*, arXiv:1309.6194v1, Example 6.1 on printed page 32 asserts an equality between the derived subgroup of the normalized two-variable boxed group and the subgroup with vanishing degree-two coordinates. Only inclusion follows from the displayed degree-two calculation.

For a fixed letter i, let P_i(f)(z)=sum_{n>=1} f[i^n]z^n. The partition formula gives P_i(f box g)=P_i(f) box P_i(g). The target one-variable group is abelian, so P_i sends every commutator to z. Since its kernel is a subgroup, it sends every product of commutators to z as well. However, e+z_i^3 has zero degree-two coordinates and P_i(e+z_i^3)=z+z^3. This refutes the equality over any nonzero commutative coefficient ring. It also refutes the stated extension to more variables.

A safe replacement is:

    [U_s,U_s] is contained in F^3 U_s intersected with all kernels of P_i.

No assertion that this containment is equality is made. The frozen packet uses only the valid filtration inclusion, so its conclusion is unaffected.

Source: https://arxiv.org/abs/1309.6194v1

## Existing exclusions that must be preserved

- The preprint's equation (35) does not identify the full derived subgroup correctly.
- Bounded-degree polynomials are not subgroups of the full series group; finite degree means quotient.
- A faithful regular representation need not be minimal or uniquely preferred.
- The tuple map factors through formal distributions and needs invertible means.
- The scalar boxed law is for commutative coefficient rings. It is not the operator-valued convolution law.
- Radial central series and the torus do not amount to a proved classification of the entire center.

## Notational clarification only

When using the integral Hopf algebra with R-valued characters, the finite representation module is the bounded-weight part of R tensor_Z H_s. This is already implicit in describing it as a free R-module; it introduces no new hypothesis or correction to the proof.
