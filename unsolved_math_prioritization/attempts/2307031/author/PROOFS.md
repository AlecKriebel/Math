# Smooth comparison failure and a counting bound for Hayman's double sums

## Status and notation

These are authored proofs of partial results for Hayman--Lingham Problem 7.31,
not a classification of every possible test function. Independent audit and
historical-priority review are pending.

Throughout, let a_1>0 and 0<=a_n<=n for every positive integer n, and put

    b_n = sum_{k=1}^n a_k,
    c_n = sum_{k=1}^n b_k = sum_{k=1}^n (n-k+1)a_k.

For a_n>0 write r_n=c_n/a_n. For a_n=0 set r_n=+infinity and f(r_n)=0.
All test functions below tend to zero at infinity. In particular r_n>=1
whenever it is finite. These conventions make zero terms unambiguous.

## Theorem 1  Completely monotone entire counterexample

There are a sequence satisfying a_1=1 and 0<=a_n<=n, and an entire function
f whose restriction to [0,infinity) is positive and completely monotone,
such that

    sum_{n>=1} f(n^2) <= sqrt(pi)/2 < infinity,
    sum_{n>=1} f(r_n) = infinity.

In fact (-1)^k f^{(k)}(t)>0 for every integer k>=0 and every t>=0.
Thus positivity, monotonicity, convexity, real analyticity, and even complete
monotonicity do not by themselves give the proposed convergence implication.

### An exact constant-ratio block

Fix an integer m>=2 and set q=m/(m-1). Suppose a finite prefix ends before
index m, with total mass B>0. Fill the unused indices through m-1 with zeros.
Then b_{m-1}=B and c_{m-1}<mB. At successive active indices starting at m,
define

    a_n = (c_{n-1}+b_{n-1})/(m^2-1),
    b_n = b_{n-1}+a_n,
    c_n = c_{n-1}+b_n.                       (1)

Every active term is positive and c_n=m^2 a_n, so r_n=m^2 exactly.
The auxiliary quantity W_n=c_n+m b_n satisfies

    W_n = q W_{n-1}.                         (2)

Indeed, the coefficients of c_{n-1} and b_{n-1} in W_n are respectively
1+(m+1)/(m^2-1)=q and (m+1)(1+1/(m^2-1))=qm.
Initially W_{m-1}<(2m)B. Since c+b<=c+mb for m>=1, the r-th active term
obeys

    a_{m+r-1} <= 2m B q^(r-1)/(m^2-1).      (3)

We will use q^m<=4. To check this for every real m>=2, the derivative of
x log(x/(x-1)) equals log(1+1/(x-1))-1/(x-1), which is negative; its value
at x=2 is log 4. Exponentiation gives the asserted inequality.

### Recursive construction of the sequence

Set a_1=1, and let the initial endpoint be E_0=1. At stage j>=1 let B_j
be the total mass of the already constructed prefix. Choose an integer m_j
such that

    m_j > E_{j-1},
    m_j >= 2,
    m_j^2 >= 16 B_j 4^(2^j).                (4)

Such an integer always exists, since the prefix and B_j are finite.
Put a_n=0 from E_{j-1}+1 through m_j-1. Starting at n=m_j, use (1) with
m=m_j for exactly

    L_j = 2^j m_j

terms. Set E_j=m_j+L_j-1, then proceed to the next stage. This specifies
a unique sequence after any fixed admissible rule for choosing m_j, for
example the least integer satisfying (4). Every prefix is finite and
rational. The endpoints strictly increase to infinity, so all indices
are eventually assigned.

For each active term in the j-th block, (3), q^L_j<=4^(2^j), and (4) give

    a_n <= 2m_j B_j 4^(2^j)/(m_j^2-1)
         <= m_j^3/[8(m_j^2-1)]
         <= m_j/6
         <= n.                              (5)

The penultimate inequality uses m_j^2/(m_j^2-1)<=4/3. Therefore the
construction respects the original cap at every index, without a limiting
or approximate correction. Every active index in block j has r_n=m_j^2.

