# Local Ricci-pinching maxima on an almost-abelian group

Alec Kriebel — independent researcher; ORCID https://orcid.org/0009-0001-9320-500X.
Research note, 13 October 2026 (UTC).

The [six-page preprint](preprint/local_ricci_pinching_maxima.pdf) gives an explicit negative answer to the literal fixed-group assertion in [Morgan–Pansu Question 14, section 11](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf#page=12). For the known five-dimensional family A_u = J ⊕ uE₁₂, every parameter 0 < u < 1/2 has a standard metric that is a non-strict local maximum of F = Scal²/||Ric||² with value 1/3 among all nearby left-invariant metrics on the fixed simply connected group. Its Ricci endomorphism fails Ric = cI + D with D a derivation of that group's Lie algebra. An explicit metric on the same group has F = 9/17, so this local maximum is not global. The proof covers the full metric Gram matrix and unrestricted cross-block, with a uniform cubic remainder along the flat family; the Hessian alone is insufficient. Neither endpoint is included.

The metric is nevertheless a geometric Ricci soliton, isometric to R² × H₃. A solvsoliton presentation on another transitive group does not meet the derivation assertion for the original fixed group.

Lauret's [23 July 2018 talk](https://www.ime.usp.br/~mtg/slides/j_lauret.pdf) already announces the relevant negative existence result. The family and value 1/3 are prior Lauret–Will work. The actually inspected arXiv versions [I v1](https://arxiv.org/abs/1808.01380v1) and [I v2](https://arxiv.org/abs/1808.01380v2) leave positive small-parameter local maximality unknown. The chronology does not establish withdrawal or falsity of the earlier announcement. Final journal full texts were inaccessible and are not attested. This is an attributed explicit proof note; it claims no novelty, first assertion, first proof, or current community-open status. Its bibliography and bounded priority qualifications are in the paper and verification materials.

AI tools were used extensively in solving, symbolic computation, source review, drafting, and adversarial verification. The preprint is unrefereed and has received no external human peer review. Machine-agent reviews are not human refereeing.

## Files and reproduction

- [Standalone TeX](preprint/local_ricci_pinching_maxima.tex) and [source ZIP](preprint/local_ricci_pinching_maxima_source.zip): source, build instructions, and a byte manifest. Compiler versions can change PDF serialization; the distributed PDF has its own exact hash.
- [Verification ZIP](preprint/local_ricci_pinching_maxima_verification.zip): 100 members, comprising the intact 73-file version-2 core, 25 selected complete review/check artifacts, a README and support manifest. The selections outside the core do not represent the entire sealed review corpus or redistribute third-party primary-source PDFs. Historical and private case-relative references are identified in the support README.
- [Version-2 instructions](verification_v2/README.md): 54 mandatory evaluations of 39 preserved predicates in normal and optimized Python, exact input custody, and corruption controls. Run `python -B verification_v2/run_all.py` and `python -B -O verification_v2/run_all.py` in an environment containing the recorded SymPy version. The ZIP also includes exact standard-library rational curvature and boundary checks.
- [Proposed preprint metadata](preprint/ZENODO_METADATA.json) and [delivery manifest](DELIVERY_MANIFEST.json): exact bytes, source origins and Git modes. Actual production DOI and tracker receipts are recorded separately after publication; the proposed metadata is not a publication receipt.

The original mathematical proofs and historical audit are preserved. Current prose addenda correct status/version interpretations and prior-source credit. The three current checkers preserve their original mathematical predicates in mandatory branches. Original historical optimized assertion outputs remain uncertified, and two absent historical byte objects remain unattested. Historical component conclusions are distinct from later complete-package reviews.

The selected source row is `claimed_solved` with author turns `2/5`; editorial, verification and publication work adds zero substantive author proof-search turns. The result is the explicit negative answer stated above, with the priority qualifications already disclosed. This delivery packet covers only problem 6800014.
