# Coupled constitutive coercivity, stress spectrum, and singular ellipticity

E-6322, shared pass 3, 16 October 2026.

This report uses the actual density, rather than a freely chosen pressure tensor. All coefficient statements hold for arbitrary fixed a,b,c,d>0. The conclusions are algebraic coercivity and restricted stationary consequences; the full benchmark remains unresolved.

## 1. A global relative-minor formulation of the minimizer problem

Fix any A in GL^+(3), put K_A=cof A and j=det A, and define

D_p(X,Y)=|X|^p-|Y|^p-p|Y|^{p-2}Y:(X-Y).

For F with J=det F>0 and K=cof F, define

R_A(F)=a D_6(F,A)+b D_3(K,K_A)+c(J-j)^2
       +d (J-j)^2(2J+j)/(j^3 J^2).                     (1)

This is precisely the convex Bregman remainder in the independent minor variables. The last term uses the identity

J^{-2}-j^{-2}+2j^{-3}(J-j)
= (J-j)^2(2J+j)/(j^3 J^2)
>= (J^{-1}-j^{-1})^2.                                  (2)

In particular R_A is nonnegative. There are positive universal constants k_6,k_3 such that

R_A(F) >= k_6 a [|A|^4|F-A|^2+|F-A|^6]
          +k_3 b [|K_A||K-K_A|^2+|K-K_A|^3]
          +c|J-j|^2+d|J^{-1}-j^{-1}|^2.                (3)

For completeness, uniform convexity here follows directly from the Hessian integral

D_p(Y+H,Y) >= p|H|^2 integral_0^1 (1-t)|Y+tH|^{p-2} dt.

Projection on H and restriction to [0,1/2] give a positive constant times |H|^p. If |H|<=|Y|/2, the whole segment has norm at least |Y|/2; otherwise |Y|^{p-2}|H|^2 is controlled by |H|^p. Combining the two estimates proves (3) for p=3,6. No global Hessian convexity of W as a function of F is being asserted.

### 1.1 Why this is an exact reformulation even for nonaffine data

The difference W(F)-R_A(F) is W(A) plus the constant-coefficient linear minor expression

6a|A|^4 A:(F-A)
+3b|K_A|K_A:(cof F-K_A)
+(2cj-2dj^{-3})(det F-j).                               (4)

The integrals of every first-, second-, and third-order minor are the same for two W^{1,6} maps having the same complete trace. One can justify this by approximating their zero-trace difference strongly in W^{1,6} by compactly supported smooth maps and using the polynomial null-Lagrangian identity; the minors converge respectively in L^6,L^3,L^2.

Consequently, for every two full-class competitors y,z with the prescribed g,

I(y)-I(z)=integral R_A(Dy)-integral R_A(Dz).              (5)

An actual minimizer minimizes this nonnegative relative-minor energy for every fixed A. In particular its relative-minor energy is bounded above by that of the permitted smooth extension G. The same cancellation holds for local replacements with identical trace on a subdomain.

For affine trace Ax+q, (5) becomes

I(y)-|Omega|W(A)=integral R_A(Dy),                       (6)

which proves global strong quasiconvex coercivity and affine-data uniqueness. For arbitrary trace, (5) supplies a faithful positive excess functional, but not an upper comparison with an affine map whose trace does not match. This distinction is the precise remaining issue in an excess-decay argument.

## 2. Rank-one ellipticity is positive but not uniformly nondegenerate

Write S=|F|^2, K=cof F, J=det F. Let R=u tensor v be a rank-one matrix and L=D(cof)(F)[R], j_R=cof F:R. Along the rank-one line, both cof(F+tR) and det(F+tR) are affine in t. Thus

D^2W(F)[R,R]
=6a S^2|R|^2+24a S(F:R)^2
 +3b|K||L|^2+3b|K|^{-1}(K:L)^2
 +(2c+6dJ^{-4})j_R^2.                                 (7)

All displayed terms are nonnegative; in particular the Legendre-Hadamard lower bound is 6a|F|^4|R|^2. Formula (7) does not imply convexity of W along arbitrary matrix directions: second derivatives of the minors then also occur.

### 2.1 Exact conformal-compression calculation

At F=tI with t>0, in the unit rank-one shear direction E12,

D^2W(tI)[E12,E12]=(54a+3sqrt(3)b)t^4.                   (8)

The determinant is exactly constant along this shear, so both determinant terms contribute zero. The lower rank-one stiffness therefore tends to zero as t tends to zero, despite the energy barrier tending to infinity.

In the unit rank-one direction E33,

D^2W(tI)[E33,E33]
=(126a+10sqrt(3)b+2c)t^4+6d t^{-8}.                    (9)

More generally, for a unit rank-one matrix R=u tensor v, with |u||v|=1 and z=u dot v, direct substitution gives

D^2W(tI)[R,R]=(54a+3sqrt(3)b)t^4
 +[(72a+7sqrt(3)b+2c)t^4+6d t^{-8}]z^2.

