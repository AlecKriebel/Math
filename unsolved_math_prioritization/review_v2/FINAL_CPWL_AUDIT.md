# Independent CPWL promotion challenge: 30006217

Audit date: 2026-09-22T05:18:27.286694+00:00. Bounded triage only: no solution, novelty claim, or large computation was undertaken. The cached exact record, original statement, September 2026 primary article, and general real-algebraic algorithm references were checked.

## Recommendation

Retain as a **conditional proof candidate**. Impact **4** and conditional five-turn `p_solve=.15` are defensible optimistic planning estimates because the proposed mechanism is concrete and needs no substantial numerical execution. I recommend `p_valid_open=.60` for now rather than `.75`, pending an explicit input/output model and confirmation that a general algorithmic existence observation is a novel answer to the intended question. The `.75` estimate is an optimistic ceiling, not something this short audit establishes. Do not mark the record ready or solved on this basis.

Suggested short note: “Free max-affine coefficients suggest global real quantifier elimination; settle exact input/output encoding, Pareto versus total-piece objective, and novelty before claiming resolution.”

## Primary-source scope

The journal article, published September 1, 2026, asks for decomposition into convex CPWL functions with few pieces. Its introduction and end of §6.2 explicitly identify a global finite algorithm as missing. Definition 4.11 uses coordinatewise nondomination of the two piece counts within a fixed compatible complex. Theorem 4.12 gives vertex enumeration only within that restriction; Proposition 6.7 shows the restriction can miss global optima. Section 2.2 counts minimal full-dimensional affine regions; for convex functions this agrees with irredundant affine components. The paper permits real coefficients and does not specify a Turing input encoding. Its finite-procedure challenge states no efficiency requirement. [Brandenburg, Grillo, Hertrich, Problem 1.1, §2.2, Definition 4.11, Proposition 6.7 and conclusion of §6.2](https://link.springer.com/article/10.1007/s00454-026-00875-1).

## Mechanism stress test

The following are independent audit deductions and proof obligations, not claims that the open problem has been resolved.

- **Global versus fixed complex:** use the input cells only to encode the value of f. The affine coefficients describing g and h must remain free; forcing either function to be affine on each input cell would reintroduce the already-known restricted problem. New, cancelling breakpoints of g and h inside a linearity region of f must remain admissible.
- **Finite semialgebraic description:** fixed finite max-affine term counts plausibly give a first-order real formula for existence and global equality. Products of unknown coefficients with universally quantified spatial coordinates are bilinear polynomials, so linear programming is insufficient but real quantifier elimination remains relevant. Equality must cover all of R^d, including unbounded regions and interfaces; checking vertices or finitely many samples is not enough.
- **Piece counts:** raw max-term counts are upper bounds, because duplicate or inactive terms can occur. The eventual argument must connect feasibility with at-most counts to actual irredundant piece counts, including constants and affine functions. It must not equate a redundant presentation with exact complexity without justification.
- **What the existing bound buys:** a known decomposition with counts (A,B) supplies a finite search rectangle sufficient to seek one globally Pareto-minimal pair. A potential dominator of a pair in that rectangle is also inside it. This does not enumerate the entire Pareto frontier and does not justify restricting a minimum-total-pieces search to that rectangle. A total objective instead has the separate available bound A+B. The eventual target must state which objective is being answered.
- **No coefficient compactness assumption:** a finite count bound does not bound slopes or intercepts. The method must quantify over unbounded coefficient space rather than assume a bounded parameter box. Standard semialgebraic feasibility does not intrinsically require a compact box.
- **Decision versus construction:** merely deciding existence for each count pair does not output a decomposition. Exact witness extraction must be part of the cited algorithmic machinery, with a supported representation of the resulting coefficients.

Effective real quantifier elimination and semialgebraic sample-point algorithms are established tools; their existence alone does not certify this application or its novelty. [Basu, Algorithms in Real Algebraic Geometry: A Survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).

## Encoding and resource conditions

The cleanest candidate statement takes a finite rational or real-algebraic cell-and-affine description, or another explicitly reducible finite exact description, and permits real-algebraic output coefficients. Rational input does not by itself justify promising rational optimal witnesses. Restricting both input and output to rationals is a different feasibility question from real quantifier elimination.

For arbitrary real coefficients, specify a symbolic parameter treatment or an exact ordered-field/oracle model and its allowed operations. An unqualified appeal to a Turing algorithm reading arbitrary real numbers is not meaningful. A routine based on rational approximations cannot simply substitute for exact sign and equality decisions. A rational/algebraic theorem must be labeled with that scope rather than silently advertised as settling every possible arbitrary-real input interpretation.

The user’s resource constraint permits a short proof that an exact finite procedure exists; it does not require executing the procedure on a large instance. If practical computation or an efficient complexity guarantee becomes the intended success criterion, this route needs reevaluation and should not inherit the `.15` estimate.

## Novelty and readiness boundary

Two focused searches combining minimal CPWL decomposition and quantifier elimination found no direct prior resolution. This is weak negative search evidence, not an exhaustive literature result. The very general nature of the proposed machinery makes an overlooked standard corollary or mismatch of computational conventions a material possibility. No external communication was initiated.

Before consuming the five proof turns, record a finite input representation, allowed output field, one-minimal-pair versus total-piece objective, the intended global comparison class, exact witness-extraction reference, and the novelty check. If those align, this is a credible focused attempt. None of these triage observations establishes a completed proof or guarantees a new mathematical contribution.
