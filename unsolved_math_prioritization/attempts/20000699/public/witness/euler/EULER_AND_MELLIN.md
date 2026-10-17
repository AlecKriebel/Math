# Prescribed density and corrected zero/one-swap functional

Status: authored pass-1 proof, with two explicit corrections to the specified CK Mellin presentation. The Ramanujan density itself is unchanged.

## 1. Notation and conclusions

Write L=log N, d=alpha+beta, u=gamma-alpha, v=delta-beta,

G(z)=1/zeta(1+z),

g_p(u,v)=p^(-2-u-v)/[(1-p^(-1-u))(1-p^(-1-v))],

S_z(h)=sum_(q>=1) c_q(h) F_(alpha,gamma)(q)F_(beta,delta)(q)/q^2,

D_z(h)=G(u)G(v)S_z(h).

Thus the prescribed profile is m_z(x,h)=D_z(h)x^(1-d)/(1-d), and its ordinary differential for x>0 is D_z(h)x^(-d)dx. Both orientations have the SAME prescribed profile: swapping the two coefficient pairs exchanges u,v and preserves d. This symmetry concerns the profile, not the actual arithmetic sums.

The proven conclusions are:

1. The fixed-h Ramanujan series converges absolutely and normally on a neighborhood of the gate's polydisc, and D_z(h) and m_z(x,h) are holomorphic there, including all pair collisions.
2. The unconditionally proved arithmetic Mellin identity is

   chi(1-k) J_z(k) = B_(-beta,beta-k,gamma+k-d,delta)(1),

   where J_z(k)=sum_(h>=1) D_z(h)h^(-k) initially for Re k>1. Equivalently, with k=d+s, the right side is

   B_(-beta,-alpha-s,gamma+s,delta)(1).

   It is NOT, in general, B_(-beta,-alpha,gamma,delta)(1+s), as printed in CK2016 Theorems 1 and 2 and CK2017's corresponding formulas.
3. The linearized off-diagonal density functional has an exact Mellin representation. On moving to an ordinary integrable t-moment contour, a necessary endpoint term involving w(0) appears. This term is generally too large to suppress under the gate's assumptions.
4. This Euler/Mellin proof imports no GRH-dependent additive-twist residue identity. If the original additive-twist double-contour object C is used, its GRH qualification must remain explicit. Nothing here proves that original pole-exclusion step without GRH.

The exact-to-linearized kernel and cutoff estimates are supplied in the forward-transfer proof. Combining those estimates with Section 6 below establishes correspondence of the ACTUAL Q, rather than merely calling Q a ratios main term.

## 2. Absolute convergence, bounds, and holomorphy

Only squarefree q contribute. For a prime p,

c_p(h)=p-1 if p divides h, and c_p(h)=-1 otherwise.

Consequently

S_z(h)=product_p [1+c_p(h)g_p(u,v)].                         (2.1)

Fix h>=1. In any sufficiently small fixed polydisc, say |u|,|v|<1/8, all local denominators are nonzero, and

|g_p(u,v)| <= C p^(-7/4).

For p not dividing h this is summable in p; the primes dividing h are finite. Thus the product and the original squarefree-q series converge absolutely, locally uniformly in the complex shifts. Indeed the absolute q-series is product_p(1+|c_p(h)g_p|). This proves the identity and joint holomorphy; it does not appeal to a conditionally convergent formal Euler product.

The factor G is holomorphic near zero and has a simple zero there. To see this without a zero-free-region assumption, z*zeta(1+z) is holomorphic and equals 1 at zero, so it is nonvanishing in some fixed disk, and

G(z)=z/[z*zeta(1+z)]=z+O(z^2).

For all sufficiently large T, even the four-variable polydisc of radius 2c/L about (r,r,r,r) lies in this neighborhood. Also |d|<1/2. Hence m_z(x,h) is holomorphic on a neighborhood of the closed D in the gate. The finitely many smaller T can be excluded by the theorem's explicit asymptotic threshold; no assertion is made that an arbitrary small T polydisc avoids all reciprocal-zeta poles.

A useful uniform finite-range bound is

sup_(z in D,1<=h<=N) |D_z(h)| <= C L^(B-2),               (2.2)

for fixed C,B depending on c (and harmless threshold choices). Here and below increasing B is allowed. Proof: |G(u)G(v)|<=C L^(-2). For p|h<=N the shrinking shifts give p^(-Re(u+v))<=exp(4c), so p|g_p|<=C_c/p. The p not dividing h factors have a uniformly bounded product. Thus

