# Turn 1: a literal counterexample and exact boundary-layer coupling cost

2026-10-02. Complete candidate counterexample to the **unnormalized entire-box statement as printed**. Independent mathematical and source-scope review pending. This does not claim a solution to an unstated normalized or buffered variant; indeed the example satisfies the normalized version.

## 1. Exact source and the limitation of the claim

Jeffrey Steif's Question A in OWR11/2020, printed p632, asks whether uniqueness of the Gibbs state makes the expected total number of disagreements inside the growing box uniformly at most epsilon for every boundary pair. The same paragraph says the property holds under Dobrushin uniqueness. https://ems.press/content/serial-article-files/46847 . There is no divisor by volume and no inner box in that statement. The imported record has the same wording.

The construction below has all the usual regularity properties: finite spins, strictly positive finite-range translation-invariant specification, uniqueness among all Gibbs states (including nontranslation-invariant ones), and a Dobrushin coefficient below1. Nevertheless its unnormalized coupling cost is bounded away from zero. Thus the printed unnormalized assertion, including its parenthetical claim about the Dobrushin regime, is false. The contradiction indicates a formulation/normalization issue; it must not be represented as resolving the author's possible intended normalized question.

## 2. A concrete specification

Work first on Z, with spins{-1,+1}. Set

    J=(log3)/2,     r=tanh J=1/2.

For any finite set Lambda, define the nearest-neighbor zero-field Ising kernel by

    gamma_Lambda^eta(sigma) proportional to
      exp[J * sum_{edges {i,i+1} meeting Lambda} s_i*s_(i+1)],

where s equals sigma in Lambda and the boundary configuration eta outside it. Exterior-only interactions are omitted. These kernels are proper and consistent: on conditioning a finite-volume law on a subset complement, all terms not involving the subset become a constant, and the remaining terms are exactly its specified Hamiltonian. They are strictly positive and depend on finitely many boundary spins, so the specification is quasilocal and finite-range. Translation invariance is immediate.

Introduce the stochastic matrix

    K(a,b)=(1+r*a*b)/2,

so K(a,a)=3/4 and K(a,-a)=1/4. Its powers are

    K^t(a,b)=(1+a*b*r^t)/2.

This follows by diagonalizing its constant and sign eigenvectors (eigenvalues1 andr), or induction. Because K(a,b)=exp(Jab)/(2cosh J), the Gibbs law in an interval of m sites with exterior endpoint spins a,b is exactly the Markov bridge

    mu_m^(a,b)(s_1,...,s_m)
      = K(a,s_1)*K(s_1,s_2)*...*K(s_m,b) / K^(m+1)(a,b).

All formulas are finite and have positive denominators.

## 3. Uniqueness among all Gibbs measures

The stationary two-sided Markov chain with stationary distribution(1/2,1/2) and transition matrix K exists and is Gibbs for this specification: its finite-interval conditional distribution given the exterior depends only on the two adjacent endpoints and is the bridge just displayed.

To prove uniqueness without assuming stationarity of an arbitrary Gibbs measure, fix a central interval[-l,l]. Its marginal inside the bridge on[-n,n] with arbitrary endpoint spins a,b is, for x=(x_-l,...,x_l),

    K^(n-l+1)(a,x_-l)
       * product_{i=-l}^{l-1} K(x_i,x_(i+1))
       * K^(n-l+1)(x_l,b)
       / K^(2n+2)(a,b).

As n tends to infinity, the formula for K^t shows uniform convergence over the four endpoint pairs to

    (1/2) * product_{i=-l}^{l-1} K(x_i,x_(i+1)).

If nu is any Gibbs measure, its central marginal is the average of the preceding finite-volume marginal over its exterior boundary, by the DLR equation. Uniform convergence therefore forces the same limit for every nu. Every finite cylinder probability is fixed, so nu equals the stationary Markov-chain measure. Thus uniqueness holds among all Gibbs measures.

## 4. The Dobrushin coefficient is exactly4/5

Given neighboring spins a,b, the conditional plus probability at a site is

    P(+ | a,b)=exp(J(a+b))/(2cosh(J(a+b))).

For a+b=-2,0,2 these probabilities are1/10,1/2,9/10. Flipping either single neighbor can therefore change the one-site law in total variation by at most2/5, attained when the other neighbor is fixed. Other sites have zero influence. The row sum of the Dobrushin influence matrix is consequently4/5<1. This is a direct computation, and uniqueness above does not rely on invoking the Dobrushin theorem.

