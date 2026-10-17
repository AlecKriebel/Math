# Stage 3: exact low-moment obstruction and a coverage certificate

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 3.

**Status.** The exact random translate-covering problem remains unresolved. This report establishes an obstruction to degree-at-most-99 moment methods and derives an explicit degree-201 polynomial inequality required by every cover. The inequality is violated by Poisson moments at mean 100, giving a precise possible bridge, but the cover-specific estimates needed to apply it have not been proved. A uniform positive-polynomial-expectation assertion over *all* translating sets is deterministically false.

## 1. Exact model and occupancy data

Let p tend to infinity through primes, k=floor(sqrt(p)), c=floor(100 sqrt(p)), and A be a uniform k-element subset of G=Z/pZ. For T subset G define

f_T(x)=(1_A*1_T)(x),
mu_j(A,T)=p^(-1) sum_x (f_T(x))_j,

where (z)_j=z(z-1)...(z-j+1), and mu_0=1.

Coverage is exactly f_T(x)>=1 for every x. For |T|=c, the mean is

lambda_p=kc/p -> 100,

with the exact total sum_x f_T(x)=kc and the deterministic bound 0<=f_T(x)<=k. For sufficiently large p, every smaller cover can be padded to size c, so a global negative argument may focus on |T|=c. Such padding is not automatically allowed in a localized light-remainder argument, because it may violate that argument's additional hypotheses.

The abstract profiles constructed below satisfy the occupancy bounds and total mass but are **not asserted to be additive convolutions**. This is an obstruction to reasoning solely from those numerical data, not a counterexample to the random-set problem.

## 2. A zero-free law matching the first 99 Poisson moments exactly

Let n=100 and let lambda>=sqrt(n(n-1)). Write

p_j=e^(-lambda) lambda^j/j!, j>=0.

Define a new probability law by

q_j=p_j-e^(-lambda)(-1)^j binom(n,j), 0<=j<=n,
q_j=p_j, j>n.                                      (2.1)

Then:

- q_0=0;
- q_j>=0 for every j;
- sum_j q_j=1;
- sum_j q_j (j)_r=lambda^r for 0<=r<=99.             (2.2)

**Positivity.** Odd-index corrections add mass. At an even j>=2, positivity is equivalent to

lambda^j >= (n)_j.

Pairing consecutive factors shows

(n)_j <= [n(n-1)]^(j/2) <= lambda^j.

At lambda=100 every q_j with j>=1 is strictly positive. The threshold sqrt(9900) is strictly below 100, so the exact cap mean lambda_p satisfies it for all sufficiently large p.

**Mass and moments.** For every polynomial R of degree less than n,

sum_{j=0}^n (-1)^j binom(n,j) R(j)=0.              (2.3)

This is the elementary nth finite-difference identity. Apply it to R=1 and R(j)=(j)_r. The correction in (2.1) changes neither total mass nor any factorial moment of order below 100. The Poisson factorial moments are lambda^r, proving (2.2).

The order-100 factorial moment does change: its correction is -e^(-lambda)100!, so the agreement is not an equality of all moments.

### Consequence for polynomial certificates

Suppose P is any polynomial of degree at most 99 with

P(0)=1 and P(j)<=0 for every positive integer j.

Since the q-law has zero mass at 0,

E_Pois(lambda) P(X)=E_q P(X)<=0.                   (2.4)

Thus no such polynomial can obtain a positive Poisson expectation at the target mean. Exact agreement of these 99 moments is compatible with no holes at all. The statement applies to coefficients chosen as a function of lambda as well: the moment identity is exact.

## 3. Bounded support and lattice-accurate profiles

The preceding obstruction does not rely on an unbounded tail. There is a fixed integer H and an open interval I containing 100 such that, for every lambda in I, a probability law supported on {1,...,H} has factorial moments lambda^r for every 0<=r<=99.

**Proof at lambda=100.** Start with the q-law from Section 2. Its masses at 1,...,100 are all strictly positive. Truncate above H>=101, without initially renormalizing. The lost factorial moments are

tau_r(H)=sum_{j>H} q_j (j)_r, 0<=r<=99,

and each tends to zero as H tends to infinity. Consider the square matrix

V_{r,j}=(j)_r, 0<=r<=99, 1<=j<=100.

It is invertible: falling factorials of degrees 0,...,99 form a polynomial basis, and evaluation at the 100 distinct points 1,...,100 is an invertible Vandermonde-type map. Solve

V b=tau(H).