|S_z(h)| <= C product_(p|h)(1+C_c/p)
           <= C exp(C_c sum_(p<=N)1/p) <= C L^B.

The last estimate needs only an elementary upper bound: with eta=1/L, sum_(p<=N)1/p <= e sum_p p^(-1-eta) <= e log zeta(1+eta) <= e log L+O(1). This supplies a completely explicit choice B=e*C_c after enlarging constants. This very weak polylogarithmic bound is adequate because lambda<2 is strict.

For fixed small shift neighborhoods one also has S_z(h)=O_epsilon(h^epsilon), with the constant uniform in the neighborhood. Split the p|h factors into finitely many small primes and large primes for which log(1+C p^(-3/4))<=epsilon log p. This supplies, when needed, elementary normal convergence of h-Dirichlet series in Re k>1+epsilon.

### Collision check

At alpha=gamma and beta=delta, D_z(h)=0, including odd h. At the common point alpha=beta=gamma=delta=r, the mixed numerator derivative is

partial_alpha partial_beta D_z(h) = S_(r,r,r,r)(h).

Both derivatives must hit the two simple G zeros; all terms involving derivatives of S_z vanish at that point. Here

S_(r,r,r,r)(h)=product_p [1+c_p(h)/(p-1)^2].

For p|h the factor is p/(p-1), and for p not dividing h it is p(p-2)/(p-1)^2. These are exactly

(1-nu_p(h)/p)/(1-1/p)^2.

In particular the p=2 factor vanishes for odd h. Prime-power valuations beyond divisibility do not enter, because all q are squarefree. This independently recovers the prescribed Hardy–Littlewood singular series.

## 3. The h-series, in a genuine common convergence domain

For Re k>1,

J_z(k)=sum_(h>=1) D_z(h)h^(-k)
      =G(u)G(v) zeta(k) V_z(k),                           (3.1)

where

V_z(k)=product_p [1+(p^(1-k)-1)g_p(u,v)].                 (3.2)

To justify interchanging h and q, use |c_q(h)|<=gcd(q,h) for squarefree q and

sum_(h>=1) gcd(q,h)h^(-sigma)
 =zeta(sigma) sum_(a|q) phi(a)a^(-sigma)
 <=zeta(sigma) product_(p|q)(1+p^(1-sigma)).

After multiplication by |F(q)F'(q)|/q^2, the q-series is bounded by a convergent product

product_p [1+|g_p|(1+p^(1-sigma))]

for sigma>1 and sufficiently small shifts. This proves (3.1) directly, without an unjustified exchange of divergent Ramanujan sums. The exact inner identity is

sum_(h>=1)c_q(h)h^(-k)=zeta(k)product_(p|q)(p^(1-k)-1)

for squarefree q, obtained from c_q(h)=sum_(a|(q,h)) a*mu(q/a).

For Re k>=1/2 and shifts in the shrinking neighborhood, the product (3.2) converges normally and is uniformly bounded, even as Im k varies: the local deviation is O(p^(-3/2+4c/L)+p^(-2+4c/L)). In this strip J_z(k) is meromorphic, its only possible pole is the simple zeta pole at k=1, and

Res_(k=1) J_z(k)=G(u)G(v),                              (3.3)

because V_z(1)=1 exactly. This residue can of course vanish on collision hyperplanes. Combined expressions remain holomorphic in the shifts.

## 4. Correct arithmetic one-swap identity

For arbitrary parameters a,b,c,e the ordinary rank-one Rankin–Selberg series is

B_(a,b,c,e)(z)=sum_n I_(a,c)(n)I_(b,e)(n)n^(-z),

initially in its absolute convergence half-plane. Its local factor is

[1-p^(-z-b-c)-p^(-z-a-e)+p^(-z-c-e)]/[1-p^(-z-a-b)].     (4.1)

This follows by summing the geometric series for I_(a,c)(p^j)=p^(-ja)(1-p^(a-c)), j>=1. Its familiar meromorphic continuation can be obtained by extracting zeta factors from this rational local factor.

Define the actual swapped function

B*_z(k)=B_(-beta,beta-k,gamma+k-d,delta)(1).

The local factor (4.1) becomes

[1-p^(-1-u)-p^(-1-v)+p^(-1-k-u-v)]/[1-p^(-1+k)].         (4.2)

On the other hand,

(1-p^(-1-u))(1-p^(-1-v))
 * [1+(p^(1-k)-1)g_p]
 =1-p^(-1-u)-p^(-1-v)+p^(-1-k-u-v).                     (4.3)

