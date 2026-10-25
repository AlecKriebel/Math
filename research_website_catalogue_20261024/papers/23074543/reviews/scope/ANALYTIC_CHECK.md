# Independent derivation: discotope exposed-point irreducibility

The complete actual four-page selected PDF, every raw page render and full controlling paper.tex were read before the initial independent seal. This note expands that reconstruction and checks literal source scope afterward. No historical reviewer verdict or current sibling opinion supplies an inference below.

## Exact objects and claims

A disc is a centered linear image of a closed Euclidean unit ball, with actual linear-span dimension m_i. The main theorem considers every finite N>=1 and all real matrices A_i:R^(m_i)->R^d of full column rank with m_i>=2, forming D=sum A_i(B^(m_i)). It asserts that E(D), the complex Zariski closure in C^d of points uniquely maximizing a nonzero real linear functional, is irreducible. It does not require D to span R^d, independent radicals, distinct summands or spans, a one-to-one support map, a differential-rank condition or a generic configuration.

The separate identification theorem assumes D full-dimensional and requires GP for every subset J: dim(sum_(i in J) L_i)=min(d,sum_(i in J) m_i). Under those assumptions S(D)=E(D), where S is the complex Zariski closure of (sum relative summand boundaries) intersect the topological boundary of D. Each summand boundary is relative to its own span. The boundary of D in this theorem is in the full ambient space. Reducing to the linear span is the original source's full-dimensionality convention; it must not be confused with an automatic assertion about S defined using a larger ambient boundary.

No rank-one extension, nongeneric S=E assertion, degree formula, birationality assertion or irreducibility of the whole complex critical locus is claimed. The finite sum and the minimum actual rank two are essential to the stated mechanism. Translated balls, infinite sums and other general convex summands are outside the stated theorem, even where separate extensions might be possible; no follow-up extension is pursued.

## The connected real domain and the exact support image

Any linear image of a ball admits an injective minimal parametrization A_i by restricting its singular-value decomposition to nonzero singular directions. Q_i=A_i A_i^T is real positive semidefinite of rank m_i. Cauchy–Schwarz gives support value ||A_i^T u|| and, when that vector is nonzero, its unique maximizing point

p_i(u)=A_i A_i^T u/||A_i^T u||=Q_i u/sqrt(u^T Q_i u).

When A_i^T u=0, the functional is constant on the entire positive-dimensional disc. Equality in the Minkowski support inequality is equivalent to equality in each summand because each deficit is nonnegative. Hence the face is the sum of the summand faces. Such a sum is a singleton exactly when all the summand faces are singletons: fix points in all other faces to embed any nonsingleton face by translation. This argument does not require uniqueness of an arbitrary decomposition in the sum.

Consequently the normals exposing singleton faces are exactly U=R^d minus the union of ker A_i^T, and Exp(D)=F(U) exactly, where F=sum p_i. The origin is excluded, so no zero functional slips into the definition. The statement is stronger than merely having a dense set of parametrized exposed points, and avoids an unnecessary appeal to density of exposed points among extreme points.

Each excluded kernel has codimension m_i>=2. A finite union of proper real subspaces cannot fill R^d: choose a nonzero linear form vanishing on each and take their nonzero product. Its complement is nonempty and open. For x,y in the complement, every M_i+R x and M_i+R y is proper, of dimension at most d-1. Choose z outside their finite union. If (1-t)x+t z belongs to M_i with 0<t<=1, then z belongs to M_i+R x, a contradiction; t=0 is already excluded by x in U. The same argument joins y to z. Thus U is path connected. There is no unproved assertion about connectivity of a complex branched cover or a critical locus.

All radicands are strictly positive on U. Positive real inverse square root is real analytic on (0,infinity), so F is real analytic on all of this one connected open real domain. Passing from u to -u causes no branch-selection discontinuity in U. No global complex square-root branch is chosen.

## Prime ideal argument over C

Let I be the ideal of complex polynomials vanishing on F(U). It is proper because U is nonempty. If P Q belongs to I and P does not, continuity gives a nonempty real open neighborhood on which P(F(u)) is nonzero; Q(F(u)) vanishes there. Real and imaginary parts of Q composed with F are real analytic on connected U. Analytic uniqueness therefore makes both vanish everywhere, so Q belongs to I. This proves primality over C directly.

Analytic uniqueness is supplied in the manuscript, not hidden in an unsupported import. The points near which an analytic function is identically zero form a nonempty open set. At a limit point inside U, continuity of every derivative implies that all Taylor coefficients vanish. A convergent analytic Taylor expansion makes the function vanish in a neighborhood there. The set is therefore also relatively closed, and connectedness finishes the proof. The conclusion does not hold for arbitrary merely connected continuous images; analyticity is used precisely here.

By definition I is the vanishing ideal of the complex Zariski closure of F(U); the standard prime-ideal characterization yields irreducibility. Repeated discs, coincident spans, algebraically dependent radicals and singular support images do not enter the ideal argument. This proves the full non-generic and possibly lower-dimensional main theorem.

Kucharz–Kurdyka's actual 2017 Proposition4.3 proof explicitly records the real-Zariski analytic-image principle. The current complex-valued argument is a direct elementary counterpart. That principle and analytic uniqueness are prior facts, not new mathematical credit for this application.

