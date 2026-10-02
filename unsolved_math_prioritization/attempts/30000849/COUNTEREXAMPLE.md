# A mass-budget obstruction to the displayed OWR normalization

Problem 30000849 / OWR-1729-002. Substantive author turn 1.

**Candidate conclusion, pending independent review.** The scaling limit displayed
in OWR46/2007, Conjecture1, printed p.2756, cannot hold for all its stated
parameters. Take p=1/4, alpha=1, omega=0 and c_j(0)=0 for every j. For every
positive finite size constant K, the prescribed scale is sigma(t)=K t^(4/5)
and the prescribed amplitude exponent is r=2/3. There is an actual global,
nonnegative, finite-mass classical componentwise solution for which no finite
normalizing constant A gives the stated positive interior profile.

The conclusion holds separately for the literal printed equations and for the
standard mass-conserving addition equations. It therefore does not depend on
exploiting the printed birth-coefficient typo. This is a correction to the
**displayed normalization**, not a proof or disproof of convergence under a
corrected normalization. No historical priority is asserted.

## 1. Exact target and the two systems

Write a_j=j^(1/4). In both systems the monomer equation is

    c_1' = 1 - c_1^2 - c_1 sum_{j>=1} a_j c_j.                  (1)

For j>=2, write

    c_j' = b_j c_1 c_{j-1} - a_j c_1 c_j.                    (2)

The two conventions are:

- Standard addition: b_j=(j-1)^(1/4)=a_{j-1}.
- Literal OWR display: b_j=j^(-3/4).

The latter is what is actually printed in equation(1), p.2754; its p=0
specialization conflicts with the coefficient1 used immediately afterward.
The former is the specialization a_j=j^p of the same author's general
addition system(123), 2015 survey, p.57. Neither convention will be silently
substituted for the other.

The conjecture's profile at these parameters is

    Phi(eta)=eta^(-1/4)(1-eta^(3/4))^(-2/3),  0<eta<1.         (3)

It is continuous and strictly positive on [1/4,1/2]. The source defines
c-tilde only by composing c_j with the inverse time change: there is no
hidden multiplication of c_j by j^p or sigma^p in that definition.

The unspecified source constant Q_p(omega) affects K only. Our obstruction
holds for **every** 0<K<infinity. A nonpositive or nonreal size constant does
not give the stated positive increasing real time scale. For the amplitude,
A=0 or A<0 cannot converge to (3) because c_j>=0. Thus it is enough to rule
out every 0<A<infinity. Even if a complex A were allowed, nonzero positive
real limits of A times nonnegative real numbers force A positive real.

Zero initial data satisfy the clean statement with rho=1 and mu=3, since
r+p=11/12. They also satisfy every polynomial upper bound, so the source's
undefined bare r in its initial-data condition cannot exclude these data.
The constant input1 is smooth at t=0; omega=0>-1/2 and p=1/4<1.

## 2. Actual infinite-system solutions

For each integer n>=2 retain c_1,...,c_n with equations(1)-(2), replacing
the monomer sum by its first n terms. Retain the loss from c_n and discard
clusters born beyond n. Set all initial values to zero. This is a finite
polynomial ODE with nonnegative constant coefficients b_j,a_j. At c_1=0
its first vector-field component is1; at c_j=0, j>=2, its jth component
is b_j c_1 c_{j-1}>=0. Hence its nonnegative orthant is forward invariant.

Let M_n=sum_{j=1}^n j c_j. Directly differentiating the **finite** sum gives

    M_n' = 1 +(2 b_2-2)c_1^2
             + c_1 sum_{i=2}^{n-1} [(i+1)b_{i+1}-(i+1)a_i]c_i
             -(n+1)a_n c_1 c_n.                             (4)

For standard addition this simplifies to

    M_n' = 1 -(n+1)n^(1/4)c_1 c_n <= 1.                     (5)

For the printed system, 2b_2-2=2^(1/4)-2<0, and the interior coefficients
are (i+1)^(1/4)-(i+1)i^(1/4)<0. The last inequality follows, for example,
by taking fourth powers of the positive quantities: i+1 < (i+1)^4 i.
Thus again M_n'<=1. Consequently

    0 <= c_j^(n)(t) <= t/j,     M_n(t)<=t.                   (6)

