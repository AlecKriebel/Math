# Independent source-first hand derivations

These deductions were made from the actual original manuscript before any support/proof-code/results/foreign/current-opinion body. No mathematical program was executed. They are checkable derivations and controls, not finite-test claims and not a full-original disposition.

## 1. Two-terminal graph and possible hidden matching states

With ell=bits(W), the initial DAG s->t has one path. Appending binary bit b adds t->z, t->a, a->z and, only for b=1, s->z. Since a,z are fresh and placed after every old vertex, all arcs are forward with no duplicate. Each old s-t path has two extensions, while the optional direct path is new. Thus w maps to2w+b, giving exactlyW paths, 2ell vertices and <=4ell-3 arcs.

Split an internal vertex i into L_i,R_i with identity edge L_i R_i; retain L_s and R_t as terminals and replace arc i->j by L_i R_j. A perfect matching either takes the identity at i or takes exactly one incoming and one outgoing selected arc there. Full matching therefore yields one source-to-sink path plus possible directed cycles; DAG acyclicity eliminates the cycles. Conversely the path fixes arc edges and off-path identities uniquely. After deleting both terminals, any nonempty chosen arcs would have balanced positive in/out degrees and therefore a directed cycle; only the all-identity state remains. Deleting exactly one terminal leaves odd order. This gives (W,1,0,0) without relying merely on the full count.

There are 2(2ell-2)+2=4ell-2 split vertices, 4ell-4 internal vertices, and <=(4ell-3)+(2ell-2)=6ell-5 edges. W=1 has precisely a single terminal edge, signature(1,1,0,0), no internal vertices. W=0 is not an allowed gadget call: zero input edges are removed first. Fresh internal labels and forward arcs preclude loops or parallel edges.

## 2. Gluing, simplicity and exact fiber law

Each gadget has even internal order, covered only by edges assigned to it. In a global perfect matching the number of old endpoints covered by that gadget is therefore even, hence0 or2. Every original vertex is covered once, so the two-endpoint gadgets form precisely an original perfect matching. A zero-endpoint gadget has one completion; a selected edge gadget has W_e completions. Conversely every such choice is a distinct global matching. Distinct internal labels prevent shared internal edges; an edge between two old endpoints can only come from their unique original-edge gadget (in fact W=1). Arbitrary local orientation changes no signature or fiber count.

For positive A_e=p_e/q_e, D=product(q_e), W_e=p_e(D/q_e) are positive integers, even for unreduced fractions. The fiber count is product(W_e:e in M)=D^m product(A_e:e in M); summing gives #PM(H)=D^m Z_A. No step needs cancellations, negative coefficients or a lower positive bound. Nonnegative support is essential.

Hand controls:

- m=0: D=1,H empty,#PM=1 and the unique matching is empty.
- All-zero support with m>0: H has2m isolated vertices and count0. A support obstruction/disconnected odd component likewise gives no perfect matching.
- Two vertices with A12=1/2: D=2,W=1,H a single edge,count1, giving haf=1/2.
- A12=2/3: D=3,W=2,ell=2,H has6 vertices; the DAG construction has2 paths, so count2 and terminal-deleted count1, giving2/3.
- Four vertices, positive A12=1/2,A34=3/5,A14=2,A23=1/3, all other pairs zero: D=30 and W12,W34,W14,W23=(15,18,60,10). The two original matching weights are3/10 and2/3; Z_A=29/30. Fibers270 and600 sum to870=30^2*(29/30). Bit lengths(4,5,6,4) give60 internal vertices plus4 old vertices, and edge upper bound19+25+31+19=94. The factor is D^m, not D or an extra gadget-dependent factor.

## 3. General graph is genuinely required

Although each split gadget is bipartite, gluing through original vertices need not admit a consistent global bipartition. For all six positive unit weights on four original vertices, each gadget is a single edge and H=K4. It has three perfect matchings and contains triangles. Thus a theorem only for bipartite permanent counting would leave the central FPRAS consequence unsupported. This is a dependency falsifier, not a counterexample to the source, which explicitly invokes general graphs.

## 4. Binary bit costs and diagonal/representation boundary

For an explicitly encoded matrix, 2m and the number r of positive entries are O(L). The sum of denominator bit lengths is bounded byL, hence bits(D)=O(L); each numerator also has O(L) bits, so bits(W_e)=O(L). Summing r logarithmic gadgets gives O(L^2) vertices/edges and another logarithm for endpoint names. Computing D^m uses O(mL+1) output bits. Each product/exact division is polynomial in these operand lengths; there is no unary expansion into W_e copies. Unreduced fractions may enlargeD but stay within the same bound. The diagonal never contributes to hafnian or graph construction.

