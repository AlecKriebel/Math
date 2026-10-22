# Quantitative fixed-window gaps from exact local rerooting

Shared PASS4, row1778 /30005770. This sharpens the certified finite-K growth gap but does not establish adaptive-window sufficiency or the1324 permuton limit. Earlier accepted files are unchanged.

## 1. Definitions and accepted counting inputs

Let a_n=|Av_n(1324)|, lambda=lim a_n^(1/n), and

    gamma=log C(1/lambda),
    C(z)=(1-sqrt(1-4z))/(2z).

For K>=1 let b_(n,K) count avoiders with at most K canonical greedy cells, and let g_K=limsup b_(n,K)^(1/n). The exact directed cell kernel is the accepted PASS2 encoding.

Use the two accepted PASS3 counting facts below.

1. For each 0<eta<gamma there is a constant A_eta<infinity such that the number F_N(q) of size-N avoiders with first cell size at least q obeys

    F_N(q)<=A_eta lambda^N exp(-eta q)                        (1)

for all N,q>=1. This is the absolute, uniform frontier bound of pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md, Section B-C; its generating-function proof retains the exact descendant counts.

2. For any fixed marked cell after the first, of size q and with predecessor size p, the accepted rotation-plus-one-point construction maps it into a size-(n+1) avoider with first cell size at least q. The connector has at most n+1 possible inverse locations, and the omitted edge has at most binom(p+q,p) possible shuffles. Hence the number of such marked objects is at most

    (n+1) binom(p+q,p) F_(n+1)(q).                           (2)

This is the stronger unrelaxed fibre count explicitly proved in pass3_concentration_audit/REROOTING_ONE_POINT_BOUND.md. It preserves every other edge; there is no independent or uniform-remainder assumption.

Define the homogeneous entropy cost

    E(p,q)=(p+q)log(p+q)-p log p-q log q,                     (3)

with0 log0=0. Thus binom(p+q,p)<=exp E(p,q).

For a mass vector x=(x_1,...,x_K), with x_j>=0, sum x_j=1 and x_0=0, put

    V_eta(x)=max_(1<=j<=K) [eta*x_j-E(x_(j-1),x_j)],
    kappa_K(eta)=min_x V_eta(x).                             (4)

Zero trailing entries permit vectors with fewer than K nonempty cells. This is a deterministic profile optimization, not a random cell law.

## 2. Exact minimax recurrence

Set y_0=0. For each j>=1 define y_j as the unique positive solution on the increasing positive branch of

    eta*y_j-E(y_(j-1),y_j)=1.                                (5)

Then

    kappa_K(eta)=1/(y_1+...+y_K)>0.                          (6)

Proof. For p>=0 define R_eta(p,q)=eta*q-E(p,q). When p>0, R_eta(p,0)=0, its derivative in q is eta-log(1+p/q), and its second derivative is p/[q(p+q)]>0. Thus it initially decreases, then increases strictly to infinity. For any d>0, the inequality R_eta(p,q)<=d is equivalent to0<=q<=Q_eta(p,d), where Q is its unique positive root at level d. For p=0 this is just q<=d/eta. The root Q increases with p, since E increases with p, and is homogeneous: Q_eta(dp,d)=d Q_eta(p,1).

Given a normalized vector x, the first positive coordinate has zero predecessor and positive R_eta, so d=V_eta(x)>0. Inductively x_j<=d*y_j: it holds for j=1, and the monotonicity of Q gives it at the next coordinate. Summing yields1<=d sum y_j, hence d>=1/sum y_j. Conversely, the vector x_j=y_j/(sum y_i) is normalized and makes every local penalty exactly1/(sum y_i), by homogeneity of E. This proves (6), including the fact that padding a given vector with trailing zeros leaves its score unchanged. Increasing the allowed positive dimension can reduce the minimax value.

The functions y_j and kappa_K are continuous in eta>0 by the implicit equation on its strictly increasing branch. They are strictly positive for every fixed K. Formula(6) is the sharp guaranteed single-edge penalty for this particular profile-union reduction. It is not claimed to equal the true gap log(lambda/g_K), or to capture all possible joint constraints among edges.

## 3. Uniform finite count and fixed-K growth gap

