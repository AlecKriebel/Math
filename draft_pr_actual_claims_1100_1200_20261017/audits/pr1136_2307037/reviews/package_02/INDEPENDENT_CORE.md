# Independent derivation and decision core (recorded before prior audit conclusions/code)

UTC checkpoint: 2026-10-17T22:29:59.838114+00:00 (recorded log timestamp). Review completion estimate: 22%.

Read at this stage: operative main.tex, original PROOF.md and source hypotheses/identity records; freshly downloaded EH 1995 entire five-page text, LP author-manuscript pp.6,12–18,54–55,58–59, HL v2 pp.172–173. No package_01 conclusions/code or earlier mathematical-review conclusions/code have been read. Source interfaces are being tested rather than presumed correct.

## Exact target

HL requires finite rational functions given by squared-pole sums with arbitrary positive real weights of total coefficient one, arbitrary complex pole locations, and ONE set S(g) with area pi for EVERY R>1. It asks for an absolute additive constant; compactness and the displayed numerical constant are stronger conclusions. Neither the adjacent solved Problem 7.36 nor the historical update determines 7.37's current or historical priority.

## Derivative chain surviving the EH general-distortion correction

Let E be a measurable subset of the unit disk with a=|E| in (0,pi), and mu bounded by one supported in D\E. For the normalized principal Beltrami family f_t with coefficient t mu, conformality on E gives A(t)=|f_t(E)|=integral_E |partial f_t|^2. L2 Neumann-resolvent differentiation at zero gives partial f_t=1+t Tmu+O_L2(t^2), so A'(0)=2 Re integral_E Tmu. Only conformal-on-E Theorem 1(i) is needed:

A(t) <= a exp((2t/(1+t)) log(pi/a)), t>=0, A(0)=a.

The right derivative at zero is 2a log(pi/a). Thus Re integral_E Tmu <= a log(pi/a). The Beurling kernel is symmetric under interchange of its two spatial variables; its L2 complex bilinear pairing is symmetric (no conjugation in this pairing). Hence integral_E Tmu = integral_(D\E) mu T1_E. Choose mu=conj(T1_E)/|T1_E| where nonzero (zero elsewhere) and use standard bounded/simple approximants if needed. This gives the needed indicator estimate. The t-derivative is taken at zero, not at t=1; the factor 2 cancels. The combined general-distortion statement is absent from this chain. For a=0 or pi the estimate follows directly, or by L2 continuity. Compact inside approximation plus L2 continuity/Fatou extends a compact-set form to measurable E while the masks converge a.e. after a subsequence.

## LP interface

LP Proposition 6.6 explicitly quantifies arbitrary finite positive masses and integrable superharmonic tests on the ENTIRE smash sum. Both signs of bounded harmonic tests are admissible. Definition (4) includes both inputs. Boundedness follows from Lemma 2.15; binary indicators are integer-valued and satisfy the density gap (24) with any lambda in (0,1). Proposition 2.12 makes the new open-set boundary null and Corollary 2.13 preserves summed area. Finite iteration and associativity therefore give a bounded open Omega containing disks of areas pi lambda_j, mass pi, and whole-domain harmonic quadrature. Overlap, remote centers, repeated centers (combine first) and arbitrarily small positive weights do not violate any hypothesis.

For z outside closure(Omega), distance to Omega is positive. The real/imaginary parts of (w-z)^(-2) are bounded harmonic on all Omega, even when z is in a bounded complementary component. Quadrature gives integral_Omega(w-z)^(-2)dA=pi g(z). Hence T1_Omega=-g on ALL complement components. There is no boundary differentiation, analytic continuation across holes, or principal-value target integral. Since each pole has a disk of radius sqrt(lambda_j) in Omega, on the complement each term has absolute value <=1, so |g|<=n. Closure has area pi because boundary is null.

## Localization and endpoints

For L=cR, c>1, set a=|Omega cap D_L| and t=a/pi. Scaling contributes the correct total area factor L^2. The integrated far kernel is pi log(rho^2/(rho^2-R^2)); its maximum at rho=cR gives log(c^2/(c^2-1)) per unit far mass after division by pi. At c=sqrt(2), the sum divided by pi is

2t log R + log 2 - t log t.

The difference from 2logR+log2+1/e is 2(1-t)logR + 1/e+t log t, nonnegative for R>=1 and t in [0,1]. At t=0 use 0log0=0, and at t=1 the logarithmic coefficient is exactly 2. R down to1 remains covered, without any pole-location uniform bound beyond total mass. Positivity is essential only to the quadrature construction; the theorem does not imply a signed-coefficient version.

## Sharpness and a separate contour falsification plan

For g=z^-2, radial decreasing rearrangement puts an area-pi exclusion optimally in D1: replace any excluded exterior area by unexcluded interior area and the retained integral cannot increase. The paper's mass-comparison argument implements this without subtracting infinities. Therefore integral_(D_R\S)|z|^-2 >=2pi logR, even for arbitrary measurable S of that area and infinite left side. This proves the coefficient lower bound.

Independent exact controls will use the complex Green formula for disks, not the previous formal EH coefficient-series or removal-budget mechanisms. On a circle centered a with radius squared q, bar(w)=bar(a)+q/(w-a). The boundary integrand bar(w)/(w-z)^2 has residue q/(a-z)^2 at a. If z is outside the disk, the area kernel divided by pi is q/(a-z)^2; if z is inside, the pole at z contributes the opposite residue and the total is zero. This tests the pi mass normalization, sign and cancellation directly in rational arithmetic. Annulus subtraction produces the same field as a point at its center in the unbounded component, but ZERO field inside the inner disk, where the putative point-field is nonzero. This will be a guard against replacing whole-domain quadrature by exterior-only continuation. An exact Fourier sampling identity will independently check the integrated angular absolute kernel and reject a wrong sign in its denominator. These finite controls check mechanisms and wrong alternatives, not the universal theorem.

## Provisional decision

No mathematical defect found in the proposed universal deduction at these interfaces. This is NOT yet package acceptance: visual QA, source visual confirmation (EH scans lose equations in extraction), code, reproducibility, historical/current records, archive membership and priority access limits remain to inspect. No historical firstness conclusion is supported by this derivation.
