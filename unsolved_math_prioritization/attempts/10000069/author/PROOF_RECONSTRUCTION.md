# Reconstruction of the credited characterization

This is an independently written verification of the mathematical claims in the external DannyExperiments manuscript identified in MODEL_AND_STATUS.md. The spectral result is credited to that public manuscript. The argument below is not a claim of a new result. All integrals are over (0,1); functions are identified almost everywhere.

## 1. Laws, means and Jensen domination

Fix 1/2<p<1 and put q=1-p. For an integrable nonnegative decreasing function f, take independent uniform U,V and Bernoulli(p) B. Let T f be the decreasing quantile of the law of

B(f(U)+f(V))+(1-B)min(f(U),f(V)).

Quantiles exist for every such law. Write M(f)=integral f. Monotone coupling shows that T preserves order; scaling the coupled variables shows positive homogeneity. For coupled inputs f,g, addition and minimum each satisfy the two-coordinate Lipschitz bound. Consequently the coupled expected absolute output difference is at most 2||f-g||_1. The quantile coupling minimizes expected absolute difference in one dimension, so ||Tf-Tg||_1<=2||f-g||_1.

Let m_n=M(T^n 1). For a fixed binary tree of n levels with fixed series/parallel choices, the value at its root as a function of its leaf lengths is nonnegative, increasing, homogeneous and concave. This follows by induction: sum preserves concavity, and the pointwise minimum of concave functions is concave, as can also be seen by intersecting their convex hypographs. Jensen therefore bounds the expected value with iid mean-one leaves by its value with all leaves equal to one. Averaging over all gate choices proves

M(T^n f)<=m_n whenever M(f)=1.                                   (1)

Take f=T^k1/m_k and use homogeneity to obtain m_(n+k)<=m_n m_k. Since 1<=D_n<=2^n, the logarithms are finite. Fekete's lemma gives

rho=lim m_n^(1/n)=inf_(n>=1) m_n^(1/n), delta=log rho.

The one-step mean obeys 2p M(f)<=M(Tf)<=(1+p)M(f), hence 2p<=rho<=1+p.

## 2. A closed compact domain

Put R=1/(2p-1). Define K to be all nonnegative decreasing f with M(f)=1 and S(f)=integral f^2<=R. The constant function belongs to K; K is convex.

For general decreasing f in L^2 define A(f)=2 integral u f(u)du and C(f)=2 integral u f(u)^2 du. These are the first and second moments of min(f(U),f(V)): max(U,V) has density 2u. Direct calculation for M(f)=1 yields

d(f):=M(Tf)=2p+q A(f),
S(Tf)=2p S(f)+2p+q C(f).

The following identity establishes the essential estimate without a distributional assumption beyond decreasing f:

A(f)S(f)-C(f)M(f)
 = integral integral (u-v)f(u)f(v)(f(v)-f(u))du dv >=0.             (2)

The sign is nonnegative for each pair u,v. All four expanded terms are integrable because f is in L^1 and L^2; expansion and Fubini justify the equality. Thus C(f)<=A(f)S(f) on K. Since 0<=A(f)<=1 and d(f)>=2p,

S(Tf/d(f)) <= S(f)/d(f)+2p/d(f)^2
            <= (S(f)+1)/(2p) <= R.                             (3)

Therefore N(f)=Tf/d(f) maps K continuously into itself. In particular E D_n^2/(E D_n)^2<=R for every n.

To prove compactness, decreasing mean-one functions satisfy f(u)<=1/u. On each interval [eta,1), Helly selection supplies a subsequence converging at all continuity points of a monotone limit. A diagonal choice as eta decreases gives almost-everywhere convergence on (0,1). The uniform L^2 bound supplies uniform integrability through integral_E f<=sqrt(R |E|). Vitali's theorem gives L^1 convergence. Nonnegativity and monotonicity persist, the mean remains one, and Fatou preserves the L^2 bound. Thus the limit lies in K. Sequential compactness in the metric L^1 topology is compactness.

## 3. An eigenfunction at the actual growth rate

For epsilon>0 let T_e f=Tf+epsilon M(f)1 and normalize it to N_e f=T_e f/M(T_e f). This map is order-preserving before normalization, positively homogeneous, and continuous. If a variable with first moment m>0 and second moment s is increased by a constant c>=0, its normalized second moment cannot increase: after clearing positive denominators the required inequality is c(2m+c)(s-m^2)>=0. Apply this with m=d(f), c=epsilon to (3); N_e is a continuous self-map of compact convex K.

