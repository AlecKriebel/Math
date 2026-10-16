# Independent scalar-jet and ordered-connection audit of PR946

Audit family: `jet_calculus`. Target: numeric ID 6000001 / AMR-059-0001.
Authenticated original head: `7d3adb0e500b0414a49a449e7981d34ade329427`.
Authenticated original proof SHA-256: `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`.

## Verdict and limits

**PASS for the assigned mathematical family. No required correction or counterexample was found.** Sections 2–5 and 7 have a valid independent reconstruction. In particular, the scalar-jet section transforms correctly, its normal-coordinate cubic has the correct sign and factor, the finite feature map is surjective on every scalar 3-jet, its right inverse is globally smooth without compactness or a uniform singular-value bound, and the differentiated identities induce the specified connections in their stated order.

I also inspected the full claim and the intervening Hessian extension for compatibility with these conclusions. Its pointwise Schur-complement argument and restriction to an open positivity set fit the jet construction; I found no contradiction there. This report supplies an independent proof of the assigned steps, not an attribution or historical-priority finding. Proper smooth Whitney embedding, smooth bundle metrics, and the Euclidean tubular-neighborhood theorem remain explicitly identified standard inputs. Their historical source wording and the original problem's interpretation belong to the separate dependency/source audit. No literature-only closure or novelty claim is made here.

The scope is precisely smooth Hausdorff second-countable finite-dimensional manifolds without boundary, positive-definite smooth metrics, and smooth mutually dual torsion-free connection pairs; a variable nonconvex open Hessian target is allowed. Completeness, convexity, finite probability models, globally injective dual coordinates, indefinite metrics, prescribed/minimal codimension and manifolds with boundary are not established. The zero-dimensional case is elementary and separate.

## Custody, independence and success criterion

I read the root and queue policies, the queue README and selected working-tree row, the selected complete source statement and prior report, the eligibility and identity records, the charter, the original snapshot and the entire original proof. Before doing mathematics I independently compared all 33 original files against actual `git cat-file blob` output at the immutable head, the saved original disk bytes and the snapshot SHA-256 values. All agree; `SOURCE_AUTHENTICATION.json` records exact paths, byte counts and hashes. No original verification script was run. Existing independent mathematical verdicts were not imported.

The working-tree queue row read here is historical `queued 0/5`; the independently established audit gate concerns the immutable original-head `claimed_solved 4/5`. This family makes no queue, proof-budget, branch or index change. This is verification of an existing complete candidate, adding zero substantive proof-attempt turns. No new realization mechanism was introduced.

Success for this family means a coordinate-independent global jet argument and checkable sign/order identities, including curved and nonlinear-coordinate falsification attempts. A finite rank calculation alone would not establish the universal theorem. An invocation of an unproved embedding or exact-pair theorem would be a central gap. Neither substitution is needed below.

## 1. Connection algebra

Let `L` be Levi-Civita and define

\[
B(X,Y,Z)=g((\nabla-L)_X Y,Z).
\]

Torsion-freeness of `nabla` makes `B` symmetric in its first two arguments. The metric dual connection satisfies

\[
g(Y,(\nabla^*-L)_X Z)=-B(X,Y,Z).
\]

Torsion-freeness of `nabla*` therefore gives `B(X,Y,Z)=B(Z,Y,X)`. Together these two transpositions give full symmetry. Since `Lg=0`,

\[
C(X,Y,Z)=(\nabla_Xg)(Y,Z)
=-B(X,Y,Z)-B(X,Z,Y)=-2B(X,Y,Z).
\]

Thus the original signs are correct:

\[
\Gamma_{ijk}=L_{ijk}-\tfrac12 C_{ijk},\qquad
\Gamma^*_{ijk}=L_{ijk}+\tfrac12 C_{ijk}.
\]

Consequently

\[
Q_{ijk}:=\partial_k g_{ij}+\Gamma_{ijk}
=\tfrac12(\partial_i g_{jk}+\partial_j g_{ik}
+\partial_k g_{ij}-C_{ijk})
\]

is symmetric in all three indices. It is intentionally an ordinary scalar third-jet component with a nonzero lower-order Hessian, not a tensor.

