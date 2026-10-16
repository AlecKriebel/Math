# Independent Cartesian mechanism freeze

UTC 2026-10-16 04:35:51. This file was written after reading only the audit INTAKE metadata and the submitted `sources/pinned_problem.json` and `sources/pinned_report.json`. No submitted proof, checker, or reviewer opinion has been opened. The parent task supplied the exact signed-area target and requested physical geometry independence.

Exact target under attack: for a billiard Poncelet family on one ellipse with one fixed confocal caustic, the ordered tangent-intersection polygon has signed area A', and the ordered feet from the ellipse center onto its side lines have signed area B. The product A'B is constant for odd N and N=2 mod 4. The precise original-source scope, especially hyperbolic caustics, is not assumed settled.

## Mechanism derived independently

Set Q_i=(a cos t_i,b sin t_i), with a>=b>0 and O=(0,0). The tangent line is n_i dot X=1 with n_i=(cos t_i/a,sin t_i/b). Solve the actual 2 by 2 linear systems to obtain V_i=T_i intersect T_{i+1}. The orthogonal foot onto T_i is H_i=n_i/(n_i dot n_i). The side line of the V polygon through V_{i-1},V_i is exactly T_i, including star polygons. Therefore a cyclic shift of H has the intended signed shoelace area. Reversal changes both signed areas and preserves their product.

Writing D(t)=b^2 cos^2 t+a^2 sin^2 t gives the directly derived checks

* A'=ab sum_i tan((t_{i+1}-t_i)/2), provided consecutive tangents intersect finitely.
* B=(a^3 b^3/2) sum_i sin(t_{i+1}-t_i)/(D(t_i)D(t_{i+1})).

These identities hold for arbitrary cyclic ellipse points and do not depend on Poncelet closure. They can be verified against direct line intersections and foot vectors, so failures isolate geometric construction/sign mistakes.

A chord joining t=mu-delta and t=mu+delta has equation cos(mu)x/a+sin(mu)y/b=cos(delta). Its tangency to the confocal conic with squared semiaxes a^2-lambda,b^2-lambda is equivalent to

sin(delta)^2=lambda*(cos(mu)^2/a^2+sin(mu)^2/b^2).

The initial computational family will evolve a real billiard by Cartesian reflection, without Jacobi parametrization or the submitted area/trace formulas: choose a boundary point, determine one chord direction tangent to the desired caustic, intersect with the ellipse again, reflect by its Euclidean normal, and repeat. Solve a closure parameter independently for low periods. Validate closure, ellipse incidence, reflection residual, and the caustic quadratic tangency discriminant separately before testing products. Numerical diagnostics, including high precision, are uncertified finite evidence.

## Falsification plan and expected gaps

1. Exact algebraic low-N families and rational configurations whenever available.
2. Primitive N=4 and N=8 same-caustic phase variation as genuine boundary failures, rather than comparing different caustics.
3. Odd and 2 mod 4 periods; coprime stars and reversal; repetition with the actual signed shoelace multiplication law; near-circle, thin ellipses, and large periods.
4. Identify finite-intersection and nondegenerate-caustic restrictions. Probe the hyperbolic branch separately if the original source includes it.
5. Only after this freeze read inherited material; compare every geometric equivalence and claimed universal step with direct derivation. A universal trace or area theorem remains unsupported until independently verified; a finite experiment cannot supply that step.

Current best-guess completion of this physical audit: 10%. No target edits, Git mutations, publications, environment creation, or external outreach were performed.
