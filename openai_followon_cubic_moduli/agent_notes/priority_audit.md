# Independent priority and terminology audit

Checkpoint: 2026-10-06 22:14:15 PDT. Assigned priority-audit completion: 98%; mathematical validation of the upstream gap theorem: not performed in this audit; publication novelty clearance: **failed for a new-resolution claim**. No external individual was contacted. The upstream clone remained read-only.

## Decisive finding

The exact proposed conclusion in every dimension at least five is already covered by a publicly accessible manuscript, **Bochao Kong, Yu Shen, Junyan Zhao, and Minghao Zhao, _K-moduli of cubic hypersurfaces_**. Its dated manuscript is September 30, 2026; the publicly linked PDF was independently fetched during this audit on October 6, 2026 PDT. The actual earliest posting time has not been established. A manuscript date and PDF creation time do not establish public priority. Current public access, however, establishes that the result is already disclosed before any proposed deposit from this project.

- [Primary author research page](https://sites.google.com/uic.edu/jzhao/research).
- [Public manuscript PDF](https://drive.google.com/file/d/1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO/view?usp=sharing).
- Local audit copy: `references/Kong_Shen_Zhao_Zhao_cubic_kstable.pdf`, 403,695 bytes, 15 pages, SHA256 `6813e3d3be36c087e60b696f40652f8a837da7fcd9e3bdbd7af7df030c3ad65e`.
- Text extraction: `references/Kong_Shen_Zhao_Zhao_cubic_kstable.txt`.
- Retrieval evidence: `references/priority_web_retrieval_receipt.json`, and saved primary author-page HTML files. These are research evidence, not redistributable publication payloads absent an applicable license.

Theorem 1.1 on page 2 states that every K-semistable Fano variety in the cubic smoothing component is itself a cubic hypersurface in projective space. It states equivalence of K and GIT semistability/polystability/stability, a natural isomorphism of their quotient stacks and good moduli spaces, and smoothness/connected-component structure of the cubic K-moduli stack. The component is specified by intrinsic dimension n, volume 3(n-1)^n, and a Q-Gorenstein deformation to a smooth cubic in P^(n+1). This exceeds the proposed closed-point/topological target. Corollary 1.2 states K-stability for nodal cubics and KE existence for smooth cubics.

The proof mechanism is different from the proposed unrestricted-gap route: refined local normalized-volume and threshold estimates, the limiting linear system |L|, slope semistability of the tangent sheaf, and the classification of varieties of minimal degree. Theorem 4.1 on pages 11–12 proves that K-semistable cubic-family limits remain cubics; the final comparison on page 13 explicitly refers to the established Liu–Xu/Liu moduli argument. I read the exact main statements, definitions of the component, proof sketch, relevant final proof, and bibliography; I have **not** independently verified every intermediate inequality in this competing paper. Its availability is a priority conflict independently of whether a full mathematical audit ultimately accepts it.

The [authors' AI disclosure](https://sites.google.com/uic.edu/jzhao/ai-disclosure) reports the arbitrary-dimensional result and an independent GPT-assisted development. The downloaded paper specifically names **Zhiyuan Li, Long Pan, and Haoyu Wu** for that independent development; the web disclosure currently names Pan and Wu. I did not locate an independently accessible Li–Pan–Wu cubic manuscript in the searches below, so this is a disclosed parallel development, not a second independently inspected proof.

Fresh direct retrieval of the author research page lists “K-moduli of cubic hypersurfaces”; the search engine's older indexed excerpt instead lists “K-moduli of cubic fivefolds.” This is a concrete warning against relying on cached snippets or the previous triage's search results.

## Consequence for this project's novelty

The exact moduli target is not presently an unclaimed new theorem. If the unrestricted upstream gap is correct, the requested Spotti–Sun argument is an immediate newly available consequence of that gap plus a transfer already public since 2017. It could be useful exposition or an alternative deduction, but it cannot be advertised as the first solution or as completing a presently unresolved n>=5 moduli case. The distinct proof ingredients of the competing manuscript do not establish novelty of our composition of already public inputs.

No additional theorem within the specified compactification scope has been identified here that escapes this overlap. Stronger scheme, stack, functor, stability, or nodal-existence claims are also explicitly in the competing main statements. A genuinely new in-scope extension would need its own mathematical and priority audit; merely adding these upgrades does not cure duplication. The user prohibits duplicate preprints advertised as a new solution. Recommend retaining an internal consequence note and withholding a new-resolution deposit unless a separately justified contribution emerges.

## Exact lower-dimensional background and established transfer

| Source | Public dates/version checked | Exact relevant scope |
|---|---|---|
| [Odaka–Spotti–Sun, Compact Moduli Spaces of Del Pezzo Surfaces and Kähler–Einstein metrics](https://arxiv.org/abs/1210.0858) | v1 Oct 2 2012; v3 Mar 10 2015; inspected v3 Theorem 1.1 and Section 4.2 | Theorem 1.1 gives the GH/algebraic compactification homeomorphism; Section 4.2 identifies degree-three case with cubic-surface GIT. Cubic curves are outside this positive-KE Fano discussion. |
| [Liu–Xu, K-stability of cubic threefolds](https://arxiv.org/abs/1706.01933) | v1 Jun 6 2017; v3 Jan 26 2019; Duke Math. J. 168 (2019), 2029–2073 | Cubic threefold K/GIT comparison, with unrestricted three-dimensional volume bounds as main input. |
| [Liu, K-stability of cubic fourfolds](https://arxiv.org/abs/2007.14320) | v1 Jul 28 2020; v2 Jan 10 2022; J. Reine Angew. Math. 786 (2022), 55–77 | Theorem 1.1 states K-(semi/poly)stable iff GIT-(semi/poly)stable for cubics in P^5, and isomorphism of the smoothable K-polystable good space with GIT. Theorem 1.3 proves unrestricted-dimensional lci ODP gap, not arbitrary klt ODP gap. Its higher-dimensional introduction already identifies Cartierness of the limiting hyperplane divisor as the remaining moduli step. |
| [Spotti–Sun, Explicit Gromov–Hausdorff compactifications of moduli spaces of Kähler–Einstein Fano manifolds](https://arxiv.org/abs/1705.00377) | v1 Apr 30 2017; only public arXiv version listed; exact Theorem 1.3(2), Sections 5.1–5.2 inspected | Theorem 1.3(2) states the cubic KE/K-GIT identification conditionally on metric ODP gaps in every required dimension k<=n. This transfer belongs to Spotti–Sun, not this project. |

The dates printed by current experimental arXiv HTML as “August 24, 2026” in some old manuscripts appear to be renderer-generated document dates. Their authoritative submission histories are the arXiv abstract/version pages and are used above.

## Recent cubic boundary singularity theorem

[Sung Gi Park, _The GIT stability and Hodge structures of hypersurfaces via minimal exponent_](https://arxiv.org/abs/2510.14352), v1 public October 16, 2025 (only listed version), has an exact Theorem B: for a GIT-semistable cubic X in ambient P^N, N>=3, its minimal exponent is at least max{4/3,(N+1)/9}; if N>=6 it is at least 5/3 and X has terminal singularities. Thus **all intrinsic cubic n-folds with n>=5 that are GIT semistable already have terminal singularities** in this public result. Canonical singularities are asserted in all relevant lower dimensions as well. Its Theorem A gives the general sufficient GIT-stability criterion via minimal exponent. This resolves Spotti–Sun Question 5.8, rather than the complete K/GIT comparison by itself. Do not claim canonical or terminal boundary structure as a new corollary of our note. Ambient dimension N is one greater than this project's intrinsic n.

## Modern smoothable K-moduli terminology

The K-moduli **stack** parametrizes K-semistable Q-Fano varieties/families with the appropriate Kollár condition. The associated projective **good moduli space** has closed complex points corresponding to isomorphism classes of K-polystable representatives; semistable objects with a common polystable degeneration determine the same point. “Coarse space of polystable limits” should be explained in this sense, since nontrivial stabilizers remain and the K-semistable stack is not itself a set of polystable objects.

Relevant primary foundations: [Li–Wang–Xu](https://arxiv.org/abs/1411.0761), v1 Nov 4 2014, v4 Jan 7 2019, Theorems 1.1(iii) and 1.3; [Xu–Zhuang](https://arxiv.org/abs/1912.12961), v1 Dec 30 2019, v3 Aug 31 2020, Corollary 1.2. The first provides the smoothable KE/GH correspondence and a proper good moduli construction; the second provides projectivity/ample CM polarization for the smoothable K-polystable space. The competing 2026 manuscript's Theorem 2.4 states the modern general projective good-space formulation and cites the later foundational K-moduli corpus.

Specify the cubic smoothing locus/closure, not all n-dimensional K-polystable Fanos of anticanonical volume 3(n-1)^n. Equal dimension and volume alone do not define the required deformation family. A homeomorphism of complex points to GIT with its analytic topology does not establish an isomorphism of schemes/stacks or a statement about every nonclosed semistable orbit. The proposed publication scope expressly disallows silently making those upgrades.

There is also a metric-topology qualification: the KE moduli in Spotti–Sun is defined by biholomorphic isometry classes, in the complex/polarized GH setting. The bare metric-space GH quotient loses the complex structure: a cubic and its complex conjugate carry isometric underlying Riemannian metrics. Any precise statement must retain the complex/polarized moduli information or explain the relevant topology rather than claiming an injective map from unadorned metric spaces to arbitrary complex GIT points.

## Upstream and companion duplication audit

Pinned/read-only clone: `/Users/alec/Desktop/math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. A read-only remote `ls-remote` returned the same current main commit. The local log gives initial-commit author timestamp October 6, 2026 14:58:50 PDT; this alone does not certify when the repository first became public.

The source catalogue's family 037 contains exactly the all-dimensional gap manuscript and its fourfold companion. I read their README citation information, exact main statements, introductions, conclusion scope, and principal bibliography entries. Focused corpus-wide text searches covered all `.tex`, `.md`, `.bib`, and `.json` files in the clone, including the catalogue and overview. Searches for cubic/GIT/K-moduli/Spotti–Sun identifiers found no explicit cubic compactification theorem in family 037 or elsewhere in that corpus. Hits in the irrational-cubic-fourfold/K3-category manuscript concern a different rationality problem; the Pixton compactification references concern curves. A later uniform-Cartier-sections manuscript cites the upstream gap in its bibliography, but no cubic identification was found there. This does not prove global novelty and does not negate the decisive external duplication.

Source SHA256 values:

- all-dimensional `paper.pdf`: `5e2cdac4857afef7065967c49c6f4f9a1aec01b0b776ce324220707545e8e114`;
- all-dimensional introduction: `508d1b624f4cff3ea2317ee0822aa4f6e8650c9c1741650c21940850e171a31a`;
- fourfold-companion `paper.pdf`: `6d58101115e4bf4f963ea2bc4e301f041eaff601e3b325ec475200e43e3031a4`;
- fourfold-companion `build/paper.tex`: `2e1eb5a05a308182d34d75eb428474fbe11cce86445cb01bc4e654e9a5e25390`.

Use the repository-supplied manuscript-specific BibTeX author **OpenAI** and title _The ordinary-double-point gap in every dimension_, with its exact GitHub manuscript URL. The mathematical innovation claimed by that upstream source is its unrestricted ODP gap proof. The algebraic-to-metric minimization machinery is Li–Liu/Li–Xu and the global moduli transfer is Spotti–Sun. Our current proposed text supplies no new gap proof or transfer mechanism. No family-037 Lean scope file at `lean/docs/037.md` was found; I make no formal-verification claim.

## Search record and limits

All searches occurred October 6, 2026 PDT. Query families included:

- `cubic hypersurfaces K-moduli GIT fivefold Spotti Sun volume gap`;
- `cubic hypersurfaces semistable singularities K-stability 2025 2026`;
- `cubic n-fold Kähler Einstein GIT compactification dimensions`;
- `"cubic" "K-moduli" "2026" fivefold`;
- `"cubic hypersurfaces" "K-stability" "2025" "2026"`;
- `"ordinary-double-point gap" OpenAI cubic moduli`;
- `"K-moduli of cubic fivefolds"`;
- `"cubic fivefolds" "K-polystable"`;
- `"K-moduli of cubic hypersurfaces"`;
- `"cubic" "Kong" "Shen" "Zhao" K-moduli`;
- `"cubic hypersurfaces" "Li" "Pan" "Wu" "K-moduli"`;
- `"K-moduli" "cubic" "Long Pan"` and `"K-moduli" "cubic" "Haoyu Wu"`.

Broad searches did not initially return the current arbitrary-dimensional PDF. The current author-site primary PDF, reached through a fivefold keyword result, overturned the previous triage. Several narrow title/author searches still returned unrelated older material. These failures have no evidentiary force for novelty. Direct inspection of current primary manuscripts and author-page links was decisive. No inference of being first, no precise ordering between unpublished/undated web postings, and no outreach is warranted from this audit.

## Strongest verified outcome and remaining gap

Verified priority outcome: a presently public exact stronger cubic K/GIT theorem exists, with a checkable downloadable artifact and specific main statements. Remaining priority gap: earliest public posting date and independent full-proof certification of that competing paper were not determined. Neither uncertainty permits a first-solution claim. Remaining mathematical gap for this project's own route is the independent validation of the unreviewed upstream unrestricted gap; this audit does not resolve it. Publication package is not novelty-cleared on the present target.
