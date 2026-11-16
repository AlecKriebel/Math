# Independent derivations and adversarial controls — source-first

Only the native manuscript/TeX and my fresh images have been read. Statements labelled inputs below are obligations for later primary checking, not verified citations.

## 1. Exact conditional field construction, including holes

Assume there is a bounded open Omega containing each disk of radius sqrt(lambda_j) about z_j, with null boundary, area pi, and integral h over Omega equal to pi*sum lambda_j*h(z_j) for every real integrable harmonic h on ALL Omega. S=closure(Omega) is then compact with area pi. For any z outside S, distance(z,S)>0; the real and imaginary parts of (w-z)^(-2) are bounded integrable harmonic functions of w on all Omega. Testing both gives integral_Omega (w-z)^(-2) dA(w)=pi*g(z), hence T1_Omega(z)=-g(z), with T=-1/pi times the kernel integral. This uses neither analytic continuation nor connectedness. Each pole is protected by its own disk, so outside S, lambda_j/|z-z_j|^2<=1 and |g|<=n. Thus every bounded integration region is finite, independently of the operator estimate. Repeated poles can be combined, with their positive weights added, before invoking the input.

This is conditional on the full stated quadrature input. Merely knowing analytic quadrature for tests extending through the holes, or the exterior field on the unbounded component, would be insufficient.

## 2. Independent angular and radial kernel calculation

Rotate w to rho>R. For 0<=r<=R, s=r/rho<1. Multiply the two uniformly absolutely convergent geometric series for (1-s*exp(i theta))^-1 and its conjugate. Angular integration retains only equal exponents, giving integral_0^(2pi) |rho-r exp(i theta)|^-2 dtheta=2*pi/(rho^2-r^2). Fubini is justified by uniform convergence or by positivity. Integrating r dr from 0 to R gives K(R,rho)=pi*log(rho^2/(rho^2-R^2)). For rho>=sqrt(2)*R, the argument of log is <=2, so K<=pi*log(2). The ratio inequality is exact: rho^2/(rho^2-R^2)<=2 iff rho^2>=2R^2. There is no origin assumption on any pole.

## 3. Reconstructed uniform estimate

Assume the indicator estimate integral_(D_L\E) |T1_E|<=a*log(pi*L^2/a) for any measurable E subset D_L, a=|E|; define the a=0 term by continuity. Fix the single Omega above. For an arbitrary R>1, put L=sqrt(2)R, E=Omega intersect D_L and F=Omega\D_L, so |F|=pi-a. On D_R\S the ordinary integrals agree with the L2 transform representatives almost everywhere, and T1_Omega=T1_E+T1_F. Its absolute value is bounded by the sum; D_R\S is contained in D_L\E. The near term is therefore <=a*log(2*pi*R^2/a).

For the far term, distance(D_R,F)>=L-R>0. Its absolute kernel is nonnegative and integrable by the preceding formula, so Tonelli gives integral_(D_R\S)|T1_F| <=(1/pi)*integral_F K(R,|w|)dA(w) <=(pi-a)log(2). Consequently the total is <=2a log(R)+pi log(2)+a log(pi/a). Let t=a/pi in [0,1]. Calculus gives H(t)=t log(1/t), H(0)=H(1)=0, H'(t)=-log(t)-1, H''(t)=-1/t, hence max H=1/e at t=1/e. Since log(R)>0, 2a log(R)<=2pi log(R). This proves exactly the target constant, conditional only on the two inputs. Although E,F depend on R, Omega and S were already fixed. Endpoints a=0 and a=pi cause no division-by-zero issue after continuity. R>1 and positivity/finite total mass are used explicitly.

## 4. Different sharpness mechanism: layer-cake, with no infinity subtraction

Take g(z)=z^-2 and any measurable S of area pi, with no geometric restrictions on S. For h(z)=|z|^-2 on D_R, nonnegative Tonelli gives integral_(D_R\S)h = integral_0^infty |{z in D_R\S:h(z)>t}|dt. Removing S can erase at most pi area, so this is >= integral_0^infty max(pi*min(R^2,1/t)-pi,0)dt. For R>1 the latter integral is

pi*(R^2-1)/R^2 + pi*integral_(1/R^2)^1 (1/t-1)dt = 2*pi*log(R).

All terms in the layer-cake argument are nonnegative, so it remains valid if the original integral is infinite. The centered unit disk attains equality. If the proposed leading coefficient c were <2pi with fixed finite C, (2pi-c)log(R)>C for large R contradicts the target bound. This proves leading sharpness without using either external input. It does not prove optimality of the displayed additive constant.

## 5. Calibration and deliberate wrong alternatives

For a disk D(c,r), the normalized Cauchy integral C(z)=(1/pi) integral_D (z-w)^-1 dA(w) is conjugate(z-c) inside, and r^2/(z-c) outside, with the center translation handled in the interior expression. Differentiating in z yields T1_D=0 inside and -r^2/(z-c)^2 outside. The exterior formula also follows directly from the mean-value identity applied to the holomorphic kernel. A centered disk of radius r<L therefore gives integral_(D_L\D_r)|T1_D|=2*pi*r^2 log(L/r)=a log(pi*L^2/a): the indicator normalization is calibrated exactly.

For two disjoint disks centered at -2 and 2, each squared radius 1/2, their total area is pi. The independent disk mean-value identity gives T of their union equal to -g outside both disks, g=(1/2)/(z+2)^2+(1/2)/(z-2)^2. Exact checks: g(0)=1/4, g(i)=3/25, g(3)=13/25. Simply taking a union would fail for overlapping disks: two coincident mass-1/2 disks have union area pi/2, not pi. This attacks a tempting substitute for the construction; the paper combines coincident poles and invokes the proper quadrature input.

For the annulus A={1<|w|<sqrt(2)}, area pi, subtracting the two disk fields gives T1_A(z)=-1/z^2 for |z|>sqrt(2), but T1_A(z)=0 for |z|<1. At z=1/2 the continuation of the exterior formula would predict -4 instead of zero. This is an exact falsifier of the WEAKER premise that equality on the unbounded component supplies all holes. It is not a counterexample to the manuscript, whose whole-domain harmonic testing is stronger and whose quadrature nodes must lie in the domain.

## 6. Actual result and remaining boundary

The elementary deduction, field implication conditional on the stated strong quadrature input, and independent leading-sharpness proof are complete written arguments. Exact arithmetic and high-precision scalar diagnostics are recorded separately. They cannot certify the two external theorems or a historical firstness claim. No native code/results/archived review has been read or executed; no current peer/root findings or foreign bodies have been read. Final scientific disposition remains withheld pending primary-source gates and comparison. Follow-up is null.
