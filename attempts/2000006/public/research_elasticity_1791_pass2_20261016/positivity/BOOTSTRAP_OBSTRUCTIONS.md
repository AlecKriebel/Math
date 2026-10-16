# Why the attempted endpoint bootstrap does not yet close

E-6322, shared pass 2, 2026-10-16.

## 1. What a successful bootstrap would need

Write H(F)=a|F|^6+b|cof F|^3+c(det F)^2 and B(F)=d(det F)^{-2} on GL^+(3). The baseline supplies H(Dy), B(Dy) in L^1. Pass 1 proves the implication

Dy in L^{6q}  =>  B(Dy) in L^q,  q>1,

for minimizers, via the global pressure equation. It does not prove the premise, and it does not run backward. An actual improvement to Dy in L^{6+delta}, or a Dini modulus for the positive-degree tensor, requires a new estimate that uses the minimizer inequality with admissible competitors.

This pass tested conventional cut-off Caccioppoli, finite composition comparisons, and a finite-valued tangent-barrier regularization. None yielded such an unconditional gain.

## 2. Two independent failures in the conventional Caccioppoli argument

A conventional cut-off comparison with an affine map ell(x)=Ax+b is

v=(1-eta)y+eta ell,

Dv=(1-eta)Dy+eta A+(ell-y) tensor Deta.

The frozen density causes two distinct problems.

First, Dv need not stay in GL^+(3). This is not repaired by taking one universal small interpolation parameter. For any sufficiently small tau>0, take

F_epsilon=diag(-epsilon,-2epsilon,1), A=I.

The determinant of (1-tau)F_epsilon+tau I is negative whenever

tau/[2(1-tau)] < epsilon < tau/(1-tau).

Both endpoint matrices have positive determinant, and |F_epsilon| remains bounded as tau tends to zero. Thus bounded gradient size alone cannot justify this cut-off interpolation. The rank-one cut-off term introduces another determinant sign issue. An energy estimate showing that the bad set is small does not help: a positive-measure negative-determinant set gives infinite competitor energy, however small that measure is.

This is a matrix-level obstruction to the proposed comparison step, not a constructed singular minimizer.

Second, the density has no global upper 6-growth bound. Along the bounded matrices F_epsilon=diag(1,1,epsilon), the barrier is d epsilon^{-2}. Therefore no constants L,C independent of F can satisfy W(F)<=L|F|^6+C on GL^+(3). At large norm, the problem is not only a bounded-matrix singularity: along diag(L,L,L^{-m}) with m>5, the barrier grows as L^{2m-4}, faster than the degree-six positive terms.

These failures occur before invoking Sobolev–Poincaré or Gehring. A reverse Hölder conclusion cannot be imported after omitting either hypothesis.

## 3. What uniformly bi-Lipschitz comparisons can preserve

Material and target compositions are genuinely admissible, as checked in pass 1. But a composition with fixed bi-Lipschitz constant K preserves the gradient's L^s integrability class, for every finite s.

For a material map phi with A=Dphi, ||A|| and ||A^{-1}|| bounded by K, change of variables gives the transformed gradient FA^{-1} and determinant weight k=det A. Since

|FA^{-1}| >= K^{-1}|F|,  k>=K^{-3},

the transformed |F|^s integral is bounded below by K^{-(s+3)} times the original one, and an analogous upper bound follows from the reverse estimates. For target compositions, the inequality |AF|>=K^{-1}|F| gives the corresponding statement without a material change of variables.

Thus fixed-distortion comparisons cannot themselves act as a direct Lipschitz truncation of a genuinely nonintegrable gradient tail. A proposed truncation has to allow growing distortion and account quantitatively for its determinant and cofactor costs.

This does not prove that minimality under uniformly controlled comparisons has no regularity consequences. It only identifies what a direct truncation construction of this form cannot accomplish. The variations lane derives an actual finite radial comparison and a low-Jacobian estimate; its estimate still contains the un-improved L^1 positive-degree energy.

## 4. A convex finite-valued regularization and its exact costs

For epsilon>0, define on the entire real line

h_epsilon(J) = J^{-2},                         J>=epsilon,
             = 3epsilon^{-2}-2epsilon^{-3}J,  J<epsilon.

This is the tangent-line continuation of J^{-2}. It is convex, C^1, nonnegative, and finite even at nonpositive J. Put

W_epsilon(F)=H(F)+d h_epsilon(det F).

This regularized density is finite on all matrices and has a polyconvex representation. It has upper 6-growth with constants depending on epsilon. The original orientation constraint is absent from its minimization problem, so a regularized minimizer is not automatically an admissible E-6322 competitor.

### 4.1 Uniform energy does control certain bad sets

Let y_epsilon minimize the regularized functional with the same prescribed trace. The smooth allowed extension is a competitor, and h_epsilon(J)<=J^{-2} for J>0. Hence

I_epsilon(y_epsilon)<=I(G).

This gives a uniform L^6 gradient bound. It also gives the exact bounds

|{det Dy_epsilon<=epsilon}| <= epsilon^2 I(G)/d,

integral_Omega (det Dy_epsilon)_- <= epsilon^3 I(G)/(2d).

Indeed h_epsilon>=epsilon^{-2} on J<=epsilon, and h_epsilon>=2epsilon^{-3}J_- for all J. The negative part tends to zero in L^1, but those maps can still fail positive determinant on sets of positive measure for each epsilon. Neither estimate gives a uniform positive lower determinant bound.

### 4.2 The exact optimal additive p-growth constant blows up as epsilon^{-6}

Let

A0=27a+3sqrt(3)b+c.

Along F=-tI, t>=0, one has |F|^6=27t^6, det F=-t^3, and