This relies on an explicit matrix representation whose input length pays for its order/support, not an unstated succinct oracle representation of an astronomically large matrix. Rational epsilon,delta,eta encodings must be counted. A successful-tape runtime statement alone would not bound failed estimate output lengths or the sampler's all-tape arithmetic. That precise upstream every-execution claim remains to verify.

## 5. Exact-zero and approximation composition

On a feasible graph C=#PM(H)>=1. On a successful relative-epsilon estimate, C_hat>=(1-epsilon)C>0. Therefore changing a zero estimate to1 affects only failed tapes. Exact support feasibility already returns0 on every infeasible tape; the clamp forces a positive estimate on every feasible tape. Dividing by positive exact D^m preserves relative error. Delta'=min(delta,1/4)<=delta meets the asserted upstream parameter range, including delta>=1/2. On positive inputs Z_A>=D^-m, so very small rational values do not force super-polynomial encodings. Empty order bypasses the algorithm and returns1.

The argument needs a nonnegative rational result on every tape. A theorem returning signed errors, nonterminating failure executions or an unbounded-length representation would not meet this interface merely because it is informally called an FPRAS.

## 6. Counting self-reduction, failed estimates and adaptive histories

At a current feasible residual graph, each feasible child G-{v,u} has a positive integer count c_i. Matching completion bijections partition current matchings, so p_i=c_i/sum(c) are exactly the next-edge probabilities of a uniform matching. Products telescope along a deletion sequence, giving the ideal uniform law. Exact witnesses make every selected child feasible, including on failed counting tapes. A lone child requires no count. All estimates zero leads to a stored-witness completion, also always feasible; its distribution may be bad, but this event entails at least one failed positive-child estimate and is covered by the failure budget.

On successful estimates (1-alpha)c_i<=a_i<=(1+alpha)c_i. Summing and dividing yields (1-alpha)/(1+alpha)<=q_i/p_i<=(1+alpha)/(1-alpha). Therefore |q_i-p_i|<=2alpha p_i/(1-alpha), and TV(p,q)<=alpha/(1-alpha). This requires no lower bound on any nonzero p_i.

The exact integer CDF intervals floor(2^b Q_(i-1))<=R<floor(2^b Q_i) form a disjoint cover of every integer R in[0,2^b), because Q0=0,Qj=1 and floors are monotone. Zero-length intervals are harmless. Endpoint/floor arithmetic, not rounded floating-point arithmetic, is required. Per-coordinate mass error is bounded by2*2^-b (indeed the direct floor-difference bound is tighter, but no strengthening is needed), so categorical TV error<=j2^-b. There is no rejection loop.

Conditional on any prior adaptive history, the current graph and parameters are fixed before fresh independent counting tapes. A union bound then gives current estimation-failure probability<=j gamma. Charge discrepancy at most1 on that event. Couple actual and ideal processes only while histories agree; sum the conditional first-disagreement bounds. This avoids the invalid route of conditioning every step on a future global event that all calls succeeded. The accumulated bound is

TV <= k alpha/(1-alpha) + C gamma + C 2^-b.

At residual size2h there are at most2h-1 candidate neighbors. Summing over h=1..k gives k^2=C, bounding both the total candidate feasibility checks and the sum of outcome counts; one initial witness adds1. Thus there are at most C counting calls, C+1 feasibility calls and k categorical draws. With alpha=eta/(4k)<1/4, gamma=eta/(4C), b=ceil(log2(4C/eta)), the three terms are <=eta/3,eta/4,eta/4, whose sum5eta/6<eta. The stated strict bound has slack. k=1 has only the one possible feasible child and needs no count; the empty graph is handled separately. Infeasible input is recognized before sampling.

Exact summation/normalization of at mostN rational estimates of at mostT bits can be implemented by integer arithmetic with polynomially growing product denominators; no exponentially many terms are summed. The integer ceiling of the rational logarithm can be characterized by exact integer comparisons. At mostkb fair bits and no rejection plus witness fallback give deterministic termination, conditional on all-tape termination of the imported algorithms. Tiny branch probabilities cause additive TV loss only; they do not imply pointwise almost-uniformity.

## 7. Weighted projection and what is still unproved here

Uniform law on H assigns an original matching M exactly its fiber size divided by #PM(H), namely D^m product(A_e)/(D^m Z_A). For any approximate law, deterministic projection contracts TV by grouping terms and applying the triangle inequality. This proves the weighted-law consequence conditional on the uniform sampler/oracle interfaces; no additional assumption that the fibers have equal size is appropriate.

No local counterexample has been obtained in these hand checks, but the full-original approximation and sampling conclusions remain pending substantive verification of the cited general-graph FPRAS proof and exact algorithmic interface. The finite native enumeration described by the manuscript cannot certify a universal polynomial randomized algorithm. I have not yet read or run it. No primary body is yet read, and no priority assertion is independently established. A central gap, if found, affects the full original claim and must be recorded as such rather than repaired or narrowed.
