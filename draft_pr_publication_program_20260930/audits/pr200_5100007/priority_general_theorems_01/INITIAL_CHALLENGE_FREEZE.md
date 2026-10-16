# Initial implication challenge (frozen)

Time: 2026-10-16 04:36:21 UTC. Audit completion estimate: 0%.

This file was written before reading the submitted proof or another audit's conclusions. The assignment supplies the target and named sources; those are leads, not evidence for priority.

## Exact target supplied for audit

Fix a proper nested confocal ellipse pair with outer semiaxes `a>b>0`, inner semiaxes `sqrt(a^2-lambda),sqrt(b^2-lambda)`, `0<lambda<b^2`. Let a primitive Poncelet billiard orbit have least period `N` divisible by four, allowing any primitive coprime star winding. Let `Q_i` be intersections of successive tangents to the outer ellipse at the billiard vertices. The ordinary Euclidean product `prod_i |Q_i-F|` is independent of phase and has the same value for either focus `F` of the ORIGINAL outer ellipse.

The audit assumes no novelty. It attempts to establish an already-published corollary, or delimit an exact unresolved bridge.

## Independent challenge routes

1. Read the literal general statements in Akopyan--Schwartz--Tabachnikov, *Billiards in ellipses revisited*, and Bialy--Tabachnikov, *Dan Reznik's identities and more*. Test whether products of trigonometric factors, distances, tangent lengths, or polar quantities imply the target after a complete geometric dictionary.
2. Read the literal k115 table entry and relevant proof scope in the named Reznik--Garcia--Koiller source and Stachel's canonical parameterization. Separate an existing conjecture/empirical invariant from an existing proof; an exact tabulated conjecture alone does not establish an old theorem.
3. Search primary sources for focus inversion, pedal polygons, tangent/polar duality, and circle theorems. A theorem concerning the foci of the `Q` locus is not automatically a theorem about the original foci.
4. Examine whether an old elliptic norm/product theorem applies by a short substitution. Distinguish a generic norm fact from the nontrivial verification that the present function has the required divisor or torsion cancellation.

## Conditions for a successful old-corollary finding

A source must predate the claim and have an actual theorem with hypotheses covering the required real regime and primitive star periods, or a rigorously justified specialization. The audit must show every map: orbit points, tangencies, focus, Euclidean distances, product, and closure/parity. No label match, bibliographic assertion, title, broad abstract claim, or unverified analogy suffices.

## Adversarial boundary checks

- `N=4` versus all `4|N`, even-but-not-four-divisible periods, nonprimitive covers, and coprime star steps.
- Correct original foci, rather than foci of an auxiliary ellipse.
- Q is generally not a confocal billiard polygon for the original ellipse pair.
- Vanishing or signed factors versus ordinary positive Euclidean distance.
- Degenerate circle or caustic limits must not be silently used to extend a proper-ellipse theorem.

## Restrictions

No Git, refs, PR changes, publication, or external outreach. No reading old favorable triage, other priority families, or root priority verdicts. Only this audit directory will be written. Third-party fulltexts/readings stay private and are excluded from the safe output manifest. The report will not certify world completeness, firstness, or independence.
