# Author turn 2: epimorphisms require an appropriate copy, not the given embedding

**Partial; original target unresolved.** 2026-10-01.

The attempted route is to turn Moore's PFA embedding of an arbitrary Aronszajn order into a monotone surjection. The following exact criterion identifies the missing cut condition. It also supplies a countercontrol inside eta_C showing why requiring a retraction onto the *given* copy is too strong.

## 1. Retraction criterion for a specified suborder

Let A be a linear order and B a nonempty suborder. For x in A\B put

    B_x^-={b in B:b<x},    B_x^+={b in B:x<b}.

There is a monotone retraction r:A→B (so r(b)=b for every b in B) if and only if for every x outside B at least one of the following is true:

    B_x^- has a greatest element, or B_x^+ has a least element.           (1)

Empty sets do not have these extrema. Thus (1) includes the outer-ray conditions: a point below all B requires a minimum of B, and a point above all B requires a maximum of B.

Necessity: r(x) is in B and is either below or above x. If below, monotonicity and the retraction property force b<=r(x) for every b in B_x^-, so r(x) is its greatest point. If above, the reverse argument makes r(x) the least point of B_x^+.

Sufficiency: fix B pointwise; for x outside B choose the greatest point of B_x^- when it exists, and otherwise the least point of B_x^+. This defines a single value on every complementary interval of A\B, because points in the same such interval determine the same cut in B. Each chosen value is above every left B point and below every right B point. If two inputs are separated by a B point, these inequalities give monotonicity; if not, they are in the same complementary interval and receive the same value. Thus the map is a monotone retraction.

This is a direct elementary cut formulation of the standard definition-by-pieces issue; Camerlo–Carroy–Marcone's Lemma2.8 similarly makes endpoint compatibility explicit. No priority is claimed.

## 2. An exact reformulation for abstract epimorphisms

For arbitrary nonempty orders A,B, there is a monotone epimorphism A→B if and only if B has *some* order-embedded copy B′ in A satisfying (1).

For the forward implication, choose one point e(b) from each nonempty fiber of an epimorphism f. Monotonicity of f forces e to be increasing. Then e composed with f is a retraction onto e[B], so (1) holds there. Conversely a retraction onto an embedded copy followed by its inverse order isomorphism is an epimorphism onto B. The choice of one representative per fiber is legitimate in ZFC and hence under PFA.

Applied to eta_C, the remaining step is not merely to embed each target B, but to find a copy with no realized nonprincipal cut as in (1). This reformulation is exact. It does not by itself solve the target and is marked blocked at the unsupported assertion that all PFA embeddings can be selected with this property.

## 3. A failed retraction is not a negative answer

Inside L=eta_C consider the zero-prefix cylinder

    B=[(0)]={0 concatenated with x:x in L}.

It is convex and isomorphic to L. It has neither endpoint. Every point of L with positive first coordinate is above every point of B, so its B-left set has no maximum and its B-right set is empty. Criterion (1) fails, and there is no retraction L→B fixing this copy pointwise.

Nevertheless prefixing a zero,

    f(x)=0 concatenated with x,

is an order isomorphism from L onto B, and in particular is an epimorphism. It is not the identity on B. Thus a failure of the retraction criterion for the initially supplied suborder is not a counterexample to strong surjectivity. One must exclude *all* alternative section copies, or construct a map not fixing the original copy.

This example also prevents an overstrong interpretation of the universal embedding theorem. Even a perfectly explicit convex copy of the entire domain can be unsuitable as the section of a retraction, while the two abstract order types are isomorphic.

## 4. What the elementary endpoint tests do settle

Every nonempty finite B⊆L satisfies (1), so there is a direct monotone retraction onto every finite target. At the other extreme, cofinality and coinitiality do not give a negative test for the target: L is short and has no endpoints, hence its cofinality and coinitiality are countable; every nonempty suborder without the respective endpoint has the same countable cofinality/coinitiality. This is consistent with the credited necessary condition of Camerlo–Carroy–Marcone Proposition2.4, but does not make it sufficient.

The real issue is the arrangement of cuts, not just their two outer cofinalities. A countable-stage construction can satisfy all finite endpoint conditions and still produce a limit cut with no point of the requested target. The next attempt investigates that failure of finite-level or product closure rather than assumes it away.

Substantive author turns: 2/5. Completion estimate20%. The exact cut/section criterion and finite-target result are retained; no universal good-copy theorem or genuine target counterexample is obtained.
