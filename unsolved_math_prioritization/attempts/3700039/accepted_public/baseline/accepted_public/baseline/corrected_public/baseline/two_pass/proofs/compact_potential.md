# Compact logarithmic potentials with polynomial harmonic parts

This is a partial theorem, not a resolution of the unrestricted median conjecture.

Let each mu_j be a finite positive measure supported in one fixed disk |a|<=R, with integral |log|a|| dmu_j(a)<infinity. Let P_j be a polynomial with Re P_j(0)=0. Define

u_j(z) = Re P_j(z) + integral [log|z-a|-log|a|] dmu_j(a).

These are whole-plane subharmonic functions with u_j(0)=0. Logarithmic poles are allowed away from the origin. Let v_2 be their pointwise median and B(r) their common upper envelope on the circle.

Then sup_{r>0, B(r)>0} I(r,v_2)/B(r)>=0, unless all three functions are identically zero, which is the explicit 0/0 degeneracy.

## Proof

Put M_j=mu_j(C) and C_j=integral log|a| dmu_j(a). For r>2R,

u_j(r exp(i theta)) = Re P_j(r exp(i theta)) + M_j log r - C_j + O(1/r)

uniformly in theta. This follows from log|z-a|=log r+log|1-a/z| and |log|1-a/z||<=2|a|/r.

If every Re P_j is zero, then each function with M_j>0 is eventually positive uniformly in theta. If M_j=0, positivity of the measure implies mu_j=0 and u_j=0. Thus all three are nonnegative on every sufficiently large circle, giving I(r,v_2)>=0 there; B(r)>0 unless all three vanish identically.

Otherwise let d>=1 be the largest degree of a nonzero real harmonic polynomial Re P_j, and write the degree-d terms as r^d h_j(theta), allowing h_j=0. Each h_j satisfies

h_j(theta+pi/d)=-h_j(theta).

Let H=median(h_1,h_2,h_3). Then H(theta+pi/d)=-H(theta), so integral H=0. Coordinatewise medians are 1-Lipschitz for the maximum norm. Consequently the uniform asymptotics give

I(r,v_2)=O(r^{d-1}+log r),
B(r)=r^d b+O(r^{d-1}+log r),

where b=max_{j,theta}h_j(theta)>0. Hence I(r,v_2)/B(r) tends to 0 as r tends to infinity. Its supremum is therefore at least 0, even when its value is negative at every finite radius.

## Limitations

This excludes finite atomic logarithmic constructions and arbitrary compactly supported finite logarithmic mass with a polynomial harmonic part. It does not cover a nonpolynomial entire harmonic part combined with singular potentials, noncompact Riesz support, or infinite Riesz mass. No general classification of possible counterexamples follows.
