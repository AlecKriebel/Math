# Completed square reconstruction and fresh falsification mechanisms

This completes the independently sealed reconstruction, after reading all
four family reports/derivations and actual scripts. It validates attributed
external results. It neither claims research novelty nor certifies broader
rectangular or continuous-shape transition results. Standard Gamma/Beta,
Laguerre, finite Pfaffian and hypergeometric identities are used within
their domains. All infinite steps are analytic; finite controls are stated
separately. No root/family verdict is a proof premise.

## 1. Square real law and finite skew inverses

The exact law is the square Gaussian SVD Jacobian in the early seal.
Use p_j=L_j, w=x^-1/2 exp(-x/2), phi_j=w p_j,
psi_j=integral sign(y-x)phi_j(y)dy, B_ij=integral phi_i psi_j,
v_j=integral phi_j. The operator D=x d/dx+(1-x)/2 obeys

    D p_j=((j+1)p_(j+1)-j p_(j-1))/2,
    w Dp_j=(x phi_j)',
    (j+1)B_(i,j+1)-jB_(i,j-1)=-4 delta_ij.

The last identity follows by integration by parts in the defining skew
integral, since x phi_j vanishes at both endpoints; its weight exponent at
zero is +1/2. This is an identity of actual Gaussian integrals, not a
presumed density. Antisymmetry gives zero same-parity entries and

    B_(2k,2l+1)=0 (l<k),
    B_(2k,2l+1)=-4/(2k+1) product_(a=k+1)^l 2a/(2a+1) (l>=k).

The recurrence starts at j=0, with B_(i,1)=-4 delta_i0, and inductively
fixes every finite entry. Independently, the generating function for v is
sqrt(2pi)(1-z^2)^-1/2, hence v_(2k)=sqrt(2pi)(1/2)_k/k! and odd v=0.
All generating integrals converge absolutely near zero.

For even N the omitted column B_(i,N) vanishes for i<N, giving
B_N D_N=-2I and B_N^-1=-D_N/2. For odd N the last column of B_N vanishes,
while B_(i,N)=-4v_i/(Nv_(N-1)). Append the border v to the finite matrix.
Direct multiplication verifies the augmented inverse

    [ -D_N/2, -e_last/v_last ; e_last^T/v_last, 0 ].

Specifically B_N(-D_N/2)=I-v e_last^T/v_last, v^T D_N=0,
B_N e_last=0, and the border supplies the missing rank-one term. This
establishes the odd case, including N=1, without continuation from even N.
The determinant/Pfaffian pairing expansion of the ordered joint law and
functional differentiation give counting density

    R_even=-phi^T B_N^-1 psi,
    R_odd=phi^T D_N psi/2+phi_last/v_last.

The sign follows from psi_j'=-2phi_j. For bounded test functions the
differentiation is immediate; polynomial/exponential-tail bounds extend
it to sqrt(x). Laguerre telescoping reduces the adjacent-pair sum to

    e^-x sum_(j<N)L_j^2+(N/4)phi_(N-1)psi_N.

The odd border is then added. The recursion
psi_(j+1)=j psi_(j-1)/(j+1)-4x phi_j/(j+1), starting from
psi_0=sqrt(2pi)[2 erfc(sqrt(x/2))-1], produces exactly the parity
Phi1/Phi2 and Gamma duplication factors in the sealed density formula.
At N=1, e^-x cancels phi_0 psi_1/4 and the border leaves
exp(-x/2)/sqrt(2pi x), the exact chi-square-one density.

Fresh Livan--Vivo publisher bytes also give equation(16), with their
rho=R(x/2)/(2N), R_2 having weight exp(-x). Their equation(1) instead
uses exp(-x/2) for both beta values. Substituting x/2 therefore supplies
the exact 1/2 Jacobian and the same square formula. This separate primary
cross-check agrees with the direct joint-law argument.

## 2. The newly supplied angular route, checked after the seal

The real falsifier's mechanism was not read before my seal. I subsequently
checked its elementary Gaussian integration independently. With
a=(1+z)/(2(1-z)), b=(1+t)/(2(1-t)), x=u^2,y=v^2, the joint Laguerre
skew generator is

    B(z,t)=4/((1-z)(1-t)) integral_(u,v>0)
           sign(v-u) exp(-au^2-bv^2) du dv
          =4/sqrt((1-z^2)(1-t^2)) [pi/2-2 arctan R],
    R=sqrt((1+t)(1-z)/((1-t)(1+z))).

After U=sqrt(a)u,V=sqrt(b)v the angular switch is arctan sqrt(b/a),
and the radial integral is 1/2. In a real neighborhood of zero this is an
ordinary absolutely convergent integral; analytic extension near zero
allows coefficient extraction. Differentiating the explicit expression
and using R/(1+R^2)=sqrt((1-z^2)(1-t^2))/(2(1-zt)) gives

    (1-t^2) B_t-tB=-4/(1-zt).

