# A whole-boundary pressure-modulus criterion beyond Dini continuity

E-6322, fifth and final shared pass, 16 October 2026.

This is a conditional sharpening, not a regularity theorem for arbitrary minimizers. The pass-2 Dini-pressure theorem remains useful under its own, different hypothesis, which does not require continuity of Dy.

## 1. Statement

Let y be any full-class minimizer and additionally suppose Dy has a continuous representative on the compact closure of the original domain. Let omega be its uniform modulus,

omega(r)=sup{|Dy(x)-Dy(z)|:x,z in closure Omega, |x-z|<=r}.

For any fixed sufficiently small geometric R>0, suppose

liminf_{r down to 0} omega(r)^2
 [1+integral_r^R omega(t) dt/t]=0.                       (1)

Then det Dy has a strictly positive minimum on the closure, and hence the requested global essential lower bound holds for this minimizer.

In particular the conclusion holds if, for some alpha>1/3,

omega(r)<=C[log(eR/r)]^{-alpha}

at small scales. This includes some non-Dini moduli. No such modulus has been established for all frozen-target minimizers.

## 2. Truncated pressure means need no pressure boundary trace

The valid material stress is

E=pI+Q(Dy),  p=3d(det Dy)^{-2},  div E=0,

where Q is the positive-degree constitutive tensor of degree six. Initially p belongs only to L^1. Boundedness of the continuous gradient gives

|Q(Dy(x))-Q(Dy(z))|<=C omega(|x-z|).

The pass-2 negative-norm/Bogovskii argument, starting from this initial L^1 pressure, gives on balls and on uniformly shrinking boundary caps U_r

(average_{U_r}|p-p_{U_r}|^2)^{1/2}<=C omega(c r).          (2)

The boundary caps are uniformly star-shaped after scaling, as proved in the sealed pass-2 report. Their volume ratios are uniformly bounded. Comparing successive cap means, or successive ball means, and telescoping only down to radius r therefore gives

p_{U_r}<=C_0+C_1 integral_r^{R'} omega(t) dt/t.            (3)

Here R' is a fixed geometric multiple of R, and the constants depend on the domain, coefficients, gradient bound, and the original finite pressure integral. Replacing R' by R only changes C_0. No Dini convergence at zero is needed because the sum is truncated. Neither a trace nor continuity of p or of its derivatives is used.

## 3. A zero would force a conflicting lower mean

The determinant has a continuous nonnegative representative. If J(x_0)=0 at any interior or boundary point, the determinant's Lipschitz dependence on bounded matrices gives

0<=J(x)<=C omega(r) for x in U_r around x_0.

Since J>0 almost everywhere, this implies

p_{U_r}>=c omega(r)^{-2}.                               (4)

If omega vanishes on a whole sufficiently small scale, J would vanish on a set of positive volume, already a contradiction. Otherwise combine (3)-(4): for every sufficiently small r,

omega(r)^2[1+integral_r^R omega(t)dt/t]>=c_*>0.

This contradicts (1). Boundary zeros are excluded by the same cap estimate, not by an assumed derivative or pressure trace. Compactness of the closure then supplies a positive determinant minimum.

## 4. Logarithmic threshold and exact scope

With T=log(eR/r), the product in (1) is bounded, up to constants, by

T^{1-3alpha},          0<alpha<1,
T^{-2}log T,          alpha=1,
T^{-2alpha},         alpha>1.

It tends to zero for alpha>1/3. The endpoint alpha=1/3 is not covered by this calculation. No sharpness claim is made for the actual constitutive minimizer problem.

The mechanism uses both the pressure mean estimate and the algebraic blow-up p=3dJ^{-2} tied to a continuous gradient. It is stronger than applying the abstract Dini pressure theorem with a nonsummable modulus and pretending its divergent integral is finite. It still leaves the central missing premise: a sufficient whole-boundary gradient modulus has not been derived from minimality alone.