## 2. Finite global scalar-jet surjectivity

Fix any immersion `e:M->R^K`. At each `p`, some `n` ambient linear functions have independent differentials after pullback: select `n` independent rows of the derivative of `e`. Their restrictions `y^1,...,y^n` form local coordinates by the inverse function theorem.

Every scalar 3-jet at `p` has a representative

\[
\sum_{|\alpha|\leq3}c_\alpha(y-y(p))^\alpha.
\]

Because the `y` are ambient linear functions, this expression is the restriction of an ambient polynomial of degree at most three. Constants arising from the translation `y-y(p)` are included in that polynomial space. Therefore the evaluation map from the **same** finite-dimensional space `P_3(R^K)` onto `J^3_p(M,R)` is surjective at every point. No cover, partition sum, interpolation theorem, compactness or extension of a global function from `M` is invoked.

Scalar jets of real-valued functions form a genuine vector bundle: coordinate transitions act linearly on the value and derivative components, with the familiar mixing of lower-order derivative components into higher ones. In local trivializations the evaluation matrix consists of smooth partial derivatives of the fixed features, hence is a smooth bundle map of constant full target rank.

With `K=2n+1`, the feature count is

\[
N=\dim P_3(\mathbb R^K)=\binom{K+3}{3}=\binom{2n+4}{3}>n.
\]

Degree-one features recover the given proper embedding `e`, so the full feature map is an injective immersion and a topological embedding. If `B` is compact in feature space, `f^{-1}(B)` is closed inside the compact set `e^{-1}(pi(B))`; it is compact. Thus properness and closedness of the image do not depend on jet surjectivity.

### Smooth splitting on noncompact manifolds

Equip the scalar-jet bundle with any smooth positive-definite bundle metric. For the fiberwise adjoint,

\[
\langle EE^\dagger v,v\rangle
=\lVert E^\dagger v\rVert^2.
\]

Surjectivity of `E` implies injectivity of `E^dagger`: a vector perpendicular to its full image is zero. Thus `EE^dagger` is positive and invertible on each fiber. In every bundle trivialization its inverse has smooth entries, by the adjugate/determinant formula, because its determinant never vanishes. Hence

\[
R=E^\dagger(EE^\dagger)^{-1},\qquad ER=I,
\]

is a global smooth right inverse. These are local smoothness statements, not bounded-operator claims on a function space. A uniform lower bound for the least singular value is unnecessary.

An explicit stress case makes the distinction concrete. Take `M=(0,infinity)` with coordinate `t` and proper embedding `e(t)=(log t,0,0)` into `R^3`. A desired jet with value, first and second `t` derivatives zero and third derivative one is represented in the effective feature variable `y=log t` by

\[
q_t(y)=\frac{t^3}{6}(y-\log t)^3.
\]

The coefficient of `y^3` is forced to be `t^3/6`, so any right inverse for these features has unbounded norm as `t` tends to infinity in the standard jet trivialization. Nevertheless these coefficients are smooth for every `t>0`. The metric `dt^2` is incomplete on this manifold; neither incompleteness nor unbounded splitting coefficients obstruct the argument.

## 3. The prescribed normal jet is smooth and covariant

The smooth geodesic ODE has a smooth exponential map on an open neighborhood of the zero section in `TM`, even for incomplete metrics. For each base point, its derivative in the vector variable at zero is the identity, so it gives a local normal-coordinate inverse germ. In a smooth local tangent frame these inverse germs depend smoothly on the base point, by the inverse function theorem applied with the base point retained as a parameter. No global injectivity radius or common positive radius is required.

Define the jet of the germ

\[
q_p(\exp_p v)=\frac12g_p(v,v)-\frac1{12}C_p(v,v,v).
\]

Changing a tangent frame acts linearly on `v` and preserves both tensor contractions. The germs therefore define a smooth global scalar-jet section. This is a section of a jet bundle, not a claim that there is one scalar function on `M` having these jets simultaneously.

