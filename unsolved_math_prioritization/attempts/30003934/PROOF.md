# Uniqueness of a Nash equilibrium in rank-one bimatrix games: a coNP-completeness reduction

Status: complete candidate proof, pending the parent’s independent acceptance decision. The algebraic and source-quantifier gaps identified during development are addressed below; independent audit results are recorded separately.

## Target and central statement

Input: explicitly listed rational payoff matrices A,B, with rank(A+B)=1; variable dimensions; no nondegeneracy promise. Decide whether exactly one mixed-strategy Nash equilibrium exists.

The proposed reduction is from PARTITION to NONUNIQUENESS. It uses the parametric minimum-cost flow construction of Disser and Skutella, *The Simplex Algorithm Is NP-Mighty*, ACM Transactions on Algorithms 15(1), Article 5 (2018), DOI 10.1145/3280847, Sections 3.1–3.2 and Corollary 1.7. Public source: https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf .

The rank-1 equilibrium/parametric-LP equivalence is also proved directly below; no nondegeneracy assumption is used.

## 1. Source network and the source-quantifier issue to audit

For positive integer partition weights w_1,...,w_n, S=sum w_i, take a_i=w_i/(24S), epsilon_0=1/(24S). Then sum a_i=1/24<1/12, and every a_i is an integer multiple of epsilon_0. The DS construction has two gadgets, with signs +a and -a. Gadget sign v has nodes s_i,t_i (0<=i<=n); arc s_0 -> t_0 has capacity 1 and cost epsilon_0/5. For 1<=i<=n, add:

- s_i -> s_{i-1} and t_{i-1} -> t_i, each capacity 2^{i-1}, cost v_i/2;
- s_i -> t_{i-1} and s_{i-1} -> t_i, each capacity 2^{i-1}, cost (2^i-1-v_i)/2.

Add global s,t, and arcs s -> s_n, t_n -> t for each gadget, capacity 2^n and cost 0. The distinguished arc e goes from s_0 in the + gadget to t_0 in the - gadget, capacity 1 and cost 0. This graph is acyclic. Its maximum flow value is F=2^{n+1}. A zero-e maximum flow exists (both gadgets in their terminal state).

DS Lemma 3.2 proves that successive shortest paths (SSP), each augmenting one unit, uses e if and only if the partition instance is yes. When it uses e forward, the e-flow rises from 0 to 1 and is removed in the immediately following augmentation. Therefore, in a yes instance, some minimum-cost flow of half-integer value q<=F-3/2 has f_e=1/2. The continuous interpolation during an SSP augmentation is optimal at the intermediate flow values.

**All-optimal quantifier, with an explicit robustification.** A statement about one selected unperturbed SSP path is not by itself sufficient. Let D be the least common multiple of the denominators of the original arc costs and enumerate the p arcs by i=1,...,p. Add

rho_i = 1/(4D 3^i)

to arc i's cost. The sum of all perturbations is less than 1/(8D). Every simple residual path has a signed incidence vector with entries in {-1,0,1}, so changing costs perturbs a difference of two path costs by less than 1/(4D). Every original nonzero path-cost difference is an integer multiple of 1/D. Consequently every perturbed shortest path is an original shortest path in the same residual network: the perturbation can only break original ties. Residual capacities and augmentation amounts do not depend on costs. Inductively, the entire perturbed SSP execution is therefore a legitimate execution of the original SSP algorithm. DS Lemma 3.2 states its conclusion for SSP without imposing a special tie-breaking rule, so the perturbed execution uses e if and only if PARTITION is yes. This coupling avoids assuming that the authors' descriptive sequence was the only possible unperturbed execution.

There is no simple residual cycle with nonzero projected arc-incidence vector and zero perturbed cost. To see this, consider a simple directed residual cycle with nonzero projected arc-incidence vector sigma in {-1,0,1}^p. Its original cost is either a nonzero multiple of 1/D, whose sign cannot change, or zero. In the latter case its perturbed cost is sum sigma_i/(4D 3^i), which is nonzero: the earliest nonzero ternary digit strictly dominates the sum of all later digits. The formal two-cycle consisting of the forward and reverse copies of the same original arc has zero projected incidence and is irrelevant; it changes no flow.

For each fixed real flow value q, the minimum-cost flow is unique. If f and g were distinct optima, their difference could be decomposed sign-conformally into directed residual cycles of f. Optimality of f makes each such cycle nonnegative in cost. Since the total cost difference is zero, at least one nonzero cycle would have zero cost, a contradiction. This argument applies to fractional q, not only to integral network vertices.

