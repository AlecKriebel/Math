# Adversarial cross-review of near-threshold calculation and table rendering

Date: 2026-09-06T04:44:10Z. This review was assigned after the independent algebra/topology report was completed. Other agents' conclusions were treated as hypotheses.

## Near-threshold m=3 control

**Verdict:** the claim survives a second independent reaction-derived reconstruction, including the full onset hypotheses. Its mathematical validity is stronger than the existing original verifier's limited linkage shows. A small supplementary proof/checkability addition is appropriate; this is not a false cubic-sign or bifurcation result.

Reviewed material:

- `../source_snapshot/manuscript/supplement.tex:901–954` defines the affine path and the m=3 control.
- `../source_snapshot/independent_verifier/frontier_verify_near_threshold.py:13–71` checks generic affine identities and sign bounds, but inserts the specific cubic rational function at lines 62–65 rather than reconstructing it from the field.
- `../pde/near_threshold_independent.py:6–16` independently builds A and Hessian tensors from reaction exponent lists.
- That reviewer's lines 29–44 perform the actual m=3 harmonic solves and cubic reconstruction; lines 53–69 certify the full first/higher-mode linear conditions.

The PDE reviewer's reaction derivatives are correct: for a unit-equilibrium monomial with exponent vector y, its Hessian is `y y^T-diag(y)`. Multiplication by each stoichiometric column supplies the vector-field Hessian. The m=3 right vector matches the printed path with `(omega,theta,M)=(2/9,1/2,1)`. The bordered solve uses the homogeneous right kernel vector and the correct c-weighted mass constraint. The forcing lies in c^perp, so the bordering multiplier is zero; the computed first four entries therefore solve the intended mass-gauged equation.

To avoid accepting a shared construction error, I created `crosscheck_near_threshold.py` without importing the PDE reviewer's or project's code. It reuses only this algebra audit's independent reaction-to-polynomial constructor, differentiates each polynomial with SymPy's Hessian operation, solves the zero-mode equation as an overdetermined system with the mass row appended (a different solve from the PDE reviewer's bordered method), and forms the cubic by the printed harmonic-projection formula. It checks the zero-mode, mass-gauge, and second-harmonic residuals explicitly.

The resulting diffusion entries are

```text
d1 = e(3e+8)/6
 d2 = e(4-9e)/(9e^2+32e+18)
 d3 = e
 dZ = 16e/(9-13e).
```

They are strictly positive throughout `0<e<=1/1000`. The cubic agrees with the full archived rational function, and independently gives

```text
c3(e) = 6/1379 + (421985/11409846)e + O(e^2).
```

I also directly certified `c3(e)>0` on the entire stated interval, rather than inferring it only from the positive limiting constant. The substitution `e=1/[1000(1+z)]`, `z>=0`, is a bijection onto that interval. After clearing denominators with their correct sign, both the numerator and denominator of the cubic have strictly positive coefficients and strictly positive constants. The same method certifies positive diffusivities, negative left/right pairing, and positive transversality.

For linear onset, I computed `det(lambda I-A+tD)` directly as a four-by-four determinant and checked its identity with the reviewer's boundary-polynomial expression; this removes a possible unverified reduction in that script. Writing it as

```text
lambda^4+a1 lambda^3+a2 lambda^2+a3 lambda+a4,
```

and substituting `t=1+v`, `v>=0`, produces positive rational certificates for `a1`, `a2`, `a3`, `a4/(t-1)`, `H2=a1*a2-a3`, and `H3=a3*H2-a1^2*a4`. The numbers of positive numerator terms match the independently reviewed script: `11,18,22,17,42,105` respectively. Denominator coefficients and constants are positive after a consistent sign normalization, so no hidden pole or endpoint exception is introduced.

At t=1, a4=0 and a3>0, so zero is algebraically simple. The remaining cubic is Hurwitz because a1,a2,a3,H2 are positive. For t>1, a4>0 and the quartic Hurwitz determinants are all positive. Thus every higher Neumann mode and the stable side of the first mode are controlled. The homogeneous mode is the independently verified stable a=b=H=1 reaction realization. Finally, I checked

```text
eta = [partial_t a4(1)]/a3(1) > 0,
```

against the independently computed adjoint-projection formula, proving the correct crossing orientation for the parameter `mu=1-t`.

**Scope:** these are exact parameter-interval proofs for m=3, not finite epsilon sampling. They do not establish the nonlinear sign for arbitrary m or a uniform spectral gap as epsilon tends to zero. The printed statement is confined to m=3 and does not need either extension. At epsilon=0 the diffusivities collapse to zero and the nonzero-mode spectral gaps need not persist; that excluded endpoint was not used as a bifurcation point.

**Run and artifacts:**

```text
/Users/alec/Documents/Math/.venv/bin/python crosscheck_near_threshold.py
```

Exit code 0, PASS. Full output: `near_threshold_crosscheck_run.log`. Structured checks, exact rational cubic, transversality expression, and certificate counts: `near_threshold_crosscheck_results.json`.

**Recommended local addition:** connect the specific path to the existing normal-form formula by providing the reaction-derived solve in the maintained verifier, and state the short quartic Routh certificate argument for the linear onset. The original sign-only hardcoded-function check is weaker than that complete derivation; the result itself is independently verified here.

## Independent visual check of the journal supplement table

I viewed `../documents/rendered/table_detail.png` and read `../documents/TABLE_SPACING_WITNESS.json` without assuming the parent's diagnosis.

**Verdict:** the raster shows an actual visible spacing/overprinting defect. This is not merely overlapping font bounding boxes with otherwise separated ink. Successive rational rows touch or overprint: the denominator `91125` impinges on the following numerator `4420871`, and the same problem recurs at `33075`/`1147126` and later entries. At enlargement the intended integers can still be inferred, but row separation is visibly lost and parsing is needlessly difficult.

The witness reports approximately 1.513 pt vertical overlap and 19.854 pt horizontal overlap for the first pair on journal supplement page 15. That numerical witness agrees with the directly viewed raster. Increasing the row struts or cell padding is warranted before submission, followed by a fresh rendered-table inspection. This is a presentation defect, not an algebraic inconsistency in the coefficients.
