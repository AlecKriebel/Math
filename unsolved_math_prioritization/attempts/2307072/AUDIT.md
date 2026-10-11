# Mathematical audit of the Beurling annihilator witnesses

Date: 11 October 2026 (UTC).

Target: problem 2307072, AMR0227072, Hayman–Lingham Problem 7.72.

This proof and audit are AI-assisted. No external human review, peer review, or formal proof certification is claimed. The word PASS below is the outcome of the stated mathematical checks, not an institutional endorsement.

## Verdict

**PASS for both negative answers under the printed definitions.** The polynomial witnesses disprove a uniform bound on the polynomial subspace, and the single bounded angular witness has an essentially unbounded transform. The companion [PROOF.md](PROOF.md) supplies a standalone derivation, establishes the exact polynomial norm, and explicitly handles the analytic and distributional issues described below.

**Historical credit remains unresolved at primary-source level.** The later edition's bibliography is now primary-verified, but the chapter's asserted Volberg attribution was not independently accessible in primary full text. Do not label this verification a new solution or attribute these particular witnesses to Volberg or Bañuelos–Janakiraman on the evidence obtained here.

## Proof identity

The companion proof is preserved byte-for-byte in this edition: 10,718 bytes, SHA-256 `e9d43de1562948d62264be2ddb40a68019dedcfd38406671a32608a47e05059b`. The exact editorial changes to this audit are recorded in [EDITORIAL_MAP.json](EDITORIAL_MAP.json). The mathematical-check section is unchanged.

## Mathematical checks

1. **Printed conventions: PASS.** Independently rendered and visually inspected arXiv:1809.07200v2, PDF p.184 / printed p.183. The integral defining the annihilator is bilinear, the analytic test space is area-integrable holomorphic functions, the Beurling kernel has coefficient −1/π, and the polynomial class includes both z and its conjugate. The formula integrates over the unit disc, exactly equivalent to zero extension of the input for the full-plane transform.

2. **Polynomial class and normalization: PASS.** The input is the finite polynomial z²Σ(j=0 to m−1)(1−z z̄)^j. Its modulus at radius squared t is 1−(1−t)^m. It is strictly below one inside the disc but approaches one on annuli of positive area, so the essential norm is exactly one.

3. **Annihilation of all analytic L1 tests: PASS.** The bounded input times any analytic L1 test is absolutely integrable. Polar Fubini is therefore valid. For each fixed interior radius, uniform convergence of the Taylor series permits the angular integral; all modes have strictly positive exponent. No density assertion, boundary Taylor convergence, or unproved interchange over the whole disc is needed.

4. **Direct Cauchy transform: PASS.** An independent angular calculation gives Cf(z)=−z∫(|z|² to 1)a(s)/s ds for angular mode e^(2iθ)a(r²), and zero outside the disc. The integral with the Cauchy kernel is absolutely convergent, so this calculation has no principal-value Fubini issue. This identifies the proposed primitives exactly, avoiding a possible entire-function ambiguity in distributional inversion.

5. **Sign and normalization: PASS.** With ∂=(∂x−i∂y)/2, differentiation of 1/(πz) gives −pv(1/z²)/π. The direct absolutely convergent integral at zero independently gives −H_m for every polynomial witness. The radial substitution dA=2πr dr=πdt supplies the correct constant.

6. **Polynomial essential supremum: PASS, strengthened.** Inside the disc the transform is G_m(|z|²), where G_m(t)=1−(1−t)^m−Σ(k=1 to m)(1−t)^k/k. It is continuous and strictly increasing from −H_m to 1, since G_m′=P_m+m(1−t)^(m−1)>0 on (0,1). Consequently the exact essential norm is H_m. Positive-area neighborhoods of the origin justify the lower bound; an isolated value is not being used as sufficient evidence.

7. **Zero boundary trace: PASS.** Both primitives vanish on the unit circle and are continuous across it after zero extension. Integration by parts produces no boundary measure in their first derivatives. The polynomial primitive belongs to W^(1,∞)(C).

8. **Single-witness origin: PASS.** The primitive z log|z|² tends to zero at the origin. The inner boundary error in an integration-by-parts calculation is O(ε²|log ε|), tending to zero. Both weak derivatives belong to every finite Lp, so the primitive belongs to W^(1,p)(C) for 1≤p<∞. There is no point mass at zero.

9. **Principal values: PASS.** Polynomial inputs are smooth at every interior point, and the angular input is smooth at every nonzero interior point. Subtraction of the local input value, combined with zero angular mean of the kernel, yields ordinary principal-value convergence and agreement with the distributional derivative at these points. The single witness has no finite principal value at zero; this null-set exception is stated explicitly and does not affect its almost-everywhere transform or essential norm.

