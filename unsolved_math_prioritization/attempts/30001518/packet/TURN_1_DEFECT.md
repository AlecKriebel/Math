# Turn 1: exact attainment through the resistance defect

This is a substantive mathematical attempt, not a literature-status turn. The aim was to turn the known extremal value of resistance into an attainment or nonattainment theorem. The outcome is a rigorous criterion and a scoped obstruction, not a solution.

Let the incident phase measure be normalized to a probability measure μ, and let v and w be the unit incoming and outgoing velocities, defined μ-almost everywhere. Put r = (1/2) ∫(1−v·w) dμ. Direct expansion gives

    1−r = (1/4) ∫ |v+w|² dμ.

The integrand is nonnegative. Consequently r=1 if and only if w=−v μ-almost everywhere. If Δ is the angle between w and −v, then

    μ{Δ≥δ} ≤ (1−r)/sin²(δ/2),  0<δ≤π.

Both assertions follow from |v+w|²=4 sin²(Δ/2); no billiard existence theorem is used. These are elementary consequences of the normalized resistance formalism in Plakhov, Mathematical retroreflectors, §2.3. They are not presented as historically new results.

In dimension two, let C=conv(B), let P be its perimeter, and suppose that the regular common boundary E=∂B∩∂C has length L₀. The incoming flux measure on this set is ds cosφ dφ/(2P), −π/2<φ<π/2. Specular reflection at E immediately escapes the convex hull and has |v+w|²/4=sin²φ. Therefore

    1−r(B) ≥ (L₀/(2P)) ∫[-π/2,π/2] sin²φ cosφ dφ
            = L₀/(3P).

The normalized incident measure is the one obtained from rays interacting with B. For a compact connected planar body, projections onto a line are intervals, so almost every ray entering its convex hull does interact with B; this is the setting in which the displayed 2P normalization applies. A body with positive-length regular exposed boundary cannot be perfect. In particular a convex planar body has r=2/3, in agreement with the cited source.

Why the attempt does not close the problem: L₀ may vanish; perfect retroreflection would also require every positive-weight hollow to be perfect. Neither the inequality nor knowing sup r=1 forces the supremum to be attained. Concentration near the antipodal velocity relation does not imply that any member of the concentrating family has exact reversal almost everywhere.

Proof of the elementary limitation: on any probability space with a fixed incoming unit vector, let w_n be −v rotated through 1/n. Then r_n→1, but μ{w_n=−v}=0 for every n. This is a measure-theoretic counterexample to an inference, not a claimed billiard construction.
