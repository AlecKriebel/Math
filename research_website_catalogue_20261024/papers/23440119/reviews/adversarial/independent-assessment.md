# Sealed independent adversarial assessment

Record: Zenodo 23440119, DOI 10.5281/zenodo.23440119, Version 1.0.0, 17 October 2026. Title: *A negative-curvature normal barrier on an algebraic cone that is not a hyperbolicity cone*. Target: the actual published five-page PDF, SHA256 `ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0`, freshly acquired 2026-10-25T05:22:37Z. The starting local copy has that identical SHA256. Supplement ZIP SHA256 `d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e` is identified but **has not been opened for this initial assessment**.

## Independence and success criteria

Read extent before sealing: every page of the actual PDF, both extracted text and rendered page images; acquisition checksum/receipt; root AGENTS.md. No submitted code, proof supplement, historical audit, favorable verdict, or other reviewer's opinion has been read. Primary-source control PDFs were requested but have not yet been read. This artifact records the original adversarial position before that subsequent inspection. Only the reviewer's own standard-library script was run.

The hypothesis is exactly Theorem 1: the closed one-sided cone `K={(x,y,z)>=0:xy^2>=z^3}` is regular algebraic convex; `F=-25 log(z(xy^2-z^3))` on its interior is a parameter-100 logarithmically homogeneous self-concordant barrier; `D^3F(a)[h,u,u]<=0` holds for *all* `a` in the interior, `h` in closed K, and real `u`; and K is no homogeneous-polynomial hyperbolicity cone in its ambient R^3. Success requires checking the universal proof, including boundary and null directions, rather than trusting finite tests. The “negative curvature” here is the explicitly stated third-derivative condition. This is not a claim about the sectional curvature of the Hessian Riemannian metric.

## Adversarial mechanism and evidence

The attack family starts from raw derivatives of `p=x*y*y-z*z*z`, rather than reusing the published matrix as input. For `p_h=Dp[h]`, the numerator of the curvature matrix for `-log p` is

`(-p^3 D^3[-log p][h])_ij = 2 p_h p_i p_j - p(p_hi p_j+p_hj p_i+p_ij p_h) + p^2 p_hij`.

The `-log z` summand adds `2p^3 h_z/z^3` to entry zz. The independently written `independent_check.py` represents the result at `(s+1,1,1)`, `h=(t^3,1,t)` in a sparse integer ring Z[s,t]. It reproduces every printed entry, both leading-minor identities, and both endpoint/exceptional matrices exactly. The script also attacks the signs with 80 exact rational normalized cases at `s` as small as `10^-12` and as large as `10^12`; `t` includes 0, 1, numbers one millionth to either side of 1, and `10^6`. It tests every principal minor at those cases. Another 500 exact generic cases use unnormalized coordinates, closed-cone directions, arbitrary mixed derivative directions, positive Hessians, and the claimed mixed self-concordance bound. All 1,591 assertions passed. Those finite checks are explicitly supplementary.

For a negative control, deleting `-log z` gives, at `(5,1,1)` and `h=(8,1,2)`,

```
-4^3 D^3[-log p][h] = [[8,-8,0],[-8,96,72],[0,72,24]].
```

Its determinant is `-24576`. With the independently found integer `u=(-10,-10,7)`, `u^T M u=-104`, so `D^3[-log p][h,u,u]=13/8>0`. The attack therefore detects the natural missing-term failure exactly; it does not produce a failure of the actual stated barrier.

## Universal sign reasoning, including degeneracies

After verifying the direct tensor matches the paper, the universal sign can be checked through discriminants, avoiding dependence on the paper's square-completion presentation. Write `P=A s^2+B s+C`. For `0<=t<1`, its coefficients are positive or nonnegative, with `C>0`; the same holds for `R/(t+2)` (at t=0 its linear and constant terms are positive). At t=1 both P and R equal `6s^2>0`. For t>1,

`disc_s P=-3(t-1)^2 (8t^3+21t^2+6t-11)<0`,

`disc_s(R/(t+2))=-3(t-1)^3 (8t^2+13t+3)<0`.

The first bracket equals `8v^3+45v^2+72v+24` at `t=1+v`; the second bracket is positive for t>1. Each leading coefficient is positive. Thus P and R are positive for all s>0, t>=0. For t!=1, the three leading minors are positive, and the matrix is positive definite.

