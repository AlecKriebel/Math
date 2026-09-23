# Independent computation review

Checkpoint: 2026-09-23 03:36 UTC. Completion estimate for this bounded
coordinate-verification task: **100%**. This is not a percentage estimate of
historical priority or of the full publication task.

## Scope and result

The independent verifier `verification/verify_symbolic.py` reconstructs the
Levi-Civita connection from the coordinate metric

\[
h_0=\operatorname{diag}(1,\sin^2\theta,1)
\]

and differentiates its Christoffel symbols to obtain every curvature
component. It does not enter the candidate's product-curvature formula as
the calculated curvature. That formula is used only as the expected result
against which all components are compared.

All **403 explicit exact checks pass** with SymPy 1.14.0 and Python 3.9.6.
The stored `verification/symbolic_output.txt` comes from an optimized Python
run (`python -O`); failure detection uses exceptions and does not depend on
Python assertions. There are no numerical tolerances or sampled floating
point values.

The checks establish the following coordinate identities:

- All torsion and covariant metric-derivative components vanish for the
  reconstructed Levi-Civita connection.
- Every component of the product curvature agrees with the unit-sphere
  product formula. The Ricci matrix is
  `diag(1, sin(theta)**2, 0)`.
- For an arbitrary symbolic smooth function `phi(theta, chi, t)`, all 81
  components of the curvature of `Gamma - h * grad(phi)` agree with
  \(R(X,Y)Z-h(Y,Z)A(X)+h(X,Z)A(Y)\), where
  \(A(X)=\nabla_X\operatorname{grad}\phi-d\phi(X)\operatorname{grad}\phi\).
- The two relevant coordinate equations throughout the nonsingular chart
  force the same component \(A^\theta_{\ \theta}\) to equal both 1 and 0.
  Independently, at \(\theta=\pi/2\), the complete linear system in nine
  unrestricted entries of \(A\) has coefficient rank 9 and augmented rank
  10, and its exact solution set is empty.
- The independently contracted projective Weyl component
  \(W^t{}_{t\theta\theta}\) is \(-1/2\).
- For \(h_1=e^t h_0\) and the projectively changed connection, the computed
  cubic tensor has the stated formula, is totally symmetric, and satisfies
  \(C_{ttt}=-3e^t\). The connection is torsion-free.
- Solving the defining metric-duality equation in every component gives
  the claimed dual connection. The geodesic-acceleration difference is
  exactly \(2v^t v\), and the additional conformal change of the dual equals
  the base change with conformal function \(t+\psi\).

## Falsification controls

The same unrestricted-endomorphism solver accepts Euclidean curvature,
computed from its metric, with the unique solution \(A=0\). It also accepts
the algebraic unit constant-curvature tensor with the unique solution
\(A=\mathrm{id}\). Thus inconsistency is not built into the solver.

A deliberate mutation retaining the projectively changed connection while
omitting the required metric factor \(e^t\) fails cubic symmetry: the
computed difference \(C_{t\theta\theta}-C_{\theta t\theta}\) is \(-1\).
The verifier requires this mutated construction to fail.

## Limits and remaining gap

This computation supports the tensor algebra in dimension three. It does
not verify the quantified theorem about radial integrability for every
centre, the meaning of the original printed problem, completeness of a
literature search, or novelty. Those require the accompanying proofs and
source audit. The coordinate chart excludes the usual polar singularities;
the coordinate-independent orthonormal-frame proof applies at every point,
and spherical coordinates can be rotated around any chosen point. The
higher-dimensional extension likewise belongs to the written product proof.

No algebraic discrepancy remains in the checked identities. No external
person was contacted, and this review neither grants priority nor asserts
that absence of a known prior publication proves novelty.

## Reproduction

From the package directory, use Python with the pinned dependency:

```text
python -m pip install -r verification/requirements.txt
python verification/verify_symbolic.py
python -O verification/verify_symbolic.py
```

Both runs must end with `SUCCESS: 403 explicit exact checks` and exit with
status zero. The expected transcript is in
`verification/symbolic_output.txt`.
