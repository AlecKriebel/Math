# Five approaches: proofs and exact gaps

All assertions below concern the explicit hypotheses stated here. None establishes maximum convergence on Bernoulli percolation clusters for every p>1/2. The finite-network facts and probability inequalities are elementary, and no novelty is asserted.

## 1. Homogenization does not make the maximum continuous

The direct route would infer the target from convergence of a rescaled field or of Green kernels away from the diagonal. The following obstruction shows why such an implication needs additional hypotheses.

### Proposition 1 (sparse centered Gaussian spikes)

For each N choose N distinct sites x_{N,1},...,x_{N,N} in V_N. Let Z_{N,i} be independent standard Gaussians, and let X_N(x_{N,i})=N Z_{N,i}, with X_N=0 at all other sites. All pairwise covariances are nonnegative. For every bounded test function f on [0,1]^2,

    A_N(f)=N^{-2} sum_{x in V_N} f(x/N) X_N(x)

converges to zero in L^2. Nevertheless, for every real K,

    P(max_{x in V_N} X_N(x) <= K log N) -> 0.

Proof. Independence gives Var A_N(f)=N^{-2} sum_{i=1}^N f(x_{N,i}/N)^2 <= ||f||_infinity^2/N. The mean is zero. If K>=0, the probability in the second assertion equals Phi(K log N/N)^N, which tends to zero since its base tends to 1/2. For K<0 it is zero because there are zero-valued sites when N>1. The same variance argument applies jointly to any finite collection of test functions. This also yields a Sobolev-space version: the random distribution N^{-1} sum_i Z_{N,i} delta_{x_{N,i}/N} on the two-dimensional torus has expected squared H^{-s} norm O(1/N) for s>1, because point masses have a common finite H^{-s} norm and the cross terms vanish. QED.

This is not a percolation GFF counterexample. Its sole implication is that even centered Gaussianity, nonnegative covariance, and vanishing density of exceptional sites do not make weak convergence of fields imply convergence of maxima.

Exact gap. For the actual cluster field, sharp near-diagonal covariance information and quantitative control at exceptional sites are needed. Theorem 1.9 of the cited preprint separates the all-supercritical homogenization assumptions (A.2)-(A.4), (B.2)-(B.3) from the near-one variance-defect requirements (A.1), (B.1). This package does not extend the latter requirements. Numbering refers specifically to the inspected arXiv v1; the publisher full text was not retrieved.

## 2. Elliptic regularization: a valid finite-volume step

Here is a network formulation that also handles components disconnected from the boundary before regularization. It avoids assigning a nonexistent Gaussian density to ungrounded components.

Let H be a finite graph with a nonempty grounded vertex set B, with all vertices connected to B in H. Give its edges conductances c_0(e)>=0 and c_epsilon(e)=c_0(e)+epsilon d(e), where d(e)>=0 and the positive c_epsilon network connects every vertex to B for epsilon>0. Let I be a nonempty union of whole c_0-open components in H\B, each of which reaches B by c_0-positive edges, and suppose there are no c_0-positive edges from I to the remaining interior vertices J. Let L_I be the positive-definite grounded Laplacian on I for c_0. Write C_0=L_I^{-1} and let C_epsilon be the restriction to I of the full c_epsilon-GFF covariance.

### Proposition 2 (finite-volume approximation and maximum transfer)

For each fixed network,

    0 < C_epsilon <= C_0 in positive-semidefinite order,
    C_epsilon -> C_0 as epsilon decreases to zero.

Consequently there is a Gaussian coupling X_0=X_epsilon+eta, where X_epsilon and eta are independent and Cov eta=C_0-C_epsilon. If m=|I| and delta=max_i (C_0-C_epsilon)_{ii}, then, for every t>0 and delta>0,

    P(|max_I X_0 - max_I X_epsilon|>t)
        <= 2m exp[-t^2/(2 delta)].                         (2.1)

For delta=0 the left side is zero. Thus for a sequence of such networks, the sufficient condition delta_N log(2m_N)->0 transfers any convergence-in-law result with the same centering from one coupled maximum to the other.

Proof. Let Q_epsilon be the full grounded Laplacian. Its Schur complement on I is S_epsilon, so C_epsilon=S_epsilon^{-1}. For a vector x on I,

    x^T S_epsilon x = min_y (x,y)^T Q_epsilon (x,y),

where y ranges over J; the minimum exists since Q_epsilon is positive definite. Dropping the nonnegative added-conductance energy and using the absence of c_0-open edges between I and J gives the lower bound x^T L_I x. For the upper bound set y=0. This gives

    L_I <= S_epsilon <= L_I+epsilon A

for a fixed positive-semidefinite matrix A, the energy of the d-network at (x,0). Inverting gives the covariance order and, in finite dimension, convergence. The difference C_0-C_epsilon is positive semidefinite, so the asserted independent Gaussian construction exists. The deterministic inequality |max(x+z)-max x|<=max |z_i| and a Gaussian tail union bound give (2.1). When delta_N log(2m_N)->0, for each fixed t>0 the right side tends to zero: its logarithm is log(2m_N)-t^2/(2delta_N). Slutsky's theorem completes the transfer. QED.

