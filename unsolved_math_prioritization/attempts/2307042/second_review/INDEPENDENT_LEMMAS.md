# Independent analytic verification of the annular example

This is a fresh derivation for Problem 2307042, written without consulting any first audit. It verifies the frozen author's theorem; it does not modify the frozen submission. All formulas and reasoning below are authored mathematics, not extracts from third-party sources.

## 1. Domain, normalization, and the relevant assertion

Let D = {z : 1 < |z| < e}, let a = exp(1/2), and let xi = -1. In the cylinder coordinates z = exp(x + iy), take 0 < x < 1 and y modulo 2 pi. The base is A = (1/2,0), and xi is represented by (0,pi). The cylinder and annulus have the same positive harmonic functions under this change of coordinates. Define H_a(z) as the supremum of h(z) over all positive harmonic h on D with h(a) <= 1. Local Harnack inequalities, joined by a finite chain of interior discs, show this supremum is finite at each fixed interior point. In particular H_a(a) = 1.

We will identify a normalized minimal Martin kernel K at xi and prove that K < H_a throughout a punctured neighborhood of a. This excludes equality on every nontrivial curve approaching a, and hence excludes equality throughout a Green line issuing from a. No calculation of individual Green trajectories is necessary.

## 2. Strip Green function and boundary density

Use w = y + ix in the strip S = {0 < Im(w) < 1}. Interchanging these two coordinates is an isometry, so the use of w instead of x + iy does not change harmonicity. The holomorphic map F(w) = exp(pi w) maps S bijectively to the upper half-plane. Pulling back its logarithmically normalized Green function gives

    g_S(y+ix, eta+is)
      = log |(exp(pi(y+ix)) - exp(pi(eta-is)))
                / (exp(pi(y+ix)) - exp(pi(eta+is)))|
      = (1/2) log [(cosh(pi(y-eta)) - cos(pi(x+s)))
                     / (cosh(pi(y-eta)) - cos(pi(x-s)))].

For 0 < x,s < 1 this is positive: the numerator minus the denominator inside the last ratio is 2 sin(pi x) sin(pi s) > 0. It vanishes for x = 0 and x = 1, is harmonic away from the pole, and has singularity -log|w-w'| plus a harmonic function.

The upper-half-plane Poisson density at a real boundary coordinate r is Im(F(w))/(pi |F(w)-r|^2). Set r = exp(pi eta), and use dr = pi exp(pi eta) d eta. The resulting density at the lower side of S, relative to d eta, is

    p(x,y-eta) = sin(pi x) / [2(cosh(pi(y-eta)) - cos(pi x))].

This also follows by directly differentiating the displayed Green function:

    (partial/partial s) g_S(y+ix,eta+is)|_(s=0)
       = pi sin(pi x)/(cosh(pi(y-eta))-cos(pi x))
       = 2 pi p(x,y-eta).

Thus the factor 2 pi is correct for the logarithmic Green normalization. It cancels in the normalized Martin ratio.

## 3. Periodization, convergence, and identification of the Martin limit

Set

    g_C(w,w') = sum_(k in Z) g_S(w,w'+2 pi k),
    P_eta(x,y) = sum_(k in Z) p(x,y-eta+2 pi k),
    P = P_pi.

For horizontal separation T, cosh(pi T) is bounded below by (1/2) exp(pi|T|). From the explicit formulas, the tails of g_S, p, and each fixed finite order derivative are bounded by a constant times exp(-pi|T|). On a fixed compact set of first-variable interior points, second-variable boundary parameters eta near pi, and 0 <= s <= s_0 sufficiently small, all these tail constants can be chosen uniformly. The finitely many remaining terms have denominators bounded away from zero when the first variable stays away from the pole. The Weierstrass test therefore gives local uniform convergence with the required derivatives, including second-variable derivatives at s = 0.

The sum g_C is periodic in both horizontal coordinates modulo 2 pi, positive, zero on both boundary circles, and has exactly one logarithmic pole on the quotient cylinder. To see the last point, work in any local lift of the pole: exactly one summand is singular, with coefficient one, and every other summand is smooth. The difference from the Dirichlet Green function is harmonic after removing the canceled singularity and zero on the compact cylinder boundary, so the maximum principle gives equality. Alternatively these properties themselves characterize that Green function.

Uniform differentiation at the lower boundary gives

    g_C(w,eta+is) = 2 pi s P_eta(w) + O(s^2)

locally uniformly for interior w and uniformly for eta near pi. At A, P_pi(A) > 0 because every term is positive. Therefore, as s decreases to zero and eta tends to pi in any manner,

    g_C(w,eta+is)/g_C(A,eta+is) -> P_pi(w)/P_pi(A) =: K(w)

locally uniformly in the interior. This is a Martin boundary limit for approach to xi. Tangential approaches cause no loss: both numerator and denominator have their common factor s, and the normal derivative at A remains bounded away from zero near eta = pi.

## 4. Minimality without a boundary representation theorem

The series P is positive. It extends smoothly to zero on the cylinder boundary away from xi. Near xi write t = y - pi and r^2 = x^2+t^2. The term with boundary separation t satisfies

    p(x,t) = x/(pi r^2) + O(x).

Indeed sin(pi x) = pi x(1+O(x^2)) and
2(cosh(pi t)-cos(pi x)) = pi^2 r^2(1+O(r^2)), uniformly in angle. The other periodized summands are smooth across x = 0 and vanish there, so their sum is O(x) uniformly. Hence

    P(x,pi+t) = x/(pi r^2) + O(x).                         (M1)

Suppose v is harmonic and 0 <= v <= P. The squeeze theorem gives its continuous zero boundary values away from xi. Odd reflection across the flat side x = 0 is therefore harmonic in a punctured disc. Domination and (M1) give absolute size O(1/r) for this reflected function.

