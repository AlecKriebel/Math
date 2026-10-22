# Half-strip sewing: verified partial results and exact unresolved question

Problem 2306063 / AMR-022-6063, rank 585. Written 2026-10-04.

**Disposition: unsolved, five substantive approach families. No full affirmative or negative resolution is claimed.** The results below are restricted theorems, explicit controls, and obstructions to proposed proof routes. No novelty claim is made for the classical special cases or the extremal-length method.

## 0. Target, type, and the essential quantifier

Let H = {x+iy : x>0, 0<=y<=1}. An increasing homeomorphism alpha from (0,infinity) onto (alpha(0),infinity), with alpha(0)>=0, identifies the lower point x with the upper point alpha(x)+i. Assume this identification is a conformal sewing and its resulting end at infinity is hyperbolic. The question is whether some continuous function epsilon:(0,infinity)->(0,infinity) makes every admissible sewing beta with

    |beta(x)-alpha(x)| < epsilon(x), for every x>0,

hyperbolic as well. This is openness in the fine C0 topology, relative to admissible sewings. Epsilon is a function and may decrease arbitrarily rapidly at either endpoint. A single constant tolerance, compact-open convergence, C1 perturbations, and uniformly quasiconformal perturbations are different questions.

The recovered prior desk report replaced this function by a constant epsilon. We do not use that abbreviated target. The primary problem and update were checked in Hayman–Lingham, arXiv:1809.07200v2, printed pp.140–141; the 2018 update reports no progress. A 1977 original problem listing was also identified. This search does not establish that no later solution exists.

An annular end is parabolic if its missing endpoint is conformally a puncture, and hyperbolic if it is a nondegenerate boundary component of a finite-modulus annulus. This is the meaning of hyperbolic **end**, not merely existence of a hyperbolic metric on the whole surface. Removing or attaching a compact collar does not change end type.

For arbitrary nonregular weldings, existence and uniqueness of a compatible conformal structure must not be assumed. In the explicit examples and comparison theorems below, locally bi-Lipschitz or analytic boundary identifications give the standard locally quasiconformal sewing and locally quasicircular, removable seams. Those are explicit extra hypotheses, not restrictions silently imposed on the original problem.

## 1. Approach 1: exact affine uniformization

### Theorem 1

For alpha(x)=a x+b with a>0 and b>=0, the end is hyperbolic exactly when a!=1. The end is parabolic when a=1, including b=0.

### Proof: translation case

Put d=b+i and

    Q(z)=exp(2 pi i z/d).

The sewing is the restriction of T(z)=z+d, and Q(Tz)=Q(z). Since Q' is nonzero, Q is locally conformal. If Q(z1)=Q(z2), then z1-z2=n d for an integer n. In the open strip, the imaginary difference has absolute value less than one, so n=0. Boundary identifications are precisely the n=+/-1 possibilities. Thus Q is injective on the sewn quotient.

Moreover

    log|Q(x+iy)| = 2 pi (x-b y)/(1+b^2).

Every sufficiently large value of |Q| has a preimage in the strip: choose a logarithm, then add an integral multiple of d to the resulting z so that 0<=Im z<1. The displayed formula ensures Re z>0 once |Q| is large. Consequently a neighborhood of the end is an exterior disk, hence a punctured disk after inversion. It is parabolic.

### Proof: dilation case

Assume a!=1 and set

    c=(b+i)/(a-1),    w=z+c,    L=log a.

The sewing is the restriction of T(z)=a z+b+i. The identity

    T(z)+c = a(z+c)

shows that, on a sufficiently far-right tail where a single branch of Log is available,

    Q(z)=exp(2 pi i Log(z+c)/L)

descends across the sewing. Its derivative is nonzero there.

