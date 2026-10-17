# Independent audit of the idempotent danger envelope

Auditor: invariant lane, shared final PASS5.

Reviewed frozen producer:
`../pass5_survival/IDEMPOTENT_DANGER_ENVELOPE.md`, SHA256
`1d9f4f881832dcd9501dc4ab98ffc6654762d976d882da0cfd6595e0a123cdb2`.

**Verdict: accepted without correction.** The invariant lane supplied
the initial isolated-hole argument; this review independently checks
the complete authored theorem, interleaved injections, both sharpness
claims, and the stated limitation on game use. No independent-origin
claim is made for the central idea.

## Closure and mass

For an absent point outside J(B), an absent adjacent partner also lies
outside J(B), because the two points prevent one another from being
initially isolated holes. Thus the pair survives filling every isolated
hole simultaneously. This proves idempotence, not merely a one-step
cardinality estimate. Monotonicity follows by checking whether an
initial isolated hole has itself been inserted into the larger seed
set. The inclusion T(B) subset J(B) follows from the eight required
distinct neighbors when the center is absent.

Every tile of a fixed disjoint 2-by-2 tiling contains at most one
isolated hole and, when it does, contains three original B-sites.
This proves 3|I(B)|<=|B| with no boundary loss. The finite assumption
is sufficient for all counts. Monotonicity of T and invariance of J(B)
give every iterate, including the zeroth iterate, inside the same
envelope.

## Injections and sharpness

For any finite injection history, the envelope of the union of all
seeds contains every intermediate state: seed injection preserves
membership and T maps the envelope into itself. This also bounds the
ever-occupied union. It does not allow removing old seeds or silently
changing spatial coordinates between applications.

In the side-(2m+1) square with the m-squared odd/odd sites removed,
each removed point is an isolated hole. There are no outside isolated
holes, so the exact counts are 3m^2+4m+1 and 4m^2+4m+1. Their ratio
tends to 4/3. The union of the initial set and its first T image is
exactly the envelope, proving sharpness for ever-occupied mass as
well. The producer correctly does not claim sharpness for the mass of
one particular iterate.

## One insertion

If the inserted point was already in J(B), extensivity, monotonicity,
and idempotence force no change in the envelope. Otherwise each other
new envelope site is an initially absent neighbor of the inserted
point, with no other initially absent neighbor. These newly filled
holes are pairwise king-nonadjacent. A side-three square partitions
into four side-at-most-two rectangles, so at most four such holes
exist. Including the inserted seed gives the bound five.

The side-five square with the center and four diagonal neighbors
removed attains five: before insertion every missing point has an
absent adjacent partner; after insertion all four diagonal holes are
isolated. The count twenty to twenty-five is exact.

## Scope

The result is a bounded nonlinear spatial envelope, not an exact
mixed-time online viability invariant. In particular, a union over
different adversarial responses to different candidate moves is not
one legal seed injection. The separate frozen artifact
`ADAPTIVE_A8_RECURSION_OBSTRUCTION.md`, SHA256
`526e62b1eaf4d102c207c93c84555d2bb9753f48e3227fb5020048ef506a6064`,
also gives an explicit later-time update that creates four new
intermediate danger centers and defeats a naive backward threshold
sweep. This is consistent with all envelope statements.

No arbitrary-H or unrestricted survival conclusion follows from this
audit. All prior frozen artifacts remain unchanged.
