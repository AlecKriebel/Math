# Independent source and convention referee report

Checkpoint: 2026-09-21 21:07 PDT. Scoped source/convention audit: **100% complete**. This percentage concerns this bounded audit, not an exhaustive priority certification or the overall mathematical verification.

## Verdict and required editorial change

The manuscript addresses the invariant and Boolean meet-semilattice question actually attributed to P. J. Cameron as Kourovka Notebook Problem 16.45. There is no convention mismatch involving nonfaithful actions. The September 2026 official notebook still lists the problem without a solution comment. This supports a carefully dated statement about the checked sources, not an unrestricted claim to priority.

The important missing reference is Cameron's **published 2024 account**, which explicitly restates the question as unknown. Add it to the introduction and bibliography. Existing 2010/2014 titles, dates and arXiv identification are correct. The 2014 item should remain identified as a preprint; the published 2024 article has a different title and is not simply a journal version under the old title.

## Primary-source checks

1. **Official notebook.** [Official site](https://kourovkanotebookorg.wordpress.com/) presents its latest update as 1 September 2026. The [full 21st edition](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf) places Problem 16.45 on printed page 100 (PDF page 100, one-based), in the 16th Issue (2006) section. It attributes the question to P. J. Cameron, maximizes inclusion-minimal base size over all permutation representations, asks equality with maximal independent-set size, and gives the equivalent normal-bottom Boolean meet-semilattice question. No solution comment follows. Searching extracted text gives one numbered occurrence in the full volume; the [separate update](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf) gives none. These are direct document checks, not conclusions from search snippets.

2. **2014 preprint.** Peter J. Cameron, *Some measures of finite groups related to permutation bases*, arXiv:1408.0968v1, submitted 5 August 2014; [record](https://arxiv.org/abs/1408.0968), [PDF](https://arxiv.org/pdf/1408.0968), DOI [10.48550/arXiv.1408.0968](https://doi.org/10.48550/arXiv.1408.0968). Section 2, printed page 3, expressly permits nonfaithful representations. Proposition 3.2(b), printed page 6, identifies the Boolean bottom with the action kernel. Propositions 3.1–3.2 and Corollary 3.3 establish the characterizations and inequality used in the manuscript; the following paragraph asks whether strict inequality occurs. Its notation is b_2 and mu-prime. The preprint itself says the work predates submission by more than ten years; do not describe 2014 as the first date of the question.

3. **Published 2024 source — add to manuscript.** Peter J. Cameron, *Independence and bases: theme and variations*, **Model Theory 3** (2024), no. 2, 417–431, DOI [10.2140/mt.2024.3.417](https://doi.org/10.2140/mt.2024.3.417); [publisher PDF](https://msp.org/mt/2024/3-2/mt-v3-n2-p08-s.pdf). Section 7, printed pages 428–429, defines b_2 using nonfaithful representations too, states the relevant characterizations as Proposition 2(a)–(c), and says after its proof that necessity of the normal-bottom condition remains unknown. The independent-set invariant is written mu with an upward arrow, not mu-prime. The DOI includes **3.417**; the author's publications page has a malformed variant missing that dot, so use the publisher DOI. This is a published primary reaffirmation as of 2024, not a proof of status in all subsequent literature.

4. **Author's expositions.** [The symmetric group, 7](https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/), 22 July 2010, explicitly allows representations that are neither faithful nor transitive. It uses b_2 and mu-star; its mu concerns independent generating sets for the whole group. [Groups, lattices and bases](https://cameroncounts.wordpress.com/2014/08/06/groups-lattices-and-bases/), 6 August 2014, restates the question and proposes computation. These confirm attribution and conventions but are secondary to the notebook for problem numbering.

5. **Later related paper with a different convention.** Marina Anagnostopoulou-Merkouri and Timothy C. Burness, *On the regularity number of a finite group and other base-related invariants*, [arXiv:2405.15300v2](https://arxiv.org/abs/2405.15300), 27 October 2024; [journal DOI](https://doi.org/10.1112/jlms.70035). Remark 1(c) defines its b_2 over **faithful** representations only. Thus its b_2 is the manuscript's b_f, not the manuscript's all-actions b. The paper concerns regularity and related base invariants and does not supply a resolution of the specific all-actions equality checked here. Do not import its notation without qualification.

## Independent equivalence check

This part is an independent mathematical deduction, not a quotation from a source.

For an action rho: X -> Sym(Omega), the permutation image is the group to which the base definition applies. Pulling the identity stabilizer back to X gives ker(rho). Requiring identity in X while simultaneously admitting nonfaithful rho would exclude those actions and conflict with Cameron's explicit kernel statement. The manuscript correctly avoids that error.

Let L_1,...,L_t be point stabilizers of a minimal base. Their total intersection is the normal kernel N; deleting any member strictly enlarges the intersection. Conversely, let such an irredundant subgroup family have normal total intersection N. In the disjoint union of X/L_i, the kernel is the intersection of the cores, which equals Core_X(N)=N. The identity cosets give a minimal base. Normality is essential in this converse.

For any irredundant subgroup family, choose x_i lying in every L_j for j != i, but not in L_i. Then x_i is outside the subgroup generated by all the other chosen elements. Conversely, the omission-generated subgroups of an independent t-set are meet-irredundant, since each omitted generator witnesses essentiality. Hence unrestricted maximal meet rank equals maximal independent-set size.

The manuscript's map A -> intersection of L_i for i outside A preserves intersections, maps the full index set to X, and is injective: if i is in A but not B, x_i belongs to the image of A but not B. Its bottom is the total subgroup intersection. These facts establish exactly a top-preserving Boolean meet embedding; they do not imply preservation of joins. The analogous normal-bottom maximum is precisely the all-actions base invariant. Therefore, if the other referees verify b(G)=3 and mu-prime(G)=4, that strict inequality answers the notebook question negatively.

Boundary cases check correctly: the empty intersection is X; the trivial action's empty minimal base has size zero; repeated points cannot occur in a minimal base; a finite group acting on an infinite set still admits finite subbases. No transitivity or maximal-point-stabilizer assumption is licensed by the original question.

## Search scope and bounded priority conclusion

Focused searches used the exact problem number with Kourovka/Cameron, the 2014 title, maximal minimal bases and independent sets, Boolean embeddings with normal bottom, the explicit order 100920, and SL(2,5) in conjunction with base invariants. The searches identified the additional 2024 published account and the related faithful-convention paper above; they did not identify an earlier counterexample. Number/order searches also returned irrelevant pages, which were discarded.

Suggested manuscript wording: “Cameron's published account in 2024 still states this question as open, and the September 2026 update of the Kourovka Notebook records Problem 16.45 without a solution comment. We give a counterexample.” A claim that no earlier resolution exists anywhere would go beyond this audit. No outreach was made or prepared.

## Reproducibility of source inspection

Sources were downloaded directly from the linked primary hosts and inspected through PDF text extraction. Full third-party PDFs and extracted text are local working material in ignored `tmp/primary_sources/`; they should not be redistributed in the research release. Browser PDF fetches for the notebook failed, but direct HTTPS downloads succeeded. The following SHA-256 values identify the actual files inspected.

- `21tkt.pdf` (1769460 bytes): `2fcce9b98a4df10267fe120229217bfe556c70510704e311540da0cef438f911`
- `21upd.pdf` (293230 bytes): `6dd201b3ae6673b0a053bf8b7d4e3aa8ab54025f19ebf1d8e5e33ca0b838dc0b`
- `cameron2014.pdf` (84079 bytes): `f65c1b2ac82e4c5a6813297d0f39fae49304f7bcbc3d180d9e3926a9307836c5`
- `cameron2024.pdf` (361494 bytes): `94ba37fc539f64f83481b255373c115f078cea0d6accaabeb0f4a4138662f12f`
- `regularity.pdf` (617478 bytes): `ada14c4420f6dda8ec892269546ae25ea9806088e88fc7470b1cb98da00445e7`
