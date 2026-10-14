# Stage 4: a bounded zero-mass certificate and exact clipping obstructions

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 4.

**Status.** The original random covering problem remains unresolved. This argument replaces the unbounded degree-201 polynomial by a bounded one-sided observable evaluated on the actual convolution, with no alteration of the translating set. It accommodates drift-free compound-Poisson laws, including parity/clustered laws, but no approximation theorem for unrestricted adaptive translates is asserted. At the required p^(3/4) expectation scale, a vanishing-parameter version is quantitatively equivalent to the optimal residual problem. Two exact typical-A constructions show why literal pointwise clipping or support-preserving deletion of a pencil cannot stand in for a factorization-preserving argument.

## 1. Exact model

For prime p, let k=floor(sqrt(p)), c=floor(100 sqrt(p)), and let A be uniform over all k-subsets of G=Z/pZ. For a translating set T define

f_T(x)=(1_A*1_T)(x),
U_T(A)=#{x:f_T(x)=0},
R_c(A)=min_{T subset G, |T|<=c} U_T(A).

All minima below allow arbitrary dependence of T on the whole A. We use the at-most-c domain explicitly. There is no assumption that the new observable is monotone when centres are added.

## 2. A bounded, one-sided observable

For 0<q<=1/2 and integers n>=0, put

g_q(n)=(1-n)q^n.

Then

g_q(0)=1, g_q(1)=0,
-q^2<=g_q(n)<=0 for n>=2.                         (2.1)

Indeed, (n-1)q^n starts at q^2 for n=2, and its successive ratio is nq/(n-1)<=2q<=1. In particular,

1_{n=0}-q^2 <= g_q(n) <= 1_{n=0}.                 (2.2)

Define the actual-convolution functional and its unrestricted optimum by

G_q(A,T)=sum_x g_q(f_T(x)),
B_q(A)=min_{|T|<=c} G_q(A,T).

No profile is replaced or assumed to be realizable: G_q is evaluated directly on 1_A*1_T, and the centre set and budget are unchanged. Large spikes contribute a bounded negative amount instead of the divergent polynomial contribution from Stage 3.

Every actual cover satisfies G_q(A,T)<=0, and hence

{R_c(A)=0} subset {B_q(A)<=0}.                     (2.3)

For each candidate T, and then for the minima over the same candidate domain,

U_T(A)-q^2p <= G_q(A,T) <= U_T(A),
R_c(A)-q^2p <= B_q(A) <= R_c(A).                  (2.4)

The passage to minima uses the pointwise inequalities, not monotonicity of g_q. The minimum of G_q over exactly c centres need not equal B_q. An exactly-c version separately satisfies the same sandwich because the residual minimum is unchanged by padding; we do not identify the two G_q minima.

## 3. An unrestricted concentration bridge, and its exact limitation

The single-step increment of g_q obeys

-1 <= g_q(n+1)-g_q(n) <= q^2, n>=0.                (3.1)

For n=0 it is -1; for n=1 it is -q^2; subsequent increments are nonnegative and at most q^2.

If A and A' differ by exchanging one point, let Q be their common (k-1)-set. For a fixed T of size m, adding either exchanged point changes the functional from G_q(Q,T) by a sum of m increments from (3.1). Either increment sum lies in [-m,mq^2]. Consequently

