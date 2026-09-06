# Independent nonlinear and PDE referee report

Audited source: preserved `source_snapshot/`, commit `6f68ad3e795c`; report completed 2026-09-06 04:41 UTC. Prior referee reports were not read before the independent mathematical audit. The relevant discovery goal here is verification of the existing claims, not discovery of a new theorem. Audit progress: 100% of this assigned scope.

## Verdict and exact scope

I found **no false theorem or substantive unresolved nonlinear/PDE gap** in the unit-equilibrium or certified equilibrium-scaled stable-pattern constructions. Their all-dimensional justification is mathematical, not an extrapolation from finite floating spectra. The physical mass gauge, normal-form normalization, cubic sign, exceptional dimension, corrected lower endpoint, first-mode algebraic simplicity, and local H1 stability survive this review.

I read main Sections 6--13, supplement S5--S11, the load-bearing generic cubic, mode, gauge, and near-threshold verifiers, and relevant earlier definitions of the network and conservation law. The precise positive result is for each **fixed** integer m>=3, on a fixed one-dimensional Neumann interval, on the affine class of fixed integrated c-mass, with positive diagonal diffusion, sufficiently small bifurcation parameter, and (for the scaled family) L in its displayed closed interval. No estimate here establishes global attraction, a dimension-uniform neighborhood, stability against changing the integrated mass, or intrinsic wavelength selection on arbitrarily large domains.

Three minor improvements remain advisable. None changes the core theorem.

| Item | Location in preserved source | Assessment and minimal action |
|---|---|---|
| PDE-M1 | main.tex:650--651 | The full well-mixed Jacobian has a conservation zero. The current phrase is understandable from its immediate c-perp qualification, but change it to “the well-mixed Jacobian restricted to c-perp, equivalently the fixed-mass homogeneous k=0 mode, is Hurwitz.” |
| PDE-M2 | supplement.tex:947--954; independent_verifier/frontier_verify_near_threshold.py:64 onward | The subcritical control is true, but the supplied near-threshold verifier starts from a hardcoded rational cubic and checks no first/higher-mode spectral hypotheses. Add the short onset verification below and anchor that rational cubic to the actual reaction/Hessian calculation. Independent exact evidence now supplied in `near_threshold_independent.py`. This is a checkability/exposition omission concerning a secondary example. |
| PDE-M3 | main.tex:91--94, 150--159; relation-to-prior-work discussion | Clarify the finite-interval convention for “Turing.” The construction has an unstable band extending to arbitrarily small positive wavenumber; it does not prove finite-wavelength selection independent of domain size. A sufficient sentence is: “Here Turing bifurcation means a stationary diffusion-driven bifurcation on a fixed Neumann interval; no domain-independent finite-wavelength selection is asserted.” This avoids confusion with the narrower terminology in Conradi--Mincheva--Uecker, without requiring a title change. |

## Reconstructed spectrum and equality cases

The derivative and Hessian were regenerated from the reaction source and product stoichiometries, independently of manuscript helpers. For every reaction of unit flux, the contributions are `(product-source)*source^T` to A and `(product-source)*(source*source^T-diag(source))` to the Hessian. This includes the inflow, whose derivative is zero, and the empty chain at m=3. It reproduces the displayed B tensor, c^T A=0, c^T B=0, and rho=(2,-2,...,-2,0,1) in ker A.

The generic sparse determinant has a direct four-boundary derivation, valid for arbitrary chain length. Eliminate rows 3,...,m-1 and write Rchain as the product of their diagonal factors. The remaining boundary matrix is

```
[ g1    1/Rchain    1   -2 ]
[  1       g2     -2    0 ]
[ -1   -2/Rchain  gm   -2 ]
[ -2        0     -2   gZ ]
```

Multiplication of its determinant by Rchain yields `Q*F-G`, where Q=g2*Rchain and F,G are precisely the printed factors. The identity was checked in the rational function field with arbitrary boundary symbols, so this link is not merely a low-dimensional determinant fit. In the closed right half-plane the eliminated factors are nonzero; elsewhere the identity extends polynomially.