Application of the finite-volume assertion. In a fixed lattice box take I=S_N, J=V_N\S_N, keep open conductances one, and replace zero conductances by epsilon, including exiting edges. No open edge joins an infinite-cluster vertex to a finite-cluster vertex. Every I-component reaches the exterior. The hypotheses above therefore hold. This proves convergence of the restricted finite-box covariance and maximum as epsilon->0 for each N.

Exact gaps. The known fixed-epsilon theorem concerns the maximum over the entire box, not automatically its environment-selected subset S_N. A theorem for that restricted maximum is one missing step. Even with one, a sufficiently uniform estimate as both epsilon->0 and N->infinity would be needed. Fixed-N covariance convergence does not provide that estimate. For example, the deterministic family r_{N,epsilon}=N epsilon/(1+N epsilon) satisfies lim_epsilon lim_N r=1 whereas lim_N lim_epsilon r=0. Choosing epsilon_N separately small enough for each fixed-box coupling does not make a fixed-epsilon asymptotic theorem uniform along that sequence.

## 3. Pendant geometry and resistance

### Proposition 3a (tree attached at one vertex)

Take a finite grounded positive-conductance network K. Attach a finite tree at one vertex r of K, so that the tree has no other contact with K or the grounded set. Orient its edges away from r. For the GFF with energy (1/2) sum_e c_e(phi_u-phi_v)^2, the tree increments

    xi_e=phi_child-phi_parent

are independent centered Gaussians of variance 1/c_e and are independent of the entire field on K. The marginal field on K is exactly its GFF before the tree was added. Hence for a tree vertex v,

    Var(phi_v)=Var(phi_r)+sum_{e on r-to-v path} 1/c_e.

Proof. Transform the tree vertex variables into edge increments, leaving the variables on K unchanged. Ordering vertices from the root outward makes this linear transformation triangular with unit diagonal and Jacobian one. The energy is the sum of the K energy and (1/2) sum_e c_e xi_e^2. The Gaussian density therefore factors, with its normalization factoring as well. The variance identity follows from independence. QED.

For a unit-conductance pipe of L edges, the variance increase is exactly L. Pinning the tip, introducing another attachment, or replacing the exterior Dirichlet condition with an internal boundary changes this identity; none of those changes is permitted silently.

### Proposition 3b (a conditional percolation tail obstruction)

Fix p in (1/2,1), a>0, and assume explicitly that a vertex on the boundary of the half-plane {x_1>=0} has probability theta_H(p)>0 to connect to infinity using edges within that half-plane. This half-plane positivity hypothesis is left explicit; its proof is not part of this package.

For each environment define the extended nonnegative random variable

    T_0=max(0, sup_{N,w: 0 in V_N(w) intersect C_infinity}
                    [2*pi*a G_{N,w}(0,0)-log N]),

with empty supremum zero. Here G is the unnormalized grounded covariance, and N and w range over positive integer side lengths and lattice shifts. Set

    lambda(p)=-log[p(1-p)^2].

Then for every integer L>=1,

    P(T_0 >= 2*pi*a L-log(3L+1))
         >= theta_H(p)(1-p) exp[-lambda(p)L].             (3.1)

In particular, for every kappa>lambda(p)/(2*pi*a), E exp(kappa T_0)=infinity. No bound P(T_0>t)<=C exp(-kappa t) can hold for such a kappa.

Proof. Open the L horizontal edges from 0 to r=(L,0). Close the two vertical edges incident to each of (i,0), 0<=i<L, and close the horizontal edge from 0 to (-1,0). The L prescribed open edges and 2L+1 prescribed closed edges are distinct. Independently require r to connect to infinity inside {x_1>=L}; this event uses none of the prescribed edges. The joint probability is exactly theta_H(p) p^L(1-p)^{2L+1}. On this event the pipe belongs to C_infinity and attaches to the remainder only at r.

Use the box V_{3L+1}((-L,-L)); the whole pipe, including its root, lies in its interior. Proposition 3a gives G_{N,w}(0,0)=G_{N,w}(r,r)+L>=L, proving (3.1). Therefore

    E exp(kappa T_0)
       >= theta_H(p)(1-p)(3L+1)^{-kappa}
          exp[(2*pi*a*kappa-lambda(p))L],

which diverges as L->infinity when the stated strict inequality holds. For the claimed exclusion of a tail upper bound, compare it directly with (3.1), or choose an intermediate exponential moment exponent. The distinction between > and >= is removed by lowering each test threshold by a fixed positive constant. QED.