The perturbed SSP curve, including its linear interpolation within each augmentation, gives an optimum at each q. Therefore, in a no instance, EVERY optimum has f_e=0. In a yes instance, the perturbed SSP execution still has a unit augmentation on which f_e rises from 0 to 1, and its halfway flow is the required unique optimum with f_e=1/2.

Make every arc cost strictly positive by adding a topological potential: cbar_(u,v)=cpert_(u,v)+H(r(v)-r(u)), where r is a topological ordering and H=1+max_i |cpert_i|. For fixed feasible flow value q this adds only H(r(t)-r(s))*q, so it does not change the optimizing flows. All encoded sizes remain polynomial in the partition input length.

## 2. A simplex containing the relevant flows, with controlled parameter range

Let p be the number of arcs and let L=|V|-1, an upper bound on the number of arcs in a directed path. Every feasible nonnegative flow in the DAG satisfies sum_i f_i <= L q, by path decomposition. Set

K=1/(2L), epsilon=K/2.

Use x=(x_0,x_*,x_1,...,x_p) in the standard simplex. Define affine-linear quantities (in fact linear):

h = F(1-x_0),
f_i = LF x_i,
q = h-K f_e.

The simplex automatically gives f>=0, 0<=h<=F, sum f_i<=Lh, and
q >= h-K Lh = h/2 >=0.

Conversely, any f>=0,h with sum f<=Lh and 0<=h<=F has the unique simplex representation
x_i=f_i/(LF), x_*=h/F-sum f_i/(LF), x_0=1-h/F.

Impose network capacities f_i<=u_i, network flow-conservation equations Df=q d (d has +1 at s, -1 at t), and the parameter equation q=lambda. Write these as finitely many inequalities
R x <= r+s lambda.

Let c in simplex coordinates satisfy c^T x=sum_i cbar_i f_i. For lambda in [0,F], the resulting LP is feasible: scale a zero-e maximum flow, so h=q=lambda and sum f<=Llambda. Its feasible set is compact.

In a no instance, the unique original minimum-cost flow at every lambda has e-flow 0, hence h=lambda<=F and lies in the simplex. Thus the restricted LP has exactly the original optimum flow, with f_e=0.

In a yes instance, take the original optimal SSP flow with f_e=1/2 at q=lambda<=F-3/2. Then h=lambda+K/2<F and sum f<=Lq<=Lh. This original optimum remains feasible and optimal in the restricted LP.

## 3. Uniform exact-penalty lemma

For lambda in [0,F], consider
min c^T x subject to x in the simplex and Rx<=r+s lambda.

There is a positive integer M with polynomial binary encoding length such that, for every lambda in this interval, ALL minimizers of

phi_lambda(x)=c^T x+M max(0,max_j (R_jx-r_j-s_j lambda)), x in simplex,

are feasible and optimal for this LP.

Proof: the dual has variables mu>=0 and nu free, constraints
nu*1 <= c+R^T mu,
and objective nu-(r+s lambda)^T mu. Its feasible polyhedron is independent of lambda and nonempty (take mu=0 and nu<=min_i c_i). It is pointed: a direction that generated an entire line would have zero mu coordinates because mu>=0, and then zero nu coordinate because of the upper-bound inequalities. Since the primal is feasible and compact, strong duality gives a nonempty attained dual optimal face. That face is a pointed polyhedron and has a vertex; a vertex of an optimal face is a vertex of the whole dual polyhedron, since every convex decomposition of an optimum into feasible points remains in that face. Clear all denominators in the dual constraints by one positive integer Q, and let H_0>=1 bound every absolute integer coefficient and right-hand side after clearing. Put d_0=k+1, where k is the number of rows of R. Cramer's rule bounds each coordinate of every dual vertex by d_0! H_0^{d_0}. Therefore C=k*d_0! H_0^{d_0} uniformly bounds ||mu||_1 for a choice of optimal dual vertex. Take M=C+1.

For delta_x=max(0,max_j (R_jx-r_j-s_jlambda)), weak duality gives
c^Tx >= optimum-||mu||_1 delta_x.
Hence phi_lambda(x)>=optimum+(M-C)delta_x, strictly above optimum if delta_x>0. Feasible minimizers attain the original optimum. The encoded lengths of Q,H_0,C,M are polynomial.

## 4. Form the rank-1 game

Include index j=0 for the zero-violation affine function (R_0,r_0,s_0)=(0,0,0). Define

G_j = c+M R_j^T-M r_j*1,
b_j = -M s_j,
A_{:,j}=-G_j,
a_0=-epsilon,
a_i=F-epsilon for every i!=0,
B=-A+a b^T.

