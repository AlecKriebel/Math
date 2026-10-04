# Movable cycle cones on toric varieties

Problem 30003592, OWR-15586-003. Research checkpoint dated 4 October 2026.

**Status: unsolved.** No proof of rational polyhedrality for all smooth toric varieties, and no counterexample to that assertion, was obtained. The five approaches recorded here do not settle the smooth projective case in intermediate dimensions.

The main artifact is [PARTIAL.md](PARTIAL.md). It gives:

- a rational polyhedral outer cone from effective boundary-divisor intersections;
- an explicit calculation on the toric fourfold P(O^2 + O(1)^2) over P^1, including a movable surface class with negative intersection against an effective surface;
- a proof that taking a product with projective space splits the movable cone into movable cones of the original variety;
- an exact Hodge-index obstruction explaining why the set of irreducibly representable classes must not be substituted for its convex cone.

The fourfold calculation is a worked verification of a case already covered by Fulger and Lehmann, not a new resolution. No priority claim is made for the other elementary deductions.

[Source and scope checks](SOURCE_GATE.md), [the five approach records](RESEARCH_LOG.md), and [validation limits](VALIDATION_LIMITS.md) accompany the note. Run `python3 verify.py` and `python3 verify_manifest.py` from this directory. The former checks the finite algebraic controls, not the universal problem or all geometric arguments. An independent mathematical audit is pending.

This is a provisional AI-assisted research notebook. It has not been peer reviewed.
