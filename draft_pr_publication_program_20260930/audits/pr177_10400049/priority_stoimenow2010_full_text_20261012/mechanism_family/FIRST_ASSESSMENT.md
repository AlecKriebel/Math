# Independent first assessment: Stoimenow 2010 mechanism priority

UTC: 2026-10-13T03:13:08.178508+00:00
Owner-task completion estimate: 65%. Overall PR177 estimate remains 40%.

Independence: I have read no sibling or root reports or hypothesis files. This assessment uses only the assigned task, the user-supplied paper, and mathematical deductions explicitly identified below.

## First substantive assessment

The supplied paper contains prior published tools sufficient for the exact PR177 obstruction after an elementary extra algebraic deduction. It does not itself state an arbitrary-ideal actual-link Nullstellensatz refutation, construct the ideal g(4g-1)V, define the half-twist character, or compare the radical of an ideal with the ideal of its actual-link zero set. Its algebraic-dependence statements concern polynomial identities among selected invariants and determination on specified classes of knots; its growth and norm statements concern the order filtration and asymptotic bounds. These are not the same assertions as an actual-link zero-set/radical identity.

The material mechanism is already present: Definitions 2.2--2.3 and Theorem 2.1 (journal pp. 690--691, with prior work cited as [63]) give polynomial restrictions of every finite type invariant on braiding sequences, for an arbitrary fixed component number and complex coefficients. On the even two-strand braid closure family L_n = closure(sigma^(2n)), finite differences of a degree-d invariant vanish beyond d, so each restriction is a unique polynomial P_v(n). Restriction defines a homomorphism from the entire ordinary finite-order invariant algebra to C[n], since polynomial equality follows from equality at infinitely many integers. Evaluation at n=1/2 is consequently a whole-algebra character. This is an audit deduction from the published polynomiality mechanism, not an author assertion in the supplied paper.

For g = sum_(i<j) lk_ij^2, one has g(L_n)=n^2. Actual links have nonnegative integral g, so h=g(4g-1) has precisely the same actual-link zeros as g. The zero set is nonempty (the unlink). The character sends h to 0 and g to 1/4, so no positive power of g belongs to hV. The conclusion works on the full algebra, without pretending that a character on C[g] automatically extends.

Scope caveats checked: the paper parameterizes replacement of an existing crossing by odd half-twist numbers; PR177 uses even total braid exponents. Start with the Hopf diagram sigma^2, keep one crossing, replace the other by x=2n-1 parallel half twists: the total exponent is x+1=2n. Thus no odd/even component mixing is required. The paper also has a default non-split-link convention (p. 688), while its graph/tangle conventions explicitly allow disconnected objects (p. 689). For m>2, appending split unknots is safest justified directly by the same finite-difference skein argument, rather than silently ignoring that default convention. This direct argument verifies the fullV construction for all fixed m>=2 and for the all-component finite-order algebra.

Provisional priority disposition: the source does not establish an already-published equivalent arbitrary-ideal assertion; the precise refutation is a short corollary of longstanding published tools plus integrality of linking numbers. It therefore cannot support a claim that the twist-polynomial mechanism is new, or that the algebraic obstruction requires a new finite type theorem. Whether the extra formulation/corollary is publishably novel is not settled by this source audit. No global historical novelty clearance is issued.