In `L`-normal coordinates the value and first derivative vanish, the second derivative is `g`, and the ordinary third derivative is `-C/2`: the third derivative of a symmetric cubic contraction is six times its coefficient. For any scalar germ with zero first derivative,

\[
(L^3q)_{ijk}=\partial_i\partial_j\partial_kq
-L_{ij}^{a}g_{ak}-L_{ik}^{a}g_{aj}-L_{jk}^{a}g_{ai}.
\]

Terms containing a derivative of `L` are multiplied by the vanishing first derivative of `q`. The three displayed connection terms sum to

\[
\tfrac12(\partial_i g_{jk}+\partial_j g_{ik}+\partial_k g_{ij}).
\]

Therefore the prescribed ordinary third derivative is exactly `Q`, with the original `-1/12` coefficient and the original connection ordering.

### Direct non-affine chart law

Write `x=x(y)`, `X_a^i=partial_a x^i` and `X_ab^i=partial_a partial_b x^i` at the point. A zero-gradient scalar jet with Hessian `g` transforms as

\[
Q'_{abc}=X_a^iX_b^jX_c^kQ_{ijk}
+g_{ij}(X_{ab}^iX_c^j+X_{ac}^iX_b^j+X_{bc}^iX_a^j).
\]

There is no term involving the third derivative of the coordinate change, because it would multiply the zero scalar first derivative. Independently transforming the lowered connection gives

\[
\Gamma'_{abc}=X_a^iX_b^jX_c^k\Gamma_{ijk}
+g_{ij}X_{ab}^iX_c^j.
\]

Transforming `partial_c g_ab` contributes exactly the other two inhomogeneous terms. Hence `Q'=partial_c g'_ab+Gamma'_abc`, which verifies the scalar-jet law directly without assuming `Q` is a tensor.

## 4. Differentiation and the exact pair

Set `a=RJ` and `phi=-a`. In evaluating `E_p(a(p))`, the coefficient vector is held constant with respect to the scalar germ variable. Once the resulting pointwise identities are written as identities of smooth fields, their base-point derivatives **do** differentiate `a`:

\[
a_Af^A=0,\quad a_Af_i^A=0,\quad
a_Af_{ij}^A=g_{ij},\quad a_Af_{ijk}^A=Q_{ijk}.
\]

Differentiating the second identity gives

\[
f_i^A\partial_j\phi_A=a_A f_{ij}^A=g_{ij}.
\]

Differentiating the third gives

\[
f_{ij}^A\partial_k\phi_A
=a_A f_{ijk}^A-\partial_k g_{ij}
=\Gamma_{ijk}.
\]

Finally `phi_A df^A=0`. Thus the pair is global and exact. These deductions neither assume an embedding theorem for statistical manifolds nor transfer the central realization problem to another unsupported assertion. Positivity implies that `dphi` is injective on each tangent space, while injectivity of the map `phi` itself is unnecessary.

## 5. Compatibility with the Hessian extension and the ordered connections

For the original tubular potential, the normal covector property gives `dPsi|_S=phi` and `Psi|_S=0`. The added squared-normal term has zero first jet along `S`. Differentiating the gradient identity in fixed ambient coordinates therefore gives the full mixed identity

\[
G_{AB}(f(p))f_k^B=\partial_k\phi_A.
\]

In particular,

\[
(f^*G)_{ik}=f_i^A\partial_k\phi_A=g_{ik},\qquad
G(f_{ij},f_k)=f_{ij}^A\partial_k\phi_A=\Gamma_{ijk}.
\]

These equations recover the `G`-orthogonal tangential projection of `D` as the specified `nabla`, with no connection swap. Orthogonal projection is valid since the tangent metric is positive definite. Projecting ambient duality then makes the other induced connection the unique `g`-dual of `nabla`, namely the specified `nabla*`.

For completeness, the original positivity estimate is internally sufficient: along `S` the tangent block `A` is positive, the mixed block is `B`, and the normal block after correction is `2(1+t)I`, where `t=tr(A^{-1})||B||_HS^2`. Thus

\[
B^tA^{-1}B\leq tI,\qquad
2(1+t)I-B^tA^{-1}B\geq(2+t)I>0.
\]