For a>1, the shifted strip has imaginary heights h0=1/(a-1) and h1=a/(a-1). Fix a small positive angle theta. The intersection of the ray arg w=theta with the strip has radial endpoints h0/sin theta and h1/sin theta. Their ratio is a. For theta sufficiently small the whole segment lies to the right of the original finite boundary. In Log coordinates it is an interval of length L, and the sewing identifies its endpoints by translation by L. Thus Q maps that quotient segment once onto the circle of radius exp(-2 pi theta/L). Letting 0<theta<theta0 gives precisely an annulus

    exp(-2 pi theta0/L) < |Q| < 1.

For 0<a<1, both heights are negative. Use theta<0 close to zero. The radial ratio is 1/a, the interval length is |L|, and the endpoint identification is still multiplication by a, or translation by L. Since theta/L>0, the same argument gives a finite annulus with outer radius 1. In both cases x->infinity corresponds to theta->0 and |Q|->1. This proves hyperbolicity. The real shift b/(a-1) only changes the finite cutoff. QED.

### Consequence and gap

Hyperbolicity is open inside the affine parameter family: if a!=1 and |a'-a|<|a-1|/2, then a'!=1. This does not establish a neighborhood among arbitrary homeomorphic sewings. The scalar family is a calibration of conventions, not a solution of the target.

## 2. Approach 2: quasiconformal transport, and a fine-C0 obstruction

### Theorem 2: an explicit sufficient comparison

Assume alpha and beta are locally bi-Lipschitz homeomorphisms of (0,infinity) onto itself, with limits zero at zero. Set h=beta composed with alpha^{-1}. Suppose h is locally absolutely continuous and, almost everywhere,

    0<m<=h'(x)<=M<infinity,       |h(x)-x|<=B<infinity.

Their standard sewn surfaces have the same end type.

### Proof

On the closed strip define

    F(x,y)=((1-y)x+y h(x), y).

For each y, the first coordinate is an increasing homeomorphism of (0,infinity) onto itself. Thus F is a proper homeomorphism preserving the end. On the bottom it is the identity; on the top it is h. Since h(alpha(x))=beta(x), it respects precisely the source and target seam identifications.

At almost every point its derivative is

    DF = [[p,q],[0,1]],
    p=1-y+y h'(x),   q=h(x)-x.

Write m0=min(1,m), M0=max(1,M). Then det DF=p>=m0 and the squared Frobenius norm is at most M0^2+B^2+1. The ratio of singular values, equal to the squared largest singular value divided by the determinant, is therefore at most

    K0=(M0^2+B^2+1)/m0.

So F is uniformly quasiconformal in the open strip. The sewing assumptions ensure that locally the two seam arcs are quasicircular. The descended continuous homeomorphism is quasiconformal across them: straighten a local quasicircle quasiconformally, use the ACL gluing theorem across a line, and then use that the exceptional seam has area zero to retain the almost-everywhere K0 bound. This argument requires the stated regular sewing class.

Finally a K-quasiconformal homeomorphism distorts extremal length by a factor between 1/K and K. To recall why, transport a test metric using the largest singular value, apply the area formula and the singular-value bound, and then apply the same argument to the inverse. For an annular end, the extremal length of essential separating loops is the reciprocal of its modulus, with value zero when the modulus is infinite. Hence a finite K preserves the distinction between finite and infinite modulus. QED.

### Lemma 2A: every fine C0 neighborhood permits unbounded local distortion

Fix alpha(x)=a x with a>0, and any continuous positive epsilon. There is a locally bi-Lipschitz homeomorphism beta:(0,infinity)->(0,infinity) in that neighborhood such that the relative map h=beta composed with alpha^{-1} has no uniform adjacent-interval quasisymmetry bound. The particular interpolation F above has unbounded quasiconformal distortion.

Choose t_n=3n. Put

    eta_n=min{epsilon(u): (t_n-1)/a <= u <= (t_n+1)/a}>0,
    0<ell_n<min(1/4,eta_n/2),     s_n=2^{-n}.

On I_n=[t_n-ell_n,t_n+ell_n], let h fix both endpoints and be piecewise affine with slope s_n on the left half and 2-s_n on the right half. Let h be the identity elsewhere. The intervals are disjoint and locally finite. All slopes on every compact subinterval have finite positive bounds; h is therefore locally bi-Lipschitz and strictly increasing. It fixes zero in the limiting sense and is onto because its displacement is bounded.