Because V is fixed, every b_j tends to zero. For sufficiently large fixed H, |b_j|<q_j/2 for 1<=j<=100. Adding b_j to those 100 retained masses restores all 100 moment equations, including normalization, and keeps every mass positive. Other retained masses stay unchanged.

**Means near 100.** Keeping this same H, correct the masses at 1,...,100 by

V^(-1) ((lambda^r-100^r)_{r=0}^{99}).

This is continuous in lambda and tends to zero as lambda tends to 100. All masses therefore remain positive in some neighborhood I. The mass at 101 stays positive and unchanged. This proves the assertion.

This also strengthens (2.4): for all sufficiently large p, no degree-at-most-99 polynomial satisfying P(0)=1 and P(j)<=0 only on the finite occupancy range 1<=j<=k can have positive Poisson(lambda_p) expectation. The bounded-support law lies entirely inside that range and matches the moments exactly. This conclusion does not require its coefficients to be bounded or independent of p.

### Integer profiles with the exact floor-model total

For every sufficiently large prime p there exists a function

h_p:G -> {1,...,H}

such that

sum_x h_p(x)=kc,
p^(-1)sum_x (h_p(x))_r=lambda_p^r+O_H,r(1/p),
for every 0<=r<=99.                                (3.1)

To see this, use the finite law at lambda_p. Round p times its H masses down to integers and put the fewer than H leftover sites at value 100. This gives exactly p sites, and changes the total value from kc by an integer of absolute size O(H^2). The counts at values 100 and 101 are positive fixed proportions of p, uniformly for lambda near 100. Moving O(H^2) sites between these two values corrects the total exactly. Each of the finitely many factorial moments changes by O_H,r(1/p).

These profiles have no zero entries, have maximum H independent of p, satisfy H<delta k for every fixed delta>0 eventually, and have exactly the required total representation count. Their first 99 factorial moments are Poisson-like even at the natural O(1/p) empirical precision.

They are not claimed to factor as 1_A*1_T. That additional additive incidence structure is precisely information that a full argument must use if it works at this degree. Nor does approximate empirical agreement alone control polynomial combinations with arbitrarily growing coefficients; the exact finite-law argument above is the separate, stronger polynomial impossibility statement.

## 4. An explicit degree-201 certificate that genuinely uses coverage

The next construction shows that a higher fixed degree can distinguish the Poisson moment vector from zero-free occupancy. It is self-contained.

### 4.1 Orthogonal polynomial identities

For a positive integer M define

a_j=M^j/j!,
C_j(x;M)=sum_{ell=0}^j binom(j,ell)(-1/M)^ell (x)_ell.

These are rational polynomials. Their exponential generating function is

sum_{j>=0} C_j(x;M)t^j/j! = e^t(1-t/M)^x.

For X distributed as Poisson(M), multiplying two generating functions and taking expectation gives exp(st/M). Comparing coefficients proves

E[C_i(X;M)C_j(X;M)]=1_{i=j}/a_j.                   (4.1)

Thus q_j(x)=sqrt(a_j)C_j(x;M) are orthonormal. Direct coefficient comparison also gives

x q_j(x)=-sqrt(M(j+1))q_{j+1}(x)
         +(M+j)q_j(x)-sqrt(Mj)q_{j-1}(x).          (4.2)

Here q_{-1}=0. Finally,

C_j(0;M)=1,
C_j(1;M)=1-j/M.                                   (4.3)

### 4.2 The polynomial

Put a=a_{M-1}=a_M and define

Q_M(x)=sum_{j=0}^{M-1} a_j(1-j/M)C_j(x;M)
       + [a/(2M-1)]C_M(x;M).                      (4.4)

Its value at zero telescopes:

Q_M(0)=a+a/(2M-1)=2M a/(2M-1).                    (4.5)

To evaluate E[(1-X)Q_M(X)^2], use the Jacobi matrix from (4.2). Its first M coordinates have diagonal M+j and negative off-diagonal entries -sqrt(M(j+1)). The vector

v_j=q_j(1)=sqrt(a_j)(1-j/M), 0<=j<=M-1,

has eigenvalue 1 in that M-by-M principal block: the omitted next value q_M(1) is zero. The last coordinate of Q_M in the orthonormal basis is

b=sqrt(a)/(2M-1).

Extending the vector by b changes its quadratic form for I-J by

2 sqrt(a)b-(2M-1)b^2=a/(2M-1).                    (4.6)

The cross term uses v_{M-1}=sqrt(a)/M and the connecting coefficient M. Equations (4.1)-(4.6) therefore show