10. **General membership failure: PASS.** For the single input, Bv=1+log|z|² at every nonzero interior point. For every M≥1, the set where |Bv|>M has area π exp(−M−1)>0. This proves essential unboundedness directly, not merely pointwise divergence at zero.

11. **Scope: PASS.** Every individual polynomial transform in the family is bounded; what fails on the polynomial subspace is a common bound. The separate angular witness handles the stronger claim that all inputs have bounded transforms. Both calculated transforms vanish almost everywhere outside the disc, resolving any ambiguity between disc and full-plane output norms.

## Source and attribution audit

### Primary problem statement

Hayman and Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, 21 September 2018. The version record confirms v2 is the latest arXiv version displayed on the audit date. The audited PDF was pinned and independently rendered; the definition and Problem 7.72 were visually checked on PDF p.184 / printed p.183. Its update reports no progress known to the authors at that time; that sentence is not evidence of present-day openness.

- Version record: https://arxiv.org/abs/1809.07200v2
- PDF: https://arxiv.org/pdf/1809.07200v2
- PDF SHA-256: 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0
- PDF size: 1706228 bytes

### Later book and its reference 52

The publisher's 2019 book page and Chapter 7 landing page were inspected. They verify the publication and Chapter 7 page range, 185–216, but the chapter text is subscription content. The freely available publisher-hosted back matter was downloaded, pinned, and rendered. On back-matter PDF p.7 / printed p.247, reference 52 is Bañuelos and Janakiraman, *Lp-bounds for the Beurling–Ahlfors transform*, Transactions of the American Mathematical Society 360(7), 3603–3612 (2008), and is explicitly indexed to Problem 7.72. This bibliographic connection is primary-verified.

- Book: https://link.springer.com/book/10.1007/978-3-030-25165-9
- Chapter 7: https://link.springer.com/chapter/10.1007/978-3-030-25165-9_7
- Back matter: https://link.springer.com/content/pdf/bbm:978-3-030-25165-9/1
- Back-matter PDF SHA-256: 1a86ad9f007d381840aedef146b64b98b4ce9f68a76552b8de61ebdc21b97afe
- Back-matter PDF size: 422343 bytes

### Bañuelos and Janakiraman paper

The author-hosted 11-page PDF was read in extracted text, including its introduction, further remarks and references, and rendered pages 1 and 10 were visually inspected. Its topic is full-plane finite-p norm estimates; equation (1.1) confirms the same negative Beurling kernel. The inspected author-hosted text does not explicitly discuss the bilinear annihilator, Problem 7.72, or the two witnesses audited here. Mentions of Volberg concern finite-p norm estimates. This absence in the inspected version does not prove that no related result exists elsewhere, and the author-hosted file should not be represented as a verified byte-identical copy of the final published article.

- Author-hosted PDF: https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf
- DOI: https://doi.org/10.1090/S0002-9947-08-04537-6
- Author-hosted PDF SHA-256: 430876e18a0941fdfbdf30d33dc73dd876cccd39c2d38cc735610fcc45363a66
- Author-hosted PDF size: 199679 bytes

The AMS final-PDF retrieval returned HTTP 403; no attempt was made to evade that restriction. Therefore the final published article was not independently inspected in this audit.

### Remaining historical uncertainty

A secondary transcription of the 2019 book says that Update 7.72 credits Volberg and refers to reference 52. This was useful as a research lead only. The publisher bibliography confirms the reference's identity and linkage to 7.72, but it does not reproduce the attribution sentence or an explicit proof of the annihilator result. The publisher chapter was not available in full text, and no primary document explicitly crediting the resolution was established. The safe conclusion is an independently verified negative answer with historical attribution left qualified. The proof in `PROOF.md` uses only the printed definitions and its own calculations.

## Verification scope and public artifacts

The all-m argument is the mathematical proof. The audit also recorded 512 exact-rational polynomial identity checks for m = 1 through 64, with successful runs under normal Python, `-O`, and `-OO`. These finite checks are ancillary; they do not certify the analytic argument, settle historical priority, or replace the proof. Packet preparation rechecked file identities and the reported outcomes; it did not rerun those mathematical checks or repeat the source inspections.

- [PROOF.md](PROOF.md): the complete standalone proof, including the exact polynomial norm.
- [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json): public scholarly-source titles, URLs, PDF hashes and sizes, and the recorded access and inspection scope.
- [EDITORIAL_MAP.json](EDITORIAL_MAP.json): exact byte ranges, replacement text, and hashes for the editorial changes, with the proof and mathematical-check section preserved.
- [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json): the closed public file list with hashes and byte counts.

This edition contains authored mathematical analysis and public verification metadata. It includes no copied source documents, extracted source text, source images, dataset contents, programs, raw check tables, or private coordination material. The source inspections described above were performed during the audit on 11 October 2026; packaging is not a further independent review. Historical credit remains primary-unverified, and no novelty claim is made.
