# Line-union discrepancy: orientation-sensitive results

Problem ID **30002421**; source label **OWR-12723-007**; queue position **1825**. Prepared 20 October 2026.

## Outcome after five attempts

**UNSOLVED, 5/5, for the unqualified original question and for unrestricted rotations.** The original report says cubes contained in the unit cube but does not expressly fix their orientations. Current publication status of that exact unrestricted problem has not been independently established.

**The axis-parallel reading is DISPROVED, not merely a failed attempt.** An explicit sequence of admissible full-chord unions has normalized discrepancy O(1/L), uniformly even over all axis-parallel rectangular boxes. This is a rigorous reduction to Borda's bounded-error theorem, not a floating-point conjecture.

The distinction is substantive: every mutually parallel family satisfies the proposed logarithmic lower bound once arbitrary cube rotations are allowed, including the same oblique family that disproves the axis-parallel reading.

## Established results

Let C=[0,1]^3, let A be a finite union of full affine-line chords of C, and let L=H^1(A)>0. Arclength is taken on the set union, not with multiplicity. Write D_axis and D_rot for normalized discrepancy over closed contained axis-parallel and arbitrary-orientation cubes, respectively.

- Universal axis-parallel baseline: D_axis(A) >= 1/(8 max(1,L)^(3/2)). See [Attempt 1](ATTEMPT_1.md).
- Axis-parallel disproof: with alpha=(sqrt(2),sqrt(3),1), integer-duration torus-flow chords have L_n=sqrt(6)n and D_axis(A_n)<=sqrt(6)K_alpha/L_n. Hence L_n D_axis(A_n)/log L_n tends to zero. See [Attempt 2](ATTEMPT_2.md).
- Universal rotating-cube baseline: D_rot(A)>=1/(16 max(1,L)). See [Attempt 3](ATTEMPT_3.md).
- Every mutually parallel full-chord family: D_rot(A)>=c log L/L for L>1, with a universal c>0 independent of direction and individual chord lengths. See [Attempt 4](ATTEMPT_4.md) and the [weighted-square transfer](WEIGHTED_SQUARE_ROUTE.md).
- Every fixed finite mixture of the specified pairwise nonparallel positive algebraic-flow families also has a logarithmic rotating-cube lower bound for all sufficiently large L. The threshold may depend on the fixed family. The number of directions cannot grow under this conclusion. See [Attempt 5](ATTEMPT_5.md).

The imported ordinary planar square lower bound is an established result, and the imported flow estimates are Borda's theorems. These notes give authored reductions and geometric arguments; no historical novelty claim is made.

## What remains unresolved

No proof or counterexample is provided for arbitrary finite unions with unrestricted cube orientations. The parallel proof does not control cancellation from arbitrary other directions. The fixed-mixture proof controls cancellation only because all other fixed families have bounded unnormalized error for a specially chosen fixed orientation.

It is invalid to turn a constant for each fixed nonresonant orientation into one constant uniform over all rotations. It is also invalid to replace full chords by arbitrary interior segments, total arclength by line count, equal-sided cubes by rectangular boxes, or a sampled numerical maximum by a supremum upper bound.

## Contents and use

- [Scope](SCOPE.md): exact model, quantifiers, interpretation, and remaining gaps.
- [Sources](SOURCES.md): public citations, theorem dependencies, and source verification metadata.
- ATTEMPT_1.md through ATTEMPT_5.md: the five sequential mathematical investigations. Earlier statements of what an individual attempt had not established are historical to that attempt; the final outcomes are those summarized above.
- WEIGHTED_SQUARE_ROUTE.md: twelve-square transfer, fit, signed-measure boundary treatment, and arbitrary-reference coefficient.
- AUDIT.md: independent acceptance audit, including the final extension in §§6–7, and limits of the claims.
- [Reproducibility](REPRODUCIBILITY.md): dependency versions, isolated replay, and numerical limitations.
- test_direction_mixtures.py and DIRECTION_MIXTURE_EXPERIMENT.json: optional floating-point diagnostics only. They are not proof certificates and supply no certified numerical counterexample.
- verify_replay.py and REPLAY_VERIFICATION.json: isolated replay and mathematical-output comparison, excluding timing.
- MANIFEST.json: byte counts and SHA-256 hashes of all other public payload files.

The package contains authored mathematical notes, authored code, authored diagnostic output, and public bibliographic/verification metadata. It does not include source PDFs, source extracts, source images, raw catalog records or dataset contents, or private coordination material.