|G_q(A,T)-G_q(A',T)| <= m(1+q^2).

Taking a minimum over T preserves the common Lipschitz constant, so

|B_q(A)-B_q(A')| <= c(1+q^2).                     (3.2)

Expose a uniform k-set as an ordered sample without replacement and couple completions after two possible values by transposing them. The final samples differ by at most one exchange. Azuma therefore gives

Pr[B_q <= E B_q-u]
 <= exp[-u^2/(2kc^2(1+q^2)^2)].                   (3.3)

If E B_q>0, (2.3) implies

Pr[R_c=0]
 <= exp[-(E B_q)^2/(2kc^2(1+q^2)^2)].             (3.4)

Thus E B_q>=a c sqrt(k), for fixed a>0 along unbounded primes, would give a fixed positive failure probability along that subsequence. This is a fully adaptive sufficient bridge. Its expectation hypothesis has not been proved.

### The smoothing error at the required scale

From (2.4),

0 <= E R_c-E B_q <= q^2p.                          (3.5)

Since c sqrt(k) is asymptotic to 100p^(3/4), choosing

q=o(p^(-1/8))

makes the difference o(c sqrt(k)). For example, q=p^(-1/6) works eventually. At this scale, proving a positive constant-sized normalized lower bound on E B_q is essentially the same unresolved task as proving it for E R_c. Boundedness removes the high-spike failure of the raw polynomial; it does not independently provide the required expectation gap.

At fixed q, the q^2p comparison error is larger than p^(3/4), so (3.5) cannot transfer a merely p^(3/4)-sized lower bound on E R_c to a positive lower bound on E B_q. This distinction must not be hidden.

At the still smaller scale q^2p<1, integrality makes the reformulation exact: R_c=0 if and only if B_q<=0. Indeed, a noncover has R_c>=1 and hence B_q>=1-q^2p>0, while a cover gives B_q<=0 by (2.3). The bounded observable is not an independent existence proof merely because its sign encodes coverage.

## 4. Exact fixed-candidate expectation and the clustered-law extension

### 4.1 Fixed candidates: hypergeometric identity

Write H(N,K,b;q)=E[q^X] for X distributed hypergeometrically with population N, K marked elements, and b draws. For a fixed m-set T and uniform k-set A, every f_T(x) has the hypergeometric intersection law with parameters (p,k,m). Size bias gives

E[Xq^X]=(km/p)q H(p-1,k-1,m-1;q).

Therefore, for m>=1,

E_A G_q(A,T)
 =p[H(p,k,m;q)-(km/p)q H(p-1,k-1,m-1;q)].          (4.1)

The same identity holds for fixed A and a uniform m-set T. For m=0, G_q=p directly.

If k~sqrt(p), m~C sqrt(p), and q is fixed, the elementary hypergeometric point probabilities converge to Poisson(C), and g_q is bounded. Thus

p^(-1)E G_q -> exp[-C(1-q)](1-Cq).                (4.2)

This is strictly positive when q<1/C. It is a fixed-candidate expectation, not a lower bound on the expectation of the unrestricted minimum. In particular, exchanging minimum and expectation in the favorable direction is invalid.

### 4.2 Drift-free compound-Poisson laws

Let

Y=sum_{j>=1} jN_j,

where the N_j are independent Poisson variables with means beta_j>=0, and

lambda=sum_{j>=1} j beta_j <=100.

This is a drift-free compound-Poisson law. Its probability generating function is

F(q)=E[q^Y]=exp[sum_j beta_j(q^j-1)].

Differentiating the generating function, justified by the finite mean, yields

E g_q(Y)=F(q)[1-sum_j j beta_j q^j].               (4.3)

For 0<q<1/100,

sum_j j beta_j q^j <= q lambda <=100q,
F(q)>=exp[-sum_j beta_j]>=exp(-100).

Hence

E g_q(Y) >= (1-100q)e^(-100)>0.                   (4.4)

This includes laws such as twice a Poisson variable, so the parity obstruction to universal Poisson moment matching does not defeat this certificate. The bound also passes to mixtures whose conditional compound-Poisson means are each at most 100.

The **no-drift hypothesis is essential**. A law D+Y with deterministic integer D>=1 is zero-free and satisfies g_q(D+Y)<=0 pointwise. Nor does a mere unconditional mean bound on an arbitrary mixture license (4.4).

No result here states that the occupancy distribution of every adaptive convolution is drift-free compound-Poisson, or is close to such a law in any metric. Proving a suitable one-sided approximation for this single bounded observable could be useful, but the factorization and adaptive-uniformity theorem needed for that step is missing. Known low autocorrelation, small Fourier coefficients, or low moments do not establish it.

## 5. Literal clipping is not factorization-preserving, even at the exact cap

The previous certificate changes the observable, not the profile. This distinction is necessary.

Use the proved exact-size typical event

L(A)=max_{d!=0}|A intersect (A+d)| <=3r,
r=ceil(4 log p/log log p).

Its failure probability is at most p(e/r)^r=p^(-3+o(1)); see the self-contained p-cycle matching proof in Stage 2.

Fix any A on this event. Choose B uniformly among the (c-k)-subsets of G\\(-A), and put

T=(-A) disjoint-union B.

Then |T|=c and f_T(0)=k exactly, because B excludes all centres that cover 0. For x!=0,

f_T(x)=r_A(x)+|B intersect (x-A)|.

The latter variable is hypergeometric with population p-k, sample size c-k, and at most k marked points. A union bound over r draw positions gives

Pr[|B intersect (x-A)|>=r]
 <= [e(c-k)k/(r(p-k))]^r
 <= (101e/r)^r

for sufficiently large p. Union over x gives p(101e/r)^r=p^(-3+o(1)). Therefore there exists such a B, indeed a proportion tending to one of them, for which

f_T(0)=k,
max_{x!=0} f_T(x)<=M_p=4r<k.                      (5.1)

Consider the literal clipped profile

h(x)=min(f_T(x),M_p).

Only the value at zero is changed, and hence

sum_x h(x)=kc-k+M_p.

This integer is not divisible by k because 0<M_p<k. But every profile of the form 1_A*1_S has total mass k|S|, divisible by k. Consequently h is **not** 1_A*1_S for any set S, irrespective of its budget. It is not even a convolution with nonnegative integer centre multiplicities.

These translating sets are not asserted to cover G. This is a counterexample to replacing an actual convolution by its pointwise clipping and then silently treating the result as another feasible centre set. It does not invalidate applying a bounded observable such as g_q to the original f_T, or redistributing removed mass through a separately proved construction.

## 6. Support-preserving deletion cannot remove a typical pencil spike

A related deterministic step, deleting centres from a pencil while keeping its covered set unchanged, also fails to produce a light profile on typical A.

Define

D_1(A)={d!=0:r_A(d)=1}.

For sufficiently large p, in particular k>=2 and p>=2k+1, the following count applies. For a fixed nonzero d, the d-cycle has exactly one selected edge when r_A(d)=1. Choose that edge in p ways, exclude the two adjacent outside vertices, and choose the remaining k-2 nonadjacent selected vertices along the remaining path of length p-4. This gives the exact count

Pr[r_A(d)=1]
 =p binom(p-k-1,k-2)/binom(p,k).                  (6.1)

There is no overcount because the selected edge is unique. Thus

E|D_1(A)|=(p-1)p binom(p-k-1,k-2)/binom(p,k)
          =(e^(-1)+o(1))p.                        (6.2)

For the limit, rewrite (6.1) as

[k(k-1)/(p-1)]
 * binom(p-k-1,k-2)/binom(p-2,k-2).

The first factor tends to 1, and the logarithm of the second tends to -1 by its exact product formula.

Exchanging one point of A changes only differences involving the removed or inserted point, at most 4(k-1) nonzero difference values. Each indicator of multiplicity exactly one changes by at most 1. Hence |D_1(A)| is swap-Lipschitz with constant 4k. Uniform-subset Azuma and (6.2) give

Pr[|D_1(A)|<p/(2e)] <= exp[-Omega(k)].             (6.3)

Now take the pencil T_0=-A. Its convolution is r_A, and every d in D_1(A) is a private point of its unique representing translate. Each centre owns at most k such points, so at least

|D_1(A)|/k >= p/(2ek) >= k/(2e)

centres have a private point. If S subset -A satisfies

A+S=A-A,

it must retain every such indispensable centre. All pencil centres cover 0, so

(1_A*1_S)(0)=|S|>=k/(2e).                          (6.4)

Thus deleting centres from a typical pencil while preserving its entire covered set cannot achieve maximum multiplicity o(k). The obstruction holds in the exact random model, not only for exceptional algebraic examples.

This does not rule out replacing deleted centres by new centres, changing which points are covered, or a completely different construction. It isolates the precise failure of support-preserving *subfamily deletion* as a clipping device. The starting pencil has only k centres, already within the allowed at-most-c budget; the exact-cap obstruction is separately supplied by Section 5.

## 7. Outcome and remaining bridge

The bounded certificate g_q is a valid one-sided test of the original convolution, preserves the actual centre budget, and avoids the unbounded negative spike of fixed high-degree polynomials. It remains positive under drift-free compound-Poisson laws of bounded mean, so neither exact Poisson matching nor parity exclusion is required.

Nevertheless, no lower bound E B_q>=a c sqrt(k), no adequate one-sided adaptive compound-Poisson estimate, and no complete covering construction has been established. When q shrinks enough for the comparison error to be negligible, the E B_q problem reformulates the unresolved E R_c gap rather than solving it.

Literal clipping and support-preserving pencil deletion cannot be used to bypass that gap: Sections 5-6 give actual factorization obstructions on a high-probability class of A. These do not refute every possible budget-preserving replacement or bounded-observable argument.
