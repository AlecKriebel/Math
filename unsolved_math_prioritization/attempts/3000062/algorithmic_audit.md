# Orientation-compatible integer multicover: algorithmic audit

Date: 2026-10-21. Exact target: row 1872, ID 3000062. This is authored mathematical analysis, not a copied source. No general polynomial-time algorithm or matching hardness theorem is claimed. No publication or queue change is part of this audit.

## Scope and primary sources

The input is a finite digraph with nonnegative even integer arc weights W. The output must be a nonnegative integer vector x with x_u+x_v >= W_uv on every arc, and, whenever x_v>0, at least one **incoming** arc u→v with equality. Binary input complexity matters. Empty vertex sets and instances with all weights zero have the immediate all-zero answer; subsequent formulas using 1/n or normalization by M assume n>=1 and M>0.

Existence and the indegree-one polynomial algorithm were already proved in Király–Pap, EGRES TR-2012-04, Theorem 3.4 and Proposition 3.5, https://egres.elte.hu/tr/egres-12-04.pdf. The question immediately following Theorem 3.4 asks for a general polynomial algorithm. The submitted 2013 manuscript is https://real.mtak.hu/20824/1/dm_submission.pdf. The source gate and metadata in the parent directory document the recovery. The paper's broader PPAD-completeness results do not establish hardness of this exact graph problem.

## Approach 1: exact fixed points and removal of integrality

Define F_v(x)=max({0} union {W_uv-x_u : u→v}). The required conditions are exactly x=F(x): feasibility gives x>=F(x); a positive coordinate's incoming equality supplies the reverse inequality; a zero coordinate already equals F_v(x). This also handles sources, whose fixed-point coordinate is zero. A loop contributes W_vv-x_v and hence the correct constraint 2x_v>=W_vv.

F is coordinatewise antitone, convex in each output, and 1-Lipschitz in the sup norm. With M=max W (or zero for an empty arc set), F maps [0,M]^n into itself. Every solution is in this box.

Let R be nearest-integer rounding with ties to even. R is monotone, R(0)=0, and R(W-t)=W-R(t) for every even integer W and every real t. The last identity follows from reflection symmetry of nearest-integer rounding around an integer and invariance under translation by an even integer, including tie cases. Monotonicity preserves finite maxima. Consequently R(F(x))=F(R(x)) coordinatewise. Any real fixed point therefore yields an integer fixed point by R. This is a valid reduction, not a computation of the real fixed point.

### Robust rounding of an approximate fixed point

A stronger exact recovery statement holds. Suppose x is rational and nonnegative, and ||F(x)-x||_infinity <= epsilon < 1/n. For t in (0,1), define R_t with transitions from even 2k to odd 2k+1 at 2k+t, and from that odd integer to even 2k+2 at 2k+2-t. Choose the even value at transition points. This is a monotone integer-valued map, fixes zero, and satisfies R_t(W-z)=W-R_t(z) for even W. Thus it also commutes with F.

Put phi(z)=dist(z,2Z), which takes values in [0,1] and is 1-Lipschitz. For each coordinate let I_v be the closed interval between x_v and F_v(x). The image phi(I_v) is an interval of length at most epsilon. Their union has length at most n epsilon<1. Choose rational t in (0,1) outside that union. No I_v crosses a transition of R_t, so R_t(x_v)=R_t(F_v(x)). Therefore R_t(x)=F(R_t(x)), exactly.

Computing F, the forbidden intervals and a rational point in their complement is polynomial in the rational input bit lengths. For example epsilon=1/(4n) suffices. Fixed nearest-integer rounding alone does not give robust recovery: on a two-cycle of weight 2, x=(1/2+eta,3/2+eta) has residual 2eta, arbitrarily small, but rounds to (1,2), not a fixed point. The adjustable threshold is essential to this proof. This does NOT establish a polynomial approximate-fixed-point algorithm. On normalizing the box to [0,1]^n, this requires error 1/(4nM), not a weight-independent tolerance. No claim of novelty is made for either rounding lemma.

## Approach 2: ordinary LP and convex optimization

Minimizing the sum of coordinates over the cover polyhedron does not enforce incoming tightness. On arcs s→a and s→b, each of weight 2, the unique minimum-sum nonnegative cover is (2,0,0): for x_s<=2 the minimum total is 4-x_s, and for x_s>=2 it is x_s. The positive source has no incoming witness. The valid answer (0,2,2) has larger total. Integrality of the cover polyhedron cannot repair this failure.

Nor is the required solution set generally convex. Take arcs 1↔2 of weight 4, 1→3 of weight 2, and 2→3 of weight 4. Both (0,4,2) and (2,2,2) are fixed points. Their midpoint (1,3,2) is feasible but maps to (1,3,1), so vertex 3 lacks incoming tightness. This rules out treating the exact fixed-point set itself as an ordinary convex feasible region. It does not rule out an extended formulation with a different decoding.

## Approach 3: iteration, two-cycles, and contraction

Synchronous F iteration need not converge. Even the two-vertex cycle with equal positive weights has 0↔(W,W). Since F^2 is monotone, the sequence l_0=0, l_(k+1)=F^2(l_k) is nondecreasing and bounded by M. With integer data it stabilizes after at most nM strict iterations, yielding l and u=F(l) with F(u)=l. This bound is only pseudo-polynomial. Stabilizing the interval does not necessarily produce a fixed point. There is an explicit binary-size lower bound even when the iterates do converge: take 2→1 of weight 2K+2 and 1→2 of weight 2K. From zero, F^(2t)(0)=(2t,0) for 0<=t<=K+1, and F^(2t+1)(0)=(2K+2,2K-2t) for 0<=t<=K. The unique fixed point is (2K+2,0), reached only after Theta(K) synchronous iterations. This is exponential in the bit length of K, although the graph has only two vertices and indegree one.

