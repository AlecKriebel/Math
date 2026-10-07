# Exact targets and current status

Status: complete mathematical proof candidate, justified by the manually audited upstream analytic inequality and established existence/regularity inputs. Independent complete-package review and publication remain pending. No firstness or novel transfer machinery claim is made. No independent Lean rebuild was completed.

Let n>=2 be ambient dimension. Write dω for the unnormalized round area measure on S^(n-1), ∇² for its covariant Hessian and I for the identity on its (n-1)-dimensional tangent spaces. A solution is a positive even C∞ support function h with Q(h)=∇²h+hI positive definite everywhere. Its body K is compact, full-dimensional, origin-symmetric and has smooth boundary with positive Gauss curvature. This admissible class is more precise than arbitrary positive functions or strict convexity without a curvature condition.

## T1 — Smooth existence and uniqueness

For every p∈[0,1) and every f∈C∞(S^(n-1)) that is even and strictly positive, exactly one admissible h satisfies

    h^(1-p) det Q(h) = f.

The determinant is of an (n-1) by (n-1) form in an orthonormal tangent frame. There is no independent volume-one normalization. Scaling h by c>0 scales its prescribed density by c^(n-p). The origin is fixed; evenness excludes translations. At p=0, ∫f dω=n|K|, hence volume is determined by the data.

## T2 — General-body uniqueness for positive p

For 0<p<1, if K,L⊂R^n are arbitrary full-dimensional origin-symmetric convex bodies and h_K^(1-p)dS_K=h_L^(1-p)dS_L as Borel measures on S^(n-1), then K=L. Smoothness and a positive density are not assumed.

## B0 — Endpoint boundary

T2 is false at p=0. A coordinate box with half-widths a_i>0 has mass |K|/2 at each normal ±e_i for the measure h_K dS_K (and |K|/(2n) for cone volume). Thus distinct equal-volume boxes with fixed coordinate normals share this measure. This does not falsify T1.

## Success criteria

Every pivotal theorem, including the unreviewed upstream inequality, must withstand semantic/proof checks. Existence regularity and He–Liu's conditional uniqueness must be checked beyond abstracts. A complete package requires priority/attribution review, two complete-package adversarial reviews with a fresh final pass, clean compilation and PDF inspection, verified production publication and tracker read-back. If a material upstream gap remains, preserve the conditional implications and exact obstruction; do not label T1/T2 unconditionally resolved.
