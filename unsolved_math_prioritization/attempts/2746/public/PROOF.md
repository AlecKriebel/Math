# Isolated real-polynomial realization of fibered links

## 0. Exact target and conventions

Let L be a fibered link in S³, meaning the binding of an open book whose pages
are Seifert surfaces. The target is a real polynomial map
F : (R⁴,0) → (R²,0) such that, for some ε₀>0,

1. rank DF(0)<2;
2. rank DF(x)=2 whenever 0<|x|<ε₀;
3. F⁻¹(0)∩S³_ε has link type L for all sufficiently small ε>0.

This is K3 Problem 1.87, also Benedetti–Shiota Conjecture 1.6. No specified
open-book representative or monodromy is an additional demand of the question.
In contrast, *weak* isolation only requires rank two on the punctured zero
fiber. A link realized by a weakly isolated map need not have an isolated-map
realization furnished by the same construction.

**Outcome.** The universal target remains unresolved by this packet. The five
routes below establish only their expressly stated partial conclusions. They
are reconstructions of known ideas or elementary controls, not claims of new
theorems about the conjecture.

## 1. Smooth coning: complete realization in the wrong category

### Proposition 1

Every smooth open book on S³ has a smooth map F:R⁴→R², defined near the origin,
flat at the origin, whose only critical point near the origin is the origin and
whose link there is its binding L.

### Proof

Write θ:S³\L→S¹ for the open-book map. In a tubular neighborhood L×D² it is
the angular coordinate of the normal disk. Choose a smooth h:S³→C such that
h⁻¹(0)=L, h/|h|=θ off L, and h is the normal complex disk coordinate near L.
To construct h, multiply θ by a positive smooth modulus off L equal to the
normal radius near L; the product is then smooth across L.

For r>0 and u∈S³ put a(r)=exp(−1/r²) and F(ru)=a(r)h(u); set F(0)=0.
Every derivative in Cartesian coordinates is bounded by a finite sum of terms
C r^(−m)exp(−1/r²), since h and its derivatives on S³ are bounded. Each such
term tends to zero faster than every power of r. Induction on derivative order
shows that the extension is C∞ and every derivative at 0 vanishes.

At h(u)=0, the tangent differential dh:T_uS³→C is onto, so DF is onto. At
h(u)≠0, the radial derivative is a'(r)h(u), where a'(r)>0. Since θ is a
submersion there is X∈T_uS³ with d(arg h)(X)≠0. Consequently

Im(conj(h) dh(X))=|h|² d(arg h)(X)≠0.

Thus a'h and a dh(X) are real-linearly independent. DF has rank two at every
nonzero point. Its zero set is exactly the cone over L, so every small sphere
has the required link. At 0, DF=0. ∎

### Attempted transfer and exact gap

Taylor approximation of this F cannot yield the desired polynomial: every
finite Taylor polynomial is identically zero. Approximation on a fixed compact
annulus can preserve rank there, but gives no uniform control as r→0. The
smallest differential singular value can decay faster than every power.
One needs a realization with finite-order quantitative nondegeneracy at the
origin, not ordinary unweighted approximation. This does not show that another
analytic realization is impossible. Benedetti–Shiota already record the flat
smooth cone construction in Remark 1.5(6) and Section 6.

## 2. Analytic finite jets and the blow-down gap

### Proposition 2 (known finite-sufficiency mechanism, reconstructed)

Suppose f:(R⁴,0)→(R²,0) is real analytic *at* 0, has an isolated critical
point there, and its punctured zero set is transverse to every sufficiently
small centered sphere. Then a sufficiently high Taylor polynomial P of f
has an isolated critical point at 0 and the same small-sphere link.

### Proof

For a real 2×4 matrix A define M(A) as the sum of the squares of its six
2×2 minors. Then M(A)>0 if and only if rank A=2. Put R=|x|² and

A_f(x)=Df(x),  B_f(x)=Df(x)(R I−xxᵀ),
d_f(x)=M(A_f(x)),  h_f(x)=|f(x)|²+M(B_f(x)).

These are analytic scalar functions. On x≠0 the matrix R I−xxᵀ has image
T_xS³_|x| and acts there as multiplication by R. Thus M(B_f)>0 is precisely
surjectivity of the tangent differential of f on that sphere. Isolated
criticality implies d_f>0 on a punctured small ball. At any nonzero zero of f,
sphere transversality implies M(B_f)>0. Else |f|²>0. Hence h_f>0 on the
same punctured ball. Both vanish at 0.

