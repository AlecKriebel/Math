# Sources, credit and verification boundary

Problem 30005461 / OWR-12697710-007. The full two-clause target is accepted in the included [mathematical audit](MATHEMATICAL_AUDIT.md). No priority or novelty is claimed. Source identities, exact PDF digests and sizes, and historical inspection coverage are recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json).

## Original question and exact family

Bruce Reznick, *The Odd Powers of the Motzkin Polynomial, etc.*, in *Real Algebraic Geometry with a View toward Koopman Operator Methods*, [Oberwolfach Report 14/2023](https://doi.org/10.4171/owr/2023/14), printed pp.778–780 / PDF pp.38–40. Both questions occur on printed p.780, whose page image was independently inspected. The exact coefficient perturbation is f_c=x^4*y^2+x^2*y^4+1-c*x^2*y^2. The report's different positive-definite perturbation by c(x²+y²+z²)³ is not a substitute for this family.

## First clause: published result and both corrections

Grigoriy Blekherman, Khazhgali Kozhasov and Bruce Reznick, *On odd powers of nonnegative polynomials that are not sums of squares*, [Forum of Mathematics, Sigma 14 (2026), e65](https://doi.org/10.1017/fms.2026.10221), published online 27 April 2026. The mixed-exponent result is published Theorem 5.3, previously Theorem 44 in [arXiv:2407.21779v1](https://arxiv.org/abs/2407.21779v1). The truncated-binomial ingredient is credited by BKR to Iosif Pinelis. This attribution was verified through BKR; the cited MathOverflow discussion was not independently inspected.

[CREDITED_MIXED_EXPONENT_PROOF.md](CREDITED_MIXED_EXPONENT_PROOF.md) gives the complete authored proof, including a direct argument for arbitrary real polynomials and a separate equal-degree homogenization check. It retains both necessary corrections openly:

- The archived positivity assertion needs the even index 2r. Literal positivity for index r is false; n=3,r=1,t=-1 gives -2.
- The homogenization sum's upper limit must be 2r. The printed n=3,r=1 expression v²+3uv is negative at (-1,1); the corrected form is v²+3uv+3u².

The archived p.21 and current publisher HTML were checked. The correctly indexed proof establishes the published theorem; these corrections do not create a novelty claim. BKR published Theorem 6.3 supplies the threshold interval convention. The inspected final paragraph still asks whether the limit is 3, so this edition does not describe the limit as explicitly stated in that source.

## Threshold: published projective Positivstellensatz

Claus Scheiderer, *A Positivstellensatz for projective real varieties*, [Manuscripta Mathematica 138 (2012), 73–88](https://doi.org/10.1007/s00229-011-0484-3), Corollary 4.2. The inspected [author manuscript](https://www.math.uni-konstanz.de/~scheider/preprints/ppss.pdf) is dated 5 April 2011 and has 14 pages; it is not represented as the publisher's 16-page typeset PDF. The publisher lists online publication on 6 August 2011 and issue publication in May 2012. The historical reading covered the positivity convention in Sections 2.4–2.5, the full Theorem 4.1 statement and proof, Corollary 4.2 and Remark 4.8. PDF pages 9 and 11 were visually inspected, and the independent audit rechecked the corollary and publication identity.

The essential result permits reduced singular projective schemes; smoothness is not a hypothesis. It requires no curve components, Zariski-dense real points, an ample square-line-bundle factor and strict positivity at every real point. It gives the relevant sum of squares for every sufficiently large N. The full target-specific verification for ABC=D³, including singular boundary points and even-N/odd-power parity, is in [PROOF.md](PROOF.md). No theorem for merely positive affine polynomials or for nonnegative sections on smooth surfaces is substituted.

[Stacks Project, Lemma 30.8.1](https://stacks.math.columbia.edu/tag/01XS) supplies H¹(P³,O(t−3))=0 for every integer t. The cubic hypersurface exact sequence then lifts every global square-root section to a homogeneous polynomial and identifies the kernel. The cubic substitution is a polynomial ring homomorphism; its projective base points create no denominator or missing-point issue.

Scheiderer's theorem and projective-space cohomology are credited imported results, not re-proved foundational theorems or formal certificates. The written proof checks their applicability in full and proves the exact substitution and limiting inference. It produces no explicit exponent, rate or uniform exponent as c approaches 3, and no affirmative SOS claim at c=3.

## Optional real-delta calculation

Lorenzo Baldi, Grigoriy Blekherman, Khazhgali Kozhasov, Daniel Plaumann, Bruce Reznick and Rainer Sinn, [*Stubborn Polynomials*, arXiv:2602.01191v1](https://arxiv.org/abs/2602.01191v1), is treated as a preprint. The historical arXiv record listed no journal reference, and Blekherman's author page described it as submitted for publication. The arXiv submission is 1 February 2026; the PDF is dated 3 February 2026.

Definition 6.3 supplies only the real-delta recursion used in [REAL_DELTA_APPENDIX.md](REAL_DELTA_APPENDIX.md). The unchanged appendix explicitly checks all real projective zeros and both real charts at each blowup, giving 3+3=6 for 0<c<3. The independent audit accepts this direct local calculation. The main limit proof does not depend on the preprint, its Del Pezzo/resolution criteria, or their deeper references. The historical source inspection read the relevant preprint proof route and visually inspected pp.19–20; this does not amount to a new independent foundational audit of those criteria. No total-delta assertion at c=3 is made.

## Edition and review limits

The complete principal argument, all substantive independent audit findings, the complete credited mixed-exponent proof/corrections, and the unchanged optional appendix are included. This AI-assisted edition is unrefereed. Mathematical acceptance does not mean external human peer review, journal acceptance, exhaustive literature clearance or formal proof-assistant certification.

Historical finite checks support transcription and vulnerable interfaces. They do not replace the universal proofs. Edition preparation rechecked frozen byte identities and publication integrity without new scholarly retrieval, source-text inspection, literature searching or mathematical-computation reruns. Programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded. The mathematical verdict does not depend on omitted software or certificates.