For u in I_n, |h(u)-u|<ell_n. With beta(x)=h(a x), the corresponding x lies in the compact interval defining eta_n, so

    |beta(x)-alpha(x)| < ell_n < epsilon(x).

Off those intervals the error is zero. But the ratio of images of equal adjacent halves is

    [h(t_n+ell_n)-h(t_n)]/[h(t_n)-h(t_n-ell_n)]
      =(2-s_n)/s_n -> infinity.

Moreover, in the left half of I_n and for 1-s_n<y<1, the interpolation matrix has p<=2s_n. Its largest singular value is at least one, so its singular-value ratio is at least 1/(2s_n). Each such region has positive area. Thus the essential supremum of its distortion is infinite. QED.

The lemma supplies actual locally regular admissible sewings, but **makes no claim that their ends have changed type**. It proves that a fine C0 bound alone cannot furnish the uniform derivative or interpolation-distortion bounds used in Theorem 2. It does not exclude a different comparison mechanism.

## 3. Approach 3: invariant one-forms and an expanding derivative criterion

This is a restricted reconstruction of the classical extremal-length mechanism in Jenkins, *On a Type Problem* (1959), not a new general type criterion.

### Theorem 3

Let f be real analytic on a tail [c,infinity), with f(c)>c, and f'(x)>=lambda>1 there. Sew the height-one half-strip over that tail by x~f(x)+i. The end is hyperbolic.