For the unit homogeneous problem, P=(1+lambda)F0. The m=3 quotient is `(lambda+7)(lambda^2+5lambda+2)`. For m>=4 the 35-term certificate excludes every nonzero closed-right-half-plane root, and q_m(0)=16m-34>0 makes the zero simple. Since c^T rho=17-8m is nonzero, the complementary spectrum is exactly the spectrum of A restricted to c-perp.

For unit spatial damping t>=1, each chain modulus is at least its real value at lambda=0,t=1. Keeping the y^2 contribution of any one factor gives `|Q|^2 >= (91/90)^2+y^2`: the product of the other factors is at least 1. Thus the 77-term certificate is attached to the actual determinant. For the scaled case, factoring `K_(i-1)/K_i` gives the printed bound with `|1+L lambda|^(2nu)` and then the 84-term certificate. The homogeneous scaled estimate uses a different factor F0 and the 22-term certificate. Confusing these two factors would invalidate the argument; the current source keeps them separate.

I independently expanded all four modulus polynomials without loading JSON tables. Counts are 35,77,84,22, all asserted coefficients have the required signs, and each polynomial contains positive pure powers of every nonnegative variable. Therefore its claimed equality set is exactly the origin, including the 22-term lower boundary U=0. A modulus inequality alone does not prove a simple critical zero. The current source separately supplies Pi'_m(0)=-(163/45)ell^T r>0; its logarithmic derivative uses sum 1/(1+1/K_i)=nu-hfrak. The harmonic bound proves strict positivity. The scaled kernel remains one-dimensional, and ell^T H^-1 r<0 rules out a length-two Jordan chain, hence any nonsimple zero.

The scaled homogeneous lower bound nu L^2>=5/4 is sufficient, not intrinsic. For m=3 the direct cubic Routh calculation applies at both endpoints. Finite spectral probes independently checked unit, lower, and upper profiles at m=3,4,20,148,149,150,256 and modes k=0,1,2,3. All intended tests passed. At m=149 the certified lower endpoint has homogeneous complementary abscissa approximately -0.00396045; the deliberately out-of-range older value L=1/21 has +0.00013654967. This adversarial check confirms why the broader cubic-sign interval cannot silently replace the current spectral interval. Large-m gaps shrink; no uniform gap is inferred.

## Cubic coefficient, gauge, and all-dimensional proof bridge

Write the center graph at onset as `u=A*r*cos(xi)+A^2*(w0+w2*cos(2xi))+...`, with A the adjoint projection and ell^T r nonzero. The quadratic Taylor term is B(u,u)/2. Consequently both harmonic forcing equations have `-B(r,r)/4`. Projection of B(r,w2) cos(xi)cos(2xi) gives its factor 1/2. The order-three center coefficient is therefore exactly the printed formula, without a missing factorial or Fourier normalization. Since the order-two reduced vector field vanishes, the center-manifold invariance term cannot alter these stable corrections at this order.

The zero-mode solve is uniquely fixed by c^T w0=0. The second harmonic is invertible by the all-mode spectrum proof, independently of its explicit boundary denominator. The stated four-factor recurrence solves `w_(i-1)-(1+4/K_i)w_i=sigma`. Its contraction against ell_i reduces as follows: the interior B component is `4*w_i/K_i+sigma-w_1/(63nu)`, so only the sums of `w_i/(K_i K_(i-1))` and `1/K_(i-1)` occur. The four-factor expression leaves a quadratic product after division, hence an elementary finite polynomial sum plus hfrak. The generic verifier checks precisely this identity in Q(m,hfrak), including the vanishing interior sum at m=3; it is not merely finite regression. I independently checked its mechanism and ran it successfully. Its reduction to R_m+C_m*hfrak, together with shifted-positive denominator/numerator certificates and C_m<0, proves c_m<0 for all m.

Independent reaction-derived exact matrix solves checked the resulting contraction for m=3,4,7,10, obtaining respective c values approximately -0.00244361956, -0.00135494852, -0.000573472601, -0.000363321983. Those values are diagnostics, not the all-dimensional proof. At m=3,4 an additional symbolic-L calculation reconstructs the physical mass gauge and adjoint denominator.

For the scaled PDE, normalized dynamics has row factor H, left vector H^-1 ell, and mass covector H^-1 c. The second harmonic is unchanged, but the constant correction must shift by tau*rho. This shift is essential. A further independent generic reconstruction used