The analytic Łojasiewicz inequality for a scalar function with isolated zero
gives constants c>0 and finite positive exponents a,b such that, after
shrinking the ball,

d_f(x)≥c|x|^a,  h_f(x)≥c|x|^b.

Let P be the Taylor polynomial through degree m and f_s=f+s(P−f), 0≤s≤1.
Uniformly in s, f_s−f=O(|x|^(m+1)) and Df_s−Df=O(|x|^m).
The expressions d and h are polynomial expressions in x, f, and Df, whose
entries are bounded on the chosen ball. It follows that

d_{f_s}−d_f=O(|x|^m),  h_{f_s}−h_f=O(|x|^m),

uniformly in s. Choose m>max(a,b) and m≥1, then shrink the ball once more.
The two lower bounds persist with c/2, for all s. Therefore every f_s has
rank two away from 0; at its zero set the restriction to every small sphere
also has rank two. The first jet at 0 is unchanged, so 0 remains critical.

For any fixed sufficiently small ε the set

{(x,s)∈S³_ε×[0,1] : f_s(x)=0}

is a compact smooth manifold with boundary. Its projection onto [0,1] is a
submersion: surjectivity in the x-directions solves the equation for the
velocity of x for any velocity of s. A smooth horizontal vector field and its
flow identify the fibers, giving an isotopy of their embeddings in S³_ε.
At s=0 and s=1 these are the links of f and P. ∎

The sphere-transversality hypothesis is the usual analytic link/cone fact;
it is stated explicitly rather than silently inferred for arbitrary smooth
maps. The only external analytic input in this proof is the indicated
Łojasiewicz lower bound. No effective exponent is asserted.

### Attempted analytic construction and exact gap

An analytic germ at the origin would therefore suffice. But analyticity after
blowing up is not analyticity downstairs. Benedetti–Shiota Theorem 1.8 supplies
a tame g for nontrivial fibered knots such that g composed with a resolving
blow-up is analytic and has rank two away from the exceptional divisor. Their
following discussion explicitly identifies the missing analytic blow-down
lemma. It does not supply the hypothesis of Proposition 2. Claims about tame
maps or functions analytic only off the origin cannot fill this gap. We do
not infer a universal analytic-germ result from abbreviated later summaries.

## 3. Weak isolation cannot be upgraded from the zero set alone

### Proposition 3 (explicit same-link controls)

There are real polynomial maps with zero set the same coordinate 2-plane,
and with DF(0)=0, for which one has an isolated critical point and the other
has only a weakly isolated one. In particular, even a fibered zero-set link
does not certify isolation for its defining map.

### Proof

In coordinates (x,y,z,w), set R=x²+y²+z²+w² and

G(x,y,z,w)=(xR,yR),
H(x,y,z,w)=(xR, yR(y²+z²+w²−x²)).

Both vanish exactly on x=y=0. For H, the first component forces x=0 away
from the origin; the second then equals yR², forcing y=0. Both differentials
vanish at the origin.

The (x,y)-minor of DG is

(R+2x²)(R+2y²)−4x²y² = R(R+2x²+2y²)>0  (R>0).

So G has an isolated critical point. Its small-sphere zero set is a standard
unknot.

On x=y=0, the (x,y)-minor of DH is R³, positive off 0. Hence H has weak
isolation. On the punctured curve (x,y,z,w)=(t,0,t,0), t≠0, its second
Jacobian row is zero and its first row is nonzero; therefore rank DH=1.
These critical points accumulate at 0 and lie off H⁻¹(0). Thus H is not
isolated despite its identical fibered link. ∎

For an additional operation control, put f(z,w)=z²+w² and g(z,w)=z²−w².
Both holomorphic maps have isolated critical points. The real polynomial
J=f conjugate(g) has weak isolation: off 0 its zero set consists of four
distinct complex lines, and at any zero precisely one of f,g vanishes, with
surjective differential. But on w=0,z≠0, J=|z|⁴ and its differential has
rank one. Consequently multiplication with a conjugated factor does not
automatically preserve isolated critical points. No claim that this product
is a general plumbing operation is made.

### Exact gap

Akbulut–King's weak realization theorem does not control rank on the rest of
the punctured ball. Source and target diffeomorphisms preserve the rank of the
defining map, so coordinate changes alone cannot repair H. A new
link-preserving construction that eliminates *all* off-fiber critical points
is still needed in general. The explicit G repairs the unknot example only.

