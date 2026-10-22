# Scoped results for two exceptional spherical codes

**Original target remains unsolved.** This note does not prove universal
optimality of either exceptional code and does not give a counterexample. It
proves the restricted comparison in Theorem 4, the one-point local result in
Theorem 3, and the explicit obstruction in Theorem 2. Finite exact computations
used in these proofs are reproduced by `verify.py`; their complete output is
`CHECK_RESULTS.json`. No historical novelty or priority claim is made.

## 1. Target, normalization, and the configurations

Schürmann's contribution to Oberwolfach Report 44/2008, printed pp. 2538–2540,
asks whether the configurations with 40 points in R^10 and 64 points in R^14
described by Ballinger–Blekherman–Cohn–Giansiracusa–Kelly–Schürmann (BBCGKS)
are universally optimal. The question concerns *all* configurations of the same
cardinality on the same unit sphere, not just association schemes or codes with
specified inner products. The definition uses

    E_f(C) = sum_{unordered {x,y} in C} f(||x-y||^2),

where f is continuous on (0,4], smooth on (0,4), and completely monotonic:
(-1)^j f^(j) >= 0, including j=0. Put g(t)=f(2-2t). Then g is absolutely
monotonic on [-1,1), and write E_g(C)=sum_{x<y}g(x·y). Throughout this note
energies are unordered-pair energies. Multiplying by two does not affect
minimizers. In particular f(r)=(4-r)^k corresponds to 2^k g_k(t), where
g_k(t)=(1+t)^k.

The constructions below are those in BBCGKS §4, not newly discovered codes.

### 1.1 The 40-point code C40

Index the orthonormal coordinates of R^10 by the unordered pairs from Z/5Z.
For each i in Z/5Z, consider vectors whose four coordinates on pairs containing
i are zero and whose other six coordinates are ±1/sqrt(6). On the four vertices
other than i, put an edge exactly where the coordinate is negative. If e is the
number of edges and d_j the degree at vertex j, retain the vector if

    d_(i+1) = d_(i+2) = e (mod 2),
    d_(i-1) = d_(i-2) = e+1 (mod 2).

There are eight retained vectors of each type i and 40 altogether. Their
off-diagonal inner products and per-point multiplicities are

    (-1/2,8), (-1/3,3), (0,4), (1/6,24).

Let H40 be the integer dot-product matrix before division by 6. The checker
constructs all vectors from the parity rule, verifies distinctness and the
displayed multiplicities, and verifies H40^2=24 H40. Thus G40=H40/6 is PSD
with nonzero eigenvalue 4 and rank 10.

### 1.2 The 64-point code C64

Take F8=F2[z]/(z^3+z+1), and index points by (a,b) in F8^2. Set the Gram
entry to 1 for equal pairs, -1/7 if a=c but b!=d, and otherwise to -3/7
when

    b+d is either (a+c)^3 or ac(a+c),

and to 1/7 otherwise. This is BBCGKS Table 12. Addition here is field addition,
not addition of integer labels. The checker uses the explicit binary field
arithmetic and verifies, for H64=7G64, the identity H64^2=32 H64. Symmetry,
diagonal 7, and trace 448 then prove PSD, nonzero eigenvalue 32/7 for G64,
and rank 14. A real factorization of G64 supplies 64 distinct unit vectors.
Their off-diagonal data are

    (-3/7,14), (-1/7,7), (1/7,42).

Thus no floating-point spectral factorization or externally downloaded
coordinate list is needed to establish the configurations used here.

### 1.3 Three-design identities and shell balance

For both matrices the exact checks give G1=0, G^2=(N/n)G, and
sum_(i,j)G_ij^3=0. For any Gram realization x_1,...,x_N:

* G1=0 implies sum_i x_i=0.
* The frame operator sum_i x_i x_i^T=(N/n)I, by the nonzero spectrum of G.
* The squared norm of sum_i x_i^(tensor 3) equals sum_(i,j)G_ij^3, so the
  third tensor sum vanishes.

These are precisely the degree-one, degree-two, and degree-three sphere
moment identities. They prove that both configurations are spherical
3-designs. The positive fourth Gegenbauer moments in §3 show that they are
not 4-designs. Consequently neither meets the sharp-design criterion: C40
has four distances and would require strength 7; C64 has three and would
require strength 5.

For each occurring off-diagonal value t, let A_t be its adjacency matrix and
m_t its per-point multiplicity. The checker verifies the stronger identities

    G A_t = m_t t G.

