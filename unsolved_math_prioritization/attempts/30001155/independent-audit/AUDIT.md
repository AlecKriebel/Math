# Independent adversarial audit: problem 30001155

Audit date: 2026-10-04 UTC. Target: rank 667, OWR-3389-006, area-refined Dirichlet spectral gap. This is an AI-assisted mathematical and reproducibility review, not journal refereeing or a formal proof-assistant certificate.

## Disposition

**PASS for the proposed status: unresolved after five substantive approaches (5/5), with the stated scoped partial results.** No blocking mathematical defect was found. No correction to the frozen proofs is required. This disposition does not certify the conjecture for arbitrary convex planar domains, all equality cases, or all extremizing sequences.

The mathematical deductions support:

1. Strict inequality for every nondegenerate rectangle, and saturation by elongated rectangles in relative or diameter-normalized terms.
2. Strict inequality for all triangles, conditional on the published Lu–Rowlett theorem as explicitly credited.
3. The inequality for ellipses with minor/major semiaxis ratio at least √15/4, with equality only for the circle within this range.
4. A convex family showing that local convergence to a strip does not alone force normalized saturation, by a valid application of Friedlander–Solomyak.

The finite-element computations remain exploratory. Every author qualification concerning the full conjecture, literature completeness, numerical certification and historical novelty must be retained.

## Exact binding and replay

The reviewed archive is `rank667-30001155-authored-packet.zip`, 25,174 bytes, SHA-256:

`02d7ebf85303b54d4643a79c266f0273d7881d80cddc0ddd215db2be2d35e6d9`

The reviewed `MANIFEST.json` has SHA-256:

`63fb043ce525074d79d5731b8f8cf583df52cf8cdb029bfa22531bc31644952e`

The reviewed `PROOF_AND_PARTIALS.md` has SHA-256:

`685142aa8e5bacf48c70ce348f3b73b593f626ff1d21a1af64495069d5593de1`

All 13 manifest-listed files matched their recorded sizes and hashes. All 14 ZIP entries matched the corresponding packet files; the archive contains no additional entries. The freeze receipt agreed with these bindings. The original packet, archive and receipt were preserved.

The author's exact verifier replayed **2,031 assertions**, and its output was byte-identical to `exact_results.json`. The manifest verifier reported 13 files and 56,299 bytes. The independent audit additionally reconstructed the Bessel signs using different truncation orders, reconstructed the Bernstein coefficients by exact rational interpolation and elimination rather than the author's conversion formula, checked the π bracket through Machin's identity and alternating arctangent series, and recalculated the ellipse margin.

All 28 floating-point runs also replayed with byte-identical output in the recorded environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, one OpenBLAS thread. Byte identity is an observation about this environment, not a promise for other BLAS or library versions.

`verify_audit.py` reproduces the binding and independent exact controls without writing to the supplied packet. Its optional `--numerical` replay runs author scripts only in a temporary copy. Example:

    python3 -B verify_audit.py --packet /path/to/packet --archive /path/to/rank667-30001155-authored-packet.zip --numerical

## Primary statement and normalization