Using chi(1-k)zeta(k)=zeta(1-k), (3.1) and (4.3) prove

B*_z(k)=zeta(1-k)G(u)G(v)V_z(k)=chi(1-k)J_z(k).          (4.4)

For complete analytic logic, (4.1) and (4.3) first identify both sides in a nonempty absolute-convergence region with Re k<0, Re u,Re v>0, Re(k+u+v)>0; then use meromorphic continuation. Equation (3.1) is separately proved for Re k>1. Thus (4.4) is an identity of meromorphic functions, not an assertion of absolute convergence of the original B series on the final k=1/2 contour.

With s=k-d, this is B_(-beta,-alpha-s,gamma+s,delta)(1). It is also the swap obtained directly from the shifted ratios input R_(alpha+s,beta,gamma+s,delta): the numerator shifts alpha+s,beta are negated and exchanged while the denominator shifts gamma+s,delta are retained. It has an equivalent allocation obtained by distributing s to the other original ratio. This is actual swap algebra.

### Defect in the printed source and an exact test

CK2016 arXiv:1604.06124v2 Theorem 1, Theorem 2, and the final line of Section 2 print B_(-beta,-alpha,gamma,delta)(1+s). The source's own Section 3 instead identifies its arithmetic product with A_(-beta,-alpha-s,gamma+s,delta), consistent with (4.4). The printed forms differ.

A decisive test is alpha=beta=gamma=delta=0 and Re s=2. Then I_(0,0)(n)=1 if n=1 and 0 otherwise. The frozen density D_z(h)=0, so J_z(k)=0 and the corrected swapped contribution vanishes. The printed B_(0,0,0,0)(1+s) equals 1, not 0. Under the residue-first interpretation used in the source proof, each finite-q original additive-twist double-contour term also vanishes at these shifts: the twist series reduce to constants and the remaining kernel is holomorphic on sufficiently small product disks when s=2. This observation does not assert normal convergence of the unreduced q-series on those contours. More directly, the printed Theorem 2 at the collision gives an extra swapped Perron contribution for a finite polynomial that is identically 1, whereas the corrected swap vanishes. This is not a numerical or extraction artifact; the source page images show the printed expression.

The correction changes the source's displayed identity, not the frozen Ramanujan profile. Any final theorem using this proof must disclose the corrected shifted B expression and must not claim literal verification of the printed formula.

### Exact role of GRH

CK2016 Section 3 and CK2017's proof invoke GRH when expanding additive twists in Dirichlet characters, to assert that only principal characters supply poles in a fixed neighborhood of w=1. Without that hypothesis, zeros of nonprincipal denominator L-functions may produce additional poles; the source proof does not remove them. The printed source statements themselves say “Assuming the Generalized Riemann Hypothesis.”

Our argument starts from the explicitly frozen F factors and proves (3.1)–(4.4) directly by convergent arithmetic products, elementary algebra, and the zeta functional equation. It does not use those additive-twist functions. Consequently the correspondence for this prescribed-density witness needs no GRH. The stronger assertion that the prescribed density equals the full additive-twist double-residue object still carries the source's GRH assumption, and is not claimed here unconditionally.

## 5. Exact Mellin representation of the linearized density functional

Put

W(v)=hat w(v)+hat w(-v), v>=0,

M_W(k)=integral_0^infinity W(v)v^(k-1)dv, Re k>0.

W is smooth, supported on [0,A], and flat at A. No evenness of w is assumed. The sum of the two orientations has this W because their profiles coincide. For Re k in any compact subinterval of (0,infinity), repeated integration by parts with v*d/dv proves, for every integer m>=0,

|M_W(k)| <= C_(m,w) (1+|Im k|)^(-m).                    (5.1)

There are no boundary terms: v^(Re k) vanishes at zero and W is flat at its upper support boundary.

Define

L_z(T,N)=T sum_(h>=1) D_z(h)
            integral_0^N x^(-1-d) W(Th/(2pi x))dx.       (5.2)

Only h<=2pi A N/T contribute; moreover each integrand vanishes for x<Th/(2pi A). For T>2pi A, replacing the lower limit 0 by 1 does not change (5.2), even when Re d>=0; convergence at zero is therefore not an issue.

Let Psi_d(y)=integral_y^infinity W(v)v^(d-1)dv. In the domain Re k>max(0,Re d), absolute integration gives the precisely parametrized transform identity

