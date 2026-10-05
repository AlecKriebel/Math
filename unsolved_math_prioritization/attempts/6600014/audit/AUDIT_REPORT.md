# Independent audit: planar Delone ambient extension

## Disposition

**PASS.** The frozen submission correctly classifies problem **6600014 / AMR-065-0014**, rank **734**, as **already_solved**, using **1/5** approaches and assigning **zero original-solution credit**. No mandatory mathematical or provenance revision was found. This is a verified application of an external published theorem, not an independent reconstruction of that theorem's long proof.

Reviewed freeze: `DELONE_6600014_SAFE_AUDIT.zip`, 15,113 bytes, SHA-256 `2511a95f32681a85c337393c1c0ac2f7ad5525247f3e484c00d6150423c477cb`. All nine archived files equal the author directory byte for byte. The eight nonmanifest payload hashes and the separately pinned author manifest agree with the freeze receipt. The author freeze was not edited; no remote writes were made.

## Exact problem and hypothesis audit

The primary authority is [Adiceam's published problem collection, section 2.6](https://link.springer.com/article/10.1007/s40598-016-0046-6). The BL definition in its introduction requires a bijection. Problem 2.6.1 concerns a Delone subset of the plane already BL-equivalent to the integer lattice and asks for an ambient bilipschitz rectification. This was cross-checked against page 8 of [arXiv:1604.06280v2](https://arxiv.org/abs/1604.06280), including a fresh visual rendering.

The submission preserves all essential quantifiers. Linear repetitivity and the Burago-Kleiner condition occur in subsequent historical discussion as sufficient special cases. Neither is an assumption of the question. Repetitivity, finite local complexity, periodicity, bounded displacement, homogeneity, origin fixing, unit-translation equivariance, and orientation are likewise not requirements. The target is existence of some ambient map. A prescribed-map extension theorem is therefore stronger than needed.

The identifier and rank are supported by the retained campaign descriptor and queue-read evidence. This audit does not turn those into a claim of current live-catalogue verification: the author's HTTP 403 retrieval receipt was reviewed, and no live-catalogue text or status is asserted.

## Published theorem identity and status

The resolving article is Michael Dymond and Vojtech Kaluza, *Planar bilipschitz extension from separated nets*, **Journal of the London Mathematical Society 113(4), e70540**, [DOI 10.1112/jlms.70540](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.70540). Publisher metadata gives first publication **23 April 2026**; [Birmingham's record](https://research.birmingham.ac.uk/en/publications/planar-bilipschitz-extension-from-separated-nets/) agrees. [ISTA's record](https://research-explorer.ista.ac.at/record/21778) gives 1 April, labels the PDF as the published version, and provides an MD5 matching the freshly downloaded bytes. The author already explains the date discrepancy correctly.

Theorem 1.1 is on published page 3; its quantitative version, Theorem 1.5, is on page 7. They apply to **every** L-bilipschitz map from Z² into R², for L >= 1, and supply an extension defined on the entire plane. The explicit bound is **10^20000 L^6000**. There is no small-distortion, orientation, repetitivity, or equivariance assumption. The publisher HTML and freshly rendered PDF agree. The article's introduction explicitly identifies Adiceam Problem 2.6.1 as resolved.

The source's bilipschitz constant is max(Lip(f), Lip(f inverse)); this is exactly the convention used in the submission. Its terminology sometimes uses homeomorphism for an embedding onto its image. Consequently surjectivity still merits an explicit argument rather than a terminological assumption.

[arXiv:2410.22294v3](https://arxiv.org/abs/2410.22294) is the accepted manuscript dated 19 March 2026. Its v1 had the title *Extending bilipschitz mappings between separated nets*. The separate companion [arXiv:2507.22007v3](https://arxiv.org/abs/2507.22007), now published under [DOI 10.54330/afm.181562](https://research-explorer.ista.ac.at/record/21766), uses that earlier title. The submission does not confuse the two works. Targeted correction/retraction searches returned no contrary notice; this is a bounded search, not a bibliographic guarantee.

## Complete reduction audit

1. A bijection b from D to Z² with constant L has an inverse g on all of Z² with the same two-sided metric bounds. The theorem's fixed domain hypothesis is satisfied exactly.
2. Apply the published theorem to g. The output H is defined on all of R² and agrees with g on Z². Its finite lower metric bound makes it injective and its upper bound makes it continuous.
3. Invariance of domain makes H(R²) open. If H(x_j) converges, the lower bound makes x_j Cauchy; completeness and continuity supply a preimage of its limit. Thus H(R²) is also closed. Nonemptiness and connectedness give surjectivity. This step uses the whole-plane domain and the global lower bound, not merely that the lattice image is Delone.
4. The inverse A = H inverse is bilipschitz with the same constant. For each d in D, set z = b(d). Then H(z) = d, hence A(d) = z. This proves both A restricted to D equals b and A(D) = Z², including the equality rather than just an inclusion.

All four steps are valid. Invariance of domain is openly imported as a standard topological theorem. No orientation is chosen or promised; inverses of either orientation work. The fixed lattice-domain route also explains why separation and covering constants of D need not enter this particular bound. It does not imply that arbitrary Delone sets admit a bijection to the lattice.

## Scope and negative-control audit

The complete elementary arguments in `SCOPE_AND_CONTROLS.md` were reviewed, not inferred from numerical sampling.

- **Missing rectifiability:** an ambient rectification restricts to a bijection, so nonrectifiable Delone sets are outside the hypotheses. The [Cortez-Navas primary paper](https://msp.org/gt/2016/20-4/gt-v20-n4-p03-s.pdf), first two article pages, genuinely supplies repetitive nonrectifiable examples in dimension two and higher.
- **Earlier special case:** [Navas's 2016 note](https://www.numdam.org/item/10.1016/j.crma.2016.08.010.pdf), pages 976-977, assumes linear repetitivity in its main theorem and discusses the Burago-Kleiner route. It is not incorrectly substituted for the general planar result.
- **Bounded displacement:** for D = 2Z² and a proposed displacement bound M, counting preimages of lattice points in [-n,n]² yields the stated contradiction for every integer n > M. The dilation still rectifies D. The proof handles arbitrary real M >= 0, not only the integers sampled by the author.
- **Origin and homogeneity:** translating the lattice by (1/2,0) excludes 0 from D. An injective map fixing 0 cannot send D onto a set containing 0. The homogeneity implication at x = 0 is valid.
- **Specified unit equivariance:** its values on 2Z² must form F(0) + 2Z². If that were Z², containing 0 forces F(0) into 2Z², leaving the parity obstruction at (1,0).
- **Dimension one:** the adjacent transposition is a 2-bilipschitz involution on Z but cannot have a continuous injective extension to R, by the two intermediate-value occurrences stated in the submission. This does not refute existential one-dimensional rectification. Increasing enumeration of a Delone subset gives gaps between r and 2R; the piecewise-linear map has global positive slope bounds and is onto. The warning about the historical phrase “any dimension” is justified.

## Source and computational verification

All **six** PDFs were independently downloaded again by ordinary public HTTP requests. Each returned HTTP 200 and matched its retained SHA-256, byte count, and page count exactly. Metadata-only receipts are in `INDEPENDENT_SOURCE_VERIFICATION.json`. Public PDFs, extracted article text, screenshots, raw catalogue records, and private coordination are excluded from this audit package.

The author verifier passed in place and in a fresh relocated directory. Seven altered-copy controls were rejected: changed deduction, changed source hash, changed expected arithmetic, added file, added directory, missing file, and a same-content symlink. The author script is assertion-based; it was run in normal Python mode, as instructed. Its checks are not a standalone cryptographic trust anchor; this audit also pins the external freeze and every author file.

The independent verifier uses explicit exceptions rather than assertions. It adds 32,896 exact adjacent-swap pair checks; 1,601 rational displacement bounds; 18 reflected/unreflected affine scale-and-translation cases with 1,458 inverse points and 58,320 exact squared-distance pairs; and 57 rational checks of the ceiling estimate. The general proofs above remain the mathematical basis.

The polynomial arithmetic was checked against the displayed source parameters: the product gives exponents **14,142** on 10 and **5,418** on L. The claimed 20,000 and 6,000 dominate because L >= 1. This verifies substitution arithmetic, not the published construction or its lemmas.

## Limits and reproducibility

The full retained deduction, scope controls, metadata, verifier, and prior-attempt summary were reviewed. The author's bounded repository search receipts were inspected and support only their stated limited negative result; this audit did not rerun an exhaustive repository history search. Neither reviewer nor author claims independent verification of the full published 34-page article, the full companion proof, or the literature-control constructions.

Run `python verify_audit.py` from any working directory to check the audit manifest and exact controls. Optional arguments `--author-dir`, `--author-archive`, and `--source-dir` compare local inputs with pinned metadata without downloading or copying them into the package. The source directory expects the six filenames recorded in the source manifest. `INDEPENDENT_CHECKS.json` records the acceptance and rejection results. A separate archive receipt pins this audit's manifest and archive; checksums are integrity evidence, not digital signatures.

**Final recommendation:** accept the exact frozen author package as a credited prior resolution, **already_solved, 1/5**, with no novelty claim and no further original proof attempts required for this precise statement.