For completeness, a single-valued real harmonic function U on a punctured disc has a radial constant/logarithmic part and Fourier terms r^n and r^(-n) times cos(n theta) and sin(n theta), for n >= 1. This follows by taking its circle Fourier coefficients and solving the radial Laplace equation. If |U| <= C/r, then each Fourier coefficient has that same bound; letting r decrease to zero forces the coefficients of r^(-n) to vanish for n >= 2. Reflection x -> -x sends theta -> pi-theta. Oddness removes the constant/logarithmic radial part and the singular tangential term t/r^2. The only allowed singularity is A_0 x/r^2. The remaining positive-power Fourier series is harmonic across the origin and odd in x. Consequently

    v(x,pi+t) = A_0 x/r^2 + v_0(x,t),                    (M2)

where v_0 is harmonic across zero and odd in x. Along t = 0, multiply 0 <= v <= P by x and let x decrease to zero. Equations (M1)-(M2) give 0 <= A_0 <= 1/pi.

The harmonic function v - pi A_0 P has its dipole canceled. Near xi it is v_0 + O(x), which tends uniformly to zero, since the odd regular function v_0 vanishes at the origin. At every other boundary point it also tends to zero. It thus extends continuously to the compact annular closure with boundary value zero. Apply the maximum principle to it and its negative to obtain v = pi A_0 P. Every nonnegative harmonic minorant of P is a constant multiple, proving minimality. The normalized function K is therefore an admissible minimal Martin kernel, with K(A)=1.

## 5. Exact derivative calculation and non-numerical bounds

Put q_k = sech((2k-1)pi^2), S_1 = sum q_k, and S_2 = sum q_k^2. These positive sums converge exponentially. At A, each denominator in p has cos(pi x)=0. Direct differentiation, justified above, gives

    P(A) = S_1/2,
    P_x(A) = -pi S_2/2,
    P_y(A) = 0.

For the final identity pair k and 1-k, whose horizontal arguments are negatives; p_y is odd in that argument. Consequently

    grad K(A) = (-c,0),   c = pi S_2/S_1 > 0.

Since q_k <= sech(pi^2), the ratio S_2/S_1 is a convex weighted mean of the q_k. Thus c <= pi sech(pi^2). The elementary bounds 3 < pi < 4 and cosh u > 1+u^2/2 at u=pi^2 give

    cosh(pi^2) > 83/2,
    0 < c < 8/83 < 1/10.

This is an all-terms argument. It does not assume a truncation error, a floating-point identity, or an angular sampling result.

## 6. Global competitors and a uniform directional margin

Let b = 1/(2 cosh(1/2)) and define

    h_1 = 1+(x-1/2),      h_2 = 1-(x-1/2),
    h_3 = 1+b sin(y) cosh(x-1/2),
    h_4 = 1-b sin(y) cosh(x-1/2).

All four are periodic and single-valued on D. Their Laplacians vanish. The first pair has values strictly between 1/2 and 3/2. For the second pair, |b sin(y) cosh(x-1/2)| <= 1/2, so they are positive as well. All have value one at A and are admissible competitors for H_a. Their gradients at A are respectively (1,0), (-1,0), (0,b), (0,-b).

The series for cosh gives cosh(1/2) <= sum_(n>=0)(1/4)^n = 4/3 < 2, hence b > 1/4. For an arbitrary nonzero displacement d=(u,v), let rho=|d| and M=max(|u|,b|v|). The maximal first-order improvement over K is exactly

    max_j [grad h_j(A)-grad K(A)] dot d = M+cu.

Since |u| <= M, this is at least (1-c)M. Also rho^2 <= M^2(1+b^(-2)) < 17 M^2 < 25 M^2, so M > rho/5. We obtain the independent bound

    max_j [grad h_j(A)-grad K(A)] dot d
       > (75/83)(rho/5) = (15/83)rho > rho/10.          (G1)

This slightly strengthens the author's margin while using the same four competitors. It holds for all directions, including directions depending on rho. The maximizing index may vary with direction; taking the finite maximum is legitimate and does not require the envelope to be differentiable.

## 7. Uniform remainder and the conclusion

Choose r_0 < 1/4 so that the closed coordinate disc of radius r_0 around A lies in one interior cylinder chart. For f_j=h_j-K, set

    B = max_(1<=j<=4) sup_(|d|<=r_0) ||D^2 f_j(A+d)||_op,
    C = max(1,B/2).

Smoothness and compactness give B<infinity. Taylor's integral formula, with f_j(A)=0, gives

    |f_j(A+d)-grad f_j(A) dot d| <= C rho^2

for all j simultaneously and every |d|<=r_0. Combining with (G1), for
0<rho<min(r_0,1/(20C)) one has

    max_j h_j(A+d)-K(A+d) > rho/10-C rho^2 > rho/20 > 0.

Since H_a is at least each h_j, K<H_a throughout this punctured disc, hence throughout a punctured annular neighborhood of a. Equality at a is retained. Every nontrivial curve issuing from a has non-base points arbitrarily close to a, so equality throughout such a curve is impossible. The annulus is bounded, smooth, doubly connected, and a Green domain. One minimal Martin kernel failing the universal property suffices for the negative answer under the primary statement's equality-along-the-line meaning.

## Verification boundary

The proof is analytic and self-contained apart from elementary harmonic reflection, Fourier expansion, the maximum principle, and the conformal invariance of two-dimensional harmonic/Green functions. No numerical grid establishes any claim. This verifies the submitted counterexample, not historical novelty, publication status, current global openness, or formal proof-assistant certification. It makes no assertion about isolated contact farther from a.
