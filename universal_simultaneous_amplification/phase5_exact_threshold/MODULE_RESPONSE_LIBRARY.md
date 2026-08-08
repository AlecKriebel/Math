# Exact module-response library

Last updated: 2026-08-08.  This is a live library, not a completeness claim.

For a dilute gadget type `H`, write its normalized leading correction as

\[
v_H(r)=(B_H(r),D_H(r)).
\]

Nonnegative dilute mixtures add their response vectors after the full
singleton, reciprocal-invasion, macro-fixation, and far-field terms have
been included.

## 1. Ordinary hub leaf

Per leaf relative to the dilute satellite scale,

\[
\boxed{v_L(r)=\left({1\over r-1},-1\right).}           \tag{M1}
\]

Thus adding `lambda` leaves adds
`(lambda/(r-1),-lambda)`.

## 2. Strong clique satellite `K_s`

For order `s>=2` and internal scale `sigma>0`,

\[
\boxed{
b_s(r,\sigma)={s(\sigma-1)\over1+\sigma(r^s-1)},}
\]

\[
\boxed{
d_s(r,\sigma)
 ={s\{sr-r^s-(s-1)\sigma\}
   \over (s-1)\sigma+sr(r^{s-1}-1)}.}                 \tag{M2}
\]

With ordinary leaves, feasibility requires a `lambda>0` satisfying

\[
b_s+{\lambda\over r-1}>0,
\qquad
d_s-\lambda>0,
\]

hence necessarily

\[
d_s+(r-1)b_s>0.                                      \tag{M3}
\]

At `r=3/2`, `s=2` is the unique feasible clique satellite.  The `K_2` plus
leaf tangency gives the sextic `R_hyb`.

## 3. Optimized `K_2`--leaf hybrid

For `s=2`, write

\[
B(r;\sigma,\lambda)
 ={2(\sigma-1)\over1+\sigma(r^2-1)}+{\lambda\over r-1},
\]

\[
D(r;\sigma,\lambda)
 ={2\{r(2-r)-\sigma\}\over\sigma+2r(r-1)}-\lambda.   \tag{M4}
\]

The optimal fixed pair `(sigma_*,lambda_*)` is positive on every
`1<r<R_hyb`, with simultaneous tangency at `R_hyb`.

## 4. Strong integrated finite gadget

Let a fixed gadget have portal loads `x_i>=0`, symmetric internal weights
`a_ij>=0`, and

\[
d_i=x_i+\sum_j a_{ij}.
\]

Let `u_U(i)` be the exact local probability, starting from mutant singleton
`i`, of producing a surviving core lineage.  Put `p=1-1/r`, `P=sum_i x_i`,

\[
s_B=r\sum_i x_i u_B(i)-(r-1)\sum_i{x_i\over d_i},
\]

\[
s_D=r\sum_i{x_i u_D(i)\over d_i}-(r-1)(P+r-1).
\]

The full tangent, including ordinary-core singleton Poisson response, is

\[
\boxed{B_H={\sum_i u_B(i)\over p}-s+{s_B\over(r-1)^2},}
\]

\[
\boxed{D_H={\sum_i u_D(i)\over p}-s+1+{s_D\over(r-1)^2}.} \tag{M5}
\]

These formulas reduce the finite-gadget search to exact local absorption.
No completeness theorem for positive internal matrices is proved.

### Portal-clone equality manifold

If every leading internal weight is zero, then exactly

\[
\boxed{B_H=0,qquad
D_H=-\sum_i{(x_i-1)^2\over1+(r-1)x_i}\le0.}           \tag{M6}
\]

Equality holds exactly at `x_i=1` for every vertex.  The first-order vector
then vanishes, leaving a genuine second-order problem.

## 5. Symmetric correlated `K_2` doublet

For two identical strong pairs with common scale `sigma` and symmetric
portal-scale coupling `u>=0`, define

\[
H(z,\theta)={z(z+1+r^2\theta)
 \over (z+1)^2+\theta\{1+(1+r^2)z\}},
\]

\[
H_B=H(\sigma(r^2-1),\sigma u),
\qquad
H_D=H(2r(r-1)/\sigma,u).
\]

Then

\[
\boxed{F_B=4\left({rH_B\over(r+1)p}-1\right),
\qquad
F_D=4\left({H_D\over2p}-1\right).}                  \tag{M7}
\]

At `r=R_hyb`,

\[
F_D+(R_{\rm hyb}-1)F_B\le0,
\]

with equality only at `u=0,sigma=sigma_*`.  This is a first-order symmetric
doublet obstruction only.  Letting `(u,sigma-sigma_*)` vanish with graph
size creates an unresolved second-order regime.

## 6. Weighted-leaf regimes

The phase-4 weighted-leaf classification contains exact response vectors
for common-hub and distinct-hub heavy leaves, including the far-field
ordinary-singleton term.  In every audited regime at `r>=3/2`, the
leaf-eliminated separator is nonpositive.  These vectors are retained as
negative generators and must not be replaced by local-only approximations.

Canonical source:
`phase4_landmark_closure/threshold/endpoint_construction_v2/weighted_leaf_scaling/`.

## 7. Response-cone problem

For an admissible menu `H_1,...,H_m` and nonnegative densities `c_j`, the
first-order target on an interval `I` is

\[
\sum_jc_jB_{H_j}(r)>0,
\qquad
\sum_jc_jD_{H_j}(r)>0
\quad(r\in I).                                        \tag{M8}
\]

The current library proves feasibility on every compact subinterval of
`(1,R_hyb)`.  It neither proves nor refutes feasibility on every compact
subinterval of `(1,2)` when the menu may grow with the diagonal index.

## 8. Missing generators with priority

1. second-order perturbations of (M6);
2. asymmetric correlated pairs or triples;
3. positive-internal-matrix gadgets from (M5);
4. growing-rank modules with exact spectral recurrences;
5. nonseparated modules whose fast law is not supported on monomorphic
   gadget states.