In particular, the midpoint of such a two-cycle need not work. On arcs 2→1 of weight 2, 2→3 of weight 4, and 3→2 of weight 4, F(0)=(2,4,4) and F(2,4,4)=0. The midpoint (1,2,2) maps to (0,2,2). Convexity ensures the midpoint is a feasible cover, but not the required incoming witnesses.

The discounted map F_lambda,v=max(0,max incoming(W_uv-lambda x_u)), 0<lambda<1, is a contraction and has a unique fixed point x_lambda in [0,M]^n. Its original residual is at most (1-lambda)M. Taking 1-lambda sufficiently small and applying robust rounding is a valid approximate route, but contraction iteration then has a bound proportional to 1/(1-lambda), hence proportional to M for this choice. This route has not supplied a binary-input polynomial bound. No claim that every implementation actually needs that many steps is made. Moreover sup-norm nonexpansiveness cannot simply be replaced by finite-p nonexpansiveness: a star s→a,s→b of weight 2 sends a small change delta in x_s to two output changes of magnitude delta, expanding the finite-p norm by 2^(1/p).

## Approach 4: witness policies and exact exhaustive search

For each vertex independently choose either its zero constraint, or an incoming arc intended as a tight witness. Add the selected equalities to all cover inequalities and x>=0. Feasibility of each resulting rational linear system is polynomial-time decidable. If feasible, monotone reflection-compatible rounding preserves all cover inequalities and selected equalities, producing an integer answer. Every genuine solution belongs to at least one policy system. Thus this is a complete finite exact algorithm using at most product_v(1+d_in(v)) LP checks. That count is exponential in general.

An arbitrary choice of one incoming arc is unsound. Use arcs 2↔3 of weight 2, 2→1 of weight 2, and 3→1 of weight 6. Solving the selected functional subgraph using 2→1 forces x_1<=2 and x_3<=2, leaving the omitted weight-6 arc uncovered. A policy-improvement bound or other polynomial method for selecting policies remains missing.

## Approach 5: SCC decomposition and correction of the known cycle algorithm

Process strongly connected components in topological order. Values of external predecessors are then fixed. Define b_v=max({0} union {W_uv-x_u : u outside the component, u→v}). The remaining equations are x_v=max(b_v,max internal incoming(W_uv-x_u)). If b_v>0, some external incoming arc is tight whenever x_v=b_v.

This yields a polynomial construction when each nontrivial SCC is a directed cycle, even if global indegrees exceed one. Parallel arcs can be collapsed to their maximum weight. A singleton without loops takes x_v=b_v; with loops it takes max(b_v,max_loop W_vv/2), an integer because loop weights are even.

For a directed cycle indexed modulo k, solve x_i=max(b_i,W_(i-1,i)-x_(i-1)). First test the all-internal-tight equations x_i+x_(i+1)=W_(i,i+1), with x_i>=b_i. For odd k these determine the coordinates uniquely as half alternating sums of even weights, hence integers. For even k they give either inconsistency or one free parameter, with integer interval endpoints imposed by the integer lower bounds. An integral choice is available whenever feasible.

If not all cycle arcs can be tight, every solution has some coordinate x_i=b_i: failure of an internal equality leaves the baseline branch active. Try each anchor i, set x_i=b_i, propagate the max recurrence once around the cycle, and verify the closing equation. Existence of a solution to this restricted component problem follows by extending the fixed upstream assignment to a real fixed point of its continuous box self-map and then applying rounding, which also fixes integer baselines; alternatively use the explicit clamp-composition fixed-point argument. Rounding fixes each integer baseline b_v, so R(max(b_v,z))=max(b_v,R(z)); noninteger baselines would need separate treatment. The baselines here are integers because upstream coordinates and arc weights are integers.

The source manuscript's 'minimum of 0 and residual' cannot be the intended recurrence: nonnegativity and incoming tightness force max(0,W_previous-x_previous). In the paper's W=2w convention the positive run from a zero anchor is 2w_(i-1,i)-2w_(i-2,i-1)+... with alternating signs; omitting the factors 2 changes the task. This audit corrects the algebra only and does not claim the indegree-one case as a new solution.

The SCC extension does not handle a general strongly connected digraph with branching incoming choices. It relocates the unresolved part into those SCCs rather than resolving it.

## Checks and disposition

`check_algorithms.py` uses exact rational arithmetic, verifies the LP/midpoint counterexamples, and checks rounding on all 729 loopless three-vertex digraphs with each possible arc absent or of weight 2 or 4 over the half-integral grid [0,4]^3. This finite check is not a proof of the general rounding lemma, which is proved above. The associated JSON records check counts. A second exact-rational script, `check_robust_rounding.py`, tested 30,000 seeded random instances/vectors, found 624 satisfying the approximate-residual premise, and successfully recovered an exact integer fixed point in every such case; `robust_check_results.json` records the results. It also checks the explicit failure of fixed nearest rounding at arbitrarily small residual. These are finite checks, not substitutes for the proofs.

An independent adversarial reviewer checked the main identities and counterexamples and highlighted singleton-loop and parallel-arc caveats, included above. A separate review note records its disposition.

Conclusion: useful exact reformulations, robust rounding, explicit failures of natural shortcuts, an exponential exact algorithm, and a restricted SCC algorithm have been established. The unrestricted binary-input polynomial-time construction remains NOT SOLVED by this work. Neither a fresh existence proof nor a special-case construction changes that disposition.
