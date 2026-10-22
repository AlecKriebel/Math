# Pass 2: an admissible whole-boundary collar comparison

E-6322, 2026-10-16. This complements the interior finite comparison. The estimate is uniform along the entire smooth boundary for sufficiently thin collars, but remains an integral estimate rather than the asserted essential Jacobian lower bound.

## 1. Geometry and the finite maps

Let delta(x)=dist(x,partial Omega) inside Omega. Since the boundary is compact and smooth, there is a positive tubular radius h0 such that delta is smooth in 0<delta<h0, |grad delta|=1 there, and its Hessian is bounded. Put

M=sup_{0<delta<h0}|D^2 delta|,
K=sup_{0<delta<h0}|Delta delta|.

Choose h>0 with 2h<h0, hM<=1 and hK<=1/4. Write C_h={x in Omega:delta(x)<h}. Define the continuous piecewise-linear function

f_h(s)=s for 0<=s<=h,
f_h(s)=2h-s for h<s<2h,
f_h(s)=0 for s>=2h.

On the collar set eta_h(x)=-f_h(delta(x)) grad delta(x), and set it to zero elsewhere and on the boundary. This is a Lipschitz vector field which vanishes on the entire boundary. It need not be compactly supported in the open domain.

For sufficiently small |t|, phi_t(x)=x+t eta_h(x) is a bi-Lipschitz homeomorphism of Omega fixing its entire boundary pointwise. One direct verification uses tubular coordinates x=z+s n(z): the map preserves z and replaces s by s-t f_h(s), a strictly increasing positive function with fixed endpoints 0 and 2h. It is the identity off the collar. Extending eta_h by zero outside Omega also gives a globally Lipschitz field, so Id+t eta_h is a global bi-Lipschitz map for |t| Lip(eta_h)<1.

The competitor y_t=y composed with phi_t^{-1} therefore has exactly the prescribed trace, belongs to W^{1,6}, and has positive determinant a.e. Uniform bounds on Dphi_t and its inverse make all target energy terms finite. This proves full-class admissibility without any derivative trace of y or topological injectivity of y.

The exact finite energy change is the same material-composition formula as in the interior note. Differentiation at t=0 is dominated by a constant times W(Dy), because Deta_h is bounded. Consequently

integral_Omega E(Dy):Deta_h=0.

The piecewise derivative jumps on the two collar surfaces do not affect this finite-map argument.

## 2. Signs and constants

Use P,B,U_+ from `FINITE_COMPARISON.md`. Then

E=E_++3B I,
E_+=P I-U_+.

Since U_+ is positive semidefinite and has trace 6P,

|E_+| <= (sqrt(3)+6)P <=8P.

Put n=grad delta. On the inner collar C_h,

Deta_h=-n tensor n-delta D^2 delta,
div eta_h=-1-delta Delta delta <=-3/4.

On C_{2h} minus C_h,

Deta_h=n tensor n-(2h-delta)D^2 delta,
div eta_h=1-(2h-delta)Delta delta <=5/4.

Everywhere in C_{2h}, |Deta_h|<=1+hM<=2. Therefore

|E_+:Deta_h|<=16P.

Insert these estimates into the justified identity:

0<=16P(C_{2h})-(9/4)B(C_h)+(15/4)B(C_{2h} minus C_h).

Rearranging gives the quantitative whole-boundary estimate

B(C_h) <= (5/8)B(C_{2h})+(8/3)P(C_{2h}).       (C)

The constants are independent of h once the stated tubular and curvature restrictions hold. They do not depend on any regularity of the minimizer beyond the frozen admissible class.

## 3. Scope and limitation

Inequality (C) is a genuine trace-fixing boundary comparison, including every boundary component. It does not assume a derivative trace for y. Curvature is accounted for by the explicit Hessian terms, rather than silently identifying the energy with a flat-coordinate energy.

However, P is initially only in L^1. Thus (C) gives no positive-rate decay for its right-hand side without an additional estimate. Even an improved rate of decay of the barrier mass in a collar would be an integral assertion; it would not, by itself, eliminate arbitrarily small determinant values on thin sets.

This closes the admissibility issue for this particular boundary-layer variation. It does not close the regularity or determinant-positivity problem in E-6322.