The finite solutions extend globally: on any bounded time interval all
coordinates remain bounded by(6), precluding a finite-time ODE blow-up.

Fix T<infinity. Put P_n(t)=sum_{j=1}^n j^(1/4)c_j^(n)(t). Since
j^(1/4)<=j, P_n<=T and c_1^(n)<=T. Thus

    |(c_1^(n))'| <= 1+2T^2,
    |(c_j^(n))'| <= T^2 [b_j/(j-1)+a_j/j]  (2<=j<=n).      (7)

For every fixed coordinate these bounds are independent of n. Apply
Arzela-Ascoli and diagonal extraction over coordinates and integer time
intervals [0,T]. There is one subsequence along which every coordinate
converges locally uniformly to a nonnegative continuous function c_j,
with c_j(0)=0. Finite partial sums and(6) imply

    M(t):=sum_{j>=1} j c_j(t) <= t.                          (8)

For L>=1, uniformly for t in[0,T] and n,

    sum_{j>L}^n j^(1/4)c_j^(n)(t)
       <= (L+1)^(-3/4) M_n(t) <= T(L+1)^(-3/4).             (9)

The same bound holds for the limit. Splitting each monomer sum into its
first L terms and its tail shows that P_n converges uniformly to
P(t)=sum_{j>=1}j^(1/4)c_j(t). In particular P is continuous. Passing to
the integral forms of each finite ODE now proves(1)-(2) for the limits.
Their right sides are continuous, so every c_j is C^1 on[0,infinity).
This proves existence of a genuine global classical componentwise
solution, not merely a formal balance or a finite-dimensional surrogate.

In fact c_1(t)>0 for t>0 by variation of constants in
c_1'+(c_1+P)c_1=1. Induction in(2) then gives c_j(t)>0 for all j and t>0.
Strict positivity is not needed for(8), but excludes a spurious zero
solution interpretation.

### Optional strengthening for standard addition

The standard solution above can be chosen with exact mass M(t)=t; the
counterexample is not a mass-losing solution selected through gelation.
Let S_n=sum_{j=1}^n j^2 c_j^(n). A second finite telescoping calculation is

    S_n' = 1 +2c_1 sum_{i=1}^{n-1} i a_i c_i
                 -(n^2+1)a_n c_1 c_n
           <= 1+2t S_n.                                   (10)

Therefore S_n(t)<=exp(t^2) integral_0^t exp(-u^2)du. Write H_T for the
finite maximum of this bound on[0,T]. Uniformly there,

    sum_{j>L} j c_j^(n) <= H_T/(L+1),
    (n+1)a_n c_1 c_n <= 2T H_T n^(-3/4).                   (11)

The first bound lets the full masses pass to the coordinatewise limit;
the second makes the integrated loss in(5) vanish as n tends to infinity.
Hence M(t)=t. Neither equality nor uniqueness is needed below.

## 3. A fixed-ray mass-budget lemma

The source states a limit along eta=j/sigma **fixed**. It does not assert
uniformity in eta. The following argument works under exactly that weak
reading; it uses no floor(j/sigma) replacement and no unproved Riemann-sum
limit.

Suppose nonnegative measurable functions c_j(t) satisfy

    sum_{j>=1} j c_j(t) <= C(1+t)^beta,  beta>=0,

and let sigma(t)=K t^s, K,s>0. Suppose for every eta in a fixed interval
[a,b] contained in(0,infinity), with 0<a<b, we have

    A(j/eta)^r c_j((j/(K eta))^(1/s)) -> Phi(eta)             (12)

as the integer j tends to infinity, where A>0 and Phi is measurable and
strictly positive almost everywhere on[a,b]. Then a necessary condition is

    s(2-r) <= beta.                                        (13)

