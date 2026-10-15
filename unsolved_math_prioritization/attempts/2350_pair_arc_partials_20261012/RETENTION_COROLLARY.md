# A strict improvement on four-fifths for canonical Bose–Chowla subsets

12 October 2026. Authored theorem, subsequently independently accepted unchanged in AUDIT_PAIR_MIXING.md. No novelty claim; the original research made no publication or repository mutation.

## Theorem

Let p tend to infinity through odd finite-field orders. Take any full p-point affine Bose–Chowla residue set modulo p²−1, and either its positive canonical integer lift or its positive canonical single-coset half-integer lift. If B′ is a retained subset with

    B′ ∩ (B′+B′+B′)=∅,

then, uniformly over translations, unit dilations, and those two separate lift conventions,

    |B′| ≤ (4859/6075+o(1))p
         = (4/5−1/6075+o(1))p.

The rational leading constant is approximately 0.799835390946502. The proof also permits the slightly smaller constant

    4/5−(18−8√5)/675,

but the main claim uses the simple exact rational certificate. No effective field-order threshold is asserted. This is a construction-specific obstruction, not a theorem for arbitrary Sidon sets or arbitrary lifts, and does not resolve Erdős 864.

## Dependency chain

1. [the complete accepted one-vertex proof](../2350_stronger_partials_20261012/BOSE_FOUR_FIFTHS_PROOF.md) is the frozen, independently accepted four-fifths proof. Only its uniform weighted one-vertex incidence upper bounds, total weighted edge asymptotic, lift conventions, and established character-sum inputs are needed here.
2. `SPECTRAL_PAIR_PROOF.md` is the new, separately identifiable arithmetic theorem. It proves the O(p^(3/4)) operator norm, the arbitrary-subset source-pair law, and the passage to the nonlinear almost-everywhere constraint for every limiting deletion density. This theorem was subsequently independently accepted unchanged in AUDIT_PAIR_MIXING.md.
3. `CONTINUUM_GAP_PROOF.md` is the separately authored exact measurable continuum certificate. It proves that every measurable d∈[0,1] satisfying that nonlinear constraint has integral at least 1216/6075. Its author's separate check is not treated as final independent acceptance of the combined theorem.

The continuum certificate explicitly smooths the one-dimensional optimal coupling before integrating an almost-everywhere inequality. It then uses fixed-function L1 translation continuity, a scaled linear cover bound, and a rational six-inequality certificate. In particular, it does not assume uniqueness of a fractional optimizer or evaluate an arbitrary measurable density on a null curve without justification.

## Passage to the stated uniform asymptotic

Suppose the rational theorem failed uniformly. There would be a fixed η>0 and a sequence of allowed fields, affine choices, lifts, and retained sets with p→∞ and

    |B′|/p ≥4859/6075+η.

The deletion empirical measures ν_D are dominated by the corresponding full seed measures, which converge uniformly to Lebesgue measure. After extracting a weakly convergent subsequence, their limit is d(x)dx with 0≤d≤1 and

    ∫d ≤1216/6075−η.

Section 6 of the spectral-pair theorem proves for this same d, almost everywhere on x,y,z>0, x+y+z<1,

    d(x)+d(y)+d(z)+d(x+y+z)
      ≥1+(2/3)[d(x)d(y)+d(x)d(z)+d(y)d(z)].

The pinned continuum certificate gives ∫d≥1216/6075, a contradiction. This proves the claimed uniform o(1). Replacing its rational final bound by the optimized threshold proves the optional stronger constant in exactly the same way.

The order of limits is unchanged throughout: first p→∞ for each fixed smooth test weight; only after a fixed limiting density has been obtained are the continuum smoothings refined. No field-dependent shrinking cutoff, arbitrary-subset equidistribution hypothesis, or inference from first-moment row sums enters the proof.

## Audit boundary

This is an independently accepted mathematical proof with an explicit dependency chain. Finite diagnostics accompany it, including nonprime odd field orders. They do not prove the asymptotic character estimates, replace the measurable-analysis argument, or constitute an independent acceptance report. Acceptance of the older four-fifths theorem does not automatically accept this new operator-norm theorem or retention improvement.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
