# Acquisition and scope review — Zenodo 23127955

**Disposition: PASS_SCOPE_ONLY.** The exact publication, its included reader documents, the claimed theorem, its external theorem interfaces and a restrained page-content candidate have been identified. This is not a mathematical PASS, a promotion authorization, a human peer review or a novelty certificate. The independent analytic and adversarial reviews are separate. No sibling conclusions were consulted.

## Edition and immutable material

The selected record is [Zenodo 23127955](https://zenodo.org/records/23127955), DOI **10.5281/zenodo.23127955**, concept record 23127954. Fresh public metadata gives title *The spatial locus of common tangents to three disjoint convex sets is null*, author Alec Kriebel, ORCID 0009-0001-9320-500X, publication date **2026-10-03**, and version **1.0**. The manuscript prints **3 October 2026** and **Unrefereed preprint**; it does not print a separate numbered edition. Do not turn the archive version into “1.0.0.” The public license is CC BY 4.0.

Both public assets were freshly acquired from the Zenodo API. Byte counts and MD5 agree with the public record and queued expected values; the queued PDF SHA-256 also agrees. The SHA-256 bindings are:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `common_tangent_nullness.pdf` | 92,307 | `80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327` |
| `common_tangents_null_locus_v1.zip` | 182,613 | `1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5` |

`sources/receipt.json` binds the raw metadata, URLs, timestamps, asset hashes and all extracted members. ZIP CRCs were checked before extraction. Absolute/traversal paths, duplicate names, symlinks and special nodes were rejected, with bounded member counts and expanded sizes. There are **15 regular archive members**. The internal manifest independently matches the exact 14-file set it covers, with matching byte sizes and SHA-256 values; it does not list itself.

There is **one unique reader PDF, eight pages**. It occurs once as the standalone download and once, byte-identically, in the ZIP. There is no separate reader supplement PDF and no nested archive. All eight published pages were read as full extracted PDF text, including the proof, boundary examples, disclosure and references, and compared with the complete corresponding TeX. The complete mathematical support `source/CANDIDATE.md` and complete `verify.py` were also read. PDF text extraction drops some overbars and mathematical glyphs, so the actual TeX resolves those expressions; for example the compact cap on manuscript page 2 is `closure(K_i) intersect B_i`, not `K_i intersect B_i`.

## Exact claim and reader-facing scope

For any three pairwise disjoint convex subsets of **ℝ³**, collect the **complete affine lines** that are tangent to all three. A line is tangent only if it **actually meets** a set and is contained in a plane bounding a closed halfspace containing that set. The claimed conclusion is **three-dimensional Lebesgue outer measure zero of the spatial union of those lines**. It is not a measure claim about the four-dimensional space whose points represent lines.

The statement permits nonclosed, unbounded, nonsmooth and lower-dimensional convex sets. An empty input gives an empty tangent locus. There is no generic-position, positive-volume, strict-convexity, unique-contact or unique-support-plane assumption. Contact may be a segment. Pairwise disjointness concerns the original sets, and their closures may intersect. The actual-contact requirement cannot be replaced by contact with the closure.

The distinction worth explaining is **two contacts versus three**. The published two-rectangle example on page 7 has a two-parameter common-tangent family sweeping a region of volume 2/3 between their planes. For three disjoint sets, the proof obtains three distinct roots of a determinant of degree at most two. This gives an understandable reason the third contact is consequential. That example was read in the paper and code, not freshly executed by this scope reviewer.

The following stronger claims must not appear in the page:

- A countable cover by 2-manifolds, a Hausdorff-dimension bound of two, 2-rectifiability or a smooth-surface description. Those do not follow merely from volume zero.
- Closedness of the tangent locus for arbitrary nonclosed inputs. Page 7 gives an explicit counterexample to that extension; closedness is used only after compact localization.
- A finite number of tangent lines, an enumeration algorithm, higher-dimensional analogues, or claims about ordinary secants through the interiors.
- First-proof priority, exhaustive literature coverage or present-day openness inferred from a 2008 or archived historical question.
- Human peer review, or treating finite computational checks as an oracle for the universal convex-geometry and measure-theory proof.

## Proof map and interfaces to preserve

The following is a dependency map, not an independent proof verdict.

| Published location | Mechanism and required scope |
|---|---|
| Pages 1–2, §1; TeX lines 29–49 | Theorem 1, supporting tangency, outer measure, density/Rademacher/area inputs. The area formula is used on measurable subsets and does not require injectivity. |
| Page 2, §2; TeX lines 51–89 | A fixed countable rational-ball collection in the original coordinates localizes actual distinct contacts to disjoint compact caps of the closures. The support gap is Lipschitz without differentiable support functions. |
| Pages 3–5, §3; TeX lines 91–164 | For two compact sets of affine dimension at least two, exclude lines contained in a planar affine hull. Local contact caps, normal hemispheres, strict monotonicity, cross estimates and explicit root brackets give a contraction on a closed square and a Lipschitz graph on an open two-parameter domain. Countability is organized by fixed rational cap pairs. |
| Pages 5–6, §4; TeX lines 166–227 | Compact tangency gives a Borel selected parameter set. Density and differentiability hold almost everywhere, not at every tangent parameter. Four affine-dimension cases give rank restrictions at contacts. Three distinct contact heights annihilate the quadratic determinant; bounded patches and the area formula make the swept images null. |
| Page 7, §5; TeX lines 229–238 | Cases with a point or two intervals provide separate line-family parametrizations, with open domains even at interval endpoints. Discarded lines/planes are null; countable unions finish the compact and arbitrary-set reductions. |
| Pages 7–8, §6; TeX lines 240–255 | Controls delimit two contacts, repeated contacts, density, supporting tangency and closedness. AI assistance and lack of external human peer review are explicit. |

No uniform lower bound on contact separation, angular margins or chart size is claimed. The proof uses local quantitative constants and countably many charts. The maps may contain extra lines; the Borel tangent subset selects the relevant ones. No injective parametrization or open set of tritangent parameters is assumed.

## Fresh primary-source checks

The locally saved originals and retrieval hashes are recorded in `primary-source-receipts.json`. The relevant statements, rather than historical audit claims, were inspected directly.

**Goaoc, original problem.** [Official Oberwolfach Report 44/2008](https://ems.press/content/serial-article-files/46191), physical PDF page 76, printed page **2552**, section 13, was read in full. Its tangency convention agrees with actual intersection plus a containing supporting plane. Its S(A,B,C) is the union in physical space of the complete common tangent lines. Conjecture 4 asks for containment in a measure-zero set for pairwise disjoint convex sets, without compactness or full-dimensional qualifications in that statement. Conjecture 3 separately asks for a countable union of 2-manifolds. The paper accurately targets Conjecture 4. The original paragraph’s general closedness assertion is not transferred to nonclosed inputs; the new manuscript itself flags the failure. This source establishes historical attribution, not current priority.

**Simon, exact analytic interfaces.** [The author-hosted NTU notes](https://math.stanford.edu/~lms/ntu-gmt-text.pdf) were checked at chapter 1 Corollary 3.10, printed page **18** (physical page 13); chapter 2 Theorem 1.4, printed page **45** (physical page 26); and chapter 2 Theorem 3.3 plus Remark 3.4, printed pages **57–58** (physical pages 32–33). The PDF prints two book pages per physical page. These are the theorem-statement and interface checks, not a new proof of Simon’s results:

- Density is for Lebesgue-measurable sets, with density one almost everywhere on the set. The manuscript applies it to a Borel subset of its parameter domain.
- The displayed Rademacher theorem is scalar, globally Lipschitz on ℝⁿ. The vector-valued, open-domain version needed here follows componentwise after local Lipschitz extension and a countable localization. It does not require an open set of selected tangent parameters.
- The area formula assumes an open domain, local Lipschitz regularity, domain dimension at most target dimension, and a Lebesgue-measurable subset. It counts preimages with multiplicity; injectivity is needed only for the simplified equality with the image measure. Remark 3.4 includes measurability of that multiplicity. For domain and target dimension three, its Jacobian is the absolute determinant, so the paper’s upper bound on image outer measure is the applicable consequence. It is not relying on a C¹-only version of Sard’s theorem.

The additional Federer and Evans–Gariepy references were not acquired or independently checked. They are alternative background references; the required interfaces were available in Simon. No access limitation is concealed by citing those books as if read.

**Demouth–Goaoc historical compact question.** The [official-author-host archived manuscript](https://web.archive.org/web/20110401122240id_/http://www.loria.fr/~goaoc/papers/TopVE.pdf), section 7, printed page **11**, was read for its compact-convex nullness question and the distinction from nowhere density. The 1 April 2011 date is the capture date. It is not asserted to be the publication date or to identify the manuscript version cited in September 2008. This is historical context, not a load-bearing theorem for the new proof.

**Cheong–Goaoc–Holmsen context.** The [publisher preview](https://link.springer.com/article/10.1007/s00454-023-00573-2) confirms the title, authors, online date 16 November 2023 and journal citation 72 (2024), 674–703. The full journal article was not obtained. The accessible, pinned [author preprint v2](https://arxiv.org/abs/2205.14681v2), dated 5 September 2024, was read on pages 1–2 for its definitions, Theorem 1 and context: it concerns line transversals meeting **open** disjoint convex sets and acyclicity of their connected components in line space. Its abstract uses the stronger word “contractible”; the candidate describes the displayed theorem’s acyclicity formulation. No claim about that stronger wording is needed here. Its topic and hypotheses do not supply the claimed spatial-nullness result. Neither this preprint’s proof nor the full journal article has been independently audited for this scope task.

The fresh literature inspection is deliberately bounded to these sources and exact interfaces. It cannot exclude every earlier proof or certify novelty.

## Included code, provenance and independence

The full `verify.py` was read to map its scope. It contains formal polynomial coefficient identities, rational motion-basis determinants, support-increment controls, root-bracket/contraction diagnostics, finite nonsmooth models and boundary countercontrols. It uses the standard library, explicitly rejects optimized execution, includes an intentionally failing mode, and writes `verification.json` when run. **It was not executed by this scope reviewer**, and no old `verification.json` outputs were adopted. Acquisition, CRCs, cryptographic hashes, manifest matching, PDF inventory and editorial consistency checks are the fresh executions reported here. Their success is not mathematical proof validation.

Dedicated historical/status files such as `PROVENANCE.md`, `README.md`, `primary_source_scope.json` and `verification.json` were not read for opinions. Hashing all archive bytes and reading the structural manifest does not adopt their contents. The necessary mathematical support `source/CANDIDATE.md` was read in full and incidentally exposes historical status/audit/priority language at its header and final literature discussion; `paper.tex` itself also mentions a previous bounded literature audit. `verify.py` contains a comment about a discarded 5/8 estimate. These statements are disclosed as incidental exposure and were not treated as current independent evidence. No neighboring archived audits or current sibling review reports were read.

Raw primary-source URLs, paths and hashes were shared with the independent mathematical reviewers, without sending this reviewer’s interpretation or reading their opinions. Source files and published bytes remain unchanged.

## Candidate and remaining gates

`content.json` is an **unpromoted editorial candidate**. It preserves the complete original abstract, with only TeX-to-Unicode formatting and paragraph breaks; gives the supporting-plane definition; explains the two-versus-three distinction; and separates exact scope, standard analytic inputs, prior attribution and limits. It includes both published downloads, clear unrefereed/AI status and a professional invitation for substantive mathematical collaboration. No individual is contacted and no outreach message is prepared.

`follow_up` is **null**. The stronger manifold question is an important existing problem, but this scope review identifies no new mechanism providing the required regularity. It belongs in the limits and historical context, not an invented follow-up section.

The analytic/adversarial mathematical gates, root disposition and any later promotion remain outside this scope verdict. No `publication.json`, `promotion.json`, website files, spreadsheet entries, Git state, Zenodo assets or public records were changed. The author-facing page must not replay this internal acquisition and checking history.

The timestamped log and final hash-bound verdict record completion of the acquisition/scope assignment, not completion of all review or publication work.