W_epsilon(-tI)=A0 t^6+3d epsilon^{-2}+2d epsilon^{-3}t^3.

Suppose one seeks an upper bound

W_epsilon(F)<=L|F|^6+C_epsilon

with L fixed independently of epsilon. Necessarily 27L>A0 for this ray. With kappa=27L-A0>0 and z=t^3, maximizing the difference over z>=0 gives

sup_t [W_epsilon(-tI)-L|-tI|^6]
= d^2 epsilon^{-6}/kappa+3d epsilon^{-2},

attained at z=d epsilon^{-3}/kappa. Therefore

C_epsilon >= d^2 epsilon^{-6}/(27L-A0)+3d epsilon^{-2}.

In fact this is the exact optimal constant over all matrices, not just a raywise lower bound. Put t=|F|/sqrt(3). The elementary minor inequalities give H(F)<=A0 t^6 and |det F|<=t^3, both with equality on conformal matrices. Since

h_epsilon(J)<=3epsilon^{-2}+2epsilon^{-3}|J|

for every real J, the same concave quadratic in z=t^3 bounds W_epsilon(F)-L|F|^6 from above for every F. The negative conformal ray attains that upper bound at its optimizer. Thus

sup_F [W_epsilon(F)-L|F|^6]
= d^2 epsilon^{-6}/(27L-A0)+3d epsilon^{-2}

for L>A0/27. For L<=A0/27 the supremum is infinite. The epsilon^{-6} divergence is therefore not merely a careless Young-inequality estimate.

Even when only positive determinants are considered, the bounded rank-two limit diag(1,1,0) forces an additive cost of order epsilon^{-2}; allowing all matrices in the regularized comparison class creates the sharper epsilon^{-6} obstruction above.

### 4.3 The usual reverse-Hölder estimates are consequently nonuniform

For finite-valued p-growth functionals, conventional cut-off proofs lead schematically to

average_{B_r}|Dy_epsilon|^6
<= C[(average_{B_R}|Dy_epsilon|^2)^3+C_epsilon]

on fixed-ratio nested balls, after Sobolev–Poincaré, with analogous nonhomogeneous estimates near the boundary. A Gehring improvement may give an exponent independent of epsilon if L is fixed, but these standard estimates still retain the diverging additive source C_epsilon. Uniform original energy alone does not erase that term from the proof.

Thus an argument which first regularizes, then invokes finite-valued p-growth higher integrability, and finally lets epsilon tend to zero has not obtained the uniform higher-integrability norm required for the last passage. This is a failure of the displayed proof route, not a theorem that all possible regularizations or all possible estimates must fail.

### 4.4 Upper ellipticity constants also deteriorate

At F=diag(1,1,epsilon), the determinant changes by the increment in the rank-one direction E33. From the positive side of the regularization threshold,

D^2[d(det F)^{-2}][E33,E33]=6d epsilon^{-4}.

The positive-degree contribution stays bounded for 0<epsilon<=1. Hence the standard upper ellipticity bound is not uniform, even in a bounded set of matrices. The main a|F|^6 term supplies a positive rank-one lower bound near these matrices, but it does not remove the epsilon-dependent upper coefficient. A uniform Schauder or Meyers argument must address that anisotropic singularity rather than silently discard it.

## 5. Exact direction of the moment-transfer obstruction

The exact lane constructs an identity-boundary triangular deformation on a smooth ball with determinant uniformly between 1/2 and 3/2, finite frozen energy, and gradient outside L^{6+delta} for every delta>0. Its transverse profile is

u(r)=r^{2/3}[log(e/r)]^{-sigma},  sigma>1/6,

multiplied by smooth compactly supported cutoffs. The derivative has sixth-power radial integral comparable to integral dr/[r(log(e/r))^{6sigma}], while every higher power diverges. The full construction and checks are in `../exact/ENDPOINT_CERTIFICATION.md`, Section 3; its separate continuous-Q pressure obstruction is in Section 4.

This is not a minimizer. It establishes the narrow point needed here: even all inverse-Jacobian moments, or a uniform determinant lower bound by itself, cannot be substituted for a gradient higher-integrability estimate. The pressure transfer is one-way; a backward step needs additional minimizer structure.

## 6. Literature checks relevant to this attempted route

Schiffer's *A-free truncation and higher integrability of minimisers*, Calculus of Variations and PDE 64 (2025), states its natural p-growth hypothesis as a finite upper bound by nu|w|^p+c. The frozen singular law does not satisfy that premise. The available curl-free truncation therefore cannot be used without separately preserving the nonlinear determinant constraint. https://doi.org/10.1007/s00526-024-02855-w

Dougherty's institutional thesis abstract, *Higher gradient integrability of minimizers for functionals with polyconvex local energies* (1995), describes lower-order quasiconvex perturbations of gradient powers and a different quadratic-gradient/asymptotically-linear-determinant model. It does not state a theorem for this inverse-barrier law. Only the institutional abstract was inspected here, not the full thesis. https://docs.lib.purdue.edu/dissertations/AAI9601489/

The separate literature lane checks further asymptotic p-growth theorems and their exclusions. None of these source observations is an exhaustive novelty or impossibility claim.

## 7. Pass outcome

The new Dini pressure theorem gives a precise sufficient regularity target and a quantitative whole-domain pressure bound. The regularization calculation proves specific diverging constants and the comparison analysis identifies the missing admissibility step. No unconditional Caccioppoli or reverse-Hölder inequality with the required gain was proved for the frozen full-class minimizer.

Further work must exploit structure not captured by the present L^1 pressure estimate: a genuinely controlled determinant-preserving replacement, an independent strain-energy improvement, or another mechanism ruling out the relevant singular configurations. The benchmark remains unresolved.