## 5. A uniform lower bound for every coupling

Take plus boundary a=b=+1 and minus boundary a=b=-1. Let mu_m^+ and mu_m^- be the respective interval laws. Spin-flip symmetry sends one to the other.

For1<=k<=m, bridge multiplication gives

    E_mu_m^+[s_k]=(r^k+r^(m+1-k))/(1+r^(m+1)),
    E_mu_m^-[s_k]=-E_mu_m^+[s_k].

To verify the first formula, sum t*K^k(+,t)*K^(m+1-k)(t,+) over t=+/-1 and divide by K^(m+1)(+,+).

For any coupling(X,Y) of these laws, the mismatch probability at site k is at least the total-variation distance of its two one-site marginals, namely E_mu_m^+[s_k]. Hence every coupling satisfies

    E[number of mismatches]
      >= sum_{k=1}^m (r^k+r^(m+1-k))/(1+r^(m+1))
      = 2r(1-r^m)/[(1-r)(1+r^(m+1))].

Even the first term is at least r: (r+r^m)/(1+r^(m+1))>=r. At r=1/2, choosing epsilon=1/4 therefore defeats the proposed property for every interval length, not merely along a subsequence. For the centered n-box[-n,n], m=2n+1.

## 6. The lower bound is the exact Wasserstein cost

The preceding sum is attained by a monotone coupling of the two bridges. Sample from left to right. If the previous spin is s and the right boundary is b, the transition at position k is

    P(s_k=t | s_(k-1)=s, right boundary b)
      = K(s,t)*K^(m+1-k)(t,b) / K^(m+2-k)(s,b).

Its plus probability is increasing in both s and b. Indeed its odds ratio is

    [(1+r*s)/(1-r*s)] * [(1+b*r^(m+1-k))/(1-b*r^(m+1-k))],

and each factor increases when its sign argument increases. Couple the two sequential samples by using the same independent uniform random variable at each position, starting with the ordered left boundary pair(+1,-1), and using right boundaries(+1,-1). Induction gives X_k>=Y_k at every site. Each mismatch indicator is then(X_k-Y_k)/2, so its expected value equals the marginal lower bound. Both marginal laws are the correct Markov bridges by their displayed transition kernels.

Therefore the exact unnormalized Hamming-Wasserstein distance is

    W_H(mu_m^+,mu_m^-)
       =2r(1-r^m)/[(1-r)(1+r^(m+1))].

At r=1/2 this is2(1-2^(-m))/(1+2^(-m-1)), tending to2, and already equals4/5 at m=1.

## 7. Every dimension, if desired

For Z^d use the same interaction only along edges parallel to the first coordinate, with zero coupling in the other directions. This is still translation invariant, finite range and strictly positive, and every site's influence sum is4/5. A Gibbs specification in a finite box factors into its one-dimensional row bridges.

The product of stationary row chains is a Gibbs measure. Uniqueness among arbitrary measures follows by applying the uniform bridge convergence simultaneously to any finite set of rows/cylinders in larger boxes: every finite-volume conditional law factorizes, and its finite-cylinder limit is the same product uniformly in all boundaries. The DLR averaging argument thus fixes every cylinder law.

In the box[-n,n]^d, with m=2n+1, there are m^(d-1) rows. The one-site lower bounds add over all rows, and independent copies of the monotone row coupling attain them. Thus plus/minus boundaries have exact cost

    W_H = m^(d-1) * 2r(1-r^m)/[(1-r)(1+r^(m+1))].

It tends to2 in dimension1 and grows like2*m^(d-1) in higher dimensions at r=1/2. No restriction in the printed question requires rotation-invariant interactions.

## 8. What the example does not refute

After dividing by the box volume m^d, this exact cost is

    2r(1-r^m)/[m(1-r)(1+r^(m+1))] -> 0.

Hence the example is NOT a counterexample to a normalized-average-disagreement question. Likewise, removing a boundary layer of diverging width changes the conclusion: for an interval retaining sites at distance at least b from either endpoint, the sum is bounded by2*r^b/(1-r), which tends to zero as b tends to infinity. The printed statement includes neither modification.

Final candidate scope: complete negative answer to the literal unnormalized entire-box formulation, with an explicit warning that its Dobrushin parenthetical signals a possible missing normalization/buffer. No full answer to an unstated repaired problem and no historical novelty is claimed. One substantive author turn consumed. The literal mathematical target's completion estimate is100% pending separate review; this is a planning estimate, not confidence or peer-review certification.
