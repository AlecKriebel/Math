# Independent derivation, before reading previous audits

Input: submitted head `ad138ddd5bd1a51c0f225f03342c0c058873f790`, hashes in `INPUT_PINS.json`. Written 2026-10-13 UTC. Neither `independent_audit/AUDIT.md` nor `independent_audit/FINAL_ACCEPTANCE.md` has been read at this checkpoint. Assigned downstream correctness, not priority or publication. Completion estimate: 40%.

## Claim and conditional interface

The target is the ordinary language of explicitly encoded rational, variable-size bimatrix games with `rank(A+B)=1` and exactly one mixed-strategy **pair**. Arbitrary degeneracy is allowed. The proposed reduction maps a no PARTITION instance to a unique strict pure equilibrium, and a yes instance to that equilibrium and an additional pair. It does not establish a nondegenerate-game promise, strong hardness, fixed dimensions, or payoff uniqueness.

The downstream argument needs a polynomially encoded acyclic capacitated network with distinguished arc e, p arcs, V vertices, maximum value F, and strictly positive costs. A zero-e flow of value F must exist. For every real q in [0,F] an optimum must exist. In a no instance **every** optimum must have e-flow zero. In a yes instance **some** optimum must have e-flow 1/2 at q <= F-3/2. These quantifiers, including the continuous values and the perturbation preserving the yes/no property, are the source-flow family's responsibility. Nothing below proves that interface for the submitted DS gadget by assuming it.

## Simplex embedding

Put L=V-1, K=1/(2L), eps=1/(4L), and introduce simplex coordinates x0, xstar, x1,...,xp. Write h=F(xstar+sum xi), fi=LF xi, and q=h-K fe. Thus the coefficient of q at x0 is zero, at xstar and every ordinary arc coordinate it is F, and at the e coordinate it is F/2. Consequently q >= h/2 >= 0, with q>0 at every x other than the pure row x0. This strict statement will be crucial at negative lambda. Also sum fi <= Lh, and 0<=h<=F.

The inverse map is unique: x0=1-h/F, xi=fi/(LF), and xstar=h/F-sum fi/(LF). It is nonnegative exactly under the displayed bounds. Thus there is no spare simplex coordinate that can create multiple row strategies representing the same flow and h.

Every nonnegative s-t flow in a DAG is a nonnegative combination of directed s-t paths (no circulation remains); hence sum fi<=Lq. For a fixed parameter lambda impose capacity bounds, conservation `Df=q d`, and q=lambda as pairs of inequalities where appropriate. Scaling a zero-e maximum flow by lambda/F proves feasibility for every real lambda in [0,F]; its h=q=lambda and path bound guarantee membership in the simplex.

An optimum with e-flow zero and q=lambda has h=lambda and is retained. In a no instance, if every original optimum has e-flow zero, the restricted LP keeps an original optimum and therefore has the same value; every restricted optimum is then an original optimum, so also has e-flow zero. **Uniqueness of the original optimizer is stronger than downstream necessity.** If uniqueness is known, the inverse map proves uniqueness of its x. For a yes witness q<=F-3/2, fe=1/2 gives h=q+eps<=F-3/2+eps<F because L>=1 and eps<=1/4. The same witness has q<=F-eps. No endpoint or upper-simplex clipping removes it.

## Uniform exact penalty over real parameters

Let d(lambda)=r+s lambda. Primal: minimize c^T x subject to x>=0, 1^T x=1, Rx<=d(lambda). Its dual is

`maximize nu-d(lambda)^T mu`, subject to `mu>=0`, `nu 1<=c+R^T mu`.

The sign of mu is positive: for feasible x, `c^T x >= nu-mu^T Rx >= nu-mu^T d`. The dual feasible polyhedron is independent of lambda and nonempty, using mu=0 and nu=min c. It has no nontrivial line: mu>=0 forces the mu direction of any two-sided line to vanish, then the upper inequalities force the nu direction to vanish. For every real lambda in [0,F], primal feasibility and compactness give finite attained optimum; LP duality gives an attained optimal dual face. This face is a nonempty pointed polyhedron, so it has a vertex. A vertex of an optimal face is a vertex of the original dual: a feasible convex decomposition would have both endpoints optimal, because the objective cannot exceed its optimum.