This is a conditional limitation on one type of local variance-defect estimate, not a counterexample to the maximum limit. With a=a_p, an exponential rate strictly above 2 would require lambda(p)/(2*pi*a_p)>2 (or at least a nonempty interval of compatible rates). No value or rigorous lower bound of a_p establishing the opposite inequality for a particular p is claimed here; even failure of this criterion would not disprove the conjecture by itself.

A related warning is exact: the resistance between endpoints of two disjoint unit-conductance paths of equal length L is L/2, while their shortest-path distance is L. This follows from the series and parallel laws, or from minimizing energy. Chemical distance can overestimate variance-relevant resistance. The check program verifies both identities with exact fractions.

## 4. Exceptional-site control gives a conditional first-order bound

The next proposition is deliberately weaker than centered-maximum convergence. It isolates what a one-point exponential moment can buy without assuming independence of field coordinates or defects.

### Proposition 4 (conditional upper bound)

Let X_N(v), v in an environment-dependent set I_N of at most N^2 sites in V_N, be conditionally centered Gaussian. Suppose nonnegative environment variables T_v (set to zero off I_N if necessary) satisfy, for N>=2,

    Var(X_N(v) | environment) <= log N + T_v,
    sup_{N,v} E exp(kappa T_v) <= C < infinity

for some kappa>2. The variables may instead depend on N, provided the same uniform bound holds. For every eta>0,

    P_annealed(max_{I_N} X_N > (2+eta)log N) -> 0.

Along N=2^j the corresponding quenched exceedance probabilities tend to zero almost surely. This proposition does not assert a quenched all-N statement.

Proof. Choose 0<eta'<=eta with r=(2+eta')^2/2<kappa. Such a choice exists because kappa>2. For s=log N and T>=0,

    1/(s+T) >= 1/s-T/s^2.

The centered Gaussian Chernoff bound, followed by this inequality at u=(2+eta')s, gives

    P(X_N(v)>u | environment)
       <= exp[-u^2/(2(s+T_v))]
       <= N^{-r} exp(r T_v).

Taking expectations, using r<kappa and T_v>=0, and summing over at most N^2 sites gives an annealed bound C N^{2-r}. It tends to zero since r>2. The event at eta is contained in that at eta'. On N=2^j these bounds are summable. If q_j is the quenched exceedance probability, Tonelli gives E sum_j q_j<infinity; hence sum_j q_j<infinity almost surely, and q_j->0. QED.

For the percolation normalization X_N=phi/sqrt(g_p), the hypothesis is a moment bound on the corresponding normalized diagonal variance defect. It has not been established here for every p>1/2. It also omits the covariance-difference component of the published general criterion.

Why this does not establish tightness. Even with T_v=0, using the same one-point union bound at

    u_N=2s-(3/4)log s+t

gives

    N^2 exp[-u_N^2/(2s)]
      = exp[(3/2)log s-2t-((3/4)log s-t)^2/(2s)],

which diverges as s->infinity for fixed t. This is an algebraic diagnosis of the bound, not a lower bound on the true exceedance probability. Correlations and the organization of near-maximizers are essential at the requested O(1) scale. No deletion of exceptional sites has been proved harmless at that scale.

## 5. Annealed convergence cannot replace the quenched target

### Proposition 5a (the forward implication)

If for almost every environment the conditional laws of Y_N converge weakly to the same deterministic probability measure mu, then their annealed laws converge weakly to mu.

Proof. For every bounded continuous f, the conditional expectations E[f(Y_N)|environment] converge almost surely to integral f dmu and are bounded by ||f||_infinity. Dominated convergence gives the same limit after averaging over the environment, which characterizes weak convergence. QED.

### Proposition 5b (failure of the converse, even for centered Gaussian laws)

Let the environment be independent fair bits B_1,B_2,... . Conditional on it, let Y_N be centered Gaussian with variance 1 if B_N=0 and variance 4 if B_N=1. The annealed law is the same probability measure (1/2)Normal(0,1)+(1/2)Normal(0,4) for every N. For almost every environment, however, both bits occur infinitely often. The quenched laws therefore have the two distinct subsequential limits Normal(0,1) and Normal(0,4) and do not converge.

Proof. The annealed calculation is immediate by conditioning on B_N. Independence and the Borel-Cantelli lemma imply infinitely many occurrences of each bit. Distinctness of the two laws follows, for example, from their characteristic functions exp(-t^2/2) and exp(-2t^2) at t=1. QED.

This example is outside the percolation model. It refutes only the logical inference from annealed convergence to the almost-sure quenched statement. A proof for the actual cluster model would require quantitative environment control, an appropriate concentration/ergodic argument, or a direct quenched construction. None is supplied by simply averaging first.

## Final remaining claim

For every fixed p in (1/2,1), prove that the actual zero-boundary cluster maximum minus b_N(p) has a nondegenerate limiting law for almost every percolation realization, including environments with rare high-resistance local defects. The preceding propositions neither furnish this conclusion nor rule it out. The exact missing estimates, and the order-of-limits and topology pitfalls, are now explicit.
