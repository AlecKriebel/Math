# Independent mathematical audit of construction results

## Decision and scope

Accepted as partial results, with the explicit regularity clarification below. These arguments do not settle the unrestricted median inequality. This is an audit of the first shared substantive pass, not a further research pass. No novelty claim is made.

The source is A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. It concerns three whole-plane subharmonic functions normalized by u_j(0)=0, their pointwise median v_2, the unnormalized integral I(r)=integral_0^{2 pi} v_2(r exp(i theta)) dtheta, and B(r)=max_{j,theta} u_j(r exp(i theta)). The homogeneous and harmonic cases are credited to the source. Its zero-denominator convention is unspecified.

All normalized conclusions here use radii with B(r)>0. This convention must be stated rather than described as an established equivalence to assigning a value to 0/0. A successful nonzero log-periodic counterexample of the form below would have B(r)>0 at every radius and would avoid that ambiguity entirely.

## 1. Common logarithmic spiral: accepted

For rho>0 and real kappa, let continuous real 2 pi-periodic h_j satisfy

L h_j = (1+kappa^2)h_j'' - 2 rho kappa h_j' + rho^2 h_j >= 0

in distributions. Then u_j(r exp(i theta))=r^rho h_j(theta-kappa log r), with u_j(0)=0, are whole-plane subharmonic and I(r)>=0 for every r>0.

Independent reconstruction: write a=rho kappa/(1+kappa^2), b=rho/(1+kappa^2)>0. The operator divided by 1+kappa^2 is (D-a)^2+b^2. The Green formula across s=pi/b yields

h(theta+s)+exp(a s)h(theta)
 = integral_0^s exp(a(s-x)) sin(b(s-x)) f(theta+x)/b dx >=0,

where f=((D-a)^2+b^2)h>=0. This first holds for smooth h. Positive angular mollification preserves Lh>=0 and converges uniformly for continuous h, so the inequality holds without a smoothness assumption. The same positive coefficient c=exp(pi kappa) and shift s apply to all three functions. Coordinatewise monotonicity and sign reversal of the median give H(theta+s)+cH(theta)>=0 for H=median(h_j). Periodicity gives (1+c) integral H>=0. No rationality or size restriction on s modulo 2 pi is needed.

The polar Laplacian formula is correct. Continuity and rho>0 give uniform convergence to 0 as r approaches 0. The bounded-above removable-singularity theorem gives the stated extension. There is no hidden negative point mass at the origin.

## 2. Constant-coefficient angular lemma: accepted

If A>0, C>0 and B is real, continuous periodic h_j satisfying Ah_j''+Bh_j'+Ch_j>=0 have nonnegative median integral.

For complex roots a+-ib, b>0, the preceding positive half-period Green kernel applies unchanged. For real roots lambda_1,lambda_2, their product C/A is positive, so both are nonzero and have the same sign. The inverse of D-lambda on periodic functions reverses positivity for lambda>0 and preserves positivity for lambda<0: this follows at an extremum from y'-lambda y=f>=0. Composing two inverses of the same sign gives h>=0. More explicitly, if both roots are positive, y=(D-lambda_2)h<=0, so (D-lambda_2)(-h)>=0 implies -h<=0. If both roots are negative, both steps preserve nonnegativity. Repeated roots cause no change. Positive mollification again extends the conclusion to the stated distributional hypotheses.

C>0 is essential to this particular classification; no assertion for arbitrary C<=0 is inferred.

## 3. Common rotating-separable functions: accepted, with a clean regularity proof

Assume F:R->(0,infinity) and psi:R->R are C^2, F(t)->0 as t->-infinity, h_j are continuous and periodic, and U_j(t,theta)=F(t)h_j(theta-psi(t)) are subharmonic in the corresponding punctured plane. Then I(r)>=0 for every r.

A positive C^2 function F on the entire real line with that left limit must have F''(t_0)>0 somewhere. Otherwise F is concave. A positive derivative would force negative values far to the left; a negative derivative would force negative values far to the right. Hence a globally positive concave F is constant, contrary to its left limit.

The coefficient calculation is correct:

A(t)=1+psi'(t)^2,
B(t)=-(2F'(t)psi'(t)/F(t)+psi''(t)),
C(t)=F''(t)/F(t).

A robust justification of positivity at the selected radius avoids any informal restriction of a distribution to a slice. Convolve u_j with a nonnegative approximate identity in the rotation variable. Rotations preserve subharmonicity, and their positive average is subharmonic. Its angular profile is h_{j,epsilon}=h_j*eta_epsilon, smooth in angle; because F and psi are C^2, the averaged u_j is C^2 away from 0. Its pointwise nonnegative Laplacian gives