It follows that sum_{j:x_i·x_j=t} x_j = m_t t x_i: take its scalar products
with the spanning set of all x_l. In particular, the tangent component of
each shell sum vanishes. Both codes are stationary for every differentiable
radial pair potential. This statement alone is not a minimum assertion.

## 2. Power potentials and the first successful global cases

### Lemma 1 (nonnegative power expansion)

An absolutely monotonic continuous function g on [-1,1), smooth in its
interior, has an expansion

    g(t)=sum_(k>=0) a_k(1+t)^k,  a_k>=0,

convergent with all derivatives on compact subintervals of (-1,1). It is
uniformly convergent on every compact subinterval of [-1,1).

Here is a justification of the analytic point, to specify the endpoint issue.
Write h(u)=g(u-1) on [0,2). Every derivative has a finite nonnegative limit
at zero, because it is nonnegative and increasing and is bounded by its
value at any positive interior point. Taylor's theorem with nonnegative
remainder gives h^(m)(0)/m! <= h(r)/r^m for 0<r<2. Hence the series at zero
converges for u<2. More generally the same Taylor inequality at an interior
point v bounds derivatives there by h(r)/(r-v)^m for v<r. Taylor's remainder
then proves local analyticity (first in a sufficiently small neighborhood).
The series and h agree near zero by that remainder estimate and therefore
agree throughout (0,2) by analytic continuation along the interval. Continuity
settles u=0; convergence and termwise differentiation follow on smaller
compact intervals from the displayed coefficient bound. This is the classical
absolutely-monotonic-function theorem used in Cohn–Kumar, p.106, and
Cohn–Woo, §4.

For any two fixed finite configurations of distinct points all inner products
are below 1. Thus comparison for all g_k implies comparison for all such g
by termwise summation, or by uniform approximation. The same expansion can
be differentiated at the finitely many inner products when computing Hessians.

### Proposition 1 (global optimality through degree three)

C40 and C64 minimize E_g for every absolutely monotonic polynomial g of
degree at most three, among all N-point configurations on S^(n-1).

**Proof.** For a configuration D=(x_i), set T_l=sum_i x_i^(tensor l).
Then sum_(i,j)(x_i·x_j)^l=||T_l||^2. For l=1,3 this is nonnegative. For l=2,
T_2 is a PSD frame operator of trace N, so Cauchy–Schwarz gives
||T_2||^2>=N^2/n. Both codes attain all these bounds by §1.3. The expansion
of each (1+t)^k for k<=3 has nonnegative coefficients in t^l. Subtracting
the fixed diagonal N 2^k and dividing by two proves optimality for g_k.
Lemma 1, or Taylor's finite formula at -1, handles the stated polynomials. ∎

This does not establish even the unrestricted quartic case. The moment lower
bound for a degree-four term need not be attainable with these sizes.

## 3. An exact obstruction to two-point polynomial certificates

Let P_k^(n) be the normalized Gegenbauer polynomial with P_k^(n)(1)=1,
P_0=1, P_1=t, and

    (k+n-3) P_k(t)=(2k+n-4)t P_(k-1)(t)-(k-1)P_(k-2)(t).

Define the per-point moment S_k=1+sum_t m_t P_k^(n)(t); the double sum
over the whole code is N S_k. Direct rational evaluation gives, in degrees
1,2,3, the value zero for both codes. In degrees 4,5,6,7 the values are:

    C40: 280/297, 4480/2673, 32/33, 2240/3159;
    C64: 20928/22295, 46080/31213, 3689216/3714347,
         21795840/26000429.

There is also a uniform proof for every remaining degree, rather than a
finite-degree extrapolation. The Laplace integral representation of the
normalized Gegenbauer polynomial (DLMF 18.10.4 with parameter (n-3)/2) says

    P_k^(n)(t) = E[(t+i sqrt(1-t^2) U)^k],

where U is one coordinate of a uniform point on the unit sphere in R^(n-1).
Its even moments are

    E U^(2j) = product_(l=1..j) (2l-1)/(n+2l-3).

The integral formula can also be checked by expanding the integrand, using
these beta-integral moments, and recovering the displayed recurrence and
initial values. If |t|^2<=b and k>=8, then

    |P_k^(n)(t)| <= E[(t^2+(1-t^2)U^2)^(k/2)]
                  <= E[(b+(1-b)U^2)^4] = B.

The second inequality uses a base between zero and one. Taking b=1/4 for
C40 and b=9/49 for C64 gives respectively

    B40=19/858,             1-39 B40=3/22>0;
    B64=25307617/3458057057,
                            1-63 B64=266239598/494008151>0.

Hence S_k>0 for every k>=4 in both cases. The only zero positive-degree
moments are exactly degrees 1,2,3.

