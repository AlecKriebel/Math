# Pass 2: sharp endpoint obstructions and independent exact certification

E-6322, 2026-10-16. The frozen density and full admissible class are unchanged. All a,b,c,d are positive. This report contains new auxiliary results and checks, not a global counterexample or a proof of Jacobian positivity for minimizers.

## 1. A single compatible homeomorphism saturates every inverse-integrability endpoint

Fix 1/6<kappa<1/2. On the unit ball, put

L(r)=r^(−1/2)[log(e/r)]^(−kappa),  0<r<=1,

y(x)=(L(r)x1,L(r)x2,L(r)^(−5)x3),  y(0)=0.

This is an identity-trace admissible homeomorphism. It has finite benchmark energy, but its inverse has exactly the available endpoint moment exponents:

Dv belongs to L^p iff 0<p<=9/5;
cof Dv belongs to L^s iff 0<s<=9/4;
det Dv belongs to L^t iff 0<t<=3.

The statements below concern the actual inverse map v, with respect to target Lebesgue measure. For Sobolev membership we use p>=1; the smaller exponents are just moment statements. In particular no larger exponent can follow from the original energy, the full smooth identity trace, and even global homeomorphism, without an additional minimizing or differential-equation argument.

### 1.1 Exact derivative and determinant

Write n=x/r and

beta(r)=r L'(r)/L(r)=−1/2+kappa/log(e/r).

Then −1/2<beta<0 and L>=1. Define

D=diag(L,L,L^(−5)),
w=beta(n1,n2,−5n3),
M=I+w tensor n.

Direct differentiation gives Dy=DM, and the determinant lemma gives

J=L^(−3) Delta,
Delta=1+beta(1−6n3^2).

Uniformly in r and n,

1/2<Delta<7/2.

Both M and M^(−1)=I−(w tensor n)/Delta are uniformly bounded. Consequently

|Dy| comparable to L,
|cof Dy| comparable to L^2,
J comparable to L^(−3),
|(Dy)^(−1)| comparable to L^5,
|cof((Dy)^(−1))|=|Dy|/J comparable to L^4.

All comparisons are two-sided, with constants depending only on kappa. For the cofactor comparison one can use cof(DM)=cof D cof M and the uniform invertibility of cof M; cof D=diag(L^(−4),L^(−4),L^2).

### 1.2 Finite energy and genuine homeomorphism

The three possibly large positive/barrier terms are all comparable to L^6. Their radial integral is

integral_0^1 r^2 L(r)^6 dr
= integral_0^1 dr/[r(log(e/r))^(6kappa)]
=1/(6kappa−1)<infinity.

The determinant-square term is bounded. The continuous extension at 0 follows from rL(r)->0 and rL(r)^(−5)->0. The classical gradient off 0 extends as the weak W^{1,6} gradient: integration by parts on punctured balls has a boundary error bounded by C epsilon^2 sup_{|x|=epsilon}|y(x)|, which tends to zero. Thus the map belongs to the full frozen class.

To prove injectivity without an unverified global-inverse theorem, set

A(r)=rL(r),  C(r)=rL(r)^(−5).

Their logarithmic derivatives are 1+beta>1/2 and 1−5beta>1, so both increase strictly from 0 to 1. The image of the sphere of radius r is the ellipsoid with semiaxes A(r),A(r),C(r). For every nonzero target X in B1, the function

(X1^2+X2^2)/A(r)^2 + X3^2/C(r)^2

decreases strictly from infinity to |X|^2<1 as r runs from 0 to 1. It therefore equals 1 at exactly one r. Then x1=X1/L(r), x2=X2/L(r), x3=X3 L(r)^5 gives the unique preimage. This establishes a homeomorphism of the closed ball, and a smooth diffeomorphism off 0. The boundary map is exactly the identity, certified by G(x)=x.

### 1.3 Sharp inverse exponents

Change of variables on punctured balls, followed by monotone convergence, gives

integral_B1 |Dv(X)|^p dX comparable to integral_0^1 r^2 L(r)^(5p−3) dr,

integral_B1 |cof Dv(X)|^s dX comparable to integral_0^1 r^2 L(r)^(4s−3) dr,