At t=1 it is essential not to infer semidefiniteness merely by zero leading minors. Direct substitution yields a zero first row/column and a positive definite lower block: `(2r+1)(r+2)-9=(r-1)(2r+7)>0`. Its kernel is exactly the x coordinate direction. For the exceptional ray `e_x`, the direct tensor equals `2aa^T+6s bb^T`, where `a=(1,2,-3)` and `b=(0,1,-1)`; this is positive semidefinite with kernel spanned by `(1,1,1)`. At h=0 it is zero. These are real equality directions, not omitted singular cases.

The ray reduction is exact: for h_y>0, `h=h_y(t^3,1,t)+(h_x-h_z^3/h_y^2)e_x`, `t=h_z/h_y>=0`, with nonnegative coefficients. If h_y=0, the cone inequality forces h_z=0. Diagonal maps used to normalize a base point have strictly positive entries, preserve K, and are held fixed when differentiating. The required transfer is therefore a valid linear change of directions and congruence. Neither s=0 nor negative t is required: s=0 is a boundary *base* point outside the derivative domain; negative t is a direction outside the one-sided cone.

## Normality and geometry attacks

The Hessian of `m=x^(1/3)y^(2/3)` displayed on page 2 is a nonpositive rank-one matrix on the positive orthant. Continuity extends concavity to the nonnegative orthant. Its hypograph with `z>=0` is convex. The coordinate inequalities make K closed, pointed, conic; `(2,1,1)` proves a nonempty interior. Points with x=0 or y=0 necessarily have z=0 and are not missed by the barrier boundary check.

For `g=z^3/y^2`, `delta=x-g`, `f=-log delta-2log y-log z`, the direct directional identities use `D^2g[u,u]=6g(c-b)^2` and `D^3g[u,u,u]=6g(c-b)^2(c-4b)`. Thus `D^2f[u,u]=w^2+v^2+2b^2+c^2` is positive definite. The cubic term `-3wv^2+(c-4b)v^2` has the printed sign. The Cauchy bound `|c-4b|<=3 sqrt(2b^2+c^2)` is correct because the squared dual weighted norm is `1+16/2=9`. In the polarized cubic, grouping the terms as in the paper gives bounds 2,3,3,2 times `||h||_f||u||_f^2` (loose bounds are sufficient). Scaling by 25 converts 10 to the mixed standard constant 2: `25*10/(5^3)=2`. No optimality of 25 or 100 is claimed.

Logarithmic homogeneity follows from the degree-four product zp. Differentiating gives `H_F a=-grad F`, and `a^T H_F a=100`; since the Hessian is positive definite, the dual squared gradient norm is exactly 100, giving the claimed gradient bound. At a finite boundary point either z=0 or p=0, so along an interior sequence tending to it the product zp tends to 0 from above. All finite factors remain bounded. The extended function is therefore lower semicontinuous and convex. Behavior at infinity is not a barrier blow-up requirement.

## All-polynomial hyperbolicity attack

The root obstruction is independent of barrier estimates. If H had closed hyperbolicity cone K and direction e, e lies in the interior, hence all its coordinates are positive. The curved positive boundary patch is a boundary subset and must be in `{H=0}` by continuity of the real roots and nonzero leading coefficient H(e). Inserting `(z^3/y^2,y,z)` makes H vanish for every y,z>0. Clearing denominators yields a polynomial identity; division in R(y,z)[x] and primitivity of `y^2x-z^3` give p|H in R[x,y,z]. This does not assume a degree for H.

Set `a=(e_x e_y^2)^(1/3)>b=e_z>0`. On `v=(0,0,1)` the restriction is

`p(v+te)=((a-b)t-1)((a^2+ab+b^2)t^2+(a+2b)t+1)`.

The quadratic discriminant is `-3a^2<0`, and its leading coefficient is positive. The restricted polynomial is nonzero with cubic coefficient p(e)>0; moreover H(e)>0 prevents the restricted quotient from vanishing identically. Polynomial multiplication cannot cancel those nonreal roots. Thus the exclusion genuinely covers *every* homogeneous H, not merely the displayed defining polynomial or a determinant representation. A lifted or projected spectrahedral description, if one existed, would not contradict this ambient-space statement.

## Initial disposition and exact remaining scope

No substantive mathematical defect or counterexample found in the actual five-page argument. The proof of the theorem is checkable and self-contained once the stated standard barrier/hyperbolicity definitions are accepted. The exact remaining review tasks are to inspect the cited primary definitions and question, read the actual full supplement and code after this seal, examine historical deltas if present, and audit safely reproducible checker execution without treating its PASS as proof. No recommendation for research follow-up is made at this stage; default follow-up is null. This is an unrefereed AI adversarial review, not proof-assistant certification or external human peer review, and it grants no promotion clearance.