```
hs = sum_(i=2)^(m-1) 1/K_i = hfrak + 1/(8190nu),
sum j/K_(j+2) = (91nu-1)*hs-nu.
```

Substitution in `(H^-1 c)^T w0` reproduces exactly the printed tau rational function for symbolic nu,L,hfrak. Thus the generic gauge is independently connected to the physical conservation condition. The gauge derivative signs, endpoint comparison tau<1/20, S in (-1/10,0), and Nref>1/100 correctly imply N(L)>1/200 even when tau is negative. The denominator is `-485873/924210-(11180/1467)Lnu<0`. Both crossing and cubic signs follow with the correct physical-to-normalized transformation.

## Functional analysis and local stability

Main.tex:760--823 and supplement.tex:956--1024 now supply a checkable Fredholm proof. On the homogeneous cosine coefficient the fixed integrated-mass condition removes exactly the conservation direction. At k=1 the right kernel is r and the range is ell-perp. Higher modes are invertible. The inverse bound `O(k^-2)` maps compatible L2 data into H2 with Neumann conditions, so the range is closed and the Fredholm index is zero; its cokernel pairing with the parameter derivative is nonzero. The stationary map is smooth H2_N to L2. These are the hypotheses of the original Crandall--Rabinowitz simple-eigenvalue theorem, not an appeal based only on a numerical zero.

The positive diagonal Neumann diffusion operator preserves integrated mass (the boundary derivative terms vanish), has compact resolvent, and, after an innocuous positive shift, fractional domain of order 1/2 equal to fixed-mass H1. The quadratic reaction map is smooth H1 to L2 on a one-dimensional interval. A parameter-dependent diffusion coefficient causes no obstruction: one may rescale time by 1-mu near onset to put the parameter dependence into the bounded reaction perturbation. The finite reflection group permits an equivariant center manifold. Reflection takes the critical mode to its negative, so the reduced field is odd and the claimed fifth-order/parameter remainder follows from finite smoothness of arbitrarily high order. No assertion of a globally analytic center manifold is required.

On the patterned branch, the reaction derivative is bounded multiplication and the diffusion remains strictly positive. The real-part energy bound and sectorial resolvent estimates control all sufficiently high frequencies uniformly in a local parameter neighborhood, while the finitely many bounded spectral clusters continue. Spatial modes need not remain uncoupled on the nonconstant branch; continuation of the finite spectral projection, rather than independent continuation of Fourier blocks, supplies the needed argument. The center eigenvalue is -2 eta mu+O(mu^2), and the remaining spectrum stays strictly left. The analytic-semigroup stability principle gives exponential convergence in H1 on the same fixed-mass affine class. Positivity follows from H2-to-C0 convergence to the strictly positive equilibrium. There is no continuous translation-neutral mode on this Neumann interval.

The robustness proposition fixes m and L and permits local variation within the positive-equilibrium realization manifold, diffusion ratios and interval length. Transport to a fixed reference interval and retune one scalar diffusion multiplier. The simple real eigenvalue, nonzero multiplier derivative, cubic sign and high-frequency bounds persist. This is a legitimate codimension-one implicit-function statement. It does not imply every nearby unretuned parameter value is already critical.