### Construction and regularity of f

Define for complex z

    f(z) = sum_{j>=1} (2^(-j)/m_j) exp(-z/m_j^2).            (6)

On every disk |z|<=R, the absolute value of the k-th derivative of the
j-th summand is at most

    2^(-j) 2^(-2k-1) exp(R/4).

These bounds are summable in j. The series and each derivative therefore
converge locally uniformly. Consequently f is entire and may be
differentiated term by term. For real t>=0,

    (-1)^k f^{(k)}(t)
       = sum_{j>=1} 2^(-j) m_j^(-2k-1) exp(-t/m_j^2) > 0.

Dominated convergence also gives f(t)->0 as t->infinity. In particular
the convention f(+infinity)=0 is consistent.

### The convergent comparison series

For m>0, the function x->exp(-x^2/m^2) decreases on [0,infinity). Thus

    sum_{n>=1} exp(-n^2/m^2)
       <= integral_0^infinity exp(-x^2/m^2) dx
       = m sqrt(pi)/2.

Tonelli's theorem applies to the nonnegative terms in (6), and yields

    sum_{n>=1} f(n^2)
       <= (sqrt(pi)/2) sum_{j>=1} 2^(-j)
       = sqrt(pi)/2.                        (7)

### Divergence for the constructed double sums

At every active index in block j, the j-th summand of (6) gives

    f(r_n)=f(m_j^2) >= 2^(-j)/(e m_j).

There are L_j=2^j m_j such indices, so their combined contribution is
at least 1/e. The blocks are disjoint and infinitely many. Their sums
therefore diverge. This proves Theorem 1.

## Theorem 2  Uniform sublevel counting estimate

For T>=4 put m=sqrt(T), and let

    N_a(T) = #{n>=1 : a_n>0 and r_n<=T}.

Then

    N_a(T) <= ceil(m)-1
               +(2m+1) log( m^2(1+m)/a_1 ).               (8)

In particular N_a(T)=O_{a_1}(sqrt(T) log T), uniformly over all admissible
sequences with the specified a_1. This is a global count, not a bound on
the locations of the contributing indices.

### Proof

For this fixed real m>=2 define

    W_n=c_n+m b_n,     P_n=W_n/(n+m).

The sequence P_n is nondecreasing. For n>=2, the numerator of
P_n-P_{n-1}, after multiplication by its positive denominators, is

    (n-1)b_{n-1}-c_{n-1}
       +(n-1+m)(m+1)a_n,

which is nonnegative because c_{n-1}<= (n-1)b_{n-1}.
Also P_1=a_1.

Call n good when a_n>0 and c_n<=m^2 a_n. At a good index,

    (m^2-1)a_n >= c_{n-1}+b_{n-1}.

The same algebra as (2), now as an inequality, implies

    W_n >= [m/(m-1)] W_{n-1}.

If also n>=ceil(m), then

    P_n/P_{n-1}
       >= [m/(m-1)] [1-1/(n+m)]
       >= (2m-1)/(2m-2)
       >= 1+1/(2m).                        (9)

At every good index, c_n<=m^2 a_n<=m^2 n and b_n<=c_n, hence

    P_n <= m^2 n(1+m)/(n+m) <= m^2(1+m).   (10)

If K good indices have occurred with n>=ceil(m), monotonicity at all
other indices and (9) give, at the K-th such index,

    a_1 [1+1/(2m)]^K <= m^2(1+m).

The inequality log(1+x)>=x/(1+x), valid for x>=0 by differentiation,
therefore gives

    K <= (2m+1) log(m^2(1+m)/a_1).

This bounds every finite initial count and hence the entire count. There
are at most ceil(m)-1 remaining indices below ceil(m). This proves (8).

## Corollary 3  A sufficient class beyond power decay

Let f:[1,infinity)->[0,infinity) be locally bounded, eventually
nonincreasing, and tend to zero. If

    sum_{k>=1} (k+1) 2^(k/2) f(2^k) < infinity,            (11)