### Theorem 2 (no sharp polynomial two-point bound for the quartic)

For either code there is no polynomial h of any degree such that h(t)<=
(1+t)^4 on [-1,1), all its positive-degree Gegenbauer coefficients are
nonnegative, and the standard two-point linear-programming energy bound
from h is sharp at that code. The constant coefficient may be arbitrary.

**Proof.** If h=sum a_k P_k, the bound is

    E_g(D) >= (N^2 a_0-N h(1))/2.

Indeed E_g>=E_h and the omitted positive-degree double sums are
nonnegative by the harmonic addition formula. Sharpness at C requires both
h(t)=g(t) at every occurring inner product and a_k S_k=0 for k>=1. This
is exactly the equality argument of Cohn–Kumar Proposition 4.1. Since
S_k>0 for k>=4, all corresponding coefficients vanish and deg(h)<=3.
The nonzero quartic q=(1+t)^4-h is nonnegative on (-1,1). Each of its
zeros there has even multiplicity. C64 has three distinct interior contact
values, requiring at least six roots counted with multiplicity; C40 has four,
requiring eight. Both contradict deg(q)=4. ∎

The obstruction is to this certificate method, not to universal optimality.
It concerns attainment by a polynomial auxiliary function; it does not assert
that every conceivable infinite-series or higher-point certificate is impossible,
or that the supremum of a relaxation is separated by a specified positive gap.
Non-LP-universal behavior was already established by Boyvalenkov–Dragnev–
Hardin–Saff–Stoyanova (arXiv version Theorem 4.11; journal numbering differs).
The proof above gives a direct, all-degree, exact quartic attainment obstruction
without importing that paper's numerical table.

## 4. Universal strict local stability under moving one point

### Theorem 3

For either exceptional code, every point is a strict local energy minimum
when that one point is allowed to move on the sphere and all the others are
fixed, for every nonconstant completely monotonic potential f.

This is **not** a claim about simultaneous perturbations of several points,
nor about the global one-point relocation problem.

