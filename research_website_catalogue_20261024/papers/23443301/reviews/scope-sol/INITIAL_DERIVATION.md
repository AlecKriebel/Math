# Source-only independent reconstruction

This artifact was written after reading the complete published 288-line TeX, the complete freshly extracted four-page PDF text and four freshly rendered original pages. Current peer/root science, archived README/audit/acceptance/result bodies and external primary bodies remain closed at this checkpoint. Source claims about earlier audits, priority and inaccessible literature are author assertions, not evidence supplied by those audits. My previous role was source acquisition: opaque extraction, hashes, metadata and filenames, not mathematical review.

## Exact claim and normalization

Let n,d be integers at least one. Let f,g be nonzero real multilinear functions on the independent uniform sign cube, of degree at most d. For a, write N_a=E[a²] and rho_i(a)=sum_{S containing i} a_hat(S)²/N_a. The constant coefficient is included in N_a. Walsh orthogonality gives N_a>0 and the formula for rho; in particular 0≤rho_i≤1. Nonzero is a function condition equivalent to a nonzero multilinear coefficient vector. Products are tested as functions at vertices, not as unreduced ordinary polynomials.

The full original theorem is: f(x)g(x)=0 for all vertices implies delta=max_i max(rho_i(f),rho_i(g))≥1/(1024 d^8). Its stated consequence is that delta≤1/(4096 d^8) implies a common nonzero vertex. It allows arbitrary common zeros, constant terms, n<d and unequal actual degrees. It asserts neither optimal constants/exponent, a polynomial-time algorithm, general input measures/groups nor historical firstness. No theorem is being repaired or narrowed here.

## Endpoint derivative bound without relying on an unread primary

For a degree-at-most-m real polynomial Q on [-1,1], m≥1, bounded by one, interpolate at x_j=cos(j*pi/m), j=0,...,m. Let ell_j be the degree-m Lagrange basis. For j>0, ell_j'(1) has sign (-1)^j: its numerator is a product of positive factors 1-x_k, while its denominator has exactly j negative factors x_j-x_k. Also ell_0'(1)=sum_{k>0}1/(1-x_k)>0. Since the Chebyshev polynomial T_m takes value (-1)^j at x_j,

    sum_j |ell_j'(1)| = sum_j (-1)^j ell_j'(1) = T_m'(1) = m².

The last equality follows from T_m(cos theta)=cos(m theta) and the limit m sin(m theta)/sin theta→m². Thus |Q'(1)|≤m². For P(t)=Q(1-2t), |P'(0)|≤2m². This is only the classical endpoint Markov bound, reconstructed here, with no novelty claim. The case m=0 is immediate.

If R on {0,1}^b has degree≤m, |R|≤1, R(0)=1, R(e_j)≤0, its Bernoulli(t) expectation P has degree≤m: first use its multilinear representative and replace every monomial of size k by t^k. The expectation remains between -1 and 1. Differentiating the finite mass formula at zero yields P'(0)=sum_j(R(e_j)-1)≤-b. Hence b≤2m². No dimension-dependent derivative bound or numerical approximation is used.

## Total separator and its query depth

Apply the affine sign/bit conversion, which preserves degree, nonzeroness, support disjointness and decision-tree query depth. At each restricted subcube:

1. If p=0, assign output0; if q=0 but p≠0, assign output1. If both vanish, output0 is a fixed total convention. Thus common-zero vertices never leave the tree partial.
2. Otherwise both restrictions are nonzero. Neither can be a nonzero constant, since that would force the other to vanish everywhere. Let D=max(deg p,deg q)≥1 and s be the multilinear representative of p²-q², of degree≤2D. A vertex maximizing |s| has positive absolute value, since the supports are disjoint and at least one function is nonzero. Suppose p is nonzero there; then s(z)>0 and q(z)=0. The other case is symmetric.
3. Select an inclusion-maximal disjoint family M_1,...,M_b of supports of maximum-degree monomials of q. Every M_j has size deg q, and its top coefficient survives fixing all outside variables to z: a competing contribution to that entire support would need a strictly containing monomial, forbidden by maximal degree. The restricted q is therefore a nonzero function on M_j. Its value at z is zero, so some nonempty flip E_j⊆M_j makes it nonzero. Disjoint support then makes p=0 and s<0 there.
4. Encode the disjoint E_j flips with b bits. Each original coordinate is constant or affine in one bit; reducing powers on the bit cube cannot increase degree. Dividing by s(z)=max|s| gives R with degree≤2D, |R|≤1, R(0)=1 and R(e_j)<0. The endpoint bound gives b≤8D².
5. H=union M_j meets every maximum-degree monomial, because otherwise a disjoint one could be added to the family. Its size is at most deg(q)*8D²≤8d³. Querying every coordinate of H forces each top-degree term to lose a variable on every answer branch. Thus q either vanishes or strictly loses degree; p never gains degree. Only free coordinates are queried.

At every continuing stage deg p+deg q decreases by at least one from a value≤2d. Zero functions terminate before degree is consulted. At most2d stages of cost≤8d³ give total worst-case depth T≤16d⁴, with no repeated coordinate on any branch. Choices of a maximizer and a maximal family may be fixed deterministically, so this is a total finite deterministic tree. The proof is existential/query-complexity based: computing the choices from coefficients need not be efficient.

