# Independent core before primary-source inspection

Recorded before reading any old audit or prior conclusions. Scope: input PROOF.md, 13,567 bytes, SHA-256 20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1. This artifact states deductions independently checked from that proof and the standard Markov inequality; citation verification remains outstanding.

## Markov and Bernoulli block bound

For a real degree-at-most-m polynomial Q on [-1,1], the classical bound is sup|Q'| <= m^2 sup|Q|. Defining Q(x)=P((x+1)/2) gives Q'=P'/2, hence sup_[0,1]|P'| <= 2m^2 sup_[0,1]|P|, including m=0. For a multilinear R on {0,1}^b let P(t)=E[R(Ber(t)^b)]. Monomials of cardinality k map to t^k, so degree does not increase and P is bounded on the entire real interval [0,1] by convexity. Its derivative at zero is sum_j(R(e_j)-R(0)); this can equally be derived by the first-order expansion of the Bernoulli product measure, and includes all mixed monomials automatically. If R(0)=1 and all R(e_j)<=0, then P'(0)<=-b. Markov yields b<=2m^2. No assumption that R is Boolean valued is involved. The m=0 and b=0 cases are harmless; b>0,m=0 is impossible.

## Separator reconstruction

A restriction of multilinear p,q with disjoint supports remains disjoint. If one is zero, label the leaf 0 when p=0 and 1 otherwise. This is valid even when both are zero. If both are nonzero, neither can have degree zero: a nonzero constant has full support. Put D=max(deg p,deg q)>=1 and s=p^2-q^2 reduced in the Boolean quotient. Its degree is at most 2D. Because each nonzero multilinear cube polynomial is nonzero at a cube vertex and disjointness holds, max|s|>0; choose any maximizer z. Exactly one polynomial is nonzero there.

Suppose p(z)!=0. Take any inclusion-maximal pairwise-disjoint family M_1,...,M_b of supports of the degree-deg(q) monomials of q. Each support is nonempty. For any M_j, restricting all outside variables to z leaves the M_j coefficient unchanged: the only possible additional source is a proper superset, forbidden by maximum degree. The restricted q is nonzero as a function by uniqueness of the multilinear cube expansion. Since it is zero at z, some nonempty subset E_j of M_j, flipped from z, gives q!=0 and thus p=0. These blocks are disjoint and nonempty.

The map from y in {0,1}^b to z flipped on the union of selected E_j substitutes x_i=z_i or x_i=z_i+(1-2z_i)y_j. Every factor has degree at most one in one y_j. Products and Boolean multilinearization cannot increase total degree, even when several original coordinates share a y_j. Therefore R=s(composed map)/|s(z)| has degree <=2D, all vertex values in [-1,1], R(0)=1, and R(e_j)<0. The block bound gives b<=8D^2. Thus H=union M_j has <=8D^2 deg(q)<=8d^3 variables.

Inclusion-maximality (not maximum cardinality) is sufficient: any maximum-degree monomial disjoint from H could be appended to the family. Query all H. Every maximum-degree monomial loses at least one variable on every answer branch; lower-degree monomials cannot gain degree, and cancellation only lowers it further. Hence q becomes zero or has degree below its previous degree. Degree of p never increases. The q(z)!=0 case interchanges roles.

Each recursive nonterminal node has positive degrees for both polynomials. Their sum, initially <=2d, strictly decreases at every batch of queries; terminal handling covers zero restrictions without assigning a degree to the zero polynomial. Consequently at most 2d batches occur and depth <=16d^4. This estimate is deliberately loose; positivity of both degrees even gives at most 2d-1 batches, but no sharper bound is needed. All H consist of remaining free coordinates, so no query repeats on a branch. The construction is total, finite and deterministic after arbitrary fixed tie-breaks.

## Edge checks and downstream interface

Real signs do not matter because squares give s the support sign. Arbitrary coefficient magnitude does not matter because max|s| normalizes, and it is strictly positive. The case n<d is covered by the inequalities using deg<=d; indeed depth also cannot exceed n. Affine substitution between +/-1 and 0/1 coordinates preserves degree in both directions and query depth. Constants and zero restrictions terminate. A nonzero constant and a nonzero disjoint companion cannot coexist. Common zeros impose no conflicting leaf constraints.

With total separator h, nonzero normalized u=f^2/Ef^2 and v=g^2/Eg^2 obey hu=u and hv=0, so Cov(h,u)=1-Eh and Cov(h,v)=-Eh regardless of common zeros. If the stated adaptive covariance and resampling bounds hold, each absolute covariance <=T sqrt(delta), giving 1<=2T sqrt(delta), hence delta>=1/(1024d^8) for T<=16d^4. No strict-endpoint concern enters the stronger necessary lower bound. Input threshold 1/(4096d^8) then yields a strict contradiction.

Provisional result: no gap found in separator/Markov proof. Primary source literal verification, independent exact finite checks, mutation guards, and final artifact authentication remain open.
