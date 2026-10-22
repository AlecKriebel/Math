# Source and scope check

Checked: 2026-10-04 UTC. Numeric upstream identity: **2305070**; source label **AMR-022-5070**; queue rank **580**.

## Primary statement

- Start page: https://www.unsolvedmath.com/problems/2305070 . The web reader could not retrieve it; an ordinary HTTP request returned 403. No inaccessible page content is treated as verified.
- Source: W. K. Hayman and E. F. Lingham, Research Problems in Function Theory (New Edition), https://arxiv.org/abs/1809.07200 . Problem and Update 5.70 are on printed p. 111 (zero-based PDF page 111). The exact question is quoted in PROOF.md.
- The question distinguishes a single unbranched component from the earlier branched construction. The 2018 update gives no later progress. This is a dated statement, not evidence that the problem must still be open in 2026.
- The arXiv PDF was retrieved and its SHA-256 checked against the copy used for reading: 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0. Size: 1,706,228 bytes. The document is not redistributed in this report.

## Original and related primary literature

1. Barth–Clunie (1982), DOI https://doi.org/10.1090/S0002-9939-1982-0660605-9, is the cited earlier construction. The publisher full text could not be retrieved. Its proof has not been reconstructed or accepted as an unbranched solution.
2. Hayman–Wu (1981), DOI https://doi.org/10.1007/BF02566219, Theorem 1, p. 366. The author-uploaded article text identifies the finite-length theorem for preimages of lines or circles under univalent maps. The theorem is used only within those hypotheses in PROOF.md. Source: https://www.researchgate.net/publication/226448362_Level_sets_of_univalent_functions . Its proof is a cited dependency, not claimed as a new result.
3. Nicolau–Reijonen (2021, first online 2020), https://doi.org/10.1112/blms.12395, final discussion; author PDF https://mat.uab.cat/~artur/data/nicolau_reijonen_nou-1.pdf . The discussion cites Jones's example with infinite total length at every intermediate modulus and discusses a different inner-function question. It does not state that one component has infinite length. It therefore does not resolve the target here.
4. Jones (1980), DOI https://doi.org/10.1307/mmj/1029002311. Publisher access was blocked in this check. No reconstruction of Jones's proof is claimed. The total-length/component distinction is independently demonstrated by Proposition 2, which has a complete proof in this report.

Searches included the exact problem wording, unbranched level components, Barth–Clunie and the original article title, and newer level-set literature. No verified later solution to the exact question was found. This is a bounded search result, not a proof of current open status or novelty of the auxiliary observations.

## Imported record and prior work

- The repository manifest pins ulamai/UnsolvedMath at revision 37e53eabe540fb458758e198be61634bd02ee008: https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/37e53eabe540fb458758e198be61634bd02ee008 . Both full source downloads matched the recorded sizes and SHA-256 checksums before selecting this record and its prior report.
- problems.json: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- research_results.json: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. The relevant report is keyed by AMR-022-5070. It records source/web triage without a proof and leaves the unbranched example unresolved. The imported report is treated as an untrusted research aid.
- At the read snapshot main=df9f2c05f61cad48f851c2d2ba7a63611a0acfa0, the live queue row was queued 0/5. The per-ID attempt directory returned 404; a repository PR search for 2305070 returned no matches; state.json contained no entry for this ID; related_target_groups.json contained no group listing it. These checks do not exclude differently named prior material.
- The public report omits source PDFs, the statement/report corpus, and unrelated queue data.

## Acceptance test and present result

A successful positive resolution needs one bounded nonconstant analytic function, a fixed positive modulus, proof of maximal component membership, a divergence argument for that component's Euclidean length, and exclusion of branch points on it. A negative resolution must cover all such functions and components. Neither test is met. The correct result of this attempt is **unsolved**, with five substantive approaches and proved auxiliary controls.
