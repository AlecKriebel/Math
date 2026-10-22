# Independent analytic input for PR1049's Jensen repair

This note was derived independently after reading all of Yakir, arXiv:2011.06234v2, including Sections 3–5. It supplies the analytic argument missing from the conditional repair, rather than assuming Lemma 1.3. This is an AI-assisted audit note, not an independent human peer review or a new publication. It does not change any PR or published paper. The two standard background theorems used are stated explicitly below; their hypotheses are checked. No global priority claim or proof of those classical theorems is made.

## 1. Exact target and source defects

Let n be an integer, P(z)=sum_{j=0}^{n-1} X_j z^j, with independent uniform signs. Put

S_r=sum_{j=0}^{n-1} r^(2j), sigma_r=sqrt(S_r), p_r(theta)=P(r exp(i theta))/sigma_r,

and let mu be normalized angular measure. The required input is, uniformly for |r-1|<=n^(-11/10),

E L_r = -gamma/2 + O(n^(-1/2) log^2 n),
E L_r^2 = gamma^2/4 + O(n^(-1/2) log^2 n),
L_r=integral log|p_r(theta)| dmu(theta).

The second line is an ordinary second moment, not an absolute second moment of the pointwise logarithm before angular integration. Together these statements give E(L_r+gamma/2)^2=O(n^(-1/2)log^2 n).

Yakir's Lemma 3.2 is false under its written angle exclusions. Because the coefficients are real, |p_r(-theta)|^2=|p_r(theta)|^2 identically. At theta=pi/2, phi=-pi/2, its joint conclusion would turn the same nondegenerate random variable into two asymptotically independent exponential variables. For r=1 and n divisible by four, the two coordinates of P(i)/sqrt(n) converge to independent N(0,1/2), so, at x=y=1, the joint CDF tends to 1-exp(-1), whereas F(1)^2=(1-exp(-1))^2. Their difference tends to exp(-1)-exp(-2)>0. These angles meet the stated exclusions for all sufficiently large n. The marginal assertion also fails at theta=pi: P(-1)/sqrt(n) is real, and its squared modulus tends to chi-square with one degree of freedom, not Exp(1).

The following correction removes all resonances of the covariance, including endpoints of the angular interval. Their total measure remains O(n^(-1/2)), which suffices after truncation. The original source's pointwise lemma must not be cited as literally correct. Other imprecisions in its root-factorization and truncation bookkeeping are replaced below.

## 2. Standard background, with precise scope

**Turan–Nazarov inequality.** If Q(theta)=sum_{k=1}^h c_k exp(i m_k theta) has h distinct integer frequencies, I is an interval, and E is a measurable subset of positive measure, then

sup_I |Q| <= (C |I|/|E|)^(h-1) sup_E |Q|.