Its every-index recurrence is the one in Section1. The scale, sign, and
zero same-parity blocks agree. Thus this is an independent integration
of the all-index skew premise. It is not a circular appeal to the claimed
one-point correction.

## 3. Abel/Fubini, ordinary tails, and the positive correction

The sealed Beta/parity generator is valid at every 0<zeta<1. For each
fixed monomial x^j from L_(N-1), the absolute integral of either signed
generator branch against x^(j+1/2)e^-x is
Gamma(j+3/2)(1 minus/plus zeta z)^(j+1/2). This is bounded by a constant
times 2^(j+1/2); the remaining (1-z^2)^-1/2 is integrable. This is an
absolute majorant, including the negative branch which grows in x.
It justifies Fubini and integrated dominated convergence. At an interior
zeta, choose a Cauchy circle zeta<A<1; the coefficient bound contains
A^-s exp(x A/(1+A)). After multiplication by e^-x the exponential tail
is exp(-x/(1+A)), and (zeta/A)^s is summable. Thus termwise integration
at an interior Abel parameter is also justified independently.

The boundary changes of variable give Phi2, and cancel the finite parity
initial segment. Both parities leave second index N-1+2u, u>=1. The
finite connection Q(r,s)=sum sigma_(r-j)sigma_(s-j)h_j gives
Q(r,s)=O_r(s^-3/2); weights are O(m^-1/2), so the completed tail is an
ordinary absolutely convergent O_N(m^-2) series. Constants may depend on
fixed N. No uniform-in-N tail estimate is required for subtraction of two
fixed dimensions.

The Fourier/Beta identities in the seal show
K_(r,d)=kappa_d+E_(r,d)>0 and K_(r+1,d)<=K_(r,d), including r=0.
This proves Xi_N=sum_(u>=1) A_(N,u)K_(N-1,2u) with ordinary convergence.
Kernel positivity alone was not used to excuse an interchange.

## 4. All-N square coefficient comparison, without a shape hypothesis

I checked the new falsifier's Gamma-product mechanism after my seal.
Write c=N/2. The exact ratio A_(N+1,u)/A_(N,u) is the sealed finite
product. Each product factor exceeds one; its infinite limit is
Gamma(c)Gamma(c+1)/Gamma(c+1/2)^2. For c>1/4 set

    f(c)=log[Gamma(c+1/2)/Gamma(c)]-(1/2)log(c-1/4).
    f'(c)=(1/2) integral_0^infinity e^(-(c-1/4)t)
                         [sech(t/4)-1]dt<0.

This follows from the standard digamma difference integral by combining
denominators before subtraction. All integrals converge for c>1/4.
Gamma quotient asymptotics give f(c)->0, so f(c)>0 throughout that
domain. Consequently Gamma(c+1/2)/Gamma(c)>sqrt(c-1/4).

For N>=2 the finite ratio is strictly below
(N/(N+1))^1.5(2N+1)/(2N-1)<1. Squaring is legal and its exact residue
is 4N^4-5N^2-N+1; at N=t+2 it is
4t^4+32t^3+91t^2+107t+43>0. At N=1 the exact infinite product bounds
the finite ratio by 3pi/(8sqrt2)<1, using pi<22/7, sqrt2>7/5.
Thus all positive dimensions and every u have strict coefficient decrease.
The finite product is also >N/(N+1), as its first prefactor already is.

The early reconstruction's q(x)=G(x)/sqrt(x), q'>0, q(3/2)>15/16,
and exact first-diagonal ratio give
Xi_N-Xi_(N+1)>1/[8pi N(N+1)] for N>=3. Every discarded term is
nonnegative in the common-coordinate subtraction

    sum_u (A_Nu-A_(N+1,u))K_(N-1,2u)
    +sum_u A_(N+1,u)(K_(N-1,2u)-K_(N,2u)).

No unsupported continuous-shape theorem is essential. The source's
auxiliary shape comparison is itself a Gamma-product inequality: its
derivative reduces to x^2-x-1/2>=0 for N>=3, and its shape-one product
telescopes. I checked that algebra too. It cannot smuggle the target,
and the square-only route eliminates it entirely.

## 5. Complete complex bound, analytic transfer and exact constant

