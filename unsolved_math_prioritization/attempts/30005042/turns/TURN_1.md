# Turn 1: first-moment fixed-point classification and integrated convergence

**Scoped partial, substantive author turn1/5. The original functional-limit and process-description bundle remains unresolved.** The argument uses classical Kesten–Stigum and a direct truncation estimate. No novelty is asserted. It improves the moment scope of the inspected manuscript's finite-second-moment fixed-point argument, but does not replace the source's J1 convergence request by a weaker topology.

## 1. Setup and the exact partial claims

Use the source's nondecreasing càdlàg integer-valued offspring process X on I⊂(1,infinity), with E X(lambda)=lambda, iid offspring-process copies at different individuals/generations, Z_0=1, and W_n(lambda)=Z_n(lambda)/lambda^n. We examine the natural weak hypothesis

    E[X(lambda) log^+ X(lambda)]<infinity, for every lambda in I.       (L)

No increment moment bound or finite variance is imposed. On a compact[a,b]⊂I, the endpoint X(b) dominates all earlier offspring variables and their X log X moments.

For a finite collection 1<lambda_1<...<lambda_d, let Psi act on probability laws on [0,infinity)^d by

    Psi(mu)=Law( lambda_i^(-1) sum_(r=1)^(X(lambda_i)) U_(r,i) : i=1,...,d ),

where the U_r are iid vectors with law mu, independent of the entire offspring vector. The same descendant vectors are used in all coordinates, as required by the source's coupling.

**Theorem A.** Psi has a law with finite coordinate means all equal to1 if and only if E[X(lambda_i)log^+X(lambda_i)] is finite for every i. If it exists, it is unique and equals the joint martingale-limit law. For every integrable mean-one seed law nu, Psi^n(nu) converges to it in the first Wasserstein distance associated with the l1 norm. Finite second moments are unnecessary.

**Theorem B.** Under(L), the original W_n converge in expected L1([a,b])-norm on every compact[a,b]⊂I to a jointly measurable version of their pointwise martingale limits. In particular they converge in probability as L1([a,b])-valued random variables.

Neither theorem asserts existence of a càdlàg limiting version or J1 tightness. Theorem A gives an abstract weak-moment law characterization, not a simple explicit description of the binary/geometric/Poisson limiting processes requested in the source discussion.

## 2. Coupled tree iteration and a first-moment averaging estimate

Attach iid copies of X to vertices of the countable Ulam tree. At parameter lambda a vertex has children numbered1 through X(lambda). The generation-n sets T_n(lambda_i) are nested in i. For each finite parameter collection, this construction has the same joint generation-count law as the source's recursion with generation-indexed iid arrays: condition on the current generation and order its vertices by their first appearance among the finitely many parameters, breaking ties by any rule using only the past. Their future offspring-process copies remain iid; the next counts are sums over nested initial segments of lengths Z_n(lambda_i). This is precisely the finite-dimensional transition rule of that recursion.

Place independent seed vectors U_u with law nu at the depth-n vertices of T_n(lambda_d), independently of the tree. Repeated root decomposition shows that the vector

    Y_(n,i)=lambda_i^(-n) sum_(u in T_n(lambda_i)) U_(u,i)              (2.1)

has law Psi^n(nu). The common mark at a leaf is used in every coordinate in which that leaf is present. This construction retains dependence between parameter values; separate marginal couplings would not suffice.

Here is the needed elementary estimate. Let V be any integrable mean-zero variable, independent copies being attached to a random finite set of size Z with E Z=m^n, independently of Z. For K>0 write

    zeta_K=V 1_(|V|<=K)-E[V 1_(|V|<=K)],
    rho_K=V-zeta_K.

Then zeta_K is centered with finite variance sigma_K² and

    E|rho_K| <= 2 E[|V| 1_(|V|>K)] = 2 epsilon_K.

Conditional Cauchy–Schwarz for the truncated sum and the triangle inequality for the remainder give

    E | m^(-n) sum_(r=1)^Z V_r |
       <= sigma_K m^(-n/2) + 2 epsilon_K.                (2.2)

Indeed E sqrt(Z)<=sqrt(E Z)=m^(n/2), and E Z/m^n=1. First let n tend to infinity, then K tend to infinity. The left side tends to zero, without any second moment of V and without any moment of Z beyond its mean. The same estimate applies conditional on the full tree to each random leaf subset in(2.1).

For V=U_i−1 and m=lambda_i, (2.2) yields

    E|Y_(n,i)−W_n(lambda_i)|
       <= sigma_(i,K) lambda_i^(-n/2) + 2 epsilon_(i,K) -> 0.          (2.3)

The seed law is fixed while n varies. Summing over the finite coordinate set proves convergence of this difference in expected l1 norm. No uniform claim over an uncountable parameter set follows from(2.3).

## 3. Proof of the mean-one classification

For each lambda_i, W_n(lambda_i) is a nonnegative mean-one martingale and converges almost surely to W(lambda_i). Classical Kesten–Stigum says its limit has mean1, and the convergence is in L1, exactly under the corresponding X log X condition. If that condition fails, the limit is zero almost surely. This scalar theorem is an established input, not a new result here.