integral_B1 |det Dv(X)|^t dX comparable to integral_0^1 r^2 L(r)^(3t−3) dr.

For any real exponent m,

integral_0^1 r^2 L(r)^m dr
=integral_0^1 r^(2−m/2)[log(e/r)]^(−kappa m) dr.

It is finite when m<6, finite at m=6 because 6kappa>1, and infinite when m>6. This proves all three sharp thresholds simultaneously for this **single fixed map**.

The inverse is genuinely W^{1,9/5}, not merely a formal inverse derivative: it is continuous and bounded, smooth off 0, and the displayed classical derivative is integrable. Integration by parts across a shrinking target sphere has a boundary term tending to zero, so there is no singular weak-derivative contribution at 0.

### 1.4 Scope

This example is not a minimizer. For identity data, null-Lagrangian identities and strict convexity in the F variable give the identity as the unique full-class minimizer. The example proves sharpness of the **class-level inverse moment arithmetic**, not sharpness of any regularity theorem specific to minimizers.

## 2. The power family and failure of naive Jacobian hard truncation

The variations lane proposed the simpler exact power family

y_alpha(x)=(r^(−alpha)x1,r^(−alpha)x2,r^(5alpha)x3),  0<alpha<1/2.

The same calculation, now beta=−alpha, gives

J=r^(3alpha)(1−alpha+6alpha n3^2),
|Dy| comparable to r^(−alpha),
|cof Dy| comparable to r^(−2alpha),
P(Dy) comparable to r^(−6alpha),

where P(F)=a|F|^6+b|cof F|^3+cJ^2. It has identity trace and is a homeomorphism, by the same nested-ellipsoid argument. Energy is finite exactly for alpha<1/2, whereas

P(Dy)/J comparable to r^(−9alpha)

is nonintegrable whenever alpha>=1/3.

For an ideal isotropic material change with derivative A=k^(1/3)I and determinant k, homogeneity gives the exact transformed density

k W(F A^(−1))=P(F)/k+d k^3 J^(−2).

Setting k=J/epsilon on {J<epsilon} would replace the Jacobian by epsilon, but the positive term becomes epsilon P(F)/J. For the preceding admissible maps with 1/3<=alpha<1/2, that ideal positive contribution is infinite. Thus a direct hard-truncation proposal must first solve both compatibility of its material derivative and finiteness of its transformed energy. The latter already fails for this formal isotropic rule on legitimate competitors.

This does not rule out a more sophisticated comparison, and it does not claim that such a matrix field A is a gradient. It identifies a precise obstruction before that compatibility issue is even reached.

### Additional local nonstationarity check

Along the positive x3-axis, the third cofactor row is r^(−2alpha)e3 and J=(1+5alpha)r^(3alpha). The third component of the barrier stress divergence is exactly

18d alpha (1+5alpha)^(−3) r^(−11alpha−1).

The positive part's third-component divergence is O(r^(alpha−1)). The barrier term therefore cannot be canceled near 0. A compactly supported additive test in a small ball around a positive-axis point is admissible for sufficiently small amplitude and supplies a strict descent direction. Energy scaling balance does not make this ansatz stationary.

## 3. All inverse-Jacobian moments do not bootstrap gradient integrability backward

This independently certifies the positivity lane's proposed endpoint example.

In B(0,3), use cylindrical coordinates rho=sqrt(x1^2+x2^2), z=x3. Let

u(rho)=rho^(2/3)[log(e/rho)]^(−a0)

near 0, with a0>1/6, smoothly cut off to zero for rho>=1. Let chi be a nonzero smooth function compactly supported in |z|<1. Set

y(x)=(x1,x2,z+epsilon u(rho)chi(z)).

Choose epsilon>0 with epsilon ||u chi'||_infinity<=1/2. Then

J=1+epsilon u(rho)chi'(z) lies in [1/2,3/2].

The whole deformation differs from the identity only in a compact interior cylinder. Every vertical fiber map is strictly increasing and fixes the endpoints, so this too is a homeomorphism with the permitted entire-boundary identity trace.

Near 0,

u'(rho)=rho^(−1/3)[log(e/rho)]^(−a0)
            [2/3+a0/log(e/rho)].