## 4. P-fibered braids: quantitative rank criterion and parity obstruction

### Proposition 4 (a sufficient polynomialization criterion)

Let g_t(u)=uⁿ+Σ_{j=0}^{n−1}a_j(t)uʲ, n≥2, be a smooth 2π-periodic loop of
monic complex polynomials with distinct roots. Suppose the a_j are finite
Fourier series. Assume that at every (u,t) with ∂g_t/∂u=0,

Im(conj(g_t(u)) ∂g_t(u)/∂t) ≠ 0.                         (4.1)

Suppose some positive integer k satisfies, for every coefficient c_{jℓ}≠0
in the Fourier series of a_j (including ℓ=0),

k(n−j)≥|ℓ|,  k(n−j)≡ℓ (mod 2),  j+k(n−j)≥2.             (4.2)

Then

F(u,v)=uⁿ+Σ_{j,ℓ} c_{jℓ}uʲ v^((k(n−j)+ℓ)/2)
                                      conjugate(v)^((k(n−j)−ℓ)/2)

is a real polynomial with an isolated critical point at 0. Its link is the
closure of the root braid of g_t, using the standard embedding of C×S¹
into S³ minus a braid axis.

### Proof

Conditions (4.2) make all exponents nonnegative integers and every monomial
have total degree at least two. Thus F is polynomial and DF(0)=0. At v=re^{it}
with r>0, write u=r^k q. In these smooth coordinates

F(r^kq,re^{it})=r^(kn)g_t(q).

If g_q≠0, variation in complex q already gives real rank two. If g_q=0,
the roots being simple imply g≠0. The r- and t-derivatives are
kn r^(kn−1)g and r^(kn)g_t; their real determinant is
kn r^(2kn−1)Im(conj(g)g_t), nonzero by (4.1). At v=0,u≠0 we have
F(u,0)=uⁿ and F_u=nu^(n−1)≠0 (all lower-u terms have positive total
v,conjugate(v) degree), again giving rank two.

The zero set away from the origin is the weighted cone
{(r^kq,re^{it}):g_t(q)=0,r>0}. Each weighted ray meets S³_ε once because
r^(2k)|q|²+r² is strictly increasing from 0 to infinity. The projection to
t identifies its roots as the original root braid. Changing k continuously
among positive real weights, and radially adjusting the unique sphere
intersection, is an isotopy of these links; equivalently it is the usual
closed-braid embedding (q,t)↦ε(q,e^{it})/sqrt(1+|q|²) when k=1.
Distinct roots remain distinct on each t-page because the radial map
q↦r(|q|)^k q is injective: its modulus increases strictly with |q| by the
same sphere equation. This proves the link assertion. ∎

Condition (4.1) is the usual nonvanishing angular derivative of polynomial
critical values underlying P-fibered braids. The proposition is an explicit
special-case reconstruction of the known radial braid mechanism.

### A parity failure with no topological counterexample

Take a=1/4 and g_t(u)=u²−exp(it)−a exp(2it). Its roots are distinct because
exp(it)(1+a exp(it)) never vanishes. The only critical point in u is 0, and
for its nonzero critical value c(t),

d arg c/dt = (1+3a cos t+2a²)/(1+2a cos t+a²)>0.

For a=1/4 the numerator is at least 3/8 and the denominator is at most
25/16, so the derivative is at least 6/25. Nevertheless a_0 contains the
two modes 1 and 2, whereas k(n−0)=2k is even. The mode 1 fails (4.2) for
every integer k. Increasing radial degree cannot cure this parity conflict.

Replacing t by 2t repairs parity; k=2 gives
F=u²−v³conjugate(v)−(1/4)v⁴. But it squares the root braid. Homotoping
a to 0 keeps the roots distinct, so the original braid is σ₁, with one-component
unknot closure; its square is σ₁², with two-component Hopf-link closure.
Squaring is therefore a change of target, not a realization of the original
link by this construction. The unknot is already real algebraic by Section 3.

### Exact gap and current results

No proof is given that every fibered link has a P-fibered representative, or
that arbitrary such representatives admit link-preserving polynomialization.
Bode's 2025 theorem handles T-homogeneous braids with a substantially more
flexible construction. Bode–Hsueh's 2025 preprint gives P-fibered
representatives for all canonically fibered links; its universal version
remains Conjecture B. Neither statement removes both gaps for every link.

