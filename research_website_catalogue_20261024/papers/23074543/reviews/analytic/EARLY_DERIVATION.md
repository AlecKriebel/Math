# Independent analytic reconstruction, sealed before reference reading

Checkpoint UTC: 2026-10-25T07:00:00Z. Best-guess completion of this bounded analytic review: 48%. This is a scientific review artifact, not publication authority. The overall catalogue remains ongoing.

Only the complete actual four-page PDF and its controlling published-source/paper.tex, plus source-authentication receipts and the project policy, have been read. No historical proof, author audit, root or sibling review, adversarial report, or external primary body has been consulted. The PDF's four rendered pages have also been inspected. Its theorem statements, displayed formulas, examples, and references agree with the controlling TeX.

## Exact targets and assumptions

Let N be a positive finite integer. Each D_i is the image of a closed unit Euclidean ball under a real linear map, centered at zero, with rank m_i >= 2. It can consequently be represented as A_i B^{m_i} with A_i injective. The ambient space is finite-dimensional R^d and need not be the span of the sum. Exp(D) comprises unique maximizers of nonzero real linear functionals. The first claim is irreducibility over C of the complex Zariski closure E(D) of Exp(D). No rank of the differential, independence of radicals, genericity, or full dimension is assumed.

The second claim concerns S(D), the complex Zariski closure of (sum_i boundary_{L_i} D_i) intersect boundary D, where L_i = image A_i. It assumes the sum is full-dimensional and, for every index set J, rank[A_j]_{j in J} = min(d, sum_{j in J} m_j). The target is S(D) = E(D), hence irreducibility. Whether these targets resolve the precisely cited conjectures is reserved until the reference interfaces are read.

## Universal derivation of the first claim

1. Set q_i(u) = ||A_i^T u||^2. Maximizing u^T A_i v over ||v|| <= 1 reduces to maximizing (A_i^T u)^T v. If q_i(u)>0, Cauchy--Schwarz gives one maximizer v_i = A_i^T u / ||A_i^T u|| and hence p_i(u) = A_i A_i^T u / sqrt(q_i(u)). If q_i(u)=0, every point of D_i maximizes.

2. For a decomposition x=sum_i x_i with x_i in D_i, its deficit from the sum of support values is sum_i [h_i(u)-u^T x_i]. Each bracket is nonnegative, so equality holds exactly when every bracket is zero. Thus the supporting face of the sum is the Minkowski sum of supporting faces. A nonsingleton face remains nonsingleton after adding fixed points from all other faces. There can be no cancellation of face widths. Therefore the sum has a singleton supporting face exactly when every q_i(u)>0.

3. Consequently Exp(D)=F(U) exactly, where U = R^d minus union_i ker A_i^T and F(u)=sum_i p_i(u). There is no missing exposed-point stratum: any normal exposing a point must be in U. Zero lies in every excluded kernel and so never enters U. Each excluded subspace has codimension m_i >= 2.

4. To connect x,y in U, avoid the finitely many linear spaces ker A_i^T + R x and ker A_i^T + R y when choosing z. Each has dimension at most d-1. A finite union of proper real linear spaces cannot cover R^d (take a product of their nonzero vanishing linear forms). If an interior point of segment xz entered ker A_i^T then z would belong to ker A_i^T + R x; likewise for yz. The broken line x-z-y lies in U. Thus U is nonempty, open and path connected. This also covers coincident or nested kernels.

5. Every q_i is polynomial and strictly positive on U. The positive square root and its reciprocal are real analytic locally at every positive real number. Composition shows F is real analytic throughout U, with one real positive branch. No global complex square-root choice is involved.

6. Let I = {P in C[X_1,...,X_d] : P(F(u))=0 for every u in U}. It is proper since U is nonempty. If PQ lies in I and P does not, choose u_0 with P(F(u_0)) != 0. Continuity gives a nonempty open neighbourhood where P(F(u)) != 0, forcing Q(F(u))=0 there. Its real and imaginary parts are real analytic. The analytic identity theorem on a connected open domain forces both to vanish on all U. One elementary justification: the set of points where such a function vanishes on some neighbourhood is open, and is relatively closed because all derivatives are continuous and its convergent local Taylor series is zero at a limit point. Hence Q lies in I. This is an explicit primeness proof.

7. The complex zero locus of I is precisely the complex Zariski closure of F(U), and I is its vanishing ideal: a polynomial vanishing on F(U) vanishes on that closure by definition; the reverse inclusion is immediate. A proper prime vanishing ideal defines an irreducible affine complex algebraic set. This proves the first target. Connectedness of a merely continuous image would not suffice; the decisive bridge is the analytic identity theorem and primeness, which have been supplied.

## Universal derivation of the identification claim