Schauder's fixed-point theorem gives f_e in K and lambda_e=d(f_e)+epsilon such that

Tf_e+epsilon 1=lambda_e f_e.

In particular f_e>=epsilon/lambda_e=:c_e>0. Since T_e>=T and both are monotone, induction gives

lambda_e^n f_e=T_e^n f_e>=c_e T^n 1.

Integrate and let n tend to infinity to get lambda_e>=rho. Also 2p+epsilon<=lambda_e<=1+p+epsilon. Along epsilon_j decreasing to zero compactness gives f_ej ->f in L^1; the bounded scalars admit a convergent subsequence. Passing to the eigen-equation using continuity of T yields Tf=lambda f and lambda>=rho. But (1) gives lambda^n=M(T^n f)<=m_n for every n, so lambda<=rho. Thus lambda=rho and an eigenfunction f in K exists at the true growth rate.

For any other mean-one, nonnegative, integrable decreasing eigenfunction g, (1) gives its eigenvalue at most rho, even if g is not in K. Thus rho is the maximal eigenvalue in that admissible class. No uniqueness follows.

## 4. Exact lower and upper formulas

If f in K satisfies Tf>=a f for a>=0, then induction and (1) imply a^n<=m_n. Thus a<=rho, with equality attained by the eigenfunction above. Hence

rho=max {a>=0: there is f in K with Tf>=a f}.

If f in K has essential infimum at least c>0 and Tf<=b f, then c T^n1<=T^n f<=b^n f. Integration gives rho<=b. Conversely the perturbed functions from section 3 satisfy Tf_e<=lambda_e f_e and have positive essential infimum. Every subsequential limit of lambda_e as epsilon decreases is rho by that section's argument; boundedness then implies convergence of the whole family of eigenvalues, regardless of the fixed-point selection. Therefore

rho=inf {b>0: there is f in K with ess inf f>0 and Tf<=b f}.

The upper infimum need not be attained by a function bounded away from zero. The lower maximum is attained. The definitions use only p and the explicit operator, not an unknown value of delta.

## 5. Optional invariant-measure form

Let I be the N-invariant Borel probability measures on compact metric K and h(f)=log d(f), a continuous bounded function. The eigenfunction gives a fixed point of N and a Dirac measure with integral h=log rho. For any Pi in I,

n integral h dPi=integral log M(T^n f)dPi<=log m_n

by telescoping the normalizations, invariance, and (1). Divide by n and pass to the limit. Consequently delta=max_(Pi in I) integral h dPi. This does not say that every maximizing measure is supported on fixed points.

## 6. Endpoints and shape consequences

For p<=r, use the same uniform gate marks at every vertex of every finite binary tree. Changing a min gate into a sum gate only increases its output for nonnegative leaves. Hence D_n(p)<=D_n(r) in this coupling and delta is nondecreasing. The published Chen-Derrida-Duquesne-Shi Theorem 1 states delta(1/2+epsilon)~(pi/sqrt(6))sqrt(epsilon). Since delta>=0, monotonicity squeezes delta(1/2) to zero. This use of their theorem is explicit; its long proof is not re-proved here. At p=1, induction gives D_n=2^n.

The external canonical proof also observes the following right-end estimate. For its mean-one eigenlaw X with E X^2<=R, independent X,Y satisfy

E min(X,Y)=1-(1/2)E|X-Y|>=1-sqrt((R-1)/2).

This follows by Cauchy-Schwarz and E(X-Y)^2=2(R-1). Taking the mean in the eigen-equation therefore gives

1+p-(1-p)^(3/2)/sqrt(2p-1)<=rho<=1+p.

As p increases to one, logarithmic expansion yields delta(p)=log 2-(1-p)/2+O((1-p)^(3/2)). This estimate, too, is credited rather than presented as new.

## 7. Exact boundaries of the reconstruction

The proof is for the exponent of an expectation. Neither the normalized-moment estimate nor existence of an eigenlaw identifies the limiting law of the actual normalized sequence. Neither proves convergence of n^-1 log D_n at every interior parameter. The cited published article explicitly separates that issue. Nothing above concerns uniform random SP graphs, graph diameter or effective resistance. K ceases to have its stated finite bound at p=1/2; the Schauder argument cannot be applied there by substituting that value. Finite exact checks accompanying this document are error controls only, not a replacement for any of these universal arguments.