E[(1-X)Q_M(X)^2]=a/(2M-1)>0.

Normalize:

P_M(x)=(1-x)[Q_M(x)/Q_M(0)]^2.                    (4.7)

This rational polynomial has degree 2M+1 and satisfies

P_M(0)=1,
P_M(j)<=0 for every positive integer j,
E_Pois(M) P_M(X)=delta_M=(2M-1)/(4M^2 a)>0.         (4.8)

No numerical approximation is used for the sign.

At M=100, the degree is 201 and

delta_100=199*99!/(40000*100^99)>0.                 (4.9)

### 4.3 Exact necessary inequality for every cover

For every nonnegative integer-valued profile f, pointwise

1_{f(x)=0} >= P_100(f(x)).

Consequently

|G\\supp(f)|/p >= p^(-1)sum_x P_100(f(x)).         (4.10)

Every genuine cover T must therefore satisfy

p^(-1)sum_x P_100(f_T(x))<=0.                      (4.11)

This is a specific global moment inequality implied by full coverage. It is not merely a private-point or pair-overlap condition.

Write P_100(x)=sum_{j=0}^{201} b_j(x)_j. The coefficients b_j are fixed rational numbers specified by (4.4)-(4.7). Then (4.11) is

sum_{j=0}^{201} b_j mu_j(A,T)<=0.                  (4.12)

In contrast, sum_j b_j 100^j=delta_100>0. Since lambda_p tends to 100,

sum_j b_j lambda_p^j -> delta_100.                 (4.13)

For all sufficiently large p, any candidate with

sum_j |b_j| |mu_j(A,T)-lambda_p^j| < delta_100/4    (4.14)

has at least delta_100 p/4 holes, using (4.10)-(4.13). This reduces the earlier degree-399 sufficient Poisson bridge to an explicit degree-201 inequality. It does not establish the estimates in (4.14).

A global proof could seek this single weighted combination rather than estimate every moment separately, but the next section explains why an unrestricted claim over all candidates would be false.

## 5. Why the obvious uniform polynomial bridge is false

For every k-set A and sufficiently large p, choose a c-set T containing -A. Then f_T(0)=k. The leading coefficient of P_100 is strictly negative, and its degree is 201. At every other site, P_100(f_T(x))<=1. Hence

p^(-1)sum_x P_100(f_T(x))
 <= 1+P_100(k)/p -> -infinity.                    (5.1)

The last limit uses k^2/p->1. No probability or atypical-A event is involved. Thus the statement that this polynomial average is uniformly positive over all c-sets T is false for every A, and any unrestricted uniform moment estimate implying it is also false.

This T is not claimed to be a cover. A possible negative proof must instead establish an appropriate estimate using the *cover condition* or other necessary cover structure, or replace the raw polynomial by a correctly analyzed truncated/localized observable. The degree-201 certificate is a genuine necessary inequality and a precise conditional contradiction; it is not an accomplished full negative argument.

The same warning applies after merely imposing a diverging light cutoff. Choosing h points of a set z-A, with h a fixed fraction below the allowed cutoff, creates f(z)=h. Its high fixed-degree moments can dominate despite h<delta k. Removing only a fixed fraction of the maximal possible spike is not a bounded-support argument.

On a localized set H_X, the mean is not automatically lambda_p and may be as large as 100p/|H_X|. The fixed mean-100 polynomial expectation and global padding reduction above cannot be transferred there without additional work. All statements in Sections 1 and 4 concern the global averaging measure on G.

## 6. What this establishes and what remains

- Even exact first-99 Poisson factorial moments, bounded positive support, and the exact total representation count are compatible at the abstract profile level with no holes. This is a rigorous lower-degree obstruction, not a covering construction.
- Every cover satisfies the explicit degree-201 inequality (4.12); the Poisson target violates it by a strictly positive exact amount.
- High-multiplicity adaptive choices make a blanket positive-polynomial-expectation assertion impossible. A successful proof must supply genuinely cover-specific or correctly localized/truncated information.
- No theorem here proves that the finite-support profiles are realizable as 1_A*1_T, nor that a random A admits or excludes a cover. The remaining factorization and adaptive-uniformity questions are substantial.

## 7. Independent audit and exact checks

The public moment-certificate checker verifies exact algebraic identities and finite probability-law certificates. These checks do not establish convolution realizability, adaptive moment estimates, or the original probability limit; see the reproducibility guide for the included replay and its scope.