On a z subinterval where |chi| is bounded below, the large gradient part is comparable to |u'|. Cylindrical integration gives

integral |Dy|^6 finite iff 6a0>1,

because the critical integral is integral d rho/[rho(log(e/rho))^(6a0)]. For every delta>0, the L^{6+delta} integral diverges by its power rho^(−1−delta/3). All inverse-Jacobian moments are bounded, since J>=1/2.

Thus no reverse transfer from arbitrary high moments of J^(−1) to any extra integrability of Dy is available from admissibility and algebra alone. It remains possible that minimization supplies an independent gain; this example is not a minimizer.

## 4. A continuous, even negative-definite pressure tensor can support unbounded pressure

This is an exact **abstract tensor-equation obstruction**. Q below is not asserted to equal the constitutive tensor Q(Dy) of any minimizer.

On B1, let

L0(r)=log(e^2/r),
p(r)=log L0(r),
q(r)=r^(−2) integral_0^r s/L0(s) ds,
Q(x)=q(r) n tensor n for x!=0,  Q(0)=0.

Since

p'(r)=−1/[r L0(r)],
q'(r)+2q(r)/r=1/[r L0(r)],

one has exactly

grad p+div Q=0

away from 0. The identity also holds distributionally on the entire ball: grad p and DQ are locally integrable and the shrinking-sphere boundary terms vanish.

The elementary bounds

3/[8(L0(r)+log 2)] <= q(r) <= 1/[2L0(r)]

follow by integrating respectively over [r/2,r] and [0,r]. Hence Q is bounded and continuous at 0. But p is positive, unbounded, and belongs to every finite L^s. Moreover j=p^(−1/2), extended by j(0)=0, is continuous, has essential infimum zero and satisfies j^(−s) in L^1 for every finite s.

Subtracting the constant tensor I leaves div Q unchanged and makes Q−I uniformly negative definite, since q<=1/4. Thus even a definite sign on this otherwise arbitrary tensor cannot rescue an L-infinity pressure estimate.

This demonstrates that boundedness or mere continuity of the pressure tensor, even together with all finite pressure moments and continuity of the scalar j, does not logically imply a positive lower bound for j through the distributional pressure equation alone. The modulus at 0 behaves like 1/log(e^2/r), and its Dini integral diverges. This is consistent with the positivity lane's separate proposed Dini-modulus sufficient condition.

## 5. Independent exact check of the concentric material comparison

Notation: P=W_+, B=dJ^(−2), U=F^T DW_+(F). Then

U=6a|F|^4 F^T F
  +3b|cof F|[|cof F|^2 I−(cof F)^T(cof F)]
  +2cJ^2 I.

Every term is positive semidefinite, and tr U=6P. The inner stress is

E=(P+3B)I−U.

For 0<r<R and s=(r/R)^3, put m=s/(1−s), ell=r^3/(1−s). The proposed material flow has core radius scaling (1−t)^(1/3), shell radius satisfying

f_t(rho)^3=(1+mt)rho^3−ell t,

and is fixed outside B_R. Its generator is V=−x/3 in B_r and

DV=[m/3−ell/(3rho^3)]I+ell rho^(−3)n tensor n

in the shell. In particular, div V is −1 in the core and m in the shell. Pairing with E gives

core: E:DV=P−3B;
shell: E:DV=3mB−mP+2ell rho^(−3)P−ell rho^(−3)U_nn.

The stationarity identity therefore rearranges exactly to

B(B_r)=s B(B_R)+(1−s)P(B_r)/3
       +(1/3) integral_shell [2(r/rho)^3−s]P
       −(1/3) integral_shell (r/rho)^3 U_nn.

The signs, coefficients and dimensions in the variations lane's identity are correct. Dropping the last term gives an upper bound because U_nn>=0. This computation checks the identity; the variations report separately justifies approximation/admissibility of the piecewise-smooth material test.

## 6. Independent check of the smooth angular anisotropic stationarity obstruction

The counterexample lane considers

y_i(r,theta)=r^(alpha_i) phi_i(theta),
0<alpha1<=alpha2<=alpha3,
J=r^gamma j(theta),  gamma=alpha1+alpha2+alpha3−3>0,