The density/finite connection/generating function/ODE and sign induction
are in the early seal. `new_controls.py` independently multiplies the
polynomial coefficients of the conjugated ODE. With
g=z(1-z)^-5/2, the recurrence operator applied to gF is exactly

    g(1-z)[z(1-z)F''+F'-F/4].

This identity, not a tested dimension prefix, proves the recurrence for
every coefficient. The standard hypergeometric continuation is on the
principal branch C minus [1,infinity). The Gamma/digamma extraction
uses fixed half-integer shifts, which are not poles. The first three
singular coefficients reproduce the exact -17/6 constant; for instance
65/48-15/8+11/32=-17/96. The derivative of log n in a consecutive
difference supplies the further -1/2, producing -10/3, rather than merely
doubling the level constant.

Here is the relevant transfer argument explicitly. Choose a full
Delta-domain |z|<1+eta with a narrow wedge from 1 excluded. Because F
has its only unit-circle singularity at1 and is analytic on the principal
slit plane, the domain exists. Truncation through J leaves
R_J=O(|1-z|^(J-3/2)(1+|log(1-z)|)) uniformly on its closed subsectors.
Deform the Cauchy coefficient contour to two rays from1 at fixed angles
having |z|>1, a radius1/n arc, and outer arcs away from the singularity.
The outer arcs are exponentially small. On a ray distance rho>=1/n,
|z|^-n<=C exp(-c n rho), so the integral is bounded by

    C integral_(1/n)^eta exp(-c n rho) rho^(J-3/2)
                            (1+|log rho|) d rho
      =O(n^(-J+1/2)log n).

The small arc has length O(1/n) and the same bound. This proves the
coefficient remainder used by AP. A real-axis expansion alone, or an
extra pole elsewhere on the unit circle, would not allow the deformation.

Arbitrary-depth transfer estimates must precede substituting the
asymptotic expansion in the recurrence. For any fixed desired coefficient,
choose the remainder sufficiently small even after multiplication by n^2;
then coefficient comparison is valid. Only indices j,j-2,... couple,
with multiplier j(j-2), nonzero for odd j. Thus all odd inverse powers
vanish. This produces the O(log n/n^4) level remainder; bounding two
remainders separately gives the stated O(log n/n^4) decrement remainder.
Therefore E_n->C0=gamma+6log2-10/3 analytically, not by fitting data.

The remaining universal AP dependency is checked in the early seal:
positive convolution gives the independent alpha_C auxiliary upper bound;
the all-0<t<1 even/odd coefficient comparison gives the q upper bound,
including q1; the exact recurrence makes E strictly decreasing to C0;
that establishes the lower Delta sign and alpha_C>8/(3pi); only then the
first positive q coefficient gives the desired Delta upper bound through
infinite telescoping. The dependency graph is acyclic. Strictness of the
infinite upper bound is retained because at least its first summand has a
strict inequality and the positive majorant series converges.

AP's printed Lemma6 index omits q1, but its actual proof explicitly proves
the scalar inequality on every 0<t<1, including t=1/2. This checkable
wording repair requires no conjectural extension. My new direct rational
log/radical enclosure additionally verifies the actual q1 boundary, not
merely its Taylor coefficients. BD's printed real domain x>=0 is read as
0<=x<=1; every use x=1/N lies there. Both local wording issues are already
described correctly by the corrected package.

## 6. Real reserve, exact N=1,2,3, and limit

Subtracting the proven AP decrement gives the early sealed pointwise
reserve. H_4+6log2-10/3<59/20<3 and increments 1/(N+1)<3/4 prove the
harmonic inequality inductively for all N>=4. Positive rational constants
then give the strict uniform reserve 1/(160N^2). N=3 uses the exact first
diagonal with rational bounds, or the independently reproduced interval.

Direct finite density integration gives the raw means
Y1=sqrt(2/pi), Y2=sqrt(pi)(2-sqrt2/2),
Y3=3sqrt(pi)/2+2sqrt(2/pi),
Y4=sqrt(pi)(153/32-3sqrt2/4).
The even incomplete-Gamma integrals satisfy I0=2-sqrt2,
I_j=2jI_(j-1)-sqrt2 Gamma(j+1/2)/sqrt(pi), proved by integration by
parts; odd border integrals are 2^(j+1)j!. These produce the displayed
values without assuming an Appendix assertion. The independent monomial
joint-law integration reproduces them, and the exact Machin/pi and
integer-square-root enclosures reproduce N1..3 strictly above their
rational targets. Decimal illustrations do not decide acceptance.

Square Marchenko--Pastur convergence has the required uniform
integrability: expected empirical first eigenvalue moment of XX*/N is1,
so the discarded sqrt(x) tail beyond M is at most1/sqrt(M). Therefore both
means tend to8/(3pi). This uses no continuous-shape transition conclusion.

## 7. Materially new controls and explicit overlap

The new 112-control script imports no historical/sibling code. Its skew
products, Gamma constants and Pfaffian mechanism overlap the analytic
routes already read; I do not count those premises as a new independent
theorem proof. Its new application checks the *joint partition*, which
tests eigenvalue correlations beyond one-point density moments.

For the monomial weight x^(i-1/2)exp(-x/2), replacing the Gaussian rate by
a/2 scales each skew entry by a^-(i+j+1) and an odd border by a^-(i+1/2).
Congruence of a finite Pfaffian scales its partition by
a^-sum_(i=0)^(N-1)(i+1/2)=a^(-N^2/2). Independently,
Tr(XX^T) is the sum of N^2 independent squared standard real Gaussians,
so its Laplace transform is (1+2t)^(-N^2/2). They agree universally.
The script checks the exact finite matrices for N1..10 at a=4,9,16.
Finite Pfaffian log derivatives give mean N^2 and variance2N^2 for the
*joint trace*, distinct from ETr(W^2) tested earlier. A wrong beta/radial
exponent and an untilted odd border are rejected. These are exact rational
tests with both parities, bounded in dimension.

Two analytic negative controls also show why the universal assumptions
matter. Adding z^40/(1+z) to H preserves its first39 coefficients and is
analytic at+1; it creates a unit-circle singularity at-1 and alternating
coefficients. The added Y/sqrt(pi) coefficients are (-1)^(n-40), so the
normalized sequence acquires an n^-3/2 alternating error; its E sequence
has no prescribed finite limit. The full Delta-domain/sole-singularity
hypothesis rejects this construction, although the initial prefix does
not. Adding z^40(1-z)^-1/2 also preserves that prefix and the leading
limit/logarithmic slope, but its Gamma coefficients add 1/n^2 to alpha
to leading order and 16pi to the E constant. It fails the exact recurrence
already at n=39. Thus a fitted leading limit and log slope cannot certify
the telescoping constant. These are constructed mutants, not claimed
counterexamples to the actual law. The script detects their exact first
recurrence failure, and the analysis above gives their asymptotic effect.

The new direct q1 enclosure uses the positive rational expansion
log2=2 sum_(k>=0)1/((2k+1)3^(2k+1)), with an explicit geometric tail,
and integer-square-root radical intervals. It proves
0<q1=3sqrt3+1-(35/8)sqrt2<3log2/(160sqrt2).
This is a finite analytic boundary certificate. Every diagnostic range
and count remains explicit; no number of executed assertions proves an
unbounded theorem.

The complex family's alternate finite contiguous certificate was also read
and checked after the seal. Put D=(k-1)(k+2). Multiplying its exact summand
ratio by q_(j+1) cancels all denominators, leaving

    n(q_(j+1)g_(j+1)/g_j-q_j)
      =(j-n)(j+1-k)(j+k+2)-j(j+1)(j+alpha+1)
      =-(n+alpha-1)j^2-(D+3n+alpha+1)j+nD.

This is the stated h_j polynomial identity at every index, not an
interpolation. q_0=0 and the terminating (-n)_(n+1)=0 make the two
telescoping endpoints vanish. Direct square Q0,Q1,Q2 supply the n=1
boundary. It confirms the alternate cited recurrence route; acceptance
continues to use the independently derived square ODE, and does not
promote the family's broader rectangular theorem.

For clarity, the immutable early seal's plain-text `e^-t/4` in the
Gamma-quarter log derivative means `exp(-t/4)`, not `exp(-t)/4`. The
exact derivative is integral exp(-xt)/(1+exp(-t/4)) dt; it is greater
than1/(2x). This explicit parenthesization removes a notation ambiguity
without changing the sealed mathematical mechanism.

The all-index AP scalar coefficient proof can be written without finite
extrapolation. Put lambda_j=(128/3) binom(3/2,2j+4). Its ratio is
(4j+5)(4j+7)/[4(2j+5)(2j+6)]. Comparing to(j+1)/(j+2) leaves the
strict positive polynomial24j^2+77j+50. With lambda3=143/2048<1/12,
induction gives lambda_j<1/[3(j+1)] for every j>=3. For the other series,
a_m=integral_0^1 [s^(m+1)-(-1/2)^(m+1)]/(s+1/2) ds. Thus
a_(2j)>1/[3(j+1)] by s+1/2<=3/2. At every odd index,

    a_(2j+1)=sum_(k=0)^j 4^-k
             [1/(2j+2-2k)-1/(2(2j+1-2k))]>=0,

where each bracket is nonnegative by cross multiplication and all
denominators are positive. The remaining even comparisons are exact:
a0=lambda0=1, a2=1/3>7/24=lambda1,
a4=19/120>33/256=lambda2. Both series converge absolutely for0<t<1.
Coefficient comparison therefore proves the scalar inequality throughout
that interval, strictly because the t^2 coefficient is strict. In
particular t=1/2 proves the omitted q1 boundary; its printed index
restriction does not impose a mathematical gap.