Since 0<=z^2<=1, equations (8) and (9) are the exact minimum and maximum rank-one stiffnesses. Their ratio is exactly

(126a+10sqrt(3)b+2c)/(54a+3sqrt(3)b)
 +[6d/(54a+3sqrt(3)b)]t^{-12}.                          (10)

This is a genuine loss of lower as well as upper uniform ellipticity, not merely the upper-coefficient blow-up at the bounded rank-two sequence diag(1,1,epsilon) studied in pass 2. The barrier penalizes determinant-changing modes, while isochoric shears at strong isotropic compression remain cheap to second order.

These are constitutive matrix calculations, not singular-minimizer constructions. In fact Section 4 excludes a variable conformal factor for an inner-stationary deformation, so this particular matrix degeneration cannot by itself be promoted to a conformal minimizing core.

### 2.2 What this says about an epsilon-regularity argument

A linearization centered at A in GL^+(3) has positive rank-one ellipticity and a finite smoothness neighborhood, so the relative-minor excess is a natural starting point. Neither the size of that admissible neighborhood nor the ellipticity ratio stays uniform as A approaches the singular set. At A=diag(1,1,epsilon), even the direction -E33 exits GL^+(3) after increment epsilon. At A=tI, equations (8)-(10) show simultaneous shear degeneracy and volumetric stiffness.

No standard excess-decay theorem is imported here. To turn (1)-(7) into positivity, a proof would have to supply an admissible replacement and quantitative estimates that survive these degenerations, or prove independently that the centers of all relevant blow-ups stay away from them. Strong quasiconvex lower coercivity alone supplies neither of those steps.

## 3. The actual deviatoric stress controls strain anisotropy

Let H(F)=a|F|^6+b|cof F|^3+cJ^2 and U=F^T DH(F). In the pass-1 valid inner stress,

E=(H+3dJ^{-2})I-U,   div E=0,   tr U=6H.               (11)

Let C=F^TF have eigenvalues x_1,x_2,x_3>0, set S=x_1+x_2+x_3 and T=x_1x_2+x_1x_3+x_2x_3. Then U and C have the same eigenvectors, and the eigenvalues of U are

u_i=6a S^2 x_i+3b sqrt(T) x_i(S-x_i)+2cJ^2.            (12)

For distinct i,j,k,

u_i-u_j=(x_i-x_j)[6a S^2+3b sqrt(T)x_k].                (13)

It follows, using sum_{i<j}(u_i-u_j)^2=3|dev U|^2, that

|dev U| >= 6a S^2 |dev C|.                             (14)

Thus the actual tensor has a strict principal-stretch ordering and a quantitative deviatoric coercivity. A generic arbitrary-Q pressure example does not encode this structure.

A useful elementary consequence is the dichotomy

J^2 < S^3/216  =>  |dev U| > sqrt(3/2) a S^3.           (15)

Indeed if each x_i were at least S/6, their product would be at least S^3/216. If x_min<S/6, then |dev C|^2 >= (3/2)(x_min-S/3)^2>S^2/24, proving (15). The exact lane gives a sharper tracefree-determinant formula in its pass-3 certification. Neither inequality bounds dev U for the minimizer; it only identifies anisotropic collapse as a quantitatively nonisotropic stress regime.

## 4. One actual stationary subclass is completely excluded

Suppose, additionally, a full-class inner-stationary deformation satisfies

F^TF=lambda(x)^2 I almost everywhere.

No continuity of lambda, F, or J is assumed. Since J>0 almost everywhere, lambda>0. Put A0=27a+3sqrt(3)b+c. Equations (11)-(12) reduce exactly to

H=A0 lambda^6,  U=2H I,
E=[3d lambda^{-6}-A0 lambda^6]I.                        (16)

The scalar in brackets belongs to L^1. Its distributional gradient is zero, so on the connected original domain it equals a finite constant. The function s -> 3d s^{-6}-A0 s^6 is strictly decreasing from positive infinity to negative infinity on (0,infinity). Hence lambda is one positive constant almost everywhere, and J=lambda^3 has a global essential lower bound.

This uses the actual constitutive stationarity and no Liouville regularity theorem. It rules out the pure conformal-collapse mechanism. It does not assume or conclude that a general minimizer is conformal, and is not a resolution for arbitrary full smooth boundary data.

## 5. Outcome

The relative-minor energy and one-component theorem give exact coercivity in genuinely allowed comparison classes. The spectral identity identifies actual constitutive information absent from abstract pressure models. The conformal calculation both rules out one stationary collapse pattern and exhibits the precise nonuniform ellipticity faced by general blow-up arguments.

No new unconditional L^{6+delta} estimate, constitutive modulus, epsilon-regularity theorem across J=0, or entire-domain Jacobian lower bound has been established. The unresolved step remains an admissible replacement or another minimizer-specific estimate that turns this coupled structure into quantitative control on arbitrary low-Jacobian regions.