integral_0^infinity Psi_d(y)y^(k-d-1)dy=M_W(k)/(k-d).

Equivalently its usual Mellin transform at s is M_W(d+s)/s. Mellin inversion (or Fourier inversion on the logarithmic variable) gives

L_z(T,N)=T N^(-d)/(2pi i)
 integral_(Re k=2) (2pi N/T)^k M_W(k)J_z(k)/(k-d) dk.    (5.3)

For sufficiently large T, |d|<1/4. All exchanges on this line are absolute, by Section 3 and (5.1). The Mellin inversion is an ordinary smooth-kernel inversion; it introduces neither a half-weight ambiguity nor a sharp-Perron endpoint error. The N cutoff was integrated into Psi, and Psi is smooth.

### Moving the contour and the t=0 endpoint

Move (5.3) to Re k=1/2. The pole k=d lies to the left and is not crossed. M_W is holomorphic in the intervening strip. The only crossed pole is k=1 from J, and M_W(1)=integral_R hat w(v)dv=w(0). Therefore exactly

L_z(T,N)=E_z(T,N)+L_z^swap(T,N),                         (5.4)

E_z(T,N)=2pi w(0) N^(1-d)G(u)G(v)/(1-d),                (5.5)

L_z^swap(T,N)=T N^(-d)/(2pi i)
 integral_(Re k=1/2) (2pi N/T)^k M_W(k)J_z(k)/(k-d) dk.  (5.6)

No asymptotic error occurs in this contour movement. To make tails explicit, for Y>=2 and m>=3 the omitted vertical tails of (5.3), and the horizontal segments used in moving a height-Y rectangle, are bounded respectively by

C_(m,w,c,a0) (N^2/T) L^(-2) Y^(1-m),
C_(m,w,c,a0) (N^2/T) L^(-2) Y^(-m),                    (5.7)

after enlarging constants and assuming N/T>=1. Bounds for (5.6) are no larger. One elementary bound adequate here is zeta(k)=O(1+|Im k|) uniformly on 1/2<=Re k<=2 away from k=1; it follows from the integral continuation using the bounded fractional-part function. The product V_z is uniformly bounded. These observations and (5.1) prove (5.7), and the tails vanish as Y tends to infinity. Choosing any sufficiently large power-of-T height produces a quantitative error smaller than any prescribed inverse power of T.

For 0<Re k<1, the cosine Mellin identity gives

M_W(k)=chi(1-k) integral_R w(t)|t|^(-k)dt.              (5.8)

One rigorous derivation inserts exp(-epsilon*v) in the Fourier integral, uses Fubini, evaluates the elementary Gamma integral, and sends epsilon down to zero. The bound by a constant times |t|^(-Re k), together with Schwartz decay and Re k<1, permits dominated convergence. Both sides are holomorphic in this strip. The chi normalization is chi(s)=2^s*pi^(s-1)*sin(pi*s/2)*Gamma(1-s), so 2*Gamma(k)*cos(pi*k/2)/(2pi)^k=chi(1-k).

Combining (4.4), (5.6), and (5.8) yields the genuine one-swap expression

L_z^swap(T,N)= integral_R w(t/T) [1/(2pi i)]
 integral_(Re k=1/2) N^(k-d)/(k-d)
                  (|t|/(2pi))^(-k) B*_z(k) dk dt.      (5.9)

The precise finite-height integrated convention for this formula is specified next. The absolute t-moment with exponent -1/2 is finite. After t integration the k-integral converges absolutely, by (5.1), but this does not assert absolute convergence of the raw double integral. Values at t=0 are ignored on this Lebesgue integral; its integrable singularity is not an omitted discrete term.

### 5.9a. Important order-of-integration qualification

For an arbitrary w, the absolute double integral of the raw k-integrand in (5.9) is NOT automatically justified by Schwartz decay in t: before the t integration, |t|^(-ik) does not decay in k. Thus the rigorous convention in (5.9) is

lim_(Y->infinity) integral_R w(t/T) [1/(2pi i)]
 integral_(1/2-iY)^(1/2+iY) (...) dk dt,

with the t integral evaluated for each finite Y. Equivalently, integrate in t first; the resulting k integral is absolutely convergent by (5.1). This convention is part of the theorem. There is no claim that the unsmoothed inner infinite Perron integral is absolutely convergent for every fixed t. This removes an otherwise invalid Fubini step. The explicit tail estimate (5.7) applies to this integrated/truncated convention.