then sum_n f(r_n)<infinity for every admissible sequence.

For all sufficiently large k, each term with 2^k<r_n<=2^(k+1) is at most
f(2^k). Its count is at most N_a(2^(k+1)), bounded by a constant depending
on a_1 times (k+1)2^(k/2), by (8). The finitely many lower dyadic levels
contain only finitely many terms by (8), including any portion where f
is not monotone. Summing proves the corollary.

For eventually nonincreasing nonnegative f, criterion (11) is equivalently
the finiteness of

    integral_2^infinity f(t)(1+log t)/sqrt(t) dt.

To check equivalence, bound f on each interval [2^k,2^(k+1)] by its two
endpoint values, and note that the integral of (1+log t)/sqrt(t) over that
interval is bounded above and below by fixed positive multiples of
(k+1)2^(k/2). The two resulting series differ by one index shift and
bounded multiplicative factors.

In particular this proves convergence for

    f(t)=1/[sqrt(t)(log(e+t))^p],    p>2.                  (12)

These functions are not bounded by C t^(-alpha) for any alpha>1/2, so
this sufficient class extends the power criterion mentioned in the source.
No optimal claim about the exponent 2 in (12) is made.

## Proposition 4  The logarithm in the uniform count is necessary

For every integer m>=8 there is an admissible sequence with a_1=1 and

    N_a(m^2) >= m floor(log_4(m^2/16)).                    (13)

Thus, as a uniform bound over all such sequences, sqrt(T) log T has the
correct order, at least along square T. This does not assert that one
sequence realizes this bound at every large T.

Set a_1=1 and a_n=0 for 2<=n<m. Set

    h=floor(log_4(m^2/16)),   L=mh.

Apply the constant-ratio recurrence (1) from m for L terms, and then
set all remaining a_n=0. Here B=1, q^L<=(q^m)^h<=4^h<=m^2/16.
Exactly as in (5), every active term is at most m/6 and hence at most n.
All L active indices have ratio m^2. This proves (13).

## Two elementary obstructions to simpler proof routes

First, no universal pointwise lower bound r_n>=C n^2 is available, even
with a_1=1. For any integer N>=2, take a_1=1, a_N=N and all other terms
zero. Then c_N=2N and r_N=2. N can be arbitrarily large.

Second, a factorization

    c_n/a_n = (b_n/a_n)(c_n/b_n)

does not justify iterating a convergence statement for cumulative sums.
To see the obstruction concretely, set a_1=1 and

    a_{2*3^(j-1)}=2*3^(j-1),   j>=1,

and all other terms zero. Before the j-th active term the total mass is
3^(j-1), so b_n/a_n=3/2 at every active index. Therefore the series
sum_n g(b_n/a_n) diverges for any nonnegative g with g(3/2)>0. This says
nothing adverse about the source's stated theorem for c_n/b_n; it rules
out this particular attempted transfer to b_n/a_n.

## Scope not settled

Theorems 1 and 2 and Corollary 3 do not characterize all functions f for
which universal convergence holds. In particular the natural additional
shape condition that sqrt(t) f(t) be nonincreasing is not settled here.
Nor do these proofs decide the logarithmic family (12) for 1<p<=2.
Theorem 1 refutes the implication under the strong smoothness properties
explicitly listed; it does not refute the existential possibility of some
other regularity or shape assumption making the implication true.

The source's phrase about convergence together is interpreted as a
universal implication from the comparison series. A reverse implication
for each individual admissible sequence would already be false for a
finite-support sequence. No claim of novelty, priority, peer review, or
full resolution of the open-ended classification is made.

## Source

W. K. Hayman and E. F. Lingham, Research Problems in Function Theory
(New Edition), arXiv:1809.07200v2, Problem 7.31 and Update 7.31,
printed page 169 (PDF page 170), https://arxiv.org/abs/1809.07200.
The source is used to identify the problem and historical status, not as
a proof of any of the results above.
