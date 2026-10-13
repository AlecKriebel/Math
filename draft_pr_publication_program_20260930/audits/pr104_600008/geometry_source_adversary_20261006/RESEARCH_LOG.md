# Geometry and source-scope adversarial audit log

## 2026-10-06T03:12:16Z — audit opened; 20% complete

Target: verify/falsify the complete analytic theorem in the preserved `ANALYTIC_CRITERION.md`, not seek a new central proof. Parameters are every real `a,b,c>0`; positive equator lift, full boundary arcs, winding, parity, least versus iterated closure are explicit success criteria. No new central proof-search turn is charged; the original research turn count remains 1/5. Work and outputs stay in this audit folder. No Git, remote, queue, editor, upload or external communication actions are authorized here.

Independent derivation before old review/conclusions: writing `Q=x²/a²+y²/b²-z²/c²`, the root equation's value at `v=0` is exactly `1+cQ`, and its value at `v=c` is `1-z²/c`. Its derivative is strictly negative on the closed belt because `x,y` cannot both vanish there. Thus `v` and the signed trigonometric pair recover a unique belt point. The map is once around the belt, not the doubled covering suggested by confocal-square coordinates alone.

At the equator use the physical signed normal coordinate `q=sign(z)sqrt(c-v)`. Then `z=q sqrt(c(c+f²)/D)`, `Y(q)=sign(q)[H-τ(c-q²)]`, and `dY/dq=sqrt((c-q²)/((a+c-q²)(b+c-q²)))`; its derivative at zero is `sqrt(c/D)>0`. This independently resolves the square-root seam. Near a tropic, `τ(v)=v^(3/2)/(3sqrt(abc))+O(v^(5/2))`: the boundary coordinate map is a homeomorphism, not a smooth Lorentz chart at the degenerate metric. The actual null direction is transverse to the tropic, and concatenated arcs have cusp behavior.

## 2026-10-06T03:13:39Z — literal source wording inspected; 45% complete

Read primary extracted Tabachnikov 2015 §7 printed p62 and GKT 2007 §5 pp17–18, after the initial geometric derivation. Tabachnikov asks for conditions on `a,b,c`; the Cayley reference supplies motivation but does not explicitly require a determinant or polynomial. GKT's `T` is a North-return map, not one full tropic-to-tropic arc. One positive full arc advances the conformal angular coordinate by `2H`, the same as one equator/North/equator passage, while changing boundary component. Therefore full-arc closure requires even `n`; the folded return map does not. Source also assumes `a>b` in its original development; the candidate extends to all positive axes through its direct coordinates.

Remaining checks: direct induced-metric algebra, independent coverage controls, boundary tangent and counted examples, integral identity diagnostics, and final exact source-scope assessment. No original author review or prior imported report has been used as verification evidence.

## 2026-10-06T03:15:31Z — substantive geometry checks passed; 85% complete

Independent standard-library multivariate polynomial expansion gives zero residual for all five universal identities: ellipsoid membership, `Q=vf²/(abc)`, metric cross coefficient, and angular/normal metric coefficients. Independent ordinary-latitude point generation reconstructs 810 closed-belt points, including 324 tropic points and 540 points on coordinate axes. Ten endpoint-regular quadrature diagnostics cover rotational, swapped, anisotropic, near-axisymmetric and small/large-c cases. Largest period-identity defect is below 4.2e-11; numerical controls are labeled diagnostic, not validated quadrature.

Independent contour branch inspection confirms both upper-bank differential values have the same negative imaginary sign and that the cut-loop orientation produces the claimed positive identity. Null geodesics in the open conformal belt reach opposite boundaries; null directions there are transverse to tropic tangents. Ordinary winding equals the conformal angular lift by a positive-diagonal homotopy. Explicit axisymmetric controls falsify the parity-free full-chain interpretation but confirm the submitted parity-aware theorem. Source wordings support a complete literal analytic answer; algebraic Cayley and historical novelty are unverified stronger matters.

## 2026-10-06T03:17:04Z — review completed; 100% complete

The assigned independent geometry/source-scope audit is complete. `REPORT.md` and `VERDICT.json` record a mathematical pass for the literal analytic criterion, with no required central proof repair. The source arc-count qualification, all-positive-axis domain, boundary homeomorphism rather than nonsingular boundary chart, physical lift/winding, and least-versus-iterated distinctions are retained. The finite algebraic Cayley problem, arithmetic equivalence, novelty and publication clearance are explicitly not certified. The percentage is completion of this assigned verification effort; it does not declare the broader research/publication program complete. Zero new central proof-search turns; original accounting remains 1/5. One simple `MANIFEST.json` pins reviewed inputs and completed outputs.
