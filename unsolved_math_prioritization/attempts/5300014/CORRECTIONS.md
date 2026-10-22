# Corrections and governing clarifications

These corrections govern use of the preserved author snapshot. None changes the UNSOLVED disposition.

## C1 Completion estimates have no mathematical standing

The percentage-valued fields in author/ATTEMPTS.json are subjective heuristics without a calibrated denominator or mathematical validation. They must not be interpreted as a fraction of a proof, a measured degree of completion, a success probability, or a literature-status measure. They must not appear in summaries of this audit. The original file remains unchanged for freeze integrity; ATTEMPTS_AUDITED.json removes those fields and is the operative status record. The supported quantitative accounting is five approach families used out of the five-family budget.

## C2 Correct the free-zero count in Proposition 4

The sentence invoking Proposition 2 should distinguish the leading factor z from the free zeros. For B(z)=z^(n-2)(z+r)(z+s)/((1+r z)(1+s z)), the full zero divisor has n-2 copies of 0, -r, and -s. In Proposition 2's convention, the n-1 free zeros are n-3 copies of 0, -r, and -s. Therefore

    L_B(-1) = 1+(n-3)+(1+r)/(1-r)+(1+s)/(1-s).

The author's displayed derivative and rate formula are already correct. This fixes an indexing ambiguity, not the resulting identity.

## C3 Make the quadratic gauge explicit

For f(z)=z(az+b)/(cz+d), first divide numerator and denominator by d. Conjugate by S(z)=(d/a)z. The result is

    S^(-1) f S(z) = z(z+b/d)/(1+(c/a)z).

Thus beta=b/d and alpha=c/a. The phrase about making a=d=1 tacitly combines projective rescaling of the coefficient pair with coordinate scaling. This explicit calculation fills in that routine normalization step.

The marked third fixed point is q=(1-beta)/(1-alpha). At beta=1 it coincides with the marked point 0. Proposition 1 uses the displayed nondegenerate coefficient chart, or marked fixed-point tuples allowing repetitions. It does not use a three-distinct-fixed-points chart that keeps this third point at 1 throughout the boundary. The multiplier beta provides a continuous inverse in this labelled chart. This is the precise topology in which the stated quadratic extension is checked.

## C4 Keep external theorems and compactness assumptions scoped

The Cao-Wang-Yin theorem imported in the note is Theorem 1.1 of arXiv:2509.07350v1. The publisher confirms that the paper appeared in 2026, but this audit did not retrieve or compare the journal PDF. Do not upgrade the check to full verification of its proof or version equality. The publisher's available notes also qualify a separate self-bumping claim; no such claim is used here.

Proposition 5 is an equivalence under its explicitly stated compact metrizable Hausdorff hypotheses. Applying its converse to a particular marked rational slice requires those hypotheses in that slice's chosen normalization. The explicit two-sequence obstructions remain sufficient in Hausdorff closures without the converse. No universal compactness proof or quotient-descent theorem has been supplied by these auxiliary arguments.