## 5. Newton nondegeneracy: a genuine limitation of a large ansatz

One might hope to avoid singularity estimates by realizing every fibered link
using convenient, inner-nondegenerate mixed polynomials with Γ-nice Newton
boundary. Bode's published 2025 Part II, Example 4.11 and the paragraph after
Lemma 6.3, excludes the fibered knot 8₁₆ from that class. This is a restriction
on an ansatz, not on arbitrary real polynomials. Here is a transparent
reconstruction of its Alexander-polynomial symmetry checks.

Take the source's Alexander polynomial

Δ(t)=1−4t+8t²−9t³+8t⁴−4t⁵+t⁶.

### Proposition 5A: the 2-periodic necessary identity fails

Over F₂, Δ=t⁶+t³+1=Φ₉(t) is irreducible. Indeed a root has order nine,
and the multiplicative order of 2 modulo 9 is six, so its degree over F₂ is
six. Equivalently the portable control divides by all fourteen monic
polynomials of degrees one through three and finds no factor.

Murasugi's necessary condition for 2-periodicity, as recorded in Example
4.11, is Δ≡q(t)²(1+t+⋯+t^(λ−1)) modulo 2, up to a Laurent monomial,
where λ is positive and odd. Normalize nonzero constant terms by removing
Laurent units. Irreducibility forces q to be constant. The remaining geometric
sum would have degree six, hence λ=7, and is not t⁶+t³+1. Thus the condition
fails.

### Proposition 5B: the odd/freely 2-periodic necessary identity fails

For odd knots, the free-period-two necessary condition recorded in the same
example is

Δ(t²)=q(t)q(−t)

after normalization of Laurent units. To justify this normalization, start
with Δ(t²)=ηtᵇq(t)q(−t), where η=±1 and q is an integral Laurent polynomial.
Write q=tᵐQ with Q an ordinary polynomial and Q(0)≠0. Comparing lowest
exponents gives b+2m=0; comparing constant coefficients gives
η(−1)ᵐQ(0)²=1. Hence the combined sign is positive and the identity becomes
Δ(t²)=Q(t)Q(−t). Rename Q as q. This identity tests free period two; no
claim about every possible free period is needed here.

Suppose it holds. The constant and leading coefficients of Δ(t²) are one,
so q has degree six and constant and leading coefficients ±1. Modulo 2 the
identity becomes q(t)²=(1+t³+t⁶)². Injectivity of the squaring map on F₂[t]
gives q(t)≡1+t³+t⁶. Write q=Σ_{i=0}^6 a_i t^i. Thus a_0,a_3,a_6 are odd,
and a_1,a_2,a_4,a_5 are even. The t⁶ coefficient of q(t)q(−t) is

2a_0a_6−2a_1a_5+2a_2a_4−a_3² ≡ 2−1 ≡ 1 (mod 4).

The t⁶ coefficient of Δ(t²) is −9≡3 (mod 4), a contradiction. This
checks the needed nonfactorization without claiming a full irreducibility
certificate for Δ(t²) over Q. All 128 parity-compatible coefficient vectors
modulo 4 are checked independently by the control script. ∎

### Consequence and exact gap

With the source's knot polynomial and Murasugi/Hartley necessary conditions,
these proofs rule out the two symmetries. The inference from missing
symmetries to exclusion from the specified Newton class uses Bode's
classification, not the arithmetic alone. His theorem and the fibering of
8₁₆ are credited source inputs here, not independently reproved topology.

No obstruction to *all* real-polynomial maps follows. Degenerate mixed
polynomials, nonconvenient models, or constructions outside the stated Newton
hypotheses are not excluded. Therefore the proposed universal nondegenerate
ansatz fails, but 8₁₆ is not asserted to be a counterexample to KP-1.87.

## 6. Exact unresolved requirement

For an arbitrary fibered link, construct a real-polynomial germ with rank two
on its entire punctured neighborhood and the original link, or prove an
obstruction applying to every such polynomial. The five routes establish
neither. Proposition 2 transfers the problem to analytic germs at the origin;
Sections 1 and 3 do not provide those germs. Section 4 needs universal
braiding and link-preserving polynomialization. Section 5 shows why one
particularly useful nondegenerate class cannot suffice.

All calculations are local and exact where labeled. No numerical sample,
finite link table, literature-search negative, or subclass exclusion is used
as a proof of the universal conjecture or its negation.
