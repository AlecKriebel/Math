# Turn 3: a self-contained subpolynomial upper bound

## Main result and its limitation

For the explicitly stated finite-prefix quantity M(D),

    log M(D)/log D -> 0 almost surely.                       (1)

Together with turn 1, this places its almost-sure growth between the credited polylogarithmic lower scale and every positive power of D. It does not determine log M(D)/log log D, supply a matching polylogarithmic upper bound, or resolve the broader quantitative question.

The proof adapts the flag-exposure method of Ford–Green–Koukoulopoulos, but uses only the constant diagonal subflag. The counting argument is provided here in full. It does not invoke the full finite-subflag reduction, the recent Mao–Song threshold identities, or an unverified uniform-in-k estimate.

Here is the quantitative fixed-k statement used to prove (1). Let k>=2 be fixed, put t_0=ceil(log_2 k), and suppose

    0<c<1,  delta=c(t_0+log 2)-log 2>0.

Then for all sufficiently large D,

    P(m(A intersect (D^c,D])>=k)
       <= exp(-delta log D+C_k(log D)^(3/4))
             +C(log D+2)exp(-(1/4)sqrt(log D)),              (2)

where the constant and starting point may depend on k,c. A change in the absolute constant C accommodates the harmless endpoint and harmonic-mean estimates. These probabilities are summable on D=2^n.

In particular, for each fixed integer r>=2 one can take c=1/r and k=2^r, because delta=1-(1-1/r)log2>0. The dependence on k is not controlled uniformly when r grows with D. That missing uniformity is one reason (1) is not a sharp polylogarithmic bound.

## 1. A regularity event with a summable exceptional probability

Write L=log D and I=(D^c,D] intersect N. Consider the O(L+2) endpoints consisting of D^c and the numbers D exp(-j) that are at least D^c, for nonnegative integers j. For each such t let

    N(t)=|A intersect (D^c,t]|.

Its mean is log(t/D^c)+O(D^{-c}), uniformly in the endpoints, by the elementary harmonic-sum estimate, and its variance is at most L+O(1). Independence and the Bernoulli exponential-moment bound give

    P(|N(t)-E N(t)|>L^(3/4))
       <=2 exp(-(1/4)sqrt L)                               (3)

for large D. A union bound over the endpoints gives the second term of (2), after increasing its constant. Let R_D be the event where all these deviations are at most L^(3/4).

For completeness the standard Bernstein estimate behind (3) follows from

    log E exp(lambda(X-p)) <= p(e^lambda-1-lambda)
       <= p lambda^2/[2(1-lambda/3)],  0<lambda<3,

for a Bernoulli variable X of mean p. The same upper bound works with -lambda. Multiply over the indicators and choose lambda=u/(mu+u/3), where mu is their total mean, to obtain the tail exp(-u^2/[2(mu+u/3)]). Set u=L^(3/4), mu<=L+O(1). This proves (3).

On R_D, counts in an interval between any two listed endpoints differ from its logarithmic length by O(L^(3/4)). Also |A intersect I|<=2L for large D. Removing at most k entries changes all these estimates by at most k.

## 2. Associate a complete flag to k equal-sum subsets

Fix a realization B=A intersect I in R_D and an ordered tuple of distinct subsets A_1,...,A_k of B with equal sums. For each a in B let

    omega(a)=(1_{a in A_1},...,1_{a in A_k}) in {0,1}^k.

Start with V_0=span_Q{1}, where 1=(1,...,1). Read a in decreasing order. Whenever omega(a) is outside the space generated so far, record that a as K_j, record omega^j=omega(a), and enlarge the space by omega^j. At the end we have

    K_1>...>K_t,   V_j=span_Q(1,omega^1,...,omega^j),
    dim V_j=j+1,  1<=t<=k-1.

Every omega(a) lies in V_t. Distinctness of the A_i implies that no pair of coordinates is identically equal on V_t. The k coordinate patterns across omega^1,...,omega^t are consequently distinct members of {0,1}^t. Hence

    k<=2^t,   t>=t_0.                                      (4)

Set

    c_j=[L+ceil(log K_j-L)]/L,  j=1,...,t,
    c_{t+1}=c,   S=sum_{j=1}^t c_j.

Then 1>=c_1>=...>=c_t>c, and

    D^{c_j}/e < K_j <= D^{c_j}.                             (5)

The endpoints D^{c_j} belong to the grid in Section 1. Ties among c_j are permitted; the corresponding interval is empty.

Remove the recorded entries and write B'=B minus {K_1,...,K_t}. If a in B' is larger than D^{c_1}, then omega(a) lies in V_0. If

    D^{c_{j+1}}<a<=D^{c_j},

then omega(a) lies in V_j. Indeed every vector outside V_j occurred at or below the next recorded entry K_{j+1}<=D^{c_{j+1}}. This is the support condition used below.

Let n_j be the number of residual entries in that interval and let mu_j be their empirical probability distribution on {0,1}^k intersect V_j. When n_j=0 use the point mass at zero. By R_D and the removal of at most k entries,

    n_j=(c_j-c_{j+1})L+O_k(L^(3/4)).                       (6)

## 3. There are only polynomially many coarse data

Encode the data Lambda by t, the recorded binary vectors omega^j, the integer bins defining c_j, and the integer frequencies n_{j,omega} for all residual type cells. There are only C_k(L+2)^{C_k} such data on R_D: t and the vectors have finitely many choices depending on k, every bin has O(L+2) choices, and every frequency is an integer between zero and 2L.