Then A+B=a b^T has rank exactly 1: a is nonzero and b contains both +M and -M from the two parameter-equation inequalities.

The row player's optimal strategies in the zero-sum game (A-1*lambda*b^T,-A+1*lambda*b^T) are exactly minimizers of
max_j[-A_{:,j}^T x+lambda b_j]=phi_lambda(x).

The original game equilibria are exactly auxiliary zero-sum equilibria satisfying
lambda=a^T x=h-epsilon.
This follows because replacing a by the constant vector 1*lambda changes no column expected payoff when a^Tx=lambda, while the row payoff shift -lambda*b^T is constant across rows. Conversely every original equilibrium yields such an auxiliary equilibrium by setting lambda=a^Tx.

All candidate lambdas automatically lie in [-epsilon,F-epsilon].

## 5. Unique default equilibrium; no extraneous negative-parameter equilibria

For lambda<0, the penalty includes the violation q-lambda, which is positive everywhere because q>=0. Since c^Tx>=0 and q>=h/2,
phi_lambda(x)>=c^Tx+M(q-lambda)>=-Mlambda.
At x=x_0 (mass 1 on row 0), f=h=q=0. All conservation violations vanish, capacity violations are negative, and only q-lambda is positive, so phi_lambda(x_0)=-Mlambda. If x!=x_0 then h>0, whence q>0 and the inequality is strict. Thus x_0 is the unique optimal row strategy for every lambda<0, and its only possible hyperplane intersection is lambda=-epsilon.

At lambda=-epsilon, the unique maximizing penalty column is q-lambda. Therefore there is exactly one equilibrium there: the pure pair (row 0, column q-lambda). It is strict. Directly, row 0's A-payoff in that column is 0 and every other row has payoff -(c_i+M q_i)<0; at row 0 the selected B-payoff is M epsilon, all conservation/baseline columns give 0, the opposite parameter column gives -M epsilon, and capacity columns give -M u_i.

## 6. Positive-parameter intersections are exactly f_e=1/2

For lambda>=0 every auxiliary optimal x is feasible for the network LP by the exact-penalty lemma. Thus q=lambda. The hyperplane equation is
lambda=h-epsilon=q+Kf_e-epsilon,
i.e. f_e=epsilon/K=1/2.

No partition: all optimizing flows have f_e=0, hence the default pure equilibrium is the only equilibrium.

Yes partition: the half-augmentation optimum from Section 2 has f_e=1/2 and lambda in [0,F-epsilon]; its x therefore intersects the hyperplane. Any optimal opposing zero-sum strategy gives an additional original-game equilibrium. It is distinct from the default.

Thus PARTITION reduces in polynomial time to NONUNIQUENESS, with the no instances mapped to exactly one equilibrium and the yes instances to more than one equilibrium. Equivalently, the complement of PARTITION reduces to UNIQUENESS. This proves the candidate coNP-hardness theorem, even for instances with a known strict pure equilibrium. Combining with the rational-certificate argument in certificates/LEMMA_REPORT.md gives coNP-completeness, with arbitrary degeneracy explicitly allowed.

## 7. Encoding size, degeneracy, and verification limits

If the PARTITION instance has n weights, the graph has 4n+6 vertices and 8n+7 arcs. Thus the game has 8n+9 rows and 16n+22 columns. Its maximum flow value F has n+2 bits; every individual arc capacity also has O(n) bits. The denominators of normalized weights and the common denominator D have polynomial encoding length. The generic perturbations require O(p+log D) bits each; positive topological potentials, L,K,epsilon, and all coefficients R,r,s,c also have polynomial length. The determinant bound M satisfies log M=O(k log k+k log H_0), hence has polynomial length. Forming all matrices is consequently a polynomial-time exact-arithmetic computation. No exponential enumeration or execution of SSP is part of the reduction: SSP is used only in the correctness proof.

The constructed games are not asserted to be nondegenerate. The proof controls all auxiliary optimal strategies, not just selected basic solutions. It proves uniqueness of both players' strategies at the default crossing, and rules out every other crossing in no instances. In yes instances it requires only existence of one additional pair; a positive-dimensional additional equilibrium set would still be a correct yes instance. No perturbation of the game matrices to force nondegeneracy is used.

The standard-library script computation/verify_reduction.py supplies exact rational regression checks. Six complete game constructions verify the identity A+B=ab^T, a strict default equilibrium, and all yes-case additional equilibrium pairs by exact best-response inequalities; it uses the stated determinant-bound M. An additional 39-case network sweep matches brute-force PARTITION. These finite checks support reproducibility but are not evidence replacing the quantified proof. Independent audit and acceptance remain separate from this candidate manuscript.