For external reference verification, I matched the stationary hypotheses to the original [Crandall--Rabinowitz paper](https://doi.org/10.1016/0022-1236(71)90015-2), Theorem 1.7, using its reproduced primary text. [Henry's publisher record](https://link.springer.com/book/10.1007/BFb0089647) confirms the cited equilibrium and invariant-manifold chapters. Full Henry/Kato volumes were not available through the publisher in this run; the operator, phase-space, smoothness, and spectral-gap hypotheses were checked directly above rather than represented as a fresh page-by-page audit of those books.

## Near-threshold secondary control: independent completion

The independently reconstructed m=3 profile is

```
d1=epsilon*(3epsilon+8)/6,
d2=epsilon*(4-9epsilon)/(9epsilon^2+32epsilon+18),
dm=epsilon,
dZ=16epsilon/(9-13epsilon).
```

All entries are positive on 0<epsilon<=1/1000. Direct reaction-derived nullvectors, Hessian, mass-gauged w0 and w2 reproduce both the hardcoded exact rational cubic and its constant and linear expansion coefficients. In particular the number 6/1379 is not a fitted limit.

Let `p(lambda,t)=lambda^4+a1(t)lambda^3+a2(t)lambda^2+a3(t)lambda+a4(t)` be the exact characteristic polynomial for damping tD(epsilon), and put H2=a1*a2-a3 and H3=a3*H2-a1^2*a4. Substitute `t=1+v`, `epsilon=1/[1000(1+z)]` with v,z>=0. After clearing denominators, a1,a2,a3,a4/(t-1),H2,H3 all have strictly positive numerator and denominator coefficient lists. Their numerator term counts are 11,18,22,17,42,105. At t=1 this proves a simple zero and a Hurwitz cubic complement; for t>1 it proves full quartic Hurwitz stability. The exact transverse crossing follows from the simple zero and the positive derivative of a4 at t=1. Together with c3>0, this is a genuine primary subcritical control on the fixed interval throughout the stated epsilon range.

Suggested minimal addition to S9: “For this m=3 path all four diffusivities are positive on the stated interval. Writing the characteristic polynomial at damping tD as lambda^4+a1 lambda^3+a2 lambda^2+a3 lambda+a4, exact coefficient positivity after t=1+v and epsilon=1/[1000(1+z)] proves a1,a2,a3,a4/(t-1),a1a2-a3, and a3(a1a2-a3)-a1^2a4 positive for v,z>=0. Thus t=1 is a simple transverse stationary crossing with stable complement, and every t>1 is stable. The accompanying reaction-derived calculation gives the cubic below.” The verification code should actually perform that reconstruction, as the supplied audit code does.

## Reproducibility, evidence boundaries, remaining gaps

- `independent_checks.py`: no project imports; reaction-derived finite exact checks, generic Schur identity, independently generated four polynomial certificates, 88 floating spectral probes. All pass. Results in `independent_results.json`.
- `generic_gauge_independent.py`: independent all-dimensional telescoping of the physical mass gauge. Pass.
- `near_threshold_independent.py`: reaction-derived cubic and exact entire-interval, all-t>=1 Routh certification. Pass. Output in `near_threshold_results.txt`.
- Existing `verify_generic_cubic_recurrence.py` and `verify_symbolic_certificates.py`: both pass; the latter's full aggregate output ends `ALL_SYMBOLIC_CERTIFICATES_PASS`.
- Runtime used: existing Math/.venv Python, SymPy 1.14.0, NumPy 2.0.2. Symbolic identities use exact rational arithmetic. Floating eigenvalues are explicitly supplementary diagnostics.

The only remaining mathematical exposition work identified within this scope is the secondary-example checkability addition and the two wording clarifications above. The hardcoded near-threshold expression was not treated as its own proof; it was independently reconstructed. No stronger global, continuum-wavelength, or dimension-uniform claim should be inferred from the verified theorem. Repository integrity, release links, journal presentation, and novelty are reported by the other audit lines and are outside this report's verdict.

## Cross-review of the algebra line, after independent completion

I independently checked both reported omission-proof wording defects. At m=3,a=b=1 the core matrix has all nine entries nonzero, hence all six permutation cycle covers survive. Their signed products are -10,8,5,-2,2,-1, summing to 2. Thus main.tex:485's “two surviving cycle covers” is inaccurate as a combinatorial count, although the resulting signed determinant is correct. At m=5 with X3 omitted, the stated order X2,X4,{X1,X5,Z} has nonzero couplings on both sides of the alleged block diagonal: X4 feeds the triad and the triad feeds X2. The order X4,{X1,X5,Z},X2 is block lower triangular. Thus the algebra agent's two findings and minor severity are independently confirmed; the actual determinant factorization and core theorem survive.

Verifier scope was also checked: `verify_generic_cubic_recurrence.py` establishes the all-dimensional rational identity, while `verify_cubic_sign.py` and `dd_verify_cubic_sign.py` contain finite matrix contraction checks and sign certificates; the duplicate explicitly identifies itself as such. `verify_branch_stability.py` is honestly labeled a finite floating spectral-gap regression, not a nonlinear stability proof. `verify_exchange_of_stability.py` supplies finite spectral regression, with exact finite sign checks. The four exact modulus generators and generic Schur argument carry the infinite spectrum/dimension claims; neither regression count nor duplicate entrypoint count should be described as independent proofs.
