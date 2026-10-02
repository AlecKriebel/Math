# Explicit verification of the credited negative answer

The small-component mechanism is already stated in the original OWR contribution, and the broader negative answer is in Conlon–Zhao. This is a self-contained verification with explicit parameters, not a new discovery or a new author search turn.

All graphs below are finite, simple and undirected. For possibly overlapping vertex sets, e(S,T)=sum over s in S,t in T of A_st. Discrepancy bounds are uniform over all such pairs.

## 1. A deterministic sparse regular base

For an integer q≥3 put k=q². Let H_q have vertex set {1,...,q}^k, with two vertices adjacent exactly when they differ in every coordinate. It is the categorical tensor product of k copies of K_q, with

    N=q^k,  d=(q−1)^k.

Its adjacency matrix is (J_q−I_q) tensor ... tensor (J_q−I_q). Since J_q−I_q has eigenvalues q−1 once and−1 with multiplicity q−1, the tensor eigenvalues are (q−1)^(k−j)(−1)^j for0≤j≤k. The leading eigenvalue d is simple and all others have absolute value at most lambda=d/(q−1).

The graph is connected: for any two vertices, choose a third coordinatewise different from both, which is possible for q≥3. Thus they have a path of length at most two. Every edge lies in a triangle by the same observation.

Moreover d/N=(1−1/q)^(q²)≤exp(−q)→0, while d→infinity and lambda/d=1/(q−1)→0. The standard spectral decomposition and Cauchy–Schwarz give

    |e_H(S,T)−(d/N)|S||T|| ≤ lambda sqrt(|S||T|) ≤ lambda N.

This mixing bound can also be derived directly by writing each indicator as its mean plus its orthogonal component; the matrix A_H−(d/N)J has operator norm lambda.

## 2. Add the source's small clique

Let m=d+1 and form G_q=H_q disjoint union K_m, on n=N+m vertices. It is d-regular and d/n→0. The clique contributes a second eigenvalue d. More intrinsically, the vector equal to1/m on the clique and−1/N on the base is orthogonal to the global all-ones vector and is an eigenvector with eigenvalue d. Hence the requested nontrivial eigenvalue condition fails.

Here is the uniform discrepancy estimate with normalization n, rather than N. Write x=|S intersection H|,y=|T intersection H|,s=|S intersection K_m|,t=|T intersection K_m|. The base error is at most lambda N. The absolute normalization difference is bounded by

    d[(1/N−1/n)xy+(xt+sy+st)/n]
       ≤ d[mN/n+(2Nm+m²)/n] ≤3dm.

The clique has at most dm ordered adjacency incidences in total, so its contribution is at most dm. Therefore, for every S,T,

    |e_G(S,T)−(d/n)|S||T|| ≤ lambda N+4dm.

Dividing by nd gives at most

    1/(q−1)+4m/n →0.

Indeed m/n≤(d+1)/N≤exp(−q)+1/N. Thus the exact uniform o(nd) hypothesis holds while a nontrivial eigenvalue is d. The sequence of orders n=n(q) tends to infinity; a subsequence of integer orders suffices to refute a universal asymptotic implication.

## 3. Optional connected version, with no ambiguous repeated top eigenvalue

Choose an edge uv in the clique and an edge xy in H_q. Delete uv and xy, then add ux and vy. Both original edges lie in triangles, so deleting either leaves its original component connected. The new cross edges join the two components. The resulting graph G'_q is connected, simple and still d-regular.

Only four undirected edges have changed, or eight adjacency entries, so its uniform cut error differs from G_q's by at most8. Since nd tends to infinity, it still satisfies the same o(nd) hypothesis.

Use the same vector w, with values1/m on the clique and−1/N on the base. It has sum zero and squared norm1/m+1/N=n/(mN). Every remaining internal edge has zero w-difference, and exactly two cross edges have difference1/m+1/N. The graph-Laplacian Rayleigh quotient is therefore

    [2(1/m+1/N)²]/[1/m+1/N]=2n/(mN).

The adjacency Rayleigh quotient is d−2n/(mN). The variational principle on the orthogonal complement of the constant vector yields

    lambda_2(G'_q)/d ≥1−2n/(dmN) →1.

Because G'_q is connected, its leading eigenvalue d is simple. This is a genuine positive nontrivial eigenvalue near d, not an appeal to a disconnected eigenvalue convention. It again disproves the desired o(d) conclusion.

## 4. Scope and credit

The result is already negative in the original source, and the positive Cayley/vertex-transitive theorem is not contradicted: adding the small component or performing the switch destroys that symmetry. No claim is made about stronger size-sensitive discrepancy bounds such as an error proportional to sqrt(|S||T|). The checker validates small tensor-product/switch fixtures, exact balanced-vector identities and uniform cut bounds; the written estimates prove the asymptotic statement for the full explicit sequence.