Assume first that a mean-one integrable fixed law mu exists. Use mu as the seed in(2.1). Every Y_n then has law mu. Equation(2.3), which required only integrability of the seed and finite mean offspring, shows Y_n−W_n tends to zero in probability. The vector W_n converges almost surely in its finitely many coordinates, so the constant law of Y_n must equal the law of W. Hence each W(lambda_i) has mean1. Kesten–Stigum forces the X log X condition in every coordinate. This proves necessity and, at the same time, uniqueness among integrable mean-one laws.

Conversely, suppose all these moments are finite. Then the vector W_n converges in expected l1 norm. Its limiting law has coordinate means1. The usual root decomposition, now simultaneously in all d parameters, passes to the limit: the root has finitely many children at lambda_d almost surely, so only finitely many independent descendant limits are summed. Their joint laws are copies of the same limit vector and they are independent of the root offspring process. Thus its law is a fixed point of Psi.

Finally, for any integrable mean-one seed nu, couple Y_n with W_n as in(2.1). The expected l1 distance in(2.3) tends to zero, as does E||W_n−W||_1. Their sum bounds the first Wasserstein distance from Psi^n(nu) to the limit law. This proves Theorem A. The argument is iterative averaging, not a claimed one-step strict contraction in W1.

### All finite-mean fixed points

The same proof gives a complete finite-dimensional integrable classification. Let m_i be the finite nonnegative coordinate means of a fixed law. Coordinates with m_i=0 vanish almost surely. On the remaining coordinates divide by m_i and apply Theorem A to that subvector. A fixed law exists for this prescribed mean vector exactly when every positive-mean coordinate has finite offspring X log X moment; it is then unique and is the coordinatewise scaling of the canonical joint limit on those coordinates.

In particular the normalization must be prescribed at every parameter. At the level of finite-dimensional equations, multiplying a solution family by a deterministic finite nonnegative profile c(lambda) produces another such family; this does not assert that an arbitrary profile preserves càdlàg paths. The freedom is not restricted to one common scalar. Under(L), mean1 at every lambda determines all finite-dimensional laws. If a càdlàg process with those laws exists, its law on D is consequently determined. This conditional uniqueness is not a proof of such a version's existence.

## 4. Proof of integrated functional convergence

The W_n are jointly measurable in the probability variable and lambda: they are random càdlàg functions by the source construction. Define W(lambda) as their finite limit where that limit exists, and zero elsewhere. This is a jointly measurable nonnegative function. For each fixed lambda, martingale convergence identifies it with the usual limit almost surely; exceptional sets may depend on lambda.

Under(L), scalar Kesten–Stigum gives

    E|W_n(lambda)−W(lambda)| -> 0,
    E W_n(lambda)=E W(lambda)=1.

The integrand is bounded by2. Fubini and dominated convergence on[a,b] imply

    E integral_a^b |W_n(lambda)−W(lambda)| d lambda -> 0.              (4.1)

Also E integral_a^b W(lambda)d lambda=b−a, so the random function represents an L1([a,b]) element almost surely. Joint measurability and separability of L1 give the usual measurable random-element interpretation. Markov's inequality applied to(4.1) proves convergence in probability in L1([a,b]). This establishes Theorem B without assuming simultaneous pointwise convergence at every lambda or a càdlàg limit.

## 5. Why the source theorem is still not proved

L1 convergence does not imply Skorokhod J1 convergence. For example, on[0,1], the càdlàg functions

    f_n(t)=1_[1/2, 1/2+1/n)(t), n>=3,

have L1 norm1/n but cannot converge in J1 to zero. Any increasing onto time change retains their supremum1, and convergence to a continuous zero limit in J1 would require uniform convergence. This example is only a topology countercontrol; it is not claimed to arise from the source's offspring model.

The substantive unresolved step is J1 tightness of W_n under(L), or an admissible X satisfying(L) for which it fails. Pointwise, finite-dimensional, integrated and smoothing-law results cannot substitute for that step. The source's additional request for simple descriptions of the binary, geometric and Poisson limit processes also remains beyond the abstract classification given here.

Thus the original bundle is **unresolved after1/5 turns**. The route has a precise first-moment partial theorem and a precise topology gap. No complete-result publication is warranted at this stage.

## 6. Sources and attribution

- Mailler–Marckert, [Parametrised branching processes](https://arxiv.org/abs/2106.01426), Definition1.2, Proposition1.6, Theorem1.7, Lemma1.9, Section1.3 and Open question1. The manuscript already proves finite-dimensional convergence and finite-variance fixed-point uniqueness; those are credited, not relabeled as discoveries.
- Lyons–Pemantle–Peres, [Conceptual Proofs of L log L Criteria](https://arxiv.org/pdf/math/0404083), TheoremA, for the classical scalar mean-one criterion. The root decomposition and centered truncation estimate are standard probability arguments developed explicitly here for the coupled vector transform.
- [OWR12/2022](https://ems.press/content/serial-article-files/46949), pp592–593, for the actual two-part target. The final-full-text access caveat in SOURCE_GATE.md remains in force.

Exact finite controls check the coupled two-parameter recursion against independent tree decomposition and verify normalization and the truncation algebra. They do not establish the infinite limit theorem or fill the J1 gap.