Here the constant C is absolute and all frequencies are purely imaginary exponents. This is the specialization of the theorem stated in F. Nazarov, *Local estimates for exponential polynomials and their applications to inequalities of the uncertainty principle type*, Algebra i Analiz 5:4 (1993), 3–66; English translation St. Petersburg Math. J. 5:4 (1994), 663–717. Its primary journal abstract gives the more general complex-exponent formula, with the extra exp(max |Re lambda_k| |I|) factor. That factor equals one here. We use h<=20 only. [Primary journal statement](https://m.mathnet.ru/php/archive.phtml?jrnid=aa&option_lang=rus&paperid=397&wshow=paper).

**Fixed-dimensional convex-set Berry–Esseen inequality.** For independent centered R^d-valued Y_j with V=Cov(sum Y_j) positive definite, if Z is centered Gaussian with covariance V, then

sup_{K convex Borel} |Pr(sum Y_j in K)-Pr(Z in K)|
 <= C d^(1/4) sum_j E|V^(-1/2)Y_j|^3.

We use d=2 or 4. This is the theorem stated in V. Bentkus, *A Lyapunov-type bound in R^d*, Theory Probab. Appl. 49:2 (2005), 311–323, DOI 10.1137/S0040585X97981123 (original 2004). [Primary journal statement](https://www.mathnet.ru/php/archive.phtml?jrnid=tvp&option_lang=eng&paperid=230&wshow=paper). It applies to nonidentically distributed summands and to products of disks, since those sets are convex. It is not an appeal to an unspecified CLT with an unspecified rate.

## 3. Uniform radial bounds and a deterministic logarithmic bound

All constants below are uniform over |r-1|<=n^(-11/10), for all sufficiently large integer n. For 0<=j<n, j|log r|=O(n^(-1/10)), hence r^j and r^(-j) are bounded by fixed constants and S_r=n(1+O(n^(-1/10))). In particular c n<=S_r<=C n. Cauchy–Schwarz gives |p_r(theta)|<=sqrt(n).

P has degree n-1, nonzero constant term, and leading coefficient of modulus one. The elementary Cauchy root bound, applied also to its reversed polynomial, places every root beta in 1/2<|beta|<2. Therefore

log|p_r(theta)|=(n-1)log r-log sigma_r
                   +sum_{j=1}^{n-1} log|exp(i theta)-beta_j/r|.

For large n, |beta_j/r| lies in a fixed compact annulus, say [1/4,4]. Uniformly on this annulus, the L^4(mu) norm of log|exp(i theta)-a| is bounded. Indeed the positive part is bounded above by log 5; with t the circular distance from theta to arg a, the identity

|exp(i theta)-a|^2=(1-|a|)^2+4|a|sin^2(t/2)

bounds the negative part by C+|log |t||, whose fourth power is integrable. Minkowski's inequality, with |(n-1)log r-log sigma_r|=O(log n), consequently gives

integral |log|p_r(theta)||^4 dmu(theta) <= C n^4.              (A)

This holds for every sign choice, including repeated roots and roots exactly on |z|=r. Thus all angular logarithmic integrals in this note exist. Finite sign spaces and the absolute integral bound justify each interchange with expectation; a divergent pointwise expectation at theta=0 or pi causes no Fubini problem here.

## 4. A uniform small-value estimate with sufficient tail strength

We prove the only strength needed later, without trusting the numerical exponent 240 in the source's Proposition 3.1:

q_r(a):=integral Pr(|P(r exp(i theta))|<=a)dmu(theta)
 <= C [n^(-5)+a+n^(121) a log(1/a)]     (0<a<1/3).          (B)

First, a Fourier smoothing bound gives, for any real random variable Y with characteristic function g,

Pr(|Y|<=a) <= C a integral_{-2/a}^{2/a} |g(lambda)| dlambda.

For completeness take K(u)=(sin u/u)^2: K is bounded below by a positive constant on [-1,1], and its Fourier transform is a nonnegative triangular function supported on [-2,2]. Fourier inversion and expectation prove the displayed bound. Thus no density assumption is needed.

For Y=Re P(r exp(i theta)), independence and the inequalities

|cos u|<=exp(-2 ||u/pi||_(R/Z)^2),
cos(2u)>=1-2pi^2 ||u/pi||_(R/Z)^2

give, writing H_lambda(theta)=sum_{j=0}^{n-1}cos(2lambda r^j cos(j theta)),

|g(lambda)| <= exp(-n/pi^2) exp(H_lambda(theta)/pi^2).

The set H_lambda<n/2 contributes O(exp(-c n)) after multiplication by a and integration over an interval of length 4/a. For its complement Lambda_lambda, Markov's inequality with the tenth power will apply. Expand H_lambda^10 into at most 2^10 n^10 oscillatory integrals with phases

T(theta)=2sum_{ell=1}^{10} s_ell r^(k_ell) cos(k_ell theta),
s_ell in {-1,1}, 0<=k_ell<n.                               (C)

The harmless powers of 2 from the cosine expansion are absorbed into C. If T is constant, every nonzero frequency has balanced signs, so every nonzero index has even multiplicity. Since ten is even, the zero index also has even multiplicity. There are O(n^5) such index tuples, and at most 2^10 sign choices per tuple. Their integral has absolute value one. This counts constant nonzero phases as well as identically zero phases.

For a nonconstant T, combine equal frequencies before applying Turan. There are at most 20 nonzero frequencies in T'; they lie in [-n,n]. Every nonzero Fourier coefficient of T is an integer multiple of r^k, so at least one nonzero-frequency coefficient of T' has modulus >=c>0, uniformly in r; all coefficients of T are <=C because at most ten summands were combined. Parseval gives sup |T'|>=c. Notice that T is real; we assert no oscillatory bound for an arbitrary complex phase.

Set b=n^(-120), E={|T'|<=b}. The measurable-set Turan–Nazarov theorem applied to T', whose number h of terms satisfies 2<=h<=20, yields

mu(E) <= C b^(1/(h-1)) <= C n^(-120/19) <= C n^(-6).

On the complement, split at the zeros of T'' and at the level crossings T'=+b or -b. A nonzero trigonometric polynomial of degree <=n has at most 2n zeros per period. Each level equation has at most 2n roots, so there are O(n) pieces. T'' is not identically zero for a nonconstant periodic T. On every piece T' has constant sign, is monotone, and has modulus >=b. Integration by parts then gives absolute oscillatory integral <=C/(|lambda|b): the endpoint terms are bounded by 2/(|lambda|b), and the integral of |T''|/|T'|^2 equals the variation of 1/T', at most 2/b. Consequently

|integral exp(i lambda T(theta))dmu(theta)|
 <=C [n^(-6)+n^(121)/|lambda|], lambda!=0.                  (D)

This proof handles cancellations, coefficients outside the source claim's stated [1/2,1] range, and the number of level crossings explicitly.

Expanding (C), bounding the O(n^5) constant phases separately, and using (D) on the rest gives

integral H_lambda(theta)^10 dmu(theta)
 <= C [n^5+n^10 n^(-6)+n^10 n^(121)/|lambda|].

Since H_lambda>=n/2 on Lambda_lambda, Markov gives

mu(Lambda_lambda)<= min{1,C[n^(-5)+n^(121)/|lambda|]}.

Integrate this from |lambda|=1 to 2/a, bound |lambda|<=1 by its length, and apply the smoothing inequality. This proves (B); exp(-c n) is absorbed by n^(-5), and log(2/a)<=C log(1/a). In particular, with a_n=n^(-400),

q_r(a_n)<=C n^(-5).                                      (E)

The large exponent 400 is a fixed proof parameter, independent of r and of the signs. No claim is made that it is optimal.

## 5. Corrected angular Gaussian estimate

Let d(eta) be distance to 2pi Z, and let h_n=n^(-1/2). By the geometric sum,

W_r(eta)=(1/S_r)sum_{j=0}^{n-1}r^(2j)exp(i j eta)
          =(1-r^(2n)exp(i n eta))/(S_r(1-r^2 exp(i eta))).

For d(eta)>0,

|W_r(eta)|<= C/(n d(eta)).                               (F)

Indeed r^(2n) is bounded uniformly and
|1-r^2 exp(i eta)|^2=(1-r^2)^2+2r^2(1-cos eta)>=c d(eta)^2.
This proof includes r=1 by continuity and does not subtract nearly equal radial and angular bounds.

For the one-point approximation exclude d(2theta)<=h_n. For the two-point approximation exclude

B_n={d(2theta)<=h_n} union {d(2phi)<=h_n}
        union {d(theta-phi)<=h_n} union {d(theta+phi)<=h_n}.  (G)

The one-dimensional excluded measure is O(h_n), and (mu x mu)(B_n)=O(h_n): each of the four conditions describes finitely many strips on the two-dimensional torus. Thus real-axis, conjugate-angle, diagonal, and wraparound resonances are all covered.

Outside (G), expand the covariance matrix of (Re p(theta),Im p(theta),Re p(phi),Im p(phi)) using the product-to-sum identities. Its diagonal 2x2 blocks differ from (1/2)I_2 by linear combinations of W_r(2theta), respectively W_r(2phi); its off-diagonal blocks are linear combinations of W_r(theta-phi) and W_r(theta+phi). By (F),

V=(1/2)I_4+O(n^(-1/2)) in operator norm, uniformly.

The analogous two-dimensional assertion holds outside the one-point excluded set. In particular eigenvalues lie in [1/4,3/4] for all large n. Each independent centered summand has norm <=C n^(-1/2), so

sum_j E|V^(-1/2)Y_j|^3<=C n^(-1/2).

Bentkus's inequality therefore compares the distribution with N(0,V) to error C n^(-1/2) on disks or products of disks.

Here is also an explicit uniform comparison of N(0,V) with N(0,(1/2)I_d), replacing the source's informal density expansion. Set V_s=(1/2)I_d+s(V-(1/2)I_d), E=V-(1/2)I_d. If f_s is the Gaussian density, then

d f_s(x)/ds=(1/2)f_s(x)[-tr(V_s^(-1)E)+x^T V_s^(-1) E V_s^(-1)x].

Integrating the absolute value bounds its L^1 norm by C_d ||E||, since all V_s eigenvalues stay between 1/4 and 3/4. Integrating s from zero to one gives Gaussian total variation O(n^(-1/2)). Squared norms of independent two-dimensional N(0,(1/2)I_2) blocks have distribution F(x)=1-exp(-x). We have proved

sup_x |Pr(|p(theta)|^2<=x)-F(x)|<=C n^(-1/2),

and

sup_{x,y} |Pr(|p(theta)|^2<=x,|p(phi)|^2<=y)-F(x)F(y)|
 <=C n^(-1/2),                                          (H)

on the corrected good sets. No such assertion is needed on B_n.

## 6. Truncation, tail errors, and both moments

Let f(theta)=log|p_r(theta)| and A_theta={|P(r exp(i theta))|<=a_n}, with a_n=n^(-400). Bound (A) gives a deterministic integral |f|^4<=C n^4, and (E) gives E integral 1_A<=C n^(-5).

On the product probability/angular space, Cauchy–Schwarz yields

E integral |f(theta)|1_A dmu <= C n * q_r(a_n)^(1/2)
                              <=C n^(-3/2).

For the second moment, on the product space of signs,theta,phi,

E integral integral |f(theta) f(phi)|1_{A_theta} dmu dmu
 <= [E (integral f(theta)^2dmu)^2]^(1/2) q_r(a_n)^(1/2)
 <= C n^2 q_r(a_n)^(1/2) <= C n^(-1/2).

The same bound holds with A_phi. Hence deleting the events A_theta or A_phi changes the first or second moment by at most O(n^(-1/2)). These estimates justify the tails uniformly, rather than inferring integrability from a pointwise limiting distribution.

For the truncated variables put

v_n=a_n^2/S_r, U_theta=|p_r(theta)|^2,
g_n(x)=(1/2)log x * 1_{v_n<x<=n}.

Since U_theta<=n, g_n(U_theta)=f(theta)1_{A_theta^c} exactly, including the chosen endpoint convention. Uniformly, v_n is between c n^(-801) and C n^(-801), and g_n has total variation O(log n), including both endpoint jumps. A one-dimensional integration by parts against CDFs bounds expectation differences by CDF sup-distance times total variation. Applying it twice gives the two-dimensional product bound with TV(g_n)^2. Endpoint atoms are covered by the jump terms (or their one-sided limits); no assertion of absolute continuity of the sign distribution is made. Thus (H) gives, on the respective good sets,

E g_n(U_theta)=-gamma/2+O(n^(-1/2)log n)+O(n^(-800)),
E[g_n(U_theta)g_n(U_phi)]=gamma^2/4+O(n^(-1/2)log^2 n).

Here integral_0^infty log x exp(-x)dx=-gamma, and deleting the exponential tails below v_n and above n costs O(v_n |log v_n|+exp(-n)log n)=O(n^(-800)); squaring the expectation only alters the same negligible order. The independent exponential comparison factorizes exactly.

On the excluded sets, |g_n|<=C log n deterministically, so their contributions are O(h_n log n) in the first moment and O(h_n log^2 n) in the second. The limiting constant's contribution over these sets has the same or smaller error. Adding the tail bounds proves precisely

E L_r=-gamma/2+O(n^(-1/2)log^2 n),
E L_r^2=gamma^2/4+O(n^(-1/2)log^2 n),

uniformly for |r-1|<=n^(-11/10). This verifies the needed analytic input from explicit estimates and two standard, precisely identified background theorems, without assuming the false pointwise Lemma 3.2 or the desired Lemma 1.3.

## 7. Joining the independent analytic proof to the Jensen repair

Let delta=(1/10)n^(-11/10) and use t=log r. For all sufficiently large n, exp(plus or minus delta) belongs to the radial interval just proved. Put J(t)=integral log|P(exp(t+i theta))|dmu and psi(t)=(1/2)log sum_j exp(2jt), so L(t)=J(t)-psi(t).

The weighted variance identity psi''(t)=2 Var_t(j)<= (n-1)^2/2 holds at every real t. Therefore each psi secant over [0,delta] or [-delta,0] differs from (n-1)/2 by <=delta(n-1)^2/4<=n^(9/10)/40. When n^(9/10)>=20 this places it within n^(9/10)/20 of n/2.

Jensen's exact root formula is

J(t)=log|P(0)|+sum_{P(alpha)=0} max{0,t-log|alpha|}.

It holds including roots on the integration circle by angular log integrability. J is convex, its left derivative at zero counts roots in the OPEN disk, and its right derivative additionally counts circle roots. Consequently

[J(0)-J(-delta)]/delta <= N_open <= [J(delta)-J(0)]/delta.

If N_open>=n/2+n^(9/10), then L(delta)-L(0)>=(19/20)delta n^(9/10). If N_open<=n/2-n^(9/10), then L(0)-L(-delta)<=-(19/20)delta n^(9/10). No circle-root probability estimate or reciprocal-polynomial argument is needed.

Each L difference has second moment O(n^(-1/2)log^2 n) by the proven centered moments and (u-v)^2<=2u^2+2v^2 after adding gamma/2 to both. Squared Markov and the union bound give

Pr(|N_open-n/2|>=n^(9/10))
 <=C n^(-1/2)log^2 n / [delta^2 n^(18/10)]
 =O(n^(-1/10)log^2 n) ->0.

This is for every sufficiently large integer n, without a parity restriction. The finitely many smaller n are immaterial to the claimed limit; no all-n numerical bound with an unspecified constant is asserted. For Hayman's exact polynomial H(z)=zP(z), the origin contributes exactly one simple root because P(0)=plus or minus one. The same n signs parametrize all 2^n polynomials, and a uniform tolerance n^(9/10)+1 is o(n). Thus the exact full original assertion follows, with algebraic multiplicity and open disk throughout.

## Scope of this result

The Jensen repair itself is correct. Its previously conditional analytic premise can be supplied by the preceding corrected proof. The source has additional errors that must be disclosed, particularly Lemma 3.2's missing resonance exclusions. The corrected analytic note is newly prepared review material and should be independently read before adopting it in an accounting disposition; no publication, ledger repair, PR correction, or merge is performed here. This does not establish that the inaccessible journal PDF is text-identical to arXiv v2, nor does it claim that any correction is novel or requires a separate publication.
