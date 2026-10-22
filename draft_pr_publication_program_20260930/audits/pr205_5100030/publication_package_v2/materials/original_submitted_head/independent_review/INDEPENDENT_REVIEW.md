# Independent review: 5100030 / k601

Date: 2026-10-01. **Verdict: PASS for the complete source target. No mathematical correction required.**

Frozen candidate SHA-256:

    09bfb91289e683809e71a668e020c1d37f8f99f717e3658d1cc80268fe55f147

Frozen author manifest SHA-256:

    bc0b834d753f0df8c6912d364144bbe3bea9bfde95c026fc815b0cb9a4b61fd9

I independently checked the proof, exact source scope, all denominators and index permutations, and the geometric distance normalization. The result is a credited application of classical Jacobi identities and a published billiard parametrization; this review does not certify novelty, priority or human peer review.

## 1. Exact source and geometric scope

I inspected the full imported target and both rendered Table 7 pages: [arXiv:2004.12497v11](https://arxiv.org/pdf/2004.12497v11), printed p. 9, and the [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), p. 349. Both retain k601 as the product of the two sums of ordinary focal-pedal distances for odd N. Section 3.7 defines these as distances from each focus to the foot on the original orbit's side line.

The candidate uses the correct side lines and ordinary nonnegative Euclidean distances. It does not replace them by signed distances, contact-point distances, an area product, or distances to antipedal vertices. The adjacent k603/PR110 antipedal telescoping result is a different statement and is not an input. Nearby table renumbering does not change k601.

The source's nondegenerate nested confocal ellipse setting is retained. The proof includes every permitted primitive odd winding class and correctly handles odd repetitions by scaling each sum. It does not claim hyperbolic-caustic or degenerate-caustic cases.

## 2. Published parametrization and notation

Stachel's full published *On the motion of billiards in ellipses*, DOI [10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2), was checked at Theorem 4.3, pp. 1614–1615. Printed p. 1614 was independently rendered. It supplies exactly the vertex parametrization and the outer-axis formulas used in the candidate.

The source calls the caustic eccentricity a modulus m; the candidate renames it k and consistently reserves m=k² for the elliptic parameter. This is correct. For 0<tau<N/2, h=2tau K/N lies strictly between 0 and K, so cn(h)>0 and dn(h)>0. No axis formula divides by zero. Their squared difference is alpha²−beta²=c², as required; the constructed outer ellipse strictly contains the caustic.

## 3. The finite cyclic identity is valid for every odd N

I verified the [DLMF addition formulas](https://dlmf.nist.gov/22.8), [real period/zero conventions](https://dlmf.nist.gov/22.4), and [Jacobi epsilon/zeta formulas](https://dlmf.nist.gov/22.16). DLMF 22.16.27 initially states the epsilon law; the paragraph in §22.16(iii) explicitly gives the same law for zeta, and 22.16.34 gives its real period 2K. The candidate's citation is accurate.

For a_r=4Kr/N, a nonzero shift with 1≤r<N can be a zero of sn only if N divides 2r. That never occurs for odd N. Since 0<m<1, division by m sn(a_r) is legitimate. The shifted arguments permute the N-point set modulo 4K; zeta's smaller period 2K is compatible with, rather than an obstruction to, that permutation. Summing its addition formula gives the stated constant cyclic sn correlation with the correct sign and factor N.

The two difference identities were independently recovered by solving their 2-by-2 linear system. Its determinant 1−mS² is strictly positive on real arguments, since |S|≤1 and m<1. The resulting signs are

    dn(x)dn(y)=dn(a)−m cn(a) sn(x)sn(y),
    cn(x)cn(y)=cn(a)−dn(a) sn(x)sn(y).

Their combination is exactly equation (3.3). Grouping ordered pairs by j−i modulo N counts every off-diagonal term once; no factor of two or parity multiplicity is missing. The diagonal contribution is N(1−m). This proves the all-odd-N lemma, not merely a collection of tested periods. The excluded even shift r=N/2 genuinely has sn(a_r)=0 and is not divided through by continuity.

## 4. The distances and the quarter-period step

The proposed caustic tangent at v_i=u+(2i+1)h passes through both neighboring vertices. Substitution reduces its incidence equation to the second difference identity, with shift h or −h; cn and dn are even, so both endpoints are covered.

The squared norm of the tangent normal is dn(v_i)²/beta². Since dn is positive for real arguments, the positive norm is dn(v_i)/beta. At the two foci the absolute line evaluations become 1±k sn(v_i), both strictly positive because 0<k<1. Therefore the displayed q± formula is for the actual ordinary distance, for all phases and star winding classes. The fixed foci are inside the caustic, consistent with these signs. Feet on line extensions create no exceptional case.

The pointwise relation q+q−=beta² is checked but is not mistaken for constancy of the product of sums. The latter is supplied by the cyclic lemma.

The coprimality gcd(tau,N)=1 permutes the arguments modulo the full 4K real period, exactly as required for sn/dn. Using a 2K period for that function would be wrong; the candidate does not do so. Quarter-shift identities give A=D/k' and B=−C/k', with k'=beta/alpha. Hence beta²(A²−mB²)=alpha²(D²−mC²), including the scale factor in (4.3).

At v=0, the odd function sn/dn cancels in opposite argument pairs, and the resulting positive expression (5.1) is correct. Reversing orientation permutes distances. Repeating an odd primitive orbit multiplies the product by the square of the repetition number. The separate circular case k=0 is correctly proved directly, without using the m-denominator argument; beta=0 remains excluded.

## 5. Independent controls and provenance

My separately authored `independent_check.py` passed **3,609 exact assertions** and **8,938 numerical diagnostics**. Exact checks cover the inverted addition system, cross-correlation algebra, diagonal identity, distance normalization, and odd-shift/permutation arithmetic through N=101.

The numerical portion uses direct Euclidean distances to lines through the computed original vertices, rather than taking the proposed distance formula as its input. It tests 45 families, all primitive winding classes for N=3,5,7,9,13 at three moduli and three phases, caustic tangency, positivity, the family constant, quarter-shift normalization and phase-independent cyclic correlations. At 75 decimal digits, the maximum scaled residual is about 3.49e-74. An even-period negative control has variation about 0.2144. These diagnostics are not interval certificates; the written telescoping proof supplies the universal conclusion.

I inspected the author's checker and its stated separation of exact algebra from 126 numerical cases. I did not execute that checker or count its tests as my own independent run. The source identity and independent controls agree with its reported results.

All eleven entries of the frozen author manifest match, as do all three primary PDF hashes in source_manifest.json. No frozen author file was edited. Reading PDFs and page images are excluded from the portable review package. The public review artifacts are this report, `independent_check.py`, `INDEPENDENT_CHECKS.json`, and `REVIEW_SHA256SUMS`.

The scoped review is complete (100%). No remaining mathematical blocker was identified. Publication remains the coordinator's action; this review made no remote changes for k601.