1. Each regular supporting point p_i(u) is the image under the linear homeomorphism A_i:R^{m_i}->L_i of a unit vector, so lies on the relative summand boundary. Since an exposed point of a full-dimensional compact convex body belongs to its boundary, Exp(D) is in the set defining S(D). Therefore E(D) is contained in S(D).

2. For x=sum_i x_i in that defining set, take a nonzero supporting normal u at x. The nonnegative support deficits from the first derivation vanish individually. Write J={j:A_j^T u=0}. For i outside J one has x_i=p_i(u). For j in J write x_j=A_j v_j with ||v_j||=1; this uses injectivity and the relative boundary condition, rather than an unjustified Euclidean normalization of x_j.

3. The columns of A_J lie in u-perp, whose dimension is d-1. Under the stated maximal-rank condition, if sum_{j in J} m_j >= d, their rank would be d, a contradiction. Thus that sum is <= d-1, and the same condition gives column independence. It follows that A_J^T:R^d -> direct_sum_j R^{m_j} is onto. Prescribe A_j^T w=v_j simultaneously; a real solution w exists.

4. For epsilon>0 and j in J, A_j^T(u+epsilon w)=epsilon v_j, so the regular support point is identically A_j v_j=x_j. For all other finitely many indices their nonzero projected normals remain nonzero for all sufficiently small epsilon, and their support points converge to x_i by continuity. Thus u+epsilon w is in U and F(u+epsilon w)->x. In particular it is automatically nonzero. If J is empty x already equals F(u).

5. A complex algebraic set is closed in the Euclidean topology because it is an intersection of polynomial zero sets. Therefore every such x belongs to E(D); taking the complex Zariski closure gives S(D) contained in E(D). Together with step 1 this proves equality. No uniform choice of w across the boundary, or global parametrization of the singular strata, is needed.

6. Maximal concatenated ranks are simultaneous open conditions given by nonvanishing maximal minors (a finite union of charts for each rank condition). Their intersection is nonempty: take distinct real t and vectors (1,t,...,t^{d-1}), and assign them to blocks of sizes m_i<=d. Any k<=d columns are independent by a k-by-k Vandermonde minor in their first k rows; a larger set contains d independent columns. This proves the generic assertion within the matrix parameter space. If total rank is below d, the stated full-dimensional theorem must be applied in the actual ambient span; it cannot simply be invoked in the larger ambient space where boundary D would include every point of D.

## Boundary and falsification checks reconstructed without external bodies

* Rank one is a real boundary: the interval has exposed set {-1,1}, reducible over C. Adding a planar round disc to a nonzero horizontal interval gives two circular arcs; each arc is Zariski dense in its circle by analytic uniqueness, and the two translated circle polynomials are distinct for a>0. The exposed closure is therefore the union of two distinct conics. This explains the codimension requirement without claiming that every rank-one configuration fails.
* Repeated discs and coincident spans do not affect the first proof. Their kernels can coincide; the connectivity argument still applies, and the prime-ideal proof does not require an injective F.
* A single rank-two ellipsoidal disc in R^3 gives U=R^3 minus its normal axis. This is connected, although the convex body is not full-dimensional. The first proof remains valid. The generic identification theorem as stated assumes full dimension and is not being extended to that ambient-boundary convention.
* In R^3 with two xy unit discs and one xz unit disc, a regular support point satisfies X=a+b, a^2+Y^2=4, b^2+Z^2=1, with a=2u_1/sqrt(u_1^2+u_2^2), b=u_1/sqrt(u_1^2+u_3^2). Hence X^2+Y^2+Z^2-5=2ab, yielding P=(X^2+Y^2+Z^2-5)^2-4(4-Y^2)(1-Z^2)=0. Meanwhile e_3=e_1+(-e_1)+e_3 is a sum of three relative boundary points on the face with normal e_3. Its polynomial value is P(0,0,1)=16. Thus e_3 is in S but outside E. This is an exact algebraic separation, stronger than an unsuccessful limiting-normal test.
* For full-dimensional summands, every nonzero normal is regular for that summand. For d=2 every permitted summand is full rank, so U=R^2 minus {0}; no disconnected normal regions arise. Empty J requires no perturbation. Nonempty J necessarily has positive total rank <=d-1.
* Finiteness of N, positive-dimensional discs, real positive branches, and exact relative summand boundaries are substantive hypotheses. Zero-dimensional summands are excluded by the written theorem; no necessity assertion for excluding them is made. General convex summands or nonanalytic support maps are outside the proof.

## Early result and remaining gap

No central mathematical defect was found in the two universal deductions or in the given counterexamples. The strongest independently supported conclusion at this seal is the two mathematical theorem statements with their written assumptions. Exact conjecture matching, prior special cases, attribution of the analytic lemma, public timing and version provenance, and bounded novelty evidence have not yet been checked. These are genuine open review tasks, not presumed successes. No historical-priority conclusion is drawn.
