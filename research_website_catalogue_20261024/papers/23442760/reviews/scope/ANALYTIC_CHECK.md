# Independent full-claim derivation and exact prior interfaces

The early reconstruction was fixed from the entire actual five-page PDF and controlling TeX before historical/current opinions or current target primary passages. This expands that reconstruction after primary-interface checking; it does not replace the theorem by a narrower result.

Let K be a compact convex body in R^n, n>=1, with nonempty interior. Let f be a real polynomial, a any minimizer, H=max_K||Hess f||op, gamma=1+H/2, ell=grad f(a).(x-a), g=ell+gamma||x-a||², G=max_K g. The hierarchy uses globally SOS degree<=2r and integral_K q dx=1. It is not an unnormalized infimum or a positivity certificate restricted to K.

Since every segment from a to x remains in K, the derivative at its minimizing endpoint gives ell>=0. Taylor's integral remainder on that segment gives 0<=f-f(a)<=ell+(H/2)||x-a||²<=g. Thus G is positive and finite and u=g/G is a polynomial of degree at most two with range[0,1]. The added one in gamma handles affine and constant f. No convexity of f, boundary smoothness or semialgebraicity is used. The argument also holds for C² f on an open neighborhood of K, because only its derivatives and quadratic proxy enter the density.

For F(t)=vol{x in K:u(x)<=t} and 0<s<=t, contraction from a by alpha=s/t sends S_t into S_s: g(a+alpha(x-a))=alpha ell+alpha²gamma||x-a||²<=alpha g(x). The Jacobian is alpha^n. Consequently F(t)<=(t/s)^n F(s), also for t>1; F(h)>=h^n vol(K)>0. The direction is important: the tail mass is bounded relative to the same core mass, not only to total volume. No density or differentiability of F is assumed.

For m>=1 put N=2m+1 and A_m(t)=[1+2sum_{j=1}^m T_j(1-2t)]/N. It has degree m, A_m(0)=1. Substituting v=asin sqrt(t), the finite Dirichlet identity gives A_m(t)=sin(Nv)/(N sqrt(t)). The polynomial sum bounds its absolute value by1; the quotient gives the bound1/(N sqrt(t)). With h=N^-2, convexity of arcsin places it below its endpoint chord, so Nv<=pi/2 on[0,h]. Then sin(Nv)>=2Nv/pi and v>=sqrt(t) give A_m>=2/pi there, including zero by continuity.

Choose L=n+2 and Q=A_m(u)^(2L), the square of A_m(u)^L globally on R^n. Its normalization Z is at least (2/pi)^(2L)F(h), and Q<=min{1,(h/u)^L} on K. The core contributes at most hF(h) to integral uQ. Shell 2^j h<u<=2^(j+1)h contributes at most

    2^(j+1)h * 2^(-jL) * F(2^(j+1)h)
    <= hF(h) 2^(n+1) 2^{j(n+1-L)}.

The series sums to2 because L=n+2. The outer shell is justified even when its top exceeds1 by the same contraction inequality. Thus the numerator is at most hF(h)(1+2^(n+2)); division cancels exactly F(h), yielding

    integral uQ / integral Q
    <= (pi/2)^(2L)(1+2^(n+2))/(2m+1)^2.

Oscillation and zeros off the core do not affect the positive normalization; no mass outside a local simplex is discarded. For r>=2L, m=floor(r/(2L)) gives deg(A_m(u)^L)<=2mL<=r and deg Q<=2r. N>=r/(2L) gives C_n=4L²(pi/2)^(2L)(1+2^(n+2)). For1<=r<2L, constant density has error<=G and C_n/r²>=1. This proves the literal explicit bound for every integer r>=1 with one global square. The lower inequality follows from nonnegativity and unit mass.

For the claimed sharpness, shifted Legendre orthonormal polynomials l_j satisfy sum_{j=0}^r l_j(t)²<=sum(2j+1)=(r+1)²=M. Cauchy-Schwarz gives p(t)²<=M integral p² for each degree<=r p. Summing any SOS representation with unit integral gives q<=M. At most one half of its mass lies below alpha=1/(2M), so integral t q>=alpha/2=1/(4M). For the product body, apply the same bound at each fixed y then integrate y, giving a marginal with mass1 and boundM, with no extra volume factor. Classical Rodrigues/Legendre identities and the finite complex-integral representation supply the indicated orthogonality and supremum bound. The claim is a worst-case instance in each dimension; constant objectives have zero error. There is no universal positive lower rate for each f.

The exact source interfaces check from actual primary bodies. Laurent's entire OWR contribution, printed2991-2993, states the general convex-body convergence question and contextualizes probability measures. Its displayed equations(3)-(4) actually leave the normalization integral without an equality/value. The paper explicitly supplies unit mass. Slot-Laurent arXiv1905.08142v2 Eq(3) supplies the full normalized hierarchy; Theorem11 states O(log²r/r²) for convex bodies, and the final questions at PDF29 explicitly ask whether the logarithm can be removed. Their Lemmas1/4 already prove the constrained-gradient and quadratic-proxy reductions. De Klerk-Laurent arXiv1703.00744v1 Corollary4.3 and its complete proof at PDF7-8 also use the quadratic proxy. No originality belongs to these reductions here. De Klerk-Laurent arXiv1804.05524v1 Theorem3.1/Corollaries3.2-3.3 already establish matching interval/Jacobi and product-box lower rates. The coarse1/4 constant is proved here, not misrepresented as their literal printed constant.

The manuscript's positive older-ingredient consequence from Totik-Varga Theorem2.1 checks independently. Its hypotheses admit psi(v)=sqrt(v): it is increasing, has fixed doubling factor sqrt2, psi(0+)=0, and integral_1^infinity psi(v)/v² dv=2. With endpoint parameter a=0 the actual estimate becomes |P_m(t)|<=A exp[-c(m²t)^(1/4)], while P_m(0)=1, deg<=m and sup_[0,1]|P_m|<=2. Classical Markov on[0,1] gives ||P_m'||<=4m²; hence P_m>=1/2 on h=1/(8m²). Let Q=P_m(u)². Its denominator is at least F(h)/4; the core numerator is at most4hF(h). On dyadic shells the numerator is bounded by hF(h) times a fixed multiple of

    sum_{j>=0} 2^{j(n+1)} exp[-c'2^{j/4}],

which converges for every fixed n. The same mass cancellation gives O(m^-2), with deg Q<=4m, so m=floor(r/2) for r>=2 and constant-density fallback at r=1 prove the same upper-rate theorem from those older ingredients. This is a deduction checked now, not documentary evidence that an older source printed the complete target theorem. Totik-Varga's actual Christoffel proof at publishedpp383-385 compares shell integrals with the same local core mass; broad relative shell/core mechanisms receive prior credit.

The final Laurent-Slot2026 overview at actualPDF10-11/printed158-159 still lists the logarithmic rate for general convex bodies and quadratic rates for special bodies. This confirms the contents of that source, not worldwide openness or first discovery. Bounded current searches do not overcome incomplete indexing or unread predecessor bodies. No new-method or firstness certification is supplied.

No central gap is identified in the full main theorem, C² extension or stated worst-case proposition. Arbitrary measures, original-objective-only pushforward densities for general nonconvex f, empty-interior bodies, nonconvex bodies, efficient minimizer computation, exact asymptotic constants or sharp dimension dependence remain outside these claims. The finite exact diagnostics corroborate selected identities and moments, not the universal theorem.