For every n,K>=1 and0<eta<gamma,

    b_(n,K) <= A_eta lambda (n+1)^(K+1)
                  lambda^n exp[-n*kappa_K(eta)].             (7)

For each possible cell-size vector with at most K positive entries, choose a coordinate maximizing the penalty in (4), breaking ties deterministically. With p and q its adjacent sizes, the selected penalty is at least n*kappa_K(eta). If it is the first cell, apply(1) directly. Otherwise apply(2), then(1) and the entropy bound. Either way the count for that complete cell-size vector is bounded by

    A_eta lambda (n+1) lambda^n exp[-n*kappa_K(eta)].

The count bound does not require the output of the rotation to preserve the original size vector; it is an upper bound for the subset having that vector. There are at most(n+1)^K possible vectors, after padding with zeros. Summing proves(7). Every factor is explicit except the accepted fixed-eta frontier constant A_eta. In particular no hidden conditional completion weights have been suppressed.

For fixed K, divide logarithms by n and let n tend to infinity. Then let eta increase to gamma, using continuity in (6). This proves

    g_K <= lambda exp[-kappa_K(gamma)] < lambda.              (8)

Equation(7) is valid for varying K as a finite count, but it does NOT imply a useful normalized probability estimate for arbitrary growing K. The factor(n+1)^K and the unknown defect n log(lambda)-log(a_n) must both be controlled before making such an inference. Only fixed-K growth conclusions are asserted here.

## 4. Explicit exponential-in-K estimates

Let H(t)=(1+t)log(1+t)-t log t for t>=0, with H(0)=0. For eta>0 let t_eta>0 be the unique root H(t_eta)=eta, and put

    R=1/t_eta,  d=log(1+1/t_eta),  c=t_eta*d.

In our application eta<=gamma<=log2, while H(1/2)>log2, so t_eta<1/2 and R>2.

The recurrence(5) gives y_1=1/eta and, for j>=2,

    y_j > R*y_(j-1).                                        (9)

Indeed, positivity of R_eta(y_(j-1),y_j) requires H(y_(j-1)/y_j)<eta. Therefore

    y_j >= R^(j-1)/eta,
    kappa_K(eta) <= eta/(sum_(i=0)^(K-1) R^i).                (10)

For a lower bound, the concavity of H gives its tangent inequality at t_eta. After multiplication by q it reads

    E(p,q)<=d*p+log(1+t_eta)*q,
    eta*q-E(p,q)>=c*q-d*p.                                  (11)

Consequently y_j<=R*y_(j-1)+1/c, and

    y_j <= (1/c) sum_(i=0)^(j-1) R^i,
    kappa_K(eta) >= c/[sum_(j=1)^K sum_(i=0)^(j-1) R^i].      (12)

Since R>2, these upper and lower bounds have the same exponential order R^(-K). The denominator in(12) can be written explicitly as

    [R^(K+1)-(K+1)R+K]/(R-1)^2.

Thus(8) has a certified quantitative gap with a completely specified recurrence and explicit bounds. Optimizing a non-tangent affine bound is unnecessary to obtain its exponential scale.

## 5. A sharp limitation of this certificate

Even the exact kappa_K certificate does not automatically beat adaptive boundary entropy. The independent mass-profile lane studies this comparison directly. A quick upper envelope already follows from the test vector

    x_j=2^(j-1)/(2^K-1).

For j>=2 the local penalty is x_j[eta-H(1/2)]<0 when eta<=gamma<=log2, and the first penalty is eta/(2^K-1). Hence

    kappa_K(eta)<=eta/(2^K-1).                               (13)

The symmetric geometric profile with ratio1/2 has much larger boundary losses for containing-center windows than this available certificate. Its complete finite-profile and canonical-realization analysis belongs to the independent profile lane.

This limitation concerns the proved profile-union certificate. The true gap log(lambda/g_K) could be larger. Therefore it does not refute every adaptive-window approach, and no counterexample under the uniform avoidance law follows.

## Credited inputs and scope

The external staircase input remains Bevan, Brignall, Elvey Price and Pantone, Proposition1 and proof:
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

All new quantitative steps above are proved from accepted exact counts. There is no numerical growth extrapolation, no substitution of a biased remainder by a uniform one, and no assertion that a growing-K limit follows from fixed-K estimates. The universal target and its1324 case remain unresolved by this argument.