All quantities are smooth bundle invariants and finite pointwise. Defining `U` by positivity of the Hessian gives one open neighborhood of the whole image without a uniform estimate. This is compatible with unbounded coefficients and variable tubular radii.

The metric dual of `D` has

\[
(\Gamma^*)^C_{AB}=G^{CD}\partial_A G_{BD}.
\]

Its torsion vanishes because the third derivatives of `Psi` are symmetric. The functions `eta_E=partial_E Psi` have invertible differential `G` and satisfy

\[
\partial_A\partial_B\eta_E
-(\Gamma^*)^C_{AB}\partial_C\eta_E=0.
\]

They are local affine coordinates for the dual connection. Flatness follows locally and hence globally as a tensor identity; global injectivity of the gradient map is unnecessary. Necessity of torsion-freeness follows from projecting the torsion identity for either ambient connection. The countable discrete zero-dimensional case properly embeds in the line and has no nontrivial connection or metric tangent data.

## 6. Independent falsifiable controls

`independent_checks.py` uses only standard-library exact rational arithmetic and imports no original script. Its machine-readable output is `INDEPENDENT_CHECKS.json`. The controls passed:

1. The connection and cubic identities for the positive metric `(2+u+2v+u^2+v^2)(du^2+dv^2)`, whose Gaussian curvature at the origin is `-3/16`, with a nonzero symmetric cubic having components `C111=2`, `C112=-1`, `C122=3`, `C222=-4`.
2. The complete scalar third-jet law under a chart transformation with determinant `3` and nonzero second and third derivatives. All eight ordered triples agree; omission of the inhomogeneous connection term is detected.
3. The normal-coordinate cubic factor. Doubling the original cubic coefficient is detected.
4. For a two-dimensional curved proper feature embedding in `R^5`, scalar-jet rank is `10` out of `10` at `(0,0)`, `(1/2,-1/3)` and `(5,-7)` using all `56` features. Removing the constant at the origin drops rank to `9`; using only degree-two features of a linear embedding gives rank `6`.
5. Polynomial identities along `f(t)=(1,t,t^2,t^3)` for `g=1+t^2` and `C=2+2t^3`, with `Gamma_lower=t-1-t^3`. Using `phi=+a` is detected.
6. An explicit local polynomial Hessian extension at `t=0`, with positive leading principal minors `20,20,395,7800`. It induces lowered coefficients `-1` from `D` and `+1` from `D*`, correctly recovering the ordered pair; swapping them is detected. Its ambient third derivative `Psi_111=2` also confirms the cubic sign.

The local polynomial extension is only a finite verification witness of the same first-jet extension principle, not a proposed new global proof mechanism. The finite checks support reproducibility and mutation detection; the preceding arguments establish the universal statements.

## 7. Findings register and strongest verified conclusion

Required findings: **none**. No central gap, circularity, failed coordinate transformation, missing compactness assumption, incorrect factor/sign or connection-order mismatch was found.

Optional exposition findings, none needed for correctness:

- **O1:** Add the explicit chart transformation law in section 3 of this report to make the non-tensorial role of `Q` immediately checkable. The original normal-coordinate argument already establishes it.
- **O2:** Explicitly call the prescribed scalar jet section nonholonomic and distinguish the germ variable from the base point when explaining the two differentiations. The original text's instruction to hold coefficients constant in the jet evaluation is correct.
- **O3:** The `log t` example above is a concise illustration of why unbounded splitting coefficients on a noncompact manifold do not create a smoothness obstruction. This is explanatory, not an added hypothesis.

Strongest verified statement: under the stated proper-embedding and tubular-neighborhood inputs, the original finite scalar-jet construction supplies a global smooth exact pair satisfying `df dphi=g`, `f_ij dphi=Gamma_ijk` and `phi df=0`; the original positive Hessian extension then induces the exact ordered dual connection pair on the whole manifold. No repair or additional invariant is needed within this claim's scope. Overall publication readiness, exact historical source interpretation and priority are not decided by this family.

Audit completion: **100% of this assigned family**. This is not a percentage estimate of historical novelty or of the wider publication workflow.
