# Independent adversarial review of the scoped fast-diffusion audit

Reviewed 21 October 2026. This is an independently authored mathematical review, not a resolution or novelty certificate. No publication or queue edit was performed.

## Verdict on the five approaches

The formulas and qualifications in `MATHEMATICAL_AUDIT.md` pass this review. In particular:

1. **Known quadratic deficit.** With the audit's notation, `h=(1−q)(1−2q)` and `C=kh/2`. Freezing the decreasing scale gives the stated Riccati upper bound. The bound improves the prefactor but not the limiting exponent 4. The endpoint `q=1/2` makes this improvement zero.
2. **Scale lower bound.** The identity `s'=−qkf` and baseline decay give `s∞≥s0−qkf0/4`. Moment matching gives `kf0=4s0−k∫u0^m/(1−m)`, so `s∞≥(1−q)s0>0`; in fact the omitted entropy term gives a further positive contribution. The warning against inserting a lower bound for `s` into the negative quadratic dissipation term is correct. The proposed two-variable equality system is not covered by a cooperative comparison theorem: its off-diagonal derivatives have opposite signs.
3. **Tail-class separation.** The radial power-tail datum is valid. For d≥3 and m≥m1, one can simplify the choice to `d+2<p<2/(1−m)`, because `d/m<d+2`. The resulting datum has finite mass, second moment, and m-power integral, but infinite tail functional A. It even has finite Fisher information, since `p(2m−1)>d−2`. The truncation argument establishes divergence of the needed tail parameter, not deterioration of any specific uncomputed function ζ or failure of actual decay.
4. **Clock conversion.** For the physical equation used in the OWR source, the adaptive scale equation `Ra'=2σ^(−D/2)Ra^(1−D)` and `dτ/dt=σ^(D/2)e^(2Dt)` are correct. The dilation is `uad(x)=λ^d vfixed(λx)` with `λ=e^(2(t−r))`. Its optimized entropy scales as `λ^(−2q)`. The conditional bound with `L=[(1−q)s0]^(D/(2q))` and `η=4+ζ−4q` is therefore correct, including the final `min(1,L)^(−η/(2D))` prefactor. It remains conditional on an applicable fixed-frame theorem with its initial-data normalization and tail hypotheses; the calculation neither removes them nor identifies an optimal adaptive rate.
5. **Spectral splice.** The two-time bound follows from integrating an independently justified entropy-production inequality after an independently justified entry time. None of those missing inputs follows from the splice itself. The endpoint and limiting-entry-time warnings are necessary and correctly retained.

The layer-cake estimate `∫|x|²v≤β/(β−2) M^(1−2/β) A^(2/β)` and the ensuing upper bound on normalized relative entropy also check. This supplies a mathematically valid way to bound an entropy input by A at fixed mass. It does not identify two separately published explicit constants, and would require a uniform version of the constructive theorem to infer an A-only rate from an arbitrary pointwise formula depending on both A and G.

**Minor regularity qualification:** finite initial entropy and second moment do not imply finite initial Fisher information in general. The ODE identities should be read for positive times under their regularity/integration-by-parts hypotheses, or along the approximation used to justify the cited theorem. The entropy bounds extend to initial time by the corresponding continuity/approximation argument. The smooth tail counterexample does not suffer this problem.

## Exact-identity discrepancy in the inspected 2013-source preprint

Source: Dolbeault–Toscani, *Improved interpolation inequalities, relative entropy and fast diffusion equations*, inspected arXiv:1110.5175v2, https://arxiv.org/abs/1110.5175, equations (10), (21), and Remark 4 on manuscript p.16. The displayed Remark 4 was visually checked in its PDF, so the issue below is not a text-extraction error. This review does not certify what changes, if any, appear in a different version or an official erratum.

Use `a=d(m−mc)/2=1−q`, `b=d(1−m)=2q`, `η=σ^a`, and `z=η∇u^(m−1)−2x`. The Fisher information in the paper is

`j = m/[(1−m)η] ∫u|z|²`.

For frozen η, equation (10) implies

`(∂t j)_σ+4j = −R`,

where

`R = 2∫u^m (|∇z|²−(1−m)(div z)²) ≥ 0`.

The factor η in the differentiated integral cancels against the factor η in the Fisher-information denominator. There is no residual factor σ^(2a) when z is defined as above.

Equation (21), evaluated at the moment-matching scale, gives

`∂σ Iσ = (a/σ)(j−4bf)`.

The chain rule therefore yields the exact identity

`j'+4j = a(σ'/σ)(j−4bf)−R`

`         = ab(σ'/σ)(j−4f)+h(σ'/σ)j−R`,

with `h=a(1−b)` as in the main audit.

By contrast, the inspected Remark 4 prints `b` rather than `ab` as the first coefficient and `σ^(2a)R` rather than R when using its stated scaled z. Both discrepancies are substantive for an exact ODE closure. The alternative remainder normalization `2σ^(2a)∫u^m Q(∇u^(m−1)−2σ^(−a)x)` would be equivalent to R, but that is not the vector field stated there.

This does **not** invalidate the inequalities used in the main audit: `a,b>0`, `σ'≤0`, and `j−4f≥0` still give `j'+4j≤h(σ'/σ)j`, and hence the cited quadratic entropy-production improvement. The current audit does not rely on the misnormalized exact line.

## Independent smooth-profile diagnostic

A second derivation tests the exact line on the family

`u=(C+xᵀAx)^(−n)`, `n=1/(1−m)`, `A=diag(Ai)>0`,

with the same mass as `B1=(1+|x|²)^(−n)`. This requires `C=(det A)^(−1/(2n−d))`. Set

`σ=C tr(A^−1)/d`, `Li=2(σ^a Ai−1)`.

The adaptive PDE stays within this family and gives

`C'=(tr L)C/n`, `Ai'=[(tr L)/n−2Li]Ai`.

Let M be the conserved mass and `H=n−1−d/2`. The directly integrated quantities are

`∫u^m/M = C(n−1)/H`,

`f/M = n(n−1)(σ^q−C)/H`,

`j/M = [(n−1)C/((2n−d−2)σ^a)] Σ Li²/Ai`,

`R/M = 2[C(n−1)/H][ΣLi²−(ΣLi)²/n]`.

For d=3, m=3/4, and A=diag(1/2,1,2), C=1 and σ=7/6. Differentiating these formulas along the displayed finite-dimensional PDE gives, per unit mass:

- `j'+4j = −23.9851911881948345822565969624`.
- Corrected exact identity: the same value, with residual below 10^−58 at 60-decimal arithmetic.
- Printed Remark 4 identity: `−29.1421801380736185669663352236`, with residual about `5.1569889498787839847097382612`.

The accompanying `CHECK_ADAPTIVE_IDENTITY.py` independently reproduces these values by differentiating the explicit formulas, rather than differentiating the candidate identity. The numerical residual is a diagnostic supporting the analytic derivation, not a substitute for it.

## Final scope assessment

The candidate audit is a valid qualified partial result after the stated regularity qualification. It has not established an unrestricted sharp all-time envelope, a best coefficient, or a full-domain explicit spectral entry time. The tail-class obstruction and clock distinction are real. The extra source-identity finding should be kept separate from the main theorem-based reasoning and described only for the inspected source version unless the publisher's version is also checked.
