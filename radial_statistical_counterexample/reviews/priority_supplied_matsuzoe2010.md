# Supplied full-text review: Matsuzoe (2010)

**Checkpoint:** 2026-09-24 04:16 UTC. **Completion estimate:** 100% of the
bounded review of this supplied paper; no percentage of historical priority
is asserted.

**Verdict:** this paper does not state an answer to FMU (1998), Question 3(e),
or exhibit the proposed cylinder as its counterexample. Its theorems do not
deduce dual statistical 1-conformal flatness from the all-centres radial
integrability hypothesis. It supplies substantial prior machinery used in
the candidate, including an exact prior formula for its non-self-dual
deformation. This closes this paper's former full-text-access gap without
certifying novelty of the assembled answer.

## Source and coverage

Hiroshi Matsuzoe, *Statistical manifolds and affine differential geometry*,
Advanced Studies in Pure Mathematics 57 (2010), 303-321,
[DOI 10.2969/aspm/05710303](https://doi.org/10.2969/aspm/05710303).
The supplied `Download (1).pdf` contains all 19 pages.
Its independently checked SHA-256 is:

```text
7429bb37d18d3a3fe8a0c68f0cbcfe556ee92fc96dafb07b4dea3c04a40479fd
```

I read the complete extracted text, including all eight sections and the
26-item bibliography, and visually inspected printed pages 305, 308, 309,
311, 312, 313, 315, 318, and 319. The displayed definitions, formula signs,
and theorem hypotheses below were checked against page images, not trusted
to OCR alone. Page references below are the printed pages, not PDF indices.

## Direct comparison of hypotheses and conclusions

| Location | Actual content and relevance |
| --- | --- |
| pp.304-306, equation (1), Propositions 2.1-2.3, Definition 2.4 | Metric duality, curvature duality, symmetric cubic forms, and torsion-free statistical structures. Setting the cubic form to zero recovers a Levi-Civita structure. There is no exclusion of the self-dual case. |
| pp.307-308, Proposition 3.1 and equations (2)-(4) | Potentials, Legendre duality, and canonical divergences under an existing dually flat hypothesis. These do not infer flatness from radial integrability. |
| pp.308-310, Sections 3.2.1-3.2.4 | Distinguishes ordinary conformal equivalence, projective equivalence, dual-projective equivalence, and statistical alpha-conformal equivalence. The alpha=1 convention agrees with the candidate's connection change. |
| pp.310-311, Proposition 4.1 | Generalized duality and semi-Weyl compatibility with an extra one-form. No all-centres geodesic-orthogonality condition occurs. |
| p.311, equation (10); pp.312-313, Proposition 5.2 and Theorem 5.3 | The affine-hypersurface Gauss equation has the same pointwise curvature form as the candidate's necessary obstruction. The realization results assume a nondegenerate equiaffine immersion or 1-conformal/dual-projective flatness; they do not supply such an immersion from radial integrability. |
| pp.313-315, Propositions 5.4-5.5 | Conormal duality and agreement of geometric and canonical divergence in the dually flat case. No converse with the problem's radial premise is asserted. |
| pp.315-317, Theorem 6.1 | A simply connected conformally-projectively flat statistical manifold has a codimension-two centroaffine realization. This uses a broader flatness condition than 1-conformal flatness. |
| pp.317-320, Propositions 7.1-7.2 and 8.1, Example 8.2 | Torsion-admitting structures, affine distributions represented by an ambient-vector-valued one-form, and an SLD quantum-state example. These distributions are not the radial hyperplane fields in Question 3(e). |

The full text does not present the round product cylinder, a claimed solution
of Question 3(e), or a correction of its wording. The bibliography does not
cite the FMU problem list. The conclusion above rests on reading the actual
statements, not on that absent citation or a keyword search.

## Established machinery that must receive credit

On p.309, Section 3.2.4 explicitly gives

\[
\widetilde h=e^{\psi+\phi}h,\qquad
\widetilde\nabla_XY=\nabla_XY-h(X,Y)\operatorname{grad}_h\psi
 +d\phi(Y)X+d\phi(X)Y.
\]

It identifies constant \(\psi\) as the statistical \((-1)\)-conformal
case. Taking \(\psi=0\), \(\phi=t\), and the base product structure gives
**exactly** the candidate's \(h_1=e^t h_0\) and
\(\nabla^1=\nabla^0+dt\otimes\mathrm{Id}+\mathrm{Id}\otimes dt\).
Thus this 2010 paper is already an explicit earlier source for the general
deformation formula. It attributes the framework to older work, including
Matsuzoe (1998/1999) and Kurose (1994/2002); 2010 should not be presented as
its first discovery either. The candidate's particular use of that formula
does not make the mechanism new.

Equation (10), p.311, is

\[
R(X,Y)Z=h(Y,Z)SX-h(X,Z)SY.
\]

The candidate's obstruction is this established Gauss-form algebra with an
unrestricted endomorphism in place of \(S\). The two product-curvature
evaluations exclude it. Proposition 5.2 does not rescue the candidate's
flatness: the ordinary cylinder immersion into Euclidean four-space has a
degenerate second fundamental form, so it does not induce the candidate's
positive-definite product metric as the nondegenerate affine fundamental
form assumed there.

## Stronger-looking claims that do not conflict

Theorem 6.1 concerns *conformal-projective* flatness. The cylinder actually
has this broader property: under \(r=e^t\),
\(e^{2t}(dt^2+g_{S^2})=dr^2+r^2g_{S^2}\) is Euclidean. Taking
\(\phi=\psi=t\) in the displayed two-function formula produces its flat
Levi-Civita connection. The extra projective terms are essential. This is
consistent with failure of the more restrictive statistical 1-conformal
flattening. This application to the cylinder is my comparison of the
formulas, not a cylinder example claimed to appear in Matsuzoe's paper.

Section 8's condition \(\operatorname{Image}(d\omega)_p\subset
\operatorname{Image}\omega_p\) concerns a moving ambient affine
distribution. It contains neither a choice of centre nor terminal
geodesic velocities, and its induced connection may have torsion. Its
presence is not a hidden answer to the radial question.

**Priority consequence:** no competing explicit resolution was found in
this complete paper, and no mathematical correction to the candidate is
forced by it. The candidate's elementary ingredients are nevertheless
largely classical and directly available here. The defensible claim
remains an explicit answer with no earlier explicit answer found in the
documented search, not proof of first discovery or a novel general
flatness criterion. No external person was contacted, and no manuscript,
repository commit, or third-party file was changed during this review.