Proof. Let t_j(eta)=(j/(K eta))^(1/s), and define the nonnegative integral

    I_j=integral_a^b j c_j(t_j(eta)) |t_j'(eta)| d eta
       = integral_{t_j(b)}^{t_j(a)} j c_j(t)dt.             (14)

Because |t_j'|=K^(-1/s) j^(1/s) eta^(-1/s-1)/s,

    I_j/j^(1-r+1/s)
       = K^(-1/s)/s integral_a^b
             eta^(-1/s-1) [j^r c_j(t_j(eta))]d eta.         (15)

Equation(12) gives pointwise convergence of the bracket to
A^(-1)eta^r Phi(eta). Fatou's lemma yields

    liminf I_j/j^(1-r+1/s)
       >= K^(-1/s)/(s A) integral_a^b
                       eta^(r-1/s-1)Phi(eta)d eta >0.      (16)

This integral may be infinite; positivity still gives a fixed d>0 and J
such that I_j>=d j^(1-r+1/s) for all j>=J. For integers n>=J, sum over
n<=j<2n. Any real exponent q satisfies sum_{n<=j<2n}j^q>=c_q n^(q+1),
where c_q=min(1,2^q)>0. The lower bound is therefore

    sum_{j=n}^{2n-1} I_j >= d c_q n^(2-r+1/s).              (17)

All the intervals in(14) lie within
[(n/(K b))^(1/s),(2n/(K a))^(1/s)]. Using nonnegativity and the moment
bound in the common interval, their sum is at most

    integral_0^{(2n/(K a))^(1/s)} C(1+t)^beta dt
       = O(n^((beta+1)/s)).                                (18)

If 2-r+1/s>(beta+1)/s, (17)-(18) contradict one another as n increases.
This proves(13). Tonelli is valid because all integrands are nonnegative;
only a finite band of j is summed. No convergence rate in(12) is assumed.

## 4. Applying the lemma and displaying the contradiction

For either solution constructed in Section2, take C=1,beta=1, and use
its stronger bound M(t)<=t. The conjecture at p=1/4,omega=0 has

    s=2/(3-2p)=4/5,
    r=1/[2(1-p)]=2/3,
    s(2-r)=16/15 > 1.                                    (19)

Apply Section3 on[a,b]=[1/4,1/2] with the positive profile(3).
Equation(13) fails. More concretely, here

    1-r+1/s=19/12,
    2-r+1/s=31/12,
    (beta+1)/s=30/12.

Fatou gives I_j>=d j^(19/12) eventually. Summing n<=j<2n gives at least
d n^(31/12). All those time intervals lie below
T_n=(2n/(K a))^(5/4), while their total integral is at most
integral_0^{T_n}t dt=(1/2)(2/(K a))^(5/2)n^(30/12).
The resulting bound n^(1/12)<=constant is impossible for unbounded n.

This proves that for every K>0 there is **no** positive finite A for
which the asserted fixed-ratio limit holds at every eta in[1/4,1/2].
It does not specify which particular eta fails and does not need to:
the conjecture asserts all of them. The same actual zero-data solution
works for all choices of K and A because its bound(8) is independent of
the proposed rescaling constants.

## 5. What is and is not settled

The answer to the literal displayed universal normalization claim is
negative, under either coefficient convention. Only one admissible p and
omega is needed to refute that universal claim. The p=0 published theorem
is unaffected: when p=0, the displayed exponents satisfy the mass scaling
identity s(2-r)=1+omega.

A necessary interior-amplitude threshold at our p=1/4,omega=0 is
r>=2-1/s=3/4. Thus replacing 2/3 by3/4 would remove this particular
mass-budget contradiction. It would **not prove convergence**, identify
the correct constants, or justify any proposed front profile or the
full parameter range. We make none of those claims. The role of changing
from the monomer clock to a cluster-size scale may explain the reported
exponent mismatch, but no authorial intent or unpublished corrected
formula is claimed. The general, correctly normalized physical
self-similarity question remains outside the conclusion.

All analytic arguments above are written out. The accompanying exact
checker verifies the finite telescopes, rational exponents, and a
mass-compatible positive-profile control; finite computation is not a
substitute for the compactness or Fatou arguments.