Clear all denominators in the dual **constraints** by Q, and let H0>=1 bound the absolute integer coefficients and right-hand sides, including the nonnegativity constraints. In d0=k+1 ambient coordinates, every vertex has d0 independent active equations. Cramer's rule gives coordinate absolute value <=d0! H0^d0 because the nonzero integer denominator determinant has absolute value at least one. This remains valid for a lower-dimensional optimal face and an unbounded feasible polyhedron. The chosen mu has l1 norm <=C=k d0! H0^d0, uniformly in lambda. Set M=C+1.

For any simplex x, delta=max(0,max_j(R_j x-r_j-s_j lambda)). The chosen optimal dual vertex yields

`c^T x >= optimum-mu^T(Rx-d) >= optimum-C delta`.

Therefore `c^T x+M delta >= optimum+(M-C)delta`. Every infeasible x is strictly worse; feasible minimizers are precisely primal optima. The proof controls **all** minimizers, not one selected basic solution. Irrational lambda causes no encoding problem: lambda changes only the dual objective, while all selected vertex coordinates come from the same rational feasible polyhedron. Q may be the product of denominators; its log is bounded by the sum of their input lengths. Then log H0 and log M are polynomial. No parametric subdivision or enumeration of dual vertices is required to compute M.

## Game signs and complete correspondence

Add penalty baseline j=0 with R0=r0=s0=0. Let Gj=c+M Rj^T-M rj 1, bj=-M sj, A(:,j)=-Gj, a0=-eps, and ai=F-eps at every nonzero row. Let B=-A+ab^T. Then a^T x=h-eps. Opposite inequalities q<=lambda and -q<=-lambda supply b entries -M,+M, so b is nonzero; a is nonzero, hence A+B has **exactly** rank one.

For fixed lambda, the auxiliary zero-sum row matrix is A_lambda=A-1 lambda b^T. Against a row distribution x, column j has row payoff

`x^T A_lambda(:,j)=-c^T x-M(Rj x-rj-sj lambda)`.

Maximizing its minimum over columns is exactly minimizing the submitted penalty function. Finite zero-sum minimax identifies all optimal row strategies with all penalty minimizers.

For any x with a^T x=lambda, original column expected payoffs equal auxiliary column expected payoffs since `x^T B=-x^T A+lambda b^T`. For any y, all row payoffs change by the common scalar `-lambda b^T y`. Both players' entire best-response sets are consequently identical. This proves both directions of the equilibrium correspondence, including zero probabilities, duplicate columns, multiple opposing optimal strategies, and positive-dimensional optimal faces. There is no support regularity hypothesis.

Every original equilibrium produces lambda=a^T x in [-eps,F-eps]. Conversely every auxiliary equilibrium on this hyperplane produces an original one. For fixed lambda its original fiber is `(X_lambda intersect {a^T x=lambda}) times Y_lambda`; minimax ensures any optimal x may be paired with any optimal y.

## Negative parameters and the strict pure pair

For lambda<0, the diagnostic residual q-lambda is everywhere positive. Costs c^T x>=0, and q>=h/2, imply penalty >=M(q-lambda)>=-M lambda. Pure row x0 attains equality: f=h=q=0, capacities have negative residual, conservation has zero residual, baseline zero, opposite parameter residual lambda<0, and q-lambda=-lambda>0. For x!=x0, q>0 gives strict inequality. Thus every negative-parameter auxiliary equilibrium uses exactly x0. Its only hyperplane crossing is lambda=-eps.

At that crossing the diagnostic column is the unique penalty maximizer at x0, hence every optimal column strategy is its pure distribution. This proves uniqueness of the **pair**, not only x. Directly in the original game, A0,diagnostic=0, while all other rows have `-ci-M qi<0`, including the star row (qstar=F). Against x0, Bdiagnostic=M eps>0. Baseline and conservation columns yield zero, opposite parameter column yields -M eps, and positive-capacity columns yield -M ui<0. Both best responses are strict. No duplicate active conservation columns or slack row can supply a second pair.

## Nonnegative parameters and exhaustion

For every auxiliary optimum at lambda>=0 in the candidate interval, uniform exactness gives q=lambda. The hyperplane equality then reads `lambda=q+K fe-eps`, so **fe=1/2**. At lambda=0, any nonnegative DAG flow of value zero is zero, and therefore fe=0; no zero crossing exists. In a no instance the all-optimal interface rules out every nonnegative crossing. In a yes instance the retained witness has q<=F-eps and gives a crossing and, by minimax, at least one opposing strategy. Its x has fe=1/2 and differs from x0. All other boundary, degenerate, or support-continuum candidates are included in this exhaustion; their number in yes instances is irrelevant.

## Dimensions and bit lengths

