# Independent audit of the conflicting16-face certificate

Status: exact arithmetic reconstructed; source interpretation pending separate adversarial review.

No external code was executed. `check_certificate.py` was independently authored using only Python's standard library. The imported mathematical data are the12oriented face cycles and the16face-occurrence path printed in the external certificate, pinned to release commit7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9.

## Checks that pass

The specified combinatorial dodecahedron has20vertices,30edges,12pentagonal faces, and degree3 at each vertex. Every shared physical edge is oppositely directed in the two outward-oriented face cycles. The developed path has15strictly ordered open-edge crossings. Each between-crossing midpoint is strictly inside its indicated convex pentagon, so the full segment is contained in the chain. Exact collinearity tests against every developed vertex find only the initial and final vertices on the segment. Its endpoints0and2have graph distance2, and its squared edge-normalized length is exactly(307+137sqrt5)/2.

## The disputed step

The initial physical face cycle is[10,8,0,16,2]. Normalize0at0and16at1, with that face above the horizontal axis. Write r=exp(2pi i/5). The independently developed endpoint is

Z = (8+4sqrt5)+(1+sqrt5)r/2.

Thus0<alpha=arg(Z)<pi/5, proved by exact determinant signs; numerically alpha=5.0412820364708degrees.

Successively reflecting the **labeled billiard polygon** across each crossing gives terminal labels

physical0→label3,16→2,2→1,10→0,8→4.

There are15reflections, so the terminal labeling is clockwise. The outgoing terminal billiard ray at endpoint2is therefore2→16, not the outward physical-face ray2→10. Its developed vector is r^3, at216degrees. The reversed terminal tangent has direction180degrees+alpha. Therefore Figure8's terminal interior angle is36degrees−alpha, and

beta = 180degrees−(36degrees−alpha) =144degrees+alpha.

Consequently beta−alpha=144degrees exactly. Since alpha<36degrees and N=16 is even, this is typeA1 under Definition2.1.

The external ray2→10instead has direction108degrees. Its interior angle with the reversed tangent is72degrees+alpha≈77.041282degrees. This explains the external72-degree difference arithmetically, but it uses both the other boundary ray and an interior angle in place of the source's beta supplement. The external ray identity itself, −S0=r*S1, is correct; the claimed identification of that angle with the source-defined beta is the issue.

## Reproducibility

From this directory:

    python check_certificate.py
    python check_half_turn.py

All certification decisions use rational arithmetic inQ(sqrt5); floating point is used only to display angles and lengths. The source-type conclusion depends on the recorded exact ray identities and branch determinant signs, not on numerical subtraction of angles.

The output files preserve the exact crossing parameters and other checks. The discrepancy does not depend on whether the physical geodesic has self-intersections, and it does not impose any unprinted length bound or closedness requirement.

## Limits

This audit applies to the public literal witness and its given angle claim. It is not a judgment of the authors, and it is not permission to contact them. It has not yet received the required separate adversarial source/geometry review. Do not publish a refutation claim on this basis alone.
