# Versioned correction to the independent k609 checker

2026-10-01. The original independent review, checker and receipt remain preserved. This addendum supersedes only the independent checker’s named-side implementation and its receipt. The frozen author proof, source packet, and author checker are unchanged.

## Exact defect

For points p=(px,py), q=(qx,qy), the original helper returned

    (l,m,h)=(py-qy, qx-px, det(p,q))

and interpreted this as `l x+m y=h`. But evaluating its left side at p or q gives `-det(p,q)`, so it represented the centrally opposite side rather than the named side. The correct convention used now is

    (l,m,h)=(qy-py, px-qx, det(p,q)),

again interpreted as `l x+m y=h`. The previous checks named `implicit_projection_incidence` and `all_eight_contact_incidence` verified membership in the internally generated opposite line, not the stated original side/chord. Their old descriptions as named-side checks were wrong.

Central symmetry masked this defect in the area identities: negating the whole contact polygon preserves its signed area, and pedal areas from opposite points are equal. That explains why a passing area receipt alone did not catch the helper error.

## Corrective tests and outcome

The corrected helper is accompanied by unmasked incidence tests expressed directly in the original ordered endpoints:

    det(foot-p,q-p)=0
    det(contact-p,q-p)=0.

These do not merely reuse the helper’s line coefficients. There are 6,804 direct named-side pedal collinearity checks and eight formal original-chord contact identities, in addition to all earlier controls. The corrected run passes **25,465 exact assertions**. It still reconstructs the same seventh-degree star area expression and physical squared-distance denominator identity from the actual named sides. The author’s independent 7,006-assertion receipt remains byte-identical.

The universal analytic proof, convex positivity lemma, exact primitive eight-star zero certificate, and final domain-qualified PASS verdict are unchanged. No numerical approximation or symmetry-invariant area comparison substitutes for the new direct incidence tests. This is an explicit review-supplement correction, not a silent replacement of published history.

Original checker SHA-256: e5d1768bcfc6183c96398e53c2363d924c1303826ebd9231fd9731fa512ac499
Original receipt SHA-256: 12bbb4547e27d33b3c18b1df8a8f2980876e4708039631ef67842358d8e93e76
Original review SHA-256: 0aed6115e8e2c47a48e39042d3cce6059c1a70b711f3415d83d83adc45b5c3b9