The finite-part alternative is to keep Re k=2 and analytically continue the t-Mellin moment in (5.8). On 1<Re k<3 one may use

integral_0^1 [w(t)+w(-t)-2w(0)]t^(-k)dt
 +integral_1^infinity [w(t)+w(-t)]t^(-k)dt
 +2w(0)/(1-k).

Its pole at k=1 carries precisely the endpoint (5.5) when the contour is moved. Calling the ordinary divergent Re k=2 t-integral an ordinary integral is not permissible.

Unless w(0)=0, (5.5) is generally of size N/L^2 away from collision and therefore is NOT an O(N/T) kernel error, nor o(T/L^2). It must remain in the result for the gate's weight class. At full pair collision it vanishes; its mixed numerator derivative is 2pi*w(0)*N^(1-2r)/(1-2r), of the expected long-polynomial prime scale. This is why checking only the zero-shift undifferentiated value would miss the endpoint issue.

## 6. The zero-swap and the actual arithmetic Q

The zero-swap is the exact diagonal

Z_z(T,N)=T*hat w(0)*sum_(n<=N) I_(alpha,gamma)(n)I_(beta,delta)(n)/n.

For a literal Perron representation with no half-weight ambiguity, use the noninteger real cutoff N+1/2:

Z_z=T*hat w(0)*lim_(Y->infinity) [1/(2pi i)]
 integral_(b-iY)^(b+iY) B_(alpha,beta,gamma,delta)(1+s)
                         (N+1/2)^s/s ds,

where b=2 is adequate for all sufficiently large T. Standard Perron inversion, first on individual Dirichlet-series terms and then via absolute convergence on b, gives exactly n<=N. Alternatively the integer-N symmetric Perron formula must be supplemented by half of the n=N summand. No change to the gate's sharp arithmetic cutoff is being made.

The proved kernel/cutoff comparison in ../forward/SHARP_TO_LINEAR_COMPARISON.md supplies

Q_z=Z_z+L_z+O((N/T)L^B),                                (6.1)

uniformly on the polydisc, with the stronger bound O((N/T)(1+log N)^B/(log N)^2) in that artifact. The same elementary argument applies on the enlarged polydisc after changing constants, if an enlarged-domain comparison is desired. Therefore the explicit corrected CK-type functional for the actual gate Q is

Q_z=Z_z+E_z+L_z^swap+O((N/T)L^B).                        (6.2)

This is a zero-swap plus one-swap computation with the required endpoint correction. It was derived from the prescribed arithmetic density, with no relabeling. Since lambda<2, the displayed extra error, even after multiplication by rho^(-2)=L^2/c^2, is o(T). It also lies in o(T/L^2) before differentiation. The exact forward R−Q bound remains whatever the Abel-transfer theorem proves; (6.2) is a separate identification of Q.

Combined shift holomorphy is transparent in (5.3), (5.5), and (5.6): J_z is a holomorphic shift family on the fixed contours, |d|<1/4 keeps k-d away from zero there, and the integrals converge locally normally. Individual residue or zeta expressions need not be evaluated termwise at intersecting polar hyperplanes. Use their combined holomorphic continuation.

## 7. Source provenance and credit

- Brian Conrey and Jonathan P. Keating, “Pair correlation and twin primes revisited,” arXiv:1604.06124v2, https://arxiv.org/pdf/1604.06124v2. Relevant parts: Theorems 1–2, Sections 2–4, and Appendix. The source's Section 4 supplies the prescribed F and m; Section 3 supplies the principal-character/GRH step and the displaced A factor. The PDF page 3 and page 4 displays were inspected independently of extracted text. The publicly served HTML was also checked: https://arxiv.org/html/1604.06124v2.
- Brian Conrey and Jonathan P. Keating, “Averages of ratios of the Riemann zeta-function and correlations of divisor sums,” arXiv:1611.09198v1, https://arxiv.org/pdf/1611.09198v1. Theorem 1 explicitly assumes GRH and identifies the intended one-swap context; its singleton specialization displays the same spectral-parameter discrepancy. This audit is confined to those exact displayed formulas and source versions, not a verdict on the papers as a whole.

This is a conditional finite-polynomial witness using CK's proposed arithmetic input. It proves neither the arithmetic hypothesis, full zeta ratios, nor individual Hardy–Littlewood prime-pair asymptotics. The standard density-to-moment method and the one-swap idea belong to the cited work. The corrections above are explicit audits of the formulas needed for the present frozen gate, not a claim of an unrestricted new resolution.