Submitted network counts V=4n+6 and p=8n+7 imply m=p+2=8n+9. Capacities contribute p inequalities, conservation 2V, parameter 2, plus penalty baseline 1, so columns=p+2V+3=16n+22. Retaining redundant conservation equations affects neither dual pointedness nor the bound. F=2^(n+1) has n+2 bits. All capacities, normalized costs, arc perturbations, potentials, and simplex coefficients have polynomial length provided the flow interface supplies polynomial encoding. The determinant-bound M involves k=p+2V+2; its bit length is polynomial. Explicitly listing an m by N game remains polynomial. Executing the exponential SSP curve is not a reduction step.

## Independent membership proof, including irrational witnesses

For every pair of nonempty action sets I,J, choose i0 in I, j0 in J. Let X comprise simplex x supported inside I such that j0 is a best column and every j in J ties it. Let Y comprise simplex y supported inside J such that i0 is a best row and every i in I ties it. These are compact rational polytopes. Every pair in X times Y is a Nash pair: all actions used belong to the declared best-response sets. Every Nash pair belongs to its actual-support cell. Using closed cells permits vanishing declared probabilities without adding false equilibria.

The equilibrium set is the finite union of these products, although the number of cells is exponential. A nonempty compact polytope is the convex hull of its vertices, and vertices of X times Y are products of vertices. If the union of all cell vertices contained a single pair, every cell and the union would be that singleton. Thus any nonsingleton equilibrium set has two distinct vertex pairs, including when the initially observed pair is irrational or lies in a positive-dimensional component. Boundary vertices may have smaller supports; this is harmless.

For total encoded payoff length Linput, multiplying all payoffs by the product D of denominators creates integers bounded by 2^Linput; comparison coefficients are bounded by H=2^(Linput+1). At a vertex in ambient dimension d, independent active normals must span the ambient space: otherwise a small two-sided movement preserving all active constraints would preserve the finitely many strict inactive inequalities, contradicting extremality. Choose d independent equations. Hadamard/Cramer bounds numerator and denominator by d^(d/2) H^d; both therefore need at most ceil(d(Linput+1)+(d/2)log2 d)+2 bits. d=m or n. Lower-dimensional and degenerate cells satisfy the same bound.

Two distinct rational pairs of these bounded sizes give an NP certificate. Verify nonnegative unit sums, every pure payoff <=the mixed expected payoff for both players, and at least one distinct coordinate, all by exact arithmetic. These inequalities are sufficient because a mixed expected payoff is an average of its pure payoffs. Existence of a Nash pair is not an input promise: on the product simplex, the continuous map adding each player's positive pure-payoff gain and renormalizing has a Brouwer fixed point. At a fixed point a positive total gain would force every action with positive probability to have payoff above that player's weighted average, a contradiction. Thus all gains vanish, giving a Nash pair. Consequently complement of nonsingleton really is singleton.

Exact rank checking is polynomial: reject rank zero, choose nonzero pivot Cij in C=A+B, and test all cross-multiplication identities. Ordinary rank-one UNIQUENESS has complement consisting of rank-invalid games (decidable in polynomial time) or valid games with two pairs (NP witnesses). Hence membership is coNP for the ordinary language, as well as for the promise version. There is no reliance on recognizing degeneracy.

## Fiber/example sanity check

The submitted 2 by 2 example has sum `[[2,6],[6,18]]=(1,3)^T(2,6)`. Direct differences are 4t-3 and 4s-3. Its exact equilibria are the two diagonal pure pairs and the pair with first probabilities 3/4. For the auxiliary game the row objective is min(s-2lambda,9-3s-6lambda); its unique optimizer is s=clip(9/4-lambda,0,1). Thus a^T x-lambda has slopes -1,+1,-1 and zeros 1,3/2,3. Every equilibrium-containing fiber is singleton. This disproves a general inference from singleton support/fiber to global uniqueness; it does not itself prove hardness. The closed-fiber LP formulation is correct since the nonnegative row and column gaps sum to zero exactly when equilibrium holds, which also bounds the auxiliary payoff variables.

## Adversarial outcome of this derivation

No downstream mathematical defect has been found. Uniform exactness, strict default-pair uniqueness, full equilibrium correspondence, all nonnegative crossings, polynomial encoding, and coNP membership are independently proved above. Overall hardness remains **conditional on the independently checked source-flow interface**, especially the perturbed all-optimal no property and retained half-integer yes witness. Test scripts will supply finite reproducibility checks and deliberate failures, not replace these quantified deductions.
