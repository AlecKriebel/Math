# Turn 3: arbitrary row laws, flat tests, and the nonflat obstruction

2026-10-01. Third substantive author turn. This route uses arbitrary independent isotropic log-concave rows, with no unconditionality, latent representation or identical-law assumption. It proves the corrected sharp scale for a restricted coefficient class and identifies the precise deterministic loss in the attempted extension. The full maximal-submatrix conjecture remains unresolved.

## 1. A flat-test theorem for the actual row model

For1<=s<=n define the flat signed vectors

    V_s={u: support(u) has size s and u_i is +/-1/sqrt(s) on its support}.

Let U_m(N) be the m-sparse Euclidean unit vectors, and define

    F_(s,m)(A)=sup_(u in V_s, y in U_m(N)) |sum_i u_i <X_i,y>|.

This is at most A_(s,m), generally not equal to it. Put

    H=s log(2en/s)+m log(5eN/m).

There are universal C,c>0 such that for every v>=0,

    P(F_(s,m)>C[sqrt(H+v)+(H+v)/sqrt(s)]) <= 2 exp(-v).       (1.1)

In particular, if s>=m, writing

    Lambda_(s,m)=sqrt(m) log(3N/m)+sqrt(s) log(3n/s),

we have

    P(F_(s,m)>C[Lambda_(s,m)+sqrt(v)+v/sqrt(s)])<=2exp(-v).  (1.2)

Taking v comparable to H yields the corrected sharp-order bound with failure probability at most2exp(-cH). This covers all possible flat signs, row supports and m-column directions simultaneously for a fixed pair s,m.

## 2. Proof using only row independence and one-dimensional tails

Every centered variance-one log-concave scalar random variable has a universal subexponential norm. This is Borell's classical consequence, stated as equation(2.1) in the full2014 author manuscript *Tail estimates for norms of sums of log-concave random vectors*, Section2. A unit-direction projection <X_i,y> has exactly these assumptions.

For independent centered scalar variables Z_i with these uniform bounds, expansion of their moment generating functions gives

    E exp(theta sum_i u_i Z_i)<=exp(C theta^2 sum_i u_i^2)

whenever |theta| max_i|u_i|<=c. One may check this directly from E|Z_i|^p<=p! C_0^p for p>=2, summing the power series after the first-order term vanishes. Chernoff optimization for u in V_s therefore gives

    P(|sum_i u_i Z_i|>t)<=2exp[-c min(t^2,t sqrt(s))].        (2.1)

No coordinate independence within X_i appears here.

For each m-element column support I, choose a1/2-net of its Euclidean unit sphere with at most5^m points. For each fixed u, the supremum of the linear functional over that sphere is at most twice its maximum on the net. There are at most

    2^s binomial(n,s) binomial(N,m) 5^m <= exp(H)

signed-support/net pairs. Apply (2.1) to each pair and take a union bound. A sufficiently large universal multiple of sqrt(H+v)+(H+v)/sqrt(s) makes each tail at most2exp[-2(H+v)], which proves(1.1), including the factor two from the net.

For s>=m, the entropy terms satisfy

    sqrt(H) <= C[sqrt(s) log(3n/s)+sqrt(m) log(3N/m)],
    H/sqrt(s) <= C[sqrt(s) log(3n/s)+sqrt(m) log(3N/m)].

For the second inequality use m/sqrt(s)<=sqrt(m); all logarithms have a positive universal lower bound. Also sqrt(H+v)<=sqrt(H)+sqrt(v). This proves(1.2).

If s<m, the same elementary argument yields a column term m log(5eN/m)/sqrt(s), which can exceed the desired sqrt(m) log(3N/m). The proof does not silently claim sharpness there. The source's stronger order-statistic/projection estimates address that issue only with the known remaining losses in the full problem.

## 3. Why flat tests cannot be promoted to all coefficients by a constant factor

The obvious attempted next step is to approximate all sparse Euclidean unit vectors by a constant multiple of the convex hull of flat signed vectors of all support sizes. Such a dimension-free inclusion is false.

For k>=1 let z_j=1/sqrt(j),1<=j<=k. Then

    ||z||_2=sqrt(sum_(j=1)^k 1/j).

For any flat signed vector supported on s coordinates, the absolute pairing with z is at most

    (1/sqrt(s)) sum_(j=1)^s 1/sqrt(j) <=2.

The last inequality follows from1+integral_1^s t^(-1/2)dt=2sqrt(s)-1. Thus the one-column deterministic matrix z has full Euclidean norm tending to infinity, while all of its normalized flat signed tests remain bounded by2.

Equivalently, if u=z/||z||_2 is represented as a linear combination of flat signed atoms, the sum of the absolute coefficients must be at least ||z||_2/2. This is at least a constant times sqrt(log(k+1)). Therefore a generic atomic approximation or a triangle-inequality combination of uniform flat estimates necessarily incurs a growing loss.

This is a deterministic obstruction to the proposed proof mechanism. The displayed one-column matrix is not being claimed to have independent centered isotropic log-concave rows, and it is not a counterexample to the original random-matrix conjecture.

## 4. The elementary layer-cake loss is of the same order

Sort the absolute coordinates of an arbitrary k-sparse unit vector u as a_1>=...>=a_k>=0, put a_(k+1)=0, and retain its signs. Then exactly

    u=sum_(s=1)^k sqrt(s)(a_s-a_(s+1)) v_s,

where v_s is the flat signed vector on its first s coordinates. The coefficient sum is

    sum_s sqrt(s)(a_s-a_(s+1))
       = sum_s a_s(sqrt(s)-sqrt(s-1)).

Cauchy–Schwarz bounds it by

    [sum_s (sqrt(s)-sqrt(s-1))^2]^(1/2)
       <= [1+sum_(s=2)^k 1/s]^(1/2).

Together with Section3 this identifies the worst-case sqrt(log k) loss of this broad flat-atom step. This does not prove such a loss is necessary for the stochastic problem: independence and log-concavity might permit a different multiscale argument. It explains exactly why the present proof cannot discard all coefficient profiles after establishing(1.2).

## 5. What has and has not advanced

The positive result(1.2) directly addresses the original arbitrary row-law model, unlike the special representations in turns1–2. It proves the target order for every balanced flat row combination with row support at least the column sparsity. It does not control nonflat maximizing coefficients, nor the small-flat-support range at the desired scale.

The source's known full general-row estimate has only a sqrt(loglog) loss in one complexity term, so the naive layer-cake bound here is not an improvement over that theorem. We retain it as a rigorously diagnosed route rather than advertise an inferior bound as a new result. A remaining route must use a stochastic multiscale principle stronger than dimension-free flat-atom domination, or find an actual log-concave counterexample. The original is unresolved after3/5 substantive turns; two remain.