The publisher PDF was independently opened, and the locally available hash-matched PDF was rendered anew. Printed page 395, PDF page 41, visibly gives the radicand d⁴−16A²/π². The preceding prose identifies the Dirichlet Laplacian, and the reference disk has unit area. The original statement therefore agrees with the frozen target. A DOI-route failure was resolved by opening the direct publisher PDF; it did not prevent verification. [Official report](https://ems.press/content/serial-article-files/46205?nt=1).

Let Δ=j₁,₁²−j₀,₁², q=4A/(πd²), and θ=1−3π²/(4Δ). Direct cancellation of g=πΔ transforms the target into

    d²γ ≥ F(q) = 3π² / (1−θ+θ√(1−q²)).

The isodiametric inequality puts q in (0,1]. The certified 0<θ<1/2 makes the denominator positive, F strictly increasing, F(0)=3π² and F(1)=4Δ. A radius-R disk gives d²γ=4Δ. Scaling and the small-q expansion are consistent. In particular the first nonconstant term in the original bound is 24θ A²/d⁶; no missing π factor remains.

## Rectangle and triangle checks

For a rectangle a≥b>0, λ₂ corresponds to the (2,1) product mode, with the expected multiplicity when a=b. Thus d²γ=3π²(1+r²), r=b/a. The proof's inequalities are strict for every positive r: θ(1−√(1−q²))<q²/2, and q²/2<r²/(1+r²) follows from π²>8. Inverting the positive denominators gives the claimed strict result. The proof treats a continuum; the 1,000-point rational grid is only an additional control. As r→0, both normalized quantities approach 3π² and their ratio approaches one.

Lu–Rowlett's Theorem 3 uses the diameter-normalized Dirichlet gap and states the all-triangle lower bound 64π²/9, with equality only for the equilateral triangle. Its stated normalization and scope were checked in the paper and corroborated on the publisher page. Since F(q)≤4Δ<6π²<64π²/9, the transfer is strict for every triangle. This audit does not reconstruct their original computational proof. [Paper](https://arxiv.org/abs/1109.4117v2), [publisher](https://link.springer.com/article/10.1007/s00220-013-1670-9).

## Bessel roots and rational certification

This is not merely a sign test around unidentified roots. The analytic zero-identification argument is sound:

- For 0<z≤2.41, the alternating lower truncation for J₁ is positive. Therefore J₀′=−J₁<0 there, and the J₀ endpoint signs isolate its first positive zero in (2.4,2.41).
- On [2.41,3.84], the even eighth truncation is an upper bound for J₀. Although the first two series terms need not decrease, the tail after the truncation does; that is sufficient for the bound. All nine Bernstein coefficients are strictly negative, so J₀ is negative on the entire interval.
- J₁ is positive up to 2.41. At each later zero through 3.84, J₁′=J₀<0. Thus every such zero is a simple downward crossing. There cannot be two: returning from negative to positive would require another zero without a downward crossing. Together with J₁(3.83)>0 and J₁(3.84)<0 this identifies the first positive zero, not just an unspecified zero.

The independent exact reconstruction agrees with all nine coefficients and endpoint signs. The bounds on x, y and Δ and the rational lower ellipse margin 273124119/3618160000 are correct. Standard separation of variables and Bessel-mode ordering for the disk remain classical background; the certificate is not a stand-alone formalization of spectral theory.

## Ellipse min–max subtraction

The pullback from semiaxes (1,t) to the unit disk cancels the constant Jacobian between numerator and denominator and gives the quadratic form used in the packet. Form ordering gives λ₂(E)≥y and λ₁(E)≤x/t². **The subtraction is in the correct direction:** subtract an upper bound for λ₁ from a lower bound for λ₂.

Putting u=√(1−t²), independently simplifying the difference from F(t) gives

    4u [Δθ − x(1−θ)u − θyu²] /
        [(1−θ+θu)(1−u²)].

This is exactly the stated polynomial P(u). All denominator factors are positive on 0≤u≤1/4, and the subtracted polynomial coefficients are positive. Applying the worst endpoint u=1/4 and the strict rational brackets yields the displayed positive lower margin. For u>0 this proves strictness; for u=0 the separate disk equality calculation applies. The numerical larger threshold is explicitly noncertified and is not used to enlarge the proved interval.

## Strip example and theorem hypotheses

Friedlander–Solomyak Theorem 1.1 was checked against its assumptions and formula. The profile h(x)=2−x² on [−1,1] is positive, smooth, uniquely maximized at 0, with M=2, m=2 and c₊=c₋=1. Their α=2/(m+2) equals 1/2. The effective potential coefficient 2π²M⁻³ equals π²/4, so the oscillator's first two eigenvalues are π/2 and 3π/2. [Primary paper](https://arxiv.org/abs/0705.4058).

The domain relation K_L=LΩ_(1/L) is exact. Scaling their eigenvalue asymptotics by L⁻² yields γ(K_L)=π/L+o(L⁻¹). The upper boundary is concave, giving convexity; direct integration gives A_L=(10/3)L. The simple bounds 2L≤d_L≤√(4L²+4) suffice for d_L/(2L)→1. Consequently d_L²γ(K_L)∼4πL while q_L→0. The claimed divergence and failure of automatic saturation follow. This family does not contradict the conjectured lower bound. The warning that absolute differences vanish under arbitrary dilation is also valid.

## Quantitative literature scope

Andrews–Clutterbuck establishes the diameter-only lower bound, including zero potential. It cannot by itself imply a strictly larger area-dependent expression. [Primary paper](https://arxiv.org/abs/1006.1686v2).

The live unversioned Amato–Bucur–Fragalà record still identifies v2, revised March 18, 2025. Theorem 1 and Remarks 3–5 were independently inspected. The Dirichlet remainder is c w⁶/d⁸; the second-power result elsewhere in the paper is a Neumann result and cannot be substituted. For planar convex sets A≤dw, giving the author's c A⁶/d¹⁴ consequence. On thin unit-length rectangles, a fixed sixth-power remainder cannot dominate the target's positive second-power correction. This invalidates that proposed inference only; it does not disprove either bound or prove that sharper future arguments are impossible. [Primary paper](https://arxiv.org/abs/2407.01341v2).

Targeted current searches located no verified resolution of the exact area-refined formula. This is a limited negative search, not proof that no published, unindexed or unpublished resolution exists.

## Numerical diagnostic review

The 13 parameter cases at two resolutions, plus two stadium refinements, total 28 runs. Inspection confirms standard P1 stiffness matrices, consistent mass matrices and elimination of boundary degrees of freedom. Area and diameter are computed from the actual polygon. For support-function cases, the chosen parameters keep h+h″ positive. Shape labels identify polygonal approximations to the corresponding boundaries; they are not automatic exact smooth-domain computations.

Every replayed Ritz-gap margin was positive; the minimum was 0.33438435884646367. The largest recorded relative matrix residual was about 7.83×10⁻¹¹. Neither fact bounds the PDE gap from below. Individual Ritz upper bounds cannot be subtracted to create a gap lower bound, and algebraic residuals measure only the finite-dimensional problem.

The stadium with length parameter 10 has normalized computed gaps:

- (64,12): 132.02199446189775
- (128,24): 63.56449208630818
- (256,48): 41.24532621061223
- (512,96): 33.66357767517758

These changes justify the explicit underresolution warning. Refinement changes both discretization and the boundary polygon, and the final value is not a certified limit. No universal conclusion or rigorous counterexample may be inferred from these tests.

## Independence, exclusions and remaining work

The reviewer did not author or modify the frozen packet and used no helper reviewers. All inspection and replay were read-only with respect to the original artifacts; no remote writes occurred. The six supplied source PDFs matched their declared public hashes and byte counts. Relevant primary statements were separately checked through live source access and independent rendering. The underlying source theorems were treated as literature dependencies, not completely reproved.

Dataset identity, prior-repository search and queue-history claims were read as provenance metadata; this mathematical audit did not re-fetch the full external dataset or independently reconstruct those earlier repository searches. No conclusion here requires interpreting those provenance claims as new independent verification.

The five approach families are substantively distinct and are documented as attempts rather than five universal proofs. The proposed exhausted-budget status is supported. Outstanding mathematical tasks remain the unrestricted inequality, all non-disk equality exclusions, and a precise classification of normalized extremizing sequences. Preserve the archive as the author freeze and associate this audit as a separate, hash-bound review.