## Adaptive coupling and the exact half factor

For any real u on the uniform sign cube define A_i(u)=E|u(X)-u(X^(i))|, where coordinate i is independently resampled, not forcibly flipped. Let a total nonrepeating deterministic tree compute h in {0,1}; r_i is the probability it queries i.

Take independent uniform X,Y. Run the tree only on X, with ordered queried coordinates i_1,...,i_L. Let Z_t replace the first t queried X-coordinates by Y-values. A full transcript fixes exactly its queried X-values: it is a cylinder, since the deterministic tree's next choices and stopping rule are determined by those values. Given this transcript, the queried Y-values and remaining unqueried X-values are independent fair signs. Therefore Z_L is uniform and independent of the transcript and h. It follows exactly that

    Cov(h,u)=E[(h(X)-1/2) * sum_{t≤L}(u(Z_{t-1})-u(Z_t))].

At a pre-query transcript with next index i, previously fixed X-bits have been replaced by independent Y-bits. All unqueried X-bits are still free; Y_i is fresh because i did not occur earlier. Hence the conditional pair (Z_{t-1},Z_t) has the unconditional uniform coordinate-resampling-i law. No independence of the final h from that pair is asserted or needed: its centered absolute value is identically1/2. Taking the absolute telescoping sum and summing pre-query cylinder probabilities gives

    |Cov(h,u)| ≤ (1/2) sum_i r_i A_i(u),
    sum_i r_i = E L ≤ T.

All sums are finite, including adaptive and variable-length branches. The tree computes h, not u. This independently proves the precise inequality needed, rather than invoking an unread attribution as a missing assumption.

## Square densities and the quantitative conclusion

Write a=b+x_i c with b,c independent of x_i. Orthogonality gives N_a=E b²+E c² and rho_i=E c²/N_a. A forced sign flip changes a² by4x_i bc; independent resampling flips with probability1/2. Thus

    A_i(a²/N_a)=2 E|bc|/N_a ≤ 2 sqrt(rho_i(1-rho_i)) ≤ 2 sqrt(rho_i).

The bound includes rho_i=0 and rho_i=1; at both endpoints the squared density is independent of that coordinate.

For the separator oriented h=1 on supp f and h=0 on supp g, set u=f²/N_f, v=g²/N_g, mu=E h. Then E u=E v=1, hu=u and hv=0. Therefore Cov(h,u)=1-mu and Cov(h,v)=-mu; their absolute values sum to1. Common zeros contribute no density, so their chosen h-labels do not affect these identities. Combining the two covariance bounds with the square estimate gives

    1 ≤ sum_i r_i(sqrt(rho_i(f))+sqrt(rho_i(g)))
      ≤ 2(E L)sqrt(delta) ≤ 32d⁴ sqrt(delta).

Squaring yields delta≥1/(1024d⁸). At the claimed sufficient threshold delta≤1/(4096d⁸), the last upper bound is≤1/2, an outright contradiction. The inclusive sufficient endpoint has genuine slack.

## Adversarial boundary checks completed by exact deductions

- Dictator calibration: h=(1+x)/2 and u=x give Cov(h,u)=1/2 and A_1(u)=1. Thus the factor1/2 in the covariance statement is saturated; a spurious factor1/4 is false. For a=1+x, its normalized squared density is1+x, rho=1/2 and A_1=1, calibrating the independent-resampling half factor in the square formula too.
- Exponential-bound endpoint example: f=1+x and g=1-x have disjoint supports and relative influence1/2. This verifies the elementary counterexample to an inclusive delta≤2^(-d)/d at d=1. Whether the historical source actually prints that inclusive statement remains a primary-access question; no source attribution is inferred from this example alone.
- Common zeros: f=(1+x_1)(1+x_2), g=(1-x_1)(1-x_2) occupy opposite corners. The other two vertices are common zeros. The total separator h=(1+x_1)/2 gives the density/covariance identity without any support-covering assumption.
- Constants: if either original polynomial is a nonzero constant, its support is the whole cube and a nonzero other polynomial has a common nonzero vertex. Zero polynomials are excluded; otherwise density normalization is undefined and the assertion can fail. n=0 and d=0 are outside the stated formula. n<d remains valid because all degree and query bounds are upper bounds.
- Maximality versus maximum size: only inclusion-maximality of the disjoint top-support family is needed for hitting every top monomial. Choosing a lower-degree term would be unsafe: q=x_1(1-x_2) restricts identically to zero on M={1} when x_2=1. The published construction explicitly uses maximum-degree monomials and avoids that failure.
- Repeated queries and partial trees are not silently allowed. The construction queries free coordinates and labels every terminal subcube, which supplies exactly the assumptions needed for fresh resampling and the complete-transcript cylinder argument.
- Real coefficients, uniform independent coordinates and the full L2 denominator are actual hypotheses. No inference for correlated measures, another group, generalized ACC conjectures or polynomial-time coefficient algorithms is made.

The reconstructed original theorem has no mathematical gap identified at this source-only checkpoint. No program or finite enumeration was needed to prove its arbitrary-dimension claim. Primary-body checks of the original question and credited structural/covariance interfaces remain pending; historical firstness and global openness are neither presumed nor certified. Default follow-up: none.