In particular no continuously varying probability measure is being union-bounded without discretization. The empirical mu_j and n_j are determined by these frequencies. We consider only data satisfying (4)–(6) and the stated support conditions. A deterministic choice of one witness tuple for each B may be made if desired; an upper union bound would also suffice.

## 4. Count the residual sums modulo the diagonal

For fixed Lambda and B', consider all possible residual assignments consistent with the data. Let

    ell=sum_{a in B'} a omega(a)+V_0 in Q^k/V_0.

Entries above D^{c_1} contribute zero in this quotient. For interval j, group binary type vectors by their coset modulo V_0. The number of assignments of these cosets to its n_j distinct entries is at most

    n_j! / product_x n_{j,x}!
       <= exp(n_j H_{mu_j}(V_0)),                          (7)

where H is the entropy of that coset distribution, with natural logarithms. Assignments of vectors within the same coset give the same contribution to ell; they do not introduce an extra factor. Every coset assignment determines one residual sum, so the number of distinct possible ell is at most the product of (7).

For a d-dimensional rational vector subspace, its intersection with {0,1}^k has at most 2^d elements: choose d coordinate projections that are jointly injective on the subspace. Thus

    H_{mu_j}(V_0)<=log|V_j intersect {0,1}^k|<=(j+1)log2.

Using (6), the number of possible residual sums is therefore at most

    exp(L sum_j(c_j-c_{j+1})H_{mu_j}(V_0)+C_k L^(3/4)).     (8)

Only this one fixed quotient is used. There is no need to classify all rational subflags or count projected lattice points with an unspecified support condition.

## 5. Recover the recorded entries and account for their probabilities

The equal-sum condition gives, in Q^k/V_0,

    sum_{j=1}^t K_j omega^j+V_0=-ell.                       (9)

Since 1,omega^1,...,omega^t are linearly independent, (9) determines at most one tuple (K_1,...,K_t) for every ell. Thus for fixed B' and Lambda, at most the number in (8) of original realizations B can arise.

The exact Bernoulli weights on the finite window give

    P(A intersect I=B)/P(A intersect I=B')
       =product_{j=1}^t 1/(K_j-1)
       <=(2e)^t D^{-S},                                   (10)

for sufficiently large D, using K_j>=D^c and (5). All recorded entries are distinct and absent from B'; no independence is applied to a repeated entry. The factors 1/(K_j-1), rather than 1/K_j, account for changing an unselected residual entry into a selected one.

Summing (10) over B', whose total probability is at most one, and applying (8), bounds the probability assigned to fixed Lambda by

    C_k exp(L[-S+sum_j(c_j-c_{j+1})H_{mu_j}(V_0)]
                                      +C_k L^(3/4)).        (11)

The residual frequencies encoded by Lambda already satisfy (6), so the bound applies to every B' admitting such an assignment, not only to an unverified conditional distribution.

## 6. A uniform negative exponent from the diagonal subflag

The elementary telescoping identity

    sum_{j=1}^t(c_j-c_{j+1})(j+1)=S+c_1-(t+1)c

and the entropy bound imply

    -S+sum_j(c_j-c_{j+1})H_{mu_j}(V_0)
       <=-(1-log2)S+(log2)c_1-(t+1)c log2
       <=log2-c(t+log2)
       <=-delta.                                         (12)

The second line uses S>=tc, c_1<=1 and 1-log2>0; the last uses t>=t_0. Thus the gap is explicit and uniform over all admissible empirical data. There is no appeal to compactness over infinitely many subflags.

Sum (11) over the polynomially many Lambda. Its extra O_k(log L) logarithmic factor is absorbed in C_k L^(3/4). Add the failure probability of R_D from Section 1. This proves (2).

This argument is closely related to the diagonal-subflag consequence of the FGK entropy framework and is credited as such. The point of providing the proof is to make the special support, multiplicity and weight steps verifiable without relying on all of the more general machinery.

## 7. Deduction of the almost-sure prefix upper bound

For disjoint finite sets B,C,

    m(B union C)<=2^{|B|}m(C),                             (13)

because each choice of a subset of B leaves at most m(C) choices in C for a fixed target sum. Fix r>=2 and put c=1/r, k=2^r. The two terms of (2) are summable on D_n=2^n: the first is eventually at most exp(-delta n log2/2), and the second is at most C(n+1)exp(-c_0 sqrt n).

Borel–Cantelli implies that almost surely, for all sufficiently large n,

    m(A intersect (D_n^{1/r},D_n])<2^r.

By (13),

    M(D_n)<2^r 2^{|A intersect [1,D_n^{1/r}]|}.

The elementary count law |A intersect [1,T]|/log T->1 almost surely, proved in turn 2, gives

    limsup_n log M(D_n)/log D_n <=(log2)/r.

Monotonicity fills the intervals between consecutive dyadic D_n, whose logarithms have ratio tending to one. Take a countable intersection over all integers r>=2, then let r tend to infinity. Since M(D)>=1, this proves (1).

This order of quantifiers fixes r and k before D tends to infinity. Substituting a growing r(D) into (2) would require new bounds on C_k and the starting threshold, and is not done.

## Remaining gap at 3/5

The lower bound is polynomial in log D, while the new upper bound is subpolynomial in D. This leaves a wide gap. The next search must control increasing multiplicity on many nested scales with uniform quantitative estimates, rather than treat k as fixed or replace (13) by a false multiplicative upper bound. No limiting log-log exponent or sharp constant has been established.