**Proof.** Fix x_i and write t_j=x_i·x_j, y_j=x_j-t_j x_i. The Hessian in
a tangent direction v of the one-point energy is

    Q_g(v)=sum_(j!=i) [g''(t_j)(v·y_j)^2-g'(t_j)t_j ||v||^2].

This follows by differentiating a great-circle path with initial velocity v
and acceleration -||v||^2 x_i. The first derivative vanishes by shell balance.

For k=1,2,3, the function sum_j g_k(z·x_j) is constant for unit z by the
3-design property. Removing the j=i term shows directly that

    Q_(g_k)(v)=g_k'(1)||v||^2=k 2^(k-1)||v||^2.

For k>=4 let s be the sole positive off-diagonal inner product and m its
multiplicity. For every vertex the following tangent-frame inequalities hold:

    sum_(j:t_j=s) (v·y_j)^2 >= L||v||^2,
    (s,m,L)=(1/6,24,2) for C40,
    (s,m,L)=(1/7,42,20/7) for C64.

These are finite exact matrix certificates. For full reproducibility, the
checker does not assume vertex transitivity. It verifies all 40+64 vertices.
If G=H/d, form V_ab=d H_ab-H_ia H_ib, which is d^2 times the tangent
Gram matrix. Select n-1 independent columns by exact positive-pivot
elimination, with index set I. For v=sum_(a in I)c_a y_a the desired
inequality is equivalent, after multiplying by d^4, to PSD of

    M_ab=sum_(j:t_j=s) V_aj V_bj-L d^2 V_ab,  a,b in I.

The checker verifies PSD by exact rational symmetric elimination, rejecting
any negative pivot or zero pivot with a nonzero remaining row. It outputs
each basis and every positive pivot. The residual rank is 6 for every C40
vertex and 7 for every C64 vertex. Thus the certificates cover all tangent
directions, not just coordinate directions or a numerical eigenvalue sample.

Since g_k',g_k'' are nonnegative and all other t_j<=0,

    Q_(g_k)(v) >= [L g_k''(s)-m s g_k'(s)]||v||^2
               = g_k'(s)[L(k-1)/(1+s)-ms]||v||^2.

At k=4 the bracket is 8/7 for C40 and 3/2 for C64, and it increases
with k. Thus every nonconstant power has a positive definite one-point
Hessian. Lemma 1 allows termwise differentiation and expresses Q_g as a
nonnegative sum of these forms. For nonconstant g at least one coefficient
with k>=1 is positive, so Q_g is positive definite. Smoothness and the
vanishing first derivative give a strict local minimum. ∎

## 5. Excluding the BBCGKS one-parameter 40-point rival

BBCGKS §4.1 describes a distinguished competitor family R_a, with
0<a^2<=1/27. The paper explicitly leaves the all-potential comparison with
C40 unproved. This section supplies a restricted computer-assisted comparison;
it does not classify or exclude arbitrary competing 40-point configurations.

### 5.1 Construction and exact pair distribution

Let u_1,...,u_4 and v_1,...,v_4 be unit regular tetrahedra in R^3. Put
w_ij=u_i tensor v_j in R^9. These 16 points have inner product -1/3 in a
shared row or column and 1/9 otherwise. For sigma in S4 define

    q_sigma=-(9a/4) sum_i w_(i,sigma(i)),
    z_sigma=q_sigma+sign(sigma) sqrt(1-27a^2) e,

where e is a unit vector orthogonal to R^9. The identities

    ||q_sigma||^2=27a^2,
    q_sigma·w_ij=-3a if j=sigma(i), and a otherwise,
    q_sigma·q_tau=9a^2(F(sigma,tau)-1)

follow by expanding tetrahedral dot products; F is the number of equal
positions of sigma and tau. They verify the BBCGKS construction and unit
norms. Distinct permutations have different projections when a!=0; the
w points and z points are also distinct. This remains true at a^2=1/27.

The full unordered pair distribution is

    inner product             multiplicity
    -1/3                       48
     1/9                       72
    -3a                        96
     a                        288
     36a^2-1                   72
     1-36a^2                   36
     1-27a^2                   96
     18a^2-1                   72.

The first two rows come from the 16 w points; the next two from the
16-by-24 cross pairs. For z pairs, the relative permutation types are a
transposition, double transposition, 3-cycle, or 4-cycle, respectively.
Counting them gives the last four rows. The checker independently enumerates
all unordered pairs in S4 and verifies these multiplicities. Their sum is 780.

Write D_k(a)=E_(g_k)(R_a)-E_(g_k)(C40). The C40 energy is

    E_(g_k)(C40)=160(1/2)^k+60(2/3)^k+80+480(7/6)^k.

### Theorem 4 (the entire explicit rival family is dominated)

For every 0<a^2<=1/27 and every completely monotonic f,

    E_f(R_a) >= E_f(C40).

The inequality is strict when g(t)=f(2-2t) is not a polynomial of degree
at most two. If g has degree exactly two, equality occurs exactly when
a^2=5/162. If g has degree at most one, equality always occurs.

**Proof.** First assume a>=0. Direct expansion gives

    D_0(a)=D_1(a)=0,
    D_2(a)=(80/9)(162a^2-5)^2.

For 3<=k<=99 we certify D_k(a)>0 on the larger closed interval [0,1/5].
The admissible interval is contained in it since 1/27<1/25. Here are all
details of the finite certificate, so positivity is not based on a graph,
floating-point minimization, or a grid of sample values.

Let P_k(a)=18^k D_k(a)=sum_(i=0..D)p_i a^i, with D=2k. From the pair
distribution its integer-coefficient polynomial is

    P_k(a)=48*12^k+72*20^k
           +96(18-54a)^k+288(18+18a)^k
           +72(648a^2)^k+36(36-648a^2)^k
           +96(36-486a^2)^k+72(324a^2)^k
           -160*9^k-60*12^k-80*18^k-480*21^k.

Its Bernstein coefficients on a in [0,1/5], multiplied by the common
positive factor 5^D D!, are the integers

    B_j=sum_(i=0..j) p_i 5^(D-i) i!(D-i)! binom(j,i).

If all B_j are positive, the polynomial is positive throughout the interval,
because Bernstein basis functions are nonnegative and sum to one. Otherwise
the checker subdivides at the midpoint by de Casteljau's algorithm. It uses
successive sums rather than averages, rescaling each child's coefficients
by the common positive factor 2^D. Positivity tests therefore use integers
only. Both child intervals are recursively covered.

For the 97 polynomials the resulting certificates contain 351 leaves in
total and have maximum depth 9. Every leaf has strictly positive coefficients.
The exact binary subdivision paths are saved in CHECK_RESULTS.json and can
be regenerated from the displayed polynomial alone. The paths partition
[0,1/5]; the checker also verifies the sum of their dyadic lengths is one.
This is a finite proof of the stated positivity over full intervals.

For all k>=100 a short bound replaces further computation. Put M=7/6.
Since M^100>300, the preceding C40 formula gives

    E_(g_k)(C40) < 481 M^k.

If a>=13/75, the 288 pairs with inner product a give

    E_(g_k)(R_a) >= 288(88/75)^k > 481 M^k,

because 288(176/175)^100>481 and 176/175>1. If a<=13/75, the 96
pairs with inner product 1-27a^2 give instead

    E_(g_k)(R_a) >= 96(743/625)^k > 481 M^k,

because 96(4458/4375)^100>481. All omitted summands are nonnegative.
The three numerical-looking inequalities in this paragraph are integer
inequalities after clearing denominators and are verified exactly.

For negative a, put b=|a|. Only the cross-pair contributions change. Their
difference is

    E_(g_k)(R_(-b))-E_(g_k)(R_b)
      =192 sum_(j odd, 1<=j<=k) binom(k,j)(3^j-3)b^j >=0.

Thus D_k(a)>0 for every k>=3 throughout the admissible parameter range,
and the stated low-degree identities hold for either sign.

Finally apply Lemma 1 to each fixed rival R_a. Summing the nonnegative
power gaps proves the inequality for every f. If some a_k with k>=3 is
positive the sum is strictly positive. Otherwise g has degree at most two;
the formula for D_2 gives exactly the stated equality cases. Multiplication
by the factors 2^k for the squared-distance normalization changes none of
these conclusions. ∎

## 6. A finite higher-point route and its exact remaining gap

The Hermite argument of Cohn–Woo Lemmas 9–10 supplies a sufficient finite
certificate problem. It is included to identify what a successful higher-point
proof would have to establish; it is not asserted solved.

List each distinct inner product r_1<...<r_m of a code twice, in sorted order,
as z_1,...,z_(2m). Define B_0(t)=1 and B_j(t)=product_(l=1..j)(t-z_l).
If C minimizes E_(B_j) for every 0<=j<2m, then C is universally optimal.

For completeness, let h be the Hermite interpolant of g, matching values and
first derivatives at the r_i. Its remainder at t is a nonnegative multiple
of product_i(t-r_i)^2 by the generalized Rolle remainder formula, so h<=g
on [-1,1). Its Newton expansion is sum c_j B_j with c_j>=0: each c_j is a
confluent divided difference of g, an average of a nonnegative derivative.
For example the divided difference with one fixed node r is
integral_(0..1)g'(r+u(t-r))du, whose derivatives are nonnegative; iterating
proves the claim, including repeated nodes by continuity. Consequently

    E_g(D)>=E_h(D)=sum c_j E_(B_j)(D)
                     >=sum c_j E_(B_j)(C)=E_h(C)=E_g(C).

This proves the sufficiency assertion. The first four B_j have nonnegative
coefficients in powers of t (their factors have nonnegative constants) and
degree at most three, so §2 already proves their optimality. The remaining
six explicit sufficient inequalities, with unordered-pair target values, are:

For every 40-point D on S^9, writing A(t)=(t+1/2)^2(t+1/3)^2,

    E_A(D)             >= 500/9,
    E_(t A)(D)         >= 80/9,
    E_(t^2 A)(D)       >= 40/27,
    E_(t^2(t-1/6)A)(D) >= 0.

For every 64-point D on S^13, writing B(t)=(t+3/7)^2(t+1/7)^2,

    E_B(D)             >= 12288/343,
    E_((t-1/7)B)(D)    >= 0.

The target values follow by substituting the exact distributions; the checker
reconstructs every basis polynomial and verifies them. None of these six
unrestricted inequalities has been proved here. Some basis polynomials are
not absolutely monotonic, so this is a **sufficient strengthening**, not an
equivalent reformulation. A failure of one would invalidate this choice of
Hermite basis but would not disprove the original conjecture.

The 2024 three-point SDP proof for the 288-point code in dimension 16 uses
a different Hermite multiset and exact SDP matrices. It does not supply
certificates for these six problems. No SDP certificate, PSD matrix rounding,
or simultaneous-deformation proof for C40 or C64 is claimed in this packet.

## 7. Conclusion and claim boundary

The attempted sharp-design route stops after cubic potentials. The entire
polynomial two-point sharp-bound route already fails for a quartic. A
one-point perturbation cannot destabilize either code for any nonconstant
completely monotonic potential, but collective motion is unaddressed. The
explicit BBCGKS 40-point rival family is rigorously excluded for the full
potential class. Six stronger finite polynomial energy inequalities offer
one possible next route, with no global certificates established here.

Neither original global universal-optimality claim is settled. The status
is **unsolved after five substantive approaches**, with the restricted
results and limitations above. These are AI-assisted unrefereed notes and
computer-assisted finite certificates, not formal proof-assistant verification
or external human peer review.
