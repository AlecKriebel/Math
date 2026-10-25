# Independent reconstruction and attacks

This derivation was reconstructed from all nine published pages and the primary mathematical interfaces. Fresh standalone checks were completed before reading the supplied mathematical helper code. The conclusion concerns the exact theorem, not priority.

## 1. Flow event and all choices

For positive integer weights, S>0, alpha_i=w_i/(24S), eta=1/(24S), delta=eta/5. Every signed sum z_j is an integer multiple of eta; thus either z_j=0 or |z_j|>=5delta. The two recursively signed gadgets are the actual Disser–Skutella construction, not merely an appeal to generic flow hardness. The source's journal Section 2 assumes sum alpha_i<1/12, met here by 1/24. Figure 1's crossed edge cost is (2^i−1−sigma alpha_i)/2; the manuscript preserves it.

At synchronized state j, the within-gadget marginal costs are j+z_j+(-1)^j delta and j−z_j+(-1)^j delta. The bridge cost is j when j is even, j−2delta when odd. If z_j!=0, the cheaper whole gadget beats the bridge by at least 4delta in the even case and 4delta in the odd case as well after comparing |z_j| with delta. The other gadget then catches up, because adjacent recursive state bands are separated by 1−2(T+delta)>0. If z_j=0 the bridge wins strictly, and the next shortest path reverses it. The two-step update is the same synchronized state advance; the arc/base capacities give unit bottlenecks. The underlying journal Lemmas 3.1–3.2 prove the state induction; the manuscript corrects the printed first-level second-path constant and includes the missing delta in its cost envelope. Those corrections agree with the actual arc formula.

The forward event occurs at total demand 2j. Every yes case therefore has the midpoint q=2j+1/2 and f_e=1/2, with q<=F−3/2; every no execution has no event. This statement quantifies over all shortest choices. Fresh exhaustive searches over all reachable shortest-path choices for 12 small source instances agree, but the universal conclusion rests on the state proof and strict comparisons, not those finite searches.

The source graph is acyclic even though cheap signed costs can be negative. Hence the zero flow is the sole value-zero feasible flow and is optimal. The explicit top-level saturated routing is a zero-bridge value-F feasible flow even at n=1; scaling provides all real demands in [0,F]. No unproved availability of arbitrary demands is needed.

## 2. Perturbation, real demands and positive costs

With common denominator D, every nonzero original simple path-cost difference is at least 1/D in absolute value. Each path uses an original arc with sign in {-1,0,1}; two paths differ by coefficients bounded by two. Since sum rho_i<1/(8D), the perturbation changes a path comparison by less than 1/(4D). Thus the chosen perturbed shortest path is an unperturbed shortest path in the very same residual state; induction identifies a legitimate original SSP execution. Comparing paths in different residual states would be insufficient, but is not the argument used.

For a nonzero projected simple residual cycle, an originally nonzero cost keeps its sign. An originally zero cost becomes nonzero because the first nonzero ternary digit rho_i strictly exceeds the finite tail sum. Formal forward/reverse two-cycles project to zero and change no original flow; they are explicitly excluded from the nontrivial claim.

Suppose two distinct real feasible flows at one demand were optimal. Their difference is a sign-conformal residual circulation of the first. Decompose into positive multiples of simple cycles, using only the sign selected for each original arc. This prevents a formal zero-projection cancellation. Each cycle must have nonnegative cost by optimality; total cost zero forces an actual nonzero projected cycle with zero cost, contradicting the perturbation. Capacitated compactness ensures existence for all real feasible demands. This proves uniqueness for irrational as well as rational demand, without an integrality inference.

If an optimal flow is augmented partway along a shortest residual path of cost ell, any competitor at the increased demand differs by an s–t residual flow plus cycles. Its s–t path costs are >=ell and cycles are nonnegative; hence the interpolation is optimal. Repeating through SSP covers [0,F]. Topological potential addition contributes only H(r(t)−r(s))q at fixed demand and zero on cycles, so all optima/events are preserved and every original edge cost becomes positive.

Adversarial concerns addressed: signed cheap costs do not invalidate the zero start on a DAG; rational perturbations are chosen once before demand varies; isolation of real-demand optima does not assert distinct costs for all feasible flows; the potential shift is not an arbitrary cost increase.

## 3. Injective simplex and all feasible optima

Let L=V−1, K=1/(2L), epsilon=K/2. A nonnegative DAG flow decomposes into paths of at most L edges, so sum f_i<=Lq. The simplex construction gives f_i=LF x_i, h=F(1−x_0), q=h−K f_e. Because sum f_i<=Lh for every simplex point, q>=h−K sum f_i>=h/2. Thus q>0 at every point other than pure row zero, including the slack/star row and every arc row.

For fixed (f,h), the inverse coordinates x_i=f_i/(LF), x_*=h/F−sum f_i/(LF), x_0=1−h/F are unique. There is no extraneous slack multiplicity. The conservation and parameter equalities are included with both signs and all V rows; redundancy affects neither feasibility nor the later determinant argument.

For no source instances the unrestricted optimum has f_e=0, hence h=q=lambda<=F and its inverse lies in the simplex. Consequently the restricted optimum is the same unique flow; every restricted optimum has zero bridge flow. For a yes source midpoint, h=q+K/2<F because q<=F−3/2 and K/2<3/2. The DAG bound sum f_i<=Lq<=Lh makes its inverse feasible. Thus the needed actual midpoint survives the simplex restriction. The proof does not claim every unrestricted optimum at every demand survives that restriction on yes instances.

## 4. Uniform penalty, including degenerate faces