with smooth angular functions and j>0 on the sphere.

At a direction theta0 where phi1=phi2=0, the first two gradient rows are tangent to the sphere. Hence

C3=grad y1 cross grad y2
  =kappa0 r^(alpha1+alpha2−2) theta0,

with kappa0!=0 because J>0. Such a direction exists by positive local degree: the origin is an isolated zero, nearby regular values have positive local degree, and sufficiently small points on the third target axis must be attained. This is a topology argument about the exact ansatz, not an assumption about arbitrary minimizers.

Piola's identity gives the barrier's third divergence component at that direction:

6d kappa0 gamma j(theta0)^(−3)
   r^(alpha1+alpha2−3−3gamma),

whose coefficient is nonzero. The positive-part third divergence terms have the bounds

a term: O(r^(4alpha1+alpha3−6));
b term: O(r^(3alpha1+alpha2+alpha3−6));
c term: O(r^(2alpha1+2alpha2+alpha3−6)).

For the b term, varying row 3 changes only cofactor rows 1 and 2; this is essential to the improved component estimate. The last two powers are no smaller than the a-term power. The exponent gap between the least positive-part power and the barrier power is

eta=2(3alpha1+alpha2+2alpha3−6).

Whenever eta>0, the nonzero barrier divergence dominates and stationarity is impossible near that ray. Under the balanced energy relation gamma=3−3alpha1, this simplifies to eta=2(alpha3−alpha1)>0. The strict inequality follows because gamma>0 excludes the all-equal case. This independently validates the companion report's general exclusion, including its cofactor order and its balanced-scaling specialization.

## 7. Independent check of the whole-boundary collar comparison

For the variations lane's tent normal field eta=−f_h(delta) grad delta, take the Hessian norm in the Frobenius convention. Under h sup|D^2 delta|<=1 and h sup|Delta delta|<=1/4, one has |Deta|<=2. On the inner collar div eta<=−3/4; on the outer collar div eta<=5/4. Since |PI−U|<8P, the stationarity identity implies

(9/4)B(C_h)<=16P(C_{2h})+(15/4)[B(C_{2h})−B(C_h)].

Thus its displayed conclusion is exactly

B(C_h)<=(5/8)B(C_{2h})+(8/3)P(C_{2h}).

The finite maps preserve each normal coordinate line and send s to s−t f_h(s), which is strictly increasing for |t|<1 and fixes the endpoints 0 and 2h. The full-boundary trace and both signs of the variation are therefore compatible. The estimate remains an integral estimate with an initially L^1 source P, not a lower Jacobian bound.

## 8. Independent check of tangent-barrier regularization constants

For h_epsilon(J)=J^(−2) when J>=epsilon and h_epsilon(J)=3epsilon^(−2)−2epsilon^(−3)J otherwise, test the regularized density at F=−tI, t>=0. Put A=27a+3 sqrt(3)b+c and z=t^3. Then

W_epsilon(−tI)=A z^2+2d epsilon^(−3)z+3d epsilon^(−2).

If W_epsilon(F)<=L|F|^6+C_epsilon with a fixed L>A/27, maximizing the difference on this ray gives

C_epsilon>=d^2 epsilon^(−6)/(27L−A)+3d epsilon^(−2),

attained at z=d epsilon^(−3)/(27L−A). Hence the polynomial-growth additive constant cannot be uniform. Separately, the barrier Hessian in direction E33 at diag(1,1,epsilon) is 6d epsilon^(−4). These computations validate the positivity lane's regularization obstruction; they do not preclude a different uniform-estimate method.

## 9. Verification and result boundaries

`verify_endpoints.py` checks the determinant lemma, logarithmic derivative, all endpoint arithmetic, hard-truncation homogeneity, material-flow coefficients and anisotropic exponent identities. Its output is `verification.json`.

Every actual map constructed here has the allowed smooth identity boundary trace and finite energy. Every one is nonminimizing by the full-class affine uniqueness lemma. The pressure-tensor example is explicitly abstract. The new results close several tempting unjustified bootstrap/truncation steps, but do not resolve E-6322.