## The general-position bridge to the purely nonlinear part

Every exposed point is a sum of the unique p_i(u), each on its relative summand boundary, so E is contained in S. Conversely, take x=sum x_i in the set generating S, with x_i in the relative boundaries. Full-dimensionality of the compact convex D gives a supporting hyperplane at x with nonzero normal u. Its sum of nonnegative support deficits is zero, so each x_i lies in its corresponding u-face.

Let J be the indices annihilated by A_j^T u. For i outside J, x_i=p_i(u). All L_j for j in J lie in u-perp, a proper hyperplane. If their total parameter dimension were at least d, GP would force their span to equal R^d, a contradiction. Hence their total dimension is <=d-1, and GP makes their span dimension equal to the sum of dimensions. The concatenated column matrix A_J is injective; its transpose is therefore surjective onto the direct product of all parameter spaces.

Write x_j=A_j v_j with ||v_j||=1, justified by injectivity and the relative-boundary condition. Choose one w satisfying A_j^T w=v_j for every j in J. This is a simultaneous transpose constraint; simply setting w equal to a target vector would be wrong for non-orthonormal ellipses. For epsilon>0, u_epsilon=u+epsilon w satisfies A_j^T u_epsilon=epsilon v_j, and p_j(u_epsilon)=A_j v_j=x_j exactly. Positive epsilon matters; negative epsilon reverses these points. For all remaining finitely many indices the projections stay nonzero for sufficiently small epsilon and p_i(u_epsilon) tends to x_i. Thus u_epsilon is in U and F(u_epsilon) tends to x. When J is empty, x is already exposed.

A complex algebraic set is Euclidean closed, so the real limit x is in E. Taking complex Zariski closures gives S contained in E and hence equality. This is not an inference that every boundary point or every S-generator is itself exposed. The simultaneous perturbation only proves approximation, which is exactly what is needed for the closure.

For prescribed sizes m_i<=d, each failure of maximal concatenated rank is determinantal. There are finitely many subsets. Distinct real Vandermonde columns (1,t,...,t^(d-1))^T, partitioned into the requested blocks, give a simultaneous real witness: every at-most-d columns are independent and any larger set spans R^d. The desired condition is therefore nonempty real Zariski open in the full-rank matrix parameters. When sum m_i>=d, the total span is full. This matches the original bases-parametrized genericity convention; if the ambient span is smaller, the source explicitly works in that span. No shape genericity beyond this span condition is used in the proof.

## Boundary and algebraic-separation checks

For a one-dimensional interval, E consists of two distinct points and is reducible. A unit disc plus a nonzero horizontal segment has two exposed open semicircles, whose complex Zariski closures are the distinct conics (X-a)^2+Y^2=1 and (X+a)^2+Y^2=1. Rank one removes a hyperplane and can disconnect the real analytic normal domain; the rank threshold is substantive. The theorem does include a single rank-two or higher disc in a proper subspace and multiple copies of one disc.

For the nongeneric example D=2B_xy+B_xz in R^3, e3=e1+(-e1)+e3 lies in the sum of relative boundaries and in the face 2B_xy+e3. Write the regular support coordinates X=a+b, a=2u1/r, b=u1/s, Y=2u2/r, Z=u3/s, with r²=u1²+u2² and s²=u1²+u3². Then a²+Y²=4 and b²+Z²=1. Hence T=X²+Y²+Z²-5=2ab and

P=T²-4(4-Y²)(1-Z²)=0.

This identity holds on all exposed points and therefore their complex Zariski closure. Since P(0,0,1)=16, e3 is outside E while in S. This certifies separation algebraically, rather than merely observing that one selected normal fails to expose e3. The rational substitution only uses r,s>0, exactly the regular real normal domain.

The original symbolic controls were completely read. In the existing pinned SymPy1.14.0/mpmath1.3.0 runtime, both original programs passed. The independent one verifies the auxiliary-circle elimination ideal, a denominator-aware quotient certificate, exact separating value16, regular normals with u1=0, arbitrary rational unit targets, positive versus negative perturbations, non-orthonormal ellipse transpose constraints, and the distinct rank-one circle branches. The original program additionally checks repeated-disc support and a normal-arrangement detour. These finite exact controls corroborate formulas; the general N,d and GP claims are the proofs above.

## Literal antecedents and contribution boundary

The actual OWR contribution printed829–832 defines its target as the Zariski closure of exposed points and asks generic irreducibility when all summand dimensions are >=2. The actual GM2022/arXiv v2 body instead defines S using the summed relative boundaries, states its generic irreducibility conjecture, assumes full-dimensionality after ambient-span reduction and already uses the support gradient. Its known ranges include the low boundary-dimension sum, generic rank-two sums and full-dimensional summands. Those results receive prior credit. The current main theorem covers arbitrary rank-two-or-higher configurations, and its separate GP bridge addresses the S formulation. It does not prove the larger complex-critical-locus or birationality expectations in that paper.

The prospective new credit is this unrestricted exposed-point application and the generic identification, not the analytic-image lemma, basic support-face identity or known special cases. Bounded current source/author-list searches do not establish historical first priority. No universal novelty certificate, source repair, new extension or promotion decision is supplied here. Within the exact two stated theorems, no central analytic gap was identified.