The simplex LP dual is max nu−(r+s lambda)^T mu, subject to mu>=0 and nu*1<=c+R^T mu. Its feasible set is independent of lambda, nonempty, and contains no affine line: nonnegativity forces any line's mu direction to vanish, then the nu upper bounds force its direction to vanish. For each real lambda in [0,F], primal feasibility and compactness plus LP duality give a nonempty attained optimal face. A nonempty pointed polyhedral face has a vertex, which is also a vertex of the original polyhedron, even if the optimal objective has irrational coefficients.

Clear denominators in the fixed dual constraints and bound all integer coefficients/right sides by H0. A vertex has d0=k+1 independent active equations, including in lower-dimensional faces; otherwise a small movement in both directions within all active hyperplanes contradicts extremality. Cramer's rule yields each coordinate <=d0! H0^d0 in magnitude. Therefore some optimal mu has 1-norm <=C=k d0! H0^d0 uniformly in lambda. One computes M=C+1, not the vertices.

For residual maximum Delta>=0, dual feasibility gives c^T x>=v(lambda)−C Delta. Adding M Delta gives phi>=v+(M−C)Delta. Every infeasible point is strictly worse; feasible minimizers are exactly the original optima, with no selection of an optimal face. Equality M=C would not suffice in general, and zero penalty admits the infeasible origin at positive demand. Both are falsifiable boundary controls (the supplied replay additionally checks an exact toy example at M equal to the dual norm).

The output M can have enormous numerical value while polynomial binary length. The common denominator may be an LCM or the product; log H0 remains polynomial and log M=O(k log k+k log H0). No parameter-dependent denominator or enumeration of exponentially many bases appears.

## 5. Exact rank one and exhaustive equilibrium correspondence

With baseline penalty column, A_j=−c−M R_j^T+M r_j 1 and b_j=−M s_j. The two q=lambda inequalities give b entries ±M, while a_0=−epsilon is nonzero. Thus A+B=ab^T has exact rank one, not merely rank at most one. The construction outputs m=8n+9, N=16n+22 explicitly listed rational entries.

For A_lambda=A−1 lambda b^T, a fixed y shifts all row action payoffs by the same constant. If lambda=a^T x, the original column payoffs −x^T A+(a^T x)b^T equal the auxiliary −x^T A_lambda. Hence all row and column best-response sets agree, including zero supports and nonunique optimal opposing strategies. Conversely any original equilibrium chooses its own lambda=a^T x. This is the complete correspondence in Adsul et al.'s journal Theorem1 (v4 Theorem7), not a claim that a selected parameter path contains all equilibria merely by continuity.

For lambda<0, the q−lambda penalty gives phi>=c^T x+M(q−lambda)>=−M lambda. Row zero attains equality; every other simplex point has q>0 and is strictly worse. Consistency forces lambda=−epsilon. Against row zero, the diagnostic column alone has positive original payoff M epsilon; other columns have zero, negative inheritance residual, or negative capacity payoff. Against that column, every other row has payoff −c_i−M q_i<0, while row zero has zero. Thus this is one strict pure pair, not just a unique row strategy with a continuum of column choices.

Every other candidate lambda lies in [0,F−epsilon], so the uniform penalty forces q=lambda. The scalar equation becomes K f_e=epsilon, exactly f_e=1/2. At lambda=0 the DAG gives zero flow, so there is no crossing. No source instances have f_e=0 at every optimum and therefore no nonnegative crossing or hidden opponent. Yes source instances supply the retained midpoint; minimax supplies an optimal y and the correspondence produces a second actual equilibrium. Degenerate or positive-dimensional yes sets are allowed and irrelevant to no-case uniqueness.

## 6. Membership and encoding boundaries

The source's capacities are binary powers with O(n) bits; F has n+2 bits. Original cost denominators divide 240S; ternary isolation adds O(p) bits. Topological shifts, simplex coefficients and M have polynomial bit length. The exponential SSP curve is used only to prove correctness and is never executed by the reduction producing the game. Hardness is ordinary weak NP/coNP hardness from positive-integer Partition, not strong hardness or a fixed-dimension/nondegenerate promise theorem.

For actual supports I,J, the closed sets X(I,J),Y(I,J) are compact rational polytopes. All used rows are best responses to every y in Y, and all used columns are best responses to every x in X, so their product consists entirely of equilibria even if some declared support coordinates vanish. Conversely every equilibrium belongs to its actual-support cell. The finite union is not asserted convex or of polynomial cardinality.

Every nonempty cell is the convex hull of its product vertices. If all cell vertices coincided, every cell and the equilibrium set would be that singleton. Thus any nonsingleton equilibrium set has two distinct rational vertex pairs. Clearing rational payoff denominators gives polynomial-bit integer comparisons; the independent-active-equation argument and Hadamard/Cramer bounds give polynomial-bit coordinates even with redundant constraints, boundary supports or lower-dimensional cells. The two-pair verifier checks simplex membership, distinctness and both exact payoff inequalities; averages make those inequalities sufficient.

Finite-game existence makes uniqueness/nonuniqueness complementary on valid rank-one inputs. The ordinary languages themselves both reject malformed and rank-invalid input; the complement of uniqueness adds the easy malformed/rank-invalid branch. Exact pivot identities test rank one in polynomial time. These definitions avoid the incorrect claim that the two ordinary languages are literal complements on every bit string. The reduction always outputs valid exact-rank-one games, so complementing the restricted source decision establishes coNP hardness. The strict default pair is explicitly available with the output.

## Conclusion and limits

The quantified argument survives the examined attacks at its stated scope. Finite exact checks support—not replace—the source induction, real-demand cycle proof, uniform dual bound and support-cell certificate proof. No substantive defect was identified. This is an independent AI mathematical review, not conventional human peer review or formal proof-assistant certification. Priority and exhaustive literature novelty are outside this adversarial conclusion.