More generally, the same proof works for a smooth sewing whose local conformal charts and inverse maps extend C1 with nonzero derivatives to the boundary arcs, with f'(x)>0, f(x)>x, f_n(c)->infinity, and a nonnegative smooth q0 supported compactly inside I0=(c,f(c)), normalized by integral q0=1, for which

    E = integral over I0 of q0(t)^2 [sum over n>=0 of 1/f_n'(t)] dt

is finite. Here f_n is the nth iterate and f_0 is the identity. This more general statement retains the explicit C1 chart regularity and positive derivatives; it does not cover every smooth boundary homeomorphism by assumption alone.

### Proof

The orbit intervals I_n=(f_n(c),f_{n+1}(c)) partition the tail. Under the uniform expansion assumption, writing Delta=f(c)-c>0 gives

    f_n(c)-c >= Delta (lambda^n-1)/(lambda-1),

so the endpoints escape to infinity. On I_n define

    q(f_n(t))=q0(t)/f_n'(t),     t in I0.

Since q0 vanishes near the endpoints of I0, q is locally smooth across all orbit endpoints. It satisfies q(f(x))f'(x)=q(x). Define theta(x)=integral from c to x of q(u)du. Each orbit interval has q-mass one, and differentiation, with evaluation at c, gives

    theta(f(x))=theta(x)+1.

The circle-valued function theta(x) modulo integers thus descends to the sewn surface. It has degree one on an essential loop: the finite boundary consists of the vertical edge at c and the top segment from c to f(c), over which theta changes by one. A nearby interior core loop has the same degree.

Let omega=d theta. Locally across each seam this form has a potential: use theta on one side and theta-1 on the other. These traces agree. In the analytic case, and under the explicit C1 chart assumptions of the more general statement, the potentials glue as locally Lipschitz functions. For every piecewise smooth essential core loop gamma,

    absolute integral of omega along gamma >= 1,
    integral along gamma of |omega| >= 1.

The same bound holds for rectifiable loops by the local potential formulation. Thus the conformal norm of omega is an admissible metric for the family of separating loops. The analytic or explicitly C1 seams in this theorem have area zero. Its total area is therefore the sum of its strip-interior integrals. Change variables x=f_n(t) and use Tonelli:

    integral_H |omega|^2 dA
      = sum_n integral_I0 q0(t)^2/f_n'(t) dt
      = E.

For uniform expansion, f_n'(t)>=lambda^n, so

    E <= [lambda/(lambda-1)] integral_I0 q0(t)^2 dt < infinity.

The essential-loop extremal length is at least 1/E>0. Equivalently the annular modulus is at most E, so the end is hyperbolic. QED.

For a simple exact calibration, take f(x)=a x+b with a>1 and I0 of length L0=f(c)-c. The continuous endpoint-vanishing choice q0(t)=6v(1-v)/L0, v=(t-c)/L0, is locally Lipschitz and works by the same argument. It has integral one, square integral 6/(5L0), and

    E=6a/[5 L0 (a-1)].

This is an upper bound on modulus, not an asserted exact modulus.

### Restricted stability and gap

Within real-analytic sewings, if f'>=1+2delta eventually and |g'-f'|<=delta there, then g'>=1+delta eventually. For sufficiently large c also g(c)>c. Theorem 3 proves hyperbolicity of g. This is derivative-controlled stability. The original question permits nonsmooth sewings and gives no bounds on derivatives or on the infinite product defining f_n'. Lemma 2A prevents supplying those bounds merely from an arbitrarily small fine C0 tube.

## 4. Approach 4: parabolic tail surgery and failure of compact-open stability

### Theorem 4

For every a>1 and b>=0, the hyperbolic affine sewing alpha(x)=a x+b is a compact-open limit of locally bi-Lipschitz parabolic sewings.

### Proof

For R>0 define

    beta_R(x)=a x+b                         if x<=R,
              x+(a-1)R+b                  if x>=R.

The two formulas agree at R. The slopes a and one are positive, so beta_R is locally bi-Lipschitz, maps (0,infinity) onto (b,infinity), and admits the standard regular sewing. On the tail it is the translation x->x+c_R with c_R=(a-1)R+b. The translation coordinate from Theorem 1 uniformizes a sufficiently far-out end as a puncture. The finite kink and the finite initial region do not affect this end germ. Thus beta_R is parabolic.

Every compact subset of (0,infinity) lies below R for all sufficiently large R, where beta_R equals alpha exactly. This proves compact-open convergence. QED.

### Why this is not a counterexample to Problem 6.63

For x>R the error is (a-1)(x-R). It is unbounded. In particular the constant fine tolerance epsilon(x)=1 rejects every beta_R somewhere on its tail. A counterexample to the actual question would have to fit **every** continuous positive tolerance at one fixed hyperbolic alpha. Moving a type-changing surgery farther out does not achieve this. Nor does this construction settle even uniform-norm stability.

The proof also establishes a useful limitation on finite-window tests: complete agreement with alpha on an arbitrarily long initial interval does not determine the infinite-end type.

## 5. Approach 5: compactification, singular welding, and the fixed-side obstruction

### Lemma 5A: exact two-sided reduction

Cut the strip along y=1/2 and use w=exp(-2 pi z) on each half. The lower half maps conformally to the lower half of the punctured unit disk, and the upper half to the upper half. The common artificial cut maps to the negative real radius, with the identity identification. The original lower and upper edges map to the positive radius, with identification

    r -> tau_alpha(r)=exp(-2 pi alpha(-log r/(2 pi))),  0<r<1.

All these statements follow by tracking the argument -2 pi y and modulus exp(-2 pi x). The point x=infinity becomes r=0. Thus the end is represented by a real sewing germ with one side fixed:

    Phi(t)=t for t<0,       Phi(t)=tau_alpha(t) for t>0.

Neighborhood sizes on the two sides can differ when alpha(0)>0; this has no effect on the germ at zero. Compatible conformal charts on the original quotient and this cut quotient correspond by the displayed conformal coordinate changes. A compatible sewing which extends across zero gives a punctured, hence parabolic, end. This is an assertion about that compatible sewing; it does not manufacture uniqueness for nonregular maps.

The fine tolerance has an exact transformed form. Put x=-log r/(2 pi). Then

    |beta(x)-alpha(x)|<epsilon(x)

if and only if

    exp(-2 pi epsilon(x))
      < tau_beta(r)/tau_alpha(r)
      < exp(2 pi epsilon(x)).

No uniform or additive tolerance at zero may be substituted for these variable relative bounds.

### Lemma 5B: fine approximation of the positive side by log-singular maps

For alpha(x)=a x, a>0, tau_alpha(r)=r^a. For every prescribed fine tolerance there is an increasing homeomorphism tau_tilde:(0,1)->(0,1), extending to fix 0 and 1, that fits the transformed tube and is log-singular on (0,1). This lemma is about homeomorphisms, not yet coherent admissible sewing surfaces.

Here log-singular means that some Borel E has logarithmic capacity zero and tau_tilde((0,1) minus E) also has capacity zero. We use the published existence of a log-singular increasing homeomorphism between any two compact nondegenerate intervals, as constructed in Bishop (2007), Remark 9; affine changes preserve capacity-zero sets.

To prove the fine approximation claim, let tau(r)=r^a and put

    delta(r)=tau(r) min(1-exp(-2 pi epsilon(x)),
                       exp(2 pi epsilon(x))-1)/2 >0.

This is continuous and positive on (0,1). Take a locally finite partition into closed intervals with endpoints accumulating only at 0 and 1, refined sufficiently that on every partition interval J,

    oscillation_J tau < inf_J delta.

Such a partition is obtained by finite refinements on a compact exhaustion of (0,1), using uniform continuity of tau and positivity of delta. On each J, choose an increasing log-singular homeomorphism onto the interval between tau's endpoint values. Glue them at endpoints. Any increasing endpoint-preserving choice remains between those endpoint values, so its difference from tau is less than delta throughout J. Therefore the glued map fits the required tube. Its endpoint limits are zero and one by monotonicity and the partition values. Countable unions of capacity-zero sets have capacity zero; include the countable partition endpoints as well. The resulting map is log-singular on the positive side. QED.

### Lemma 5C: why the direct Bishop theorem does not finish the route

Extend any such positive-side map by the identity on a negative interval. The resulting two-sided map Phi is **not** log-singular on any interval about zero. Indeed choose a compact negative subinterval J. If E has capacity zero, J minus E still has positive capacity; otherwise J, a union of two capacity-zero sets, would have zero capacity. But Phi fixes J minus E, so Phi(domain minus E) has positive capacity. This contradicts the defining condition of log-singularity. QED.

Bishop's theorem that log-singular circle homeomorphisms are weldings therefore cannot be applied directly after the strip compactification. It requires singularity on the entire circle, while this reduction fixes a nondegenerate negative interval. The approximation in Lemma 5B has not been shown to admit a coherent compatible sewing through zero; even local sewing existence cannot simply be patched through a nonunique seam. It is not a counterexample.

Huber's 1986 paper gives fine approximations that force a **hyperbolic** singular end, and explicitly distinguishes the still-open opposite approximation assertion in that paper. Density of hyperbolic examples, by itself, says neither that the hyperbolic class is open nor that parabolic approximants exist inside every fine neighborhood of a hyperbolic sewing. Later regular perturbation results in Schauder/Roumieu spaces also have different hypotheses. These sources are relevant route checks, not an identified resolution of the target.

## 6. Exact remaining gap and stopping point

None of the five approaches proves that an arbitrary given hyperbolic sewing has a fine C0 neighborhood consisting of hyperbolic sewings. None constructs a parabolic admissible sewing inside every positive-continuous tolerance around a fixed hyperbolic sewing.

The affirmative route needs a robust end-capacity or modulus witness that survives value-only perturbations without the derivative, uniqueness, or uniform quasiconformality assumptions inserted above. The negative route needs a coherent parabolic sewing satisfying the pointwise tube everywhere, including the compactified singular endpoint. The bounded-displacement distortion examples, compact-open parabolic surgeries, and positive-side log-singular approximations each fail to supply that last conclusion for a different explicit reason.

The five-attempt research budget is exhausted. The mathematical disposition remains unsolved. The accompanying finite exact and numerical controls check identities and examples only. They are not a formal proof assistant verification, a numerical test of infinite end type, or a substitute for the arguments above.
