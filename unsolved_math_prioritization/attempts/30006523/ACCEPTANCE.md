# Acceptance of Schubert-support skew-sum results

## Decision

**Accept the restricted mathematical results without a substantive proof correction.** The exact ordinary polynomial factorization, Cartesian-product support theorem, left-weak convexity equivalence, skew-indecomposable minimal-counterexample reduction, and unbounded Boolean family are accepted. The complete definitions and proofs are retained in PROOF.md and the logical independent audit in AUDIT.md.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

## Exact mathematical scope

For a in S_p and b in S_q, a skew b=(q+a(1),...,q+a(p),b(1),...,b(q)). For H=S or G,

    H_(a skew b)(X,Y)=(x_1 ... x_p)^q H_a(X) H_b(Y).

The symmetric rectangular factor commutes with each within-block divided-difference step. Skew sums form a left-weak upper ideal in S_(p+q), isomorphic to the product order, with product intervals. Consequently, if G_a=sum A_u S_u and G_b=sum B_v S_v,

    G_(a skew b)=sum_(u,v) A_u B_v S_(u skew v).

Distinct pairs cannot cancel, so the support is the exact Cartesian product. It is left-weak convex if and only if both nonempty factor supports are. A smallest counterexample would therefore be skew indecomposable. Iterated skew sums of 132 have Boolean-interval supports with 2^r elements and coefficients (-1) to the number of 231 factors.

These are ordinary stable Schubert expansions over the integral polynomial ring, not quotient or back-stable identities. Operator indices refer to right-position descents; left-weak order uses adjacent-value swaps. The finite Schubert basis and stability argument ensure that no larger-index terms or interval elements are silently omitted.

The authored polynomial F=S1243-S1342+2 S2341 preserves G1243's convex support, degree-sign pattern, unique lowest Schubert term, monomial degree signs, and right-descent restriction. Its image pi_3 F=S1234+S2314 omits the intermediate 1324. The complete direct polynomial calculation is retained. F is not a Grothendieck polynomial, so this refutes only a coefficient-blind induction shortcut. For actual supported u in G_w, Des_R(u) is contained in Des_R(w), with the proof retained.

The G2143 example is established prior work from Weigandt, Example 1.4. The G13254 right-weak failure is solely a convention check. Neither is represented as a counterexample to the target left-weak conjecture.

## Independent finite evidence and limits

The historical independent audit reconstructed all 873 S1-S6 expansions and matched 1,746 complete recursive/pipe polynomials, with all 873 convexity checks passing. Its dual extraction and stability coverage is only S1-S5: 15,017 dual comparisons and 306 polynomial embeddings. It does not claim all candidate secondary counts were reproduced. Normal, -O, and -OO passed; substantive mathematical JSON agrees only after removing the optimization field, not as literal full JSON or byte identity.

The complete written universal proofs and displayed analytical identities are retained. This is not a computational reproduction package: raw expansion datasets, detailed computational certificate tables, executable code, copied source documents and images, and private coordination material are omitted. Historical finite checks support the work but are not premises of the universal theorem. The exhaustive finite checks cannot be reproduced from this edition alone. The retained G13254 expansion is an independently checked analytical identity; its full recursive calculation and computational certificate are omitted, and its reconstruction requires the stated recurrences. It is not a premise of the universal theorem. No new mathematical execution or source inspection occurred in editorial preparation.

The accepted originals remain immutable. Editorial changes state review status, distinguish historical finite coverage, expand the already accepted direct polynomial calculation, and remove private operational material. Acceptance is unchanged. Public file bindings appear in ACCEPTANCE.json; source identities and inspection limits in SOURCES.json.

## Remaining question

The general Schubert-support left-weak convexity conjecture remains unresolved by this work. No novelty, priority, exhaustive literature survey, or current-openness claim is made.