A(t)h_{j,epsilon}''+B(t)h_{j,epsilon}'+C(t)h_{j,epsilon}>=0

at every t and angle. At t=t_0 the angular lemma applies with A>0,C>0. Uniform convergence of the profiles and the 1-Lipschitz property of the median give integral median(h_j)>=0. Multiplication by F(t)>0 and angular translation then prove the result at all radii. The limit at the origin is again uniform, and the removable singularity is legitimate.

This supplies the full distributional/fixed-radius justification under exactly the reported C^2 and continuity assumptions; no stronger smoothness or almost-every-radius conclusion is being silently substituted.

## 4. Compact logarithmic potentials plus polynomial harmonic parts: accepted

Let mu_j be finite positive compactly supported measures with integral |log|a|| dmu_j(a)<infinity, and P_j polynomials with Re P_j(0)=0. Then

u_j(z)=Re P_j(z)+integral (log|z-a|-log|a|) dmu_j(a)

are admissible, allowing logarithmic poles away from 0, and satisfy the normalized supremum assertion on B>0 unless the triple is identically zero.

The log-moment assumption makes normalization finite and excludes an atom at 0. Standard local integrability and upper semicontinuity of the logarithmic potential identify it with its subharmonic representative; the defining integral at 0 is zero. If support lies in |a|<=R, then for r>2R,

u_j(r exp(i theta))=Re P_j(r exp(i theta))+M_j log r-C_j+O(r^{-1})

uniformly in angle, because |log|1-a/z||<=2|a|/r.

If every real harmonic polynomial is zero, positive mass gives eventual uniform positivity, and zero mass gives the zero function. Otherwise take the highest nonzero harmonic degree d>=1. Its profiles h_j satisfy h_j(theta+pi/d)=-h_j(theta), including the zero profiles. Their median has zero integral. Uniform 1-Lipschitz dependence of the median gives I(r)=O(r^{d-1}+log r), while B(r)=b r^d+O(r^{d-1}+log r) with b>0. Thus I/B->0. This proves only the claimed compact-mass/polynomial subclass.

## 5. Log-periodic sufficient reduction: accepted; no counterexample supplied

Let rho,omega>0 and let continuous doubly 2 pi-periodic H_j satisfy, in distributions,

L H_j=((omega partial_s+rho)^2+partial_theta^2)H_j>=0.

Then u_j(r exp(i theta))=r^rho H_j(omega log r,theta), u_j(0)=0, are admissible. Positive torus mollification proves the distributional assertion by smooth approximation, and boundedness of H_j gives the removable origin. No smoothness beyond the stated continuity is necessary.

Let M(s)=integral median(H_j(s,theta)) dtheta and C(s)=max_{j,theta}H_j(s,theta). Both are continuous. If M(s)<0 for every phase, then C(s)>0: otherwise all three u_j are nonpositive on the associated circle, whereas subharmonicity and u_j(0)=0 force each circle mean to be nonnegative, hence all three continuous circle values to vanish, contradicting M(s)<0. Set delta=-max_s M(s)>0 and C_max=max_s C(s)>0. The exact ratio satisfies

I(r)/B(r)=M(omega log r)/C(omega log r)<=-delta/C_max<0.

Because omega log r ranges over every phase, this would refute the full supremum target. A merely negative value at some phase would not.

The Fourier multiplier is exactly (rho+i omega m)^2-n^2. Its vanishing requires m=0 and rho=|n|. Consequently any positive noninteger rho permits finite Fourier inversion of a trigonometric square forcing F_j=P_j^2. Real conjugate symmetry is preserved, producing a real finite trigonometric H_j with L H_j=F_j>=0. These are legitimate candidate formulas, not a certificate of negative median.

## Numerical material

The reported finite-grid probes are exploratory. Near resonance, tiny normalized values can result from a large nearly harmonic denominator. Neither floating-point sign nor a grid maximum proves the needed continuum-phase inequality. This audit accepts no numerical claim as a theorem and makes no inference of a positive universal gap from the probes.

## Final limitation

The unrestricted conjecture remains unresolved. Common profiles and rotations, compact Riesz support with polynomial harmonic parts, and a sufficient finite-dimensional search reduction do not exhaust whole-plane subharmonic triples. The source's credited cases and these subclass results must not be presented as a general proof or a new historical resolution.
