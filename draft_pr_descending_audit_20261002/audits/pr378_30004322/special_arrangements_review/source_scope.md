# Source-first normalization

Audit family: exact special-arrangement incidence and auxiliary-line covers.

The first mathematical source inspected was the literal EMS PDF at https://ems.press/content/serial-article-files/46833, downloaded as `szemberg_literal.pdf`. Printed pages 3295--3297 are physical pages 25--27. All three were extracted, rendered, and visually read before any candidate snapshot, candidate proof, candidate code, replay history, sibling verdict, or root verdict was read.

Printed 3297 states Conjecture 1 (Pokora): for the set Z of all singular points of an arrangement of lines, epsilon(P^2,O(1);Z)=1/mpl(Z), where mpl(Z) is the maximal number of collinear points in Z. In particular, the maximum is over **every projective line**, including auxiliary lines that are not arrangement components.

Working normalization: a finite reduced arrangement of distinct complex projective lines, with nonempty finite singular set Z. For an irreducible reduced plane curve C meeting Z,

    epsilon(Z) = inf_C deg(C) / sum_{p in Z} mult_p(C),
    mpl(Z) = max_{projective lines L} #(L intersect Z).

The maximum is an integer and attained: if #Z>=2, every maximizer with >=2 points is among the lines joining pairs of distinct Z-points; if #Z=1, every line through its point has value 1. Upper bound epsilon<=1/mpl follows by using a maximizing line. The substantive claim is sum mult_p(C)<=mpl(Z) deg(C) for all irreducible reduced C.

Boundary checks: a pencil of >=2 distinct lines has Z={P}, mpl=1, and epsilon=1 because mult_P(C)<=deg C with a line attaining equality. An arrangement of zero or one line has Z empty, outside this normalized claim: 1/mpl has zero denominator and the curve-infimum definition has no admissible curves. Repeated lines require reduction before taking singular points; scheme singularities of a nonreduced divisor are a different problem.

The printed source alone does not explicitly spell out all these domain restrictions; this is the precise conventional mathematical formulation used in the audit, not an attributed quotation.
